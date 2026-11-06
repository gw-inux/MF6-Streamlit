"""Display closure guides from the inspected run, without changing its solver.

Only draw a horizontal limit when it matches the plotted quantity. NWT FLUXTOL
and IMS L2 criteria are annotated separately from maximum-cell residual traces.
Native iteration histories, values and the available iteration levels stay intact.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   convergence_guides: line 16
# END CODE CONTENTS

from settings import effective_settings


def convergence_guides(solver, kind):
    """Return comparable (value, label) lines plus any residual-norm annotation."""
    p = effective_settings(solver)
    guides = {"head_change": None, "residual": None, "residual_note": ""}
    if solver.engine == "mf2005":
        guides["head_change"] = (p["hclose"], "HCLOSE")
        if solver.method == "PCG":
            guides["residual"] = (p["rclose"], "RCLOSE")
    elif solver.engine == "mfnwt":
        guides["head_change"] = (p["headtol"], "HEADTOL")
        guides["residual_note"] = (
            f"FLUXTOL = {p['fluxtol']:.2E} m³/s\n"
            "Flux-norm criterion; this trace shows\nthe maximum cell residual.")
    elif kind == "outer":
        guides["head_change"] = (p["outer_dvclose"], "OUTER_DVCLOSE")
        guides["residual_note"] = "Flow closure is evaluated in the inner solver."
    else:
        guides["head_change"] = (p["inner_dvclose"], "INNER_DVCLOSE")
        record = p["rcloserecord"]
        value, option = (record[0], str(record[1]).upper()) if isinstance(record, (list, tuple)) else (record, "INFINITY")
        if option in ("INFINITY", "STRICT"):
            guides["residual"] = (value, "INNER_RCLOSE" + (" · STRICT" if option == "STRICT" else ""))
        else:
            guides["residual_note"] = (f"INNER_RCLOSE = {value:.2E} ({option})\n"
                "Different residual norm; not a threshold\nfor this maximum-residual trace.")
    return guides
