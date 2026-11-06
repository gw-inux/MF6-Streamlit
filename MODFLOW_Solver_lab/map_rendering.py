"""Bounded, session-owned PNG cache for the computed horizontal head map.

A browser receives a static raster, not hundreds of thousands of cell artists.
Unchanged runs reuse the same image; each session keeps only the current source
in its normal and stale colours. The full head array is hashed, never sampled.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   HEAD_MAP_DPI: line 24
#   head_map_image: line 27
# END CODE CONTENTS

from dataclasses import asdict
from hashlib import sha256
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np

from .core import fingerprint
from .plots import computed_head_map

HEAD_MAP_DPI = 160


def head_map_image(cache, scenario, heads, stale=False):
    """Return PNG bytes, invalidating on any geometry/head change."""
    values = np.asarray(heads, dtype=np.float64)
    source = (fingerprint(asdict(scenario)), sha256(values.tobytes()).hexdigest())
    if cache.get("source") != source:
        cache.clear()
        cache.update(source=source, images={})
    images = cache["images"]
    if stale not in images:
        fig = computed_head_map(scenario, values, surface=True, stale=stale)
        try:
            buffer = BytesIO()
            fig.savefig(buffer, format="png", dpi=HEAD_MAP_DPI, bbox_inches="tight", facecolor="white")
            images[stale] = buffer.getvalue()
        finally:
            plt.close(fig)
    return images[stale]
