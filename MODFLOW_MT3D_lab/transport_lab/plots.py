"""Native-grid model preview, analytical profiles, breakthrough and mass balance."""
from collections import defaultdict

import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from .analytical import applied, impulse
from .scenario import END_TIME, LEFT_HEAD, LENGTH, VELOCITY

COLORS = ("#1A5990", "#C05A18", "#19825C", "#8B57A4", "#B43C59",
          "#008A98", "#76602D", "#555F88", "#637D21", "#865A49")
INK = "#233A50"
GRID = "#DAE3E9"


def _style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["bottom", "left"]].set_color("#92A5B2")
    ax.tick_params(colors=INK, labelsize=9)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=GRID, linewidth=0.65)


def preview(case, txt):
    fig = Figure(figsize=(7.2, 3.65), layout="constrained")
    grid_ax, source_ax = fig.subplots(2, 1, gridspec_kw={"height_ratios": [1, 0.93]})
    left, right = -case.dx / 2, LENGTH + case.dx / 2
    grid_ax.add_patch(Rectangle((left, 0.10), right - left, 0.30,
                                facecolor="#EFE5C9", edgecolor="#746C5D", linewidth=1.0))
    for x in (left, LENGTH - case.dx / 2):
        grid_ax.add_patch(Rectangle((x, 0.10), case.dx, 0.30, facecolor="#376A92", edgecolor="#284F70"))
    grid_ax.vlines(case.x[:-1] + case.dx / 2, 0.10, 0.40, color="#7E755E",
                   linewidth=0.65 if case.ncol <= 101 else 0.27, alpha=0.85)
    grid_ax.text(0, 0.5, txt["specified_head"].format(head=LEFT_HEAD), fontsize=9, color=INK, ha="left")
    grid_ax.text(LENGTH, 0.5, txt["specified_head"].format(head=0.0), fontsize=9, color=INK, ha="right")
    grid_ax.annotate("", xy=(0.66 * LENGTH, 0.58), xytext=(0.34 * LENGTH, 0.58),
                     arrowprops={"arrowstyle": "->", "color": COLORS[0], "lw": 1.8})
    grid_ax.text(LENGTH / 2, 0.69, f"v = {VELOCITY:g} m/d", color=COLORS[0], ha="center", fontsize=10)
    grid_ax.set(xlim=(left, right), ylim=(0.03, 0.95), yticks=[], xlabel=txt["distance"])
    grid_ax.spines[["top", "right", "left"]].set_visible(False)
    grid_ax.spines["bottom"].set_color("#AAB9C1")
    grid_ax.tick_params(labelsize=9, colors=INK, length=3)

    duration, height = case.duration, case.height
    xx, yy = [0, 0, duration], [0, height, height]
    if duration < END_TIME:
        xx.extend([duration, END_TIME])
        yy.extend([0, 0])
    source_ax.fill_between(xx, yy, color="#D0E7ED", alpha=0.9)
    source_ax.plot(xx, yy, color="#216C7B", lw=2)
    source_ax.set(xlim=(-0.012 * END_TIME, END_TIME), ylim=(-.06 * height, 1.25 * height),
                  xlabel=txt["time"], ylabel=txt["inlet_axis"])
    _style(source_ax)
    return fig


def _coordinates(case, position, selected):
    """Include step discontinuities and narrow dispersive peaks in a plotted curve."""
    maximum = LENGTH if position == "profile" else END_TIME
    points = [np.linspace(0, maximum, 751)]
    if position == "profile":
        ages = [selected]
        if case.signal != "continuous" and selected >= case.duration:
            ages.append(selected - case.duration)
        features = [(VELOCITY * age, np.sqrt(2 * case.D * age)) for age in ages]
    else:
        arrival = selected / VELOCITY
        width = np.sqrt(2 * case.D * arrival) / VELOCITY
        features = [(arrival, width)]
        if case.signal != "continuous":
            features.append((arrival + case.duration, width))
    for centre, width in features:
        points.append(np.array([np.nextafter(centre, -np.inf), centre, np.nextafter(centre, np.inf)]))
        if width > 0:
            points.append(centre + width * np.linspace(-7, 7, 141))
    return np.unique(np.clip(np.concatenate(points), 0, maximum))


def _legend(ax):
    handles, labels = ax.get_legend_handles_labels()
    if len(handles) <= 5:
        ax.legend(loc="upper left", fontsize=8, framealpha=0.92)
    else:
        columns = 2 if max(map(len, labels)) > 32 else 3
        rows = int(np.ceil(len(labels) / columns))
        legend_height = 0.24 * rows + 0.10
        fig = ax.figure
        fig.set_size_inches(7.3, 3.6 + legend_height)
        grid = fig.add_gridspec(2, 1, height_ratios=[3.10, legend_height])
        ax.set_subplotspec(grid[0])
        key = fig.add_subplot(grid[1])
        key.set_axis_off()
        key.legend(handles, labels, loc="center left", ncols=columns,
                   fontsize=8, frameon=False, columnspacing=1.2)


def _references(ax, variants, position, selected, txt):
    applied_groups = defaultdict(list)
    ideal_groups = defaultdict(list)
    for variant in variants:
        case = variant.run.case
        applied_groups[case.applied_reference_key].append(variant)
        if case.signal == "dirac":
            ideal_groups[(case.D, case.impulse_area)].append(variant)

    for ideal, groups in ((False, applied_groups), (True, ideal_groups)):
        color_key_needed = False
        for group in groups.values():
            first = group[0]
            case = first.run.case
            # Share a black reference when every visible variant has the same reference.
            common = len(group) == len(variants)
            color = "#222B32" if common else COLORS[first.color_slot]
            name = txt["ideal_curve"] if ideal else txt["applied_curve"]
            if not common:
                name += " (" + ", ".join(f"V{v.number}" for v in group) + ")"
            # Individual references follow the variant colour; one style key suffices.
            individual = len(groups) > 1 and len(group) == 1
            if individual:
                name = "_nolegend_"
            if ideal and case.D == 0:
                location = VELOCITY * selected if position == "profile" else selected / VELOCITY
                maximum = LENGTH if position == "profile" else END_TIME
                if 0 <= location <= maximum:
                    color_key_needed |= individual
                    ax.axvline(location, color=color, ls=":", lw=1.8,
                               label=f"{name} · A={case.impulse_area:g} d")
                continue
            color_key_needed |= individual
            coords = _coordinates(case, position, selected)
            x, t = (coords, selected) if position == "profile" else (selected, coords)
            curve = impulse(x, t, case) if ideal else applied(x, t, case)
            ax.plot(coords, curve, ":" if ideal else "--", color=color,
                    lw=2.0 if ideal else 1.7, label=name, zorder=4)
        if color_key_needed:
            label = txt["ideal_color_key"] if ideal else txt["applied_color_key"]
            ax.plot([], [], ":" if ideal else "--", color="#445667", lw=1.8, label=label)


def result_figure(variants, view, selected, analytical, markers, txt):
    fig = Figure(figsize=(7.3, 3.7 + 0.10 * max(0, len(variants) - 4)), layout="constrained")
    ax = fig.subplots()
    for v in variants:
        run = v.run
        if view == "profile":
            x, y = run.case.x, run.profile(selected)
        elif view == "breakthrough":
            x, y = run.times, run.breakthrough(selected)
        else:
            x, y = run.mass_times, run.mass_error
        ax.plot(x, y, color=COLORS[v.color_slot], lw=1.35, label=v.short_label,
                marker="o" if markers else None, markersize=3.6, markerfacecolor="white",
                markevery=max(1, len(x) // 95), alpha=0.95)
    if analytical and view != "budget":
        _references(ax, variants, view, selected, txt)
    if view == "budget":
        ax.axhline(0, color="#697B88", lw=0.7)
    ax.set(xlim=(0, LENGTH if view == "profile" else END_TIME),
           xlabel=txt["distance"] if view == "profile" else txt["time"],
           ylabel=txt["mass_axis"] if view == "budget" else r"$C/C_{\mathrm{ref}}$ [–]")
    _style(ax)
    _legend(ax)
    return fig
