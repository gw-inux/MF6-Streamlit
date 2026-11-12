"""v2.1: scoped controls, integer spacing, closure guides and map reuse."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   test_full_settings_lives_in_scenario_and_keeps_values: line 32
#   test_random_k_switches_preview_only_on_activation: line 45
#   test_preferred_spacing_sequence_both_directions: line 60
#   test_integer_initialization_keeps_length_and_integral_spacings: line 75
#   test_integer_spacing_buttons_manual_values_and_invalid_geometry: line 79
#   test_spacing_modes_honor_three_cell_and_active_cell_limits: line 110
#   test_guides_from_actual_saved_solver: line 132
#   test_residual_norms_are_not_conflated: line 147
#   test_plot_thresholds_preserve_data_and_handle_zero_values: line 155
#   test_inspected_run_threshold_is_not_replaced_by_current_inputs: line 171
#   test_head_map_cache_reuses_exact_source_and_invalidates_any_head: line 187
# END CODE CONTENTS

from dataclasses import replace
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pytest
from MODFLOW_Solver_lab.core import Scenario, Solver
from MODFLOW_Solver_lab.diagnostic_guides import convergence_guides
from MODFLOW_Solver_lab.map_rendering import head_map_image
from MODFLOW_Solver_lab.plots import convergence_plot
from MODFLOW_Solver_lab.spacing import adjacent_spacing, integer_spacing_for_grid, valid_spacing_steps
from test_streamlined_revision import limited_app


def test_full_settings_lives_in_scenario_and_keeps_values():
    at=limited_app()
    panel=next(e for e in at.expander if e.label=='**Parameters for the scenario**')
    assert panel.toggle(key='full_settings').value is False
    panel.toggle(key='full_settings').set_value(True).run()
    at.number_input(key='recharge').set_value(175.)
    at.toggle(key='full_settings').set_value(False).run()
    at.run()
    at.toggle(key='full_settings').set_value(True).run()
    assert at.number_input(key='recharge').value==175.
    assert not at.exception


def test_random_k_switches_preview_only_on_activation():
    at=limited_app()
    at.toggle(key='complexity').set_value(True).run()
    assert at.selectbox(key='preview_quantity').value=='Empty cells'
    at.toggle(key='random_k').set_value(True).run()
    assert at.selectbox(key='preview_quantity').value=='K zones'
    at.selectbox(key='preview_quantity').set_value('Initial heads').run()
    at.number_input(key='k_zones').set_value(7).run()
    assert at.selectbox(key='preview_quantity').value=='Initial heads'
    at.toggle(key='random_k').set_value(False).run()
    at.toggle(key='random_k').set_value(True).run()
    assert at.selectbox(key='preview_quantity').value=='K zones'
    assert not at.exception


def test_preferred_spacing_sequence_both_directions():
    expected=[1000,500,250,200,100,50,25,20,10,5,3,2,1]
    # 6,000 m supports every requested step, including 3 m.
    for a,b in zip(expected,expected[1:]):
        assert adjacent_spacing(a,6000.,-1)==b
        assert adjacent_spacing(b,6000.,1)==a
    assert adjacent_spacing(1,6000.,-1) is None
    assert 3 not in valid_spacing_steps(5000.)
    assert adjacent_spacing(5,5000.,-1)==2
    assert adjacent_spacing(125,5000.,-1)==100
    assert adjacent_spacing(125,5000.,1)==200


@pytest.mark.parametrize('length,cells,expected', [(5000.,11,500),(5000.,7,1000),
    (5000.,10001,1),(2573.,32,83),(1.,3,1),(2573.5,11,257)])
def test_integer_initialization_keeps_length_and_integral_spacings(length,cells,expected):
    assert integer_spacing_for_grid(length,cells)==expected


def test_integer_spacing_buttons_manual_values_and_invalid_geometry():
    at=limited_app()
    at.toggle(key='spacing_mode').set_value(True).run()
    assert type(at.number_input(key='cell_spacing').value) is int
    assert at.number_input(key='cell_spacing').value==500
    at.button(key='spacing_decrease').click().run()
    assert at.number_input(key='cell_spacing').value==250
    assert at.session_state['grid_n']==21
    at.button(key='spacing_decrease').click().run()
    assert at.number_input(key='cell_spacing').value==200
    at.button(key='spacing_increase').click().run()
    assert at.number_input(key='cell_spacing').value==250
    at.number_input(key='cell_spacing').set_value(125).run()
    assert at.session_state['grid_n']==41
    at.toggle(key='spacing_mode').set_value(False).run()
    assert at.number_input(key='n').value==41
    at.number_input(key='n').set_value(7).run()
    at.toggle(key='spacing_mode').set_value(True).run()
    assert at.number_input(key='cell_spacing').value==1000
    assert at.number_input(key='length').value==5000.
    at.number_input(key='cell_spacing').set_value(3).run()
    assert at.error and not at.exception
    assert not any(b.key=='run' for b in at.button)
    at.button(key='spacing_increase').click().run()
    assert at.number_input(key='cell_spacing').value==5 and not at.error
    at.number_input(key='length').set_value(5000.5).run()
    assert at.error and not at.exception
    at.toggle(key='spacing_mode').set_value(False).run()
    assert not at.error and not at.exception


def test_spacing_modes_honor_three_cell_and_active_cell_limits():
    at=limited_app()
    at.toggle(key='complexity').set_value(True).run()
    at.toggle(key='horizontal_2d').set_value(True).run()
    at.toggle(key='spacing_mode').set_value(True).run()
    at.number_input(key='cell_spacing').set_value(10).run()
    assert not at.error and at.session_state['grid_n']==501
    at.button(key='spacing_decrease').click().run()
    assert at.number_input(key='cell_spacing').value==5
    assert at.error and not any(b.key=='run' for b in at.button)
    at.button(key='spacing_increase').click().run()
    assert not at.error and not at.exception


@pytest.mark.parametrize('engine,method,kind,values', [
    ('mf2005','PCG','inner', {'hclose':2e-5,'rclose':3e-6}),
    ('mf2005','SIP','SIP', {'hclose':7e-5}),
    ('mfnwt','GMRES','outer', {'headtol':6e-5,'fluxtol':8e-6}),
    ('mfnwt','XMD','outer', {'headtol':6e-5,'fluxtol':8e-6}),
    ('mf6','CG','outer', {'outer_dvclose':5e-5,'inner_dvclose':1e-7}),
    ('mf6','BICGSTAB','inner', {'outer_dvclose':5e-5,'inner_dvclose':1e-7,'rcloserecord':2e-8}),
])
def test_guides_from_actual_saved_solver(engine,method,kind,values):
    cfg=Solver(engine,method,overrides=values)
    guides=convergence_guides(cfg,kind)
    expected=values.get('hclose',values.get('headtol',values.get('outer_dvclose') if kind=='outer' else values.get('inner_dvclose')))
    assert guides['head_change'][0]==expected
    if engine=='mfnwt':
        assert guides['residual'] is None
        assert '8.00E-06' in guides['residual_note'] and 'norm' in guides['residual_note']
    elif method=='SIP' or kind=='outer':
        assert guides['residual'] is None
    else:
        assert guides['residual'][0]==values.get('rclose',values.get('rcloserecord'))


@pytest.mark.parametrize('option,has_line', [('INFINITY',True),('STRICT',True),('L2NORM_RCLOSE',False),('RELATIVE_RCLOSE',False)])
def test_residual_norms_are_not_conflated(option,has_line):
    cfg=Solver('mf6','CG',overrides={'rcloserecord':[2e-6,option]})
    guides=convergence_guides(cfg,'inner')
    assert (guides['residual'] is not None)==has_line
    if not has_line:
        assert option in guides['residual_note'] and '2.00E-06' in guides['residual_note']


def test_plot_thresholds_preserve_data_and_handle_zero_values():
    cfg=Solver('mf2005','PCG',overrides={'hclose':2e-5,'rclose':3e-7})
    history=[dict(iteration=i+1,head_change=h,residual=r,kind='inner') for i,(h,r) in enumerate([(1.,.1),(.001,0.),(0.,0.)])]
    fig=convergence_plot(history,'inner',solver=cfg)
    for ax,value in zip(fig.axes,[2e-5,3e-7]):
        threshold=next(l for l in ax.lines if l.get_gid()=='closure_threshold')
        np.testing.assert_array_equal(threshold.get_ydata(),[value,value])
        assert ax.get_yscale()=='log'
    np.testing.assert_array_equal(fig.axes[0].lines[0].get_ydata(),[1.,.001])
    plt.close(fig)
    zero=convergence_plot([dict(iteration=1,head_change=0.,residual=0.,kind='inner')],'inner',solver=cfg)
    assert all(any(l.get_gid()=='closure_threshold' for l in ax.lines) for ax in zero.axes)
    zero.canvas.draw()
    plt.close(zero)


def test_inspected_run_threshold_is_not_replaced_by_current_inputs(monkeypatch):
    from MODFLOW_Solver_lab import results
    used=[]
    original=results.convergence_plot
    def capture(history,kind,solver=None):
        used.append(solver.parameters()['hclose'])
        return original(history,kind,solver)
    monkeypatch.setattr(results,'convergence_plot',capture)
    at=limited_app()
    at.number_input(key='mf2005_PCG_SIMPLE_basic_hclose').set_value(4e-5)
    at.button(key='run').click().run()
    at.number_input(key='mf2005_PCG_SIMPLE_basic_hclose').set_value(9e-4).run()
    assert used[-1]==4e-5
    assert not at.exception


def test_head_map_cache_reuses_exact_source_and_invalidates_any_head(monkeypatch):
    from MODFLOW_Solver_lab import map_rendering
    calls=[]
    original=map_rendering.computed_head_map
    def capture(*args,**kwargs):
        calls.append(kwargs)
        return original(*args,**kwargs)
    monkeypatch.setattr(map_rendering,'computed_head_map',capture)
    s=Scenario(complexity=True,horizontal_2d=True)
    heads=np.tile(s.analytic(),s.nrow).reshape(s.shape)
    cache={}
    current=head_map_image(cache,s,heads)
    assert head_map_image(cache,s,heads.copy()) is current and len(calls)==1
    stale=head_map_image(cache,s,heads,stale=True)
    assert current!=stale and len(calls)==2 and len(cache['images'])==2
    assert head_map_image(cache,s,heads) is current
    original_source=cache["source"]
    heads[0,2,3]+=.01
    head_map_image(cache,s,heads)
    assert cache["source"]!=original_source and len(calls)==3
    assert len(cache['images'])==1
    head_map_image(cache,replace(s,confined=False),heads)
    assert len(calls)==4 and len(cache['images'])==1
    with Image.open(BytesIO(current)) as picture:
        assert picture.format=='PNG' and picture.width<1500
    assert not plt.get_fignums()
