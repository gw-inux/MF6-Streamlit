# Inputs interface text

The `##` headings are stable text keys; only their contents are displayed.

## inputs_parameters_for_the_scenario

**Parameters for the scenario**

## inputs_show_full_settings

Show full settings

## inputs_confined_aquifer

Confined aquifer

## confined_help

Switch off for unconfined / convertible flow with the bottom fixed at 0 m.

## inputs_starting_head_distribution

Starting-head distribution

## confined_geometry_note

Confined: roof 0 m; bottom −b.

## unconfined_geometry_note

Unconfined / convertible: bottom 0 m; the saturated thickness follows the head up to the aquifer top.

## inputs_spatial_discretization

**Spatial discretization**

## inputs_boundary_to_boundary_length_m

Boundary-to-boundary length (m)

## inputs_define_cell_spacing_instead_of_cell_count

Define cell spacing instead of cell count

## spacing_geometry_note

Distance is between CHD cell centres. Δx = L/(N−1); spacing must divide L exactly.

## inputs_numerical_solver

**Numerical solver**

## inputs_model_preview

**Model preview**

## inputs_aquifer_top_elevation_m

Aquifer top elevation (m)

## inputs_west_left_boundary_head_m

West / left boundary head (m)

## inputs_east_right_boundary_head_m

East / right boundary head (m)

## inputs_recharge_mm_year

Recharge (mm/year)

## inputs_hydraulic_conductivity_m_s

Hydraulic conductivity (m/s)

## inputs_uniform_starting_head_elevation_m

Uniform starting head elevation (m)

## inputs_number_of_cells_along_x_and_y

Number of cells along x and y

## inputs_number_of_cells_along_x

Number of cells along x

## cell_count_help

Includes both fixed-head end cells.

## inputs_model_and_solver

**Model and solver**

## inputs_modflow_model

MODFLOW model

## inputs_solver

Solver

## inputs_linear_solver

Linear solver

## inputs_solver_settings

**Solver settings**

## inputs_preview

Preview

## inputs_aquifer_thickness_m

Aquifer thickness (m)

## inputs_minimum_initial_head_m

Minimum initial head (m)

## inputs_maximum_initial_head_m

Maximum initial head (m)

## initial_random_note

Uniform random initial heads between these limits; specified heads override the guess at the boundaries.

## inputs_solver_preset

Solver preset

## inputs_2d_horizontal_grid_x_y

2D horizontal grid (x–y)

## horizontal_grid_help

Off: one horizontal row. On: square grid, Nx = Ny and Δx = Δy. North and south are no-flow.

## inputs_add_layers

Add layers

## inputs_random_hydraulic_conductivity_field

Random hydraulic-conductivity field

## inputs_initial_head_seed

Initial-head seed

## inputs_smallest_spacing_for_this_length

Smallest spacing for this length.

## inputs_largest_preferred_spacing_for_this_length

Largest preferred spacing for this length.

## layers_note

Equal layer thicknesses. Recharge enters the highest wet active cell; vertical flow connects the layers.

## inputs_preview_layer

Preview layer

## inputs_number_of_layers

Number of layers

## inputs_minimum_k_m_s

Minimum K (m/s)

## inputs_maximum_k_m_s

Maximum K (m/s)

## inputs_k_zones_per_direction

K zones per direction

## inputs_new_realization

New realization

## inputs_cell_spacing_x_y_m

Cell spacing Δx / Δy (m)

## inputs_cell_spacing_x_m

Cell spacing Δx (m)

## inputs_n_cells_along_x

**{n} cells** along x

## inputs_and_n_along_y

 and **{n}** along y

## inputs_x_dx_g_m

 · Δx = {dx:g} m

## retained_boundary_heads

- West / east heads: **{left:g} / {right:g} m**

## retained_recharge

- Recharge: **{recharge:g} mm/year**

## retained_conductivity

- Homogeneous K: **{k:.2E} m/s**

## k_classes_note

{bands} numbered logarithmic K classes; the colour bar gives class midpoints. Native K values are unchanged.

## preview_stride_note

For visibility, only every {stride}-th grid line is drawn, plus the domain edges. All cell values are retained.

## retained_thickness

- Aquifer thickness: **{thickness:g} m**

## retained_initial_seed

- Initial-head seed: **{initial_seed}**

## integer_mode_note

Integer mode starts at {cell_spacing} m; the boundary distance stays unchanged.

## inputs_finer_grid_smaller_m

Finer grid: {smaller} m

## inputs_coarser_grid_larger_m

Coarser grid: {larger} m
