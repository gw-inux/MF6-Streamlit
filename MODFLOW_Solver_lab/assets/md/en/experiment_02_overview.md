## Experiment 2 Layers, heterogeneous conductivity, and initial heads

Investigate how three MODFLOW implementations handle a vertically discretized unconfined aquifer.
Keep 51 cells along x, add layers, introduce a reproducible random hydraulic-conductivity field, and
test alternative numerical starting heads. Compare convergence robustness, computational effort, and
the resulting hydraulic solutions.

Your working hypothesis is that MODFLOW-NWT may handle difficult changes in saturation more robustly
than the conventional MODFLOW-2005 approach. Test that hypothesis; the fastest or most robust method
is not prescribed in advance.

### Learning objectives

After completing the experiment, you should be able to:

1. Relate vertical discretization to fully saturated, partly saturated, and dry model cells, and distinguish those states from unsaturated-flow simulation.
2. Compare MODFLOW-2005 / PCG, MODFLOW-NWT / GMRES, and MODFLOW 6 / IMS-CG using the actual formulation and settings of each implementation.
3. Use an analytical solution to verify an applicable numerical benchmark, and explain its limitations when vertical flow or heterogeneous conductivity is introduced.
4. Investigate heterogeneous conductivity while retaining the same physical field across numerical-method comparisons.
5. Explain how initial heads affect a steady-state numerical solution procedure and investigate the consequences of a guess close to the overall aquifer bottom.
6. Support conclusions with convergence status, water balance, meaningful head comparisons, saturation patterns, and clearly identified runtime and iteration measures.

### Before starting

Complete the six preparation questions. Select **all correct answers** in each question and read the
feedback.

Throughout this experiment, retain **one horizontal row**. Keep **2D horizontal grid (x–y)**
switched off. Adding vertical layers produces an x–z cross section and is a separate change from
adding a horizontal y direction.
