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
        base_params = ModelParameters(
            nrow=nrow, ncol=ncol, well_positions=wells,
            pumping_rates=(0.0, 0.0, 0.0),
        )
        pump_params = ModelParameters(
            nrow=nrow, ncol=ncol, well_positions=wells,
            pumping_rates=(75.0, 100.0, 125.0),
        )
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

        # Budget names must be decoded text (not strings such as b'CHD_IN').
        if pumping.cumulative_budget:
            budget_names = [name for name, _value in pumping.cumulative_budget]
            assert all(not name.startswith("b'") for name in budget_names)
            assert any(name.endswith("_IN") for name in budget_names)
            assert any(name.endswith("_OUT") for name in budget_names)

        particle_counts = (40, 80, 120)
        tracks = run_modpath(
            pumping,
            effective_porosity=0.25,
            backward_particle_counts=particle_counts,
        )
        assert tracks.backward.requested_particles == sum(particle_counts)
        assert tracks.forward.requested_particles == NLAY * nrow * 2
        assert tracks.backward.pathline_count > 0
        assert tracks.forward.pathline_count > 0

        print(f"Dynamic grid: {NLAY} x {nrow} x {ncol}")
        print(f"Wells: {len(wells)}")
        print(f"Pumping rates: {pump_params.pumping_rates} m3/day")
        print(f"Backward particles by well: {particle_counts}")
        print(f"Backward particles total: {tracks.backward.requested_particles}")
        print(f"Forward particles: {tracks.forward.requested_particles}")
        print("Smoke test PASSED")
    finally:
        if baseline is not None:
            cleanup_workspace(baseline.workspace)
        if pumping is not None:
            cleanup_workspace(pumping.workspace)


if __name__ == "__main__":
    main()
