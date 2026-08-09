"""Interactive MODFLOW 6 + MODPATH 7 Streamlit cloud demonstration."""

from __future__ import annotations

import threading

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
import numpy as np
import streamlit as st

from mf6_model import (
    BOTM,
    DEFAULT_NCOL,
    DEFAULT_NROW,
    DELC,
    DELR,
    NLAY,
    PARTICLES_PER_WELL,
    TOP,
    WELL_LAYER,
    ModelParameters,
    TrackingResult,
    cleanup_workspace,
    get_mf6_version,
    locate_mf6,
    locate_mp7,
    run_modflow,
    run_modpath,
)

st.set_page_config(page_title="MODFLOW + MODPATH Cloud Test", page_icon="💧", layout="wide")


@st.cache_resource
def native_run_semaphore() -> threading.BoundedSemaphore:
    return threading.BoundedSemaphore(value=2)


def default_well_positions(nrow: int, ncol: int, count: int) -> list[tuple[int, int]]:
    """Return central default well positions (zero-based row/column)."""
    centre_row = nrow // 2
    centre_col = ncol // 2
    offsets = (0, -2, 2)
    return [(centre_row + offsets[i], centre_col) for i in range(count)]


def plot_model_grid(params: ModelParameters):
    """Plan-view grid directly below the inputs, with CHD and wells marked."""
    data = np.zeros((params.nrow, params.ncol), dtype=int)
    data[:, 0] = 1
    data[:, -1] = 1

    x = np.arange(params.ncol + 1)
    y = np.arange(params.nrow + 1)
    fig, ax = plt.subplots(figsize=(9.0, 4.2))
    cmap = ListedColormap(["white", "#b9dcf5"])
    ax.pcolormesh(x, y, data, cmap=cmap, shading="flat", edgecolors="0.78", linewidth=0.35)

    for idx, (row, col) in enumerate(params.well_positions, start=1):
        ax.plot(col + 0.5, row + 0.5, marker="*", markersize=11, linestyle="none", label=f"Well {idx}" if idx == 1 else None)
        ax.text(col + 0.75, row + 0.5, str(idx), va="center", fontsize=8)

    ax.set_xlim(0, params.ncol)
    ax.set_ylim(params.nrow, 0)
    ax.set_aspect("equal")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.set_title("Model grid — constant-head cells are marked on both lateral boundaries")

    xstep = max(1, params.ncol // 10)
    ystep = max(1, params.nrow // 10)
    ax.set_xticks(np.arange(0.5, params.ncol, xstep), labels=[str(i + 1) for i in range(0, params.ncol, xstep)])
    ax.set_yticks(np.arange(0.5, params.nrow, ystep), labels=[str(i + 1) for i in range(0, params.nrow, ystep)])

    from matplotlib.patches import Patch
    handles = [Patch(facecolor="#b9dcf5", edgecolor="0.6", label="CHD cell (all layers)")]
    if params.well_positions:
        handles.append(Line2D([], [], marker="*", linestyle="none", label=f"Pumping well(s), layer {WELL_LAYER + 1}"))
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False)
    fig.tight_layout()
    return fig


def _contour_levels(values: np.ndarray, dh: float) -> np.ndarray:
    vmin = float(np.nanmin(values)); vmax = float(np.nanmax(values))
    start = np.floor(vmin / dh) * dh
    stop = np.ceil(vmax / dh) * dh
    levels = np.arange(start, stop + 0.5 * dh, dh)
    if levels.size < 2:
        levels = np.array([vmin - 0.5 * dh, vmin + 0.5 * dh])
    return levels


def _plot_layer_track_segments(ax, tracking: TrackingResult, layer: int) -> None:
    """Plot only pathline portions that lie in the selected model layer."""
    for track in tracking.tracks:
        mask = np.asarray(track.layer) == layer
        if not np.any(mask):
            continue
        indices = np.flatnonzero(mask)
        splits = np.split(indices, np.where(np.diff(indices) > 1)[0] + 1)
        for seg in splits:
            if seg.size >= 2:
                ax.plot(track.x[seg], track.y[seg], linewidth=0.9, alpha=0.7, zorder=5)
            elif seg.size == 1:
                ax.plot(track.x[seg], track.y[seg], marker=".", markersize=2.5, linestyle="none", alpha=0.7, zorder=5)

    start_mask = tracking.start_layer == layer
    if np.any(start_mask):
        starts = tracking.start_xyz[start_mask]
        ax.scatter(starts[:, 0], starts[:, 1], s=16, facecolors="white", edgecolors="black", linewidths=0.55, label="Particle starts", zorder=6)


def plot_plan_view(head: np.ndarray, layer: int, params: ModelParameters, dh: float,
                   color_fill: bool, tracking: TrackingResult | None = None):
    """Plot head contours with optional color fill and one particle-tracking mode."""
    x = (np.arange(params.ncol) + 0.5) * DELR
    y = (np.arange(params.nrow) + 0.5) * DELC
    xx, yy = np.meshgrid(x, y)
    zz = np.flipud(head[layer])
    levels = _contour_levels(zz, dh)

    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    if color_fill:
        filled = ax.contourf(xx, yy, zz, levels=levels, extend="both")
        fig.colorbar(filled, ax=ax, label="Hydraulic head (m)")

    contours = ax.contour(xx, yy, zz, levels=levels, linewidths=0.8)
    ax.clabel(contours, inline=True, fontsize=8, fmt="%.2g")

    # Show CHD boundary cell centres as a subtle reference.
    boundary_y = (np.arange(params.nrow) + 0.5) * DELC
    ax.scatter(np.full(params.nrow, 0.5 * DELR), boundary_y, marker="s", s=10, alpha=0.35, label="CHD cells")
    ax.scatter(np.full(params.nrow, (params.ncol - 0.5) * DELR), boundary_y, marker="s", s=10, alpha=0.35)

    if tracking is not None:
        _plot_layer_track_segments(ax, tracking, layer)

    if layer == WELL_LAYER:
        for idx, (row, col) in enumerate(params.well_positions, start=1):
            well_x = (col + 0.5) * DELR
            well_y = (params.nrow - row - 0.5) * DELC
            ax.plot(well_x, well_y, marker="*", markersize=10, linestyle="none", label="Pumping well" if idx == 1 else None, zorder=7)
            ax.text(well_x + 0.25 * DELR, well_y, str(idx), fontsize=8, va="center", zorder=7)

    ax.set_xlim(0.0, params.ncol * DELR)
    ax.set_ylim(0.0, params.nrow * DELC)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    title = f"Hydraulic head — layer {layer + 1}"
    if tracking is not None:
        title += f" + {tracking.direction} pathlines"
    ax.set_title(title)
    ax.set_aspect("equal")
    ax.legend(loc="best")
    fig.tight_layout()
    return fig


def plot_head_profiles(head: np.ndarray, params: ModelParameters):
    """Plot head profiles through the row containing Well 1."""
    x = (np.arange(params.ncol) + 0.5) * DELR
    profile_row = params.well_positions[0][0]
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    for layer in range(NLAY):
        ax.plot(x, head[layer, profile_row, :], label=f"Layer {layer + 1}")
    marked = 0
    for row, col in params.well_positions:
        if row == profile_row:
            ax.axvline((col + 0.5) * DELR, linestyle="--", linewidth=0.8, alpha=0.6, label="Well position(s)" if marked == 0 else None)
            marked += 1
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Hydraulic head (m)")
    ax.set_title(f"Head profiles through row {profile_row + 1} (Well 1 row)")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_vertical_pathlines(tracking: TrackingResult, params: ModelParameters):
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    for track in tracking.tracks:
        ax.plot(track.x, track.z, linewidth=0.8, alpha=0.65)
    if tracking.start_xyz.size:
        ax.scatter(tracking.start_xyz[:, 0], tracking.start_xyz[:, 2], s=14, facecolors="white", edgecolors="black", linewidths=0.5, label="Particle starts", zorder=4)
    ax.axhline(TOP, linewidth=0.8, alpha=0.6)
    for bottom in BOTM:
        ax.axhline(bottom, linewidth=0.8, alpha=0.6)
    for idx, (_row, col) in enumerate(params.well_positions, start=1):
        well_x = (col + 0.5) * DELR
        layer_top = TOP if WELL_LAYER == 0 else BOTM[WELL_LAYER - 1]
        well_z = 0.5 * (layer_top + BOTM[WELL_LAYER])
        ax.plot(well_x, well_z, marker="*", markersize=9, linestyle="none", label="Pumping well(s)" if idx == 1 else None)
    ax.set_xlim(0.0, params.ncol * DELR)
    ax.set_ylim(BOTM[-1], TOP)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Elevation z (m)")
    ax.set_title(f"{tracking.direction.capitalize()} pathlines — vertical x-z projection")
    ax.legend(loc="best")
    fig.tight_layout()
    return fig


def discard_flow_workspace() -> None:
    old = st.session_state.pop("flow_result", None)
    if old is not None:
        cleanup_workspace(old.workspace)
    st.session_state.pop("flow_signature", None)
    st.session_state.pop("modpath_result", None)
    st.session_state.pop("modpath_signature", None)


def show_cumulative_budget(items: list[tuple[str, float]]) -> None:
    st.markdown("#### Cumulative mass balance")
    st.caption(
        "Values are read directly from the final MODFLOW 6 cumulative budget table. "
        "Because this steady-state test uses a 1-day stress period, cumulative flow volumes are reported over that 1-day period."
    )
    if not items:
        st.warning("No cumulative budget table could be parsed from the MODFLOW listing file.")
        return
    lines = ["| Budget term | Cumulative value |", "|---|---:|"]
    for name, value in items:
        unit = "%" if "PERCENT" in name.upper() else "m³"
        lines.append(f"| {name.replace('_', ' ')} | {value:,.4g} {unit} |")
    st.markdown("\n".join(lines))


st.title("💧 MODFLOW 6 + MODPATH 7 Cloud Test")
st.write(
    "Design a small three-layer groundwater-flow model, run MODFLOW explicitly, "
    "and optionally calculate forward or backward MODPATH pathlines without rerunning the flow model."
)

# -----------------------------------------------------------------------------
# Model inputs
# -----------------------------------------------------------------------------
st.subheader("Model design")

g1, g2, g3 = st.columns(3)
with g1:
    nrow = st.slider("Number of rows", min_value=9, max_value=61, value=DEFAULT_NROW, step=2, help="Odd values keep an unambiguous central row.")
with g2:
    ncol = st.slider("Number of columns", min_value=9, max_value=61, value=DEFAULT_NCOL, step=2, help="Odd values keep an unambiguous central column.")
with g3:
    number_wells = st.slider("Number of pumping wells", min_value=1, max_value=3, value=1, step=1)

st.caption(f"Three layers are retained; each cell is {DELR:.0f} × {DELC:.0f} m. Wells are screened in layer {WELL_LAYER + 1}.")

b1, b2, b3 = st.columns(3)
with b1:
    head_left = st.number_input("Left specified head (m)", min_value=0.0, max_value=100.0, value=32.0, step=0.5)
    head_right = st.number_input("Right specified head (m)", min_value=0.0, max_value=100.0, value=31.0, step=0.5)
with b2:
    k_layer1 = st.number_input("K layer 1 (m/day)", min_value=0.001, max_value=1000.0, value=10.0, format="%.3f")
    k_layer2 = st.number_input("K layer 2 (m/day)", min_value=0.001, max_value=1000.0, value=0.10, format="%.3f")
    k_layer3 = st.number_input("K layer 3 (m/day)", min_value=0.001, max_value=1000.0, value=5.0, format="%.3f")
with b3:
    pumping_rate = st.number_input("Pumping rate per well (m³/day)", min_value=0.0, max_value=800.0, value=300.0, step=50.0, help="Positive extraction magnitude; MODFLOW receives a negative WEL flux for every active well.")
    vertical_anisotropy = st.number_input("Vertical anisotropy Kz/Kx (-)", min_value=0.001, max_value=1.0, value=0.10, format="%.3f")

st.markdown("#### Well positions")
defaults = default_well_positions(nrow, ncol, number_wells)
well_positions: list[tuple[int, int]] = []
well_cols = st.columns(number_wells)
for i in range(number_wells):
    default_row, default_col = defaults[i]
    with well_cols[i]:
        st.markdown(f"**Well {i + 1}**")
        row_1based = st.number_input(
            "Row", min_value=1, max_value=nrow, value=default_row + 1, step=1,
            key=f"well_row_{i}_{nrow}_{ncol}",
        )
        col_1based = st.number_input(
            "Column", min_value=2, max_value=ncol - 1, value=default_col + 1, step=1,
            key=f"well_col_{i}_{nrow}_{ncol}",
            help="Boundary columns 1 and the last column are reserved for CHD cells.",
        )
        well_positions.append((int(row_1based) - 1, int(col_1based) - 1))

params = ModelParameters(
    head_left=float(head_left), head_right=float(head_right), pumping_rate=float(pumping_rate),
    k_layer1=float(k_layer1), k_layer2=float(k_layer2), k_layer3=float(k_layer3),
    vertical_anisotropy=float(vertical_anisotropy), nrow=int(nrow), ncol=int(ncol),
    well_positions=tuple(well_positions),
)

has_duplicate_wells = len(set(well_positions)) != len(well_positions)
if has_duplicate_wells:
    st.error("Two or more wells occupy the same cell. Please choose unique well positions before running MODFLOW.")

# Grid is intentionally placed immediately below the design inputs.
fig = plot_model_grid(params)
st.pyplot(fig, clear_figure=True)
plt.close(fig)

st.caption(
    f"Backward tracking will use {params.backward_particle_count} particles ({PARTICLES_PER_WELL} per well). "
    f"Forward tracking will use {params.forward_particle_count} particles (one per CHD cell)."
)

current_flow_signature = params.signature()
if "flow_signature" in st.session_state and st.session_state.flow_signature != current_flow_signature:
    discard_flow_workspace()
    st.info("Model design changed. Existing flow/pathline results were cleared; press **Run MODFLOW** for the new design.")

run_mf6_clicked = st.button("Run MODFLOW", type="primary", disabled=has_duplicate_wells)
if run_mf6_clicked:
    discard_flow_workspace()
    try:
        with st.spinner("Running MODFLOW 6..."):
            with native_run_semaphore():
                flow_result = run_modflow(params)
        st.session_state.flow_result = flow_result
        st.session_state.flow_signature = current_flow_signature
        st.success("MODFLOW terminated normally. The flow solution is ready for postprocessing and MODPATH.")
    except Exception as exc:
        discard_flow_workspace()
        st.error("The MODFLOW simulation failed.")
        st.exception(exc)

# -----------------------------------------------------------------------------
# Independent MODPATH
# -----------------------------------------------------------------------------
if "flow_result" in st.session_state:
    st.divider()
    st.markdown("#### Particle tracking")
    mp1, mp2 = st.columns([1, 2])
    with mp1:
        effective_porosity = st.number_input(
            "Effective porosity (-)", min_value=0.01, max_value=0.60, value=0.25,
            step=0.05, format="%.2f",
            help="Controls particle velocity/travel time. It does not change the steady-flow head solution.",
        )
    current_modpath_signature = (st.session_state.flow_signature, float(effective_porosity))
    if "modpath_signature" in st.session_state and st.session_state.modpath_signature != current_modpath_signature:
        st.session_state.pop("modpath_result", None)
        st.session_state.pop("modpath_signature", None)
        st.info("Effective porosity changed. MODFLOW remains valid; rerun MODPATH only.")
    with mp2:
        st.write(""); st.write("")
        run_mp7_clicked = st.button("Run MODPATH")
    if run_mp7_clicked:
        try:
            with st.spinner("Running backward and forward MODPATH 7 tracking..."):
                with native_run_semaphore():
                    mp_result = run_modpath(st.session_state.flow_result, effective_porosity=float(effective_porosity))
            st.session_state.modpath_result = mp_result
            st.session_state.modpath_signature = current_modpath_signature
            st.success("MODPATH terminated normally. MODFLOW was not rerun.")
        except Exception as exc:
            st.session_state.pop("modpath_result", None)
            st.session_state.pop("modpath_signature", None)
            st.error("The MODPATH workflow failed.")
            st.exception(exc)

# -----------------------------------------------------------------------------
# Postprocessing
# -----------------------------------------------------------------------------
if "flow_result" in st.session_state:
    flow_result = st.session_state.flow_result
    head = flow_result.head
    result_params = flow_result.params

    st.divider()
    st.subheader("Results")

    well_heads = [head[WELL_LAYER, row, col] for row, col in result_params.well_positions]
    well_text = ", ".join(f"W{i + 1}: {h:.3f} m" for i, h in enumerate(well_heads))
    st.markdown(
        f"**MODFLOW:** `{flow_result.mf6_version}`  \n"
        f"Runtime: **{flow_result.runtime_seconds:.3f} s**  \n"
        f"Head at pumping cell(s): **{well_text}**  \n"
        f"Minimum / maximum simulated head: **{np.min(head):.3f} / {np.max(head):.3f} m**"
    )

    p1, p2, p3, p4 = st.columns([1, 1, 1, 1.7])
    with p1:
        display_layer = st.selectbox("Head layer", options=list(range(NLAY)), format_func=lambda i: f"Layer {i + 1}", index=WELL_LAYER)
    with p2:
        contour_interval = st.number_input("Contour interval Δh (m)", min_value=0.01, max_value=20.0, value=1.0, step=0.25, format="%.2f")
    with p3:
        color_fill = st.toggle("Color fill", value=True)
    with p4:
        particle_options = ["No particles"]
        if "modpath_result" in st.session_state:
            particle_options += ["Forward", "Backward"]
        particle_display = st.radio("Particles / pathlines", particle_options, horizontal=True)

    selected_tracking = None
    if "modpath_result" in st.session_state:
        mp_result = st.session_state.modpath_result
        if particle_display == "Forward":
            selected_tracking = mp_result.forward
        elif particle_display == "Backward":
            selected_tracking = mp_result.backward

    left, right = st.columns(2)
    with left:
        fig = plot_plan_view(head, display_layer, result_params, float(contour_interval), bool(color_fill), selected_tracking)
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)
    with right:
        fig = plot_head_profiles(head, result_params)
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)

    if selected_tracking is not None:
        st.caption(
            f"{selected_tracking.direction.capitalize()} tracking: "
            f"{selected_tracking.requested_particles} released particles; "
            f"{selected_tracking.pathline_count} pathline records. The head plot shows only pathline portions within the selected layer."
        )
        fig = plot_vertical_pathlines(selected_tracking, result_params)
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)

    show_balance = st.toggle("Show cumulative mass balance", value=False)
    if show_balance:
        show_cumulative_budget(flow_result.cumulative_budget)

    if "modpath_result" in st.session_state:
        with st.expander("MODPATH console output"):
            st.markdown("**Backward tracking**")
            st.code(st.session_state.modpath_result.backward.stdout, language="text")
            st.markdown("**Forward tracking**")
            st.code(st.session_state.modpath_result.forward.stdout, language="text")

    with st.expander("MODFLOW console output"):
        st.code(flow_result.stdout, language="text")

with st.expander("Deployment diagnostic"):
    try:
        mf6_path = locate_mf6(); mf6_version = get_mf6_version(mf6_path)
        st.write(f"MODFLOW executable: `{mf6_path}`")
        st.write(f"MODFLOW version check: `{mf6_version}`")
        st.success("MODFLOW 6 is available to the Streamlit process.")
    except Exception as exc:
        st.error("MODFLOW 6 executable is not available."); st.exception(exc)
    try:
        mp7_path = locate_mp7()
        st.write(f"MODPATH executable: `{mp7_path}`")
        st.success("MODPATH 7 is available to the Streamlit process.")
    except Exception as exc:
        st.error("MODPATH 7 executable is not available."); st.exception(exc)
