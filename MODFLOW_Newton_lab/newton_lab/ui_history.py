"""Compact run history, shared by successful, failed and stale result views."""

import pandas as pd
import streamlit as st
from .config import SHORT_ENGINES


def render_history(history, t):
    if not history:
        return
    st.subheader(t["run_history"], divider="blue")
    st.caption(t["history_help"])
    table = pd.DataFrame(history)
    display = table[
        [
            "run",
            "engine",
            "method",
            "status",
            "runtime_s",
            "outer",
            "inner",
            "discrepancy_pct",
            "active",
            "wet",
            "dry",
            "max_discrepancy_pct",
        ]
    ].copy()
    display.engine = display.engine.map(SHORT_ENGINES)
    display.status = display.status.map(lambda x: "✓" if x == "converged" else "✗")
    display.columns = [t["hist_" + key] for key in display.columns]
    column_config = {
        t["hist_" + key]: st.column_config.NumberColumn(format="%d")
        for key in ("run", "active", "wet", "dry", "outer", "inner")
    }
    column_config[t["hist_runtime_s"]] = st.column_config.NumberColumn(format="%.3f")
    for key in ("discrepancy_pct", "max_discrepancy_pct"):
        column_config[t["hist_" + key]] = st.column_config.NumberColumn(format="%.4f")
    st.dataframe(display, hide_index=True, column_config=column_config)
    st.download_button(
        t["download_history"],
        table.to_csv(index=False),
        file_name="last_10_runs.csv",
        mime="text/csv",
    )
