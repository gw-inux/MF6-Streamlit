## Experiment 1 Getting started with the MODFLOW Solver Lab

Explore how the size and formulation of a groundwater model affect its numerical solution. Begin
with the eleven-cell model used in the finite-difference learning activity, then investigate
convergence criteria, grid refinement, and unconfined flow.

### Learning objectives

After completing this experiment, you should be able to:

1. Configure and run the simple model, identify its specified-head boundaries, and use the head plots, analytical reference, water balance, and convergence diagnostics. Compare numerical and analytical heads at matching cell centres and interpret the reported head errors.
2. Explain the different meanings of head closure and residual closure in MODFLOW-2005 PCG, and investigate how changing a closure criterion affects a calculation.
3. Refine the spatial grid while retaining the boundary-to-boundary distance, and distinguish total cells from unknown-head cells.
4. Explain why the confined formulation in this experiment is linear and why head-dependent saturated thickness introduces nonlinearity in the unconfined formulation.
5. Interpret changes in heads, iteration counts, and runtime using controlled comparisons, including results that show little or no change.
6. Distinguish a MODFLOW implementation from its solution methods, and identify the methods offered by MODFLOW-2005, MODFLOW-NWT, and MODFLOW 6 in this app.

### Before starting

Complete the six preparation questions. Select **all correct answers** in each question. Use the
feedback to identify ideas to investigate during the experiment.

Work with one horizontal row, one layer, uniform hydraulic conductivity, uniform recharge, and a
steady-state calculation. Keep **Enable additional model complexity** switched off throughout this
experiment.
