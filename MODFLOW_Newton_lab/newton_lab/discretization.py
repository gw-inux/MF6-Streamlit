"""Exact conversion between full model extent, cell count and spacing."""

import math


def count_from_spacing(length, spacing):
    """Full outer-face model extent: length = count * spacing.

    Reject non-divisors instead of silently moving boundaries or resizing
    cells. Square cells use the same returned spacing in both directions.
    """
    if (
        not math.isfinite(length)
        or not math.isfinite(spacing)
        or min(length, spacing) <= 0
    ):
        raise ValueError("grid_positive")
    intervals = length / spacing
    nearest = round(intervals)
    if not math.isclose(intervals, nearest, rel_tol=0, abs_tol=1e-8):
        raise ValueError("grid_nondivisor")
    count = nearest
    if not 5 <= count <= 151:
        raise ValueError("grid_count_range")
    return count


def spacing_from_count(length, count):
    if not math.isfinite(length) or length <= 0 or not 5 <= count <= 151:
        raise ValueError("grid_count_range")
    return length / count


PREFERRED_SPACINGS = (
    1,
    2,
    3,
    5,
    10,
    20,
    25,
    50,
    100,
    200,
    250,
    500,
    1000,
    2000,
    2500,
    5000,
    10000,
    20000,
    25000,
)


def adjacent_spacing(value, length, direction):
    """Solver Lab +/- steps skip sizes that cannot preserve the extent."""
    valid = []
    for spacing in PREFERRED_SPACINGS:
        try:
            count_from_spacing(length, spacing)
        except ValueError:
            continue
        valid.append(spacing)
    choices = reversed(valid) if direction < 0 else iter(valid)
    return next(
        (x for x in choices if (x < value if direction < 0 else x > value)), None
    )
