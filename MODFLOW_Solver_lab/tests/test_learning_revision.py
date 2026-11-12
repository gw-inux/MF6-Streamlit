"""iNUX grading, editable content, checklists and independent learning state."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   APP: line 40
#   BANKS: line 41
#   EXAMPLE: line 43
#   start_app: line 47
#   select_answer: line 53
#   test_banks_use_the_existing_inux_schema_and_markdown: line 63
#   test_all_reviewed_questions_require_the_complete_correct_selection: line 74
#   test_invalid_question_banks_fail_clearly: line 96
#   test_duplicate_option_text_is_not_silently_overwritten: line 101
#   test_assessment_paths_are_confined_to_language_resources: line 117
#   test_assessment_translation_fallback_and_manual_edits: line 122
#   test_instruction_files_have_stable_checks_and_no_embedded_assessments: line 139
#   test_checklist_parser_retains_equations_tables_and_fenced_examples: line 151
#   test_invalid_checklist_ids_fail_clearly: line 166
#   test_question_blocks_feedback_and_choices_survive_collapsing_and_model_edits: line 171
#   test_progress_and_assessments_do_not_change_a_saved_native_run: line 198
#   test_missing_assessment_is_scoped_to_its_panel: line 229
# END CODE CONTENTS

from copy import deepcopy
import json
from pathlib import Path
import shutil

import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

from MODFLOW_Solver_lab import assessments, content, core
from MODFLOW_Solver_lab.assessments import (
    evaluate_answer, load_questions, question_signature, validate_questions,
)
from MODFLOW_Solver_lab.checklists import ChecklistTask, parse_checklist


APP = Path(__file__).resolve().parents[1]
BANKS = [f"experiment_{number:02d}_{phase}.json"
         for number in range(1, 4) for phase in ("pre", "post")]
EXAMPLE = dict(question="Select **all** correct answers.",
               options={"One": True, "Two": False}, success="Correct: **one**.", error="Try again.")


def start_app():
    app = AppTest.from_file(str(APP / "app.py"), default_timeout=60).run()
    assert not app.exception
    return app


def select_answer(app, namespace, number, selections):
    question = load_questions(namespace + ".json")[number - 1]
    identity = f"{namespace}_q{number}"
    signature = question_signature(question)
    for index, selected in enumerate(selections):
        app.checkbox(key=f"learning_answer_{identity}_{signature}_{index}").set_value(selected)
    return identity


@pytest.mark.parametrize("filename", BANKS)
def test_banks_use_the_existing_inux_schema_and_markdown(filename):
    bank = load_questions(filename)
    assert len(bank) == 6
    assert all(set(question) == {"question", "options", "success", "error"} for question in bank)
    assert bank == json.loads((assessments.QUESTIONS_DIRECTORY / "en" / filename).read_text())
    assert "<details>" not in json.dumps(bank)
    assert all("Correct-selection feedback" not in question["success"] for question in bank)


@pytest.mark.parametrize("filename", BANKS)
@pytest.mark.parametrize("number", range(6))
def test_all_reviewed_questions_require_the_complete_correct_selection(filename, number):
    question = load_questions(filename)[number]
    expected = list(question["options"].values())
    assert evaluate_answer(question["options"], expected) == "correct"
    assert evaluate_answer(question["options"], [False] * len(expected)) == "empty"
    omitted = expected.copy()
    omitted[omitted.index(True)] = False
    assert evaluate_answer(question["options"], omitted) != "correct"
    if False in expected:
        extra = expected.copy()
        extra[extra.index(False)] = True
        assert evaluate_answer(question["options"], extra) == "incorrect"


@pytest.mark.parametrize("invalid", [
    [], {}, [None], [{"question": "Missing fields"}],
    [dict(EXAMPLE, options={"Only": True})],
    [dict(EXAMPLE, options={"One": "true", "Two": False})],
    [dict(EXAMPLE, options={"One": 1, "Two": False})],
    [dict(EXAMPLE, options={"One": False, "Two": False})],
    [dict(EXAMPLE, success="")], [dict(EXAMPLE, error=None)],
])
def test_invalid_question_banks_fail_clearly(invalid):
    with pytest.raises(content.ContentError):
        validate_questions(invalid)


def test_duplicate_option_text_is_not_silently_overwritten(tmp_path, monkeypatch):
    directory = tmp_path / "en"
    directory.mkdir()
    (directory / "bad.json").write_text(
        '[{"question":"Q", "options":{"Same":true,"Same":false},"success":"Yes","error":"No"}]'
    )
    monkeypatch.setattr(assessments, "QUESTIONS_DIRECTORY", tmp_path)
    with pytest.raises(content.ContentError, match="Repeated assessment"):
        load_questions("bad.json")


@pytest.mark.parametrize("filename,language", [
    ("../outside.json", "en"), ("/tmp/elsewhere.json", "en"),
    ("experiment_01_pre.json", "../en"), ("experiment_01_pre.json", "de/extra"),
    ("experiment_01_pre.txt", "en"),
])
def test_assessment_paths_are_confined_to_language_resources(filename, language):
    with pytest.raises(content.ContentError):
        load_questions(filename, language)


def test_assessment_translation_fallback_and_manual_edits(tmp_path, monkeypatch):
    shutil.copytree(assessments.QUESTIONS_DIRECTORY, tmp_path / "questions")
    monkeypatch.setattr(assessments, "QUESTIONS_DIRECTORY", tmp_path / "questions")
    german = tmp_path / "questions/de"
    german.mkdir()
    translated = [dict(EXAMPLE, question="Wählen Sie **alle** richtigen Antworten.", success="**Richtig.**")]
    path = german / "experiment_01_pre.json"
    path.write_text(json.dumps(translated, ensure_ascii=False))
    assert load_questions(path.name, "de") == translated
    assert load_questions("experiment_02_pre.json", "de") == load_questions("experiment_02_pre.json", "en")
    assert load_questions(path.name, "en") != translated
    translated[0]["question"] = "Geänderte Frage."
    path.write_text(json.dumps(translated))
    assert load_questions(path.name, "de")[0]["question"] == "Geänderte Frage."


@pytest.mark.parametrize("number,count", [(1, 8), (2, 7), (3, 9)])
def test_instruction_files_have_stable_checks_and_no_embedded_assessments(number, count):
    instructions = content.load_md(f"experiment_{number:02d}.md")
    tasks = [block for block in parse_checklist(instructions) if isinstance(block, ChecklistTask)]
    assert len(tasks) == count
    assert all(not task.initial for task in tasks)
    assert len({task.identifier for task in tasks}) == count
    assert "### Question 1" not in instructions
    assert "Correct-selection feedback" not in instructions
    assert "# Teacher notes" not in instructions
    assert "Practical investigation" in instructions and "Optional exercise" in instructions


def test_checklist_parser_retains_equations_tables_and_fenced_examples():
    prose = "## Step\n\n$x^2$\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n"
    fenced = "```markdown\n- [ ] This is an example, not a widget.\n```\n"
    document = prose + "- [ ] **Done** <!-- task: first -->\n\n" + fenced
    blocks = parse_checklist(document)
    assert blocks[0] == prose
    assert blocks[1] == ChecklistTask("first", "**Done**", False)
    assert blocks[2] == "\n" + fenced
    assert parse_checklist("- [x] Déjà fait <!-- task: first -->\n")[0].initial


@pytest.mark.parametrize("document", [
    "- [ ] A checkbox without a stable ID\n",
    "- [ ] First <!-- task: same -->\n- [ ] Second <!-- task: same -->\n",
])
def test_invalid_checklist_ids_fail_clearly(document):
    with pytest.raises(content.ContentError):
        parse_checklist(document)


def test_question_blocks_feedback_and_choices_survive_collapsing_and_model_edits():
    app = start_app()
    namespace = "experiment_01_pre"
    app.button(key=f"learning_toggle_{namespace}").click().run()
    question = load_questions(namespace + ".json")[0]
    identity = f"{namespace}_q1"
    check_key = f"learning_check_answer_{identity}"
    app.button(key=check_key).click().run()
    assert any(message.value == content.TEXT["assessment_choose_answer"] for message in app.info)
    select_answer(app, namespace, 1, list(question["options"].values()))
    app.button(key=check_key).click().run()
    assert not app.exception and app.success[0].value == question["success"]
    app.button(key=f"learning_chevron_{namespace}").click().run()
    assert not app.success
    app.number_input(key="n").set_value(51).run()
    app.button(key=f"learning_toggle_{namespace}").click().run()
    assert app.success[0].value == question["success"]
    selections = list(question["options"].values())
    selections[selections.index(False)] = True
    select_answer(app, namespace, 1, selections)
    app.run()
    assert not app.success  # Feedback disappears as soon as the answer changes.
    app.button(key=check_key).click().run()
    assert app.error[0].value == question["error"]
    assert app.number_input(key="n").value == 51


def test_progress_and_assessments_do_not_change_a_saved_native_run():
    if not core.find_executable("mf2005"):
        pytest.skip("MODFLOW-2005 executable required")
    app = start_app()
    app.number_input(key="n").set_value(51)
    app.text_input(key="run_name").set_value("Preserve while learning")
    app.button(key="run").click().run()
    assert not app.exception
    saved = deepcopy(app.session_state["runs"][-1])
    assert saved["success"]
    workspace = app.session_state["workdir"].name
    for number in range(1, 4):
        key = f"learning_check_experiment_{number:02d}_step_01"
        app.checkbox(key=key).set_value(True).run()
    namespace = "experiment_03_post"
    app.button(key=f"learning_toggle_{namespace}").click().run()
    question = load_questions(namespace + ".json")[0]
    identity = select_answer(app, namespace, 1, list(question["options"].values()))
    app.button(key=f"learning_check_answer_{identity}").click().run()
    assert not app.exception and app.success
    assert app.session_state["workdir"].name == workspace
    assert len(app.session_state["runs"]) == 1
    current = app.session_state["runs"][0]
    assert current["scenario"] == saved["scenario"]
    assert current["wall_s"] == saved["wall_s"]
    assert current["run_name"] == saved["run_name"]
    np.testing.assert_array_equal(current["heads"], saved["heads"])
    for number in range(1, 4):
        assert app.session_state["learning_checklists"][f"experiment_{number:02d}"]["step_01"]


def test_missing_assessment_is_scoped_to_its_panel(tmp_path, monkeypatch):
    shutil.copytree(assessments.QUESTIONS_DIRECTORY, tmp_path / "questions")
    (tmp_path / "questions/en/experiment_02_pre.json").unlink()
    monkeypatch.setattr(assessments, "QUESTIONS_DIRECTORY", tmp_path / "questions")
    app = start_app()
    assert not app.error
    app.button(key="learning_toggle_experiment_02_pre").click().run()
    assert not app.exception and len(app.error) == 1
    assert "experiment_02_pre.json" in app.error[0].value
    assert app.button(key="run").label == "Run Model"
