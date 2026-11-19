## introduction

Explore conservative solute transport along a groundwater flow path using a simple one-dimensional model. Compare MT3DMS with analytical solutions to see how discretization and numerical methods affect the transport signal.

## concept_explanation

Imagine a narrow stream tube following a groundwater flow path through a homogeneous, saturated aquifer. Water moves steadily along this path. A conservative solute enters at its upstream end and is carried by advection; dispersion can spread the signal along the path.

This idealized one-dimensional setting helps reveal how the numerical transport method, cell size and time step affect the computed signal. Compare MT3DMS with the analytical solution to examine front spreading, oscillations, travel time and mass balance. Choose the inlet signal and transport processes first, then compare up to ten numerical variants of that scenario.

## concept_caption

Schematic stream tube with steady one-dimensional flow and an observation point at 250 m. No water or solute crosses the lateral boundaries; transverse dimensions are not to scale.

## concept_response_caption

Illustrative analytical responses to a 400 d block input with C/Cref = 1 and v = 0.24 m/d. Green: pure advection; blue: longitudinal dispersivity 10 m, D = 2.4 m²/d and zero molecular diffusion. These fixed illustrations are independent of the current model settings.

## front_task

1. Start with continuous input, 21 cells, upstream finite differences and dispersion switched off. Predict the front position at day 2000 from the pore velocity.
2. Run the model. Locate the analytical front and examine the numerical concentrations on both sides.
3. Repeat with TVD, then with 101 cells. Which change sharpens the front? Compare the profile error with the solute mass discrepancy.

## spreading_task

1. Choose continuous input, activate dispersion and set longitudinal dispersivity to 10 m with effective diffusion at zero. Run TVD with 21 cells and inspect the analytical profile.
2. Repeat with 101 cells and then with upstream finite differences. Which part of the spreading is also present in the analytical solution?
3. Inspect the breakthrough curves at 250 m. To investigate pure advection, switch dispersion off and start a new comparison. Changing a setting under “Inlet and transport” clears the saved variants.

## impulse_task

1. Select block input with a duration of 400 d. Follow the leading and trailing edges of the pulse in the profile and at 250 m.
2. Start a new scenario with a Dirac impulse, an area of 50 d and a numerical width of 50 d. Use 101 cells and a dispersivity of 10 m. Record the applied-pulse and ideal-impulse RMSE.
3. Reduce the width to 10 d at the same area and run the new scenario. Compare the recorded errors, then refine the grid within this scenario and check the mass budget again.

## theory

The confined aquifer is 1 m thick and 1 m wide. Specified heads of approximately 6.944 m and 0 m act at the first and last cell centres, 1000 m apart. With $K=10^{-4}$ m/s and effective porosity $n_e=0.25$, the Darcy flux is 0.06 m/d and the pore velocity $v$ is 0.24 m/d. The interior starts solute-free. Outflow carries the resident concentration. Concentrations are scaled by $C_{\mathrm{ref}}=1$ g/m³, equivalent to 1 mg/L.

For longitudinal dispersivity $\alpha_L$ and effective molecular diffusion $D_e$, the lab solves $\partial C/\partial t=D\,\partial^2 C/\partial x^2-v\,\partial C/\partial x$ with $D=\alpha_L v+D_e$. With dispersion switched off, a signal travels downstream by $vt$.

For $D>0$, the unit step response to a prescribed inlet concentration on a semi-infinite column is

$$
S(x,t)=\tfrac12\left[\operatorname{erfc}\!\left(\frac{x-vt}{2\sqrt{Dt}}\right)
+e^{vx/D}\operatorname{erfc}\!\left(\frac{x+vt}{2\sqrt{Dt}}\right)\right],\quad t>0.
$$

A continuous input of height $H$ gives $HS(x,t)$. A block of duration $\tau$ gives $H[S(x,t)-S(x,t-\tau)]$, where the delayed term is zero until switch-off.

For an ideal Dirac at the inlet with concentration–time area $A=\int(C_{\mathrm{in}}/C_{\mathrm{ref}})\,dt$, the interior solution is

$$
A\frac{\partial S}{\partial t}
=A\,\frac{x}{\sqrt{4\pi D t^3}}\exp\!\left[-\frac{(x-vt)^2}{4Dt}\right].
$$

MT3DMS applies a short rectangle of width $\varepsilon$ and height $A/\varepsilon$. This preserves the area under the **inlet concentration** history. The actual solute mass budget also includes the dispersive flux at the prescribed boundary. At $D=0$ the ideal impulse travels at $v$ and has no finite pointwise peak.

## profile_hint

The numerical profiles use cell-centre concentrations. Intermediate times use linear interpolation between saved transport steps. Day 2000 uses the final solver output.

## breakthrough_hint

MT3DMS saves every transport step. The plotted concentration is interpolated between cell centres at the selected distance. Advective travel time at this location is {t:.1f} d.

## balance_hint

MT3DMS reports the signed cumulative solute discrepancy as a percentage of the mean absolute mass in and mass out, including storage. The graph uses the TOTAL IN–OUT column of the MAS file. Small budget discrepancies can coexist with a smeared front.

## dirac_reading

The dashed curve follows the finite MT3DMS inlet pulse. The dotted curve shows the ideal Dirac response. At zero dispersion the dotted vertical line locates the impulse in space or time. Its height carries no concentration information.

## outlet_hint

For {ids}, the analytical unit-step concentration at 1000 m reaches at least 1% by day 2000. The downstream part of the finite MT3DMS column can be influenced by its outlet. This screening check also covers pulses, which may have smaller outlet concentrations.

## table_hint

All saved variants are scored on the same 90 intervals of 10 m between 50 and 950 m. RMSE and MAE compare the final profile with the analytical solution for the applied inlet. Both are expressed in C/Cref.

## mass_warning

{ids} exceeds 1% absolute solute mass discrepancy at day 2000. Inspect its mass-balance curve as well as its profile. A short pulse on a coarse grid can be missed by a particle method.

## metrics_notes

The comparison treats each numerical cell concentration as constant over its cell and averages it by overlap with each 10 m scoring interval. The analytical concentration is integrated over the same interval. The common interval avoids the two boundary cells even on the coarsest grid. RMSE is the square root of the mean squared residual, and MAE is the mean absolute residual.

For a Dirac run, the additional RMSE uses the ideal impulse on the same intervals. At zero dispersion its spatial weight is $vA$. An impulse on a shared interval edge contributes half of that weight to each side. Errors scale with input amplitude. Hold the signal and its strength fixed when comparing methods.

Runtime is elapsed wall time for the two native solver processes. Input writing, output reading, plotting and error calculations are excluded. The water budget is the last MODFLOW listing discrepancy. The grid Péclet number is $v\Delta x/D$ and is infinite for pure advection. Centred differences can produce concentrations outside the inlet range. The plots retain these values.

## references

- The supplied course notebook `TRANS_1D_MT3D.ipynb`, conservative cases 1 and 2. The initial 21-cell grid is the course version of the benchmark.
- Zheng and Wang (1999), *MT3DMS*, example 1. [Benchmark description and parameters](https://modflow6-examples.readthedocs.io/en/latest/_examples/ex-gwt-mt3dms-p01.html)
- Wexler (1992), *Analytical Solutions for One-, Two-, and Three-Dimensional Solute Transport in Ground-Water Systems with Uniform Flow*, examples with a prescribed inlet concentration. [USGS TWRI 3-B7](https://pubs.usgs.gov/twri/twri3-b7/pdf/twri_3-B7_a.pdf)
- Pérez Guerrero and colleagues (2013), *Analytical solutions of the one-dimensional advection–dispersion solute transport equation subject to time-dependent boundary conditions*. [DOI](https://doi.org/10.1016/j.cej.2013.01.095)
- FloPy documentation for the [MT3DMS advection package](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtadv.html) and [specified inlet concentrations](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtssm.html).

## method_upwind

The upstream concentration sets the advective flux across each cell face. Watch for a broadened front when physical dispersion is off.

## method_central

The face flux uses concentrations on both sides. On a coarse, advection-dominated grid this can produce oscillations near a sharp front.

## method_tvd

The third-order ULTIMATE TVD scheme limits advective fluxes near sharp gradients. Compare its front width with upstream differences.

## method_moc

The method of characteristics tracks particles forward. Here MT3DMS initially places four particles in cells with a sufficiently large concentration gradient.

## method_mmoc

The modified method of characteristics traces trajectories backward to estimate the concentration carried into a cell.

## method_hmoc

The hybrid method switches between forward MOC and backward MMOC according to the local concentration gradient.
