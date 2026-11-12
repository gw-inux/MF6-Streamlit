"""Eight teaching sessions, authored as Markdown checklists.

The document route precedes model initialization and contains instructions
only. Checkboxes never apply model changes or run a numerical engine.
"""

from urllib.parse import urlencode

import streamlit as st

from .checklists import render_checklist
from .content import load_md

DOCUMENTS = ("session_confined.md", "session_unconfined.md")


def document_view(language, t):
    if st.query_params.get("view") != "md":
        return False
    doc = st.query_params.get("doc", "")
    if doc not in DOCUMENTS:
        st.error(t["unknown_document"])
        return True
    st.caption(t["document_hint"])
    render_checklist(load_md(doc, language), doc.removesuffix(".md"), language)
    return True


@st.fragment
def render_experiments(language, t):
    with st.expander(t["instructions"]):
        st.markdown(load_md("learning_overview.md", language))
        tabs = st.tabs([t["confined_sessions"], t["unconfined_sessions"]])
        for tab, doc in zip(tabs, DOCUMENTS, strict=True):
            with tab:
                url = "?" + urlencode({"view": "md", "doc": doc, "lang": language})
                st.link_button(t["open_instructions"], url)
                render_checklist(
                    load_md(doc, language), doc.removesuffix(".md"), language
                )
