"""Command-line smoke test for the MODFLOW/Streamlit deployment environment.

Run with:
    python smoke_test.py

The test runs the model twice: first without pumping and then with pumping.  It
checks the binary, model execution, expected result dimensions, boundary heads,
and the physically expected drawdown at the pumping cell.
"""

import numpy as np

from mf6_model import (
    NCOL,
    NLAY,
    NROW,
    WELL_COL,
    WELL_LAYER,
    WELL_ROW,
    ModelParameters,
    locate_mf6,
    run_model,
)


def main() -> None:
    executable = locate_mf6()
    print(f"Using MODFLOW executable: {executable}")

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

    print(f"MODFLOW version: {pumping.mf6_version}")
    print(f"No-pumping head at well cell: {h0:.6f} m")
    print(f"Pumping head at well cell:    {hp:.6f} m")
    print("Smoke test PASSED")


if __name__ == "__main__":
    main()
