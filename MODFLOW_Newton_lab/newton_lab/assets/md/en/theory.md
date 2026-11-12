### Physical and numerical setup

The horizontal cell width is uniform. CHD reservoirs occupy the left and right cell columns; the remaining outer faces are impermeable. Recharge is applied to active columns excluding the CHD reservoirs. A year is **365.25 days**. All native model inputs use **metres and seconds**.

The initial default has a confined thickness of 20 m, so

$$T = Kb = 0.002\;\mathrm{m^2/s}, \qquad S = S_s b = 0.002.$$

In confined mode, the top is fixed at **0 m** and the bottom is minus the selected thickness. In unconfined mode, the bottom is fixed at **0 m** and the selected top defines thickness. A head above a cell top is a potentiometric head, not an exposed water table.

### Time sequence

| Mode | Initialization | First stress | Second stress | Final phase |
|---|---|---|---|---|
| Steady | Linear initial guess | Selected well stress until steady | — | — |
| Regular transient | Solved steady state, no well | Pumping **or** injection, 7 days | — | No well, 14 days |
| Combined transient | Solved steady state, no well | Pumping, 7 days | Injection, 7 days | No well, 14 days |

The steady initialization is the first stress period of each native transient simulation. Its bookkeeping duration of one second is excluded from displayed elapsed time and cumulative volumes. Recharge and CHD heads remain unchanged throughout the sequence. Up to three wells share this schedule, each with independent pumping/injection magnitudes and a separate cell position. WELL, WELL2 and WELL3 are saved as separate head traces; water budgets sum their native flows.

### Analytical references

For a homogeneous confined aquifer and signed injection rate $Q$,

$$\Delta h(r,t)=\frac{Q}{4\pi T}E_1\!\left(\frac{r^2S}{4Tt}\right).$$

Pumping has $Q<0$. After shutdown at $t_p$, the change is $\Delta h(Q,t)-\Delta h(Q,t-t_p)$, where the second term is zero for $t\leq t_p$. The app offsets this head change by the numerical initial head at each observation. **Set recharge to 0** for the intended analytical experiment.

For initially unconfined observations, the optional approximation uses initial local saturated thickness $b_0$, $T_0=Kb_0$ and $S=S_y$. It transforms the linear head change by

$$\Delta h_u=\sqrt{b_0^2+2b_0\Delta h}-b_0.$$

This is a Jacob/Dupuit approximation. It does not resolve delayed yield, vertical unsaturated drainage or strong dewatering. Shutdown superposition followed by this transformation is also approximate. There is no analytical well-cell curve at radius zero. The analytical well overlay is limited to a single well; multi-well runs use the numerical comparisons.

The no-well steady comparison uses CHD **centre-to-centre distance** $L$, not outer grid width:

$$h(x)=h_L+(h_R-h_L)\frac{x}{L}+\frac{R}{2Kb}x(L-x)$$

for confinement, and

$$[h(x)-z_b]^2=[h_L-z_b]^2+\big([h_R-z_b]^2-[h_L-z_b]^2\big)\frac{x}{L}+\frac{R}{K}x(L-x)$$

for unconfined Dupuit flow, while the water table remains within the aquifer.

### Solver comparisons

MODFLOW-2005 uses **LPF + PCG**, NWT uses **UPW + NWT (XMD initially; GMRES also available)**, and MF6 uses **NPF + STO + IMS/BICGSTAB**, with Newton iteration initially enabled for convertible cells. MF6 uses `SS_CONFINED_ONLY` to align its elastic-storage treatment with the legacy formulations. The engines retain their native conductance and wetting/drying algorithms. MF2005 rewetting starts **off** and can be enabled in Expert settings. Cross-sections label MF2005 dry solver cells **Dry (inactive)** with a pale yellow fill and red cross-hatching, and NWT dry solver cells **Dry (active)** with a pale red fill. Grey hatching identifies cells excluded from the input domain, separately from cells that dry during a run. Dry reservoir layers above a CHD water level are inactive in every engine; they are not assigned a dry constant head.

NWT and MF6 use an explicit default pumping-reduction interval of **5% of cell thickness**. MODFLOW-2005 can deactivate dry well cells instead. The actual native WEL budget is always shown, allowing differences in stress delivery to be distinguished from differences in solution method.

At several layers, each well is fully penetrating with a fixed flow split based on initial saturated thickness. The app does not dynamically redistribute unused layer rates and does not solve a borehole head. This limitation matters during dewatering.

### Water budgets and diagnostics

All external native CBC flows are grouped into CHD, recharge, wells and storage. Positive flows enter groundwater; negative flows leave. Internal face flows are excluded from the whole-model budget. Both IN and OUT are retained before aggregation.

$$\mathrm{discrepancy}(\%)=100\frac{Q_\mathrm{in}-Q_\mathrm{out}}{(Q_\mathrm{in}+Q_\mathrm{out})/2}.$$

Transient cumulative volumes sum each solved end-step rate times its native time-step length. The initial steady step contributes no cumulative volume. Normal termination, absence of convergence-failure messages, complete head records and complete budgets are required before the app displays a run as converged.
