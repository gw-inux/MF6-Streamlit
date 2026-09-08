# nwt_transient_streamlit_cloud.py
#
# Educational MODFLOW-NWT model:
# - rectangular, one-layer unconfined aquifer
# - recharge over full domain
# - specified-head eastern boundary
# - optional pumping well
# - optional river
# - optional transient investigation:
#     stress period 1: steady state
#     stress period 2: 1 day transient
#     stress period 3: 7 days transient
#
# In transient mode, pumping starts at the beginning of the first transient
# period. Recharge, CHD, and (if active) river conditions remain unchanged.
#
# The app is designed for the MF6-Streamlit repository used for Streamlit
# Community Cloud. It expects a Linux MODFLOW-NWT executable at bin/mfnwt.

import os
import shutil
import stat
import tempfile
import threading
from pathlib import Path

import flopy
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


# -----------------------------------------------------------------------------
# Page
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MODFLOW-NWT steady/transient recharge model",
    layout="centered",
)

st.title("Steady and transient MODFLOW-NWT model")
st.markdown(
    """
    This educational model represents a rectangular **unconfined aquifer** with
    areal recharge and a specified-head boundary along the eastern edge.

    The model starts as a **steady-state investigation**. When the transient
    periods are activated, MODFLOW first computes the steady-state reference
    condition and then simulates **1 day + 7 days** of transient response.
    If a pumping well is active, pumping starts when the first transient period
    begins.
    """
)


# -----------------------------------------------------------------------------
# Streamlit Cloud / native executable helpers
# -----------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
BIN_DIR = APP_DIR / "bin"


@st.cache_resource
def native_run_semaphore() -> threading.BoundedSemaphore:
    """Limit simultaneous native solver processes on Streamlit Cloud."""
    return threading.BoundedSemaphore(value=2)


@st.cache_resource
def matplotlib_render_lock() -> threading.RLock:
    """Serialize Matplotlib rendering across Streamlit sessions."""
    return threading.RLock()


def show_matplotlib(fig) -> None:
    """Render and close a Matplotlib figure under a process-wide lock."""
    with matplotlib_render_lock():
        st.pyplot(fig, clear_figure=True, width="stretch")
    plt.close(fig)


def ensure_executable_permissions(path: Path) -> Path:
    """Make a repository-shipped executable runnable on Linux/macOS."""
    path = path.resolve()
    if os.name != "nt":
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return path


def locate_mfnwt() -> Path:
    """
    Locate MODFLOW-NWT.

    Streamlit Cloud:
        bin/mfnwt

    Local alternatives:
        MFNWT_EXECUTABLE environment variable
        mfnwt / mfnwtdbl available on PATH
        common Windows executable names in bin/
    """
    candidates = []

    env_path = os.environ.get("MFNWT_EXECUTABLE")
    if env_path:
        candidates.append(Path(env_path).expanduser())

    candidates.extend(
        [
            BIN_DIR / "mfnwt",
            BIN_DIR / "mfnwtdbl",
            BIN_DIR / "mfnwt.exe",
            BIN_DIR / "mfnwtdbl.exe",
            BIN_DIR / "MODFLOW-NWT_64.exe",
        ]
    )

    for program in ("mfnwt", "mfnwtdbl", "MODFLOW-NWT_64.exe"):
        resolved = shutil.which(program)
        if resolved:
            candidates.append(Path(resolved))

    checked = []
    for candidate in candidates:
        try:
            candidate = candidate.resolve()
        except OSError:
            continue

        if candidate in checked:
            continue
        checked.append(candidate)

        if candidate.exists() and candidate.is_file():
            return ensure_executable_permissions(candidate)

    checked_text = "\n".join(f"- {p}" for p in checked) or "- no candidate paths"
    raise FileNotFoundError(
        "MODFLOW-NWT executable not found. For Streamlit deployment place the "
        "Linux executable at 'bin/mfnwt'. For local development set "
        "MFNWT_EXECUTABLE or put mfnwt on PATH.\n\n"
        f"Checked:\n{checked_text}"
    )


def cleanup_workspace(path) -> None:
    """Remove a previous temporary workspace without affecting other sessions."""
    if not path:
        return
    try:
        shutil.rmtree(Path(path), ignore_errors=True)
    except Exception:
        pass


# -----------------------------------------------------------------------------
# Pure model-configuration helpers
# -----------------------------------------------------------------------------
def build_time_configuration(transient_active: bool) -> dict:
    """
    Return the MODFLOW time discretization.

    The nominal 1-day length assigned to the steady-state period is only
    bookkeeping. For transient postprocessing, the end of the steady-state
    period is treated as elapsed time 0.

    Transient time-step density:
      - first transient day: 24 steps (1 h)
      - following 7 days:   56 steps (3 h)
    """
    if transient_active:
        return {
            "nper": 3,
            "perlen": [1.0, 1.0, 7.0],
            "nstp": [1, 24, 56],
            "tsmult": [1.0, 1.0, 1.0],
            "steady": [True, False, False],
            "steady_offset": 1.0,
            "transient_duration": 8.0,
        }

    return {
        "nper": 1,
        "perlen": [1.0],
        "nstp": [1],
        "tsmult": [1.0],
        "steady": [True],
        "steady_offset": 0.0,
        "transient_duration": 0.0,
    }


def build_output_control(nstp) -> dict:
    """Save/print head and budget for every model time step."""
    oc_spd = {}
    for kper, nsteps in enumerate(nstp):
        for kstp in range(int(nsteps)):
            oc_spd[(kper, kstp)] = [
                "save head",
                "save budget",
                "print budget",
            ]
    return oc_spd


def build_well_stress_period_data(
    active_wel: bool,
    transient_active: bool,
    well_row: int,
    well_col: int,
    well_rate: float,
):
    """
    Build WEL stress-period data.

    Steady-only mode:
        pumping is active in the steady-state model, matching the original app.

    Transient mode:
        stress period 0 -> zero pumping (steady-state reference)
        stress period 1 -> pumping starts
        stress period 2 -> pumping continues
    """
    if not active_wel:
        return None

    cell = [0, int(well_row) - 1, int(well_col) - 1]

    if transient_active:
        return {
            0: [[*cell, 0.0]],
            1: [[*cell, float(well_rate)]],
            2: [[*cell, float(well_rate)]],
        }

    return {0: [[*cell, float(well_rate)]]}


def elapsed_time_from_totim(times, transient_active: bool, steady_offset: float):
    """Convert MODFLOW total time to educational elapsed transient time."""
    times = np.asarray(times, dtype=float)
    if transient_active:
        return times - float(steady_offset)
    return times.copy()


# -----------------------------------------------------------------------------
# Boundary / plotting helpers retained from the steady-state NWT app
# -----------------------------------------------------------------------------
def make_package_registry(
    active_wel=False,
    active_riv=False,
    include_storage=False,
):
    """
    Registry for MODFLOW listing-file budget terms.

    Names match MODFLOW-NWT listing-file column names used by FloPy's
    MfListBudget parser.
    """
    packages = [
        {
            "key": "Recharge",
            "label": "Recharge",
            "budget_in": "RECHARGE_IN",
            "budget_out": "RECHARGE_OUT",
        },
        {
            "key": "CHD",
            "label": "CHD",
            "budget_in": "CONSTANT_HEAD_IN",
            "budget_out": "CONSTANT_HEAD_OUT",
        },
    ]

    if active_wel:
        packages.append(
            {
                "key": "WEL",
                "label": "WEL",
                "budget_in": "WELLS_IN",
                "budget_out": "WELLS_OUT",
            }
        )

    if active_riv:
        packages.append(
            {
                "key": "RIV",
                "label": "RIV",
                "budget_in": "RIVER_LEAKAGE_IN",
                "budget_out": "RIVER_LEAKAGE_OUT",
            }
        )

    if include_storage:
        packages.append(
            {
                "key": "Storage",
                "label": "Storage",
                "budget_in": "STORAGE_IN",
                "budget_out": "STORAGE_OUT",
            }
        )

    return packages


def make_boundary_features(
    nrow,
    ncol,
    active_wel=False,
    well_row=None,
    well_col=None,
    active_riv=False,
    riv_cells=None,
):
    """Registry for preview/result maps using user-facing 1-based cells."""
    features = []

    features.append(
        {
            "key": "CHD",
            "label": "Specified head",
            "cells": [(row, ncol) for row in range(1, nrow + 1)],
            "marker": "s",
            "markersize": 5,
            "edgecolor": "red",
            "facecolor": "none",
        }
    )

    if active_wel:
        features.append(
            {
                "key": "WEL",
                "label": "Pumping well",
                "cells": [(well_row, well_col)],
                "marker": "o",
                "markersize": 7,
                "edgecolor": "black",
                "facecolor": "none",
            }
        )

    if active_riv:
        features.append(
            {
                "key": "RIV",
                "label": "River",
                "cells": riv_cells,
                "marker": "^",
                "markersize": 6,
                "edgecolor": "blue",
                "facecolor": "none",
            }
        )

    return features


def plot_boundary_features(ax, features, nrow, delr, delc):
    """Plot registered boundary features."""
    plotted_labels = set()

    for feature in features:
        for row, col in feature["cells"]:
            x = (col - 0.5) * delr
            y = (nrow - row + 0.5) * delc

            label = feature["label"] if feature["label"] not in plotted_labels else None
            plotted_labels.add(feature["label"])

            ax.plot(
                x,
                y,
                marker=feature["marker"],
                markersize=feature["markersize"],
                markerfacecolor=feature["facecolor"],
                markeredgecolor=feature["edgecolor"],
                linestyle="None",
                label=label,
            )


def plot_observation_point(ax, obs_row, obs_col, nrow, delr, delc):
    """Plot the observation cell using a visible open-square/cross symbol."""
    x = (obs_col - 0.5) * delr
    y = (nrow - obs_row + 0.5) * delc

    ax.plot(
        x,
        y,
        marker="s",
        markersize=10,
        markerfacecolor="none",
        markeredgecolor="darkgreen",
        linestyle="None",
        label="Observation point",
    )
    ax.plot(
        x,
        y,
        marker="x",
        markersize=6,
        color="darkgreen",
        linestyle="None",
    )


def plot_model_grid(ax, nrow, ncol, delr, delc):
    """Plot the structured model grid."""
    lx = ncol * delr
    ly = nrow * delc

    for xg in np.arange(0, lx + delr, delr):
        ax.plot([xg, xg], [0, ly], color="silver", linewidth=0.5)

    for yg in np.arange(0, ly + delc, delc):
        ax.plot([0, lx], [yg, yg], color="silver", linewidth=0.5)


# -----------------------------------------------------------------------------
# Listing-file budget helpers
# -----------------------------------------------------------------------------
def read_listing_budget_dataframes(list_path):
    """
    Read incremental (rates) and cumulative (volumes) listing-file budgets.

    start_datetime=None is important: FloPy then indexes both dataframes by
    MODFLOW total simulation time rather than a DatetimeIndex.
    """
    lst = flopy.utils.MfListBudget(str(list_path))
    incremental, cumulative = lst.get_dataframes(start_datetime=None)
    return incremental.copy(), cumulative.copy()


def budget_snapshot_from_row(row, package_registry):
    """Return the same standardized steady-state budget dictionary as before."""
    budget = {}

    for pkg in package_registry:
        key = pkg["key"]
        budget[f"{key} IN"] = float(row.get(pkg["budget_in"], 0.0))
        budget[f"{key} OUT"] = float(row.get(pkg["budget_out"], 0.0))

    budget["TOTAL IN"] = float(row.get("TOTAL_IN", 0.0))
    budget["TOTAL OUT"] = float(row.get("TOTAL_OUT", 0.0))
    budget["Percent discrepancy"] = float(
        row.get("PERCENT_DISCREPANCY", np.nan)
    )

    return budget


def plot_budget_bar_chart(budget, package_registry):
    """Steady-state budget plot retained from the original NWT app."""
    labels = []
    values = []
    colors = []
    hatches = []

    for pkg in package_registry:
        key = pkg["key"]
        labels.append(f"{key} IN")
        values.append(budget[f"{key} IN"])
        colors.append("tab:blue")
        hatches.append("")

    for pkg in package_registry:
        key = pkg["key"]
        labels.append(f"{key} OUT")
        values.append(-budget[f"{key} OUT"])
        colors.append("tab:orange")
        hatches.append("")

    labels.extend(["Total IN", "Total OUT"])
    values.extend([budget["TOTAL IN"], -budget["TOTAL OUT"]])
    colors.extend(["tab:green", "tab:red"])
    hatches.extend(["//", "//"])

    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(labels, values, color=colors)

    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Flow rate [m³/d]", fontsize=12)
    ax.set_title("Complete water budget from MODFLOW listing file", fontsize=12)
    ax.tick_params(axis="x", rotation=90)

    for bar, value in zip(bars, values):
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()

        if value >= 0:
            ax.text(
                x,
                y * 1.01 if y != 0 else 0,
                f"{value:.0f}",
                ha="center",
                va="bottom",
                fontsize=10,
            )
        else:
            ax.text(
                x,
                y * 1.01,
                f"{value:.0f}",
                ha="center",
                va="top",
                fontsize=10,
            )

    fig.tight_layout()
    return fig


def budget_markdown(budget, package_registry):
    """Steady-state numerical budget summary retained from the original app."""
    lines = ["**Numerical budget summary from listing file**", ""]

    for pkg in package_registry:
        key = pkg["key"]
        label = pkg["label"]
        lines.append(f"- {label} IN: `{budget[f'{key} IN']:.4f} m³/d`")
        lines.append(f"- {label} OUT: `{budget[f'{key} OUT']:.4f} m³/d`")

    lines.append(f"- Total IN: `{budget['TOTAL IN']:.4f} m³/d`")
    lines.append(f"- Total OUT: `{budget['TOTAL OUT']:.4f} m³/d`")
    lines.append(
        f"- Percent discrepancy: `{budget['Percent discrepancy']:.4e} %`"
    )

    return "\n".join(lines)


def get_budget_time_axis(df, transient_active, steady_offset):
    """Return the listing-budget index as elapsed educational time [d]."""
    total_time = np.asarray(df.index, dtype=float)
    return elapsed_time_from_totim(
        total_time,
        transient_active=transient_active,
        steady_offset=steady_offset,
    )


def package_net_series(df, pkg):
    """
    Signed budget component:
      positive -> flow into groundwater model
      negative -> flow out of groundwater model
    """
    in_values = np.asarray(
        df.get(pkg["budget_in"], np.zeros(len(df))),
        dtype=float,
    )
    out_values = np.asarray(
        df.get(pkg["budget_out"], np.zeros(len(df))),
        dtype=float,
    )
    return in_values - out_values


def plot_transient_budget_rate(
    incremental_df,
    package_registry,
    steady_offset,
):
    """Plot current signed package flow rates through the transient simulation."""
    t = get_budget_time_axis(
        incremental_df,
        transient_active=True,
        steady_offset=steady_offset,
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    for pkg in package_registry:
        ax.plot(
            t,
            package_net_series(incremental_df, pkg),
            linewidth=1.6,
            label=pkg["label"],
        )

    ax.axhline(0.0, linewidth=0.8, color="black")
    ax.axvline(1.0, linewidth=0.9, linestyle="--", color="gray")
    ax.set_xlim(left=0.0)
    ax.set_xlabel("Elapsed transient time [d]")
    ax.set_ylabel("Current flow rate [m³/d]")
    ax.set_title("Water-budget components over time")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_transient_budget_cumulative(
    cumulative_df,
    package_registry,
    steady_offset,
):
    """
    Plot signed cumulative package volumes since the transient simulation began.

    FloPy/MODFLOW cumulative values also contain the nominal steady-state period.
    The first budget row is therefore subtracted from all cumulative series so
    the educational transient cumulative budget starts at zero.
    """
    t = get_budget_time_axis(
        cumulative_df,
        transient_active=True,
        steady_offset=steady_offset,
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    for pkg in package_registry:
        values = package_net_series(cumulative_df, pkg)
        if values.size:
            values = values - values[0]

        ax.plot(
            t,
            values,
            linewidth=1.6,
            label=pkg["label"],
        )

    ax.axhline(0.0, linewidth=0.8, color="black")
    ax.axvline(1.0, linewidth=0.9, linestyle="--", color="gray")
    ax.set_xlim(left=0.0)
    ax.set_xlabel("Elapsed transient time [d]")
    ax.set_ylabel("Cumulative volume since transient start [m³]")
    ax.set_title("Cumulative water-budget components")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    return fig


# -----------------------------------------------------------------------------
# Small state helper for row/column widgets
# -----------------------------------------------------------------------------
def clamp_session_int(key, minimum, maximum, default):
    if key not in st.session_state:
        st.session_state[key] = int(default)

    st.session_state[key] = int(
        min(max(int(st.session_state[key]), int(minimum)), int(maximum))
    )


# -----------------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------------
STATE_DEFAULTS = {
    "model_done": False,
    "heads_all": None,
    "head_totim": None,
    "incremental_budget": None,
    "cumulative_budget": None,
    "steady_budget_values": None,
    "model_info": {},
    "last_model_signature": None,
}

for key, value in STATE_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------------------------------------------------------
# Model input
# -----------------------------------------------------------------------------
st.header("Model setup")

transient_active = st.toggle(
    "Activate transient periods",
    value=False,
    help=(
        "Off: one steady-state stress period, matching the original model. "
        "On: steady-state reference period followed by 1 day and 7 days "
        "of transient simulation."
    ),
)

if transient_active:
    st.info(
        "Transient experiment: the first stress period establishes the "
        "steady-state reference **without pumping**. If the well is active, "
        "pumping starts at the beginning of the 1-day transient period and "
        "continues through the following 7-day period."
    )

col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("Discretization", expanded=True):
        ncol = int(
            st.number_input(
                "Number of columns",
                value=25,
                min_value=1,
                step=1,
            )
        )
        nrow = int(
            st.number_input(
                "Number of rows",
                value=21,
                min_value=1,
                step=1,
            )
        )
        delr = float(
            st.number_input(
                "Cell size x [m]",
                value=100.0,
                min_value=1.0,
                step=10.0,
            )
        )
        delc = float(
            st.number_input(
                "Cell size y [m]",
                value=100.0,
                min_value=1.0,
                step=10.0,
            )
        )
        top = float(
            st.number_input(
                "Aquifer top [m]",
                value=20.0,
                step=1.0,
            )
        )
        botm = float(
            st.number_input(
                "Aquifer bottom [m]",
                value=0.0,
                step=1.0,
            )
        )

with col2:
    with st.expander("Parameters and boundary conditions", expanded=True):
        hk = float(
            st.number_input(
                "Hydraulic conductivity K [m/d]",
                value=50.0,
                min_value=0.0001,
                step=1.0,
            )
        )

        if transient_active:
            sy = float(
                st.number_input(
                    "Specific yield Sy [-]",
                    value=0.15,
                    min_value=0.001,
                    max_value=0.99,
                    step=0.01,
                    format="%.3f",
                )
            )
            ss = float(
                st.number_input(
                    "Specific storage Ss [1/m]",
                    value=1.0e-5,
                    min_value=0.0,
                    step=1.0e-6,
                    format="%.2e",
                )
            )
        else:
            # Storage is inactive in a steady-state calculation, but explicit
            # defaults are retained for a clean model signature.
            sy = 0.15
            ss = 1.0e-5

        recharge_mm_a = float(
            st.number_input(
                "Recharge [mm/a]",
                value=200.0,
                min_value=0.0,
                step=10.0,
            )
        )
        chd_head = float(
            st.number_input(
                "Specified head east [m]",
                value=16.0,
                step=0.5,
            )
        )

        active_wel = st.checkbox(
            "Activate pumping well",
            value=False,
        )

        default_well_row = int((nrow + 1) / 2)
        default_well_col = int((ncol + 1) / 2)

        if active_wel:
            clamp_session_int(
                "transient_nwt_well_row",
                1,
                nrow,
                default_well_row,
            )
            clamp_session_int(
                "transient_nwt_well_col",
                1,
                ncol,
                default_well_col,
            )

            well_row = int(
                st.number_input(
                    "Well row #",
                    min_value=1,
                    max_value=nrow,
                    step=1,
                    key="transient_nwt_well_row",
                )
            )
            well_col = int(
                st.number_input(
                    "Well column #",
                    min_value=1,
                    max_value=ncol,
                    step=1,
                    key="transient_nwt_well_col",
                )
            )

            well_rate_abs = float(
                st.number_input(
                    "Abstraction rate [m³/d]",
                    value=150.0,
                    min_value=0.0,
                    step=10.0,
                )
            )
            well_rate = -well_rate_abs

        else:
            well_row = default_well_row
            well_col = default_well_col
            well_rate_abs = 0.0
            well_rate = 0.0

        active_riv = st.checkbox(
            "Activate river boundary",
            value=False,
        )

        if active_riv:
            clamp_session_int(
                "transient_nwt_river_row",
                1,
                nrow,
                default_well_row,
            )

            river_row = int(
                st.number_input(
                    "River row #",
                    min_value=1,
                    max_value=nrow,
                    step=1,
                    key="transient_nwt_river_row",
                )
            )

            river_length_cols = int(
                st.number_input(
                    "River length [number of columns]",
                    min_value=1,
                    max_value=ncol,
                    value=ncol,
                    step=1,
                )
            )

            river_gradient = float(
                st.number_input(
                    "River head gradient [m/m]",
                    value=0.0001,
                    min_value=0.0,
                    step=0.00001,
                    format="%.5f",
                )
            )

            riverbed_offset = float(
                st.number_input(
                    "River bottom below river head [m]",
                    value=1.0,
                    min_value=0.0,
                    step=0.1,
                )
            )

            river_conductance = float(
                st.number_input(
                    "River conductance per cell [m²/d]",
                    value=5.0,
                    min_value=0.0,
                    step=1.0,
                )
            )

        else:
            river_row = default_well_row
            river_length_cols = 0
            river_gradient = 0.0
            riverbed_offset = 1.0
            river_conductance = 0.0

with col3:
    with st.expander("Observation and model settings", expanded=True):
        # Initialize the postprocessing point at the current well location.
        # It then remains independently adjustable without invalidating a run.
        clamp_session_int(
            "transient_nwt_obs_row",
            1,
            nrow,
            well_row,
        )
        clamp_session_int(
            "transient_nwt_obs_col",
            1,
            ncol,
            well_col,
        )

        obs_row = int(
            st.number_input(
                "Observation row #",
                min_value=1,
                max_value=nrow,
                step=1,
                key="transient_nwt_obs_row",
            )
        )
        obs_col = int(
            st.number_input(
                "Observation column #",
                min_value=1,
                max_value=ncol,
                step=1,
                key="transient_nwt_obs_col",
            )
        )

        if active_wel and (obs_row != well_row or obs_col != well_col):
            if st.button("Move observation point to well"):
                st.session_state["transient_nwt_obs_row"] = int(well_row)
                st.session_state["transient_nwt_obs_col"] = int(well_col)
                st.rerun()

        time_cfg = build_time_configuration(transient_active)

        if transient_active:
            st.markdown(
                f"""
                **Time discretization**

                - steady-state reference: 1 stress period
                - transient period 1: **1 day**, {time_cfg['nstp'][1]} steps
                - transient period 2: **7 days**, {time_cfg['nstp'][2]} steps
                - total transient observation window: **8 days**
                """
            )
        else:
            st.markdown(
                """
                **Time discretization**

                - one steady-state stress period
                - transient periods are currently inactive
                """
            )

        st.caption(
            "MODFLOW-NWT is resolved automatically from the repository "
            "(`bin/mfnwt`) on Streamlit Cloud."
        )


# -----------------------------------------------------------------------------
# Derived geometry/boundaries
# -----------------------------------------------------------------------------
recharge = recharge_mm_a / 1000.0 / 365.25  # mm/a -> m/d

riv_cells = []
if active_riv:
    river_start_col = ncol - river_length_cols + 1
    riv_cells = [
        (river_row, col)
        for col in range(river_start_col, ncol + 1)
    ]

boundary_features = make_boundary_features(
    nrow=nrow,
    ncol=ncol,
    active_wel=active_wel,
    well_row=well_row,
    well_col=well_col,
    active_riv=active_riv,
    riv_cells=riv_cells,
)


# -----------------------------------------------------------------------------
# Flow-model signature
# Observation row/column are deliberately excluded because they are
# postprocessing-only controls.
# -----------------------------------------------------------------------------
current_model_signature = {
    "ncol": int(ncol),
    "nrow": int(nrow),
    "delr": float(delr),
    "delc": float(delc),
    "top": float(top),
    "botm": float(botm),
    "hk": float(hk),
    "sy": float(sy),
    "ss": float(ss),
    "recharge_mm_a": float(recharge_mm_a),
    "chd_head": float(chd_head),
    "active_wel": bool(active_wel),
    "well_row": int(well_row),
    "well_col": int(well_col),
    "well_rate": float(well_rate),
    "active_riv": bool(active_riv),
    "river_row": int(river_row),
    "river_length_cols": int(river_length_cols),
    "river_gradient": float(river_gradient),
    "riverbed_offset": float(riverbed_offset),
    "river_conductance": float(river_conductance),
    "transient_active": bool(transient_active),
    "perlen": tuple(time_cfg["perlen"]),
    "nstp": tuple(time_cfg["nstp"]),
    "steady": tuple(time_cfg["steady"]),
}


# -----------------------------------------------------------------------------
# Invalidate stale flow results only when flow-model inputs change
# -----------------------------------------------------------------------------
if (
    st.session_state.last_model_signature is not None
    and current_model_signature != st.session_state.last_model_signature
):
    cleanup_workspace(st.session_state.model_info.get("workspace"))

    st.session_state.model_done = False
    st.session_state.heads_all = None
    st.session_state.head_totim = None
    st.session_state.incremental_budget = None
    st.session_state.cumulative_budget = None
    st.session_state.steady_budget_values = None
    st.session_state.model_info = {}


# -----------------------------------------------------------------------------
# Model setup preview
# -----------------------------------------------------------------------------
with st.expander("Model setup preview and information", expanded=True):
    fig_prev, ax_prev = plt.subplots(figsize=(7, 5))

    lx = ncol * delr
    ly = nrow * delc

    plot_model_grid(ax_prev, nrow, ncol, delr, delc)
    plot_boundary_features(
        ax_prev,
        boundary_features,
        nrow,
        delr,
        delc,
    )
    plot_observation_point(
        ax_prev,
        obs_row,
        obs_col,
        nrow,
        delr,
        delc,
    )

    ax_prev.set_aspect("equal")
    ax_prev.set_xlim(0, lx)
    ax_prev.set_ylim(0, ly)
    ax_prev.set_xlabel("x [m]")
    ax_prev.set_ylabel("y [m]")
    ax_prev.set_title("Model grid, boundaries, well and observation point")
    ax_prev.legend(loc="upper right")

    show_matplotlib(fig_prev)

    if transient_active:
        well_timing_text = (
            "starts with first transient period"
            if active_wel
            else "not active"
        )
        simulation_text = (
            "steady-state reference + 1 day transient + 7 days transient"
        )
    else:
        well_timing_text = (
            "active in steady-state period"
            if active_wel
            else "not active"
        )
        simulation_text = "steady state"

    st.markdown(
        f"""
        **Grid**

        - Rows: `{nrow}`
        - Columns: `{ncol}`
        - Cell size: `{delr:.2f} × {delc:.2f} m`
        - Model size: `{ncol * delr:.2f} × {nrow * delc:.2f} m`

        **Aquifer**

        - Type: `unconfined`
        - Top / bottom: `{top:.2f} / {botm:.2f} m`
        - Hydraulic conductivity K: `{hk:.4g} m/d`
        - Specific yield Sy: `{sy:.4g}`
        - Specific storage Ss: `{ss:.4e} 1/m`

        **Boundary conditions**

        - Eastern specified head: `{chd_head:.2f} m`
        - Recharge: `{recharge_mm_a:.2f} mm/a`
        - River active: `{active_riv}`
        - Pumping well active: `{active_wel}`
        - Well timing: `{well_timing_text}`

        **Observation**

        - Row: `{obs_row}`
        - Column: `{obs_col}`

        **Simulation**

        - Executable: `MODFLOW-NWT`
        - Mode: `{simulation_text}`
        """
    )


# -----------------------------------------------------------------------------
# Run MODFLOW-NWT
# -----------------------------------------------------------------------------
run_clicked = st.button(
    "▶ Run MODFLOW-NWT model",
    type="primary",
)

status = st.empty()

if run_clicked:
    previous_workspace = st.session_state.model_info.get("workspace")
    cleanup_workspace(previous_workspace)

    ws = Path(tempfile.mkdtemp(prefix="rect_nwt_transient_"))
    modelname = "rect_nwt_transient"

    try:
        mfnwt_exe = locate_mfnwt()

        mf = flopy.modflow.Modflow(
            modelname,
            exe_name=str(mfnwt_exe),
            model_ws=str(ws),
            version="mfnwt",
        )

        # DIS
        flopy.modflow.ModflowDis(
            mf,
            nlay=1,
            nrow=nrow,
            ncol=ncol,
            delr=delr,
            delc=delc,
            top=top,
            botm=botm,
            nper=time_cfg["nper"],
            perlen=time_cfg["perlen"],
            nstp=time_cfg["nstp"],
            tsmult=time_cfg["tsmult"],
            steady=time_cfg["steady"],
        )

        # BAS
        ibound = np.ones((1, nrow, ncol), dtype=int)
        strt = np.full((1, nrow, ncol), chd_head)

        flopy.modflow.ModflowBas(
            mf,
            ibound=ibound,
            strt=strt,
        )

        # UPW
        #
        # Sy/Ss are inactive during steady-state periods but are required for
        # the transient unconfined response. IPHDRY=1 is retained from the
        # cloud NWT version and is compatible with later MODPATH use.
        flopy.modflow.ModflowUpw(
            mf,
            laytyp=1,
            hk=hk,
            vka=hk,
            ss=ss,
            sy=sy,
            ipakcb=53,
            iphdry=1,
        )

        # CHD -- explicitly repeated for every period.
        chd_cells = [
            [0, irow, ncol - 1, chd_head, chd_head]
            for irow in range(nrow)
        ]
        chd_spd = {
            kper: chd_cells
            for kper in range(time_cfg["nper"])
        }

        flopy.modflow.ModflowChd(
            mf,
            stress_period_data=chd_spd,
        )

        # Recharge -- constant in all periods.
        recharge_spd = {
            kper: recharge
            for kper in range(time_cfg["nper"])
        }
        flopy.modflow.ModflowRch(
            mf,
            rech=recharge_spd,
            ipakcb=53,
        )

        # Optional pumping well.
        wel_spd = build_well_stress_period_data(
            active_wel=active_wel,
            transient_active=transient_active,
            well_row=well_row,
            well_col=well_col,
            well_rate=well_rate,
        )

        if wel_spd is not None:
            flopy.modflow.ModflowWel(
                mf,
                stress_period_data=wel_spd,
                ipakcb=53,
            )

        # Optional river -- explicitly repeated for every period.
        if active_riv:
            riv_period = []

            for row, col in riv_cells:
                distance_from_east = (ncol - col) * delr
                river_head = chd_head + river_gradient * distance_from_east
                river_bottom = river_head - riverbed_offset

                riv_period.append(
                    [
                        0,
                        row - 1,
                        col - 1,
                        river_head,
                        river_conductance,
                        river_bottom,
                    ]
                )

            riv_spd = {
                kper: riv_period
                for kper in range(time_cfg["nper"])
            }

            flopy.modflow.ModflowRiv(
                mf,
                stress_period_data=riv_spd,
                ipakcb=53,
            )

        # NWT solver -- retained from the original educational model.
        flopy.modflow.ModflowNwt(
            mf,
            headtol=1e-6,
            fluxtol=500,
            maxiterout=100,
            linmeth=1,
            options="SIMPLE",
        )

        # Save and print every time step so both head and listing-budget
        # time series can be postprocessed.
        flopy.modflow.ModflowOc(
            mf,
            stress_period_data=build_output_control(time_cfg["nstp"]),
            compact=True,
        )

        mf.write_input()

        status.info("Running MODFLOW-NWT...")
        with st.spinner("MODFLOW-NWT simulation"):
            with native_run_semaphore():
                success, buff = mf.run_model(
                    silent=True,
                    report=True,
                )

        if not success:
            raise RuntimeError(
                "MODFLOW-NWT did not terminate normally.\n"
                + "\n".join(buff[-20:])
            )

        # ---- Heads at every saved time
        hds_path = ws / f"{modelname}.hds"
        headobj = flopy.utils.HeadFile(str(hds_path))

        try:
            head_totim = np.asarray(
                headobj.get_times(),
                dtype=float,
            )

            heads_all = np.asarray(
                [
                    headobj.get_data(totim=float(t))[0]
                    for t in head_totim
                ]
            )
        finally:
            headobj.close()

        # ---- Listing-file budget time series
        list_path = ws / f"{modelname}.list"
        incremental_budget, cumulative_budget = (
            read_listing_budget_dataframes(list_path)
        )

        steady_registry = make_package_registry(
            active_wel=active_wel,
            active_riv=active_riv,
            include_storage=False,
        )
        steady_budget_values = budget_snapshot_from_row(
            incremental_budget.iloc[-1],
            steady_registry,
        )

        # ---- Store results
        st.session_state.model_done = True
        st.session_state.heads_all = heads_all
        st.session_state.head_totim = head_totim
        st.session_state.incremental_budget = incremental_budget
        st.session_state.cumulative_budget = cumulative_budget
        st.session_state.steady_budget_values = steady_budget_values
        st.session_state.last_model_signature = current_model_signature

        st.session_state.model_info = {
            "workspace": str(ws),
            "modelname": modelname,
            "nrow": int(nrow),
            "ncol": int(ncol),
            "delr": float(delr),
            "delc": float(delc),
            "top": float(top),
            "botm": float(botm),
            "hk": float(hk),
            "sy": float(sy),
            "ss": float(ss),
            "recharge": float(recharge),
            "recharge_mm_a": float(recharge_mm_a),
            "chd_head": float(chd_head),
            "active_wel": bool(active_wel),
            "well_row": int(well_row),
            "well_col": int(well_col),
            "well_rate_abs": float(well_rate_abs),
            "active_riv": bool(active_riv),
            "riv_cells": list(riv_cells),
            "boundary_features": boundary_features,
            "transient_active": bool(transient_active),
            "time_cfg": time_cfg,
        }

        status.success("✅ MODFLOW-NWT model finished successfully.")

    except Exception as exc:
        cleanup_workspace(ws)

        st.session_state.model_done = False
        st.session_state.heads_all = None
        st.session_state.head_totim = None
        st.session_state.incremental_budget = None
        st.session_state.cumulative_budget = None
        st.session_state.steady_budget_values = None
        st.session_state.model_info = {}

        status.error("❌ MODFLOW-NWT simulation failed.")
        st.error(str(exc))


# -----------------------------------------------------------------------------
# Postprocessing
# -----------------------------------------------------------------------------
if st.session_state.model_done:
    info = st.session_state.model_info
    heads_all = np.asarray(st.session_state.heads_all)
    head_totim = np.asarray(st.session_state.head_totim, dtype=float)
    incremental_budget = st.session_state.incremental_budget
    cumulative_budget = st.session_state.cumulative_budget

    result_transient = bool(info["transient_active"])
    result_time_cfg = info["time_cfg"]

    # Observation point is a pure postprocessing selection. Clamp against the
    # grid used for the stored result in case the UI grid was modified but not
    # rerun yet (normally stale-model handling already prevents this).
    result_obs_row = min(max(int(obs_row), 1), int(info["nrow"]))
    result_obs_col = min(max(int(obs_col), 1), int(info["ncol"]))

    obs_heads = heads_all[
        :,
        result_obs_row - 1,
        result_obs_col - 1,
    ]

    st.header("Simulation results")

    if result_transient:
        elapsed_head_time = elapsed_time_from_totim(
            head_totim,
            transient_active=True,
            steady_offset=result_time_cfg["steady_offset"],
        )

        # ---------------------------------------------------------------------
        # Observation head: primary transient diagnostic
        # ---------------------------------------------------------------------
        st.subheader("Observation point")

        fig_obs, ax_obs = plt.subplots(figsize=(8, 4.5))
        ax_obs.plot(
            elapsed_head_time,
            obs_heads,
            marker="o",
            markersize=3.5,
            linewidth=1.2,
        )
        ax_obs.axvline(
            1.0,
            linewidth=0.9,
            linestyle="--",
            color="gray",
        )
        ax_obs.set_xlim(
            0.0,
            result_time_cfg["transient_duration"],
        )
        ax_obs.set_xlabel("Elapsed transient time [d]")
        ax_obs.set_ylabel("Hydraulic head [m]")
        ax_obs.set_title(
            f"Head at observation cell "
            f"(row {result_obs_row}, column {result_obs_col})"
        )
        ax_obs.grid(True, alpha=0.25)
        fig_obs.tight_layout()
        show_matplotlib(fig_obs)

        st.caption(
            "The dashed vertical line marks the transition from the 1-day "
            "transient stress period to the following 7-day period."
        )

        # ---------------------------------------------------------------------
        # Budget over time: primary transient diagnostics
        # ---------------------------------------------------------------------
        st.subheader("Water budget over time")

        transient_registry = make_package_registry(
            active_wel=info["active_wel"],
            active_riv=info["active_riv"],
            include_storage=True,
        )

        fig_rate = plot_transient_budget_rate(
            incremental_budget,
            transient_registry,
            steady_offset=result_time_cfg["steady_offset"],
        )
        show_matplotlib(fig_rate)

        fig_cum = plot_transient_budget_cumulative(
            cumulative_budget,
            transient_registry,
            steady_offset=result_time_cfg["steady_offset"],
        )
        show_matplotlib(fig_cum)

        st.caption(
            "Positive values represent flow into the groundwater model; "
            "negative values represent flow out. The cumulative plot is "
            "referenced to zero at the end of the steady-state period, so it "
            "shows cumulative volume during the 8-day transient experiment."
        )

    else:
        # ---------------------------------------------------------------------
        # Steady-state observation + budget, preserving the original style
        # ---------------------------------------------------------------------
        st.subheader("Observation point")
        st.metric(
            "Hydraulic head",
            f"{obs_heads[-1]:.3f} m",
            help=(
                f"Steady-state head at row {result_obs_row}, "
                f"column {result_obs_col}."
            ),
        )

        st.header("Water budget")

        steady_registry = make_package_registry(
            active_wel=info["active_wel"],
            active_riv=info["active_riv"],
            include_storage=False,
        )

        steady_budget = budget_snapshot_from_row(
            incremental_budget.iloc[-1],
            steady_registry,
        )

        fig_budget = plot_budget_bar_chart(
            steady_budget,
            steady_registry,
        )
        show_matplotlib(fig_budget)

        st.markdown(
            budget_markdown(
                steady_budget,
                steady_registry,
            )
        )

    # =========================================================================
    # Additional postprocessing plots in expanders
    # =========================================================================

    # -------------------------------------------------------------------------
    # Spatial hydraulic-head map
    # -------------------------------------------------------------------------
    with st.expander("Additional plot: spatial hydraulic-head distribution"):
        if result_transient:
            elapsed_head_time = elapsed_time_from_totim(
                head_totim,
                transient_active=True,
                steady_offset=result_time_cfg["steady_offset"],
            )

            time_labels = []
            for idx, t in enumerate(elapsed_head_time):
                if idx == 0:
                    time_labels.append("Steady-state reference (t = 0 d)")
                else:
                    time_labels.append(f"Transient t = {t:.3f} d")

            selected_label = st.selectbox(
                "Head snapshot",
                options=time_labels,
                index=len(time_labels) - 1,
                key="transient_nwt_head_snapshot",
            )
            selected_index = time_labels.index(selected_label)
        else:
            selected_index = len(heads_all) - 1
            st.caption("Steady-state hydraulic-head distribution.")

        head_selected = heads_all[selected_index]

        fig_head, ax_head = plt.subplots(figsize=(8, 6))

        x_edges = np.linspace(
            0,
            info["ncol"] * info["delr"],
            info["ncol"] + 1,
        )
        y_edges = np.linspace(
            0,
            info["nrow"] * info["delc"],
            info["nrow"] + 1,
        )

        c = ax_head.pcolormesh(
            x_edges,
            y_edges,
            head_selected[::-1, :],
            shading="auto",
            alpha=0.55,
        )

        if info["nrow"] >= 2 and info["ncol"] >= 2:
            x_centers = (
                np.arange(info["ncol"]) + 0.5
            ) * info["delr"]
            y_centers = (
                np.arange(info["nrow"]) + 0.5
            ) * info["delc"]

            X, Y = np.meshgrid(
                x_centers,
                y_centers,
            )

            contours = ax_head.contour(
                X,
                Y,
                head_selected[::-1, :],
                colors="black",
                linewidths=0.8,
            )
            ax_head.clabel(
                contours,
                fmt="%.2f",
                fontsize=8,
            )

        plot_model_grid(
            ax_head,
            info["nrow"],
            info["ncol"],
            info["delr"],
            info["delc"],
        )
        plot_boundary_features(
            ax_head,
            info["boundary_features"],
            info["nrow"],
            info["delr"],
            info["delc"],
        )
        plot_observation_point(
            ax_head,
            result_obs_row,
            result_obs_col,
            info["nrow"],
            info["delr"],
            info["delc"],
        )

        ax_head.set_aspect("equal")
        ax_head.set_xlim(
            0,
            info["ncol"] * info["delr"],
        )
        ax_head.set_ylim(
            0,
            info["nrow"] * info["delc"],
        )
        ax_head.set_xlabel("x [m]")
        ax_head.set_ylabel("y [m]")
        ax_head.set_title("Simulated hydraulic head [m]")
        ax_head.legend(loc="upper right")
        fig_head.colorbar(c, ax=ax_head, label="Head [m]")
        fig_head.tight_layout()

        show_matplotlib(fig_head)

    # -------------------------------------------------------------------------
    # Cross sections
    # -------------------------------------------------------------------------
    with st.expander("Additional plots: hydraulic-head cross sections"):
        col_sec1, col_sec2 = st.columns(2)

        with col_sec1:
            selected_row = int(
                st.number_input(
                    "Row # for W-E section",
                    min_value=1,
                    max_value=int(info["nrow"]),
                    value=int((info["nrow"] + 1) / 2),
                    step=1,
                    key="transient_nwt_section_row",
                )
            )

        with col_sec2:
            selected_col = int(
                st.number_input(
                    "Column # for N-S section",
                    min_value=1,
                    max_value=int(info["ncol"]),
                    value=int((info["ncol"] + 1) / 2),
                    step=1,
                    key="transient_nwt_section_col",
                )
            )

        if result_transient:
            elapsed_head_time = elapsed_time_from_totim(
                head_totim,
                transient_active=True,
                steady_offset=result_time_cfg["steady_offset"],
            )

            section_labels = []
            for idx, t in enumerate(elapsed_head_time):
                if idx == 0:
                    section_labels.append(
                        "Steady-state reference (t = 0 d)"
                    )
                else:
                    section_labels.append(
                        f"Transient t = {t:.3f} d"
                    )

            section_time_label = st.selectbox(
                "Cross-section time",
                options=section_labels,
                index=len(section_labels) - 1,
                key="transient_nwt_section_time",
            )
            section_index = section_labels.index(section_time_label)
        else:
            section_index = len(heads_all) - 1

        section_heads = heads_all[section_index]

        # W-E
        irow = selected_row - 1
        x = (
            np.arange(info["ncol"]) + 0.5
        ) * info["delr"]
        h_we = section_heads[irow, :]

        fig_we, ax_we = plt.subplots(figsize=(8, 4))
        ax_we.plot(x, h_we, marker="o", label="Hydraulic head")
        ax_we.plot(
            [x[0], x[-1]],
            [info["top"], info["top"]],
            linestyle="--",
            label="Aquifer top",
        )
        ax_we.plot(
            [x[0], x[-1]],
            [info["botm"], info["botm"]],
            linestyle="--",
            label="Aquifer bottom",
        )
        ax_we.set_title(
            f"West-east cross section, row {selected_row}"
        )
        ax_we.set_xlabel("x [m]")
        ax_we.set_ylabel("Elevation / head [m]")
        ax_we.grid(True, alpha=0.3)
        ax_we.legend()
        fig_we.tight_layout()
        show_matplotlib(fig_we)

        # N-S
        icol = selected_col - 1
        y = (
            np.arange(info["nrow"]) + 0.5
        ) * info["delc"]
        h_ns = section_heads[::-1, icol]

        fig_ns, ax_ns = plt.subplots(figsize=(8, 4))
        ax_ns.plot(y, h_ns, marker="o", label="Hydraulic head")
        ax_ns.plot(
            [y[0], y[-1]],
            [info["top"], info["top"]],
            linestyle="--",
            label="Aquifer top",
        )
        ax_ns.plot(
            [y[0], y[-1]],
            [info["botm"], info["botm"]],
            linestyle="--",
            label="Aquifer bottom",
        )
        ax_ns.set_title(
            f"North-south cross section, column {selected_col}"
        )
        ax_ns.set_xlabel("y [m]")
        ax_ns.set_ylabel("Elevation / head [m]")
        ax_ns.grid(True, alpha=0.3)
        ax_ns.legend()
        fig_ns.tight_layout()
        show_matplotlib(fig_ns)

    # -------------------------------------------------------------------------
    # Numerical budget details
    # -------------------------------------------------------------------------
    with st.expander("Additional information: numerical budget details"):
        if result_transient:
            transient_registry = make_package_registry(
                active_wel=info["active_wel"],
                active_riv=info["active_riv"],
                include_storage=True,
            )

            final_budget = budget_snapshot_from_row(
                incremental_budget.iloc[-1],
                transient_registry,
            )

            st.markdown(
                budget_markdown(
                    final_budget,
                    transient_registry,
                )
            )
            st.caption(
                "The values above are the current rates at the final "
                "transient time step."
            )
        else:
            steady_registry = make_package_registry(
                active_wel=info["active_wel"],
                active_riv=info["active_riv"],
                include_storage=False,
            )
            steady_budget = budget_snapshot_from_row(
                incremental_budget.iloc[-1],
                steady_registry,
            )
            st.markdown(
                budget_markdown(
                    steady_budget,
                    steady_registry,
                )
            )


# -----------------------------------------------------------------------------
# Deployment diagnostic
# -----------------------------------------------------------------------------
with st.expander("Deployment diagnostic"):
    try:
        executable = locate_mfnwt()
        st.success(f"MODFLOW-NWT executable found: `{executable}`")
    except Exception as exc:
        st.error(str(exc))
