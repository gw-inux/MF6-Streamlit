"""Shared Solver Lab palette and Matplotlib defaults (presentation only)."""

from functools import wraps

import matplotlib.pyplot as plt
import numpy as np

BLUE = "#176DBB"
ANALYTICAL_GREEN = "#278247"
CHD_BLUE = "#2C78A5"
CHD_FILL = "#8AB9D6"
TEXT = "#24364B"
PREVIOUS_BLUE = "#7A91A6"
DRY_RED = "#E6A5AA"
WELL_RED = "#B33B54"
SECTION_COLOR = "#A23B7A"
COLORS = [BLUE, "#2087AA", "#7755AA", "#287B76", "#AA4E78", "#95682C"]
STYLE = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#8795A5",
    "axes.labelcolor": TEXT,
    "text.color": TEXT,
    "xtick.color": TEXT,
    "ytick.color": TEXT,
    "grid.color": "#8795A5",
    "font.size": 11,
    "legend.facecolor": "#F1F6FC",
    "legend.edgecolor": "#5489B5",
    "legend.labelcolor": BLUE,
}


def themed(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        with plt.rc_context(STYLE):
            return function(*args, **kwargs)

    return wrapped


def display_indices(count, maximum=100):
    """Decimate visible grid/dots only; always include both endpoints."""
    stride = max(1, int(np.ceil(count / maximum)))
    return np.unique(np.r_[np.arange(0, count, stride), count - 1]).astype(int)


ENGINE_COLORS = {"mf2005": "#7755AA", "mfnwt": BLUE, "mf6": "#20876E"}
ENGINE_MARKERS = {"mf2005": "o", "mfnwt": "s", "mf6": "^"}
