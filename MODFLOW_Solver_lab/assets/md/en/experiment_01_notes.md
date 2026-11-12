# Teacher notes for Experiment 1

## Teaching decisions

The addition requested during the Experiment 2 discussion makes the analytical comparison an
explicit task: compare heads at matching cell centres, record RMSE and maximum absolute error over
interior cells, and distinguish numerical verification from validation against the real aquifer.
Follow-up question 1 also assesses this distinction.

The sequence retains Thomas's progression: eleven-cell reference model, post-processing, a tighter
head-change criterion, restoration of the original criterion, 51 confined cells, 51 unconfined cells
with an aquifer top of 30 m, then 501 and 5,001 unconfined cells.

PCG is named explicitly because the first experiment introduces both head closure and residual
closure. SIP does not have a separate residual-closure input. Six preparation questions were chosen
within the requested range of four to six, followed by exactly six follow-up questions. Every item
is multiple-select and includes feedback for both correct and incorrect selections.

The brief solver-orientation task closes the learning-objective gap between running only
MODFLOW-2005 and recognizing the options offered by all three implementations. Detailed performance
comparisons between implementations remain suitable for a later experiment.

## Source-grounded scientific details

### Head profile and boundary conditions

For the confined reference, use hydraulic-head or potentiometric profile. The aquifer roof is 0 m
and its bottom is −20 m, while the prescribed heads are 18 and 16 m. The confined head profile is
consequently not a water table.

The boundary heads are specified; exchange flows are computed. The app reports the flows into the
unknown-head region as positive. See the [USGS CHD
documentation](https://water.usgs.gov/nrp/gwsoftware/modflow2000/MFDOC/chd.htm).

### Convergence and accuracy

In PCG, HCLOSE has dimensions of length and RCLOSE of volume per time; both criteria contribute to
stopping. RCLOSE is the maximum absolute nodal equation-residual criterion, not a percentage global
budget discrepancy. The nonlinear algorithm additionally checks convergence on the first inner
iteration. See the [USGS PCG
documentation](https://water.usgs.gov/nrp/gwsoftware/modflow2000/MFDOC/pcg.html).

The task changes HCLOSE from $10^{-4}$ to $10^{-5}$ m, while retaining RCLOSE at the app's default
$10^{-4}$ m³/s. An unchanged iteration count is an acceptable result. A smaller tolerance is not a
direct bound on error against the analytical solution or observations.

The residual threshold is absolute. The model's out-of-plane width is only 1 m, so students should
not generalize its numerical value to other model scales, units, or implementations. The experiment
retains the app's defaults; it is not a universal tolerance recommendation. The PCG, NWT, and IMS
residual definitions should be compared explicitly in a later solver-comparison activity.

SIP's head-only stopping criterion is documented in the [USGS SIP
guide](https://water.usgs.gov/nrp/gwsoftware/modflow2000/MFDOC/sip.html).

### Changing confinement changes geometry

The current app implements the reference confined case with roof 0 m, bottom −20 m, and a fixed
saturated thickness of 20 m. When confinement is switched off, the bottom becomes 0 m and the
entered top is used; the instructions set that top to 30 m.

Students are comparing two geometry/transmissivity representations. They should not interpret
differences in head as a solver error or as an isolated algorithm change, because PCG is used in
both cases. The confined mathematical problem is linear for the specified CHD/recharge setup with
fixed properties. The unconfined coefficients depend on head through saturated thickness. This
statement should not be generalized to all confined models, which can include other nonlinear
features.

For wet convertible cells, transmissivity follows saturated thickness while the head is below the
top. Above the top the cell is fully saturated locally; the top does not cap head or impose surface
drainage. See the [USGS LPF guide](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/lpf.html)
and the [MODFLOW 6 NPF definition of
ICELLTYPE](https://modflow6.readthedocs.io/en/latest/_mf6io/gwf-npf.html).

Using the documented analytical formulas, $K=10^{-4}$ m/s, $R=150$ mm/year, $L=5000$ m, and heads 18
and 16 m gives approximate maxima of 24.46 m for the confined reference and 24.25 m for the
unconfined reference with bottom 0 m. These are analytical checks, not MODFLOW output. They support
the suitability of a 30 m top for an entirely unconfined demonstration; students still inspect the
computed profile.

### Refinement and recharge bookkeeping

The end-cell centres are at 0 and 5,000 m, so $\Delta  x=L/(N-1)$. The first and last cells have
fixed heads; only $N-2$ heads are unknown in this one-row, one-layer model.

| Total cells | Unknowns | Spacing (m) | Recharged length (m) |
| --- | --- | --- | --- |
| 11 | 9 | 500 | 4,500 |
| 51 | 49 | 100 | 4,900 |
| 501 | 499 | 10 | 4,990 |
| 5,001 | 4,999 | 1 | 4,999 |

The code sets recharge to zero in both CHD cells. The integrated recharge to the unknown-head region
is $Q_{R}=RW(N-2)\Delta  x=RW(L-\Delta  x)$, with width $W=1$ m. Thus refining the grid changes the
total recharge represented in that reported region even when the recharge rate and CHD-centre
distance remain fixed. Absolute budget totals across grids should not be treated as unchanged
forcing totals.

For the confined, homogeneous, uniformly recharged benchmark, the analytical profile is quadratic. A
centred second difference differentiates that polynomial exactly at grid nodes. Coarse-grid nodal
heads therefore need not change appreciably with refinement. Numerical solver convergence,
input/output precision, and plotting interpolation remain separate considerations.

### Iterations, timing, and saved comparisons

The app reports outer and inner counts separately. SIP has a separate count. These are not
interchangeable measures of computational work. Refinement increases the number of unknowns but does
not require a monotonic increase in the reported iteration count for the efficient one-dimensional
PCG setup.

Time measures the native executable, including startup, solution, and its output, while excluding
input construction and plotting. A small timing difference can be inconclusive. The optional
exercise uses three repetitions: runtime is the median, while counts and errors are from the last
repeat. The convergence flag requires all repeats to succeed. Initial heads are regenerated using
the same starting rule; the previous result is not used as a warm start.

The comparison table retains ten run rows. Grid-count and confined-mode changes preserve the rows; a
horizontal dimension or extent change resets the comparison. The previous-run overlay is immediate,
whereas **Run to inspect** can select older saved diagnostic results. This is why the instructions
compare C with A through the recorded results: B, with its tighter head criterion, is the
immediately preceding run.

### Solver-family orientation

The available methods are PCG/SIP for MODFLOW-2005, GMRES/XMD within the Newton-based MODFLOW-NWT
setup, and CG/BICGSTAB within MODFLOW 6 IMS. This app creates MODFLOW 6 without Newton options, so
its formulation is Picard.

The primary descriptions are the [USGS NWT solver
inputs](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/nwt_newton_solver.html) and the
[MODFLOW 6 IMS documentation](https://modflow6.readthedocs.io/en/latest/_mf6io/sln-ims.html). These
document general solver capabilities. The specific methods, defaults, and Picard selection above
were additionally checked in the app source.

## Verified source material

The app review used the saved `MODFLOW_Solver_lab_Local.zip` and `MODFLOW_Solver_lab_Streamlit.zip`
packages available on 7 November 2026. Relevant files were `core.py`, `settings.py`, `inputs.py`,
`results.py`, `controls.py`, `app.py`, `README.md`, `CONTENT_GUIDE.md`, and the existing English
Markdown. The principal implementation files reviewed were identical between the local and Streamlit
packages.

The separately supplied, manually edited `ui_page.md` was read and retained. None of its keys or
wording are replaced by this content package.

The question structure was confirmed against `iNUX_karst_knowledge_questions.json` and
`karst_introduction_page_revised.py`: `question`, `options`, `success`, and `error`. This source
verification resolves the dictated name “Enox” as the established iNUX app format; it does not
create an ONYX assessment package.

## Assessment alignment

The six objectives are introduced in the Learning objectives section above. The practical sequence supplies
evidence for each objective: setup and diagnostics for objective 1; the controlled tolerance
comparison for objective 2; the fixed-span refinements for objective 3; the confinement comparison
for objective 4; predictions, observations, and the optional repeated timings for objective 5; and
the implementation/method orientation for objective 6.

Answer keys and explanations are provided with each preparation and follow-up question above.
Questions deliberately avoid a fixed expected runtime, a required iteration increase, or an
assumption that all native runs succeed.

| Question | Preparation focus | Follow-up focus | Main objective |
| --- | --- | --- | --- |
| 1 | Prescribed CHD head and calculated exchange | Confined head interpretation and balance | 1 |
| 2 | Head-change and residual criteria | Unchanged iterations under tighter HCLOSE | 2 |
| 3 | Spacing and unknown count | Refinement, recharge totals, and common coordinates | 3 |
| 4 | Constant versus head-dependent transmissivity | Top 30 m and the app's geometry change | 4 |
| 5 | System size versus nonlinearity | Controlled comparison and timing variability | 5 |
| 6 | Engine and method names | Actual formulations and methods in the app | 6 |
