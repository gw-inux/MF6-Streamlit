# Editing text and adding figures

## Where to edit

The interface is still English. Existing controls and default settings are unchanged. The Guided experiments
header uses dark blue/light text; CHD markers and shading use blue. Editable
text and the expander position before the inputs are retained.
The manually supplied `ui_page.md` is preserved. Text is loaded from UTF-8 Markdown beside the Python package;
paths do not depend on the directory from which Streamlit is started.

| File under `assets/md/en/` | Displayed content |
|---|---|
| `introduction.md` | Introduction and motivation |
| `equations.md` | Analytical benchmarks, numerical equations, assumptions and experiments |
| `solver_details.md` | Solver comparison, stopping criteria and documentation links |
| `conclusion.md` | Conclusion |
| `references.md` | Primary references |
| `experiment_01.md` | Guided experiment 1: the 1D benchmark, closures and grid refinement |
| `experiment_02.md` | Guided experiment 2: layers, initial heads and solver comparison |
| `experiment_03.md` | Guided experiment 3: horizontal 2D grids and layered 3D models |
| `experiment_01_overview.md` to `experiment_03_overview.md` | Experiment introductions and learning objectives, shown in the main app |
| `experiment_01_notes.md` to `experiment_03_notes.md` | Collapsible teacher notes and sources, shown in the main app |
| `ui_experiments.md` | Expander/tab labels, document links and reading-view messages |
| `ui_shared.md` | Shared captions, model summary and section headings |
| `ui_page.md` | Page headings and introduction expander labels |
| `ui_inputs.md` | Scenario, discretization and complexity labels, help and captions |
| `ui_solver.md` | Basic and expert solver labels and help |
| `ui_results.md` | Execution, comparison and diagnostic captions and controls |
| `ui_study.md` | Grid-study labels, help and result captions |

Long documents are rendered as Markdown without processing their equations.
Keep LaTeX backslashes as ordinary characters: unlike a Python string, a
Markdown file does not need a raw-string prefix or doubled backslashes.

In the `ui_*.md` files, each `## stable_key` heading identifies one text block.
Only the block below it is displayed; neither the key nor the file introduction
appears in the app. Keep those keys unchanged. To add a subheading *inside* a
block, use `###` or deeper. Do not leave a block empty or repeat a key.

Templates retain named fields such as `{grid}`, `{cells:,}` and `{head:.2E}`.
Keep field names and number formats unchanged when editing or translating.
Some small fragments deliberately start or end with a space: preserve it.
The current constant exports are loaded at Python import; restart the app
process after editing Markdown to reload all of them.

## Guided experiments and separate reading tabs

Each `experiment_0N.md` now contains only the practical instructions and optional
exercise. The main app and its separate reading view load this same file, so
edit it once. The document files are loaded on each rerun. The three filenames
and their tab order are listed in `experiments.py`; all learning-interface labels
and help messages live in `ui_experiments.md`.

The learning views call `load_learning_text(language)` in `content.py`. This
reads `ui_experiments.md` explicitly, without depending on its registration in
the general `TEXT_FILES` list, and validates all required stable keys before
rendering. Keep the `## experiments_heading` key and the other named sections
intact when editing. Missing keys produce an actionable resource message.
The loader preserves the same per-key English fallback as `load_text`; no
visible text is duplicated in Python. Upload the complete support folder and
resources together, then reboot Streamlit after a code update.

One completion checkbox follows each numbered practical step, plus one for the
optional exercise. Write a task row as ordinary Markdown with a stable ID:

```markdown
- [ ] **Completed:** Step 1 Configure the model <!-- task: step_01 -->
```

Translate the visible label, keeping `<!-- task: step_01 -->` unchanged. IDs must
be unique within each document. They keep progress independent of wording.
`checklists.py` renders these rows as interactive checkboxes while preserving
ordinary Markdown, tables, equations and fenced examples. Checkmarks record
progress; they do not apply model settings or run calculations. Progress stays
in the current browser session. A separately opened tab has independent checks.

The separate reading URL is `?view=md&doc=experiment_01.md` (or 02/03).
Links retain the current app path, including deployment below a URL subpath.
This route displays practical instructions and completion checkboxes only. It
does not include the overview, assessments or teacher notes, and does not create
a model workspace.
Unlisted documents are rejected with a readable message. Reading tabs do not
share model state or change the original tab's settings and results.

## iNUX assessments and feedback

The six files under `assets/questions/en/` are self-contained standard iNUX
JSON, matching the Soil Water Retention module's four-field structure:

```json
[
  {
    "question": "Which statements are **correct**?",
    "options": {"First statement": true, "Second statement": false},
    "success": "**Correct.** Explanation of the correct selection.",
    "error": "**Not quite.** Feedback to guide another attempt."
  }
]
```

`experiment_01_pre.json` and `experiment_01_post.json` contain the six preparation
and six follow-up questions; experiments 02 and 03 follow the same names. All
question text, option labels and feedback are Markdown strings in JSON. There
is no duplicate question text in Python or in the instruction Markdown files.
Keep JSON keys and Boolean answer values unchanged when translating. Escape
LaTeX backslashes according to JSON syntax, for example `"$\\theta$"`.

`assessments.py` renders the usual toggleable assessment container and pairs of
question blocks. **Check answer** succeeds only when all correct options and
no incorrect options are selected. The reviewed success/error explanations are
retained. Selections and feedback survive hiding a panel; changing an answer
clears outdated feedback. Editing question content starts a fresh response to
avoid grading a stale selection. The renderer uses the app's existing Streamlit
dependency and requires no additional assessment package.

The learning area is a Streamlit fragment: answer and progress interactions
update this area while the model controls and plots remain in place.

## Preparing another language

Create `assets/md/de/`, for example, and copy only the documents being
translated, retaining their filenames and stable keys. `load_md(filename, "de")`
falls back to the English document when a translation is absent. `load_text("de")`
also falls back for individual missing interface keys. The language is an
explicit loader argument, so English and German loads cannot overwrite each
other through session state or a shared language cache.

For assessments, create `assets/questions/de/` and translate the corresponding
JSON files. `load_questions(filename, "de")` falls back to English per missing
file. Both learning renderers accept an explicit language argument; the default
remains English. Narrative prose, question/feedback Markdown, and interface text
are therefore ready for later translation without editing model code.

There is deliberately no new language selector. When one is added, call the
loaders during each rerun with the selected language and pass the resulting
texts into the interface. Keep model option identifiers, widget keys, stored
run data and exported column names stable. Domain choices, engine-generated
messages, table schemas and Matplotlib labels remain with the existing model
and plotting code; a full translated interface should address their *display*
labels separately, without translating the underlying values.

## Future repository figure

The commented block immediately after the introduction in `app.py` loads:

`MF6-Streamlit/FIGS/MODFLOW_Solver_lab_intro.png`

Replace that filename with your actual figure and uncomment the block. It
uses `Path(__file__)` to resolve the shared repository `FIGS` folder and places
the figure in a centred column. Until then it has no runtime or layout effect,
and no placeholder image is required. For a figure-specific subfolder, append
it between `"FIGS"` and the filename. Future captions can be another Markdown
block rendered with `st.caption` below the image.

## Code navigation

Every delivered Python file has a table of contents with line numbers. The
complete local package includes `CODE_MAP.md`. After manual source changes:

```sh
python tools/update_code_map.py
```

The tool updates comments and the map only. It does not rewrite functions,
Markdown content, model parameters or figures.
