# Shared interface text

The `##` headings are stable text keys; only their contents are displayed.

## spacing_steps

The − / + buttons follow the preferred spacing sequence, skipping values that do not divide the boundary distance exactly. You can also type an integer. Fractional spacing remains available in grid studies.

## convergence_guides

Dashed guides use the settings saved with this run. A separate annotation identifies criteria based on a different residual norm. Available iteration levels and native convergence flags are unchanged.

## input_intro

Define the scenario, grid and solver, then run the model below. Hidden scenario values stay unchanged when you switch between limited and full settings.

## limited_hint

These values are retained in limited mode. Enable **Show full settings** to edit them.

## full_settings_help

Show or hide the additional scenario inputs. Limited mode keeps their last values and shows a read-only summary.

## complexity_title

**Additional complexity settings and model preview**

## repeat_help

Run the same configuration 1–10 times with identical inputs and realization. One comparison row represents all repetitions. Runtime is the median; all repetitions must succeed. Each native run has a fixed 120-second timeout.

## preview_caption

**{aquifer}** · top {top:g} m · bottom {bottom:g} m. Grid: {grid}; {cells:,} cells. The preview follows the current input values. Section A–A′ passes through middle cell y {row}. Vertical dimensions are exaggerated.

## random_k_help

Log-uniform, isotropic K in fixed physical zones, independent in each layer. **New realization** changes the field. Other edits and grid refinement retain the current realization.

## boundary_note

Specified heads remain uniform on wet west/east faces. North, south and the aquifer bottom have no flow. Boundary cells wholly above the specified water level are inactive.

## solver_sticky

Closure criteria and iteration limits are retained when switching presets or linear solvers. Each MODFLOW model remembers its own values.

## solver_units

Head closure: m. Flow closure: m³/s; the tests differ between solvers.

## initial_grid_hint

Before running: the orange end cells have specified (CHD) heads. MODFLOW will compute the heads in the nine interior cells.

## footer

Developed by Thomas Reimann · TU Dresden, Institute for Groundwater Management / The Groundwater Project · 2026

## execution_heading

Model execution and postprocessing

## model_summary

- **Grid:** {grid}; **{cells:,} cells**; Δx = **{dx:g} m**, Δy = **{dy:g} m**.
- **Aquifer:** {aquifer}; top = {top:g} m, bottom = {bottom:g} m. {conductivity} Recharge = {recharge:g} mm/year.
- **Model / solver:** {solver}; {preset}. Head closure = {head:.2E} m{flow}; outer/SIP limit = {outer}{inner}.

## surface_note

Layered display: the head in the **uppermost wet, active cell** of each column defines the groundwater surface (potentiometric head for confined flow). Dry overlying cells use that head only for display. Columns dry throughout remain blank; native layer heads and budgets are unchanged.

## head_map_title

**Computed heads · groundwater surface (x–y)**

## map_empty

Run the model to view the computed head surface.

## map_stale

**Inputs have changed — rerun the model.** This grey map retains the previous computed result and its original geometry.

## map_note

Heads come from the uppermost wet, active cell in each column. Dry-overlying cells use the head below; fully dry columns are blank. The dashed line marks section A–A′. Both horizontal axes use the same scale.

## comparison_heading

Further run analysis and comparison

## study_heading

Grid refinement experiment

## study_intro

Use the same model-building code to compare grids and solver effort. The boundary-to-boundary length and layer count stay fixed. The confined quadratic reference has no nodal truncation error in exact arithmetic; unconfined results also depend on the engine’s conductance approximation and cell spacing.

## study_repeats

Each selected variant runs on every chosen grid, using the **Number of runs** selected beside the main run name. Timings include startup and native output; they are not an isolated solver-speed ranking.

## study_variants

Unedited variants use their initial settings. To change a variant, select its model and solver in the input section. Its last preset and settings are retained. Excluded variants are not run.

## study_geometry

Each study keeps {layers} layer(s), aquifer geometry and boundary heads. Horizontal 2D uses Δx = Δy. The K-zone arrangement and current realization stay fixed.

## conclusion_heading

Conclusion and references

## references_title

**References**
