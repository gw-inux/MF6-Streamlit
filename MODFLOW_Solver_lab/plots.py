"""Blue Matplotlib figures on a white background; no model calculations."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   BLUE: line 36
#   ORANGE: line 37
#   CHD_FILL: line 38
#   TEXT: line 39
#   PREVIOUS_BLUE: line 40
#   MAX_VISIBLE_NODES: line 41
#   COLORS: line 42
#   STYLE: line 43
#   themed: line 49
#   display_stride: line 58
#   display_indices: line 63
#   profile_snapshot: line 68
#   head_plot: line 85
#   error_plot: line 212
#   convergence_plot: line 236
#   model_preview: line 259
#   first_layer_head_map: line 362
#   grid_study_plot: line 410
# END CODE CONTENTS

from functools import wraps
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, Normalize
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
import numpy as np
from settings import limits_summary, preset_label

BLUE = "#176DBB"
ORANGE = "#DE8428"
CHD_FILL = "#F8D5AE"
TEXT = "#24364B"
PREVIOUS_BLUE = "#7A91A6"
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


def profile_snapshot(s, result, layer=0, row=None):
    """Only store displayed section nodes, coordinates and their run label.

    Old snapshots are never reinterpreted with a later grid or layer count.
    Full native arrays remain in the separate run book for diagnostics.
    """
    if result.get("heads") is None:
        return None
    row = s.nrow//2 if row is None else row
    indices = display_indices(s.n)
    return dict(x_m=s.x[indices].tolist(),
                head_m=s.head_array(result["heads"])[layer, row, indices].tolist(),
                run_id=result["run_id"], layer=layer+1, cell_y=row+1,
                success=bool(result["success"]), comparison_group=s.comparison_group)


@themed
def head_plot(s, results=(), analytical=False, initial=True, settings=None, layer=0, row=None,
              cell_heads=True, cell_lines=True, show_heads=True, previous=None):
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
        ax.plot(1+xa/s.dx, s.analytic(xa), color="#174B79", lw=.9, label="Analytical solution")
    if initial:
        ax.plot(centres, s.starting_heads().reshape(s.shape)[layer, row], "--", color="#7B8795", lw=1.2, label="Initial heads")
    # Hidden initial heads must not influence the vertical plot extent.
    values = [np.array([s.left, s.right, s.bottom, s.top])]
    if initial:
        values.append(s.starting_heads().reshape(s.shape)[layer, row])
    if analytical:
        values.append(s.analytic(np.linspace(0, s.length, 1001)))
    for i, r in enumerate(results):
        if r["heads"] is not None:
            failed = " (not converged)" if not r["success"] else ""
            profile = s.head_array(r["heads"])[layer, row]
            color = COLORS[i % len(COLORS)]
            if i == len(results)-1:
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
        old_label = f"Previous run {previous['run_id']:02d} · layer {previous['layer']}"
        if not previous["success"]:
            old_label += " (not converged)"
        symbols, = ax.plot(x, old_heads, linestyle="none", marker="o", ms=6.5,
                           markerfacecolor="none", markeredgecolor=PREVIOUS_BLUE,
                           markeredgewidth=1., label=old_label, zorder=6)
        symbols.set_gid("previous_heads")
        values.append(old_heads)
    boundaries = s.chd_mask()[layer, row, [0, -1]]
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
        ax.set_title(f"Section A–A′ · layer {layer+1} · middle cell y {row+1}", fontsize=11, color=BLUE)
    ax.legend(loc="upper left", fontsize=8.5, framealpha=.96)
    finite = np.concatenate(values)
    finite = finite[np.isfinite(finite)]
    low, high = float(finite.min()), float(finite.max())
    span = max(high-low, .5)
    ax.set_ylim(low-.08*span, high+.65*span)
    # Extend the same sampled cell faces through the plot. The opaque model
    # domain hides these pale guides inside the aquifer, retaining its grid.
    extensions = ax.vlines(visible_faces, *ax.get_ylim(), color="#D6DBE0", lw=.5, zorder=-1)
    extensions.set_gid("grid_extensions")
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
        ax.text(.98, .97, "\n".join(lines), transform=ax.transAxes, ha="right", va="top",
                fontsize=8.5, color=BLUE,
                bbox=dict(boxstyle="round,pad=.55", facecolor="#F1F6FC", edgecolor=BLUE, alpha=.97))
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
def convergence_plot(history, kind):
    rows = [r for r in history if r["kind"] == kind]
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
    if field is not None:
        plan = axes[0].pcolormesh(xedges, yedges, field[layer], norm=norm, cmap=cmap, rasterized=True)
        axes[1].pcolormesh(xedges, zedges, field[:, row], norm=norm, cmap=cmap, rasterized=True)
    else:
        for ax, lo, hi in ((axes[0], yedges[0], yedges[-1]), (axes[1], s.bottom, s.top)):
            empty = Rectangle((xedges[0], lo), xedges[-1]-xedges[0], hi-lo,
                              facecolor="white", edgecolor="#4E6574", lw=.8)
            empty.set_gid("empty_cells")
            ax.add_patch(empty)
    axes[0].set(xlabel="x (m)", ylabel="y (m)", title=f"Horizontal grid · layer {layer+1} · {s.n} × {s.nrow} cells",
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
    for col in (0, s.n-1):
        # A uniform west/east boundary uses one rectangle per view, not one per row.
        if boundary[layer, :, col].any():
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
def first_layer_head_map(s, heads):
    """Native heads in layer 1, with equal x/y scales and no interpolation.

    Keep CHD head colours visible; outlines mark the boundary cells. Dry and
    inactive cells stay blank, including an entirely dry first layer.
    """
    field = s.head_array(heads)[0]
    xedges = np.arange(s.n+1)*s.dx-s.dx/2
    yedges = np.arange(s.nrow+1)*s.dy-s.dy/2
    fig, ax = plt.subplots(figsize=(8, 7), layout="constrained")
    finite = field[np.isfinite(field)]
    if finite.size:
        low, high = float(finite.min()), float(finite.max())
        norm = Normalize(low-.1 if low == high else low, high+.1 if low == high else high)
        mesh = ax.pcolormesh(xedges, yedges, field, norm=norm, cmap="Blues", rasterized=True)
        mesh.set_gid("first_layer_heads")
        fig.colorbar(mesh, ax=ax, label="Head (m)", shrink=.9)
    else:
        ax.text(.5, .5, "No wet, active heads in layer 1", ha="center", va="center",
                transform=ax.transAxes, color=BLUE,
                bbox=dict(facecolor="white", edgecolor="none", alpha=.9), zorder=7)
    xfaces = np.unique(np.r_[xedges[::display_stride(s.n)], xedges[-1]])
    yfaces = np.unique(np.r_[yedges[::display_stride(s.nrow)], yedges[-1]])
    ax.vlines(xfaces, yedges[0], yedges[-1], color="#4E6574", lw=.4, alpha=.6, zorder=3)
    ax.hlines(yfaces, xedges[0], xedges[-1], color="#4E6574", lw=.4, alpha=.6, zorder=3)
    handles = []
    boundary = s.chd_mask()[0]
    for col in (0, s.n-1):
        if boundary[:, col].any():
            patch = Rectangle((xedges[col], yedges[0]), s.dx, yedges[-1]-yedges[0],
                              facecolor="none", edgecolor=ORANGE, lw=1.4, zorder=4)
            patch.set_gid("head_map_chd")
            ax.add_patch(patch)
    if ax.patches:
        handles.append(Patch(facecolor="none", edgecolor=ORANGE, label="Specified-head cells"))
    section = ax.axhline((s.nrow//2)*s.dy, color="#B63355", ls="--", lw=1.1, zorder=5)
    section.set_gid("section_trace")
    handles.append(Line2D([], [], color="#B63355", ls="--", label="Section A–A′"))
    ax.legend(handles=handles, loc="upper left", fontsize=8)
    ax.set(xlabel="x (m)", ylabel="y (m)", title="Computed heads · first layer (layer 1)",
           xlim=(xedges[0], xedges[-1]), ylim=(yedges[0], yedges[-1]))
    ax.title.set_color(BLUE)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(False)
    return fig


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
