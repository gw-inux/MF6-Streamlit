"""Session-local variants, plot controls and multilingual comparison tables."""
from dataclasses import dataclass

import numpy as np
import pandas as pd
import streamlit as st

from .analytical import step
from .engine import Run
from .figure_io import show_figure
from .plots import result_figure
from .scenario import END_TIME, LENGTH, MAX_VARIANTS, VELOCITY


@dataclass
class Variant:
    number: int
    color_slot: int
    name: str
    run: Run

    @property
    def short_label(self):
        return f"V{self.number}"

    def label(self, txt):
        suffix = self.name or f"{txt[self.run.case.method]} · {self.run.case.ncol} {txt['cells_unit']}"
        return f"{self.short_label} · {suffix}"


def clear_variants():
    """A changed inlet/transport widget starts a new physical scenario."""
    if st.session_state.get("history"):
        st.session_state.comparison_cleared = True
    st.session_state.history = []
    st.session_state.next_number = 1
    st.session_state.pop("visible", None)
    st.session_state.pop("remove_number", None)


def add_variant(run, name):
    history = st.session_state.history
    used = {v.color_slot for v in history}
    free = [k for k in range(MAX_VARIANTS) if k not in used]
    if not free:
        return
    number = st.session_state.next_number
    history.append(Variant(number, free[0], name, run))
    st.session_state.next_number = number + 1
    if "visible" in st.session_state:
        st.session_state.visible = [*st.session_state.visible, number]


def _delete_variant():
    number = st.session_state.remove_number
    st.session_state.history = [v for v in st.session_state.history if v.number != number]
    if "visible" in st.session_state:
        st.session_state.visible = [k for k in st.session_state.visible if k != number]


def _rows(history, txt):
    rows = []
    for v in history:
        r, c = v.run, v.run.case
        rows.append({
            "variant": f"{v.short_label} · {v.name}" if v.name else v.short_label,
            "scheme": txt[c.method], "cell_count": c.ncol,
            "rmse": r.rmse, "mae": r.mae, "ideal_rmse": r.ideal_rmse,
            "mass_error": r.mass_error[-1], "seconds": r.flow_seconds + r.transport_seconds,
            "signal": txt[c.signal], "run_name": v.name, "dx_col": c.dx,
            "height_col": c.height, "duration_col": c.duration,
            "area_col": c.impulse_area if c.signal == "dirac" else None,
            "pulse_cells": VELOCITY * c.duration / c.dx if c.signal != "continuous" else None,
            "alpha_col": c.dispersivity, "dm_col": c.diffusion, "d_col": c.D,
            "pe_col": VELOCITY * c.dx / c.D if c.D > 0 else np.inf,
            "co_col": c.courant, "count_col": len(r.times) - 1,
            "flow_s": r.flow_seconds, "mt_s": r.transport_seconds,
            "flow_error": r.flow_discrepancy, "min_c": float(r.concentration[-1].min()),
            "max_c": float(r.concentration[-1].max()),
        })
    return pd.DataFrame(rows)


def _table(frame, txt, columns, formats):
    config = {k: (st.column_config.NumberColumn(txt[k], format=formats[k]) if k in formats
                  else txt[k]) for k in columns}
    st.dataframe(frame[columns], column_config=config, hide_index=True, width="stretch")


def render_results(txt, language="en"):
    history = st.session_state.history
    if not history:
        return
    st.subheader(txt["results"])
    by_number = {v.number: v for v in history}
    st.session_state.setdefault("visible", list(by_number))
    selected = st.multiselect(txt["visible"], list(by_number),
                              format_func=lambda k: by_number[k].label(txt), key="visible")
    variants = [by_number[i] for i in selected]
    left, right = st.columns(2)
    analytical = left.toggle(txt["show_analytical"], value=True, key="show_analytical")
    markers = right.toggle(txt["show_markers"], value=True, key="show_markers")

    if variants:
        profile, btc, budget = st.tabs([txt["profile"], txt["breakthrough"], txt["budget"]])
        with profile:
            time = st.slider(txt["profile_time"], 0, int(END_TIME), int(END_TIME), 10, key="profile_time")
            show_figure(result_figure(variants, "profile", time, analytical, markers, txt), language)
            st.caption(txt["profile_hint"])
        with btc:
            distance = st.slider(txt["observation"], 100, 900, 250, 5, key="observation")
            show_figure(result_figure(variants, "breakthrough", distance, analytical, markers, txt), language)
            st.caption(txt["breakthrough_hint"].format(t=distance / VELOCITY))
        with budget:
            show_figure(result_figure(variants, "budget", None, False, markers, txt), language)
            st.caption(txt["balance_hint"])
        if analytical and any(v.run.case.signal == "dirac" for v in variants):
            st.caption(txt["dirac_reading"])
        influence = [v.short_label for v in variants if step(LENGTH, END_TIME, v.run.case.D) >= 0.01]
        if analytical and influence:
            st.info(txt["outlet_hint"].format(ids=", ".join(influence)))
    else:
        st.info(txt["no_selection"])

    st.subheader(txt["comparison"])
    frame = _rows(history, txt)
    columns = ["variant", "scheme", "cell_count", "rmse", "mae"]
    if any(v.run.case.signal == "dirac" for v in history):
        columns.append("ideal_rmse")
    columns += ["mass_error", "seconds", "signal"]
    formats = {k: "%.4g" for k in ("rmse", "mae", "ideal_rmse", "min_c", "max_c")}
    formats.update({k: "%.4f" for k in ("mass_error", "flow_error", "flow_s", "mt_s", "seconds")})
    st.caption(txt["table_hint"])
    _table(frame, txt, columns, formats)
    imbalanced = [v.short_label for v in history if abs(v.run.mass_error[-1]) > 1.0]
    if imbalanced:
        st.warning(txt["mass_warning"].format(ids=", ".join(imbalanced)))
    with st.expander(txt["detail_heading"]):
        extra = [k for k in frame.columns if k not in columns]
        _table(frame, txt, ["variant", *extra], formats)
        st.markdown(txt["metrics_notes"])
    csv = frame.rename(columns={key: txt[key] for key in frame}).to_csv(index=False)
    st.download_button(txt["download"], csv.encode("utf-8-sig"), "MT3D_transport_comparison.csv",
                       "text/csv", key="download_csv", on_click="ignore")
    with st.expander(txt["manage"]):
        st.selectbox(txt["remove_choice"], list(by_number),
                     format_func=lambda k: by_number[k].label(txt), key="remove_number")
        st.button(txt["remove"], key="remove", on_click=_delete_variant)
