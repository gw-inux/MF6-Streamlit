"""Minimal Streamlit + MODFLOW 6 + MODPATH 7 cloud-deployment test."""

from __future__ import annotations

import threading

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from mf6_model import (
    BACKWARD_PARTICLE_COUNT,
    BOTM,
    DELC,
    DELR,
    FORWARD_PARTICLE_COUNT,
    NCOL,
    NLAY,
    NROW,
    TOP,
    WELL_COL,
    WELL_LAYER,
    WELL_ROW,
    ModelParameters,
    TrackingResult,
    get_mf6_version,
    locate_mf6,
    locate_mp7,
    run_model,
)


st.set_page_config(
    page_title="MODFLOW + MODPATH Cloud Test",
    page_icon="💧",
    layout="wide",
)


@st.cache_resource
def model_run_semaphore() -> threading.BoundedSemaphore:
    """Limit simultaneous native model processes in this Streamlit server."""

    # The complete workflow now includes one MF6 run followed by two MP7 runs.
    # Two simultaneous workflows remain a conservative Community Cloud limit.
    return threading.BoundedSemaphore(value=2)


def plot_plan_view(head: np.ndarray, layer: int, tracking: TrackingResult):
    """Plot hydraulic head and MODPATH pathlines in plan projection."""

    x_edges = np.arange(NCOL + 1) * DELR
    y_edges = np.arange(NROW + 1) * DELC

    fig, ax = plt.subplots(figsize=(8.0, 4.8))

    # MODFLOW row 0 is conventionally shown at the top/north.  Flipping the
    # head array makes the y axis increase upward, consistent with FloPy's
    # global particle coordinates returned by MODPATH.
    mesh = ax.pcolormesh(
        x_edges,
        y_edges,
        np.flipud(head[layer]),
        shading="auto",
    )
    fig.colorbar(mesh, ax=ax, label="Hydraulic head (m)")

    # Pathlines are shown as a plan-view projection.  They may move between
    # layers; the vertical projection is shown separately in the next figure.
    for track in tracking.tracks:
        ax.plot(track.x, track.y, color="black", linewidth=0.8, alpha=0.65)

    if tracking.start_xyz.size:
        ax.scatter(
            tracking.start_xyz[:, 0],
            tracking.start_xyz[:, 1],
            s=16,
            facecolors="white",
            edgecolors="black",
            linewidths=0.6,
            label="Particle starts",
            zorder=4,
        )

    well_x = (WELL_COL + 0.5) * DELR
    well_y = (NROW - WELL_ROW - 0.5) * DELC
    ax.plot(
        well_x,
        well_y,
        marker="x",
        color="red",
        markersize=9,
        mew=2,
        linestyle="none",
        label="Pumping well",
        zorder=5,
    )

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(f"Heads in layer {layer + 1} with pathline projection")
    ax.set_aspect("equal")
    ax.legend(loc="best")
    fig.tight_layout()
    return fig


def plot_vertical_pathlines(tracking: TrackingResult):
    """Plot all pathlines as an x-z projection through the layered system."""

    fig, ax = plt.subplots(figsize=(8.0, 4.2))

    for track in tracking.tracks:
        ax.plot(track.x, track.z, color="black", linewidth=0.8, alpha=0.65)

    if tracking.start_xyz.size:
        ax.scatter(
            tracking.start_xyz[:, 0],
            tracking.start_xyz[:, 2],
            s=16,
            facecolors="white",
            edgecolors="black",
            linewidths=0.6,
            label="Particle starts",
            zorder=4,
        )

    # Layer boundaries make vertical movement through the three layers easier
    # to interpret.  The plot is an x-z projection; y is intentionally omitted.
    ax.axhline(TOP, color="0.5", linewidth=0.8)
    for bottom in BOTM:
        ax.axhline(bottom, color="0.5", linewidth=0.8)

    well_x = (WELL_COL + 0.5) * DELR
    well_z = 0.5 * (BOTM[WELL_LAYER - 1] + BOTM[WELL_LAYER])
    ax.plot(
        well_x,
        well_z,
        marker="x",
        color="red",
        markersize=9,
        mew=2,
        linestyle="none",
        label="Pumping well",
        zorder=5,
    )

    ax.set_xlim(0.0, NCOL * DELR)
    ax.set_ylim(BOTM[-1], TOP)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Elevation z (m)")
    ax.set_title("Pathlines — vertical x-z projection")
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


st.title("💧 MODFLOW 6 + MODPATH 7 Cloud Test")
st.write(
    "This application runs a small three-layer MODFLOW 6 model on the Streamlit "
    "server and then performs MODPATH 7 particle tracking using the calculated "
    "heads and cell-by-cell flows."
)

with st.expander("Model definition", expanded=True):
    st.markdown(
        f"""
- **Grid:** {NLAY} layers × {NROW} rows × {NCOL} columns; cells are {DELR:.0f} × {DELC:.0f} m.
- **Layer elevations:** top = {TOP:.0f} m; bottoms = {BOTM.tolist()} m.
- **Boundaries:** specified heads on the complete left and right faces in all layers.
- **Well:** one pumping well in the centre of layer {WELL_LAYER + 1}.
- **Flow formulation:** all layers confined; steady-state; no recharge.
- **Backward MODPATH:** {BACKWARD_PARTICLE_COUNT} particles in the pumping cell (5 × 2 × 2 subdivisions).
- **Forward MODPATH:** one particle per specified-head cell on both lateral faces ({FORWARD_PARTICLE_COUNT} particles total).
        """
    )
    st.caption(
        "MODPATH is advective particle tracking. It does not represent dispersion, "
        "diffusion, or chemical retardation."
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
    effective_porosity = st.number_input(
        "Effective porosity for MODPATH (-)",
        min_value=0.01,
        max_value=0.60,
        value=0.25,
        step=0.05,
        format="%.2f",
        help=(
            "Porosity controls particle velocity and travel time. For this steady "
            "flow field it does not change the geometric pathline."
        ),
    )

params = ModelParameters(
    head_left=float(head_left),
    head_right=float(head_right),
    pumping_rate=float(pumping_rate),
    k_layer1=float(k_layer1),
    k_layer2=float(k_layer2),
    k_layer3=float(k_layer3),
    vertical_anisotropy=float(vertical_anisotropy),
    effective_porosity=float(effective_porosity),
)

# Hide stale results immediately when a model or particle-velocity parameter
# changes.  Native executables run only after the dedicated button is pressed.
if (
    "last_run_signature" in st.session_state
    and st.session_state.last_run_signature != params.signature()
):
    st.session_state.pop("model_result", None)
    st.session_state.pop("last_run_signature", None)
    st.info(
        "Model parameters changed. Press **Run MODFLOW + MODPATH** to calculate new results."
    )

run_clicked = st.button("Run MODFLOW + MODPATH", type="primary")

if run_clicked:
    try:
        with st.spinner("Running MODFLOW 6 and MODPATH 7..."):
            with model_run_semaphore():
                result = run_model(params)
        st.session_state.model_result = result
        st.session_state.last_run_signature = params.signature()
        st.success("MODFLOW and both MODPATH simulations terminated normally.")
    except Exception as exc:
        st.session_state.pop("model_result", None)
        st.session_state.pop("last_run_signature", None)
        st.error("The MODFLOW / MODPATH workflow failed.")
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
MODPATH: `{result.backward.mp7_version}`  
Total workflow runtime: **{result.runtime_seconds:.3f} s**  
MODFLOW runtime: **{result.mf6_runtime_seconds:.3f} s**  
Backward MODPATH runtime: **{result.backward.runtime_seconds:.3f} s**  
Forward MODPATH runtime: **{result.forward.runtime_seconds:.3f} s**  
Head at the pumping cell (layer {WELL_LAYER + 1}): **{well_head:.3f} m**  
Minimum / maximum simulated head: **{np.min(head):.3f} / {np.max(head):.3f} m**
        """
    )

    st.subheader("Particle tracking")
    tracking_option = st.radio(
        "Tracking visualization",
        options=["Backward from pumping well", "Forward from specified-head boundaries"],
        horizontal=True,
    )

    if tracking_option.startswith("Backward"):
        tracking = result.backward
        st.markdown(
            f"**Backward tracking:** {tracking.requested_particles} particles were "
            "released inside the pumping cell and tracked backward toward their "
            "hydraulic source locations."
        )
    else:
        tracking = result.forward
        st.markdown(
            f"**Forward tracking:** {tracking.requested_particles} particles were "
            "released — one in every specified-head boundary cell on the left and "
            "right sides. Particles placed in boundary cells acting as outflow may "
            "terminate very quickly at that boundary."
        )

    st.caption(
        f"MODPATH returned {tracking.pathline_count} particle pathline records. "
        "The white circles show the defined release locations."
    )

    display_layer = st.selectbox(
        "Head layer shown below the plan-view pathlines",
        options=list(range(NLAY)),
        format_func=lambda i: f"Layer {i + 1}",
        index=WELL_LAYER,
    )

    left, right = st.columns(2)
    with left:
        fig = plot_plan_view(head, display_layer, tracking)
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)

    with right:
        fig = plot_vertical_pathlines(tracking)
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)

    with st.expander("Hydraulic-head profile"):
        fig = plot_head_profiles(head)
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)

    with st.expander("MODFLOW console output"):
        st.code(result.mf6_stdout, language="text")

    with st.expander("MODPATH console output"):
        st.markdown("**Backward tracking**")
        st.code(result.backward.stdout, language="text")
        st.markdown("**Forward tracking**")
        st.code(result.forward.stdout, language="text")

with st.expander("Deployment diagnostic"):
    try:
        mf6_path = locate_mf6()
        mf6_version = get_mf6_version(mf6_path)
        st.write(f"MODFLOW executable: `{mf6_path}`")
        st.write(f"MODFLOW version check: `{mf6_version}`")
        st.success("MODFLOW 6 is available to the Streamlit process.")
    except Exception as exc:
        st.error("MODFLOW 6 executable is not available.")
        st.exception(exc)

    try:
        mp7_path = locate_mp7()
        st.write(f"MODPATH executable: `{mp7_path}`")
        st.success("MODPATH 7 is available to the Streamlit process.")
    except Exception as exc:
        st.error("MODPATH 7 executable is not available.")
        st.exception(exc)
