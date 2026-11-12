## Experiment 3 From one dimension to large 2D and 3D models

## Practical investigation

Work through the blocks in order. At each change, first write a prediction, then inspect the
computed result, and finally explain whether the evidence supports your prediction. Treat a failed
or timed-out run as an observation to diagnose, not as a successful fast calculation.

### 1. Establish the one-dimensional reference

Return to one horizontal row and one layer. Keep **2D horizontal grid (x–y)** off and **Random
hydraulic-conductivity field** off. Use cell-count entry rather than **Define cell spacing instead
of cell count**.

| Setting | Value |
| --- | --- |
| Cells along x | 11 |
| Aquifer condition | Unconfined |
| Aquifer bottom / top | 0 m / 30 m |
| Distance between west/east CHD cell centres | 5,000 m |
| West / east prescribed head | 18 m / 16 m |
| Homogeneous, isotropic conductivity | 0.0001 m/s |
| Recharge | 150 mm/year |
| Starting-head distribution | Linear between boundaries |
| Number of runs | 1 initially |

Select **MODFLOW-2005 / PCG** and run the model. Inspect the heads, the water balance, and the
convergence information. Activate **Show analytical solution** and compare numerical heads with the
reference at the same cell-centre positions. Record analytical RMSE and maximum absolute error where
available.

Save the one-dimensional comparison and heads CSV before the next step: switching horizontal 2D on
clears the current individual-run comparison and saved profiles.

- [ ] **Completed:** 1. Establish the one-dimensional reference <!-- task: step_01 -->

### 2. Extend the model into the x–y plane

Enable the additional complexity controls and **2D horizontal grid (x–y)**. Retain 11 cells along
each horizontal direction and one layer. Inspect **Additional complexity settings and model
preview**: the model now contains 11 × 11 = **121 cells**.

Run **MODFLOW-2005 / PCG** again. Examine **Computed heads · groundwater surface (x–y)** and the
middle-row section A–A′. Keep **Show analytical solution** on.

Investigate these questions:

- Does the middle-row numerical profile agree with the analytical reference within the observed numerical error?
- At the same x coordinate, are the heads approximately equal across different rows? Use the plan view, the head-error envelope, or the exported heads CSV to check.
- Which assumptions allow the one-dimensional analytical solution to remain applicable?

In this model, homogeneous isotropic K, geometry and recharge independent of y, uniform west/east
CHD heads, and no-flow north/south sides permit a solution independent of y. Adding rows therefore
increases the numerical system without requiring a new physical head gradient in y. Pronounced
row-to-row differences deserve investigation.

**Compare heads and budgets appropriately.** The original one-row model is 1 m wide; the square
model is much wider. Its total volumetric recharge and boundary flows therefore differ even when the
head profile is essentially unchanged. Use the budget of each model to check its own mass balance.
For a cross-model flow comparison, account for the width and the actual area receiving recharge.

- [ ] **Completed:** 2. Extend the model into the x–y plane <!-- task: step_02 -->

### 3. Increase horizontal resolution and compare the procedures

Keep K homogeneous and retain the hydraulic parameters, recharge rate, boundary heads, and 5,000 m
CHD-centre span. In this app, the full-cell width and total area receiving recharge change slightly
with grid refinement. Account for the actual recharge area when comparing volumetric budgets across
grids. Use the following square, single-layer grids:

| Cells along x and y | Total cells | Cell-centre spacing for L = 5,000 m |
| --- | --- | --- |
| 11 | 121 | 500 m |
| 21 | 441 | 250 m |
| 51 | 2,601 | 100 m |
| 501 | 251,001 | 10 m |

The app uses **spacing = L / (N − 1)** because the boundary cell centres are at x = 0 and x = L.
Total cells are **N × N**, including prescribed-head cells; this is not the same as the number of
unknown heads.

At each grid size, compare these representative configurations:

| Implementation | Configuration for this investigation |
| --- | --- |
| MODFLOW-2005 | PCG with the app's conventional unconfined formulation |
| MODFLOW-NWT | Newton formulation with UPW and GMRES |
| MODFLOW 6 | The app's current NPF/Picard formulation with IMS-CG |

Use the intended baseline settings from the earlier experiments. Restore a head-closure value of
**0.0001 m** if it was changed; for MODFLOW 6 inspect both outer and inner head criteria. Record
each engine's actual flow/residual criterion, iteration limits, and other numerical settings.
Selecting a preset may retain earlier manual edits. Keep those settings fixed within each engine
during the grid-size sweep.

Identical numerical threshold values do not establish equivalent stopping conditions across engines.
Evaluate the resulting heads and budgets as well as the declared convergence status. This compares
the complete configured procedures; it does not isolate compiler performance or only the inner
linear algorithm.

For each run:

1. Inspect the model preview and confirm the intended grid.
2. Give the run a descriptive name, for example `E3_H_51x51_1L_NWT`.
3. Run the model and inspect the plan view and middle-row section.
4. Record convergence or failure, elapsed runtime, clearly identified inner/outer iteration counts, analytical head errors, and budget discrepancy.
5. Check whether the result remains approximately invariant in y.

Complete 11 × 11, 21 × 21, and 51 × 51 with the three configurations first. These make nine
individual runs. Export the comparison before proceeding to the three **501 × 501** runs. Export
that larger-grid block separately. The individual-run table retains ten entries; save heads CSV
files and native listings for cases that you want to inspect later.

The 501 × 501 grid is an advanced size test. It fits the app's 255,000-cell limit, but that does not
guarantee completion. The native execution timeout is 120 seconds per run. Record timeout,
non-convergence, and invalid hydraulic outcomes separately. Do not silently loosen the stopping
criteria merely to obtain a successful flag.

**Interpretation.** How much did total cells, iterations, and runtime change? Did analytical errors
change? A larger system can require more work per iteration even if it needs the same number of
iterations. Neither runtime nor iteration count is guaranteed to grow monotonically. If a small
timing difference matters to your conclusion, repeat that particular successful comparison with
**Number of runs = 3**. The app reports median runtime; the reported counts and errors belong to the
last repetition, and all repetitions must succeed for aggregate success.

- [ ] **Completed:** 3. Increase horizontal resolution and compare the procedures <!-- task: step_03 -->

### 4. Introduce a fixed heterogeneous conductivity field

Return to **51 × 51 cells and one layer**. Keep **Linear between boundaries** as the starting-head
distribution. Enable **Random hydraulic-conductivity field** with these reproducible choices:

| Control | Value |
| --- | --- |
| Minimum K | 0.00001 m/s |
| Maximum K | 0.001 m/s |
| K zones per direction | 11 |

Inspect the **K zones** preview. Retain the same realization while comparing all three procedures:
do not select **New realization** between them. Save a heads CSV, which includes the actual K array.

For each implementation, examine the head map, middle-row section, convergence, budget, and runtime.
Does the head pattern now vary in y? How does the numerical effort compare with the homogeneous 51 ×
51 case for that implementation?

The original homogeneous analytical reference is unavailable for this general K(x, y) field. Compare
numerical results at matching locations and use budgets, residuals, saturation, and controlled
cross-engine checks. Agreement between engines is useful evidence, but is not by itself proof of
accuracy. Do not label differences between heterogeneous and homogeneous heads as numerical error.

- [ ] **Completed:** 4. Introduce a fixed heterogeneous conductivity field <!-- task: step_04 -->

### 5. Apply the initial-head investigation to horizontal 2D

Keep **51 × 51 × 1**, the same conductivity realization, and the numerical settings fixed. Reuse the
heterogeneous runs from Step 4 as the first row of this comparison:

| Starting-head distribution | Settings | Purpose |
| --- | --- | --- |
| Linear between boundaries | 18 m to 16 m | Controlled reference guess |
| Random distribution | Minimum 10 m, maximum 25 m; Initial-head seed 24 under Show full settings | Test an irregular initial estimate |
| Specified uniform head | 0.1 m | Test very small positive initial saturated thickness |

Run each initial-head choice with each of the three configurations. With the reused reference runs,
this block contains nine results. Do not generate a new K realization. Keep the grid unchanged so
that the fixed initial-head seed reproduces the same cell-by-cell random guesses across engines.

Use **Show initial heads** to compare the starting guesses with the computed profile. Which choices
converge? Do successful runs approach consistent heads and saturation patterns? How do iterations
and runtime change? Random starting heads need not be the most difficult choice: test that
prediction with the recorded results.

**Near-zero and exact-zero are different cases.** With bottom 0 m, the supported uniform start of
0.1 m gives the one-layer interior a small positive saturated thickness. The west/east CHD heads
remain prescribed at 18 m and 16 m. Exactly 0 m is rejected by the current app before MODFLOW is
called, so it cannot be recorded as a native solver failure.

Discuss the hypothetical exact-zero case instead: zero interior saturated thickness can remove
transmissivity there, but the boundary conditions, recharge, hydraulic connections, and the engine's
treatment of drying and wetting must also be considered. There is no justified prediction that every
numerical formulation must fail. In the current app, explicit LPF/NPF rewetting is enabled for
unconfined multilayer cases, not this single-layer stage; NWT uses its own UPW/Newton treatment.

Export this block before proceeding. If you want to isolate initial-head effects from heterogeneous
K, an optional repetition with homogeneous K restores the analytical reference; random initial heads
alone do not invalidate that steady reference.

- [ ] **Completed:** 5. Apply the initial-head investigation to horizontal 2D <!-- task: step_05 -->

### 6. Add the vertical direction in controlled stages

Before adding layers, confirm **51 cells along x and y**. In particular, do not retain 501 × 501
when activating layers. Switch **Random hydraulic-conductivity field** off and restore **Linear
between boundaries**. Keep bottom 0 m and top 30 m.

Run a homogeneous 51 × 51 × 1 reference with each configuration, then repeat with three layers and
ten layers:

| Horizontal grid | Layers | Layer thickness | Total cells |
| --- | --- | --- | --- |
| 51 × 51 | 1 | 30 m | 2,601 |
| 51 × 51 | 3 | 10 m | 7,803 |
| 51 × 51 | 10 | 3 m | 26,010 |

At each stage, inspect **Layer heads and geometry** as well as the groundwater-surface map and
middle-row section. Where are cells fully saturated, partly saturated, or dry? How do the heads vary
with depth? Do the three implementations produce similar hydraulically meaningful results?

Adding layers changes more than the total cell count. For example, with three layers the upper layer
has bottom 20 m, above the 18–16 m initial profile. It therefore starts dry in the interior. With
ten layers, several upper layers start dry. Investigate how the configured procedures handle these
conditions and how saturation changes during the computation where diagnostics permit.

The groundwater-surface map represents the **uppermost wet active-cell head**, not the highest head
over all layers. Inspect individual layers before interpreting that map. Blank or masked
dry/inactive values are not zero heads. Dry upper cells can be physically reasonable; an entirely
dry interior column is a different concern and is rejected by the app's result check.

The app disables its analytical overlay and analytical error metrics when layers are added. Retain
the homogeneous single-layer reference from earlier stages for a qualified comparison, but do not
call every layered difference a solver error: vertical gradients and the depth-resolved formulation
can contribute. Check budgets and the layer results directly. Export the nine-run block.

- [ ] **Completed:** 6. Add the vertical direction in controlled stages <!-- task: step_06 -->

### 7. Extend the 3D model toward 250,000 cells

For the larger homogeneous 3D test, retain ten layers and enter **159 cells along x and y** in
cell-count mode:

**159 × 159 × 10 = 252,810 cells.**

This fits the 255,000-cell cap and retains a row exactly at the horizontal centre. By comparison, 51
× 51 × 10 has only 26,010 cells, while 501 × 501 × 10 would have 2,510,010 and is blocked.

Keep homogeneous K and the linear initial profile. Compare all three procedures with recorded
settings. Apply the same solution checks before interpreting runtime. If a run reaches an iteration
or time limit, save the diagnostic evidence. A later recovery attempt that changes one numerical
setting should be recorded as a new configuration rather than substituted into the original
comparison.

- [ ] **Completed:** 7. Extend the 3D model toward 250,000 cells <!-- task: step_07 -->

### 8. Combine 3D, heterogeneity, and alternative initial heads

Start this investigation at **51 × 51 × 10**, with the linear initial profile. Enable random K using
the same bounds and zone count as Step 4. Inspect the layer-dependent field and preserve this new
three-dimensional realization across the three engine runs.

Next compare the linear profile, random initial heads of 10–25 m with seed 24, and the uniform 0.1 m
start. Keep the grid and conductivity field fixed. In this multilayer model, the low uniform guess
lies below the bottoms of most upper layers, making its saturation implications different from the
one-layer case. Export the nine-run block.

For the final large-model challenge, repeat the heterogeneous comparison at **159 × 159 × 10**,
initially using the linear profile with all three procedures. Preserve the realization and export
it. Then test random and near-bottom initial heads on that same grid if continuing the full stress
investigation. Record failures and timeouts as well as accepted solutions; no particular engine is
expected to win in advance.

Changing the horizontal resolution with the same K settings, seed and layer count retains the
underlying zonal conductivity field, although it is sampled by a different grid. Changing the layer
count changes the vertical field. Random initial heads are generated cell by cell, so keeping their
seed while changing the grid does not preserve one physical initial-head pattern. Interpret each
comparison accordingly.

- [ ] **Completed:** 8. Combine 3D, heterogeneity, and alternative initial heads <!-- task: step_08 -->

### Record and assess your evidence

For every retained run, record the grid, conductivity realization, initial-head choice and seed
where relevant, engine/linear method, actual numerical settings, outcome, runtime, identified
iteration counts, budget discrepancy, and head/saturation observations. Include analytical head
errors only where that reference is applicable. Save the heads CSV and native listing for
discrepancies that need investigation.

Conclude with three separate statements:

1. **Efficiency:** Which accepted configurations required less computation for the tested cases?
2. **Robustness:** Which configurations completed the difficult starting-head and saturation cases, and under what settings?
3. **Solution quality:** What evidence supports the heads, saturation patterns, and water balance, and what remains uncertain?

Complete the six follow-up questions and use their feedback to identify any step that needs
revisiting.

## Optional exercise Do similar cell counts imply similar difficulty?

Use the homogeneous large-model results already collected in Steps 3 and 7. Compare:

| Model | Grid | Total cells |
| --- | --- | --- |
| A: horizontal 2D | 501 × 501 × 1 | 251,001 |
| B: full 3D | 159 × 159 × 10 | 252,810 |

Model B has only about **0.72% more total cells**. Predict whether that similarity should lead to
similar runtime or iteration counts, then test your prediction against the results.

### Your task

Prepare a one-page evidence summary containing:

1. A comparison table for both models and all three configured procedures: outcome, runtime, inner/outer counts where available, budget discrepancy, and the head/saturation checks used.
2. A short explanation of at least three reasons that equal total cell counts need not give equal computational difficulty. Consider connectivity and coupling, numbers of active unknowns, saturation changes, conditioning, and work within each iteration.
3. A statement explaining the different roles of the analytical reference: direct comparison for the homogeneous one-layer model, and a qualified reference for the layered model where the app disables its analytical error metrics.
4. A recommendation for the tested large-model cases, identifying which accepted configuration was efficient and which was robust. State any unresolved differences in the hydraulic results.

If small timing differences determine your recommendation, repeat those particular successful
comparisons three times. Do not compare a successful computation with a failure as if both had
delivered an acceptable solution.

These are different discretizations with different vertical behaviour. Their comparison investigates
why total cell count alone is insufficient; it is not a test in which only the algorithm changes.

### Optional transfer question

Choose one fixed heterogeneous 3D realization and assess how your recommendation changes between the
linear, random, and 0.1 m initial guesses. Use existing results where possible. What additional
observation would most strengthen or overturn your conclusion?

### Review criteria

A strong submission calculates the sizes correctly, identifies the actual numerical settings and
formulations, keeps physical and numerical changes distinct, evaluates solution quality before
speed, and limits its recommendation to the cases tested. A well-documented failure with a sound
explanation is useful evidence; an unsupported universal solver ranking is not.

- [ ] **Completed:** Optional exercise <!-- task: optional_exercise -->
