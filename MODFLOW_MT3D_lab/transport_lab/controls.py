"""Streamlit model inputs and preview. All widget values use language-neutral keys."""
import streamlit as st

from .scenario import DEFAULT_SIGNAL, END_TIME, K_MS, LENGTH, METHODS, SIGNALS, VELOCITY, Scenario
from .plots import preview
from .figure_io import show_figure
from .results import clear_variants


def _remembered_number(field, label, low, high, initial, step=1, **kwargs):
    """Retain conditional input values when Streamlit removes a hidden widget."""
    saved = st.session_state.setdefault("conditional_values", {})
    value = st.number_input(label, low, high, saved.get(field, initial), step,
                            key=field, on_change=clear_variants, **kwargs)
    saved[field] = value
    return value


def model_inputs(txt):
    st.subheader(txt["setup"])
    physics, grid, solver = st.columns(3)
    with physics, st.container(key="physics_panel"), st.expander(f'**{txt["inlet_processes"]}**'):
        st.caption(txt["scenario_reset_hint"])
        signal = st.selectbox(txt["signal"], SIGNALS, format_func=lambda k: txt[k],
                              index=SIGNALS.index(DEFAULT_SIGNAL), key="signal", on_change=clear_variants)
        amplitude, block_days, area, impulse_days = 1.0, 400, 50.0, 50
        if signal != "dirac":
            amplitude = _remembered_number("amplitude", txt["amplitude"], 0.05, 10.0, 1.0, 0.05)
        if signal == "block":
            block_days = _remembered_number("block_days", txt["block_days"], 1, int(END_TIME) - 1, 400)
        if signal == "dirac":
            area = _remembered_number("impulse_area", txt["impulse_area"], 0.1, 500.0, 50.0, 1.0)
            impulse_days = _remembered_number("impulse_days", txt["impulse_days"], 1, 500, 50)
            st.caption(txt["rectangle"].format(height=area / impulse_days))
        dispersion = st.toggle(txt["dispersion"], key="dispersion", value=False, on_change=clear_variants)
        al, dm = 0.0, 0.0
        if dispersion:
            al = _remembered_number("dispersivity", txt["dispersivity"], 0.0, 100.0, 10.0, 0.5)
            dm = _remembered_number("diffusion", txt["diffusion"], 0.0, 1.0, 0.0, 0.0001, format="%.5f")
    with grid, st.container(key="grid_panel"), st.expander(f'**{txt["grid_time"]}**'):
        mode = st.radio(txt["grid_by"], ["cells", "spacing"], horizontal=True,
                        format_func=lambda k: txt[k], key="grid_by")
        previous = st.session_state.get("grid_cells", 21)
        if mode == "cells":
            ncol = st.number_input(txt["cell_count"], 11, 501, previous, step=1, key="ncol")
        else:
            target = st.number_input(txt["target_spacing"], 2.0, 100.0, LENGTH / (previous - 1), 0.5, key="spacing")
            ncol = int(LENGTH / target + 0.5) + 1
        st.session_state.grid_cells = ncol
        st.caption(txt["grid_summary"].format(n=ncol, dx=LENGTH / (ncol - 1)))
        courant = st.slider(txt["courant"], 0.1, 1.0, 0.5, 0.05, key="courant")
        st.caption(txt["time_hint"])
    with solver, st.container(key="solver_panel"), st.expander(f'**{txt["solver"]}**'):
        method = st.selectbox(txt["scheme"], list(METHODS), format_func=lambda k: txt[k], key="method")
        mixelm, nadvfd = METHODS[method]
        codes = f"MIXELM = {mixelm}"
        if mixelm == 0:
            codes += f" · NADVFD = {nadvfd}"
        st.caption(codes)
        st.markdown(txt[f"method_{method}"])
        st.caption(txt["solver_hint"])
    case = Scenario(ncol=ncol, method=method, signal=signal, dispersivity=al,
                    diffusion=dm, courant=courant, amplitude=amplitude,
                    block_days=block_days, impulse_area=area, impulse_days=impulse_days)
    return case


def show_preview(case, txt, language="en"):
    st.markdown(f'**{txt["preview"]}**')
    _, middle, _ = st.columns([0.15, 5, 0.15])
    with middle, st.container(key="model_frame"):
        show_figure(preview(case, txt), language)
        st.caption(txt["hydraulic_summary"].format(k=K_MS))
        st.caption(txt["preview_summary"].format(signal=txt[case.signal], scheme=txt[case.method],
                                                 n=case.ncol, dx=case.dx, D=case.D))
        if case.signal != "continuous":
            length = VELOCITY * case.duration
            st.caption(txt["pulse_resolution"].format(length=length, cells=length / case.dx))
