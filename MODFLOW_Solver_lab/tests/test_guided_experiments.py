"""Guided reading tabs must leave the numerical app and its session intact."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   APP: line 29
#   ENTRYPOINTS: line 30
#   start_app: line 33
#   test_three_tabs_share_the_document_view_content: line 41
#   test_document_view_stops_before_model_initialization: line 62
#   test_document_route_only_accepts_listed_experiments: line 82
#   test_other_query_parameters_leave_normal_model_available: line 92
#   test_missing_experiment_has_a_readable_error_without_breaking_model: line 102
#   test_reading_view_does_not_change_an_existing_model_run: line 120
# END CODE CONTENTS

from copy import deepcopy
from pathlib import Path
import shutil
from urllib.parse import parse_qs, urlsplit

import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

from MODFLOW_Solver_lab import content, core
from MODFLOW_Solver_lab.checklists import ChecklistTask, parse_checklist
from MODFLOW_Solver_lab.experiments import EXPERIMENT_FILES, document_url

APP = Path(__file__).resolve().parents[1]
ENTRYPOINTS = [APP / "app.py", APP / "streamlit_app.py", APP.parent / "MODFLOW_Solver_lab.py"]


def start_app(entry=APP / "app.py", **query):
    app = AppTest.from_file(str(entry), default_timeout=60)
    app.query_params.update(query)
    app.run()
    assert not app.exception
    return app


def test_three_tabs_share_the_document_view_content():
    app = start_app()
    assert [tab.label for tab in app.tabs] == [
        content.TEXT[f"experiment_{number}_tab"] for number in range(1, 4)
    ]
    panel = next(item for item in app.expander if item.label == content.TEXT["experiments_heading"])
    assert not panel.proto.expanded
    links = app.get("link_button")
    assert len(links) == 3
    for tab, link, filename in zip(app.tabs, links, EXPERIMENT_FILES, strict=True):
        name = Path(filename).stem
        assert tab.markdown[0].value == content.load_md(f"{name}_overview.md").strip()
        blocks = parse_checklist(content.load_md(filename))
        tasks = [block for block in blocks if isinstance(block, ChecklistTask)]
        assert [item.label for item in tab.checkbox] == [task.label for task in tasks]
        assert link.proto.url == document_url(filename)
        assert link.proto.ignore_rerun


@pytest.mark.parametrize("filename", EXPERIMENT_FILES)
@pytest.mark.parametrize("entry", ENTRYPOINTS)
def test_document_view_stops_before_model_initialization(filename, entry, monkeypatch):
    def unexpected_engine_lookup(*args, **kwargs):
        pytest.fail("A document-only tab must not initialize a model.")

    monkeypatch.setattr(core, "find_executable", unexpected_engine_lookup)
    app = start_app(entry, view="md", doc=filename)
    assert not app.button and not app.number_input and not app.toggle
    assert not app.tabs and not app.error
    blocks = parse_checklist(content.load_md(filename))
    prose = [block.strip() for block in blocks if isinstance(block, str) and block.strip()]
    assert [item.value for item in app.markdown][-len(prose):] == prose
    assert len(app.checkbox) == sum(isinstance(block, ChecklistTask) for block in blocks)
    assert not app.get("link_button")
    rendered = "\n".join(item.value for item in app.markdown)
    assert "### Question 1" not in rendered and "# Teacher notes" not in rendered
    assert "runs" not in app.session_state
    assert "workdir" not in app.session_state


@pytest.mark.parametrize("filename", ["", "missing.md", "../core.py", "equations.md"])
def test_document_route_only_accepts_listed_experiments(filename):
    with pytest.raises(ValueError, match="Unknown experiment"):
        document_url(filename)
    app = start_app(view="md", doc=filename)
    assert len(app.error) == 1
    assert app.error[0].value == content.TEXT["experiment_unknown_document"]
    assert not app.button
    assert "workdir" not in app.session_state


def test_other_query_parameters_leave_normal_model_available():
    app = start_app(view="other", doc="experiment_01.md")
    assert app.button(key="run").label == "Run Model"
    for filename in EXPERIMENT_FILES:
        url = urlsplit(document_url(filename))
        assert not url.scheme and not url.netloc and not url.path
        assert parse_qs(url.query) == {"view": ["md"], "doc": [filename]}


@pytest.mark.parametrize("document_only", [False, True])
def test_missing_experiment_has_a_readable_error_without_breaking_model(
    tmp_path, monkeypatch, document_only
):
    md = tmp_path / "md"
    shutil.copytree(content.MD_DIRECTORY, md)
    (md / "en" / "experiment_02.md").unlink()
    monkeypatch.setattr(content, "MD_DIRECTORY", md)
    query = dict(view="md", doc="experiment_02.md") if document_only else {}
    app = start_app(**query)
    assert len(app.error) == 1
    assert "experiment_02.md" in app.error[0].value
    if document_only:
        assert not app.button
        assert "runs" not in app.session_state
    else:
        assert app.button(key="run").label == "Run Model"


def test_reading_view_does_not_change_an_existing_model_run():
    if not core.find_executable("mf2005"):
        pytest.skip("MODFLOW-2005 executable required")
    app = start_app()
    app.number_input(key="n").set_value(51)
    app.number_input(key="mf2005_PCG_SIMPLE_basic_hclose").set_value(2e-5)
    app.text_input(key="run_name").set_value("Keep my model")
    app.button(key="run").click().run()
    assert not app.exception
    saved = deepcopy(app.session_state["runs"])
    assert len(saved) == 1 and saved[0]["success"]
    workspace = app.session_state["workdir"].name
    for filename in EXPERIMENT_FILES:
        reader = start_app(view="md", doc=filename)
        assert not reader.error and "workdir" not in reader.session_state
    app.run()
    assert not app.exception
    assert app.number_input(key="n").value == 51
    assert app.number_input(key="mf2005_PCG_SIMPLE_basic_hclose").value == 2e-5
    assert app.text_input(key="run_name").value == "Keep my model"
    assert app.session_state["workdir"].name == workspace
    current = app.session_state["runs"]
    assert len(current) == 1 and current[0]["run_name"] == saved[0]["run_name"]
    assert current[0]["scenario"] == saved[0]["scenario"]
    assert current[0]["wall_s"] == saved[0]["wall_s"]
    np.testing.assert_array_equal(current[0]["heads"], saved[0]["heads"])
