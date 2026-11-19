"""Introductory figures computed from the existing analytical benchmark.

The illustrations use a fixed block input and never create a model variant.
All prose and figure labels come from the translated Markdown resources.
"""
from dataclasses import replace

import streamlit as st
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from .analytical import applied
from .figure_io import show_figure
from .plots import COLORS, INK, _coordinates, _style
from .scenario import END_TIME, LEFT_HEAD, LENGTH, VELOCITY, Scenario

EXAMPLE = Scenario(signal="block", block_days=400.0)
EXAMPLE_DISPERSIVITY = 10.0
OBSERVATION_X = 250.0


def conceptual_model(txt):
    """Stream tube with no transverse exchange; transverse scale is schematic."""
    figure = Figure(figsize=(7.2, 2.0), layout="constrained")
    ax = figure.subplots()
    ax.add_patch(Rectangle((0, 0.25), LENGTH, 0.35,
                           facecolor="#E9F1F6", edgecolor=COLORS[0], linewidth=1.4))
    ax.vlines([0, LENGTH], 0.25, 0.60, colors=COLORS[0], linewidth=4)
    for start in (70, 430, 750):
        ax.annotate("", xy=(start + 160, 0.425), xytext=(start, 0.425),
                    arrowprops={"arrowstyle": "->", "color": COLORS[0], "lw": 1.5})
    ax.vlines(OBSERVATION_X, 0.15, 0.63, colors=COLORS[2], linestyles="--", linewidth=1.3)
    ax.text(0, 0.82, txt["specified_head"].format(head=LEFT_HEAD), ha="left", color=INK, fontsize=9)
    ax.text(LENGTH, 0.82, txt["specified_head"].format(head=0.0), ha="right", color=INK, fontsize=9)
    ax.text(LENGTH / 2, 0.67, f"v = {VELOCITY:g} m/d", ha="center", color=COLORS[0], fontsize=10)
    ax.text(0, 0.06, txt["concept_inlet"] + "\n" + r"$C_{\mathrm{in}}(t)$",
            ha="left", va="top", color=INK, fontsize=9)
    ax.text(OBSERVATION_X, 0.06, txt["concept_observation"] + f"\nx = {OBSERVATION_X:g} m",
            ha="center", va="top", color=COLORS[2], fontsize=9)
    ax.text(LENGTH, 0.06, txt["concept_outlet"] + f"\nx = {LENGTH:g} m",
            ha="right", va="top", color=INK, fontsize=9)
    ax.set(xlim=(-20, LENGTH + 20), ylim=(-0.38, 1.00))
    ax.set_axis_off()
    return figure


def typical_responses(txt):
    """Exact block responses, including sharp pure-advection discontinuities."""
    figure = Figure(figsize=(7.2, 5.5), layout="constrained")
    profile, breakthrough = figure.subplots(2, 1)
    cases = [(EXAMPLE, txt["concept_advection"], COLORS[2], "--"),
             (replace(EXAMPLE, dispersivity=EXAMPLE_DISPERSIVITY),
              txt["concept_dispersion"], COLORS[0], "-")]
    for case, label, color, linestyle in cases:
        x = _coordinates(case, "profile", END_TIME)
        t = _coordinates(case, "breakthrough", OBSERVATION_X)
        profile.plot(x, applied(x, END_TIME, case), label=label, color=color, ls=linestyle, lw=1.8)
        breakthrough.plot(t, applied(OBSERVATION_X, t, case), label=label,
                          color=color, ls=linestyle, lw=1.8)
    profile.set(xlim=(0, LENGTH), xlabel=txt["distance"],
                title=txt["concept_profile"].format(time=END_TIME))
    breakthrough.set(xlim=(0, END_TIME), xlabel=txt["time"],
                     title=txt["concept_breakthrough"].format(distance=OBSERVATION_X))
    for ax in (profile, breakthrough):
        ax.set(ylim=(-0.04, 1.18), ylabel=r"$C/C_{\mathrm{ref}}$ [–]")
        _style(ax)
        ax.legend(loc="upper left", fontsize=8, framealpha=0.94)
        ax.title.set_fontsize(10)
        ax.title.set_color(INK)
    return figure


def show_introduction(txt, language):
    st.markdown(txt["introduction"])
    with st.expander(f'**{txt["concept_title"]}**'):
        st.markdown(txt["concept_explanation"])
        show_figure(conceptual_model(txt), language)
        st.caption(txt["concept_caption"])
        show_figure(typical_responses(txt), language)
        st.caption(txt["concept_response_caption"])
