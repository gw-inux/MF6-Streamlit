"""Execute grid-study plans, including exclusions, custom grids and repeats."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   test_grid_studies_use_saved_settings_and_exclude_unselected_variants: line 13
# END CODE CONTENTS

import pytest
from MODFLOW_Solver_lab.core import find_executable
from test_ui import app


def test_grid_studies_use_saved_settings_and_exclude_unselected_variants():
    if not all(find_executable(e) for e in ('mf2005', 'mfnwt', 'mf6')):
        pytest.skip('All three engines required')
    at = app()
    at.selectbox(key='repeats').set_value(1)
    at.selectbox(key='grid_count').set_value(1).run()
    at.button(key='run_grid').click().run()
    assert not at.exception
    first = at.session_state['studies'][0]
    assert len(first['rows']) == 6
    assert all(r['Status'] == 'Converged' for r in first['rows'])
    assert not at.session_state['runs']
    at.number_input(key='mf2005_PCG_SIMPLE_basic_hclose').set_value(2e-6).run()
    at.selectbox(key='engine').set_value('mf6').run()
    at.selectbox(key='preset_mf6').set_value('COMPLEX').run()
    at.selectbox(key='method_mf6').set_value('BICGSTAB').run()
    at.number_input(key='mf6_BICGSTAB_COMPLEX_basic_outer_dvclose').set_value(1e-7).run()
    at.multiselect(key='grid_variants').set_value(['mf2005/PCG', 'mf6/BICGSTAB'])
    at.selectbox(key='grid_count').set_value(3).run()
    at.text_input(key='grid_size_1').set_value('11')
    at.text_input(key='grid_size_2').set_value('17')
    at.text_input(key='grid_size_3').set_value('51')
    at.selectbox(key='repeats').set_value(2)
    at.text_input(key='study_name').set_value('Modified study').run()
    assert not at.exception
    at.button(key='run_grid').click().run()
    assert not at.exception
    saved = at.session_state['studies'][-1]
    assert saved['name'] == 'Modified study' and saved['sizes'] == [11,17,51]
    assert len(saved['rows']) == 6 and saved['repeats'] == 2
    assert set(saved['plan']) == {'mf2005/PCG', 'mf6/BICGSTAB'}
    assert saved['plan']['mf2005/PCG']['overrides']['hclose'] == 2e-6
    assert saved['plan']['mf6/BICGSTAB']['overrides']['outer_dvclose'] == 1e-7
    assert all(r['Status'] == 'Converged' and r['Repeats'] == 2 for r in saved['rows'])
    assert first['plan']['mf2005/PCG']['overrides']['hclose'] == 1e-4
    at.text_input(key='grid_size_3').set_value('2, invalid').run()
    assert at.button(key='run_grid').disabled
    at.text_input(key='grid_size_3').set_value('51')
    at.multiselect(key='grid_variants').set_value([]).run()
    assert at.button(key='run_grid').disabled
    assert not at.exception
