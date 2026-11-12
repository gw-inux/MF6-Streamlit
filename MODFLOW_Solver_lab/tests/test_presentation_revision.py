"""First-visit teaching cues and failed-run presentation, without solver changes."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   test_initial_guidance_disappears_after_scenario_edit_and_stays_dismissed: line 20
#   test_initial_guidance_dismisses_after_a_native_run_and_table_clear: line 31
#   test_plot_guidance_is_limited_to_the_initial_grid_and_preserves_geometry: line 45
#   test_failed_repeated_result_marks_status_and_legend_even_with_no_heads: line 58
# END CODE CONTENTS

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import numpy as np
import pytest
from MODFLOW_Solver_lab.core import Scenario, Solver
from MODFLOW_Solver_lab.plots import head_plot, FAILED_FILL, FAILED_RED
from test_streamlined_revision import limited_app


def test_initial_guidance_disappears_after_scenario_edit_and_stays_dismissed():
    at = limited_app()
    assert not at.session_state['initial_grid_notes_dismissed']
    assert any('nine interior cells' in c.value for c in at.caption)
    at.number_input(key='n').set_value(21).run()
    assert at.session_state['initial_grid_notes_dismissed']
    at.number_input(key='n').set_value(11).run()
    assert not any('nine interior cells' in c.value for c in at.caption)
    assert not at.exception


def test_initial_guidance_dismisses_after_a_native_run_and_table_clear():
    at = limited_app()
    at.button(key='run').click().run()
    assert at.session_state['runs'][-1]['success']
    assert at.session_state['initial_grid_notes_dismissed']
    at.session_state['runs'] = []
    at.run()
    assert not any('nine interior cells' in c.value for c in at.caption)
    assert not at.exception


@pytest.mark.parametrize('scenario,expected', [
    (Scenario(), 3), (Scenario(n=21), 0),
    (Scenario(confined=False), 0), (Scenario(complexity=True), 0)])
def test_plot_guidance_is_limited_to_the_initial_grid_and_preserves_geometry(scenario, expected):
    plain = head_plot(scenario, initial=False, settings=Solver("mf2005"))
    notes = head_plot(scenario, initial=False, settings=Solver("mf2005"), intro_notes=True)
    labels = [t for t in notes.axes[0].texts if t.get_gid() in ('initial_chd_note', 'initial_interior_note')]
    assert len(labels) == expected
    assert notes.axes[0].get_xlim() == plain.axes[0].get_xlim()
    assert notes.axes[0].get_ylim() == plain.axes[0].get_ylim()
    grid = lambda f: next(c for c in f.axes[0].collections if c.get_gid() == 'model_grid_faces')
    np.testing.assert_array_equal(grid(plain).get_segments(), grid(notes).get_segments())
    plt.close(plain); plt.close(notes)


@pytest.mark.parametrize('has_heads', [False, True])
def test_failed_repeated_result_marks_status_and_legend_even_with_no_heads(has_heads):
    s = Scenario()
    # Graphics fixture: aggregate success is false even if the last repeat converged.
    r = dict(success=False, status='One or more repetitions failed', repeats=2,
             heads=np.full(s.shape, 18.).ravel().tolist() if has_heads else None,
             outer_iterations=2, inner_iterations=8, sip_iterations=None, wall_s=.1)
    fig = head_plot(s, [r], initial=False, settings=Solver("mf2005"), intro_notes=True)
    ax = fig.axes[0]
    status = next(t for t in ax.texts if t.get_gid() == 'run_status')
    assert status.get_color() == FAILED_RED
    assert status.get_bbox_patch().get_facecolor()[:3] == to_rgba(FAILED_FILL)[:3]
    assert ax.get_legend().get_frame().get_facecolor()[:3] == to_rgba(FAILED_FILL)[:3]
    assert not any(t.get_gid() == 'initial_interior_note' for t in ax.texts)
    if has_heads:
        nodes = next(l for l in ax.lines if l.get_gid() == 'cell_head_dots')
        np.testing.assert_array_equal(nodes.get_ydata(), np.full(s.n, 18.))
    plt.close(fig)
