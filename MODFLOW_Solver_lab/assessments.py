"""Standard iNUX question banks and reusable, state-preserving question blocks.

JSON uses the established Soil Water Retention schema: question, options
(Markdown text -> Boolean), success and error. All prose stays in content
resources. This module neither imports nor modifies the model implementation.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   QUESTIONS_DIRECTORY: line 33
#   QUESTION_FIELDS: line 34
#   ANSWERS_KEY: line 35
#   unique_object: line 38
#   validate_questions: line 48
#   load_questions: line 69
#   evaluate_answer: line 86
#   question_signature: line 97
#   remember_option: line 102
#   toggle_assessment: line 109
#   render_question: line 113
#   render_assessment: line 141
# END CODE CONTENTS

import hashlib
import json
from pathlib import Path

import streamlit as st

from .content import ContentError, DEFAULT_LANGUAGE, _language_directory, load_text


QUESTIONS_DIRECTORY = Path(__file__).resolve().parent / "assets" / "questions"
QUESTION_FIELDS = {"question", "options", "success", "error"}
ANSWERS_KEY = "learning_assessments"


def unique_object(pairs):
    """Reject duplicate JSON fields or option texts rather than lose an answer."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContentError(f"Repeated assessment field or option: {key!r}.")
        result[key] = value
    return result


def validate_questions(questions):
    """Check the usual four-field iNUX structure before rendering any widgets."""
    if not isinstance(questions, list) or not questions:
        raise ContentError("An assessment must contain a non-empty list of questions.")
    for number, question in enumerate(questions, 1):
        if not isinstance(question, dict) or set(question) != QUESTION_FIELDS:
            raise ContentError(f"Question {number} needs question, options, success and error fields.")
        if any(not isinstance(question[field], str) or not question[field].strip()
               for field in ("question", "success", "error")):
            raise ContentError(f"Question {number} has missing question or feedback text.")
        options = question["options"]
        if not isinstance(options, dict) or len(options) < 2:
            raise ContentError(f"Question {number} needs at least two answer options.")
        if any(not isinstance(label, str) or not label.strip() or type(correct) is not bool
               for label, correct in options.items()):
            raise ContentError(f"Question {number} options must map Markdown text to true/false.")
        if not any(options.values()):
            raise ContentError(f"Question {number} needs at least one correct option.")
    return questions


def load_questions(filename, language=DEFAULT_LANGUAGE):
    """Read a language-specific iNUX file, with the same English fallback as prose."""
    _language_directory(language)  # Reuse the existing language-code validation.
    if Path(filename).name != filename or not filename.endswith(".json"):
        raise ContentError(f"Expected an assessment JSON filename, received {filename!r}.")
    path = QUESTIONS_DIRECTORY / language / filename
    if not path.is_file():
        path = QUESTIONS_DIRECTORY / DEFAULT_LANGUAGE / filename
    try:
        questions = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ContentError(
            f"Cannot read assessment resource {path.name}. Include the complete assets/questions/en folder."
        ) from error
    return validate_questions(questions)


def evaluate_answer(options, selections):
    """Require every correct option and no incorrect option for success."""
    expected = tuple(options.values())
    actual = tuple(selections)
    if len(actual) != len(expected) or any(type(value) is not bool for value in actual):
        raise ValueError("Selections must contain one Boolean for each option.")
    if not any(actual):
        return "empty"
    return "correct" if actual == expected else "incorrect"


def question_signature(question):
    """A changed question gets fresh widgets and cannot keep stale grading."""
    return hashlib.sha256(json.dumps(question, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]


def remember_option(question_id, option_index, widget_key):
    """Retain answers when their assessment is collapsed; clear outdated feedback."""
    record = st.session_state[ANSWERS_KEY][question_id]
    record["selections"][option_index] = bool(st.session_state[widget_key])
    record["verdict"] = None


def toggle_assessment(panel_key):
    st.session_state[panel_key] = not st.session_state.get(panel_key, False)


def render_question(question, question_id, number, language=DEFAULT_LANGUAGE):
    """Render one question, answer checkboxes and its submitted feedback."""
    TEXT = load_text(language)
    records = st.session_state.setdefault(ANSWERS_KEY, {})
    signature = question_signature(question)
    if records.get(question_id, {}).get("signature") != signature:
        records[question_id] = dict(
            signature=signature, selections=[False] * len(question["options"]), verdict=None
        )
    record = records[question_id]
    with st.container(border=True, key=f"question_{question_id}"):
        st.markdown(TEXT["assessment_question_heading"].format(number=number, question=question["question"]))
        for index, label in enumerate(question["options"]):
            widget_key = f"learning_answer_{question_id}_{signature}_{index}"
            st.checkbox(
                label, value=record["selections"][index], key=widget_key,
                on_change=remember_option, args=(question_id, index, widget_key),
            )
        if st.button(TEXT["assessment_check_answer"], key=f"learning_check_answer_{question_id}"):
            record["verdict"] = evaluate_answer(question["options"], record["selections"])
        if record["verdict"] == "correct":
            st.success(question["success"])
        elif record["verdict"] == "incorrect":
            st.error(question["error"])
        elif record["verdict"] == "empty":
            st.info(TEXT["assessment_choose_answer"])


def render_assessment(filename, title, language=DEFAULT_LANGUAGE):
    """Use the reference module's toggleable container and row-wise question pairs."""
    TEXT = load_text(language)
    namespace = Path(filename).stem
    panel_key = f"learning_panel_{namespace}"
    with st.container(border=True, key=f"assessment_{namespace}"):
        label_column, chevron_column = st.columns([12, 1])
        with label_column:
            st.button(title, key=f"learning_toggle_{namespace}", type="tertiary",
                      on_click=toggle_assessment, args=(panel_key,))
        with chevron_column:
            chevron = "▲" if st.session_state.get(panel_key, False) else "▼"
            st.button(chevron, key=f"learning_chevron_{namespace}", type="tertiary",
                      on_click=toggle_assessment, args=(panel_key,), help=TEXT["assessment_toggle_help"])
        if not st.session_state.get(panel_key, False):
            return
        try:
            questions = load_questions(filename, language)
        except ContentError as error:
            st.error(TEXT["assessment_unavailable"].format(reason=error))
            return
        st.caption(TEXT["assessment_help"])
        for start in range(0, len(questions), 2):
            columns = st.columns(2)
            for offset, column in enumerate(columns):
                index = start + offset
                if index < len(questions):
                    with column:
                        render_question(questions[index], f"{namespace}_q{index + 1}", index + 1, language)
