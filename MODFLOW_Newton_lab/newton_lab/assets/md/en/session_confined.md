# Sessions 1–4 · Confined groundwater flow

## 1 · Reconnect with the steady solution

**Objective:** distinguish a steady hydraulic gradient and recharge mound from the effect of a well.

- [ ] Apply **Restore requested initial model**. Keep **Confined formulation** on and **Transient simulation** off. Switch **Well active** off. <!-- task: confined_initial -->
- [ ] Check 31 × 31 cells, 100 m spacing, one layer, top 0 m and bottom −20 m, CHD heads 18 and 16 m, and K = 10⁻⁴ m/s. Explain why these elevations and heads describe confinement. <!-- task: confined_geometry -->
- [ ] Set recharge to 0. Predict a straight head profile from left to right. Select MODFLOW-2005, NWT and MF6 and run them. <!-- task: confined_linear -->
- [ ] Inspect the map and central cross-section. Turn on the **1-D steady recharge solution** overlay and compare all three engines. Explain why flow is effectively one-dimensional although the grid is two-dimensional. <!-- task: confined_reference -->
- [ ] Change recharge to 150 mm/year and rerun. Inspect the mound and the steady budget bars. Identify whether each CHD side supplies or receives water; the budget sums both sides into CHD IN and OUT. <!-- task: confined_recharge -->
- [ ] Turn the pumping well on at 20 L/s and rerun in steady state. Compare well abstraction and boundary flow. Explain why storage does not provide a persistent steady-state source. <!-- task: confined_steady_well -->

**Discuss:** why is an infinite-domain Theis solution not a steady-state well solution? What controls the eventual steady response in this finite model?

## 2 · Pumping, Theis drawdown and recovery

**Objective:** extend a familiar analytical solution to a two-dimensional numerical model and distinguish storage release from boundary capture.

- [ ] Use recharge 0, confined formulation and **Transient simulation** on. Under **Boundary conditions**, select **Pumping well**, with the well active at 20 L/s. Set 7 days pumping and 14 days recovery under **Temporal and spatial discretization**. <!-- task: pumping_setup -->
- [ ] Use Sₛ = 10⁻⁴ m⁻¹; compute S = Sₛb = 0.002. Confirm that OBS1 is 100 m east of the central well. Predict the sign and shape of the response. <!-- task: pumping_storage -->
- [ ] Run all three engines. Confirm that t = 0 is the no-well steady solution, the well operates until day 7, and the final snapshot is day 21. <!-- task: pumping_run -->
- [ ] Inspect snapshots at the end of pumping and recovery. Plot WELL and OBS1 over time, then display drawdown and the analytical observation reference. Explain why the well-cell head is not a borehole water level. <!-- task: pumping_theis -->
- [ ] Add observations farther away, for example two and five cells from the well. Rerun and compare arrival and recovery behavior. Distinguish numerical resolution from the analytical point-source idealization. <!-- task: pumping_observations -->
- [ ] Inspect actual and cumulative water budgets. Explain why storage release falls while boundary contributions grow, and why storage accumulation can occur after shutdown. <!-- task: pumping_budget -->
- [ ] Compare native runtime, iteration counts, convergence and budget discrepancy. Tighten tolerances or increase the number of time steps and test whether the head response changes appreciably. <!-- task: pumping_convergence -->
- [ ] Check boundary sensitivity: increase the model length / width to 6,100 m and use 61 × 61 cells at 100 m. Centre the well and replace OBS1 one cell beside it. Keep the other inputs unchanged. Compare the day-7 drawdown after subtracting each run's own baseline. Coordinate changes disable automatic history overlay, so export the CSVs for this domain test. Changing only the cell count at fixed full extent tests resolution. The CHD-centre separation is the full length minus one cell width. <!-- task: pumping_boundary -->

**Discuss:** lowering the pumping rate reduces drawdown, but does it delay hydraulic diffusion? Why might recovery be more boundary-sensitive than the first seven days of pumping?

## 3 · Injection as a reversed stress

**Objective:** transfer the confined pumping concept to injection and test linear symmetry.

- [ ] Return to the 31 × 31 confined transient model with recharge 0. Select **Injection well**, 20 L/s, 7 days injection and 14 days rest. Keep all hydraulic and numerical settings unchanged. <!-- task: injection_setup -->
- [ ] Predict a head rise that mirrors the pumping drawdown relative to the initial head. Run the three engines. <!-- task: injection_prediction -->
- [ ] Overlay the analytical reference at OBS1 and display drawdown: injection should appear as negative drawdown. Check the peak at day 7 and the relaxation during rest. <!-- task: injection_theis -->
- [ ] Compare with the preceding pumping computation where positions and discretization agree. Explain the change in the signs of WEL and storage flows. <!-- task: injection_compare -->

**Discuss:** which assumptions are needed for pumping and injection to be symmetric? Would dry cells, variable saturated thickness or head-dependent pumping reduction preserve that symmetry?

## 4 · Pumping followed by injection

**Objective:** combine known stresses and understand why equal injected and abstracted volumes do not necessarily restore all heads immediately.

- [ ] Select **Combined pumping / injection** under **Boundary conditions**. Use 20 L/s pumping for 7 days, 20 L/s injection for 7 days and 14 days rest. Set the durations in **Temporal and spatial discretization**. Predict the head at days 7, 14 and 28. <!-- task: combined_setup -->
- [ ] Run the model and inspect those three snapshots. Compare head histories at the well and observations. Explain the spatial memory of the first pumping period. <!-- task: combined_heads -->
- [ ] Inspect actual and cumulative WEL volumes. Verify 12,096 m³ pumped and 12,096 m³ injected if the rates remain fully applied. Explain why boundary exchange and storage may still be nonzero at the end. <!-- task: combined_budget -->
- [ ] Set the injection magnitude independently, for example 10 or 30 L/s, and rerun. Compare heads and budgets with the immediately previous computation. <!-- task: combined_rate -->
- [ ] Optional: enable **Expert settings** and select a rectangular K zone under **Parameters for the scenario**, with a multiplier of 0.1. Keep it away from the CHD columns, run again and explain asymmetric responses at observations on opposite sides of the well. Alternatively, choose random K and retain the same seed while comparing engines. <!-- task: combined_heterogeneity -->
- [ ] Optional: in expert **Temporal and spatial discretization**, subdivide the aquifer into five layers. Inspect the cross-section, add observations in different layers and explain the consequences of the app's fully penetrating well and fixed flow split. This is a vertically discretized model, not a partial-penetration well model. <!-- task: combined_layers -->
