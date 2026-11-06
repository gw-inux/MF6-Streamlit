"""Blue Matplotlib figures on a white background; no model calculations."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   BLUE: line 43
#   ANALYTICAL_GREEN: line 44
#   ORANGE: line 45
#   CHD_FILL: line 46
#   TEXT: line 47
#   PREVIOUS_BLUE: line 48
#   FAILED_RED: line 49
#   FAILED_FILL: line 50
#   MAX_VISIBLE_NODES: line 51
#   COLORS: line 52
#   STYLE: line 53
#   themed: line 59
#   display_stride: line 68
#   display_indices: line 73
#   profile_snapshot: line 78
#   head_plot: line 96
#   error_plot: line 260
#   convergence_plot: line 284
#   model_preview: line 324
#   computed_head_map: line 431
#   first_layer_head_map: line 484
#   grid_study_plot: line 490
# END CODE CONTENTS

from functools import wraps
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, Normalize
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
from matplotlib.collections import PolyCollection
from matplotlib.ticker import MaxNLocator
import numpy as np
from .settings import limits_summary, preset_label
from .surfaces import groundwater_surface
from .diagnostic_guides import convergence_guides

BLUE = "#176DBB"
ANALYTICAL_GREEN = "#278247"
ORANGE = "#DE8428"
CHD_FILL = "#F8D5AE"
TEXT = "#24364B"
PREVIOUS_BLUE = "#7A91A6"
FAILED_RED = "#9A353B"
FAILED_FILL = "#FBE9E9"
MAX_VISIBLE_NODES = 100
COLORS = [BLUE, "#2087AA", "#7755AA", "#287B76", "#AA4E78", "#95682C"]
STYLE = {"figure.facecolor": "white", "axes.facecolor": "white", "axes.edgecolor": "#8795A5",
         "axes.labelcolor": TEXT, "text.color": TEXT, "xtick.color": TEXT, "ytick.color": TEXT,
         "grid.color": "#8795A5", "legend.facecolor": "#F1F6FC", "legend.edgecolor": "#5489B5",
         "legend.labelcolor": BLUE, "savefig.facecolor": "white", "font.size": 11}


def themed(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        with plt.rc_context(STYLE):
            return fn(*args, **kwargs)
    return wrapped



def display_stride(count):
    """One common thinning rule for node symbols and grid faces."""
    return max(1, int(np.ceil(count/MAX_VISIBLE_NODES)))


def display_indices(count):
    """Keep both end cells as well as every stride-th interior node."""
    return np.unique(np.r_[np.arange(0, count, display_stride(count)), count-1])


def profile_snapshot(s, result, layer=0, row=None, surface=False):
    """Only store displayed section nodes, coordinates and their run label.

    Old snapshots are never reinterpreted with a later grid or layer count.
    Full native arrays remain in the separate run book for diagnostics.
    """
    if result.get("heads") is None:
        return None
    row = s.nrow//2 if row is None else row
    indices = display_indices(s.n)
    field = groundwater_surface(s, result["heads"])[0] if surface else s.head_array(result["heads"])[layer]
    return dict(x_m=s.x[indices].tolist(),
                head_m=field[row, indices].tolist(), surface=surface,
                run_id=result["run_id"], layer=layer+1, cell_y=row+1,
                success=bool(result["success"]), comparison_group=s.comparison_group)


@themed
def head_plot(s, results=(), analytical=False, initial=True, settings=None, layer=0, row=None,
              cell_heads=True, cell_lines=True, show_heads=True, previous=None, surface=False,
              intro_notes=False):
    row = s.nrow//2 if row is None else row
    analytical = analytical and s.analytical_available
    fig, ax = plt.subplots(figsize=(9, 5.6), layout="constrained")
    centres = np.arange(1, s.n+1)
    faces = np.arange(s.n+1)+.5
    domain = Rectangle((.5, s.bottom), s.n, s.top-s.bottom,
                       facecolor="#F5F1E4", edgecolor="none", zorder=0)
    domain.set_gid("model_domain")
    ax.add_patch(domain)
    visible_faces = faces[::display_stride(s.n)]
    visible_faces = np.unique(np.append(visible_faces, faces[-1]))
    grid_faces = ax.vlines(visible_faces, s.bottom, s.top, color="#7A858C", lw=.65, alpha=.8, zorder=2)
    grid_faces.set_gid("model_grid_faces")
    ax.hlines([s.bottom, s.top], .5, s.n+.5, color="#8C7859", lw=1.)
    if s.nlay > 1:
        # Actual layer interfaces, visible over wet filling and CHD shading.
        interfaces = ax.hlines(s.botm[:-1], .5, s.n+.5, color="#7A858C",
                               lw=.5, alpha=.85, zorder=3.5)
        interfaces.set_gid("layer_interfaces")
    if analytical:
        xa = np.linspace(0., s.length, 1001)
        ax.plot(1+xa/s.dx, s.analytic(xa), color=ANALYTICAL_GREEN, lw=.9, label="Analytical solution")
    initial_profile = (groundwater_surface(s, s.starting_heads())[0][row] if surface
                       else s.starting_heads().reshape(s.shape)[layer, row]) if initial else None
    if initial:
        ax.plot(centres, initial_profile, "--", color="#7B8795", lw=1.2, label="Initial heads")
    # Hidden initial heads must not influence the vertical plot extent.
    values = [np.array([s.left, s.right, s.bottom, s.top])]
    if initial:
        values.append(initial_profile)
    if analytical:
        values.append(s.analytic(np.linspace(0, s.length, 1001)))
    for i, r in enumerate(results):
        if r["heads"] is not None:
            failed = " (not converged)" if not r["success"] else ""
            clean_heads = s.head_array(r["heads"])
            profile = groundwater_surface(s, r["heads"])[0][row] if surface else clean_heads[layer, row]
            color = COLORS[i % len(COLORS)]
            if i == len(results)-1:
                if surface and s.nlay > 1:
                    # Saturated filling follows actual native layer heads, not
                    # an invented head in a dry cell below a perched wet cell.
                    tops = np.r_[s.top, s.botm[:-1]]
                    for li in range(s.nlay):
                        wet = np.clip(clean_heads[li, row], s.botm[li], tops[li])
                        cells = np.flatnonzero(np.isfinite(wet) & (wet > s.botm[li]))
                        rectangles = [[(faces[j], s.botm[li]), (faces[j+1], s.botm[li]),
                                       (faces[j+1], wet[j]), (faces[j], wet[j])] for j in cells]
                        filling = PolyCollection(rectangles, facecolors="#B9DEF1", edgecolors="none",
                                                 alpha=.7, zorder=1)
                        ax.add_collection(filling)
                        filling.set_gid("wetted_cells")
                else:
                    wet = np.clip(profile, s.bottom, s.top)
                    filling = ax.fill_between(faces, s.bottom, np.append(wet, wet[-1]), step="post",
                                              color="#B9DEF1", alpha=.7, zorder=1)
                    filling.set_gid("wetted_cells")
            if show_heads and cell_lines:
                # Independent horizontal cell segments: no connecting verticals.
                segments = ax.hlines(profile, faces[:-1], faces[1:], color=color, lw=.7,
                                     label="Cell-head lines" + failed, zorder=4)
                segments.set_gid("cell_head_lines")
            if show_heads and cell_heads:
                nodes = display_indices(s.n)
                dots, = ax.plot(centres[nodes], profile[nodes], "o", color=color, ms=3.5,
                                label="Cell-head dots" + (failed if not cell_lines else ""), zorder=7)
                dots.set_gid("cell_head_dots")
            values.append(profile)
    if previous is not None:
        x = 1+np.asarray(previous["x_m"])/s.dx
        old_heads = np.asarray(previous["head_m"])
        old_view = "groundwater surface" if previous.get("surface", False) else f"layer {previous['layer']}"
        old_label = f"Previous run {previous['run_id']:02d} · {old_view}"
        if not previous["success"]:
            old_label += " (not converged)"
        symbols, = ax.plot(x, old_heads, linestyle="none", marker="o", ms=6.5,
                           markerfacecolor="none", markeredgecolor=PREVIOUS_BLUE,
                           markeredgewidth=1., label=old_label, zorder=6)
        symbols.set_gid("previous_heads")
        values.append(old_heads)
    boundaries = (s.chd_mask().any(axis=0) if surface else s.chd_mask()[layer])[row, [0, -1]]
    for cell, head, active in zip((1, s.n), (s.left, s.right), boundaries):
        if active:
            patch = Rectangle((cell-.5, s.bottom), 1., np.clip(head, s.bottom, s.top)-s.bottom,
                              facecolor="#F8D5AE", edgecolor=ORANGE, lw=1., alpha=.85, zorder=3)
            patch.set_gid("chd_cell")
            ax.add_patch(patch)
            ax.hlines(head, cell-.5, cell+.5, color=ORANGE, lw=2., zorder=6)
    ax.scatter(np.array([1, s.n])[boundaries], np.array([s.left, s.right])[boundaries], color=ORANGE,
               marker="s", s=60, label="Specified heads (CHD)", zorder=8)
    ax.set(xlabel="Cell number along x (first cell = 1)", ylabel="Elevation / hydraulic head (m)", xlim=(.5, s.n+.5))
    if s.n <= 21:
        ax.set_xticks(centres)
    else:
        ax.set_xticks(np.unique(np.r_[1, MaxNLocator(integer=True, nbins=8).tick_values(1, s.n), s.n]))
        ax.set_xlim(.5, s.n+.5)
    top = ax.secondary_xaxis("top", functions=(lambda x: (x-1)*s.dx, lambda x: 1+x/s.dx))
    top.set_xlabel("Distance from first boundary-cell centre (m)")
    top.tick_params(colors=TEXT)
    top.xaxis.label.set_color(TEXT)
    ax.grid(False, which="both")
    if s.complexity:
        view = "uppermost wet cells" if surface else f"layer {layer+1}"
        ax.set_title(f"Section A–A′ · {view} · middle cell y {row+1}", fontsize=11, color=BLUE)
    failed_run = bool(results and not results[-1]["success"])
    note_color = FAILED_RED if failed_run else BLUE
    note_fill = FAILED_FILL if failed_run else "#F1F6FC"
    ax.legend(loc="upper left", fontsize=8.5, framealpha=.96,
              facecolor=note_fill, edgecolor=note_color, labelcolor=note_color)
    finite = np.concatenate(values)
    finite = finite[np.isfinite(finite)]
    low, high = float(finite.min()), float(finite.max())
    span = max(high-low, .5)
    ax.set_ylim(low-.08*span, high+.65*span)
    # Extend the same sampled cell faces through the plot. The opaque model
    # domain hides these pale guides inside the aquifer, retaining its grid.
    extensions = ax.vlines(visible_faces, *ax.get_ylim(), color="#D6DBE0", lw=.5, zorder=-1)
    extensions.set_gid("grid_extensions")
    if intro_notes and not results and s.n == 11 and not s.complexity and s.confined:
        # First-view teaching labels only; no change to the head or grid arrays.
        for cell, text_x in ((1, 2.4), (s.n, s.n-1.4)):
            label = ax.annotate("CHD\nspecified head", xy=(cell, (s.bottom+s.top)/2),
                xytext=(text_x, s.top+.10*span), ha="center", va="bottom", fontsize=8.5,
                color="#975614", arrowprops=dict(arrowstyle="->", color=ORANGE, lw=.9),
                bbox=dict(boxstyle="round,pad=.3", facecolor="white", edgecolor=ORANGE, alpha=.95))
            label.set_gid("initial_chd_note")
        label = ax.text((s.n+1)/2, s.bottom+.4*(s.top-s.bottom),
            "Model cells\nheads computed here", ha="center", va="center", fontsize=9,
            color=BLUE, bbox=dict(boxstyle="round,pad=.35", facecolor="white", edgecolor="#ADC7DF", alpha=.95))
        label.set_gid("initial_interior_note")
    if settings:
        h, flow, outer, inner = limits_summary(settings)
        lines = [settings.label, s.aquifer_label]
        if settings.engine != "mf2005":
            lines.append(preset_label(settings))
        lines.append(f"Head closure = {h:.2E} m")
        if flow is not None:
            lines.append(f"Flow closure = {flow:.2E} m³/s")
        lines.append(f"{'SIP' if settings.method == 'SIP' else 'Outer'} limit = {outer}" +
                     (f"; inner limit = {inner}" if inner is not None else ""))
        p = settings.parameters()
        if settings.method in ("PCG", "SIP"):
            key = "relax" if settings.method == "PCG" else "accl"
            lines.append(f"{key.upper()} = {p[key]:.2f}")
        if results:
            r = results[-1]
            lines.append(r["status"])
            count = (f"SIP iterations = {r['sip_iterations']}" if settings.method == "SIP" else
                     f"Outer = {r['outer_iterations']}; inner = {r['inner_iterations']}")
            lines.append(count)
            lines.append(f"Runtime = {r['wall_s']:.4f} s" + (" (median)" if r.get("repeats", 1) > 1 else ""))
        else:
            lines.append("Initial-head preview" if initial else "No computed result")
        status = ax.text(.98, .97, "\n".join(lines), transform=ax.transAxes, ha="right", va="top",
                fontsize=8.5, color=note_color,
                bbox=dict(boxstyle="round,pad=.55", facecolor=note_fill, edgecolor=note_color, alpha=.97))
        status.set_gid("run_status")
    return fig


@themed
def error_plot(s, results):
    fig, ax = plt.subplots(figsize=(9, 3.2), layout="constrained")
    if not s.analytical_available:
        ax.text(.5, .5, "No analytical head reference for heterogeneous or layered models.\nInspect native water balance and convergence below.",
                ha="center", va="center", transform=ax.transAxes, color=BLUE)
        ax.set_axis_off()
        return fig
    for i, r in enumerate(results):
        if r["heads"] is not None:
            err = s.head_array(r["heads"])[0]-s.analytic()[None, :]
            ax.plot(s.x, err[s.nrow//2], color=COLORS[i % len(COLORS)],
                    label=r.get("run_name", r["label"]))
            if s.nrow > 1:
                ax.fill_between(s.x, np.nanmin(err, axis=0), np.nanmax(err, axis=0), color=COLORS[i % len(COLORS)], alpha=.15)
    ax.axhline(0, color="#96A6BA", lw=.7)
    ax.set(xlabel="Distance (m)", ylabel="Numerical − analytical head (m)")
    ax.ticklabel_format(axis="y", style="sci", scilimits=(-3, 3))
    if any(r["heads"] is not None for r in results):
        ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=.22)
    return fig


@themed
def convergence_plot(history, kind, solver=None):
    rows = [r for r in history if r["kind"] == kind]
    guides = convergence_guides(solver, kind) if solver else {}
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.3), layout="constrained")
    for ax, key, ylabel in zip(axes, ["head_change", "residual"], ["Max |head change| (m)", "Reported |residual| (m³/s)"]):
        x = np.array([r["iteration"] for r in rows])
        y = np.array([r[key] for r in rows])
        good = np.isfinite(y) & (y > 0)
        if good.any():
            ax.semilogy(x[good], y[good], "o-", color=BLUE, ms=4)
        else:
            message = ("All reported values are zero" if np.isfinite(y).any()
                       else "Not reported at this iteration level")
            ax.text(.5, .5, message, ha="center", fontsize=10, transform=ax.transAxes)
            ax.set_yticks([])
        guide = guides.get(key)
        if guide is not None:
            value, name = guide
            # Include the requested closure even when all recorded values are zero.
            ax.set_yscale("log")
            threshold = ax.axhline(value, color="#B75B46", ls="--", lw=1.,
                label=f"{name} = {value:.2E}", zorder=4)
            threshold.set_gid("closure_threshold")
            ax.legend(loc="upper right", fontsize=7.5)
            if not good.any():
                ax.set_ylim(value/10, value*10)
                ax.set_yticks([value/10, value, value*10])
        if key == "residual" and guides.get("residual_note"):
            ax.text(.98, .98, guides["residual_note"], transform=ax.transAxes,
                ha="right", va="top", fontsize=7.5, color="#83503F",
                bbox=dict(facecolor="white", edgecolor="#D9C7BE", alpha=.95))
        ax.set(xlabel=f"{kind.capitalize()} iteration", ylabel=ylabel)
        if len(x):
            ax.set_xlim(max(0, x.min()-.5), x.max()+.5)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, min_n_ticks=1, nbins=8))
        ax.grid(alpha=.22)
    return fig


@themed
def model_preview(s, quantity="Empty cells", heads=None, layer=0, row=None):
    """Equal-width sections; an undistorted square plan in horizontal 2D.

    K display classes use the requested zone count. They only colour the
    existing field; they never quantize or replace conductivity in the model.
    """
    row = s.nrow//2 if row is None else row
    boundaries = field = None
    k_display = quantity in ("K zones", "Hydraulic conductivity")
    if k_display:
        field = s.k_field()
        low, high = (s.k_min, s.k_max) if s.random_k else (s.k_ms, s.k_ms)
        bands = s.k_zones if s.random_k and low < high else 1
        boundaries = np.geomspace(low, high, bands+1) if bands > 1 else np.array([low/1.1, high*1.1])
        cmap = plt.get_cmap("YlGnBu", bands)
        norm = BoundaryNorm(boundaries, cmap.N, clip=True)
        numbered = np.unique(np.r_[np.arange(0, bands, max(1, int(np.ceil(bands/15)))), bands-1])
        ticks = ((boundaries[:-1]+boundaries[1:])/2)[numbered]
        middle = np.sqrt(boundaries[:-1]*boundaries[1:]) if bands > 1 else np.array([low])
        tick_labels = [f"{i+1} · {middle[i]:.2e}" for i in numbered]
        label = f"K class (1–{bands}) · midpoint (m/s)"
    elif quantity != "Empty cells":
        field = s.head_array(heads) if heads is not None else s.starting_heads().reshape(s.shape).copy()
        field[~s.active_mask()] = np.nan
        finite = field[np.isfinite(field)]
        low, high = (float(finite.min()), float(finite.max())) if finite.size else (0., 1.)
        norm = Normalize(low-.1 if low == high else low, high+.1 if low == high else high)
        label, cmap = "Head (m)", "Blues"

    # Explicit physical panel sizes avoid shrinking the equal-aspect plan.
    # Both plots share exactly the same x location and width in the figure.
    fig_width, left, panel_width = 9., .10, .69
    plan_height = fig_width*panel_width if s.horizontal_2d else 2.25
    section_height, gap, bottom, top = 2.25, .85, .65, .55
    fig_height = bottom+section_height+gap+plan_height+top
    fig = plt.figure(figsize=(fig_width, fig_height))
    axes = [fig.add_axes([left, (bottom+section_height+gap)/fig_height, panel_width, plan_height/fig_height]),
            fig.add_axes([left, bottom/fig_height, panel_width, section_height/fig_height])]
    xedges = np.arange(s.n+1)*s.dx-s.dx/2
    yedges = np.arange(s.nrow+1)*s.dy-s.dy/2
    zedges = np.linspace(s.top, s.bottom, s.nlay+1)
    plan = None
    surface = groundwater_surface(s, heads)[0] if heads is not None and s.nlay > 1 else None
    if field is not None:
        plan_field = surface if surface is not None else field[layer]
        plan = axes[0].pcolormesh(xedges, yedges, plan_field, norm=norm, cmap=cmap, rasterized=True)
        axes[1].pcolormesh(xedges, zedges, field[:, row], norm=norm, cmap=cmap, rasterized=True)
    else:
        for ax, lo, hi in ((axes[0], yedges[0], yedges[-1]), (axes[1], s.bottom, s.top)):
            empty = Rectangle((xedges[0], lo), xedges[-1]-xedges[0], hi-lo,
                              facecolor="white", edgecolor="#4E6574", lw=.8)
            empty.set_gid("empty_cells")
            ax.add_patch(empty)
    plan_title = ("Groundwater / potentiometric surface" if surface is not None else f"Horizontal grid · layer {layer+1}")
    axes[0].set(xlabel="x (m)", ylabel="y (m)", title=f"{plan_title} · {s.n} × {s.nrow} cells",
                ylim=(yedges[0], yedges[-1]))
    axes[1].set(xlabel="x (m)", ylabel="Elevation (m)", title=f"Section A–A′ · middle cell y {row+1} · {s.nlay} layer(s)",
                ylim=(s.bottom, s.top))
    xfaces = np.unique(np.r_[xedges[::display_stride(s.n)], xedges[-1]])
    yfaces = np.unique(np.r_[yedges[::display_stride(s.nrow)], yedges[-1]])
    for ax, lo, hi in ((axes[0], yedges[0], yedges[-1]), (axes[1], s.bottom, s.top)):
        faces = ax.vlines(xfaces, lo, hi, color="#4E6574", lw=.55, alpha=.8, zorder=4)
        faces.set_gid("grid_faces_x")
    axes[0].hlines(yfaces, xedges[0], xedges[-1], color="#4E6574", lw=.55, alpha=.8, zorder=4)
    axes[1].hlines(zedges, xedges[0], xedges[-1], color="#4E6574", lw=.65, alpha=.8, zorder=4)
    boundary = s.chd_mask()
    plan_boundary = boundary.any(axis=0) if surface is not None else boundary[layer]
    for col in (0, s.n-1):
        # A uniform west/east boundary uses one rectangle per view, not one per row.
        if plan_boundary[:, col].any():
            patch = Rectangle((xedges[col], yedges[0]), s.dx, yedges[-1]-yedges[0],
                              facecolor=CHD_FILL, edgecolor=ORANGE, zorder=3)
            patch.set_gid("preview_chd")
            axes[0].add_patch(patch)
        for li in range(s.nlay):
            if boundary[li, row, col]:
                patch = Rectangle((xedges[col], zedges[li+1]), s.dx, zedges[li]-zedges[li+1],
                                  facecolor=CHD_FILL, edgecolor=ORANGE, zorder=3)
                patch.set_gid("preview_chd")
                axes[1].add_patch(patch)
    section = axes[0].axhline(row*s.dy, color="#B63355", ls="--", lw=1.2, zorder=6)
    section.set_gid("section_trace")
    if s.recharge_mmy > 0:
        for x in np.linspace(.15*s.length, .85*s.length, 5):
            axes[1].annotate("", xy=(x, s.top-.13*(s.top-s.bottom)), xytext=(x, s.top),
                             arrowprops=dict(arrowstyle="->", color=BLUE), annotation_clip=False, zorder=6)
    axes[0].legend(handles=[Patch(facecolor=CHD_FILL, edgecolor=ORANGE, label="Specified heads · west / east"),
                           Line2D([], [], color="#B63355", ls="--", label="Section A–A′")],
                   loc="upper left", fontsize=8)
    for ax in axes:
        ax.title.set_color(BLUE)
        ax.set_xlim(xedges[0], xedges[-1])
    if s.horizontal_2d:
        axes[0].set_aspect("equal", adjustable="box")
    if plan is not None:
        cax = fig.add_axes([.815, bottom/fig_height, .025,
                           (section_height+gap+plan_height)/fig_height])
        if k_display:
            bar = fig.colorbar(plan, cax=cax, label=label, boundaries=boundaries,
                               ticks=ticks, spacing="uniform", drawedges=True)
            bar.ax.set_yticklabels(tick_labels, fontsize=8)
        else:
            fig.colorbar(plan, cax=cax, label=label)
    return fig


@themed
def computed_head_map(s, heads, *, surface=True, stale=False):
    """Equal-scale head map; use the uppermost wet cell for a surface view.

    With surface=False this retains the original first-layer diagnostic.
    Stale output uses a grey palette, with the previous run's own geometry.
    """
    field = groundwater_surface(s, heads)[0] if surface else s.head_array(heads)[0]
    boundary = s.chd_mask().any(axis=0) if surface else s.chd_mask()[0]
    map_color = "#747B84" if stale else BLUE
    boundary_color = "#8B8F95" if stale else ORANGE
    trace_color = "#6F747C" if stale else "#B63355"
    xedges = np.arange(s.n+1)*s.dx-s.dx/2
    yedges = np.arange(s.nrow+1)*s.dy-s.dy/2
    fig, ax = plt.subplots(figsize=(8, 7), layout="constrained")
    finite = field[np.isfinite(field)]
    if finite.size:
        low, high = float(finite.min()), float(finite.max())
        norm = Normalize(low-.1 if low == high else low, high+.1 if low == high else high)
        mesh = ax.pcolormesh(xedges, yedges, field, norm=norm, cmap="Greys" if stale else "Blues", rasterized=True)
        mesh.set_gid("groundwater_surface" if surface else "first_layer_heads")
        fig.colorbar(mesh, ax=ax, label="Head (m)", shrink=.9)
    else:
        ax.text(.5, .5, "No wet, active heads in this column set" if surface else "No wet, active heads in layer 1", ha="center", va="center",
                transform=ax.transAxes, color=BLUE,
                bbox=dict(facecolor="white", edgecolor="none", alpha=.9), zorder=7)
    xfaces = np.unique(np.r_[xedges[::display_stride(s.n)], xedges[-1]])
    yfaces = np.unique(np.r_[yedges[::display_stride(s.nrow)], yedges[-1]])
    ax.vlines(xfaces, yedges[0], yedges[-1], color="#4E6574", lw=.4, alpha=.6, zorder=3)
    ax.hlines(yfaces, xedges[0], xedges[-1], color="#4E6574", lw=.4, alpha=.6, zorder=3)
    handles = []
    for col in (0, s.n-1):
        if boundary[:, col].any():
            patch = Rectangle((xedges[col], yedges[0]), s.dx, yedges[-1]-yedges[0],
                              facecolor="none", edgecolor=boundary_color, lw=1.4, zorder=4)
            patch.set_gid("head_map_chd")
            ax.add_patch(patch)
    if ax.patches:
        handles.append(Patch(facecolor="none", edgecolor=boundary_color, label="Specified-head cells"))
    section = ax.axhline((s.nrow//2)*s.dy, color=trace_color, ls="--", lw=1.1, zorder=5)
    section.set_gid("section_trace")
    handles.append(Line2D([], [], color=trace_color, ls="--", label="Section A–A′"))
    ax.legend(handles=handles, loc="upper left", fontsize=8)
    title = ("Potentiometric surface" if s.confined else "Groundwater surface") if surface else "Computed heads · first layer (layer 1)"
    if stale:
        title += " · previous result — rerun required"
    ax.set(xlabel="x (m)", ylabel="y (m)", title=title,
           xlim=(xedges[0], xedges[-1]), ylim=(yedges[0], yedges[-1]))
    ax.title.set_color(map_color)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(False)
    return fig


def first_layer_head_map(s, heads):
    """Compatibility view for inspecting native layer-1 heads only."""
    return computed_head_map(s, heads, surface=False)


@themed
def grid_study_plot(table):
    fig, ax = plt.subplots(figsize=(9, 4), layout="constrained")
    for i, (label, group) in enumerate(table.groupby("Model / solver", sort=False)):
        good = group[group["Status"] == "Converged"].sort_values("Cells")
        if not good.empty:
            ax.loglog(good["Cells"], good["Process time (s)"], "o-", color=COLORS[i % len(COLORS)], label=label)
    ax.set(xlabel="Number of cells", ylabel="Median process time (s)")
    if ax.lines:
        ax.legend(loc="upper left", fontsize=8, ncol=2)
        # Reserve logarithmic headroom for the legend without obscuring runs.
        times = table.loc[table["Status"] == "Converged", "Process time (s)"]
        times = times[np.isfinite(times) & (times > 0)]
        if len(times):
            ax.set_ylim(times.min()/1.2, times.max()*max(3., (times.max()/times.min())**.3))
    ax.grid(alpha=.22)
    return fig
