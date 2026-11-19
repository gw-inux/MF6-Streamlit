"""MWW01 transport lab.

Contents
1. Page and language     2. Experiment and model inputs
3. Execution            4. Results and comparison
"""
from pathlib import Path

import streamlit as st

from .transport_lab.content import LANGUAGES, load_text
from .transport_lab.controls import model_inputs, show_preview
from .transport_lab.engine import RunError, find_engines, run_case
from .transport_lab.introduction import show_introduction
from .transport_lab.results import add_variant, render_results
from .transport_lab.scenario import MAX_VARIANTS

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="MWW01 · MT3DMS", layout="centered")
st.markdown("<style>" + (ROOT / "assets" / "lab.css").read_text(encoding="utf-8") + "</style>",
            unsafe_allow_html=True)
st.session_state.setdefault("history", [])
st.session_state.setdefault("next_number", 1)

_, language_slot = st.columns([3, 1])
language = language_slot.selectbox("Language / Sprache", list(LANGUAGES),
                                   format_func=LANGUAGES.get, key="language")
txt = load_text(language)
if language == "ar":
    st.markdown("""<style>
    .stMain [data-testid="stMarkdownContainer"], .stMain [data-testid="stWidgetLabel"] {
        direction: rtl; text-align: right;
    }
    .stMain .katex, .stMain .katex-display, .stMain [data-testid="stDataFrame"] {
        direction: ltr; text-align: initial;
    }
    </style>""", unsafe_allow_html=True)
st.title(txt["title"])
show_introduction(txt, language)

with st.container(key="experiments"), st.expander(f'**{txt["experiments"]}**'):
    tabs = st.tabs([txt["experiment_front"], txt["experiment_spreading"], txt["experiment_impulse"]])
    for tab, key in zip(tabs, ("front_task", "spreading_task", "impulse_task")):
        with tab:
            st.markdown(txt[key])
with st.expander(txt["theory_title"]):
    st.markdown(txt["theory"])

case = model_inputs(txt)
if st.session_state.pop("comparison_cleared", False):
    st.info(txt["comparison_cleared"])
show_preview(case, txt, language)
name = st.text_input(txt["optional_name"], placeholder=txt["name_example"], max_chars=40, key="label")
full = len(st.session_state.history) >= MAX_VARIANTS
if full:
    st.info(txt["limit"])
engines = find_engines()
missing = [label for key, label in (("flow", "MODFLOW-2005"), ("transport", "MT3DMS")) if not engines[key]]
if missing:
    st.info(txt["missing"].format(names=", ".join(missing)))
_, action, _ = st.columns([1, 1.4, 1])
clicked = action.button(txt["run"], type="primary", width="stretch",
                        disabled=full or bool(missing), key="run_model")
if clicked and not full and not missing:
    try:
        with st.spinner(txt["running"]):
            result = run_case(case, engines=engines)
        add_variant(result, name.strip())
        if len(st.session_state.history) == MAX_VARIANTS:
            st.rerun()
        st.success(txt["saved"].format(number=st.session_state.history[-1].number))
    except (RunError, OSError, ValueError) as error:
        st.error(txt["failed"])
        with st.expander(txt["diagnostic"], expanded=True):
            st.code(str(error), language=None)

render_results(txt, language)
with st.expander(txt["references_title"]):
    st.markdown(txt["references"])
