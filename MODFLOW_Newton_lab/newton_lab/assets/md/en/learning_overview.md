**Learning path:** connect a familiar steady-flow solution to transient drawdown, reverse the stress to understand injection, and combine both operations. Repeat the sequence with a water table and investigate the role of drying and rewetting.

For every experiment: **predict → run → inspect heads and budgets → explain → change one input**. Record the solver, physical inputs and time discretization before interpreting differences. Check marks document progress; they do not apply settings.

The separate instruction window contains only the instructions and checklists. The app retains the previous computation for comparison and the last ten engine runs for diagnostics.

**Finding the controls:** the three-column expanders follow the MODFLOW Solver Lab. Use **Show full settings** for hydraulic properties and storage. **Expert settings** adds layers, K heterogeneity and solver options inside the existing expanders. Well operation, rates and location belong to **Boundary conditions**. Grid resolution, layers, period durations and time steps belong to **Temporal and spatial discretization**. Observations have their own expander. Changing a display option does not run the model.

**Comparing engines:** select several engines before running. In Results, choose a reference and enable engine comparison. The plan view shows the reference and the selected engine's deviation (other − reference); the cross-section uses larger, unfilled symbols for other engines. Head and budget histories identify the models and can show the same comparisons. Use the compact diagnostics table directly below the cross-section to compare convergence, iterations, runtime and budget discrepancies.

**Multiple wells:** select one, two or three wells in Boundary conditions. Set each well's rates and cell position; all wells use the same selected operation and stress-period durations. Start the analytical exercises with one well, then add wells to explore interference numerically.
