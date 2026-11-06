"""Shared Streamlit presentation helpers and scoped colours.

Keep styling and table formatting here; model calculations live in core.py.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   APP_STYLE: line 20
#   apply_style: line 71
#   style_computed_map: line 75
#   show_fig: line 85
#   show_table: line 90
# END CODE CONTENTS

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from .settings import INTEGER_COLUMNS, SPACING_COLUMNS

APP_STYLE = """
<style>
.stApp {background-color: #FFFFFF; color: #24364B;}
.block-container {max-width: 800px; padding-top: 2rem;}
header[data-testid="stHeader"] {background: #FFFFFF;}
div[data-testid="stExpander"] {--panel-header: #F7FAFD; border-color: #BCD0E3; background: #FFFFFF; border-radius: 8px;}
div[data-testid="stExpander"] summary {background: var(--panel-header) !important; border-radius: 7px;}
div[data-testid="stExpander"] details[open] > summary {border-radius: 7px 7px 0 0;}
div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {background: #FFFFFF;}
div[data-testid="stCaptionContainer"], div[data-testid="stCaptionContainer"] p {color: #536A81;}
.st-key-scenario_panel div[data-testid="stExpander"] {--panel-header: #EEF7F0; border-color: #9CC9AB;}
.st-key-spatial_panel div[data-testid="stExpander"],
.st-key-study_grid_panel div[data-testid="stExpander"] {--panel-header: #FFF4E8; border-color: #E8BD86;}
.st-key-solver_panel div[data-testid="stExpander"],
.st-key-study_solver_panel div[data-testid="stExpander"] {--panel-header: #EDF6FD; border-color: #97C6E8;}
.st-key-complexity_panel div[data-testid="stExpander"] {--panel-header: #F0F7F8; border-color: #9CC8CF;}
.st-key-diagnostics_panel div[data-testid="stExpander"] {--panel-header: #F1EEF8; border-color: #BDB0D8;}

/* Reuse the physical-parameter and discretization colours in related inputs. */
.st-key-complexity_layers [data-testid="stNumberInputContainer"] {background-color: #FFF4E8;}
.st-key-complexity_conductivity [data-testid="stNumberInputContainer"] {background-color: #EEF7F0;}
.st-key-study_grid_panel [data-testid="stTextInputRootElement"],
.st-key-study_grid_panel [data-testid="stSelectbox"] [role="group"] {background-color: #FFF4E8;}
.st-key-study_solver_panel [data-testid="stMultiSelect"] div[role="group"],
.st-key-study_solver_panel [data-testid="stSelectbox"] [role="group"] {background-color: #EFF2F8;}

/* Solver groups: softly coloured input fields inside otherwise white panels. */
.st-key-solver_identity [data-testid="stSelectbox"] [role="group"] {background-color: #EFF2F8;}
.st-key-solver_closure [data-testid="stNumberInputContainer"] {background-color: #EEE9FA;}
.st-key-solver_iterations [data-testid="stNumberInputContainer"] {background-color: #FCEAF2;}
.st-key-solver_strategy [data-testid="stNumberInputContainer"],
.st-key-solver_strategy [data-testid="stSelectbox"] [role="group"] {background-color: #F3F1DD;}
/* The main spacing field uses explicit non-linear +/- controls. */
.st-key-integer_spacing [data-testid="stNumberInputStepDown"],
.st-key-integer_spacing [data-testid="stNumberInputStepUp"],
.st-key-integer_spacing [data-testid="stNumberInputClearButton"] {display: none;}
.st-key-integer_spacing input::-webkit-inner-spin-button,
.st-key-integer_spacing input::-webkit-outer-spin-button {-webkit-appearance: none; margin: 0;}
.st-key-integer_spacing input {appearance: textfield; -moz-appearance: textfield; text-align: center;}
.st-key-integer_spacing button {padding-left: .25rem; padding-right: .25rem;}
.st-key-model_preview_frame {background: #FCFCFC; border: 5px solid;
 border-color: #F2F5F7 #A9B7C4 #A9B7C4 #F2F5F7; border-radius: 8px;
 padding: .6rem; box-shadow: 4px 5px 9px rgba(35,55,75,.18);}
.st-key-main_run button[kind="primary"] {background: #BD4045; border-color: #BD4045; color: white;}
.st-key-grid_run button[kind="primary"] {background: #BC650D; border-color: #BC650D; color: white;}
.st-key-main_run button[kind="primary"]:hover {background: #A83439; border-color: #A83439;}
.st-key-grid_run button[kind="primary"]:hover {background: #A55305; border-color: #A55305;}
</style>
"""


def apply_style():
    st.markdown(APP_STYLE, unsafe_allow_html=True)


def style_computed_map(stale):
    """Update colour without changing the expander's identity or open state."""
    header, border = ("#E5E7EB", "#ACB3BC") if stale else ("#E6F3FA", "#96BCD5")
    st.markdown(f"""<style>
    .st-key-results_head_map div[data-testid="stExpander"] {{
        --panel-header: {header}; border-color: {border};
    }}
    </style>""", unsafe_allow_html=True)


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

