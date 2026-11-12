"""Preview and result display controls; these never alter model inputs."""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from .config import ENGINES
from .comparisons import matching_time_index, surface_difference
from .ui_history import render_history
from .spatial_plots import (
    comparison_map,
    cross_section,
    head_profile,
    model_preview,
    top_view,
)


def show_figure(fig):
    st.pyplot(fig, width="content")
    plt.close(fig)


def render_preview(s, t):
    with st.expander(t["preview"], expanded=True):
        columns = st.columns(3)
        quantity = columns[0].selectbox(
            t["preview_quantity"],
            ["empty", "k", "initial"],
            format_func=lambda key: t["preview_" + key],
            key="preview_quantity",
        )
        layer = (
            columns[1].number_input(
                t["preview_layer"],
                min_value=1,
                max_value=s.nlay,
                value=1,
                step=1,
                disabled=s.nlay == 1,
                key=f"preview_layer_{s.nlay}",
            )
            - 1
        )
        row = (
            columns[2].number_input(
                t["preview_row"],
                min_value=1,
                max_value=s.nrow,
                value=s.nrow // 2 + 1,
                step=1,
                key=f"preview_row_{s.nrow}",
            )
            - 1
        )
        with st.columns([1, 8, 1])[1], st.container(key="model_preview_frame"):
            show_figure(model_preview(s, t, quantity, layer, row))
        if quantity == "initial":
            st.caption(t["preview_initial_help"])
        st.caption(t["preview_coordinates"])


def previous_section(current, previous, time_index, axis, position, surface, layer):
    """Compare matching geometry/time, using each run's own dry/active mask.

    Do not interpolate time or stretch an old grid to fit a new section. A
    0.0864-second tolerance only accommodates native saved-time rounding.
    """
    if previous is None or not previous.get("success"):
        return None
    now, old = current["scenario"], previous["scenario"]
    geometry = ("nrow", "ncol", "nlay", "cell_size", "top", "thickness", "transient")
    if any(getattr(now, key) != getattr(old, key) for key in geometry):
        return None
    matches = np.flatnonzero(
        np.isclose(previous["days"], current["days"][time_index], rtol=0, atol=1e-6)
    )
    if not len(matches):
        return None
    return head_profile(
        old, previous["heads"][matches[-1]], axis, position, surface, layer
    )


def _retain_visible_style(changed, other):
    """Keep at least one numerical-head representation enabled."""
    if not st.session_state[changed] and not st.session_state.get(other, True):
        st.session_state[other] = True


def render_spatial_results(result, previous, t, *, comparisons=(), history=()):
    s = result["scenario"]
    st.subheader(t["spatial_heads"], divider="blue")
    index = len(result["days"]) - 1
    if s.transient:
        view = st.radio(
            t["snapshot_choice"],
            ["last", "periods", "all_times"],
            horizontal=True,
            format_func=lambda x: t[x],
            key="snapshot_mode",
        )
        if view != "last":
            options = (
                [0] + list(np.cumsum([p.steps for p in s.periods()])[1:] - 1)
                if view == "periods"
                else list(range(len(result["days"])))
            )

            def time_label(i):
                phase = s.periods()[result["keys"][i][1]].label
                return (
                    f"{result['days'][i]:.5g} {t['days']} · "
                    + t["phase_injection" if phase == "injection" else phase]
                )

            index = st.selectbox(
                t["snapshot_time"],
                options,
                index=len(options) - 1,
                format_func=time_label,
                key=f"snapshot_{result['run_id']}_{view}",
            )
        st.caption(t["snapshot_note"].format(day=result["days"][index]))
    with st.container(key="result_plot_settings"), st.expander(t["plot_settings"]):
        columns = st.columns(3)
        with columns[0]:
            axis = st.radio(
                t["section_axis"], ["x", "y"], horizontal=True, key="section_axis"
            )
            n = s.nrow if axis == "x" else s.ncol
            position = (
                st.number_input(
                    t["section_position"],
                    min_value=1,
                    max_value=n,
                    value=n // 2 + 1,
                    step=1,
                    key=f"section_{axis}_{n}",
                )
                - 1
            )
        with columns[1]:
            view_kind = st.selectbox(
                t["section_view"],
                ["surface_view", "selected_layer_view"],
                format_func=lambda key: t[key],
                key="section_view",
                disabled=s.nlay == 1,
            )
            surface = view_kind == "surface_view" or s.nlay == 1
            layer = (
                st.number_input(
                    t["layer"],
                    min_value=1,
                    max_value=s.nlay,
                    value=1,
                    step=1,
                    disabled=surface,
                    key=f"section_layer_{s.nlay}",
                )
                - 1
            )
        with columns[2]:
            show_status = st.toggle(t["show_status"], value=True, key="show_status")
            contours = st.toggle(
                t["show_contours"], key="show_contours", disabled=bool(comparisons)
            )
        st.caption(t["section_display_help"])
    reference_available = (
        not s.transient
        and not s.well_enabled
        and not s.heterogeneous
        and not s.inactive
        and axis == "x"
        and not s.combined
    )
    paired = []
    engine_profiles = []
    for other in comparisons:
        match = matching_time_index(result, other, index)
        if match is None:
            st.caption(
                t["unavailable_snapshot"].format(engine=ENGINES[other["solver"].engine])
            )
            continue
        paired.append(other)
        engine_profiles.append(
            (
                other["solver"].engine,
                head_profile(
                    other["scenario"],
                    other["heads"][match],
                    axis,
                    position,
                    surface,
                    layer,
                ),
            )
        )
    old_profile = previous_section(
        result, previous, index, axis, position, surface, layer
    )
    columns = st.columns(3)
    with columns[0]:
        reference = (
            st.toggle(
                t["show_steady_analytical"],
                key="steady_analytical",
                disabled=not reference_available,
            )
            and reference_available
        )
    with columns[1]:
        initial = st.toggle(
            t["show_initial"], key="show_initial", help=t["initial_result_help"]
        )
    with columns[2]:
        compare = st.toggle(
            t["show_previous_section"],
            key="compare_section",
            disabled=old_profile is None,
            help=t["section_comparison_unavailable"],
        )
    columns = st.columns(3)
    with columns[0]:
        dots = st.toggle(
            t["cell_head_dots"],
            value=True,
            key="show_cell_heads",
            on_change=_retain_visible_style,
            args=("show_cell_heads", "show_cell_lines"),
        )
    with columns[1]:
        lines = st.toggle(
            t["cell_head_lines"],
            value=True,
            key="show_cell_lines",
            on_change=_retain_visible_style,
            args=("show_cell_lines", "show_cell_heads"),
        )
    if compare and old_profile is not None:
        st.caption(
            t["section_comparison_identity"].format(
                run=previous["run_id"],
                engine=ENGINES[previous["solver"].engine],
                day=result["days"][index],
            )
        )
    show_figure(
        cross_section(
            s,
            result["heads"][index],
            t,
            axis,
            position,
            reference,
            initial_heads=(result["heads"][0] if s.transient else s.starting_heads())
            if initial
            else None,
            cell_heads=dots,
            cell_lines=lines,
            previous_profile=old_profile if compare else None,
            surface=surface,
            layer=layer,
            result=result,
            show_status=show_status,
            engine_profiles=engine_profiles,
        )
    )
    render_history(history, t)
    if s.confined and np.nanmin(result["heads"][index]) < s.top:
        st.warning(t["confined_below_top"])
    with (
        st.container(key="results_head_map"),
        st.expander(t["head_map"], expanded=True),
    ):
        if paired:
            by_engine = {run["solver"].engine: run for run in paired}
            key = f"difference_engine_{result['run_id']}"
            if st.session_state.get(key) not in by_engine:
                st.session_state[key] = next(iter(by_engine))
            chosen = st.selectbox(
                t["difference_engine"],
                list(by_engine),
                format_func=ENGINES.get,
                key=key,
            )
            differences = [surface_difference(result, run, index)[0] for run in paired]
            limit = max(
                (
                    float(np.max(np.abs(values[np.isfinite(values)]), initial=0))
                    for values in differences
                ),
                default=0,
            )
            show_figure(
                comparison_map(
                    result, by_engine[chosen], index, t, axis, position, limit
                )
            )
            st.caption(t["difference_help"])
        else:
            with st.columns([1, 8, 1])[1]:
                show_figure(
                    top_view(
                        s,
                        t,
                        result["heads"][index],
                        axis,
                        position,
                        show_contours=contours,
                    )
                )
        st.caption(t["surface_help"])
