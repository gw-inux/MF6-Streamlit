"""Spatial presentation following the MODFLOW Solver Lab conventions.

Plot coordinates start at the first cell centre, as in the Solver Lab. This
is a display translation only: model coordinates, locations and heads stay
unchanged. All input arrays are read-only to these functions.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection
from matplotlib.colors import BoundaryNorm, ListedColormap, Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from matplotlib.ticker import MaxNLocator

from .analytical import steady_profile
from .config import ENGINES
from .comparisons import surface_difference
from .outputs import clean_heads, groundwater_surface
from .plot_style import (
    ENGINE_COLORS,
    ENGINE_MARKERS,
    ANALYTICAL_GREEN,
    BLUE,
    CHD_BLUE,
    CHD_FILL,
    DRY_RED,
    PREVIOUS_BLUE,
    SECTION_COLOR,
    WELL_RED,
    display_indices,
    themed,
)


def _edges(count, size):
    return (np.arange(count + 1) - 0.5) * size


def _slice(values, axis, index):
    return values[..., index, :] if axis == "x" else values[..., :, index]


def head_profile(s, heads, axis, index, surface=True, layer=0):
    """Select the uppermost wet head or a native layer without interpolation."""
    field = groundwater_surface(s, heads) if surface else clean_heads(s, heads)[layer]
    return _slice(field, axis, index)


def _map_grid(ax, x, y):
    ax.vlines(
        x[display_indices(len(x))],
        y[0],
        y[-1],
        color="#4E6574",
        lw=0.55,
        alpha=0.8,
        zorder=4,
    )
    ax.hlines(
        y[display_indices(len(y))],
        x[0],
        x[-1],
        color="#4E6574",
        lw=0.55,
        alpha=0.8,
        zorder=4,
    )


def _map_markers(ax, s, t, axis, index):
    d = s.cell_size
    if s.well_enabled:
        for well in s.wells:
            ax.scatter(
                well.col * d,
                well.row * d,
                marker="v",
                s=65,
                color=WELL_RED,
                edgecolor="white",
                zorder=7,
            )
            if len(s.wells) > 1:
                ax.annotate(
                    well.name,
                    (well.col * d, well.row * d),
                    xytext=(5, -14),
                    textcoords="offset points",
                    fontsize=8,
                    zorder=8,
                    bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=1),
                )
    for obs in s.observations:
        ax.scatter(
            obs.col * d, obs.row * d, s=22, color="#24364B", edgecolor="white", zorder=7
        )
        ax.annotate(
            obs.name,
            (obs.col * d, obs.row * d),
            xytext=(6, 7),
            textcoords="offset points",
            fontsize=8,
            zorder=8,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=1),
        )
    trace = (
        ax.axhline(index * d, color=SECTION_COLOR, ls="--", lw=1.2, zorder=6)
        if axis == "x"
        else ax.axvline(index * d, color=SECTION_COLOR, ls="--", lw=1.2, zorder=6)
    )
    trace.set_gid("section_trace")


def _map_legend(ax, s, t, dry=False):
    handles = [
        Patch(facecolor=CHD_FILL, edgecolor=CHD_BLUE, label=t["chd"]),
        Line2D([], [], color=SECTION_COLOR, ls="--", label=t["section"]),
    ]
    if s.well_enabled:
        handles.append(
            Line2D([], [], marker="v", ls="", color=WELL_RED, label=t["well"])
        )
    if dry:
        handles.append(Patch(facecolor=DRY_RED, alpha=0.4, label=t["dry_inactive"]))
    ax.legend(handles=handles, loc="upper left", fontsize=8, framealpha=0.96)


def _masked_cells(ax, xedges, yedges, mask):
    """Transparent pale-red overlay, including entirely dry fields."""
    if np.any(mask):
        field = np.where(mask, 1.0, np.nan)
        mesh = ax.pcolormesh(
            xedges,
            yedges,
            field,
            cmap=ListedColormap([DRY_RED]),
            vmin=0,
            vmax=1,
            alpha=0.4,
            rasterized=True,
            zorder=2,
        )
        mesh.set_gid("dry_inactive_cells")


@themed
def model_preview(s, t, quantity="empty", layer=0, row=None):
    """Aligned plan and vertical section; true equal-scale plan geometry."""
    row = s.nrow // 2 if row is None else row
    x, y = _edges(s.ncol, s.cell_size), _edges(s.nrow, s.cell_size)
    z = np.r_[s.top, s.botm]
    # Cap physical plot height for very elongated grids without distorting x/y.
    width = min(6.21, 8.0 * s.ncol / s.nrow)
    plan_height = width * s.nrow / s.ncol
    height = 0.65 + 2.25 + 0.85 + plan_height + 0.55
    fig = plt.figure(figsize=(9, height))
    left, panel_width = 0.10, width / 9
    plan = fig.add_axes([left, 3.75 / height, panel_width, plan_height / height])
    section = fig.add_axes([left, 0.65 / height, panel_width, 2.25 / height])
    active = s.active_mask()
    field = norm = cmap = mesh = None
    if quantity == "k":
        field = np.where(active, s.k_field(), np.nan)
        levels = np.unique(field[np.isfinite(field)])
        if s.random_k and s.k_min < s.k_max:
            # Display classes only; the native random K field remains continuous.
            bounds = np.geomspace(s.k_min, s.k_max, min(s.k_zones, 12) + 1)
            levels = np.sqrt(bounds[:-1] * bounds[1:])
        else:
            bounds = (
                np.r_[
                    levels[0] / 1.1, np.sqrt(levels[:-1] * levels[1:]), levels[-1] * 1.1
                ]
                if len(levels) > 1
                else np.array([levels[0] / 1.1, levels[0] * 1.1])
            )
        cmap = plt.get_cmap("YlGnBu", len(levels))
        norm = BoundaryNorm(bounds, cmap.N)
    elif quantity == "initial":
        field = clean_heads(s, s.starting_heads())
        finite = field[np.isfinite(field)]
        lo, hi = (finite.min(), finite.max()) if finite.size else (0, 1)
        norm = Normalize(lo - 0.1 if lo == hi else lo, hi + 0.1 if lo == hi else hi)
        cmap = "Blues"
    if field is not None:
        mesh = plan.pcolormesh(
            x, y, field[layer], norm=norm, cmap=cmap, rasterized=True
        )
        section.pcolormesh(x, z, field[:, row], norm=norm, cmap=cmap, rasterized=True)
    _masked_cells(
        plan, x, y, ~active[layer] if field is None else ~np.isfinite(field[layer])
    )
    _masked_cells(
        section, x, z, ~active[:, row] if field is None else ~np.isfinite(field[:, row])
    )
    _map_grid(plan, x, y)
    section.vlines(
        x[display_indices(len(x))],
        s.bottom,
        s.top,
        color="#4E6574",
        lw=0.55,
        alpha=0.8,
        zorder=4,
    )
    section.hlines(z, x[0], x[-1], color="#4E6574", lw=0.65, alpha=0.8, zorder=4)
    chd = s.chd_mask()
    for col in (0, s.ncol - 1):
        if chd[layer, :, col].any():
            plan.add_patch(
                Rectangle(
                    (x[col], y[0]),
                    s.cell_size,
                    y[-1] - y[0],
                    facecolor=CHD_FILL,
                    edgecolor=CHD_BLUE,
                    zorder=3,
                )
            )
        for k in range(s.nlay):
            if chd[k, row, col]:
                section.add_patch(
                    Rectangle(
                        (x[col], z[k + 1]),
                        s.cell_size,
                        z[k] - z[k + 1],
                        facecolor=CHD_FILL,
                        edgecolor=CHD_BLUE,
                        zorder=3,
                    )
                )
    _map_markers(plan, s, t, "x", row)
    _map_legend(plan, s, t, not active[layer].all())
    if s.well_enabled:
        for well in s.wells:
            if well.row == row:
                section.plot(
                    [well.col * s.cell_size] * 2,
                    [s.bottom, s.top],
                    color=WELL_RED,
                    lw=2,
                    zorder=5,
                )
    for obs in s.observations:
        if obs.row == row:
            section.plot(
                obs.col * s.cell_size,
                (s.layer_tops[obs.layer] + s.botm[obs.layer]) / 2,
                "o",
                ms=4,
                color="#24364B",
                zorder=6,
            )
    if s.recharge > 0:
        for position in np.linspace(
            x[0] + 0.15 * (x[-1] - x[0]), x[0] + 0.85 * (x[-1] - x[0]), 5
        ):
            section.annotate(
                "",
                xy=(position, s.top - 0.13 * s.thickness),
                xytext=(position, s.top),
                arrowprops=dict(arrowstyle="->", color=BLUE),
                zorder=6,
            )
    plan.set(
        xlim=(x[0], x[-1]),
        ylim=(y[0], y[-1]),
        xlabel=t["x_m"],
        ylabel=t["y_m"],
        title=t["preview_plan"].format(layer=layer + 1, nx=s.ncol, ny=s.nrow),
    )
    plan.set_aspect("equal", adjustable="box")
    section.set(
        xlim=(x[0], x[-1]),
        ylim=(s.bottom, s.top),
        xlabel=t["x_m"],
        ylabel=t["elevation_m"],
        title=t["preview_section"].format(row=row + 1, layers=s.nlay),
    )
    for ax in (plan, section):
        ax.title.set_color(BLUE)
    if mesh is not None:
        cax = fig.add_axes(
            [left + panel_width + 0.035, 0.65 / height, 0.025, (height - 1.2) / height]
        )
        bar = fig.colorbar(
            mesh,
            cax=cax,
            label=(t["random_k_legend"] if s.random_k else t["k_zone_legend"])
            if quantity == "k"
            else t["head_m"],
            **(
                dict(
                    ticks=(bounds[:-1] + bounds[1:]) / 2,
                    spacing="uniform",
                    drawedges=True,
                )
                if quantity == "k"
                else {}
            ),
        )
        if quantity == "k":
            bar.ax.set_yticklabels([f"{v:.2e}" for v in levels], fontsize=8)
    return fig


@themed
def top_view(
    s, t, heads=None, section_axis="x", section_index=None, *, show_contours=False
):
    """Computed water table/potentiometric surface using uppermost wet heads."""
    if heads is None:
        return model_preview(s, t)
    index = (
        section_index
        if section_index is not None
        else (s.nrow // 2 if section_axis == "x" else s.ncol // 2)
    )
    x, y = _edges(s.ncol, s.cell_size), _edges(s.nrow, s.cell_size)
    fig, ax = plt.subplots(figsize=(8, 6.4), layout="constrained")
    field = groundwater_surface(s, heads)
    if np.isfinite(field).any():
        finite = field[np.isfinite(field)]
        lo, hi = finite.min(), finite.max()
        norm = Normalize(lo - 0.1 if lo == hi else lo, hi + 0.1 if lo == hi else hi)
        mesh = ax.pcolormesh(x, y, field, norm=norm, cmap="Blues", rasterized=True)
        mesh.set_gid("groundwater_surface")
        fig.colorbar(mesh, ax=ax, shrink=0.85, label=t["head_m"])
        if show_contours and np.nanmax(field) - np.nanmin(field) > 1e-6:
            contours = ax.contour(
                np.arange(s.ncol) * s.cell_size,
                np.arange(s.nrow) * s.cell_size,
                field,
                levels=7,
                colors="#245372",
                linewidths=0.5,
                alpha=0.65,
            )
            labels = ax.clabel(contours, fontsize=7, fmt="%.1f")
            for label in labels:
                label.set_bbox(
                    dict(facecolor="white", edgecolor="none", alpha=0.8, pad=1)
                )
    else:
        ax.text(
            0.5,
            0.5,
            t["no_wet_heads"],
            transform=ax.transAxes,
            ha="center",
            va="center",
        )
    _masked_cells(ax, x, y, ~np.isfinite(field))
    _map_grid(ax, x, y)
    for col in (0, s.ncol - 1):
        if s.chd_mask()[:, :, col].any():
            ax.add_patch(
                Rectangle(
                    (x[col], y[0]),
                    s.cell_size,
                    y[-1] - y[0],
                    facecolor="none",
                    edgecolor=CHD_BLUE,
                    lw=1.8,
                    zorder=5,
                )
            )
    _map_markers(ax, s, t, section_axis, index)
    _map_legend(ax, s, t, not np.isfinite(field).all())
    ax.set(
        xlim=(x[0], x[-1]),
        ylim=(y[0], y[-1]),
        xlabel=t["x_m"],
        ylabel=t["y_m"],
        title=t["potentiometric"] if s.confined else t["water_surface"],
    )
    ax.set_aspect("equal")
    ax.title.set_color(BLUE)
    return fig


def _dry_appearance(engine):
    """Dry solver cells differ from cells excluded from the input domain."""
    if engine == "mf2005":
        return "#F5D38A", "#B45B58", "xx", "dry_inactive_solver"
    if engine == "mfnwt":
        return DRY_RED, "#8D9AA5", None, "dry_active_solver"
    return DRY_RED, "#8D9AA5", None, "dry_cells_label"


def _cell_filling(ax, s, section_heads, active, faces, engine=None):
    """Shade each real layer independently; never fill through a dry layer."""
    for k, (bottom, top) in enumerate(zip(s.botm, s.layer_tops, strict=True)):
        rectangles = []
        for j in range(section_heads.shape[-1]):
            if not active[k, j] or not np.isfinite(section_heads[k, j]):
                patch = Rectangle(
                    (faces[j], bottom),
                    1,
                    top - bottom,
                    facecolor="#CCD3D9"
                    if not active[k, j]
                    else _dry_appearance(engine)[0],
                    alpha=0.4,
                    edgecolor="#8D9AA5"
                    if not active[k, j]
                    else _dry_appearance(engine)[1],
                    linewidth=0.4,
                    hatch="//" if not active[k, j] else _dry_appearance(engine)[2],
                    zorder=1,
                )
                patch.set_gid("inactive_cell" if not active[k, j] else "dry_cell")
                ax.add_patch(patch)
            else:
                wet = top if s.confined else np.clip(section_heads[k, j], bottom, top)
                rectangles.append(
                    [
                        (faces[j], bottom),
                        (faces[j + 1], bottom),
                        (faces[j + 1], wet),
                        (faces[j], wet),
                    ]
                )
        filling = PolyCollection(
            rectangles, facecolors="#B9DEF1", edgecolors="none", alpha=0.7, zorder=1
        )
        filling.set_gid("wetted_cells")
        ax.add_collection(filling)


def _status_box(ax, s, result, t):
    cfg = result["solver"]
    method = (
        "PCG"
        if cfg.engine == "mf2005"
        else (
            ("GMRES" if cfg.nwt_method == 1 else "XMD")
            if cfg.engine == "mfnwt"
            else "IMS"
        )
    )
    lines = [
        f"{ENGINES[cfg.engine]} · {method}",
        t["aquifer_confined" if s.confined else "aquifer_convertible"],
        t["status_closure"].format(head=cfg.head_close, flow=cfg.flow_close),
        t["status_limits"].format(outer=cfg.outer, inner=cfg.inner),
        t["converged"],
        t["status_iterations"].format(
            outer=(result.get("outer") if result.get("outer") is not None else "—"),
            inner=(result.get("inner") if result.get("inner") is not None else "—"),
        ),
        t["status_runtime"].format(seconds=result["wall_seconds"]),
    ]
    status = ax.text(
        0.98,
        0.97,
        "\n".join(lines),
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8,
        color=BLUE,
        bbox=dict(
            boxstyle="round,pad=.45",
            facecolor="#F1F6FC",
            edgecolor="#5489B5",
            alpha=0.96,
        ),
    )
    status.set_gid("solver_status")


@themed
def cross_section(
    s,
    heads,
    t,
    axis="x",
    index=None,
    analytical=False,
    *,
    initial_heads=None,
    cell_heads=True,
    cell_lines=True,
    previous_profile=None,
    surface=True,
    layer=0,
    result=None,
    show_status=True,
    engine_profiles=(),
):
    """Cell-centred dots and independent horizontal segments, as in Solver Lab."""
    index = (s.nrow // 2 if axis == "x" else s.ncol // 2) if index is None else index
    n = s.ncol if axis == "x" else s.nrow
    centres, faces = np.arange(1, n + 1), np.arange(n + 1) + 0.5
    clean = clean_heads(s, heads)
    section = _slice(clean, axis, index)
    active = _slice(s.active_mask(), axis, index)
    line = head_profile(s, clean, axis, index, surface, layer)
    fig, ax = plt.subplots(figsize=(9, 5.6), layout="constrained")
    domain = Rectangle(
        (0.5, s.bottom), n, s.thickness, facecolor="#F0EEE7", edgecolor="none", zorder=0
    )
    domain.set_gid("model_domain")
    ax.add_patch(domain)
    engine = result["solver"].engine if result is not None else None
    _cell_filling(ax, s, section, active, faces, engine)
    visible_faces = faces[display_indices(n + 1)]
    grid = ax.vlines(
        visible_faces, s.bottom, s.top, color="#7A858C", lw=0.65, alpha=0.8, zorder=2
    )
    grid.set_gid("model_grid_faces")
    ax.hlines(np.r_[s.top, s.botm], 0.5, n + 0.5, color="#8C7859", lw=0.65, zorder=3.5)
    values = [np.array([s.bottom, s.top]), line]
    nodes = display_indices(n)
    engine = result["solver"].engine if result is not None else None
    color = ENGINE_COLORS[engine] if engine else BLUE
    identity = " · " + ENGINES[engine] if engine else ""
    if cell_lines:
        segments = ax.hlines(
            line,
            faces[:-1],
            faces[1:],
            color=color,
            lw=0.7,
            label=t["cell_head_lines"] + identity,
            zorder=4,
        )
        segments.set_gid("cell_head_lines")
    if cell_heads:
        (dots,) = ax.plot(
            centres[nodes],
            line[nodes],
            "o",
            ms=3.5,
            color=color,
            label=t["cell_head_dots"] + identity,
            zorder=7,
        )
        dots.set_gid("cell_head_dots")
    if initial_heads is not None:
        initial = head_profile(s, initial_heads, axis, index, surface, layer)
        ax.plot(
            centres, initial, "--", color="#7B8795", lw=1.2, label=t["initial_heads"]
        )
        values.append(initial)
    if analytical and axis == "x":
        x, reference = steady_profile(s)
        # steady_profile uses the original outer-face coordinate convention.
        ax.plot(
            x / s.cell_size + 0.5,
            reference,
            color=ANALYTICAL_GREEN,
            lw=0.9,
            label=t["analytical"],
        )
        values.append(reference)
    if previous_profile is not None:
        old = np.asarray(previous_profile)
        (symbols,) = ax.plot(
            centres[nodes],
            old[nodes],
            ls="none",
            marker="o",
            ms=6.5,
            markerfacecolor="none",
            markeredgecolor=PREVIOUS_BLUE,
            markeredgewidth=1,
            label=t["previous"],
            zorder=6,
        )
        symbols.set_gid("previous_heads")
        values.append(old)
    for offset, (other_engine, other_profile) in enumerate(engine_profiles):
        (symbols,) = ax.plot(
            centres[nodes],
            np.asarray(other_profile)[nodes],
            linestyle="none",
            marker=ENGINE_MARKERS[other_engine],
            markersize=6.5 + offset,
            markerfacecolor="none",
            markeredgecolor=ENGINE_COLORS[other_engine],
            markeredgewidth=1.1,
            label=ENGINES[other_engine],
            zorder=8 + offset,
        )
        symbols.set_gid("engine_heads_" + other_engine)
        values.append(np.asarray(other_profile))
    boundary = _slice(
        s.chd_mask().any(axis=0) if surface else s.chd_mask()[layer], axis, index
    )
    boundary_indices = np.flatnonzero(boundary)
    boundary_layers = _slice(s.chd_mask(), axis, index)
    for k, j in np.argwhere(boundary_layers):
        if np.isfinite(section[k, j]):
            height = (
                s.layer_tops[k]
                if s.confined
                else np.clip(section[k, j], s.botm[k], s.layer_tops[k])
            ) - s.botm[k]
            patch = Rectangle(
                (faces[j], s.botm[k]),
                1,
                height,
                facecolor=CHD_FILL,
                edgecolor=CHD_BLUE,
                linewidth=1,
                alpha=0.85,
                zorder=3,
            )
            patch.set_gid("chd_cell")
            ax.add_patch(patch)
    for j in boundary_indices:
        # For y-sections in a CHD column every cell is a boundary cell.
        if np.isfinite(line[j]):
            ax.hlines(line[j], faces[j], faces[j + 1], color=CHD_BLUE, lw=2, zorder=6)
    if boundary_indices.size:
        ax.scatter(
            centres[boundary_indices],
            line[boundary_indices],
            marker="s",
            s=50,
            color=CHD_BLUE,
            label=t["chd"],
            zorder=8,
        )
    # Well and observation markers respect the selected section location.
    if s.well_enabled:
        for well in s.wells:
            if (well.row if axis == "x" else well.col) == index:
                position = (well.col if axis == "x" else well.row) + 1
                ax.plot(
                    [position] * 2,
                    [s.bottom, s.top],
                    color=WELL_RED,
                    lw=2,
                    label=t["well"] if len(s.wells) == 1 else well.name,
                    zorder=5,
                )
    for obs in s.observations:
        if (obs.row if axis == "x" else obs.col) == index:
            position = (obs.col if axis == "x" else obs.row) + 1
            value = clean[obs.layer, obs.row, obs.col]
            if np.isfinite(value):
                ax.scatter(position, value, s=20, color="#24364B", zorder=9)
                ax.annotate(
                    obs.name,
                    (position, value),
                    xytext=(5, 8),
                    textcoords="offset points",
                    fontsize=8,
                )
                values.append(np.array([value]))
    handles, _ = ax.get_legend_handles_labels()
    if (active & ~np.isfinite(section)).any():
        color, edge, hatch, label = _dry_appearance(engine)
        handles.append(
            Patch(
                facecolor=color, edgecolor=edge, hatch=hatch, alpha=0.4, label=t[label]
            )
        )
    if (~active).any():
        handles.append(
            Patch(
                facecolor="#CCD3D9",
                edgecolor="#8D9AA5",
                hatch="//",
                alpha=0.4,
                label=t["specified_inactive"],
            )
        )
    ax.legend(handles=handles, loc="upper left", fontsize=8.5, framealpha=0.96)
    ax.set(
        xlabel=t["cell_number_axis"].format(axis=axis),
        ylabel=t["elevation_head_m"],
        xlim=(0.5, n + 0.5),
    )
    ax.set_xticks(
        centres
        if n <= 21
        else np.unique(
            np.r_[1, MaxNLocator(integer=True, nbins=8).tick_values(1, n), n]
        )
    )
    ax.set_xlim(0.5, n + 0.5)
    top_axis = ax.secondary_xaxis(
        "top",
        functions=(lambda x: (x - 1) * s.cell_size, lambda x: 1 + x / s.cell_size),
    )
    top_axis.set_xlabel(t["distance_first_centre"])
    view_label = (
        t["potentiometric" if s.confined else "water_surface"]
        if surface
        else t["layer_view"].format(layer=layer + 1)
    )
    ax.set_title(
        t["cross_title"].format(axis=axis, number=index + 1) + " · " + view_label,
        fontsize=11,
        color=BLUE,
    )
    finite = np.concatenate(values)
    finite = finite[np.isfinite(finite)]
    low, high = finite.min(), finite.max()
    span = max(high - low, 0.5)
    ax.set_ylim(low - 0.08 * span, high + 0.65 * span)
    extensions = ax.vlines(
        visible_faces, *ax.get_ylim(), color="#D6DBE0", lw=0.5, zorder=-1
    )
    extensions.set_gid("grid_extensions")
    if result is not None and show_status:
        _status_box(ax, s, result, t)
    return fig


@themed
def comparison_map(
    reference, other, index, t, axis="x", position=None, difference_limit=None
):
    """Reference head and a signed, paired-wet-cell difference on equal grids."""
    comparison = surface_difference(reference, other, index)
    if comparison is None:
        raise ValueError("Engine maps require matching physical inputs and saved time.")
    difference, mismatch = comparison
    s = reference["scenario"]
    position = (
        (s.nrow // 2 if axis == "x" else s.ncol // 2) if position is None else position
    )
    field = groundwater_surface(s, reference["heads"][index])
    finite = field[np.isfinite(field)]
    low, high = (finite.min(), finite.max()) if finite.size else (0.0, 1.0)
    head_norm = Normalize(
        low - 0.1 if low == high else low, high + 0.1 if low == high else high
    )
    limit = max(
        float(np.nanmax(np.abs(difference))) if np.isfinite(difference).any() else 0.0,
        difference_limit or 0.0,
        1e-9,
    )
    x, y = _edges(s.ncol, s.cell_size), _edges(s.nrow, s.cell_size)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 5.4), layout="constrained")
    ref_name, other_name = (
        ENGINES[reference["solver"].engine],
        ENGINES[other["solver"].engine],
    )
    titles = [
        ref_name + " · " + t["reference_label"],
        t["difference_title"].format(other=other_name, reference=ref_name),
    ]
    for i, (ax, data, cmap, norm, label) in enumerate(
        zip(
            axes,
            (field, difference),
            ("Blues", "RdBu_r"),
            (head_norm, Normalize(-limit, limit)),
            (t["head_m"], t["difference_head_m"]),
            strict=True,
        )
    ):
        mesh = ax.pcolormesh(x, y, data, cmap=cmap, norm=norm, rasterized=True)
        mesh.set_gid("reference_surface" if i == 0 else "engine_difference")
        bar = fig.colorbar(mesh, ax=ax, shrink=0.8, label=label)
        bar.ax.tick_params(labelsize=8)
        _masked_cells(ax, x, y, ~np.isfinite(data))
        _map_grid(ax, x, y)
        _map_markers(ax, s, t, axis, position)
        for col in (0, s.ncol - 1):
            ax.add_patch(
                Rectangle(
                    (x[col], y[0]),
                    s.cell_size,
                    y[-1] - y[0],
                    facecolor="none",
                    edgecolor=CHD_BLUE,
                    linewidth=1.2,
                    zorder=5,
                )
            )
        ax.set(xlim=(x[0], x[-1]), ylim=(y[0], y[-1]), xlabel=t["x_m"], ylabel=t["y_m"])
        ax.set_title(titles[i], fontsize=10, color=BLUE)
        ax.set_aspect("equal")
        ax.tick_params(labelsize=8)
    if mismatch.any():
        cells = [
            [(x[j], y[i]), (x[j + 1], y[i]), (x[j + 1], y[i + 1]), (x[j], y[i + 1])]
            for i, j in np.argwhere(mismatch)
        ]
        hatching = PolyCollection(
            cells,
            facecolors="none",
            edgecolors="#985B43",
            linewidths=0,
            hatch="///",
            zorder=5,
        )
        hatching.set_gid("wet_dry_mismatch")
        axes[1].add_collection(hatching)
    handles = []
    if not np.isfinite(difference).all():
        handles.append(Patch(facecolor=DRY_RED, alpha=0.4, label=t["no_paired_heads"]))
    if mismatch.any():
        handles.append(
            Patch(
                facecolor="none",
                edgecolor="#985B43",
                hatch="///",
                label=t["wet_dry_difference"],
            )
        )
    if handles:
        axes[1].legend(handles=handles, loc="upper left", fontsize=7)
    return fig
