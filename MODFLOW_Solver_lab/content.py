"""Load editable Markdown without coupling text resources to Streamlit.

Long sections are ordinary Markdown documents in assets/md/en. Short interface
texts use named sections in ui_*.md. See CONTENT_GUIDE.md for editing, language
fallback and the deliberately inactive example for repository figures.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   English stays the default. A future language selector can pass a language: line 34
#   DEFAULT_LANGUAGE: line 36
#   MD_DIRECTORY: line 37
#   TEXT_FILES: line 38
#   LEARNING_TEXT_KEYS: line 47
#   SECTION_HEADER: line 57
#   ContentError: line 60
#   _language_directory: line 64
#   load_md: line 71
#   _sections: line 93
#   load_text: line 109
#   load_learning_text: line 126
#   These names keep the established presentation imports unchanged.: line 144
#   INTRODUCTION: line 147
#   ASSUMPTIONS: line 148
#   SOLVER_DETAILS: line 149
#   CONCLUSION: line 150
#   REFERENCES: line 151
#   TEXT: line 152
# END CODE CONTENTS

from pathlib import Path
import re

# EDIT: English stays the default. A future language selector can pass a language
# explicitly to load_md() and load_text(); no global session state is read here.
DEFAULT_LANGUAGE = "en"
MD_DIRECTORY = Path(__file__).resolve().parent / "assets" / "md"
TEXT_FILES = (
    "ui_shared.md",
    "ui_page.md",
    "ui_inputs.md",
    "ui_solver.md",
    "ui_results.md",
    "ui_study.md",
    "ui_experiments.md",
)
LEARNING_TEXT_KEYS = (
    "experiments_heading", "experiments_hint",
    "experiment_1_tab", "experiment_2_tab", "experiment_3_tab",
    "experiment_open_tab", "experiment_open_help", "experiment_document_hint",
    "experiment_unknown_document", "experiment_unavailable", "experiment_teacher_notes",
    "checklist_progress", "checklist_item_help",
    "assessment_preparation", "assessment_follow_up", "assessment_toggle_help",
    "assessment_help", "assessment_question_heading", "assessment_check_answer",
    "assessment_choose_answer", "assessment_unavailable",
)
SECTION_HEADER = re.compile(r"^## ([a-z][a-z0-9_]*)[ \t]*$", re.MULTILINE)


class ContentError(ValueError):
    """Missing or inconsistent editable text resources."""


def _language_directory(language):
    """Accept a language code, never a path; English is the fallback."""
    if not re.fullmatch(r"[a-z]{2,3}(?:-[A-Z]{2})?", language):
        raise ContentError(f"Invalid content language: {language!r}.")
    return MD_DIRECTORY / language


def load_md(filename, language=DEFAULT_LANGUAGE):
    """Read UTF-8 Markdown verbatim, falling back to English per document.

    Paths are relative to this module, not the shell's working directory.
    The explicit language argument also makes this safe for future per-session
    selection. Small files are read directly; no process-wide language cache is
    needed and edits are visible the next time this function is called.
    """
    if Path(filename).name != filename or not filename.endswith(".md"):
        raise ContentError(f"Expected a Markdown filename, received {filename!r}.")
    path = _language_directory(language) / filename
    if not path.is_file():
        path = MD_DIRECTORY / DEFAULT_LANGUAGE / filename
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ContentError(
            f"Cannot read Markdown resource {path.name}. "
            "Include the complete assets/md/en folder."
        ) from error


def _sections(markdown, filename):
    """Read `## stable_key` sections; leave their Markdown formatting intact."""
    headers = list(SECTION_HEADER.finditer(markdown))
    if not headers:
        raise ContentError(f"No text sections found in {filename}.")
    result = {}
    for index, header in enumerate(headers):
        key = header.group(1)
        end = headers[index + 1].start() if index + 1 < len(headers) else len(markdown)
        value = markdown[header.end() : end].strip("\r\n")
        if key in result or not value.strip():
            raise ContentError(f"Duplicate or empty text key {key!r} in {filename}.")
        result[key] = value
    return result


def load_text(language=DEFAULT_LANGUAGE, *, filenames=None):
    """Load short texts, optionally from an explicit bundle, with English fallback."""
    _language_directory(language)
    result = {}
    for filename in TEXT_FILES if filenames is None else filenames:
        entries = _sections(load_md(filename, DEFAULT_LANGUAGE), filename)
        if language != DEFAULT_LANGUAGE:
            translated = _language_directory(language) / filename
            if translated.is_file():
                entries.update(_sections(load_md(filename, language), filename))
        duplicate = result.keys() & entries.keys()
        if duplicate:
            raise ContentError(f"Repeated text keys in {filename}: {', '.join(sorted(duplicate))}.")
        result.update(entries)
    return result


def load_learning_text(language=DEFAULT_LANGUAGE):
    """Load learning labels directly, independently of the shared text-file list.

    Keep prose in Markdown. Validate the complete bundle before rendering so a
    partial upload gives an actionable resource message, not a redacted KeyError.
    """
    filename = "ui_experiments.md"
    entries = load_text(language, filenames=(filename,))
    missing = sorted(set(LEARNING_TEXT_KEYS) - entries.keys())
    if missing:
        raise ContentError(
            f"Missing text keys in {filename}: {', '.join(missing)}. "
            "Replace the complete MODFLOW_Solver_lab folder from the same ZIP, "
            "including assets/md/en, then reboot the app."
        )
    return entries


# EDIT: These names keep the established presentation imports unchanged.
# English is loaded once when the module is imported. A future language selector
# should call the two loaders during each Streamlit rerun, with its chosen code.
INTRODUCTION = load_md("introduction.md")
ASSUMPTIONS = load_md("equations.md")
SOLVER_DETAILS = load_md("solver_details.md")
CONCLUSION = load_md("conclusion.md")
REFERENCES = load_md("references.md")
TEXT = load_text()
