## title

1D Solute Transport Lab

## experiments

Guided experiments

## experiment_front

Advection front

## experiment_spreading

Physical dispersion

## experiment_impulse

Pulse and impulse

## theory_title

Flow field and analytical solutions

## setup

Model setup

## inlet_processes

Inlet and transport

## grid_time

Grid and time

## solver

MT3DMS method

## signal

Inlet signal

## continuous

Continuous input

## block

Block input

## dirac

Dirac impulse

## amplitude

Inlet concentration C/Cref [–]

## block_days

Pulse duration [d]

## impulse_area

Impulse area A [d]

## impulse_days

Numerical pulse width ε [d]

## rectangle

MT3DMS inlet height = {height:.4g} C/Cref.

## dispersion

Activate dispersion

## dispersivity

Longitudinal dispersivity αL [m]

## diffusion

Effective diffusion Dₑ [m²/d]

## grid_by

Specify grid by

## cells

Cell count

## spacing

Spacing

## cell_count

Cells

## target_spacing

Target cell width [m]

## grid_summary

{n} cells · actual Δx = {dx:.3g} m

## courant

Courant limit

## time_hint

All variants end at day 2000. A finite inlet pulse uses at least eight transport steps during application.

## scheme

Advection scheme

## upwind

FD · upstream

## central

FD · centred

## tvd

TVD · ULTIMATE

## moc

MOC

## mmoc

MMOC

## hmoc

HMOC

## solver_hint

MODFLOW-2005 supplies the steady flow field. MT3DMS uses GCG for its implicit equations.

## preview

Model preview

## preview_summary

{signal} · {scheme} · {n} cells · Δx = {dx:.3g} m · D = {D:.4g} m²/d

## distance

Distance from inlet [m]

## time

Time [d]

## inlet_axis

Inlet C/Cref [–]

## optional_name

Variant name (optional)

## name_example

e.g. Fine grid with TVD

## limit

Ten variants are stored. Remove a variant under “Manage variants” to run another one.

## missing

Required executable missing or unavailable on this platform — {names}. Place it in the shared bin folder or set TRANSPORT_LAB_BIN to its directory.

## run

Run model

## running

Running MODFLOW-2005 and MT3DMS …

## failed

The run could not be completed. Previously saved variants are available below.

## diagnostic

Engine details

## results

Transport results

## visible

Variants on the plots

## cells_unit

cells

## show_analytical

Analytical solution

## show_markers

Numerical markers

## profile

Concentration profile

## breakthrough

Breakthrough curve

## budget

Solute mass balance

## profile_time

Profile time [d]

## observation

Observation distance [m]

## applied_curve

Analytical · applied inlet

## ideal_curve

Ideal Dirac

## mass_axis

Mass discrepancy [%]

## no_selection

Select a variant above to show its curves.

## comparison

Final comparison · day 2000

## variant

Variant

## rmse

RMSE

## mae

MAE

## ideal_rmse

RMSE · ideal Dirac

## mass_error

Mass discrep. [%]

## seconds

Runtime [s]

## run_name

Name

## dx_col

Δx [m]

## height_col

Inlet C/Cref

## duration_col

Input duration [d]

## area_col

Dirac A [d]

## alpha_col

αL [m]

## dm_col

Dₑ [m²/d]

## d_col

D [m²/d]

## pe_col

Grid Péclet number

## co_col

Courant limit

## count_col

Transport steps

## flow_s

MODFLOW [s]

## mt_s

MT3DMS [s]

## flow_error

Water budget [%]

## min_c

Final min. C/Cref

## max_c

Final max. C/Cref

## detail_heading

Run settings and metric definitions

## download

Download comparison (CSV)

## manage

Manage variants

## remove_choice

Variant to remove

## remove

Remove selected variant

## references_title

References

## saved

Saved V{number} for comparison.

## applied_color_key

Analytical · variant colour

## ideal_color_key

Ideal Dirac · variant colour

## pulse_cells

Pulse length [cells]

## pulse_resolution

During application, advection carries the pulse {length:.3g} m, equivalent to {cells:.3g} grid cells.

## specified_head

Specified head · {head:.4g} m

## hydraulic_summary

Hydraulic conductivity K = {k:.0e} m/s

## scenario_reset_hint

Changes here clear the saved comparison variants.

## comparison_cleared

The inlet or transport settings changed. The comparison has been cleared for the new scenario.

## concept_title

Conceptual model and typical responses

## concept_inlet

Inlet

## concept_outlet

Outflow

## concept_observation

Observation

## concept_profile

Profile at t = {time:g} d

## concept_breakthrough

Breakthrough at x = {distance:g} m

## concept_advection

Pure advection

## concept_dispersion

Advection + dispersion
