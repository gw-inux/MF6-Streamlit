# Verification — startup correction, 12 November 2026

This revision starts from the delivered 12 November cosmetic packages. The
reported online traceback fails at `TEXT["experiments_heading"]` in the guided
experiments renderer. The same KeyError and source line were reproduced in the
preceding package by omitting `ui_experiments.md` from the shared text registry.
This verifies a matching failure mechanism; the live server's exact file mix
was not available for inspection.

## Correction and preserved behavior

`content.py` now supplies `load_learning_text`, which reads the existing
experiment-interface Markdown explicitly and validates its required keys.
`experiments.py`, `assessments.py` and `checklists.py` use this loader. `app.py`
checks that the helper is present before importing the learning views. A partial
upload receives an actionable message instead of the reported redacted KeyError.
No global module cache or Streamlit session state is manipulated by this fix.

These are the only five changed runtime files. All numerical, solver, input,
plotting and result modules, launchers and dependency pins remain byte-identical.
The guided header CSS is identical to the preceding cosmetic version. All 21
Markdown resources, six iNUX JSON banks, the manually edited `ui_page.md` and all
existing tests are unchanged. The translation fallback, instruction-only URLs,
question grading, checkbox state and layout are preserved.

## Executed checks

**125 targeted regression checks passed, with no failures or skips:**

- 120 text, guided-experiment, assessment, checklist and startup checks, including
  20 new cases for the reported missing-label condition, all three entry points,
  all three instruction-only routes, missing resource keys, an older content
  module, manual text edits and per-key translation fallback.
- Five import-isolation checks covering unrelated cached modules, all launchers
  and incomplete packages.

The native-engine deployment smoke check used only the 48 online files, the
existing shared `bin` directory and the repository-root launcher. It ran from
an unrelated working directory. MODFLOW-2005/PCG, MODFLOW-NWT/GMRES and MODFLOW
6/CG all converged with reported budget discrepancy 0.00%. Assessment feedback,
checkbox progress and all three instruction-only reading routes worked. The
reading routes did not initialize model workspaces or expose assessments.

Pyflakes passes. All 43 Python navigation headers and `CODE_MAP.md` were
refreshed and checked for idempotence. Both downloadable ZIPs pass integrity,
fresh-extraction, compilation and byte-comparison checks. The 48 online files
match the deployment fixture; no binaries, model output or caches are included.

The full numerical regression suite was not repeated for this text-loader fix.
No new live-browser or deployed-cloud verification is claimed. AppTest exercised
the interface and native model execution; the figure code and cosmetic CSS were
verified byte-identical to the preceding package.

`verification/` includes the reproduction, source-preservation audit, regression
logs/XML, deployment smoke report and archive-integrity report. `CHANGES.patch`
provides a focused source diff. Reboot Streamlit after replacing the complete
support folder and root launcher, including their Markdown/JSON resources.
