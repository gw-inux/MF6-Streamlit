"""MODFLOW 6 + MODPATH 7 utilities for the Streamlit cloud test.

This version keeps the proven split workflow:

1. ``run_modflow`` builds/runs a steady three-layer MODFLOW 6 model and keeps
   its private temporary workspace alive.
2. ``run_modpath`` reuses that existing flow solution. MODFLOW is not rerun.

The grid size and one to three pumping-well locations are configurable. All
wells are screened in layer 3, and each well has its own pumping rate (entered
as a positive extraction magnitude). Backward tracking releases 60 particles
per well; forward tracking releases one particle in every constant-head cell
on both lateral boundaries.
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

PARTICLES_PER_WELL = 60
BACKWARD_PARTICLE_COUNT = PARTICLES_PER_WELL  # default one-well case
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


def _read_cumulative_budget(workspace: Path) -> list[tuple[str, float]]:
    """Read the final cumulative budget table from the MODFLOW 6 list file.

    Failure to parse the optional diagnostic does not invalidate an otherwise
    successful numerical run; an empty list is returned instead.
    """

    list_file = workspace / f"{MODEL_NAME}.lst"
    if not list_file.is_file():
        return []
    try:
        budget = flopy.utils.Mf6ListBudget(str(list_file), timeunit="days")
        if not budget.isvalid():
            return []
        data = budget.get_data(incremental=False)
        if data is None:
            return []

        # ``ListBudget.get_data`` stores names as a fixed-width byte field.
        # Calling ``str`` on that value produces strings such as
        # ``b'CHD_IN'``, which breaks suffix-based IN/OUT detection in the UI.
        # Decode bytes here so every downstream consumer receives clean labels.
        items: list[tuple[str, float]] = []
        for row in data:
            raw_name = row["name"]
            if isinstance(raw_name, (bytes, np.bytes_)):
                name = raw_name.decode("ascii", errors="replace")
            else:
                name = str(raw_name)
            name = name.replace("\x00", "").strip()
            items.append((name, float(row["value"])))
        return items
    except Exception:
        return []


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


def _backward_particle_data(params: ModelParameters) -> tuple[flopy.modpath.ParticleData, np.ndarray, np.ndarray]:
    # Use a denser 5 x 4 x 3 distribution in each pumping cell.
    # This gives 60 backward particles per well while remaining lightweight.
    local_x = (np.arange(5, dtype=float) + 0.5) / 5.0
    local_y = (np.arange(4, dtype=float) + 0.5) / 4.0
    local_z = (np.arange(3, dtype=float) + 0.5) / 3.0

    locs: list[tuple[int, int, int]] = []
    lx: list[float] = []
    ly: list[float] = []
    lz: list[float] = []
    xyz: list[tuple[float, float, float]] = []
    layers: list[int] = []

    for row, col in params.well_positions:
        for zloc in local_z:
            for yloc in local_y:
                for xloc in local_x:
                    locs.append((WELL_LAYER, row, col))
                    lx.append(float(xloc)); ly.append(float(yloc)); lz.append(float(zloc))
                    xyz.append(_cell_xyz(params, WELL_LAYER, row, col, float(xloc), float(yloc), float(zloc)))
                    layers.append(WELL_LAYER)

    if len(locs) != params.backward_particle_count:
        raise RuntimeError(
            f"Backward particle construction produced {len(locs)} particles; "
            f"expected {params.backward_particle_count}."
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


def run_modpath(flow_result: FlowResult, effective_porosity: float = 0.25) -> ModpathResult:
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

    backward_data, backward_xyz, backward_layers = _backward_particle_data(params)
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
