**MB disc.** is the native MT3D mass-balance discrepancy; **Flow disc.** is the MODFLOW water-budget discrepancy. Both are percentages. **Ref. L1** is the pore-volume-weighted absolute concentration error divided by the analytical reference mass, evaluated at each run's final time. It is omitted for incompatible flow or boundary-affected cases.

**FD up** is upstream finite differences; **FD cen** is central finite differences (not a downwind method). A small balance discrepancy does not imply an accurate plume. MODPATH has no concentration mass-balance discrepancy.

A different input signal, source position/size selection, or physical domain extent starts a new comparison series. Changing cell counts, cell widths, saved outputs or solver settings retains the series. Hydraulic and dispersive parameters can also be explored as variants; use the saved configuration to identify these changes. Grid refinement can change the snapped source footprint: the table reports its realised dimensions.

**het.** marks heterogeneous material settings. Run labels remain stable when changing the display language.
