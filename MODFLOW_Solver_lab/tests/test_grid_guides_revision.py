"""v1.9: outside-aquifer grid guides and all-repeat convergence semantics."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   test_grid_guides_follow_cell_faces_and_preserve_model_grid: line 25
#   test_repeat_aggregation_keeps_an_earlier_failure: line 55
#   test_error_band_is_the_y_row_range_and_line_is_the_middle_row: line 69
# END CODE CONTENTS

from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
import pytest

from MODFLOW_Solver_lab import core
from MODFLOW_Solver_lab.core import Scenario, Solver
from MODFLOW_Solver_lab.plots import head_plot, error_plot
from test_view_revision import result


@pytest.mark.parametrize('confined', [True, False])
@pytest.mark.parametrize('cells,horizontal,layers', [
    (11, False, 1), (11, True, 3), (1001, False, 1), (101, True, 3)])
def test_grid_guides_follow_cell_faces_and_preserve_model_grid(confined, cells, horizontal, layers):
    s = Scenario(confined=confined, n=cells, complexity=True,
                 horizontal_2d=horizontal, nlay=layers)
    s.validate()
    fig = head_plot(s, [result(s)], initial=False)
    ax = fig.axes[0]
    grid = next(c for c in ax.collections if c.get_gid() == 'model_grid_faces')
    guides = next(c for c in ax.collections if c.get_gid() == 'grid_extensions')
    real = np.asarray(grid.get_segments())
    extended = np.asarray(guides.get_segments())
    np.testing.assert_array_equal(extended[:, :, 0], real[:, :, 0])
    np.testing.assert_allclose(extended[:, 0, 1], ax.get_ylim()[0])
    np.testing.assert_allclose(extended[:, 1, 1], ax.get_ylim()[1])
    np.testing.assert_allclose(real[:, 0, 1], s.bottom)
    np.testing.assert_allclose(real[:, 1, 1], s.top)
    assert real[0, 0, 0] == .5 and real[-1, 0, 0] == s.n + .5
    assert np.allclose(real[:, 0, 0] % 1, .5)  # Faces, not node centres.
    assert len(extended) <= 102  # Retain the existing dense-grid thinning.
    assert np.all(guides.get_colors()[0, :3] > grid.get_colors()[0, :3])
    assert guides.get_linewidths()[0] < grid.get_linewidths()[0]
    domain = next(p for p in ax.patches if p.get_gid() == 'model_domain')
    assert guides.get_zorder() < domain.get_zorder() < grid.get_zorder()
    assert domain.get_facecolor()[3] == 1  # Guides do not alter the model interior.
    assert not any(line.get_visible() for line in ax.get_ygridlines())
    plt.close(fig)


@pytest.mark.parametrize('successes', [
    (True,), (False,), (True, True, True), (False, True, True),
    (True, False, True), (True, True, False), (False, False, False)])
def test_repeat_aggregation_keeps_an_earlier_failure(monkeypatch, tmp_path, successes):
    # Controlled execution-status fixtures test aggregation, not model physics.
    outcomes = iter(dict(success=ok, status='Converged' if ok else 'Failed / not converged',
                         wall_s=float(i+1), outer_iterations=2, inner_iterations=4,
                         sip_iterations=None) for i, ok in enumerate(successes))
    monkeypatch.setattr(core, 'run_once', lambda *args, **kwargs: deepcopy(next(outcomes)))
    r = core.run_repeated(Scenario(), Solver('mf2005'), tmp_path, 'unused-fixture', repeats=len(successes))
    assert r['success'] == all(successes)
    assert r['all_repeats_converged'] == all(successes)
    assert [v['success'] for v in r['repeat_status']] == list(successes)
    if not all(successes):
        assert r['status'] == 'At least one repeat failed'


def test_error_band_is_the_y_row_range_and_line_is_the_middle_row():
    # Distinct synthetic row errors make the unchanged plot's meaning explicit.
    s = Scenario(n=11, complexity=True, horizontal_2d=True)
    errors = np.linspace(-2e-4, 4e-4, s.nrow)[:, None] * np.sin(np.pi*s.x/s.length)
    heads = s.analytic()[None, :] + errors
    r = dict(heads=heads.ravel().tolist(), label='Graphics fixture')
    before = deepcopy(r)
    fig = error_plot(s, [r])
    ax = fig.axes[0]
    np.testing.assert_allclose(ax.lines[0].get_ydata(), errors[s.nrow//2], atol=1e-12)
    vertices = ax.collections[0].get_paths()[0].vertices
    for i, x in enumerate(s.x):
        y = vertices[np.isclose(vertices[:, 0], x), 1]
        assert min(y) == pytest.approx(errors[:, i].min(), abs=1e-12)
        assert max(y) == pytest.approx(errors[:, i].max(), abs=1e-12)
    assert r == before
    plt.close(fig)
