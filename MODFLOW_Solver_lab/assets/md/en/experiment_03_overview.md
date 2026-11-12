## Experiment 3 From one dimension to large 2D and 3D models

Extend the familiar unconfined model into the horizontal x–y plane. First investigate a homogeneous,
isotropic aquifer whose solution remains independent of y. Use the analytical solution to check that
numerical result while increasing the grid size. Then introduce heterogeneous hydraulic
conductivity, test different initial heads, and add vertical layers.

The central question is: **How do model size, spatial complexity, and saturation affect the effort
and reliability of a numerical solution?** Compare the configured MODFLOW-2005, MODFLOW-NWT, and
MODFLOW 6 procedures using evidence from your own runs. Predict what might happen, but leave the
outcome open.

### Learning objectives

After completing the experiment, you should be able to:

1. Explain when a homogeneous, isotropic 2D model retains a one-dimensional solution, and check that solution against an applicable analytical reference across the domain.
2. Calculate horizontal and three-dimensional cell counts, and distinguish system size, iteration count, work per iteration, and measured runtime.
3. Compare the configured MODFLOW procedures while controlling the hydraulic inputs, recording numerical settings, and assessing solution quality before ranking performance.
4. Distinguish a heterogeneous conductivity field from a random initial-head field, and preserve the appropriate spatial arrays in controlled comparisons.
5. Explain the numerical implications of near-bottom starting heads while distinguishing prescribed boundary heads, positive saturated thickness, and a hypothetical exact-zero start.
6. Extend a model to three dimensions in stages, respect the cell-count limit, and use convergence, budgets, heads, and saturation patterns to support conclusions about large models.

### Before starting

Complete the six preparation questions. Select **all correct answers** in each question and read the
feedback.

Experiment 2 introduced initial-head sensitivity in a vertical cross section. Here you apply that
understanding to horizontal 2D and full 3D models. In this experiment, **2D** means one layer with
many rows and columns in x–y; **3D** means that horizontal grid with multiple vertical layers.
