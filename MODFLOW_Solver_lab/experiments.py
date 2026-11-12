"""Guided experiments, iNUX assessments and independent instruction checklists.

The document-only route uses the same practical Markdown as the main tabs.
Overview, assessments and teacher notes stay in the main app. Learning widgets
rerun as a fragment, leaving the model controls and plots in place.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   Keep this order aligned with the three tab labels below. These filenames: line 30
#   EXPERIMENT_FILES: line 32
#   EXPERIMENT_STYLE: line 34
#   document_url: line 56
#   render_prose: line 63
#   render_experiment_text: line 72
#   render_document_view: line 84
#   render_experiments: line 108
# END CODE CONTENTS

from pathlib import Path
from urllib.parse import urlencode

import streamlit as st

from .assessments import render_assessment
from .checklists import render_checklist
from .content import ContentError, DEFAULT_LANGUAGE, load_md, load_text


# EDIT: Keep this order aligned with the three tab labels below. These filenames
# also preserve the previously shared document links; only their contents change.
EXPERIMENT_FILES = ("experiment_01.md", "experiment_02.md", "experiment_03.md")

EXPERIMENT_STYLE = """
<style>
.st-key-experiments_panel div[data-testid="stExpander"] {
    --panel-header: #EDF6FD; border-color: #97C6E8;
}
.st-key-guided_experiments > div[data-testid="stExpander"] {
    border-color: #355F83;
}
.st-key-guided_experiments > div[data-testid="stExpander"] > details > summary {
    background: rgba(24, 67, 105, .92) !important;
    color: #F2F5F8 !important;
}
.st-key-guided_experiments > div[data-testid="stExpander"] > details > summary p {
    color: inherit !important;
}
.st-key-experiments_panel [class*="st-key-assessment_"] button[kind="tertiary"] {
    color: #176DBB;
}
</style>
"""


def document_url(filename):
    """Stay on the current app path, including deployments beneath a subpath."""
    if filename not in EXPERIMENT_FILES:
        raise ValueError("Unknown experiment document.")
    return "?" + urlencode({"view": "md", "doc": filename})


def render_prose(filename, language=DEFAULT_LANGUAGE):
    """Load overview/teacher prose without embedding it in Python."""
    TEXT = load_text(language)
    try:
        st.markdown(load_md(filename, language), unsafe_allow_html=True)
    except ContentError as error:
        st.error(TEXT["experiment_unavailable"].format(reason=error))


def render_experiment_text(filename, language=DEFAULT_LANGUAGE, show_title=True):
    """Render practical Markdown and its stable completion checkboxes only."""
    TEXT = load_text(language)
    try:
        document = load_md(filename, language)
        if not show_title and document.startswith("#"):
            document = document.partition("\n")[2].lstrip("\n")
        render_checklist(document, Path(filename).stem, language)
    except ContentError as error:
        st.error(TEXT["experiment_unavailable"].format(reason=error))


def render_document_view(language=DEFAULT_LANGUAGE):
    """Handle the established `?view=md&doc=...` route before model setup.

    Only practical instructions and checkboxes are rendered. Return True even
    for invalid documents, so the caller stops before initializing model state.
    """
    if st.query_params.get("view") != "md":
        return False
    TEXT = load_text(language)
    st.markdown("""<style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"],
        [data-testid="stSidebarCollapsedControl"] {display: none !important;}
        </style>""", unsafe_allow_html=True)
    filename = st.query_params.get("doc", "")
    if filename not in EXPERIMENT_FILES:
        st.error(TEXT["experiment_unknown_document"])
        return True
    with st.container(key="experiment_document"):
        st.caption(TEXT["experiment_document_hint"])
        render_experiment_text(filename, language)
    return True


@st.fragment
def render_experiments(language=DEFAULT_LANGUAGE):
    """Learning interactions redraw this section without rerunning the model UI."""
    TEXT = load_text(language)
    st.html(EXPERIMENT_STYLE)  # Style-only HTML adds no extra vertical space.
    with st.container(key="experiments_panel"):
        with st.expander(TEXT["experiments_heading"], key="guided_experiments"):
            st.caption(TEXT["experiments_hint"])
            tabs = st.tabs([
                TEXT["experiment_1_tab"], TEXT["experiment_2_tab"], TEXT["experiment_3_tab"]
            ])
            for tab, filename in zip(tabs, EXPERIMENT_FILES, strict=True):
                name = Path(filename).stem
                with tab:
                    render_prose(f"{name}_overview.md", language)
                    render_assessment(f"{name}_pre.json", TEXT["assessment_preparation"], language)
                    st.link_button(TEXT["experiment_open_tab"], url=document_url(filename),
                                   help=TEXT["experiment_open_help"])
                    render_experiment_text(filename, language, show_title=False)
                    render_assessment(f"{name}_post.json", TEXT["assessment_follow_up"], language)
                    with st.expander(TEXT["experiment_teacher_notes"]):
                        render_prose(f"{name}_notes.md", language)
