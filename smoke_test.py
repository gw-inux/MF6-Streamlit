"""Command-line smoke test for dynamic grid, multiple wells and MODPATH."""

from pathlib import Path
import numpy as np

from mf6_model import (
    MODEL_NAME, NLAY, PARTICLES_PER_WELL, WELL_LAYER,
    ModelParameters, cleanup_workspace, locate_mf6, locate_mp7,
    run_modflow, run_modpath,
)


def main() -> None:
    print(f"MF6: {locate_mf6()}")
    print(f"MP7: {locate_mp7()}")

    nrow, ncol = 17, 25
    centre_row, centre_col = nrow // 2, ncol // 2
    wells = ((centre_row, centre_col), (centre_row - 2, centre_col), (centre_row + 2, centre_col))

    baseline = pumping = None
    try:
        base_params = ModelParameters(nrow=nrow, ncol=ncol, well_positions=wells, pumping_rate=0.0)
        pump_params = ModelParameters(nrow=nrow, ncol=ncol, well_positions=wells, pumping_rate=100.0)
        baseline = run_modflow(base_params)
        pumping = run_modflow(pump_params)

        assert baseline.head.shape == (NLAY, nrow, ncol)
        assert pumping.head.shape == (NLAY, nrow, ncol)
        assert np.all(np.isfinite(pumping.head))
        assert np.allclose(pumping.head[:, :, 0], 32.0)
        assert np.allclose(pumping.head[:, :, -1], 31.0)

        for row, col in wells:
            assert pumping.head[WELL_LAYER, row, col] < baseline.head[WELL_LAYER, row, col]

        assert Path(pumping.workspace).is_dir()
        assert (Path(pumping.workspace) / f"{MODEL_NAME}.hds").is_file()
        assert (Path(pumping.workspace) / f"{MODEL_NAME}.cbc").is_file()

        tracks = run_modpath(pumping, effective_porosity=0.25)
        assert tracks.backward.requested_particles == PARTICLES_PER_WELL * len(wells)
        assert tracks.forward.requested_particles == NLAY * nrow * 2
        assert tracks.backward.pathline_count > 0
        assert tracks.forward.pathline_count > 0

        print(f"Dynamic grid: {NLAY} x {nrow} x {ncol}")
        print(f"Wells: {len(wells)}")
        print(f"Backward particles: {tracks.backward.requested_particles}")
        print(f"Forward particles: {tracks.forward.requested_particles}")
        print("Smoke test PASSED")
    finally:
        if baseline is not None:
            cleanup_workspace(baseline.workspace)
        if pumping is not None:
            cleanup_workspace(pumping.workspace)


if __name__ == "__main__":
    main()
