"""Pure comparison helpers: no interpolation, regridding, or data mutation."""

import numpy as np

from .outputs import groundwater_surface


def matching_time_index(reference, other, index):
    """Current-batch engine comparisons require identical physical inputs."""
    if not other.get("success") or reference["scenario"] != other["scenario"]:
        return None
    matches = np.flatnonzero(
        np.isclose(other["days"], reference["days"][index], rtol=0, atol=1e-6)
    )
    return int(matches[-1]) if len(matches) else None


def surface_difference(reference, other, index):
    """Return other-reference and wet-state disagreement at a common time.

    NaN is retained where a difference is undefined. A dry cell must never
    be converted to zero head or zero difference merely for display.
    """
    match = matching_time_index(reference, other, index)
    if match is None:
        return None
    ref = groundwater_surface(reference["scenario"], reference["heads"][index])
    alt = groundwater_surface(other["scenario"], other["heads"][match])
    paired = np.isfinite(ref) & np.isfinite(alt)
    difference = np.full(ref.shape, np.nan)
    np.subtract(alt, ref, out=difference, where=paired)
    mismatch = np.isfinite(ref) != np.isfinite(alt)
    return difference, mismatch
