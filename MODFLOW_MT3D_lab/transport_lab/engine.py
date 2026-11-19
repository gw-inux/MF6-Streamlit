"""FloPy inputs, native engine execution and validation of the results.

Each request owns its working directory. Only the arrays and diagnostics needed
by the app leave this directory. Timings cover the two native processes separately.
"""
from dataclasses import dataclass
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
from tempfile import TemporaryDirectory
from time import perf_counter

import flopy
from flopy.utils.binaryfile import BudgetIndexError
import numpy as np

from .analytical import final_errors
from .scenario import DARCY_FLUX, END_TIME, K, LEFT_HEAD, METHODS, POROSITY, Scenario

ROOT = Path(__file__).resolve().parents[1]
EXECUTABLE_NAMES = {
    "flow": ("mf2005_MT3D", "mf2005", "MODFLOW-2005_64", "MODFLOW2005", "MODFLOW-2005"),
    "transport": ("mt3dms5b", "mt3dms", "MT3DMS_64", "MT3DMS5", "MT3DMS"),
}


class RunError(RuntimeError):
    """A native engine or its output could not support a complete model result."""


def _available_executable(path):
    """Restore the owner execute bit for binaries uploaded through the GitHub UI."""
    try:
        if not path.is_file():
            return False
        if os.name != "nt":
            with path.open("rb") as binary:
                if binary.read(2) == b"MZ":
                    return False  # Windows executables cannot run on a Linux host.
            if not os.access(path, os.X_OK):
                path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return os.access(path, os.X_OK)
    except OSError:
        return False


def find_engines(root=ROOT):
    """Prefer the configured common folder, then app and sibling shared folders."""
    configured = os.getenv("TRANSPORT_LAB_BIN")
    folders = [Path(configured).expanduser()] if configured else []
    folders += [root / "bin", root.parent / "bin", root / "common", root.parent / "common",
                root / "common" / "bin", root.parent / "common" / "bin", root]
    extensions = (".exe", "") if os.name == "nt" else ("",)
    engines = {}
    for kind, aliases in EXECUTABLE_NAMES.items():
        names = [alias + ext for alias in aliases for ext in extensions]
        # Windows name matching is already case-insensitive on the usual filesystem.
        for folder in folders:
            match = next((folder / name for name in names
                          if _available_executable(folder / name)), None)
            if match is not None:
                engines[kind] = str(match.resolve())
                break
        else:
            engines[kind] = next((path for name in names if (path := shutil.which(name))), None)
    return engines


def write_models(case, workdir, engines):
    """Left and right hydraulic heads are imposed at the benchmark end centres."""
    flow = flopy.modflow.Modflow("flow", model_ws=str(workdir), exe_name=engines["flow"])
    nper = len(case.periods)
    flopy.modflow.ModflowDis(flow, nlay=1, nrow=1, ncol=case.ncol, delr=case.dx, delc=1.0,
                             top=0.0, botm=-1.0, perlen=list(case.periods), nper=nper,
                             nstp=1, steady=True, itmuni=4, lenuni=2)
    ibound = np.ones((1, 1, case.ncol), dtype=np.int32)
    ibound[0, 0, [0, -1]] = -1
    head = np.linspace(LEFT_HEAD, 0.0, case.ncol).reshape(ibound.shape)
    flopy.modflow.ModflowBas(flow, ibound=ibound, strt=head)
    flopy.modflow.ModflowLpf(flow, laytyp=0, hk=K, ipakcb=53)
    flopy.modflow.ModflowPcg(flow, hclose=1.0e-6, rclose=1.0e-6)
    flopy.modflow.ModflowOc(flow, stress_period_data={
        (p, 0): ["save budget", "print budget"] for p in range(nper)}, compact=True)
    flopy.modflow.ModflowLmt(flow, output_file_name="transport.ftl")
    flow.write_input()

    mt = flopy.mt3d.Mt3dms("transport", modflowmodel=flow, model_ws=str(workdir),
                            ftlfilename="transport.ftl", exe_name=engines["transport"])
    icbund = np.ones_like(ibound)
    icbund[0, 0, 0] = -1
    initial = np.zeros_like(head)
    initial[0, 0, 0] = case.height
    flopy.mt3d.Mt3dBtn(mt, prsity=POROSITY, icbund=icbund, sconc=initial,
                        tunit="D", lunit="M", munit="G", nprs=-1, savucn=True,
                        chkmas=True, nprmas=1, dt0=list(case.step_limits),
                        ttsmax=list(case.step_limits), ttsmult=1.0, mxstrn=50000)
    mixelm, nadvfd = METHODS[case.method]
    flopy.mt3d.Mt3dAdv(mt, mixelm=mixelm, nadvfd=nadvfd, percel=case.courant,
                        mxpart=max(5000, 24 * case.ncol), nplane=1, npl=0, nph=4,
                        npmin=0, npmax=8, nlsink=1, npsink=4, dceps=1e-5)
    flopy.mt3d.Mt3dDsp(mt, al=case.dispersivity, dmcoef=case.diffusion, trpt=0.0, trpv=0.0)
    # ITYPE=-1 gives a time-varying specified concentration at the first node.
    # The right CHD discharges water at resident concentration. It is not a C=0 node.
    source = {p: [(0, 0, 0, case.height if p == 0 else 0.0, -1)] for p in range(nper)}
    flopy.mt3d.Mt3dSsm(mt, stress_period_data=source)
    flopy.mt3d.Mt3dGcg(mt, mxiter=1, iter1=100, isolve=3, cclose=1e-7)
    mt.write_input()


def _tail(path, limit=4500):
    if not path.is_file():
        return ""
    with path.open("rb") as stream:
        stream.seek(0, 2)
        stream.seek(max(0, stream.tell() - limit))
        return stream.read().decode("utf-8", errors="replace")


def _execute(exe, model, folder, timeout):
    console = folder / f"{model}.log"
    detail = folder / f"{model}.list"
    start = perf_counter()
    try:
        with console.open("wb") as output:
            process = subprocess.run([str(exe), f"{model}.nam"], cwd=folder, stdin=subprocess.DEVNULL,
                                     stdout=output, stderr=subprocess.STDOUT, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RunError(f"{model}: {exc}\n{_tail(console)}") from exc
    elapsed = perf_counter() - start
    tail = _tail(console)
    marker = r"\bnormal termination\b" if model == "flow" else r"\b(program completed|normal termination)\b"
    if process.returncode or re.search(marker, tail, re.I) is None:
        raise RunError(f"{model} (exit {process.returncode})\n{tail}\n{_tail(detail)}")
    return elapsed


@dataclass
class Run:
    case: Scenario
    times: np.ndarray
    concentration: np.ndarray
    mass_times: np.ndarray
    mass_error: np.ndarray
    flow_seconds: float
    transport_seconds: float
    flow_discrepancy: float
    rmse: float
    mae: float
    ideal_rmse: float | None

    def profile(self, time):
        """Linear interpolation in time for intermediate plots. Endpoints use raw output."""
        i = int(np.searchsorted(self.times, time))
        if i == 0:
            return self.concentration[0]
        if i == len(self.times):
            return self.concentration[-1]
        if self.times[i] == time:
            return self.concentration[i]
        fraction = (time - self.times[i - 1]) / (self.times[i] - self.times[i - 1])
        profile = self.concentration[i - 1] + fraction * (self.concentration[i] - self.concentration[i - 1])
        profile[0] = self.case.height if time <= self.case.duration else 0.0
        return profile

    def breakthrough(self, x):
        """Interpolate adjacent numerical cell-centre values at the same physical x."""
        position = np.clip(x / self.case.dx, 0, self.case.ncol - 1)
        left = int(position)
        right = min(left + 1, self.case.ncol - 1)
        return self.concentration[:, left] + (position - left) * (self.concentration[:, right] - self.concentration[:, left])


def _read_flow(folder):
    with flopy.utils.CellBudgetFile(folder / "flow.cbc", precision="auto") as budget:
        face_flows = budget.get_data(text="FLOW RIGHT FACE")[-1][0, 0, :-1]
    # Unit cross section converts face discharge [m³/d] to Darcy flux [m/d].
    if not np.allclose(face_flows, DARCY_FLUX, rtol=5e-4, atol=1e-8):
        raise RunError("MODFLOW face flows do not match the benchmark velocity.")
    listing = (folder / "flow.list").read_text(errors="replace")
    discrepancies = re.findall(r"PERCENT DISCREPANCY\s*=\s*([-+0-9.Ee]+)", listing, flags=re.I)
    if not discrepancies:
        raise RunError("The final MODFLOW water-budget discrepancy is missing.")
    return float(discrepancies[-1])


def _read_mt(folder, case):
    ucn_file = folder / "MT3D001.UCN"
    mas_file = folder / "MT3D001.MAS"
    for path in (ucn_file, mas_file):
        if not path.is_file() or path.stat().st_size == 0:
            raise RunError(f"Missing MT3DMS output: {path.name}.\n{_tail(folder / 'transport.list')}")
    with flopy.utils.UcnFile(ucn_file, precision="auto") as output:
        times = np.asarray(output.get_times(), dtype=float)
        values = output.get_alldata()[:, 0, 0, :].copy()
    if (not len(times) or not np.isclose(times[-1], END_TIME, atol=0.02, rtol=0)
            or times[0] <= 0 or not np.isfinite(times).all() or np.any(np.diff(times) <= 0)
            or not np.isfinite(values).all()
            or values.shape != (len(times), case.ncol) or np.any(np.abs(values) >= 1e20)):
        raise RunError("MT3DMS returned incomplete or invalid concentration output.")
    times[-1] = END_TIME
    # The initial condition is known; MT3DMS first writes UCN after one transport step.
    initial = np.zeros((1, case.ncol), dtype=values.dtype)
    initial[0, 0] = case.height
    times = np.r_[0.0, times]
    values = np.concatenate((initial, values))
    mass = np.atleast_1d(flopy.mt3d.Mt3dms.load_mas(str(mas_file)))
    if not len(mass) or not np.isclose(mass["time"][-1], END_TIME, atol=0.06, rtol=0):
        raise RunError("The MT3DMS mass summary did not reach the end of the simulation.")
    errors = np.asarray(mass["error_in-out"], dtype=float)
    if not np.isfinite(errors[-1]):
        raise RunError("The final MT3DMS solute budget is unreadable.")
    return times, values, mass["time"].astype(float), errors


def run_case(case, engines=None, timeout=60):
    engines = find_engines() if engines is None else engines
    if not all(engines.get(k) for k in EXECUTABLE_NAMES):
        raise RunError("MODFLOW-2005 and MT3DMS executables are required.")
    with TemporaryDirectory(prefix="mww01_transport_") as directory:
        folder = Path(directory)
        write_models(case, folder, engines)
        flow_seconds = _execute(engines["flow"], "flow", folder, timeout)
        if not (folder / "transport.ftl").is_file():
            raise RunError("MODFLOW did not write the LMT flow-transport link.")
        try:
            flow_error = _read_flow(folder)
            transport_seconds = _execute(engines["transport"], "transport", folder, timeout)
            times, values, mass_times, mass_error = _read_mt(folder, case)
        except (OSError, ValueError, IndexError, EOFError, BudgetIndexError) as exc:
            raise RunError(f"{exc}\n{_tail(folder / 'transport.list')}") from exc
    rmse, mae, ideal_rmse = final_errors(case, values[-1])
    return Run(case, times, values, mass_times, mass_error, flow_seconds, transport_seconds,
               flow_error, rmse, mae, ideal_rmse)
