"""MODFLOW Solver Lab — application composition.

Run: python -m streamlit run app.py
Presentation text: content.py. Input panels: inputs.py. Results: results.py.
Native model construction, solver behavior and output reading remain in core.py.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   initialize_session: line 62
#   retain_comparable_runs: line 79
#   1 — Introduction and numerical background. Edit prose in content.py.: line 101
#   2 — Scenario, spatial discretization and numerical solver inputs.: line 112
#   3 — Additional complexity and live preview use the current validated inputs.: line 132
#   4 — Execution, plotted heads, run comparison and native diagnostics.: line 145
#   5 — Grid refinement is an independent subsection with a reviewable plan.: line 150
#   6 — Conclusion and primary documentation.: line 153
# END CODE CONTENTS

from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
import tempfile
import sys

import streamlit as st

# Support both direct local execution and the repository-root cloud launcher.
if not __package__:
    package_parent = str(Path(__file__).resolve().parent.parent)
    if package_parent in sys.path:
        sys.path.remove(package_parent)
    sys.path.insert(0, package_parent)
    __package__ = "MODFLOW_Solver_lab"

# Report a partial content update visibly, rather than a redacted ImportError.
try:
    from . import content as teaching
except ImportError:
    st.error("Incomplete Solver Lab upload: content.py could not be loaded. "
             "Replace the complete MODFLOW_Solver_lab folder from the latest ZIP, then reboot the app.")
    st.stop()
required_text = ("INTRODUCTION", "SOLVER_DETAILS", "ASSUMPTIONS", "REFERENCES", "CONCLUSION", "TEXT")
missing_text = [name for name in required_text if not hasattr(teaching, name)]
if missing_text:
    st.error("The uploaded Solver Lab files are from different releases. content.py is missing: "
             + ", ".join(missing_text) + ". Replace the complete MODFLOW_Solver_lab folder "
             "from the latest ZIP, then reboot the app.")
    st.stop()
from .content import INTRODUCTION, SOLVER_DETAILS, ASSUMPTIONS, REFERENCES, CONCLUSION, TEXT
from .controls import expert_controls
from .core import ENGINE_NAMES, Scenario, find_executable
from .inputs import (capture_input_values, scenario_controls, spatial_controls,
                    solver_controls, complexity_controls, render_model_preview)
from .results import render_execution, render_run_comparison, render_diagnostics
from .settings import (default_variants, GRID_DEFAULTS, capture_active_profile,
                      remember_main_controls, solver_from_profile)
from .studies import render_grid_study
from .ui import apply_style


def initialize_session():
    """Keep durable input values separate from Streamlit's conditional widgets."""
    defaults = dict(profiles={}, variants=default_variants(), choices={}, runs=[], next_run_id=1,
        studies=[], next_study_id=1, grid_entries=[str(v) for v in GRID_DEFAULTS],
        diagnostic_extra=None, last_profile=None, previous_profile=None, initial_grid_notes_dismissed=False,
        complexity_options=dict(horizontal_2d=False, add_layers=False, layers=3, random_k=False,
            k_min=1e-5, k_max=1e-3, k_seed=42, k_zones=11))
    for name, value in defaults.items():
        if name not in st.session_state:
            st.session_state[name] = value
    if "workdir" not in st.session_state:
        st.session_state.workdir = tempfile.TemporaryDirectory(prefix="modflow_solver_lab_")
    capture_active_profile(st.session_state)
    capture_input_values()
    return Path(st.session_state.workdir.name)


def retain_comparable_runs(scenario):
    """Only horizontal dimension/extent changes reset the existing run book."""
    group = scenario.comparison_group
    if st.session_state.get("comparison_group", group) != group:
        had_results = bool(st.session_state.runs or st.session_state.diagnostic_extra)
        st.session_state.runs = []
        st.session_state.diagnostic_extra = None
        st.session_state.last_profile = None
        st.session_state.previous_profile = None
        st.session_state.pop("head_map_cache", None)
        for key in ("inspect_run", "delete_selection"):
            st.session_state.pop(key, None)
        if had_results:
            st.info("The horizontal dimension or extent changed. The run comparison has been reset for this setup.")
    st.session_state.comparison_group = group


st.set_page_config(page_title="MODFLOW Solver Lab", page_icon="💧", layout="centered")
apply_style()
workspace = initialize_session()
executables = {engine: find_executable(engine) for engine in ENGINE_NAMES}

# 1 — Introduction and numerical background. Edit prose in content.py.
st.title("Finite-difference/Finite-volume scheme: MODFLOW solvers")
st.subheader("Groundwater flow with uniform recharge", divider="blue")
st.markdown("### Introduction and Motivation")
st.markdown(INTRODUCTION)
with st.expander(":blue[**Equations, assumptions and suggested experiments**]"):
    st.markdown(ASSUMPTIONS)
with st.expander(":blue[**Details of the numerical solvers**]"):
    st.markdown(SOLVER_DETAILS)


# 2 — Scenario, spatial discretization and numerical solver inputs.
st.subheader("Input values", divider="blue")
st.markdown(TEXT["input_intro"])
complexity = st.toggle("Enable additional model complexity", value=False, key="complexity",
    help="Reveal horizontal 2D grids, layers, random conductivity and a model preview.")
scenario_column, grid_column, solver_column = st.columns(3)
with scenario_column:
    scenario_values = scenario_controls()
with grid_column:
    geometry, grid_error = spatial_controls(complexity)
with solver_column:
    profile_id, profile = solver_controls()
if profile["expert_enabled"]:
    with st.expander(f"**Expert settings · {ENGINE_NAMES[profile['engine']]} / {profile['method']}**", expanded=True):
        expert_controls(profile, profile_id)
st.session_state.profiles[profile_id] = deepcopy(profile)
remember_main_controls(st.session_state, profile)
cfg = solver_from_profile(profile)
st.session_state.variants[f"{cfg.engine}/{cfg.method}"] = asdict(cfg)

# 3 — Additional complexity and live preview use the current validated inputs.
complex_values, preview_slot = complexity_controls(complexity)
s = Scenario(**scenario_values, **geometry, **complex_values)
try:
    if grid_error:
        st.stop()
    s.validate()
except ValueError as error:
    st.error(str(error))
    st.stop()
retain_comparable_runs(s)
preview_layer = render_model_preview(s, preview_slot)

# 4 — Execution, plotted heads, run comparison and native diagnostics.
repeats = render_execution(s, cfg, executables, workspace)
render_run_comparison()
render_diagnostics(preview_layer)

# 5 — Grid refinement is an independent subsection with a reviewable plan.
render_grid_study(s, cfg, profile, executables, workspace, repeats)

# 6 — Conclusion and primary documentation.
st.subheader(TEXT["conclusion_heading"], divider="blue")
st.markdown(CONCLUSION)
with st.expander(TEXT["references_title"]):
    st.markdown(REFERENCES)
st.divider()
st.caption(TEXT["footer"])
