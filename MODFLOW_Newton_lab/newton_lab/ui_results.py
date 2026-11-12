"""Result controls and comparisons, separate from simulation construction."""

import json
import zipfile
from dataclasses import asdict
from io import BytesIO

import numpy as np
import pandas as pd
import streamlit as st

from .config import ENGINES
from .plots import budget_plot, timeseries_plot
from .ui_spatial import render_spatial_results, show_figure
from .ui_history import render_history


def result_archive(result):
    """An explicit download includes native inputs, outputs and configuration."""
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(result["directory"].iterdir()):
            if path.is_file():
                archive.write(path, path.name)
    return buffer.getvalue()


def comparison_compatibility(current, previous):
    """Require the same observation coordinates and regime for time overlays.

    Parameters, grid spacing, boundaries and engines may differ deliberately;
    their differences are displayed alongside an explicit overlay opt-in.
    """
    if previous is None or not previous["success"]:
        return False, False, []
    now, old = current["scenario"], previous["scenario"]
    a, b = asdict(now), asdict(old)
    changes = [key for key in a if a[key] != b[key]]
    if current["solver"] != previous["solver"]:
        changes.append("solver")
    mode_ok = now.transient == old.transient
    locations_now = {
        o.name: (
            (o.col + 0.5) * now.cell_size,
            (o.row + 0.5) * now.cell_size,
            (now.layer_tops[o.layer] + now.botm[o.layer]) / 2,
        )
        for o in now.observations
    }
    locations_old = {
        o.name: (
            (o.col + 0.5) * old.cell_size,
            (o.row + 0.5) * old.cell_size,
            (old.layer_tops[o.layer] + old.botm[o.layer]) / 2,
        )
        for o in old.observations
    }

    def well_locations(s):
        return {
            w.name: ((w.col + 0.5) * s.cell_size, (w.row + 0.5) * s.cell_size)
            for w in s.wells
        }

    well_ok = well_locations(now) == well_locations(old)
    heads_ok = mode_ok and well_ok and locations_now == locations_old
    return heads_ok, mode_ok, changes


def render_results(batch, previous_batch, t, language, history=()):
    results = batch["results"]
    keys = [key for key, run in results.items() if run["success"]]
    failures = [key for key, run in results.items() if not run["success"]]
    for failed in failures:
        st.warning(t["failed_engine_note"].format(engine=ENGINES[failed]))
    if failures:
        with st.expander(t["failed_downloads"]):
            if st.session_state.get("failed_engine") not in failures:
                st.session_state.failed_engine = failures[0]
            failed = st.selectbox(
                t["inspect_engine"],
                failures,
                format_func=ENGINES.get,
                key="failed_engine",
            )
            st.error(t["run_failed"].format(reason=results[failed]["error"]))
            _downloads(results[failed], t)
    if not keys:
        render_history(history, t)
        return
    if st.session_state.get("view_engine") not in keys:
        st.session_state.view_engine = keys[0]
    engine = st.selectbox(
        t["reference_engine"], keys, format_func=ENGINES.get, key="view_engine"
    )
    result = results[engine]
    s = result["scenario"]
    st.caption(
        t["result_identity"].format(run=result["run_id"], engine=ENGINES[engine])
    )
    compare = st.toggle(
        t["compare_engines"], key="compare_engines", disabled=len(keys) < 2
    )
    comparisons = []
    if len(keys) < 2:
        st.caption(t["one_engine_help"])
    elif compare:
        others = [key for key in keys if key != engine]
        selected_engines = st.multiselect(
            t["comparison_engines"],
            others,
            default=others,
            format_func=ENGINES.get,
            key="comparison_engines_" + "_".join(keys) + "_" + engine,
        )
        comparisons = [results[key] for key in selected_engines]
        st.caption(t["engine_comparison_help"])
    if result["max_discrepancy_pct"] > 0.1:
        st.warning(t["large_discrepancy"])
    previous = None
    if previous_batch:
        candidates = previous_batch["results"]
        previous = candidates.get(engine)
        if previous is None:
            previous = next(
                (v for v in reversed(list(candidates.values())) if v["success"]), None
            )
    heads_ok, budget_ok, changes = comparison_compatibility(result, previous)
    compare_heads = compare_budget = False
    with st.expander(t["comparison"]):
        if previous is None or not previous["success"]:
            st.info(t["no_previous"])
        else:
            st.caption(
                t["previous_identity"].format(
                    run=previous["run_id"], engine=ENGINES[previous["solver"].engine]
                )
            )
            if changes:
                st.markdown(
                    t["changed_parameters"] + " " + ", ".join(f"`{k}`" for k in changes)
                )
            if heads_ok and s.transient:
                compare_heads = st.checkbox(t["compare_heads"], key="compare_heads")
            elif s.transient:
                st.info(t["locations_differ"])
            if budget_ok:
                compare_budget = st.checkbox(t["compare_budget"], key="compare_budget")
            else:
                st.info(t["regimes_differ"])
    render_spatial_results(
        result, previous, t, comparisons=comparisons, history=history
    )
    if s.transient:
        st.subheader(t["heads_over_time"], divider="blue")
        st.caption(t["well_cell_note"])
        names = list(result["timeseries"].columns[1:])
        selected = st.multiselect(
            t["select_points"], names, default=names, key=f"series_{result['run_id']}"
        )
        drawdown = st.toggle(t["drawdown"], key="drawdown_view")
        compare_time = (
            st.toggle(t["compare_time_engines"], value=True, key="compare_time_engines")
            if comparisons
            else False
        )
        add_analytical = False
        possible = (
            not s.combined
            and s.well_enabled
            and not s.heterogeneous
            and not s.inactive
            and len(s.wells) == 1
        )
        if possible:
            add_analytical = st.checkbox(t["show_theis"], key="theis")
            if add_analytical:
                st.info(t["theis_help"])
                if s.recharge != 0:
                    st.warning(t["theis_recharge"])
                if not s.confined:
                    st.info(t["unconfined_analytical"])
        elif s.combined or s.heterogeneous or s.inactive or len(s.wells) > 1:
            st.caption(t["analytical_unavailable"])
        if selected:
            show_figure(
                timeseries_plot(
                    result,
                    t,
                    selected,
                    previous if compare_heads else None,
                    add_analytical,
                    drawdown,
                    comparisons=comparisons if compare_time else (),
                )
            )
    st.subheader(t["water_balance"], divider="blue")
    st.caption(t["budget_sign"])
    cumulative = st.toggle(t["cumulative"], key="cumulative") if s.transient else False
    terms = st.multiselect(
        t["budget_terms"],
        ["CHD", "WEL", "RCH", "STO"],
        default=["CHD", "WEL", "RCH", "STO"],
        key="budget_terms",
        format_func=lambda k: t["term_" + k.lower()],
    )
    # Budget selection is independent of the spatial/head reference. A key per
    # computation prevents selections from referring to failed or removed runs.
    budget_runs = [result]
    if len(keys) > 1:
        budget_engines = st.multiselect(
            t["budget_models"],
            keys,
            default=[engine],
            format_func=lambda key: t["result_identity"].format(
                run=results[key]["run_id"], engine=ENGINES[key]
            ),
            key="budget_models_"
            + "_".join(str(results[key]["run_id"]) for key in keys),
            help=t["budget_models_help"],
        )
        budget_runs = [results[key] for key in budget_engines]
    if terms and budget_runs:
        show_figure(
            budget_plot(
                budget_runs[0],
                t,
                cumulative,
                previous if compare_budget else None,
                terms,
                comparisons=budget_runs[1:],
            )
        )
    elif not budget_runs:
        st.info(t["budget_models_empty"])
    if s.transient:
        st.caption(t["cumulative_help"])
    rate_tables = []
    reduced = False
    for run in budget_runs:
        difference = np.abs(run["budget"].actual_well - run["budget"].requested_well)
        requested = np.abs(run["budget"].requested_well)
        reduced |= bool((difference > np.maximum(1e-8, requested * 1e-4)).any())
        rates = run["budget"][["time_days", "requested_well", "actual_well"]].copy()
        rates[["requested_well", "actual_well"]] *= 1000
        rates.columns = [t["time_days"], t["requested_lps"], t["actual_lps"]]
        rates.insert(0, t["hist_engine"], ENGINES[run["solver"].engine])
        rate_tables.append(rates)
    if reduced:
        st.warning(t["reduced_well"])
    if rate_tables:
        with st.expander(t["well_rates"]):
            st.dataframe(
                pd.concat(rate_tables, ignore_index=True),
                hide_index=True,
                column_config={
                    t["time_days"]: st.column_config.NumberColumn(format="%.4f"),
                    t["requested_lps"]: st.column_config.NumberColumn(format="%.3f"),
                    t["actual_lps"]: st.column_config.NumberColumn(format="%.3f"),
                },
            )
    _downloads(result, t)


def _downloads(result, t):
    with st.expander(t["downloads"]):
        st.caption(
            t["download_engine_note"].format(engine=ENGINES[result["solver"].engine])
        )
        if result["success"]:
            st.download_button(
                t["download_heads"],
                result["timeseries"].to_csv(index=False),
                key=f"download_heads_{result['run_id']}",
                file_name="heads_over_time.csv",
                mime="text/csv",
            )
            st.download_button(
                t["download_budget"],
                result["budget"].to_csv(index=False),
                key=f"download_budget_{result['run_id']}",
                file_name="water_budget_m3_per_second_and_m3.csv",
                mime="text/csv",
            )
        st.download_button(
            t["download_config"],
            json.dumps(
                {
                    "scenario": asdict(result["scenario"]),
                    "solver": asdict(result["solver"]),
                },
                indent=2,
            ),
            key=f"download_config_{result['run_id']}",
            file_name="configuration.json",
            mime="application/json",
        )
        # Build the potentially large archive only on explicit request.
        if st.button(t["prepare_archive"], key=f"prepare_{result['run_id']}"):
            st.session_state["archive"] = (result["run_id"], result_archive(result))
        archive = st.session_state.get("archive")
        if archive and archive[0] == result["run_id"]:
            st.download_button(
                t["download_archive"],
                archive[1],
                key=f"download_archive_{result['run_id']}",
                file_name=f"run_{result['run_id']}_{result['solver'].engine}.zip",
            )
        st.download_button(
            t["download_listing"],
            result["listing"],
            key=f"download_listing_{result['run_id']}",
            file_name="native_listing.txt",
        )
        with st.expander(t["native_log"]):
            path = result["directory"] / "stdout.txt"
            st.code(
                path.read_text(errors="replace")[-12000:]
                if path.exists()
                else result["error"],
                language="text",
            )
