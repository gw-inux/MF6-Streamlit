"""Editable teaching text. Keep explanation separate from model computation."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   INTRODUCTION: line 11
#   SOLVER_DETAILS: line 24
#   ASSUMPTIONS: line 65
#   REFERENCES: line 168
# END CODE CONTENTS

INTRODUCTION = """
Groundwater models are useful tools for investigating groundwater systems.
Start with steady 1D flow bounded by two specified heads, with uniform
recharge and constant hydraulic conductivity. Add a square horizontal grid,
layers or a random K field to explore more complex systems.

Start with the same confined aquifer and boundary conditions as in the Jacobi,
Gauss–Seidel and SOR exercise, or switch to unconfined flow in the scenario
controls. Here, **MODFLOW solves the equations**.
Compare solvers, refine the grid, and check the calculated heads against
the analytical solution where applicable, and inspect native water balances.
"""

SOLVER_DETAILS = """
| Model | Solver choices | Basic controls |
|---|---|---|
| MODFLOW-2005 | PCG or SIP | Head closure, iteration limits; PCG flow closure and relaxation; SIP acceleration |
| MODFLOW-NWT | Newton with GMRES or XMD | SIMPLE / MODERATE / COMPLEX, head and flow closure, outer and inner limits |
| MODFLOW 6 | IMS with CG or BICGSTAB | SIMPLE / MODERATE / COMPLEX, head and flow closure, outer and inner limits |

**PCG** uses preconditioned conjugate gradients. **SIP** uses the strongly
implicit procedure and has a head-change stopping test. Neither has native
complexity presets. **NWT** uses the Newton formulation with UPW; SIP is not
its Newton solver. **IMS** is the iterative model solution in MODFLOW 6.
MF6 uses NPF with ICELLTYPE=0 for confined flow and ICELLTYPE=1 for
unconfined / convertible flow. It uses Picard iteration, so both CG and
BICGSTAB remain available. The app uses diagonal IMS matrix scaling to keep
the seconds-based equations well scaled; the expert controls can change it.
NWT uses Newton with UPW in both modes.

Each model starts with a head closure of **1e-4 m**, including the inner head
test. Changing the preset or linear solver retains the latest head closure,
flow closure and iteration limits. Each MODFLOW model remembers its own main
controls. Advanced settings are retained separately for each solver/preset.
The selected linear solver is also retained when the preset changes.

SIMPLE is normally appropriate for the initial 1D case. Layers or heterogeneity
can require a different preset or larger iteration limits. MODERATE and COMPLEX
adjust the solution strategy; they do not guarantee more accurate results or
increase the user's current iteration limits. Suggested flow closures are
PCG 1e-4, NWT 5e-3 and IMS 1e-4 **m³/s**. NWT's initial flux tolerance is loose
for this unit-width cross-section and can be tightened for accuracy experiments.

Head-change tolerances are not absolute head-error guarantees. Equal numeric
flow tolerances are not equivalent tests: NWT uses its nonlinear flux norm,
PCG/IMS their selected residual tests, and SIP has no independent flow-closure
input. The analytical error and final cell residual provide additional checks.

The expert toggle opens detailed controls below the input columns. NWT writes
SPECIFIED when expert controls or a changed preset-governed inner limit require
it. XMD uses SPECIFIED to apply the app head closure to its inner test. The remaining preset values are carried over explicitly. All edited values
are therefore applied to the model input.
"""

ASSUMPTIONS = """
Initially the model has one homogeneous layer, one row, a flat top and bottom, no storage
and no-flow side faces. Recharge enters as a distributed source; no unsaturated
zone is simulated. Confined mode is selected initially: the roof is 0 m and the
bottom is −b. Positive boundary heads keep the layer fully saturated, and the
plotted head is the piezometric head.

In **unconfined / convertible mode**, the bottom is 0 m and the input is the
aquifer-top elevation z_t. Saturated thickness is min(h, z_t); head below the
top represents the water table. Heads above the top are also supported, with
transmissivity capped at K z_t. There is no surface drain or overflow boundary.
Boundary and starting heads must remain above the bottom.

The unconfined reference is the 1D Dupuit solution. If the solution crosses
the aquifer top, the app solves the same continuous equation using the
discharge potential F(h)=h²/2 below the top and F(h)=z_t(h−z_t/2) above it.
F varies as F_L+(F_R−F_L)x/L+R x(L−x)/(2K), and is inverted to obtain h.
This gives continuous head and flux through the transition; the square-root
formula alone would be incorrect above the top.

The analytical boundaries are at the **centres of the two end cells**.
Only the N−2 unknown-head cells receive recharge. Their total recharge is
R W (N−2) Δx; their bounding faces lie at Δx/2 and L−Δx/2. The padded MODFLOW
grid extends from −Δx/2 to L+Δx/2. These conventions match the manual exercise.
All engines use metres and seconds. Recharge conversion uses 365.25 days/year
and 86,400 seconds/day. Head closure is in m; volumetric flow residuals in m³/s.

**Add Complexity** enables a square horizontal grid (Nx = Ny, Δx = Δy),
equal-thickness layers and an isotropic random K field. Both horizontal centre
spans equal L; the padded square has side L + Δx. The west and east boundaries
retain uniform heads in all wet boundary layers. Cells wholly above the
specified boundary water level are inactive. Recharge is excluded from both
boundary columns and applied to the highest wet active cell in each interior
column. LPF and NPF use rewetting from below for layered convertible models;
UPW uses its native Newton treatment.

Random K values are log-uniform within user limits and constant in fixed
physical zones, independently in each layer. A seed reproduces the realization.
Refinement samples the same field at the new cell centres. Initial heads can
be specified uniformly or sampled independently from a uniform distribution
between user limits, with a separate seed. Specified heads always override
the initial guess at reservoir cells.

An analytical curve and head-error metrics are available only for homogeneous
single-layer models, including their y-invariant horizontal 2D extension.
Vertical gradients or heterogeneous K invalidate that exact comparison;
those runs show native cell balances and convergence instead. Changing the
horizontal dimension (1D/2D) or extent clears the run comparison. Confined/unconfined
changes and adding/removing layers retain the comparison. Each saved run keeps
its own geometry for inspection. Horizontal refinement can also be compared.
Diagnostics follow each newly completed run, including the final grid-study run.

Grid refinement keeps the boundary-to-boundary length L fixed. The confined quadratic
analytical solution has an exact central second difference at the nodes in
exact arithmetic. This experiment therefore examines solver effort, stopping
error and precision, rather than decreasing nodal truncation error. The head plot shows full cells numbered from 1; optional dots mark the actual
node heads. On dense grids, every n-th node symbol is shown (n is reported above
the plot); horizontal cell-head segments and wetted filling retain all cells.
The first node is at x = 0 and the two end cells extend half a
spacing beyond the boundary centres. The horizontal cell-head segments are a
visual representation of discrete node values. For unconfined
flow, head-dependent conductances introduce grid effects: LPF and the
non-Newton MF6 NPF formulation use harmonic averaging here; NWT UPW uses
upstream weighting. Coarse-grid heads can therefore differ even after tight
solver convergence. The refinement experiment can show these differences
decreasing. Unconfined and complex-model diagnostics use native face flows and actual recharge placement.

Starting heads are a numerical guess. Solver iterations are not groundwater
changes through physical time. Hiding initial heads only changes the plot and
its axis scaling; the computation still uses the selected starting heads.
Initial-head visibility starts off in the cross section. Horizontal 2D models,
including those with multiple layers, also offer a first-layer head map below
the section. It displays the latest native result and identifies changed inputs.
Dots and horizontal cell-head lines start on together. Switching off the last
active style automatically turns the other style on. Wetted cells remain filled,
and thin lines show the actual layer boundaries. Hollow blue-grey symbols can
compare the previous displayed section at its original physical x coordinates.

**Suggested experiments**

1. Run the 11-cell case with each model and inspect the table and diagnostics.
2. Set recharge to zero: confined heads are linear; in a fully unconfined
   solution, squared heads are linear.
3. Refine the grid while holding L fixed. Explain why preconditioned solvers can
   keep very small iteration counts for this tridiagonal system.
4. Change closure, preconditioning, acceleration or iteration limits and record
   the effect under an individual run name.
5. Compare native presets, then give the solvers tighter closure values in the
   input section. Inspect both head error and the water balance.
6. Switch off Confined aquifer, compare the three engines, then refine the
   grid with tight closure criteria. Distinguish discretization error from
   incomplete iterative convergence.
7. Add layers or a random K field and compare solver effort and cell balances.
   Grid studies preserve the layer count and accept uniform Δx = Δy values.
   The complex setup initially selects one grid, one variant and one repeat.

The tested NWT build can fail for exact-zero residuals and for a
three-cell grid with only one unknown. Such native failures are reported
explicitly; no analytical heads replace the engine output. For the equal-head
18 m, zero-recharge, 11-cell case, COMPLEX and a specified initial head of
17.3 m were verified to work with both NWT linear solvers.
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
