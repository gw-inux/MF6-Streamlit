# MODFLOW Solver Lab

A Streamlit teaching app developed by Thomas Reimann, TU Dresden Institute for
Groundwater Management / The Groundwater Project, 2026. Real MODFLOW-2005,
MODFLOW-NWT and MODFLOW 6 executables solve steady groundwater-flow models.
The default is the confined, homogeneous 11-cell exercise; complexity is optional.

## Start locally

Extract `MODFLOW_Solver_lab_Local_2026-11-12_StartupFix.zip`, open its `MODFLOW_Solver_lab` folder:

```sh
python -m pip install -r requirements.txt
python install_engines.py
python -m streamlit run app.py
```

If the engines are already in the package's `bin`, the shared parent `bin`, or
PATH, the installer is unnecessary. `run_windows.bat` provides the Windows
shortcut after installation. Engine binaries are not bundled.

## Deploy online

Extract `MODFLOW_Solver_lab_Streamlit_2026-11-12_StartupFix.zip` into the existing **MF6-Streamlit**
repository. Its root `MODFLOW_Solver_lab.py` launches the support package beside
it. Retain the shared `bin`, root requirements, existing apps and theme.
See `DEPLOYMENT.md`. The online archive contains only required runtime files,
including **assets/md/en/** and **assets/questions/en/**. Upload these together.

## Maintain text, figures and source

- **Text:** edit Markdown under `assets/md/en/`. `CONTENT_GUIDE.md` maps the files,
  explains stable text keys and describes English fallback for future languages.
- **Experiments:** `experiment_01.md`, `experiment_02.md` and `experiment_03.md`
  supply practical instructions and checklists in the three Guided experiments
  tabs and their independent reading views. Separate overview/teacher-note
  Markdown stays in the main app. `experiments.py` composes these views.
- **Assessments:** `assets/questions/en/` holds six standard iNUX JSON banks
  with Markdown question text and feedback. `assessments.py` renders question
  blocks; `checklists.py` renders the authored Markdown task rows.
- **Future figure:** the commented block after the introduction in `app.py`
  resolves the repository's `FIGS` folder. It has no effect until uncommented.
- **Python:** every delivered Python file begins with a line-numbered table of
  contents. `CODE_MAP.md` collects the locations. After edits, run
  `python tools/update_code_map.py` from the support folder.
- **Responsibilities:** `app.py` composes the page; `inputs.py` manages panels;
  `controls.py` and `settings.py` manage solver widgets and profiles;
  `results.py` handles execution and inspection; `studies.py` handles grid studies.
  `core.py` owns native models and diagnostics. `plots.py`, `ui.py`, `surfaces.py`,
  `spacing.py`, `diagnostic_guides.py` and `map_rendering.py` contain focused helpers.

The initially closed **Guided experiments** expander remains below the
introductory explanations and above the inputs. Its tabs cover the 1D benchmark,
layers and solver comparisons, and horizontal 2D/3D models. Each retains the
reviewed objectives, preparation questions, workflow, follow-up questions,
optional exercise and teacher notes.

Questions now use the established iNUX JSON format and interactive question
blocks. Learners select all correct options, then use **Check answer** for the
reviewed feedback. Answers survive closing/reopening an assessment. Practical
steps have completion checkboxes. These learning interactions update a separate
Streamlit fragment and leave the model controls and plots in place.

**Open instructions in new tab** follows the Boundary Condition module's
document-view approach. It opens only the practical Markdown and checkboxes,
before model initialization. Assessments and teacher notes remain in the main
app. Reading or checking a step does not apply presets, change model inputs,
run a model or reset results. Only the three listed instruction files are
accepted by this route. Checkmarks belong to their own browser tab.

The manually edited `ui_page.md` is preserved exactly. This startup correction
loads experiment labels directly from `ui_experiments.md` and validates them
before rendering. It addresses the reported `experiments_heading` KeyError and
provides an actionable message for incomplete text uploads. Replace the complete
support folder and root launcher, including both resource directories, then
reboot Streamlit. The previous two-file cosmetic update instructions do not
apply to this correction.

The dark-blue guided-experiments header, blue CHD cells and beige empty cells
are preserved. Numerical, solver, input and plotting modules, all Markdown and
all question banks are unchanged. Package-relative imports retain the earlier
import-collision fix. No runtime dependency is added. `CHANGES.patch` shows the
five changed runtime files and the added startup regression tests compared with
the preceding cosmetic package. See `VERIFICATION.md` for the checks performed.

## Display and saved results

Layered sections and maps use the uppermost wet, active cell head in each
vertical column. Dry upper cells use that value for the surface display;
entirely dry columns remain blank. Native heads and per-layer exports retain
their original values. Input changes keep the previous computed map visible
in grey until rerun. Map images are cached with the complete head array and
scenario; the cache holds at most the normal and stale forms of the current map.

At least one cell-head style remains on. Analytical and initial heads start off;
dots and horizontal segments start on. The first 11-cell model has introductory
CHD and interior-cell labels. A failed run has a pale-red legend and status box.
The blue envelope in the head-error plot is the spatial min–max range across
rows at each x; its line is the middle row, not uncertainty or repeat variability.

The session keeps ten individual runs and five studies. A successful comparison
requires every repetition to converge. Confinement or layer changes preserve
that run book; horizontal dimension or extent changes reset it. Download CSVs
and native listings before closing the session. CSV heads include layer, cell
numbers, coordinates, conductivity and initial heads.

## Geometry and physics

Defaults are L = 5000 m between boundary-cell centres, west/east heads 18/16 m,
out-of-plane width 1 m, and aquifer thickness/top 20 m. Confined mode has roof
0 m and bottom −b. Convertible mode has bottom 0 m and user-defined top z_t.
The aquifer is split into equal-thickness layers when layers are enabled.
K is isotropic: Kx = Ky = Kz. There is no storage, unsaturated-zone model,
surface drain, or automatic overflow above the aquifer top.

The first/last cell centres are x = 0/L, so Δx = L/(Nx−1). The padded domain
extends from −Δx/2 to L+Δx/2. In horizontal 2D the same convention applies in y;
the padded domain is square with side L+Δx. North and south are no-flow.
West/east heads are uniform through all wet boundary layers. Convertible
boundary cells wholly above the corresponding reservoir head are inactive;
a head below a cell's bottom is not assigned as a saturated CHD.

Recharge input is converted with 365.25 × 86,400 seconds/year. It is zero in
both CHD columns and enters the highest wet active cell in each interior
vertical column. Native RCH/RCHA routing is used. Layered convertible LPF/NPF
models enable rewetting from below (threshold 0.01 m, WETFCT 0.5, IWETIT 1,
IHDWET 0); NPF also uses VARIABLECV/DEWATERED. UPW uses Newton's native dry-cell
treatment. The bottom is no-flow. Single-layer formulations are retained.

Random K is log-uniform between positive limits, constant in fixed physical
zones, and independent between layers. Computational refinement samples the
same seeded physical field at the new cell centres. Changing the seed, zone
count, layer count or K limits changes the field. Random initial heads are
independent uniform cell values; fixed boundary heads override the initial
guess. Repeats use identical fields and initial heads.

## Analytical reference and water balance

For a homogeneous single layer, the confined reference is
h(x) = hL + (hR−hL)x/L + R x(L−x)/(2Kb). Its uniform central second difference
is exact at the nodes in exact arithmetic. Refinement mainly explores solver
effort, stopping error and floating-point precision in this benchmark.

The convertible reference integrates K min(h,z_t) dh/dx. The discharge
potential is F(h) = h²/2 below z_t and z_t(h−z_t/2) above it. F(x) is quadratic;
inverting it gives the Dupuit water table and its fully saturated continuation.
LPF/NPF harmonic conductances and UPW upstream weighting need not give identical
coarse-grid heads. Refinement separates discretization from convergence error.

The analytical solution also applies to a homogeneous single-layer horizontal
2D grid because the solution is independent of y. It is deliberately disabled
for heterogeneous or layered models: layer-specific vertical gradients must
not be reported as errors against a vertically integrated homogeneous solution.

The simple confined benchmark retains an independent Darcy-balance check.
All other models use native right/front/lower face flows and actual native
recharge placement. Residual = inflows − outflows + recharge. Boundary flow
signs are positive into the unknown-head region. Native dry or inactive heads remain blank in per-layer exports/diagnostics;
surface views use the uppermost remaining wet-cell head. Entirely dry groundwater
columns invalidate a result and remain blank in any available surface plot.
Legacy input/budget rounding limits precision. A printed 0.00% budget error
is not proof of exact balance.

## Solvers, timing and numerical limits

| Engine | Flow package | Solver methods |
|---|---|---|
| MODFLOW-2005 | LPF | PCG, SIP |
| MODFLOW-NWT | UPW / Newton | GMRES, XMD |
| MODFLOW 6 | NPF / Picard | IMS CG, IMS BICGSTAB |

All app head closures start at **1e-4 m**, including IMS inner closure and
XMD head closure. These app controls explicitly override native defaults.

| Solver | Head closure (m) | Flow closure (m³/s) |
|---|---:|---:|
| PCG | 1e-4 | 1e-4 |
| SIP | 1e-4 | No separate test |
| NWT / GMRES or XMD | 1e-4 | 5e-3 |
| IMS / any preset | 1e-4 | 1e-4 |

The PCG guide defines the head and volumetric-residual tests but gives no
universal RCLOSE number. The app uses the requested 1e-4 starting number,
verified against its native model cases. The IMS 6.7.0 guide describes 0.1 m³/s
as a usual starting residual tolerance for metres/seconds. This small teaching
model uses the more conservative 1e-4 m³/s. NWT's published suggested flux value
is 500 m³/day; the retained 0.005 m³/s value is a rounded, slightly tighter SI
counterpart. It remains loose for a unit-width section and can be tightened.

These are starting controls, not universal error guarantees. Head closure and
flow closure have different dimensions even when their numerical values match.
The NWT flux norm, PCG residual and selected IMS test are not equivalent tests.
Head errors and the native budget should be inspected as well. Backtracking
controls retain their previous explicit app settings.

The app explicitly selects DIAGONAL IMS matrix scaling for the small
second-based coefficients. It is shown in the effective settings and editable
in the expert controls. This does not change the physical equations.
Preset names describe solution strategies, not guaranteed accuracy. NWT's
suggested flux tolerance is loose for a narrow cross-section; tighten controls
when studying accuracy. Head-change closure is not an absolute head-error
bound, and excessively tight tolerances may stall at numerical precision.
NWT edits to preset-controlled fields activate SPECIFIED with remaining preset
values retained. XMD also uses SPECIFIED to apply the app's tighter inner head
closure; without expert overrides that closure follows the main head closure.
Advanced settings are retained per solver/preset; the four main controls are
shared across methods/presets of each engine. SIP has no flow/inner inputs, but
switching to it retains PCG's last flow closure and inner limit for later use.
Iteration limits are not silently increased when a more demanding preset is selected.

Runtime includes executable startup, solving and native output. It excludes
input generation and plotting. Repeated runs show the median runtime; every
repeat must converge for a successful row. Counts and metrics describe the
last repeat. Native counts are never replaced by guessed values. Inner histories
longer than 20,000 records are sampled for display, with an explicit notice;
total iteration counts are preserved.

Normal termination, exit code, convergence messages, head validity and budget
readability are checked. Failed runs remain visible. Extreme starting heads,
wet/dry changes or insufficient solver limits can prevent convergence. The
tested NWT build has exact-zero-residual / three-cell edge cases. SIP can fail
while rewetting a layered unconfined model from low initial heads; the tested
case succeeds from a fully wet initial guess. The app never substitutes an
analytical solution, silently changes the user's controls, or silently retries.

A 255,000-cell limit is checked before model allocation. This bounds accidental
Nx² × layers growth; it is not a runtime guarantee. Each native run has a fixed
120-second timeout. Larger studies explicitly list their dimensions and total run count.

## Verification

See `VERIFICATION.md` and `verification/` for the executed regression and visual
comparisons. To run the included tests:

```sh
python -m pip install -r requirements-test.txt
python install_engines.py --with-api
python -m pytest tests -q
```

Missing engines or the optional API library cause explicit skips. The optional
API worker is retained for regression testing and is not required by the normal
interface or included in the minimal online archive. No live repository or
Streamlit deployment is modified by extracting these packages.

Primary references are kept in `assets/md/en/references.md` and shown in the app.
