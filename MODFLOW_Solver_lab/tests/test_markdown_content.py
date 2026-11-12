"""Editable Markdown: independent paths, language fallback and clear failures."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   editable_content: line 26
#   test_content_loading_is_independent_of_working_directory: line 33
#   test_partial_translation_falls_back_per_document_and_text_key: line 41
#   test_unknown_language_has_complete_english_fallback: line 58
#   test_manual_edits_are_read_on_the_next_load: line 63
#   test_missing_required_markdown_has_a_clear_error: line 69
#   test_invalid_snippet_documents_fail_clearly: line 83
#   test_duplicate_keys_across_files_are_rejected: line 88
#   test_language_argument_is_a_code_not_a_path: line 96
#   test_every_interface_key_is_used_and_every_reference_exists: line 101
# END CODE CONTENTS

from pathlib import Path
import re
import shutil

import pytest
from MODFLOW_Solver_lab import content


@pytest.fixture
def editable_content(tmp_path, monkeypatch):
    directory = tmp_path / "md"
    shutil.copytree(content.MD_DIRECTORY, directory)
    monkeypatch.setattr(content, "MD_DIRECTORY", directory)
    return directory


def test_content_loading_is_independent_of_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert content.load_md("equations.md") == content.ASSUMPTIONS
    assert r"\frac{d}{dx}" in content.ASSUMPTIONS
    assert "Δx" in content.TEXT["model_summary"]
    assert content.load_text() == content.TEXT


def test_partial_translation_falls_back_per_document_and_text_key(editable_content):
    german = editable_content / "de"
    german.mkdir()
    (german / "introduction.md").write_text(
        "# Einführung\n\nGrundwasserströmung.\n", encoding="utf-8"
    )
    (german / "ui_shared.md").write_text(
        "## execution_heading\n\nModellberechnung\n", encoding="utf-8"
    )
    assert content.load_md("introduction.md", "de").startswith("# Einführung")
    assert content.load_md("equations.md", "de") == content.ASSUMPTIONS
    translated = content.load_text("de")
    assert translated["execution_heading"] == "Modellberechnung"
    assert translated["repeat_help"] == content.TEXT["repeat_help"]
    assert content.load_text("en") == content.TEXT  # no cross-language cache


def test_unknown_language_has_complete_english_fallback():
    assert content.load_text("fr") == content.TEXT
    assert content.load_md("introduction.md", "fr") == content.INTRODUCTION


def test_manual_edits_are_read_on_the_next_load(editable_content):
    path = editable_content / "en" / "introduction.md"
    path.write_text("An edited introduction.\n", encoding="utf-8")
    assert content.load_md("introduction.md") == "An edited introduction.\n"


def test_missing_required_markdown_has_a_clear_error(editable_content):
    (editable_content / "en" / "equations.md").unlink()
    with pytest.raises(content.ContentError, match="equations.md.*assets/md/en"):
        content.load_md("equations.md")


@pytest.mark.parametrize(
    "document",
    [
        "## repeated\nFirst\n## repeated\nSecond\n",
        "## empty\n\n",
        "No named text sections.\n",
    ],
)
def test_invalid_snippet_documents_fail_clearly(document):
    with pytest.raises(content.ContentError):
        content._sections(document, "example.md")


def test_duplicate_keys_across_files_are_rejected(editable_content):
    with (editable_content / "en" / "ui_page.md").open("a", encoding="utf-8") as stream:
        stream.write("\n## execution_heading\nDuplicate\n")
    with pytest.raises(content.ContentError, match="Repeated text keys"):
        content.load_text()


@pytest.mark.parametrize("language", ["../en", "de/extra", "/tmp", ""])
def test_language_argument_is_a_code_not_a_path(language):
    with pytest.raises(content.ContentError, match="Invalid content language"):
        content.load_md("introduction.md", language)


def test_every_interface_key_is_used_and_every_reference_exists():
    app = Path(__file__).resolve().parents[1]
    used = set()
    for path in app.glob("*.py"):
        used.update(re.findall(r'TEXT\["([a-z][a-z0-9_]*)"\]', path.read_text(encoding="utf-8")))
    assert used == set(content.TEXT)
