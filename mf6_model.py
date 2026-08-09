"""MODFLOW 6 + MODPATH 7 model utilities for the Streamlit cloud test.

The numerical model is intentionally kept separate from Streamlit.  One call to
``run_model`` creates a temporary workspace, runs MODFLOW 6, runs two MODPATH 7
particle-tracking simulations, reads all required results into memory, and then
removes the temporary files.

Particle-tracking configurations
--------------------------------
1. Backward tracking from the pumping well:
   20 particles are distributed inside the pumping cell (5 x 2 x 2).
2. Forward tracking from the specified-head boundaries:
   one particle is placed in every left- and right-boundary cell
   (3 layers x 21 rows x 2 sides = 126 particles).
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

WELL_LAYER = 2  # zero-based index -> layer 3
WELL_ROW = NROW // 2
WELL_COL = NCOL // 2

MF6_TIMEOUT_SECONDS = 20
MP7_TIMEOUT_SECONDS = 20

BACKWARD_PARTICLE_COUNT = 20
FORWARD_PARTICLE_COUNT = NLAY * NROW * 2


@dataclass(frozen=True)
class ModelParameters:
    """Parameters exposed by the Streamlit interface.

    Pumping is entered as a positive extraction magnitude in m3/day.  The WEL
    package receives the corresponding negative MODFLOW flow rate.

    Effective porosity does not affect the MODFLOW heads.  MODPATH requires it
    to calculate particle velocities and travel times.  For steady-state flow,
    changing porosity changes travel time but not the geometric streamline.
    """

    head_left: float = 32.0
    head_right: float = 31.0
    pumping_rate: float = 300.0
    k_layer1: float = 10.0
    k_layer2: float = 0.10
    k_layer3: float = 5.0
    vertical_anisotropy: float = 0.10
    effective_porosity: float = 0.25

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
            self.effective_porosity,
        )


@dataclass
class ParticleTrack:
    """One MODPATH pathline copied out of the temporary workspace."""

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
class ModelResult:
    """Results returned after successful MODFLOW and MODPATH runs."""

    head: np.ndarray
    runtime_seconds: float
    mf6_runtime_seconds: float
    mf6_executable: str
    mf6_version: str
    mf6_stdout: str
    mp7_executable: str
    backward: TrackingResult
    forward: TrackingResult


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
    """Locate one bundled/native executable using a common resolution order."""

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
    """Locate the MODFLOW 6 executable."""

    return _locate_executable(
        env_var="MF6_EXE",
        linux_name="mf6",
        windows_name="mf6.exe",
        display_name="MODFLOW 6",
    )


def locate_mp7() -> Path:
    """Locate the MODPATH 7 executable."""

    return _locate_executable(
        env_var="MP7_EXE",
        linux_name="mp7",
        windows_name="mp7.exe",
        display_name="MODPATH 7",
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


def _extract_mp7_version(output: str) -> str:
    """Extract the MODPATH version line from normal program output."""

    for line in output.splitlines():
        if "MODPATH VERSION" in line.upper():
            return line.strip()
    return "MODPATH version not reported"


def _initial_head(params: ModelParameters) -> np.ndarray:
    """Create a linear left-to-right initial head field for all three layers."""

    line = np.linspace(params.head_left, params.head_right, NCOL)
    return np.broadcast_to(line, (NLAY, NROW, NCOL)).copy()


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

    # Horizontal conductivity differs by layer. K33 is vertical hydraulic
    # conductivity; a ratio below 1 represents vertical anisotropy.
    k = np.empty((NLAY, NROW, NCOL), dtype=float)
    k[0, :, :] = params.k_layer1
    k[1, :, :] = params.k_layer2
    k[2, :, :] = params.k_layer3
    k33 = k * params.vertical_anisotropy

    flopy.mf6.ModflowGwfnpf(
        gwf,
        icelltype=0,  # all cells confined: intentionally simple for this test
        k=k,
        k33=k33,
        save_flows=True,
        save_specific_discharge=True,
    )

    # Specified-head boundaries are applied to the complete left and right model
    # faces in all layers. This creates a regional left-to-right gradient.
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

    # MODPATH 7 needs both binary heads and cell-by-cell flow information.
    # The DIS binary grid file (*.grb) is written automatically by MODFLOW 6.
    flopy.mf6.ModflowGwfoc(
        gwf,
        head_filerecord=[f"{MODEL_NAME}.hds"],
        budget_filerecord=[f"{MODEL_NAME}.cbc"],
        saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
        printrecord=[("HEAD", "LAST"), ("BUDGET", "LAST")],
    )

    return sim


def _node_number(layer: int, row: int, col: int) -> int:
    """Return the zero-based MODPATH node number for a structured DIS cell."""

    return layer * NROW * NCOL + row * NCOL + col


def _backward_nodes() -> list[int]:
    """Return the single pumping-cell node used for backward tracking."""

    return [_node_number(WELL_LAYER, WELL_ROW, WELL_COL)]


def _forward_boundary_nodes() -> list[int]:
    """Return every left- and right-CHD cell as a MODPATH starting node."""

    nodes: list[int] = []
    for layer in range(NLAY):
        for row in range(NROW):
            nodes.append(_node_number(layer, row, 0))
            nodes.append(_node_number(layer, row, NCOL - 1))
    return nodes


def _read_pathlines(pathline_file: Path) -> list[ParticleTrack]:
    """Read a MODPATH 7 pathline file and detach it from the workspace."""

    if not pathline_file.is_file():
        raise RuntimeError(f"Expected MODPATH pathline file was not created: {pathline_file}")

    pathline_reader = flopy.utils.PathlineFile(pathline_file)
    raw_tracks = pathline_reader.get_alldata()

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


def _run_modpath(
    *,
    gwf: flopy.mf6.ModflowGwf,
    workspace: Path,
    executable: Path,
    direction: str,
    nodes: list[int],
    column_divisions: int,
    row_divisions: int,
    layer_divisions: int,
    porosity: float,
    modelname: str,
) -> TrackingResult:
    """Create, execute, validate, and read one MODPATH 7 simulation."""

    # FloPy accepts node numbers as an integer, nested sequence, or NumPy array.
    # A flat Python list containing exactly one node (for example [well_node])
    # is an awkward corner case in NodeParticleData: it can be interpreted as
    # an incompletely nested node specification and raises a TypeError.
    # Normalizing to a 1-D NumPy integer array avoids that ambiguity and works
    # identically for both the single-node backward case and the many-node
    # forward case.
    node_spec = np.asarray(nodes, dtype=np.int32)

    mp = flopy.modpath.Modpath7.create_mp7(
        modelname=modelname,
        trackdir=direction,
        flowmodel=gwf,
        exe_name=str(executable),
        model_ws=str(workspace),
        columncelldivisions=column_divisions,
        rowcelldivisions=row_divisions,
        layercelldivisions=layer_divisions,
        nodes=node_spec,
        porosity=porosity,
    )

    # Compute the explicit release coordinates before running.  They are useful
    # for plotting starting points after the temporary workspace is deleted.
    # The convenience constructor uses a NodeParticleData template internally.
    # Accessing the package internals is unnecessary: recreate the same template
    # explicitly only for coordinate calculation.
    subdivision = flopy.modpath.CellDataType(
        columncelldivisions=column_divisions,
        rowcelldivisions=row_divisions,
        layercelldivisions=layer_divisions,
    )
    release_data = flopy.modpath.NodeParticleData(
        subdivisiondata=subdivision,
        nodes=node_spec,
    )
    start_xyz = np.asarray(list(release_data.to_coords(gwf.modelgrid)), dtype=float)

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
            f"MODPATH exceeded the {MP7_TIMEOUT_SECONDS}-second safety timeout."
        ) from exc
    except OSError as exc:
        raise RuntimeError(f"MODPATH could not be started: {exc}") from exc

    runtime = time.perf_counter() - started
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)

    normal_termination = "NORMAL TERMINATION" in output.upper()
    if completed.returncode != 0 or not normal_termination:
        tail = "\n".join(output.splitlines()[-50:])
        raise RuntimeError(
            f"MODPATH ({direction}) did not terminate normally.\n\n"
            f"Return code: {completed.returncode}\n"
            f"Last MODPATH messages:\n{tail}"
        )

    tracks = _read_pathlines(workspace / f"{modelname}.mppth")

    expected_particles = len(nodes) * column_divisions * row_divisions * layer_divisions
    if start_xyz.shape != (expected_particles, 3):
        raise RuntimeError(
            f"Unexpected number of {direction} particle release points: "
            f"{start_xyz.shape[0]}; expected {expected_particles}."
        )

    return TrackingResult(
        direction=direction,
        requested_particles=expected_particles,
        tracks=tracks,
        start_xyz=start_xyz.copy(),
        runtime_seconds=runtime,
        mp7_version=_extract_mp7_version(output),
        stdout=output,
    )


def run_model(params: ModelParameters) -> ModelResult:
    """Run MODFLOW 6 and both requested MODPATH 7 tracking configurations.

    The complete workflow stays inside one temporary directory because MODPATH
    requires MODFLOW's binary head, budget, and grid files.  Results are copied
    into NumPy arrays before that directory is removed.
    """

    mf6_executable = locate_mf6()
    mp7_executable = locate_mp7()
    mf6_version = get_mf6_version(mf6_executable)

    total_started = time.perf_counter()

    with tempfile.TemporaryDirectory(prefix="mf6_mp7_streamlit_") as temp_dir:
        workspace = Path(temp_dir)
        sim = build_simulation(params, workspace, mf6_executable)
        sim.write_simulation()

        mf6_started = time.perf_counter()
        try:
            completed = subprocess.run(
                [str(mf6_executable)],
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
        mf6_runtime = time.perf_counter() - mf6_started

        mf6_output = "\n".join(
            part for part in (completed.stdout, completed.stderr) if part
        )

        normal_termination = "NORMAL TERMINATION OF SIMULATION" in mf6_output.upper()
        if completed.returncode != 0 or not normal_termination:
            tail = "\n".join(mf6_output.splitlines()[-40:])
            raise RuntimeError(
                "MODFLOW did not terminate normally.\n\n"
                f"Return code: {completed.returncode}\n"
                f"Last MODFLOW messages:\n{tail}"
            )

        head_file = workspace / f"{MODEL_NAME}.hds"
        budget_file = workspace / f"{MODEL_NAME}.cbc"
        if not head_file.is_file() or not budget_file.is_file():
            raise RuntimeError(
                "MODFLOW terminated normally, but the head/budget files required "
                "for MODPATH were not created."
            )

        head = flopy.utils.HeadFile(head_file).get_data()
        head = np.asarray(head, dtype=float).copy()

        if head.shape != (NLAY, NROW, NCOL):
            raise RuntimeError(
                f"Unexpected head-array shape {head.shape}; expected {(NLAY, NROW, NCOL)}."
            )
        if not np.all(np.isfinite(head)):
            raise RuntimeError("The MODFLOW head array contains non-finite values.")

        # MODPATH must receive the GWF object that generated the head/budget files.
        gwf = sim.get_model(MODEL_NAME)

        # 20 particles in the pumping cell: 5 x 2 x 2 subdivisions.
        backward = _run_modpath(
            gwf=gwf,
            workspace=workspace,
            executable=mp7_executable,
            direction="backward",
            nodes=_backward_nodes(),
            column_divisions=5,
            row_divisions=2,
            layer_divisions=2,
            porosity=params.effective_porosity,
            modelname=f"{MODEL_NAME}_mp_backward",
        )

        # One particle at the centre of every CHD cell on both lateral faces.
        forward = _run_modpath(
            gwf=gwf,
            workspace=workspace,
            executable=mp7_executable,
            direction="forward",
            nodes=_forward_boundary_nodes(),
            column_divisions=1,
            row_divisions=1,
            layer_divisions=1,
            porosity=params.effective_porosity,
            modelname=f"{MODEL_NAME}_mp_forward",
        )

        if backward.requested_particles != BACKWARD_PARTICLE_COUNT:
            raise RuntimeError("Backward-particle count does not match the model design.")
        if forward.requested_particles != FORWARD_PARTICLE_COUNT:
            raise RuntimeError("Forward-particle count does not match the model design.")

    total_runtime = time.perf_counter() - total_started

    return ModelResult(
        head=head,
        runtime_seconds=total_runtime,
        mf6_runtime_seconds=mf6_runtime,
        mf6_executable=str(mf6_executable),
        mf6_version=mf6_version,
        mf6_stdout=mf6_output,
        mp7_executable=str(mp7_executable),
        backward=backward,
        forward=forward,
    )
