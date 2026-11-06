"""Basic/expert solver widgets; values are copied to persistent profiles."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   number: line 16
#   basic_controls: line 42
#   expert_controls: line 109
# END CODE CONTENTS

import math
import streamlit as st

from .content import TEXT


def number(label, value, key, minimum=0.0, maximum=None, help=None):
    kw = dict(label=label, value=value, key=key, help=help)
    if isinstance(value, int):
        kw.update(min_value=int(minimum), step=1)
        if maximum is not None:
            kw["max_value"] = int(maximum)
    else:
        # Keep widget-defining properties stable after a value is edited.
        spec_key = "number_specs"
        if spec_key not in st.session_state:
            st.session_state[spec_key] = {}
        specs = st.session_state[spec_key]
        if key not in specs:
            specs[key] = (
                0.1 if value == 0 else 10.0 ** (math.floor(math.log10(abs(value))) - 1),
                "%.3e" if 0 < abs(value) < 0.01 else "%.4f",
            )
        step, fmt = specs[key]
        kw.update(min_value=float(minimum), step=step, format=fmt)
        if maximum is not None:
            kw["max_value"] = float(maximum)
    if key in st.session_state:
        kw["value"] = None  # The explicitly synchronised widget state owns its value.
    return st.number_input(**kw)


def basic_controls(profile, prefix, groups=None):
    engine, method = profile["engine"], profile["method"]
    b = profile["basic"]
    specs = {
        "hclose": (TEXT["solver_head_closure_m"], 1e-10, 10.0),
        "rclose": (TEXT["solver_r_closure_m_s"], 1e-16, 10000.0),
        "mxiter": (
            (
                TEXT["solver_maximum_sip_iterations"]
                if method == "SIP"
                else TEXT["solver_maximum_outer_iterations"]
            ),
            1,
            2000,
        ),
        "iter1": (TEXT["solver_maximum_inner_iterations"], 1, 10000),
        "relax": (TEXT["solver_relaxation_relax"], 0.0, 1.0),
        "accl": (TEXT["solver_acceleration_accl"], 0.01, 2.0),
        "headtol": (TEXT["solver_head_closure_m"], 1e-10, 10.0),
        "fluxtol": (TEXT["solver_r_closure_fluxtol_m_s"], 1e-16, 10000.0),
        "maxiterout": (TEXT["solver_maximum_outer_iterations"], 1, 2000),
        "maxitinner": (TEXT["solver_maximum_inner_iterations"], 1, 10000),
        "mxiterxmd": (TEXT["solver_maximum_inner_iterations"], 1, 10000),
        "outer_dvclose": (TEXT["solver_head_closure_m"], 1e-10, 10.0),
        "rcloserecord": (TEXT["solver_r_closure_m_s"], 1e-16, 10000.0),
        "outer_maximum": (TEXT["solver_maximum_outer_iterations"], 1, 2000),
        "inner_maximum": (TEXT["solver_maximum_inner_iterations"], 1, 10000),
    }
    if groups is None:
        groups = {name: st.container() for name in ("closure", "iterations", "strategy")}
    fields = {
        "closure": ("hclose", "rclose", "headtol", "fluxtol", "outer_dvclose", "rcloserecord"),
        "iterations": (
            "mxiter",
            "iter1",
            "maxiterout",
            "maxitinner",
            "mxiterxmd",
            "outer_maximum",
            "inner_maximum",
        ),
        "strategy": ("relax", "accl"),
    }
    for group, names in fields.items():
        with groups[group]:
            if group != "strategy":
                st.markdown(
                    TEXT["solver_closure_criteria"]
                    if group == "closure"
                    else TEXT["solver_maximum_iterations"]
                )
            for field in names:
                if field in b:
                    label, lo, hi = specs[field]
                    b[field] = number(label, b[field], f"{prefix}_basic_{field}", lo, hi)
    with groups["strategy"]:
        profile["expert_enabled"] = st.toggle(
            TEXT["solver_use_expert_settings"],
            value=profile["expert_enabled"],
            key=f"{prefix}_expert_on",
        )
    if engine == "mf2005" and method == "SIP":
        st.caption(TEXT["sip_closure_note"])
    if engine == "mf6":
        st.caption(TEXT["ims_closure_note"])


def expert_controls(profile, prefix):
    engine = profile["engine"]
    p = profile["expert"]
    if engine == "mfnwt":
        st.caption(TEXT["nwt_expert_note"])
    elif engine == "mf6":
        st.caption(TEXT["ims_expert_note"])
    limits = {
        "npcond": (1, 2),
        "nbpol": (0, 2),
        "damp": (0.01, 1.0),
        "nparm": (1, 10),
        "ipcalc": (0, 1),
        "wseed": (0.0, 0.999),
        "dbdtheta": (0.0, 1.0),
        "dbdkappa": (0.0, 1.0),
        "dbdgamma": (0.0, 1.0),
        "momfact": (0.0, 1.0),
        "backflag": (0, 1),
        "maxbackiter": (1, 100),
        "backtol": (1.0, 10.0),
        "backreduce": (0.01, 0.99),
        "ilumethod": (1, 2),
        "levfill": (1, 20),
        "stoptol": (1e-14, 0.1),
        "msdr": (1, 100),
        "iacl": (0, 2),
        "norder": (0, 2),
        "level": (1, 30),
        "north": (1, 100),
        "iredsys": (0, 1),
        "rrctols": (0.0, 0.1),
        "idroptol": (0, 1),
        "epsrn": (1e-10, 0.1),
        "hclosexmd": (1e-12, 1.0),
        "thickfact": (1e-10, 1.0),
        "ibotav": (0, 1),
        "inner_dvclose": (1e-10, 10.0),
        "under_relaxation_gamma": (0.0, 1.0),
        "under_relaxation_theta": (0.0, 1.0),
        "under_relaxation_kappa": (0.0, 1.0),
        "under_relaxation_momentum": (0.0, 1.0),
        "backtracking_number": (0, 100),
        "backtracking_tolerance": (1.0, 1000000.0),
        "backtracking_reduction_factor": (0.01, 0.99),
        "backtracking_residual_limit": (0.0, 10000.0),
        "relaxation_factor": (0.0, 1.0),
        "preconditioner_levels": (0, 30),
        "preconditioner_drop_tolerance": (0.0, 1.0),
        "number_orthogonalizations": (0, 100),
    }
    choices = {
        "npcond": [1, 2],
        "nbpol": [0, 2],
        "ipcalc": [0, 1],
        "ilumethod": [1, 2],
        "iacl": [0, 1, 2],
        "norder": [0, 1, 2],
        "residual_test": ["INFINITY", "STRICT", "L2NORM_RCLOSE"],
        "under_relaxation": ["NONE", "SIMPLE", "COOLEY", "DBD"],
        "scaling_method": ["NONE", "DIAGONAL", "L2NORM"],
        "reordering_method": ["NONE", "RCM", "MD"],
    }
    labels = {
        "npcond": TEXT["solver_pcg_preconditioner_npcond"],
        "nbpol": TEXT["solver_polynomial_eigenvalue_option_nbpol"],
        "damp": TEXT["solver_head_damping_damp"],
        "nparm": TEXT["solver_sip_iteration_parameters_nparm"],
        "ipcalc": TEXT["solver_sip_seed_calculation_ipcalc"],
        "wseed": TEXT["solver_sip_seed_wseed"],
        "backtracking_residual_limit": TEXT["solver_backtracking_residual_limit_m_s"],
        "hclosexmd": TEXT["solver_xmd_head_closure_m"],
        "inner_dvclose": TEXT["solver_inner_head_closure_m"],
        "residual_test": TEXT["solver_ims_residual_test"],
        "under_relaxation": TEXT["solver_ims_under_relaxation"],
        "under_relaxation_gamma": TEXT["solver_under_relaxation_gamma"],
        "under_relaxation_theta": TEXT["solver_dbd_theta"],
        "under_relaxation_kappa": TEXT["solver_dbd_kappa"],
        "under_relaxation_momentum": TEXT["solver_dbd_momentum"],
    }
    explanations = {
        "npcond": TEXT["npcond_help"],
        "nbpol": TEXT["nbpol_help"],
        "ipcalc": TEXT["ipcalc_help"],
        "iacl": TEXT["iacl_help"],
        "ibotav": TEXT["ibotav_help"],
        "thickfact": TEXT["thickfact_help"],
    }
    columns = st.columns(2)
    for i, (field, value) in enumerate(list(p.items())):
        with columns[i % 2]:
            key = f"{prefix}_expert_{field}"
            label = labels.get(field, field.upper())
            if field in choices:
                options = choices[field]
                p[field] = st.selectbox(
                    label,
                    options,
                    index=options.index(value),
                    key=key,
                    help=explanations.get(field),
                )
            else:
                lo, hi = limits[field]
                if field == "under_relaxation_gamma":
                    key += "_" + p["under_relaxation"]
                    if p["under_relaxation"] == "SIMPLE":
                        lo, value = 0.01, value if value > 0 else 0.7
                p[field] = number(label, value, key, lo, hi, explanations.get(field))
