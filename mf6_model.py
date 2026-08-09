"""MODFLOW 6 + MODPATH 7 utilities for the Streamlit cloud test.

The numerical workflow is deliberately split into two independent stages:

1. ``run_modflow`` creates a private temporary workspace, runs MODFLOW 6,
   validates the output, and *keeps that workspace alive*.
2. ``run_modpath`` reuses the already-computed MODFLOW head/budget/grid files
   and runs backward and forward MODPATH 7 simulations without rerunning MF6.

The Streamlit session stores the workspace path.  When flow-model parameters
change, or when a new MODFLOW simulation is started, the old workspace can be
removed with ``cleanup_workspace``.

Particle definitions
--------------------
Backward tracking
    20 explicit particles are distributed inside the pumping cell using a
    5 x 2 x 2 pattern.

Forward tracking
    One explicit particle is placed at the centre of each specified-head cell
    on both lateral boundaries: 3 layers x 21 rows x 2 sides = 126 particles.

Explicit ``ParticleData`` is used instead of ``NodeParticleData`` templates.
This avoids a FloPy 3.10 edge case in the template ``to_coords`` helper for a
single template applied to many nodes, and it makes the release locations
fully transparent and easy to validate.
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

# Fixed discretization for this deployment test.
# Odd row/column counts place the pumping well exactly in the grid centre.
NLAY = 3
NROW = 21
NCOL = 31
DELR = 100.0  # m
DELC = 100.0  # m
TOP = 30.0  # m
BOTM = np.array([20.0, 10.0, 0.0])  # m

WELL_LAYER = 2  # zero-based -> layer 3
WELL_ROW = NROW // 2
WELL_COL = NCOL // 2

MF6_TIMEOUT_SECONDS = 20
MP7_TIMEOUT_SECONDS = 20

BACKWARD_PARTICLE_COUNT = 20
FORWARD_PARTICLE_COUNT = NLAY * NROW * 2

# Only workspaces created by this module are removed by cleanup_workspace().
WORKSPACE_PREFIX = "mf6_streamlit_"


@dataclass(frozen=True)
class ModelParameters:
    """Flow-model parameters exposed by the Streamlit interface.

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
        """Return a stable signature used by Streamlit to detect stale flow results."""

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
class FlowResult:
    """Validated MODFLOW result plus the persistent per-session workspace."""

    head: np.ndarray
    workspace: str
    runtime_seconds: float
    mf6_executable: str
    mf6_version: str
    stdout: str
    parameter_signature: tuple[float, ...]


@dataclass
class ParticleTrack:
    """One MODPATH pathline copied into memory."""

    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    time: np.ndarray
    layer: np.ndarray


@dataclass
class TrackingResult:
    """Results for one MODPATH tracking direction."""

    direction: str
    requested_particles: int
    tracks: list[ParticleTrack]
    start_xyz: np.ndarray
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
        maxima = [float(np.max(track.time)) for track in self.tracks if track.time.size]
        return max(maxima, default=0.0)


@dataclass
class ModpathResult:
    """Backward and forward tracking results for one existing flow field."""

    backward: TrackingResult
    forward: TrackingResult
    runtime_seconds: float
    mp7_executable: str
    effective_porosity: float
    flow_parameter_signature: tuple[float, ...]


# -----------------------------------------------------------------------------
# Executable handling
# -----------------------------------------------------------------------------

def _set_executable_permission(path: Path) -> None:
    """Ensure a bundled native executable can be started on Linux."""

    if os.name != "nt":
        current_mode = path.stat().st_mode
        path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _locate_executable(
    *,
    env_var: str,
    linux_name: str,
    windows_name: str,
    display_name: str,
) -> Path:
    """Locate a bundled/native executable using a deterministic search order."""

    candidates: list[Path] = []

    env_exe = os.environ.get(env_var)
    if env_exe:
        candidates.append(Path(env_exe).expanduser())

    project_root = Path(__file__).resolve().parent
    bundled_name = windows_name if os.name == "nt" else linux_name
    candidates.append(project_root / "bin" / bundled_name)

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
    return _locate_executable(
        env_var="MF6_EXE",
        linux_name="mf6",
        windows_name="mf6.exe",
        display_name="MODFLOW 6",
    )


def locate_mp7() -> Path:
    return _locate_executable(
        env_var="MP7_EXE",
        linux_name="mp7",
        windows_name="mp7.exe",
        display_name="MODPATH 7",
    )


def get_mf6_version(executable: Path) -> str:
    """Return the first version line reported by MODFLOW 6."""

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


def _extract_mp7_version(output: str) -> str:
    for line in output.splitlines():
        if "MODPATH VERSION" in line.upper():
            return line.strip()
    return "MODPATH version not reported"


# -----------------------------------------------------------------------------
# MODFLOW model
# -----------------------------------------------------------------------------

def _initial_head(params: ModelParameters) -> np.ndarray:
    """Create a linear left-to-right initial head field in all layers."""

    line = np.linspace(params.head_left, params.head_right, NCOL)
    return np.broadcast_to(line, (NLAY, NROW, NCOL)).copy()


def build_simulation(
    params: ModelParameters,
    workspace: Path,
    executable: Path,
) -> flopy.mf6.MFSimulation:
    """Build the small three-layer steady-state MODFLOW 6 simulation."""

    sim = flopy.mf6.MFSimulation(
        sim_name=MODEL_NAME,
        version="mf6",
        exe_name=str(executable),
        sim_ws=str(workspace),
    )

    flopy.mf6.ModflowTdis(
        sim,
        time_units="DAYS",
        nper=1,
        perioddata=[(1.0, 1, 1.0)],
    )

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

    k = np.empty((NLAY, NROW, NCOL), dtype=float)
    k[0, :, :] = params.k_layer1
    k[1, :, :] = params.k_layer2
    k[2, :, :] = params.k_layer3
    k33 = k * params.vertical_anisotropy

    flopy.mf6.ModflowGwfnpf(
        gwf,
        icelltype=0,
        k=k,
        k33=k33,
        save_flows=True,
        save_specific_discharge=True,
    )

    # Constant-head boundaries on both lateral faces, in every layer.
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

    # Extraction is negative in MODFLOW.
    well_data = [((WELL_LAYER, WELL_ROW, WELL_COL), -abs(params.pumping_rate))]
    flopy.mf6.ModflowGwfwel(
        gwf,
        stress_period_data={0: well_data},
        save_flows=True,
        pname="WEL",
    )

    # MODPATH requires heads, cell-by-cell budget and the DIS binary grid file.
    flopy.mf6.ModflowGwfoc(
        gwf,
        head_filerecord=[f"{MODEL_NAME}.hds"],
        budget_filerecord=[f"{MODEL_NAME}.cbc"],
        saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
        printrecord=[("HEAD", "LAST"), ("BUDGET", "LAST")],
    )

    return sim


def cleanup_workspace(workspace: str | Path | None) -> None:
    """Remove a temporary model workspace created by this module.

    The prefix check is intentional: it prevents an accidental call from
    recursively deleting an arbitrary user/project directory.
    """

    if not workspace:
        return

    path = Path(workspace)
    if path.name.startswith(WORKSPACE_PREFIX) and path.exists():
        shutil.rmtree(path, ignore_errors=True)


def _validate_modflow_outputs(workspace: Path) -> np.ndarray:
    """Validate required MODFLOW files and return the final head array."""

    head_file = workspace / f"{MODEL_NAME}.hds"
    budget_file = workspace / f"{MODEL_NAME}.cbc"

    # FloPy/MODPATH derives the exact GRB name from the DIS package.  Checking
    # for at least one *.grb file catches an incomplete MF6 output set early.
    grb_files = list(workspace.glob("*.grb"))

    if not head_file.is_file() or not budget_file.is_file() or not grb_files:
        raise RuntimeError(
            "MODFLOW terminated normally, but one or more files required by "
            "MODPATH (head, budget, binary grid) are missing."
        )

    head = np.asarray(flopy.utils.HeadFile(head_file).get_data(), dtype=float).copy()

    if head.shape != (NLAY, NROW, NCOL):
        raise RuntimeError(
            f"Unexpected head-array shape {head.shape}; expected {(NLAY, NROW, NCOL)}."
        )
    if not np.all(np.isfinite(head)):
        raise RuntimeError("The MODFLOW head array contains non-finite values.")

    return head


def run_modflow(params: ModelParameters) -> FlowResult:
    """Run MODFLOW only and preserve its temporary workspace for later MODPATH.

    If the run fails, the newly created workspace is removed immediately.
    On success, the caller owns the workspace and should eventually call
    ``cleanup_workspace`` (normally when parameters change or a new run starts).
    """

    executable = locate_mf6()
    version = get_mf6_version(executable)
    workspace = Path(tempfile.mkdtemp(prefix=WORKSPACE_PREFIX))

    try:
        sim = build_simulation(params, workspace, executable)
        sim.write_simulation()

        started = time.perf_counter()
        try:
            completed = subprocess.run(
                [str(executable)],
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=MF6_TIMEOUT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                f"MODFLOW exceeded the {MF6_TIMEOUT_SECONDS}-second safety timeout."
            ) from exc
        except OSError as exc:
            raise RuntimeError(f"MODFLOW could not be started: {exc}") from exc

        runtime = time.perf_counter() - started
        output = "\n".join(
            part for part in (completed.stdout, completed.stderr) if part
        )

        if (
            completed.returncode != 0
            or "NORMAL TERMINATION OF SIMULATION" not in output.upper()
        ):
            tail = "\n".join(output.splitlines()[-40:])
            raise RuntimeError(
                "MODFLOW did not terminate normally.\n\n"
                f"Return code: {completed.returncode}\n"
                f"Last MODFLOW messages:\n{tail}"
            )

        head = _validate_modflow_outputs(workspace)

        return FlowResult(
            head=head,
            workspace=str(workspace),
            runtime_seconds=runtime,
            mf6_executable=str(executable),
            mf6_version=version,
            stdout=output,
            parameter_signature=params.signature(),
        )

    except Exception:
        cleanup_workspace(workspace)
        raise


# -----------------------------------------------------------------------------
# Explicit MODPATH particle definitions
# -----------------------------------------------------------------------------

def _cell_xyz(
    layer: int,
    row: int,
    col: int,
    localx: float,
    localy: float,
    localz: float,
) -> tuple[float, float, float]:
    """Convert local structured-cell coordinates (0..1) to model coordinates."""

    x = (col + localx) * DELR

    # MODFLOW row 0 is the top/north row; model y increases upward.
    y = (NROW - row - 1 + localy) * DELC

    layer_top = TOP if layer == 0 else float(BOTM[layer - 1])
    layer_bottom = float(BOTM[layer])
    z = layer_bottom + localz * (layer_top - layer_bottom)

    return float(x), float(y), float(z)


def _backward_particle_data() -> tuple[flopy.modpath.ParticleData, np.ndarray]:
    """Create exactly 20 explicit particles inside the pumping cell."""

    local_x = (np.arange(5, dtype=float) + 0.5) / 5.0
    local_y = (np.arange(2, dtype=float) + 0.5) / 2.0
    local_z = (np.arange(2, dtype=float) + 0.5) / 2.0

    locs: list[tuple[int, int, int]] = []
    lx: list[float] = []
    ly: list[float] = []
    lz: list[float] = []
    xyz: list[tuple[float, float, float]] = []

    for zloc in local_z:
        for yloc in local_y:
            for xloc in local_x:
                locs.append((WELL_LAYER, WELL_ROW, WELL_COL))
                lx.append(float(xloc))
                ly.append(float(yloc))
                lz.append(float(zloc))
                xyz.append(
                    _cell_xyz(
                        WELL_LAYER,
                        WELL_ROW,
                        WELL_COL,
                        float(xloc),
                        float(yloc),
                        float(zloc),
                    )
                )

    if len(locs) != BACKWARD_PARTICLE_COUNT:
        raise RuntimeError(
            f"Backward particle construction produced {len(locs)} particles; "
            f"expected {BACKWARD_PARTICLE_COUNT}."
        )

    pdata = flopy.modpath.ParticleData(
        partlocs=locs,
        structured=True,
        localx=np.asarray(lx, dtype=float),
        localy=np.asarray(ly, dtype=float),
        localz=np.asarray(lz, dtype=float),
        drape=0,
    )
    return pdata, np.asarray(xyz, dtype=float)


def _forward_particle_data() -> tuple[flopy.modpath.ParticleData, np.ndarray]:
    """Create one explicit particle at the centre of every CHD boundary cell."""

    locs: list[tuple[int, int, int]] = []
    xyz: list[tuple[float, float, float]] = []

    for layer in range(NLAY):
        for row in range(NROW):
            for col in (0, NCOL - 1):
                locs.append((layer, row, col))
                xyz.append(_cell_xyz(layer, row, col, 0.5, 0.5, 0.5))

    if len(locs) != FORWARD_PARTICLE_COUNT:
        raise RuntimeError(
            f"Forward particle construction produced {len(locs)} particles; "
            f"expected {FORWARD_PARTICLE_COUNT}."
        )

    # Scalar local coordinates are intentionally used: every particle starts at
    # the centre of its specified-head cell.
    pdata = flopy.modpath.ParticleData(
        partlocs=locs,
        structured=True,
        localx=0.5,
        localy=0.5,
        localz=0.5,
        drape=0,
    )
    return pdata, np.asarray(xyz, dtype=float)


def _read_pathlines(pathline_file: Path) -> list[ParticleTrack]:
    """Read a MODPATH 7 pathline file and detach all arrays from disk."""

    if not pathline_file.is_file():
        raise RuntimeError(f"Expected MODPATH pathline file was not created: {pathline_file}")

    raw_tracks = flopy.utils.PathlineFile(pathline_file).get_alldata()

    tracks: list[ParticleTrack] = []
    for rec in raw_tracks:
        if rec.size == 0:
            continue
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
    """Remove only files belonging to a previous run of this MP7 model name."""

    for path in workspace.glob(f"{modelname}*"):
        if path.is_file():
            path.unlink(missing_ok=True)


def _load_existing_gwf(workspace: Path, mf6_executable: Path):
    """Reload the already-run MF6 model definition without running MODFLOW."""

    sim = flopy.mf6.MFSimulation.load(
        sim_ws=str(workspace),
        exe_name=str(mf6_executable),
        verbosity_level=0,
    )
    gwf = sim.get_model(MODEL_NAME)
    if gwf is None:
        raise RuntimeError(f"Could not reload groundwater-flow model '{MODEL_NAME}'.")
    return sim, gwf


def _run_one_modpath(
    *,
    gwf,
    workspace: Path,
    executable: Path,
    direction: str,
    particle_data: flopy.modpath.ParticleData,
    start_xyz: np.ndarray,
    porosity: float,
    modelname: str,
) -> TrackingResult:
    """Create and run one pathline simulation using explicit ParticleData."""

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
        # Explicit names make the dependency on the already-run flow solution
        # clear and avoid any ambiguity when the MF6 model is reloaded.
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
            [str(executable), mp.namefile],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=MP7_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"MODPATH ({direction}) exceeded the "
            f"{MP7_TIMEOUT_SECONDS}-second safety timeout."
        ) from exc
    except OSError as exc:
        raise RuntimeError(f"MODPATH ({direction}) could not be started: {exc}") from exc

    runtime = time.perf_counter() - started
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)

    if completed.returncode != 0 or "NORMAL TERMINATION" not in output.upper():
        tail = "\n".join(output.splitlines()[-50:])
        raise RuntimeError(
            f"MODPATH ({direction}) did not terminate normally.\n\n"
            f"Return code: {completed.returncode}\n"
            f"Last MODPATH messages:\n{tail}"
        )

    tracks = _read_pathlines(workspace / f"{modelname}.mppth")

    requested_particles = int(start_xyz.shape[0])
    if start_xyz.ndim != 2 or start_xyz.shape[1] != 3:
        raise RuntimeError(
            f"Invalid {direction} start-coordinate array shape: {start_xyz.shape}."
        )
    if requested_particles <= 0:
        raise RuntimeError(f"No {direction} particles were defined.")

    return TrackingResult(
        direction=direction,
        requested_particles=requested_particles,
        tracks=tracks,
        start_xyz=np.asarray(start_xyz, dtype=float).copy(),
        runtime_seconds=runtime,
        mp7_version=_extract_mp7_version(output),
        stdout=output,
    )


def run_modpath(flow_result: FlowResult, effective_porosity: float = 0.25) -> ModpathResult:
    """Run backward and forward MODPATH using an existing MODFLOW solution.

    MODFLOW is *not* executed in this function.  The function requires the
    persistent workspace returned by ``run_modflow``.
    """

    if not (0.0 < effective_porosity <= 1.0):
        raise ValueError("Effective porosity must be greater than 0 and no more than 1.")

    workspace = Path(flow_result.workspace)
    if not workspace.is_dir():
        raise RuntimeError(
            "The MODFLOW workspace is no longer available. Run MODFLOW again "
            "before running MODPATH."
        )

    # Confirm that the flow files still exist before constructing MP7 input.
    _validate_modflow_outputs(workspace)

    mf6_executable = locate_mf6()
    mp7_executable = locate_mp7()

    # Reload only the model definition. This does not run MF6.
    _sim, gwf = _load_existing_gwf(workspace, mf6_executable)

    backward_data, backward_xyz = _backward_particle_data()
    forward_data, forward_xyz = _forward_particle_data()

    total_started = time.perf_counter()

    backward = _run_one_modpath(
        gwf=gwf,
        workspace=workspace,
        executable=mp7_executable,
        direction="backward",
        particle_data=backward_data,
        start_xyz=backward_xyz,
        porosity=effective_porosity,
        modelname=f"{MODEL_NAME}_mp_backward",
    )

    forward = _run_one_modpath(
        gwf=gwf,
        workspace=workspace,
        executable=mp7_executable,
        direction="forward",
        particle_data=forward_data,
        start_xyz=forward_xyz,
        porosity=effective_porosity,
        modelname=f"{MODEL_NAME}_mp_forward",
    )

    if backward.requested_particles != BACKWARD_PARTICLE_COUNT:
        raise RuntimeError("Backward-particle count does not match the model design.")
    if forward.requested_particles != FORWARD_PARTICLE_COUNT:
        raise RuntimeError("Forward-particle count does not match the model design.")

    return ModpathResult(
        backward=backward,
        forward=forward,
        runtime_seconds=time.perf_counter() - total_started,
        mp7_executable=str(mp7_executable),
        effective_porosity=float(effective_porosity),
        flow_parameter_signature=flow_result.parameter_signature,
    )
