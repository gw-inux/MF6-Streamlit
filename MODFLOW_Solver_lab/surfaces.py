"""Display-only groundwater surfaces; native heads and model inputs stay intact.

A surface head is the head in the uppermost wet, active cell of each vertical
column. Dry overlying cells therefore display the head found below them. A
fully dry column has no defined saturated head and remains NaN, never zero.
For confined models this is a potentiometric surface, not a free water table.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   groundwater_surface: line 17
# END CODE CONTENTS

import numpy as np


def groundwater_surface(scenario, heads):
    """Return surface heads and their one-based source layers (0 if all dry).

    The scenario's existing mask excludes inactive cells, native dry/no-flow
    sentinels, nonfinite values and convertible heads at/below cell bottoms.
    Selection is from the top down, not by maximum head; deeper heads can be
    higher where vertical hydraulic gradients exist.
    """
    clean = scenario.head_array(heads)
    wet = np.isfinite(clean)
    has_water = wet.any(axis=0)
    upper = wet.argmax(axis=0)
    surface = np.take_along_axis(clean, upper[None, ...], axis=0)[0].copy()
    surface[~has_water] = np.nan
    source_layer = np.where(has_water, upper + 1, 0)
    return surface, source_layer
