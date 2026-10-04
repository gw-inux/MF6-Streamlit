"""
Streamlit + FloPy teaching app for a steady 2-D x-z groundwater-flow
cross section solved with MODFLOW-NWT and optionally tracked backward with
MODPATH 6.

Conceptual/numerical defaults
-----------------------------
* one MODFLOW row, 1 m width, fixed model length = 10 km
* no-flow left boundary and bottom; uniform recharge from the top
* vertically discretized CHD area at the right outlet
* initial UI mode = Individual setting; Presets A/B provide guided investigations
* dx = 100 m; dz = 10 m; all layers convertible (UPW + NWT)
* CHD reference elevation = 60 m above model bottom; Preset A uses one CHD layer
* optional backward MODPATH 6 releases with independently controlled counts left of and below the CHD

Code map (line ranges in this file)
-----------------------------------
01. Imports, data containers, input helper ........ lines 37-249
02. Geometry and CHD helpers ...................... lines 250-376
03. Executable discovery .......................... lines 377-423
04. MODFLOW-NWT construction and execution ........ lines 424-721
05. MODPATH 6 backward tracking ................... lines 722-977
06. Plotting / water-table interpolation .......... lines 978-1761
07. Session-state signatures ...................... lines 1762-1817
08. Streamlit UI, presets, execution, results ..... lines 1818-end

Run locally
-----------
    pip install streamlit flopy numpy matplotlib
    streamlit run modflow_nwt_potentiometric_cross_section_app.py

Required external executables:
* Streamlit Cloud / Linux: bundle `bin/mfnwt` and `bin/mp6` beside this app.
* Local Windows: MODFLOW-NWT_64.exe/mfnwt.exe and mpath6.exe/mp6.exe on PATH also work.
"""

from __future__ import annotations

import gc
import math
import os
import shutil
import stat
import subprocess
import tempfile
import uuid
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Optional

APP_DIR = Path(__file__).resolve().parent

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st



try:
    import flopy
    # FloPy exposes the MODPATH 6 starting-location writer from the mp6sim
    # module, not from the top-level flopy.modpath namespace in several
    # commonly installed releases. Import it explicitly for compatibility.
    from flopy.modpath.mp6sim import StartingLocationsFile as MP6StartingLocationsFile
except ImportError as err:  # pragma: no cover
    st.error(
        "FloPy is not installed or its MODPATH 6 support is unavailable. "
        "Install/update it with `pip install flopy` and restart the app."
    )
    st.stop()
    raise err


# -----------------------------------------------------------------------------
# Data containers
# -----------------------------------------------------------------------------
@dataclass(frozen=True)
class Config:
    recharge_mm_yr: float = 200.0
    river_level_above_bottom: float = 60.0
    chd_thickness_m: float = 10.0
    kx_m_s: float = 1.0e-4
    kz_over_kx: float = 0.1
    porosity: float = 0.25
    model_length_m: float = 10_000.0
    model_bottom: float = 0.0
    model_top: float = 130.0
    target_dx: float = 100.0
    target_dz: float = 10.0
    width_y: float = 1.0
    n_particles_left: int = 4
    n_particles_below: int = 4
    contour_interval: float = 5.0
    water_table_method: str = "smooth_pchip"
    water_table_smoothing_m: float = 500.0
    show_dupuit: bool = False

    @property
    def recharge_m_day(self) -> float:
        return self.recharge_mm_yr / 1000.0 / 365.25

    @property
    def recharge_m_s(self) -> float:
        return self.recharge_m_day / 86400.0

    @property
    def kz_m_s(self) -> float:
        return self.kx_m_s * self.kz_over_kx

    @property
    def river_reference_elevation(self) -> float:
        return self.model_bottom + self.river_level_above_bottom


@dataclass
class Geometry:
    x: np.ndarray
    x_edges: np.ndarray
    delr: np.ndarray
    model_top: np.ndarray
    botm: np.ndarray
    zc: np.ndarray
    z_edges: np.ndarray
    active: np.ndarray

    @property
    def nlay(self) -> int:
        return int(self.botm.shape[0])

    @property
    def ncol(self) -> int:
        return int(self.botm.shape[2])

    @property
    def dx(self) -> float:
        return float(self.delr[0])


@dataclass
class FlowResult:
    workspace: Path
    modelname: str
    geometry: Geometry
    head: np.ndarray
    water_table: np.ndarray
    ibound: np.ndarray
    river_layer: int
    chd_layers: tuple[int, ...]
    river_head: float
    chd_actual_thickness_m: float
    recharge_in: float
    constant_head_out: float
    budget_error_pct: float
    solver_profile: str
    outlet_wet_cells_above: int
    outlet_head_above: float


# -----------------------------------------------------------------------------
# Reusable Streamlit parameter input helper
# -----------------------------------------------------------------------------
def parameter_input(
    label,
    *,
    key,
    min_value,
    max_value,
    default,
    number_mode,
    scale="linear",
    number_format="%.2e",
    number_step=None,
    log_steps_per_decade=20,
    help=None,
):
    """Render one parameter as either a slider or a number input.

    The physical value is stored independently from the active widget. This is
    the established input-mode pattern used in the other teaching apps: a user
    can switch input mode without changing the parameter value.
    """
    value_key = f"{key}__value"
    number_key = f"_{key}__number"
    slider_key = f"_{key}__slider"

    if value_key not in st.session_state:
        st.session_state[value_key] = float(default)

    current = float(st.session_state[value_key])
    current = min(max(current, float(min_value)), float(max_value))
    st.session_state[value_key] = current

    def _update_from_number():
        value = float(st.session_state[number_key])
        st.session_state[value_key] = min(max(value, float(min_value)), float(max_value))

    def _update_from_slider():
        st.session_state[value_key] = float(st.session_state[slider_key])

    if number_mode:
        if number_step is None:
            magnitude = 10.0 ** np.floor(np.log10(max(current, float(min_value))))
            widget_step = max(float(min_value), magnitude / 10.0)
        else:
            widget_step = float(number_step)
        st.session_state[number_key] = current
        st.number_input(
            label,
            min_value=float(min_value),
            max_value=float(max_value),
            step=float(widget_step),
            format=number_format,
            key=number_key,
            on_change=_update_from_number,
            help=help,
        )
    else:
        if scale == "log":
            decades = np.log10(float(max_value)) - np.log10(float(min_value))
            n_steps = int(round(decades * int(log_steps_per_decade))) + 1
            options = [
                float(v)
                for v in np.logspace(
                    np.log10(float(min_value)),
                    np.log10(float(max_value)),
                    n_steps,
                )
            ]
            if not any(np.isclose(current, v, rtol=1e-12, atol=0.0) for v in options):
                options.append(current)
                options.sort()
            st.session_state[slider_key] = current
            st.select_slider(
                label,
                options=options,
                key=slider_key,
                format_func=lambda value: f"{value:.2e}",
                on_change=_update_from_slider,
                help=help,
            )
        else:
            st.session_state[slider_key] = current
            st.slider(
                label,
                min_value=float(min_value),
                max_value=float(max_value),
                key=slider_key,
                on_change=_update_from_slider,
                help=help,
            )

    return float(st.session_state[value_key])


# -----------------------------------------------------------------------------
# Geometry helpers
# -----------------------------------------------------------------------------
def make_geometry(config: Config) -> Geometry:
    """Construct the uniform structured x-z grid.

    The model length is fixed to 10 km. Horizontal nodes are cell centred and
    the vertical grid is horizontal with nominal spacing ``target_dz``. The
    lowest layer is shortened only when necessary to meet the model bottom.
    """
    length = float(config.model_length_m)
    ncol = max(2, int(round(length / config.target_dx)))
    dx = length / ncol
    x_edges = np.linspace(0.0, length, ncol + 1)
    x = 0.5 * (x_edges[:-1] + x_edges[1:])
    delr = np.full(ncol, dx, dtype=float)

    grid_top_elev = float(config.model_top)
    dz = float(config.target_dz)
    z_edges = [grid_top_elev]
    z = grid_top_elev
    while z - dz > config.model_bottom + 1.0e-9:
        z -= dz
        z_edges.append(z)
    if z_edges[-1] > config.model_bottom + 1.0e-9:
        z_edges.append(float(config.model_bottom))
    z_edges = np.asarray(z_edges, dtype=float)

    nlay = len(z_edges) - 1
    botm_1d = z_edges[1:]
    botm = np.broadcast_to(botm_1d[:, None, None], (nlay, 1, ncol)).copy()
    zc_1d = 0.5 * (z_edges[:-1] + z_edges[1:])
    zc = np.broadcast_to(zc_1d[:, None, None], (nlay, 1, ncol)).copy()
    model_top = np.full((1, ncol), grid_top_elev, dtype=float)
    active = np.ones((nlay, 1, ncol), dtype=bool)

    return Geometry(
        x=x,
        x_edges=x_edges,
        delr=delr,
        model_top=model_top,
        botm=botm,
        zc=zc,
        z_edges=z_edges,
        active=active,
    )


def river_layer_from_geometry(geometry: Geometry, river_reference_elevation: float) -> int:
    """Find the right-edge layer whose vertical interval contains river stage."""
    for k in range(geometry.nlay):
        cell_top = geometry.z_edges[k]
        cell_bot = geometry.z_edges[k + 1]
        if (
            river_reference_elevation <= cell_top + 1.0e-10
            and river_reference_elevation >= cell_bot - 1.0e-10
        ):
            if not geometry.active[k, 0, -1]:
                raise ValueError(
                    "The cell intersecting the river stage is inactive. "
                    "Check river stage and right-side land-surface elevation."
                )
            return k
    raise ValueError(
        "River reference elevation does not intersect the model grid. "
        "Check model bottom, dz, and river elevation above bottom."
    )


def river_cell_head(geometry: Geometry, river_layer: int) -> float:
    """Return the CHD head at the vertical centre of the selected river cell."""
    return 0.5 * (
        float(geometry.z_edges[river_layer])
        + float(geometry.z_edges[river_layer + 1])
    )


def chd_layers_from_thickness(
    geometry: Geometry, river_layer: int, requested_thickness_m: float
) -> tuple[int, ...]:
    """Return contiguous CHD layers starting at the head-defining cell.

    The requested CHD thickness is represented discretely by the minimum number
    of cells, starting with the cell whose centre defines the specified head and
    extending downward, whose cumulative thickness reaches the requested value.
    """
    requested = max(float(requested_thickness_m), 0.0)
    layers: list[int] = []
    cumulative = 0.0
    for k in range(int(river_layer), geometry.nlay):
        if not geometry.active[k, 0, -1]:
            continue
        layers.append(k)
        cumulative += float(geometry.z_edges[k] - geometry.z_edges[k + 1])
        if cumulative + 1.0e-9 >= requested:
            break
    if not layers:
        raise ValueError("No active cells are available for the CHD boundary.")
    return tuple(layers)


def chd_actual_thickness(geometry: Geometry, chd_layers: tuple[int, ...]) -> float:
    return float(
        sum(float(geometry.z_edges[k] - geometry.z_edges[k + 1]) for k in chd_layers)
    )


def extract_water_table(
    head: np.ndarray,
    botm: np.ndarray,
    ibound: np.ndarray,
    hdry_cutoff: float = -1.0e20,
) -> np.ndarray:
    """Head in the uppermost wet active cell of each vertical column."""
    nlay, _, ncol = head.shape
    wt = np.full(ncol, np.nan, dtype=float)
    for j in range(ncol):
        for k in range(nlay):
            if ibound[k, 0, j] == 0:
                continue
            h = float(head[k, 0, j])
            if np.isfinite(h) and h > hdry_cutoff and h > botm[k, 0, j] + 1.0e-6:
                wt[j] = h
                break
    return wt


# -----------------------------------------------------------------------------
# Executable handling
# -----------------------------------------------------------------------------
def _make_executable(path: Path) -> None:
    """Restore execute permissions for bundled Linux binaries when needed."""
    try:
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except OSError:
        # On Windows the executable bit is not relevant; on a read-only file
        # system the subsequent executable check will decide whether it is usable.
        pass


def resolve_executable(exe) -> Optional[str]:
    """Resolve an executable from an explicit path or the system PATH.

    Repository-local binaries are passed as absolute/relative paths.  If such a
    file exists, its Linux execute bit is repaired before it is handed to FloPy.
    Plain executable names fall back to ``shutil.which`` for local installations.
    """
    exe = str(exe).strip().strip('"')
    if not exe:
        return None

    p = Path(exe).expanduser()
    if p.is_file():
        _make_executable(p)
        if os.name == "nt" or os.access(p, os.X_OK):
            return str(p.resolve())

    resolved = shutil.which(exe)
    if resolved:
        rp = Path(resolved)
        _make_executable(rp)
        return str(rp.resolve())
    return None


def find_first_executable(candidates) -> Optional[str]:
    for candidate in candidates:
        resolved = resolve_executable(candidate)
        if resolved:
            return resolved
    return None


def _environment_executable(*names: str) -> Optional[str]:
    """Return the first valid executable referenced by an environment variable."""
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            resolved = resolve_executable(value)
            if resolved:
                return resolved
    return None


def find_mfnwt_executable() -> Optional[str]:
    """Locate MODFLOW-NWT on Streamlit Cloud or a local workstation."""
    from_env = _environment_executable("MFNWT_EXE", "MFNWT_EXECUTABLE")
    if from_env:
        return from_env

    return find_first_executable(
        [
            # Preferred Streamlit Community Cloud layout.
            APP_DIR / "bin" / "mfnwt",
            APP_DIR / "bin" / "mfnwtdbl",
            # Also allow binaries placed directly beside the app.
            APP_DIR / "mfnwt",
            APP_DIR / "mfnwtdbl",
            # Local Windows / PATH fallbacks.
            "MODFLOW-NWT_64.exe",
            "MODFLOW-NWT_64",
            "mfnwt.exe",
            "mfnwt",
            "mfnwtdbl.exe",
            "mfnwtdbl",
        ]
    )


def find_mp6_executable() -> Optional[str]:
    """Locate MODPATH 6 on Streamlit Cloud or a local workstation."""
    from_env = _environment_executable("MP6_EXE", "MODPATH6_EXE", "MP6_EXECUTABLE")
    if from_env:
        return from_env

    return find_first_executable(
        [
            # Preferred Streamlit Community Cloud layout.
            APP_DIR / "bin" / "mp6",
            APP_DIR / "bin" / "mpath6",
            # Also allow binaries placed directly beside the app.
            APP_DIR / "mp6",
            APP_DIR / "mpath6",
            # Local Windows / PATH fallbacks.
            "mpath6.exe",
            "mpath6",
            "mp6.exe",
            "mp6",
            "MODPATH6.exe",
            "MODPATH6",
            "modpath6.exe",
            "modpath6",
        ]
    )


# -----------------------------------------------------------------------------
# MODFLOW-NWT model
# -----------------------------------------------------------------------------
def build_flow_model(
    config: Config,
    workspace: Path,
    mfnwt_exe: str,
    modelname: str = "xsec_nwt",
    solver_profile: str = "complex_standard",
):
    geometry = make_geometry(config)
    river_layer = river_layer_from_geometry(
        geometry, config.river_reference_elevation
    )
    chd_head = river_cell_head(geometry, river_layer)
    chd_layers = chd_layers_from_thickness(
        geometry, river_layer, config.chd_thickness_m
    )

    workspace.mkdir(parents=True, exist_ok=True)

    mf = flopy.modflow.Modflow(
        modelname=modelname,
        exe_name=mfnwt_exe,
        version="mfnwt",
        model_ws=str(workspace),
    )

    flopy.modflow.ModflowDis(
        mf,
        nlay=geometry.nlay,
        nrow=1,
        ncol=geometry.ncol,
        nper=1,
        delr=geometry.delr,
        delc=config.width_y,
        top=geometry.model_top,
        botm=geometry.botm,
        perlen=1.0,
        nstp=1,
        steady=True,
        itmuni=1,  # seconds
        lenuni=2,  # metres
    )

    ibound = geometry.active.astype(np.int32)
    # Keep BAS cells active; the outlet is represented explicitly by the CHD package.
    strt = np.full((geometry.nlay, 1, geometry.ncol), float(config.model_top), dtype=float)

    flopy.modflow.ModflowBas(
        mf,
        ibound=ibound,
        strt=strt,
        hnoflo=-999.99,
    )

    flopy.modflow.ModflowUpw(
        mf,
        laytyp=np.ones(geometry.nlay, dtype=int),
        layavg=0,
        chani=1.0,
        layvka=0,  # VKA is entered as vertical K directly
        laywet=0,
        ipakcb=53,
        hdry=-1.0e30,
        iphdry=1,  # required for robust MODPATH interpretation of NWT dry cells
        hk=config.kx_m_s,
        vka=config.kz_m_s,
        ss=1.0e-5,
        sy=0.20,
    )

    chd_spd = [
        [k, 0, geometry.ncol - 1, chd_head, chd_head]
        for k in chd_layers
    ]
    flopy.modflow.ModflowChd(
        mf,
        stress_period_data={0: chd_spd},
        ipakcb=53,
    )

    flopy.modflow.ModflowRch(
        mf,
        nrchop=1,  # recharge to top layer
        ipakcb=53,
        rech=np.full((1, geometry.ncol), config.recharge_m_s, dtype=float),
    )

    # Solver continuation is used only if a fine-grid run needs it. The first
    # attempt keeps a very small dry-cell transition zone. A fallback increases
    # THICKFACT from 1e-4 to 1e-3; for dz=10 m this is still only 0.01 m. The
    # final fallback also tests IBOTAV=1, whose convergence behaviour USGS notes
    # is problem-specific. All physical model inputs remain unchanged.
    use_smoothing = "smooth" in solver_profile
    ibotav = 1 if solver_profile.endswith("ibotav1") else 0
    flopy.modflow.ModflowNwt(
        mf,
        headtol=1.0e-4,
        fluxtol=1.0e-3,
        maxiterout=500,
        thickfact=1.0e-3 if use_smoothing else 1.0e-4,
        linmeth=2,  # XMD linear solver
        iprnwt=0,
        ibotav=ibotav,
        options="COMPLEX",
    )

    oc = flopy.modflow.ModflowOc(
        mf,
        stress_period_data={(0, 0): ["save head", "save budget", "print budget"]},
        compact=True,
    )
    oc.reset_budgetunit(budgetunit=53, fname=f"{modelname}.cbc")

    return mf, geometry, ibound, river_layer, chd_layers, chd_head

def _budget_array(cbc, text: str) -> Optional[np.ndarray]:
    try:
        records = cbc.get_data(text=text, full3D=True)
    except Exception:
        return None
    if not records:
        return None
    return np.asarray(np.ma.filled(records[-1], 0.0), dtype=float)


def _close_flopy_reader(reader) -> None:
    """Close a FloPy binary reader robustly across FloPy versions."""
    if reader is None:
        return
    try:
        close = getattr(reader, "close", None)
        if callable(close):
            close()
            return
    except Exception:
        pass
    for attr in ("file", "_file"):
        try:
            fobj = getattr(reader, attr, None)
            close = getattr(fobj, "close", None)
            if callable(close):
                close()
                return
        except Exception:
            pass


def run_flow_model(
    config: Config,
    workspace: Path,
    mfnwt_exe: str,
    modelname: str = "xsec_nwt",
) -> FlowResult:
    """Run NWT with a conservative solver fallback sequence.

    Every attempt has its own subdirectory, so neither Streamlit reruns nor
    failed native executables require deleting files that Windows may still
    have open. Physical model inputs are identical between attempts.
    """
    workspace.mkdir(parents=True, exist_ok=False)

    attempt_profiles = [
        ("COMPLEX / standard", "complex_standard"),
        ("COMPLEX / dry-cell smoothing", "complex_smooth"),
        ("COMPLEX / dry-cell smoothing / IBOTAV=1", "complex_smooth_ibotav1"),
    ]
    failed_outputs: list[tuple[str, list[str]]] = []

    for i, (label, profile) in enumerate(attempt_profiles, start=1):
        attempt_ws = workspace / f"attempt_{i}"
        attempt_ws.mkdir(parents=True, exist_ok=False)

        mf, geometry, ibound, river_layer, chd_layers, chd_head = build_flow_model(
            config,
            attempt_ws,
            mfnwt_exe,
            modelname=modelname,
            solver_profile=profile,
        )
        mf.write_input()
        success, buff = mf.run_model(silent=True, report=True)
        run_output = [str(line) for line in (buff or [])]

        if not success:
            failed_outputs.append((label, run_output[-50:]))
            del mf
            gc.collect()
            continue

        hds_path = attempt_ws / f"{modelname}.hds"
        cbc_path = attempt_ws / f"{modelname}.cbc"
        if not hds_path.exists() or not cbc_path.exists():
            failed_outputs.append(
                (label, run_output[-50:] + ["Expected HDS/CBC output was not written."])
            )
            del mf
            gc.collect()
            continue

        hds = None
        try:
            hds = flopy.utils.HeadFile(str(hds_path))
            times = hds.get_times()
            if not times:
                raise RuntimeError("The MODFLOW head file contains no output times.")
            head = np.asarray(hds.get_data(totim=times[-1]), dtype=float).copy()
        finally:
            _close_flopy_reader(hds)

        wt = extract_water_table(head, geometry.botm, ibound)
        if not np.isfinite(wt).any():
            failed_outputs.append((label, run_output[-50:] + ["No finite water table found."]))
            del mf
            gc.collect()
            continue

        cbc = None
        try:
            cbc = flopy.utils.CellBudgetFile(str(cbc_path), precision="auto")
            rch = _budget_array(cbc, "RECHARGE")
            chd = _budget_array(cbc, "CONSTANT HEAD")
        finally:
            _close_flopy_reader(cbc)

        recharge_in = float(np.sum(rch[rch > 0.0])) if rch is not None else float("nan")
        constant_head_out = (
            float(-np.sum(chd[chd < 0.0])) if chd is not None else float("nan")
        )

        if np.isfinite(recharge_in) and np.isfinite(constant_head_out):
            denom = 0.5 * (recharge_in + constant_head_out)
            budget_error_pct = (
                100.0 * (recharge_in - constant_head_out) / denom
                if denom > 0.0
                else float("nan")
            )
        else:
            budget_error_pct = float("nan")

        # Diagnose hydraulic connection above the top of the CHD interval.
        # Wet cells above the specified-head area can drive a downward
        # component into the outlet boundary.
        wet_cells_above = 0
        head_above = float("nan")
        if river_layer > 0:
            for kk in range(river_layer):
                h_above_k = float(head[kk, 0, -1])
                if (
                    ibound[kk, 0, -1] != 0
                    and np.isfinite(h_above_k)
                    and h_above_k > -1.0e20
                    and h_above_k > geometry.botm[kk, 0, -1] + 1.0e-7
                ):
                    wet_cells_above += 1
            kk = river_layer - 1
            h_above_k = float(head[kk, 0, -1])
            if (
                ibound[kk, 0, -1] != 0
                and np.isfinite(h_above_k)
                and h_above_k > -1.0e20
                and h_above_k > geometry.botm[kk, 0, -1] + 1.0e-7
            ):
                head_above = h_above_k

        del mf
        gc.collect()

        return FlowResult(
            workspace=attempt_ws,
            modelname=modelname,
            geometry=geometry,
            head=head,
            water_table=wt,
            ibound=ibound,
            river_layer=river_layer,
            chd_layers=tuple(chd_layers),
            river_head=chd_head,
            chd_actual_thickness_m=chd_actual_thickness(geometry, tuple(chd_layers)),
            recharge_in=recharge_in,
            constant_head_out=constant_head_out,
            budget_error_pct=budget_error_pct,
            solver_profile=label,
            outlet_wet_cells_above=wet_cells_above,
            outlet_head_above=head_above,
        )

    details: list[str] = []
    for label, lines in failed_outputs:
        details.append(f"--- {label} ---")
        details.extend(lines)
    raise RuntimeError(
        "MODFLOW-NWT did not terminate normally with the robust solver sequence.\n\n"
        + "\n".join(details[-120:])
    )


# -----------------------------------------------------------------------------
# MODPATH 6
# -----------------------------------------------------------------------------
def _sample_vertical_saturated_intervals(
    result: FlowResult,
    column: int,
    layers_to_sample: tuple[int, ...],
    n_particles: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Sample saturated thickness regularly over selected cells in one column."""
    n = max(1, int(n_particles))
    g = result.geometry
    intervals: list[tuple[int, float, float]] = []
    for k in reversed(layers_to_sample):  # bottom upward
        if k < 0 or k >= g.nlay or result.ibound[k, 0, column] == 0:
            continue
        cell_top = float(g.z_edges[k])
        cell_bot = float(g.z_edges[k + 1])
        h = float(result.head[k, 0, column])
        if not np.isfinite(h) or h <= -1.0e20:
            continue
        effective_top = min(cell_top, h)
        if effective_top > cell_bot + 1.0e-8:
            intervals.append((k, cell_bot, effective_top))

    if not intervals:
        raise RuntimeError("No saturated neighboring cells are available for particle release.")

    thicknesses = np.asarray([top - bot for _, bot, top in intervals], dtype=float)
    total = float(np.sum(thicknesses))
    if total <= 0.0:
        raise RuntimeError("Saturated neighboring thickness is zero.")

    if n == 1:
        distances = np.asarray([0.5 * total], dtype=float)
    else:
        inset = min(0.02 * total, 0.05)
        distances = np.linspace(inset, total - inset, n)

    cum = np.cumsum(thicknesses)
    prev = np.concatenate(([0.0], cum[:-1]))
    out_layers = np.empty(n, dtype=int)
    localz = np.empty(n, dtype=float)
    release_z = np.empty(n, dtype=float)
    for ip, distance in enumerate(distances):
        ii = min(int(np.searchsorted(cum, distance, side="right")), len(intervals) - 1)
        k, bot, top = intervals[ii]
        within = float(np.clip(distance - prev[ii], 0.0, top - bot))
        frac = float(np.clip(within / (top - bot), 0.01, 0.99))
        out_layers[ip] = k
        localz[ip] = frac
        release_z[ip] = bot + frac * (top - bot)
    return out_layers, localz, release_z


def _neighbor_particle_locations(
    result: FlowResult,
    n_left: int,
    n_below: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Build backward releases immediately left of and below the CHD.

    ``n_left`` controls the regular vertical distribution in the neighboring
    column left of the CHD. ``n_below`` controls the regular horizontal
    distribution in the cell below the lowest CHD cell. The two counts are
    independent; at least one must be positive.
    """
    n_left = max(0, int(n_left))
    n_below = max(0, int(n_below))
    if n_left + n_below < 1:
        raise RuntimeError("At least one backward particle is required.")

    g = result.geometry
    j_chd = g.ncol - 1
    j_left = max(0, j_chd - 1)
    chd_layers = tuple(int(k) for k in result.chd_layers)
    lowest_chd = max(chd_layers)
    below_layer = lowest_chd + 1

    layer_parts: list[np.ndarray] = []
    column_parts: list[np.ndarray] = []
    localx_parts: list[np.ndarray] = []
    localz_parts: list[np.ndarray] = []

    if n_left > 0:
        left_layers, left_localz, _ = _sample_vertical_saturated_intervals(
            result, j_left, chd_layers, n_left
        )
        layer_parts.append(left_layers)
        column_parts.append(np.full(n_left, j_left, dtype=int))
        localx_parts.append(np.full(n_left, 0.99, dtype=float))
        localz_parts.append(left_localz)

    if n_below > 0:
        if below_layer >= g.nlay or result.ibound[below_layer, 0, j_chd] == 0:
            raise RuntimeError(
                "Particles below the CHD were requested, but no active cell exists below the CHD area."
            )
        k = int(below_layer)
        cell_top = float(g.z_edges[k])
        cell_bot = float(g.z_edges[k + 1])
        h = float(result.head[k, 0, j_chd])
        effective_top = min(cell_top, h)
        if not np.isfinite(h) or h <= -1.0e20 or effective_top <= cell_bot + 1.0e-8:
            raise RuntimeError(
                "Particles below the CHD were requested, but the cell below the "
                "CHD is dry or has negligible saturated thickness."
            )

        layer_parts.append(np.full(n_below, k, dtype=int))
        column_parts.append(np.full(n_below, j_chd, dtype=int))
        if n_below == 1:
            below_localx = np.asarray([0.5], dtype=float)
        else:
            below_localx = np.linspace(0.05, 0.95, n_below, dtype=float)
        localx_parts.append(below_localx)
        localz_parts.append(np.full(n_below, 0.99, dtype=float))

    return (
        np.concatenate(layer_parts),
        np.concatenate(column_parts),
        np.concatenate(localx_parts),
        np.concatenate(localz_parts),
    )


def run_modpath6_from_existing_flow(
    result: FlowResult,
    config: Config,
    mp6_exe: str,
):
    """Run steady-state backward MODPATH 6 from cells neighboring the CHD."""
    ws = Path(result.workspace)
    flow_nam = ws / f"{result.modelname}.nam"
    if not flow_nam.exists():
        raise RuntimeError(f"Completed MODFLOW name file not found: {flow_nam}")

    flow_model = flopy.modflow.Modflow.load(
        flow_nam.name,
        model_ws=str(ws),
        exe_name=None,
        version="mfnwt",
        check=False,
        forgive=False,
    )
    if flow_model is None:
        raise RuntimeError("FloPy could not reload the completed MODFLOW-NWT model.")

    mp_name = f"{result.modelname}_mp6_{uuid.uuid4().hex[:8]}"
    mp = flopy.modpath.Modpath6(
        modelname=mp_name,
        exe_name=mp6_exe,
        modflowmodel=flow_model,
        model_ws=str(ws),
    )

    flopy.modpath.Modpath6Bas(
        mp,
        hnoflo=float(flow_model.bas6.hnoflo),
        hdry=float(flow_model.upw.hdry),
        def_face_ct=1,
        bud_label=["RECHARGE"],
        def_iface=[6],
        laytyp=np.asarray(flow_model.upw.laytyp.array, dtype=int),
        ibound=np.asarray(flow_model.bas6.ibound.array, dtype=int),
        prsity=float(config.porosity),
    )
    layers, columns, xlocs, zlocs = _neighbor_particle_locations(
        result, int(config.n_particles_left), int(config.n_particles_below)
    )
    n = int(len(layers))

    loc = MP6StartingLocationsFile(mp, inputstyle=1, extension="loc", use_pandas=False)
    pdata = loc.get_empty_starting_locations_data(n)
    pdata["particlegroup"] = 1
    pdata["initialgrid"] = 1
    pdata["k0"] = layers
    pdata["i0"] = 0
    pdata["j0"] = columns
    pdata["xloc0"] = xlocs
    pdata["yloc0"] = 0.5
    pdata["zloc0"] = zlocs
    pdata["initialtime"] = 0.0
    pdata["groupname"] = "outlet_neighbors"
    for ip in range(n):
        pdata["label"][ip] = f"neighbor_{ip + 1}"
    loc.data = pdata
    loc.write_file()
    loc_filename = f"{mp_name}.loc"

    sim = mp.create_mpsim(
        trackdir="backward",
        simtype="pathline",
        packages=loc_filename,
        start_time=(0, 0, 1.0),
    )
    sim.option_flags[2] = 1
    sim.option_flags[3] = 1
    if hasattr(sim, "options_dict"):
        sim.options_dict["WeakSinkOption"] = 1
        sim.options_dict["WeakSourceOption"] = 1

    mp.write_name_file()
    mp.write_input()
    simfile = f"{mp_name}.mpsim"
    timeout_seconds = 60
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        completed = subprocess.run(
            [str(mp6_exe), simfile],
            cwd=str(ws),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            timeout=timeout_seconds,
            check=False,
            creationflags=creationflags,
        )
        run_output = (completed.stdout or "").splitlines()
    except subprocess.TimeoutExpired as exc:
        captured = exc.stdout or ""
        if isinstance(captured, bytes):
            captured = captured.decode(errors="replace")
        raise RuntimeError(
            f"MODPATH 6 did not finish within {timeout_seconds} s.\n\n"
            + str(captured)[-4000:]
        ) from exc
    if completed.returncode != 0:
        raise RuntimeError(
            f"MODPATH 6 returned exit code {completed.returncode}.\n\n"
            + "\n".join(run_output[-80:])
        )

    pathline_path = ws / f"{mp_name}.mppth"
    if not pathline_path.exists():
        raise RuntimeError(
            "MODPATH 6 reported normal termination but no pathline file was written.\n\n"
            + "\n".join(run_output[-80:])
        )
    pth = None
    try:
        pth = flopy.utils.PathlineFile(str(pathline_path))
        pathlines = pth.get_alldata()
    finally:
        _close_flopy_reader(pth)
    if pathlines is None or len(pathlines) == 0:
        raise RuntimeError("MODPATH 6 terminated normally but returned no pathlines.")

    del mp
    del flow_model
    gc.collect()
    return pathlines


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
def _distance_from_chd_node_km(x_m, geometry: Geometry, model_length_m: float):
    """Convert native x to the node-centred display distance from the CHD.

    For presentation, the CHD node is 0 km and the centre of the first model
    column is exactly ``model_length_m`` upstream. This coordinate transform is
    display-only; MODFLOW and MODPATH retain their native block-centred grid.
    """
    x = np.asarray(x_m, dtype=float)
    x_left = float(geometry.x[0])
    x_chd = float(geometry.x[-1])
    span = x_chd - x_left
    if span <= 0.0:
        return np.zeros_like(x, dtype=float)
    return (float(model_length_m) / 1000.0) * (x_chd - x) / span


def plot_model_preview(config: Config):
    """Plot the node-centred numerical grid and boundary conditions."""
    g = make_geometry(config)
    river_layer = river_layer_from_geometry(g, config.river_reference_elevation)
    chd_head = river_cell_head(g, river_layer)
    chd_layers = chd_layers_from_thickness(g, river_layer, config.chd_thickness_m)
    x_chd = float(g.x[-1])

    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    d_left = float(config.model_length_m) / 1000.0
    ax.fill_between(
        [d_left, 0.0],
        [config.model_bottom, config.model_bottom],
        [config.model_top, config.model_top],
        color="#eef9fb",
        alpha=0.9,
        zorder=0,
        label="Active model domain",
    )

    # Grid lines are deliberately visible in the preview. Distances are
    # measured from the CHD node (cell centre), not from the external model edge.
    for xe in g.x_edges[:-1]:
        d = float(_distance_from_chd_node_km(float(xe), g, config.model_length_m))
        if d >= -1.0e-12:
            ax.plot([d, d], [config.model_bottom, config.model_top], color="0.52", lw=0.60, alpha=0.55)
    for z in g.z_edges:
        ax.plot([d_left, 0.0], [z, z], color="0.52", lw=0.60, alpha=0.55)

    ax.plot(
        [d_left, d_left],
        [config.model_bottom, config.model_top],
        color="0.30",
        lw=1.6,
        ls="--",
        label="No flow",
    )
    ax.axhline(config.model_bottom, color="0.25", lw=1.1)

    # Show the western half of the outlet column up to the node at d=0.
    d_chd_west = float(_distance_from_chd_node_km(float(g.x_edges[-2]), g, config.model_length_m))
    for k in chd_layers:
        top = float(g.z_edges[k])
        bot = float(g.z_edges[k + 1])
        ax.fill_between([d_chd_west, 0.0], [bot, bot], [top, top], color="#1555ff", alpha=0.16, zorder=4)
        ax.plot(
            [d_chd_west, 0.0, 0.0, d_chd_west, d_chd_west],
            [bot, bot, top, top, bot],
            color="#1555ff",
            lw=0.9,
            alpha=0.80,
            zorder=5,
        )
    ax.plot(
        [d_chd_west, 0.0],
        [chd_head, chd_head],
        color="#1555ff",
        lw=4.0,
        solid_capstyle="round",
        label=f"Specified head = {chd_head:g} m",
        zorder=6,
    )

    ax.set_xlim(d_left, 0.0)
    ax.set_ylim(
        config.model_bottom,
        config.model_top + max(5.0, 0.05 * (config.model_top - config.model_bottom)),
    )
    ax.set_xlabel("Distance from CHD node (km; increasing to the left)")
    ax.set_ylabel("Elevation (m)")
    ax.set_title("Model preview before MODFLOW-NWT run")
    ax.grid(False)
    ax.legend(loc="lower left", frameon=False, fontsize=8.5)
    fig.tight_layout()
    return fig, g


def _pava_nonincreasing(values: np.ndarray) -> np.ndarray:
    """Least-squares monotone (non-increasing) fit using pooled adjacent blocks."""
    y = np.asarray(values, dtype=float)
    if y.size <= 1:
        return y.copy()

    means: list[float] = []
    weights: list[float] = []
    starts: list[int] = []
    ends: list[int] = []
    for i, value in enumerate(y):
        means.append(float(value))
        weights.append(1.0)
        starts.append(i)
        ends.append(i)
        while len(means) >= 2 and means[-2] < means[-1]:
            w = weights[-2] + weights[-1]
            means[-2] = (weights[-2] * means[-2] + weights[-1] * means[-1]) / w
            weights[-2] = w
            ends[-2] = ends[-1]
            means.pop()
            weights.pop()
            starts.pop()
            ends.pop()

    out = np.empty_like(y)
    for mean, start_i, end_i in zip(means, starts, ends):
        out[start_i : end_i + 1] = mean
    return out


def _local_quadratic_smooth(x: np.ndarray, y: np.ndarray, bandwidth: float) -> np.ndarray:
    """Smooth a 1-D profile with local weighted quadratic regression.

    The procedure is used only for displaying the phreatic surface.  It is
    deliberately local and shape-preserving at the scale of the model: no
    analytical groundwater assumption is introduced and the raw NWT heads are
    not modified.  Mirrored points at the no-flow divide enforce an
    approximately zero horizontal derivative there.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    out = np.full_like(y, np.nan, dtype=float)
    finite = np.isfinite(x) & np.isfinite(y)
    if np.count_nonzero(finite) < 3:
        return y.copy()

    xf = x[finite]
    yf = y[finite]
    order = np.argsort(xf)
    xf = xf[order]
    yf = yf[order]

    # A short running median removes isolated one-cell layer-transition spikes
    # before the weighted fit. It does not smooth the regional curvature.
    yclean = yf.copy()
    if yf.size >= 5:
        med = yf.copy()
        for i in range(yf.size):
            i0 = max(0, i - 2)
            i1 = min(yf.size, i + 3)
            med[i] = float(np.median(yf[i0:i1]))
        # Only replace conspicuous single-cell deviations.  The threshold is
        # small compared with the 10-m layer thickness but large enough to
        # leave normal regional curvature untouched.
        replace_spike = np.abs(yf - med) > 0.35
        yclean[replace_spike] = med[replace_spike]

    # Mirror the near-divide profile across x=0.  This implements the physical
    # symmetry/no-flow condition dh/dx=0 at the groundwater divide without
    # forcing the head itself to any prescribed value.
    mirror_mask = xf <= max(3.0 * bandwidth, xf[0] + bandwidth)
    xfit_all = np.concatenate((-xf[mirror_mask][::-1], xf))
    yfit_all = np.concatenate((yclean[mirror_mask][::-1], yclean))

    for idx, x0 in enumerate(xf):
        dist = xfit_all - x0
        use = np.abs(dist) <= 3.0 * bandwidth
        if np.count_nonzero(use) < 3:
            # Fall back to the nearest available points.
            nearest = np.argsort(np.abs(dist))[: min(5, dist.size)]
            use = np.zeros(dist.size, dtype=bool)
            use[nearest] = True

        du = dist[use]
        yu = yfit_all[use]
        w = np.exp(-0.5 * (du / bandwidth) ** 2)

        # Local quadratic in coordinates centred on the evaluation point.
        # The intercept is the smoothed head at x0.
        degree = 2 if np.count_nonzero(use) >= 5 else 1
        if degree == 2:
            A = np.column_stack((np.ones_like(du), du, du * du))
        else:
            A = np.column_stack((np.ones_like(du), du))
        sw = np.sqrt(np.maximum(w, 1.0e-12))
        Aw = A * sw[:, None]
        bw = yu * sw
        try:
            coef = np.linalg.lstsq(Aw, bw, rcond=None)[0]
            out_value = float(coef[0])
        except np.linalg.LinAlgError:
            out_value = float(yclean[idx])
        out[np.flatnonzero(finite)[order[idx]]] = out_value

    return out


def _pchip_monotone_interpolate(
    x: np.ndarray,
    y: np.ndarray,
    xq: np.ndarray,
    *,
    left_zero_slope: bool = True,
) -> np.ndarray:
    """Shape-preserving cubic Hermite interpolation for monotone profiles.

    This compact implementation follows the same monotonicity logic as PCHIP
    without adding SciPy as a dependency.  It is used only for plotting the
    phreatic surface; no MODFLOW values are changed.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xq = np.asarray(xq, dtype=float)
    if x.size < 2:
        return np.full_like(xq, y[0] if y.size else np.nan, dtype=float)
    if np.any(np.diff(x) <= 0.0):
        raise ValueError("PCHIP x coordinates must be strictly increasing.")

    h = np.diff(x)
    delta = np.diff(y) / h
    n = x.size
    d = np.zeros(n, dtype=float)

    for i in range(1, n - 1):
        d0 = delta[i - 1]
        d1 = delta[i]
        if d0 == 0.0 or d1 == 0.0 or np.sign(d0) != np.sign(d1):
            d[i] = 0.0
        else:
            w1 = 2.0 * h[i] + h[i - 1]
            w2 = h[i] + 2.0 * h[i - 1]
            d[i] = (w1 + w2) / (w1 / d0 + w2 / d1)

    def _edge_slope(h0: float, h1: float, del0: float, del1: float) -> float:
        val = ((2.0 * h0 + h1) * del0 - h0 * del1) / (h0 + h1)
        if np.sign(val) != np.sign(del0):
            return 0.0
        if np.sign(del0) != np.sign(del1) and abs(val) > abs(3.0 * del0):
            return 3.0 * del0
        return float(val)

    if n == 2:
        d[:] = delta[0]
    else:
        d[0] = 0.0 if left_zero_slope else _edge_slope(h[0], h[1], delta[0], delta[1])
        d[-1] = _edge_slope(h[-1], h[-2], delta[-1], delta[-2])

    xqc = np.clip(xq, x[0], x[-1])
    idx = np.searchsorted(x, xqc, side="right") - 1
    idx = np.clip(idx, 0, n - 2)
    hi = x[idx + 1] - x[idx]
    t = (xqc - x[idx]) / hi
    t2 = t * t
    t3 = t2 * t
    h00 = 2.0 * t3 - 3.0 * t2 + 1.0
    h10 = t3 - 2.0 * t2 + t
    h01 = -2.0 * t3 + 3.0 * t2
    h11 = t3 - t2
    return (
        h00 * y[idx]
        + h10 * hi * d[idx]
        + h01 * y[idx + 1]
        + h11 * hi * d[idx + 1]
    )


def _water_table_observations(result: FlowResult) -> tuple[np.ndarray, np.ndarray]:
    """Return free-surface observations at MODFLOW column centres.

    For every non-CHD column, the observation is the NWT head in the
    uppermost wet active cell and is located at the *horizontal cell centre*.
    The final point is the specified head at the centre of the CHD column.
    This is the spatial location represented by the finite-difference head.
    """
    g = result.geometry
    if g.ncol < 1:
        return np.asarray([], dtype=float), np.asarray([], dtype=float)

    if g.ncol == 1:
        return np.asarray([float(g.x[0])]), np.asarray([float(result.river_head)])

    x_raw = np.asarray(g.x[:-1], dtype=float)
    y_raw = np.asarray(result.water_table[:-1], dtype=float)
    finite = np.isfinite(x_raw) & np.isfinite(y_raw)
    x = x_raw[finite]
    y = y_raw[finite]

    # The specified-head value belongs to the centre of the final CHD column.
    # It is an explicit boundary-condition anchor rather than an inferred
    # water-table value from another cell.
    x = np.append(x, float(g.x[-1]))
    y = np.append(y, float(result.river_head))
    order = np.argsort(x)
    return x[order], y[order]


def _zero_pressure_water_table_observations(
    result: FlowResult, max_cells: int = 3
) -> tuple[np.ndarray, np.ndarray]:
    """Estimate the phreatic surface from h(z)-z = 0 in each column.

    For every non-CHD column, a least-squares line h(z)=a*z+b is fitted to
    the uppermost 2--3 wet active cell heads located at their geometric cell
    centres. The water-table estimate is the elevation where pressure head
    vanishes, i.e. h(z)-z=0. If the local fit is ill-conditioned or produces
    an implausible extrapolation, the raw uppermost-wet-cell head is retained.
    The final CHD-centre point is anchored exactly at the specified head.
    """
    g = result.geometry
    xs: list[float] = []
    zs: list[float] = []

    for j in range(max(0, g.ncol - 1)):
        wet: list[tuple[float, float]] = []
        for k in range(g.nlay):
            if result.ibound[k, 0, j] == 0:
                continue
            h = float(result.head[k, 0, j])
            bot = float(g.z_edges[k + 1])
            if not np.isfinite(h) or h <= -1.0e20 or h <= bot + 1.0e-8:
                continue
            zc = 0.5 * (float(g.z_edges[k]) + bot)
            wet.append((zc, h))
            if len(wet) >= max(2, int(max_cells)):
                break

        raw = float(result.water_table[j]) if np.isfinite(result.water_table[j]) else np.nan
        estimate = raw
        if len(wet) >= 2:
            z = np.asarray([item[0] for item in wet], dtype=float)
            h = np.asarray([item[1] for item in wet], dtype=float)
            A = np.column_stack((z, np.ones_like(z)))
            try:
                a, b = np.linalg.lstsq(A, h, rcond=None)[0]
                denom = 1.0 - float(a)
                if abs(denom) > 1.0e-4:
                    root = float(b / denom)
                    # Accept only a local extrapolation near the uppermost wet
                    # interval. This prevents unstable roots when dh/dz ~ 1.
                    top0 = float(g.z_edges[int(np.flatnonzero(
                        (result.ibound[:, 0, j] != 0)
                        & np.isfinite(result.head[:, 0, j])
                        & (result.head[:, 0, j] > -1.0e20)
                        & (result.head[:, 0, j] > g.botm[:, 0, j] + 1.0e-8)
                    )[0])])
                    dz_ref = max(float(np.max(-np.diff(g.z_edges))), 1.0)
                    lower = float(wet[0][0]) - 1.5 * dz_ref
                    upper = max(top0 + 1.5 * dz_ref, raw + 1.5 * dz_ref if np.isfinite(raw) else top0)
                    if np.isfinite(root) and lower <= root <= upper:
                        estimate = root
            except (np.linalg.LinAlgError, ValueError, FloatingPointError):
                pass

        if np.isfinite(estimate):
            xs.append(float(g.x[j]))
            zs.append(float(estimate))

    xs.append(float(g.x[-1]))
    zs.append(float(result.river_head))
    order = np.argsort(xs)
    return np.asarray(xs, dtype=float)[order], np.asarray(zs, dtype=float)[order]


def _dupuit_water_table_profile(result: FlowResult, config: Config) -> tuple[np.ndarray, np.ndarray]:
    """Analytical Dupuit reference on the app's node-centred 10 km axis.

    The solution uses Kx only and assumes predominantly horizontal flow, so it
    is a diagnostic reference rather than a replacement for the vertically
    anisotropic MODFLOW-NWT solution. For consistency with the displayed model,
    the first and last MODFLOW column centres represent the analytical divide
    and CHD locations and are mapped to 10 km and 0 km, respectively.
    """
    g = result.geometry
    L = float(config.model_length_m)
    if L <= 0.0 or config.kx_m_s <= 0.0:
        return np.asarray([], dtype=float), np.asarray([], dtype=float)
    hr = float(result.river_head - config.model_bottom)
    if hr <= 0.0:
        return np.asarray([], dtype=float), np.asarray([], dtype=float)

    analytical_x = np.linspace(0.0, L, 600)
    native_x = np.linspace(float(g.x[0]), float(g.x[-1]), analytical_x.size)
    radicand = hr * hr + (config.recharge_m_s / config.kx_m_s) * (
        L * L - analytical_x * analytical_x
    )
    z = config.model_bottom + np.sqrt(np.maximum(radicand, 0.0))
    z[-1] = float(result.river_head)
    return native_x, z


def _water_table_profile(
    result: FlowResult,
    method: str = "smooth_pchip",
    smoothing_length_m: float = 500.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Return a display water-table curve using a selectable interpolation.

    All source values are located at MODFLOW column centres.  The curve starts
    at the no-flow divide (x=0) with zero horizontal gradient and terminates at
    the *centre* of the CHD column at the specified head.

    Methods
    -------
    ``linear``
        Piecewise-linear interpolation through the raw uppermost-wet-cell
        heads and the CHD-centre anchor.  This is the most transparent method
        but retains grid-scale steps.
    ``pchip``
        Shape-preserving cubic Hermite interpolation through the raw points.
        It is smoother than linear interpolation and does not introduce the
        oscillatory overshoot typical of an unconstrained cubic spline.
    ``smooth_pchip``
        Recommended display method. A local weighted quadratic regression is
        applied to the non-CHD cell-centre heads, followed by a monotone
        least-squares projection and PCHIP interpolation. The raw MODFLOW
        solution is never modified; this is visualization only.
    ``zero_pressure_pchip``
        Reconstruct the phreatic surface column-by-column by fitting the upper
        wet-cell head profile h(z) and solving h=z (zero pressure head), then
        use shape-preserving PCHIP interpolation between those estimates.
    """
    g = result.geometry
    x_obs, y_obs = _water_table_observations(result)
    if x_obs.size == 0:
        return x_obs, y_obs
    if x_obs.size == 1:
        return x_obs.copy(), y_obs.copy()

    method = str(method).lower().strip()
    if method not in {"linear", "pchip", "smooth_pchip", "zero_pressure_pchip"}:
        method = "smooth_pchip"

    if method == "zero_pressure_pchip":
        x_obs, y_obs = _zero_pressure_water_table_observations(result)
        if x_obs.size == 0:
            return x_obs, y_obs
        if x_obs.size == 1:
            return x_obs.copy(), y_obs.copy()

    # The last observation is the CHD-centre anchor.  Smoothing is applied only
    # to the computed heads; the boundary value itself remains exact.
    y_work = y_obs.copy()
    if method == "smooth_pchip" and x_obs.size >= 4:
        x_num = x_obs[:-1]
        y_num = y_obs[:-1]
        dx = float(g.dx)
        bandwidth = max(float(smoothing_length_m), 2.0 * dx)
        y_smooth = _local_quadratic_smooth(x_num, y_num, bandwidth=bandwidth)
        good = np.isfinite(y_smooth)
        if np.count_nonzero(good) >= 2 and not np.all(good):
            y_smooth[~good] = np.interp(x_num[~good], x_num[good], y_smooth[good])
        elif np.count_nonzero(good) < 2:
            y_smooth = y_num.copy()

        # The homogeneous one-outlet problem should decline toward the outlet.
        # PAVA removes only residual cell-scale reversals in the display curve.
        y_smooth = np.maximum(y_smooth, float(result.river_head))
        y_smooth = _pava_nonincreasing(y_smooth)
        y_work[:-1] = y_smooth

    # Preserve the exact CHD centre head and the expected monotone decline for
    # the recommended method.  Raw linear/PCHIP options deliberately expose the
    # numerical observations without this projection for diagnostic comparison.
    y_work[-1] = float(result.river_head)
    if method in {"smooth_pchip", "zero_pressure_pchip"}:
        y_work = _pava_nonincreasing(y_work)
        y_work[-1] = float(result.river_head)

    # Add the no-flow divide.  The first finite-difference head is at dx/2; the
    # boundary value is mirrored as the same head so dh/dx=0 is respected.
    x_knots = np.concatenate(([0.0], x_obs))
    y_knots = np.concatenate(([float(y_work[0])], y_work))

    # Dense coordinates end at the CHD *cell centre*, not at its western edge.
    x_end = float(g.x[-1])
    target_spacing = max(5.0, min(25.0, float(g.dx) / 4.0))
    n_dense = int(np.clip(math.ceil(x_end / target_spacing) + 1, 250, 4000))
    x_dense = np.linspace(0.0, x_end, n_dense)

    if method == "linear":
        y_dense = np.interp(x_dense, x_knots, y_knots)
    else:
        y_dense = _pchip_monotone_interpolate(
            x_knots,
            y_knots,
            x_dense,
            left_zero_slope=True,
        )
        if method in {"smooth_pchip", "zero_pressure_pchip"}:
            # Guard only against tiny numerical reversals after cubic evaluation.
            y_dense = np.minimum.accumulate(y_dense)

    # Enforce the exact endpoint after floating-point interpolation.
    y_dense[-1] = float(result.river_head)
    return x_dense, y_dense


def water_table_for_plot(result: FlowResult, config: Config) -> np.ndarray:
    """Water-table values at MODFLOW column centres for contour masking."""
    g = result.geometry
    wt = np.full(g.ncol, np.nan, dtype=float)
    x_dense, y_dense = _water_table_profile(
        result,
        method=config.water_table_method,
        smoothing_length_m=config.water_table_smoothing_m,
    )
    if x_dense.size >= 2:
        inside = g.x <= x_dense[-1] + 1.0e-9
        idx = np.flatnonzero(inside)
        wt[idx] = np.interp(g.x[idx], x_dense, y_dense)
    wt[-1] = float(result.river_head)
    return wt


def water_table_plot_coordinates(
    result: FlowResult, config: Config
) -> tuple[np.ndarray, np.ndarray]:
    """Return the selected water-table interpolation in native x coordinates."""
    x_dense, y_dense = _water_table_profile(
        result,
        method=config.water_table_method,
        smoothing_length_m=config.water_table_smoothing_m,
    )
    return x_dense / 1000.0, y_dense


def build_contour_grid(result: FlowResult, config: Config):
    """Create a smooth plotting field from all valid saturated-cell heads.

    Raw MODFLOW values are retained at their physical locations. Shape-
    preserving interpolation is applied vertically and horizontally only for
    visualization. This avoids visible contour-angle changes caused by direct
    piecewise-linear contouring of the finite-difference cell centres.
    """
    g = result.geometry
    H = np.asarray(result.head[:, 0, :], dtype=float)
    ib = np.asarray(result.ibound[:, 0, :])
    bot = np.asarray(g.botm[:, 0, :], dtype=float)

    nint = g.ncol
    wt_x, wt_y = _water_table_profile(
        result,
        method=config.water_table_method,
        smoothing_length_m=config.water_table_smoothing_m,
    )
    if wt_x.size < 2:
        return None, None, None

    x_centres = np.asarray(g.x[:nint], dtype=float)
    wt_centres = np.interp(x_centres, wt_x, wt_y)
    valid = (
        np.isfinite(H[:, :nint])
        & (H[:, :nint] > -1.0e20)
        & (ib[:, :nint] != 0)
        & (H[:, :nint] > bot[:, :nint] + 1.0e-7)
    )

    plot_dz = min(0.5, max(0.1, float(config.target_dz) / 40.0))
    zmax = float(np.nanmax(wt_y))
    nz = max(3, int(math.ceil((zmax - config.model_bottom) / plot_dz)) + 1)
    z_plot = np.linspace(config.model_bottom, zmax, nz)
    h_columns = np.full((nz, nint), np.nan, dtype=float)

    for j in range(nint):
        wj = float(wt_centres[j])
        if not np.isfinite(wj) or wj <= config.model_bottom + 1.0e-9:
            continue
        ks = np.flatnonzero(valid[:, j])
        if ks.size == 0:
            continue

        # Bottom uses the lowest-cell head (zero-gradient plotting extension);
        # the uppermost convertible-cell head is represented by h=z at the
        # reconstructed free surface. All deeper wet-cell heads are included.
        z_nodes = [float(config.model_bottom)]
        h_nodes = [float(H[int(ks[-1]), j])]
        for kk in ks[1:][::-1]:
            zc = float(g.zc[int(kk), 0, j])
            if zc < wj - 1.0e-8:
                z_nodes.append(zc)
                h_nodes.append(float(H[int(kk), j]))
        z_nodes.append(wj)
        h_nodes.append(wj)

        z_nodes = np.asarray(z_nodes, dtype=float)
        h_nodes = np.asarray(h_nodes, dtype=float)
        order = np.argsort(z_nodes)
        z_nodes = z_nodes[order]
        h_nodes = h_nodes[order]

        unique_z: list[float] = []
        unique_h: list[float] = []
        for zz, hh in zip(z_nodes, h_nodes):
            if unique_z and abs(zz - unique_z[-1]) <= 1.0e-8:
                unique_h[-1] = float(hh)
            else:
                unique_z.append(float(zz))
                unique_h.append(float(hh))
        if len(unique_z) < 2:
            continue

        inside = z_plot <= wj + 1.0e-9
        h_columns[inside, j] = _pchip_monotone_interpolate(
            np.asarray(unique_z),
            np.asarray(unique_h),
            z_plot[inside],
            left_zero_slope=True,
        )

    # Interpolate each elevation level onto a dense horizontal grid ending at
    # the CHD node (centre of the final finite-difference cell).
    x_chd = float(g.x[-1])
    target_spacing = max(5.0, min(25.0, float(g.dx) / 4.0))
    nx = int(np.clip(math.ceil(x_chd / target_spacing) + 1, 300, 4000))
    x_dense = np.linspace(0.0, x_chd, nx)
    wt_dense = np.interp(x_dense, wt_x, wt_y)
    h_dense = np.full((nz, nx), np.nan, dtype=float)

    for iz in range(nz):
        row = h_columns[iz, :]
        good = np.flatnonzero(np.isfinite(row))
        if good.size < 2:
            continue

        xr = x_centres[good]
        hr = row[good]
        x_aug = np.concatenate(([0.0], xr))
        h_aug = np.concatenate(([float(hr[0])], hr))

        # For this one-outlet problem head should not increase toward the
        # outlet at a fixed elevation. Remove only cell-scale reversals in the
        # display field; raw heads remain unchanged.
        h_aug = _pava_nonincreasing(h_aug)
        values = _pchip_monotone_interpolate(
            x_aug, h_aug, x_dense, left_zero_slope=True
        )
        wet = z_plot[iz] <= wt_dense + 1.0e-9
        h_dense[iz, wet] = values[wet]

    X, Z = np.meshgrid(x_dense / 1000.0, z_plot)
    return X, Z, h_dense


def plot_cross_section(
    result: FlowResult,
    config: Config,
    pathlines=None,
    display_distance_km: Optional[float] = None,
):
    """Plot the final flow field in distance from the node-centred CHD outlet."""
    g = result.geometry
    max_distance_km = float(config.model_length_m) / 1000.0
    wt_xkm, wt_plot = water_table_plot_coordinates(result, config)
    wt_d = _distance_from_chd_node_km(wt_xkm * 1000.0, g, config.model_length_m)

    fig, ax = plt.subplots(figsize=(9.2, 5.6))

    if wt_xkm.size >= 2:
        ax.fill_between(
            wt_d,
            config.model_bottom,
            wt_plot,
            where=np.isfinite(wt_plot),
            color="#dff7fb",
            alpha=0.95,
            zorder=0,
        )
        ax.plot(wt_d, wt_plot, color="black", lw=2.0, label="Water table", zorder=5)

    Xc, Zc, Hc = build_contour_grid(result, config)
    if Xc is not None and Zc is not None and Hc is not None:
        finite_heads = Hc[np.isfinite(Hc)]
        if finite_heads.size:
            hmin = max(result.river_head, float(np.nanmin(finite_heads)))
            hmax = float(np.nanmax(finite_heads))
            step = float(config.contour_interval)
            first = math.ceil(hmin / step) * step
            last = math.floor(hmax / step) * step
            if last >= first:
                levels = np.arange(first, last + 0.5 * step, step)
                Dc = _distance_from_chd_node_km(Xc * 1000.0, g, config.model_length_m)
                cs = ax.contour(
                    Dc,
                    Zc,
                    np.ma.masked_invalid(Hc),
                    levels=levels,
                    colors="black",
                    linewidths=1.1,
                    zorder=3,
                )
                ax.clabel(cs, fmt=lambda v: f"{v:.0f}", fontsize=8.5, inline=True)

    dupuit_ymax = float("nan")
    if config.show_dupuit:
        x_dup, y_dup = _dupuit_water_table_profile(result, config)
        if x_dup.size >= 2:
            d_dup = _distance_from_chd_node_km(x_dup, g, config.model_length_m)
            ax.plot(
                d_dup,
                y_dup,
                color="#f28e2b",
                lw=1.6,
                ls="--",
                label="Dupuit analytical reference",
                zorder=7,
            )
            finite_dupuit = y_dup[np.isfinite(y_dup)]
            if finite_dupuit.size:
                dupuit_ymax = float(np.max(finite_dupuit))

    if pathlines is not None:
        for rec in pathlines:
            if rec is None or len(rec) < 1:
                continue
            ax.plot(
                _distance_from_chd_node_km(np.asarray(rec["x"], dtype=float), g, config.model_length_m),
                rec["z"],
                color="#1555ff",
                lw=1.35,
                alpha=0.90,
                zorder=4,
            )

    # Show the discretized CHD interval in the western half of the final cell,
    # up to the CHD node at distance zero.
    d_chd_west = float(_distance_from_chd_node_km(float(g.x_edges[-2]), g, config.model_length_m))
    for k in result.chd_layers:
        top = float(g.z_edges[k])
        bot = float(g.z_edges[k + 1])
        ax.fill_between([d_chd_west, 0.0], [bot, bot], [top, top], color="#1555ff", alpha=0.16, zorder=2)
        ax.plot(
            [d_chd_west, 0.0, 0.0, d_chd_west, d_chd_west],
            [bot, bot, top, top, bot],
            color="#1555ff",
            lw=0.8,
            alpha=0.75,
            zorder=6,
        )
    ax.plot(
        [d_chd_west, 0.0],
        [result.river_head, result.river_head],
        color="#1555ff",
        lw=4.5,
        solid_capstyle="round",
        label=f"Specified head = {result.river_head:g} m",
        zorder=7,
    )

    ax.axhline(config.model_bottom, color="0.25", lw=1.0)

    min_view_km = min(max_distance_km, 0.5)
    if display_distance_km is None or not np.isfinite(display_distance_km):
        view_distance_km = max_distance_km
    else:
        view_distance_km = float(np.clip(display_distance_km, min_view_km, max_distance_km))
    ax.set_xlim(view_distance_km, 0.0)

    valid_heads = np.asarray(result.head, dtype=float)
    valid_heads = valid_heads[np.isfinite(valid_heads) & (valid_heads > -1.0e20)]
    highest_head = float(np.nanmax(wt_plot)) if np.isfinite(wt_plot).any() else config.model_bottom
    if valid_heads.size:
        highest_head = max(highest_head, float(np.nanmax(valid_heads)))
    if np.isfinite(dupuit_ymax):
        highest_head = max(highest_head, dupuit_ymax)
    highest_head = max(highest_head, float(g.z_edges[min(result.chd_layers)]))
    y_margin = max(3.0, 0.04 * max(1.0, highest_head - config.model_bottom))
    ax.set_ylim(config.model_bottom, highest_head + y_margin)

    ax.set_xlabel("Distance from CHD node (km; increasing to the left)")
    ax.set_ylabel("Elevation (m)")
    ax.set_title("Steady unconfined potentiometric cross section — MODFLOW-NWT")
    ax.grid(False)
    ax.legend(loc="best", frameon=False, fontsize=8.5)
    fig.tight_layout()
    return fig


# -----------------------------------------------------------------------------
# Streamlit state helpers
# -----------------------------------------------------------------------------
APP_STATE_VERSION = 24


def flow_signature(config: Config) -> tuple:
    """Parameters that require a new MODFLOW-NWT solution when changed."""
    return (
        float(config.recharge_mm_yr),
        float(config.river_level_above_bottom),
        float(config.chd_thickness_m),
        float(config.kx_m_s),
        float(config.kz_over_kx),
        float(config.model_length_m),
        float(config.model_bottom),
        float(config.model_top),
        float(config.target_dx),
        float(config.target_dz),
        float(config.width_y),
    )


def particle_signature(
    flow_sig: tuple,
    porosity: float,
    n_particles_left: int,
    n_particles_below: int,
    backend: str,
) -> tuple:
    """Parameters that require a new particle-tracking run when changed."""
    return (
        flow_sig,
        float(porosity),
        int(n_particles_left),
        int(n_particles_below),
        str(backend),
        "left_below_chd_neighbors_v2",
    )


def clear_particle_state() -> None:
    for key in (
        "mp_pathlines",
        "mp_signature",
    ):
        st.session_state.pop(key, None)


def clear_flow_state() -> None:
    st.session_state.pop("flow_result", None)
    st.session_state.pop("flow_signature", None)
    st.session_state.pop("flow_config", None)
    clear_particle_state()


# -----------------------------------------------------------------------------
# Streamlit application
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MODFLOW-NWT potentiometric cross section",
    layout="centered",
)

st.title("MODFLOW-NWT potentiometric cross section")

# Keep the conceptual figure relative to the app, as in the other teaching
# modules. Replace the placeholder by the final source figure without changing
# the Python code.
INTRO_FIGURE = APP_DIR / "FIGS" / "cherry_cohen.png"

st.markdown(
    """
This interactive model illustrates **groundwater flow in an unconfined aquifer**
and the development of horizontal and vertical flow components within a groundwater
catchment bounded by a no-flow boundary on the left and a specified-head discharge
boundary on the right.

The model allows investigation of the influence of:

- **horizontal hydraulic conductivity (Kx) and anisotropy (Kz/Kx)**
- **groundwater recharge**
- **the geometry of the discharge boundary**
- **numerical discretization and particle-tracking settings**

The steady-state flow field is computed with **MODFLOW-NWT**, with optional
particle tracking. The model represents a **10 km cross section** and illustrates
how a 2-D section can reveal the three-dimensional character of groundwater flow.
"""
)

if INTRO_FIGURE.exists():
    st.image(
        str(INTRO_FIGURE),
        caption=(
            "Conceptual potentiometric cross section used as motivation for "
            "the numerical experiment. From [Cherry and Cohen, 2020](https://books.gw-project.org/conceptual-and-visual-understanding-of-hydraulic-head-and-groundwater-flow/)"
        ),
        use_container_width=True,
    )
else:
    st.info(
        "**Figure placeholder:** place the conceptual Freeze/Cohen source "
        "figure at `FIGS/potentiometric_cross_section_concept.png`."
    )

WT_METHOD_MAP = {
    "Linear through computed heads": "linear",
    "PCHIP through computed heads": "pchip",
    "Local quadratic + PCHIP (recommended)": "smooth_pchip",
    "Zero-pressure extrapolation + PCHIP": "zero_pressure_pchip",
}
DEFAULT_WT_LABEL = "Local quadratic + PCHIP (recommended)"

PRESET_A = "Preset A"
PRESET_B = "Preset B"
INDIVIDUAL = "Individual setting"
PRESET_UI_STATE_VERSION = 7

# Discrete anisotropy values used in both preset and individual modes. Keeping
# one shared ordered list avoids slightly different controls in different UI
# branches and makes subsequent manual changes straightforward.
ANISOTROPY_VALUES = (
    1.0e-5,
    5.0e-5,
    1.0e-4,
    5.0e-4,
    1.0e-3,
    5.0e-3,
    1.0e-2,
    5.0e-2,
    1.0e-1,
    5.0e-1,
    1.0,
    5.0,
    10.0,
)


def anisotropy_label(value: float) -> str:
    """Compact fixed-point labels for the discrete Kz/Kx choices."""
    value = float(value)
    if value >= 1.0:
        return f"{value:g}"
    if value >= 0.1:
        return f"{value:.1f}"
    if value >= 0.01:
        return f"{value:.2f}"
    if value >= 0.001:
        return f"{value:.3f}"
    return f"{value:.5f}"


def anisotropy_slider(label: str, *, key: str, default: float, help_text: str) -> float:
    """Render the common discrete Kz/Kx selector used throughout the app."""
    default = float(default)
    if key not in st.session_state or float(st.session_state[key]) not in ANISOTROPY_VALUES:
        st.session_state[key] = default
    return float(
        st.select_slider(
            label,
            options=ANISOTROPY_VALUES,
            key=key,
            format_func=anisotropy_label,
            help=help_text,
        )
    )


def _nearest_anisotropy_value(value: float) -> float:
    """Return the closest value from the shared discrete anisotropy sequence."""
    value = float(value)
    return float(min(ANISOTROPY_VALUES, key=lambda option: abs(float(option) - value)))


def _step_anisotropy_number(canonical_key: str, number_key: str, direction: int) -> None:
    """Move a preset number input by one entry in ``ANISOTROPY_VALUES``."""
    current = _nearest_anisotropy_value(st.session_state.get(canonical_key, 1.0))
    index = ANISOTROPY_VALUES.index(current)
    index = int(np.clip(index + int(direction), 0, len(ANISOTROPY_VALUES) - 1))
    new_value = float(ANISOTROPY_VALUES[index])
    st.session_state[canonical_key] = new_value
    st.session_state[number_key] = new_value


def _snap_anisotropy_number(canonical_key: str, number_key: str) -> None:
    """Snap a typed preset anisotropy value to the nearest teaching value."""
    new_value = _nearest_anisotropy_value(st.session_state[number_key])
    st.session_state[number_key] = new_value
    st.session_state[canonical_key] = new_value


def preset_anisotropy_input(
    label: str, *, key: str, default: float, help_text: str
) -> float:
    """Preset Kz/Kx control with slider or discrete-step numerical entry.

    The toggle and value control are placed side by side. In number-input mode,
    the dedicated minus/plus buttons move exactly one position through the same
    discrete teaching values used by the slider. Typed values are snapped to the
    nearest permitted value so both modes always represent the same parameter set.
    """
    default = _nearest_anisotropy_value(default)
    if key not in st.session_state:
        st.session_state[key] = default
    st.session_state[key] = _nearest_anisotropy_value(st.session_state[key])

    mode_key = f"{key}_number_mode"
    number_key = f"{key}_number_value"
    slider_key = f"{key}_slider_value"
    last_mode_key = f"_{key}_last_number_mode"

    mode_col, input_col = st.columns([0.34, 0.66])
    with mode_col:
        number_mode = st.toggle(
            "Use number input",
            value=False,
            key=mode_key,
            help=(
                "Switch between the discrete slider and numerical entry. In numerical "
                "mode, use the −/+ buttons to move through the same predefined Kz/Kx values."
            ),
        )

    previous_mode = st.session_state.get(last_mode_key)
    if previous_mode is None or bool(previous_mode) != bool(number_mode):
        current = float(st.session_state[key])
        st.session_state[number_key] = current
        st.session_state[slider_key] = current
    st.session_state[last_mode_key] = bool(number_mode)

    with input_col:
        if number_mode:
            st.caption(label)
            minus_col, number_col, plus_col = st.columns([0.16, 0.68, 0.16])
            with minus_col:
                st.button(
                    "−",
                    key=f"{key}_previous",
                    help="Previous discrete Kz/Kx value",
                    on_click=_step_anisotropy_number,
                    args=(key, number_key, -1),
                    use_container_width=True,
                )
            with number_col:
                st.number_input(
                    label,
                    min_value=float(ANISOTROPY_VALUES[0]),
                    max_value=float(ANISOTROPY_VALUES[-1]),
                    step=0.00001,
                    format="%.5f",
                    key=number_key,
                    on_change=_snap_anisotropy_number,
                    args=(key, number_key),
                    help=help_text,
                    label_visibility="collapsed",
                )
            with plus_col:
                st.button(
                    "+",
                    key=f"{key}_next",
                    help="Next discrete Kz/Kx value",
                    on_click=_step_anisotropy_number,
                    args=(key, number_key, 1),
                    use_container_width=True,
                )
            value = _nearest_anisotropy_value(st.session_state[number_key])
        else:
            value = float(
                st.select_slider(
                    label,
                    options=ANISOTROPY_VALUES,
                    key=slider_key,
                    format_func=anisotropy_label,
                    help=help_text,
                )
            )

    st.session_state[key] = float(value)
    return float(value)


# Presets lock the parameters that define the teaching comparison while leaving
# Kz/Kx interactive. Preset B additionally exposes the CHD thickness because
# changing the outlet penetration is part of that investigation.
PRESET_VALUES = {
    PRESET_A: {
        "recharge_mm_yr": 200.0,
        "river_level_above_bottom": 60.0,
        "chd_thickness_m": 1.0,
        "kx_m_s": 1.0e-4,
        "kz_over_kx": 5.0e-3,
        "model_top": 130.0,
        "model_bottom": 0.0,
        "target_dx": 100.0,
        "target_dz": 10.0,
        "contour_interval": 2,
        "display_distance_km": 5.0,
        "show_dupuit": False,
        "activate_modpath": True,
        "porosity": 0.25,
        "n_particles_left": 4,
        "n_particles_below": 4,
    },
    PRESET_B: {
        "recharge_mm_yr": 200.0,
        "river_level_above_bottom": 60.0,
        "chd_thickness_m": 65.0,
        "kx_m_s": 1.0e-3,
        "kz_over_kx": 1.0,
        "model_top": 130.0,
        "model_bottom": 0.0,
        "target_dx": 100.0,
        "target_dz": 10.0,
        "contour_interval": 2,
        "display_distance_km": 3.0,
        "show_dupuit": False,
        "activate_modpath": True,
        "porosity": 0.25,
        "n_particles_left": 7,
        "n_particles_below": 0,
    },
}

PRESET_PREFIX = {PRESET_A: "preset_a", PRESET_B: "preset_b"}


def preset_state_key(profile: str, name: str) -> str:
    """Stable profile-specific state key so A/B plot controls never interfere."""
    return f"{PRESET_PREFIX[profile]}_{name}"


def reset_preset_state(profile: str) -> None:
    """Restore the interactive values of one preset to its declared defaults.

    This is called only when a user *enters* Preset A or Preset B (and during a
    one-time UI-state migration). It deliberately does not run on ordinary
    widget reruns, so user changes made while staying in a preset are preserved.
    Both the canonical anisotropy value and its slider/number-input widget state
    are synchronized to avoid stale Streamlit widget values overriding the
    preset default.
    """
    defaults = PRESET_VALUES[profile]

    kz_key = preset_state_key(profile, "kz_over_kx")
    kz_default = float(defaults["kz_over_kx"])
    st.session_state[kz_key] = kz_default
    st.session_state[f"{kz_key}_slider_value"] = kz_default
    st.session_state[f"{kz_key}_number_value"] = kz_default

    contour_key = preset_state_key(profile, "plot_contour_interval")
    contour_widget_key = preset_state_key(profile, "plot_contour_interval_widget")
    st.session_state[contour_key] = int(defaults["contour_interval"])
    # The postprocessing control is created only after a model result exists.
    # Remove its widget state when entering a preset so its first render is
    # initialized explicitly from the canonical preset value rather than from
    # Streamlit's number-input minimum or a stale frontend widget value.
    st.session_state.pop(contour_widget_key, None)

    st.session_state[preset_state_key(profile, "post_display_distance_km")] = float(
        defaults["display_distance_km"]
    )
    st.session_state[preset_state_key(profile, "post_show_dupuit")] = bool(
        defaults["show_dupuit"]
    )

    if profile == PRESET_B:
        st.session_state[preset_state_key(PRESET_B, "chd_thickness_m")] = float(
            defaults["chd_thickness_m"]
        )


def on_settings_profile_change() -> None:
    """Apply a preset's initial values exactly when the user switches to it."""
    profile = st.session_state.get("settings_profile")
    if profile in PRESET_VALUES:
        reset_preset_state(profile)


def sync_preset_contour_widget(profile: str) -> None:
    """Copy the visible preset contour control into its persistent preset state."""
    contour_key = preset_state_key(profile, "plot_contour_interval")
    widget_key = preset_state_key(profile, "plot_contour_interval_widget")
    st.session_state[contour_key] = int(st.session_state[widget_key])


def sync_individual_contour_widget() -> None:
    """Copy the visible individual contour control into persistent plot state."""
    st.session_state["ind_plot_contour_interval"] = int(
        st.session_state["ind_plot_contour_interval_widget"]
    )


# Stateful expander styling. Each expander has a stable key and a callback
# that stores its open/closed state across app reruns.
# The keyed CSS classes are documented Streamlit behavior; the backgrounds are
# deliberately very subtle so they remain readable in light and dark themes.
st.markdown(
    """
<style>
.st-key-exp_boundary, .st-key-exp_boundary details { background-color: rgba(33, 150, 243, 0.035) !important; }
.st-key-exp_geometry, .st-key-exp_geometry details { background-color: rgba(76, 175, 80, 0.035) !important; }
.st-key-exp_particles, .st-key-exp_particles details { background-color: rgba(255, 152, 0, 0.035) !important; }
.st-key-exp_preview, .st-key-exp_preview details { background-color: rgba(156, 39, 176, 0.030) !important; }
.st-key-exp_postprocessing, .st-key-exp_postprocessing details { background-color: rgba(0, 150, 136, 0.035) !important; }
.st-key-exp_details, .st-key-exp_details details { background-color: rgba(96, 125, 139, 0.035) !important; }
.st-key-setup_profile_box { background-color: rgba(100, 116, 139, 0.025) !important; }
.st-key-preset_plot_controls { background-color: rgba(0, 150, 136, 0.020) !important; }
</style>
    """,
    unsafe_allow_html=True,
)


def tracked_expander(title: str, *, key: str, color: str):
    """Return a collapsed-by-default expander with persistent open/closed state.

    Streamlit removes widget state when a conditional widget disappears for a
    rerun. A separate non-widget backup therefore stores each expander state.
    This is particularly important for the result-only postprocessing expander,
    which temporarily disappears when a changed flow setup invalidates a result.
    """
    backup_key = f"_{key}__open_backup"
    if backup_key not in st.session_state:
        st.session_state[backup_key] = False
    if key not in st.session_state:
        st.session_state[key] = bool(st.session_state[backup_key])

    def _remember_state():
        st.session_state[backup_key] = bool(st.session_state[key])

    label = f":{color}[**{title}** (Click to open/close)]"
    return st.expander(
        label,
        expanded=False,
        key=key,
        on_change=_remember_state,
    )


# -------------------------------------------------------------------------
# Setup mode / presets
# -------------------------------------------------------------------------
# The app now starts in Individual setting. Each preset owns its own widget
# state so that changing A/B plot controls (for example a 1 m contour interval)
# remains active consistently through reruns and does not leak into the other
# preset.
if st.session_state.get("_preset_ui_state_version") != PRESET_UI_STATE_VERSION:
    st.session_state["settings_profile"] = INDIVIDUAL
    for profile in PRESET_VALUES:
        reset_preset_state(profile)
    st.session_state.setdefault("ind_kz_over_kx", 0.1)
    # One-time UI migration: Individual mode starts with a 5 m contour interval.
    # Subsequent parameter changes keep the user's current value because this
    # block only runs when the UI-state version changes.
    st.session_state["ind_plot_contour_interval"] = 5
    # The individual postprocessing widget is created only after a result exists.
    # Clear any stale frontend/widget value (notably the number-input minimum 1)
    # so the first visible render is initialized from the canonical 5 m value.
    st.session_state.pop("ind_plot_contour_interval_widget", None)
    st.session_state["_preset_ui_state_version"] = PRESET_UI_STATE_VERSION

# Ensure all profile-specific keys exist also in sessions created with a newer
# app version but partially cleared widget state.
for _profile, _preset_defaults in PRESET_VALUES.items():
    st.session_state.setdefault(
        preset_state_key(_profile, "kz_over_kx"), float(_preset_defaults["kz_over_kx"])
    )
    st.session_state.setdefault(
        preset_state_key(_profile, "plot_contour_interval"),
        int(_preset_defaults["contour_interval"]),
    )
    st.session_state.setdefault(
        preset_state_key(_profile, "post_display_distance_km"),
        float(_preset_defaults["display_distance_km"]),
    )
    st.session_state.setdefault(
        preset_state_key(_profile, "post_show_dupuit"), bool(_preset_defaults["show_dupuit"])
    )
st.session_state.setdefault(
    preset_state_key(PRESET_B, "chd_thickness_m"),
    float(PRESET_VALUES[PRESET_B]["chd_thickness_m"]),
)

with st.container(border=True, key="setup_profile_box"):
    st.markdown("""
        #### Model setup mode
         - **Preset A** focuses on the conceptual 2-D flow pattern illustrated above with a shallow localized CHD.
         - **Preset B** provides a more Dupuit-like case with predominantly horizontal regional flow and an adjustable CHD penetration.
         - **Individual setting** exposes the complete set of hydraulic, boundary, grid, particle-tracking, and postprocessing controls for custom investigations.
        """
    )
    
    settings_profile = st.radio(
        "Choose how much of the model setup you want to control",
        options=[PRESET_A, PRESET_B, INDIVIDUAL],
        horizontal=True,
        key="settings_profile",
        on_change=on_settings_profile_change,
    )

    using_preset = settings_profile in PRESET_VALUES
    if using_preset:
        preset = PRESET_VALUES[settings_profile]
        if settings_profile == PRESET_A:
            st.caption(
                "Preset A: Kx = 1×10⁻⁴ m/s, recharge = 200 mm/year, dx = 100 m, "
                "dz = 10 m, and a one-layer CHD. The initial Kz/Kx ratio is 0.005. "
                "Plot defaults are 2 m contours and a 5 km view. Backward particle "
                "tracking is active with 4 particles left of and 4 below the CHD."
            )
        else:
            st.caption(
                "Preset B: Kx = 1×10⁻³ m/s, recharge = 200 mm/year, dx = 100 m, "
                "dz = 10 m, and an initially fully penetrating 65 m CHD. Kz/Kx starts at "
                "1 and the Dupuit reference is shown initially. Seven left-side particles "
                "provide at least one release per CHD layer. Below-CHD particles are used "
                "whenever the CHD does not reach the lowest model layer."
            )

        kz_over_kx = preset_anisotropy_input(
            "Vertical anisotropy Kz/Kx (-)",
            key=preset_state_key(settings_profile, "kz_over_kx"),
            default=float(preset["kz_over_kx"]),
            help_text=(
                "Discrete teaching values for Kz/Kx. Kz = Kx × (Kz/Kx); values "
                "below 1 represent reduced vertical hydraulic conductivity."
            ),
        )

        if settings_profile == PRESET_B:
            st.number_input(
                "CHD area thickness (m)",
                min_value=1.0,
                max_value=70.0,
                step=1.0,
                key=preset_state_key(PRESET_B, "chd_thickness_m"),
                help=(
                    "Thickness measured downward from the head-defining CHD cell. "
                    "With the preset grid, 65 m reaches the model bottom after vertical "
                    "discretization; smaller values produce a partially penetrating CHD."
                ),
            )

        st.caption(
            f"Resulting vertical conductivity: **Kz = {preset['kx_m_s'] * kz_over_kx:.3g} m/s**"
        )

# -------------------------------------------------------------------------
# Model inputs
# -------------------------------------------------------------------------
if using_preset:
    recharge_mm_yr = float(preset["recharge_mm_yr"])
    river_level_above_bottom = float(preset["river_level_above_bottom"])
    chd_thickness_m = (
        float(st.session_state[preset_state_key(PRESET_B, "chd_thickness_m")])
        if settings_profile == PRESET_B
        else float(preset["chd_thickness_m"])
    )
    kx_m_s = float(preset["kx_m_s"])
    model_top = float(preset["model_top"])
    model_bottom = float(preset["model_bottom"])
    target_dx = float(preset["target_dx"])
    target_dz = float(preset["target_dz"])
    activate_modpath = bool(preset.get("activate_modpath", False))
    porosity = float(preset.get("porosity", 0.25))
    n_particles_left = int(preset.get("n_particles_left", 4))
    n_particles_below = int(preset.get("n_particles_below", 0))
else:
    with tracked_expander(
        "1. Boundary conditions and hydraulic properties",
        key="exp_boundary",
        color="blue",
    ):
        boundary_col, hydraulic_col = st.columns(2)

        with boundary_col:
            st.markdown("**Boundary conditions**")
            recharge_mm_yr = st.number_input(
                "Recharge (mm/year)",
                min_value=0.0,
                max_value=2000.0,
                value=200.0,
                step=10.0,
                help="Uniform recharge applied to the upper model layer.",
            )
            river_level_above_bottom = st.number_input(
                "River reference elevation above model bottom (m)",
                min_value=1.0,
                value=60.0,
                step=1.0,
                help=(
                    "The specified head is placed at the centre of the vertical cell "
                    "containing this reference elevation."
                ),
            )
            chd_thickness_m = st.number_input(
                "CHD area thickness (m)",
                min_value=1.0,
                max_value=60.0,
                value=10.0,
                step=1.0,
                help=(
                    "Nominal vertical thickness of the specified-head area, starting "
                    "with the head-defining outlet cell and extending downward. The "
                    "finite-difference representation uses the minimum whole number "
                    "of layers that reaches this thickness."
                ),
            )

        with hydraulic_col:
            st.markdown("**Hydraulic properties**")
            hydraulic_number_mode = st.toggle(
                "Use number input for Kx instead of logarithmic slider",
                value=False,
                key="hydraulic_number_mode",
                help=(
                    "Switch only the Kx control between a logarithmic slider and "
                    "direct numerical entry without changing its value. Kz/Kx uses "
                    "the discrete teaching-value slider below."
                ),
            )
            kx_m_s = parameter_input(
                "Horizontal hydraulic conductivity Kx (m/s)",
                key="kx_m_s",
                min_value=1.0e-5,
                max_value=1.0e-1,
                default=1.0e-4,
                number_mode=hydraulic_number_mode,
                scale="log",
                number_format="%.2e",
            )

            kz_over_kx = anisotropy_slider(
                "Vertical anisotropy Kz/Kx (-)",
                key="ind_kz_over_kx",
                default=0.1,
                help_text=(
                    "Discrete teaching values for the ratio of vertical to horizontal "
                    "hydraulic conductivity. Kz = Kx × (Kz/Kx)."
                ),
            )
            st.caption(
                f"Resulting vertical conductivity: **Kz = {kx_m_s * kz_over_kx:.3g} m/s**"
            )

    with tracked_expander(
        "2. Geometry and model grid",
        key="exp_geometry",
        color="green",
    ):
        geometry_col, grid_col = st.columns(2)

        with geometry_col:
            st.markdown("**Geometry**")
            model_top = st.number_input(
                "Model top elevation (m)",
                value=130.0,
                step=1.0,
            )
            model_bottom = st.number_input(
                "Model bottom elevation (m)",
                value=0.0,
                step=10.0,
            )
            st.caption("Fixed horizontal model length: **10.00 km**.")

        with grid_col:
            st.markdown("**Numerical discretization**")
            target_dx = st.number_input(
                "Horizontal cell size dx (m)",
                min_value=10.0,
                max_value=1000.0,
                value=100.0,
                step=10.0,
            )
            target_dz = st.number_input(
                "Vertical cell size dz (m)",
                min_value=1.0,
                max_value=100.0,
                value=10.0,
                step=1.0,
            )
            suggested_dz = max(1.0, float(target_dx) * min(1.0, float(kz_over_kx)))
            st.caption(
                f"Suggested dz for the current dx and anisotropy: **{suggested_dz:.1f} m**  \n"
                "Guidance: dz ≈ dx · min(1, Kz/Kx), with a 1 m lower limit. "
                "This is a discretization heuristic, not a physical requirement."
            )

    # Particle tracking is intentionally controlled outside an expander.
    activate_modpath = st.toggle(
        "Activate backward particle tracking (MODPATH 6)",
        value=False,
        key="activate_modpath",
        help=(
            "Particles are released in the saturated cells immediately left of and "
            "below the CHD area."
        ),
    )

    if activate_modpath:
        with tracked_expander(
            "Particle-tracking settings",
            key="exp_particles",
            color="orange",
        ):
            p1, p2 = st.columns(2)
            with p1:
                n_particles_left = st.number_input(
                    "Particles left of CHD (vertical)",
                    min_value=0,
                    max_value=60,
                    value=int(st.session_state.get("mp_n_particles_left", 4)),
                    step=1,
                    key="mp_n_particles_left",
                    help=(
                        "Regular vertical distribution in the saturated neighboring "
                        "column immediately left of the CHD area."
                    ),
                )
            with p2:
                n_particles_below = st.number_input(
                    "Particles below CHD (horizontal)",
                    min_value=0,
                    max_value=60,
                    value=int(st.session_state.get("mp_n_particles_below", 4)),
                    step=1,
                    key="mp_n_particles_below",
                    help=(
                        "Regular horizontal distribution in the saturated cell "
                        "immediately below the lowest CHD cell."
                    ),
                )
            porosity = st.number_input(
                "Effective porosity (-)",
                min_value=0.01,
                max_value=0.80,
                value=float(st.session_state.get("mp_porosity_pre", 0.25)),
                step=0.01,
                key="mp_porosity_pre",
            )
            st.caption(
                "Changing porosity or either particle count invalidates only the "
                "MODPATH result. An existing MODFLOW-NWT solution is reused."
            )
    else:
        porosity = float(st.session_state.get("mp_porosity_pre", 0.25))
        n_particles_left = int(st.session_state.get("mp_n_particles_left", 4))
        n_particles_below = int(st.session_state.get("mp_n_particles_below", 4))

# Keep postprocessing state separate between preset and individual modes so
# switching modes does not overwrite the user's individual plotting choices.
if "ind_plot_contour_interval" not in st.session_state:
    st.session_state["ind_plot_contour_interval"] = int(
        st.session_state.get("plot_contour_interval", 5)
    )
if "ind_post_display_distance_km" not in st.session_state:
    st.session_state["ind_post_display_distance_km"] = float(
        st.session_state.get("post_display_distance_km", 10.0)
    )
if "ind_post_show_dupuit" not in st.session_state:
    st.session_state["ind_post_show_dupuit"] = bool(
        st.session_state.get("post_show_dupuit", False)
    )

if using_preset:
    contour_interval = int(
        st.session_state[preset_state_key(settings_profile, "plot_contour_interval")]
    )
    show_dupuit = bool(
        st.session_state[preset_state_key(settings_profile, "post_show_dupuit")]
    )
else:
    contour_interval = int(st.session_state.get("ind_plot_contour_interval", 5))
    show_dupuit = bool(st.session_state.get("ind_post_show_dupuit", False))

water_table_method = "smooth_pchip"
water_table_smoothing_m = float(
    st.session_state.get("post_wt_smoothing_length_m", 500.0)
)

config = Config(
    recharge_mm_yr=float(recharge_mm_yr),
    river_level_above_bottom=float(river_level_above_bottom),
    chd_thickness_m=float(chd_thickness_m),
    kx_m_s=float(kx_m_s),
    kz_over_kx=float(kz_over_kx),
    porosity=float(porosity),
    model_length_m=10_000.0,
    model_bottom=float(model_bottom),
    model_top=float(model_top),
    target_dx=float(target_dx),
    target_dz=float(target_dz),
    n_particles_left=int(n_particles_left),
    n_particles_below=int(n_particles_below),
    contour_interval=float(contour_interval),
    water_table_method=water_table_method,
    water_table_smoothing_m=float(water_table_smoothing_m),
    show_dupuit=bool(show_dupuit),
)

# -------------------------------------------------------------------------
# Pre-run validation and preview
# -------------------------------------------------------------------------

problems: list[str] = []
warnings: list[str] = []

if config.recharge_m_s <= 0.0:
    problems.append("Recharge must be greater than zero.")
if config.kx_m_s <= 0.0:
    problems.append("Horizontal hydraulic conductivity must be greater than zero.")
if config.river_level_above_bottom <= 0.0:
    problems.append("River elevation above the model bottom must be greater than zero.")
if config.model_top <= config.river_reference_elevation:
    problems.append("Model top must be above the river reference elevation.")
if config.model_top <= config.model_bottom:
    problems.append("Model top must be above the model bottom.")
if config.chd_thickness_m <= 0.0:
    problems.append("CHD thickness must be greater than zero.")
if config.model_length_m <= 0.0:
    problems.append("Model length must be greater than zero.")

preview_geometry = None
preview_chd_layers: tuple[int, ...] = ()
if not problems:
    try:
        preview_geometry = make_geometry(config)
        preview_river_layer = river_layer_from_geometry(
            preview_geometry, config.river_reference_elevation
        )
        preview_chd_layers = chd_layers_from_thickness(
            preview_geometry, preview_river_layer, config.chd_thickness_m
        )
        chd_reaches_bottom = max(preview_chd_layers) == preview_geometry.nlay - 1

        # A fully penetrating CHD has no model cell below it. In that case any
        # requested below-CHD releases are suppressed rather than passed to
        # MODPATH, while left-side releases remain available.
        if activate_modpath and chd_reaches_bottom and int(n_particles_below) > 0:
            n_particles_below = 0
            config = replace(config, n_particles_below=0)
            warnings.append(
                "The CHD reaches the model bottom, so particles below the CHD "
                "are disabled for this setup."
            )

        if activate_modpath and int(n_particles_left) + int(n_particles_below) < 1:
            problems.append(
                "Activate at least one backward particle left of the CHD; no "
                "below-CHD release cell is available when the CHD reaches the bottom."
                if chd_reaches_bottom
                else "Activate at least one backward particle left of or below the CHD."
            )

        if preview_geometry.dx > 200.0:
            warnings.append(
                "The horizontal grid is coarse relative to the localized outlet. "
                "The default/reference discretization uses dx = 100 m."
            )
    except Exception as exc:
        problems.append(f"The model geometry could not be constructed: {exc}")

if problems:
    for problem in problems:
        st.error(problem)
else:
    st.markdown(
        "**Boundary representation:** the right edge contains a vertically "
        "discretized specified-head area extending downward from the head-defining "
        "outlet cell. The left side and model bottom are no-flow boundaries; "
        "recharge is applied to the top model layer."
    )
    for warning in warnings:
        st.warning(warning)

    with tracked_expander(
        "Preview model before run",
        key="exp_preview",
        color="violet",
    ):
        st.caption(
            "The preview is available in all setup modes and shows the numerical "
            "grid and boundary conditions only. Recharge and the initial head are "
            "intentionally omitted."
        )
        try:
            preview_fig, preview_geometry = plot_model_preview(config)
            st.pyplot(preview_fig, clear_figure=True, use_container_width=True)
            plt.close(preview_fig)

            vertical_thicknesses = np.diff(preview_geometry.z_edges) * -1.0
            dz_text = f"{config.target_dz:g} m"
            if not np.allclose(vertical_thicknesses, config.target_dz):
                dz_text += " (bottom layer adjusted)"
            st.markdown(
                f"**Fixed model length:** {config.model_length_m / 1000.0:.2f} km  \n"
                f"**CHD head (node/cell centre):** "
                f"{river_cell_head(preview_geometry, preview_river_layer):.2f} m  \n"
                f"**Requested / discretized CHD thickness:** {config.chd_thickness_m:.1f} / "
                f"{chd_actual_thickness(preview_geometry, preview_chd_layers):.1f} m  \n"
                f"**Horizontal grid:** {preview_geometry.ncol} columns, "
                f"dx = {preview_geometry.dx:.1f} m  \n"
                f"**Vertical grid:** {preview_geometry.nlay} layers, dz = {dz_text}"
            )
        except Exception as exc:
            st.warning(f"Model preview could not be constructed: {exc}")

# -------------------------------------------------------------------------
# Execution state and run action
# -------------------------------------------------------------------------
if st.session_state.get("_app_state_version") != APP_STATE_VERSION:
    clear_flow_state()
    st.session_state["_app_state_version"] = APP_STATE_VERSION

current_flow_sig = flow_signature(config)
if (
    "flow_signature" in st.session_state
    and st.session_state["flow_signature"] != current_flow_sig
):
    clear_flow_state()

current_mp_sig = particle_signature(
    current_flow_sig,
    float(porosity),
    int(n_particles_left),
    int(n_particles_below),
    "MODPATH 6",
)
if (
    "mp_signature" in st.session_state
    and st.session_state["mp_signature"] != current_mp_sig
):
    clear_particle_state()

flow_current_for_button = (
    st.session_state.get("flow_result") is not None
    and st.session_state.get("flow_signature") == current_flow_sig
)
mp_current_for_button = (
    activate_modpath
    and st.session_state.get("mp_signature") == current_mp_sig
    and st.session_state.get("mp_pathlines") is not None
)
run_button_label = (
    "▶ Update particle tracking"
    if flow_current_for_button and activate_modpath and not mp_current_for_button
    else "▶ Run model"
)

run_clicked = st.button(run_button_label, type="primary", disabled=bool(problems))
status = st.empty()

root_ws = Path(tempfile.gettempdir()) / "mf_nwt_cross_section_workspace"
root_ws.mkdir(parents=True, exist_ok=True)

if run_clicked:
    result_now = st.session_state.get("flow_result")
    flow_is_current = (
        result_now is not None
        and st.session_state.get("flow_signature") == current_flow_sig
    )

    if not flow_is_current:
        mfnwt_exe = find_mfnwt_executable()
        if mfnwt_exe is None:
            st.error(
                "MODFLOW-NWT was not found. For Streamlit Cloud, place the Linux "
                "executable at `bin/mfnwt` in the repository. Local installations "
                "may also provide MODFLOW-NWT through PATH or `MFNWT_EXE`."
            )
            st.stop()

        run_id = uuid.uuid4().hex[:10]
        flow_workspace = root_ws / f"flow_{run_id}"
        try:
            status.info("Building and running MODFLOW-NWT...")
            with st.spinner("MODFLOW-NWT simulation"):
                result_now = run_flow_model(
                    config, flow_workspace, mfnwt_exe, modelname="xsec_nwt"
                )
            st.session_state["flow_result"] = result_now
            st.session_state["flow_signature"] = current_flow_sig
            st.session_state["flow_config"] = config
            clear_particle_state()
        except Exception as exc:
            status.error("❌ MODFLOW-NWT simulation failed.")
            st.error(str(exc))
            st.stop()
    else:
        status.info("Using the existing MODFLOW-NWT flow solution...")

    if activate_modpath:
        mp_exe = find_mp6_executable()
        if mp_exe is None:
            status.warning("MODFLOW-NWT finished, but MODPATH 6 was not found.")
            st.error(
                "For Streamlit Cloud, place the Linux executable at `bin/mp6` in "
                "the repository. Local installations may also provide MODPATH 6 "
                "through PATH or `MP6_EXE`."
            )
            clear_particle_state()
        else:
            mp_config = replace(
                st.session_state["flow_config"],
                porosity=float(porosity),
                n_particles_left=int(n_particles_left),
                n_particles_below=int(n_particles_below),
            )
            try:
                status.info("Running backward MODPATH 6 tracking...")
                with st.spinner("MODPATH 6 backward tracking"):
                    pathlines = run_modpath6_from_existing_flow(
                        st.session_state["flow_result"], mp_config, mp_exe
                    )
                st.session_state["mp_pathlines"] = pathlines
                st.session_state["mp_signature"] = current_mp_sig
                status.success(
                    "✅ MODFLOW-NWT and backward MODPATH 6 finished successfully."
                )
            except Exception as exc:
                clear_particle_state()
                status.warning("MODFLOW-NWT finished, but particle tracking failed.")
                st.error(str(exc))
    else:
        clear_particle_state()
        status.success("✅ MODFLOW-NWT simulation finished.")

result = st.session_state.get("flow_result")
flow_config = st.session_state.get("flow_config")

if result is None or flow_config is None:
    st.info(
        "Review the model setup above if desired, then click **Run model**. "
        "If particle tracking is activated, MODPATH 6 runs automatically after "
        "MODFLOW-NWT."
    )
    st.stop()

# -------------------------------------------------------------------------
# Result-only postprocessing controls
# -------------------------------------------------------------------------
max_display_km = float(flow_config.model_length_m) / 1000.0
min_display_km = min(max_display_km, 0.5)

if using_preset:
    view_key = preset_state_key(settings_profile, "post_display_distance_km")
    contour_key = preset_state_key(settings_profile, "plot_contour_interval")
    dupuit_key = preset_state_key(settings_profile, "post_show_dupuit")
    preset_plot_defaults = PRESET_VALUES[settings_profile]
    st.session_state.setdefault(view_key, float(preset_plot_defaults["display_distance_km"]))
    st.session_state.setdefault(contour_key, int(preset_plot_defaults["contour_interval"]))
    st.session_state.setdefault(dupuit_key, bool(preset_plot_defaults["show_dupuit"]))
else:
    view_key = "ind_post_display_distance_km"
    contour_key = "ind_plot_contour_interval"
    dupuit_key = "ind_post_show_dupuit"
    st.session_state.setdefault(view_key, max_display_km)
    st.session_state.setdefault(contour_key, 5)
    st.session_state.setdefault(dupuit_key, False)

clipped = float(np.clip(st.session_state[view_key], min_display_km, max_display_km))
st.session_state[view_key] = round(clipped / 0.5) * 0.5

if using_preset:
    with st.container(border=True, key="preset_plot_controls"):
        st.markdown("#### Plot controls")
        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            contour_widget_key = preset_state_key(
                settings_profile, "plot_contour_interval_widget"
            )
            contour_interval = st.number_input(
                "Head-contour interval (m)",
                min_value=1,
                max_value=50,
                value=int(st.session_state[contour_key]),
                step=1,
                key=contour_widget_key,
                on_change=sync_preset_contour_widget,
                args=(settings_profile,),
                help="Plotting only; this does not rerun MODFLOW.",
            )
            # Keep plotting and the persistent preset state on the same value in
            # the current rerun as well as after the widget callback.
            st.session_state[contour_key] = int(contour_interval)
        with pc2:
            st.slider(
                "Displayed distance from CHD node (km)",
                min_value=float(min_display_km),
                max_value=float(max_display_km),
                step=0.5,
                key=view_key,
                help=(
                    "Postprocessing only. Distance zero is the centre of the CHD "
                    "column; the centre of the first model column is 10 km upstream."
                ),
            )
        with pc3:
            show_dupuit = st.toggle(
                "Show Dupuit analytical reference",
                key=dupuit_key,
                help=(
                    "Postprocessing only. The Dupuit curve uses Kx and uniform "
                    "recharge and ignores vertical gradients/anisotropy."
                ),
            )
    water_table_method = "smooth_pchip"
    water_table_smoothing_m = float(
        st.session_state.get("post_wt_smoothing_length_m", 500.0)
    )
else:
    with tracked_expander(
        "Postprocessing",
        key="exp_postprocessing",
        color="red",
    ):
        pp1, pp2 = st.columns(2)
        with pp1:
            contour_widget_key = "ind_plot_contour_interval_widget"
            contour_interval = st.number_input(
                "Head-contour interval (m)",
                min_value=1,
                max_value=50,
                value=int(st.session_state[contour_key]),
                step=1,
                key=contour_widget_key,
                on_change=sync_individual_contour_widget,
                help="Plotting only; this does not rerun MODFLOW or MODPATH.",
            )
            # Mirror the preset implementation: the canonical plotting value and
            # the visible widget value stay identical from the very first render.
            st.session_state[contour_key] = int(contour_interval)
            show_dupuit = st.toggle(
                "Show Dupuit analytical reference",
                key=dupuit_key,
                help=(
                    "Postprocessing only. The Dupuit curve uses Kx and uniform "
                    "recharge and ignores vertical gradients/anisotropy."
                ),
            )

        with pp2:
            st.slider(
                "Displayed distance from CHD node (km)",
                min_value=float(min_display_km),
                max_value=float(max_display_km),
                step=0.5,
                key=view_key,
                help=(
                    "Postprocessing only. Distance zero is the centre of the CHD "
                    "column; the centre of the first model column is 10 km upstream. "
                    "Changing this value does not rerun MODFLOW or MODPATH."
                ),
            )

        advanced_post = st.toggle(
            "Advanced postprocessing settings",
            value=bool(st.session_state.get("post_advanced_settings", False)),
            key="post_advanced_settings",
            help=(
                "Show optional controls for the water-table interpolation and its "
                "display smoothing. These settings never modify the MODFLOW solution."
            ),
        )

        if advanced_post:
            prior_label = st.session_state.get("post_wt_method_label", DEFAULT_WT_LABEL)
            if prior_label not in WT_METHOD_MAP:
                prior_label = DEFAULT_WT_LABEL
            wt_method_label = st.selectbox(
                "Water-table interpolation",
                options=list(WT_METHOD_MAP.keys()),
                index=list(WT_METHOD_MAP.keys()).index(prior_label),
                key="post_wt_method_label",
                help=(
                    "Display-only interpolation of the numerical free surface. Raw "
                    "MODFLOW heads are unchanged."
                ),
            )
            water_table_method = WT_METHOD_MAP[wt_method_label]

            if water_table_method == "smooth_pchip":
                min_smooth = max(float(flow_config.target_dx), 50.0)
                max_smooth = max(
                    min_smooth,
                    min(3000.0, 0.35 * float(flow_config.model_length_m)),
                )
                water_table_smoothing_m = st.number_input(
                    "Water-table smoothing length (m)",
                    min_value=float(min_smooth),
                    max_value=float(max_smooth),
                    value=float(
                        np.clip(
                            st.session_state.get("post_wt_smoothing_length_m", 500.0),
                            min_smooth,
                            max_smooth,
                        )
                    ),
                    step=float(max(25.0, flow_config.target_dx)),
                    format="%.0f",
                    key="post_wt_smoothing_length_m",
                    help=(
                        "Display-only local quadratic bandwidth used before PCHIP "
                        "interpolation."
                    ),
                )
            else:
                water_table_smoothing_m = float(
                    st.session_state.get("post_wt_smoothing_length_m", 500.0)
                )
        else:
            water_table_method = "smooth_pchip"
            water_table_smoothing_m = float(
                st.session_state.get("post_wt_smoothing_length_m", 500.0)
            )


# Use the result-only settings for plotting without changing the numerical
# signatures used above.
display_distance_km = float(st.session_state[view_key])
plot_config = replace(
    flow_config,
    contour_interval=float(contour_interval),
    water_table_method=str(water_table_method),
    water_table_smoothing_m=float(water_table_smoothing_m),
    show_dupuit=bool(show_dupuit),
    porosity=float(porosity),
    n_particles_left=int(n_particles_left),
    n_particles_below=int(n_particles_below),
)

pathlines = None
if activate_modpath and st.session_state.get("mp_signature") == current_mp_sig:
    pathlines = st.session_state.get("mp_pathlines")

# -------------------------------------------------------------------------
# Result diagnostics and final figure
# -------------------------------------------------------------------------
left_wt = (
    float(result.water_table[0])
    if np.isfinite(result.water_table[0])
    else float("nan")
)
expected_recharge = (
    flow_config.recharge_m_s
    * flow_config.model_length_m
    * flow_config.width_y
)

if np.isfinite(result.budget_error_pct) and abs(result.budget_error_pct) > 0.05:
    st.warning(
        f"The package water-budget discrepancy is {result.budget_error_pct:.3g} %. "
        "Treat the head field cautiously and inspect the NWT output before interpretation."
    )

finite_sequence = result.water_table[:-1]
finite_sequence = finite_sequence[np.isfinite(finite_sequence)]
if finite_sequence.size > 1 and np.any(np.diff(finite_sequence) > 0.05):
    st.warning(
        "The raw uppermost-wet-cell heads contain local discretization-scale "
        "reversals toward the outlet. A finer dz or an advanced water-table "
        "reconstruction can reduce their visual influence; raw MODFLOW heads "
        "are unchanged."
    )

if (
    result.outlet_wet_cells_above > 0
    and np.isfinite(result.outlet_head_above)
    and result.outlet_head_above > result.river_head + 1.0e-4
):
    st.warning(
        f"The cell directly above the top CHD layer is wet "
        f"(head ≈ {result.outlet_head_above:.2f} m) and exceeds the specified "
        f"head ({result.river_head:.2f} m). This creates a downward hydraulic "
        "component into the CHD area."
    )

final_fig = plot_cross_section(
    result,
    plot_config,
    pathlines=pathlines,
    display_distance_km=display_distance_km,
)
st.pyplot(final_fig, clear_figure=True, use_container_width=True)
plt.close(final_fig)

if activate_modpath:
    if pathlines is not None:
        st.success("✅ Backward MODPATH 6 tracking terminated normally.")
    else:
        st.info(
            "Particle tracking is active. Click **Run model** to calculate/update "
            "the pathlines."
        )

# -------------------------------------------------------------------------
# Secondary information
# -------------------------------------------------------------------------
if not using_preset:
    with tracked_expander(
        "Numerical and model details",
        key="exp_details",
        color="gray",
    ):
        vertical_thicknesses = -np.diff(result.geometry.z_edges)
        wt_plot_cells = water_table_for_plot(result, plot_config)
        wt_raw_cells = np.asarray(result.water_table, dtype=float)
        wt_mask = np.isfinite(wt_plot_cells) & np.isfinite(wt_raw_cells)
        if wt_mask.size:
            wt_mask[-1] = False
        wt_plot_adjustment = (
            float(np.max(np.abs(wt_plot_cells[wt_mask] - wt_raw_cells[wt_mask])))
            if np.any(wt_mask)
            else float("nan")
        )
        interpolation_label = next(
            (
                label
                for label, code in WT_METHOD_MAP.items()
                if code == plot_config.water_table_method
            ),
            plot_config.water_table_method,
        )
        st.markdown(
            f"**Computed water table at the no-flow divide:** {left_wt:.2f} m  \n"
            f"**Fixed model length:** {flow_config.model_length_m / 1000.0:.2f} km  \n"
            f"**Node-centred maximum plotted distance:** {max_display_km:.3f} km  \n"
            f"**Recharge / specified-head outflow:** {result.recharge_in:.4g} / "
            f"{result.constant_head_out:.4g} m³/s  \n"
            f"**Water-budget discrepancy:** {result.budget_error_pct:.4g} %  \n"
            f"**Expected recharge over the 1 m-wide section:** "
            f"{expected_recharge:.4g} m³/s  \n"
            f"**Solver:** MODFLOW-NWT, {result.solver_profile}  \n"
            f"**FloPy:** {flopy.__version__}  \n"
            f"**Grid:** {result.geometry.nlay} layers × 1 row × "
            f"{result.geometry.ncol} columns; dx = {result.geometry.dx:.2f} m; "
            f"nominal dz = {flow_config.target_dz:g} m  \n"
            f"**Actual layer thickness range:** "
            f"{float(np.min(vertical_thicknesses)):.2f}–"
            f"{float(np.max(vertical_thicknesses)):.2f} m  \n"
            f"**Hydraulics:** Kx = {flow_config.kx_m_s:.1e} m/s; "
            f"Kz = {flow_config.kz_m_s:.1e} m/s; "
            f"Kz/Kx = {flow_config.kz_over_kx:g}  \n"
            f"**CHD head:** {result.river_head:g} m; requested / discretized "
            f"thickness = {flow_config.chd_thickness_m:g} / "
            f"{result.chd_actual_thickness_m:g} m; layers = "
            f"{', '.join(str(k + 1) for k in result.chd_layers)}  \n"
            f"**Water-table interpolation:** {interpolation_label}"
            + (
                f"; smoothing length = {plot_config.water_table_smoothing_m:.0f} m"
                if plot_config.water_table_method == "smooth_pchip"
                else ""
            )
            + f"; Dupuit shown = {'yes' if plot_config.show_dupuit else 'no'}  \n"
            f"**Maximum display adjustment relative to raw uppermost-wet-cell "
            f"heads:** {wt_plot_adjustment:.3f} m  \n"
            f"**Wet cells above top CHD layer:** {result.outlet_wet_cells_above}; "
            f"head directly above = {result.outlet_head_above:.3f} m  \n"
            f"**Particle tracking:** "
            f"{'backward MODPATH 6; left/below CHD neighbors' if activate_modpath else 'off'}; "
            f"particles left/below CHD = {int(n_particles_left)} / "
            f"{int(n_particles_below)}"
        )
