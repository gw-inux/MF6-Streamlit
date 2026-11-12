"""Teaching references and a boundary-influence screening calculation.

Theis is used for head CHANGE from each point's pre-stress baseline. It is not
a solution for recharge, finite boundaries, dry cells or borehole losses.
"""

import numpy as np
from scipy.special import exp1

from .config import DAY


def theis_change(times_seconds, radius, discharge, transmissivity, storativity):
    """Head change for signed injection Q; pumping Q is negative."""
    t = np.asarray(times_seconds, dtype=float)
    if min(radius, transmissivity, storativity) <= 0:
        raise ValueError(
            "Theis radius, transmissivity and storativity must be positive."
        )
    result = np.zeros_like(t)
    positive = t > 0
    u = radius**2 * storativity / (4 * transmissivity * t[positive])
    result[positive] = discharge / (4 * np.pi * transmissivity) * exp1(u)
    return result


def effective_properties(s, baseline_head):
    thickness = (
        s.thickness
        if s.confined
        else np.clip(baseline_head - s.bottom, 1e-8, s.thickness)
    )
    storage = s.ss * s.thickness if s.confined or baseline_head >= s.top else s.sy
    return s.conductivity * thickness, storage, thickness


def regular_solution(s, days, radius, baseline_head):
    """Theis + shutdown superposition; approximate Jacob correction if unconfined.

    For a water table, use S_y and invert s' = s - s²/(2 b0).
    This approximation excludes delayed gravity drainage and requires small
    relative drawdown. A negative radicand is masked, never clipped silently.
    """
    if not s.transient or s.combined or not s.well_enabled or len(s.wells) != 1:
        raise ValueError(
            "The transient analytical reference requires a regular active-well scenario."
        )
    trans, store, b0 = effective_properties(s, baseline_head)
    q = s.injection_lps / 1000 if s.injection else -s.pumping_lps / 1000
    duration = (s.injection_days if s.injection else s.pumping_days) * DAY
    seconds = np.asarray(days) * DAY
    change = theis_change(seconds, radius, q, trans, store)
    change -= theis_change(seconds - duration, radius, q, trans, store)
    if not s.confined and baseline_head < s.top:
        squared = b0**2 + 2 * b0 * change
        change = np.sqrt(np.maximum(squared, 0)) - b0
        change = np.where(squared > 0, change, np.nan)
        # The unconfined correction is invalid after reaching the aquifer roof.
        change = np.where(baseline_head + change < s.top, change, np.nan)
    return baseline_head + change


def steady_profile(s):
    """1-D recharge profile between CHD centres, for a homogeneous no-well case."""
    x = np.arange(s.ncol) * s.cell_size
    length = x[-1]
    if s.confined:
        heads = s.left + (s.right - s.left) * x / length
        heads += s.recharge_ms / (2 * s.conductivity * s.thickness) * x * (length - x)
    else:
        left, right = s.left - s.bottom, s.right - s.bottom
        saturated = np.sqrt(
            left**2
            + (right**2 - left**2) * x / length
            + s.recharge_ms / s.conductivity * x * (length - x)
        )
        heads = s.bottom + saturated
        heads[heads >= s.top] = (
            np.nan
        )  # free-surface Dupuit expression is no longer valid
    return x + s.cell_size / 2, heads


def boundary_screen(s, well=None):
    """First-image estimate, not a claim of a sharp radius of influence.

    Sum absolute contributions from four first reflection wells at the
    pumping-cell centre. CHD boundaries pass through reservoir-cell centres;
    north/south no-flow boundaries pass through outer faces. Higher images,
    heterogeneity and nonlinear effects are omitted.
    """
    well = s.wells[0] if well is None else well
    baseline = float(s.starting_heads()[0, well.row, well.col])
    trans, storage, _ = effective_properties(s, baseline)
    d = s.cell_size
    distances = np.array(
        [
            well.col * d,
            (s.ncol - 1 - well.col) * d,
            (well.row + 0.5) * d,
            (s.nrow - well.row - 0.5) * d,
        ]
    )
    days = s.injection_days if s.injection and not s.combined else s.pumping_days
    q = (
        well.injection_lps if s.injection and not s.combined else well.pumping_lps
    ) / 1000
    seconds = days * DAY
    observed = abs(float(theis_change(np.array([seconds]), d, q, trans, storage)[0]))
    images = sum(
        abs(float(theis_change(np.array([seconds]), 2 * dist, q, trans, storage)[0]))
        for dist in distances
    )
    local = abs(
        float(theis_change(np.array([seconds]), distances.min(), q, trans, storage)[0])
    )
    return dict(
        transmissivity=trans,
        storage=storage,
        distance=float(distances.min()),
        drawdown_100m=observed,
        boundary_change=local,
        image_sum=images,
        ratio_pct=100 * images / observed if observed else 0.0,
        days=days,
    )
