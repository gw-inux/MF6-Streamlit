"""Analytical conservative-transport reference for the 2D / 3D teaching lab.

Units are metres, days, grams and dissolved concentration in g/m3 water.
The equation is n*dC/dt = n*(Dx*Cxx + Dy*Cyy + Dz*Czz - v*Cx) + s.
Flow is uniform in +x; porosity and dispersion are homogeneous and constant.
The x domain is infinite. The y and z faces are reflecting (zero dispersive
flux), matching the idealized numerical model's closed lateral/top/base faces.

A Dirac input is instantaneous IN TIME, uniformly distributed over the actual
source-cell box. Finite pulses and continuous sources are mass-loading rates,
not imposed concentration boundaries. Both the source and receiver volumes are
integrated, avoiding a point-source versus finite-cell comparison. The attached
point-source apps motivated this benchmark; their continuous concentration-
boundary approximations do not describe the mass-loading experiment here.
"""
from __future__ import annotations

import math
from typing import Sequence

import numpy as np
from scipy.integrate import quad, quad_vec
from scipy.special import ndtr, log_ndtr

SQRT_2PI = math.sqrt(2.0 * math.pi)


def _intervals(edges: Sequence[float]) -> tuple[np.ndarray, np.ndarray]:
    edges = np.asarray(edges, dtype=float)
    if edges.ndim != 1 or len(edges) < 2 or not np.isfinite(edges).all():
        raise ValueError("Grid edges must be a finite 1D array with at least two entries.")
    delta = np.diff(edges)
    if not (np.all(delta > 0) or np.all(delta < 0)):
        raise ValueError("Grid edges must be strictly monotone.")
    return np.minimum(edges[:-1], edges[1:]), np.maximum(edges[:-1], edges[1:])


def _box_density(a: np.ndarray, b: np.ndarray, s0: float, s1: float,
                 shift: float, sigma: float) -> np.ndarray:
    """Cell-average probability density from a uniform initial source interval."""
    q = [b - s0 - shift, a - s0 - shift, b - s1 - shift, a - s1 - shift]
    if sigma == 0.0:
        overlap = np.maximum(0.0, np.minimum(b, s1 + shift) - np.maximum(a, s0 + shift))
        return overlap / ((s1 - s0) * (b - a))
    # Separate the exact zero-dispersion overlap from the small smooth correction.
    # This also avoids cancellation of large positive linear terms in far tails.
    overlap = np.maximum(0.0, np.minimum(b, s1 + shift) - np.maximum(a, s0 + shift))
    correction = np.zeros_like(a)
    for sign, u in zip((1, -1, -1, 1), q):
        aa = np.abs(u)
        correction += sign * (sigma * np.exp(-0.5 * (aa / sigma) ** 2) / SQRT_2PI
                              - aa * ndtr(-aa / sigma))
    answer = (overlap + correction) / ((s1 - s0) * (b - a))
    return np.maximum(answer, 0.0)  # Remove roundoff below zero, never rescale mass.


def _reflecting_density(a: np.ndarray, b: np.ndarray, s0: float, s1: float,
                        domain: tuple[float, float], sigma: float) -> np.ndarray:
    """Neumann heat kernel averaged over source/receiver intervals.

    Image sources are used for narrow plumes and the convergent cosine series
    for broad plumes. Both preserve the finite domain's mass and uniform limit.
    """
    lo, hi = domain
    length = hi - lo
    if math.isclose(s0, lo, rel_tol=0, abs_tol=1e-12 * length) and math.isclose(
        s1, hi, rel_tol=0, abs_tol=1e-12 * length
    ):
        return np.full_like(a, 1.0 / length)
    if sigma == 0:
        return _box_density(a, b, s0, s1, 0.0, 0.0)
    if sigma >= 0.35 * length:
        # exp(-D*t*k^2) = exp(-0.5*sigma^2*k^2).
        count = max(1, int(math.ceil(math.sqrt(-2 * math.log(1e-14)) * length / (math.pi * sigma))))
        wavenumber = np.arange(1, count + 1) * math.pi / length
        smean = (np.sin(wavenumber * (s1 - lo)) - np.sin(wavenumber * (s0 - lo))) / (wavenumber * (s1 - s0))
        rmean = (np.sin(wavenumber[:, None] * (b - lo)) - np.sin(wavenumber[:, None] * (a - lo))) / (wavenumber[:, None] * (b - a))
        density = (1 + 2 * np.sum((np.exp(-0.5 * (sigma * wavenumber) ** 2) * smean)[:, None] * rmean, axis=0)) / length
        return np.maximum(density, 0.0)
    density = np.zeros_like(a)
    count = int(math.ceil(8 * sigma / (2 * length))) + 1
    for image in range(-count, count + 1):
        offset = 2 * image * length
        density += _box_density(a, b, s0 + offset, s1 + offset, 0, sigma)
        density += _box_density(a, b, 2 * lo - s1 + offset, 2 * lo - s0 + offset, 0, sigma)
    return density


def _age_integral_no_dispersion(a: np.ndarray, b: np.ndarray, s0: float,
                               s1: float, velocity: float, age_lo: float,
                               age_hi: float) -> np.ndarray:
    """Exact time integral of the advected box, including sharp fronts."""
    if velocity == 0:
        return (age_hi - age_lo) * _box_density(a, b, s0, s1, 0, 0)
    answer = np.zeros_like(a)
    # Integrate the overlap's four positive-part terms with a quadratic primitive.
    for sign, q in zip((1, -1, -1, 1), (b - s0, a - s0, b - s1, a - s1)):
        answer += sign * (np.maximum(q - velocity * age_lo, 0) ** 2
                          - np.maximum(q - velocity * age_hi, 0) ** 2) / (2 * velocity)
    return np.maximum(answer / ((s1 - s0) * (b - a)), 0.0)


def injected_mass(time: float, source_kind: str, source_mass: float = 0.0,
                  mass_rate: float = 0.0, pulse_duration: float = 0.0) -> float:
    """Cumulative mass (g), including initial mass at t=0 for a Dirac slug."""
    if time < 0:
        return 0.0
    source_kind = source_kind.lower()
    if source_kind == "dirac":
        return float(source_mass)
    if source_kind == "pulse":
        return float(mass_rate * min(time, pulse_duration))
    if source_kind == "continuous":
        return float(mass_rate * time)
    raise ValueError("source_kind must be dirac, pulse, or continuous.")


def reference_concentration(
    x_edges: Sequence[float], y_edges: Sequence[float], z_edges: Sequence[float], *,
    time: float, velocity: float, dispersion: Sequence[float], porosity: float,
    source_bounds: Sequence[Sequence[float]], source_kind: str = "dirac",
    source_mass: float = 1.0, mass_rate: float = 1.0, pulse_duration: float = 1.0,
    integration_rtol: float = 2e-6,
) -> np.ndarray:
    """Return reference cell-average C with shape (nz, ny, nx).

    Edge arrays may be ascending or descending; output order follows each array.
    ``source_bounds`` is ((xmin,xmax), (ymin,ymax), (zmin,zmax)); it must be the
    actual finite source box, including grid snapping. ``velocity`` is pore
    velocity in m/day; ``dispersion`` contains Dx,Dy,Dz in m2/day (not alpha).
    Porosity is dissolved-water volume / bulk volume. The initial/source mass
    is uniformly distributed in this source box. A single layer, or a source
    across all z, reduces to vertically uniform 2D transport without a special
    thickness correction. Positive source time starts at zero.

    Only call for homogeneous steady confined flow. Infinite x does not match
    the finite numerical boundary after plume interaction: inspect
    :func:`boundary_diagnostics` before reporting an analytical error metric.
    """
    intervals = [_intervals(e) for e in (x_edges, y_edges, z_edges)]
    bounds = np.asarray(source_bounds, dtype=float)
    disp = np.asarray(dispersion, dtype=float)
    kind = source_kind.lower()
    if bounds.shape != (3, 2) or not np.isfinite(bounds).all() or np.any(bounds[:, 1] <= bounds[:, 0]):
        raise ValueError("source_bounds must contain three finite, increasing intervals.")
    if disp.shape != (3,) or not np.isfinite(disp).all() or np.any(disp < 0):
        raise ValueError("Dispersion must contain three finite nonnegative coefficients.")
    if not (np.isfinite(time) and time >= 0 and np.isfinite(velocity) and velocity >= 0):
        raise ValueError("Time and +x velocity must be finite and nonnegative.")
    if not np.isfinite(porosity) or not 0 < porosity <= 1:
        raise ValueError("Porosity must be in (0, 1].")
    if not np.isfinite([source_mass, mass_rate, pulse_duration]).all() or min(source_mass, mass_rate, pulse_duration) < 0:
        raise ValueError("Source mass, rate and duration must be finite and nonnegative.")
    if kind not in ("dirac", "pulse", "continuous"):
        raise ValueError("source_kind must be dirac, pulse, or continuous.")
    domains = [(float(a.min()), float(b.max())) for a, b in intervals]
    for dim in range(3):
        if bounds[dim, 0] < domains[dim][0] - 1e-10 or bounds[dim, 1] > domains[dim][1] + 1e-10:
            raise ValueError("Source box must be inside the modeled domain.")
    shape = tuple(len(ab[0]) for ab in intervals[::-1])

    def density(age: float) -> np.ndarray:
        sigmas = np.sqrt(2 * disp * max(age, 0.0))
        px = _box_density(*intervals[0], *bounds[0], velocity * age, sigmas[0])
        py = _reflecting_density(*intervals[1], *bounds[1], domains[1], sigmas[1])
        pz = _reflecting_density(*intervals[2], *bounds[2], domains[2], sigmas[2])
        return pz[:, None, None] * py[None, :, None] * px[None, None, :] / porosity

    if kind == "dirac":
        return source_mass * density(time)
    age_lo = max(0.0, time - pulse_duration) if kind == "pulse" else 0.0
    age_hi = time
    if age_hi <= age_lo or mass_rate == 0:
        return np.zeros(shape, dtype=float)
    if np.all(disp == 0):
        px = _age_integral_no_dispersion(*intervals[0], *bounds[0], velocity, age_lo, age_hi)
        py = _reflecting_density(*intervals[1], *bounds[1], domains[1], 0)
        pz = _reflecting_density(*intervals[2], *bounds[2], domains[2], 0)
        return mass_rate / porosity * pz[:, None, None] * py[None, :, None] * px[None, None, :]
    # age=u^2 removes the sqrt(age) endpoint behaviour of a finite source box.
    # Adaptive vector integration controls the entire plume, not just its peak.
    answer, error, info = quad_vec(
        lambda u: 2 * u * density(u * u), math.sqrt(age_lo), math.sqrt(age_hi),
        epsrel=integration_rtol, epsabs=1e-12, norm="max", limit=300,
        cache_size=16_000_000, full_output=True,
    )
    if not info.success:
        raise RuntimeError(f"Analytical time integration did not converge: {info.message}")
    return mass_rate * np.maximum(answer, 0.0)


def _crossing_fraction(time: float, velocity: float, dx: float,
                       source_x: tuple[float, float], boundary_positions: tuple[float, float],
                       source_kind: str, pulse_duration: float) -> float:
    """Conservative union bound for mass ever crossing either finite-x face.

    Each individual face uses the exact Brownian first-passage distribution for
    drift v and diffusivity Dx, averaged over the finite source and release time.
    Adding both crossing fractions can double-count paths hitting both faces;
    that makes this screen conservative, never an assertion of exact loss mass.
    """
    s0, s1 = source_x
    left, right = boundary_positions
    width = s1 - s0

    def for_age(age):
        if age <= 0:
            return 0.0
        if dx == 0:
            return float(np.clip((s1 - max(s0, right - velocity * age)) / width, 0, 1))
        sigma = math.sqrt(2 * dx * age)

        def at_source(s):
            dleft, dright = s - left, right - s
            if dleft <= 0 or dright <= 0:
                return 1.0
            left_first = ndtr((-dleft - velocity * age) / sigma)
            left_image = math.exp(min(0.0, -velocity * dleft / dx + log_ndtr((-dleft + velocity * age) / sigma)))
            right_first = ndtr((-dright + velocity * age) / sigma)
            right_image = math.exp(min(0.0, velocity * dright / dx + log_ndtr((-dright - velocity * age) / sigma)))
            return min(1.0, float(left_first + left_image + right_first + right_image))

        # Breakpoint anticipates a near-sharp advective front for very small Dx.
        front = right - velocity * age
        points = [front] if s0 < front < s1 else None
        return quad(at_source, s0, s1, epsabs=1e-8 * width, epsrel=1e-7,
                    points=points, limit=100)[0] / width

    if source_kind == "dirac":
        return for_age(time)
    age_lo = max(0.0, time - pulse_duration) if source_kind == "pulse" else 0.0
    if time <= age_lo:
        return 0.0
    # This quantity is normalized by actual cumulative injected mass; the input
    # rate cancels. It therefore treats all release ages, including early losses.
    umax, umin = math.sqrt(time), math.sqrt(age_lo)
    points = []
    if velocity > 0:
        for source_edge in (s0, s1):
            age = (right - source_edge) / velocity
            if age_lo < age < time:
                points.append(math.sqrt(age))
    return float(quad(lambda u: 2 * u * for_age(u * u), umin, umax,
                      epsabs=1e-7 * (time-age_lo), epsrel=1e-6,
                      points=points or None, limit=100)[0] / (time - age_lo))


def boundary_diagnostics(
    concentration: np.ndarray, x_edges: Sequence[float], y_edges: Sequence[float],
    z_edges: Sequence[float], *, porosity: float, time: float,
    source_kind: str, source_mass: float = 0.0, mass_rate: float = 0.0,
    pulse_duration: float = 0.0, retention_threshold: float = 0.995,
    velocity: float | None = None, dispersion: Sequence[float] | None = None,
    source_bounds: Sequence[Sequence[float]] | None = None,
    boundary_positions: tuple[float, float] | None = None,
) -> dict:
    """Screen finite-x boundary limitations of a computed reference field.

    Pass velocity, dispersion, source_bounds for a cumulative first-passage
    screen, detecting upstream leakage even if it later advects back into the
    domain. ``boundary_positions`` defaults to outer edges; for specified-head
    cells pass their x cell centers instead. The crossing fraction is a
    conservative union upper bound, not an exact finite-domain mass deficit.
    Scores require both retained mass and the cumulative screen to pass.
    Without those three optional inputs only present-time retention is checked.
    """
    dx, dy, dz = (np.abs(np.diff(np.asarray(e, float))) for e in (x_edges, y_edges, z_edges))
    c = np.asarray(concentration, float)
    if c.shape != (len(dz), len(dy), len(dx)):
        raise ValueError("Concentration dimensions do not match the grid.")
    if not 0 < retention_threshold <= 1:
        raise ValueError("retention_threshold must be in (0,1].")
    mass = float(np.sum(c * dz[:, None, None] * dy[None, :, None] * dx[None, None, :]) * porosity)
    kind = source_kind.lower()
    total = injected_mass(time, kind, source_mass, mass_rate, pulse_duration)
    fraction = mass / total if total > 0 else 1.0
    crossing = None
    supplied = (velocity is not None, dispersion is not None, source_bounds is not None)
    if any(supplied) and not all(supplied):
        raise ValueError("Cumulative boundary screen requires velocity, dispersion and source_bounds together.")
    if all(supplied):
        xpos = tuple(sorted(boundary_positions if boundary_positions is not None
                            else (min(x_edges), max(x_edges))))
        source_x = tuple(float(v) for v in source_bounds[0])
        if xpos[0] >= source_x[0] or xpos[1] <= source_x[1]:
            crossing = 1.0
        elif total == 0:
            crossing = 0.0
        else:
            crossing = _crossing_fraction(time, velocity, float(dispersion[0]), source_x,
                                          xpos, kind, pulse_duration)
    eligible = bool(fraction >= retention_threshold and fraction <= 1.0001
                    and (crossing is None or crossing <= 1 - retention_threshold))
    tolerance_percent = 100 * (1 - retention_threshold)
    return {
        "reference_mass_g": mass,
        "injected_mass_g": total,
        "retained_fraction": fraction,
        "outside_x_fraction": max(0.0, 1.0 - fraction),
        "cumulative_x_crossing_upper_bound": crossing,
        "accuracy_eligible": eligible,
        "retention_threshold": retention_threshold,
        "message": ("Infinite-x analytical reference: boundary proximity screen passed."
                    if eligible else f"Analytical accuracy disabled: x-boundary interaction exceeds the {tolerance_percent:.2g}% screen."),
    }


def point_source_concentration(x, y, z, *, time: float, velocity: float,
                               dispersion: Sequence[float], porosity: float,
                               mass: float = 1.0, source=(0.0, 0.0, 0.0),
                               thickness: float | None = None):
    """Unbounded Green solution for teaching (not finite-cell comparison).

    With ``thickness`` return a vertically uniform 2D concentration; otherwise
    return the 3D point-source solution. t>0 and active D>0 are required because
    the exact distribution is singular when diffusion/dispersion vanishes.
    """
    dimensions = 2 if thickness is not None else 3
    d = np.asarray(dispersion, float)[:dimensions]
    if time <= 0 or len(d) != dimensions or np.any(d <= 0) or porosity <= 0:
        raise ValueError("Point-source Green function requires t>0, n>0 and positive active dispersion.")
    if thickness is not None and thickness <= 0:
        raise ValueError("Thickness must be positive.")
    xyz = np.broadcast_arrays(np.asarray(x, float), np.asarray(y, float), np.asarray(z, float))
    delta = [xyz[j] - source[j] - (velocity * time if j == 0 else 0) for j in range(dimensions)]
    exponent = sum(dd * dd / (4 * coefficient * time) for dd, coefficient in zip(delta, d))
    denominator = porosity * (4 * math.pi * time) ** (dimensions / 2) * math.sqrt(float(np.prod(d)))
    if thickness is not None:
        denominator *= thickness
    return mass / denominator * np.exp(-exponent)
