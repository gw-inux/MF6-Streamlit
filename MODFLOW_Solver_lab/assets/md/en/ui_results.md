# Results interface text

The `##` headings are stable text keys; only their contents are displayed.

## all_nodes_note

Every node symbol is plotted; segments and wetted filling retain all cells.

## results_show_analytical_solution

Show analytical solution

## analytical_help

Enabling the analytical solution also switches on cell-head dots for comparison.

## results_show_initial_heads

Show initial heads

## initial_visibility_help

Only changes visibility and axis scaling, not the solver's starting heads.

## results_show_previous_run

Show previous run

## previous_run_help

Hollow symbols show the saved section at its original physical coordinates.

## results_cell_head_dots

Cell-head dots

## head_dots_help

Switching off the last active head style enables the other.

## results_cell_head_lines

Cell-head lines

## head_lines_help

Horizontal segments span each cell; at least one head style stays active.

## analytical_unavailable_note

The analytical reference is unavailable for layered or heterogeneous models. Native balance and convergence diagnostics remain available.

## nwt_limitation_note

This setup can encounter a native NWT zero-residual / small-system limitation. Any failure is retained as a failed result.

## results_individual_run_name_optional

Individual run name (optional)

## results_number_of_runs

Number of runs

## results_run_model

Run Model

## comparison_empty

Your computations will appear here. The table retains up to the latest ten runs.

## results_select_runs_to_remove

Select runs to remove

## results_remove_selected_runs

Remove selected runs

## results_download_comparison_csv

Download comparison CSV

## diagnostics_expander

**Head errors, water balance and convergence diagnostics**

## section_stale_note

Inputs have changed. The section previews the current setup; computed runs remain in the table.

## section_initial_note

Current setup. Run the model to obtain MODFLOW heads.

## diagnostics_empty

Run a model to inspect its errors, budget and native convergence information.

## results_run_to_inspect

Run to inspect

## results_solver_settings_used_for_this_run

Solver settings used for this run

## nwt_presets_note

For native NWT presets, the reference values describe the tested release; the executable's listing is authoritative.

## results_download_native_listing

Download native listing

## results_program_output

Program output

## convergence_success_note

The native stopping criteria were met in every repeat.

## native_floating_point_error

The executable reported a native floating-point error. No substitute solution was calculated.

## confined_balance_note

Fluxes are positive into the unknown-head region. The independent residual uses the requested physical inputs; legacy input rounding can leave a small residual. A printed budget discrepancy of 0.00% does not prove exact balance.

## complex_balance_note

Fluxes are positive into the unknown-head region. Cell residuals combine native face flows with actual native recharge placement, so they respect each engine's variable transmissivity. A printed budget discrepancy of 0.00% does not prove exact balance.

## results_iteration_level

Iteration level

## logarithmic_history_note

Zero values are omitted from the logarithmic plots and retained in the table. The confined problem is linear; convertible flow generally needs more outer iterations. NWT reports its residual at its own evaluation stage.

## history_empty

No recognized iteration history was produced by this run.

## results_download_heads_csv

Download heads CSV

## head_output_missing

The latest run has no readable head output.

## unconverged_heads_warning

This run did not converge. These heads are not a converged solution.

## results_layer_heads_and_geometry

**Layer heads and geometry**

## native_layers_note

The plan uses the uppermost wet-cell head; the section colours retain native layer heads. Blank section cells are dry or inactive. Orange cells mark specified heads.

## sampled_history_note

This long solve has a sampled inner-iteration history (up to 20,000 points). Native total iteration counts are unchanged.

## summary_random_k

Random K = {k_min:.2E}–{k_max:.2E} m/s.

## summary_uniform_k

K = {k_ms:.2E} m/s.

## node_stride_note

For visualization, one node symbol is plotted every {stride} cells, plus both end nodes. Segments and wetted filling retain all cells.

## results_groundwater_surface

groundwater surface

## results_layer_layer

layer {layer}

## executable_missing

{engine} was not found. Check the shared bin folder or the setup instructions.

## run_caption

Run {run_id:02d}: {run_name} · {status}

## previous_section_note

Hollow symbols: saved section from run {run_id:02d}, {view}, middle cell y {cell_y}.

## comparison_note

{runs_count}/{max_runs} retained runs. A new run replaces the oldest once the table is full. Outer, inner and SIP counts describe different work. Time is the median; counts and errors are from the last repeat. Convergence: ✓ = all repetitions succeeded; ✗ = at least one failed. WB discrep. = water-budget discrepancy (%). RMSE excludes the fixed-head cells and is only shown where an analytical reference applies. het. = heterogeneous hydraulic conductivity.

## results_running_label_repeats_repeat_s

Running {label} · {repeats} repeat(s)…

## results_any_available_heads_remain_marked_as_a

. Any available heads remain marked as a failed result.

## results_native_output_could_not_be_evaluated

Native output could not be evaluated: 
