"""Grid-refinement plans and results, separate from the individual-run book."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   render_grid_study: line 23
# END CODE CONTENTS

from copy import deepcopy
from dataclasses import asdict, replace
import time
import pandas as pd
import streamlit as st

from content import TEXT
from core import MAX_CELLS, Solver, comparison_row, fingerprint
from plots import grid_study_plot
from results import execute, TIMEOUT_SECONDS
from settings import (VARIANTS, parse_grid_entries, parse_grid_spacings,
                      variant_plan, settings_table, formatted_csv)
from ui import show_fig, show_table


def render_grid_study(s, cfg, profile, executables, workspace, repeats):
    st.subheader(TEXT["study_heading"], divider="blue")
    st.markdown(TEXT["study_intro"])
    st.markdown(TEXT["study_repeats"])
    with st.container(key="study_grid_panel"), st.expander("**Grid settings and study name**"):
        study_name = st.text_input("Study name (optional)", placeholder="Grid study", key="study_name")
        grid_input = st.selectbox("Grid input", ["Cell counts along x", "Uniform cell spacing (m)"],
                                  index=1 if s.complexity else 0, key=f"grid_input_{s.complexity}")
        grid_count = st.selectbox("Number of grid sizes", list(range(1, 11)), index=0 if s.complexity or profile["expert_enabled"] else 2,
                                 key="grid_count_complex" if s.complexity or profile["expert_enabled"] else "grid_count")
        use_spacing = grid_input == "Uniform cell spacing (m)"
        if use_spacing:
            spacing_key = f"spacing_entries_{s.length}_{s.n}_{s.nlay}_{s.horizontal_2d}"
            if spacing_key not in st.session_state:
                max_count = min(10001, int((MAX_CELLS/s.nlay)**.5) if s.horizontal_2d else MAX_CELLS//s.nlay)
                candidates = [s.n] + list(range(11, min(max_count, 101)+1, 10)) + list(range(3, max_count+1))
                counts = list(dict.fromkeys(candidates))[:10]
                st.session_state[spacing_key] = [f"{s.length/(count-1):.10g}" for count in counts]
            entries = st.session_state[spacing_key]
        else:
            entries = st.session_state.grid_entries
        for start in range(0, grid_count, 5):
            grid_columns = st.columns(5)
            for i in range(start, min(start+5, grid_count)):
                with grid_columns[i-start]:
                    entries[i] = st.text_input(f"Grid {i+1}" + (" · Δ (m)" if use_spacing else ""), value=entries[i],
                        key=f"{spacing_key}_{i}" if use_spacing else f"grid_size_{i+1}",
                        help="Uniform Δx = Δy in horizontal 2D. Spacing must divide the boundary-centre distance exactly." if use_spacing
                             else "Cells along x, including the two fixed-head end cells (3–10,001). In horizontal 2D, Ny = Nx.")
        st.caption(TEXT["study_geometry"].format(layers=s.nlay))
        grid_error = None
        try:
            sizes = parse_grid_spacings(entries[:grid_count], s.length) if use_spacing else parse_grid_entries(entries[:grid_count])
            for size in sizes:
                replace(s, n=size).validate()
            show_table(pd.DataFrame([{"Cells x": size, "Cells y": size if s.horizontal_2d else 1, "Layers": s.nlay,
                                     "Cells": replace(s, n=size).total_cells, "Δx (m)": replace(s, n=size).dx,
                                     "Δy (m)": replace(s, n=size).dy} for size in sizes]), key="grid_geometry")
        except ValueError as error:
            sizes, grid_error = [], str(error)
            st.warning(grid_error)
    with st.container(key="study_solver_panel"), st.expander("**Solver settings for the experiment**"):
        variant_labels = {v: Solver(**st.session_state.variants[v]).label for v in VARIANTS}
        chosen = st.multiselect("Model / solver variants to include", VARIANTS, default=[f"{cfg.engine}/{cfg.method}"] if s.complexity else VARIANTS, key="complex_grid_variants" if s.complexity else "grid_variants",
            format_func=variant_labels.get)
        st.markdown(TEXT["study_variants"])
        plan = variant_plan(st.session_state.variants, executables)
        show_table(plan[plan["Variant"].isin(chosen)].drop(columns="Variant"), key="grid_plan")
        if chosen:
            if st.session_state.get("inspect_variant") not in chosen:
                st.session_state.pop("inspect_variant", None)
            inspect_variant = st.selectbox("Show full settings for", chosen, key="inspect_variant",
                format_func=variant_labels.get)
            show_table(settings_table(Solver(**st.session_state.variants[inspect_variant])))
    unavailable = [v for v in chosen if not executables[v.split('/')[0]]]
    if unavailable:
        st.warning("Exclude variants whose executable is not available before starting this study: " + ", ".join(unavailable))
    calls = len(chosen)*len(sizes)*int(repeats)
    st.caption(f"Study plan: {len(chosen)} variant(s) × {len(sizes)} grid(s) × {repeats} repeat(s) = {calls} native model runs.")
    plan_signature = fingerprint(dict(scenario=asdict(s), variants={v: st.session_state.variants[v] for v in chosen},
                                     sizes=sizes, repeats=repeats, timeout=TIMEOUT_SECONDS, executables=executables))
    _, run_column, _ = st.columns([1, 2, 1])
    with run_column, st.container(key="grid_run"):
        run_study = st.button("Run grid study", type="primary", width="stretch",
            disabled=not chosen or not sizes or bool(unavailable) or grid_error is not None, key="run_grid")
    if run_study:
        rows = []
        folder = workspace / f"study_{time.time_ns()}"
        planned = {v: deepcopy(st.session_state.variants[v]) for v in chosen}
        progress = st.progress(0., text="Preparing grid study…")
        total = len(sizes)*len(chosen)
        for index, (size, variant) in enumerate((size, variant) for size in sizes for variant in chosen):
            vc = Solver(**planned[variant])
            progress.progress(index/total, text=f"{vc.label} · {replace(s, n=size).grid_label} · {repeats} repeat(s)")
            r = execute(replace(s, n=size), vc, folder/str(size)/variant.replace("/", "_"), int(repeats), executables)
            rows.append(comparison_row(r) | {"Repeats": int(repeats)})
        progress.empty()
        study = dict(study_id=st.session_state.next_study_id, name=study_name.strip() or f"Grid study {st.session_state.next_study_id}",
                     rows=rows, plan=planned, scenario=asdict(s), sizes=sizes, repeats=int(repeats), signature=plan_signature)
        st.session_state.studies = [*st.session_state.studies, study][-5:]
        st.session_state.next_study_id += 1
        st.session_state.study_view = study["study_id"]
        st.session_state.diagnostic_extra = dict(r, run_id=-study["study_id"],
            run_name=f"{study['name']} · last run · {vc.label} · {size} cells along x")
        st.session_state.pending_inspect = -study["study_id"]
        st.rerun()
    if st.session_state.studies:
        studies = {v["study_id"]: v for v in st.session_state.studies}
        if st.session_state.get("study_view") not in studies:
            st.session_state.pop("study_view", None)
        study_id = st.selectbox("Study results", list(studies), index=None if "study_view" in st.session_state else len(studies)-1, key="study_view", format_func=lambda k: studies[k]["name"])
        study = studies[study_id]
        if study["signature"] != plan_signature:
            st.caption("These saved study results belong to earlier settings. The recorded settings below preserve the study as run.")
        gt = pd.DataFrame(study["rows"])
        show_table(gt)
        show_fig(grid_study_plot(gt))
        st.caption(f"Saved study: {len(study['plan'])} variants, grids {', '.join(map(str, study['sizes']))}, "
                   f"{study['repeats']} repeat(s) per configuration. Up to five studies are retained separately from the ten-run table.")
        with st.expander("**Settings used in the saved study**"):
            saved_variant = st.selectbox("Inspect settings used in this study", list(study["plan"]), key=f"study_settings_{study_id}")
            show_table(settings_table(Solver(**study["plan"][saved_variant])))
        st.download_button("Download grid study CSV", formatted_csv(gt), "grid_study.csv", "text/csv")
