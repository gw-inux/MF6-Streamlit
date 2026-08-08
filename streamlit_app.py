"""Minimal Streamlit + MODFLOW 6 cloud-deployment test."""

from __future__ import annotations

import threading

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from mf6_model import (
    BOTM,
    DELC,
    DELR,
    NCOL,
    NLAY,
    NROW,
    TOP,
    WELL_COL,
    WELL_LAYER,
    WELL_ROW,
    ModelParameters,
    locate_mf6,
    get_mf6_version,
    run_model,
)


st.set_page_config(
    page_title="MODFLOW 6 Cloud Test",
    page_icon="💧",
    layout="wide",
)


@st.cache_resource
def model_run_semaphore() -> threading.BoundedSemaphore:
    """Limit simultaneous MF6 processes in this Streamlit server process."""

    # Community Cloud currently provides at most a small number of CPU cores.
    # Two concurrent tiny models are sufficient for this deployment experiment.
    return threading.BoundedSemaphore(value=2)


def plot_plan_view(head: np.ndarray, layer: int):
    """Plot heads for one model layer in physically meaningful x/y coordinates."""

    x_edges = np.arange(NCOL + 1) * DELR
    y_edges = np.arange(NROW + 1) * DELC

    fig, ax = plt.subplots(figsize=(8.0, 4.8))

    # MODFLOW row 0 is conventionally shown at the top/north.  Flipping the
    # array lets the y axis increase upward while preserving that convention.
    mesh = ax.pcolormesh(
        x_edges,
        y_edges,
        np.flipud(head[layer]),
        shading="auto",
    )
    fig.colorbar(mesh, ax=ax, label="Hydraulic head (m)")

    well_x = (WELL_COL + 0.5) * DELR
    well_y = (NROW - WELL_ROW - 0.5) * DELC
    ax.plot(well_x, well_y, marker="x", markersize=9, mew=2, label="Pumping well")

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(f"Hydraulic head — layer {layer + 1}")
    ax.set_aspect("equal")
    ax.legend(loc="best")
    fig.tight_layout()
    return fig


def plot_head_profiles(head: np.ndarray):
    """Plot the head profile through the row containing the pumping well."""

    x = (np.arange(NCOL) + 0.5) * DELR

    fig, ax = plt.subplots(figsize=(8.0, 4.2))
    for layer in range(NLAY):
        ax.plot(x, head[layer, WELL_ROW, :], label=f"Layer {layer + 1}")

    well_x = (WELL_COL + 0.5) * DELR
    ax.axvline(well_x, linestyle="--", linewidth=1, label="Well column")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Hydraulic head (m)")
    ax.set_title("Head profiles through the pumping-well row")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    return fig


st.title("💧 MODFLOW 6 Cloud Test")
st.write(
    "This small application tests whether MODFLOW 6 can be executed directly "
    "inside a Streamlit deployment. The model is intentionally simple and "
    "steady-state so that deployment issues are easy to diagnose."
)

with st.expander("Model definition", expanded=True):
    st.markdown(
        f"""
- **Grid:** {NLAY} layers × {NROW} rows × {NCOL} columns; cells are {DELR:.0f} × {DELC:.0f} m.
- **Layer elevations:** top = {TOP:.0f} m; bottoms = {BOTM.tolist()} m.
- **Boundaries:** specified heads on the complete left and right faces in all layers.
- **Well:** one pumping well in the centre of layer {WELL_LAYER + 1}.
- **Flow formulation:** all layers confined; steady-state; no recharge.
- **Vertical conductivity:** `Kz = anisotropy × Kx` in each layer.
        """
    )

# -----------------------------------------------------------------------------
# Model inputs
# -----------------------------------------------------------------------------
st.subheader("Model parameters")

col1, col2, col3 = st.columns(3)
with col1:
    head_left = st.number_input(
        "Left specified head (m)",
        min_value=0.0,
        max_value=100.0,
        value=32.0,
        step=0.5,
    )
    head_right = st.number_input(
        "Right specified head (m)",
        min_value=0.0,
        max_value=100.0,
        value=31.0,
        step=0.5,
    )

with col2:
    k_layer1 = st.number_input(
        "K layer 1 (m/day)",
        min_value=0.001,
        max_value=1000.0,
        value=10.0,
        format="%.3f",
    )
    k_layer2 = st.number_input(
        "K layer 2 (m/day)",
        min_value=0.001,
        max_value=1000.0,
        value=0.10,
        format="%.3f",
    )
    k_layer3 = st.number_input(
        "K layer 3 (m/day)",
        min_value=0.001,
        max_value=1000.0,
        value=5.0,
        format="%.3f",
    )

with col3:
    pumping_rate = st.number_input(
        "Pumping rate (m³/day)",
        min_value=0.0,
        max_value=800.0,
        value=300.0,
        step=50.0,
        help="Enter a positive extraction magnitude; MODFLOW receives the negative WEL flux.",
    )
    vertical_anisotropy = st.number_input(
        "Vertical anisotropy Kz/Kx (-)",
        min_value=0.001,
        max_value=1.0,
        value=0.10,
        format="%.3f",
    )

params = ModelParameters(
    head_left=float(head_left),
    head_right=float(head_right),
    pumping_rate=float(pumping_rate),
    k_layer1=float(k_layer1),
    k_layer2=float(k_layer2),
    k_layer3=float(k_layer3),
    vertical_anisotropy=float(vertical_anisotropy),
)

# Hide stale results immediately when a model parameter changes.  Streamlit will
# rerun the Python script when a widget changes, but MODFLOW itself is executed
# only after the dedicated button is pressed.
if (
    "last_run_signature" in st.session_state
    and st.session_state.last_run_signature != params.signature()
):
    st.session_state.pop("model_result", None)
    st.session_state.pop("last_run_signature", None)
    st.info("Model parameters changed. Press **Run MODFLOW** to calculate new results.")

run_clicked = st.button("Run MODFLOW", type="primary")

if run_clicked:
    try:
        with st.spinner("Running MODFLOW 6..."):
            with model_run_semaphore():
                result = run_model(params)
        st.session_state.model_result = result
        st.session_state.last_run_signature = params.signature()
        st.success("MODFLOW terminated normally.")
    except Exception as exc:
        st.session_state.pop("model_result", None)
        st.session_state.pop("last_run_signature", None)
        st.error("The MODFLOW run failed.")
        st.exception(exc)

# -----------------------------------------------------------------------------
# Results
# -----------------------------------------------------------------------------
if "model_result" in st.session_state:
    result = st.session_state.model_result
    head = result.head

    st.subheader("Results")

    well_head = head[WELL_LAYER, WELL_ROW, WELL_COL]
    st.markdown(
        f"""
**Run summary**  
MODFLOW: `{result.mf6_version}`  
Runtime including model writing and output reading: **{result.runtime_seconds:.3f} s**  
Head at the pumping cell (layer {WELL_LAYER + 1}): **{well_head:.3f} m**  
Minimum / maximum simulated head: **{np.min(head):.3f} / {np.max(head):.3f} m**
        """
    )

    display_layer = st.selectbox(
        "Layer shown in plan view",
        options=list(range(NLAY)),
        format_func=lambda i: f"Layer {i + 1}",
        index=WELL_LAYER,
    )

    left, right = st.columns(2)
    with left:
        fig = plot_plan_view(head, display_layer)
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)

    with right:
        fig = plot_head_profiles(head)
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)

    with st.expander("MODFLOW console output"):
        st.code(result.stdout, language="text")

with st.expander("Deployment diagnostic"):
    try:
        mf6_path = locate_mf6()
        mf6_version = get_mf6_version(mf6_path)
        st.write(f"MODFLOW executable: `{mf6_path}`")
        st.write(f"Version check: `{mf6_version}`")
        st.success("The MODFLOW executable is available to the Streamlit process.")
    except Exception as exc:
        st.error("MODFLOW executable is not available.")
        st.exception(exc)
