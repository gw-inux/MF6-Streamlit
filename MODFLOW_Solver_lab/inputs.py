"""Input panels: retained scenario values, grid controls and solver groups.

Widget keys are transient; scenario_values and complexity_options own values
that must survive hiding inputs. Model assembly remains in core.Scenario.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   INITIAL_DISTRIBUTIONS: line 35
#   capture_input_values: line 43
#   scenario_controls: line 73
#   set_cell_spacing: line 162
#   spatial_controls: line 168
#   solver_controls: line 276
#   regenerate_k: line 322
#   select_k_preview: line 329
#   complexity_controls: line 335
#   render_model_preview: line 422
# END CODE CONTENTS

from copy import deepcopy
from dataclasses import asdict

import streamlit as st

from .content import TEXT
from .controls import basic_controls
from .core import ENGINE_NAMES, Scenario
from .plots import display_stride, model_preview
from .settings import METHODS, parse_grid_spacings, select_profile
from .ui import show_fig
from .spacing import adjacent_spacing, integer_spacing_for_grid

# Keep these model identifiers stable; translated labels can use format_func.
INITIAL_DISTRIBUTIONS = [
    "Mean boundary head",
    "Linear between boundaries",
    "Specified uniform head",
    "Random distribution",
]


def capture_input_values():
    """Save incoming widget edits before any conditional widgets disappear."""
    defaults = asdict(Scenario())
    mapping = {"k": "k_ms", "recharge": "recharge_mmy"}
    names = (
        "confined",
        "thickness",
        "aquifer_top",
        "left",
        "right",
        "recharge",
        "k",
        "initial",
        "initial_head",
        "initial_min",
        "initial_max",
        "initial_seed",
    )
    values = st.session_state.setdefault(
        "scenario_values", {key: defaults[mapping.get(key, key)] for key in names}
    )
    for key in values:
        if key in st.session_state:
            values[key] = st.session_state[key]
    options = st.session_state.complexity_options
    for key in options:
        if key in st.session_state:
            options[key] = st.session_state[key]


def scenario_controls():
    """Limited mode exposes confinement, unconfined top and starting heads."""
    values = deepcopy(st.session_state.scenario_values)

    def number(key, label, minimum, maximum, step=None, **kwargs):
        value = st.number_input(
            label,
            minimum,
            maximum,
            value=None if key in st.session_state else values[key],
            step=step,
            key=key,
            **kwargs,
        )
        values[key] = value
        return value

    with st.container(key="scenario_panel"), st.expander(
        TEXT["inputs_parameters_for_the_scenario"]
    ):
        full_settings = st.toggle(
            TEXT["inputs_show_full_settings"],
            value=False,
            key="full_settings",
            help=TEXT["full_settings_help"],
        )
        values["confined"] = st.toggle(
            TEXT["inputs_confined_aquifer"],
            value=values["confined"],
            key="confined",
            help=TEXT["confined_help"],
        )
        if values["confined"]:
            if full_settings:
                number("thickness", TEXT["inputs_aquifer_thickness_m"], 0.1, 1000.0, 0.5)
        else:
            number("aquifer_top", TEXT["inputs_aquifer_top_elevation_m"], 0.1, 1000.0, 0.5)
        if full_settings:
            number("left", TEXT["inputs_west_left_boundary_head_m"], 0.1, 5000.0, 0.5)
            number("right", TEXT["inputs_east_right_boundary_head_m"], 0.1, 5000.0, 0.5)
            number("recharge", TEXT["inputs_recharge_mm_year"], 0.0, 2000.0, 1.0)
            number("k", TEXT["inputs_hydraulic_conductivity_m_s"], 1e-9, 1.0, format="%.3e")
        values["initial"] = st.selectbox(
            TEXT["inputs_starting_head_distribution"],
            INITIAL_DISTRIBUTIONS,
            index=INITIAL_DISTRIBUTIONS.index(values["initial"]),
            key="initial",
        )
        if values["initial"] == "Specified uniform head":
            number(
                "initial_head", TEXT["inputs_uniform_starting_head_elevation_m"], 0.1, 10000.0, 0.5
            )
        elif values["initial"] == "Random distribution":
            number("initial_min", TEXT["inputs_minimum_initial_head_m"], 0.1, 10000.0, 0.5)
            number("initial_max", TEXT["inputs_maximum_initial_head_m"], 0.1, 10000.0, 0.5)
            if full_settings:
                number("initial_seed", TEXT["inputs_initial_head_seed"], 0, 2**31 - 1, 1)
            st.caption(TEXT["initial_random_note"])
        if not full_settings:
            retained = []
            if values["confined"]:
                retained.append(TEXT["retained_thickness"].format(thickness=values["thickness"]))
            retained.extend(
                [
                    TEXT["retained_boundary_heads"].format(
                        left=values["left"], right=values["right"]
                    ),
                    TEXT["retained_recharge"].format(recharge=values["recharge"]),
                    TEXT["retained_conductivity"].format(k=values["k"]),
                ]
            )
            if values["initial"] == "Random distribution":
                retained.append(
                    TEXT["retained_initial_seed"].format(initial_seed=values["initial_seed"])
                )
            st.markdown("\n".join(retained))
            st.caption(TEXT["limited_hint"])
        st.caption(
            TEXT["confined_geometry_note"]
            if values["confined"]
            else TEXT["unconfined_geometry_note"]
        )
    st.session_state.scenario_values = values
    return {
        ("k_ms" if key == "k" else "recharge_mmy" if key == "recharge" else key): value
        for key, value in values.items()
    }


def set_cell_spacing(value):
    """Custom +/- callback; the number field still accepts manual integers."""
    if value is not None:
        st.session_state.cell_spacing = int(value)


def spatial_controls(complexity):
    """Keep the existing exact-length cell-count/spacing conversion."""
    with st.container(key="spatial_panel"), st.expander(TEXT["inputs_spatial_discretization"]):
        length = st.number_input(
            TEXT["inputs_boundary_to_boundary_length_m"], 1.0, 100000.0, 5000.0, 100.0, key="length"
        )
        horizontal = complexity and st.session_state.complexity_options["horizontal_2d"]
        spacing_mode = st.toggle(
            TEXT["inputs_define_cell_spacing_instead_of_cell_count"],
            value=False,
            key="spacing_mode",
        )
        last_n = int(st.session_state.get("grid_n", 11))
        if st.session_state.get("previous_spacing_mode", False) != spacing_mode:
            if spacing_mode:
                st.session_state.cell_spacing = integer_spacing_for_grid(length, last_n)
                if abs(st.session_state.cell_spacing - length / (last_n - 1)) > 1e-9:
                    st.caption(
                        TEXT["integer_mode_note"].format(cell_spacing=st.session_state.cell_spacing)
                    )
            else:
                st.session_state.n = last_n
        error = None
        if spacing_mode:
            if st.session_state.get("cell_spacing") is None:
                st.session_state.cell_spacing = integer_spacing_for_grid(length, last_n)
            # Migrate a previous floating-point widget value to integer input.
            st.session_state.cell_spacing = int(round(st.session_state.cell_spacing))
            label = (
                TEXT["inputs_cell_spacing_x_y_m"] if horizontal else TEXT["inputs_cell_spacing_x_m"]
            )
            st.markdown(label)
            smaller = adjacent_spacing(st.session_state.cell_spacing, length, -1)
            larger = adjacent_spacing(st.session_state.cell_spacing, length, 1)
            with st.container(key="integer_spacing"):
                decrease, entry, increase = st.columns(
                    [1, 2.5, 1], gap="small", vertical_alignment="bottom"
                )
                with decrease:
                    st.button(
                        "−",
                        key="spacing_decrease",
                        width="stretch",
                        disabled=smaller is None,
                        on_click=set_cell_spacing,
                        args=(smaller,),
                        help=(
                            TEXT["inputs_finer_grid_smaller_m"].format(smaller=smaller)
                            if smaller
                            else TEXT["inputs_smallest_spacing_for_this_length"]
                        ),
                    )
                with entry:
                    spacing = st.number_input(
                        label,
                        min_value=1,
                        value=None,
                        step=1,
                        format="%d",
                        key="cell_spacing",
                        label_visibility="collapsed",
                    )
                with increase:
                    st.button(
                        "+",
                        key="spacing_increase",
                        width="stretch",
                        disabled=larger is None,
                        on_click=set_cell_spacing,
                        args=(larger,),
                        help=(
                            TEXT["inputs_coarser_grid_larger_m"].format(larger=larger)
                            if larger
                            else TEXT["inputs_largest_preferred_spacing_for_this_length"]
                        ),
                    )
            st.caption(TEXT["spacing_steps"])
            try:
                n = parse_grid_spacings([spacing], length)[0]
            except ValueError as exc:
                error, n = str(exc), last_n
                st.error(error)
        else:
            n = st.number_input(
                (
                    TEXT["inputs_number_of_cells_along_x_and_y"]
                    if horizontal
                    else TEXT["inputs_number_of_cells_along_x"]
                ),
                3,
                10001,
                None if "n" in st.session_state else last_n,
                1,
                key="n",
                help=TEXT["cell_count_help"],
            )
        if error is None:
            st.session_state.grid_n = int(n)
        st.session_state.previous_spacing_mode = spacing_mode
        st.markdown(
            TEXT["inputs_n_cells_along_x"].format(n=n)
            + (TEXT["inputs_and_n_along_y"].format(n=n) if horizontal else "")
            + TEXT["inputs_x_dx_g_m"].format(dx=length / (n - 1))
        )
        st.caption(TEXT["spacing_geometry_note"])
    return dict(n=int(n), length=length, width=1.0), error


def solver_controls():
    """Render identity, closures, iteration limits, then solver strategy."""
    with st.container(key="solver_panel"), st.expander(TEXT["inputs_numerical_solver"]):
        with st.container(key="solver_identity"):
            st.markdown(TEXT["inputs_model_and_solver"])
            engine = st.selectbox(
                TEXT["inputs_modflow_model"],
                list(ENGINE_NAMES),
                format_func=ENGINE_NAMES.get,
                key="engine",
            )
            choice = st.session_state.choices.get(
                engine, dict(preset="SIMPLE", method=METHODS[engine][0])
            )
            method = st.selectbox(
                TEXT["inputs_solver"] if engine == "mf2005" else TEXT["inputs_linear_solver"],
                METHODS[engine],
                index=METHODS[engine].index(choice["method"]),
                key=f"method_{engine}",
            )
        # Container positions determine visual order; preset selection must be
        # evaluated before loading its profile and drawing the retained values.
        groups = {
            name: st.container(key=f"solver_{name}")
            for name in ("closure", "iterations", "strategy")
        }
        with groups["strategy"]:
            st.markdown(TEXT["inputs_solver_settings"])
            preset = (
                "SIMPLE"
                if engine == "mf2005"
                else st.selectbox(
                    TEXT["inputs_solver_preset"],
                    ["SIMPLE", "MODERATE", "COMPLEX"],
                    index=["SIMPLE", "MODERATE", "COMPLEX"].index(choice["preset"]),
                    key=f"preset_{engine}",
                )
            )
        st.session_state.choices[engine] = dict(preset=preset, method=method)
        profile_id, profile = select_profile(st.session_state, engine, method, preset)
        basic_controls(profile, profile_id, groups=groups)
        st.caption(TEXT["solver_sticky"])
        st.caption(TEXT["solver_units"])
    return profile_id, profile


def regenerate_k():
    """Advance the internal seed only on an explicit request for a new field."""
    seed = (int(st.session_state.complexity_options["k_seed"]) + 1) % (2**31)
    st.session_state.complexity_options["k_seed"] = seed
    st.session_state.k_seed = seed


def select_k_preview():
    """Switch on activation only; subsequent preview choices remain editable."""
    if st.session_state.get("random_k", False):
        st.session_state.preview_quantity = "K zones"


def complexity_controls(enabled):
    options = deepcopy(st.session_state.complexity_options)
    preview_slot = None
    if enabled:
        with st.container(key="complexity_panel"), st.expander(
            TEXT["complexity_title"], expanded=True
        ):
            left, right = st.columns(2)
            with left:
                options["horizontal_2d"] = st.toggle(
                    TEXT["inputs_2d_horizontal_grid_x_y"],
                    value=options["horizontal_2d"],
                    key="horizontal_2d",
                    help=TEXT["horizontal_grid_help"],
                )
                options["add_layers"] = st.toggle(
                    TEXT["inputs_add_layers"], value=options["add_layers"], key="add_layers"
                )
                if options["add_layers"]:
                    with st.container(key="complexity_layers"):
                        options["layers"] = st.number_input(
                            TEXT["inputs_number_of_layers"],
                            2,
                            50,
                            options["layers"],
                            1,
                            key="layers",
                        )
                    st.caption(TEXT["layers_note"])
            with right, st.container(key="complexity_conductivity"):
                options["random_k"] = st.toggle(
                    TEXT["inputs_random_hydraulic_conductivity_field"],
                    value=options["random_k"],
                    key="random_k",
                    on_change=select_k_preview,
                )
                if options["random_k"]:
                    lower, upper = st.columns(2)
                    with lower:
                        options["k_min"] = st.number_input(
                            TEXT["inputs_minimum_k_m_s"],
                            1e-9,
                            1.0,
                            options["k_min"],
                            format="%.3e",
                            key="k_min",
                        )
                    with upper:
                        options["k_max"] = st.number_input(
                            TEXT["inputs_maximum_k_m_s"],
                            1e-9,
                            1.0,
                            options["k_max"],
                            format="%.3e",
                            key="k_max",
                        )
                    zones, refresh = st.columns(2, vertical_alignment="bottom")
                    with zones:
                        options["k_zones"] = st.number_input(
                            TEXT["inputs_k_zones_per_direction"],
                            1,
                            100,
                            options["k_zones"],
                            1,
                            key="k_zones",
                        )
                    with refresh:
                        st.button(
                            TEXT["inputs_new_realization"],
                            key="regenerate_k",
                            on_click=regenerate_k,
                            width="stretch",
                        )
                    st.caption(TEXT["random_k_help"])
            st.caption(TEXT["boundary_note"])
            preview_slot = st.container()
    st.session_state.complexity_options = options
    scenario_values = dict(
        complexity=enabled,
        horizontal_2d=enabled and options["horizontal_2d"],
        nlay=int(options["layers"]) if enabled and options["add_layers"] else 1,
        random_k=enabled and options["random_k"],
        **{key: options[key] for key in ("k_min", "k_max", "k_seed", "k_zones")},
    )
    return scenario_values, preview_slot


def render_model_preview(scenario, slot):
    """Draw from the just-validated scenario, including current confinement."""
    if slot is None:
        return 0
    with slot:
        st.markdown(TEXT["inputs_model_preview"])
        quantity_column, layer_column = st.columns(2)
        with quantity_column:
            quantity = st.selectbox(
                TEXT["inputs_preview"],
                ["Empty cells", "K zones", "Initial heads"],
                key="preview_quantity",
            )
        with layer_column:
            if st.session_state.get("plot_layer", 1) > scenario.nlay:
                st.session_state.plot_layer = 1
            layer = (
                st.number_input(TEXT["inputs_preview_layer"], 1, scenario.nlay, 1, key="plot_layer")
                - 1
                if scenario.nlay > 1
                else 0
            )
        _, framed, _ = st.columns([1, 8, 1])
        with framed, st.container(key="model_preview_frame"):
            show_fig(model_preview(scenario, quantity, layer=layer, row=scenario.nrow // 2))
        st.caption(
            TEXT["preview_caption"].format(
                aquifer=scenario.aquifer_label,
                top=scenario.top,
                bottom=scenario.bottom,
                grid=scenario.grid_label,
                cells=scenario.total_cells,
                row=scenario.nrow // 2 + 1,
            )
        )
        if scenario.random_k and quantity == "K zones":
            bands = scenario.k_zones if scenario.k_min < scenario.k_max else 1
            st.caption(TEXT["k_classes_note"].format(bands=bands))
        stride = display_stride(scenario.n)
        if stride > 1:
            st.caption(TEXT["preview_stride_note"].format(stride=stride))
    return layer
