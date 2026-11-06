"""Editable teaching text. Keep explanation separate from model computation."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   INTRODUCTION: line 14
#   SOLVER_DETAILS: line 21
#   ASSUMPTIONS: line 63
#   REFERENCES: line 121
#   Presentation text. Stable keys keep the English interface ready for translation.: line 134
#   TEXT: line 135
#   CONCLUSION: line 167
# END CODE CONTENTS

INTRODUCTION = """
Explore how the grid, solver and stopping criteria affect steady groundwater-flow
results. Start with uniform recharge between two specified heads; then add layers,
a horizontal 2D grid or heterogeneous conductivity. Compare heads, convergence,
runtime and water balance.
"""

SOLVER_DETAILS = """
#### Models and methods

| Model | Solver choices | Main controls |
|---|---|---|
| MODFLOW-2005 | PCG or SIP | Head closure, iteration limits; PCG residual closure and relaxation; SIP acceleration |
| MODFLOW-NWT | Newton with GMRES or XMD | Head and flux closure, iteration limits, complexity preset |
| MODFLOW 6 | IMS with CG or BICGSTAB | Head and residual closure, iteration limits, complexity preset |

- **PCG**: preconditioned conjugate gradients. **SIP**: strongly implicit procedure.
- **NWT** uses Newton's method with the UPW flow package.
- **MODFLOW 6** uses NPF with Picard iteration in this app; both IMS methods
  remain available. Diagonal scaling is enabled initially.

#### Iterations and stopping criteria

- **Outer iterations** update the equations, including head-dependent
  conductances. **Inner iterations** solve the current linear system.
  SIP reports its own iteration count.
- **Head closure** limits the change between iterates (m), not the error
  relative to the exact solution. **Flow closure** tests a residual (m³/s);
  the norm differs between solvers. SIP has no separate flow-closure input.
- Inspect the water balance and, where available, the analytical head error
  as well as the convergence flag. Solver iterations are not physical time.

#### Settings in this app

- Head closures start at **1e-4 m**. Main closure values and iteration limits
  are retained when switching methods or presets within each MODFLOW model.
- **SIMPLE / MODERATE / COMPLEX** change NWT or IMS solution strategies;
  they do not guarantee accuracy or increase your chosen iteration limits.
- **Expert settings** expose advanced controls. NWT uses SPECIFIED when
  required to apply those edits; the remaining preset values are retained.

#### Solver documentation

[PCG](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/pcg.htm) ·
[SIP](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/sip.htm) ·
[NWT](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/nwt_newton_solver.html) ·
[MODFLOW 6 IMS](https://modflow6.readthedocs.io/en/6.7.0/_mf6io/sln-ims.html)
"""

ASSUMPTIONS = r"""
#### Analytical benchmarks

For steady 1D flow with uniform recharge $R$, constant conductivity $K$ and
specified heads $h_L$, $h_R$ at $x=0$, $L$:

**Confined aquifer** — constant thickness $b$, transmissivity $T=Kb$:

$$
T\frac{d^2h}{dx^2}+R=0,\qquad
h(x)=h_L+\frac{h_R-h_L}{L}x+\frac{R}{2T}x(L-x).
$$

**Unconfined aquifer** — horizontal bottom at zero, Dupuit approximation,
with the entire profile below the aquifer top:

$$
\frac{d}{dx}\left(Kh\frac{dh}{dx}\right)+R=0,\qquad
h(x)=\sqrt{h_L^2+\frac{h_R^2-h_L^2}{L}x+\frac{R}{K}x(L-x)}.
$$

If heads rise above the top, the app's convertible reference caps the saturated
thickness there; the square-root formula alone no longer applies.

The same **1D reference applies to horizontal 2D** when properties and boundary
conditions are uniform in y and the north/south boundaries have no flow.
Analytical comparisons are disabled for layered or heterogeneous models.

#### Numerical model

MODFLOW writes a water-balance equation for each unknown-head cell, couples it
to neighbouring cells and solves the resulting system for the heads. For this
app's homogeneous confined 1D case:

$$
C(h_{i-1}-2h_i+h_{i+1})+RW\Delta x=0,
\qquad C=\frac{KbW}{\Delta x}.
$$

- Heads belong to **cell centres**; the two end-cell heads are fixed by CHD.
  $L$ is their centre-to-centre distance, so $\Delta x=L/(N-1)$.
- Recharge enters the interior columns; other outer faces have no flow.
  The model is steady: no storage or unsaturated-zone flow is simulated.
- In convertible flow, conductance depends on saturated thickness, requiring
  nonlinear iteration. Initial heads are the numerical starting guess.

See the [MODFLOW-2005 formulation](https://pubs.usgs.gov/tm/2005/tm6A16/).

#### Suggested experiments

1. Compare solvers on the initial 11-cell model; inspect heads and water balance.
2. Change closure criteria or iteration limits; compare errors and runtime.
3. Refine the grid, then add unconfined flow, layers or random K. Distinguish
   discretization effects from incomplete solver convergence. For the uniform
   confined case, the quadratic reference has an exact central second difference
   at the nodes, so refinement mainly tests solver effort and precision.
"""

REFERENCES = """
- [MODFLOW-2005 technical report (Harbaugh, 2005)](https://pubs.usgs.gov/tm/2005/tm6A16/)
- [LPF layer types and conductance averaging](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/lpf.htm)
- [UPW layer types and upstream weighting](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/upw_upstream_weighting_package.htm)
- [MODFLOW 6 NPF layer types and conductance averaging](https://modflow6.readthedocs.io/en/6.7.0/_mf6io/gwf-npf.html)
- [PCG controls](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/pcg.htm) and [SIP controls](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/sip.htm)
- [MODFLOW-NWT solver](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/nwt_newton_solver.html) and [preset values](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/suggested_input_values_for_the.htm)
- [MODFLOW 6 IMS options and preset table](https://modflow6.readthedocs.io/en/stable/_mf6io/sln-ims.html)
- [MODFLOW 6 recharge placement](https://modflow6.readthedocs.io/en/6.7.0/_mf6io/gwf-rcha.html)
- [FloPy documentation](https://flopy.readthedocs.io/en/stable/)
"""


# EDIT: Presentation text. Stable keys keep the English interface ready for translation.
TEXT = {
    "spacing_steps": "The − / + buttons follow the preferred spacing sequence, skipping values that do not divide the boundary distance exactly. You can also type an integer. Fractional spacing remains available in grid studies.",
    "convergence_guides": "Dashed guides use the settings saved with this run. A separate annotation identifies criteria based on a different residual norm. Available iteration levels and native convergence flags are unchanged.",
    "input_intro": "Define the scenario, grid and solver, then run the model below. Hidden scenario values stay unchanged when you switch between limited and full settings.",
    "limited_hint": "These values are retained in limited mode. Enable **Show full settings** to edit them.",
    "full_settings_help": "Show or hide the additional scenario inputs. Limited mode keeps their last values and shows a read-only summary.",
    "complexity_title": "**Additional complexity settings and model preview**",
    "repeat_help": "Run the same configuration 1–10 times with identical inputs and realization. One comparison row represents all repetitions. Runtime is the median; all repetitions must succeed. Each native run has a fixed 120-second timeout.",
    "preview_caption": "**{aquifer}** · top {top:g} m · bottom {bottom:g} m. Grid: {grid}; {cells:,} cells. The preview follows the current input values. Section A–A′ passes through middle cell y {row}. Vertical dimensions are exaggerated.",
    "random_k_help": "Log-uniform, isotropic K in fixed physical zones, independent in each layer. **New realization** changes the field. Other edits and grid refinement retain the current realization.",
    "boundary_note": "Specified heads remain uniform on wet west/east faces. North, south and the aquifer bottom have no flow. Boundary cells wholly above the specified water level are inactive.",
    "solver_sticky": "Closure criteria and iteration limits are retained when switching presets or linear solvers. Each MODFLOW model remembers its own values.",
    "solver_units": "Head closure: m. Flow closure: m³/s; the tests differ between solvers.",
    "initial_grid_hint": "Before running: the orange end cells have specified (CHD) heads. MODFLOW will compute the heads in the nine interior cells.",
    "footer": "Developed by Thomas Reimann · TU Dresden, Institute for Groundwater Management / The Groundwater Project · 2026",
    "execution_heading": "Model execution and postprocessing",
    "model_summary": "- **Grid:** {grid}; **{cells:,} cells**; Δx = **{dx:g} m**, Δy = **{dy:g} m**.\n- **Aquifer:** {aquifer}; top = {top:g} m, bottom = {bottom:g} m. {conductivity} Recharge = {recharge:g} mm/year.\n- **Model / solver:** {solver}; {preset}. Head closure = {head:.2E} m{flow}; outer/SIP limit = {outer}{inner}.",
    "surface_note": "Layered display: the head in the **uppermost wet, active cell** of each column defines the groundwater surface (potentiometric head for confined flow). Dry overlying cells use that head only for display. Columns dry throughout remain blank; native layer heads and budgets are unchanged.",
    "head_map_title": "**Computed heads · groundwater surface (x–y)**",
    "map_empty": "Run the model to view the computed head surface.",
    "map_stale": "**Inputs have changed — rerun the model.** This grey map retains the previous computed result and its original geometry.",
    "map_note": "Heads come from the uppermost wet, active cell in each column. Dry-overlying cells use the head below; fully dry columns are blank. The dashed line marks section A–A′. Both horizontal axes use the same scale.",
    "comparison_heading": "Further run analysis and comparison",
    "study_heading": "Grid refinement experiment",
    "study_intro": "Use the same model-building code to compare grids and solver effort. The boundary-to-boundary length and layer count stay fixed. The confined quadratic reference has no nodal truncation error in exact arithmetic; unconfined results also depend on the engine’s conductance approximation and cell spacing.",
    "study_repeats": "Each selected variant runs on every chosen grid, using the **Number of runs** selected beside the main run name. Timings include startup and native output; they are not an isolated solver-speed ranking.",
    "study_variants": "Unedited variants use their initial settings. To change a variant, select its model and solver in the input section. Its last preset and settings are retained. Excluded variants are not run.",
    "study_geometry": "Each study keeps {layers} layer(s), aquifer geometry and boundary heads. Horizontal 2D uses Δx = Δy. The K-zone arrangement and current realization stay fixed.",
    "conclusion_heading": "Conclusion and references",
    "references_title": "**References**",
}

CONCLUSION = """
This app demonstrates the effects of different solver options and settings
across a range of groundwater models, from simple to complex. Compare
convergence, runtime, head errors and water balance to judge the results.
Grid refinement helps distinguish discretization effects from incomplete
solver convergence. A successful convergence flag is one part of that
assessment; the physical plausibility and diagnostics matter as well.
"""
