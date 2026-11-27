<!-- key: title -->
MT3D – 2D/3D Transport Lab

<!-- key: intro_caption -->
Introductory illustration: an example plume and breakthrough curve. This illustration is independent of the current model inputs.

<!-- key: Model & run -->
1 · Model & run

<!-- key: Results & method comparison -->
2 · Results & method comparison

<!-- key: series_reset -->
A new comparison series has started because the input signal or model/source geometry changed. Previous runs were cleared.

<!-- key: grid_summary -->
Grid: {nx} × {ny} × {nz} cells. Actual cell width: Δx = {dx:.3f} m; Δy = {dy:.3f} m; Δz = {dz:.3f} m.

<!-- key: velocity_summary -->
Homogeneous reference pore velocity: {velocity:.4f} m/day.

<!-- key: source_bounds -->
x = {x0:.2f}–{x1:.2f} m; y = {y0:.2f}–{y1:.2f} m; z = {z0:.2f}–{z1:.2f} m.

<!-- key: source_snap_hint -->
The source occupies the selected cells. Changing resolution can change its realised dimensions. Cell-width input preserves the total model extent and reports the actual uniform spacing.

<!-- key: input_error -->
Please correct the highlighted model settings before running.

<!-- key: missing_executables -->
Required programs missing: {names}. Provide compatible executables in the application or repository `bin/` folder. For local setup: `python setup_executables.py`.

<!-- key: label_placeholder -->
Automatic: 01 TVD / Pulse (heterogeneous: / het.)

<!-- key: history_full -->
Ten runs are stored. Remove a run or clear the series to continue.

<!-- key: running -->
Running MODFLOW, MT3D and optional MODPATH…

<!-- key: run_success -->
Run completed. The latest run is now displayed.

<!-- key: run_failed -->
This run could not be completed and was not added to the comparison.

<!-- key: changed_source_footprint -->
Grid refinement changed the realised source footprint. Check Source box in the extended table when comparing resolution.

<!-- key: nearest_time -->
{name}: nearest saved time {time:.3f} days (displayed run: {target:.3f} days).

<!-- key: no_comparison_time -->
{name}: no output at {time:.3f} days; omitted.

<!-- key: evaluating_reference -->
Evaluating the analytical reference…

<!-- key: export_hint -->
The run archive includes model inputs, logs, concentration/head arrays, mass diagnostics and particle data. Particle arrival details remain available in the export.

<!-- key: no_runs -->
Run the baseline pulse experiment to view the plume, profiles, observation curves and method comparison.

<!-- key: footer -->
MT3D 2D/3D Transport Lab · v{version} · Working version for live teaching · Developed by Thomas Reimann · TU Dresden · The Groundwater Project

<!-- key: transient_hint -->
The original flow field first equilibrates; the right head changes at t = 0.

<!-- key: expert_flow_hint -->
Enable expert settings to edit flow-solver tolerances and iterations.

<!-- key: stochastic_hint -->
Fixed seed = reproducible zones. K and Ss are sampled uniformly in log space; porosity is sampled uniformly. The same realisation is retained on grid refinement.

<!-- key: zones_hint -->
Rectangular zones select cells by their centres; later rows override earlier rows. Layer numbers start at 1.

<!-- key: observation_hint -->
Observation curves use the containing cell. Locations can be changed without rerunning stored models.

<!-- key: output_hint -->
Includes t = 0 and the final time. This controls concentration output for plots and export.

<!-- key: preset_homogeneous -->
Homogeneous

<!-- key: preset_lens -->
Low K lens

<!-- key: preset_channel -->
High K channel

<!-- key: preset_barrier -->
Partial low K barrier

<!-- key: preset_stochastic -->
Stochastic zonation

<!-- key: preset_custom -->
Custom rectangles

<!-- key: preset_hint_lens -->
Central lens: K = 0.01 × background K; full model depth.

<!-- key: preset_hint_channel -->
Longitudinal channel: K = 10 × background K; full model depth.

<!-- key: preset_hint_barrier -->
Partial cross-flow barrier: K = 0.01 × background K; a bypass remains.

<!-- key: signal_pulse -->
Pulse / block input

<!-- key: signal_continuous -->
Continuous input

<!-- key: signal_dirac -->
Dirac / instantaneous slug

<!-- key: signal_short_pulse -->
Pulse

<!-- key: signal_short_continuous -->
Cont

<!-- key: signal_short_dirac -->
Dirac

<!-- key: Concept, assumptions and equations -->
Concept, assumptions and equations

<!-- key: Guided experiments -->
Guided experiments

<!-- key: Expert settings -->
Expert settings

<!-- key: Use sliders for main parameters -->
Use sliders for main parameters

<!-- key: Flow & domain -->
Flow & domain

<!-- key: Transport & source -->
Transport & source

<!-- key: Post-processing & observations -->
Post-processing & observations

<!-- key: Hydraulic properties -->
Hydraulic properties

<!-- key: Hydraulic conductivity K (m/s) -->
Hydraulic conductivity K (m/s)

<!-- key: Effective porosity (-) -->
Effective porosity (-)

<!-- key: Specific storage Ss (1/m) -->
Specific storage Ss (1/m)

<!-- key: Vertical / horizontal K -->
Vertical / horizontal K

<!-- key: Boundary conditions -->
Boundary conditions

<!-- key: Specified head left (m) -->
Specified head left (m)

<!-- key: Specified head right (m) -->
Specified head right (m)

<!-- key: Transient flow experiment -->
Transient flow experiment

<!-- key: Right head after t = 0 (m) -->
Right head after t = 0 (m)

<!-- key: Model extent and spatial discretization -->
Model extent and spatial discretization

<!-- key: Model length in x-direction (m) -->
Model length in x-direction (m)

<!-- key: Model width in y-direction (m) -->
Model width in y-direction (m)

<!-- key: Aquifer thickness / top elevation (m) -->
Aquifer thickness / top elevation (m)

<!-- key: Define the grid by -->
Define the grid by

<!-- key: Number of cells -->
Number of cells

<!-- key: Cell width -->
Cell width

<!-- key: Cells x -->
Cells x

<!-- key: Cells y -->
Cells y

<!-- key: Cell width x (m) -->
Cell width x (m)

<!-- key: Cell width y (m) -->
Cell width y (m)

<!-- key: Number of layers -->
Number of layers

<!-- key: Numerical solution for flow -->
Numerical solution for flow

<!-- key: Head tolerance (m) -->
Head tolerance (m)

<!-- key: Flow residual tolerance (m³/day) -->
Flow residual tolerance (m³/day)

<!-- key: PCG outer iterations -->
PCG outer iterations

<!-- key: PCG inner iterations -->
PCG inner iterations

<!-- key: Flow time steps (approximately total) -->
Flow time steps (approximately total)

<!-- key: Hydrogeology and zonation -->
Hydrogeology and heterogeneity

<!-- key: Hydrogeology preset -->
Hydrogeology preset

<!-- key: Number of zones -->
Number of zones

<!-- key: Random seed -->
Random seed

<!-- key: K range (m/s) -->
K range (m/s)

<!-- key: Ss range (1/m) -->
Ss range (1/m)

<!-- key: Porosity range (-) -->
Porosity range (-)

<!-- key: Minimum -->
Minimum

<!-- key: Maximum -->
Maximum

<!-- key: Edit hydrogeological zones -->
Edit hydrogeological zones

<!-- key: Zone name -->
Zone name

<!-- key: First layer -->
First layer

<!-- key: Last layer -->
Last layer

<!-- key: Porosity -->
Porosity

<!-- key: Boundary conditions and source -->
Boundary conditions and source

<!-- key: Input signal -->
Input signal

<!-- key: Released mass (g) -->
Released mass (g)

<!-- key: Mass input rate (g/day) -->
Mass input rate (g/day)

<!-- key: Pulse duration (days) -->
Pulse duration (days)

<!-- key: Source x (m) -->
Source x (m)

<!-- key: Source y (m) -->
Source y (m)

<!-- key: Source cells x -->
Source cells x

<!-- key: Source cells y -->
Source cells y

<!-- key: Source spans all layers -->
Source spans all layers

<!-- key: Source layer (1 = top) -->
Source layer (1 = top)

<!-- key: Transport parameters -->
Transport parameters

<!-- key: Dispersion -->
Dispersion

<!-- key: Longitudinal dispersivity (m) -->
Longitudinal dispersivity (m)

<!-- key: Horizontal transverse / longitudinal -->
Horizontal transverse / longitudinal

<!-- key: Vertical transverse / longitudinal -->
Vertical transverse / longitudinal

<!-- key: Temporal discretization -->
Temporal discretization

<!-- key: Transport duration (days) -->
Transport duration (days)

<!-- key: DT0 · initial step (days; 0 = automatic) -->
DT0 · initial step (days; 0 = automatic)

<!-- key: TTSMAX · maximum step (days; 0 = automatic) -->
TTSMAX · maximum step (days; 0 = automatic)

<!-- key: TTSMULT · step multiplier -->
TTSMULT · step multiplier

<!-- key: MXSTRN · maximum transport steps -->
MXSTRN · maximum transport steps

<!-- key: Numerical solution for transport -->
Numerical solution for transport

<!-- key: MT3D advection method -->
MT3D advection method

<!-- key: MODPATH particle comparison -->
MODPATH particle comparison

<!-- key: PERCEL · Courant number -->
PERCEL · Courant number

<!-- key: CCLOSE · concentration tolerance -->
CCLOSE · concentration tolerance

<!-- key: Timeout per executable (seconds) -->
Timeout per executable (seconds)

<!-- key: Expert transport solver settings -->
Expert transport solver settings

<!-- key: MXPART · maximum particles -->
MXPART · maximum particles

<!-- key: ITRACK · tracking algorithm -->
ITRACK · tracking algorithm

<!-- key: WD · concentration weighting -->
WD · concentration weighting

<!-- key: DCEPS · gradient threshold -->
DCEPS · gradient threshold

<!-- key: NPLANE · particle planes -->
NPLANE · particle planes

<!-- key: NPL · low-gradient particles -->
NPL · low-gradient particles

<!-- key: NPH · high-gradient particles -->
NPH · high-gradient particles

<!-- key: NPMIN · minimum particles/cell -->
NPMIN · minimum particles/cell

<!-- key: NPMAX · maximum particles/cell -->
NPMAX · maximum particles/cell

<!-- key: INTERP · interpolation -->
INTERP · interpolation

<!-- key: NLSINK · sink planes -->
NLSINK · sink planes

<!-- key: NPSINK · sink particles -->
NPSINK · sink particles

<!-- key: DCHMOC · HMOC threshold -->
DCHMOC · HMOC threshold

<!-- key: MXITER · GCG outer iterations -->
MXITER · GCG outer iterations

<!-- key: ITER1 · GCG inner iterations -->
ITER1 · GCG inner iterations

<!-- key: ISOLVE · preconditioner -->
ISOLVE · preconditioner

<!-- key: NCRS · cross-dispersion -->
NCRS · cross-dispersion

<!-- key: ACCL · relaxation -->
ACCL · relaxation

<!-- key: IPRGCG · print interval -->
IPRGCG · print interval

<!-- key: MODPATH release settings -->
MODPATH release settings

<!-- key: Particles per source cell -->
Particles per source cell

<!-- key: Release batches (pulse / continuous) -->
Release batches (pulse / continuous)

<!-- key: Observation points -->
Observation points

<!-- key: Number of observation points -->
Number of observation points

<!-- key: Output settings -->
Output settings

<!-- key: Saved transport times -->
Saved transport times

<!-- key: Actual source footprint -->
Actual source footprint

<!-- key: Optional run label -->
Optional run label

<!-- key: Run model -->
Run model

<!-- key: Run diagnostic -->
Run diagnostic

<!-- key: More comparison metrics -->
More comparison metrics

<!-- key: Displayed run -->
Displayed run

<!-- key: Run to remove -->
Run to remove

<!-- key: Remove -->
Remove

<!-- key: Clear comparison runs -->
Clear comparison runs

<!-- key: Plume & sections -->
Plume & sections

<!-- key: Observation curves -->
Observation curves

<!-- key: Mass & diagnostics -->
Mass & diagnostics

<!-- key: Export -->
Export

<!-- key: Time (days) -->
Time (days)

<!-- key: Top-view layer -->
Top-view layer

<!-- key: Layer {number} -->
Layer {number}

<!-- key: Analytical reference -->
Analytical reference

<!-- key: Plot settings and section positions -->
Plot settings and section positions

<!-- key: x-direction section · y (m) -->
x-direction section · y (m)

<!-- key: y-direction section · x (m) -->
y-direction section · x (m)

<!-- key: Colour fill -->
Colour fill

<!-- key: Contour lines -->
Contour lines

<!-- key: Log colours -->
Log colours

<!-- key: Particle paths -->
Particle paths

<!-- key: Opacity -->
Opacity

<!-- key: Compare runs in x / y sections -->
Compare runs in x / y sections

<!-- key: Compare section profiles -->
Compare section profiles

<!-- key: Runs for section comparison -->
Runs for section comparison

<!-- key: Also overlay top-view contours -->
Also overlay top-view contours

<!-- key: Download plume figure (PNG) -->
Download plume figure (PNG)

<!-- key: Runs in breakthrough comparison -->
Runs in breakthrough comparison

<!-- key: Observation cells used by each run -->
Observation cells used by each run

<!-- key: Download breakthrough curves (CSV) -->
Download breakthrough curves (CSV)

<!-- key: Detailed mass-budget data -->
Detailed mass-budget data

<!-- key: Stored run configuration -->
Stored run configuration

<!-- key: Download comparison table (CSV) -->
Download comparison table (CSV)

<!-- key: Download run configuration (JSON) -->
Download run configuration (JSON)

<!-- key: Prepare complete displayed-run archive -->
Prepare complete displayed-run archive

<!-- key: Preparing archive… -->
Preparing archive…

<!-- key: Download run archive (ZIP) -->
Download run archive (ZIP)

<!-- key: Run -->
Run

<!-- key: Method -->
Method

<!-- key: Signal -->
Signal

<!-- key: Grid -->
Grid

<!-- key: K zones -->
K zones

<!-- key: Flow -->
Flow

<!-- key: MB disc. (%) -->
MB disc. (%)

<!-- key: Flow disc. (%) -->
Flow disc. (%)

<!-- key: MT3D (s) -->
MT3D (s)

<!-- key: MP7 (s) -->
MP7 (s)

<!-- key: Flow (s) -->
Flow (s)

<!-- key: Total (s) -->
Total (s)

<!-- key: Ref. L1 (%) -->
Ref. L1 (%)

<!-- key: Mass (g) -->
Mass (g)

<!-- key: Input (g) -->
Input (g)

<!-- key: Min. C (g/m³) -->
Min. C (g/m³)

<!-- key: Neg. mass (g) -->
Neg. mass (g)

<!-- key: Centroid x (m) -->
Centroid x (m)

<!-- key: Steps -->
Steps

<!-- key: Source box (m) -->
Source box (m)

<!-- key: End (d) -->
End (d)

<!-- key: Scenario -->
Scenario

<!-- key: Point -->
Point

<!-- key: Requested x -->
Requested x

<!-- key: Requested y -->
Requested y

<!-- key: Requested z -->
Requested z

<!-- key: Cell centre x -->
Cell centre x

<!-- key: Cell centre y -->
Cell centre y

<!-- key: Cell centre z -->
Cell centre z

<!-- key: Layer -->
Layer

<!-- key: Row -->
Row

<!-- key: Column -->
Column

<!-- key: Cumulative in (g) -->
Cumulative in (g)

<!-- key: Cumulative out (g) -->
Cumulative out (g)

<!-- key: Sources (g) -->
Sources (g)

<!-- key: Sinks (g) -->
Sinks (g)

<!-- key: Fluid storage (g) -->
Fluid storage (g)

<!-- key: Native resident mass (g) -->
Native resident mass (g)

<!-- key: Alternative disc. (%) -->
Alternative disc. (%)

<!-- key: Analytical reference requires homogeneous steady flow. -->
Analytical reference requires homogeneous steady flow.

<!-- key: Source cells -->
Source cells

<!-- key: Specified head -->
Specified head

<!-- key: Section locations -->
Section locations

<!-- key: Background flow -->
Background flow

<!-- key: Model preview: grid, boundaries and source -->
Model preview: grid, boundaries and source

<!-- key: Computed head contours -->
Computed head contours

<!-- key: Homogeneous steady head contours -->
Homogeneous steady head contours

<!-- key: Time (d) -->
Time (d)

<!-- key: Mass rate (g/d) -->
Mass rate (g/d)

<!-- key: Instantaneous mass (g) -->
Instantaneous mass (g)

<!-- key: Dirac input (initial cell mass) -->
Dirac input (initial cell mass)

<!-- key: Finite pulse input -->
Finite pulse input

<!-- key: Continuous input -->
Continuous input

<!-- key: Concentration (g/m³) -->
Concentration (g/m³)

<!-- key: Elevation z (m) -->
Elevation z (m)

<!-- key: MODPATH advection (slice) -->
MODPATH advection (slice)

<!-- key: Analytical -->
Analytical

<!-- key: Analytical (active run) -->
Analytical (active run)

<!-- key: Mass output unavailable -->
Mass output unavailable

<!-- key: MT3D discrepancy (%) -->
MT3D discrepancy (%)

<!-- key: Initial + injected mass (first run) -->
Initial + injected mass (first run)

<!-- key: Resident mass: grid sum and MT3D budget -->
Resident mass: grid sum and MT3D budget

<!-- key: Reported mass-balance closure -->
Reported mass-balance closure

<!-- key: Example: pulse plume after 600 days -->
Example: pulse plume after 600 days

<!-- key: Example: observation P1 -->
Example: observation P1

<!-- key: P1 · x (m) -->
P1 · x (m)

<!-- key: P1 · y (m) -->
P1 · y (m)

<!-- key: P1 · elevation z (m) -->
P1 · elevation z (m)

<!-- key: P2 · x (m) -->
P2 · x (m)

<!-- key: P2 · y (m) -->
P2 · y (m)

<!-- key: P2 · elevation z (m) -->
P2 · elevation z (m)

<!-- key: P3 · x (m) -->
P3 · x (m)

<!-- key: P3 · y (m) -->
P3 · y (m)

<!-- key: P3 · elevation z (m) -->
P3 · elevation z (m)

<!-- key: P4 · x (m) -->
P4 · x (m)

<!-- key: P4 · y (m) -->
P4 · y (m)

<!-- key: P4 · elevation z (m) -->
P4 · elevation z (m)

<!-- key: P5 · x (m) -->
P5 · x (m)

<!-- key: P5 · y (m) -->
P5 · y (m)

<!-- key: P5 · elevation z (m) -->
P5 · elevation z (m)

<!-- key: fig_head -->
Specified head: {head:g} m

<!-- key: fig_layers -->
{layers} layer(s); vertical scale exaggerated

<!-- key: fig_total -->
Total: {mass:g} g

<!-- key: fig_initial -->
{mass:g} g at t = 0

<!-- key: fig_xprofile -->
x profile at y = {y:.3g} m

<!-- key: fig_yprofile -->
y profile at x = {x:.3g} m

<!-- key: fig_section -->
{axis}–z section at {other} = {value:.3g} m

<!-- key: fig_title -->
{method} · t = {time:g} d · layer {layer} (z = {z:.3g} m)

<!-- key: fig_gridmass -->
{label}: grid sum

<!-- key: fig_nativemass -->
{label}: MT3D budget

<!-- key: fig_nodata -->
{label}: outside domain — no data

<!-- key: table_help_MB disc. (%) -->
Final MT3D mass-balance discrepancy, as reported by the native program.

<!-- key: table_help_Flow disc. (%) -->
Final MODFLOW water-budget discrepancy.

<!-- key: table_help_MT3D (s) -->
Transport executable wall-clock runtime.

<!-- key: table_help_MP7 (s) -->
MODPATH executable runtime; particles describe advection only.

<!-- key: table_help_Ref. L1 (%) -->
Pore-volume-weighted absolute concentration error relative to reference mass.

<!-- key: table_help_Mass (g) -->
Final dissolved mass integrated from the concentration grid.

<!-- key: MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings. -->
MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings.

<!-- key: At least one MODFLOW water-budget discrepancy exceeds 0.1%. -->
At least one MODFLOW water-budget discrepancy exceeds 0.1%.

<!-- key: Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate. -->
Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate.

<!-- key: Source coordinates must lie inside the domain. -->
Source coordinates must lie inside the domain.

<!-- key: This confined lab requires heads at or above aquifer top. -->
This confined lab requires heads at or above aquifer top.

<!-- key: Pulse duration must be between zero and model duration. -->
Pulse duration must be between zero and model duration.

<!-- key: Observation point is outside the model. -->
Observation point is outside the model.

<!-- key: TVD requires PERCEL no greater than 1. -->
TVD requires PERCEL no greater than 1.

<!-- key: language_fallback -->
Missing translations use the English fallback.

<!-- key: preset_random -->
Random stochastic parameters

<!-- key: Random unit x (m) -->
Random unit x (m)

<!-- key: Random unit y (m) -->
Random unit y (m)

<!-- key: random_hint -->
Small units give a fine random pattern; larger units give larger patches. Keep seed and unit sizes fixed to preserve the physical realization during grid refinement.

<!-- key: Active cells -->
Active cells

<!-- key: table_help_Active cells -->
All non-inactive model cells, including specified-head cells.

<!-- key: Random field -->
Random field

<!-- key: Comparison runs -->
Comparison runs

<!-- key: discard_tags_hint -->
Remove a run tag with its × to discard that run. Clear all tags to start a fresh comparison. Export any run you want to keep first.

<!-- key: Head contours -->
Head contours

<!-- key: Computed head contours (m) -->
Computed head contours (m)

<!-- key: Head contours appear after running the model -->
Head contours appear after running the model

<!-- key: fig_background_k -->
Background K = {k:.2e} m/s

<!-- key: fig_low_lens_k -->
Low K lens: K = {k:.2e} m/s

<!-- key: fig_high_channel_k -->
High K channel: K = {k:.2e} m/s

<!-- key: fig_low_barrier_k -->
Low K barrier: K = {k:.2e} m/s

<!-- key: Focus on plume -->
Focus on plume

<!-- key: Focus threshold (% of peak) -->
Focus threshold (% of peak)

<!-- key: focus_hint -->
Focus uses the current positive peak of each displayed plume, with a 20% margin on each side. Visible MODPATH paths are included. Empty views retain the full domain. Only the top view changes.

<!-- key: Download plume figure (SVG) -->
Download plume figure (SVG)

<!-- key: steady -->
steady

<!-- key: transient -->
transient

<!-- key: fig_minimum -->
Numerical minimum: {minimum:.3g} g/m³

<!-- key: fig_minimum_log -->
Numerical minimum: {minimum:.3g} g/m³ (nonpositive values hidden on log scale)

<!-- key: The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark. -->
The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark.

<!-- key: fig_reference_boundary -->
Analytical accuracy disabled: x-boundary interaction exceeds the {tolerance_percent:.2g}% screen.

<!-- key: Low K lens -->
Low K lens

<!-- key: High K channel -->
High K channel

<!-- key: Low K barrier -->
Partial low K barrier

<!-- key: Page width -->
Page width

<!-- key: width_1 -->
Narrow

<!-- key: width_2 -->
Compact

<!-- key: width_3 -->
Standard

<!-- key: width_4 -->
Large

<!-- key: width_5 -->
Wide

<!-- key: page_width_hint -->
Five page widths, from narrow to full width. Standard retains the previous width. Small screens always use the available space.

<!-- key: Show model grid -->
Show model grid

<!-- key: grid_hint -->
Subtle cell boundaries of the displayed run. Single-layer concentration profiles show vertical cell-edge guides.

<!-- key: Plume-centered x/y -->
Plume-centered x/y

<!-- key: relative_hint -->
Zero is the positive dissolved-mass centroid in the displayed layer. All overlays share this origin. Input coordinates and elevation remain absolute.

<!-- key: relative_mass_origin -->
Relative origin: x = {x:.2f} m; y = {y:.2f} m (plume mass center).

<!-- key: relative_source_origin -->
No positive plume mass in this layer: origin at the snapped source center, x = {x:.2f} m; y = {y:.2f} m.

<!-- key: fig_relative_xprofile -->
x profile at y′ = {y:.3g} m

<!-- key: fig_relative_yprofile -->
y profile at x′ = {x:.3g} m

<!-- key: fig_relative_section -->
{axis}–z section at {other}′ = {value:.3g} m

<!-- key: MODPATH particle count -->
MODPATH particle count

<!-- key: particle_count_cell -->
Per source cell

<!-- key: particle_count_total -->
Whole source per release

<!-- key: Particles in the whole source per release -->
Particles in the whole source per release

<!-- key: particle_count_summary -->
{count} particles across {cells} source cells × {groups} releases = {total} particles.

<!-- key: expert_transport_hint -->
All transport solver controls are shown. NPL / NPH and NPMIN / NPMAX control MOC / HMOC particles; MXPART limits their total. Help icons explain method applicability. MODPATH uses separate particles.

<!-- key: Plume animation -->
Plume animation

<!-- key: Animation view -->
Animation view

<!-- key: animation_2d -->
Top view and sections

<!-- key: animation_3d -->
3D cell-centre concentrations

<!-- key: Animation frames -->
Animation frames

<!-- key: Playback speed (frames/s) -->
Playback speed (frames/s)

<!-- key: Vertical exaggeration -->
Vertical exaggeration

<!-- key: Generate / refresh animation -->
Generate / refresh animation

<!-- key: Generating animation… -->
Generating animation…

<!-- key: Download animation (HTML) -->
Download animation (HTML)

<!-- key: Play -->
Play

<!-- key: Pause -->
Pause

<!-- key: Animation frame -->
Animation frame

<!-- key: animation_layers_hint -->
Add layers in expert settings for a 3D view.

<!-- key: animation_hint -->
Uses saved times of the displayed run. Choose independent animation colours and zoom below; the colour scale stays fixed across time. Other 2D plot settings are retained. Comparisons and analytical overlays stay in static plots. The generated player appears below these settings; downloaded HTML plays offline.

<!-- key: animation_3d_hint -->
3D shows cell-centre concentrations above the threshold, with a fixed camera. At most {maximum} evenly sampled cells are displayed; calculations and exports retain all cells. Particle markers are an advective comparison. Vertical exaggeration changes display only.

<!-- key: animation_refresh_hint -->
Plot or animation settings changed. Generate again to update the player.

<!-- key: animation_failed -->
Animation could not be generated. Stored model results are retained.

<!-- key: animation_size_limit -->
Animation exceeds 45 MiB. Choose fewer frames and generate again.

<!-- key: help_s_percel -->
Maximum advective travel per transport step, in cell widths. TVD requires ≤ 1.

<!-- key: help_s_mxpart -->
MOC/HMOC: total moving-particle capacity, not particles per cell.

<!-- key: help_s_itrack -->
MOC/MMOC/HMOC: 1 = Euler, 2 = fourth-order Runge–Kutta, 3 = hybrid tracking.

<!-- key: help_s_wd -->
Characteristic methods: concentration weighting during operator splitting; 0.5–1.

<!-- key: help_s_dceps -->
MOC/HMOC: relative concentration-gradient threshold separating NPL and NPH placement.

<!-- key: help_s_nplane -->
MOC/HMOC: 0 = random placement; positive = horizontal particle planes per cell.

<!-- key: help_s_npl -->
MOC/HMOC: initial particles per low-gradient cell (gradient ≤ DCEPS); zero allowed.

<!-- key: help_s_nph -->
MOC/HMOC: initial particles per high-gradient cell. Fixed patterns may round this count.

<!-- key: help_s_npmin -->
MOC/HMOC: insert particles when the cell count falls below this minimum.

<!-- key: help_s_npmax -->
MOC/HMOC: exceeding this cell count triggers replacement by an NPH-sized set.

<!-- key: help_s_interp -->
MMOC/HMOC: concentration interpolation; only 1 (linear) is supported.

<!-- key: help_s_nlsink -->
MMOC/HMOC sink cells: 0 = random placement; positive = particle planes.

<!-- key: help_s_npsink -->
MMOC/HMOC: particles representing each sink cell.

<!-- key: help_s_dchmoc -->
HMOC: use MOC above this relative-gradient threshold, MMOC below it.

<!-- key: help_s_mxiter -->
GCG outer iteration limit. One is sufficient for this linear conservative-transport model.

<!-- key: help_s_iter1 -->
GCG inner iteration limit for solving the transport equations.

<!-- key: help_s_isolve -->
GCG preconditioner: 1 = Jacobi, 2 = SSOR, 3 = modified incomplete Cholesky (MIC).

<!-- key: help_s_ncrs -->
Dispersion cross terms: 0 = right-hand-side approximation; 1 = full tensor in the matrix.

<!-- key: help_s_accl -->
Relaxation factor used only by SSOR (ISOLVE = 2).

<!-- key: help_s_cclose -->
Relative concentration-change tolerance for GCG convergence. Smaller values tighten convergence.

<!-- key: help_s_iprgcg -->
Print concentration changes every N GCG iterations; 0 prints at each stress-period end.

<!-- key: help_s_dt0 -->
Initial transport-step length in days; 0 lets MT3D choose it automatically.

<!-- key: help_s_ttsmult -->
Successive step multiplier for implicit FD transport; characteristic and TVD methods ignore this growth control.

<!-- key: help_s_ttsmax -->
Upper step length in days when TTSMULT > 1; 0 uses the native automatic limit.

<!-- key: help_s_mxstrn -->
Maximum transport steps within one flow time step; reaching the limit can stop the run.

<!-- key: help_s_timeout -->
Wall-clock limit for each native executable. Larger particle counts may need more time.

<!-- key: help_s_hclose -->
PCG head-change convergence tolerance, in metres.

<!-- key: help_s_rclose -->
PCG flow-residual convergence tolerance, in m³/day.

<!-- key: help_s_flow_mxiter -->
Maximum outer iterations of the MODFLOW PCG flow solver.

<!-- key: help_s_flow_iter1 -->
Maximum inner PCG iterations per outer flow iteration.

<!-- key: help_particle_count_mode -->
Choose particles per source cell or an exact total for the whole source at each release time.

<!-- key: help_particles_per_cell -->
Particles are evenly placed inside each source cell at each release. This controls MODPATH only, not MOC.

<!-- key: help_total_source_particles -->
Exact count per release, spread over all source cells; at least one per cell. Cell counts differ by at most one; mass weights follow pore volume.

<!-- key: help_release_groups -->
Equal-time midpoint releases approximate pulse or continuous input. More batches refine release timing; Dirac uses one release at t = 0.

<!-- key: help_run_label -->
Leave blank to use the suggested name. A custom label replaces the method/signal text; numbering and the heterogeneous suffix remain automatic.

<!-- key: help_expert -->
Expose layer controls and every supported flow/transport solver parameter. Existing values are retained when hidden.

<!-- key: help_sliders -->
Switch between numeric fields and sliders without changing model values.

<!-- key: help_extent -->
Physical domain extent in metres. Changing extent starts a new comparison series.

<!-- key: help_thickness -->
Confined aquifer thickness; bottom elevation is 0 m and the top equals this value. Layers divide the thickness evenly.

<!-- key: help_grid_mode -->
Set cell numbers or maximum cell widths. Width mode rounds cell counts upward while preserving the physical domain.

<!-- key: help_grid_count -->
Number of uniform cells in this direction. Refinement retains previous comparison runs.

<!-- key: help_cell_width -->
Requested maximum cell width in metres. The preview reports the actual uniform width.

<!-- key: help_nlay -->
One layer gives a plan-view model; multiple equal-thickness layers enable vertical transport and 3D views.

<!-- key: help_k -->
Background horizontal hydraulic conductivity. Enter m/s; the model converts to m/day.

<!-- key: help_porosity -->
Mobile pore-volume fraction; controls pore-water velocity and solute storage.

<!-- key: help_ss -->
Water released per aquifer volume per unit head decline (1/m). No storage term acts in this steady-flow interface.

<!-- key: help_kv_ratio -->
Vertical hydraulic conductivity divided by horizontal conductivity, applied in every layer.

<!-- key: help_zones_preset -->
Choose homogeneous properties, a repeatable random field, or a defined lens/channel/barrier.

<!-- key: help_zone_seed -->
Repeatable random-field seed. The same seed and settings reproduce the same physical pattern.

<!-- key: help_random_unit -->
Physical size of random blocks in this direction, independent of numerical grid refinement.

<!-- key: help_random_k -->
Bounds for random hydraulic conductivity, sampled uniformly in log space (m/s).

<!-- key: help_random_ss -->
Bounds for log-uniform specific storage (1/m). Stored for the model, inactive under steady flow.

<!-- key: help_random_por -->
Bounds for uniformly sampled effective porosity; values must lie between zero and one.

<!-- key: help_head -->
Specified hydraulic head on this outer column. Left must exceed right; both must be at or above the aquifer top.

<!-- key: help_duration -->
Total simulated transport time in days. This is independent of the animation playback speed.

<!-- key: help_dispersion -->
Include mechanical spreading proportional to pore-water velocity. Turning this off isolates advection and numerical spreading.

<!-- key: help_al -->
Longitudinal dispersivity along flow, in metres; the associated dispersion coefficient is αL times speed.

<!-- key: help_trpt -->
Horizontal transverse dispersivity divided by longitudinal dispersivity: αTH/αL.

<!-- key: help_trpv -->
Vertical transverse dispersivity divided by longitudinal dispersivity: αTV/αL. Relevant with multiple layers.

<!-- key: help_source_kind -->
Dirac: initial dissolved mass at t = 0. Pulse: constant loading until pulse end. Continuous: constant loading throughout the run.

<!-- key: help_source_mass -->
Total dissolved mass initially distributed through source pore volume (grams).

<!-- key: help_mass_rate -->
Total solute loading rate (g/day), apportioned by source pore volume. No water is injected.

<!-- key: help_pulse_duration -->
Loading stops after this time (days); it must be shorter than total transport duration.

<!-- key: help_source_position -->
Absolute source-centre coordinate in metres, snapped to a model cell. The source must avoid specified-head columns.

<!-- key: help_source_cells -->
Number of source cells in this direction. Preview the actual footprint; changing source geometry starts a new series.

<!-- key: help_source_all_layers -->
Distribute the source over every layer; otherwise use the selected layer only.

<!-- key: help_src_layer -->
Layer receiving the source; 1 is the uppermost layer.

<!-- key: help_method -->
Choose MT3D advection: FD up/central, TVD, forward MOC, backward MMOC or hybrid HMOC. This does not select MODPATH.

<!-- key: help_track_particles -->
Run MODPATH 7 in the computed flow field. Particles represent advection only; no dispersion or concentrations are calculated by MODPATH.

<!-- key: help_observation -->
Absolute observation coordinate in metres. Concentration is sampled from the containing cell, not interpolated between cells.

<!-- key: help_nobs -->
Compare concentrations at one to five observation points using the stored runs.

<!-- key: help_outputs -->
Number of saved transport times, including t = 0. Pulse end is also retained. More outputs improve animation and curve sampling, not solver time-step accuracy.

<!-- key: help_length -->
Physical domain extent in metres. Changing extent starts a new comparison series.

<!-- key: help_width -->
Physical domain extent in metres. Changing extent starts a new comparison series.

<!-- key: help_ncol -->
Number of uniform cells in this direction. Refinement retains previous comparison runs.

<!-- key: help_nrow -->
Number of uniform cells in this direction. Refinement retains previous comparison runs.

<!-- key: help_cell_x -->
Requested maximum cell width in metres. The preview reports the actual uniform width.

<!-- key: help_cell_y -->
Requested maximum cell width in metres. The preview reports the actual uniform width.

<!-- key: help_random_unit_x -->
Physical size of random blocks in this direction, independent of numerical grid refinement.

<!-- key: help_random_unit_y -->
Physical size of random blocks in this direction, independent of numerical grid refinement.

<!-- key: help_zone_k_min -->
Bounds for random hydraulic conductivity, sampled uniformly in log space (m/s).

<!-- key: help_zone_k_max -->
Bounds for random hydraulic conductivity, sampled uniformly in log space (m/s).

<!-- key: help_zone_ss_min -->
Bounds for log-uniform specific storage (1/m). Stored for the model, inactive under steady flow.

<!-- key: help_zone_ss_max -->
Bounds for log-uniform specific storage (1/m). Stored for the model, inactive under steady flow.

<!-- key: help_zone_por_min -->
Bounds for uniformly sampled effective porosity; values must lie between zero and one.

<!-- key: help_zone_por_max -->
Bounds for uniformly sampled effective porosity; values must lie between zero and one.

<!-- key: help_head_left -->
Specified hydraulic head on this outer column. Left must exceed right; both must be at or above the aquifer top.

<!-- key: help_head_right -->
Specified hydraulic head on this outer column. Left must exceed right; both must be at or above the aquifer top.

<!-- key: help_src_x -->
Absolute source-centre coordinate in metres, snapped to a model cell. The source must avoid specified-head columns.

<!-- key: help_src_y -->
Absolute source-centre coordinate in metres, snapped to a model cell. The source must avoid specified-head columns.

<!-- key: help_src_ncol -->
Number of source cells in this direction. Preview the actual footprint; changing source geometry starts a new series.

<!-- key: help_src_nrow -->
Number of source cells in this direction. Preview the actual footprint; changing source geometry starts a new series.

<!-- key: help_animation_mode -->
2D repeats the plan and profiles/sections. 3D shows computed cell-centre concentrations with a fixed viewpoint; it requires multiple layers.

<!-- key: help_animation_frames -->
Select up to 80 saved snapshots, including first and last. No concentration interpolation between times.

<!-- key: help_animation_fps -->
Frames shown per real second. Each frame reports its actual simulated time; playback does not change the model.

<!-- key: help_animation_exaggeration -->
Scale the visual height of the 3D domain. Elevations and numerical calculations remain unchanged.

<!-- key: help_generate_animation -->
Render saved results only when requested. Regenerate after changing view settings; the model is not rerun.

<!-- key: help_view_time -->
Choose a saved transport time; this does not rerun the model.

<!-- key: help_view_layer -->
Layer displayed in plan view; 1 is the top layer.

<!-- key: help_section -->
Absolute section position in metres; sampled from the nearest containing row/column. Relative plotting does not move the section.

<!-- key: help_fill -->
Fill model cells using the concentration colour scale; zero concentration remains white.

<!-- key: help_lines -->
Draw concentration isolines over the colour fill.

<!-- key: help_show_heads -->
Overlay thin computed hydraulic-head contours, labelled in metres.

<!-- key: help_log -->
Use logarithmic colours for positive concentrations. Nonpositive cells are hidden in this display only.

<!-- key: help_particle_paths -->
Show MODPATH positions and thin paths up to the selected time. Display samples at most 120 trajectories; exports retain all particles.

<!-- key: help_opacity -->
Colour-fill opacity: 1 is opaque; smaller values reveal underlying features.

<!-- key: help_focus_plume -->
Zoom around the positive plume and displayed MODPATH trajectories, adding a margin. Animation uses one fixed window over its selected times.

<!-- key: help_focus_threshold -->
Static focus: percent of each plume peak. In 3D animation: percent of the fixed colour-scale maximum magnitude used to display cells.

<!-- key: help_analytical -->
Compare with the homogeneous, steady-flow analytical reference. Heterogeneous or transient flow is outside its assumptions.

<!-- key: help_compare -->
Compare saved runs at their nearest available times on the displayed run’s section locations.

<!-- key: help_analytic_on -->
Compare with the homogeneous, steady-flow analytical reference. Heterogeneous or transient flow is outside its assumptions.

<!-- key: help_btc_analytical -->
Compare with the homogeneous, steady-flow analytical reference. Heterogeneous or transient flow is outside its assumptions.

<!-- key: help_compare_sections -->
Compare saved runs at their nearest available times on the displayed run’s section locations.

<!-- key: help_overlay_runs -->
Compare saved runs at their nearest available times on the displayed run’s section locations.

<!-- key: help_compare_top -->
Compare saved runs at their nearest available times on the displayed run’s section locations.

<!-- key: help_btc_runs -->
Compare concentrations at one to five observation points using the stored runs.

<!-- key: Animation settings -->
Animation settings

<!-- key: Animation colour scale -->
Animation colour scale

<!-- key: animation_colour_enhanced -->
Enhanced low concentrations (fixed scale)

<!-- key: animation_colour_linear -->
Linear (fixed scale)

<!-- key: animation_colour_log -->
Logarithmic (fixed scale)

<!-- key: help_animation_colour -->
Enhanced colours use a power mapping (exponent 0.35) to reveal smaller concentrations. Every frame uses the same physical concentration limits; zero remains white. Linear and enhanced scales retain negative numerical values; logarithmic colours hide nonpositive values. Numerical data are unchanged.

<!-- key: Zoom animation to plume -->
Zoom animation to plume

<!-- key: help_animation_focus -->
Use one fixed window enclosing the positive plume and displayed MODPATH paths over all selected times, with 20% padding. Independent of static-plot zoom. Turn off to show the whole domain. Available in 2D and 3D.

<!-- key: Plume threshold (% of peak) -->
Plume threshold (% of peak)

<!-- key: help_animation_threshold -->
Zoom includes concentrations above this percentage of each frame’s positive peak. In 3D, this also sets the cell-display cutoff as a percentage of the fixed scale’s maximum absolute concentration. Default 0.1%. This affects display only.

<!-- key: animation_progress -->
Generating animation… {percent}%

<!-- key: MODPATH settings -->
MODPATH settings

<!-- key: expert_transport_location_hint -->
The MT3D expert parameters are in the separate **Expert transport solver settings** expander directly below. MODPATH settings follow afterwards.
