"""Streamlit teaching app, v1.9. Start from this folder: python -m streamlit run app.py

Contents: 1 Introduction · 2 Three input columns · 3 Expert/timing options
          4 Head plot and Run · 5 Ten-run table · 6 Diagnostics · 7 Grid studies
Confined flow is the default; convertible flow uses a separate formulation.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   keep_head_style: line 69
#   show_fig: line 79
#   show_table: line 84
#   execute: line 111
#   render_main_plot: line 123
#   1 — Edit INTRODUCTION in content.py to replace the placeholder prose.: line 160
#   2 — Match the three-column organisation of the manual numerical app.: line 178
#   Scenario parameters and starting heads: line 185
#   Spatial discretization: line 216
#   Numerical solver controls: line 247
#   3 — Expert options and timing stay below the input columns, hidden initially.: line 264
#   Additional complexity and preview controls: line 274
#   Options for numerical model execution: line 300
#   Scenario construction, validation and comparison retention: line 313
#   4 — Persistent plot containers, execution, and visibility controls.: line 374
#   First-layer postprocessing for horizontal 2D and layered horizontal models: line 433
#   5 — Exactly one named, bounded run collection. Repeats do not create extra rows.: line 454
#   6 — Additional diagnostics for any retained run, using that run's own inputs.: line 488
#   7 — Explicit plan, selectable variants, custom cell counts, and repeat studies.: line 554
# END CODE CONTENTS

from copy import deepcopy
from dataclasses import asdict, replace
from pathlib import Path
import tempfile
import time

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from core import MAX_CELLS, ENGINE_NAMES, Scenario, Solver, comparison_row, find_executable, fingerprint, run_repeated
from controls import basic_controls, expert_controls
from content import INTRODUCTION, SOLVER_DETAILS, ASSUMPTIONS, REFERENCES
from settings import (METHODS, VARIANTS, MAX_RUNS, INTEGER_COLUMNS, SPACING_COLUMNS, solver_from_profile,
                      default_variants, variant_plan, settings_table, parse_grid_entries, parse_grid_spacings, GRID_DEFAULTS,
                      append_run, remove_runs, run_table, formatted_csv, capture_active_profile,
                      select_profile, remember_main_controls)
from plots import (head_plot, error_plot, convergence_plot, grid_study_plot,
                   model_preview, first_layer_head_map, display_stride, profile_snapshot)

st.set_page_config(page_title="Finite differences · MODFLOW solvers", page_icon="💧", layout="centered")
st.markdown("""<style>
.stApp {background-color: #FFFFFF; color: #24364B;}
.block-container {max-width: 800px; padding-top: 2rem;}
header[data-testid="stHeader"] {background: #FFFFFF;}
div[data-testid="stExpander"] {--panel-header: #F7FAFD; border-color: #BCD0E3; background: #FFFFFF; border-radius: 8px;}
div[data-testid="stExpander"] summary {background: var(--panel-header) !important; border-radius: 7px;}
div[data-testid="stExpander"] details[open] > summary {border-radius: 7px 7px 0 0;}
div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {background: #FFFFFF;}
div[data-testid="stCaptionContainer"], div[data-testid="stCaptionContainer"] p {color: #536A81;}
.st-key-scenario_panel div[data-testid="stExpander"] {--panel-header: #EEF7F0; border-color: #9CC9AB;}
.st-key-spatial_panel div[data-testid="stExpander"] {--panel-header: #FFF4E8; border-color: #E8BD86;}
.st-key-solver_panel div[data-testid="stExpander"] {--panel-header: #EDF6FD; border-color: #97C6E8;}
.st-key-timing_panel div[data-testid="stExpander"] {--panel-header: #F0F4FC; border-color: #A8BCDF;}
.st-key-complexity_panel div[data-testid="stExpander"] {--panel-header: #F0F7F8; border-color: #9CC8CF;}
</style>""", unsafe_allow_html=True)


def keep_head_style(changed_key, other_key):
    """Switch to the other style when the last active style is turned off.

    Streamlit runs this callback before rebuilding either toggle, so both
    widget values and the figure see the same updated state in one rerun.
    """
    if not st.session_state[changed_key] and not st.session_state.get(other_key, True):
        st.session_state[other_key] = True


def show_fig(fig, target=st):
    target.pyplot(fig, clear_figure=False)
    plt.close(fig)


def show_table(frame, key=None, height=None):
    """Identical formatting conventions in main, diagnostic and study tables."""
    frame = frame.copy()
    config = {}
    for column in frame:
        if column == "Model / solver":
            config[column] = st.column_config.TextColumn(width="medium")
        elif column in INTEGER_COLUMNS:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").astype("Int64")
            config[column] = st.column_config.NumberColumn(format="%d")
        elif column in ("Budget discrepancy (%)", "WB discrep."):
            # Native values already are percentages: append %, without scaling by 100.
            config[column] = st.column_config.NumberColumn(format="%.2f %%", help="Water-budget discrepancy (%)")
        elif column == "Convergence":
            config[column] = st.column_config.TextColumn(width=120, help="✓: all repetitions succeeded; ✗: at least one repetition failed.")
        elif pd.api.types.is_numeric_dtype(frame[column]):
            fmt = "%.10g" if column in SPACING_COLUMNS else (
                "%.4f" if "time" in column.lower() and "(s)" in column else "%.3e")
            config[column] = st.column_config.NumberColumn(format=fmt)
    options = dict(hide_index=True, width="stretch", column_config=config)
    if key:
        options["key"] = key
    if height:
        options["height"] = height
    st.dataframe(frame, **options)


def execute(scenario, cfg, folder, repeats, timeout):
    try:
        return run_repeated(scenario, cfg, folder, executables[cfg.engine], repeats, timeout)
    except Exception as error:
        # Preserve a failed row rather than silently dropping it from comparisons.
        return dict(engine=cfg.engine, method=cfg.method, label=cfg.label,
            scenario=asdict(scenario), solver=asdict(cfg), success=False, status="Input / output error",
            outer_iterations=None, inner_iterations=None, sip_iterations=None, wall_s=float("nan"),
            heads=None, metrics={}, budget_percent=None, history=[], listing="", repeats=repeats,
            stdout=f"{type(error).__name__}: {error}")


def render_main_plot(last, same, previous):
    """Render once into a stable container; do not clear it during reruns."""
    current = [last] if same else []
    show_fig(head_plot(s, current, analytical=analytical, initial=show_initial,
        settings=cfg, layer=plot_layer, row=plot_row, cell_heads=show_cell_heads,
        cell_lines=show_cell_lines,
        previous=previous if show_previous else None), plot_slot)
    if same:
        st.session_state.last_profile = profile_snapshot(s, last, plot_layer, plot_row)
        plot_note.caption(f"Run {last['run_id']:02d}: {last['run_name']} · {last['status']}")
    elif last:
        plot_note.caption("Inputs have changed. The plot previews the current inputs; previous results remain in the table.")
    else:
        plot_note.caption("Current inputs. Run the computation to obtain MODFLOW heads.")
    if show_previous and previous is not None:
        plot_note.caption(f"Hollow symbols: saved section from run {previous['run_id']:02d}, "
                          f"layer {previous['layer']}, cell y {previous['cell_y']}. Coordinates and heads are retained as displayed.")


# Session-owned state is distinct from transient widget state. This preserves
# hidden solver controls when the user switches models or presets.
defaults = dict(profiles={}, variants=default_variants(), choices={}, runs=[], next_run_id=1,
                studies=[], next_study_id=1, grid_entries=[str(v) for v in GRID_DEFAULTS],
                last_thickness=20., last_aquifer_top=20., diagnostic_extra=None,
                last_profile=None, previous_profile=None,
                complexity_options=dict(horizontal_2d=False, add_layers=False, layers=3, random_k=False,
                    k_min=1e-5, k_max=1e-3, k_seed=42, k_zones=11),
                starting_options=dict(initial_head=17., initial_min=10., initial_max=25., initial_seed=24))
for name, value in defaults.items():
    if name not in st.session_state:
        st.session_state[name] = value
if "workdir" not in st.session_state:
    st.session_state.workdir = tempfile.TemporaryDirectory(prefix="modflow_1d_")
workspace = Path(st.session_state.workdir.name)
capture_active_profile(st.session_state)
executables = {engine: find_executable(engine) for engine in ENGINE_NAMES}

# 1 — Edit INTRODUCTION in content.py to replace the placeholder prose.
st.title("Finite-difference scheme: MODFLOW solvers")
st.subheader("Groundwater flow with uniform recharge", divider="blue")
st.markdown("### Introduction and Motivation")
st.markdown(INTRODUCTION)
with st.expander(":blue[**Details of the numerical solvers**]"):
    st.markdown(SOLVER_DETAILS)
with st.expander(":blue[**Equations, assumptions and suggested experiments**]"):
    st.markdown("**Confined flow**, roof at 0 m and bottom at −b:")
    st.latex(r"T=Kb,\quad T\frac{d^2h}{dx^2}+R=0,\qquad h(0)=h_L,\quad h(L)=h_R")
    st.latex(r"h(x)=h_L+\frac{h_R-h_L}{L}x+\frac{R}{2T}x(L-x)")
    st.latex(r"C(h_{i-1}-2h_i+h_{i+1})+RW\Delta x=0,\qquad C=\frac{KbW}{\Delta x}")
    st.markdown("**Unconfined / convertible flow**, bottom at 0 m:")
    st.latex(r"\frac{d}{dx}\left[K\min(h,z_t)\frac{dh}{dx}\right]+R=0")
    st.caption("For an entirely unconfined profile, including both boundary heads, below the aquifer top:")
    st.latex(r"h(x)=\sqrt{h_L^2+\frac{h_R^2-h_L^2}{L}x+\frac{R}{K}x(L-x)}")
    st.markdown(ASSUMPTIONS)

# 2 — Match the three-column organisation of the manual numerical app.
st.subheader("Input values", divider="blue")
st.write("Define the scenario, grid and solver below. Then run the computation to update the head plot "
         "and add the result to the comparison table.")
complexity = st.toggle("Enable additional model complexity", value=False, key="complexity",
                       help="Reveal horizontal 2-D grids, layers, random hydraulic conductivity and a model preview.")
columns = st.columns(3)
# EDIT: Scenario parameters and starting heads
with columns[0], st.container(key="scenario_panel"):
    with st.expander("**Parameters for the scenario**"):
        confined = st.toggle("Confined aquifer", value=True, key="confined",
                             help="Switch off for unconfined / convertible flow with the bottom fixed at 0 m.")
        thickness = st.session_state.last_thickness
        aquifer_top = st.session_state.last_aquifer_top
        if confined:
            thickness = st.number_input("Aquifer thickness (m)", .1, 1000., thickness, .5, key="thickness")
            st.session_state.last_thickness = thickness
        else:
            aquifer_top = st.number_input("Aquifer top elevation (m)", .1, 1000., aquifer_top, .5, key="aquifer_top")
            st.session_state.last_aquifer_top = aquifer_top
        left = st.number_input("West / left boundary head (m)", .1, 5000., 18., .5, key="left")
        right = st.number_input("East / right boundary head (m)", .1, 5000., 16., .5, key="right")
        recharge = st.number_input("Recharge (mm/year)", 0., 2000., 150., 1., key="recharge")
        k = st.number_input("Hydraulic conductivity (m/s)", 1e-9, 1., 1e-4, format="%.3e", key="k")
        initial = st.selectbox("Starting-head distribution", ["Mean boundary head", "Linear between boundaries", "Specified uniform head", "Random distribution"], key="initial")
        so = deepcopy(st.session_state.starting_options)
        if initial == "Specified uniform head":
            so["initial_head"] = st.number_input("Uniform starting head elevation (m)", .1, 10000., so["initial_head"], .5, key="initial_head")
        elif initial == "Random distribution":
            so["initial_min"] = st.number_input("Minimum initial head (m)", .1, 10000., so["initial_min"], .5, key="initial_min")
            so["initial_max"] = st.number_input("Maximum initial head (m)", .1, 10000., so["initial_max"], .5, key="initial_max")
            so["initial_seed"] = st.number_input("Initial-head seed", 0, 2**31-1, so["initial_seed"], 1, key="initial_seed")
            st.caption("Independent uniform random values between these limits. Specified-head cells always retain their boundary values.")
        st.session_state.starting_options = so
        if confined:
            st.caption("Confined: aquifer roof 0 m; bottom −b. Positive heads keep the aquifer fully saturated.")
        else:
            st.caption("Unconfined / convertible: bottom 0 m; saturated thickness follows the head up to the aquifer top. Above the top, the full layer thickness applies.")
# EDIT: Spatial discretization
with columns[1], st.container(key="spatial_panel"):
    with st.expander("**Spatial discretization**"):
        length = st.number_input("Boundary-to-boundary length (m)", 1., 100000., 5000., 100., key="length")
        horizontal = complexity and st.session_state.get("horizontal_2d", st.session_state.complexity_options["horizontal_2d"])
        spacing_mode = st.toggle("Define cell spacing instead of cell count", value=False, key="spacing_mode")
        last_n = int(st.session_state.get("grid_n", 11))
        if st.session_state.get("previous_spacing_mode", False) != spacing_mode:
            if spacing_mode:
                st.session_state.cell_spacing = length/(last_n-1)
            else:
                st.session_state.n = last_n
        grid_error = None
        if spacing_mode:
            spacing = st.number_input("Cell spacing Δx / Δy (m)" if horizontal else "Cell spacing Δx (m)",
                min_value=.0001, value=None if "cell_spacing" in st.session_state else length/(last_n-1), format="%.6f", key="cell_spacing")
            try:
                n = parse_grid_spacings([spacing], length)[0]
            except ValueError as error:
                grid_error = str(error)
                n = last_n
                st.error(grid_error)
        else:
            n = st.number_input("Number of cells along x and y" if horizontal else "Number of cells along x",
                3, 10001, None if "n" in st.session_state else last_n, 1, key="n", help="Includes both fixed-head end cells.")
        if grid_error is None:
            st.session_state.grid_n = int(n)
        st.session_state.previous_spacing_mode = spacing_mode
        width = 1.  # Unit-width cross section; in 2D the core uses Δy = Δx.
        st.write(f"{n} cells along x" + (f" and {n} along y" if horizontal else "") + f" · Δx = {length/(n-1):g} m")
        st.caption("Distance is measured between the centres of the CHD cells. Δx = L/(N−1); spacing must divide L exactly. Refinement keeps L fixed.")
# EDIT: Numerical solver controls
with columns[2], st.container(key="solver_panel"):
    with st.expander("**Numerical solver**"):
        engine = st.selectbox("MODFLOW model", list(ENGINE_NAMES), format_func=ENGINE_NAMES.get, key="engine")
        choice = st.session_state.choices.get(engine, dict(preset="SIMPLE", method=METHODS[engine][0]))
        preset = "SIMPLE"
        if engine != "mf2005":
            preset = st.selectbox("Solver preset", ["SIMPLE", "MODERATE", "COMPLEX"],
                                  index=["SIMPLE", "MODERATE", "COMPLEX"].index(choice["preset"]), key=f"preset_{engine}")
        method = st.selectbox("Solver" if engine == "mf2005" else "Linear solver", METHODS[engine],
                              index=METHODS[engine].index(choice["method"]), key=f"method_{engine}")
        st.session_state.choices[engine] = dict(preset=preset, method=method)
        profile_id, profile = select_profile(st.session_state, engine, method, preset)
        basic_controls(profile, profile_id)
        st.caption("Main closure and iteration limits stay unchanged when switching presets or linear solvers. Each MODFLOW model remembers its own values.")
        st.caption("Head closure is in metres. R closure is a flow criterion in m³/s; its value and test differ between solvers.")

# 3 — Expert options and timing stay below the input columns, hidden initially.
if profile["expert_enabled"]:
    with st.expander(f"**Expert settings · {ENGINE_NAMES[engine]} / {method}**", expanded=True):
        expert_controls(profile, profile_id)
st.session_state.profiles[profile_id] = deepcopy(profile)
remember_main_controls(st.session_state, profile)
cfg = solver_from_profile(profile)
st.session_state.variants[f"{engine}/{method}"] = asdict(cfg)

# Additional geometry is opt-in. Hidden controls retain their entered values.
# EDIT: Additional complexity and preview controls
co = deepcopy(st.session_state.complexity_options)
if complexity:
    with st.container(key="complexity_panel"), st.expander("**Add Complexity**", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            co["horizontal_2d"] = st.toggle("2D horizontal grid (x–y)", value=co["horizontal_2d"], key="horizontal_2d",
                help="Off: 1D horizontal flow. On: a square grid with Nx = Ny and Δx = Δy; north and south remain no-flow.")
            st.caption("2D horizontal: square x–y grid." if co["horizontal_2d"] else "1D horizontal: one row along x.")
            co["add_layers"] = st.toggle("Add layers", value=co["add_layers"], key="add_layers")
            if co["add_layers"]:
                co["layers"] = st.number_input("Number of layers", 2, 50, co["layers"], 1, key="layers")
                st.caption("Equal layer thicknesses across the aquifer. Recharge enters the highest wet active cell; vertical flow connects the layers.")
        with c2:
            co["random_k"] = st.toggle("Random hydraulic-conductivity field", value=co["random_k"], key="random_k")
            if co["random_k"]:
                co["k_min"] = st.number_input("Minimum K (m/s)", 1e-9, 1., co["k_min"], format="%.3e", key="k_min")
                co["k_max"] = st.number_input("Maximum K (m/s)", 1e-9, 1., co["k_max"], format="%.3e", key="k_max")
                co["k_seed"] = st.number_input("K-field seed", 0, 2**31-1, co["k_seed"], 1, key="k_seed")
                co["k_zones"] = st.number_input("K zones per horizontal direction", 1, 100, co["k_zones"], 1, key="k_zones")
                st.caption("Log-uniform K in fixed spatial zones, independent in each layer. K is isotropic. The same seed and zones retain the same physical field during grid refinement.")
        st.caption("Specified heads remain uniform on the wet west/east faces. North, south and the aquifer bottom have no flow. "
                   "Layered unconfined models omit boundary cells that lie wholly above the specified water level.")
        complexity_preview = st.container()
    st.session_state.complexity_options = co

# EDIT: Options for numerical model execution
with st.container(key="timing_panel"), st.expander("**Options for numerical model execution**"):
    c1, c2 = st.columns(2)
    with c1:
        repeats = st.number_input("Independent repeats per configuration", 1, 10, 1, key="repeats")
    with c2:
        timeout = st.number_input("Timeout per engine run (seconds)", 1, 300, 60, key="timeout")
    st.caption("Each repeat starts a fresh model run with the same inputs and random seeds. One table entry represents the group of repeats. "
               "Runtime is the median process wall time, including startup and native output; input generation and plotting are excluded.")

if grid_error is not None:
    st.stop()

# EDIT: Scenario construction, validation and comparison retention
s = Scenario(n=int(n), length=length, thickness=thickness, k_ms=k, recharge_mmy=recharge,
             left=left, right=right, width=width, initial=initial, **so,
             confined=confined, aquifer_top=aquifer_top, complexity=complexity,
             horizontal_2d=complexity and co["horizontal_2d"],
             nlay=int(co["layers"]) if complexity and co["add_layers"] else 1,
             random_k=complexity and co["random_k"],
             **{key: co[key] for key in ("k_min", "k_max", "k_seed", "k_zones")})
try:
    s.validate()
except ValueError as error:
    st.error(str(error))
    st.stop()

group = s.comparison_group
if st.session_state.get("comparison_group", group) != group:
    had_results = bool(st.session_state.runs or st.session_state.diagnostic_extra)
    st.session_state.runs = []
    st.session_state.diagnostic_extra = None
    st.session_state.last_profile = None
    st.session_state.previous_profile = None
    for key in ("inspect_run", "delete_selection"):
        st.session_state.pop(key, None)
    if had_results:
        st.info("The horizontal dimension or extent changed. The run comparison has been reset for this setup.")
st.session_state.comparison_group = group
plot_layer, plot_row = 0, s.nrow//2
if complexity:
    with complexity_preview:
        st.markdown("**Model preview**")
        preview_columns = st.columns(2)
        with preview_columns[0]:
            quantity = st.selectbox("Preview", ["Empty cells", "K zones", "Initial heads"], key="preview_quantity")
        with preview_columns[1]:
            if st.session_state.get("plot_layer", 1) > s.nlay:
                st.session_state.plot_layer = 1
            plot_layer = st.number_input("Layer to display", 1, s.nlay, 1, key="plot_layer")-1 if s.nlay > 1 else 0
        show_fig(model_preview(s, quantity, layer=plot_layer, row=plot_row))
        st.caption(f"{s.grid_label} · {s.total_cells:,} cells · Δx = {s.dx:g} m · Δy = {s.dy:g} m. "
                   f"Section A–A′ follows middle cell y {plot_row+1}. "
                   "The horizontal 2D view uses equal x/y scales. The vertical scale is exaggerated.")
        if s.random_k and quantity == "K zones":
            bands = s.k_zones if s.k_min < s.k_max else 1
            st.caption(f"K colours use {bands} numbered logarithmic classes; the legend gives each class midpoint. "
                       "These display ranges use the selected zone count without changing any model K value.")
        stride = display_stride(s.n)
        if stride > 1:
            st.caption(f"For visibility, only every {stride}-th horizontal grid line is drawn, plus the domain edges. All cell values are retained.")
transmissivity_label = "Transmissivity" if confined else "Fully saturated transmissivity limit"
caption = f"Grid: {s.grid_label} · {s.total_cells:,} cells · Δx = {s.dx:g} m"
if not s.random_k:
    caption += f" · {transmissivity_label}: {s.transmissivity:.3E} m²/s"
st.write(caption)
st.caption("Model time unit: seconds. Conductivity and recharge calculations use m/s; flow residuals and water balances use m³/s. Recharge input remains mm/year.")
if cfg.engine == "mfnwt" and ((s.n-2)*s.nrow*s.nlay == 1 or (s.recharge_mmy == 0 and s.left == s.right)):
    st.info("This setup can encounter a native NWT zero-residual / small-system limitation. See the explanation above; "
            "any failure will be retained as a failed result.")
if not executables[engine]:
    st.info(f"{ENGINE_NAMES[engine]} was not found. Use your existing bin folder or PATH; the README also explains "
            "the executable environment variables and installer.")

# 4 — Persistent plot containers, execution, and visibility controls.
# Containers keep the previous image in place until one replacement is ready.
# In particular, do not call st.empty() here: it sends an explicit blank delta.
signature = fingerprint(dict(scenario=asdict(s), solver=asdict(cfg), executable=executables[engine], repeats=repeats, timeout=timeout))
visibility_slot = st.container(key="result_visibility")
plot_slot = st.container(key="results_plot")
plot_note = st.container(key="results_note")
head_map_slot = st.container(key="results_head_map")
default_name = f"{ENGINE_NAMES[engine]} · {method} · {s.total_cells} cells · run {st.session_state.next_run_id:02d}"
run_name = st.text_input("Individual run name (optional)", placeholder=default_name, key="run_name",
                         help="Leave blank to use the generated name. Run numbers remain unique even if names are reused.")
_, run_column, _ = st.columns([1, 2, 1])
with run_column:
    run = st.button("Run the computation", type="primary", width="stretch", disabled=not executables[engine], key="run")
if run:
    folder = workspace / f"run_{time.time_ns()}"
    with st.spinner(f"Running {cfg.label} · {repeats} repeat(s)…"):
        result = execute(s, cfg, folder, int(repeats), float(timeout))
    result["signature"] = signature
    st.session_state.previous_profile = deepcopy(st.session_state.last_profile)
    st.session_state.runs = append_run(st.session_state.runs, result, st.session_state.next_run_id, run_name.strip() or default_name)
    st.session_state.inspect_run = st.session_state.next_run_id
    st.session_state.next_run_id += 1

last = st.session_state.runs[-1] if st.session_state.runs else None
same = bool(last and last["signature"] == signature)
# During input editing, compare the new preview to the latest completed run.
# After a new computation, compare that run to its saved predecessor.
previous = st.session_state.previous_profile if same else st.session_state.last_profile
with visibility_slot:
    c1, c2, c3 = st.columns(3)
    with c1:
        analytical = st.toggle("Show analytical solution", value=False, key="analytical", disabled=not s.analytical_available)
    with c2:
        show_initial = st.toggle("Show initial heads", value=False, key="show_initial",
            help="Hides this curve and excludes it from axis scaling. Starting heads used by the solver are unchanged.")
    with c3:
        show_previous = st.toggle("Show previous run", value=False, key="show_previous", disabled=previous is None,
            help="Show saved section heads as hollow symbols. During input editing this is the latest completed run.")
    c1, c2 = st.columns(2)
    # Recover an invalid old session before either widget is instantiated.
    if not st.session_state.get("show_cell_heads", True) and not st.session_state.get("show_cell_lines", True):
        st.session_state.show_cell_lines = True
    with c1:
        show_cell_heads = st.toggle("Cell-head dots", value=True, key="show_cell_heads",
            on_change=keep_head_style, args=("show_cell_heads", "show_cell_lines"),
            help="If this is the last active style, switching it off turns the horizontal lines on.")
    with c2:
        show_cell_lines = st.toggle("Cell-head lines", value=True, key="show_cell_lines",
            on_change=keep_head_style, args=("show_cell_lines", "show_cell_heads"),
            help="Horizontal segments span individual cells. Switching off the last active style turns the dots on.")
    stride = display_stride(s.n)
    node_note = ("For visualization, every node symbol is plotted. " if stride == 1 else
                 f"For visualization, one node symbol is plotted every {stride} cells, plus both end nodes. ")
    st.caption(node_note + "The interval follows the cell count. Cell-head segments and wetted-cell filling retain all cells.")
    if not s.analytical_available:
        st.caption("Analytical head errors are unavailable for layered or heterogeneous models. Native convergence and water-balance diagnostics remain available.")
render_main_plot(last, same, previous)

# EDIT: First-layer postprocessing for horizontal 2D and layered horizontal models
with head_map_slot:
    if s.horizontal_2d:
        with st.expander("**Computed heads · first layer (x–y)**"):
            if last is None:
                st.caption("Run the computation to view the first-layer heads.")
            elif last["heads"] is None:
                st.info("The latest run has no readable head output.")
            else:
                map_s = Scenario(**last["scenario"])
                st.caption(f"Run {last['run_id']:02d}: {last['run_name']} · {last['status']} · layer 1")
                if not same:
                    st.caption("Inputs have changed. This map retains the latest computed model; run again to update it.")
                if not last["success"]:
                    st.warning("This run did not converge. These heads are not a converged solution.")
                show_fig(first_layer_head_map(map_s, last["heads"]))
                st.caption("Native cell heads in layer 1; dry or inactive cells are blank. Orange outlines mark CHD cells. "
                           "The dashed line marks the middle section A–A′. Both horizontal axes use the same scale.")
                if display_stride(map_s.n) > 1:
                    st.caption(f"Only every {display_stride(map_s.n)}-th horizontal grid line is drawn, plus the domain edges. All cell heads are retained.")

# 5 — Exactly one named, bounded run collection. Repeats do not create extra rows.
st.subheader("Run comparison", divider="blue")
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

# 6 — Additional diagnostics for any retained run, using that run's own inputs.
if "pending_inspect" in st.session_state:
    st.session_state.inspect_run = st.session_state.pop("pending_inspect")
with st.expander("**Head errors, water balance and convergence diagnostics**"):
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
            show_fig(model_preview(rs, "Computed heads", heads=r["heads"],
                                   layer=min(plot_layer, rs.nlay-1), row=rs.nrow//2))
            st.caption("Computed heads: blank cells are dry or inactive. Orange cells mark specified heads.")
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
            show_fig(convergence_plot(r["history"], kind))
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

# 7 — Explicit plan, selectable variants, custom cell counts, and repeat studies.
with st.expander("**Grid-refinement experiment**"):
    st.write("This experiment demonstrates the scalability of the script-based approach: the same model-building code "
             "generates, runs and evaluates several grids. It also explores how solver effort changes with cell count. "
             "The boundary-to-boundary length stays fixed. The confined quadratic benchmark has no nodal truncation error in exact arithmetic; "
             "unconfined results also depend on the engine's conductance approximation and grid spacing.")
    st.caption("Each selected model/solver variant is run once for every grid, with the number of independent repeats "
               "defined in Options for numerical model execution above. Timings include startup and output, so this is not an isolated solver-speed ranking.")
    variant_labels = {v: Solver(**st.session_state.variants[v]).label for v in VARIANTS}
    chosen = st.multiselect("Model / solver variants to include", VARIANTS, default=[f"{engine}/{method}"] if complexity else VARIANTS, key="complex_grid_variants" if complexity else "grid_variants",
        format_func=variant_labels.get)
    st.caption("The table below lists the exact plan. Unedited variants use their initial settings. "
               "To change a variant, select its model and solver in the input section above and edit its controls. "
               "Each variant retains its most recently selected preset and settings; excluded variants are not run.")
    plan = variant_plan(st.session_state.variants, executables)
    show_table(plan[plan["Variant"].isin(chosen)].drop(columns="Variant"), key="grid_plan")
    if chosen:
        if st.session_state.get("inspect_variant") not in chosen:
            st.session_state.pop("inspect_variant", None)
        inspect_variant = st.selectbox("Show full settings for", chosen, key="inspect_variant",
            format_func=variant_labels.get)
        show_table(settings_table(Solver(**st.session_state.variants[inspect_variant])))
    grid_input = st.selectbox("Grid input", ["Cell counts along x", "Uniform cell spacing (m)"],
                              index=1 if complexity else 0, key=f"grid_input_{complexity}")
    grid_count = st.selectbox("Number of grid sizes", list(range(1, 11)), index=0 if complexity or profile["expert_enabled"] else 2,
                             key="grid_count_complex" if complexity or profile["expert_enabled"] else "grid_count")
    use_spacing = grid_input == "Uniform cell spacing (m)"
    if use_spacing:
        spacing_key = f"spacing_entries_{length}_{s.n}_{s.nlay}_{s.horizontal_2d}"
        if spacing_key not in st.session_state:
            max_count = min(10001, int((MAX_CELLS/s.nlay)**.5) if s.horizontal_2d else MAX_CELLS//s.nlay)
            candidates = [s.n] + list(range(11, min(max_count, 101)+1, 10)) + list(range(3, max_count+1))
            counts = list(dict.fromkeys(candidates))[:10]
            st.session_state[spacing_key] = [f"{length/(count-1):.10g}" for count in counts]
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
    st.caption(f"Each study keeps {s.nlay} layer(s), the same aquifer geometry and boundary heads. "
               "In horizontal 2D each entry sets Δx = Δy. Fixed K zones and their seed stay unchanged.")
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
    unavailable = [v for v in chosen if not executables[v.split('/')[0]]]
    if unavailable:
        st.warning("Exclude variants whose executable is not available before starting this study: " + ", ".join(unavailable))
    study_name = st.text_input("Study name (optional)", placeholder="Grid study", key="study_name")
    calls = len(chosen)*len(sizes)*int(repeats)
    st.caption(f"Study plan: {len(chosen)} variant(s) × {len(sizes)} grid(s) × {repeats} repeat(s) = {calls} native model runs.")
    plan_signature = fingerprint(dict(scenario=asdict(s), variants={v: st.session_state.variants[v] for v in chosen},
                                     sizes=sizes, repeats=repeats, timeout=timeout, executables=executables))
    if st.button("Run grid study", disabled=not chosen or not sizes or bool(unavailable) or grid_error is not None, key="run_grid"):
        rows = []
        folder = workspace / f"study_{time.time_ns()}"
        planned = {v: deepcopy(st.session_state.variants[v]) for v in chosen}
        progress = st.progress(0., text="Preparing grid study…")
        total = len(sizes)*len(chosen)
        for index, (size, variant) in enumerate((size, variant) for size in sizes for variant in chosen):
            vc = Solver(**planned[variant])
            progress.progress(index/total, text=f"{vc.label} · {replace(s, n=size).grid_label} · {repeats} repeat(s)")
            r = execute(replace(s, n=size), vc, folder/str(size)/variant.replace("/", "_"), int(repeats), float(timeout))
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
        saved_variant = st.selectbox("Inspect settings used in this study", list(study["plan"]), key=f"study_settings_{study_id}")
        show_table(settings_table(Solver(**study["plan"][saved_variant])))
        st.download_button("Download grid study CSV", formatted_csv(gt), "grid_study.csv", "text/csv")

with st.expander("**Primary documentation**"):
    st.markdown(REFERENCES)
st.divider()
st.caption("Based on Thomas Reimann’s finite-difference teaching app · TU Dresden, Institute for Groundwater Management · 2026 · v1.9")
