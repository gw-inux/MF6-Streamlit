"""Independent numerical and workflow checks for the layered / 2-D extension."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   strict: line 31
#   independent_confined_solution: line 44
#   test_defaults_and_reproducible_fields: line 82
#   test_seconds_and_written_geometry: line 107
#   test_confined_models_against_independent_darcy_solution: line 138
#   test_unconfined_dry_layers_and_recharge_routing: line 151
#   test_sip_dry_start_failure_is_retained: line 167
#   test_invalid_complex_inputs_do_not_allocate_large_models: line 183
#   test_spacing_and_fixed_layer_geometry: line 188
#   test_plot_runtime_head_visibility_and_model_previews: line 200
#   test_ui_dimensions_latest_inspection_and_complex_grid_study: line 216
# END CODE CONTENTS

from dataclasses import replace
import numpy as np
import pytest
import flopy
import matplotlib.pyplot as plt

from MODFLOW_Solver_lab.core import Scenario, Solver, build_model, run_once, SECONDS_PER_YEAR
from MODFLOW_Solver_lab.plots import head_plot, model_preview
from MODFLOW_Solver_lab.settings import new_profile, solver_from_profile, parse_grid_spacings
from test_models import CHOICES, executable
from test_ui import app


def strict(engine, method):
    if engine == 'mf2005':
        p = dict(hclose=1e-7, mxiter=1000)
        if method == 'PCG':
            p.update(rclose=1e-11, iter1=1000)
    elif engine == 'mfnwt':
        p = dict(headtol=1e-7, fluxtol=1e-10, maxiterout=1000)
    else:
        p = dict(outer_dvclose=1e-7, inner_dvclose=1e-8,
                 rcloserecord=1e-10, outer_maximum=1000, inner_maximum=1000)
    return Solver(engine, method, 'COMPLEX', p)


def independent_confined_solution(s):
    """Dense Darcy-network solve, independent of FloPy and native budgets.

    Each face uses the harmonic mean of the two isotropic conductivities;
    recharge occurs only in the uppermost layer. Reservoirs are eliminated.
    """
    k = s.k_field()
    fixed = s.chd_mask()
    free = np.argwhere(~fixed)
    numbers = np.full(s.shape, -1, dtype=int)
    for i, cell in enumerate(free):
        numbers[tuple(cell)] = i
    matrix = np.zeros((len(free), len(free)))
    rhs = np.zeros(len(free))
    dz = (s.top-s.bottom)/s.nlay
    geometry = (s.dx*s.dy/dz, dz*s.dx/s.dy, dz*s.dy/s.dx)
    for i, cell in enumerate(free):
        loc = tuple(cell)
        if cell[0] == 0:
            rhs[i] += s.recharge_ms*s.dx*s.dy
        for axis in range(3):
            for direction in [-1, 1]:
                nb = cell.copy()
                nb[axis] += direction
                if not 0 <= nb[axis] < s.shape[axis]:
                    continue
                nb = tuple(nb)
                c = 2*k[loc]*k[nb]/(k[loc]+k[nb])*geometry[axis]
                matrix[i,i] += c
                if fixed[nb]:
                    rhs[i] += c*(s.left if nb[2] == 0 else s.right)
                else:
                    matrix[i,numbers[nb]] -= c
    h = s.starting_heads().reshape(s.shape)
    h[~fixed] = np.linalg.solve(matrix, rhs)
    return h


def test_defaults_and_reproducible_fields():
    s = Scenario()
    assert s.k_ms == 1e-4 and s.recharge_mmy == 150.
    assert s.recharge_ms == 0.150/SECONDS_PER_YEAR
    s = replace(s, complexity=True, horizontal_2d=True, nlay=3, random_k=True,
                initial='Random distribution', initial_min=25., initial_max=60.)
    k = s.k_field()
    assert k.shape == (3,11,11) and np.ptp(k) > 0
    assert k.min() >= s.k_min and k.max() <= s.k_max
    np.testing.assert_array_equal(k, s.k_field())
    fine = replace(s, n=101).k_field()
    np.testing.assert_allclose(k, fine[:,::10,::10], rtol=0, atol=0)
    assert not np.array_equal(k, replace(s,k_seed=43).k_field())
    h = s.starting_heads().reshape(s.shape)
    np.testing.assert_array_equal(h, s.starting_heads().reshape(s.shape))
    assert h[:,:,1:-1].min() >= 25. and h[:,:,1:-1].max() <= 60.
    assert (h[:,:,0] == s.left).all() and (h[:,:,-1] == s.right).all()
    assert s.comparison_group == replace(s,n=21).comparison_group
    assert s.comparison_group == replace(s,nlay=4).comparison_group
    assert not s.analytical_available
    with pytest.raises(ValueError,match='reference'):
        s.analytic()


@pytest.mark.parametrize('engine,method', CHOICES)
def test_seconds_and_written_geometry(engine,method,tmp_path):
    s = Scenario(n=7, complexity=True, horizontal_2d=True, nlay=3, random_k=True)
    build_model(s, strict(engine,method), tmp_path, executable(engine))
    if engine == 'mf6':
        sim = flopy.mf6.MFSimulation.load(sim_ws=tmp_path, verbosity_level=0)
        model = sim.get_model()
        assert sim.tdis.time_units.get_data().lower() == 'seconds'
        assert model.dis.nlay.get_data() == 3 and model.dis.nrow.get_data() == 7
        np.testing.assert_allclose(model.npf.k.array, s.k_field(), rtol=1e-14)
        np.testing.assert_allclose(model.npf.k33.array, s.k_field(), rtol=1e-14)
        recharge = model.rcha.recharge.array[0]
        records = model.chd.stress_period_data.get_data(0)
        assert len(records) == 2*7*3
    else:
        model = flopy.modflow.Modflow.load('flow.nam', model_ws=tmp_path, version=engine, check=False, verbose=False)
        assert model.dis.itmuni == 1 and model.nrow == 7 and model.nlay == 3
        flow = model.lpf if engine == 'mf2005' else model.upw
        np.testing.assert_allclose(flow.hk.array, s.k_field(), rtol=6e-8)
        np.testing.assert_allclose(flow.vka.array, s.k_field(), rtol=6e-8)
        recharge = model.rch.rech.array[0]
        assert len(model.chd.stress_period_data[0]) == 2*7*3
    np.testing.assert_allclose(recharge[...,1:-1], s.recharge_ms, rtol=6e-8)
    assert np.all(recharge[...,[0,-1]] == 0)


@pytest.mark.parametrize('engine,method', CHOICES)
@pytest.mark.parametrize('scenario', [Scenario(),
    Scenario(n=7,complexity=True,horizontal_2d=True),
    Scenario(n=7,complexity=True,nlay=3),
    Scenario(n=7,complexity=True,horizontal_2d=True,nlay=3,random_k=True,
             initial='Random distribution')])
def test_confined_models_against_independent_darcy_solution(engine,method,scenario,tmp_path):
    expected = independent_confined_solution(scenario)
    r = run_once(scenario,strict(engine,method),tmp_path,executable(engine))
    assert r['success'], r.get('read_error',r['stdout'][-1500:])
    np.testing.assert_allclose(np.array(r['heads']).reshape(scenario.shape), expected, rtol=0, atol=2e-5)
    assert r['metrics']['max_residual_m3s'] < 2e-8
    assert abs(r['metrics']['balance_m3s']) < 2e-7
    assert r['metrics']['boundary_error_m'] < 1e-9
    assert (r['metrics']['rmse_m'] is not None) == scenario.analytical_available


@pytest.mark.parametrize('engine,method', CHOICES)
@pytest.mark.parametrize('recharge', [0., 10.])
def test_unconfined_dry_layers_and_recharge_routing(engine,method,recharge,tmp_path):
    s = Scenario(n=7,complexity=True,horizontal_2d=True,nlay=5,confined=False,
                 left=8.,right=5.,recharge_mmy=recharge,initial='Specified uniform head',initial_head=20.)
    r = run_once(s,strict(engine,method),tmp_path,executable(engine))
    assert r['success'],r.get('read_error',r['stdout'][-1500:])
    assert r['metrics']['dry_cells'] > 0
    h = s.head_array(r['heads'])
    assert np.isfinite(h[:,:,1:-1]).any(axis=0).all()
    expected = s.recharge_ms*s.dx*s.dy*(s.n-2)*s.nrow
    assert r['metrics']['recharge_m3s'] == pytest.approx(expected,rel=1e-7,abs=1e-12)
    assert abs(r['metrics']['balance_m3s']) < 2e-7
    assert r['metrics']['max_residual_m3s'] < 2e-8
    assert r['metrics']['boundary_error_m'] < 1e-9
    assert r['metrics']['rmse_m'] is None


def test_sip_dry_start_failure_is_retained(tmp_path):
    # The tested SIP executable can lose hydraulic connectivity while rewetting.
    # A fully wet initial guess succeeds in the parameterized test above.
    s=Scenario(n=7,complexity=True,horizontal_2d=True,nlay=5,confined=False,
               left=8.,right=5.,recharge_mmy=10.,initial='Specified uniform head',initial_head=6.)
    r=run_once(s,strict('mf2005','SIP'),tmp_path,executable('mf2005'))
    if r['success']:  # A future executable may resolve the native limitation.
        assert abs(r['metrics']['balance_m3s']) < 2e-7
    else:
        assert r['status'] != 'Converged'
        assert 'DIVIDE BY 0 IN SIP' in r['listing'] or 'dry' in r.get('read_error','')


@pytest.mark.parametrize('kwargs', [dict(complexity=True,horizontal_2d=True,n=1001),
    dict(nlay=3), dict(complexity=True,nlay=51), dict(complexity=True,random_k=True,k_min=1.,k_max=.1),
    dict(initial='Random distribution',initial_min=30.,initial_max=20.), dict(k_seed=-1)])
def test_invalid_complex_inputs_do_not_allocate_large_models(kwargs):
    with pytest.raises(ValueError):
        Scenario(**kwargs).validate()


def test_spacing_and_fixed_layer_geometry():
    assert parse_grid_spacings(['500','250','50'],5000.) == [11,21,101]
    for entries in [['0'],['nan'],['inf'],['400'],['500','500'],['5001']]:
        with pytest.raises(ValueError):
            parse_grid_spacings(entries,5000.)
    s=Scenario(complexity=True,horizontal_2d=True,nlay=4)
    for count in parse_grid_spacings(['500','250','50'],s.length):
        refined=replace(s,n=count)
        assert refined.nlay == 4 and refined.dx == refined.dy
        assert refined.nrow == refined.n


def test_plot_runtime_head_visibility_and_model_previews():
    s=Scenario(complexity=True,horizontal_2d=True,nlay=3,random_k=True,
               initial='Specified uniform head',initial_head=5000.)
    cfg=solver_from_profile(new_profile('mf6','CG'))
    r=dict(heads=np.full(s.total_cells,18.).tolist(),success=True,status='Converged',
           wall_s=.1234,outer_iterations=2,inner_iterations=14)
    fig=head_plot(s,[r],initial=False,settings=cfg)
    assert fig.axes[0].get_ylim()[1] < 60.  # Full aquifer depth is now part of the section.
    assert any('Runtime = 0.1234 s' in txt.get_text() for txt in fig.axes[0].texts)
    for quantity in ['Hydraulic conductivity','Initial heads','Computed heads']:
        f=model_preview(s,quantity,heads=r['heads'] if quantity=='Computed heads' else None)
        f.canvas.draw()
        plt.close(f)
    plt.close(fig)


def test_ui_dimensions_latest_inspection_and_complex_grid_study():
    at=app()
    assert at.number_input(key='k').value == 1e-4
    assert at.number_input(key='recharge').value == 150.
    assert at.selectbox(key='repeats').value == 1
    for _ in range(2):
        at.button(key='run').click().run()
    assert at.selectbox(key='inspect_run').value == 2
    at.selectbox(key='inspect_run').set_value(1).run()
    at.button(key='run').click().run()
    assert at.selectbox(key='inspect_run').value == 3
    at.toggle(key='complexity').set_value(True).run()
    assert len(at.session_state['runs']) == 3
    at.toggle(key='horizontal_2d').set_value(True)
    at.toggle(key='add_layers').set_value(True)
    at.toggle(key='random_k').set_value(True).run()
    at.selectbox(key='initial').set_value('Random distribution').run()
    at.number_input(key='initial_min').set_value(12.)
    at.number_input(key='initial_max').set_value(45.)
    at.button(key='run').click().run()
    assert not at.exception
    result=at.session_state['runs'][-1]
    assert result['success'] and result['scenario']['nlay'] == 3
    assert result['scenario']['horizontal_2d'] and result['scenario']['initial_min'] == 12.
    assert at.toggle(key='analytical').disabled
    assert at.selectbox(key='grid_count_complex').value == 1
    assert at.multiselect(key='complex_grid_variants').value == ['mf2005/PCG']
    at.selectbox(key='grid_count_complex').set_value(2).run()
    fields=[w for w in at.text_input if w.key.startswith('spacing_entries_')]
    fields[1].set_value('250').run()
    at.button(key='run_grid').click().run()
    assert not at.exception
    study=at.session_state['studies'][-1]
    assert study['sizes'] == [11,21]
    assert all(r['Layers'] == 3 and r['Status'] == 'Converged' for r in study['rows'])
    assert at.selectbox(key='inspect_run').value == -study['study_id']
    assert len(at.session_state['runs']) == 1
    at.button(key='run').click().run()
    assert at.selectbox(key='inspect_run').value == at.session_state['runs'][-1]['run_id']
    at.number_input(key='layers').set_value(4).run()
    assert len(at.session_state['runs']) == 2 and at.session_state['diagnostic_extra'] is not None
    at.toggle(key='complexity').set_value(False).run()
    assert not at.exception and not at.toggle(key='analytical').disabled
