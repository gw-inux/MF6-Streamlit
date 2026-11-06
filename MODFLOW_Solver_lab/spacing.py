"""Integer spacing controls without changing the fixed boundary-centre distance.

Manual integer entries remain possible. The +/- buttons move through the
preferred teaching values, skipping values that cannot fit the current length.
Grid-refinement text entries still support fractional spacings as before.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   SPACING_STEPS: line 20
#   valid_spacing_steps: line 24
#   adjacent_spacing: line 36
#   integer_spacing_for_grid: line 44
# END CODE CONTENTS

import math

from .settings import parse_grid_spacings

SPACING_STEPS = (1, 2, 3, 5, 10, 20, 25, 50, 100, 200, 250, 500,
                 1000, 2000, 2500, 5000, 10000, 20000, 25000, 50000)


def valid_spacing_steps(length):
    """Return preferred values that preserve length and the column-count limit."""
    valid = []
    for spacing in SPACING_STEPS:
        try:
            parse_grid_spacings([spacing], length)
        except ValueError:
            continue
        valid.append(spacing)
    return valid


def adjacent_spacing(value, length, direction):
    """Nearest preferred value above/below the entered value, or None."""
    choices = valid_spacing_steps(length)
    if direction < 0:
        return next((v for v in reversed(choices) if v < value), None)
    return next((v for v in choices if v > value), None)


def integer_spacing_for_grid(length, cells):
    """Keep an already integral spacing, else use the nearest valid integer.

    A fractional boundary distance cannot be divided into integer-metre cells
    exactly. In that case return a readable integer suggestion; the unchanged
    grid validator explains that cell-count mode or a different length is needed.
    """
    current = length / (cells - 1)
    if math.isclose(current, round(current), rel_tol=0., abs_tol=1e-9) and current >= 1:
        return int(round(current))
    rounded_length = round(length)
    if not math.isclose(length, rounded_length, rel_tol=0., abs_tol=1e-9):
        return max(1, int(round(current)))
    divisors = set()
    for divisor in range(1, math.isqrt(rounded_length) + 1):
        if rounded_length % divisor == 0:
            for candidate in (divisor, rounded_length // divisor):
                if 2 <= rounded_length // candidate <= 10000:
                    divisors.add(candidate)
    if not divisors:
        return max(1, int(round(current)))
    return min(divisors, key=lambda v: (abs(v-current), v))
