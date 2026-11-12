## Experiment 1 Getting started with the MODFLOW Solver Lab

## Practical investigation

Before each change, make a short prediction. After running the model, record what happened and
explain whether the result supports your prediction. A result that changes very little is also
evidence.

### Step 1 Configure the eleven-cell reference model

Choose **MODFLOW-2005** and **PCG**. Keep **Confined aquifer** switched on. Open **Show full
settings** and check the following values; settings retained from an earlier session may differ.

| Setting | Reference value |
| --- | --- |
| Number of cells along x, including the two CHD cells | 11 |
| Boundary-to-boundary length | 5,000 m |
| Hydraulic conductivity | $1\times 10^{-4}$ m/s |
| Recharge | 150 mm/year |
| West / left boundary head | 18 m |
| East / right boundary head | 16 m |
| Confined aquifer thickness | 20 m |
| Starting-head distribution | Mean boundary head: 17 m in the interior |
| Head closure | $1\times 10^{-4}$ m |
| R closure | $1\times 10^{-4}$ m³/s |
| Maximum outer / inner iterations | 100 / 100 |
| Number of runs | 1 |

Keep expert settings off. The reference PCG preconditioner is the app's default modified incomplete
Cholesky option. Retain the same starting-head rule and other solver settings in the following
comparisons.

Locate the first and last cells. These are **CHD cells**: their hydraulic heads are prescribed. The
boundary exchange flows are calculated. The other nine cell heads are unknowns to be solved for.

The 5,000 m length is measured **between the centres of the two CHD cells**. For this grid, the
centre spacing is 500 m. Recharge is applied to the interior cells; the two CHD cells receive no
recharge in this app.

Give the run the name **A — 11 cells confined** and press **Run Model**.

- [ ] **Completed:** Step 1 Configure the eleven-cell reference model <!-- task: step_01 -->

### Step 2 Explore the results and post-processing

First check whether the calculation converged. Then explore these controls:

- **Cell-head dots** and **Cell-head lines**: relate the displayed heads to the numerical cells.
- **Show analytical solution**: compare the numerical heads with the reference for this idealized problem.
- **Show initial heads**: distinguish the numerical starting guess from the computed result. This display switch changes visibility, not the heads supplied to the solver.
- **Further run analysis and comparison**: locate the convergence status, **Outer**, **Inner**, **Time (s)**, head errors, and **WB discrep.**
- **Head errors, water balance and convergence diagnostics**: examine the head errors, boundary exchanges, recharge, cell residuals, and available convergence history. Check **Solver settings used for this run**.

Discuss these observations:

1. Do the two boundary-cell heads equal the prescribed values?
2. How does recharge influence the shape of the head profile?
3. What are the directions of exchange at the left and right boundaries?
4. Does the water balance support the convergence result?
5. How do the numerical heads compare with the analytical reference?

In the confined case, call the curve the **hydraulic-head profile** or **potentiometric profile**.
It is not the aquifer's water table.

The app reports boundary fluxes as positive **into the unknown-head region**. Discharge from that
region is therefore negative. Check the balance for the selected run. A displayed discrepancy of
0.00% is rounded and does not imply an exactly zero residual.

#### Compare the numerical and analytical solutions explicitly

The analytical solution provides an independent reference for this idealized mathematical problem.
Use it to assess the numerical result, rather than judging the smoothness of the plotted curve
alone.

1. Enable **Show analytical solution** and display the numerical **Cell-head dots**.
2. Compare the numerical and analytical heads at the **same cell-centre coordinates**. For a cell at $x_{i}$, the head difference is $e_{i}=h_{num}(x_{i})-h_{ana}(x_{i})$.
3. Record both **RMSE (m)** and **Max error (m)**. RMSE summarizes the typical size of the differences through their mean square; the maximum error identifies the largest absolute difference. The app calculates these metrics over the interior cells, excluding the two prescribed-head end cells.
4. Inspect the spatial head-error plot and decide whether an apparently coincident pair of head curves conceals small numerical differences. The fixed boundary heads agree by construction and do not, by themselves, establish the accuracy of the interior solution.
5. Repeat this comparison for the later homogeneous, single-layer runs. Ask whether tighter closure or a finer grid changed the reported errors as well as the runtime and iteration counts.

Agreement with the analytical reference supports **verification of the numerical solution under the
stated assumptions**. It does not establish that those assumptions and parameters describe a real
aquifer correctly. The confined and unconfined cases have different analytical references; use the
reference corresponding to the current formulation.

- [ ] **Completed:** Step 2 Explore the results and post-processing <!-- task: step_02 -->

### Step 3 Tighten head closure

In PCG, **head closure** limits the maximum head change during an iteration. **Residual closure**
limits the maximum absolute equation residual, expressed as a flow rate. Their units in this model
are metres and cubic metres per second, respectively. Both stopping tests must be satisfied; the
residual closure is not the percentage water-budget discrepancy.

Predict what will happen if the permitted head change becomes smaller.

1. Change **Head closure (m)** from $10^{-4}$ m to $10^{-5}$ m.
2. Keep **R closure (m³/s)** at $10^{-4}$ m³/s and retain all other settings.
3. Name the run **B — 11 cells tighter closure** and press **Run Model**.
4. Compare convergence, outer and inner iterations, runtime, head errors, and the head profile with run A. Use **Show previous run** for the profile comparison.
5. Restore head closure to $10^{-4}$ m before changing the grid.

A stricter head-change criterion may increase computational effort. It can also leave the iteration
counts unchanged if the calculation already meets it. The threshold is a stopping criterion; it is
not a guarantee that the final heads differ from the exact solution by less than that value.

- [ ] **Completed:** Step 3 Tighten head closure <!-- task: step_03 -->

### Step 4 Refine the confined grid to 51 cells

Change **Number of cells along x** from 11 to 51. Keep the 5,000 m boundary-centre distance and the
restored solver settings. The spacing is now 100 m and there are 49 unknown-head cells.

Predict the effects on the head profile, iteration counts, and runtime. Name the run **C — 51 cells
confined**, then compute it.

Compare C with A using the run table and **Run to inspect**. These runs have the same closure
criteria. The immediately previous run is B, so an overlay of C and B does not isolate the grid
change as cleanly as the A–C comparison.

Explain why more cells make the algebraic system larger while leaving the boundary-to-boundary
distance unchanged. Do not assume that the iteration count must rise in direct proportion to the
number of cells.

The analytical head profile is quadratic for this homogeneous confined case with uniform recharge.
The centred difference formula reproduces the second derivative of a quadratic exactly.
Consequently, heads at common grid nodes may already agree very closely on coarse and fine grids.
Here, refinement is particularly useful for investigating computational effort and numerical
precision.

**When comparing water budgets between grids:** the recharge rate remains fixed, but the total
recharge reported for the unknown-head region changes. This app excludes recharge from both CHD
cells, so the recharged length is $(N-2)\Delta  x=L-\Delta  x$: 4,500 m for 11 cells and 4,900 m for
51 cells. Compare recharge and boundary exchanges within each run before interpreting differences
between runs.

- [ ] **Completed:** Step 4 Refine the confined grid to 51 cells <!-- task: step_04 -->

### Step 5 Introduce unconfined conditions

Before changing the model, discuss:

> For this simple CHD-and-recharge problem, why is the confined formulation generally easier to solve
> than the unconfined formulation?

With fixed thickness $b$, confined transmissivity is $T=Kb$ and does not depend on the unknown head.
Where the water table lies between the bottom and the top, unconfined transmissivity is
$T(h)=K(h-z_{b})$. The coefficients therefore depend on the heads being calculated.

1. Keep 51 cells and MODFLOW-2005 / PCG.
2. Switch **Confined aquifer** off.
3. Enter **Aquifer top elevation (m)** = **30 m**.
4. Keep K, recharge, both boundary heads, the initial-head rule, and the solver controls unchanged.
5. Name the run **D — 51 cells unconfined** and press **Run Model**.
6. Compare D directly with C using **Show previous run** and the saved diagnostics.

Inspect whether the computed heads lie above the bottom and below the top. The aquifer top is a
geometric elevation; entering 30 m does not prescribe a water table at 30 m. For the reference
parameters, an entirely unconfined profile below this top is expected; verify it in your results.

**Account for the app's geometry:** the confined reference has a roof at 0 m and a bottom at −20 m.
In unconfined mode the bottom is fixed at 0 m, and the entered top is 30 m. Thus the toggle changes
the geometry and transmissivity representation as well as introducing head dependence. Interpret
differences in the computed heads in that context. The solution method remains PCG.

Record whether outer iterations, inner iterations, or runtime changed. Explain the results using
head-dependent saturated thickness, while recognizing that a simple unconfined model may still
converge quickly.

- [ ] **Completed:** Step 5 Introduce unconfined conditions <!-- task: step_05 -->

### Step 6 Refine the unconfined grid

Retain the unconfined setup with top 30 m. Run the following cases one at a time, retaining the same
K, recharge rate, heads, starting-head rule, and solver settings.

| Run | Total cells | Unknown-head cells | Spacing | Aquifer |
| --- | --- | --- | --- | --- |
| A | 11 | 9 | 500 m | Confined, reference closure |
| B | 11 | 9 | 500 m | Confined, tighter head closure |
| C | 51 | 49 | 100 m | Confined, reference closure |
| D | 51 | 49 | 100 m | Unconfined, top 30 m |
| E | 501 | 499 | 10 m | Unconfined, top 30 m |
| F | 5,001 | 4,999 | 1 m | Unconfined, top 30 m |

Name the new runs **E — 501 cells unconfined** and **F — 5001 cells unconfined**. After each run,
inspect convergence before interpreting its heads. If a run fails, record the failure and the native
diagnostic message; its available heads are not an accepted converged solution.

Use $\Delta  x=L/(N-1)$ to check the spacings. These refinements increase the number of unknowns in
the same 5,000 m boundary span. For 501 and 5,001 cells, the recharged lengths are 4,990 and 4,999
m, respectively.

For each run, retain the following observations, using the comparison table and **Download
comparison CSV** where helpful:

| Run | Converged? | Outer | Inner | Time (s) | Head at x = 2,500 m (m) | RMSE (m) | Maximum head error (m) | WB discrep. (%) | Explanation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A |  |  |  |  |  |  |  |  |  |
| B |  |  |  |  |  |  |  |  |  |
| C |  |  |  |  |  |  |  |  |  |
| D |  |  |  |  |  |  |  |  |  |
| E |  |  |  |  |  |  |  |  |  |
| F |  |  |  |  |  |  |  |  |  |

The middle coordinate occurs in all these grids; obtain its head from **Download heads CSV** if
needed. Do not substitute a different location when comparing heads.

The app times execution of the native MODFLOW program, including startup and native output. Very
short timings can vary for reasons unrelated to numerical difficulty. **Outer** and **Inner** count
different operations; neither represents elapsed physical time in the aquifer.

- [ ] **Completed:** Step 6 Refine the unconfined grid <!-- task: step_06 -->

### Step 7 Locate the other MODFLOW implementations and methods

Open **Details of the numerical solvers** and identify the choices below. This is a short
orientation task; the six main calculations above use MODFLOW-2005 / PCG throughout.

| MODFLOW implementation | Methods offered by this app | Flow formulation in this app |
| --- | --- | --- |
| MODFLOW-2005 | PCG or SIP | LPF; iterative updates of coefficients for convertible flow |
| MODFLOW-NWT | GMRES or XMD | UPW with a Newton formulation |
| MODFLOW 6 | IMS with CG or BICGSTAB | NPF with a Picard formulation |

Explain the distinction between selecting a MODFLOW implementation and selecting a solution method
within it. SIP has a head-change stopping criterion but no separate residual-closure input. Criteria
in different implementations are not automatically equivalent just because their numerical values
match. The current app uses Picard for MODFLOW 6; the availability of other formulations in MODFLOW
6 does not mean they are activated here.

- [ ] **Completed:** Step 7 Locate the other MODFLOW implementations and methods <!-- task: step_07 -->

### Complete the experiment

Complete the six follow-up questions, selecting **all correct answers**. Then write three sentences
explaining what you learned about grid size, nonlinear flow, and convergence criteria. Use your own
recorded observations as evidence.

## Optional exercise Explain an unexpected result

Choose one comparison from this experiment: A–B for head closure, A–C for confined grid refinement,
C–D for the aquifer formulation, or D–E–F for unconfined grid refinement.

Before running or revisiting that comparison, write down:

- What you predict will happen to outer iterations, inner iterations, and runtime.
- What you predict will happen to the head at x = 2,500 m.
- Which settings you will hold fixed.

Compare the prediction with the recorded result. Classify it as **supported**, **unsupported**, or
**inconclusive**, and explain your decision. If little changes, explain why this can be a valid
numerical outcome.

If the conclusion depends on a very small timing difference, set **Number of runs** to **3** and
repeat both configurations under comparable conditions. Use the app's median runtime and inspect its
timing range. The reported iteration counts and head errors belong to the last repetition, while the
convergence indicator requires all repetitions to succeed. Repeats use the same initial heads; the
preceding solution is not reused as a starting guess.

Finish with a short conclusion:

> Which observation tells you most about numerical difficulty, and which additional observation would
> you need before making a stronger claim?

Use **Download comparison CSV** to retain the results if you continue experimenting; the app keeps
only the latest ten run rows.

- [ ] **Completed:** Optional exercise <!-- task: optional_exercise -->
