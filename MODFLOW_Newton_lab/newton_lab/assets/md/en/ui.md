## title
ModFlow Newton Lab
## version
Review version {version} · from steady flow to pumping, injection and recovery
## model_and_run
1 · Model & run
## results
2 · Results
## run_history
Last ten runs
## mode
Interface mode
## easy
Easy
## expert
Expert
## transient
Transient simulation
## presets
**Starting configurations**
## preset_help
Apply a complete physical starting configuration. This resets the grid, hydraulic properties, boundaries, well and observation point. Solver settings are retained. Use the instructions below to select steady or transient operation.
## preset_confined
Restore requested initial model
## preset_unconfined
Use unconfined teaching preset
## tab_parameters
Parameters
## tab_boundaries
Boundaries & well
## tab_grid
Grid & time
## tab_observations
Observations
## tab_solver
Numerical engines
## confined
Confined aquifer
## conductivity
Hydraulic conductivity K (m/s)
## ss
Specific storage Sₛ (1/m)
## sy
Specific yield Sᵧ (–)
## vertical_ratio
Vertical / horizontal conductivity (–)
## storage_help
Confined storage is S = Sₛ × thickness. Specific yield governs water-table drainage in convertible cells; selecting convertible cells does not guarantee that the aquifer is initially unconfined.
## heterogeneity
Add a rectangular conductivity zone
## k_factor
Conductivity multiplier within the zone
## zone_help
The zone spans all layers. Outside the zone, the specified K applies. Keep the CHD columns outside the zone for a clear boundary comparison.
## left
Left CHD head (m)
## right
Right CHD head (m)
## recharge
Recharge (mm/year)
## well_enabled
Well active
## combined
Combined pumping → injection → recovery
## combined_transient_only
The combined pumping/injection sequence is available in transient mode.
## injection
Injection well (off = pumping well)
## pumping_lps
Pumping magnitude (L/s)
## injection_lps
Injection magnitude (L/s)
## cell_x
Cell number · x-direction
## cell_y
Cell number · y-direction
## cell_x_short
Cell x
## cell_y_short
Cell y
## layer
Layer
## centre_well
Place well at grid centre
## well_help
Enter positive magnitudes. Internally, pumping is negative and injection positive. The well occupies one horizontal cell and penetrates the aquifer. With several layers, flow is split in fixed proportions by initial saturated thickness; this is not a multi-node borehole model.
## pumping_days
Pumping duration (days)
## injection_days
Injection duration (days)
## rest_days
Recovery / rest (days)
## ncol
Cells in x-direction
## nrow
Cells in y-direction
## cell_size
Cell width (m)
## top
Aquifer top (m)
## top_help
Aquifer bottom is fixed at 0 m in unconfined mode. Enter a positive aquifer-top elevation; the total thickness is top minus 0 m.
## thickness
Aquifer thickness (m)
## nlay
Number of equal-thickness layers
## grid_help
The first and last x-columns are CHD reservoirs. The other sides and the aquifer base are no-flow boundaries. Plots start at the first cell centre; cell numbers start at 1. CHD heads act at cell centres.
## inactive
Add an inactive rectangular block
## steps
Time steps per transient stress period
## multiplier
Time-step multiplier
## time_help
Each stress period starts with a short time step; successive steps grow by the multiplier. All time steps are saved. The initial steady-state bookkeeping second is removed from plotted time and cumulative budgets.
## obs_count
Number of observation points
## observation_help
Observations report the head of the selected model cell. OBS1 starts one 100 m cell east of the well. After changing the grid or moving the well, check the observation positions and distances.
## place_observation
Place OBS1 one cell beside the well
## observation_name
Name
## engines
Engines to run
## solver_help
Select one or several engines. A run uses identical physical inputs and time discretization for every selected engine. Engine-native wetting, storage discretization and flow-reduction algorithms may still differ.
## easy_settings
Closure criteria and iteration limits are in Numerical solver. Enable Expert settings for wetting and Newton options.
## expert_retained
Previously selected layers and heterogeneity remain active when expert controls are hidden.
## locations_adjusted
Some cell numbers were moved inside the reduced grid. Check the well, zone and observation positions before running.
## zone_x_start
First cell · x
## zone_x_end
Last cell · x
## zone_y_start
First cell · y
## zone_y_end
Last cell · y
## head_close
Head-change tolerance (m)
## flow_close
Flow / residual tolerance (m³/s)
## outer_limit
Maximum outer iterations
## inner_limit
Maximum inner iterations
## rewet
Enable rewetting (LPF or MF6 Picard)
## wetdry
Wetting threshold (m)
## damping
PCG damping factor
## nwt_method
NWT linear method
## ibotav
NWT bottom-cell correction IBOTAV
## flow_reduction
Pumping-reduction fraction of cell thickness
## newton
MF6 Newton formulation for convertible cells
## timeout
Native execution timeout (s)
## instructions
**Guided sessions · instructions & checklists**
## confined_sessions
Sessions 1–4 · confined
## unconfined_sessions
Sessions 5–8 · unconfined
## open_instructions
Open instructions in a new tab
## unknown_document
Unknown instruction document.
## document_hint
Instructions only · completion marks belong to this browser session. Use the main app tab to change inputs and run models.
## checklist_progress
Completed steps: {completed} / {total}
## checklist_item_help
Mark this step complete. This does not change or execute the model.
## theory
**Physical assumptions & analytical references**
## model_summary
{nx} × {ny} cells at {dx:g} m → {lx:g} × {ly:g} m · {layers} layer(s) · top {top:g} m · bottom {bottom:g} m
## convertible_confined
Both CHD heads are above the aquifer top. Convertible cells therefore start in a confined state. Use the unconfined preset or lower the heads to investigate a water table within the aquifer.
## preview
**Model preview**
## boundary_check
**Pumping scale & boundary influence**
## boundary_values
For the initial local thickness and storage: **T = {transmissivity:.3g} m²/s**, **S = {storage:.3g}**. The nearest boundary is **{distance:g} m** from the well. At **{days:g} days**, the infinite-aquifer estimate at **{spacing:g} m** is **{drawdown_100m:.3g} m** of head change. The absolute sum of the four first-image contributions at the well is approximately **{image_sum:.3g} m** ({ratio_pct:.2f}% of that observation response).
## boundary_help
Groundwater diffusion has no sharp front: boundary influence is never exactly zero. This first-image screening estimate helps judge whether the early response is approximately independent of the boundaries. Verify by enlarging the domain while keeping the same cell size, hydraulic properties and well/observation offsets. The nearest-boundary infinite-aquifer response can be nonzero even when the reflected effect near the well is small. Longer recovery periods and lower storage may show appreciably more boundary influence.
## boundary_influence
The screening estimate exceeds 1%. Consider a larger domain or explicitly investigate boundary effects. Lowering the pumping rate reduces absolute drawdown but does not change hydraulic diffusivity.
## boundary_approximation
This screen assumes homogeneous linear flow and is only qualitative for convertible cells or conductivity contrasts.
## missing_engines
Missing executable(s): {engines}. From the extracted app folder run `python install_engines.py`, or place your native executables in `bin`. See README.md for executable names and environment overrides.
## select_engine
Select at least one numerical engine.
## run
Run selected model(s)
## running
Running {engine}…
## stale_results
Model inputs or solver settings have changed. The previous plots are hidden; run the updated model to generate current results. Run history and the previous computation remain available for comparison after the new run.
## inspect_engine
Inspect current result
## result_identity
Run {run} · {engine}
## run_failed
This run did not produce validated converged results: {reason}
## convergence
Convergence
## converged
Converged
## failed
Failed / not converged
## runtime
Native runtime
## budget_error
Final budget discrepancy
## cell_counts
Declared active cells: {active} · wet / valid at final time: {wet} · dry: {dry} · inactive: {inactive}
## comparison
**Compare with the previous computation**
## no_previous
Run a second computation to compare head histories and water budgets.
## previous_identity
Previous computation: run {run} · {engine}. Solid/dashed lines belong to the current run; dotted lines or black marks show the previous run.
## changed_parameters
Changed inputs:
## compare_heads
Overlay previous head histories
## compare_budget
Overlay previous water balance
## locations_differ
Observation or well coordinates differ. Head-history overlay is disabled to avoid comparing different locations as if they were identical.
## regimes_differ
Steady and transient budgets use different displays; their overlay is disabled.
## spatial_heads
Heads · map & cross-section
## snapshot_choice
Displayed time
## last
End of model run
## periods
End of stress periods
## all_times
Any saved time
## snapshot_time
Snapshot
## days
days
## baseline
Initial steady state · no well
## steady
Steady state
## pumping
Pumping
## recovery
Recovery / rest
## snapshot_note
Spatial plots show t = {day:.5g} days after the initial steady state.
## section_axis
Cross-section direction
## section_position
Cross-section cell number
## surface_help
The map uses the uppermost wet-cell head in each column. It represents the water table where the head lies below the aquifer top; heads above the top represent a potentiometric surface. Entirely dry or inactive columns are pale red.
## show_steady_analytical
Overlay the 1-D steady recharge solution
## confined_below_top
Some computed heads are below the aquifer top although the confined formulation is selected. The numerical model still uses the full thickness; interpret this as a mathematical confined reference or switch to convertible cells for dewatering.
## heads_over_time
Heads through pumping, injection & recovery
## well_cell_note
WELL, WELL2 and WELL3 show the uppermost wet-cell head at each configured well, not the water level in a borehole.
## select_points
Points to plot
## drawdown
Show drawdown from each run's initial head
## show_theis
Overlay analytical reference at observation points
## theis_help
Theis assumes an infinite, homogeneous aquifer and constant transmissivity/storage. Shutdown is represented by superposition. Compare head change from the numerical pre-pumping baseline. The grid resolves the near-well response only approximately, especially at one-cell distance.
## theis_recharge
The analytical reference does not represent recharge. Set recharge to 0 for the intended analytical comparison. In strictly linear confined flow, the steady recharge background can cancel when considering drawdown; this does not remove the other Theis assumptions.
## unconfined_analytical
For initially unconfined observations, the overlay uses Sᵧ and a Jacob/Dupuit drawdown correction. This is an approximation, not a full delayed-yield solution. Use small drawdown relative to saturated thickness. Recovery is approximate. Curves are masked if the correction becomes invalid or the head reaches the aquifer roof; an initially confined observation uses Sₛ × thickness instead.
## analytical_unavailable
The analytical well overlay is available for one well in a regular, homogeneous scenario.
## water_balance
Water balance
## budget_sign
Positive values enter the groundwater system; negative values leave it. Storage IN is release from storage; storage OUT is accumulation. Solid = IN, dashed/hatched = OUT. Flow components are actual native budget flows.
## cumulative
Show cumulative volumes
## budget_terms
Budget components
## cumulative_help
Rate curves show each solved end-step flow over its own time interval. Cumulative curves integrate those rates from t = 0 and exclude the initial steady-state bookkeeping step. CSV rate columns use m³/s; cumulative columns use m³.
## reduced_well
The total actual well flow differs from the requested total in at least one displayed model/time step. Dry-cell deactivation or automatic pumping reduction may explain this. Inspect the native listing and well-rate table.
## well_rates
Requested and actual well rates · all wells combined
## requested_lps
Requested (L/s)
## actual_lps
Actual (L/s)
## downloads
**Download results & native model files**
## download_heads
Download heads over time · CSV
## download_budget
Download complete water balance · CSV
## download_config
Download model configuration · JSON
## prepare_archive
Prepare native model ZIP
## download_archive
Download native model ZIP
## download_listing
Download native listing
## native_log
**Native console output · final 12,000 characters**
## history_help
✓ converged · ✗ failed or timed out. Native iteration totals differ in meaning between engines. Time is native execution only. ¹Active counts the input domain; MF2005 can deactivate dry cells during a run. Up to ten engine runs are retained.
## hist_run
Run
## hist_engine
Engine
## hist_method
Solver
## hist_status
State
## hist_active
Active¹
## hist_wet
Wet
## hist_dry
Dry
## hist_outer
Outer
## hist_inner
Inner
## hist_runtime_s
Time (s)
## hist_discrepancy_pct
WB discrep. (%)
## hist_max_discrepancy_pct
Max |WB| (%)
## download_history
Download run history · CSV
## references
**References & numerical implementation**
## preview_title
Plan view · model grid
## log_k
log₁₀ K (m/s)
## head_m
Head (m)
## potentiometric
Potentiometric surface
## water_surface
Uppermost wet-cell head
## well
Well
## chd
CHD cells
## section
Cross-section
## dry_inactive
Dry / inactive
## x_m
x (m)
## y_m
y (m)
## elevation_m
Elevation (m)
## analytical
Analytical reference
## cross_title
Cross-section · {axis}-direction · cell {number}
## time_title
Head response at well and observations
## previous
Previous run
## time_days
Time (days)
## drawdown_m
Drawdown (m; negative = rise)
## budget_title
Groundwater budget · IN / OUT
## volume_m3
Cumulative volume (m³)
## flow_lps
Flow (L/s)
## term_chd
CHD
## term_wel
Well
## term_rch
Recharge
## term_sto
Storage
## in
IN
## out
OUT

## phase_injection
Injection
## timed_out
Timed out
## large_discrepancy
The native solver terminated, but the absolute budget discrepancy exceeds 0.1% in at least one saved step. Inspect the budget and consider tighter convergence criteria before interpreting the result.

## show_complexity
Enable additional model complexity
## scenario_panel
**Parameters for the scenario**
## show_full_settings
Show full settings
## confined_help
On: aquifer top is 0 m; enter its thickness. Off: aquifer bottom is 0 m; enter its top. Hydraulic parameters and CHD heads are retained.
## retained_parameters
K = **{conductivity:.2e} m/s**  
Sₛ = **{ss:.2e} 1/m** · Sᵧ = **{sy:g}**  
Top = **{top:g} m** · thickness = **{thickness:g} m**
## limited_settings_help
Enable Show full settings or Expert settings to edit these parameters. Hiding the controls retains their values.
## geometry_preserved
Changing the formulation retains the elevations and boundary heads. The starting configurations below provide complete confined and unconfined examples.
## spatial_panel
**Temporal and spatial discretization**
## solver_panel
**Numerical solver**
## solver_identity
**Model and solver**
## settings_engine
Settings for
## pcg_method
LPF · PCG
## ims_method
NPF / STO · IMS
## solver_closure
**Closure criteria**
## solver_iterations
**Iteration limits**
## expert_settings
Expert settings
## boundary_panel
**Boundary conditions**
## well_panel
**Well & stress periods**
## observation_panel
**Observation points**
## expert_solver_title
**Expert solver settings · {engine}**
## complexity_panel
**Additional model complexity**
## complexity_layers
**Layers & anisotropy**
## complexity_retained
Additional layers, conductivity zones or inactive cells remain in the model. Enable Expert settings to inspect or edit them.
## expert_strategy
**Solution strategy**
## expert_wetting
**Wetting & well flow**
## expert_execution
**Execution**
## preview_quantity
Preview display
## preview_empty
Empty cells
## preview_k
K zones
## preview_initial
Initial heads
## preview_layer
Plan-view layer
## preview_row
Section A–A′ · cell number y
## preview_plan
Horizontal grid · layer {layer} · {nx} × {ny} cells
## preview_section
Section A–A′ · cell y {row} · {layers} layer(s)
## preview_initial_help
Initial heads in this preview are the linear solver starting guess. For transient runs, the model first solves the no-well steady state; that solved baseline is available in Results.
## preview_coordinates
Plot distances start at the first cell centre, as in the Solver Lab. The CHD-centre separation is one cell width shorter than the full model extent. This plotting convention does not change model coordinates or observation distances.
## cell_head_lines
Cell-head lines
## cell_head_dots
Cell-head dots
## initial_heads
Initial heads
## cell_number_axis
Cell number along {axis} (first cell = 1)
## elevation_head_m
Elevation / hydraulic head (m)
## distance_first_centre
Distance from first cell centre (m)
## layer_view
Layer {layer}
## aquifer_confined
Confined aquifer
## aquifer_convertible
Convertible / unconfined aquifer
## status_closure
Head closure = {head:.2e} m
Flow closure = {flow:.2e} m³/s
## status_limits
Outer limit = {outer}; inner limit = {inner}
## status_iterations
Outer = {outer}; inner = {inner}
## status_runtime
Runtime = {seconds:.3f} s
## no_wet_heads
No wet, active heads in this view
## show_initial
Show initial heads
## show_previous_section
Show previous run
## initial_result_help
For transient runs, Initial heads shows the solved no-well steady state at t = 0. For steady runs, it shows the solver's initial head guess.
## section_comparison_unavailable
The previous section needs the same grid geometry, simulation regime and a saved result at the displayed time. Other parameter changes are allowed and are listed in the comparison section.
## section_comparison_identity
Hollow circles: run {run} · {engine} · t = {day:.5g} days. Each run uses its own active/dry-cell mask.
## plot_settings
**Expert plot settings**
## section_view
Cross-section head display
## surface_view
Groundwater / potentiometric surface
## selected_layer_view
Selected layer
## show_status
Show solver information
## head_map
**Computed heads · plan view**
## section_display_help
Dots show cell-centre heads; lines span each cell. MF2005 dry/inactive solver cells are yellow with red cross-hatching; NWT dry/active solver cells are pale red. Grey hatching marks input-excluded boundary cells. The plan view uses the uppermost wet-cell head.
## k_zone_legend
K zones · conductivity (m/s)
## show_contours
Show head contours on map

## expert_visibility_help
Show layer subdivision, rectangular grids, conductivity heterogeneity and advanced solver/time controls inside their existing expanders. Hidden values remain active.
## grid_length
Model length / width in x / y (m)
## spacing_mode
Define cell size instead of cell count
## square_grid
Same cell count in x and y
## resolved_grid
{nx} × {ny} cells · Δx = Δy = {size:.6g} m · full extent {lx:.6g} × {ly:.6g} m
## spacing_geometry_note
Length / width is the full outer-edge model extent: L = N × cell size. CHD heads act at the first and last cell centres, separated by L − cell size. Check well and observation cells after changing the grid.
## grid_positive
Enter a positive model length and cell size.
## grid_nondivisor
The cell size must divide the full model length exactly. Change the size or length; the app does not round the grid silently.
## grid_count_range
Choose a discretization with 5–151 cells in each direction.
## retained_layers
Retained vertical discretization: {layers} equal-thickness layer(s). Enable Expert settings to subdivide the aquifer.
## temporal_settings
**Temporal discretization**
## well_boundary
**Well boundary**
## well_operation
Well operation
## pumping_well
Pumping well
## injection_well
Injection well
## combined_well
Combined pumping / injection
## k_mode
Hydraulic conductivity distribution
## uniform_k
Uniform K
## zone_k
Rectangular K zone
## random_k_field
Random K zones
## k_min
Minimum random K (m/s)
## k_max
Maximum random K (m/s)
## k_zones
Random zones per horizontal direction
## k_seed
Random-field seed
## new_realization
New K realization
## random_k_help
K is sampled uniformly in log space between the specified limits. Fixed physical zones are sampled at cell centres; layers receive independent values. The same seed and field are used by every engine. Changing display settings does not regenerate K. Select New K realization to change the seed.
## reference_engine
Reference engine
## compare_engines
Compare numerical engines
## comparison_engines
Other engines to compare
## engine_comparison_help
The selected engines are compared in sections, maps, head histories and water budgets. Only successful results from this computation can be compared. Spatial differences are other engine minus reference at the same saved time.
## one_engine_help
Select and run at least two numerical engines in Numerical solver to enable comparison.
## failed_engine_note
{engine} did not converge or did not produce validated output. It remains in the run-history table and is excluded from comparisons.
## failed_downloads
**Inspect a failed engine run**
## difference_engine
Engine for deviation map
## difference_title
{other} − {reference}
## difference_head_m
Head deviation (m)
## no_paired_heads
No paired wet heads
## wet_dry_difference
Different wet / dry state
## difference_help
Deviation = other engine − reference (m). Differences are calculated only where both engines provide a wet, active head. Shaded cells have no paired value; hatching marks a different wet/dry state. For multilayer models each surface uses its own uppermost wet-cell head.
## compare_time_engines
Compare selected engines in head histories
## compare_budget_engines
Compare selected engines in water balance
## reference_label
Reference
## unavailable_snapshot
{engine} has no compatible saved result at this time and is omitted from the spatial comparison.
## random_k_legend
K display class · geometric midpoint (m/s)
## download_engine_note
These downloads belong to {engine}. Select another reference engine to download its results.
## finer_spacing
Next finer preferred cell size that exactly fits the model distance.
## coarser_spacing
Next coarser preferred cell size that exactly fits the model distance.

## confined_geometry
Aquifer top = 0 m; bottom = −thickness.

## unconfined_geometry
Aquifer bottom = 0 m; thickness = aquifer top.

## grid_length_x
Model length in x (m)

## ncol_xy
Number of cells in x / y direction

## well_count
Number of wells

## well_heading
**Well {number}**

## well_cell_heading
Cell number in x / y direction

## well_rates_heading
Pumping / injection magnitude (L/s)

## multiple_wells_help
Each well has its own rates and cell position. All wells follow the selected operation and the same stress-period durations. Use different cells for the wells.

## boundary_multi_help
Screening is shown separately for each well. These single-well estimates do not quantify combined interference or the full multi-well boundary response.

## dry_inactive_solver
Dry (inactive)

## dry_active_solver
Dry (active)

## dry_cells_label
Dry

## specified_inactive
Inactive (specified)
