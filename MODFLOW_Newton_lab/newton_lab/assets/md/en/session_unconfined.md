# Sessions 5–8 · Unconfined groundwater flow

**Starting point:** switch **Confined aquifer** off. The aquifer bottom is then fixed at **0 m**, and **Aquifer top** is the editable geometric parameter (initially **20 m**). The CHD heads of **18 and 16 m** lie inside the aquifer. The unconfined teaching preset applies these values and recharge **0**.

The thickness input is available only in confined mode, where the top is fixed at 0 m. Switching back restores the previously selected confined thickness. Hydraulic parameters and boundary heads are retained when switching formulation.

## 5 · Steady unconfined flow

**Objective:** connect numerical water-table behavior with the familiar Dupuit solution and distinguish head from saturated thickness.

- [ ] Apply **Use unconfined teaching preset**. Keep transient mode off and switch the well off. Verify that **Confined formulation** is off and both CHD heads lie inside the aquifer. <!-- task: unconfined_initial -->
- [ ] Predict the water-table shape between the boundaries. Run MODFLOW-2005, NWT and MF6, inspect the central section, and activate the steady analytical overlay. Compare head and squared saturated thickness. <!-- task: unconfined_steady -->
- [ ] Introduce modest recharge, for example 25 mm/year, and rerun. Increase it gradually and identify when a head approaches the aquifer top. The free-surface analytical expression is masked where it would exceed the top. <!-- task: unconfined_recharge -->
- [ ] Inspect CHD and recharge bars and the water-budget discrepancy. Explain why differences in intercell conductance averaging can produce small numerical differences even when every run converges. <!-- task: unconfined_steady_budget -->

## 6 · Pumping and dewatering

**Objective:** distinguish storage release by water-table drainage from confined elastic storage, and investigate wetting/drying algorithms.

- [ ] Set recharge to 0. Enable the well and transient mode; select regular pumping at 20 L/s for 7 days with 14 days recovery. Use Sᵧ = 0.2 and Sₛ = 10⁻⁴ m⁻¹. <!-- task: unconfined_pumping_setup -->
- [ ] Run all three engines and compare with the confined response. Explain the smaller far-field response associated with the larger storage coefficient. <!-- task: unconfined_pumping_run -->
- [ ] Inspect heads, drawdown and the approximate unconfined analytical overlay at OBS1. Explain the assumptions of the Jacob/Dupuit correction and why it does not describe delayed drainage or large drawdown. <!-- task: unconfined_approximation -->
- [ ] Inspect end-of-pumping and recovery cross-sections, actual well rates and storage budgets. Count dry cells and distinguish them from explicitly inactive cells. <!-- task: unconfined_dry_check -->
- [ ] For a drying challenge, first reduce recharge to 0, then increase pumping stepwise or lower the initial CHD heads. Change only one input at a time. Observe the first appearance of dry cells, flow reduction or a failed run. Do not interpret failed results as a physical solution. <!-- task: unconfined_challenge -->
- [ ] Enable **Expert settings**, then use **Numerical solver** to compare MODFLOW-2005 rewetting enabled/disabled, NWT GMRES/XMD, and MF6 Newton/Picard. Keep physical inputs, time steps and appropriate tolerances comparable. Select a reference engine in Results and compare the maps, section symbols, head histories and budgets. Record which cells reactivate during recovery and whether the requested pumping was actually delivered. <!-- task: unconfined_algorithms -->
- [ ] Optional: set five layers in expert **Temporal and spatial discretization** and repeat. Track the uppermost wet-cell head as the upper layer dries. Check observation layer numbers; an observation in a dry layer has a missing head, rather than a fabricated water level. <!-- task: unconfined_layers -->

**Discuss:** large differences between engines are not guaranteed in a mildly nonlinear, fully wet case. They become especially informative near drying/rewetting or when well-flow reduction changes the actual stresses.

## 7 · Injection and rewetting

**Objective:** understand why injection need not mirror pumping in a convertible aquifer.

- [ ] Restore the unconfined preset and select transient regular injection: 20 L/s for 7 days, then 14 days rest. Keep recharge at 0. Predict how increasing saturated thickness changes transmissivity. <!-- task: unconfined_injection_setup -->
- [ ] Run all engines. Compare the rise and recovery with the previous unconfined pumping case. Use the same observation cells and compare each run relative to its own starting head. <!-- task: unconfined_injection_run -->
- [ ] Inspect the analytical approximation only while its small-change and unconfined assumptions remain appropriate. Identify any cells whose heads rise above the aquifer top and become confined. <!-- task: unconfined_injection_reference -->
- [ ] Inspect storage accumulation, actual injected flow and CHD exchange. Explain why the head change can be asymmetric with pumping even when the magnitudes and durations match. <!-- task: unconfined_injection_budget -->

## 8 · Combined operation, nonlinear memory and heterogeneity

**Objective:** combine pumping and injection where saturated thickness, cell status and conductivity vary.

- [ ] Select combined operation: 7 days pumping, 7 days injection and 14 days rest. Start with 20 L/s for both stresses, recharge 0, and the unconfined initial heads. <!-- task: unconfined_combined_setup -->
- [ ] Inspect the day-7, day-14 and day-28 maps and sections. Explain why injected water can restore the local well head before the full drawdown cone has recovered. <!-- task: unconfined_combined_snapshots -->
- [ ] Compare requested and actual WEL volumes. If pumping was reduced by dewatering, equal requested magnitudes no longer imply equal actual volumes. <!-- task: unconfined_combined_actual -->
- [ ] Repeat a controlled drying challenge from session 6. Compare MODFLOW-2005 rewetting and the Newton formulations during the switch to injection. Inspect convergence and mass balance before interpreting differences. <!-- task: unconfined_combined_drying -->
- [ ] Optional: introduce a rectangular K zone or random K in expert **Parameters for the scenario**, add observations on both sides and rerun. Keep the random seed unchanged when comparing engines. Describe separately the effects of heterogeneity, nonlinear storage/transmissivity and solver behavior. <!-- task: unconfined_combined_heterogeneity -->
- [ ] Export head histories, water budgets, configuration and the run-history table. Write a short explanation supported by one head plot, one budget plot and the convergence diagnostics. <!-- task: unconfined_conclusion -->
