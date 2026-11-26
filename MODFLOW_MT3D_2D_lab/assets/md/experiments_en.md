Use **Flow & domain**, **Transport & source**, and **Post-processing & observations** to find the inputs. Use **Compare section profiles** to overlay runs in x/y views. The analytical control always sits on the right.

### 1. Follow a finite pulse

1. Begin with the default homogeneous one-layer model and TVD. Before running, estimate the travel distance $vt$ and the total pulse mass $\dot M\tau$.
2. Run the model. Move through the saved times and locate the leading and trailing parts of the plume.
3. Inspect the x and y concentration profiles and the observation breakthrough curve. Why does the signal at the observation point last longer than the source pulse?
4. Compare the numerical plume with the analytical reference, then inspect the mass-balance discrepancy. Does a good mass balance guarantee a good plume shape?

### 2. Separate physical and numerical spreading

1. Switch dispersion off and compare FD upstream, FD central and TVD without changing the source or grid.
2. Record runtime, minimum concentration, solute discrepancy and analytical error. Explain any spreading or negative concentrations that remain.
3. Restore dispersion. Repeat the method comparison. Identify the spreading shared by the analytical and numerical solutions.
4. Refine the grid. Check the realised source extent before interpreting differences: retaining a fixed number of source cells also changes the physical source volume.

### 3. Investigate characteristic methods

1. Keep the pulse experiment and compare MOC, MMOC and HMOC with TVD.
2. Open expert settings. Increase the particle density controls appropriate to the chosen method and repeat the run.
3. Compare runtime and mass discrepancy with the plume and breakthrough curve. Is the most expensive run also the most accurate?
4. Reduce PERCEL and repeat. Explain why a stable calculation may still depend on the transport step.

### 4. Compare a Dirac slug with a finite pulse

1. Choose Dirac and follow the finite initial source volume as it advects and spreads.
2. Export the Dirac result, then choose a short pulse with the same total mass $M=\dot M\tau$.
3. The signal change starts a new comparison series. Compare early and late plume shapes using the exported results. Why do they differ near the source even though their total masses are equal?
4. Add more observation points, including a point displaced in y. Relate peak arrival and peak concentration to longitudinal and transverse spreading.

### 5. Introduce a conductivity zone

1. Add a low-conductivity lens between the source and observation point. Keep the model steady initially.
2. Compare the resulting plume with MODPATH trajectories. Explain flow deflection, travel-time differences and dispersion across flow paths.
3. Try the high-K channel and partial barrier presets. Then choose random stochastic parameters. Compare small and large physical unit sizes; keep the seed and unit sizes fixed while refining the grid. Inspect cross-sections through and beside zones.
4. Explain why the homogeneous analytical error is unavailable for this experiment. Which alternative checks support confidence in the result?

### 6. Read the steady flow field

1. Compare the computed head contours for homogeneous material, a low-K lens and random heterogeneity. Explain the changes in hydraulic gradient and particle paths.
2. Change the specified-head difference and compare plume travel with MODPATH. Keep the source signal and geometry fixed.
3. Change specific storage Ss while keeping all other steady-flow inputs unchanged. Explain why it does not alter the computed flow or transport in this experiment.
4. Refine the numerical grid at fixed physical random-unit sizes. Check which geological features the coarse grid can resolve.

### 7. Extend the experiment to 3D

1. Enable expert settings and add at least three layers. Use a source in one selected layer instead of all layers.
2. Examine the x–z and y–z sections. Increase vertical transverse dispersivity and compare spreading between layers.
3. Choose random heterogeneity and inspect the MODPATH trajectories and concentration sections. The horizontal material pattern spans every layer; vertical concentration spreading arises from the localized source and vertical dispersion.
4. Repeat with a vertically uniform source and homogeneous materials. Explain why the solution becomes vertically uniform even though the numerical grid is three-dimensional.

For each experiment, record a prediction before running, compare the observed behaviour with that prediction, and use the numerical diagnostics to support your explanation.
