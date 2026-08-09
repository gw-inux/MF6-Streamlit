"""Interactive MODFLOW 6 + MODPATH 7 Streamlit cloud demonstration.

The numerical workflow deliberately remains simple and explicit:

* edit the conceptual/numerical model;
* run MODFLOW once;
* optionally run MODPATH against that stored flow solution;
* explore plan-view and cross-section postprocessing without rerunning either
  executable.
"""

from __future__ import annotations

import threading

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
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


st.set_page_config(
    page_title="MODFLOW + MODPATH Cloud Test",
    page_icon="💧",
    layout="centered",
)


@st.cache_resource
def native_run_semaphore() -> threading.BoundedSemaphore:
    """Limit native solver processes on the small Community Cloud instance."""
    return threading.BoundedSemaphore(value=2)


@st.cache_resource
def matplotlib_render_lock() -> threading.RLock:
    """Serialize Matplotlib rendering across sessions.

    Matplotlib is not fully thread-safe. A shared lock makes figure generation
    more deterministic on a multi-user Streamlit deployment and also avoids
    occasional one-frame rendering artefacts.
    """
    return threading.RLock()


TRACK_COLORS = {
    "forward": "#1f77b4",
    "backward": "#d62728",
}


def default_well_positions(nrow: int, ncol: int, count: int) -> list[tuple[int, int]]:
    """Return central default well positions (zero-based row/column)."""
    centre_row = nrow // 2
    centre_col = ncol // 2
    offsets = (0, -2, 2)
    return [(centre_row + offsets[i], centre_col) for i in range(count)]


def _show_matplotlib(fig) -> None:
    """Render a Matplotlib figure at a stable Streamlit container width."""
    st.pyplot(fig, clear_figure=True, width="stretch")
    plt.close(fig)


def plot_model_grid(params: ModelParameters):
    """Plan-view model grid with CHD boundary cells and pumping wells."""
    data = np.zeros((params.nrow, params.ncol), dtype=int)
    data[:, 0] = 1
    data[:, -1] = 1

    x = np.arange(params.ncol + 1)
    y = np.arange(params.nrow + 1)

    # A fixed canvas plus an explicit axes box aspect keeps the rendered figure
    # stable while still showing square model cells for different grid sizes.
    fig, ax = plt.subplots(figsize=(7.0, 5.1))
    fig.subplots_adjust(left=0.13, right=0.97, top=0.88, bottom=0.25)
    cmap = ListedColormap(["white", "#b9dcf5"])
    ax.pcolormesh(
        x,
        y,
        data,
        cmap=cmap,
        shading="flat",
        edgecolors="0.80",
        linewidth=0.35,
    )

    for idx, (row, col) in enumerate(params.well_positions, start=1):
        ax.plot(
            col + 0.5,
            row + 0.5,
            marker="*",
            markersize=7,
            linestyle="none",
            zorder=4,
        )
        ax.text(col + 1.0, row + 0.6, str(idx), va="center", fontsize=8, zorder=4)

    ax.set_xlim(0, params.ncol)
    ax.set_ylim(params.nrow, 0)
    ax.set_box_aspect(params.nrow / params.ncol)
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.set_title("Model grid — constant-head cells on both lateral boundaries")

    xstep = max(1, params.ncol // 10)
    ystep = max(1, params.nrow // 10)
    xindices = np.arange(0, params.ncol, xstep)
    yindices = np.arange(0, params.nrow, ystep)
    ax.set_xticks(xindices + 0.5, labels=[str(i + 1) for i in xindices])
    ax.set_yticks(yindices + 0.5, labels=[str(i + 1) for i in yindices])

    handles = [Patch(facecolor="#b9dcf5", edgecolor="0.6", label="CHD cell (all layers)")]
    if params.well_positions:
        handles.append(
            Line2D([], [], marker="*", linestyle="none", label=f"Pumping well(s), layer {WELL_LAYER + 1}")
        )
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.03), ncol=2, frameon=False)
    return fig


def _contour_levels(values: np.ndarray, dh: float) -> np.ndarray:
    finite = np.asarray(values, dtype=float)[np.isfinite(values)]
    if finite.size == 0:
        return np.array([0.0, dh])
    vmin = float(np.min(finite))
    vmax = float(np.max(finite))
    start = np.floor(vmin / dh) * dh
    stop = np.ceil(vmax / dh) * dh
    levels = np.arange(start, stop + 0.5 * dh, dh)
    if levels.size < 2:
        centre = 0.5 * (vmin + vmax)
        levels = np.array([centre - 0.5 * dh, centre + 0.5 * dh])
    return levels


def _split_masked_segments(mask: np.ndarray) -> list[np.ndarray]:
    indices = np.flatnonzero(mask)
    if indices.size == 0:
        return []
    return [segment for segment in np.split(indices, np.where(np.diff(indices) > 1)[0] + 1) if segment.size]


def _plot_layer_track_segments(ax, tracking: TrackingResult, layer: int) -> None:
    """Plot pathline portions located in the selected model layer."""
    color = TRACK_COLORS[tracking.direction]
    first_line = True
    for track in tracking.tracks:
        mask = np.asarray(track.layer) == layer
        for seg in _split_masked_segments(mask):
            if seg.size >= 2:
                ax.plot(
                    track.x[seg],
                    track.y[seg],
                    color=color,
                    linewidth=0.45,
                    alpha=0.75,
                    zorder=5,
                    label=f"{tracking.direction.capitalize()} pathlines" if first_line else None,
                )
                first_line = False
            elif seg.size == 1:
                ax.plot(
                    track.x[seg],
                    track.y[seg],
                    marker=".",
                    color=color,
                    markersize=2.0,
                    linestyle="none",
                    alpha=0.75,
                    zorder=5,
                )

    start_mask = tracking.start_layer == layer
    if np.any(start_mask):
        starts = tracking.start_xyz[start_mask]
        ax.scatter(
            starts[:, 0],
            starts[:, 1],
            s=6,
            color=color,
            linewidths=0,
            label="Particle starts",
            zorder=6,
        )


def plot_plan_view(
    head: np.ndarray,
    layer: int,
    params: ModelParameters,
    dh: float,
    color_fill: bool,
    tracking: TrackingResult | None = None,
    section_row: int | None = None,
    section_col: int | None = None,
):
    """Plot head contours with optional color fill and one tracking direction."""
    x = (np.arange(params.ncol) + 0.5) * DELR
    y = (np.arange(params.nrow) + 0.5) * DELC
    xx, yy = np.meshgrid(x, y)
    zz = np.flipud(head[layer])
    levels = _contour_levels(zz, dh)

    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    if color_fill:
        filled = ax.contourf(xx, yy, zz, levels=levels, extend="both")
        fig.colorbar(filled, ax=ax, label="Hydraulic head (m)")

    contours = ax.contour(xx, yy, zz, levels=levels, linewidths=0.75)
    ax.clabel(contours, inline=True, fontsize=8, fmt="%.2g")

    boundary_y = (np.arange(params.nrow) + 0.5) * DELC
    ax.scatter(
        np.full(params.nrow, 0.5 * DELR),
        boundary_y,
        marker="s",
        s=9,
        alpha=0.30,
        label="CHD cells",
    )
    ax.scatter(
        np.full(params.nrow, (params.ncol - 0.5) * DELR),
        boundary_y,
        marker="s",
        s=9,
        alpha=0.30,
    )

    # Mark the currently selected section traces subtly in plan view.
    if section_row is not None:
        section_y = (params.nrow - section_row - 0.5) * DELC
        ax.axhline(
            section_y, color="0.25", linewidth=0.65, linestyle="--",
            alpha=0.40, zorder=4,
        )
        ax.text(
            0.01 * params.ncol * DELR, section_y + 0.08 * DELC,
            f"row {section_row + 1}", color="0.30", fontsize=7, alpha=0.70, zorder=4,
        )
    if section_col is not None:
        section_x = (section_col + 0.5) * DELR
        ax.axvline(
            section_x, color="0.25", linewidth=0.65, linestyle=":",
            alpha=0.40, zorder=4,
        )
        ax.text(
            section_x + 0.08 * DELR, 0.985 * params.nrow * DELC,
            f"column {section_col + 1}", color="0.30", fontsize=7,
            alpha=0.70, rotation=90, va="top", zorder=4,
        )

    if tracking is not None:
        _plot_layer_track_segments(ax, tracking, layer)

    if layer == WELL_LAYER:
        for idx, (row, col) in enumerate(params.well_positions, start=1):
            well_x = (col + 0.5) * DELR
            well_y = (params.nrow - row - 0.5) * DELC
            ax.plot(
                well_x,
                well_y,
                marker="*",
                markersize=7,
                linestyle="none",
                label="Pumping well(s)" if idx == 1 else None,
                zorder=7,
            )
            ax.text(well_x + 0.50 * DELR, well_y, str(idx), fontsize=7, va="center", zorder=7)

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


def _plot_row_tracking(ax, tracking: TrackingResult, params: ModelParameters, row: int) -> None:
    """Overlay pathlines intersecting one row-cell-wide x-z section."""
    color = TRACK_COLORS[tracking.direction]
    y0 = (params.nrow - row - 1) * DELC
    y1 = (params.nrow - row) * DELC
    first_line = True
    for track in tracking.tracks:
        mask = (track.y >= y0) & (track.y <= y1)
        for seg in _split_masked_segments(mask):
            if seg.size >= 2:
                ax.plot(
                    track.x[seg],
                    track.z[seg],
                    color=color,
                    linewidth=0.45,
                    alpha=0.75,
                    zorder=6,
                    label=f"{tracking.direction.capitalize()} pathlines" if first_line else None,
                )
                first_line = False
    if tracking.start_xyz.size:
        mask = (tracking.start_xyz[:, 1] >= y0) & (tracking.start_xyz[:, 1] <= y1)
        if np.any(mask):
            starts = tracking.start_xyz[mask]
            ax.scatter(starts[:, 0], starts[:, 2], s=6, color=color, linewidths=0, zorder=7, label="Particle starts")


def _plot_column_tracking(ax, tracking: TrackingResult, params: ModelParameters, col: int) -> None:
    """Overlay pathlines intersecting one column-cell-wide y-z section."""
    color = TRACK_COLORS[tracking.direction]
    x0 = col * DELR
    x1 = (col + 1) * DELR
    first_line = True
    for track in tracking.tracks:
        mask = (track.x >= x0) & (track.x <= x1)
        for seg in _split_masked_segments(mask):
            if seg.size >= 2:
                ax.plot(
                    track.y[seg],
                    track.z[seg],
                    color=color,
                    linewidth=0.45,
                    alpha=0.75,
                    zorder=6,
                    label=f"{tracking.direction.capitalize()} pathlines" if first_line else None,
                )
                first_line = False
    if tracking.start_xyz.size:
        mask = (tracking.start_xyz[:, 0] >= x0) & (tracking.start_xyz[:, 0] <= x1)
        if np.any(mask):
            starts = tracking.start_xyz[mask]
            ax.scatter(starts[:, 1], starts[:, 2], s=6, color=color, linewidths=0, zorder=7, label="Particle starts")


def _plot_section_background(
    fig,
    ax,
    horizontal_centres: np.ndarray,
    horizontal_edges: np.ndarray,
    section_top_to_bottom: np.ndarray,
    dh: float,
    color_fill: bool,
    show_contours: bool,
    xlabel: str,
) -> None:
    """Draw cell-based head colors and optional head contours for a section."""
    # pcolormesh requires increasing z coordinates; reverse the model layers so
    # layer 3 is first (bottom) and layer 1 last (top).
    z_edges = np.array([BOTM[-1], BOTM[-2], BOTM[-3], TOP], dtype=float)
    z_centres = 0.5 * (z_edges[:-1] + z_edges[1:])
    section_bottom_to_top = section_top_to_bottom[::-1, :]

    if color_fill:
        mesh = ax.pcolormesh(
            horizontal_edges,
            z_edges,
            section_bottom_to_top,
            shading="flat",
            vmin=float(np.nanmin(section_top_to_bottom)),
            vmax=float(np.nanmax(section_top_to_bottom)),
        )
        fig.colorbar(mesh, ax=ax, label="Hydraulic head (m)")

    if show_contours:
        levels = _contour_levels(section_bottom_to_top, dh)
        contours = ax.contour(
            horizontal_centres,
            z_centres,
            section_bottom_to_top,
            levels=levels,
            linewidths=0.75,
        )
        if len(contours.levels):
            ax.clabel(contours, inline=True, fontsize=8, fmt="%.2g")

    for bottom in BOTM[:-1]:
        ax.axhline(float(bottom), linewidth=0.75, alpha=0.55)
    ax.set_ylim(float(BOTM[-1]), TOP)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Elevation z (m)")
    ax.grid(alpha=0.12)


def _plot_potentiometric_head_profiles(
    ax,
    horizontal_centres: np.ndarray,
    section_top_to_bottom: np.ndarray,
) -> None:
    """Overlay hydraulic-head profiles for all layers on a vertical section.

    The test model is confined, so these curves are potentiometric-head
    profiles rather than a true phreatic water table.  Plotting head as an
    elevation makes the pumping drawdown immediately visible, including head
    values above the physical model top.
    """
    linestyles = ("-", "--", "-.")
    for layer in range(NLAY):
        ax.plot(
            horizontal_centres,
            section_top_to_bottom[layer],
            linewidth=1.35,
            linestyle=linestyles[layer % len(linestyles)],
            zorder=5,
            label=f"Head profile L{layer + 1}",
        )

    finite = np.asarray(section_top_to_bottom, dtype=float)
    finite = finite[np.isfinite(finite)]
    head_max = float(np.max(finite)) if finite.size else TOP
    ax.set_ylim(float(BOTM[-1]), max(TOP, head_max) + 0.6)


def plot_row_cross_section(
    head: np.ndarray,
    params: ModelParameters,
    row: int,
    dh: float,
    color_fill: bool,
    show_contours: bool,
    tracking: TrackingResult | None,
):
    """Vertical x-z cross section through a user-selected model row."""
    x_centres = (np.arange(params.ncol) + 0.5) * DELR
    x_edges = np.arange(params.ncol + 1) * DELR
    section = head[:, row, :]

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    _plot_section_background(
        fig,
        ax,
        x_centres,
        x_edges,
        section,
        dh,
        color_fill,
        show_contours,
        "x (m)",
    )
    _plot_potentiometric_head_profiles(ax, x_centres, section)

    for idx, (well_row, well_col) in enumerate(params.well_positions, start=1):
        if well_row == row:
            x = (well_col + 0.5) * DELR
            layer_top = TOP if WELL_LAYER == 0 else BOTM[WELL_LAYER - 1]
            z = 0.5 * (layer_top + BOTM[WELL_LAYER])
            ax.plot(x, z, marker="*", markersize=9, linestyle="none", zorder=8, label="Pumping well(s)" if idx == 1 else None)
            ax.text(x + 0.15 * DELR, z, str(idx), fontsize=8, va="center", zorder=8)

    if tracking is not None:
        _plot_row_tracking(ax, tracking, params, row)

    ax.set_xlim(0.0, params.ncol * DELR)
    ax.set_title(f"Cross section along row {row + 1}")
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(loc="best")
    fig.tight_layout()
    return fig


def plot_column_cross_section(
    head: np.ndarray,
    params: ModelParameters,
    col: int,
    dh: float,
    color_fill: bool,
    show_contours: bool,
    tracking: TrackingResult | None,
):
    """Vertical y-z cross section through a user-selected model column."""
    y_centres = (np.arange(params.nrow) + 0.5) * DELC
    y_edges = np.arange(params.nrow + 1) * DELC
    # Model row 0 is at the upper side of the plan view; reverse rows so the
    # section horizontal coordinate increases from y=0 to y=max.
    section = head[:, ::-1, col]

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    _plot_section_background(
        fig,
        ax,
        y_centres,
        y_edges,
        section,
        dh,
        color_fill,
        show_contours,
        "y (m)",
    )
    _plot_potentiometric_head_profiles(ax, y_centres, section)

    for idx, (well_row, well_col) in enumerate(params.well_positions, start=1):
        if well_col == col:
            y = (params.nrow - well_row - 0.5) * DELC
            layer_top = TOP if WELL_LAYER == 0 else BOTM[WELL_LAYER - 1]
            z = 0.5 * (layer_top + BOTM[WELL_LAYER])
            ax.plot(y, z, marker="*", markersize=9, linestyle="none", zorder=8, label="Pumping well(s)" if idx == 1 else None)
            ax.text(y + 0.15 * DELC, z, str(idx), fontsize=8, va="center", zorder=8)

    if tracking is not None:
        _plot_column_tracking(ax, tracking, params, col)

    ax.set_xlim(0.0, params.nrow * DELC)
    ax.set_title(f"Cross section along column {col + 1}")
    handles, labels = ax.get_legend_handles_labels()
    if handles:
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
    """Plot the parsed cumulative MODFLOW budget components.

    Only package-specific ``*_IN`` and ``*_OUT`` terms are plotted.  Aggregate
    ``TOTAL_*`` fields are deliberately excluded from the bars.  The MODFLOW
    ``IN-OUT`` balance error and percent discrepancy are shown numerically.

    The normalizer accepts both ordinary names (``CHD_IN``) and the literal
    byte-string representations occasionally returned through some
    FloPy/Numpy combinations (``b'CHD_IN'``).
    """
    st.markdown("#### Cumulative mass balance")
    st.caption(
        "The final cumulative MODFLOW 6 listing-file budget is shown below. "
        "Package-specific inflow/outflow terms are plotted directly; aggregate "
        "TOTAL terms are omitted. The stress period is one day."
    )
    if not items:
        st.info("No cumulative external budget could be read from the MODFLOW outputs.")
        return

    def normalise(name: object) -> str:
        if isinstance(name, (bytes, np.bytes_)):
            text = name.decode("ascii", errors="replace")
        else:
            text = str(name)
        text = text.replace("\x00", "").strip().rstrip(":")
        if (
            len(text) >= 3
            and text[0] in {"b", "B"}
            and text[1] in {"'", '"'}
            and text[-1] == text[1]
        ):
            text = text[2:-1]
        return text.strip().upper().replace(" ", "_")

    # Keep every parsed value, including zero-valued package terms.  This means
    # the bar plot corresponds directly to the MODFLOW cumulative-budget table.
    normalized_items = [(normalise(name), float(value)) for name, value in items]
    values = {name: value for name, value in normalized_items}

    components: list[tuple[str, float]] = []
    for key, value in normalized_items:
        if key.startswith("TOTAL_"):
            continue
        if key.endswith("_IN") or key.endswith("_OUT"):
            components.append((key.replace("_", " ").title(), value))

    balance_error = values.get("IN-OUT", values.get("IN_OUT"))
    discrepancy = next(
        (value for key, value in values.items() if "PERCENT" in key and "DISCREP" in key),
        None,
    )

    # Defensive derivation for nonstandard listings.  The standard MF6 listing
    # already provides IN-OUT and PERCENT_DISCREPANCY, as seen in the diagnostic
    # output from the deployed test app.
    if balance_error is None and components:
        balance_error = float(sum(value for _label, value in components))
    if discrepancy is None and components:
        total_in = sum(value for label, value in components if label.upper().endswith(" IN"))
        total_out_abs = sum(abs(value) for label, value in components if label.upper().endswith(" OUT"))
        denominator = 0.5 * (total_in + total_out_abs)
        discrepancy = 100.0 * float(balance_error) / denominator if denominator > 0.0 else 0.0

    if components:
        labels = [label for label, _ in components]
        bar_values = np.asarray([value for _, value in components], dtype=float)

        fig, ax = plt.subplots(figsize=(7.0, 4.0))
        bars = ax.bar(labels, bar_values)
        ax.axhline(0.0, color="0.25", linewidth=0.8)
        ax.set_ylabel("Cumulative volume (m³)")
        ax.set_title("MODFLOW cumulative water budget")
        ax.tick_params(axis="x", rotation=25)
        ax.grid(axis="y", alpha=0.20)

        scale = max(float(np.max(np.abs(bar_values))), 1.0)
        for bar, value in zip(bars, bar_values):
            # Put labels just above positive bars and just below negative bars.
            # Zero-valued terms remain visible numerically even though the bar
            # itself has no height.
            offset = 0.025 * scale if value >= 0.0 else -0.025 * scale
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                value + offset,
                f"{value:,.4g}",
                ha="center",
                va="bottom" if value >= 0.0 else "top",
                fontsize=8,
            )
        fig.tight_layout()
        with matplotlib_render_lock():
            _show_matplotlib(fig)
    else:
        st.info("No package-specific *_IN or *_OUT terms were present in the parsed budget.")

    error_text = "not available" if balance_error is None else f"{float(balance_error):,.6g} m³"
    discrepancy_text = "not available" if discrepancy is None else f"{float(discrepancy):,.6g} %"
    st.markdown(
        f"**Balance error (IN − OUT):** {error_text}  \n"
        f"**Percent discrepancy:** {discrepancy_text}"
    )


# =============================================================================
# User interface
# =============================================================================

st.title("💧 MODFLOW 6 + MODPATH 7 Cloud Test")
st.write(
    "This compact example demonstrates how a native MODFLOW 6 groundwater model and "
    "MODPATH 7 particle tracking can run directly inside Streamlit Community Cloud. "
    "Define the three-layer flow model, inspect the grid, run MODFLOW, and then "
    "optionally run MODPATH without recalculating the flow solution."
)
st.info(
    "The model is intentionally idealized: specified heads are applied along the two "
    "lateral boundaries, one to three wells pump from layer 3, and all cells are "
    "100 × 100 m. Changing a model parameter clears old numerical results; changing "
    "only postprocessing options does not rerun MODFLOW or MODPATH."
)

# -----------------------------------------------------------------------------
# Model inputs
# -----------------------------------------------------------------------------
st.subheader("Model design")

with st.expander("General model parameters", expanded=True):
    g1, g2 = st.columns(2)
    with g1:
        nrow = st.slider(
            "Number of rows",
            min_value=9,
            max_value=61,
            value=DEFAULT_NROW,
            step=2,
            help="Odd values keep an unambiguous central row.",
        )
        head_left = st.number_input(
            "Left specified head (m)",
            min_value=0.0,
            max_value=100.0,
            value=32.0,
            step=0.5,
        )
        k_layer1 = st.number_input(
            "K layer 1 (m/day)", min_value=0.001, max_value=1000.0, value=10.0, format="%.3f"
        )
        k_layer2 = st.number_input(
            "K layer 2 (m/day)", min_value=0.001, max_value=1000.0, value=0.10, format="%.3f"
        )
        k_layer3 = st.number_input(
            "K layer 3 (m/day)", min_value=0.001, max_value=1000.0, value=5.0, format="%.3f"
        )
    with g2:
        ncol = st.slider(
            "Number of columns",
            min_value=9,
            max_value=61,
            value=DEFAULT_NCOL,
            step=2,
            help="Odd values keep an unambiguous central column.",
        )
        head_right = st.number_input(
            "Right specified head (m)",
            min_value=0.0,
            max_value=100.0,
            value=31.0,
            step=0.5,
        )

        vertical_anisotropy = st.number_input(
            "Vertical anisotropy Kz/Kx (-)",
            min_value=0.001,
            max_value=1.0,
            value=0.10,
            format="%.3f",
        )
    st.caption(
        f"The model retains three layers; every cell is {DELR:.0f} × {DELC:.0f} m. "
        f"All pumping wells are screened in layer {WELL_LAYER + 1}."
    )

with st.expander("Pumping-well parameters", expanded=True):
    number_wells = st.slider("Number of pumping wells", min_value=1, max_value=3, value=1, step=1)
    st.caption(
        "Each well has an independent row, column, pumping rate, and backward-particle "
        "count. Pumping rates are positive extraction magnitudes; particle counts affect "
        "MODPATH only."
    )

    defaults = default_well_positions(nrow, ncol, number_wells)
    well_positions: list[tuple[int, int]] = []
    pumping_rates: list[float] = []
    backward_particle_counts: list[int] = []
    well_cols = st.columns(number_wells)
    for i in range(number_wells):
        default_row, default_col = defaults[i]
        with well_cols[i]:
            st.markdown(f"**Well {i + 1}**")
            row_1based = st.number_input(
                "Row",
                min_value=1,
                max_value=nrow,
                value=default_row + 1,
                step=1,
                key=f"well_row_{i}_{nrow}_{ncol}",
            )
            col_1based = st.number_input(
                "Column",
                min_value=2,
                max_value=ncol - 1,
                value=default_col + 1,
                step=1,
                key=f"well_col_{i}_{nrow}_{ncol}",
                help="Boundary columns are reserved for specified-head cells.",
            )
            rate = st.number_input(
                "Pumping rate (m³/day)",
                min_value=0.0,
                max_value=800.0,
                value=300.0,
                step=50.0,
                key=f"well_rate_{i}",
                help="MODFLOW receives the corresponding negative WEL flux.",
            )
            particle_count = st.number_input(
                "Backward particles",
                min_value=10,
                max_value=500,
                value=PARTICLES_PER_WELL,
                step=10,
                key=f"well_particles_{i}",
                help=(
                    "Number of particles released throughout this pumping cell "
                    "for backward MODPATH tracking. Changing this value does not "
                    "require rerunning MODFLOW."
                ),
            )
            well_positions.append((int(row_1based) - 1, int(col_1based) - 1))
            pumping_rates.append(float(rate))
            backward_particle_counts.append(int(particle_count))

params = ModelParameters(
    head_left=float(head_left),
    head_right=float(head_right),
    pumping_rates=tuple(pumping_rates),
    k_layer1=float(k_layer1),
    k_layer2=float(k_layer2),
    k_layer3=float(k_layer3),
    vertical_anisotropy=float(vertical_anisotropy),
    nrow=int(nrow),
    ncol=int(ncol),
    well_positions=tuple(well_positions),
)

has_duplicate_wells = len(set(well_positions)) != len(well_positions)
if has_duplicate_wells:
    st.error("Two or more wells occupy the same cell. Choose unique well positions before running MODFLOW.")

with matplotlib_render_lock():
    _show_matplotlib(plot_model_grid(params))

backward_total = int(sum(backward_particle_counts))
backward_detail = ", ".join(
    f"W{i + 1}: {count}" for i, count in enumerate(backward_particle_counts)
)
st.caption(
    f"Backward tracking will use {backward_total} particles ({backward_detail}). "
    f"Forward tracking will use {params.forward_particle_count} particles "
    "(one per CHD cell)."
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
            "Effective porosity (-)",
            min_value=0.01,
            max_value=0.60,
            value=0.25,
            step=0.05,
            format="%.2f",
            help="Controls particle velocity/travel time but not the steady-flow head solution.",
        )
    current_modpath_signature = (
        st.session_state.flow_signature,
        float(effective_porosity),
        tuple(backward_particle_counts),
    )
    if "modpath_signature" in st.session_state and st.session_state.modpath_signature != current_modpath_signature:
        st.session_state.pop("modpath_result", None)
        st.session_state.pop("modpath_signature", None)
        st.info(
            "Effective porosity or backward-particle counts changed. "
            "MODFLOW remains valid; rerun MODPATH only."
        )
    with mp2:
        st.write("")
        st.write("")
        run_mp7_clicked = st.button("Run MODPATH", type="primary")
    if run_mp7_clicked:
        try:
            with st.spinner("Running backward and forward MODPATH 7 tracking..."):
                with native_run_semaphore():
                    mp_result = run_modpath(
                        st.session_state.flow_result,
                        effective_porosity=float(effective_porosity),
                        backward_particle_counts=tuple(backward_particle_counts),
                    )
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
    well_text = ", ".join(
        f"W{i + 1}: {h:.3f} m (Q = {rate:.0f} m³/day)"
        for i, (h, rate) in enumerate(zip(well_heads, result_params.pumping_rates))
    )
    st.markdown(
        f"**MODFLOW:** `{flow_result.mf6_version}`  \n"
        f"Runtime: **{flow_result.runtime_seconds:.3f} s**  \n"
        f"Head at pumping cell(s): **{well_text}**  \n"
        f"Minimum / maximum simulated head: **{np.min(head):.3f} / {np.max(head):.3f} m**"
    )

    selected_tracking: TrackingResult | None = None
    if "modpath_result" in st.session_state:
        p1, p2, p3, p4 = st.columns([1, 1, 1, 1.7])
    else:
        p1, p2, p3 = st.columns(3)
        p4 = None

    with p1:
        display_layer = st.selectbox(
            "Head layer",
            options=list(range(NLAY)),
            format_func=lambda i: f"Layer {i + 1}",
            index=WELL_LAYER,
        )
    with p2:
        contour_interval = st.number_input(
            "Contour interval Δh (m)",
            min_value=0.01,
            max_value=20.0,
            value=1.0,
            step=0.25,
            format="%.2f",
        )
    with p3:
        color_fill = st.toggle("Color fill", value=True)

    if p4 is not None:
        with p4:
            particle_display = st.radio(
                "Particles / pathlines",
                ["No particles", "Forward", "Backward"],
                horizontal=True,
            )
        mp_result = st.session_state.modpath_result
        if particle_display == "Forward":
            selected_tracking = mp_result.forward
        elif particle_display == "Backward":
            selected_tracking = mp_result.backward

    # Resolve cross-section locations before the plan plot is rendered.  The
    # actual widgets remain in the cross-section expander below; Streamlit
    # session state lets the selected traces be shown in plan view immediately.
    section_row_key = f"section_row_{result_params.nrow}_{result_params.ncol}"
    section_col_key = f"section_col_{result_params.nrow}_{result_params.ncol}"
    default_section_row = result_params.well_positions[0][0] + 1
    default_section_col = result_params.well_positions[0][1] + 1
    section_row_for_plot = int(st.session_state.get(section_row_key, default_section_row)) - 1
    section_col_for_plot = int(st.session_state.get(section_col_key, default_section_col)) - 1

    # Plan view first, full-width in the centered page.
    with matplotlib_render_lock():
        _show_matplotlib(
            plot_plan_view(
                head,
                display_layer,
                result_params,
                float(contour_interval),
                bool(color_fill),
                selected_tracking,
                section_row=section_row_for_plot,
                section_col=section_col_for_plot,
            )
        )

    if selected_tracking is not None:
        st.caption(
            f"{selected_tracking.direction.capitalize()} tracking: "
            f"{selected_tracking.requested_particles} released particles and "
            f"{selected_tracking.pathline_count} pathline records. In plan view only "
            "the portions located in the selected layer are drawn."
        )

    # Cross sections are intentionally below the plan view and kept in an
    # expander so the default result page remains compact.
    with st.expander("Cross sections", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            section_row = st.number_input(
                "Cross-section row",
                min_value=1,
                max_value=result_params.nrow,
                value=default_section_row,
                step=1,
                key=section_row_key,
            )
        with c2:
            section_col = st.number_input(
                "Cross-section column",
                min_value=1,
                max_value=result_params.ncol,
                value=default_section_col,
                step=1,
                key=section_col_key,
            )

        c3, c4 = st.columns(2)
        with c3:
            cross_fill = st.toggle("Color fill in cross sections", value=True)
        with c4:
            cross_contours = st.toggle(
                "Head contour lines in cross sections",
                value=True,
                help="Uses the same Δh selected for the plan-view contours.",
            )

        st.caption(
            "The vertical scale is exaggerated so the three 10-m-thick layers are visible. "
            "The three line profiles show potentiometric head in layers 1–3; because this "
            "test model is confined they are not a true phreatic water table. When pathlines "
            "are selected above, only portions intersecting the selected row or column cell "
            "are shown."
        )

        with matplotlib_render_lock():
            _show_matplotlib(
                plot_row_cross_section(
                    head,
                    result_params,
                    int(section_row) - 1,
                    float(contour_interval),
                    bool(cross_fill),
                    bool(cross_contours),
                    selected_tracking,
                )
            )
        with matplotlib_render_lock():
            _show_matplotlib(
                plot_column_cross_section(
                    head,
                    result_params,
                    int(section_col) - 1,
                    float(contour_interval),
                    bool(cross_fill),
                    bool(cross_contours),
                    selected_tracking,
                )
            )

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
        mf6_path = locate_mf6()
        mf6_version = get_mf6_version(mf6_path)
        st.write(f"MODFLOW executable: `{mf6_path}`")
        st.write(f"MODFLOW version check: `{mf6_version}`")
        st.success("MODFLOW 6 is available to the Streamlit process.")
    except Exception as exc:
        st.error("MODFLOW 6 executable is not available.")
        st.exception(exc)
    try:
        mp7_path = locate_mp7()
        st.write(f"MODPATH executable: `{mp7_path}`")
        st.success("MODPATH 7 is available to the Streamlit process.")
    except Exception as exc:
        st.error("MODPATH 7 executable is not available.")
        st.exception(exc)
