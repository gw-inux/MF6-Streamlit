"""Input panels: retained scenario values, grid controls and solver groups.

Widget keys are transient; scenario_values and complexity_options own values
that must survive hiding inputs. Model assembly remains in core.Scenario.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   capture_input_values: line 34
#   scenario_controls: line 51
#   set_cell_spacing: line 108
#   spatial_controls: line 114
#   solver_controls: line 169
#   regenerate_k: line 194
#   select_k_preview: line 201
#   complexity_controls: line 207
#   render_model_preview: line 245
# END CODE CONTENTS

from copy import deepcopy
from dataclasses import asdict

import streamlit as st

from content import TEXT
from controls import basic_controls
from core import ENGINE_NAMES, Scenario
from plots import display_stride, model_preview
from settings import METHODS, parse_grid_spacings, select_profile
from ui import show_fig
from spacing import adjacent_spacing, integer_spacing_for_grid


def capture_input_values():
    """Save incoming widget edits before any conditional widgets disappear."""
    defaults = asdict(Scenario())
    mapping = {"k": "k_ms", "recharge": "recharge_mmy"}
    names = ("confined", "thickness", "aquifer_top", "left", "right", "recharge", "k",
             "initial", "initial_head", "initial_min", "initial_max", "initial_seed")
    values = st.session_state.setdefault("scenario_values", {
        key: defaults[mapping.get(key, key)] for key in names})
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
        value = st.number_input(label, minimum, maximum,
            value=None if key in st.session_state else values[key],
            step=step, key=key, **kwargs)
        values[key] = value
        return value

    with st.container(key="scenario_panel"), st.expander("**Parameters for the scenario**"):
        full_settings = st.toggle("Show full settings", value=False, key="full_settings",
            help=TEXT["full_settings_help"])
        values["confined"] = st.toggle("Confined aquifer", value=values["confined"], key="confined",
            help="Switch off for unconfined / convertible flow with the bottom fixed at 0 m.")
        if values["confined"]:
            if full_settings:
                number("thickness", "Aquifer thickness (m)", .1, 1000., .5)
        else:
            number("aquifer_top", "Aquifer top elevation (m)", .1, 1000., .5)
        if full_settings:
            number("left", "West / left boundary head (m)", .1, 5000., .5)
            number("right", "East / right boundary head (m)", .1, 5000., .5)
            number("recharge", "Recharge (mm/year)", 0., 2000., 1.)
            number("k", "Hydraulic conductivity (m/s)", 1e-9, 1., format="%.3e")
        values["initial"] = st.selectbox("Starting-head distribution",
            ["Mean boundary head", "Linear between boundaries", "Specified uniform head", "Random distribution"],
            index=["Mean boundary head", "Linear between boundaries", "Specified uniform head", "Random distribution"].index(values["initial"]),
            key="initial")
        if values["initial"] == "Specified uniform head":
            number("initial_head", "Uniform starting head elevation (m)", .1, 10000., .5)
        elif values["initial"] == "Random distribution":
            number("initial_min", "Minimum initial head (m)", .1, 10000., .5)
            number("initial_max", "Maximum initial head (m)", .1, 10000., .5)
            if full_settings:
                number("initial_seed", "Initial-head seed", 0, 2**31-1, 1)
            st.caption("Uniform random initial heads between these limits; specified heads override the guess at the boundaries.")
        if not full_settings:
            retained = []
            if values["confined"]:
                retained.append(f"- Aquifer thickness: **{values['thickness']:g} m**")
            retained.extend([
                f"- West / east heads: **{values['left']:g} / {values['right']:g} m**",
                f"- Recharge: **{values['recharge']:g} mm/year**",
                f"- Homogeneous K: **{values['k']:.2E} m/s**"])
            if values["initial"] == "Random distribution":
                retained.append(f"- Initial-head seed: **{values['initial_seed']}**")
            st.markdown("\n".join(retained))
            st.caption(TEXT["limited_hint"])
        st.caption("Confined: roof 0 m; bottom −b." if values["confined"] else
                   "Unconfined / convertible: bottom 0 m; the saturated thickness follows the head up to the aquifer top.")
    st.session_state.scenario_values = values
    return {("k_ms" if key == "k" else "recharge_mmy" if key == "recharge" else key): value
            for key, value in values.items()}


def set_cell_spacing(value):
    """Custom +/- callback; the number field still accepts manual integers."""
    if value is not None:
        st.session_state.cell_spacing = int(value)


def spatial_controls(complexity):
    """Keep the existing exact-length cell-count/spacing conversion."""
    with st.container(key="spatial_panel"), st.expander("**Spatial discretization**"):
        length = st.number_input("Boundary-to-boundary length (m)", 1., 100000., 5000., 100., key="length")
        horizontal = complexity and st.session_state.complexity_options["horizontal_2d"]
        spacing_mode = st.toggle("Define cell spacing instead of cell count", value=False, key="spacing_mode")
        last_n = int(st.session_state.get("grid_n", 11))
        if st.session_state.get("previous_spacing_mode", False) != spacing_mode:
            if spacing_mode:
                st.session_state.cell_spacing = integer_spacing_for_grid(length, last_n)
                if abs(st.session_state.cell_spacing - length/(last_n-1)) > 1e-9:
                    st.caption(f"Integer mode starts at {st.session_state.cell_spacing} m; the boundary distance stays unchanged.")
            else:
                st.session_state.n = last_n
        error = None
        if spacing_mode:
            if st.session_state.get("cell_spacing") is None:
                st.session_state.cell_spacing = integer_spacing_for_grid(length, last_n)
            # Migrate a previous floating-point widget value to integer input.
            st.session_state.cell_spacing = int(round(st.session_state.cell_spacing))
            label = "Cell spacing Δx / Δy (m)" if horizontal else "Cell spacing Δx (m)"
            st.markdown(label)
            smaller = adjacent_spacing(st.session_state.cell_spacing, length, -1)
            larger = adjacent_spacing(st.session_state.cell_spacing, length, 1)
            with st.container(key="integer_spacing"):
                decrease, entry, increase = st.columns([1, 2.5, 1], gap="small", vertical_alignment="bottom")
                with decrease:
                    st.button("−", key="spacing_decrease", width="stretch", disabled=smaller is None,
                        on_click=set_cell_spacing, args=(smaller,),
                        help=f"Finer grid: {smaller} m" if smaller else "Smallest spacing for this length.")
                with entry:
                    spacing = st.number_input(label, min_value=1, value=None, step=1,
                        format="%d", key="cell_spacing", label_visibility="collapsed")
                with increase:
                    st.button("+", key="spacing_increase", width="stretch", disabled=larger is None,
                        on_click=set_cell_spacing, args=(larger,),
                        help=f"Coarser grid: {larger} m" if larger else "Largest preferred spacing for this length.")
            st.caption(TEXT["spacing_steps"])
            try:
                n = parse_grid_spacings([spacing], length)[0]
            except ValueError as exc:
                error, n = str(exc), last_n
                st.error(error)
        else:
            n = st.number_input("Number of cells along x and y" if horizontal else "Number of cells along x",
                3, 10001, None if "n" in st.session_state else last_n, 1, key="n",
                help="Includes both fixed-head end cells.")
        if error is None:
            st.session_state.grid_n = int(n)
        st.session_state.previous_spacing_mode = spacing_mode
        st.markdown(f"**{n} cells** along x" + (f" and **{n}** along y" if horizontal else "") + f" · Δx = {length/(n-1):g} m")
        st.caption("Distance is between CHD cell centres. Δx = L/(N−1); spacing must divide L exactly.")
    return dict(n=int(n), length=length, width=1.), error


def solver_controls():
    """Render identity, closures, iteration limits, then solver strategy."""
    with st.container(key="solver_panel"), st.expander("**Numerical solver**"):
        with st.container(key="solver_identity"):
            st.markdown("**Model and solver**")
            engine = st.selectbox("MODFLOW model", list(ENGINE_NAMES), format_func=ENGINE_NAMES.get, key="engine")
            choice = st.session_state.choices.get(engine, dict(preset="SIMPLE", method=METHODS[engine][0]))
            method = st.selectbox("Solver" if engine == "mf2005" else "Linear solver", METHODS[engine],
                index=METHODS[engine].index(choice["method"]), key=f"method_{engine}")
        # Container positions determine visual order; preset selection must be
        # evaluated before loading its profile and drawing the retained values.
        groups = {name: st.container(key=f"solver_{name}") for name in ("closure", "iterations", "strategy")}
        with groups["strategy"]:
            st.markdown("**Solver settings**")
            preset = "SIMPLE" if engine == "mf2005" else st.selectbox(
                "Solver preset", ["SIMPLE", "MODERATE", "COMPLEX"],
                index=["SIMPLE", "MODERATE", "COMPLEX"].index(choice["preset"]), key=f"preset_{engine}")
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
        with st.container(key="complexity_panel"), st.expander(TEXT["complexity_title"], expanded=True):
            left, right = st.columns(2)
            with left:
                options["horizontal_2d"] = st.toggle("2D horizontal grid (x–y)", value=options["horizontal_2d"], key="horizontal_2d",
                    help="Off: one horizontal row. On: square grid, Nx = Ny and Δx = Δy. North and south are no-flow.")
                options["add_layers"] = st.toggle("Add layers", value=options["add_layers"], key="add_layers")
                if options["add_layers"]:
                    with st.container(key="complexity_layers"):
                        options["layers"] = st.number_input("Number of layers", 2, 50, options["layers"], 1, key="layers")
                    st.caption("Equal layer thicknesses. Recharge enters the highest wet active cell; vertical flow connects the layers.")
            with right, st.container(key="complexity_conductivity"):
                options["random_k"] = st.toggle("Random hydraulic-conductivity field", value=options["random_k"], key="random_k", on_change=select_k_preview)
                if options["random_k"]:
                    lower, upper = st.columns(2)
                    with lower:
                        options["k_min"] = st.number_input("Minimum K (m/s)", 1e-9, 1., options["k_min"], format="%.3e", key="k_min")
                    with upper:
                        options["k_max"] = st.number_input("Maximum K (m/s)", 1e-9, 1., options["k_max"], format="%.3e", key="k_max")
                    zones, refresh = st.columns(2, vertical_alignment="bottom")
                    with zones:
                        options["k_zones"] = st.number_input("K zones per direction", 1, 100, options["k_zones"], 1, key="k_zones")
                    with refresh:
                        st.button("New realization", key="regenerate_k", on_click=regenerate_k, width="stretch")
                    st.caption(TEXT["random_k_help"])
            st.caption(TEXT["boundary_note"])
            preview_slot = st.container()
    st.session_state.complexity_options = options
    scenario_values = dict(complexity=enabled, horizontal_2d=enabled and options["horizontal_2d"],
        nlay=int(options["layers"]) if enabled and options["add_layers"] else 1,
        random_k=enabled and options["random_k"],
        **{key: options[key] for key in ("k_min", "k_max", "k_seed", "k_zones")})
    return scenario_values, preview_slot


def render_model_preview(scenario, slot):
    """Draw from the just-validated scenario, including current confinement."""
    if slot is None:
        return 0
    with slot:
        st.markdown("**Model preview**")
        quantity_column, layer_column = st.columns(2)
        with quantity_column:
            quantity = st.selectbox("Preview", ["Empty cells", "K zones", "Initial heads"], key="preview_quantity")
        with layer_column:
            if st.session_state.get("plot_layer", 1) > scenario.nlay:
                st.session_state.plot_layer = 1
            layer = st.number_input("Preview layer", 1, scenario.nlay, 1, key="plot_layer") - 1 if scenario.nlay > 1 else 0
        _, framed, _ = st.columns([1, 8, 1])
        with framed, st.container(key="model_preview_frame"):
            show_fig(model_preview(scenario, quantity, layer=layer, row=scenario.nrow//2))
        st.caption(TEXT["preview_caption"].format(aquifer=scenario.aquifer_label, top=scenario.top,
            bottom=scenario.bottom, grid=scenario.grid_label, cells=scenario.total_cells, row=scenario.nrow//2+1))
        if scenario.random_k and quantity == "K zones":
            bands = scenario.k_zones if scenario.k_min < scenario.k_max else 1
            st.caption(f"{bands} numbered logarithmic K classes; the colour bar gives class midpoints. Native K values are unchanged.")
        stride = display_stride(scenario.n)
        if stride > 1:
            st.caption(f"For visibility, only every {stride}-th grid line is drawn, plus the domain edges. All cell values are retained.")
    return layer
