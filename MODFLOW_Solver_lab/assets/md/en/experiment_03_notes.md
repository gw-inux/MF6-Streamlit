# Teacher notes for Experiment 3

## Purpose and sequence

This investigation separates additional computational dimensions from additional hydraulic
complexity. A homogeneous, isotropic square model can retain a one-dimensional steady solution;
heterogeneous conductivity or vertical discretization can introduce additional flow components.
Increased cell count, iteration count, runtime, robustness, and accuracy are different outcomes.

The sequence starts with an explicitly reset 11 × 1 × 1 unconfined model, bottom 0 m and top 30 m.
It proceeds through homogeneous 11², 21², 51², and 501² single-layer grids; a fixed 51²
heterogeneous field with linear, random, and 0.1 m initial guesses; and a homogeneous 51² model with
linear initial heads and then three and ten layers. The advanced extension uses 159² × 10, first
homogeneous and then heterogeneous. Investigate initial-head sensitivity at 51² × 10 before
transferring selected settings to the larger case. No particular engine is required to win or fail.

## Grid arithmetic, geometry, and budgets

The square-grid count is `N × N × number of layers`. The 255,000-cell cap includes prescribed-head
and inactive cells; it does not count only unknown active heads.

| Grid | Total cells |
| --- | --- |
| 11 × 11 × 1 | 121 |
| 21 × 21 × 1 | 441 |
| 51 × 51 × 1 | 2,601 |
| 501 × 501 × 1 | 251,001 |
| 51 × 51 × 3 | 7,803 |
| 51 × 51 × 10 | 26,010 |
| 159 × 159 × 10 | 252,810 |
| 501 × 501 × 10 | 2,510,010: exceeds the cap |

Direct cell-count mode accepts 159. Its spacing is 5,000/158 ≈ 31.6456 m; the main spacing widget
accepts integer metres, so use count mode. An odd count places the displayed middle row exactly at y
= 2,500 m.

The boundary-centre separation is L = 5,000 m, with Δx = Δy = Δ = L/(N−1). Cell edges extend half a
cell beyond the first and last centres; the square's actual side is L + Δ. North/south and the
bottom are no-flow. West/east CHD heads are uniform along wet boundary faces. Recharge is zero in
the two CHD columns, giving a recharge area of N(N−2)Δ² = L²−Δ². That area changes slightly with
refinement. The one-row baseline is only 1 m wide, so compare heads directly but account for width
before comparing total volumetric flows.

The optional 501² × 1 versus 159² × 10 exercise compares similar total counts, not equivalent
computational problems. Connectivity, vertical aspect ratios, wet/dry states, and the number of
unknowns can differ substantially.

## Analytical verification and spatial interpretation

For homogeneous, isotropic conductivity with geometry, recharge, and west/east heads independent of
y, the single-layer solution can be independent of y. The matching one-dimensional reference remains
applicable. Random initial heads change numerical guesses, not these steady physical assumptions.
Pronounced row differences should prompt checks of actual inputs, convergence, and sensitivity to
tighter criteria.

The analytical overlay is deliberately disabled when random K is enabled or more than one layer is
used. Homogeneous layering can resolve vertical gradients; its layer heads must not be labelled
errors against the depth-integrated reference. This restriction concerns the app's reference, not
all possible analytical solutions.

The main section uses the middle row. The error plot adds the minimum–maximum error envelope across
rows. Tabulated RMSE and maximum absolute error use all rows and interior x columns, excluding both
CHD columns; the plotted profile includes boundary endpoints. Agreement in one row does not verify
the complete field.

Layered surface views select the head in the uppermost wet active cell, not the maximum head across
layers. Examine native layer heads separately. Dry/inactive values and convertible heads at or below
cell bottom are masked; blank cells are not zero-head observations. The app provides head maps and
native budget diagnostics, not computed flow-vector maps.

## Formulations, wetting, and starting guesses

The three configurations compare MODFLOW-2005 LPF/PCG, MODFLOW-NWT UPW/Newton with GMRES, and the
app's current MODFLOW 6 NPF/Picard configuration with IMS-CG. MF6 Newton options are not enabled.
LPF/NPF harmonic conductance treatment and UPW upstream weighting can produce different coarse-grid
heads; an engine comparison changes more than the inner linear solver. The official LPF, NWT, and
NPF references describe these distinctions [1–3].

Special LPF/NPF wetting controls are enabled only for unconfined models with multiple layers:
rewetting from below, WETDRY = −0.01, WETFCT = 0.5, IWETIT = 1, and IHDWET = 0. MF6 additionally
uses VARIABLECV DEWATERED. These explicit rewetting controls are off for the single-layer phase. NWT
uses its own Newton/UPW treatment.

The uniform-head UI minimum is 0.1 m; validation also rejects a specified head ≤0. At bottom 0 m,
0.1 m gives positive initial saturated thickness in a single layer. It is not an exact-zero trial.
Positive CHD heads override the interior guesses. An unsupported zero-start thought experiment must
consider boundaries, recharge, connectivity, and native wetting treatment; universal failure cannot
be inferred from the interior guess alone.

Initial values are not clipped to individual layer bottoms. With three layers, linear 18→16 m
guesses lie below the upper layer's 20 m bottom. With ten layers, four upper layers start at or
below their bottoms. Adding layers therefore introduces wetting behavior as well as more cells.
These are steady-state numerical initial guesses, not a transient drainage history. Different final
states require investigation of convergence and accessible wet connections.

## Reproducible heterogeneity and initialization

Random K is log-uniform and isotropic within each cell, with fixed horizontal zones and independent
values in each layer. Defaults are 10⁻⁵–10⁻³ m/s and 11 zones per horizontal direction. The internal
seed starts at 42; **New realization** advances it. There is no editable K-seed widget. Preserve the
current realization and export the actual K array in the heads CSV.

Horizontal refinement samples the same zonal physical field when dimensionality, layer count,
bounds, zone count, and seed remain fixed. Changing layers or switching between one row and square
2D changes that field. Keep the heterogeneous engine and initial-head comparisons on a fixed grid.

Random initial heads are independent uniform values on the current computational array, defaulting
to 10–25 m and editable seed 24 under **Show full settings**. Unlike zonal K, they do not preserve
one spatial initial-head field when the grid changes. Fixed-grid engine comparisons and repeats
reproduce them. A random guess may help or hinder convergence; its effect must be observed.

## Numerical settings, timing, and quality checks

The app remembers each engine's numerical settings when switching engines, methods, or presets.
Record the actual values used. Fresh profiles initially use SIMPLE; switching presets does not
necessarily reset retained closure criteria or iteration limits.

| App starting criterion | PCG | NWT | IMS |
| --- | --- | --- | --- |
| Main head closure (m) | 10⁻⁴ | 10⁻⁴ | 10⁻⁴ |
| Flow closure (m³/s) | 10⁻⁴ | 5 × 10⁻³ | 10⁻⁴ |

IMS also starts with an inner head closure of 10⁻⁴ m. These are app defaults, not equivalent
accuracy specifications. Residual definitions, norms, and evaluation stages differ; equal numbers do
not establish matched stopping conditions [4–6]. Keep inner and outer iterations separate.

Assess convergence, analytical errors where applicable, native budgets/residuals, heads, and
saturation before comparing performance. A short failed run is not a fast successful solution. The
app's success flag does not impose an additional teacher-selected budget-discrepancy threshold, and
a printed 0.00% discrepancy does not prove exact balance.

Runtime measures the native process, including startup, solution, and native output; it excludes
model construction and plotting. Repeats use identical inputs. The displayed time is the median,
while counts and errors come from the last repeat; every repeat must succeed. The limit is 120
seconds per native execution. Begin exploratory cases with one repeat; repeat selected successful
configurations for timing comparisons. An admitted grid may still be impractical. A timeout does not
prove the problem has no solution.

## Run retention and assessment

Switching horizontal 2D on/off clears the individual comparison book; export the one-row baseline
first. Grid-count, layer, K, and initial-head changes retain runs, but only the latest ten
individual rows survive. A repeated configuration occupies one row. Export between blocks.

The automated study can retain all twelve summaries for four grids × three engines and provides a
study CSV; up to five studies are kept separately. Only the final native study run is exposed for
detailed inspection. Use individual blocks when students need every case's head map, heads CSV, or
listing.

The six preparation and six follow-up questions align as follows. Each question uses multiple
independently true/false options; feedback should support reasoning about all selected statements.

| Objective | Preparation question | Follow-up question and evidence |
| --- | --- | --- |
| O1: Explain y symmetry and reference applicability. | Q1: symmetric, homogeneous isotropic problem. | Q1: investigate row differences; check several rows and analytical errors. |
| O2: Distinguish cell count, work per iteration, and runtime. | Q2: square/layer scaling. | Q2: interpret equal iteration counts on 51² and 501². |
| O3: Compare recorded engine configurations fairly. | Q3: physical controls, formulations, and criteria. | Q3: solution quality, repeated timing, and inner/outer counts. |
| O4: Separate physical heterogeneity from numerical initialization. | Q4: broken y symmetry and frozen K. | Q4: distinguish random K from random starting heads. |
| O5: Interpret near-bottom guesses and boundary constraints. | Q5: small thickness and unchanged CHD heads. | Q5: 0.1 m evidence versus unsupported exact zero. |
| O6: Assess staged 3D extensions. | Q6: size, vertical heads, saturation, reference limits. | Q6: 3/10-layer counts, 255,000 cap, and hydraulic checks. |

## Sources and verification

App behavior was checked in the supplied source: `core.py` (`Scenario`, `build_model`,
`head_metrics`, `run_repeated`), `inputs.py`, `settings.py`, `results.py`, `studies.py`, `plots.py`,
`surfaces.py`, `README.md`, and English interface text. These checks substantiate controls and
interpretation, not measured solver outcomes. No live app or native MODFLOW executions were
performed for these notes.

Official references checked for the relevant numerical definitions:

1. USGS: [LPF package](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/lpf.html) — layer types, conductance averaging, wetting controls.
2. Niswonger, Panday, and Ibaraki (2011): [MODFLOW-NWT, a Newton formulation for MODFLOW-2005](https://pubs.usgs.gov/tm/tm6a37/) — Newton/UPW and drying nonlinearities.
3. MODFLOW 6.7.0: [NPF package](https://modflow6.readthedocs.io/en/6.7.0/_mf6io/gwf-npf.html) — convertible cells, REWET, VARIABLECV/DEWATERED.
4. USGS: [PCG package](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/pcg.html) — head/residual tests and iteration levels.
5. USGS: [NWT solver](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/nwt_newton_solver.html) — nonlinear criteria and solver controls.
6. MODFLOW 6.7.0: [IMS solution package](https://modflow6.readthedocs.io/en/6.7.0/_mf6io/sln-ims.html) — inner/outer criteria, norms, presets, and overrides.
