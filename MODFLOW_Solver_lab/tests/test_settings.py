"""Exercise UI-generated solver inputs with the native MODFLOW engines."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   PROFILES: line 18
#   test_ui_suggested_profiles_run_with_native_engines: line 24
#   test_nwt_basic_inner_edit_is_written_and_used: line 38
#   test_custom_grids_reject_invalid_counts: line 53
#   test_custom_grid_order_and_table_precision: line 58
#   test_mf6_expert_residual_option_and_damping_run: line 67
# END CODE CONTENTS

import pandas as pd
import pytest
from MODFLOW_Solver_lab.core import Scenario, find_executable, run_once
from MODFLOW_Solver_lab.settings import METHODS, new_profile, solver_from_profile, parse_grid_entries, formatted_csv

PROFILES = [(engine, method, preset) for engine, methods in METHODS.items() for method in methods
            for preset in (['SIMPLE'] if engine == 'mf2005' else ['SIMPLE','MODERATE','COMPLEX'])]


@pytest.mark.parametrize('engine,method,preset', PROFILES)
@pytest.mark.parametrize('expert', [False, True])
def test_ui_suggested_profiles_run_with_native_engines(engine, method, preset, expert, tmp_path):
    exe = find_executable(engine)
    if not exe:
        pytest.skip(f'{engine} executable required')
    profile = new_profile(engine, method, preset)
    profile['expert_enabled'] = expert
    cfg = solver_from_profile(profile)
    r = run_once(Scenario(), cfg, tmp_path, exe)
    assert r['success'], r['stdout'][-2000:]
    assert r['metrics']['max_error_m'] < .01
    assert abs(r['budget_percent']) < .01


@pytest.mark.parametrize('method,inner', [('GMRES','maxitinner'), ('XMD','mxiterxmd')])
def test_nwt_basic_inner_edit_is_written_and_used(method, inner, tmp_path):
    exe = find_executable('mfnwt')
    if not exe:
        pytest.skip('NWT executable required')
    profile = new_profile('mfnwt', method, 'MODERATE')
    profile['basic'][inner] = 17
    cfg = solver_from_profile(profile)
    r = run_once(Scenario(), cfg, tmp_path, exe)
    assert cfg.nwt_specified
    assert cfg.parameters()[inner] == 17
    assert 'SPECIFIED' in (tmp_path/'flow.nwt').read_text()
    assert r['success']


@pytest.mark.parametrize('extra', ['2', '10002', '11.5', '-11', 'abc'])
def test_custom_grids_reject_invalid_counts(extra):
    with pytest.raises(ValueError):
        parse_grid_entries(['11', extra])


def test_custom_grid_order_and_table_precision():
    assert parse_grid_entries(['101', ' 11 ', '17', '51']) == [101,11,17,51]
    frame = pd.DataFrame({'Run':[1], 'Process time (s)':[.1234567], 'RMSE (m)':[.000012346],
                          'Outer iterations':[2], 'Inner iterations':[None]})
    text = formatted_csv(frame)
    assert text.splitlines()[1] == '1,0.1235,1.235E-05,2,'


@pytest.mark.parametrize('residual_test', ['STRICT','L2NORM_RCLOSE'])
def test_mf6_expert_residual_option_and_damping_run(residual_test, tmp_path):
    exe = find_executable('mf6')
    if not exe:
        pytest.skip('MODFLOW 6 executable required')
    profile = new_profile('mf6','BICGSTAB','MODERATE')
    profile['expert_enabled'] = True
    profile['expert'].update(residual_test=residual_test, under_relaxation='SIMPLE',
                             under_relaxation_gamma=.7, inner_dvclose=1e-8,
                             scaling_method='L2NORM')
    profile['basic'].update(outer_dvclose=1e-8, rcloserecord=1e-10, outer_maximum=500)
    r = run_once(Scenario(n=101), solver_from_profile(profile), tmp_path, exe)
    assert r['success'], r['stdout'][-2000:]
    assert r['metrics']['max_error_m'] < 1e-6
    assert residual_test in (tmp_path/'lab.ims').read_text()
