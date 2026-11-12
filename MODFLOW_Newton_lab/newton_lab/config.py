"""Physical inputs, units and stress periods; no Streamlit dependencies.

All native models use metres and seconds. UI cell numbers are one-based;
all dataclasses and numerical code use zero-based (layer, row, column).
"""

import json
import math
from dataclasses import asdict, dataclass, field
from hashlib import sha256

import numpy as np

DAY = 86400.0
YEAR = 365.25 * DAY
ENGINES = {"mf2005": "MODFLOW-2005", "mfnwt": "MODFLOW-NWT", "mf6": "MODFLOW 6"}
SHORT_ENGINES = {"mf2005": "MF2005", "mfnwt": "MFNWT", "mf6": "MF6"}


@dataclass(frozen=True)
class Well:
    """One fully penetrating WEL stress; the scenario supplies its schedule."""

    name: str
    row: int
    col: int
    pumping_lps: float = 20.0
    injection_lps: float = 20.0


@dataclass(frozen=True)
class Observation:
    name: str = "OBS1"
    row: int = 15
    col: int = 16
    layer: int = 0


@dataclass(frozen=True)
class Period:
    label: str
    seconds: float
    steps: int
    multiplier: float
    steady: bool
    rate: float  # m³/s, positive injection


@dataclass(frozen=True)
class Scenario:
    nrow: int = 31
    ncol: int = 31
    cell_size: float = 100.0
    nlay: int = 1
    top: float = 0.0
    thickness: float = 20.0
    left: float = 18.0
    right: float = 16.0
    confined: bool = True
    conductivity: float = 1e-4
    vertical_ratio: float = 1.0
    ss: float = 1e-4
    sy: float = 0.2
    recharge: float = 150.0  # mm/year
    transient: bool = False
    combined: bool = False
    well_enabled: bool = True
    injection: bool = False
    pumping_lps: float = 20.0
    injection_lps: float = 20.0
    well_row: int = 15
    well_col: int = 15
    additional_wells: tuple[Well, ...] = ()
    pumping_days: float = 7.0
    injection_days: float = 7.0
    rest_days: float = 14.0
    steps: int = 48
    multiplier: float = 1.08
    observations: tuple[Observation, ...] = field(
        default_factory=lambda: (Observation(),)
    )
    heterogeneity: bool = False
    random_k: bool = False
    k_min: float = 1e-5
    k_max: float = 1e-3
    k_zones: int = 5
    k_seed: int = 42
    k_factor: float = 0.1
    zone_row0: int = 10
    zone_row1: int = 20
    zone_col0: int = 18
    zone_col1: int = 22
    inactive: bool = False
    inactive_row0: int = 3
    inactive_row1: int = 6
    inactive_col0: int = 3
    inactive_col1: int = 6

    @property
    def bottom(self):
        return self.top - self.thickness

    @property
    def wells(self):
        """Keep WELL as the first trace name for existing single-well exports."""
        return (
            Well(
                "WELL",
                self.well_row,
                self.well_col,
                self.pumping_lps,
                self.injection_lps,
            ),
            *self.additional_wells,
        )

    def well_rate(self, well, period):
        """Signed native rate for one well in a shared stress period (m³/s)."""
        if not self.well_enabled or period.label in ("baseline", "recovery"):
            return 0.0
        inject = period.label == "injection" or (period.steady and self.injection)
        return (well.injection_lps if inject else -well.pumping_lps) / 1000.0

    def total_well_rate(self, period):
        return sum(self.well_rate(well, period) for well in self.wells)

    @property
    def shape(self):
        return (self.nlay, self.nrow, self.ncol)

    @property
    def botm(self):
        return np.linspace(self.top, self.bottom, self.nlay + 1)[1:]

    @property
    def layer_tops(self):
        return np.r_[self.top, self.botm[:-1]]

    @property
    def recharge_ms(self):
        return self.recharge / 1000.0 / YEAR

    def active_mask(self):
        active = np.ones(self.shape, dtype=bool)
        if not self.confined:
            # Dry reservoir layers must not be CHD cells: legacy engines abort
            # when a constant-head cell is at/below its layer bottom. Exclude
            # those dry boundary cells consistently in all three engines.
            for col, head in ((0, self.left), (self.ncol - 1, self.right)):
                active[self.botm >= head - 1e-6, :, col] = False
        if self.inactive:
            active[
                :,
                self.inactive_row0 : self.inactive_row1 + 1,
                self.inactive_col0 : self.inactive_col1 + 1,
            ] = False
        return active

    def chd_mask(self):
        mask = np.zeros(self.shape, dtype=bool)
        mask[:, :, [0, -1]] = True
        return mask & self.active_mask()

    @property
    def heterogeneous(self):
        return self.heterogeneity or self.random_k

    def k_field(self):
        """A seeded log-uniform field on fixed physical zones, as in Solver Lab.

        The same realization is sampled at cell centres by every engine.
        Changing numerical grid resolution does not regenerate the zones.
        Layers receive independent values; zones span equal fractions of
        the first-to-last cell-centre distance in each horizontal direction.
        """
        if self.random_k:
            rng = np.random.default_rng(self.k_seed)
            zones = rng.uniform(
                np.log(self.k_min),
                np.log(self.k_max),
                (self.nlay, self.k_zones, self.k_zones),
            )
            cols = np.minimum(
                (np.arange(self.ncol) / (self.ncol - 1) * self.k_zones).astype(int),
                self.k_zones - 1,
            )
            rows = np.minimum(
                (np.arange(self.nrow) / (self.nrow - 1) * self.k_zones).astype(int),
                self.k_zones - 1,
            )
            return np.exp(zones[:, rows[:, None], cols[None, :]])
        conductivity = np.full(self.shape, self.conductivity)
        if self.heterogeneity:
            conductivity[
                :,
                self.zone_row0 : self.zone_row1 + 1,
                self.zone_col0 : self.zone_col1 + 1,
            ] *= self.k_factor
        return conductivity

    def starting_heads(self):
        profile = np.linspace(self.left, self.right, self.ncol)
        return np.broadcast_to(profile, self.shape).copy()

    def periods(self):
        """One native SS step, then optional pumping/injection and recovery.

        The SS bookkeeping second is removed from all displayed transient
        times and cumulative budgets. The native solver transfers its solved
        SS heads directly into the first transient time step.
        """
        rate = (
            self.injection_lps / 1000.0
            if self.injection
            else -self.pumping_lps / 1000.0
        )
        if not self.well_enabled:
            rate = 0.0
        if not self.transient:
            return [Period("steady", 1.0, 1, 1.0, True, rate)]
        periods = [Period("baseline", 1.0, 1, 1.0, True, 0.0)]
        if self.combined:
            periods.extend(
                [
                    Period(
                        "pumping",
                        self.pumping_days * DAY,
                        self.steps,
                        self.multiplier,
                        False,
                        -self.pumping_lps / 1000.0 if self.well_enabled else 0.0,
                    ),
                    Period(
                        "injection",
                        self.injection_days * DAY,
                        self.steps,
                        self.multiplier,
                        False,
                        self.injection_lps / 1000.0 if self.well_enabled else 0.0,
                    ),
                ]
            )
        else:
            duration = self.injection_days if self.injection else self.pumping_days
            periods.append(
                Period(
                    "injection" if self.injection else "pumping",
                    duration * DAY,
                    self.steps,
                    self.multiplier,
                    False,
                    rate,
                )
            )
        periods.append(
            Period(
                "recovery",
                self.rest_days * DAY,
                self.steps,
                self.multiplier,
                False,
                0.0,
            )
        )
        return periods

    def well_cells(self, well=None):
        """Fully penetrating well; fixed split by initial saturated thickness.

        This is a WEL stress, not a multi-node well. Individual layer flows
        are not redistributed dynamically when a layer dries.
        """
        well = self.wells[0] if well is None else well
        if self.confined:
            weights = np.full(self.nlay, self.thickness / self.nlay)
        else:
            initial = self.starting_heads()[:, well.row, well.col]
            weights = np.clip(initial - self.botm, 0, self.thickness / self.nlay)
        weights = weights / weights.sum()
        return [
            (k, well.row, well.col, float(w)) for k, w in enumerate(weights) if w > 0
        ]

    def validate(self):
        for name, value in asdict(self).items():
            if isinstance(value, (int, float)) and not math.isfinite(value):
                raise ValueError(f"{name}: enter a finite number.")
        if not (
            5 <= self.nrow <= 151 and 5 <= self.ncol <= 151 and 1 <= self.nlay <= 10
        ):
            raise ValueError("Grid: use 5–151 rows/columns and 1–10 layers.")
        for name in (
            "cell_size",
            "thickness",
            "conductivity",
            "vertical_ratio",
            "ss",
            "pumping_days",
            "injection_days",
            "rest_days",
            "k_factor",
        ):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name}: must be greater than zero.")
        if self.heterogeneity and self.random_k:
            raise ValueError("Choose a rectangular K zone or random K, not both.")
        if self.random_k:
            if not 0 < self.k_min <= self.k_max:
                raise ValueError("Random K requires 0 < minimum K <= maximum K.")
            if not isinstance(self.k_zones, int) or not 1 <= self.k_zones <= 100:
                raise ValueError("Random K: use 1–100 zones per direction.")
            if not isinstance(self.k_seed, int) or not 0 <= self.k_seed < 2**31:
                raise ValueError(
                    "Random K seed must be an integer from 0 to 2147483647."
                )
        if not 0 < self.sy <= 1:
            raise ValueError("Specific yield must be greater than 0 and at most 1.")
        if min(self.recharge, self.pumping_lps, self.injection_lps) < 0:
            raise ValueError("Recharge and well magnitudes must be nonnegative.")
        if min(self.left, self.right) <= self.bottom:
            raise ValueError("CHD heads must be above the aquifer bottom.")
        if not (1 <= self.well_col < self.ncol - 1 and 0 <= self.well_row < self.nrow):
            raise ValueError("Place the well inside the grid, away from CHD columns.")
        if not (1 <= self.steps <= 300 and 1 <= self.multiplier <= 1.3):
            raise ValueError("Time steps: use 1–300 steps and a multiplier of 1–1.3.")
        if self.transient:
            for period in self.periods()[1:]:
                first_step = (
                    period.seconds / period.steps
                    if period.multiplier == 1
                    else period.seconds
                    * (period.multiplier - 1)
                    / (period.multiplier**period.steps - 1)
                )
                if first_step < 0.001:
                    raise ValueError(
                        "The first time step is below 0.001 s. Reduce the time-step "
                        "multiplier or number of steps to preserve native time precision."
                    )
        if self.combined and not self.transient:
            raise ValueError("The combined scenario requires transient mode.")
        for enabled, prefix in (
            (self.heterogeneity, "zone"),
            (self.inactive, "inactive"),
        ):
            if enabled:
                a, b = getattr(self, prefix + "_row0"), getattr(self, prefix + "_row1")
                c, d = getattr(self, prefix + "_col0"), getattr(self, prefix + "_col1")
                if not (0 <= a <= b < self.nrow and 1 <= c <= d < self.ncol - 1):
                    raise ValueError(
                        "Zone limits must be ordered and exclude the CHD columns."
                    )
        active = self.active_mask()
        if len(self.additional_wells) > 2:
            raise ValueError("Use one, two or three wells.")
        locations, well_names = set(), set()
        for well in self.wells:
            if not (1 <= well.col < self.ncol - 1 and 0 <= well.row < self.nrow):
                raise ValueError(
                    f"{well.name}: place the well inside the grid, away from CHD columns."
                )
            if not active[:, well.row, well.col].all():
                raise ValueError(
                    f"{well.name}: the well cannot be in an inactive cell."
                )
            if (well.row, well.col) in locations:
                raise ValueError("Place each well in a different model cell.")
            if not well.name or well.name in well_names or well.name == "time_days":
                raise ValueError(
                    "Well names must be nonempty, unique and not time_days."
                )
            if any(
                not math.isfinite(q) or q < 0
                for q in (well.pumping_lps, well.injection_lps)
            ):
                raise ValueError(f"{well.name}: rates must be finite and nonnegative.")
            locations.add((well.row, well.col))
            well_names.add(well.name)
        names = set()
        if len(self.observations) > 12:
            raise ValueError("Use at most 12 observation points.")
        for obs in self.observations:
            if (
                not obs.name.strip()
                or obs.name in names
                or obs.name in well_names | {"time_days"}
            ):
                raise ValueError(
                    "Observation names must be nonempty and unique; well names and time_days are reserved."
                )
            names.add(obs.name)
            if not (
                0 <= obs.layer < self.nlay
                and 0 <= obs.row < self.nrow
                and 0 <= obs.col < self.ncol
            ):
                raise ValueError(f"{obs.name}: observation is outside the grid.")
            if not active[obs.layer, obs.row, obs.col]:
                raise ValueError(f"{obs.name}: observation is in an inactive cell.")
        records = sum(p.steps for p in self.periods())
        if np.prod(self.shape) * records > 8_000_000:
            raise ValueError(
                "Reduce cells, layers or saved time steps (limit: 8 million cell records)."
            )


@dataclass(frozen=True)
class Solver:
    engine: str = "mfnwt"
    head_close: float = 1e-5
    flow_close: float = 1e-6  # native m³/s; criteria differ between engines
    outer: int = 200
    inner: int = 200
    damping: float = 1.0
    rewet: bool | None = None
    wetdry: float = 0.01
    nwt_method: int = 2  # XMD default; GMRES remains available for comparison
    ibotav: int = 0
    newton: bool = True
    flow_reduction: float = 0.05
    timeout: float = 180.0

    def __post_init__(self):
        # MF2005 starts with rewetting off; retain the previous MF6 default.
        if self.rewet is None:
            object.__setattr__(self, "rewet", self.engine != "mf2005")

    def validate(self):
        if self.engine not in ENGINES:
            raise ValueError("Unknown numerical engine.")
        values = asdict(self)
        if any(
            not math.isfinite(v) for v in values.values() if isinstance(v, (float, int))
        ):
            raise ValueError("Solver values must be finite.")
        if (
            min(self.head_close, self.flow_close, self.outer, self.inner, self.timeout)
            <= 0
        ):
            raise ValueError("Solver tolerances and iteration limits must be positive.")
        if not (
            0 < self.damping <= 1 and 0 < self.flow_reduction <= 1 and self.wetdry > 0
        ):
            raise ValueError(
                "Invalid damping, wetting threshold or flow-reduction fraction."
            )
        if self.nwt_method not in (1, 2) or self.ibotav not in (0, 1):
            raise ValueError("Invalid NWT method or bottom-cell option.")


def fingerprint(scenario, solvers):
    payload = {"scenario": asdict(scenario), "solvers": [asdict(s) for s in solvers]}
    return sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def scenario_from_dict(values):
    values = dict(values)
    values["observations"] = tuple(Observation(**obs) for obs in values["observations"])
    values["additional_wells"] = tuple(
        Well(**well) for well in values.get("additional_wells", ())
    )
    return Scenario(**values)
