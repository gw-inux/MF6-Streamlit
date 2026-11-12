"""Prevent the online experiments_heading failure with mixed text registrations."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   APP: line 21
#   ENTRIES: line 22
#   test_learning_views_load_their_own_markdown_with_an_older_registry: line 27
#   test_missing_learning_key_is_actionable_and_does_not_raise_keyerror: line 53
#   test_old_content_module_has_a_clear_startup_message: line 71
#   test_learning_labels_keep_markdown_translation_fallback_and_manual_edits: line 79
# END CODE CONTENTS

from pathlib import Path
import shutil

import pytest
from streamlit.testing.v1 import AppTest

from MODFLOW_Solver_lab import content

APP=Path(__file__).resolve().parents[1]
ENTRIES=(APP/'app.py',APP/'streamlit_app.py',APP.parent/'MODFLOW_Solver_lab.py')


@pytest.mark.parametrize('entry',ENTRIES)
@pytest.mark.parametrize('number',[0,1,2,3])
def test_learning_views_load_their_own_markdown_with_an_older_registry(entry,number,monkeypatch):
    monkeypatch.setattr(content,'TEXT_FILES',tuple(name for name in content.TEXT_FILES if name!='ui_experiments.md'))
    assert 'experiments_heading' not in content.load_text()
    app=AppTest.from_file(str(entry),default_timeout=60)
    if number:
        app.query_params.update(view='md',doc=f'experiment_{number:02d}.md')
    app.run()
    assert not app.exception and not app.error
    if number:
        assert len(app.checkbox)==(8,7,9)[number-1]
        assert not app.button and 'workdir' not in app.session_state
        app.checkbox[0].check().run()
        assert app.checkbox[0].value
    else:
        assert len(app.tabs)==3
        app.button(key='learning_toggle_experiment_01_pre').click().run()
        app.button(key='learning_check_answer_experiment_01_pre_q1').click().run()
        assert any(item.value==content.load_learning_text()['assessment_choose_answer'] for item in app.info)
        app.checkbox(key='learning_check_experiment_01_step_01').check().run()
        assert app.checkbox(key='learning_check_experiment_01_step_01').value
        assert app.button(key='run').label=='Run Model'
    assert not app.exception


@pytest.mark.parametrize('missing_key',['experiments_heading','assessment_help','checklist_progress'])
@pytest.mark.parametrize('reader',[False,True])
def test_missing_learning_key_is_actionable_and_does_not_raise_keyerror(tmp_path,monkeypatch,missing_key,reader):
    folder=tmp_path/'md';shutil.copytree(content.MD_DIRECTORY,folder)
    path=folder/'en/ui_experiments.md'
    text=path.read_text().replace('## '+missing_key+'\n','## renamed_'+missing_key+'\n')
    path.write_text(text)
    monkeypatch.setattr(content,'MD_DIRECTORY',folder)
    app=AppTest.from_file(str(APP/'app.py'),default_timeout=60)
    if reader:app.query_params.update(view='md',doc='experiment_01.md')
    app.run()
    assert not app.exception and len(app.error)==1
    assert missing_key in app.error[0].value and 'ui_experiments.md' in app.error[0].value
    assert 'complete MODFLOW_Solver_lab folder' in app.error[0].value
    if reader:
        assert 'workdir' not in app.session_state and not app.button
    else:
        assert app.button(key='run').label=='Run Model'


def test_old_content_module_has_a_clear_startup_message(monkeypatch):
    monkeypatch.delattr(content,'load_learning_text')
    app=AppTest.from_file(str(APP/'app.py'),default_timeout=60).run()
    assert not app.exception and len(app.error)==1
    assert 'load_learning_text' in app.error[0].value
    assert 'different releases' in app.error[0].value


def test_learning_labels_keep_markdown_translation_fallback_and_manual_edits(tmp_path,monkeypatch):
    folder=tmp_path/'md';shutil.copytree(content.MD_DIRECTORY,folder)
    (folder/'de').mkdir()
    (folder/'de/ui_experiments.md').write_text('## experiments_heading\n\n**Angeleitete Experimente**\n',encoding='utf-8')
    monkeypatch.setattr(content,'MD_DIRECTORY',folder)
    german=content.load_learning_text('de')
    assert german['experiments_heading']=='**Angeleitete Experimente**'
    assert german['assessment_help']==content.load_learning_text('en')['assessment_help']
    path=folder/'en/ui_experiments.md'
    path.write_text(path.read_text().replace('**Guided experiments**','**My edited experiments**'))
    assert content.load_learning_text()['experiments_heading']=='**My edited experiments**'
    assert content.load_learning_text('de')['experiments_heading']=='**Angeleitete Experimente**'
