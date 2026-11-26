### Conceptual model

The lab follows a conservative solute in a fully saturated, confined aquifer. Specified heads in the first and last columns drive background flow. The other outer faces are closed to groundwater flow and dispersive solute flux. Solute entering with specified-head inflow has zero concentration; outflow transports the resident concentration. No reactions, sorption, density effects, recharge or pumping are included.

The basic experiment has one layer and represents horizontal 2D transport. Adding layers enables vertical concentration gradients and vertical spreading. A homogeneous, uniform source through all layers remains vertically uniform: adding layers alone does not create vertical flow. Material zones and a source confined to one layer provide useful 3D investigations.

All distances are in metres, time is in days, mass is in grams and concentration is in g/m³ of water. Numerically, 1 g/m³ equals 1 mg/L. The internal conductivity unit is m/d; a value of $10^{-4}$ m/s corresponds to 8.64 m/d.

### Flow and storage

For homogeneous steady flow the pore velocity is

$$
v_x=\frac{K}{n_e}\frac{h_L-h_R}{L-\Delta x}.
$$

The denominator is the distance between the specified-head **cell centres**, not the distance between the external model faces. In heterogeneous models, MODFLOW calculates the nonuniform flow field from the cell conductivities. The vertical conductivity is the local horizontal conductivity multiplied by the selected vertical/horizontal ratio.

The interactive lab uses steady flow. Specific storage $S_s$ is recorded as a material property but does not affect the steady heads or velocities. The aquifer is confined and all specified heads must remain at or above its top. Specific yield is not used.

### Three input signals

| Signal | Numerical representation | Preserved quantity |
|---|---|---|
| Dirac / instantaneous slug | Initial concentration distributed uniformly through the selected source cells at time zero | Initial solute mass $M$ |
| Finite pulse / block | Prescribed mass-loading rate $\dot M$ from time zero until the selected switch-off time | Total applied mass $\dot M\tau$ |
| Continuous | Prescribed mass-loading rate $\dot M$ throughout the transport period | Applied mass by time $t$: $\dot M t$ |

These are internal mass sources, rather than injection wells. Adding solute does not add water or disturb the imposed background flow. A pulse is switched off at a stress-period boundary, with an explicit zero mass-loading rate afterwards. A numerical Dirac source is instantaneous in time but has the finite spatial extent of the selected cells. Its initial concentration is $M/(n_e V_s)$ for a homogeneous source region. A source spanning different porosities is weighted by local pore volume to obtain the same starting concentration.

The source is snapped to the grid. Its realised width, thickness and position should therefore be checked after changing the grid. Refinement with the same source-cell counts changes its physical footprint, so that experiment changes source geometry as well as numerical resolution.

### Advection and dispersion

For homogeneous steady flow in the x direction, the equation is

$$
\frac{\partial C}{\partial t}
=D_x\frac{\partial^2 C}{\partial x^2}
+D_y\frac{\partial^2 C}{\partial y^2}
+D_z\frac{\partial^2 C}{\partial z^2}
-v_x\frac{\partial C}{\partial x}+\frac{s}{n_e}.
$$

Here $s$ is the solute input per unit bulk volume and time. For uniform flow, $D_x=\alpha_L|v_x|+D_e$, $D_y=\alpha_{TH}|v_x|+D_e$, and $D_z=\alpha_{TV}|v_x|+D_e$. The transverse dispersivities are supplied as ratios to $\alpha_L$. In heterogeneous flow, MT3D constructs the dispersion tensor using the local velocity components. Molecular diffusion is fixed at zero in the interactive teaching experiment. Turning dispersion off removes mechanical spreading. With a single layer there is no vertical intercell concentration gradient or solute exchange across the closed top/base; the vertical transverse dispersivity therefore has no effect and is displayed only for multilayer models.

| Method | MT3D option | What to investigate |
|---|---|---|
| FD up | MIXELM = 0, NADVFD = 0 | Front smearing from numerical dispersion |
| FD cen | MIXELM = 0, NADVFD = 2 | Oscillations and negative concentrations on coarse, advection-dominated grids |
| TVD | MIXELM = −1 | Resolution of sharp concentration fronts with flux limiting |
| MOC | MIXELM = 1 | Forward characteristic tracking; sensitivity to particle density |
| MMOC | MIXELM = 2 | Backward characteristic tracking; sensitivity of mass balance |
| HMOC | MIXELM = 3 | Local switching between MOC and MMOC |

The expert settings expose the MT3D advection controls, the GCG linear solver controls, transport time-step controls and MODFLOW solver tolerances. A parameter may apply only to selected methods; for example, MXPART limits the moving-particle allocation for MOC/HMOC. PERCEL controls how far advection may move in one transport step. TVD requires PERCEL no larger than one. Compare solutions after changing tolerances or particle settings; successful termination alone is not an accuracy test.

### Analytical comparison

The analytical reference uses constant velocity, porosity and dispersion. It integrates the Green function over the **actual source volume** and over each receiving cell. The y and z boundaries reflect solute, matching the closed faces; the x direction is treated as infinite. A one-layer source therefore reduces to the thickness-normalised 2D solution. Pulse and continuous sources use a time convolution of the same kernel.

The unbounded 3D instantaneous point-source Green function is

$$
C=\frac{M}{n_e(4\pi t)^{3/2}\sqrt{D_xD_yD_z}}
\exp\!\left[-\frac{(x-x_s-v_xt)^2}{4D_xt}
-\frac{(y-y_s)^2}{4D_yt}-\frac{(z-z_s)^2}{4D_zt}\right].
$$

For the unbounded horizontal 2D case, replace the denominator by $4\pi n_e b t\sqrt{D_xD_y}$ and omit the z exponent. These point-source equations explain the plume shape; the comparison calculation uses finite volumes so that source dilution is consistent with MT3D.

A homogeneous analytical reference is not an exact solution for zoned or transient flow. The app therefore suppresses analytical error metrics for those cases. For eligible cases, the finite x boundaries must remain sufficiently far from the plume. The reference mass-retention check is a boundary-proximity diagnostic, not a proof that the finite and infinite domains are identical. Increase domain size and check sensitivity if the plume approaches either specified-head boundary.

### MODPATH comparison

MODPATH 7 uses the MODFLOW flow field and the same effective porosity to follow advective particle trajectories. It does not simulate dispersion or calculate dissolved concentrations. Particle clouds and paths can illustrate travel time and flow deflection, but their width must not be interpreted as a dispersive plume. A particle's represented source mass is only a quadrature weight for the release distribution; it is not a MODPATH solute mass budget. MT3D MOC particles and MODPATH particles serve different purposes.

### Reading the results

Check the plume shape and observation breakthrough curves together with the comparison table. A small mass-balance discrepancy can accompany substantial numerical spreading or oscillation. Keep the source, flow, transport parameters and grid fixed while comparing methods. Runtime measures elapsed wall time and can vary with machine load; compare repeated runs on the same machine before drawing performance conclusions.

Observation points are sampled at their containing cell; the realised cell location is shown. Cross-section positions also select the nearest grid section. The model retains signed numerical concentrations so that negative values are detectable. Logarithmic plume displays necessarily omit nonpositive concentrations; use a linear view and the minimum-concentration diagnostic to examine oscillations.

### References

- [MT3DMS advection package and method parameters — FloPy](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtadv.html)
- [MT3DMS source/sink mixing and mass-loading sources — FloPy](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtssm.html)
- [MT3DMS GCG solver parameters — FloPy](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtgcg.html)
- [Pollock (2016), User guide for MODPATH Version 7 — USGS](https://pubs.usgs.gov/publication/ofr20161086)
- [Wexler (1992), Analytical solutions for solute transport with uniform flow — USGS](https://pubs.usgs.gov/twri/twri3-b7/)
- [Official MODFLOW and related program executables](https://github.com/MODFLOW-ORG/executables)

The four analytical applications supplied for this development informed the teaching examples. Their point-source and concentration-boundary formulas are not directly substituted for the finite-volume mass-source benchmark used here.

### Heterogeneity and comparison series

The presets are homogeneous, random stochastic parameters, low-K lens, high-K channel and partial low-K barrier. The overview uses white for the reference material and colours the contrasting K cells; its legend gives K in m/s. Random parameters are assigned on a physical lattice: units close to the model-cell size give a fine cell-wise pattern; larger unit sizes give larger patches. K and Ss are sampled uniformly in log space; porosity is sampled uniformly. The same horizontal pattern spans all layers. This is a teaching random pattern, not a geostatistical field with a specified covariance.

A fixed random seed and fixed physical unit sizes preserve the material realization across numerical refinement. Each numerical cell samples the unit containing its centre, so a coarser grid can miss smaller features. Changing grid resolution alone does not resample the physical field. The original rectangle and transient input formats remain supported for reproducing older exported configurations outside the interface.

The newest completed run is displayed automatically. Changes to input signal or physical domain/source geometry start a new comparison series. Cell counts, cell widths and solution settings remain variants. Source geometry is snapped to cells, so inspect its realized footprint after refinement. FD cen means central finite differences.

Remove run tags to discard comparison runs. The displayed run can be selected separately. Top-view result plots include the computed head contours by default (h in metres), alongside concentration contours and colour fill. For one layer, x/y plots are concentration profiles. For several layers, x–z and y–z plots show concentration by colour and contour labels at each elevation, with the same concentration units as the top view.

### Plume focus and run names

Heterogeneous runs carry the compact suffix **het.**; run names remain stable when switching languages. **Focus on plume** uses 0.1% of the current positive peak in each displayed top-view plume by default. The threshold is adjustable. Qualifying cell edges receive a 20% margin on each side; visible, time-limited MODPATH paths are included. An empty view retains the full domain. Only top-view axis limits change: concentrations, sections and colour normalization remain unchanged.
