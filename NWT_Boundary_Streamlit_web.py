"""RIV, DRN, GHB and EVT boundaries: a small, steady MODFLOW-NWT teaching model.

Cloud entrypoint: NWT_Boundary_Streamlit_web.py
Run: python -m streamlit run NWT_Boundary_Streamlit_web.py
Place beside the other apps in MF6-Streamlit; reuse its existing bin/mfnwt.
This cloud variant changes executable resolution only; model/UI behavior
matches the reviewed local version 1.2.0.

TABLE OF CONTENTS (search for the numbered headings below)
  01. Constants, defaults and grid geometry
  02. Input validation and boundary equations
  03. Executable resolution and MODFLOW model construction
  04. Execution, output checks and water budget
  05. Run history and Q-h series management
  06. Cross-section, budget and Q-h figures
  07. Streamlit style and input controls
  08. Post-processing, downloads and deletion controls
  09. Main interface

Maintenance notes
-----------------
* All model quantities use metres and seconds; only displayed flow rates are
  converted to m3/day. C is TOTAL conductance over the 100 m boundary strip.
* Uniform spacing can be 100, 50, 20, 10 or 5 m. CHD centres stay at 0 and
  1000 m; the boundary stays at x=450...550 m. Edge overlaps conserve its area.
* The single row represents 1 m along the river. The layer is convertible
  (unconfined); other than the two CHDs and chosen boundary, faces are no-flow.
* Q-h uses area-weighted groundwater head across the boundary strip. With
  the original 100 m grid this is the single middle-cell head. Q sums all
  boundary-cell rates; mixed regimes on refined grids must not be collapsed
  into a single-cell law. EVT uses 365.25 days per year for mm/a conversion.
* Numerical functions do not depend on Streamlit. State stores ordinary
  dictionaries so it survives script reruns without dataclass identity issues.
* Only successful, checked runs enter history. Each subprocess has its own
  temporary directory and a timeout. No shared simulation directories/caches.
* Interface and budget style follow the user's Fieldcase and NWT cross-section
  apps. No executable-location widget is exposed to learners.
"""
from __future__ import annotations

import colorsys
import csv
import io
import inspect
import json
import math
import os
import re
import shutil
import stat
import subprocess
import tempfile
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
import numpy as np


# =============================================================================
# 01. CONSTANTS, DEFAULTS AND GRID GEOMETRY
# =============================================================================
APP_VERSION = "1.2.1-cloud"
ROOT = Path(__file__).resolve().parent
MODEL_NAME = "river_demo"
SEC_DAY = 86400.0
SEC_YEAR = 365.25 * SEC_DAY
MODEL_LENGTH = 1000.0
BOUNDARY_LEFT, BOUNDARY_RIGHT = 450.0, 550.0
BOUNDARY_WIDTH = BOUNDARY_RIGHT - BOUNDARY_LEFT
GRID_SIZES = (100., 50., 20., 10., 5.)
# Default-grid aliases retained for older numerical checks; model code uses model_grid(p).
NCOL, BOUNDARY_CELL = 11, 5                 # zero-based middle-cell index
DX, ROW_WIDTH = 100.0, 1.0                  # metres
TOP, BOTTOM = 30.0, 0.0
X = np.arange(NCOL, dtype=float) * DX       # 0, 100, ..., 1000 m
EDGES = np.arange(NCOL + 1) * DX - DX / 2   # -50, 50, ..., 1050 m
MIN_RUNS_FOR_LINE = 4                       # distinct end-head settings
RUN_TIMEOUT_SECONDS = 30
MAX_BUDGET_DISCREPANCY_PERCENT = 1.0
INITIAL_Q_AXIS_LIMIT = 100.0                # symmetric m³/day; expands only
BOUNDARY_LABELS = {"RIV": "River (RIV)", "DRN": "Drain (DRN)",
                   "GHB": "General-head (GHB)", "EVT": "Evapotranspiration (EVT)"}
BUDGET_TERMS = {"RIV": "RIVER LEAKAGE", "DRN": "DRAINS", "GHB": "HEAD DEP BOUNDS",
                "EVT": "ET"}
BOUNDARY_MARKERS = {"RIV": "o", "GHB": "s", "DRN": "x", "EVT": "^"}
PALETTE = ("#1f77b4", "#d17a22", "#29834c", "#aa4499", "#bd4545",
           "#238d9c", "#876444", "#5c62ab", "#858720", "#b85b80")


@dataclass(frozen=True)
class ModelInputs:
    k_m_s: float = 1e-3
    end_head_m: float = 25.0
    boundary_head_m: float = 20.0
    river_bottom_m: float = 18.0
    conductance_m2_s: float = 1e-4
    boundary_type: str = "RIV"
    cell_size_m: float = 100.0
    max_et_mm_year: float = 250.0
    et_surface_m: float = 20.0
    extinction_depth_m: float = 5.0


@dataclass(frozen=True)
class SolverSettings:
    headtol_m: float = 1e-4
    fluxtol_m3_s: float = 1e-4
    maxiterout: int = 500
    preset: str = "COMPLEX"



@dataclass(frozen=True)
class GridGeometry:
    """Uniform node-centered grid and exact overlap with the fixed boundary."""
    dx: float
    x: np.ndarray
    edges: np.ndarray
    overlap_m: np.ndarray

    @property
    def ncol(self) -> int:
        return len(self.x)

    @property
    def weights(self) -> np.ndarray:
        return self.overlap_m / BOUNDARY_WIDTH

    @property
    def boundary_cells(self) -> np.ndarray:
        return np.flatnonzero(self.overlap_m > 0)


def model_grid(p: ModelInputs) -> GridGeometry:
    dx = p.cell_size_m
    ncol = int(round(MODEL_LENGTH / dx)) + 1
    x = np.arange(ncol, dtype=float) * dx
    edges = np.arange(ncol + 1, dtype=float) * dx - dx/2
    overlap = np.maximum(0., np.minimum(edges[1:], BOUNDARY_RIGHT)
                         - np.maximum(edges[:-1], BOUNDARY_LEFT))
    return GridGeometry(dx, x, edges, overlap)


def boundary_mean_head(result: dict) -> float:
    p = ModelInputs(**result["inputs"])
    return float(np.dot(model_grid(p).weights, result["heads"]))


def zero_exchange_expected(p: ModelInputs) -> bool:
    if p.boundary_type == "EVT":
        return p.max_et_mm_year == 0 or p.end_head_m <= p.et_surface_m-p.extinction_depth_m
    if p.boundary_type == "DRN":
        return p.end_head_m <= p.boundary_head_m
    return abs(p.end_head_m-p.boundary_head_m) < 1e-12


def boundary_head_slope(p: ModelInputs) -> float:
    """Largest absolute dQ/dh for the entire 100 m strip, in m2/s."""
    if p.boundary_type == "EVT":
        return (p.max_et_mm_year / 1000 / SEC_YEAR * BOUNDARY_WIDTH * ROW_WIDTH
                / p.extinction_depth_m)
    return p.conductance_m2_s


def boundary_thresholds(p: ModelInputs) -> list[float]:
    if p.boundary_type == "RIV":
        return [p.river_bottom_m]
    if p.boundary_type == "DRN":
        return [p.boundary_head_m]
    if p.boundary_type == "EVT":
        return [p.et_surface_m-p.extinction_depth_m, p.et_surface_m]
    return []


# =============================================================================
# 02. INPUT VALIDATION AND BOUNDARY EQUATIONS
# =============================================================================
def validate_inputs(p: ModelInputs, solver: SolverSettings) -> None:
    if p.boundary_type not in BOUNDARY_LABELS:
        raise ValueError("Choose RIV, DRN, GHB or EVT as the boundary type.")
    numeric = (p.k_m_s, p.end_head_m, p.boundary_head_m,
               p.river_bottom_m, p.conductance_m2_s, p.cell_size_m,
               p.max_et_mm_year, p.et_surface_m, p.extinction_depth_m)
    if not all(math.isfinite(v) for v in numeric):
        raise ValueError("All model inputs must be finite numbers.")
    if p.cell_size_m not in GRID_SIZES:
        raise ValueError("Choose a cell size of 100, 50, 20, 10 or 5 m.")
    if p.boundary_type == "EVT":
        if not 0 <= p.max_et_mm_year <= 500:
            raise ValueError("Maximum ET must be between 0 and 500 mm/a.")
        if not BOTTOM <= p.et_surface_m <= TOP:
            raise ValueError("ET surface must be between 0 and 30 m.")
        if not 0.1 <= p.extinction_depth_m <= TOP-BOTTOM:
            raise ValueError("ET extinction depth must be between 0.1 and 30 m.")
    if not 1e-5 <= p.k_m_s <= 1e-2:
        raise ValueError("Hydraulic conductivity must be between 1e-5 and 1e-2 m/s.")
    if not 1.0 <= p.end_head_m <= TOP:
        raise ValueError("The common specified head must be between 1 and 30 m.")
    if not 0.1 <= p.boundary_head_m <= TOP:
        raise ValueError("Boundary head must be between 0.1 and 30 m.")
    if p.boundary_type == "RIV" and not BOTTOM <= p.river_bottom_m < p.boundary_head_m:
        raise ValueError("River bottom must be at least 0 m and lower than the river stage.")
    if not 1e-6 <= p.conductance_m2_s <= 1e-2:
        raise ValueError("Conductance must be between 1e-6 and 1e-2 m²/s.")
    if not (math.isfinite(solver.headtol_m) and 1e-8 <= solver.headtol_m <= 1e-3
            and math.isfinite(solver.fluxtol_m3_s)
            and 1e-12 <= solver.fluxtol_m3_s <= 1e-3
            and 1 <= solver.maxiterout <= 5000
            and solver.preset in ("SIMPLE", "MODERATE", "COMPLEX")):
        raise ValueError("Invalid NWT solver settings.")


def boundary_flux_m3_s(head_m, p: ModelInputs):
    """Whole-strip package law for uniform h; positive enters groundwater.

    Multiply by each cell's overlap weight for distributed, nonuniform heads.
    EVT's maximum rate is converted from mm/a to m/s and multiplied by area.
    """
    h = np.asarray(head_m)
    if p.boundary_type == "EVT":
        qmax = p.max_et_mm_year / 1000 / SEC_YEAR * BOUNDARY_WIDTH * ROW_WIDTH
        fraction = np.clip((h-(p.et_surface_m-p.extinction_depth_m))/p.extinction_depth_m, 0., 1.)
        return -qmax * fraction
    if p.boundary_type == "RIV":
        return p.conductance_m2_s * (p.boundary_head_m - np.maximum(h, p.river_bottom_m))
    if p.boundary_type == "DRN":
        return -p.conductance_m2_s * np.maximum(h - p.boundary_head_m, 0.0)
    return p.conductance_m2_s * (p.boundary_head_m - h)


def starting_heads(p: ModelInputs) -> np.ndarray:
    """Perturb zero-flow initial guesses where needed to avoid GMRES breakdown.

    All CHD and package data remain unchanged. The preview shows this guess.
    """
    grid = model_grid(p)
    heads = np.full(grid.ncol, p.end_head_m, dtype=float)
    if zero_exchange_expected(p) and (p.boundary_type in ("DRN", "EVT") or p.cell_size_m < 100):
        increment = 0.01 if p.end_head_m < TOP-0.01 else -0.01
        heads[1:-1] += increment * np.sin(np.pi * grid.x[1:-1] / MODEL_LENGTH)
    return heads


def series_signature(p: ModelInputs) -> tuple:
    """End head samples a series; only active package data define a new series."""
    if p.boundary_type == "EVT":
        data = (p.max_et_mm_year, p.et_surface_m, p.extinction_depth_m)
    else:
        data = (p.boundary_head_m, p.conductance_m2_s,
                p.river_bottom_m if p.boundary_type == "RIV" else None)
    return (p.boundary_type, p.k_m_s, p.cell_size_m, *data)


# =============================================================================
# 03. EXECUTABLE RESOLUTION AND MODFLOW MODEL CONSTRUCTION
# =============================================================================
def _usable_mfnwt_binary(path: Path) -> str:
    """Use the installed solver, restoring its Linux execute bit if needed.

    This follows the existing cloud apps' repository-bin approach. It never
    downloads a program and never changes model or solver parameters.
    """
    path = path.resolve()
    if not path.is_file():
        raise RuntimeError("The configured MODFLOW-NWT program is unavailable.")
    if os.name != "nt":
        try:
            with path.open("rb") as binary:
                prefix = binary.read(4)
        except OSError as exc:
            raise RuntimeError("The configured MODFLOW-NWT program cannot be read.") from exc
        if prefix[:2] == b"MZ":
            raise RuntimeError("The configured MODFLOW-NWT program is a Windows executable; "
                               "this deployment requires a Linux executable.")
        if not os.access(path, os.X_OK):
            try:
                path.chmod(path.stat().st_mode | stat.S_IXUSR)
            except OSError as exc:
                raise RuntimeError("MODFLOW-NWT does not have execute permission in this deployment.") from exc
            if not os.access(path, os.X_OK):
                raise RuntimeError("MODFLOW-NWT does not have execute permission in this deployment.")
    return str(path)


def find_mfnwt_executable() -> str | None:
    """Resolve the shared repository solver independently of the run workspace.

    Place this app beside the other apps in MF6-Streamlit. The expected Linux
    executable is bin/mfnwt (or bin/mfnwtdbl). A parent/cwd bin folder supports
    an entrypoint in a subfolder, matching the existing Fieldcase cloud app.
    MFNWT_EXECUTABLE remains an optional administrator override, not a widget.
    """
    override = os.environ.get("MFNWT_EXECUTABLE")
    if override:
        direct = Path(override).expanduser()
        candidates = [direct] if direct.is_absolute() else [ROOT/direct, Path.cwd()/direct]
        for candidate in candidates:
            if candidate.is_file():
                return _usable_mfnwt_binary(candidate)
        found = shutil.which(override)
        if found:
            return _usable_mfnwt_binary(Path(found))
        raise RuntimeError("The configured MODFLOW-NWT program is unavailable.")
    names = (["MODFLOW-NWT_64.exe", "MODFLOW-NWT_64", "mfnwt.exe",
              "mfnwt", "mfnwtdbl.exe"] if os.name == "nt"
             else ["mfnwt", "mfnwtdbl", "MODFLOW-NWT_64.exe"])
    folders = [ROOT/"bin", ROOT.parent/"bin", Path.cwd()/"bin", ROOT]
    seen, errors = set(), []
    for folder in folders:
        for name in names:
            candidate = (folder/name).resolve()
            if candidate in seen:
                continue
            seen.add(candidate)
            if candidate.is_file():
                try:
                    return _usable_mfnwt_binary(candidate)
                except (OSError, RuntimeError) as exc:
                    errors.append(exc)
    for name in names:
        found = shutil.which(name)
        if found:
            try:
                return _usable_mfnwt_binary(Path(found))
            except (OSError, RuntimeError) as exc:
                errors.append(exc)
    if errors:
        raise RuntimeError(str(errors[0])) from errors[0]
    return None



def build_model(p: ModelInputs, solver: SolverSettings, workspace: Path,
                executable: str):
    """Construct one layer and one row at the selected node spacing with FloPy."""
    import flopy
    validate_inputs(p, solver)
    grid = model_grid(p)
    model = flopy.modflow.Modflow(MODEL_NAME, version="mfnwt",
                                 model_ws=str(workspace), exe_name=executable)
    flopy.modflow.ModflowDis(
        model, nlay=1, nrow=1, ncol=grid.ncol, nper=1, delr=grid.dx, delc=ROW_WIDTH,
        top=TOP, botm=BOTTOM, perlen=1.0, nstp=1, steady=True,
        itmuni=1, lenuni=2, xul=-grid.dx / 2, yul=ROW_WIDTH)
    flopy.modflow.ModflowBas(model, ibound=1, strt=starting_heads(p).reshape(1, 1, grid.ncol))
    flopy.modflow.ModflowUpw(
        model, laytyp=1, layavg=0, hk=p.k_m_s, vka=p.k_m_s,
        sy=0.2, ss=1e-5, ipakcb=53, hdry=-1e30, iphdry=1)
    # CHD makes the first and last cells fixed-head cells during stress period 1.
    flopy.modflow.ModflowChd(model, stress_period_data={0: [
        [0, 0, j, p.end_head_m, p.end_head_m] for j in (0, grid.ncol - 1)]})
    if p.boundary_type == "EVT":
        # EVTR is an areal rate; NWT multiplies it by the FULL cell area.
        # Edge-cell fractions restrict ET to the exact 100 m footprint.
        rates = p.max_et_mm_year / 1000 / SEC_YEAR * grid.overlap_m / grid.dx
        flopy.modflow.ModflowEvt(model, nevtop=1, ipakcb=53,
            surf=p.et_surface_m, evtr=rates.reshape(1, grid.ncol), exdp=p.extinction_depth_m)
    else:
        records = [[0, 0, int(j), p.boundary_head_m,
                    p.conductance_m2_s*grid.weights[j]] for j in grid.boundary_cells]
        if p.boundary_type == "RIV":
            records = [r + [p.river_bottom_m] for r in records]
            flopy.modflow.ModflowRiv(model, ipakcb=53, stress_period_data={0: records})
        elif p.boundary_type == "DRN":
            flopy.modflow.ModflowDrn(model, ipakcb=53, stress_period_data={0: records})
        else:
            flopy.modflow.ModflowGhb(model, ipakcb=53, stress_period_data={0: records})
    flopy.modflow.ModflowNwt(
        model, headtol=solver.headtol_m, fluxtol=solver.fluxtol_m3_s,
        maxiterout=solver.maxiterout, linmeth=1, iprnwt=1, ibotav=0,
        options=solver.preset, Continue=False)
    flopy.modflow.ModflowOc(model, compact=True, stress_period_data={(0, 0):
        ["save head", "save budget", "print budget"]})
    model.write_input()
    return model


# =============================================================================
# 04. EXECUTION, OUTPUT CHECKS AND WATER BUDGET
# =============================================================================
class SimulationError(RuntimeError):
    """Failure with diagnostic text; never converted into an accepted result."""
    def __init__(self, message: str, diagnostics: str = ""):
        super().__init__(message)
        self.diagnostics = diagnostics


def read_listing_budget(path: Path, boundary_type: str = "RIV") -> dict:
    """Read incremental RATE columns, not cumulative stress-period volumes."""
    import flopy
    reader = flopy.utils.MfListBudget(str(path), timeunit="seconds")
    rows = reader.get_incremental()
    if rows is None or not len(rows):
        raise ValueError("The MODFLOW listing contains no water-budget record.")
    row = rows[-1]
    values = {re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_"):
              float(row[name]) for name in rows.dtype.names}

    def require(name):
        value = values.get(name)
        if value is None or not math.isfinite(value):
            raise ValueError(f"Missing or invalid listing-budget term: {name}.")
        return value

    token = BUDGET_TERMS[boundary_type].replace(" ", "_")
    return {
        "chd_in": require("CONSTANT_HEAD_IN"),
        "chd_out": require("CONSTANT_HEAD_OUT"),
        "boundary_in": require(token + "_IN"),
        "boundary_out": require(token + "_OUT"),
        "total_in": require("TOTAL_IN"),
        "total_out": require("TOTAL_OUT"),
        "percent_discrepancy": require("PERCENT_DISCREPANCY"),
    }


def read_cbc_term(reader, label: str, ncol: int = NCOL) -> np.ndarray:
    records = reader.get_data(kstpkper=(0, 0), text=label, full3D=True)
    if len(records) != 1:
        raise ValueError(f"Expected one cell-budget record for {label}.")
    array = np.asarray(np.ma.filled(records[0], 0.0), dtype=float)
    # EVT with NEVTOP=1 writes an IMETH=4 horizontal array. FloPy leaves this
    # record two-dimensional even with full3D=True. This model has one layer.
    if label == "ET" and array.shape == (1, ncol):
        array = array.reshape(1, 1, ncol)
    if array.shape != (1, 1, ncol) or not np.all(np.isfinite(array)):
        raise ValueError(f"Invalid cell-budget array for {label}.")
    return array[0, 0]


def check_outputs(heads: np.ndarray, boundary: np.ndarray, chd: np.ndarray,
                  budget: dict, p: ModelInputs,
                  solver: SolverSettings = SolverSettings()) -> None:
    """Reject missing/dry output, poor balance and inconsistent boundary exchange."""
    grid = model_grid(p)
    if heads.shape != (grid.ncol,) or not np.all(np.isfinite(heads)):
        raise ValueError("Invalid head output.")
    if np.any(heads <= BOTTOM) or np.any(np.abs(heads) > 1e20):
        raise ValueError("The model contains dry or invalid heads.")
    if not np.allclose(heads[[0, -1]], p.end_head_m, atol=2e-5, rtol=0):
        raise ValueError("Computed end heads do not match the specified heads.")
    # A theoretically inactive drain can retain a tiny outflow after NWT stops.
    # A relative budget is ill-conditioned at zero flow. Require uniform heads
    # within HEADTOL, and limit every absolute exchange using the conductances
    # times that head tolerance (never more than FLUXTOL). RIV/GHB on the
    # original 100 m grid retain their previous 1e-8 m3/s equilibrium limit.
    # Refined grids use their smaller CHD spacing. No raw rate is set to zero.
    zero_flow_limit = 1e-8
    if p.boundary_type in ("DRN", "EVT") or p.cell_size_m < 100:
        end_face_conductance = p.k_m_s * ROW_WIDTH * TOP / grid.dx
        zero_flow_limit = min(solver.fluxtol_m3_s, max(1e-8,
            (boundary_head_slope(p) + 2*end_face_conductance) * solver.headtol_m))
    zero_expected = zero_exchange_expected(p)
    near_zero = (zero_expected
                 and np.max(np.abs(heads - p.end_head_m)) <= solver.headtol_m
                 and max(budget["total_in"], budget["total_out"],
                         float(np.max(np.abs(boundary))), float(np.max(np.abs(chd)))) <= zero_flow_limit)
    budget["near_zero_flow"] = bool(near_zero)
    if not near_zero and abs(budget["percent_discrepancy"]) > MAX_BUDGET_DISCREPANCY_PERCENT:
        raise ValueError("Listing-file budget discrepancy exceeds 1%; "
                         "this run has not been added to the Q–h plot.")
    # Check every boundary cell, then aggregate; a single mean head cannot
    # represent mixed RIV/DRN/EVT regimes across a refined boundary strip.
    expected = boundary_flux_m3_s(heads, p) * grid.weights
    equation_tol = np.maximum(1e-10, np.maximum(np.abs(expected)*2e-5,
        boundary_head_slope(p)*grid.weights*np.maximum(np.abs(heads), 1)*5e-7))
    if np.any(np.abs(boundary-expected) > equation_tol):
        raise ValueError("The computed boundary exchange does not match its package equation.")
    for term, prefix in ((boundary, "boundary"), (chd, "chd")):
        listed = budget[f"{prefix}_in"] - budget[f"{prefix}_out"]
        if not np.isclose(term.sum(), listed, rtol=5e-4, atol=1e-10):
            raise ValueError(f"Listing and binary {prefix.upper()} budgets disagree.")
    # Guard against a listing value rounded to 0.00% concealing a large error.
    q_in = sum(np.maximum(a, 0).sum() for a in (boundary, chd))
    q_out = sum(-np.minimum(a, 0).sum() for a in (boundary, chd))
    scale = 0.5 * (q_in + q_out)
    if not near_zero and scale > 1e-10 and abs(q_in - q_out) / scale > 0.01:
        raise ValueError("Binary water-budget discrepancy exceeds 1%.")


def run_model(p: ModelInputs, solver: SolverSettings,
              executable: str | None = None) -> dict:
    """Run NWT, validate outputs, and return a self-contained result snapshot."""
    import flopy
    validate_inputs(p, solver)
    executable = executable or find_mfnwt_executable()
    if executable is None:
        raise SimulationError("MODFLOW-NWT is unavailable. The model cannot run.")
    grid = model_grid(p)
    log, listing_text = "", ""
    with tempfile.TemporaryDirectory(prefix="riv_nwt_") as folder:
        workspace = Path(folder)
        try:
            build_model(p, solver, workspace, executable)
            completed = subprocess.run(
                [executable, f"{MODEL_NAME}.nam"], cwd=workspace,
                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                errors="replace", timeout=RUN_TIMEOUT_SECONDS, check=False)
            log = completed.stdout
            listing_path = workspace / f"{MODEL_NAME}.list"
            if listing_path.exists():
                listing_text = listing_path.read_text(errors="replace")
            combined = log + "\n" + listing_text
            failed = re.search(r"failed to (?:converge|meet solver)|failure to converge",
                               combined, flags=re.I)
            if completed.returncode != 0 or "normal termination" not in combined.lower() or failed:
                raise ValueError("MODFLOW-NWT did not converge and terminate normally.")
            head_reader = flopy.utils.HeadFile(str(workspace / f"{MODEL_NAME}.hds"),
                                                precision="auto")
            try:
                head_array = head_reader.get_data(kstpkper=(0, 0))
                if head_array.shape != (1, 1, grid.ncol):
                    raise ValueError("Unexpected head-file dimensions.")
                heads = np.asarray(head_array[0, 0], dtype=float)
            finally:
                head_reader.close()
            cbc = flopy.utils.CellBudgetFile(str(workspace / f"{MODEL_NAME}.cbc"),
                                              precision="auto")
            try:
                boundary = read_cbc_term(cbc, BUDGET_TERMS[p.boundary_type], grid.ncol)
                chd = read_cbc_term(cbc, "CONSTANT HEAD", grid.ncol)
            finally:
                cbc.close()
            budget = read_listing_budget(listing_path, p.boundary_type)
            check_outputs(heads, boundary, chd, budget, p, solver)
            archive = io.BytesIO()
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
                for path in sorted(workspace.iterdir()):
                    if path.is_file():
                        bundle.write(path, path.name)
                bundle.writestr("run_settings.json", json.dumps({
                    "app_version": APP_VERSION, "model": asdict(p),
                    "solver": asdict(solver), "row_width_m": ROW_WIDTH}, indent=2))
                bundle.writestr("console.txt", log)
            return {"inputs": asdict(p), "solver": asdict(solver),
                    "heads": heads.tolist(), "boundary_cbc": boundary.tolist(),
                    "chd_cbc": chd.tolist(), "budget": budget,
                    "q_boundary_m3_s": float(boundary.sum()),
                    "listing": listing_text, "log": log,
                    "model_zip": archive.getvalue()}
        except subprocess.TimeoutExpired as exc:
            raise SimulationError(
                f"MODFLOW-NWT exceeded {RUN_TIMEOUT_SECONDS} seconds and was stopped. "
                "No result was added.", str(exc)) from exc
        except (OSError, ValueError, EOFError, KeyError, IndexError) as exc:
            raise SimulationError(str(exc), log + "\n" + listing_text) from exc


# =============================================================================
# 05. RUN HISTORY AND Q-h SERIES MANAGEMENT
# =============================================================================
def empty_history() -> dict:
    return {"series": [], "active_id": None, "next_series_id": 1, "next_run_id": 1,
            "q_axis_limit": INITIAL_Q_AXIS_LIMIT, "schema_version": 3, "type_counts": {}}


def expand_flow_axis(history: dict, flow_m3_day: float) -> None:
    """Stable, symmetric 1/2/5-decade limits; no contraction after deletion."""
    limit = history.get("q_axis_limit", INITIAL_Q_AXIS_LIMIT)
    required = abs(flow_m3_day) * 1.1
    if required > limit:
        decade = 10.0 ** math.floor(math.log10(required))
        limit = next(f * decade for f in (1, 2, 5, 10) if f * decade >= required)
    history["q_axis_limit"] = limit


def upgrade_history(history: dict) -> None:
    """Keep live 1.0.x/1.1.x experiments and assign stable per-type symbol sizes."""
    if history.get("schema_version") == 3:
        return
    def inputs(data):
        if "river_stage_m" in data:
            data["boundary_head_m"] = data.pop("river_stage_m")
        for key, value in asdict(ModelInputs()).items():
            data.setdefault(key, value)
    counts = {}
    for series in history["series"]:
        inputs(series["inputs"])
        p = ModelInputs(**series["inputs"])
        series["signature"] = series_signature(p)
        counts[p.boundary_type] = counts.get(p.boundary_type, 0) + 1
        series.setdefault("marker_size", 36 + 6*((counts[p.boundary_type]-1) % 4))
        for run in series["runs"]:
            inputs(run["inputs"])
            for old, new in (("q_riv_m3_s", "q_boundary_m3_s"), ("river_cbc", "boundary_cbc")):
                if old in run:
                    run[new] = run.pop(old)
            for old, new in (("riv_in", "boundary_in"), ("riv_out", "boundary_out")):
                if old in run["budget"]:
                    run["budget"][new] = run["budget"].pop(old)
            expand_flow_axis(history, run["q_boundary_m3_s"] * SEC_DAY)
    history.setdefault("q_axis_limit", INITIAL_Q_AXIS_LIMIT)
    history["type_counts"] = counts
    history["schema_version"] = 3


def series_color(series_id: int) -> str:
    if series_id <= len(PALETTE):
        return PALETTE[series_id - 1]
    hue = (series_id * 0.61803398875) % 1.0
    return matplotlib.colors.to_hex(colorsys.hsv_to_rgb(hue, 0.65, 0.68))


def append_result(history: dict, result: dict) -> dict:
    """New series only on a successful run with a changed physical setup."""
    p = ModelInputs(**result["inputs"])
    signature = series_signature(p)
    active = next((s for s in history["series"]
                   if s["id"] == history["active_id"]), None)
    if active is None or tuple(active["signature"]) != signature:
        sid = history["next_series_id"]
        counts = history.setdefault("type_counts", {})
        counts[p.boundary_type] = counts.get(p.boundary_type, 0) + 1
        if history["next_run_id"] == 1 and p.boundary_type == "EVT":
            # 500 mm/a over 100 m2 is only 0.137 m3/day: give a fresh EVT
            # experiment a useful scale without shrinking any existing plot.
            history["q_axis_limit"] = 0.2
        active = {"id": sid, "signature": signature, "color": series_color(sid),
                  "marker_size": 36 + 6*((counts[p.boundary_type]-1) % 4),
                  "inputs": asdict(p), "runs": []}
        history["series"].append(active)
        history["active_id"] = sid
        history["next_series_id"] += 1
    result = dict(result, run_id=history["next_run_id"], series_id=active["id"])
    history["next_run_id"] += 1
    active["runs"].append(result)
    expand_flow_axis(history, result["q_boundary_m3_s"] * SEC_DAY)
    return result


def latest_result(history: dict) -> dict | None:
    return max((r for s in history["series"] for r in s["runs"]),
               key=lambda r: r["run_id"], default=None)


def retain_series(history: dict, keep_ids) -> None:
    """Permanent session deletion, not just hiding points in the figure."""
    history["series"] = [s for s in history["series"] if s["id"] in keep_ids]
    if history["active_id"] not in keep_ids:
        history["active_id"] = None


def delete_latest(history: dict) -> None:
    latest = latest_result(history)
    if latest is None:
        return
    for series in history["series"]:
        series["runs"] = [r for r in series["runs"] if r["run_id"] != latest["run_id"]]
    retain_series(history, [s["id"] for s in history["series"] if s["runs"]])


def distinct_variants(series: dict) -> int:
    return len({r["inputs"]["end_head_m"] for r in series["runs"]})


def series_label(series: dict) -> str:
    p = series["inputs"]
    if p["boundary_type"] == "EVT":
        data = (f"ETmax {p['max_et_mm_year']:g} mm/a; SURF {p['et_surface_m']:g} m; "
                f"EXDP {p['extinction_depth_m']:g} m")
    else:
        bottom = f"bottom {p['river_bottom_m']:g} m; " if p["boundary_type"] == "RIV" else ""
        data = f"head {p['boundary_head_m']:g} m; {bottom}C {p['conductance_m2_s']:.1e} m²/s"
    return f"S{series['id']} · {p['boundary_type']}: {data}; K {p['k_m_s']:.1e} m/s; Δx {p['cell_size_m']:g} m"


def history_csv(history: dict) -> str:
    output = io.StringIO()
    fields = ["series_id", "run_id", "boundary_type", "k_m_s", "end_head_m", "boundary_head_m",
              "river_bottom_m", "conductance_m2_s", "boundary_cell_head_m",
              "q_boundary_m3_s", "q_boundary_m3_day", "budget_discrepancy_percent",
              "cell_size_m", "max_et_mm_year", "et_surface_m", "extinction_depth_m",
              "boundary_mean_head_m",
              "equilibrium_near_zero_flow", "absolute_budget_imbalance_m3_day"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for series in history["series"]:
        for result in series["runs"]:
            writer.writerow({**result["inputs"],
                "river_bottom_m": result["inputs"]["river_bottom_m"] if result["inputs"]["boundary_type"] == "RIV" else "",
                "series_id": series["id"],
                "run_id": result["run_id"],
                "boundary_cell_head_m": result["heads"][len(result["heads"])//2],
                "boundary_mean_head_m": boundary_mean_head(result),
                "boundary_head_m": result["inputs"]["boundary_head_m"] if result["inputs"]["boundary_type"] != "EVT" else "",
                "conductance_m2_s": result["inputs"]["conductance_m2_s"] if result["inputs"]["boundary_type"] != "EVT" else "",
                **{name: result["inputs"][name] if result["inputs"]["boundary_type"] == "EVT" else ""
                   for name in ("max_et_mm_year", "et_surface_m", "extinction_depth_m")},
                "q_boundary_m3_s": result["q_boundary_m3_s"],
                "q_boundary_m3_day": result["q_boundary_m3_s"] * SEC_DAY,
                "budget_discrepancy_percent": result["budget"]["percent_discrepancy"],
                "equilibrium_near_zero_flow": result["budget"]["near_zero_flow"],
                "absolute_budget_imbalance_m3_day": abs(result["budget"]["total_in"]-
                    result["budget"]["total_out"])*SEC_DAY})
    return output.getvalue()


# =============================================================================
# 06. CROSS-SECTION, BUDGET AND Q-h FIGURES
# =============================================================================
def cross_section_figure(p: ModelInputs, heads=None):
    """Full cells and a fixed 100 m boundary footprint, on any offered grid."""
    preview = heads is None
    grid = model_grid(p)
    fig, ax = plt.subplots(figsize=(10.5, 4.2), layout="constrained")
    ax.set_facecolor("white")
    if not preview:
        # Color only the modeled volume, leaving axis margins white.
        domain = Rectangle((grid.edges[0], BOTTOM), grid.edges[-1]-grid.edges[0], TOP-BOTTOM,
                           facecolor="#f5f1e4", edgecolor="none", zorder=0)
        domain.set_gid("model_domain")
        ax.add_patch(domain)
        for j, head in enumerate(heads):
            rect = Rectangle((grid.edges[j], BOTTOM), grid.dx,
                np.clip(head, BOTTOM, TOP)-BOTTOM, facecolor="#b9def1", edgecolor="none", zorder=1)
            rect.set_gid("saturated_cell")
            ax.add_patch(rect)
    for edge in grid.edges:
        ax.vlines(edge, BOTTOM, TOP, color="#8a8a8a" if preview else "#929ca0",
                  lw=.65 if grid.dx >= 20 else .35, alpha=.7 if grid.dx >= 20 else .45, zorder=2)
    ax.hlines([BOTTOM, TOP], grid.edges[0], grid.edges[-1],
              color="black" if preview else "#7b6e50", lw=1.2)
    for j, align in ((0, "left"), (grid.ncol-1, "right")):
        color = "black" if preview else "#376d43"
        rect = Rectangle((grid.edges[j], BOTTOM), grid.dx, p.end_head_m-BOTTOM,
            facecolor="none" if preview else "#d4e6d0", edgecolor=color, lw=1.3, zorder=3)
        rect.set_gid("chd_boundary")
        ax.add_patch(rect)
        ax.hlines(p.end_head_m, grid.edges[j], grid.edges[j+1], color=color, lw=2.3, zorder=6)
        ax.plot(grid.x[j], p.end_head_m, marker="s", color=color, markersize=6,
                markerfacecolor="white", zorder=8)
        ax.annotate(f"CHD = {p.end_head_m:g} m", (grid.x[j], p.end_head_m),
            xytext=(8 if align == "left" else -8, 10 if p.end_head_m < 5 else -16),
            textcoords="offset points", ha=align, fontsize=9,
            bbox={"facecolor":"white", "edgecolor":"none", "alpha":.8}, zorder=9)

    left, right = BOUNDARY_LEFT, BOUNDARY_RIGHT
    color = "black" if preview else {"RIV":"#11658f", "DRN":"#985e34",
                                     "GHB":"#70528c", "EVT":"#47773d"}[p.boundary_type]
    reference = p.et_surface_m if p.boundary_type == "EVT" else p.boundary_head_m
    if p.boundary_type == "RIV":
        rect = Rectangle((left, p.river_bottom_m), BOUNDARY_WIDTH, p.boundary_head_m-p.river_bottom_m,
            facecolor="none" if preview else "#70c4eb", edgecolor=color, lw=.8, zorder=4)
        rect.set_gid("middle_boundary")
        ax.add_patch(rect)
        ax.hlines(p.river_bottom_m, left, right,
                  color="black" if preview else "#8a623a", lw=2, ls="--", zorder=6)
    elif p.boundary_type == "EVT":
        ax.hlines(p.et_surface_m-p.extinction_depth_m, left, right,
                  color=color, lw=1.8, ls="--", zorder=6)
    ax.hlines(reference, left, right, color=color, lw=2.5,
              ls="--" if p.boundary_type == "DRN" else "-", zorder=6)
    if p.boundary_type == "EVT":
        data_label = (f"EVT  SURF = {p.et_surface_m:g} m\n"
                      f"ETmax = {p.max_et_mm_year:g} mm/a; EXDP = {p.extinction_depth_m:g} m")
        caption = (f"EVT · ETmax {p.max_et_mm_year:g} mm/a · SURF {p.et_surface_m:g} m · "
                   f"EXDP {p.extinction_depth_m:g} m")
    else:
        data_label = (f"{p.boundary_type}  h_{p.boundary_type} = {p.boundary_head_m:g} m\n"
                      f"C = {p.conductance_m2_s:.1e} m²/s")
        if p.boundary_type == "RIV":
            data_label += f"; bottom = {p.river_bottom_m:g} m"
        bottom = f" · bottom {p.river_bottom_m:g} m" if p.boundary_type == "RIV" else ""
        caption = (f"{p.boundary_type} · boundary head {p.boundary_head_m:g} m{bottom}"
                   f" · C {p.conductance_m2_s:.1e} m²/s")
    if preview:
        ax.annotate(data_label, (right, reference), xytext=(9, -9 if reference > 24 else 9),
            textcoords="offset points", ha="left", va="top" if reference > 24 else "bottom",
            fontsize=8.5, bbox={"facecolor":"white", "edgecolor":"none", "alpha":.9}, zorder=10)
        ax.plot(grid.x, starting_heads(p), color="#666666", lw=.9, ls="--", zorder=3)
        handles = [Line2D([], [], color="#666666", lw=.9, ls="--", label="Initial head (starting guess)")]
        title = "Model preview · before computation"
    else:
        steps = ax.stairs(heads, grid.edges, baseline=None, color="#225b8b", lw=1.2, zorder=7)
        steps.set_gid("computed_step_heads")
        ax.plot(grid.x, heads, "o", color="#225b8b", markerfacecolor="white",
                markersize=4.7 if grid.dx >= 50 else 2.5 if grid.dx >= 20 else 1.5, zorder=8)
        handles = [Line2D([], [], color="#225b8b", marker="o", markerfacecolor="white",
                          lw=1.1, label="Cell head (constant within each cell)"),
                   Patch(facecolor="#b9def1", label="Saturated part of each cell")]
        title = "Computed groundwater heads"
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0, -.19), ncol=2, fontsize=8)
    ax.set(xlim=(grid.edges[0], grid.edges[-1]), ylim=(BOTTOM-1, TOP+1),
           xticks=np.arange(0, MODEL_LENGTH+1, 100),
           xlabel="Distance perpendicular to the boundary, x (m)", ylabel="Elevation, z (m)",
           title=title+"\n"+caption)
    ax.spines["bottom"].set_bounds(0, MODEL_LENGTH)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_yticks(np.arange(0, 31, 5))
    ax.grid(axis="y", alpha=.12)
    return fig


def budget_figure(result: dict):
    """Match the existing Fieldcase signed horizontal IN/OUT bar chart."""
    b = result["budget"]
    labels = ["Specified heads\n(CHD)", BOUNDARY_LABELS[result["inputs"]["boundary_type"]], "TOTAL"]
    incoming = np.array([b["chd_in"], b["boundary_in"], b["total_in"]]) * SEC_DAY
    outgoing = np.array([b["chd_out"], b["boundary_out"], b["total_out"]]) * SEC_DAY
    fig, ax = plt.subplots(figsize=(5.5, 4.2), layout="constrained")
    y = np.arange(len(labels))
    bars_in = ax.barh(y-.19, incoming, height=.38, color="#2577a7", label="IN (+)")
    bars_out = ax.barh(y+.19, -outgoing, height=.38, color="#d7853a", label="OUT (−)")
    for bar in (bars_in[-1], bars_out[-1]):
        bar.set_hatch("///")
        bar.set_edgecolor("#333333")
        bar.set_linewidth(.7)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    extent = max(float(np.max(incoming)), float(np.max(outgoing)), 0.01) * 1.18
    ax.set_xlim(-extent, extent)
    ax.axvline(0, color="#353535", lw=.7)
    ax.grid(axis="x", alpha=.15)
    ax.set_axisbelow(True)
    ax.set_xlabel("Volumetric flow rate (m³/day)")
    ax.set_title("Water budget · latest retained run")
    ax.legend(loc="lower right", ncol=2, fontsize=8)
    return fig


def qh_segments(series: dict, axis: str = "boundary_cell") -> list:
    """Insert physical transition vertices, never artificial model-run dots.

    One boundary cell retains the exact original piecewise Q-h law. With a
    refined grid, linearly interpolate the individual cell heads between runs
    and insert EVERY cell's regime transition before summing its flux. This
    respects partially connected RIV/DRN and partially active EVT footprints.
    Interpolated profiles are guides, not additional numerical simulations.
    """
    p = ModelInputs(**series["inputs"])
    grid = model_grid(p)
    cells = grid.boundary_cells
    weights = grid.weights[cells]
    runs = sorted(series["runs"], key=boundary_mean_head)
    profiles = np.array([r["heads"] for r in runs])[:, cells]
    local = profiles @ weights
    end = np.array([r["inputs"]["end_head_m"] for r in runs])
    flow = np.array([r["q_boundary_m3_s"]*SEC_DAY for r in runs])
    thresholds = boundary_thresholds(p)
    if len(cells) == 1:
        limits = [float(local.min())] + [h for h in thresholds if local.min() < h < local.max()] + [float(local.max())]
        if axis != "end_head":
            return [(boundary_flux_m3_s(np.array([a,b]),p)*SEC_DAY, np.array([a,b]))
                    for a,b in zip(limits[:-1],limits[1:])]
        # Preserve the original optional end-head interpolation convention.
        output = []
        for a,b in zip(limits[:-1],limits[1:]):
            inside = (local > a) & (local < b)
            q = np.r_[float(boundary_flux_m3_s(a,p))*SEC_DAY, flow[inside],
                      float(boundary_flux_m3_s(b,p))*SEC_DAY]
            h = np.r_[np.interp(a,local,end),end[inside],np.interp(b,local,end)]
            output.append((q,h))
        return output
    q_vertices, h_vertices = [], []
    for i in range(len(runs)-1):
        start, finish = profiles[i], profiles[i+1]
        delta = finish-start
        times = [0.,1.]
        for threshold in thresholds:
            moving = np.abs(delta) > 1e-12
            crossings = (threshold-start[moving])/delta[moving]
            times.extend(crossings[(crossings > 0) & (crossings < 1)].tolist())
        for t in sorted(set(times)):
            if i > 0 and t == 0:
                continue
            heads = start+t*delta
            q = float(np.dot(boundary_flux_m3_s(heads,p),weights))*SEC_DAY
            # At a simulated profile retain its measured, unmodified CBC rate.
            if t == 0: q = flow[i]
            if t == 1: q = flow[i+1]
            h = end[i]+t*(end[i+1]-end[i]) if axis == "end_head" else float(np.dot(heads,weights))
            q_vertices.append(q)
            h_vertices.append(h)
    return [(np.array(q_vertices),np.array(h_vertices))]


def qh_figure(history: dict, axis: str = "boundary_cell"):
    fig, ax = plt.subplots(figsize=(5.5, 4.2), layout="constrained")
    for series in history["series"]:
        head = [r["inputs"]["end_head_m"] if axis == "end_head" else boundary_mean_head(r)
                for r in series["runs"]]
        flow = [r["q_boundary_m3_s"]*SEC_DAY for r in series["runs"]]
        if distinct_variants(series) >= MIN_RUNS_FOR_LINE:
            for q, h in qh_segments(series, axis):
                ax.plot(q, h, color=series["color"], lw=.85, alpha=.85)
        marker = BOUNDARY_MARKERS[series["inputs"]["boundary_type"]]
        style = {"color": series["color"]} if marker == "x" else {"facecolors": "none", "edgecolors": series["color"]}
        ax.scatter(flow, head, s=series.get("marker_size",36), marker=marker, **style,
                   linewidths=1.4, zorder=3,
                   label=f"S{series['id']} · {series['inputs']['boundary_type']} · {distinct_variants(series)} variants")
    ax.axvline(0, color="#555555", lw=.8, zorder=0)
    extent = history.get("q_axis_limit", INITIAL_Q_AXIS_LIMIT)
    ax.set_xlim(-extent, extent)
    ax.set_ylim(BOTTOM, TOP+.5)
    ax.grid(alpha=.16)
    ax.set_xlabel("Boundary exchange Q (m³/day)")
    ax.set_ylabel("Specified head at model ends, H (m)" if axis == "end_head"
                  else "Mean groundwater head in boundary area, h (m)")
    ax.set_title("Boundary Q–h relationship")
    ax.ticklabel_format(axis="x", style="plain", useOffset=False)
    if history["series"]:
        # Keep labels outside the data area after transposing the axes.
        ax.legend(loc="upper left", bbox_to_anchor=(0, -.20), fontsize=8,
                  ncol=2 if len(history["series"]) > 1 else 1)
    return fig


# =============================================================================
# 07. STREAMLIT STYLE AND INPUT CONTROLS
# =============================================================================
def inject_styles(st) -> None:
    # Soft panels from the Fieldcase app; stable keys, not positional selectors.
    panels = {"aquifer": ("248,226,107", "#c3a846"),
              "boundaries": ("83,163,108", "#76ae79"),
              "heads": ("93,169,206", "#6eafcb"),
              "budget": ("80,156,142", "#69a89c"),
              "details": ("151,160,167", "#a3abb0")}
    css = [".block-container {max-width: 1150px;}",
           '[class*="st-key-riv-panel-"] [data-testid="stExpander"] > details '
           '{border-radius:.7rem; overflow:hidden;}',
           '[class*="st-key-riv-panel-"] [data-testid="stExpander"] summary p '
           '{font-weight:650;}']
    for name, (rgb, border) in panels.items():
        css.append(f'.st-key-riv-panel-{name} [data-testid="stExpander"] > details '
                   f'{{background-color:rgba({rgb},.11); border-color:{border};}}')
    st.markdown("<style>" + "\n".join(css) + "</style>", unsafe_allow_html=True)


def panel(st, title: str, key: str, expanded=False):
    """Keyed expander preserves its open state across ordinary Streamlit reruns."""
    return st.expander(title + " (Click to open/close)", key="panel_"+key,
                       expanded=expanded)


def numeric_control(st, label: str, name: str, minimum: float, maximum: float,
                    default: float, step: float, use_numbers: bool,
                    logarithmic=False) -> float:
    """Separate stable value from slider/number widget lifetimes."""
    values = st.session_state.setdefault("input_values", {})
    value = values.get(name, default)
    key = name + ("_number" if use_numbers else "_slider")
    if use_numbers:
        value = st.number_input(label, min_value=float(minimum), max_value=float(maximum),
            value=float(value), step=float(step), format="%.3e" if logarithmic else "%.2f",
            key=key)
    elif logarithmic:
        exponent = st.slider(f"log₁₀ {label}", min_value=math.log10(minimum),
            max_value=math.log10(maximum), value=math.log10(value), step=.05,
            format="%.2f", key=key)
        value = min(max(10.0**exponent, minimum), maximum)
        st.caption(f"{label}: {value:.3e}")
    else:
        value = st.slider(label, min_value=float(minimum), max_value=float(maximum),
            value=float(value), step=float(step), format="%.1f", key=key)
    values[name] = float(value)
    return float(value)


def show_figure(st, fig, alt: str) -> None:
    """Use only explicit pyplot parameters supported by this Streamlit version.

    Older releases accept unknown keywords through **kwargs and forward them
    to Matplotlib's savefig. Passing alt that way raises a print_png TypeError.
    Keep accessible descriptions when supported, without forwarding them (or
    width) to Matplotlib on older versions.
    """
    parameters = inspect.signature(st.pyplot).parameters
    options = {}
    if "width" in parameters:
        options["width"] = "stretch"
    elif "use_container_width" in parameters:
        options["use_container_width"] = True
    if "alt" in parameters:
        options["alt"] = alt
    try:
        st.pyplot(fig, **options)
    finally:
        plt.close(fig)


# =============================================================================
# 08. POST-PROCESSING, DOWNLOADS AND DELETION CONTROLS
# =============================================================================
def prune_from_widget() -> None:
    import streamlit as st
    retain_series(st.session_state["history"], st.session_state["retained_series"])


def delete_last_callback() -> None:
    import streamlit as st
    delete_latest(st.session_state["history"])
    st.session_state["retained_series"] = [s["id"] for s in st.session_state["history"]["series"]]
    st.session_state.pop("run_error", None)


def clear_all_callback() -> None:
    import streamlit as st
    st.session_state["history"] = empty_history()
    st.session_state["retained_series"] = []
    st.session_state.pop("run_error", None)


def render_results(st, current: ModelInputs, solver: SolverSettings) -> None:
    history = st.session_state["history"]
    result = latest_result(history)
    if result is None:
        st.info("Run the model to see computed heads, the water budget and Q–h points.")
        return
    p = ModelInputs(**result["inputs"])
    st.subheader("Post-processing")
    if series_signature(p) != series_signature(current) or p.end_head_m != current.end_head_m or result["solver"] != asdict(solver):
        st.info(f"Inputs have changed. The cross section and budget below still show "
                f"run {result['run_id']} (S{result['series_id']}); run again to update them.")
    else:
        st.success(f"MODFLOW-NWT completed successfully · run {result['run_id']} · "
                   f"series S{result['series_id']}")
    with st.container(key="riv-panel-heads"):
        with panel(st, "4 · Computed heads", "heads", expanded=True):
            show_figure(st, cross_section_figure(p, result["heads"]),
                        "Computed cell heads with a light blue saturated fill in each cell.")
            h = boundary_mean_head(result)
            boundary_heads = np.asarray(result["heads"])[model_grid(p).boundary_cells]
            q = result["q_boundary_m3_s"] * SEC_DAY
            regime = ("Equilibrium: negligible net river exchange." if result["budget"]["near_zero_flow"]
                      else "Gaining river: groundwater discharges to the river." if q < -1e-6
                      else "Losing river: water enters groundwater." if q > 1e-6
                      else "Negligible net river exchange.")
            if p.boundary_type == "RIV":
                if np.all(boundary_heads < p.river_bottom_m):
                    regime += " The full river strip is leakage-limited."
                elif np.any(boundary_heads < p.river_bottom_m):
                    regime += " Part of the river strip is leakage-limited."
            elif p.boundary_type == "DRN":
                regime = "Drain inactive: no discharge." if result["budget"]["near_zero_flow"] or h <= p.boundary_head_m else "Groundwater discharges to the drain."
            elif p.boundary_type == "GHB":
                regime = ("Negligible general-head exchange." if result["budget"]["near_zero_flow"]
                          else "General-head boundary: inflow to groundwater." if q > 1e-6
                          else "General-head boundary: groundwater outflow." if q < -1e-6
                          else "Negligible general-head exchange.")
            elif p.boundary_type == "EVT":
                regime = ("ET inactive: negligible groundwater loss." if result["budget"]["near_zero_flow"]
                          else "Maximum ET across the full strip." if np.all(boundary_heads >= p.et_surface_m)
                          else "Groundwater loss varies with head between the EVT thresholds.")
            st.caption(f"Mean head in boundary area: {h:.4f} m · Total Q = {q:+.5g} m³/day. {regime}")

    with st.container(key="riv-panel-budget"):
        with panel(st, "5 · Water budget and Q–h series", "budget", expanded=True):
            series_by_id = {s["id"]: s for s in history["series"]}
            st.multiselect("Retained series — remove × to delete a complete series",
                options=list(series_by_id), key="retained_series",
                format_func=lambda sid: series_label(series_by_id[sid]),
                on_change=prune_from_widget,
                help="Removing a tag deletes all runs of that series from this session.")
            a, b = st.columns(2)
            a.button("Delete latest run", on_click=delete_last_callback, width="stretch")
            b.button("Clear all runs and series", on_click=clear_all_callback, width="stretch")
            active = next((s for s in history["series"] if s["id"] == history["active_id"]), None)
            if active:
                count = distinct_variants(active)
                st.caption(f"S{active['id']}: {count} different end-head settings. "
                           "Use at least 4 per series; a thin line then connects the points in head order.")
            st.caption("Q > 0: into groundwater · Q < 0: out of groundwater. "
                       "Budget and Q values represent the 1 m model width along the boundary.")
            # Preserve the old axis selection during a live source update.
            if st.session_state.get("qh_axis") in ("Groundwater head in the river cell", "Groundwater head in the boundary cell"):
                st.session_state["qh_axis"] = "Groundwater head in the boundary area"
            axis_label = st.selectbox("Head shown on the vertical axis",
                ["Groundwater head in the boundary area", "Specified head at both model ends"],
                key="qh_axis")
            axis = "boundary_cell" if axis_label.startswith("Groundwater") else "end_head"
            left, right = st.columns(2)
            with left:
                show_figure(st, budget_figure(result), "Signed MODFLOW water budget.")
                budget = result["budget"]
                st.caption(f"Total IN: {budget['total_in']*SEC_DAY:.5g} m³/day · "
                           f"Total OUT: {budget['total_out']*SEC_DAY:.5g} m³/day")
                if budget["near_zero_flow"]:
                    st.caption("Equilibrium: negligible absolute flows. The percentage "
                               "discrepancy is not meaningful near zero flow. "
                               f"Absolute imbalance: {abs(budget['total_in']-budget['total_out'])*SEC_DAY:.2e} m³/day "
                               f"(raw LIST: {budget['percent_discrepancy']:+.2f}%).")
                else:
                    st.caption(f"Listing-file discrepancy: {budget['percent_discrepancy']:+.4f}% · target ±1%.")
            with right:
                show_figure(st, qh_figure(history, axis), "Boundary head versus flux for all retained runs.")
                st.caption("Each marker is one successful model run. Coincident runs overlap. "
                           "Circles: RIV · squares: GHB · crosses: DRN · triangles: EVT. "
                           "The symmetric flow axis expands only when needed.")
                st.caption("Lines include boundary-regime transitions; vertices are not extra model runs. "
                           "On refined grids, h is area-weighted and lines use interpolated cell heads, "
                           "so parts of the strip may change regime at different points.")
                if axis == "end_head":
                    st.caption("For end head H, lines are interpolation guides; the bend's H-coordinate "
                               "is estimated between neighbouring runs. The exact boundary law uses local h.")
            with st.expander("Boundary equations and suggested experiment"):
                st.latex(r"\mathrm{RIV}:\quad Q=C\,[h_b-\max(h,z_b)]")
                st.latex(r"\mathrm{DRN}:\quad Q=-C\,\max(h-h_b,0)")
                st.latex(r"\mathrm{GHB}:\quad Q=C\,(h_b-h)")
                st.latex(r"\mathrm{EVT}:\quad Q=-E_{max}A\,\mathrm{clip}\!\left(\frac{h-(SURF-EXDP)}{EXDP},0,1\right)")
                st.markdown("The equations apply to each boundary cell using its share of conductance or area; "
                            "the graph sums the cell flows. **h** in these equations is the cell head, "
                            "**hᵦ** is the external boundary head, "
                            "and **zᵦ** is the river bottom. RIV reaches a constant inflow below "
                            "its bottom; DRN cannot supply groundwater; GHB permits both directions. "
                            "EVT removes water between zero and its specified maximum, according to head.")
                st.markdown("Keep the boundary settings fixed and try end heads of "
                            "**25, 20, 17, 15, 10 and 5 m**. Then change boundary type, "
                            "head or conductance and repeat to start a new series. For EVT, use end heads "
                            "below SURF − EXDP, between the thresholds, and above SURF.")
                st.markdown("[USGS boundary-condition explanation](https://water.usgs.gov/"
                            "nrp/gwsoftware/modflow2000/MFDOC/head-dependent_flux_boundary_p.html)")

    with st.container(key="riv-panel-details"):
        with panel(st, "6 · Model details and downloads", "details"):
            grid = model_grid(p)
            st.dataframe({"Cell": list(range(1, grid.ncol+1)), "x (m)": grid.x,
                          "Computed head (m)": result["heads"]}, hide_index=True)
            budget = result["budget"]
            st.dataframe({"Component": ["Specified heads (CHD)", BOUNDARY_LABELS[p.boundary_type], "TOTAL"],
                "IN (m³/day)": [budget[n]*SEC_DAY for n in ("chd_in", "boundary_in", "total_in")],
                "OUT (m³/day)": [budget[n]*SEC_DAY for n in ("chd_out", "boundary_out", "total_out")]},
                hide_index=True)
            st.download_button("Download all retained Q–h points (CSV)", history_csv(history),
                               "boundary_qh_runs.csv", "text/csv")
            st.download_button("Download latest retained model (ZIP)", result["model_zip"],
                               f"river_model_run_{result['run_id']}.zip", "application/zip")
            st.download_button("Download latest MODFLOW listing", result["listing"],
                               "river_demo.list", "text/plain")
            st.caption("Runs are retained in this browser session. Download the CSV before "
                       "closing or refreshing the session if you want to keep the experiment.")


# =============================================================================
# 09. MAIN INTERFACE
# =============================================================================
def main() -> None:
    import streamlit as st
    st.set_page_config(page_title="Groundwater · Boundary conditions", page_icon="💧", layout="wide")
    inject_styles(st)
    st.session_state.setdefault("history", empty_history())
    upgrade_history(st.session_state["history"])
    st.session_state.setdefault("retained_series", [])
    st.title("💧 Head-dependent boundary conditions")
    st.markdown("Explore river, drain, general-head and evapotranspiration boundaries with a **one-layer, "
                "steady-state MODFLOW-NWT model**. Set the inputs, preview the model, "
                "then compute heads and build a Q–h diagram one run at a time.")
    default = ModelInputs()
    with st.container(key="riv-panel-aquifer"):
        with panel(st, "1 · Aquifer properties and model geometry", "aquifer"):
            numbers = st.toggle("Use number inputs", value=False, key="use_numbers")
            k = numeric_control(st, "Hydraulic conductivity K (m/s)", "k",
                1e-5, 1e-2, default.k_m_s, 1e-5, numbers, logarithmic=True)
            cell_size = st.select_slider("Grid cell size Δx (m)", options=list(GRID_SIZES),
                value=default.cell_size_m, format_func=lambda value: f"{value:g} m", key="cell_size")
            st.caption(f"One unconfined layer · top 30 m · bottom 0 m · "
                       f"{int(MODEL_LENGTH/cell_size)+1} cells × {cell_size:g} m · 1 m width along the boundary.")
            st.caption("CHD node centres stay 1,000 m apart. The boundary strip stays 100 m wide "
                       "(x = 450–550 m); partial overlaps at its edges preserve the total area and conductance.")
    with st.container(key="riv-panel-boundaries"):
        with panel(st, "2 · Boundary conditions", "boundaries"):
            left, right = st.columns(2)
            with left:
                with st.container(border=True):
                    st.markdown("**Specified-head boundaries (CHD)**")
                    end_head = numeric_control(st, "Specified head at both ends H (m)", "end_head",
                        1., 30., default.end_head_m, .5, numbers)
                    st.caption("Both end heads are equal. Change H between runs to add points "
                               "to the current Q–h series.")
            with right:
                with st.container(border=True):
                    st.markdown("**Central boundary area**")
                    boundary_type = st.selectbox("Boundary type", list(BOUNDARY_LABELS),
                        format_func=BOUNDARY_LABELS.get, key="boundary_type")
                    values = st.session_state.get("input_values", {})
                    head = values.get("river_stage", default.boundary_head_m)
                    bottom = values.get("river_bottom", default.river_bottom_m)
                    conductance = values.get("conductance", default.conductance_m2_s)
                    et_max = values.get("max_et", default.max_et_mm_year)
                    et_surface = values.get("et_surface", default.et_surface_m)
                    et_depth = values.get("extinction_depth", default.extinction_depth_m)
                    if boundary_type == "EVT":
                        et_max = numeric_control(st, "Maximum ET (mm/a)", "max_et",
                            0., 500., default.max_et_mm_year, 10., numbers)
                        et_surface = numeric_control(st, "ET surface SURF (m)", "et_surface",
                            0., 30., default.et_surface_m, .1, numbers)
                        et_depth = numeric_control(st, "Extinction depth EXDP (m)", "extinction_depth",
                            .1, 30., default.extinction_depth_m, .1, numbers)
                        st.caption("ET acts over the 100 m × 1 m strip. EXDP is a depth below SURF. "
                                   "ET stops at SURF − EXDP and reaches its maximum at SURF. 1 a = 365.25 days.")
                    else:
                        head = numeric_control(st, "Boundary head (m)", "river_stage",
                            .1, 30., default.boundary_head_m, .1, numbers)
                        if boundary_type == "RIV":
                            bottom = numeric_control(st, "River-bottom elevation (m)", "river_bottom",
                                0., 30., default.river_bottom_m, .1, numbers)
                        conductance = numeric_control(st, "Conductance C (m²/s)", "conductance",
                            1e-6, 1e-2, default.conductance_m2_s, 1e-5, numbers, logarithmic=True)
                        st.caption("C is the total conductance of the 100 m strip for the 1 m model width. "
                                   "Boundary head is river stage, drain elevation or external GHB head.")
            st.caption("Changing boundary data, K or grid size starts a new series on the next successful run. "
                       "Each boundary type keeps its symbol; new series get a new color and a slightly different size.")
    p = ModelInputs(k, end_head, head, bottom, conductance, boundary_type,
                    cell_size, et_max, et_surface, et_depth)
    # Fixed user-requested solver criteria; no editable learner controls.
    solver = SolverSettings()
    invalid = None
    try:
        validate_inputs(p, solver)
    except ValueError as exc:
        invalid = str(exc)
        st.error(invalid)
    with st.container(key="riv-panel-preview"):
        with panel(st, "3 · Model preview: grid and boundaries", "preview", expanded=True):
            if invalid is None:
                show_figure(st, cross_section_figure(p), "Black-and-white full-cell grid and boundary sketch.")
            st.caption("Full-cell view: x = 0 and 1,000 m mark the CHD node centres. "
                       "The central boundary spans x = 450–550 m. No recharge; other faces are no-flow.")
    if st.button("▶ Run MODFLOW-NWT model", type="primary", width="stretch",
                 disabled=invalid is not None, key="run_model"):
        st.session_state.pop("run_error", None)
        try:
            with st.spinner("Computing steady groundwater flow…"):
                result = run_model(p, solver)
            append_result(st.session_state["history"], result)
            st.session_state["retained_series"] = [s["id"] for s in st.session_state["history"]["series"]]
        except (SimulationError, RuntimeError) as exc:
            st.session_state["run_error"] = {"message": str(exc),
                "diagnostics": getattr(exc, "diagnostics", "")}
    failure = st.session_state.get("run_error")
    if failure:
        st.error(f"Run not accepted: {failure['message']}")
        if failure["diagnostics"]:
            with st.expander("Failed-run diagnostics"):
                st.code(failure["diagnostics"][-12000:], language="text")
                st.download_button("Download full failed-run log", failure["diagnostics"],
                                   "river_failed_run.txt", "text/plain")
    render_results(st, p, solver)


if __name__ == "__main__":
    main()
