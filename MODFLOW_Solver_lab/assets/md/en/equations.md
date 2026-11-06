
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
