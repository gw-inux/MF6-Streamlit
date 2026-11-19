"""Benchmark geometry, input signals and numerical choices, independent of the UI."""
from dataclasses import dataclass
from math import isfinite

import numpy as np

LENGTH = 1000.0       # distance between the two constant-head cell centres [m]
END_TIME = 2000.0     # days
SECONDS_PER_DAY = 86400.0
K_MS = 1.0e-4        # horizontal hydraulic conductivity [m/s]
K = K_MS * SECONDS_PER_DAY  # MODFLOW uses days for this benchmark [m/d]
POROSITY = 0.25
VELOCITY = 0.24       # pore velocity [m/d]
DARCY_FLUX = POROSITY * VELOCITY
LEFT_HEAD = DARCY_FLUX * LENGTH / K
MAX_VARIANTS = 10

# MT3DMS advection schemes: (MIXELM, NADVFD). NADVFD applies only to MIXELM=0.
METHODS = {
    "upwind": (0, 1),
    "central": (0, 2),
    "tvd": (-1, 1),
    "moc": (1, 1),
    "mmoc": (2, 1),
    "hmoc": (3, 1),
}
SIGNALS = ("continuous", "block", "dirac")
DEFAULT_SIGNAL = "block"


@dataclass(frozen=True)
class Scenario:
    ncol: int = 21
    method: str = "upwind"
    signal: str = DEFAULT_SIGNAL
    dispersivity: float = 0.0    # m
    diffusion: float = 0.0       # effective molecular diffusion [m²/d]
    courant: float = 0.5
    amplitude: float = 1.0       # C/Cref, continuous and block inputs
    block_days: float = 400.0
    impulse_area: float = 50.0   # integral of C/Cref over time [d]
    impulse_days: float = 50.0   # width of the box used by MT3DMS [d]

    def __post_init__(self):
        if not isinstance(self.ncol, (int, np.integer)) or not 11 <= self.ncol <= 501:
            raise ValueError("ncol must be an integer from 11 to 501.")
        if self.method not in METHODS or self.signal not in SIGNALS:
            raise ValueError("Unknown transport method or inlet signal.")
        for value in (self.courant, self.amplitude, self.impulse_area):
            if not isfinite(value) or value <= 0:
                raise ValueError("Courant number, amplitude and impulse area must be positive.")
        if self.courant < 0.1 or self.courant > 1.0:
            raise ValueError("Use a Courant limit from 0.1 to 1.")
        for width in (self.block_days, self.impulse_days):
            if not isfinite(width) or not 1 <= width < END_TIME:
                raise ValueError("The input duration must be in [1, 2000) days.")
        if any(not isfinite(x) or x < 0 for x in (self.dispersivity, self.diffusion)):
            raise ValueError("Dispersion coefficients must be finite and nonnegative.")

    @property
    def dx(self):
        return LENGTH / (self.ncol - 1)

    @property
    def x(self):
        return np.linspace(0.0, LENGTH, self.ncol)

    @property
    def D(self):
        return self.dispersivity * VELOCITY + self.diffusion

    @property
    def height(self):
        return self.impulse_area / self.impulse_days if self.signal == "dirac" else self.amplitude

    @property
    def duration(self):
        return {"continuous": END_TIME, "block": self.block_days, "dirac": self.impulse_days}[self.signal]

    @property
    def periods(self):
        if self.signal == "continuous":
            return (END_TIME,)
        return (self.duration, END_TIME - self.duration)

    @property
    def step_limits(self):
        base = self.courant * self.dx / VELOCITY
        if self.signal == "continuous":
            return (base,)
        # Resolve the imposed box in time, even on the coarsest grid.
        return (min(base, self.duration / 8), base)

    @property
    def applied_reference_key(self):
        # Grids and numerical methods can share the same analytical curve.
        return (self.D, self.height, self.duration)
