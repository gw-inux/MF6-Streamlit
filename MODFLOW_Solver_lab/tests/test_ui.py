"""Real Streamlit interactions: solver controls, retained settings and run book."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   app: line 16
#   test_solver_switching_presets_and_expert_controls: line 24
#   test_named_runs_cap_deletion_stale_plot_and_failed_run: line 65
# END CODE CONTENTS

from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest
from MODFLOW_Solver_lab.core import Solver, find_executable


def app():
    at = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'), default_timeout=90).run()
    assert not at.exception
    at.toggle(key="full_settings").set_value(True).run()
    assert not at.exception
    return at


def test_solver_switching_presets_and_expert_controls():
    at = app()
    assert at.number_input(key='n').value == 11
    at.number_input(key='mf2005_PCG_SIMPLE_basic_hclose').set_value(2e-6)
    at.number_input(key='mf2005_PCG_SIMPLE_basic_relax').set_value(.85)
    at.toggle(key='mf2005_PCG_SIMPLE_expert_on').set_value(True).run()
    at.selectbox(key='mf2005_PCG_SIMPLE_expert_npcond').set_value(2).run()
    at.selectbox(key='engine').set_value('mf6').run()
    at.selectbox(key='preset_mf6').set_value('MODERATE').run()
    assert at.selectbox(key='method_mf6').value == 'CG'
    at.selectbox(key='method_mf6').set_value('BICGSTAB').run()
    assert at.number_input(key='mf6_BICGSTAB_MODERATE_basic_outer_dvclose').value == 1e-4
    at.number_input(key='mf6_BICGSTAB_MODERATE_basic_outer_dvclose').set_value(1e-6).run()
    cfg = Solver(**at.session_state['variants']['mf6/BICGSTAB'])
    assert cfg.parameters()['inner_dvclose'] == 1e-6
    at.toggle(key='mf6_BICGSTAB_MODERATE_expert_on').set_value(True).run()
    at.number_input(key='mf6_BICGSTAB_MODERATE_expert_inner_dvclose').set_value(2e-7)
    at.selectbox(key='mf6_BICGSTAB_MODERATE_expert_residual_test').set_value('STRICT').run()
    cfg = Solver(**at.session_state['variants']['mf6/BICGSTAB'])
    assert cfg.parameters()['inner_dvclose'] == 2e-7
    assert cfg.parameters()['rcloserecord'] == [1e-4, 'STRICT']
    at.selectbox(key='engine').set_value('mfnwt').run()
    at.selectbox(key='preset_mfnwt').set_value('COMPLEX').run()
    at.selectbox(key='method_mfnwt').set_value('XMD').run()
    key = 'mfnwt_XMD_COMPLEX_basic_mxiterxmd'
    at.number_input(key=key).set_value(at.number_input(key=key).value+1).run()
    cfg = Solver(**at.session_state['variants']['mfnwt/XMD'])
    assert cfg.nwt_specified and cfg.parameters()['options'] == 'SPECIFIED'
    at.toggle(key='mfnwt_XMD_COMPLEX_expert_on').set_value(True).run()
    assert not at.exception
    at.selectbox(key='engine').set_value('mf2005').run()
    assert at.number_input(key='mf2005_PCG_SIMPLE_basic_hclose').value == 2e-6
    assert at.number_input(key='mf2005_PCG_SIMPLE_basic_relax').value == .85
    assert at.toggle(key='mf2005_PCG_SIMPLE_expert_on').value
    assert at.selectbox(key='mf2005_PCG_SIMPLE_expert_npcond').value == 2
    at.selectbox(key='engine').set_value('mf6').run()
    assert at.selectbox(key='preset_mf6').value == 'MODERATE'
    assert at.number_input(key='mf6_BICGSTAB_MODERATE_expert_inner_dvclose').value == 2e-7
    assert not at.exception


def test_named_runs_cap_deletion_stale_plot_and_failed_run():
    if not find_executable('mf2005'):
        pytest.skip('MODFLOW-2005 executable required')
    at = app()
    at.selectbox(key='repeats').set_value(1).run()
    for i in range(11):
        at.text_input(key='run_name').set_value(f'Trial {i+1}')
        at.button(key='run').click().run()
        assert not at.exception
        if i == 0:
            at.selectbox(key='inspect_run').set_value(1).run()
    runs = at.session_state['runs']
    assert len(runs) == 10
    assert [r['run_id'] for r in runs] == list(range(2, 12))
    assert all(r['success'] for r in runs)
    assert runs[-1]['run_name'] == 'Trial 11'
    at.toggle(key='analytical').set_value(False).run()
    assert any('Run 11:' in c.value for c in at.caption)
    at.number_input(key='n').set_value(101).run()
    assert any('Inputs have changed' in c.value for c in at.caption)
    assert at.session_state['runs'][-1]['scenario']['n'] == 11
    at.selectbox(key='inspect_run').set_value(2).run()
    at.multiselect(key='delete_selection').set_value([2, 7]).run()
    at.button(key='remove_runs').click().run()
    assert not at.exception
    assert [r['run_id'] for r in at.session_state['runs']] == [3,4,5,6,8,9,10,11]
    at.number_input(key='mf2005_PCG_SIMPLE_basic_mxiter').set_value(1)
    at.number_input(key='mf2005_PCG_SIMPLE_basic_iter1').set_value(1)
    at.text_input(key='run_name').set_value('   ')
    at.button(key='run').click().run()
    assert not at.exception
    failed = at.session_state['runs'][-1]
    assert not failed['success']
    assert failed['run_name'].endswith('run 12')
    ids = [r['run_id'] for r in at.session_state['runs']]
    at.multiselect(key='delete_selection').set_value(ids).run()
    at.button(key='remove_runs').click().run()
    assert not at.exception and not at.session_state['runs']
