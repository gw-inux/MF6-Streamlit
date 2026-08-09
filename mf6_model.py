"""MODFLOW 6 + MODPATH 7 utilities for the Streamlit cloud test.

This version keeps the proven split workflow:

1. ``run_modflow`` builds/runs a steady three-layer MODFLOW 6 model and keeps
   its private temporary workspace alive.
2. ``run_modpath`` reuses that existing flow solution. MODFLOW is not rerun.

The grid size and one to three pumping-well locations are configurable. All
wells are screened in layer 3, and each well has its own pumping rate (entered
as a positive extraction magnitude). Backward tracking uses a user-defined number of particles for each well;
forward tracking releases one particle in every constant-head cell on both lateral
boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import shutil
import stat
import subprocess
import tempfile
import time

import flopy
import numpy as np


MODEL_NAME = "three_layer_test"

NLAY = 3
DEFAULT_NROW = 21
DEFAULT_NCOL = 31
# Backward-compatible aliases used by older tests/imports.
NROW = DEFAULT_NROW
NCOL = DEFAULT_NCOL

DELR = 100.0  # m
DELC = 100.0  # m
TOP = 30.0  # m
BOTM = np.array([20.0, 10.0, 0.0])  # m

WELL_LAYER = 2  # zero-based -> layer 3
WELL_ROW = DEFAULT_NROW // 2
WELL_COL = DEFAULT_NCOL // 2

MF6_TIMEOUT_SECONDS = 20
MP7_TIMEOUT_SECONDS = 20

PARTICLES_PER_WELL = 100  # default backward-particle count per well
BACKWARD_PARTICLE_COUNT = PARTICLES_PER_WELL  # backward-compatible one-well default
FORWARD_PARTICLE_COUNT = NLAY * DEFAULT_NROW * 2

WORKSPACE_PREFIX = "mf6_streamlit_"


@dataclass(frozen=True)
class ModelParameters:
    """Parameters defining one flow-model realization.

    ``well_positions`` contains zero-based ``(row, column)`` pairs. Wells are
    fixed to layer 3 for this teaching model. ``pumping_rates`` contains one
    positive extraction magnitude for each well; MODFLOW receives the
    corresponding negative WEL fluxes.
    """

    head_left: float = 32.0
    head_right: float = 31.0
    pumping_rates: tuple[float, ...] = (300.0,)
    k_layer1: float = 10.0
    k_layer2: float = 0.10
    k_layer3: float = 5.0
    vertical_anisotropy: float = 0.10
    nrow: int = DEFAULT_NROW
    ncol: int = DEFAULT_NCOL
    well_positions: tuple[tuple[int, int], ...] = ((WELL_ROW, WELL_COL),)

    def validate(self) -> None:
        if self.nrow < 3 or self.ncol < 3:
            raise ValueError("The grid must contain at least 3 rows and 3 columns.")
        if not 1 <= len(self.well_positions) <= 3:
            raise ValueError("Define between one and three pumping wells.")
        if len(set(self.well_positions)) != len(self.well_positions):
            raise ValueError("Pumping wells must occupy different cells.")
        if len(self.pumping_rates) != len(self.well_positions):
            raise ValueError("Provide exactly one pumping rate for each well.")
        for rate in self.pumping_rates:
            if not np.isfinite(rate) or rate < 0.0:
                raise ValueError("Pumping rates must be finite and non-negative.")
        for row, col in self.well_positions:
            if not (0 <= row < self.nrow):
                raise ValueError(f"Well row {row + 1} is outside the model grid.")
            if not (0 < col < self.ncol - 1):
                raise ValueError(
                    "Pumping wells must be inside the model and cannot share "
                    "the left/right constant-head boundary columns."
                )
        if self.vertical_anisotropy <= 0.0:
            raise ValueError("Kz/Kx must be greater than zero.")

    @property
    def backward_particle_count(self) -> int:
        return PARTICLES_PER_WELL * len(self.well_positions)

    @property
    def forward_particle_count(self) -> int:
        return NLAY * self.nrow * 2

    def signature(self) -> tuple[object, ...]:
        return (
            self.head_left,
            self.head_right,
            self.pumping_rates,
            self.k_layer1,
            self.k_layer2,
            self.k_layer3,
            self.vertical_anisotropy,
            self.nrow,
            self.ncol,
            self.well_positions,
        )


@dataclass
class FlowResult:
    head: np.ndarray
    workspace: str
    runtime_seconds: float
    mf6_executable: str
    mf6_version: str
    stdout: str
    parameter_signature: tuple[object, ...]
    params: ModelParameters
    cumulative_budget: list[tuple[str, float]]


@dataclass
class ParticleTrack:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    time: np.ndarray
    layer: np.ndarray


@dataclass
class TrackingResult:
    direction: str
    requested_particles: int
    tracks: list[ParticleTrack]
    start_xyz: np.ndarray
    start_layer: np.ndarray
    runtime_seconds: float
    mp7_version: str
    stdout: str

    @property
    def pathline_count(self) -> int:
        return len(self.tracks)

    @property
    def max_travel_time(self) -> float:
        if not self.tracks:
            return 0.0
        maxima = [float(np.max(t.time)) for t in self.tracks if t.time.size]
        return max(maxima, default=0.0)


@dataclass
class ModpathResult:
    backward: TrackingResult
    forward: TrackingResult
    runtime_seconds: float
    mp7_executable: str
    effective_porosity: float
    flow_parameter_signature: tuple[object, ...]


# -----------------------------------------------------------------------------
# Executable handling
# -----------------------------------------------------------------------------

def _set_executable_permission(path: Path) -> None:
    if os.name != "nt":
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _locate_executable(*, env_var: str, linux_name: str, windows_name: str, display_name: str) -> Path:
    candidates: list[Path] = []
    env_exe = os.environ.get(env_var)
    if env_exe:
        candidates.append(Path(env_exe).expanduser())

    root = Path(__file__).resolve().parent
    bundled_name = windows_name if os.name == "nt" else linux_name
    candidates.append(root / "bin" / bundled_name)

    on_path = shutil.which(windows_name if os.name == "nt" else linux_name)
    if on_path:
        candidates.append(Path(on_path))

    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate.is_file():
            _set_executable_permission(candidate)
            return candidate

    searched = "\n".join(f"  - {p}" for p in candidates) or "  - no candidates"
    raise FileNotFoundError(
        f"{display_name} executable was not found. Searched:\n{searched}\n"
        f"Add bin/{bundled_name}, put the executable on PATH, or set {env_var}."
    )


def locate_mf6() -> Path:
    return _locate_executable(env_var="MF6_EXE", linux_name="mf6", windows_name="mf6.exe", display_name="MODFLOW 6")


def locate_mp7() -> Path:
    return _locate_executable(env_var="MP7_EXE", linux_name="mp7", windows_name="mp7.exe", display_name="MODPATH 7")


def get_mf6_version(executable: Path) -> str:
    try:
        completed = subprocess.run([str(executable), "-v"], capture_output=True, text=True, timeout=5, check=False)
    except OSError as exc:
        raise RuntimeError(f"Could not execute MODFLOW 6: {exc}") from exc
    text = "\n".join(part for part in (completed.stdout, completed.stderr) if part).strip()
    return text.splitlines()[0] if text else "Version not reported"


def _extract_mp7_version(output: str) -> str:
    for line in output.splitlines():
        if "MODPATH VERSION" in line.upper():
            return line.strip()
    return "MODPATH version not reported"


# -----------------------------------------------------------------------------
# MODFLOW model
# -----------------------------------------------------------------------------

def _initial_head(params: ModelParameters) -> np.ndarray:
    line = np.linspace(params.head_left, params.head_right, params.ncol)
    return np.broadcast_to(line, (NLAY, params.nrow, params.ncol)).copy()


def build_simulation(params: ModelParameters, workspace: Path, executable: Path) -> flopy.mf6.MFSimulation:
    params.validate()

    sim = flopy.mf6.MFSimulation(
        sim_name=MODEL_NAME,
        version="mf6",
        exe_name=str(executable),
        sim_ws=str(workspace),
    )

    flopy.mf6.ModflowTdis(sim, time_units="DAYS", nper=1, perioddata=[(1.0, 1, 1.0)])
    flopy.mf6.ModflowIms(sim, print_option="SUMMARY", complexity="SIMPLE", linear_acceleration="BICGSTAB")

    gwf = flopy.mf6.ModflowGwf(
        sim,
        modelname=MODEL_NAME,
        list=f"{MODEL_NAME}.lst",
        print_flows=True,
        save_flows=True,
    )

    flopy.mf6.ModflowGwfdis(
        gwf,
        nlay=NLAY,
        nrow=params.nrow,
        ncol=params.ncol,
        delr=DELR,
        delc=DELC,
        top=TOP,
        botm=BOTM,
    )
    flopy.mf6.ModflowGwfic(gwf, strt=_initial_head(params))

    k = np.empty((NLAY, params.nrow, params.ncol), dtype=float)
    k[0] = params.k_layer1
    k[1] = params.k_layer2
    k[2] = params.k_layer3
    k33 = k * params.vertical_anisotropy

    flopy.mf6.ModflowGwfnpf(
        gwf,
        icelltype=0,
        k=k,
        k33=k33,
        save_flows=True,
        save_specific_discharge=True,
    )

    chd_data = []
    for layer in range(NLAY):
        for row in range(params.nrow):
            chd_data.append(((layer, row, 0), params.head_left))
            chd_data.append(((layer, row, params.ncol - 1), params.head_right))

    flopy.mf6.ModflowGwfchd(gwf, stress_period_data={0: chd_data}, save_flows=True, pname="CHD")

    well_data = [
        ((WELL_LAYER, row, col), -abs(rate))
        for (row, col), rate in zip(params.well_positions, params.pumping_rates)
    ]
    flopy.mf6.ModflowGwfwel(gwf, stress_period_data={0: well_data}, save_flows=True, pname="WEL")

    flopy.mf6.ModflowGwfoc(
        gwf,
        head_filerecord=[f"{MODEL_NAME}.hds"],
        budget_filerecord=[f"{MODEL_NAME}.cbc"],
        saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
        printrecord=[("HEAD", "LAST"), ("BUDGET", "ALL")],
    )
    return sim


def cleanup_workspace(workspace: str | Path | None) -> None:
    if not workspace:
        return
    path = Path(workspace)
    if path.name.startswith(WORKSPACE_PREFIX) and path.exists():
        shutil.rmtree(path, ignore_errors=True)


def _validate_modflow_outputs(workspace: Path, params: ModelParameters) -> np.ndarray:
    head_file = workspace / f"{MODEL_NAME}.hds"
    budget_file = workspace / f"{MODEL_NAME}.cbc"
    grb_files = list(workspace.glob("*.grb"))
    if not head_file.is_file() or not budget_file.is_file() or not grb_files:
        raise RuntimeError(
            "MODFLOW terminated normally, but one or more files required by MODPATH "
            "(head, budget, binary grid) are missing."
        )

    head = np.asarray(flopy.utils.HeadFile(head_file).get_data(), dtype=float).copy()
    expected = (NLAY, params.nrow, params.ncol)
    if head.shape != expected:
        raise RuntimeError(f"Unexpected head-array shape {head.shape}; expected {expected}.")
    if not np.all(np.isfinite(head)):
        raise RuntimeError("The MODFLOW head array contains non-finite values.")
    return head


def _normalise_budget_name(name: object) -> str:
    """Return a clean MODFLOW budget field name.

    Some FloPy/Numpy combinations expose listing-budget field names as real
    byte strings, while others expose their *string representation*, for
    example ``"b'CHD_IN'"``.  Normalize both forms so downstream code always
    receives ordinary names such as ``CHD_IN``.
    """
    if isinstance(name, (bytes, np.bytes_)):
        text = name.decode("ascii", errors="replace")
    else:
        text = str(name)

    text = text.replace("\x00", "").strip().rstrip(":")

    # Strip a literal byte-string wrapper that can survive conversion through
    # a structured NumPy dtype, e.g. "b'WEL_OUT'" or 'b"WEL_OUT"'.
    if len(text) >= 3 and text[0] in {"b", "B"} and text[1] in {"'", '"'} and text[-1] == text[1]:
        text = text[2:-1]

    return text.strip()


def _read_binary_external_budget(workspace: Path) -> list[tuple[str, float]]:
    """Fallback external budget from the binary cell-budget file.

    The model contains only CHD and WEL external stresses.  For the single
    one-day steady stress period, the final rates multiplied by the elapsed
    simulation time are also the cumulative volumes.  This fallback avoids
    relying on listing-file formatting while retaining the same IN/OUT terms.
    """
    budget_file = workspace / f"{MODEL_NAME}.cbc"
    if not budget_file.is_file():
        return []

    try:
        cbc = flopy.utils.CellBudgetFile(str(budget_file), precision="auto")
        names = [str(n).strip().upper() for n in cbc.get_unique_record_names(decode=True)]
        times = cbc.get_times()
        elapsed_days = float(times[-1]) if times else 1.0
        elapsed_days = max(elapsed_days, 0.0)

        items: list[tuple[str, float]] = []
        total_in = 0.0
        total_out = 0.0

        for package in ("CHD", "WEL"):
            matching = next((n for n in names if n == package), None)
            if matching is None:
                continue
            records = cbc.get_data(text=matching)
            if not records:
                continue
            raw_record = records[-1]
            if getattr(getattr(raw_record, "dtype", None), "names", None) and "q" in raw_record.dtype.names:
                values = np.asarray(raw_record["q"], dtype=float).ravel()
            else:
                record = np.ma.asarray(raw_record, dtype=float)
                values = record.compressed() if np.ma.isMaskedArray(record) else np.asarray(record).ravel()
            values = values[np.isfinite(values)]
            if values.size == 0:
                continue

            rate_in = float(values[values > 0.0].sum())
            rate_out = float(-values[values < 0.0].sum())
            volume_in = rate_in * elapsed_days
            volume_out = rate_out * elapsed_days

            if volume_in > 0.0:
                items.append((f"{package}_IN", volume_in))
                total_in += volume_in
            if volume_out > 0.0:
                items.append((f"{package}_OUT", -volume_out))
                total_out += volume_out

        if not items:
            return []

        error = total_in - total_out
        denominator = 0.5 * (total_in + total_out)
        discrepancy = 100.0 * error / denominator if denominator > 0.0 else 0.0
        items.extend(
            [
                ("TOTAL_IN", total_in),
                ("TOTAL_OUT", -total_out),
                ("IN-OUT", error),
                ("PERCENT_DISCREPANCY", discrepancy),
            ]
        )
        return items
    except Exception:
        return []


def _read_cumulative_budget(workspace: Path) -> list[tuple[str, float]]:
    """Read the final cumulative water budget with a binary-file fallback.

    ``Mf6ListBudget.get_cumulative`` exposes the cumulative table directly as
    one record per time step with named fields (CHD_IN, WEL_OUT, TOTAL_IN,
    etc.).  This is more robust here than reconstructing the table through
    ``get_data``.  If a deployed FloPy/MF6 combination still yields no external
    IN/OUT component fields, the binary cell-budget file is used as a fallback.
    """
    list_file = workspace / f"{MODEL_NAME}.lst"
    items: list[tuple[str, float]] = []

    if list_file.is_file():
        try:
            budget = flopy.utils.Mf6ListBudget(str(list_file), timeunit="days")
            cumulative = budget.get_cumulative() if budget.isvalid() else None
            if cumulative is not None and len(cumulative):
                last = cumulative[-1]
                metadata = {"totim", "time_step", "stress_period"}
                for field in cumulative.dtype.names or ():
                    if field in metadata:
                        continue
                    value = float(last[field])
                    if np.isfinite(value):
                        items.append((_normalise_budget_name(field), value))
        except Exception:
            items = []

    # Require at least one real external component.  TOTAL/PERCENT entries alone
    # are not enough for the requested component bar plot.
    component_names = [name.upper() for name, _ in items]
    has_components = any(
        name.endswith("_IN") or name.endswith("_OUT")
        for name in component_names
        if not name.startswith("TOTAL_")
    )
    if has_components:
        return items

    binary_items = _read_binary_external_budget(workspace)
    return binary_items if binary_items else items


def run_modflow(params: ModelParameters) -> FlowResult:
    params.validate()
    executable = locate_mf6()
    version = get_mf6_version(executable)
    workspace = Path(tempfile.mkdtemp(prefix=WORKSPACE_PREFIX))

    try:
        sim = build_simulation(params, workspace, executable)
        sim.write_simulation()

        started = time.perf_counter()
        try:
            completed = subprocess.run(
                [str(executable)], cwd=workspace, capture_output=True, text=True,
                timeout=MF6_TIMEOUT_SECONDS, check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"MODFLOW exceeded the {MF6_TIMEOUT_SECONDS}-second safety timeout.") from exc
        except OSError as exc:
            raise RuntimeError(f"MODFLOW could not be started: {exc}") from exc

        runtime = time.perf_counter() - started
        output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
        if completed.returncode != 0 or "NORMAL TERMINATION OF SIMULATION" not in output.upper():
            tail = "\n".join(output.splitlines()[-40:])
            raise RuntimeError(
                "MODFLOW did not terminate normally.\n\n"
                f"Return code: {completed.returncode}\nLast MODFLOW messages:\n{tail}"
            )

        head = _validate_modflow_outputs(workspace, params)
        cumulative_budget = _read_cumulative_budget(workspace)

        return FlowResult(
            head=head,
            workspace=str(workspace),
            runtime_seconds=runtime,
            mf6_executable=str(executable),
            mf6_version=version,
            stdout=output,
            parameter_signature=params.signature(),
            params=params,
            cumulative_budget=cumulative_budget,
        )
    except Exception:
        cleanup_workspace(workspace)
        raise


# -----------------------------------------------------------------------------
# MODPATH particles
# -----------------------------------------------------------------------------

def _cell_xyz(params: ModelParameters, layer: int, row: int, col: int, localx: float, localy: float, localz: float) -> tuple[float, float, float]:
    x = (col + localx) * DELR
    y = (params.nrow - row - 1 + localy) * DELC
    layer_top = TOP if layer == 0 else float(BOTM[layer - 1])
    layer_bottom = float(BOTM[layer])
    z = layer_bottom + localz * (layer_top - layer_bottom)
    return float(x), float(y), float(z)


def _radical_inverse(index: int, base: int) -> float:
    """Low-discrepancy coordinate in (0, 1) for deterministic particle seeding."""
    value = 0.0
    factor = 1.0 / float(base)
    i = int(index)
    while i > 0:
        value += factor * (i % base)
        i //= base
        factor /= float(base)
    return value


def _backward_particle_data(
    params: ModelParameters,
    particle_counts: tuple[int, ...],
) -> tuple[flopy.modpath.ParticleData, np.ndarray, np.ndarray]:
    """Create exactly the requested number of backward particles per well.

    A deterministic low-discrepancy distribution is used instead of requiring
    the requested count to factor into a regular 3-D subdivision.  This permits
    arbitrary practical counts while spreading release points throughout each
    pumping cell rather than clustering them at the cell centre.
    """
    if len(particle_counts) != len(params.well_positions):
        raise ValueError("Provide one backward-particle count for each pumping well.")
    if any(int(count) < 1 for count in particle_counts):
        raise ValueError("Each backward-particle count must be at least 1.")

    locs: list[tuple[int, int, int]] = []
    lx: list[float] = []
    ly: list[float] = []
    lz: list[float] = []
    xyz: list[tuple[float, float, float]] = []
    layers: list[int] = []

    eps = 1.0e-4
    for (row, col), count in zip(params.well_positions, particle_counts):
        count = int(count)
        for ip in range(count):
            # Hammersley-like coordinates: one stratified coordinate and two
            # radical-inverse coordinates.  Clip only to avoid cell faces.
            xloc = (ip + 0.5) / count
            yloc = _radical_inverse(ip + 1, 2)
            zloc = _radical_inverse(ip + 1, 3)
            xloc = float(np.clip(xloc, eps, 1.0 - eps))
            yloc = float(np.clip(yloc, eps, 1.0 - eps))
            zloc = float(np.clip(zloc, eps, 1.0 - eps))

            locs.append((WELL_LAYER, row, col))
            lx.append(xloc); ly.append(yloc); lz.append(zloc)
            xyz.append(_cell_xyz(params, WELL_LAYER, row, col, xloc, yloc, zloc))
            layers.append(WELL_LAYER)

    expected = int(sum(int(c) for c in particle_counts))
    if len(locs) != expected:
        raise RuntimeError(
            f"Backward particle construction produced {len(locs)} particles; expected {expected}."
        )

    pdata = flopy.modpath.ParticleData(
        partlocs=locs, structured=True,
        localx=np.asarray(lx), localy=np.asarray(ly), localz=np.asarray(lz), drape=0,
    )
    return pdata, np.asarray(xyz, dtype=float), np.asarray(layers, dtype=int)


def _forward_particle_data(params: ModelParameters) -> tuple[flopy.modpath.ParticleData, np.ndarray, np.ndarray]:
    locs: list[tuple[int, int, int]] = []
    xyz: list[tuple[float, float, float]] = []
    layers: list[int] = []

    for layer in range(NLAY):
        for row in range(params.nrow):
            for col in (0, params.ncol - 1):
                locs.append((layer, row, col))
                xyz.append(_cell_xyz(params, layer, row, col, 0.5, 0.5, 0.5))
                layers.append(layer)

    if len(locs) != params.forward_particle_count:
        raise RuntimeError(
            f"Forward particle construction produced {len(locs)} particles; "
            f"expected {params.forward_particle_count}."
        )

    pdata = flopy.modpath.ParticleData(
        partlocs=locs, structured=True, localx=0.5, localy=0.5, localz=0.5, drape=0,
    )
    return pdata, np.asarray(xyz, dtype=float), np.asarray(layers, dtype=int)


def _read_pathlines(pathline_file: Path) -> list[ParticleTrack]:
    if not pathline_file.is_file():
        raise RuntimeError(f"Expected MODPATH pathline file was not created: {pathline_file}")
    raw_tracks = flopy.utils.PathlineFile(pathline_file).get_alldata()
    tracks: list[ParticleTrack] = []
    for rec in raw_tracks:
        tracks.append(
            ParticleTrack(
                x=np.asarray(rec["x"], dtype=float).copy(),
                y=np.asarray(rec["y"], dtype=float).copy(),
                z=np.asarray(rec["z"], dtype=float).copy(),
                time=np.asarray(rec["time"], dtype=float).copy(),
                layer=np.asarray(rec["k"], dtype=int).copy(),
            )
        )
    return tracks


def _remove_old_modpath_files(workspace: Path, modelname: str) -> None:
    for path in workspace.glob(f"{modelname}*"):
        if path.is_file():
            path.unlink(missing_ok=True)


def _load_existing_gwf(workspace: Path, mf6_executable: Path):
    sim = flopy.mf6.MFSimulation.load(sim_ws=str(workspace), exe_name=str(mf6_executable), verbosity_level=0)
    gwf = sim.get_model(MODEL_NAME)
    if gwf is None:
        raise RuntimeError(f"Could not reload groundwater-flow model '{MODEL_NAME}'.")
    return sim, gwf


def _run_one_modpath(*, gwf, workspace: Path, executable: Path, direction: str,
                     particle_data: flopy.modpath.ParticleData, start_xyz: np.ndarray,
                     start_layer: np.ndarray, porosity: float, modelname: str) -> TrackingResult:
    _remove_old_modpath_files(workspace, modelname)

    particle_group = flopy.modpath.ParticleGroup(
        particlegroupname=f"{direction.upper()}_PARTICLES",
        filename=f"{modelname}.sloc",
        particledata=particle_data,
    )

    mp = flopy.modpath.Modpath7(
        modelname=modelname,
        flowmodel=gwf,
        exe_name=str(executable),
        model_ws=str(workspace),
        headfilename=f"{MODEL_NAME}.hds",
        budgetfilename=f"{MODEL_NAME}.cbc",
    )
    flopy.modpath.Modpath7Bas(mp, porosity=porosity)
    flopy.modpath.Modpath7Sim(
        mp,
        simulationtype="pathline",
        trackingdirection=direction,
        weaksinkoption="pass_through",
        weaksourceoption="pass_through",
        budgetoutputoption="summary",
        referencetime=0.0,
        stoptimeoption="extend",
        particlegroups=particle_group,
    )
    mp.write_input()

    started = time.perf_counter()
    try:
        completed = subprocess.run(
            [str(executable), mp.namefile], cwd=workspace, capture_output=True,
            text=True, timeout=MP7_TIMEOUT_SECONDS, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"MODPATH ({direction}) exceeded the {MP7_TIMEOUT_SECONDS}-second safety timeout.") from exc
    except OSError as exc:
        raise RuntimeError(f"MODPATH ({direction}) could not be started: {exc}") from exc

    runtime = time.perf_counter() - started
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    if completed.returncode != 0 or "NORMAL TERMINATION" not in output.upper():
        tail = "\n".join(output.splitlines()[-50:])
        raise RuntimeError(
            f"MODPATH ({direction}) did not terminate normally.\n\n"
            f"Return code: {completed.returncode}\nLast MODPATH messages:\n{tail}"
        )

    tracks = _read_pathlines(workspace / f"{modelname}.mppth")
    requested = int(start_xyz.shape[0])
    if start_xyz.ndim != 2 or start_xyz.shape[1] != 3 or start_layer.shape != (requested,):
        raise RuntimeError(f"Invalid {direction} particle start arrays.")

    return TrackingResult(
        direction=direction,
        requested_particles=requested,
        tracks=tracks,
        start_xyz=np.asarray(start_xyz, dtype=float).copy(),
        start_layer=np.asarray(start_layer, dtype=int).copy(),
        runtime_seconds=runtime,
        mp7_version=_extract_mp7_version(output),
        stdout=output,
    )


def run_modpath(
    flow_result: FlowResult,
    effective_porosity: float = 0.25,
    backward_particle_counts: tuple[int, ...] | None = None,
) -> ModpathResult:
    if not (0.0 < effective_porosity <= 1.0):
        raise ValueError("Effective porosity must be greater than 0 and no more than 1.")

    workspace = Path(flow_result.workspace)
    if not workspace.is_dir():
        raise RuntimeError("The MODFLOW workspace is no longer available. Run MODFLOW again before running MODPATH.")

    params = flow_result.params
    _validate_modflow_outputs(workspace, params)
    mf6_executable = locate_mf6()
    mp7_executable = locate_mp7()
    _sim, gwf = _load_existing_gwf(workspace, mf6_executable)

    if backward_particle_counts is None:
        backward_particle_counts = tuple(PARTICLES_PER_WELL for _ in params.well_positions)
    backward_particle_counts = tuple(int(c) for c in backward_particle_counts)
    if len(backward_particle_counts) != len(params.well_positions):
        raise ValueError("Provide one backward-particle count for each pumping well.")

    backward_data, backward_xyz, backward_layers = _backward_particle_data(
        params, backward_particle_counts
    )
    forward_data, forward_xyz, forward_layers = _forward_particle_data(params)

    total_started = time.perf_counter()
    backward = _run_one_modpath(
        gwf=gwf, workspace=workspace, executable=mp7_executable,
        direction="backward", particle_data=backward_data,
        start_xyz=backward_xyz, start_layer=backward_layers,
        porosity=effective_porosity, modelname=f"{MODEL_NAME}_mp_backward",
    )
    forward = _run_one_modpath(
        gwf=gwf, workspace=workspace, executable=mp7_executable,
        direction="forward", particle_data=forward_data,
        start_xyz=forward_xyz, start_layer=forward_layers,
        porosity=effective_porosity, modelname=f"{MODEL_NAME}_mp_forward",
    )

    return ModpathResult(
        backward=backward,
        forward=forward,
        runtime_seconds=time.perf_counter() - total_started,
        mp7_executable=str(mp7_executable),
        effective_porosity=float(effective_porosity),
        flow_parameter_signature=flow_result.parameter_signature,
    )
