"""Input panels with durable values and explicit, reviewable presets.

Widget values are copied to a separate dictionary before conditional widgets
disappear. Hiding full or expert settings never discards a retained value.
"""

from dataclasses import asdict

import streamlit as st

from .config import ENGINES, Observation, Scenario, Solver, Well
from .discretization import adjacent_spacing, count_from_spacing, spacing_from_count

UI_METADATA = {
    "geometry_confined",
    "confined_thickness",
    "unconfined_top",
    "uses_full_extent",
    "last_spacing_mode",
}


def initialize_inputs():
    state = st.session_state
    if "input_values" not in state:
        state.input_values = asdict(Scenario())
        state.input_values["mode"] = "easy"
        state.input_values["engines"] = ["mfnwt"]
        state.input_values["obs_count"] = 1
        state.input_values.update(
            obs_0_name="OBS1", obs_0_row=16, obs_0_col=17, obs_0_layer=1
        )
        for engine in ENGINES:
            for key, value in asdict(Solver(engine)).items():
                if key != "engine":
                    state.input_values[engine + "_" + key] = value
    state.input_values.pop("values", None)
    # Capture frontend changes before rebuilding any conditional panel.
    for key in list(state):
        if (
            key.startswith("input_")
            and key != "input_values"
            and key[6:] not in UI_METADATA
        ):
            state.input_values[key[6:]] = state[key]

    values = state.input_values
    for key, value in asdict(Scenario()).items():
        values.setdefault(key, value)
    if not values.get("uses_full_extent", False):
        set_values({"grid_length": values["ncol"] * values["cell_size"]})
        values["uses_full_extent"] = True
    values["inactive"] = False  # User-defined inactive blocks are no longer offered.
    values.setdefault("well_count", 1)
    for i, direction in enumerate((1, -1)):
        values.setdefault(f"extra_{i}_row", values["nrow"] // 2)
        values.setdefault(
            f"extra_{i}_col",
            max(
                1,
                min(
                    values["ncol"] - 2,
                    values["ncol"] // 2 + direction * max(1, values["ncol"] // 6),
                ),
            ),
        )
        values.setdefault(f"extra_{i}_pumping_lps", 20.0)
        values.setdefault(f"extra_{i}_injection_lps", 20.0)
    _sync_formulation_geometry(values)
    values.setdefault("spacing_mode", False)
    values.setdefault("square_grid", values["ncol"] == values["nrow"])
    values.setdefault(
        "k_mode",
        "random_k_field"
        if values["random_k"]
        else ("zone_k" if values["heterogeneity"] else "uniform_k"),
    )
    values.setdefault(
        "well_operation",
        "combined_well"
        if values["combined"]
        else ("injection_well" if values["injection"] else "pumping_well"),
    )
    # Capture operation before drawing time controls in a different column.
    values["combined"] = values["well_operation"] == "combined_well"
    values["injection"] = values["well_operation"] == "injection_well"


def _sync_formulation_geometry(values):
    """Retain separate teaching inputs for the two vertical conventions.

    Confined: top 0, editable thickness. Unconfined: bottom 0, editable top.
    Resolve geometry before previews, location bounds and native model inputs.
    """
    values.setdefault("confined_thickness", values["thickness"])
    values.setdefault("unconfined_top", 20.0)
    previous = values.get("geometry_confined", True)
    if previous != values["confined"]:
        if previous:
            values["confined_thickness"] = values["thickness"]
        else:
            values["unconfined_top"] = values["top"]
        changes = (
            {"top": 0.0, "thickness": values["confined_thickness"]}
            if values["confined"]
            else {
                "top": values["unconfined_top"],
                "thickness": values["unconfined_top"],
            }
        )
    elif values["confined"]:
        values["confined_thickness"] = values["thickness"]
        changes = {"top": 0.0}
    else:
        values["unconfined_top"] = values["top"]
        changes = {"thickness": values["top"]}
    set_values(changes)
    values["geometry_confined"] = values["confined"]


def set_values(changes):
    """Callback executed before widgets are instantiated on the next rerun."""
    for key, value in changes.items():
        st.session_state.input_values[key] = value
        st.session_state["input_" + key] = value


def apply_preset(name):
    base = asdict(Scenario())
    base.pop("observations")
    base.update(
        obs_count=1, obs_0_name="OBS1", obs_0_row=16, obs_0_col=17, obs_0_layer=1
    )
    if name == "unconfined":
        # Use a water table above a zero-elevation aquifer bottom.
        base.update(
            confined=False,
            top=20.0,
            thickness=20.0,
            left=18.0,
            right=16.0,
            recharge=0.0,
        )
    base.update(
        grid_length=3100.0,
        uses_full_extent=True,
        well_count=1,
        confined_thickness=20.0,
        unconfined_top=20.0,
        geometry_confined=base["confined"],
        spacing_mode=False,
        square_grid=True,
        last_spacing_mode=False,
        k_mode="uniform_k",
        well_operation="pumping_well",
    )
    set_values(base)


def _key(name, default=None):
    values = st.session_state.input_values
    if name not in values:
        values[name] = default
    key = "input_" + name
    if key not in st.session_state:
        st.session_state[key] = values[name]
    return key


def number(t, name, label=None, default=None, **kwargs):
    key = _key(name, default)
    value = st.number_input(t[label or name], key=key, **kwargs)
    st.session_state.input_values[name] = value
    return value


def toggle(t, name, label=None, **kwargs):
    value = st.toggle(t[label or name], key=_key(name, False), **kwargs)
    st.session_state.input_values[name] = value
    return value


def select(t, name, options, label=None, **kwargs):
    value = st.selectbox(
        t[label or name],
        options,
        key=_key(name, options[0]),
        format_func=lambda x: t.get(x, ENGINES.get(x, x)),
        **kwargs,
    )
    st.session_state.input_values[name] = value
    return value


def _cell_input(t, name, maximum, label, **kwargs):
    """Geometry fields store zero-based values but show one-based cell numbers."""
    ui_name = name + "_display"
    current = st.session_state.input_values[name] + 1
    if ui_name not in st.session_state.input_values:
        st.session_state.input_values[ui_name] = current
    value = number(
        t, ui_name, label, min_value=1, max_value=max(1, maximum), step=1, **kwargs
    )
    st.session_state.input_values[name] = int(value) - 1


def _sync_display_cells():
    """Keep preset/location callbacks and display widgets consistent."""
    values = st.session_state.input_values
    for key in (
        "well_row",
        "well_col",
        "extra_0_row",
        "extra_0_col",
        "extra_1_row",
        "extra_1_col",
        "zone_row0",
        "zone_row1",
        "zone_col0",
        "zone_col1",
        "inactive_row0",
        "inactive_row1",
        "inactive_col0",
        "inactive_col1",
    ):
        widget = "input_" + key + "_display"
        # Presets explicitly supply canonical values; callbacks clear display keys.
        if widget not in st.session_state:
            values[key + "_display"] = values[key] + 1


def preset_callback(name):
    apply_preset(name)
    for key in list(st.session_state):
        if key.startswith("input_") and key.endswith("_display"):
            del st.session_state[key]
    for key in list(st.session_state.input_values):
        if key.endswith("_display"):
            del st.session_state.input_values[key]


def centre_well():
    values = st.session_state.input_values
    row, col = values["nrow"] // 2, values["ncol"] // 2
    set_values(
        dict(
            well_row=row,
            well_col=col,
            well_row_display=row + 1,
            well_col_display=col + 1,
        )
    )


def place_observation():
    values = st.session_state.input_values
    col = values["well_col"] + (1 if values["well_col"] < values["ncol"] - 2 else -1)
    set_values(
        dict(
            obs_0_name="OBS1",
            obs_0_row=values["well_row"] + 1,
            obs_0_col=col + 1,
            obs_0_layer=1,
            obs_count=max(1, values["obs_count"]),
        )
    )


def _fit_cell_numbers(t):
    """Keep location widgets valid after a grid reduction and disclose changes."""
    values = st.session_state.input_values
    changed = {}
    for key, value in list(values.items()):
        if key.endswith("_display"):
            maximum = values["nrow"] if "row" in key else values["ncol"]
        elif key.startswith("obs_") and key.endswith(("_row", "_col", "_layer")):
            maximum = (
                values["nrow"]
                if key.endswith("_row")
                else (values["ncol"] if key.endswith("_col") else values["nlay"])
            )
        else:
            continue
        if not 1 <= value <= maximum:
            changed[key] = max(1, min(maximum, value))
    if changed:
        set_values(changed)
        st.info(t["locations_adjusted"])


def render_inputs(t):
    """Three familiar columns; expert controls stay inside their owning panel."""
    initialize_inputs()
    values = st.session_state.input_values
    expert = st.toggle(
        t["expert_settings"], key="expert_settings", help=t["expert_visibility_help"]
    )
    with st.container(key="primary_input_columns"):
        columns = st.columns(3)
        # Resolve the grid before drawing controls whose bounds depend on it.
        # Column order is visual; this evaluation order prevents stale bounds.
        with columns[1]:
            errors = _grid_controls(t, expert)
        _fit_cell_numbers(t)
        _sync_display_cells()
        with columns[0]:
            _scenario_controls(t, expert)
            _boundary_controls(t)
        with columns[1]:
            observations = _observation_controls(t)
        with columns[2]:
            selected, engine = _solver_controls(t, expert)
    if not expert and (
        values["heterogeneity"] or values["random_k"] or values["nlay"] > 1
    ):
        st.info(t["expert_retained"])
    with st.expander(t["presets"]):
        st.markdown(t["preset_help"])
        a, b = st.columns(2)
        a.button(
            t["preset_confined"],
            key="preset_confined",
            on_click=preset_callback,
            args=("confined",),
        )
        b.button(
            t["preset_unconfined"],
            key="preset_unconfined",
            on_click=preset_callback,
            args=("unconfined",),
        )
    scenario_values = {
        key: values[key]
        for key in Scenario.__dataclass_fields__
        if key != "observations"
    }
    scenario_values["observations"] = tuple(observations)
    scenario_values["additional_wells"] = tuple(
        Well(
            name=f"WELL{i + 2}",
            row=values[f"extra_{i}_row"],
            col=values[f"extra_{i}_col"],
            pumping_lps=values[f"extra_{i}_pumping_lps"],
            injection_lps=values[f"extra_{i}_injection_lps"],
        )
        for i in range(values["well_count"] - 1)
    )
    solvers = [
        Solver(
            engine=engine,
            **{
                key: values[engine + "_" + key]
                for key in Solver.__dataclass_fields__
                if key != "engine"
            },
        )
        for engine in selected
    ]
    return Scenario(**scenario_values), solvers, errors


def _scenario_controls(t, expert):
    values = st.session_state.input_values
    with st.container(key="scenario_panel"), st.expander(t["scenario_panel"]):
        full = st.toggle(t["show_full_settings"], key="full_settings")
        toggle(t, "confined", help=t["confined_help"])
        toggle(t, "transient")
        if values["confined"]:
            number(t, "thickness", min_value=0.1, max_value=1000.0, step=1.0)
            st.caption(t["confined_geometry"])
        else:
            number(
                t, "top", min_value=0.1, max_value=1000.0, step=0.5, help=t["top_help"]
            )
            # Capture this edit on the same rerun used for model construction.
            values["thickness"] = values["top"]
            st.caption(t["unconfined_geometry"])
        if full or expert:
            number(
                t,
                "conductivity",
                min_value=1e-10,
                max_value=1.0,
                format="%.3e",
                step=1e-5,
            )
            number(t, "ss", min_value=1e-9, max_value=1.0, format="%.3e", step=1e-5)
            number(t, "sy", min_value=0.001, max_value=1.0, step=0.01)
            st.caption(t["storage_help"])
        else:
            st.markdown(t["retained_parameters"].format(**values))
            st.caption(t["limited_settings_help"])
        if expert:
            number(t, "vertical_ratio", min_value=1e-5, max_value=100.0, format="%.3g")
            with st.container(key="complexity_conductivity"):
                mode = select(t, "k_mode", ["uniform_k", "zone_k", "random_k_field"])
                values["heterogeneity"] = mode == "zone_k"
                values["random_k"] = mode == "random_k_field"
                if values["heterogeneity"]:
                    number(
                        t,
                        "k_factor",
                        min_value=0.0001,
                        max_value=10000.0,
                        format="%.4g",
                    )
                    _rectangle(t, "zone", values)
                    st.caption(t["zone_help"])
                elif values["random_k"]:
                    number(t, "k_min", min_value=1e-10, max_value=1.0, format="%.3e")
                    number(t, "k_max", min_value=1e-10, max_value=1.0, format="%.3e")
                    number(t, "k_zones", min_value=1, max_value=100, step=1)
                    number(t, "k_seed", min_value=0, max_value=2**31 - 1, step=1)
                    st.button(
                        t["new_realization"],
                        key="new_realization",
                        on_click=regenerate_k,
                    )
                    st.caption(t["random_k_help"])


def regenerate_k():
    """Only an explicit new-realization action advances the seed."""
    values = st.session_state.input_values
    set_values({"k_seed": (values["k_seed"] + 1) % (2**31)})


def _grid_controls(t, expert):
    values = st.session_state.input_values
    errors = []
    with st.container(key="spatial_panel"), st.expander(t["spatial_panel"]):
        if expert:
            toggle(t, "square_grid")
        length = number(
            t,
            "grid_length",
            "grid_length" if values["square_grid"] else "grid_length_x",
            min_value=1.0,
            max_value=100000.0,
            step=100.0,
        )
        spacing_mode = toggle(t, "spacing_mode")
        if spacing_mode != values.get("last_spacing_mode", False):
            # Both modes describe the same physical grid when only toggled.
            set_values(
                {"cell_size": values["cell_size"]}
                if spacing_mode
                else {"ncol": values["ncol"]}
            )
        try:
            if spacing_mode:
                smaller = adjacent_spacing(values["cell_size"], length, -1)
                larger = adjacent_spacing(values["cell_size"], length, 1)
                st.markdown(t["cell_size"])
                with st.container(key="spacing_input"):
                    less, entry, more = st.columns(
                        [1, 2.5, 1], gap="small", vertical_alignment="bottom"
                    )
                    less.button(
                        "−",
                        key="spacing_less",
                        disabled=smaller is None,
                        on_click=set_values,
                        args=({"cell_size": float(smaller or 1)},),
                        help=t["finer_spacing"],
                        width="stretch",
                    )
                    with entry:
                        spacing = number(
                            t,
                            "cell_size",
                            min_value=0.001,
                            max_value=25000.0,
                            step=1.0,
                            format="%.6g",
                            label_visibility="collapsed",
                        )
                    more.button(
                        "+",
                        key="spacing_more",
                        disabled=larger is None,
                        on_click=set_values,
                        args=({"cell_size": float(larger or 1)},),
                        help=t["coarser_spacing"],
                        width="stretch",
                    )
                values["ncol"] = count_from_spacing(length, spacing)
            else:
                count = number(
                    t,
                    "ncol",
                    "ncol_xy" if values["square_grid"] else "ncol",
                    min_value=5,
                    max_value=151,
                    step=1,
                )
                values["cell_size"] = spacing_from_count(length, count)
        except ValueError as error:
            errors.append(t[str(error)])
        values["last_spacing_mode"] = spacing_mode
        if values["square_grid"]:
            values["nrow"] = values["ncol"]
        elif expert:
            number(t, "nrow", min_value=5, max_value=151, step=1)
        st.caption(
            t["resolved_grid"].format(
                nx=values["ncol"],
                ny=values["nrow"],
                size=values["cell_size"],
                lx=values["ncol"] * values["cell_size"],
                ly=values["nrow"] * values["cell_size"],
            )
        )
        st.caption(t["spacing_geometry_note"])
        if expert:
            with st.container(key="complexity_layers"):
                number(t, "nlay", min_value=1, max_value=10, step=1)
        else:
            st.caption(t["retained_layers"].format(layers=values["nlay"]))
        if values["transient"]:
            st.markdown(t["temporal_settings"])
            if values["combined"] or not values["injection"]:
                number(t, "pumping_days", min_value=0.01, max_value=3650.0, step=1.0)
            if values["combined"] or values["injection"]:
                number(t, "injection_days", min_value=0.01, max_value=3650.0, step=1.0)
            number(t, "rest_days", min_value=0.01, max_value=3650.0, step=1.0)
            if expert:
                number(t, "steps", min_value=1, max_value=300, step=1)
                number(t, "multiplier", min_value=1.0, max_value=1.3, step=0.01)
                st.caption(t["time_help"])
        st.caption(t["grid_help"])
    return errors


def _boundary_controls(t):
    values = st.session_state.input_values
    with st.container(key="boundary_panel"), st.expander(t["boundary_panel"]):
        number(t, "left", step=0.5)
        number(t, "right", step=0.5)
        number(t, "recharge", min_value=0.0, max_value=10000.0, step=10.0)
        st.markdown(t["well_boundary"])
        toggle(t, "well_enabled")
        operation = select(
            t, "well_operation", ["pumping_well", "injection_well", "combined_well"]
        )
        values["combined"] = operation == "combined_well"
        values["injection"] = operation == "injection_well"
        count = st.selectbox(t["well_count"], [1, 2, 3], key=_key("well_count", 1))
        values["well_count"] = count
        for i in range(count):
            if count > 1:
                st.markdown(t["well_heading"].format(number=i + 1))
            prefix = "" if i == 0 else f"extra_{i - 1}_"
            if values["combined"]:
                st.markdown(t["well_rates_heading"])
                pump, inject = st.columns(2)
                with pump:
                    number(
                        t,
                        prefix + "pumping_lps",
                        "pumping_lps",
                        min_value=0.0,
                        max_value=10000.0,
                        step=1.0,
                        label_visibility="collapsed",
                        help=t["pumping_lps"],
                    )
                with inject:
                    number(
                        t,
                        prefix + "injection_lps",
                        "injection_lps",
                        min_value=0.0,
                        max_value=10000.0,
                        step=1.0,
                        label_visibility="collapsed",
                        help=t["injection_lps"],
                    )
            else:
                rate = "injection_lps" if values["injection"] else "pumping_lps"
                number(
                    t, prefix + rate, rate, min_value=0.0, max_value=10000.0, step=1.0
                )
            st.markdown(t["well_cell_heading"])
            x, y = st.columns(2)
            with x:
                _cell_input(
                    t,
                    "well_col" if i == 0 else prefix + "col",
                    values["ncol"],
                    "cell_x",
                    label_visibility="collapsed",
                    help=t["cell_x"],
                )
            with y:
                _cell_input(
                    t,
                    "well_row" if i == 0 else prefix + "row",
                    values["nrow"],
                    "cell_y",
                    label_visibility="collapsed",
                    help=t["cell_y"],
                )
            if i == 0:
                st.button(t["centre_well"], key="centre_well", on_click=centre_well)
        if count > 1:
            st.caption(t["multiple_wells_help"])
        st.caption(t["well_help"])


def _solver_controls(t, expert):
    values = st.session_state.input_values
    with (
        st.container(key="solver_panel"),
        st.expander(t["solver_panel"], expanded=False),
    ):
        with st.container(key="solver_identity"):
            st.markdown(t["solver_identity"])
            selected = st.multiselect(
                t["engines"],
                list(ENGINES),
                key=_key("engines"),
                format_func=ENGINES.get,
            )
            values["engines"] = selected
            options = selected or list(ENGINES)
            if st.session_state.get("settings_engine") not in options:
                st.session_state.settings_engine = options[0]
            engine = st.selectbox(
                t["settings_engine"],
                options,
                key="settings_engine",
                format_func=ENGINES.get,
                disabled=len(options) == 1,
            )
            if engine == "mfnwt":
                method = st.selectbox(
                    t["nwt_method"],
                    [1, 2],
                    key=_key(engine + "_nwt_method"),
                    format_func=lambda x: "GMRES" if x == 1 else "XMD",
                )
                values[engine + "_nwt_method"] = method
            else:
                st.caption(t["pcg_method" if engine == "mf2005" else "ims_method"])
        with st.container(key="solver_closure"):
            st.markdown(t["solver_closure"])
            number(
                t,
                engine + "_head_close",
                "head_close",
                min_value=1e-10,
                max_value=1.0,
                format="%.2e",
            )
            number(
                t,
                engine + "_flow_close",
                "flow_close",
                min_value=1e-12,
                max_value=1.0,
                format="%.2e",
            )
        with st.container(key="solver_iterations"):
            st.markdown(t["solver_iterations"])
            number(
                t, engine + "_outer", "outer_limit", min_value=1, max_value=5000, step=1
            )
            number(
                t, engine + "_inner", "inner_limit", min_value=1, max_value=5000, step=1
            )
        with st.container(key="solver_strategy"):
            if expert:
                _solver_expert_controls(t, engine)
        st.caption(t["solver_help"])
    return selected, engine


def _observation_controls(t):
    values = st.session_state.input_values
    observations = []
    with (
        st.container(key="observation_panel"),
        st.expander(t["observation_panel"], expanded=False),
    ):
        number(t, "obs_count", min_value=0, max_value=12, step=1)
        st.button(
            t["place_observation"], key="place_observation", on_click=place_observation
        )
        st.caption(t["observation_help"])
        for i in range(values["obs_count"]):
            if i:
                st.divider()
            name = f"obs_{i}_name"
            values[name] = st.text_input(
                t["observation_name"], key=_key(name, f"OBS{i + 1}")
            )
            col = number(
                t,
                f"obs_{i}_col",
                "cell_x",
                default=min(values["ncol"], values["well_col"] + i + 2),
                min_value=1,
                max_value=values["ncol"],
                step=1,
            )
            row = number(
                t,
                f"obs_{i}_row",
                "cell_y",
                default=values["well_row"] + 1,
                min_value=1,
                max_value=values["nrow"],
                step=1,
            )
            layer = (
                number(
                    t,
                    f"obs_{i}_layer",
                    "layer",
                    default=1,
                    min_value=1,
                    max_value=values["nlay"],
                    step=1,
                )
                if values["nlay"] > 1
                else 1
            )
            observations.append(Observation(values[name], row - 1, col - 1, layer - 1))
    return observations


def _rectangle(t, prefix, values):
    _cell_input(t, prefix + "_col0", values["ncol"], "zone_x_start")
    _cell_input(t, prefix + "_col1", values["ncol"], "zone_x_end")
    _cell_input(t, prefix + "_row0", values["nrow"], "zone_y_start")
    _cell_input(t, prefix + "_row1", values["nrow"], "zone_y_end")


def _solver_expert_controls(t, engine):
    prefix = engine + "_"
    with st.container(key="expert_strategy"):
        st.markdown(t["expert_strategy"])
        if engine == "mf2005":
            number(
                t,
                prefix + "damping",
                "damping",
                min_value=0.01,
                max_value=1.0,
                step=0.05,
            )
        elif engine == "mfnwt":
            value = st.selectbox(t["ibotav"], [0, 1], key=_key(prefix + "ibotav"))
            st.session_state.input_values[prefix + "ibotav"] = value
        else:
            toggle(t, prefix + "newton", "newton")
    with st.container(key="expert_wetting"):
        st.markdown(t["expert_wetting"])
        if engine != "mfnwt":
            toggle(t, prefix + "rewet", "rewet")
            number(
                t,
                prefix + "wetdry",
                "wetdry",
                min_value=0.00001,
                max_value=10.0,
                format="%.4g",
            )
        if engine != "mf2005":
            number(
                t,
                prefix + "flow_reduction",
                "flow_reduction",
                min_value=0.001,
                max_value=1.0,
                step=0.01,
            )
    with st.container(key="expert_execution"):
        st.markdown(t["expert_execution"])
        number(
            t, prefix + "timeout", "timeout", min_value=5.0, max_value=600.0, step=10.0
        )
