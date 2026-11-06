"""Basic/expert solver widgets; values are copied to persistent profiles."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   number: line 14
#   basic_controls: line 38
#   expert_controls: line 75
# END CODE CONTENTS

import math
import streamlit as st


def number(label, value, key, minimum=0., maximum=None, help=None):
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
            specs[key] = (.1 if value == 0 else 10.**(math.floor(math.log10(abs(value)))-1),
                          "%.3e" if 0 < abs(value) < .01 else "%.4f")
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
        "hclose": ("Head closure (m)", 1e-10, 10.), "rclose": ("R closure (m³/s)", 1e-16, 10000.),
        "mxiter": ("Maximum SIP iterations" if method == "SIP" else "Maximum outer iterations", 1, 2000),
        "iter1": ("Maximum inner iterations", 1, 10000), "relax": ("Relaxation (RELAX)", 0., 1.),
        "accl": ("Acceleration (ACCL)", .01, 2.),
        "headtol": ("Head closure (m)", 1e-10, 10.), "fluxtol": ("R closure / FLUXTOL (m³/s)", 1e-16, 10000.),
        "maxiterout": ("Maximum outer iterations", 1, 2000),
        "maxitinner": ("Maximum inner iterations", 1, 10000), "mxiterxmd": ("Maximum inner iterations", 1, 10000),
        "outer_dvclose": ("Head closure (m)", 1e-10, 10.), "rcloserecord": ("R closure (m³/s)", 1e-16, 10000.),
        "outer_maximum": ("Maximum outer iterations", 1, 2000), "inner_maximum": ("Maximum inner iterations", 1, 10000),
    }
    if groups is None:
        groups = {name: st.container() for name in ("closure", "iterations", "strategy")}
    fields = {
        "closure": ("hclose", "rclose", "headtol", "fluxtol", "outer_dvclose", "rcloserecord"),
        "iterations": ("mxiter", "iter1", "maxiterout", "maxitinner", "mxiterxmd", "outer_maximum", "inner_maximum"),
        "strategy": ("relax", "accl"),
    }
    for group, names in fields.items():
        with groups[group]:
            if group != "strategy":
                st.markdown("**Closure criteria**" if group == "closure" else "**Maximum iterations**")
            for field in names:
                if field in b:
                    label, lo, hi = specs[field]
                    b[field] = number(label, b[field], f"{prefix}_basic_{field}", lo, hi)
    with groups["strategy"]:
        profile["expert_enabled"] = st.toggle("Use expert settings", value=profile["expert_enabled"], key=f"{prefix}_expert_on")
    if engine == "mf2005" and method == "SIP":
        st.caption("SIP has a head-change test; it has no separate R-closure input.")
    if engine == "mf6":
        st.caption("Basic head closure applies to outer and inner iterations; expert settings can separate them.")


def expert_controls(profile, prefix):
    engine = profile["engine"]
    p = profile["expert"]
    if engine == "mfnwt":
        st.caption("NWT writes SPECIFIED with the selected preset as its starting point. Basic closure and iteration limits remain above.")
    elif engine == "mf6":
        st.caption("These values override IMS preset controls. Basic outer closure and iteration limits remain above.")
    limits = {
        "npcond": (1, 2), "nbpol": (0, 2), "damp": (.01, 1.), "nparm": (1, 10), "ipcalc": (0, 1), "wseed": (0., .999),
        "dbdtheta": (0., 1.), "dbdkappa": (0., 1.), "dbdgamma": (0., 1.), "momfact": (0., 1.),
        "backflag": (0, 1), "maxbackiter": (1, 100), "backtol": (1., 10.), "backreduce": (.01, .99),
        "ilumethod": (1, 2), "levfill": (1, 20), "stoptol": (1e-14, .1), "msdr": (1, 100),
        "iacl": (0, 2), "norder": (0, 2), "level": (1, 30), "north": (1, 100), "iredsys": (0, 1),
        "rrctols": (0., .1), "idroptol": (0, 1), "epsrn": (1e-10, .1), "hclosexmd": (1e-12, 1.),
        "thickfact": (1e-10, 1.), "ibotav": (0, 1),
        "inner_dvclose": (1e-10, 10.), "under_relaxation_gamma": (0., 1.), "under_relaxation_theta": (0., 1.),
        "under_relaxation_kappa": (0., 1.), "under_relaxation_momentum": (0., 1.),
        "backtracking_number": (0, 100), "backtracking_tolerance": (1., 1000000.),
        "backtracking_reduction_factor": (.01, .99), "backtracking_residual_limit": (0., 10000.),
        "relaxation_factor": (0., 1.), "preconditioner_levels": (0, 30),
        "preconditioner_drop_tolerance": (0., 1.), "number_orthogonalizations": (0, 100),
    }
    choices = {"npcond": [1, 2], "nbpol": [0, 2], "ipcalc": [0, 1],
               "ilumethod": [1, 2], "iacl": [0, 1, 2], "norder": [0, 1, 2],
               "residual_test": ["INFINITY", "STRICT", "L2NORM_RCLOSE"],
               "under_relaxation": ["NONE", "SIMPLE", "COOLEY", "DBD"],
               "scaling_method": ["NONE", "DIAGONAL", "L2NORM"], "reordering_method": ["NONE", "RCM", "MD"]}
    labels = {"npcond": "PCG preconditioner (NPCOND)", "nbpol": "Polynomial eigenvalue option (NBPOL)",
              "damp": "Head damping (DAMP)", "nparm": "SIP iteration parameters (NPARM)",
              "ipcalc": "SIP seed calculation (IPCALC)", "wseed": "SIP seed (WSEED)",
              "backtracking_residual_limit": "Backtracking residual limit (m³/s)",
              "hclosexmd": "XMD head closure (m)",
              "inner_dvclose": "Inner head closure (m)", "residual_test": "IMS residual test",
              "under_relaxation": "IMS under-relaxation", "under_relaxation_gamma": "Under-relaxation gamma",
              "under_relaxation_theta": "DBD theta", "under_relaxation_kappa": "DBD kappa",
              "under_relaxation_momentum": "DBD momentum"}
    explanations = {"npcond": "1 = modified incomplete Cholesky; 2 = polynomial.",
                    "nbpol": "0 = calculate the eigenvalue estimate; 2 = assume an upper bound of 2. Used only with NPCOND=2.",
                    "ipcalc": "1 = calculate the seed; 0 = use WSEED.",
                    "iacl": "0 = CG; 1 = ORTHOMIN; 2 = Bi-CGSTAB inside XMD.",
                    "ibotav": "NWT bottom-head adjustment option; inactive for fully confined flow.",
                    "thickfact": "NWT saturation-smoothing interval as a fraction of layer thickness; relevant to convertible flow."}
    columns = st.columns(2)
    for i, (field, value) in enumerate(list(p.items())):
        with columns[i % 2]:
            key = f"{prefix}_expert_{field}"
            label = labels.get(field, field.upper())
            if field in choices:
                options = choices[field]
                p[field] = st.selectbox(label, options, index=options.index(value), key=key, help=explanations.get(field))
            else:
                lo, hi = limits[field]
                if field == "under_relaxation_gamma":
                    key += "_" + p["under_relaxation"]
                    if p["under_relaxation"] == "SIMPLE":
                        lo, value = .01, value if value > 0 else .7
                p[field] = number(label, value, key, lo, hi, explanations.get(field))
