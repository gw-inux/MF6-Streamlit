"""Minimal Streamlit + MODFLOW 6 + MODPATH 7 cloud-deployment test.

MODFLOW and MODPATH are intentionally controlled by separate buttons.  MODPATH
reuses the latest successful MODFLOW workspace and therefore does not rerun the
flow model.
"""

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
    cleanup_workspace,
    get_mf6_version,
    locate_mf6,
    locate_mp7,
    run_modflow,
    run_modpath,
)


st.set_page_config(
    page_title="MODFLOW + MODPATH Cloud Test",
    page_icon="💧",
    layout="wide",
)


@st.cache_resource
def native_run_semaphore() -> threading.BoundedSemaphore:
    """Limit simultaneous native processes in this Streamlit server."""

    return threading.BoundedSemaphore(value=2)


def plot_plan_view(
    head: np.ndarray,
    layer: int,
    tracking: TrackingResult | None = None,
):
    """Plot hydraulic head, optionally with MODPATH pathlines."""

    x_edges = np.arange(NCOL + 1) * DELR
    y_edges = np.arange(NROW + 1) * DELC

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    mesh = ax.pcolormesh(
        x_edges,
        y_edges,
        np.flipud(head[layer]),
        shading="auto",
    )
    fig.colorbar(mesh, ax=ax, label="Hydraulic head (m)")

    if tracking is not None:
        for track in tracking.tracks:
            ax.plot(track.x, track.y, linewidth=0.8, alpha=0.65)

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
        markersize=9,
        mew=2,
        linestyle="none",
        label="Pumping well",
        zorder=5,
    )

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    title = f"Hydraulic head in layer {layer + 1}"
    if tracking is not None:
        title += " with pathline projection"
    ax.set_title(title)
    ax.set_aspect("equal")
    ax.legend(loc="best")
    fig.tight_layout()
    return fig


def plot_vertical_pathlines(tracking: TrackingResult):
    """Plot an x-z projection of the selected pathlines."""

    fig, ax = plt.subplots(figsize=(8.0, 4.8))

    for track in tracking.tracks:
        ax.plot(track.x, track.z, linewidth=0.8, alpha=0.65)

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

    ax.axhline(TOP, linewidth=0.8, alpha=0.6)
    for bottom in BOTM:
        ax.axhline(bottom, linewidth=0.8, alpha=0.6)

    well_x = (WELL_COL + 0.5) * DELR
    well_top = TOP if WELL_LAYER == 0 else BOTM[WELL_LAYER - 1]
    well_bottom = BOTM[WELL_LAYER]
    well_z = 0.5 * (well_top + well_bottom)
    ax.plot(
        well_x,
        well_z,
        marker="x",
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
    """Plot heads through the row containing the pumping well."""

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


def discard_flow_workspace() -> None:
    """Delete the current flow workspace and all results derived from it."""

    old_result = st.session_state.pop("flow_result", None)
    if old_result is not None:
        cleanup_workspace(old_result.workspace)

    st.session_state.pop("flow_signature", None)
    st.session_state.pop("modpath_result", None)
    st.session_state.pop("modpath_signature", None)


st.title("💧 MODFLOW 6 + MODPATH 7 Cloud Test")
st.write(
    "This application first runs a small three-layer MODFLOW 6 model on the "
    "Streamlit server. MODPATH 7 can then be run independently against the "
    "latest successful MODFLOW solution."
)

with st.expander("Model definition", expanded=True):
    st.markdown(
        f"""
- **Grid:** {NLAY} layers × {NROW} rows × {NCOL} columns; cells are {DELR:.0f} × {DELC:.0f} m.
- **Layer elevations:** top = {TOP:.0f} m; bottoms = {BOTM.tolist()} m.
- **Boundaries:** specified heads on the complete left and right faces in all layers.
- **Well:** one pumping well in the centre of layer {WELL_LAYER + 1}.
- **Flow formulation:** all layers confined; steady-state; no recharge.
- **Backward MODPATH:** {BACKWARD_PARTICLE_COUNT} particles inside the pumping cell (5 × 2 × 2 positions).
- **Forward MODPATH:** one particle at the centre of each specified-head boundary cell ({FORWARD_PARTICLE_COUNT} particles total).
        """
    )
    st.caption(
        "MODPATH performs advective particle tracking. It does not represent "
        "dispersion, diffusion, or chemical retardation."
    )

# -----------------------------------------------------------------------------
# Flow-model inputs
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
        help="Enter a positive extraction magnitude; MODFLOW receives a negative WEL flux.",
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

current_flow_signature = params.signature()

# A changed flow design invalidates both the MF6 solution and any MP7 results.
if (
    "flow_signature" in st.session_state
    and st.session_state.flow_signature != current_flow_signature
):
    discard_flow_workspace()
    st.info("Flow-model parameters changed. Press **Run MODFLOW** to calculate a new flow field.")

run_mf6_clicked = st.button("Run MODFLOW", type="primary")

if run_mf6_clicked:
    # Remove a previous workspace before creating the next one.
    discard_flow_workspace()
    try:
        with st.spinner("Running MODFLOW 6..."):
            with native_run_semaphore():
                flow_result = run_modflow(params)
        st.session_state.flow_result = flow_result
        st.session_state.flow_signature = current_flow_signature
        st.success("MODFLOW terminated normally. The flow solution is ready for MODPATH.")
    except Exception as exc:
        discard_flow_workspace()
        st.error("The MODFLOW simulation failed.")
        st.exception(exc)

# -----------------------------------------------------------------------------
# Independent MODPATH control -- deliberately placed above the Results block.
# -----------------------------------------------------------------------------
if "flow_result" in st.session_state:
    st.divider()
    st.markdown("#### Particle tracking")
    st.caption(
        "MODPATH uses the existing MODFLOW head and budget files. Pressing this "
        "button does **not** rerun MODFLOW."
    )

    mp_col1, mp_col2 = st.columns([1, 2])
    with mp_col1:
        effective_porosity = st.number_input(
            "Effective porosity (-)",
            min_value=0.01,
            max_value=0.60,
            value=0.25,
            step=0.05,
            format="%.2f",
            help=(
                "Porosity controls particle velocity and travel time. For this "
                "steady flow field it does not change the geometric streamline."
            ),
        )

    current_modpath_signature = (
        st.session_state.flow_signature,
        float(effective_porosity),
    )

    # Changing porosity invalidates pathlines/travel times, but not MODFLOW.
    if (
        "modpath_signature" in st.session_state
        and st.session_state.modpath_signature != current_modpath_signature
    ):
        st.session_state.pop("modpath_result", None)
        st.session_state.pop("modpath_signature", None)
        st.info("Effective porosity changed. The MODFLOW result is still valid; rerun MODPATH only.")

    with mp_col2:
        st.write("")
        st.write("")
        run_mp7_clicked = st.button("Run MODPATH")

    if run_mp7_clicked:
        try:
            with st.spinner("Running backward and forward MODPATH 7 tracking..."):
                with native_run_semaphore():
                    modpath_result = run_modpath(
                        st.session_state.flow_result,
                        effective_porosity=float(effective_porosity),
                    )
            st.session_state.modpath_result = modpath_result
            st.session_state.modpath_signature = current_modpath_signature
            st.success("MODPATH terminated normally. MODFLOW was not rerun.")
        except Exception as exc:
            st.session_state.pop("modpath_result", None)
            st.session_state.pop("modpath_signature", None)
            st.error("The MODPATH workflow failed.")
            st.exception(exc)

# -----------------------------------------------------------------------------
# Results
# -----------------------------------------------------------------------------
if "flow_result" in st.session_state:
    flow_result = st.session_state.flow_result
    head = flow_result.head

    st.divider()
    st.subheader("Results")

    well_head = head[WELL_LAYER, WELL_ROW, WELL_COL]
    st.markdown(
        f"""
**MODFLOW run summary**  
MODFLOW: `{flow_result.mf6_version}`  
MODFLOW runtime: **{flow_result.runtime_seconds:.3f} s**  
Head at the pumping cell (layer {WELL_LAYER + 1}): **{well_head:.3f} m**  
Minimum / maximum simulated head: **{np.min(head):.3f} / {np.max(head):.3f} m**
        """
    )

    display_layer = st.selectbox(
        "Head layer",
        options=list(range(NLAY)),
        format_func=lambda i: f"Layer {i + 1}",
        index=WELL_LAYER,
        key="head_display_layer",
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

    if "modpath_result" in st.session_state:
        mp_result = st.session_state.modpath_result

        st.subheader("Particle tracking")
        st.markdown(
            f"""
MODPATH: `{mp_result.backward.mp7_version}`  
MODPATH runtime (backward + forward): **{mp_result.runtime_seconds:.3f} s**  
Effective porosity: **{mp_result.effective_porosity:.2f}**
            """
        )

        tracking_option = st.radio(
            "Pathlines shown",
            options=[
                "Backward from pumping well",
                "Forward from specified-head boundaries",
            ],
            horizontal=True,
        )

        if tracking_option.startswith("Backward"):
            tracking = mp_result.backward
            st.markdown(
                f"**Backward tracking:** {tracking.requested_particles} particles "
                "were released at explicit positions within the pumping cell."
            )
        else:
            tracking = mp_result.forward
            st.markdown(
                f"**Forward tracking:** {tracking.requested_particles} particles "
                "were released, one at the centre of every specified-head cell on "
                "the left and right boundaries. Cells acting as outflow boundaries "
                "may produce very short pathlines."
            )

        st.caption(
            f"MODPATH returned {tracking.pathline_count} pathline records. "
            "White circles show the explicitly defined release locations."
        )

        path_layer = st.selectbox(
            "Head layer shown beneath the plan-view pathlines",
            options=list(range(NLAY)),
            format_func=lambda i: f"Layer {i + 1}",
            index=WELL_LAYER,
            key="path_display_layer",
        )

        left, right = st.columns(2)
        with left:
            fig = plot_plan_view(head, path_layer, tracking=tracking)
            st.pyplot(fig, clear_figure=True)
            plt.close(fig)

        with right:
            fig = plot_vertical_pathlines(tracking)
            st.pyplot(fig, clear_figure=True)
            plt.close(fig)

        with st.expander("MODPATH console output"):
            st.markdown("**Backward tracking**")
            st.code(mp_result.backward.stdout, language="text")
            st.markdown("**Forward tracking**")
            st.code(mp_result.forward.stdout, language="text")

    with st.expander("MODFLOW console output"):
        st.code(flow_result.stdout, language="text")

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
