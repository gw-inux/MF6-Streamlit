"""Streamlit composition. Run the repository-root streamlit_app.py."""

import shutil
import tempfile
from pathlib import Path

import streamlit as st

from . import __version__
from .analytical import boundary_screen
from .config import ENGINES, fingerprint
from .content import available_languages, load_md, load_text
from .experiments import document_view, render_experiments
from .models import find_executable
from .runtime import history_row, run_model
from .ui_inputs import render_inputs
from .ui_results import render_history, render_results
from .ui_spatial import render_preview

ROOT = Path(__file__).resolve().parent.parent


def main():
    st.set_page_config(
        page_title="ModFlow Newton Lab", page_icon="💧", layout="centered"
    )
    st.markdown(
        "<style>"
        + (Path(__file__).resolve().parent / "assets" / "style.css").read_text()
        + "</style>",
        unsafe_allow_html=True,
    )
    languages = available_languages()
    requested = st.query_params.get("lang", "en")
    language = requested if requested in languages else "en"
    if len(languages) > 1:
        language = st.selectbox(
            "Language / Sprache",
            languages,
            index=languages.index(language),
            key="language",
        )
    t = load_text(language)
    if document_view(language, t):
        return
    st.title(t["title"])
    st.caption(t["version"].format(version=__version__))
    st.markdown(load_md("introduction.md", language))
    render_experiments(language, t)
    with st.expander(t["theory"]):
        st.markdown(load_md("theory.md", language))
    st.subheader(t["model_and_run"], divider="blue")
    s, solvers, input_errors = render_inputs(t)
    valid = not input_errors
    for error in input_errors:
        st.error(error)
    try:
        s.validate()
        for cfg in solvers:
            cfg.validate()
    except ValueError as error:
        st.error(str(error))
        valid = False
    signature = fingerprint(s, solvers)
    if valid:
        st.caption(
            t["model_summary"].format(
                nx=s.ncol,
                ny=s.nrow,
                dx=s.cell_size,
                lx=s.ncol * s.cell_size,
                ly=s.nrow * s.cell_size,
                bottom=s.bottom,
                top=s.top,
                layers=s.nlay,
            )
        )
        if not s.confined and min(s.left, s.right) >= s.top:
            st.info(t["convertible_confined"])
        render_preview(s, t)
        if s.well_enabled:
            with st.expander(t["boundary_check"]):
                for well in s.wells:
                    if len(s.wells) > 1:
                        st.markdown("**" + well.name + "**")
                    screen = boundary_screen(s, well)
                    st.markdown(
                        t["boundary_values"].format(**screen, spacing=s.cell_size)
                    )
                    if screen["ratio_pct"] > 1:
                        st.warning(t["boundary_influence"])
                st.markdown(t["boundary_help"])
                if len(s.wells) > 1:
                    st.caption(t["boundary_multi_help"])
                if s.heterogeneous or s.inactive or not s.confined:
                    st.caption(t["boundary_approximation"])
    executables = {cfg.engine: find_executable(cfg.engine) for cfg in solvers}
    missing = [ENGINES[engine] for engine, path in executables.items() if path is None]
    if missing:
        st.warning(t["missing_engines"].format(engines=", ".join(missing)))
    if not solvers:
        st.info(t["select_engine"])
    if "workdir" not in st.session_state:
        st.session_state.workdir = tempfile.TemporaryDirectory(prefix="newton_lab_")
        st.session_state.history = []
        st.session_state.run_counter = 0
        st.session_state.batch = None
        st.session_state.previous_batch = None
    with st.container(key="main_run"), st.columns([1, 2, 1])[1]:
        run_clicked = st.button(
            t["run"],
            type="primary",
            disabled=not valid or bool(missing) or not solvers,
            key="run_models",
            width="stretch",
        )
    if run_clicked:
        # Retain the immediately previous computation, regardless of parameter edits.
        retired = st.session_state.previous_batch
        st.session_state.previous_batch = st.session_state.batch
        results = {}
        for cfg in solvers:
            st.session_state.run_counter += 1
            run_id = st.session_state.run_counter
            directory = (
                Path(st.session_state.workdir.name) / f"run_{run_id:04d}_{cfg.engine}"
            )
            with st.spinner(t["running"].format(engine=ENGINES[cfg.engine])):
                result = run_model(s, cfg, directory, executables[cfg.engine])
            result["run_id"] = run_id
            results[cfg.engine] = result
            st.session_state.history.append(history_row(result, run_id))
            st.session_state.history = st.session_state.history[-10:]
        st.session_state.batch = dict(signature=signature, results=results)
        st.session_state.pop("archive", None)
        if retired:
            for old in retired["results"].values():
                shutil.rmtree(old["directory"], ignore_errors=True)
    batch = st.session_state.batch
    if batch:
        if not valid or batch["signature"] != signature:
            st.info(t["stale_results"])
            render_history(st.session_state.history, t)
        else:
            st.subheader(t["results"], divider="blue")
            render_results(
                batch,
                st.session_state.previous_batch,
                t,
                language,
                st.session_state.history,
            )
    with st.expander(t["references"]):
        st.markdown(load_md("references.md", language))


if __name__ == "__main__":
    main()
