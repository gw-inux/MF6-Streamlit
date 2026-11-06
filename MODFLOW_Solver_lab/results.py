"""Run comparison, diagnostics and display controls for computed results."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   TIMEOUT_SECONDS: line 33
#   execute: line 36
#   keep_head_style: line 48
#   enable_analytical_points: line 53
#   model_summary: line 58
#   render_visibility: line 74
#   render_computed_map: line 107
#   initial_grid_notes: line 133
#   render_execution: line 140
#   render_run_comparison: line 195
#   render_diagnostics: line 231
# END CODE CONTENTS

from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
import time
import pandas as pd
import streamlit as st

from .content import TEXT
from .core import ENGINE_NAMES, Scenario, Solver, fingerprint, run_repeated
from .plots import (head_plot, profile_snapshot, display_stride,
                   error_plot, model_preview, convergence_plot)
from .settings import MAX_RUNS, append_run, remove_runs, run_table, formatted_csv, settings_table, limits_summary, preset_label
from .ui import show_fig, show_table, style_computed_map
from .map_rendering import head_map_image

TIMEOUT_SECONDS = 120.


def execute(scenario, cfg, folder, repeats, executables):
    """Execute with the fixed timeout, retaining failed runs in the comparison."""
    try:
        return run_repeated(scenario, cfg, folder, executables[cfg.engine], repeats, TIMEOUT_SECONDS)
    except Exception as error:
        return dict(engine=cfg.engine, method=cfg.method, label=cfg.label,
            scenario=asdict(scenario), solver=asdict(cfg), success=False, status="Input / output error",
            outer_iterations=None, inner_iterations=None, sip_iterations=None, wall_s=float("nan"),
            heads=None, metrics={}, budget_percent=None, history=[], listing="", repeats=repeats,
            stdout=f"{type(error).__name__}: {error}")


def keep_head_style(changed_key, other_key):
    if not st.session_state[changed_key] and not st.session_state.get(other_key, True):
        st.session_state[other_key] = True


def enable_analytical_points():
    if st.session_state.get("analytical", False):
        st.session_state.show_cell_heads = True


def model_summary(s, cfg):
    head, flow, outer, inner = limits_summary(cfg)
    conductivity = (f"Random K = {s.k_min:.2E}–{s.k_max:.2E} m/s." if s.random_k
                    else f"K = {s.k_ms:.2E} m/s.")
    text = TEXT["model_summary"].format(grid=s.grid_label, cells=s.total_cells,
        dx=s.dx, dy=s.dy, aquifer=s.aquifer_label, top=s.top, bottom=s.bottom,
        conductivity=conductivity, recharge=s.recharge_mmy, solver=cfg.label,
        preset=preset_label(cfg), head=head, outer=outer,
        flow=f"; flow closure = {flow:.2E} m³/s" if flow is not None else "",
        inner=f"; inner limit = {inner}" if inner is not None else "")
    if cfg.engine == "mf2005":
        field = "accl" if cfg.method == "SIP" else "relax"
        text += f" {field.upper()} = {cfg.parameters()[field]:g}."
    st.markdown(text)


def render_visibility(s, previous):
    """Two rows share the same three-column layout."""
    c1, c2, c3 = st.columns(3)
    with c1:
        analytical = st.toggle("Show analytical solution", value=False, key="analytical",
            disabled=not s.analytical_available, on_change=enable_analytical_points,
            help="Enabling the analytical solution also switches on cell-head dots for comparison.")
    with c2:
        initial = st.toggle("Show initial heads", value=False, key="show_initial",
            help="Only changes visibility and axis scaling, not the solver's starting heads.")
    with c3:
        old = st.toggle("Show previous run", value=False, key="show_previous", disabled=previous is None,
            help="Hollow symbols show the saved section at its original physical coordinates.")
    if not st.session_state.get("show_cell_heads", True) and not st.session_state.get("show_cell_lines", True):
        st.session_state.show_cell_lines = True
    c1, c2, _ = st.columns(3)
    with c1:
        dots = st.toggle("Cell-head dots", value=True, key="show_cell_heads", on_change=keep_head_style,
            args=("show_cell_heads", "show_cell_lines"), help="Switching off the last active head style enables the other.")
    with c2:
        lines = st.toggle("Cell-head lines", value=True, key="show_cell_lines", on_change=keep_head_style,
            args=("show_cell_lines", "show_cell_heads"), help="Horizontal segments span each cell; at least one head style stays active.")
    stride = display_stride(s.n)
    st.caption("Every node symbol is plotted; segments and wetted filling retain all cells." if stride == 1 else
        f"For visualization, one node symbol is plotted every {stride} cells, plus both end nodes. Segments and wetted filling retain all cells.")
    if s.nlay > 1:
        st.caption(TEXT["surface_note"])
    if not s.analytical_available:
        st.caption("The analytical reference is unavailable for layered or heterogeneous models. Native balance and convergence diagnostics remain available.")
    return dict(analytical=analytical and s.analytical_available, initial=initial,
                cell_heads=dots, cell_lines=lines), old


def render_computed_map(s, last, same):
    if not s.horizontal_2d:
        return
    style_computed_map(last is not None and not same)
    with st.container(key="results_head_map"):
        with st.container(key="head_map_panel"):
            with st.expander(TEXT["head_map_title"]):
                if last is None:
                    st.session_state.pop("head_map_cache", None)
                    st.caption(TEXT["map_empty"])
                    return
                if last["heads"] is None:
                    st.session_state.pop("head_map_cache", None)
                    st.info("The latest run has no readable head output.")
                    return
                map_s = Scenario(**last["scenario"])
                st.caption(f"Run {last['run_id']:02d}: {last['run_name']} · {last['status']}")
                if not same:
                    st.caption(TEXT["map_stale"])
                if not last["success"]:
                    st.warning("This run did not converge. These heads are not a converged solution.")
                cache = st.session_state.setdefault("head_map_cache", {})
                st.image(head_map_image(cache, map_s, last["heads"], stale=not same), width="stretch")
                st.caption(TEXT["map_note"])


def initial_grid_notes(s):
    """Dismiss the first-view labels after a scenario edit or any computation."""
    if s != Scenario() or st.session_state.next_run_id > 1 or st.session_state.next_study_id > 1:
        st.session_state.initial_grid_notes_dismissed = True
    return not st.session_state.initial_grid_notes_dismissed


def render_execution(s, cfg, executables, workspace):
    """Reserve plot slots above the controls, then draw once after execution."""
    st.subheader(TEXT["execution_heading"], divider="blue")
    model_summary(s, cfg)
    if cfg.engine == "mfnwt" and ((s.n-2)*s.nrow*s.nlay == 1 or (s.recharge_mmy == 0 and s.left == s.right)):
        st.info("This setup can encounter a native NWT zero-residual / small-system limitation. Any failure is retained as a failed result.")
    if not executables[cfg.engine]:
        st.info(f"{ENGINE_NAMES[cfg.engine]} was not found. Check the shared bin folder or the setup instructions.")
    visibility_slot = st.container(key="result_visibility")
    plot_slot = st.container(key="results_plot")
    note_slot = st.container(key="results_note")
    default_name = f"{ENGINE_NAMES[cfg.engine]} · {cfg.method} · {s.total_cells} cells · run {st.session_state.next_run_id:02d}"
    name_column, repeats_column = st.columns([3, 1], vertical_alignment="bottom")
    with name_column:
        name = st.text_input("Individual run name (optional)", placeholder=default_name, key="run_name")
    with repeats_column:
        repeats = st.selectbox("Number of runs", list(range(1, 11)), index=0, key="repeats", help=TEXT["repeat_help"])
    model_signature = fingerprint(dict(scenario=asdict(s), solver=asdict(cfg), executable=executables[cfg.engine]))
    signature = fingerprint(dict(model=model_signature, repeats=repeats, timeout=TIMEOUT_SECONDS))
    _, button_column, _ = st.columns([1, 2, 1])
    with button_column, st.container(key="main_run"):
        run = st.button("Run Model", type="primary", width="stretch", disabled=not executables[cfg.engine], key="run")
    if run:
        with st.spinner(f"Running {cfg.label} · {repeats} repeat(s)…"):
            result = execute(s, cfg, Path(workspace)/f"run_{time.time_ns()}", int(repeats), executables)
        result.update(signature=signature, model_signature=model_signature)
        st.session_state.previous_profile = deepcopy(st.session_state.last_profile)
        st.session_state.runs = append_run(st.session_state.runs, result,
            st.session_state.next_run_id, name.strip() or default_name)
        st.session_state.inspect_run = st.session_state.next_run_id
        st.session_state.next_run_id += 1
    last = st.session_state.runs[-1] if st.session_state.runs else None
    same = bool(last and last.get("model_signature") == model_signature)
    previous = st.session_state.previous_profile if same else st.session_state.last_profile
    intro_notes = initial_grid_notes(s)
    with visibility_slot:
        options, show_previous = render_visibility(s, previous)
        if intro_notes:
            st.caption(TEXT["initial_grid_hint"])
    show_fig(head_plot(s, [last] if same else [], settings=cfg, surface=s.nlay > 1,
        previous=previous if show_previous else None, intro_notes=intro_notes, **options), plot_slot)
    if same:
        st.session_state.last_profile = profile_snapshot(s, last, surface=s.nlay > 1)
        note_slot.caption(f"Run {last['run_id']:02d}: {last['run_name']} · {last['status']}")
    elif last:
        note_slot.caption("Inputs have changed. The section previews the current setup; computed runs remain in the table.")
    else:
        note_slot.caption("Current setup. Run the model to obtain MODFLOW heads.")
    if show_previous and previous is not None:
        view = "groundwater surface" if previous.get("surface", False) else f"layer {previous['layer']}"
        note_slot.caption(f"Hollow symbols: saved section from run {previous['run_id']:02d}, {view}, middle cell y {previous['cell_y']}.")
    # Intentionally below the run button, not above it.
    render_computed_map(s, last, same)
    return int(repeats)

def render_run_comparison():
    st.subheader(TEXT["comparison_heading"], divider="blue")
    runs = st.session_state.runs
    if not runs:
        st.caption("Your computations will appear here. The table retains up to the latest ten runs.")
    else:
        full_table = run_table(runs)
        # run_repeated sets success=False if any repetition fails, even if the last succeeds.
        display = full_table.assign(Convergence=["✓" if r["success"] else "✗" for r in runs])[[
            "Run", "Name", "Outer iterations", "Inner iterations", "Process time (s)", "Budget discrepancy (%)", "Convergence",
            "Aquifer", "Grid (x × y × layers)", "Cells", "Model / solver", "SIP iterations", "RMSE (m)", "Max error (m)"
        ]].rename(columns={"Outer iterations": "Outer", "Inner iterations": "Inner", "SIP iterations": "SIP",
                           "Process time (s)": "Time (s)", "Budget discrepancy (%)": "WB discrep."})
        show_table(display, key="comparison_table")
        st.caption(f"{len(runs)}/{MAX_RUNS} retained runs. A new run replaces the oldest once the table is full. "
                   "Outer, inner and SIP counts describe different work. Time is the median; counts and errors are from the last repeat. "
                   "Convergence: ✓ = all repetitions succeeded; ✗ = at least one failed. WB discrep. = water-budget discrepancy (%). "
                   "RMSE excludes the fixed-head cells and is only shown where an analytical reference applies. "
                   "het. = heterogeneous hydraulic conductivity.")
        labels = {r["run_id"]: f"{r['run_id']:02d} · {r['run_name']}" for r in runs}
        if "delete_selection" in st.session_state:
            st.session_state.delete_selection = [rid for rid in st.session_state.delete_selection if rid in labels]
        selected_delete = st.multiselect("Select runs to remove", list(labels), format_func=labels.get, key="delete_selection")
        if st.button("Remove selected runs", disabled=not selected_delete, key="remove_runs"):
            st.session_state.runs = remove_runs(runs, selected_delete)
            for name in ("last_profile", "previous_profile"):
                saved = st.session_state[name]
                if saved is not None and saved["run_id"] in selected_delete:
                    st.session_state[name] = None
            # Remove widget selections before the following run recreates its options.
            st.session_state.pop("delete_selection", None)
            st.rerun()
        st.download_button("Download comparison CSV", formatted_csv(full_table), "modflow_comparison.csv", "text/csv")



def render_diagnostics(plot_layer=0):
    if "pending_inspect" in st.session_state:
        st.session_state.inspect_run = st.session_state.pop("pending_inspect")
    with st.container(key="diagnostics_panel"), st.expander("**Head errors, water balance and convergence diagnostics**"):
        if not st.session_state.runs and not st.session_state.diagnostic_extra:
            st.caption("Run a model to inspect its errors, budget and native convergence information.")
        else:
            runs = st.session_state.runs + ([st.session_state.diagnostic_extra] if st.session_state.diagnostic_extra else [])
            by_id = {r["run_id"]: r for r in runs}
            if st.session_state.get("inspect_run") not in by_id:
                st.session_state.pop("inspect_run", None)
            inspect_id = st.selectbox("Run to inspect", list(by_id), index=None if "inspect_run" in st.session_state else len(runs)-1,
                format_func=lambda rid: by_id[rid]['run_name'] if rid < 0 else f"{rid:02d} · {by_id[rid]['run_name']}", key="inspect_run")
            r = by_id[inspect_id]
            rs, rcfg = Scenario(**r["scenario"]), Solver(**r["solver"])
            if r["success"]:
                st.caption("The native stopping criteria were met in every repeat.")
            else:
                st.error(r["status"] + ". Any available heads remain marked as a failed result.")
            if r.get("read_error"):
                st.caption("Native output could not be evaluated: " + r["read_error"])
            if r.get("native_fpe"):
                st.error("The executable reported a native floating-point error. No substitute solution was calculated.")
            show_fig(error_plot(rs, [r]))
            if rs.complexity and r["heads"] is not None:
                with st.expander("**Layer heads and geometry**"):
                    show_fig(model_preview(rs, "Computed heads", heads=r["heads"],
                                       layer=min(plot_layer, rs.nlay-1), row=rs.nrow//2))
                    st.caption("The plan uses the uppermost wet-cell head; the section colours retain native layer heads. Blank section cells are dry or inactive. Orange cells mark specified heads.")
            metric_frame = pd.DataFrame([dict(
                **{"RMSE (m)": r["metrics"].get("rmse_m"), "Max error (m)": r["metrics"].get("max_error_m"),
                   "Max cell residual (m³/s)": r["metrics"].get("max_residual_m3s"),
                   "Budget discrepancy (%)": r["budget_percent"],
                   "Left inflow (m³/s)": r["metrics"].get("qleft_m3s"),
                   "Right inflow (m³/s)": r["metrics"].get("qright_m3s"),
                   "Recharge (m³/s)": r["metrics"].get("recharge_m3s"),
                   "Balance (m³/s)": r["metrics"].get("balance_m3s"),
                   "Min time (s)": r.get("wall_min_s"), "Max time (s)": r.get("wall_max_s"), "Repeats": r.get("repeats", 1)})])
            show_table(metric_frame)
            if rs.confined and not rs.complexity:
                st.caption("Fluxes are positive into the unknown-head region. The independent residual uses the requested physical inputs; "
                           "legacy input rounding can leave a small residual. A printed budget discrepancy of 0.00% does not prove exact balance.")
            else:
                st.caption("Fluxes are positive into the unknown-head region. Cell residuals combine native face flows with actual native recharge placement, "
                           "so they respect each engine's variable transmissivity. A printed budget discrepancy of 0.00% does not prove exact balance.")
            if r["history"]:
                if r.get("history_sampled"):
                    st.caption("This long solve has a sampled inner-iteration history (up to 20,000 points). Native total iteration counts are unchanged.")
                kinds = list(dict.fromkeys(v["kind"] for v in r["history"]))
                kind = st.selectbox("Iteration level", kinds, key=f"iteration_kind_{inspect_id}")
                show_fig(convergence_plot(r["history"], kind, solver=rcfg))
                st.caption(TEXT["convergence_guides"])
                history = pd.DataFrame([v for v in r["history"] if v["kind"] == kind])
                show_table(history)
                st.caption("Zero values are omitted from the logarithmic plots and retained in the table. "
                           "The confined problem is linear; convertible flow generally needs more outer iterations. NWT reports its residual at its own evaluation stage.")
            else:
                st.caption("No recognized iteration history was produced by this run.")
            st.write("Solver settings used for this run")
            show_table(settings_table(rcfg))
            st.caption("For native NWT presets, the reference values describe the tested release; the executable's listing is authoritative.")
            st.download_button("Download native listing", r["listing"], f"run_{inspect_id:02d}_{r['engine']}.lst", "text/plain")
            st.text_area("Program output", r["stdout"], height=160, key=f"stdout_{inspect_id}")
            if r["heads"] is not None:
                heads = rs.heads_table(r["heads"])
                st.download_button("Download heads CSV", heads.to_csv(index=False, float_format="%.10E"),
                                   f"run_{inspect_id:02d}_heads.csv", "text/csv")

