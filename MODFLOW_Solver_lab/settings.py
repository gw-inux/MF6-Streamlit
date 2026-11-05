"""UI state, solver profiles and grid-study settings."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   METHODS: line 42
#   VARIANTS: line 43
#   MAX_RUNS: line 44
#   GRID_DEFAULTS: line 45
#   NWT_GMRES: line 46
#   NWT_XMD: line 47
#   new_profile: line 50
#   MAIN_FIELDS: line 88
#   remember_main_controls: line 96
#   capture_active_profile: line 102
#   select_profile: line 126
#   solver_from_profile: line 143
#   default_variants: line 168
#   effective_settings: line 172
#   limits_summary: line 185
#   preset_label: line 195
#   variant_plan: line 203
#   parse_grid_entries: line 217
#   append_run: line 232
#   parse_grid_spacings: line 237
#   remove_runs: line 261
#   run_table: line 266
#   display_number: line 275
#   settings_table: line 285
#   SPACING_COLUMNS: line 290
#   INTEGER_COLUMNS: line 292
#   formatted_csv: line 296
# END CODE CONTENTS

from copy import deepcopy
from dataclasses import asdict
import math

import pandas as pd

from core import DEFAULT_HEAD_CLOSE, DEFAULT_FLOW_CLOSE, IMS_PRESETS, NWT_PRESETS, SECONDS_PER_DAY, Solver, comparison_row

METHODS = {"mf2005": ("PCG", "SIP"), "mfnwt": ("GMRES", "XMD"), "mf6": ("CG", "BICGSTAB")}
VARIANTS = [f"{engine}/{method}" for engine, methods in METHODS.items() for method in methods]
MAX_RUNS = 10
GRID_DEFAULTS = [11, 101, 1001, 2001, 3001, 4001, 5001, 6001, 8001, 10001]
NWT_GMRES = {"maxitinner", "ilumethod", "levfill", "stoptol", "msdr"}
NWT_XMD = {"iacl", "norder", "level", "north", "iredsys", "rrctols", "idroptol", "epsrn", "hclosexmd", "mxiterxmd"}


def new_profile(engine, method, preset="SIMPLE"):
    """Suggested starting values; header tolerances are separate from NWT presets."""
    if engine == "mf2005":
        basic = (dict(hclose=DEFAULT_HEAD_CLOSE, rclose=DEFAULT_FLOW_CLOSE["mf2005"], mxiter=100, iter1=100, relax=1.) if method == "PCG"
                 else dict(hclose=DEFAULT_HEAD_CLOSE, mxiter=500, accl=1.))
        expert = (dict(npcond=1, nbpol=0, damp=1.) if method == "PCG"
                  else dict(nparm=5, ipcalc=1, wseed=0.))
    elif engine == "mfnwt":
        inner = "maxitinner" if method == "GMRES" else "mxiterxmd"
        basic = dict(headtol=DEFAULT_HEAD_CLOSE, fluxtol=DEFAULT_FLOW_CLOSE["mfnwt"], maxiterout=100, **{inner: NWT_PRESETS[preset][inner]})
        expert = {k: v for k, v in NWT_PRESETS[preset].items()
                  if k != inner and k not in (NWT_XMD if method == "GMRES" else NWT_GMRES)}
        expert.update(thickfact=1e-5, ibotav=0)
        if method == "XMD":
            expert["hclosexmd"] = DEFAULT_HEAD_CLOSE
    else:
        p = IMS_PRESETS[preset]
        basic = dict(outer_dvclose=DEFAULT_HEAD_CLOSE, rcloserecord=DEFAULT_FLOW_CLOSE["mf6"],
                     outer_maximum=p["outer_maximum"], inner_maximum=p["inner_maximum"])
        expert = dict(inner_dvclose=DEFAULT_HEAD_CLOSE, residual_test="INFINITY",
            under_relaxation=p["under_relaxation"], under_relaxation_gamma=0.,
            under_relaxation_theta=p.get("under_relaxation_theta", 1.),
            under_relaxation_kappa=p.get("under_relaxation_kappa", 0.), under_relaxation_momentum=0.,
            backtracking_number=p.get("backtracking_number", 0),
            backtracking_tolerance=p.get("backtracking_tolerance", 1.05),
            backtracking_reduction_factor=p.get("backtracking_reduction_factor", .1),
            backtracking_residual_limit=p.get("backtracking_residual_limit", .002/SECONDS_PER_DAY),
            relaxation_factor=p["relaxation_factor"], preconditioner_levels=p["preconditioner_levels"],
            preconditioner_drop_tolerance=p["preconditioner_drop_tolerance"],
            number_orthogonalizations=p["number_orthogonalizations"],
            scaling_method="DIAGONAL", reordering_method="NONE")
    return dict(engine=engine, method=method, preset=preset, basic=basic,
                expert=expert, expert_enabled=False)



# The four main controls belong to a model, not to a preset or linear method.
# Advanced settings still have their own preset/method profiles.
MAIN_FIELDS = {
    "mf2005": {"hclose": "head", "rclose": "flow", "mxiter": "outer", "iter1": "inner"},
    "mfnwt": {"headtol": "head", "fluxtol": "flow", "maxiterout": "outer",
              "maxitinner": "inner", "mxiterxmd": "inner"},
    "mf6": {"outer_dvclose": "head", "rcloserecord": "flow", "outer_maximum": "outer", "inner_maximum": "inner"},
}


def remember_main_controls(state, profile):
    saved = state.setdefault("main_controls", {}).setdefault(profile["engine"], {})
    saved.update({MAIN_FIELDS[profile["engine"]][key]: value
                  for key, value in profile["basic"].items() if key in MAIN_FIELDS[profile["engine"]]})


def capture_active_profile(state):
    """Capture pending widget edits before a selector can change the profile.

    Streamlit has already delivered widget values at the start of the rerun.
    Reading them here also covers an edit and preset change in the same event.
    """
    prefix = state.get("active_profile")
    if prefix not in state["profiles"]:
        return
    profile = deepcopy(state["profiles"][prefix])
    for group in ("basic", "expert"):
        for field in profile[group]:
            key = f"{prefix}_{group}_{field}"
            if field == "under_relaxation_gamma":
                key += "_" + profile["expert"]["under_relaxation"]
            if key in state:
                profile[group][field] = state[key]
    profile["expert_enabled"] = state.get(f"{prefix}_expert_on", profile["expert_enabled"])
    state["profiles"][prefix] = profile
    remember_main_controls(state, profile)
    if "variants" in state:
        state["variants"][f"{profile['engine']}/{profile['method']}"] = asdict(solver_from_profile(profile))


def select_profile(state, engine, method, preset):
    prefix = f"{engine}_{method}_{preset}"
    stored = state["profiles"].get(prefix)
    profile = deepcopy(stored) if stored is not None else new_profile(engine, method, preset)
    if state.get("active_profile") != prefix:
        saved = state.get("main_controls", {}).get(engine, {})
        for field, meaning in MAIN_FIELDS[engine].items():
            if field in profile["basic"] and meaning in saved:
                profile["basic"][field] = saved[meaning]
        # A previously displayed destination can still have widget state. Update
        # it before rendering, otherwise it wins over the profile's new value.
        for field, value in profile["basic"].items():
            state[f"{prefix}_basic_{field}"] = value
    state["active_profile"] = prefix
    return prefix, profile


def solver_from_profile(profile):
    engine, method, preset = (profile[k] for k in ("engine", "method", "preset"))
    p = deepcopy(profile["basic"])
    specified = False
    if engine == "mfnwt":
        inner = "maxitinner" if method == "GMRES" else "mxiterxmd"
        # Native keywords ignore optional linear settings. Switch explicitly to
        # SPECIFIED if the user edits one, even without the expert panel enabled.
        specified = method == "XMD" or profile["expert_enabled"] or p[inner] != NWT_PRESETS[preset][inner]
        if method == "XMD":
            p["hclosexmd"] = p["headtol"]
        if not specified:
            p.pop(inner)
    if engine == "mf6":
        p["inner_dvclose"] = p["outer_dvclose"]
    if profile["expert_enabled"]:
        expert = deepcopy(profile["expert"])
        if engine == "mf6":
            residual_test = expert.pop("residual_test")
            if residual_test != "INFINITY":
                p["rcloserecord"] = [p["rcloserecord"], residual_test]
        p.update(expert)
    return Solver(engine, method, preset, p, specified)


def default_variants():
    return {v: asdict(solver_from_profile(new_profile(*v.split("/")))) for v in VARIANTS}


def effective_settings(cfg):
    """Numeric reference for native presets, plus every explicit override."""
    p = cfg.parameters()
    if cfg.engine == "mfnwt":
        p = NWT_PRESETS[cfg.preset] | p
        omit = NWT_XMD if cfg.method == "GMRES" else NWT_GMRES
        p = {k: v for k, v in p.items() if k not in omit}
    elif cfg.engine == "mf6":
        p = dict(under_relaxation_gamma=0., under_relaxation_momentum=0.,
                 backtracking_number=0, scaling_method="NONE", reordering_method="NONE") | IMS_PRESETS[cfg.preset] | p
    return p


def limits_summary(cfg):
    p = effective_settings(cfg)
    if cfg.engine == "mf2005":
        return p["hclose"], p.get("rclose"), p["mxiter"], p.get("iter1")
    if cfg.engine == "mfnwt":
        return p["headtol"], p["fluxtol"], p["maxiterout"], p["maxitinner" if cfg.method == "GMRES" else "mxiterxmd"]
    flow = p["rcloserecord"]
    return p["outer_dvclose"], flow[0] if isinstance(flow, list) else flow, p["outer_maximum"], p["inner_maximum"]


def preset_label(cfg):
    if cfg.engine == "mf2005":
        return "User controls"
    if cfg.engine == "mfnwt" and cfg.nwt_specified:
        return f"{cfg.preset} → SPECIFIED"
    return cfg.preset


def variant_plan(variants, executables):
    defaults = default_variants()
    rows = []
    for variant in VARIANTS:
        cfg = Solver(**variants[variant])
        h, r, outer, inner = limits_summary(cfg)
        rows.append({"Variant": variant, "Model / solver": cfg.label, "Preset": preset_label(cfg),
                     "Head closure (m)": h, "Flow closure (m³/s)": r,
                     "Outer / SIP limit": outer, "Inner limit": inner,
                     "Settings source": "Input section edits" if asdict(cfg) != defaults[variant] else "Initial settings",
                     "Executable": "Available" if executables[cfg.engine] else "Not found"})
    return pd.DataFrame(rows)


def parse_grid_entries(entries):
    """One distinct whole cell count per visible field, preserving its order."""
    if not 1 <= len(entries) <= 10:
        raise ValueError("Choose between one and ten grids per study.")
    values = []
    for i, entry in enumerate(entries, 1):
        token = str(entry).strip()
        if not token.isdecimal() or not 3 <= int(token) <= 10001:
            raise ValueError(f"Grid {i}: enter a whole cell count from 3 to 10,001, including both CHD cells.")
        values.append(int(token))
    if len(set(values)) != len(values):
        raise ValueError("Enter a different cell count for each grid; duplicate grids would repeat the same study.")
    return values


def append_run(runs, result, run_id, name):
    item = dict(result, run_id=run_id, run_name=name.strip())
    return [*runs, item][-MAX_RUNS:]


def parse_grid_spacings(entries, length):
    """Uniform spacing with an exact, fixed boundary-centre distance."""
    if not 1 <= len(entries) <= 10:
        raise ValueError("Choose between one and ten grids per study.")
    counts = []
    for i, entry in enumerate(entries, 1):
        try:
            spacing = float(entry)
        except (TypeError, ValueError):
            raise ValueError(f"Grid {i}: enter a positive cell spacing in metres.") from None
        if not math.isfinite(spacing) or spacing <= 0:
            raise ValueError(f"Grid {i}: enter a positive finite cell spacing in metres.")
        intervals = length/spacing
        if not math.isfinite(intervals) or not 2-1e-7 <= intervals <= 10000+1e-7:
            raise ValueError(f"Grid {i}: the spacing must give 3–10,001 cells along x.")
        rounded = round(intervals)
        if not math.isclose(intervals, rounded, rel_tol=1e-7, abs_tol=1e-7):
            raise ValueError(f"Grid {i}: spacing must divide the boundary-to-boundary length exactly; for example {length/10:g} m gives 11 cells.")
        counts.append(rounded+1)
    if len(set(counts)) != len(counts):
        raise ValueError("Enter a different spacing for each grid.")
    return counts


def remove_runs(runs, selected):
    selected = set(selected)
    return [r for r in runs if r["run_id"] not in selected]


def run_table(runs):
    rows = []
    for r in runs:
        row = comparison_row(r)
        rows.append({"Run": r["run_id"], "Name": r["run_name"], **row,
                     "Repeats": r.get("repeats", 1), "Preset": preset_label(Solver(**r["solver"]))})
    return pd.DataFrame(rows)


def display_number(value):
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.3E}" if math.isfinite(value) else "—"
    if isinstance(value, list):
        return " ".join(display_number(v) for v in value)
    return str(value)


def settings_table(cfg):
    return pd.DataFrame([{"Parameter": k.upper(), "Effective value": display_number(v)}
                         for k, v in effective_settings(cfg).items()])


SPACING_COLUMNS = {"Δx (m)", "Δy (m)"}

INTEGER_COLUMNS = {"Run", "Cells", "Layers", "Cells x", "Cells y", "Outer", "Inner", "SIP", "Outer iterations", "Inner iterations",
                   "SIP iterations", "Repeats", "Outer / SIP limit", "Inner limit", "iteration"}


def formatted_csv(frame):
    """Same precision by quantity in every exported comparison table."""
    data = frame.copy()
    for column in data:
        if column in INTEGER_COLUMNS:
            data[column] = data[column].map(lambda v: "" if pd.isna(v) else str(int(v)))
        elif pd.api.types.is_numeric_dtype(data[column]):
            fmt = ".10g" if column in SPACING_COLUMNS else (
                ".4f" if "time" in column.lower() and "(s)" in column else ".3E")
            data[column] = data[column].map(lambda v: "" if pd.isna(v) else format(v, fmt))
    return data.to_csv(index=False)
