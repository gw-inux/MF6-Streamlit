"""Command-line smoke test for the split MODFLOW -> MODPATH workflow."""

from pathlib import Path

import numpy as np

from mf6_model import (
    BACKWARD_PARTICLE_COUNT,
    FORWARD_PARTICLE_COUNT,
    MODEL_NAME,
    NCOL,
    NLAY,
    NROW,
    WELL_COL,
    WELL_LAYER,
    WELL_ROW,
    ModelParameters,
    cleanup_workspace,
    locate_mf6,
    locate_mp7,
    run_modflow,
    run_modpath,
)


def main() -> None:
    print(f"MF6: {locate_mf6()}")
    print(f"MP7: {locate_mp7()}")

    baseline = None
    pumping = None

    try:
        baseline = run_modflow(ModelParameters(pumping_rate=0.0))
        pumping = run_modflow(ModelParameters(pumping_rate=300.0))

        assert baseline.head.shape == (NLAY, NROW, NCOL)
        assert pumping.head.shape == (NLAY, NROW, NCOL)
        assert np.all(np.isfinite(pumping.head))

        # Constant-head cells must equal their prescribed values.
        assert np.allclose(pumping.head[:, :, 0], 32.0)
        assert np.allclose(pumping.head[:, :, -1], 31.0)

        # Pumping should lower head at the well relative to the no-pumping case.
        h0 = baseline.head[WELL_LAYER, WELL_ROW, WELL_COL]
        hp = pumping.head[WELL_LAYER, WELL_ROW, WELL_COL]
        assert hp < h0

        # The successful flow workspace must still exist before MODPATH starts.
        assert Path(pumping.workspace).is_dir()
        assert (Path(pumping.workspace) / f"{MODEL_NAME}.hds").is_file()
        assert (Path(pumping.workspace) / f"{MODEL_NAME}.cbc").is_file()

        # Run MODPATH independently; this must not rerun MODFLOW.
        tracks = run_modpath(pumping, effective_porosity=0.25)

        assert tracks.backward.requested_particles == BACKWARD_PARTICLE_COUNT
        assert tracks.forward.requested_particles == FORWARD_PARTICLE_COUNT
        assert tracks.backward.start_xyz.shape == (BACKWARD_PARTICLE_COUNT, 3)
        assert tracks.forward.start_xyz.shape == (FORWARD_PARTICLE_COUNT, 3)
        assert tracks.backward.pathline_count > 0
        assert tracks.forward.pathline_count > 0

        print(f"No-pumping well head: {h0:.6f} m")
        print(f"Pumping well head:    {hp:.6f} m")
        print(f"Backward particles:   {tracks.backward.requested_particles}")
        print(f"Forward particles:    {tracks.forward.requested_particles}")
        print("Smoke test PASSED")

    finally:
        if baseline is not None:
            cleanup_workspace(baseline.workspace)
        if pumping is not None:
            cleanup_workspace(pumping.workspace)


if __name__ == "__main__":
    main()
