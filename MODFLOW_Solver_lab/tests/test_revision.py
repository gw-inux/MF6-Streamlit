"""Regression coverage for convertible physics and the revised teaching workflow."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   baseline: line 29
#   tight_solver: line 35
#   test_unconfined_reference_matches_dupuit_and_confined_limits: line 48
#   test_reference_crossing_top_preserves_potential_balance_and_boundaries: line 59
#   test_native_unconfined_results_and_face_balances: line 77
#   test_unconfined_refinement_reduces_error: line 90
#   test_unconfined_ui_presets_with_real_engines: line 103
#   test_unconfined_diagnostics_reject_dry_heads_and_missing_flows: line 110
#   test_hidden_initial_heads_do_not_affect_plot_extent_or_model_guess: line 118
#   test_grid_fields_reject_invalid_studies: line 134
#   test_geometry_visibility_and_grid_field_workflow: line 139
# END CODE CONTENTS

from dataclasses import replace
import matplotlib.pyplot as plt
import numpy as np
import pytest

from MODFLOW_Solver_lab.core import Scenario, Solver, head_metrics, run_once
from MODFLOW_Solver_lab.settings import parse_grid_entries, new_profile, solver_from_profile
from MODFLOW_Solver_lab.plots import head_plot
from test_models import CHOICES, executable
from test_ui import app

def baseline(**kwargs):
    """Retain v1.2 physical benchmark inputs while testing seconds internally."""
    return Scenario(**(dict(k_ms=1e-3, recharge_mmy=200.) | kwargs))



def tight_solver(engine, method):
    if engine == 'mf2005':
        p = dict(hclose=1e-8, mxiter=500)
        if method == 'PCG':
            p.update(rclose=1e-8/86400., iter1=1000)
    elif engine == 'mfnwt':
        p = dict(headtol=1e-8, fluxtol=1e-8/86400., maxiterout=500)
    else:
        p = dict(outer_dvclose=1e-8, inner_dvclose=1e-8,
                 rcloserecord=1e-11, outer_maximum=500, inner_maximum=1000)
    return Solver(engine, method, overrides=p)


def test_unconfined_reference_matches_dupuit_and_confined_limits():
    s = baseline(confined=False, n=101, aquifer_top=100.)
    x = s.x
    expected = np.sqrt(s.left**2+(s.right**2-s.left**2)*x/s.length
                       +s.recharge_ms/s.k_ms*x*(s.length-x))
    np.testing.assert_allclose(s.analytic(), expected, rtol=1e-14)
    s = replace(s, aquifer_top=10.)  # Entire layer is fully saturated.
    fixed = replace(s, confined=True, thickness=10.)
    np.testing.assert_allclose(s.analytic(), fixed.analytic(), rtol=1e-14)


def test_reference_crossing_top_preserves_potential_balance_and_boundaries():
    s = baseline(confined=False, n=101, aquifer_top=17.)
    h = s.analytic()
    assert min(h) < s.top < max(h)
    np.testing.assert_allclose(h[[0,-1]], [s.left,s.right], atol=1e-13)
    potential = s.discharge_potential(h)
    residual = s.k_ms*np.diff(potential,n=2)/s.dx**2+s.recharge_ms
    np.testing.assert_allclose(residual, 0., atol=1e-14)
    eps = 1e-5
    slopes = np.diff(s.discharge_potential([s.top-eps,s.top,s.top+eps]))/eps
    np.testing.assert_allclose(slopes, s.top, atol=eps)


@pytest.mark.parametrize('engine,method', CHOICES)
@pytest.mark.parametrize('scenario', [baseline(confined=False),
    baseline(confined=False,recharge_mmy=0.), baseline(confined=False,aquifer_top=17.),
    baseline(confined=False,initial='Specified uniform head',initial_head=60.),
    baseline(confined=False,aquifer_top=10.)])
def test_native_unconfined_results_and_face_balances(engine,method,scenario,tmp_path):
    r = run_once(scenario,tight_solver(engine,method),tmp_path,executable(engine))
    assert r['success'], r.get('read_error',r['stdout'][-2000:])
    assert r['metrics']['max_error_m'] < .1
    assert r['metrics']['max_residual_m3s'] < 1e-5
    assert abs(r['metrics']['balance_m3s']) < 1e-5
    assert r['metrics']['boundary_error_m'] < 1e-7
    assert abs(r['budget_percent']) < .01
    if scenario.aquifer_top == 10.:
        assert r['metrics']['max_error_m'] < 2e-6


@pytest.mark.parametrize('engine,method', CHOICES)
def test_unconfined_refinement_reduces_error(engine,method,tmp_path):
    errors=[]
    for n in [11,101,1001]:
        r=run_once(baseline(confined=False,n=n),tight_solver(engine,method),
                   tmp_path/str(n),executable(engine))
        assert r['success'],r['stdout'][-2000:]
        errors.append(r['metrics']['max_error_m'])
    assert errors[1] < errors[0]*.25,errors
    assert errors[2] < errors[1]*.3,errors


@pytest.mark.parametrize('engine,method,preset', [(e,m,p) for e,m in CHOICES
    for p in (['SIMPLE'] if e=='mf2005' else ['SIMPLE','MODERATE','COMPLEX'])])
def test_unconfined_ui_presets_with_real_engines(engine,method,preset,tmp_path):
    cfg=solver_from_profile(new_profile(engine,method,preset))
    r=run_once(baseline(confined=False),cfg,tmp_path,executable(engine))
    assert r['success'],r['stdout'][-2000:]
    assert r['metrics']['max_error_m'] < .1


def test_unconfined_diagnostics_reject_dry_heads_and_missing_flows():
    s=baseline(confined=False)
    with pytest.raises(ValueError,match='cell-face'):
        head_metrics(s,s.analytic())
    with pytest.raises(ValueError,match='dry'):
        head_metrics(s,np.zeros(s.n),np.zeros(s.n-1))


def test_hidden_initial_heads_do_not_affect_plot_extent_or_model_guess():
    s=baseline(initial='Specified uniform head',initial_head=5000.)
    original=s.starting_heads().copy()
    visible=head_plot(s,analytical=True,initial=True)
    hidden=head_plot(s,analytical=True,initial=False)
    bare=head_plot(s,analytical=False,initial=False)
    assert visible.axes[0].get_ylim()[1] > 5000
    assert hidden.axes[0].get_ylim()[1] < 60
    assert bare.axes[0].get_ylim()[1] < 60
    assert 'Initial heads' not in hidden.axes[0].get_legend_handles_labels()[1]
    np.testing.assert_array_equal(s.starting_heads(),original)
    for fig in [visible,hidden,bare]:
        plt.close(fig)


@pytest.mark.parametrize('entries',[[],['11']*2,[''],['1e3'],['11,101'],list(map(str,range(3,14)))])
def test_grid_fields_reject_invalid_studies(entries):
    with pytest.raises(ValueError):
        parse_grid_entries(entries)


def test_geometry_visibility_and_grid_field_workflow():
    at=app()
    assert at.toggle(key='confined').value
    assert not at.toggle(key='show_initial').value
    assert at.selectbox(key='grid_count').value == 3
    assert [at.text_input(key=f'grid_size_{i}').value for i in [1,2,3]] == ['11','101','1001']
    at.number_input(key='thickness').set_value(30.).run()
    at.toggle(key='confined').set_value(False).run()
    assert at.number_input(key='aquifer_top').value == 20.
    assert not any(w.key=='thickness' for w in at.number_input)
    at.number_input(key='aquifer_top').set_value(25.).run()
    at.selectbox(key='repeats').set_value(1)
    at.selectbox(key='initial').set_value('Specified uniform head').run()
    at.number_input(key='initial_head').set_value(60.)
    at.button(key='run').click().run()
    assert not at.exception
    saved=at.session_state['runs'][-1]
    assert saved['success'] and not saved['scenario']['confined']
    assert saved['scenario']['aquifer_top']==25. and saved['scenario']['initial_head']==60.
    at.toggle(key='show_initial').set_value(False).run()
    assert len(at.session_state['runs']) == 1
    assert any('Run 01:' in c.value for c in at.caption)
    at.toggle(key='confined').set_value(True).run()
    assert at.number_input(key='thickness').value==30.
    at.toggle(key='confined').set_value(False).run()
    assert at.number_input(key='aquifer_top').value==25.
    at.selectbox(key='grid_count').set_value(10).run()
    at.text_input(key='grid_size_10').set_value('9501').run()
    at.selectbox(key='grid_count').set_value(3).run()
    assert len([w for w in at.text_input if w.key.startswith('grid_size_')])==3
    at.selectbox(key='grid_count').set_value(10).run()
    assert at.text_input(key='grid_size_10').value=='9501'
    at.text_input(key='grid_size_10').set_value('11').run()
    assert at.button(key='run_grid').disabled
    assert not at.exception
