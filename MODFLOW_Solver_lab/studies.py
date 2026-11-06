"""Grid-refinement plans and results, separate from the individual-run book."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   render_grid_study: line 29
# END CODE CONTENTS

from copy import deepcopy
from dataclasses import asdict, replace
import time
import pandas as pd
import streamlit as st

from .content import TEXT
from .core import MAX_CELLS, Solver, comparison_row, fingerprint
from .plots import grid_study_plot
from .results import execute, TIMEOUT_SECONDS
from .settings import (
    VARIANTS,
    parse_grid_entries,
    parse_grid_spacings,
    variant_plan,
    settings_table,
    formatted_csv,
)
from .ui import show_fig, show_table


def render_grid_study(s, cfg, profile, executables, workspace, repeats):
    st.subheader(TEXT["study_heading"], divider="blue")
    st.markdown(TEXT["study_intro"])
    st.markdown(TEXT["study_repeats"])
    with st.container(key="study_grid_panel"), st.expander(
        TEXT["study_grid_settings_and_study_name"]
    ):
        study_name = st.text_input(
            TEXT["study_study_name_optional"],
            placeholder=TEXT["study_grid_study"],
            key="study_name",
        )
        grid_input = st.selectbox(
            TEXT["study_grid_input"],
            ["Cell counts along x", "Uniform cell spacing (m)"],
            index=1 if s.complexity else 0,
            key=f"grid_input_{s.complexity}",
        )
        grid_count = st.selectbox(
            TEXT["study_number_of_grid_sizes"],
            list(range(1, 11)),
            index=0 if s.complexity or profile["expert_enabled"] else 2,
            key="grid_count_complex" if s.complexity or profile["expert_enabled"] else "grid_count",
        )
        use_spacing = grid_input == "Uniform cell spacing (m)"
        if use_spacing:
            spacing_key = f"spacing_entries_{s.length}_{s.n}_{s.nlay}_{s.horizontal_2d}"
            if spacing_key not in st.session_state:
                max_count = min(
                    10001,
                    int((MAX_CELLS / s.nlay) ** 0.5) if s.horizontal_2d else MAX_CELLS // s.nlay,
                )
                candidates = (
                    [s.n]
                    + list(range(11, min(max_count, 101) + 1, 10))
                    + list(range(3, max_count + 1))
                )
                counts = list(dict.fromkeys(candidates))[:10]
                st.session_state[spacing_key] = [f"{s.length/(count-1):.10g}" for count in counts]
            entries = st.session_state[spacing_key]
        else:
            entries = st.session_state.grid_entries
        for start in range(0, grid_count, 5):
            grid_columns = st.columns(5)
            for i in range(start, min(start + 5, grid_count)):
                with grid_columns[i - start]:
                    entries[i] = st.text_input(
                        TEXT["study_grid_value"].format(value=i + 1)
                        + (TEXT["study_m"] if use_spacing else ""),
                        value=entries[i],
                        key=f"{spacing_key}_{i}" if use_spacing else f"grid_size_{i+1}",
                        help=(
                            TEXT["study_spacing_help"] if use_spacing else TEXT["study_count_help"]
                        ),
                    )
        st.caption(TEXT["study_geometry"].format(layers=s.nlay))
        grid_error = None
        try:
            sizes = (
                parse_grid_spacings(entries[:grid_count], s.length)
                if use_spacing
                else parse_grid_entries(entries[:grid_count])
            )
            for size in sizes:
                replace(s, n=size).validate()
            show_table(
                pd.DataFrame(
                    [
                        {
                            "Cells x": size,
                            "Cells y": size if s.horizontal_2d else 1,
                            "Layers": s.nlay,
                            "Cells": replace(s, n=size).total_cells,
                            "Δx (m)": replace(s, n=size).dx,
                            "Δy (m)": replace(s, n=size).dy,
                        }
                        for size in sizes
                    ]
                ),
                key="grid_geometry",
            )
        except ValueError as error:
            sizes, grid_error = [], str(error)
            st.warning(grid_error)
    with st.container(key="study_solver_panel"), st.expander(
        TEXT["study_solver_settings_for_the_experiment"]
    ):
        variant_labels = {v: Solver(**st.session_state.variants[v]).label for v in VARIANTS}
        chosen = st.multiselect(
            TEXT["study_model_solver_variants_to_include"],
            VARIANTS,
            default=[f"{cfg.engine}/{cfg.method}"] if s.complexity else VARIANTS,
            key="complex_grid_variants" if s.complexity else "grid_variants",
            format_func=variant_labels.get,
        )
        st.markdown(TEXT["study_variants"])
        plan = variant_plan(st.session_state.variants, executables)
        show_table(plan[plan["Variant"].isin(chosen)].drop(columns="Variant"), key="grid_plan")
        if chosen:
            if st.session_state.get("inspect_variant") not in chosen:
                st.session_state.pop("inspect_variant", None)
            inspect_variant = st.selectbox(
                TEXT["study_show_full_settings_for"],
                chosen,
                key="inspect_variant",
                format_func=variant_labels.get,
            )
            show_table(settings_table(Solver(**st.session_state.variants[inspect_variant])))
    unavailable = [v for v in chosen if not executables[v.split("/")[0]]]
    if unavailable:
        st.warning(TEXT["study_unavailable_note"] + ", ".join(unavailable))
    calls = len(chosen) * len(sizes) * int(repeats)
    st.caption(
        TEXT["study_plan_note"].format(
            chosen_count=len(chosen), sizes_count=len(sizes), repeats=repeats, calls=calls
        )
    )
    plan_signature = fingerprint(
        dict(
            scenario=asdict(s),
            variants={v: st.session_state.variants[v] for v in chosen},
            sizes=sizes,
            repeats=repeats,
            timeout=TIMEOUT_SECONDS,
            executables=executables,
        )
    )
    _, run_column, _ = st.columns([1, 2, 1])
    with run_column, st.container(key="grid_run"):
        run_study = st.button(
            TEXT["study_run_grid_study"],
            type="primary",
            width="stretch",
            disabled=not chosen or not sizes or bool(unavailable) or grid_error is not None,
            key="run_grid",
        )
    if run_study:
        rows = []
        folder = workspace / f"study_{time.time_ns()}"
        planned = {v: deepcopy(st.session_state.variants[v]) for v in chosen}
        progress = st.progress(0.0, text=TEXT["study_preparing_grid_study"])
        total = len(sizes) * len(chosen)
        for index, (size, variant) in enumerate(
            (size, variant) for size in sizes for variant in chosen
        ):
            vc = Solver(**planned[variant])
            progress.progress(
                index / total,
                text=f"{vc.label} · {replace(s, n=size).grid_label} · {repeats} repeat(s)",
            )
            r = execute(
                replace(s, n=size),
                vc,
                folder / str(size) / variant.replace("/", "_"),
                int(repeats),
                executables,
            )
            rows.append(comparison_row(r) | {"Repeats": int(repeats)})
        progress.empty()
        study = dict(
            study_id=st.session_state.next_study_id,
            name=study_name.strip() or f"Grid study {st.session_state.next_study_id}",
            rows=rows,
            plan=planned,
            scenario=asdict(s),
            sizes=sizes,
            repeats=int(repeats),
            signature=plan_signature,
        )
        st.session_state.studies = [*st.session_state.studies, study][-5:]
        st.session_state.next_study_id += 1
        st.session_state.study_view = study["study_id"]
        st.session_state.diagnostic_extra = dict(
            r,
            run_id=-study["study_id"],
            run_name=f"{study['name']} · last run · {vc.label} · {size} cells along x",
        )
        st.session_state.pending_inspect = -study["study_id"]
        st.rerun()
    if st.session_state.studies:
        studies = {v["study_id"]: v for v in st.session_state.studies}
        if st.session_state.get("study_view") not in studies:
            st.session_state.pop("study_view", None)
        study_id = st.selectbox(
            TEXT["study_study_results"],
            list(studies),
            index=None if "study_view" in st.session_state else len(studies) - 1,
            key="study_view",
            format_func=lambda k: studies[k]["name"],
        )
        study = studies[study_id]
        if study["signature"] != plan_signature:
            st.caption(TEXT["study_stale_note"])
        gt = pd.DataFrame(study["rows"])
        show_table(gt)
        show_fig(grid_study_plot(gt))
        st.caption(
            TEXT["study_saved_note"].format(
                study_plan_count=len(study["plan"]),
                grids=", ".join(map(str, study["sizes"])),
                repeats=study["repeats"],
            )
        )
        with st.expander(TEXT["study_settings_used_in_the_saved_study"]):
            saved_variant = st.selectbox(
                TEXT["study_inspect_settings_used_in_this_study"],
                list(study["plan"]),
                key=f"study_settings_{study_id}",
            )
            show_table(settings_table(Solver(**study["plan"][saved_variant])))
        st.download_button(
            TEXT["study_download_grid_study_csv"], formatted_csv(gt), "grid_study.csv", "text/csv"
        )
