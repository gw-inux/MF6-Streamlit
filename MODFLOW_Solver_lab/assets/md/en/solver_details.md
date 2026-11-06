
#### Models and methods

| Model | Solver choices | Main controls |
|---|---|---|
| MODFLOW-2005 | PCG or SIP | Head closure, iteration limits; PCG residual closure and relaxation; SIP acceleration |
| MODFLOW-NWT | Newton with GMRES or XMD | Head and flux closure, iteration limits, complexity preset |
| MODFLOW 6 | IMS with CG or BICGSTAB | Head and residual closure, iteration limits, complexity preset |

- **PCG**: preconditioned conjugate gradients. **SIP**: strongly implicit procedure.
- **NWT** uses Newton's method with the UPW flow package.
- **MODFLOW 6** uses NPF with Picard iteration in this app; both IMS methods
  remain available. Diagonal scaling is enabled initially.

#### Iterations and stopping criteria

- **Outer iterations** update the equations, including head-dependent
  conductances. **Inner iterations** solve the current linear system.
  SIP reports its own iteration count.
- **Head closure** limits the change between iterates (m), not the error
  relative to the exact solution. **Flow closure** tests a residual (m³/s);
  the norm differs between solvers. SIP has no separate flow-closure input.
- Inspect the water balance and, where available, the analytical head error
  as well as the convergence flag. Solver iterations are not physical time.

#### Settings in this app

- Head closures start at **1e-4 m**. Main closure values and iteration limits
  are retained when switching methods or presets within each MODFLOW model.
- **SIMPLE / MODERATE / COMPLEX** change NWT or IMS solution strategies;
  they do not guarantee accuracy or increase your chosen iteration limits.
- **Expert settings** expose advanced controls. NWT uses SPECIFIED when
  required to apply those edits; the remaining preset values are retained.

#### Solver documentation

[PCG](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/pcg.htm) ·
[SIP](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/sip.htm) ·
[NWT](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/nwt_newton_solver.html) ·
[MODFLOW 6 IMS](https://modflow6.readthedocs.io/en/6.7.0/_mf6io/sln-ims.html)
