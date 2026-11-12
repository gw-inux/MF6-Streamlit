"""v1.6: actual layer interfaces and recovery of old display preferences."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   test_result_layer_interfaces: line 22
#   test_old_both_off_state_recovers_and_callbacks_stay_enabled: line 46
# END CODE CONTENTS

import matplotlib.pyplot as plt
import numpy as np
import pytest

from MODFLOW_Solver_lab.core import Scenario
from MODFLOW_Solver_lab.plots import head_plot
from test_ui import app
from test_view_revision import result


@pytest.mark.parametrize('confined', [True, False])
@pytest.mark.parametrize('horizontal', [True, False])
@pytest.mark.parametrize('layers', [1, 3, 10])
def test_result_layer_interfaces(confined, horizontal, layers):
    s = Scenario(complexity=True, confined=confined, horizontal_2d=horizontal,
                 nlay=layers, thickness=30., aquifer_top=24.)
    fig = head_plot(s, [result(s)], initial=False, layer=layers-1)
    ax = fig.axes[0]
    interfaces = [c for c in ax.collections if c.get_gid()=='layer_interfaces']
    assert bool(interfaces)==(layers>1)
    if interfaces:
        collection = interfaces[0]
        segments = np.asarray(collection.get_segments())
        expected = np.linspace(s.top, s.bottom, layers+1)[1:-1]
        assert len(segments)==layers-1
        np.testing.assert_allclose(segments[:,0,1], expected)
        np.testing.assert_allclose(segments[:,1,1], expected)
        np.testing.assert_allclose(segments[:,0,0], .5)
        np.testing.assert_allclose(segments[:,1,0], s.n+.5)
        assert collection.get_linewidths()[0] <= .5
        filling = next(c for c in ax.collections if c.get_gid()=='wetted_cells')
        assert collection.get_zorder() > filling.get_zorder()
        assert all(collection.get_zorder()>p.get_zorder() for p in ax.patches if p.get_gid()=='chd_cell')
    assert not any(line.get_visible() for line in ax.get_ygridlines())
    plt.close(fig)


def test_old_both_off_state_recovers_and_callbacks_stay_enabled():
    at = app()
    at.session_state['show_cell_heads'] = False
    at.session_state['show_cell_lines'] = False
    at.session_state['show_computed_heads'] = False  # Obsolete v1.5 preference.
    at.run()
    assert at.toggle(key='show_cell_lines').value
    assert not at.toggle(key='show_cell_heads').value
    for key in ('show_cell_lines', 'show_cell_heads', 'show_cell_lines'):
        other = 'show_cell_heads' if key=='show_cell_lines' else 'show_cell_lines'
        assert at.toggle(key=key).value and not at.toggle(key=key).disabled
        at.toggle(key=key).set_value(False).run()
        assert not at.toggle(key=key).value and at.toggle(key=other).value
        assert not at.exception
