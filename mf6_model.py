"""MODFLOW 6 model and execution utilities for the Streamlit cloud test.

The module deliberately contains no Streamlit code.  Keeping the numerical model
separate from the user interface makes the model easier to test and reuse.
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

# Fixed discretization for the first cloud deployment test.
# Odd row/column counts place the pumping well exactly in the grid centre.
NLAY = 3
NROW = 21
NCOL = 31
DELR = 100.0  # m
DELC = 100.0  # m
TOP = 30.0  # m
BOTM = np.array([20.0, 10.0, 0.0])  # m

WELL_LAYER = 2  # zero-based index -> layer 3
WELL_ROW = NROW // 2
WELL_COL = NCOL // 2

MODEL_TIMEOUT_SECONDS = 20


@dataclass(frozen=True)
class ModelParameters:
    """Parameters exposed by the Streamlit interface.

    Pumping is entered as a positive extraction magnitude in m3/day.  The WEL
    package receives the corresponding negative MODFLOW flow rate.
    """

    head_left: float = 32.0
    head_right: float = 31.0
    pumping_rate: float = 300.0
    k_layer1: float = 10.0
    k_layer2: float = 0.10
    k_layer3: float = 5.0
    vertical_anisotropy: float = 0.10

    def signature(self) -> tuple[float, ...]:
        """Return a hashable representation used to invalidate old results."""
        return (
            self.head_left,
            self.head_right,
            self.pumping_rate,
            self.k_layer1,
            self.k_layer2,
            self.k_layer3,
            self.vertical_anisotropy,
        )


@dataclass
class ModelResult:
    """Small result object returned after a successful MODFLOW run."""

    head: np.ndarray
    runtime_seconds: float
    mf6_executable: str
    mf6_version: str
    stdout: str


def locate_mf6() -> Path:
    """Locate the MODFLOW 6 executable.

    Resolution order:
    1. MF6_EXE environment variable (useful for local development).
    2. A bundled executable in ``bin/`` next to this source file.
    3. ``mf6`` available on PATH (the default for the supplied Conda setup).

    This makes the same code usable with both deployment strategies discussed
    for the educational apps: Conda-installed MF6 or a repository-bundled
    Linux executable.
    """

    candidates: list[Path] = []

    env_exe = os.environ.get("MF6_EXE")
    if env_exe:
        candidates.append(Path(env_exe).expanduser())

    project_root = Path(__file__).resolve().parent
    bundled_name = "mf6.exe" if os.name == "nt" else "mf6"
    candidates.append(project_root / "bin" / bundled_name)

    on_path = shutil.which("mf6")
    if on_path:
        candidates.append(Path(on_path))

    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate.is_file():
            # Git normally preserves executable permissions, but explicitly
            # setting them makes deployment more tolerant of copied files.
            if os.name != "nt":
                current_mode = candidate.stat().st_mode
                candidate.chmod(
                    current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                )
            return candidate

    searched = "\n".join(f"  - {p}" for p in candidates) or "  - no candidates"
    raise FileNotFoundError(
        "MODFLOW 6 executable 'mf6' was not found. Searched:\n"
        f"{searched}\n"
        "Install modflow6 in the environment, add bin/mf6, or set MF6_EXE."
    )


def get_mf6_version(executable: Path) -> str:
    """Return the version string reported by the MODFLOW executable."""

    try:
        completed = subprocess.run(
            [str(executable), "-v"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(f"Could not execute MODFLOW 6: {exc}") from exc

    text = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    text = text.strip()
    return text.splitlines()[0] if text else "Version not reported"


def _initial_head(params: ModelParameters) -> np.ndarray:
    """Create a linear left-to-right initial head field for all three layers."""

    line = np.linspace(params.head_left, params.head_right, NCOL)
    initial = np.broadcast_to(line, (NLAY, NROW, NCOL)).copy()
    return initial


def build_simulation(
    params: ModelParameters,
    workspace: Path,
    executable: Path,
) -> flopy.mf6.MFSimulation:
    """Build the three-layer steady-state MODFLOW 6 simulation with FloPy."""

    sim = flopy.mf6.MFSimulation(
        sim_name=MODEL_NAME,
        version="mf6",
        exe_name=str(executable),
        sim_ws=str(workspace),
    )

    # One steady stress period.  PERLEN has no physical importance for a purely
    # steady model, but a time discretization package is still required by MF6.
    flopy.mf6.ModflowTdis(
        sim,
        time_units="DAYS",
        nper=1,
        perioddata=[(1.0, 1, 1.0)],
    )

    # SIMPLE is appropriate because all layers are treated as confined and the
    # model contains only linear stress packages (CHD and WEL).
    flopy.mf6.ModflowIms(
        sim,
        print_option="SUMMARY",
        complexity="SIMPLE",
        linear_acceleration="BICGSTAB",
    )

    gwf = flopy.mf6.ModflowGwf(
        sim,
        modelname=MODEL_NAME,
        save_flows=True,
    )

    flopy.mf6.ModflowGwfdis(
        gwf,
        nlay=NLAY,
        nrow=NROW,
        ncol=NCOL,
        delr=DELR,
        delc=DELC,
        top=TOP,
        botm=BOTM,
    )

    flopy.mf6.ModflowGwfic(gwf, strt=_initial_head(params))

    # Horizontal conductivity differs by layer.  K33 is vertical hydraulic
    # conductivity; a ratio below 1 represents vertical anisotropy.
    k = np.empty((NLAY, NROW, NCOL), dtype=float)
    k[0, :, :] = params.k_layer1
    k[1, :, :] = params.k_layer2
    k[2, :, :] = params.k_layer3
    k33 = k * params.vertical_anisotropy

    flopy.mf6.ModflowGwfnpf(
        gwf,
        icelltype=0,  # all cells confined: intentionally simple for first test
        k=k,
        k33=k33,
        save_flows=True,
        save_specific_discharge=True,
    )

    # Specified-head boundaries are applied to the complete left and right model
    # faces in all layers.  This creates a regional left-to-right gradient.
    chd_data = []
    for layer in range(NLAY):
        for row in range(NROW):
            chd_data.append(((layer, row, 0), params.head_left))
            chd_data.append(((layer, row, NCOL - 1), params.head_right))

    flopy.mf6.ModflowGwfchd(
        gwf,
        stress_period_data={0: chd_data},
        save_flows=True,
        pname="CHD",
    )

    # A single extraction well is located in the centre of the lower aquifer.
    # MODFLOW uses negative flow for extraction.
    well_data = [((WELL_LAYER, WELL_ROW, WELL_COL), -abs(params.pumping_rate))]
    flopy.mf6.ModflowGwfwel(
        gwf,
        stress_period_data={0: well_data},
        save_flows=True,
        pname="WEL",
    )

    # Save heads and the cell-by-cell budget.  The head file is read immediately
    # after each run, before the temporary workspace is deleted.
    flopy.mf6.ModflowGwfoc(
        gwf,
        head_filerecord=[f"{MODEL_NAME}.hds"],
        budget_filerecord=[f"{MODEL_NAME}.cbc"],
        saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
        printrecord=[("HEAD", "LAST"), ("BUDGET", "LAST")],
    )

    return sim


def run_model(params: ModelParameters) -> ModelResult:
    """Build, execute, validate, and read one isolated MODFLOW simulation.

    A new temporary directory is created for every call.  This is essential for
    a multi-user Streamlit application because simultaneous users must never
    write to the same MODFLOW input/output files.
    """

    executable = locate_mf6()
    version = get_mf6_version(executable)

    started = time.perf_counter()

    with tempfile.TemporaryDirectory(prefix="mf6_streamlit_") as temp_dir:
        workspace = Path(temp_dir)
        sim = build_simulation(params, workspace, executable)
        sim.write_simulation()

        try:
            completed = subprocess.run(
                [str(executable)],
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=MODEL_TIMEOUT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                f"MODFLOW exceeded the {MODEL_TIMEOUT_SECONDS}-second safety timeout."
            ) from exc
        except OSError as exc:
            raise RuntimeError(f"MODFLOW could not be started: {exc}") from exc

        output = "\n".join(
            part for part in (completed.stdout, completed.stderr) if part
        )

        normal_termination = "NORMAL TERMINATION OF SIMULATION" in output.upper()
        if completed.returncode != 0 or not normal_termination:
            tail = "\n".join(output.splitlines()[-40:])
            raise RuntimeError(
                "MODFLOW did not terminate normally.\n\n"
                f"Return code: {completed.returncode}\n"
                f"Last MODFLOW messages:\n{tail}"
            )

        head_file = workspace / f"{MODEL_NAME}.hds"
        if not head_file.is_file():
            raise RuntimeError(
                "MODFLOW reported normal termination, but the expected head file "
                f"was not created: {head_file.name}"
            )

        head = flopy.utils.HeadFile(head_file).get_data()
        head = np.asarray(head, dtype=float).copy()

        if head.shape != (NLAY, NROW, NCOL):
            raise RuntimeError(
                f"Unexpected head-array shape {head.shape}; "
                f"expected {(NLAY, NROW, NCOL)}."
            )
        if not np.all(np.isfinite(head)):
            raise RuntimeError("The MODFLOW head array contains non-finite values.")

    runtime = time.perf_counter() - started

    return ModelResult(
        head=head,
        runtime_seconds=runtime,
        mf6_executable=str(executable),
        mf6_version=version,
        stdout=output,
    )
