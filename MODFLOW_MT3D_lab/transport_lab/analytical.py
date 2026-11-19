"""First-type inlet on a semi-infinite line with zero initial interior concentration.

The point functions broadcast x and t. Spatial cell means are used for final scores.
The scaled erfc avoids overflow in the second Ogata–Banks term at high Péclet number.
"""
import numpy as np
from scipy.special import erfc, erfcx, ndtr

from .scenario import END_TIME, VELOCITY

SQRT_2PI = np.sqrt(2 * np.pi)
# Common physical support, interior even on the coarsest permitted grid (11 cells).
SCORE_EDGES = np.arange(50.0, 951.0, 10.0)


def _normal_density(z):
    return np.exp(-0.5 * z**2) / SQRT_2PI


def _step_terms(x, t, D):
    """Positive t, D. Return both terms already multiplied by one half."""
    denominator = 2 * np.sqrt(D * t)
    z = (x - VELOCITY * t) / denominator
    return 0.5 * erfc(z), 0.5 * np.exp(-z**2) * erfcx((x + VELOCITY * t) / denominator)


def step(x, t, D):
    x, t = np.broadcast_arrays(np.asarray(x, dtype=float), np.asarray(t, dtype=float))
    result = np.zeros_like(x)
    positive = t > 0
    if D == 0:
        result[positive] = (x[positive] <= VELOCITY * t[positive]).astype(float)
    else:
        first, second = _step_terms(x[positive], t[positive], D)
        result[positive] = first + second
    return result


def applied(x, t, case):
    """Point concentration for the actual inlet. At switch-off use the left limit."""
    t = np.asarray(t, dtype=float)
    response = step(x, t, case.D)
    if case.signal != "continuous":
        response -= step(x, t - case.duration, case.D)
    return case.height * np.where((np.asarray(x) == 0) & (t == 0), 1.0, np.maximum(response, 0.0))


def impulse(x, t, case):
    """Ideal temporal Dirac response at interior points, D>0."""
    if case.D <= 0:
        raise ValueError("At D=0 the ideal impulse is a distribution; use cell means.")
    x, t = np.broadcast_arrays(np.asarray(x, dtype=float), np.asarray(t, dtype=float))
    result = np.zeros_like(x)
    valid = (t > 0) & (x > 0)
    xv, tv = x[valid], t[valid]
    sigma = np.sqrt(2 * case.D * tv)
    result[valid] = case.impulse_area * xv / (tv * sigma) * _normal_density((xv - VELOCITY * tv) / sigma)
    return result


def _step_cell_means(left, right, t, D):
    """Exact integral of the unit step over each interval, divided by its width."""
    if t <= 0:
        return np.zeros_like(left)
    if D == 0:
        return np.clip((VELOCITY * t - left) / (right - left), 0.0, 1.0)

    def primitive(x):
        sigma = np.sqrt(2 * D * t)
        z = (x - VELOCITY * t) / sigma
        first, second = _step_terms(x, t, D)
        return (x - VELOCITY * t) * first - sigma * _normal_density(z) + D / VELOCITY * (second + ndtr(z))

    return np.clip((primitive(right) - primitive(left)) / (right - left), 0.0, 1.0)


def mean_reference(case, edges, t, *, ideal=False):
    """Analytical concentration averaged over each interval between successive edges."""
    left, right = edges[:-1], edges[1:]
    width = right - left
    if not ideal or case.signal != "dirac":
        values = _step_cell_means(left, right, t, case.D)
        if case.signal != "continuous":
            values -= _step_cell_means(left, right, t - case.duration, case.D)
        return case.height * np.maximum(values, 0.0)
    if t <= 0:
        return np.zeros_like(left)

    front = VELOCITY * t
    if case.D == 0:
        # The symmetric limit gives each neighbour half the delta at a shared face.
        on_face = np.isclose(front, left, atol=1e-9, rtol=0) | np.isclose(front, right, atol=1e-9, rtol=0)
        weight = np.where(on_face, 0.5, ((left < front) & (front < right)).astype(float))
        return case.impulse_area * VELOCITY * weight / width
    sigma = np.sqrt(2 * case.D * t)
    a, b = (left - front) / sigma, (right - front) / sigma
    integral = VELOCITY * (ndtr(b) - ndtr(a)) + sigma / t * (_normal_density(a) - _normal_density(b))
    return case.impulse_area * np.maximum(integral, 0.0) / width


def numerical_means(case, concentration, edges=SCORE_EDGES):
    """Conservative remap of native piecewise-constant cell values to common bins."""
    native_faces = (np.arange(case.ncol + 1) - 0.5) * case.dx
    cumulative = np.r_[0.0, np.cumsum(np.asarray(concentration, dtype=float) * case.dx)]
    return np.diff(np.interp(edges, native_faces, cumulative)) / np.diff(edges)


def final_errors(case, concentration):
    """Like-for-like RMSE, MAE and optional ideal-impulse RMSE in C/Cref."""
    numerical = numerical_means(case, concentration)
    residual = numerical - mean_reference(case, SCORE_EDGES, END_TIME)
    rmse = float(np.sqrt(np.mean(residual**2)))
    mae = float(np.mean(np.abs(residual)))
    ideal_rmse = None
    if case.signal == "dirac":
        delta = numerical - mean_reference(case, SCORE_EDGES, END_TIME, ideal=True)
        ideal_rmse = float(np.sqrt(np.mean(delta**2)))
    return rmse, mae, ideal_rmse
