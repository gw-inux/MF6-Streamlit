# Streamlit deployment — MODFLOW_Solver_lab

Extract **MODFLOW_Solver_lab_Streamlit_2026-11-12_StartupFix.zip** into the existing **MF6-Streamlit**
repository. The archive contains only the files required by the normal app.
The numerical and interface modules are the same as in the local package.

## Apply the startup fix

Replace the entire `MODFLOW_Solver_lab/` support folder and the repository-root
`MODFLOW_Solver_lab.py` with the contents of this ZIP. Include every supplied
Markdown and JSON file. Reboot the running Streamlit app after the upload so
its imported modules and text are reloaded together. A browser refresh alone
does not reload already imported Python modules.

Do not use the previous two-file cosmetic replacement instructions for this
fix. The experiment, assessment and checklist renderers now use the dedicated
loader in `content.py`, with a matching startup check in `app.py`. Keep these
files from the same archive. The missing `experiments_heading` condition was
reproduced with an older text registry; the deployed server's exact file mix
was not available for inspection.

## Required structure

| Location | Included files |
|---|---|
| Repository root | `MODFLOW_Solver_lab.py` |
| `MODFLOW_Solver_lab/` | `__init__.py`, `app.py`, `streamlit_app.py`, `content.py`, `experiments.py`, `assessments.py`, `checklists.py` |
| Same support folder | `core.py`, `settings.py`, `controls.py`, `inputs.py`, `results.py`, `studies.py` |
| Same support folder | `plots.py`, `ui.py`, `surfaces.py`, `spacing.py`, `diagnostic_guides.py`, `map_rendering.py` |
| Same support folder | `requirements.txt` |
| `MODFLOW_Solver_lab/assets/md/en/` | All 21 Markdown files supplied in the ZIP |
| `MODFLOW_Solver_lab/assets/questions/en/` | All 6 iNUX JSON assessment files supplied in the ZIP |

Both the Markdown and JSON resource directories are required. Upload the complete support folder
and root launcher together, preserving their names. There are **48 files** in
the online archive: 21 runtime/configuration files, 21 Markdown resources and
6 JSON assessment banks.
Keep `MODFLOW_Solver_lab.py` as the Streamlit main file. Restart the running app
process after updating so imported Python modules and text are loaded together.

Existing root apps, requirements, configuration, figures and shared binaries
are not included or overwritten. The folder name and package-relative imports
retain the previous fix for collisions with other apps' `content`, `core`, or
`settings` modules. Missing or malformed text resources produce a readable
startup message. No figure is required while the example in `app.py` is commented.

The Guided experiments links use the same app entry point with
`?view=md&doc=experiment_01.md` (or 02/03). No extra Streamlit page, server or
deployment is required. These independent reading tabs show instructions and
completion checkboxes only; assessments and teacher notes stay in the main app.
They stop before model initialization and retain a configured `server.baseUrlPath`.

## Dependencies and engines

Use the working Python 3.12 environment. Dependency pins are unchanged:
FloPy 3.12.0, Streamlit 1.66.1, NumPy 2.3.5, pandas 3.1.1 and Matplotlib 3.10.8.
Markdown, iNUX question blocks and checklists add no dependency. Keep the existing repository requirements;
if necessary, include this app's pins with:

```text
-r MODFLOW_Solver_lab/requirements.txt
```

Do not replace dependencies needed by other apps. Retain the working engines:

| Engine | Shared Linux executable | Alternative |
|---|---|---|
| MODFLOW-2005 | `bin/mf2005dbl` | `bin/mf2005` |
| MODFLOW-NWT | `bin/mfnwtdbl` | `bin/mfnwt` |
| MODFLOW 6 | `bin/mf6` | — |

Binaries must remain executable. They are not bundled or downloaded by the
running app. The root launcher and Markdown paths work independently of the
process's current working directory.

## Files omitted from the online ZIP

The complete local ZIP supplies documentation, tests, `tools/update_code_map.py`,
the Windows launcher, `install_engines.py` and optional `api_worker.py`. These are
not required by the deployed interface. The support-folder local theme is also
omitted online so the existing repository-root theme continues to apply.
Existing extra files do not need to be re-uploaded or deleted for this update.

For manual editing, use `CONTENT_GUIDE.md` and `CODE_MAP.md` from the complete local
package. The commented figure example points to the shared repository `FIGS`
folder. Only add an actual image when that example is activated.
