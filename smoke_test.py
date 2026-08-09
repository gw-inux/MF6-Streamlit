"""Command-line smoke test for the MODFLOW + MODPATH deployment environment.

Run with:
    python smoke_test.py

The test runs the complete workflow twice: first without pumping and then with
pumping.  It checks MODFLOW results, the expected drawdown response, both native
executables, requested MODPATH particle counts, and non-empty pathline output.
"""

import numpy as np

from mf6_model import (
    BACKWARD_PARTICLE_COUNT,
    FORWARD_PARTICLE_COUNT,
    NCOL,
    NLAY,
    NROW,
    WELL_COL,
    WELL_LAYER,
    WELL_ROW,
    ModelParameters,
    locate_mf6,
    locate_mp7,
    run_model,
)


def main() -> None:
    mf6 = locate_mf6()
    mp7 = locate_mp7()
    print(f"Using MODFLOW executable: {mf6}")
    print(f"Using MODPATH executable: {mp7}")

    no_pumping = run_model(ModelParameters(pumping_rate=0.0))
    pumping = run_model(ModelParameters(pumping_rate=300.0))

    assert no_pumping.head.shape == (NLAY, NROW, NCOL)
    assert pumping.head.shape == (NLAY, NROW, NCOL)
    assert np.all(np.isfinite(pumping.head))

    # The CHD cells must reproduce the imposed boundary heads exactly.
    np.testing.assert_allclose(pumping.head[:, :, 0], 32.0, atol=1e-6)
    np.testing.assert_allclose(pumping.head[:, :, -1], 31.0, atol=1e-6)

    h0 = no_pumping.head[WELL_LAYER, WELL_ROW, WELL_COL]
    hp = pumping.head[WELL_LAYER, WELL_ROW, WELL_COL]
    assert hp < h0, "Pumping should lower head at the pumping cell."

    # Verify that the particle definitions are exactly the requested sizes.
    assert pumping.backward.requested_particles == BACKWARD_PARTICLE_COUNT
    assert pumping.forward.requested_particles == FORWARD_PARTICLE_COUNT
    assert pumping.backward.start_xyz.shape == (BACKWARD_PARTICLE_COUNT, 3)
    assert pumping.forward.start_xyz.shape == (FORWARD_PARTICLE_COUNT, 3)

    # A successful MODPATH run should produce pathline records.  Some forward
    # particles at an outflow CHD may have very short paths; that is acceptable.
    assert pumping.backward.pathline_count > 0
    assert pumping.forward.pathline_count > 0

    print(f"MODFLOW version: {pumping.mf6_version}")
    print(f"MODPATH version: {pumping.backward.mp7_version}")
    print(f"No-pumping head at well cell: {h0:.6f} m")
    print(f"Pumping head at well cell:    {hp:.6f} m")
    print(f"Backward particles: {pumping.backward.requested_particles}")
    print(f"Forward particles:  {pumping.forward.requested_particles}")
    print("Smoke test PASSED")


if __name__ == "__main__":
    main()
