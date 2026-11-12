# Teacher notes for Experiment 2

## Intent and scope

This is a guided investigation of vertical discretization, drying/rewetting behaviour, heterogeneous
conductivity, and initial guesses in a steady-state model. It follows Thomas's dictation and retains
51 horizontal cells, an unconfined aquifer top of 30 m, and comparison of MODFLOW-2005, MODFLOW-NWT,
and MODFLOW 6.

The student-facing hypothesis is conditional: NWT may be more robust when saturation changes create
numerical difficulties. The exercise must not require NWT to win or require any particular solver to
fail. Runtime, robustness, and hydraulic accuracy are distinct outcomes.

## Analytical verification and its limits

Experiment 1 has been updated separately to make numerical–analytical comparison explicit. It now
asks students to compare heads at matching cell centres, record RMSE and maximum absolute error, and
distinguish verification of an idealized numerical problem from validation of a field model.

The current app calculates both RMSE and maximum analytical head error over interior columns,
excluding CHD columns. Its head-error plot includes the boundary endpoints. Analytical output is
available only for a homogeneous single layer; adding layers or enabling random K disables it.

For Experiment 2, the single-layer homogeneous unconfined case is therefore the supported analytical
benchmark. With bottom zero and the entire profile below top 30 m, the reference satisfies:

`h(x)^2 = h_left^2 + (h_right^2 - h_left^2) x/L + (R/K) x (L-x)`.

The table in the instructions was calculated with L = 5,000 m, K = 1e-4 m/s, recharge 0.150/(365.25
× 86,400) m/s, and end heads 18/16 m. The calculated maximum is approximately 24.2497 m, below the
specified top. These are reference calculations, not native MODFLOW results.

Identical material properties in all numerical layers do not introduce geological heterogeneity, but
a vertically resolved model can represent vertical gradients and flow resistance. The
depth-integrated Dupuit reference can therefore be useful as an approximation without being an exact
solution of the layered problem. The instructions retain the requested comparison through the
reference table and saved baseline analytical heads. They call the difference a difference from the
1D reference and keep it separate from numerical solver error.

For heterogeneous K, the app's homogeneous reference is inapplicable. This does not imply that no
heterogeneous groundwater problem can have an analytical solution; it is a statement about this
particular reference and model.

## Layering and saturation

The app permits 2–50 equal-thickness layers when **Add layers** is active. The proposed 3, 10, and
30 layers correspond to 10, 3, and 1 m thickness across the fixed 0–30 m interval. At 51 columns and
one row, their geometric cell counts are 153, 510, and 1,530. These are total grid cells, including
CHD and inactive boundary cells, not counts of unknown heads.

The horizontal 2D toggle must remain off. Otherwise the exercise also adds 51 rows, changes the
horizontal domain, and introduces another experimental factor.

A convertible cell with head between bottom and top retains positive saturated thickness. A dry
model cell has no represented saturated thickness, but the real porous material need not contain
zero water. This app has no general unsaturated-flow equation, moisture-retention model, or
transient drainage history.

Drying/rewetting during outer iterations describes the numerical search for equilibrium. It is not
the physical advance of time. A final dry-cell plot does not prove repeated wet/dry cycling; that
assertion requires suitable iteration output or listing evidence. Oscillating residuals or head
changes may suggest a cause but do not identify it uniquely.

## Verified flow formulations and wetting settings

The source activates special wetting controls when the model is unconfined and has more than one
layer:

| Configuration | Verified implementation |
| --- | --- |
| MODFLOW-2005 / PCG | Convertible LPF layers; LAYWET=1, WETDRY=-0.01, WETFCT=0.5, IWETIT=1, IHDWET=0. Negative WETDRY selects rewetting from below. |
| MODFLOW-NWT / GMRES | Convertible UPW layers with Newton's native treatment of conductance changes; LPF wetting controls are not assigned to UPW. |
| MODFLOW 6 / IMS-CG | NPF/Picard, explicitly enabled REWET, the same below-only WETDRY and wetting values, and VARIABLECV DEWATERED. Newton options are not enabled. |

MF6's VARIABLECV setting matters: in the planned layered experiment the app updates vertical
conductance with the evolving saturation state. The exercise does not inadvertently leave MF6
vertical conductances fixed solely by the initial heads.

Cross-engine comparisons nevertheless change more than the inner linear method. LPF/NPF harmonic
conductance treatment and UPW upstream weighting differ. Identical input geometry and K need not
yield identical coarse-grid heads. NWT is not a general exact reference for the other two engines.

## Convergence and performance comparisons

The core uses one representative method per implementation: PCG, GMRES, and CG. SIP, XMD, and
BICGSTAB can be considered in a later extension. Students record the actual method and full
settings, retain each implementation's settings across the controlled comparisons, and distinguish
outer from inner iteration counts.

All main head closures are set to 1e-4 m. NWT and IMS use a declared MODERATE preset for this draft;
their displayed iteration limits and flow thresholds must be recorded because session values persist
and a preset change does not necessarily reset them. The documented app flow defaults are 1e-4 m³/s
for PCG/IMS and 5e-3 m³/s for NWT. The residual norms differ, so matching numerical values alone
would not provide a rigorous matched-accuracy benchmark either.

The comparison concerns these recorded configurations. A defensible performance conclusion also
requires acceptable hydraulic diagnostics. A faster result with an inconsistent budget,
inappropriate saturation pattern, or unresolved head difference should not be ranked as superior
merely because it reports convergence. The app's success flag does not apply an additional
user-defined budget-discrepancy acceptance threshold.

Runtime measures the native process and includes startup, solution, and native output. Repetitions
use identical inputs and initial guesses; the median runtime is shown, while counts and errors come
from the last repetition. All repeats must succeed for an aggregate successful result. The app's
native-run timeout is 120 seconds; a timeout is an observed failure under that limit, not proof that
no solution exists.

## Random conductivity and reproducibility

The random-K generator uses log-uniform values between positive limits, fixed horizontal zones, and
independent values in each numerical layer. K is isotropic within each cell. The proposed settings
are the app's documented defaults: Kmin=1e-5 m/s, Kmax=1e-3 m/s, and 11 zones per direction.

The internal K seed starts at 42 and **New realization** increments it. The current UI has no direct
K-seed input. Students should preserve the current realization, retain generation settings, and
export the actual K array through the heads CSV. Switching engines with unchanged scenario settings
regenerates the same values.

Changing the layer count changes the vertical K array, even if the internal seed is unchanged. This
is why vertical refinement precedes random K, and the heterogeneity and initialization blocks retain
30 layers. A seed alone is not a complete specification of a physical random field.

The random-K field changes hydraulic properties and their spatial arrangement. A difference between
homogeneous and heterogeneous results can be a physical consequence, not evidence of numerical
instability. Gradients and vertical connections can change even when the displayed
uppermost-wet-cell profile looks smooth.

## Initial heads

The implemented choices are **Mean boundary head**, **Linear between boundaries**, **Specified
uniform head**, and **Random distribution**. A uniform 0.1 m value is permitted by the input; it is
not clipped to each layer bottom. CHD heads override the initial values at the boundaries.

The proposed random initial heads use the app's default 10–25 m range and editable seed 24. They are
independent per computational cell and are distinct from the random K realization. This may
introduce vertical as well as horizontal differences in the starting guess.

The low-start case is close to the overall aquifer bottom. It puts most upper layers initially below
their own bottoms; it is not equivalent to giving each layer 0.1 m of saturated thickness. The
optional 30 m uniform start makes all active interior layers initially wet while preserving inactive
upper boundary cells and imposed CHD heads.

For the same uniquely solvable problem with the relevant solution accessible, successful
calculations should agree within their numerical accuracy. Wetting restrictions, changes in
effective connectivity, or inconsistent convergence can complicate that expectation. Different final
heads must be investigated, rather than interpreted as a physical history effect in this
steady-state model.

## Interpreting outputs and recharge

Layered surface plots use the uppermost wet active cell head in a column, not the maximum head over
all layers. Layer-specific head output is needed to investigate vertical gradients. Native
dry/inactive values and convertible heads at or below cell bottom are masked; blank values must not
be treated as zero. Boundary cells wholly above the specified head are intentionally inactive.

Recharge is zero on the boundary columns. MODFLOW-2005/NWT use NRCHOP=3; MF6 uses RCHA without
FIXED_CELL. Each engine applies its native routing as cells become dry or inactive. Identical
prescribed recharge arrays are not sufficient evidence that recharge is delivered to the same layer
in every engine. The instructions ask students to inspect actual recharge delivery, budgets, and
saturated connectivity.

Compare numerical heads at matching coordinates and layers where both values are meaningful, but
separately inspect cells with different wet/dry status. A comparison restricted to the shared wet
subset can otherwise conceal a material difference in the flowing domain.

## Run retention and practical organization

The current app retains ten run rows. The first block consists of one single-layer PCG reference and
nine layered comparisons: three engines at 3, 10, and 30 layers. Export before the three random-K
runs. Export those again before nine new initial-head runs. The mean-boundary initial-head reference
is the random-K block already saved.

Changing a layer count, K, or initial head does not reset the comparison; older rows are
nevertheless displaced when the ten-row limit is exceeded. Each repeated configuration counts as one
row. Students must retain the comparison CSV and any heads/listings needed for the report before
those rows disappear.

## Assessment alignment

| Question | Preparation focus | Follow-up focus | Objective |
| --- | --- | --- | --- |
| 1 | Vertical discretization and partial saturation | Saturation versus numerical cell status | 1 |
| 2 | Compared formulations and linear methods | Meaning of convergence versus failure | 2 |
| 3 | Applicability of analytical verification | Single-layer benchmark and layered reference limits | 3 |
| 4 | Fixed conductivity realization | Confounding from regenerated K | 4 |
| 5 | Numerical starting guesses and layer elevations | Low-start interpretation and reachable wet states | 5 |
| 6 | Complementary checks for drying models | Shared wet-domain comparisons and differing masks | 6 |

## Sources and verification

App-specific details were checked in the currently saved local and Streamlit Solver Lab packages,
particularly `core.py`, `inputs.py`, `settings.py`, `results.py`, `surfaces.py`, `README.md`, and
the English interface Markdown. The source audit supports the operational instructions; it does not
supply measured outcomes for the proposed runs.

Primary scientific references:

- Niswonger, R.G., Panday, S., and Ibaraki, M. (2011). [MODFLOW-NWT, a Newton formulation for MODFLOW-2005](https://pubs.usgs.gov/publication/tm6A37). USGS Techniques and Methods 6-A37. Describes continuous treatment of drying/rewetting nonlinearities and the Newton/UPW formulation.
- USGS. [Layer-Property Flow package](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/lpf.html). Convertible layers, dry-head markers, and wetting controls.
- USGS. [Upstream Weighting package](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/upw_upstream_weighting_package.html). Native UPW treatment and dry-output conventions.
- MODFLOW 6 documentation. [Node Property Flow package](https://modflow6.readthedocs.io/en/latest/_mf6io/gwf-npf.html). REWET, WETDRY, VARIABLECV, and convertible-cell settings.
- USGS. [Basic package starting heads](https://water.usgs.gov/nrp/gwsoftware/modflow2000/MFDOC/bas6.html). The role of steady-state starting heads and drying/rewetting qualifications.

The JSON format is the established iNUX array of `question`, Boolean `options`, `success`, and
`error`. Content and answer keys were reviewed independently. No native MODFLOW runs or live
expander rendering were performed for this teaching-content revision.
