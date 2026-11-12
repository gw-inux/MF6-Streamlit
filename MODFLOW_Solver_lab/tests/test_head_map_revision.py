"""v1.7: uniform CHD previews, layer-1 maps and comparison presentation."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   test_preview_chd_is_opaque_and_uniform_in_both_views: line 27
#   test_head_map_uses_only_native_layer_one_without_mutating_heads: line 50
#   test_head_map_of_dry_first_layer_is_blank_with_an_explanation: line 73
#   test_heterogeneity_tag_matches_the_sampled_field: line 93
#   test_ui_surface_map_and_reordered_numeric_comparison: line 104
# END CODE CONTENTS

from copy import deepcopy
from dataclasses import asdict
import json

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
import numpy as np
import pytest

from MODFLOW_Solver_lab.core import Scenario, comparison_row
from MODFLOW_Solver_lab.plots import CHD_FILL, first_layer_head_map, model_preview
from test_ui import app


@pytest.mark.parametrize('quantity', ['Empty cells', 'K zones', 'Initial heads'])
def test_preview_chd_is_opaque_and_uniform_in_both_views(quantity):
    s = Scenario(complexity=True, horizontal_2d=True, nlay=3, random_k=True,
                 initial='Random distribution', initial_min=5., initial_max=30.)
    fig = model_preview(s, quantity)
    fig.canvas.draw()
    pixels = np.asarray(fig.canvas.buffer_rgba())
    samples = []
    for ax, ys in [(fig.axes[0], s.dy*np.array([1, 2, 3])),
                   (fig.axes[1], s.z_centres)]:
        patches = [p for p in ax.patches if p.get_gid()=='preview_chd']
        assert patches
        assert all(p.get_facecolor()[3]==1. for p in patches)
        for x in (0., s.length):
            for y in ys:
                px, py = np.rint(ax.transData.transform((x,y))).astype(int)
                samples.append(pixels[pixels.shape[0]-1-py,px,:3])
    expected = np.asarray(to_rgb(CHD_FILL))*255
    np.testing.assert_allclose(samples, np.tile(expected,(len(samples),1)), atol=1.)
    plt.close(fig)


@pytest.mark.parametrize('layers', [1, 3])
@pytest.mark.parametrize('confined', [True, False])
def test_head_map_uses_only_native_layer_one_without_mutating_heads(layers, confined):
    s = Scenario(complexity=True, horizontal_2d=True, nlay=layers, confined=confined)
    k, y, x = np.indices(s.shape)
    heads = 18.+100*k+.02*y+.01*x
    heads[0,3,4] = 1e30  # A dry/no-data output sentinel, not a solved-head fixture.
    before = heads.copy()
    fig = first_layer_head_map(s, heads)
    fig.canvas.draw()
    ax = fig.axes[0]
    mesh = next(c for c in ax.collections if c.get_gid()=='first_layer_heads')
    actual = np.ma.asarray(mesh.get_array()).filled(np.nan).reshape(s.nrow,s.n)
    np.testing.assert_allclose(actual, s.head_array(heads)[0], equal_nan=True)
    np.testing.assert_array_equal(heads,before)
    assert mesh.norm.vmax < 20.  # Deeper-layer values must not affect the colour scale.
    pixels = ax.transData.transform([[0,0],[s.dx,s.dy]])
    assert pixels[1,0]-pixels[0,0]==pytest.approx(pixels[1,1]-pixels[0,1])
    trace = next(line for line in ax.lines if line.get_gid()=='section_trace')
    assert np.all(np.asarray(trace.get_ydata())==(s.nrow//2)*s.dy)
    assert ax.get_xlim()==pytest.approx((-s.dx/2,s.length+s.dx/2))
    assert ax.get_ylim()==pytest.approx((-s.dy/2,s.length+s.dy/2))
    plt.close(fig)


def test_head_map_of_dry_first_layer_is_blank_with_an_explanation():
    s = Scenario(complexity=True, horizontal_2d=True, nlay=3,
                 confined=False, aquifer_top=60.)
    fig = first_layer_head_map(s, np.full(s.shape,17.))
    ax = fig.axes[0]
    assert len(fig.axes)==1  # No misleading colour scale for an empty layer.
    assert not any(c.get_gid()=='first_layer_heads' for c in ax.collections)
    assert any('No wet, active heads' in t.get_text() for t in ax.texts)
    assert not any(p.get_gid()=='head_map_chd' for p in ax.patches)
    plt.close(fig)


@pytest.mark.parametrize('horizontal', [False, True])
@pytest.mark.parametrize('parameters,heterogeneous', [
    ({'random_k':False},False),
    ({'random_k':True,'k_zones':1},False),
    ({'random_k':True,'k_zones':11},True),
    ({'random_k':True,'k_zones':1,'nlay':3},True),
    ({'random_k':True,'k_min':1e-4,'k_max':1e-4},False),
])
def test_heterogeneity_tag_matches_the_sampled_field(horizontal,parameters,heterogeneous):
    s = Scenario(complexity=True,horizontal_2d=horizontal,**parameters)
    r = dict(scenario=asdict(s),label='MODFLOW-2005 / PCG',status='Converged',
             outer_iterations=2,inner_iterations=3,sip_iterations=None,wall_s=.0123,
             metrics={},budget_percent=.125)
    row = comparison_row(r)
    assert row['Model / solver'].endswith(' · het.')==heterogeneous
    assert row['Budget discrepancy (%)']==.125
    assert r['label']=='MODFLOW-2005 / PCG'


def test_ui_surface_map_and_reordered_numeric_comparison():
    at = app()
    label = '**Computed heads · groundwater surface (x–y)**'
    assert not at.toggle(key='show_initial').value
    assert not any(e.label==label for e in at.expander)
    at.toggle(key='complexity').set_value(True).run()
    at.toggle(key='add_layers').set_value(True).run()
    assert not any(e.label==label for e in at.expander)  # A vertical section has no x–y map.
    at.toggle(key='horizontal_2d').set_value(True).run()
    box = next(e for e in at.expander if e.label==label)
    assert any('Run the model' in c.value for c in box.caption)
    at.button(key='run').click().run()
    assert at.session_state['runs'][-1]['success']
    at.number_input(key='plot_layer').set_value(3).run()
    box = next(e for e in at.expander if e.label==label)
    assert any('Run 01:' in c.value for c in box.caption)
    at.toggle(key='random_k').set_value(True).run()
    box = next(e for e in at.expander if e.label==label)
    assert any('Inputs have changed' in c.value for c in box.caption)
    at.button(key='run').click().run()
    assert at.session_state['runs'][-1]['success'] and len(at.session_state['runs'])==2
    table = next(d for d in at.dataframe if 'Name' in d.value.columns)
    assert list(table.value.columns)==[
        'Run', 'Name', 'Outer', 'Inner', 'Time (s)', 'WB discrep.', 'Convergence',
        'Aquifer', 'Grid (x × y × layers)', 'Cells', 'Model / solver',
        'SIP', 'RMSE (m)', 'Max error (m)']
    assert list(table.value['Convergence']) == ['✓', '✓']
    assert not table.value.iloc[0]['Model / solver'].endswith('het.')
    assert table.value.iloc[1]['Model / solver'].endswith('het.')
    config = json.loads(table.proto.columns)
    assert config['Model / solver']['width']=='medium'
    assert config['WB discrep.']['type_config']['format']=='%.2f %%'
    assert list(table.value['WB discrep.'])==[r['budget_percent'] for r in at.session_state['runs']]
    # Display-only failure fixtures cover unreadable and nonconverged native output.
    records = deepcopy(at.session_state['runs'])
    records[-1]['success'] = False
    records[-1]['status'] = 'Failed test fixture'
    at.session_state['runs'] = records
    at.run()
    assert next(e for e in at.expander if e.label==label).warning
    table = next(d for d in at.dataframe if 'Name' in d.value.columns)
    assert list(table.value['Convergence']) == ['✓', '✗']
    records[-1]['heads'] = None
    at.session_state['runs'] = records
    at.run()
    assert next(e for e in at.expander if e.label==label).info
    assert not at.exception
