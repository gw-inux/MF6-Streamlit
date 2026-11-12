## Experiment 2 Layers, heterogeneous conductivity, and initial heads

## Practical investigation

Work through three blocks: homogeneous vertical refinement, heterogeneous conductivity, and
initial-head sensitivity. Make a prediction before each change. Record both successful and
unsuccessful runs, and distinguish an observation from an explanation that still needs evidence.

### Step 1 Establish the homogeneous reference

Return to **51 cells along x**. Switch **Confined aquifer** off and enter **Aquifer top elevation
(m)** = **30 m**. The overall bottom is 0 m. Check these reference values:

| Setting | Value |
| --- | --- |
| Horizontal grid | 51 cells along x, one row |
| CHD-centre distance | 5,000 m; horizontal spacing 100 m |
| Aquifer top / bottom | 30 m / 0 m |
| Left / right CHD head | 18 m / 16 m |
| Recharge rate | 150 mm/year |
| Homogeneous conductivity | $10^{-4}$ m/s, isotropic |
| Initial-head rule | Mean boundary head, giving 17 m in the interior |
| Initial layer count | 1; **Add layers** off |
| Random hydraulic-conductivity field | Off |
| Number of runs | 1 for the initial investigation |

Start with **MODFLOW-2005 / PCG**. Restore head closure to $10^{-4}$ m, R closure to $10^{-4}$ m³/s,
and outer/inner limits to 100/100 if they were changed in Experiment 1. Keep expert settings off.
Name the run **H01-PCG-reference** and compute it.

Enable **Show analytical solution**. Compare numerical and analytical heads at the same cell centres
and record **RMSE (m)** and **Max error (m)**, as well as convergence and water balance. The
analytical solution is an independent reference for the idealized homogeneous single-layer problem.
Agreement supports numerical verification under those assumptions.

Save the heads CSV from this run: it includes analytical heads at the sampled coordinates. This
establishes the reference before the additional complexity is introduced.

- [ ] **Completed:** Step 1 Establish the homogeneous reference <!-- task: step_01 -->

### Step 2 Add vertical layers and predict saturation states

Enable **Enable additional model complexity**, keep **2D horizontal grid (x–y)** off, and switch
**Add layers** on. Use **3 layers** first. With a top of 30 m and bottom of 0 m, each layer is 10 m
thick.

Open **Model preview**. Use **Empty cells** to examine the grid and **Initial heads** to inspect the
starting guess. Identify the elevations of each layer top and bottom.

Predict where the final solution might contain:

- Fully saturated cells, where head is at or above cell top.
- Partly saturated cells, where head lies between cell bottom and top.
- Dry model cells, where no saturated thickness remains in the represented layer interval.

An initially low head in an upper layer is evaluated against **that layer's bottom**, not just the
overall aquifer bottom. A dry model cell does not imply that the real sediment contains no moisture;
this experiment does not solve general unsaturated flow.

- [ ] **Completed:** Step 2 Add vertical layers and predict saturation states <!-- task: step_02 -->

### Step 3 Compare three implementations on the same layered model

Run the three combinations below without changing the grid, physical inputs, or starting-head rule:

| Run suffix | MODFLOW implementation | Method | Treatment in this app |
| --- | --- | --- | --- |
| PCG | MODFLOW-2005 | PCG | LPF with conventional drying and rewetting |
| NWT | MODFLOW-NWT | GMRES | UPW with Newton iteration |
| MF6 | MODFLOW 6 | IMS with CG | NPF with Picard iteration and rewetting |

Use run names **H03-PCG**, **H03-NWT**, and **H03-MF6**. For NWT and MF6, select **MODERATE** as the
declared starting preset, keep expert settings off, and set head closure to $10^{-4}$ m. Record
their displayed residual criteria and iteration limits, then retain those settings for all
subsequent core runs of the same implementation. Changing a preset does not necessarily reset
retained closure values or iteration limits.

The app's starting residual criteria are $10^{-4}$ m³/s for PCG, $5\times 10^{-3}$ m³/s for NWT, and
$10^{-4}$ m³/s for IMS. Their definitions are not identical. This activity compares the **declared
configurations**; it does not isolate the linear algorithm or establish equal accuracy simply by
matching numerical tolerance values. Use the independent hydraulic checks below when interpreting
performance.

For each run, inspect:

1. **Convergence status** and any failure or timeout message.
2. **Outer**, **Inner**, and **Time (s)** in the comparison table.
3. The available convergence histories and **Solver settings used for this run**.
4. Recharge, left/right exchange, water-budget discrepancy, and maximum cell residual.
5. The displayed uppermost wet-cell head and the individual **Layer heads and geometry**.
6. The location of wet, partly saturated, and blank cells, using the exported active/CHD information where necessary.

The surface shown for a layered model uses the **uppermost wet active cell head** in each column. It
is not the maximum head among layers, and it does not show every vertical head gradient. Inspect
layer heads as well as the surface.

Blank upper cells can be dry or deliberately inactive. In particular, boundary cells wholly above
the specified reservoir level are inactive. Do not interpret their missing heads as zero or include
dry/inactive output markers in head-error statistics.

If convergence histories oscillate or stagnate, investigate the native listing. Such behaviour can
be consistent with changing saturation, but a final dry-cell pattern alone does not prove repeated
drying and rewetting during iterations. Iterations here are numerical operations, not a simulated
physical drainage history.

- [ ] **Completed:** Step 3 Compare three implementations on the same layered model <!-- task: step_03 -->

### Step 4 Refine the vertical grid

Repeat the same three-engine comparison with **10 layers**, then **30 layers**. Keep the aquifer
geometry, 51 horizontal cells, homogeneous K, recharge, boundary heads, and mean-boundary starting
rule unchanged.

| Model | Layers | Layer thickness | Geometric cell count, including boundary and inactive cells |
| --- | --- | --- | --- |
| Reference | 1 | 30 m | 51 |
| First layered case | 3 | 10 m | 153 |
| Intermediate refinement | 10 | 3 m | 510 |
| Fine vertical grid | 30 | 1 m | 1,530 |

Use **H10-PCG/NWT/MF6** and **H30-PCG/NWT/MF6** as the run names. At each refinement, predict
whether the changed layer elevations are likely to increase the number of dry upper cells or create
cells with small saturated thickness. Check what actually occurs; a larger layer count does not
prescribe a particular convergence outcome.

Together with the single-layer reference, this block contains ten new run rows. Use **Download
comparison CSV** before continuing. Save useful heads CSVs and native listings as evidence; the app
retains only the latest ten comparison rows.

#### Retain the analytical comparison with the correct interpretation

The current app disables its analytical overlay and analytical-error metrics for multiple layers.
This is intentional: resolving vertical gradients goes beyond the vertically integrated reference. A
missing RMSE is not a zero error.

For the unchanged homogeneous inputs, the saved single-layer analytical curve can still support an
**approximate reference comparison**. Compare the layered uppermost wet-cell heads at common x
coordinates with the values below, and inspect vertical head differences separately.

| x coordinate (m) | Homogeneous 1D Dupuit reference head (m) |
| --- | --- |
| 0 | 18.0000 |
| 1,000 | 22.3725 |
| 2,000 | 24.1245 |
| 2,500 | 24.2296 |
| 3,000 | 23.8410 |
| 4,000 | 21.4413 |
| 5,000 | 16.0000 |

These calculated reference values use $L=5000$ m, $K=10^{-4}$ m/s, recharge 150 mm/year converted
using 365.25 days/year, heads 18/16 m, and bottom 0 m. They are rounded to four decimal places. Use
the app's full-precision analytical outputs for the single-layer error assessment.

For a layered calculation, call the difference a **difference from the 1D reference**, not pure
solver error. Differences can include vertical-flow effects, discretization effects, conductance
formulations, and incomplete convergence. Use only the homogeneous case for this comparison; the
table is not a reference for the following random-K model.

- [ ] **Completed:** Step 4 Refine the vertical grid <!-- task: step_04 -->

### Step 5 Introduce a fixed heterogeneous conductivity field

Keep **30 layers**, 51 cells along x, and the mean-boundary starting-head rule. Enable **Random
hydraulic-conductivity field** and use:

- **Minimum K** = $10^{-5}$ m/s.
- **Maximum K** = $10^{-3}$ m/s.
- **K zones per direction** = **11**.

The app generates log-uniform conductivity values in horizontal zones, independently for each layer.
Inspect **K zones** in the preview and select different **Preview layer** values. Identify contrasts
that could change head gradients or vertical flow. The hydraulic-head profile may remain smooth
despite large conductivity contrasts.

Keep this exact realization for all comparisons. **Do not press New realization between engine
runs.** Also retain the layer count, grid, K bounds, and zone count. The actual K values are
included in the heads CSV, which provides a record of the field used. A direct K-seed input is not
available in the current interface.

Run **K30-PCG**, **K30-NWT**, and **K30-MF6** using the settings recorded earlier. Compare each with
its homogeneous H30 counterpart. Investigate convergence, iteration history, runtime, saturation
patterns, head gradients, and water balance.

Changing layer count in the random-K model changes the vertical conductivity distribution, even if
the internal seed is unchanged. Therefore, keep 30 layers throughout this block and the initial-head
block. Otherwise a supposed numerical comparison would also change the physical field.

The app's homogeneous analytical solution is no longer applicable. Agreement between two numerical
implementations and a small water-budget discrepancy provide useful checks, but neither alone proves
the heads are accurate. Inspect the actual recharge delivery and wet/dry patterns as well as heads.

Export the comparison table and save the three heads CSVs before moving on. These mean-boundary runs
provide the initial-head reference for the next block.

- [ ] **Completed:** Step 5 Introduce a fixed heterogeneous conductivity field <!-- task: step_05 -->

### Step 6 Investigate the starting-head distribution

Retain the **same 30-layer heterogeneous model and the same conductivity realization**. Keep the
physical inputs and each implementation's solver settings unchanged. Inspect the starting guess
using the model preview before computing.

The app offers four starting-head choices. The mean-boundary case was already computed in Step 5;
investigate the other three now:

| Starting-head choice | Settings for this experiment | Purpose |
| --- | --- | --- |
| Mean boundary head | 17 m in interior cells; reuse K30 results | Reference |
| Linear between boundaries | 18 m at the left to 16 m at the right, repeated through layers | Smooth horizontal initial gradient |
| Random distribution | Minimum 10 m, maximum 25 m, **Initial-head seed** 24 | Irregular initial guess, identical across engines |
| Specified uniform head | Manually enter **0.1 m** | Low guess close to the overall aquifer bottom |

For each of the three new choices, run PCG, NWT/GMRES, and MF6/CG. Use run names
**I-linear-PCG/NWT/MF6**, **I-random-PCG/NWT/MF6**, and **I-low-PCG/NWT/MF6**. The random
initial-head seed is editable under **Show full settings**; it is separate from the conductivity
realization.

For the low-head case, enter 0.1 m directly rather than stepping down from 17 m. The input is
accepted by the app and is not clipped to each layer bottom. Most upper interior layers therefore
start with heads below their bottoms. The CHD values remain prescribed at the boundaries; changing
the interior starting guess does not change those conditions.

Compare each result with the corresponding mean-boundary run. Ask:

1. Did the initial guess change the number of iterations or whether convergence was achieved?
2. If two runs converged, do their final head profiles and saturation patterns agree sufficiently for the intended comparison?
3. If they differ, do the diagnostics reveal residual, budget, recharge-routing, or wetting issues?
4. Is any speed advantage accompanied by a credible solution?

A unique steady-state solution of an unchanged, accessible mathematical problem should be
independent of the starting guess within numerical accuracy. Drying/rewetting and different
reachable saturation states can complicate that expectation. Investigate a different final result;
do not assume that convergence alone establishes equivalence.

These nine new runs fit within the ten-row retention limit, but older mean-boundary runs will be
displaced. Retain the exports from Step 5 and export this block before performing optional runs.

- [ ] **Completed:** Step 6 Investigate the starting-head distribution <!-- task: step_06 -->

### Record and interpret the evidence

Keep a brief record for each run:

| Run | Layer count and K case | Starting-head rule | Converged? | Outer / inner counts | Runtime | Water balance and max residual | Saturation pattern and head comparison |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

Record solver settings with the results. Preserve failed-run messages; do not replace an
unsuccessful core run with an undocumented change in settings. A deliberate later attempt with a
different preset or limit should be named as a separate experiment.

When comparing heads across engines, use matching coordinates and layers where the values are
physically interpretable in both runs. Also inspect locations with different wet/dry status;
excluding those cells from a numerical statistic must not hide the disagreement. Across different
vertical grids, compare the uppermost wet-cell profiles at common x coordinates and account for
differing layer elevations.

Distinguish **robustness** (obtaining credible converged results under the tested conditions),
**effort** (runtime and appropriately identified iterations), and **accuracy** (agreement with a
valid reference or other relevant checks). The current app uses different flow formulations as well
as different solution methods, so an observed ranking applies to the declared configurations and
tested cases.

### Complete the experiment

Complete the six follow-up questions, selecting **all correct answers**. State whether your results
support the hypothesis that NWT is more robust for the challenging cases, and identify the evidence
and limitations of that conclusion.

## Optional exercise Test the Newton hypothesis

Use the fixed 30-layer heterogeneous model and your recorded initial-head results. Prepare a short
recommendation about which configured procedure you would use for this case.

For each implementation, report:

- How many of the four starting-head choices produced a credible converged result.
- Whether successful runs gave consistent heads and wet/dry patterns.
- Which diagnostics support acceptance of the hydraulic solution.
- How the computational effort compares for the accepted runs.

If a small runtime difference determines your choice, repeat that specific comparison with **Number
of runs = 3**. The app reports median runtime; counts and errors refer to the last repetition, and
all repeats must converge for an aggregate successful result.

As an additional check, use **Specified uniform head = 30 m** with each implementation. This starts
all active interior layers wet, while the boundary conditions remain prescribed. Compare it with the
0.1 m case on the same physical model. Export a table before adding more than ten run rows.

Conclude in no more than five sentences:

> Did Newton provide greater robustness, lower computational cost, both, or neither in the tested
> cases? What alternative explanation or additional check would most affect your conclusion?

Do not assign a universal winner. Your conclusion concerns the recorded grid, conductivity
realization, initial guesses, flow formulations, and stopping settings. If the hydraulic diagnostics
disagree, report the comparison as unresolved rather than ranking an unverified fast result as
superior.

- [ ] **Completed:** Optional exercise <!-- task: optional_exercise -->
