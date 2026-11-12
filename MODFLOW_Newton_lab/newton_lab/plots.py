"""Head histories and budgets with explicit engine identities and comparisons.

The original rate integration remains in outputs.py. These views only select
and display native records, including each run's own initial-head baseline.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .analytical import regular_solution
from .config import ENGINES
from .plot_style import COLORS as SERIES_COLORS, ENGINE_COLORS, ENGINE_MARKERS, themed
from .spatial_plots import cross_section, top_view  # noqa: F401

BUDGET_COLORS = {"CHD": "#3c9266", "WEL": "#b33b54", "RCH": "#3181bc", "STO": "#8859aa"}


def _model_name(result):
    return ENGINES[result["solver"].engine]


def _comparison_runs(reference, comparisons):
    """Only current-batch solutions with identical physical inputs belong here."""
    return [reference] + [
        r
        for r in comparisons
        if r.get("success")
        and r["scenario"] == reference["scenario"]
        and r["solver"].engine != reference["solver"].engine
    ]


def _finish(ax, t, xlabel="time_days", ylabel="head_m"):
    ax.set_xlabel(t[xlabel])
    ax.set_ylabel(t[ylabel])
    ax.grid(alpha=0.18)
    ax.spines[["top", "right"]].set_visible(False)


def _period_lines(ax, s):
    elapsed = 0.0
    for period in s.periods()[1:-1]:
        elapsed += period.seconds / 86400
        ax.axvline(elapsed, color="#8b95a3", lw=0.8, ls="--", zorder=0)


def _legend(ax):
    """Keep the Solver Lab legend at upper left, clear of dense comparisons."""
    handles, _ = ax.get_legend_handles_labels()
    if handles:
        legend = ax.legend(
            loc="upper left", fontsize=7, ncol=2 if len(handles) <= 12 else 3
        )
        ax.margins(y=0.08)
        if len(handles) > 6 and np.isfinite(ax.dataLim.y1):
            # Reserve measured headroom so a multi-engine budget legend does
            # not cover the constant recharge curve or other high values.
            ax.figure.canvas.draw()
            fraction = min(
                0.60,
                legend.get_window_extent().height / ax.get_window_extent().height
                + 0.04,
            )
            lower = ax.get_ylim()[0]
            ax.set_ylim(lower, lower + (ax.dataLim.y1 - lower) / (1 - fraction))


@themed
def timeseries_plot(
    result,
    t,
    selected,
    previous=None,
    analytical=False,
    drawdown=False,
    *,
    comparisons=(),
):
    s = result["scenario"]
    runs = _comparison_runs(result, comparisons)
    fig, ax = plt.subplots(figsize=(9, 5.2), layout="constrained")
    for point_index, name in enumerate(selected):
        color = SERIES_COLORS[point_index % len(SERIES_COLORS)]
        for model_index, run in enumerate(runs):
            table = run["timeseries"]
            if name not in table:
                continue
            values = table[name].to_numpy()
            y = values[0] - values if drawdown else values
            engine = run["solver"].engine
            (line,) = ax.plot(
                table.time_days,
                y,
                color=color,
                linewidth=1.6 if model_index == 0 else 1.0,
                linestyle=("-", "--", "-.")[model_index % 3],
                marker=ENGINE_MARKERS[engine] if len(runs) > 1 else None,
                markersize=3.2 if model_index == 0 else 5.5 + model_index,
                markerfacecolor=color if model_index == 0 else "none",
                markevery=max(1, len(y) // 12),
                label=name + " · " + _model_name(run),
            )
            line.set_gid("heads_" + engine + "_" + name)
        if previous is not None and name in previous["timeseries"]:
            old = previous["timeseries"]
            values = old[name].to_numpy()
            ax.plot(
                old.time_days,
                values[0] - values if drawdown else values,
                color=color,
                linestyle=":",
                linewidth=1.4,
                label=name + " · " + _model_name(previous) + " · " + t["previous"],
            )
        baseline = (
            result["timeseries"][name].iloc[0]
            if name in result["timeseries"]
            else np.nan
        )
        if (
            analytical
            and len(s.wells) == 1
            and name not in {w.name for w in s.wells}
            and np.isfinite(baseline)
        ):
            obs = next(o for o in s.observations if o.name == name)
            radius = s.cell_size * np.hypot(obs.col - s.well_col, obs.row - s.well_row)
            if radius > 0:
                times = result["timeseries"].time_days.to_numpy()
                reference = regular_solution(s, times, radius, baseline)
                ax.plot(
                    times,
                    baseline - reference if drawdown else reference,
                    linestyle=(0, (5, 2, 1, 2)),
                    color=color,
                    linewidth=1.1,
                    label=name + " · " + t["analytical"] + " · " + _model_name(result),
                )
    _period_lines(ax, s)
    ax.set_title(
        t["time_title"] + "\n" + " / ".join(_model_name(r) for r in runs), fontsize=11
    )
    _finish(ax, t, ylabel="drawdown_m" if drawdown else "head_m")
    _legend(ax)
    return fig


def _budget_curve(run, term, sign, cumulative):
    """Solved end-step rates; only transient steps contribute to the plot."""
    table = run["budget"]
    rows = table[table.period > 0]
    column = term + "_" + sign + ("_CUM" if cumulative else "")
    factor = (1 if sign == "IN" else -1) * (1 if cumulative else 1000)
    values = rows[column].to_numpy() * factor
    times = np.r_[0, rows.time_days.to_numpy()]
    return times, np.r_[0 if cumulative else values[0], values]


@themed
def budget_plot(
    result,
    t,
    cumulative=False,
    previous=None,
    selected=("CHD", "WEL", "RCH", "STO"),
    *,
    comparisons=(),
):
    s = result["scenario"]
    runs = _comparison_runs(result, comparisons)
    fig, ax = plt.subplots(figsize=(9, 5.2), layout="constrained")
    if not s.transient:
        width = 0.8 / len(runs)
        for model_index, run in enumerate(runs):
            row = run["budget"].iloc[-1]
            engine = run["solver"].engine
            x = np.arange(len(selected)) + (model_index - (len(runs) - 1) / 2) * width
            ax.bar(
                x,
                [row[term + "_IN"] * 1000 for term in selected],
                width=width * 0.9,
                color=ENGINE_COLORS[engine],
                label=_model_name(run),
            )
            ax.bar(
                x,
                [-row[term + "_OUT"] * 1000 for term in selected],
                width=width * 0.9,
                color=ENGINE_COLORS[engine],
                hatch="//",
                alpha=0.65,
            )
        ax.set_xticks(
            np.arange(len(selected)), [t["term_" + term.lower()] for term in selected]
        )
        if previous is not None:
            row = previous["budget"].iloc[-1]
            x = np.arange(len(selected)) - (len(runs) - 1) / 2 * width
            ax.scatter(
                np.r_[x, x],
                [row[term + "_IN"] * 1000 for term in selected]
                + [-row[term + "_OUT"] * 1000 for term in selected],
                marker="_",
                s=160,
                color="black",
                zorder=5,
                label=_model_name(previous) + " · " + t["previous"],
            )
    else:
        all_runs = runs + ([previous] if previous is not None else [])
        for term in selected:
            for sign in ("IN", "OUT"):
                # Keep a component if it exists in ANY displayed model.
                # Otherwise a zero reference component would hide a nonzero comparison.
                curves = [
                    _budget_curve(run, term, sign, cumulative) for run in all_runs
                ]
                if not any(np.max(np.abs(y), initial=0) > 1e-12 for _, y in curves):
                    continue
                for model_index, (run, (times, values)) in enumerate(
                    zip(all_runs, curves, strict=True)
                ):
                    old = model_index >= len(runs)
                    engine = run["solver"].engine
                    kwargs = dict(
                        color=BUDGET_COLORS[term],
                        linewidth=1.5 if model_index == 0 else 1.0,
                        linestyle=":" if old else ("-" if sign == "IN" else "--"),
                        marker=ENGINE_MARKERS[engine]
                        if len(runs) > 1 and not old
                        else None,
                        markersize=3.2 if model_index == 0 else 5.5 + model_index,
                        markerfacecolor=BUDGET_COLORS[term]
                        if model_index == 0
                        else "none",
                        markevery=max(1, len(values) // 12),
                        label=t["term_" + term.lower()]
                        + " · "
                        + t[sign.lower()]
                        + " · "
                        + _model_name(run)
                        + (" · " + t["previous"] if old else ""),
                    )
                    (line,) = (
                        ax.plot(times, values, **kwargs)
                        if cumulative
                        else ax.step(times, values, where="pre", **kwargs)
                    )
                    line.set_gid(
                        "budget_"
                        + engine
                        + "_"
                        + term
                        + "_"
                        + sign
                        + ("_previous" if old else "")
                    )
        _period_lines(ax, s)
        ax.set_xlabel(t["time_days"])
    ax.axhline(0, linewidth=0.8, color="#596b7b")
    ax.set_title(
        t["budget_title"] + "\n" + " / ".join(_model_name(r) for r in runs), fontsize=11
    )
    ax.set_ylabel(t["volume_m3"] if cumulative and s.transient else t["flow_lps"])
    ax.grid(axis="y", alpha=0.18)
    _legend(ax)
    return fig
