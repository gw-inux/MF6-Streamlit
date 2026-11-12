"""Scientific regression tests use real executables, never surrogate heads."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   baseline: line 24
#   CHOICES: line 29
#   executable: line 33
#   test_exact_discrete_equation: line 41
#   test_heads_counts_and_budgets: line 55
#   test_native_presets: line 97
#   test_nwt_specified_matches_native: line 105
#   test_nonconvergence_is_not_success: line 117
#   test_api_real_outer_heads: line 123
#   test_nwt_noflow_complex_nonexact_start: line 141
#   test_invalid_physical_inputs: line 149
#   test_missing_explicit_executable_does_not_fallback: line 154
# END CODE CONTENTS

import numpy as np
import pytest
from MODFLOW_Solver_lab.core import (Scenario, Solver, find_executable, find_library,
                  head_metrics, run_once, record_mf6, NWT_PRESETS)

def baseline(**kwargs):
    """Retain v1.2 physical benchmark inputs while testing seconds internally."""
    return Scenario(**(dict(k_ms=1e-3, recharge_mmy=200.) | kwargs))


CHOICES = [("mf2005", "PCG"), ("mf2005", "SIP"), ("mfnwt", "GMRES"),
           ("mfnwt", "XMD"), ("mf6", "CG"), ("mf6", "BICGSTAB")]


def executable(engine):
    path = find_executable(engine)
    if not path:
        pytest.skip(f"{engine} executable not installed")
    return path


@pytest.mark.parametrize("n", [3, 11, 101, 1001])
def test_exact_discrete_equation(n):
    s = baseline(n=n)
    r = head_metrics(s, s.analytic())
    assert r["max_residual_m3s"] < 1e-9
    assert r["boundary_error_m"] == 0
    assert abs(r["balance_m3s"]) < 1e-9
    assert s.dx * (s.n - 1) == s.length


@pytest.mark.parametrize("engine,method", CHOICES)
@pytest.mark.parametrize("scenario", [baseline(), baseline(n=3), baseline(n=101), baseline(n=1001),
    baseline(n=10001), baseline(recharge_mmy=0), baseline(recharge_mmy=0, left=18., right=18.),
    baseline(k_ms=1e-5, thickness=45., recharge_mmy=400., left=23., right=15.),
    baseline(width=47., length=2573., initial="Specified uniform head", initial_head=60.)])
def test_heads_counts_and_budgets(engine, method, scenario, tmp_path):
    cfg = Solver(engine, method)
    # Preserve the previous regression benchmark's tolerances independently
    # of the app's revised suggested starting values.
    if engine == "mf2005":
        cfg.overrides = dict(hclose=1e-5)
        if method == "PCG":
            cfg.overrides["rclose"] = 1e-5/86400.
    elif engine == "mfnwt":
        cfg.overrides = dict(headtol=1e-5, fluxtol=1e-5/86400.)
    if engine == "mf6":
        cfg.overrides = dict(outer_dvclose=1e-5, inner_dvclose=1e-5, rcloserecord=1e-5/86400.)
    r = run_once(scenario, cfg, tmp_path, executable(engine))
    # Verify faithful failure handling for degenerate native NWT edge cases.
    # A different executable may fix them, in which case check the solution.
    edge_case = engine == "mfnwt" and (scenario.n == 3 or
                    (scenario.recharge_mmy == 0 and scenario.left == scenario.right))
    if edge_case and not r["success"]:
        assert r["native_fpe"]
        assert r["heads"] is None
        assert r["status"] == "Native floating-point failure"
        return
    assert r["success"], r["stdout"][-2000:] + r["listing"][-2000:]
    # Relative scale allows documented legacy input rounding, but is far
    # tighter than the millimetre threshold suitable for the default exercise.
    tolerance = max(1e-5, np.max(np.abs(scenario.analytic())) * 2e-7)
    assert r["metrics"]["max_error_m"] < tolerance
    assert r["metrics"]["boundary_error_m"] < 2e-6
    assert r["budget_percent"] is not None
    assert abs(r["budget_percent"]) < .01
    assert r["history"]
    if method == "SIP":
        assert r["sip_iterations"] > 0
        assert len(r["history"]) == r["sip_iterations"]
        assert r["inner_iterations"] is None
    else:
        assert r["outer_iterations"] > 0
        assert r["inner_iterations"] >= 0


@pytest.mark.parametrize("preset", ["SIMPLE", "MODERATE", "COMPLEX"])
@pytest.mark.parametrize("engine,method", CHOICES[2:])
def test_native_presets(engine, method, preset, tmp_path):
    r = run_once(baseline(), Solver(engine, method, preset), tmp_path, executable(engine))
    assert r["success"]
    assert r["metrics"]["max_error_m"] < .01


@pytest.mark.parametrize("preset", list(NWT_PRESETS))
@pytest.mark.parametrize("method", ["GMRES", "XMD"])
def test_nwt_specified_matches_native(preset, method, tmp_path):
    native = run_once(baseline(), Solver("mfnwt", method, preset), tmp_path/"native", executable("mfnwt"))
    custom = run_once(baseline(), Solver("mfnwt", method, preset, nwt_specified=True), tmp_path/"custom", executable("mfnwt"))
    assert native["success"] and custom["success"]
    np.testing.assert_allclose(native["heads"], custom["heads"], atol=1e-7, rtol=0)
    assert native["outer_iterations"] == custom["outer_iterations"]
    assert native["inner_iterations"] == custom["inner_iterations"]


@pytest.mark.parametrize("cfg", [Solver("mf2005", "PCG", overrides=dict(mxiter=1, iter1=1, npcond=2)),
    Solver("mf2005", "SIP", overrides=dict(mxiter=1)), Solver("mfnwt", "GMRES", overrides=dict(maxiterout=1)),
    Solver("mf6", "CG", overrides=dict(outer_maximum=1, inner_maximum=1, inner_dvclose=1e-12, rcloserecord=1e-12/86400.))])
def test_nonconvergence_is_not_success(cfg, tmp_path):
    r = run_once(baseline(n=101), cfg, tmp_path, executable(cfg.engine))
    assert not r["success"]
    assert "Converged" != r["status"]


def test_api_real_outer_heads(tmp_path):
    lib = find_library()
    if not lib:
        pytest.skip("libmf6 not installed")
    pytest.importorskip("modflowapi")
    s = baseline(n=101)
    cfg = Solver("mf6", "CG", overrides=dict(outer_dvclose=1e-7, inner_dvclose=1e-7, rcloserecord=1e-10,
        under_relaxation="SIMPLE", under_relaxation_gamma=.5, outer_maximum=100))
    r = run_once(s, cfg, tmp_path/"exe", executable("mf6"))
    data = record_mf6(s, cfg, tmp_path/"api", executable("mf6"), lib)
    assert data["converged"].item()
    assert len(data["heads"]) > 3
    np.testing.assert_allclose(data["heads"][0], s.starting_heads(), atol=1e-8)
    np.testing.assert_allclose(data["heads"][-1], r["heads"], atol=1e-8)
    assert len(data["heads"]) - 1 == r["outer_iterations"]


@pytest.mark.parametrize("method", ["GMRES", "XMD"])
def test_nwt_noflow_complex_nonexact_start(method, tmp_path):
    s = baseline(left=18., right=18., recharge_mmy=0., initial="Specified uniform head", initial_head=17.3)
    r = run_once(s, Solver("mfnwt", method, "COMPLEX"), tmp_path, executable("mfnwt"))
    assert r["success"]
    assert r["metrics"]["max_error_m"] < 1e-5


@pytest.mark.parametrize("kwargs", [dict(n=2), dict(n=10002), dict(k_ms=0), dict(left=-1), dict(recharge_mmy=-1), dict(width=0), dict(length=float('nan'))])
def test_invalid_physical_inputs(kwargs):
    with pytest.raises(ValueError):
        baseline(**kwargs).validate()


def test_missing_explicit_executable_does_not_fallback():
    assert find_executable("mf6", "/nonexistent/incorrect_mf6") is None
