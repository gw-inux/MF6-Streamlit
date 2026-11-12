"""Deployment regression: unrelated cached modules must never enter this app."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   APP: line 19
#   test_all_entrypoints_ignore_and_preserve_foreign_modules: line 23
#   test_partial_content_update_has_readable_message_and_cannot_run: line 43
#   test_missing_package_marker_has_readable_message: line 53
# END CODE CONTENTS

from pathlib import Path
import shutil
import sys
import types
import pytest
from streamlit.testing.v1 import AppTest
from MODFLOW_Solver_lab import content

APP = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('entry', [APP/'app.py', APP/'streamlit_app.py', APP.parent/'MODFLOW_Solver_lab.py'])
def test_all_entrypoints_ignore_and_preserve_foreign_modules(entry, monkeypatch):
    foreign = {}
    for name in ('content','core','settings','controls','plots','inputs','results','studies',
                 'ui','surfaces','spacing','diagnostic_guides','map_rendering'):
        module = types.ModuleType(name)
        module.__file__ = '/another_app/'+name+'.py'
        foreign[name] = module
        monkeypatch.setitem(sys.modules, name, module)
    at = AppTest.from_file(str(entry), default_timeout=45).run()
    assert not at.exception
    assert at.button(key='run').label == 'Run Model'
    assert 'Developed by Thomas Reimann' in at.caption[-1].value
    at.run()
    assert not at.exception
    for name,module in foreign.items():
        assert sys.modules[name] is module
    own = sys.modules['MODFLOW_Solver_lab.content']
    assert Path(own.__file__).resolve() == APP/'content.py'


def test_partial_content_update_has_readable_message_and_cannot_run(monkeypatch):
    monkeypatch.delattr(content, 'CONCLUSION')
    at = AppTest.from_file(str(APP/'app.py'), default_timeout=45).run()
    assert not at.exception
    assert len(at.error) == 1
    assert 'content.py is missing: CONCLUSION' in at.error[0].value
    assert 'Replace the complete MODFLOW_Solver_lab folder' in at.error[0].value
    assert not at.button


def test_missing_package_marker_has_readable_message(tmp_path):
    entry = tmp_path/'streamlit_app.py'
    shutil.copy2(APP/'streamlit_app.py',entry)
    at = AppTest.from_file(str(entry), default_timeout=45).run()
    assert not at.exception
    assert '__init__.py is missing' in at.error[0].value
    assert not at.button
