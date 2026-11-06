# Solver interface text

The `##` headings are stable text keys; only their contents are displayed.

## solver_use_expert_settings

Use expert settings

## sip_closure_note

SIP has a head-change test; it has no separate R-closure input.

## ims_closure_note

Basic head closure applies to outer and inner iterations; expert settings can separate them.

## nwt_expert_note

NWT writes SPECIFIED with the selected preset as its starting point. Basic closure and iteration limits remain above.

## ims_expert_note

These values override IMS preset controls. Basic outer closure and iteration limits remain above.

## solver_closure_criteria

**Closure criteria**

## solver_maximum_iterations

**Maximum iterations**

## solver_head_closure_m

Head closure (m)

## solver_r_closure_m_s

R closure (m³/s)

## solver_maximum_sip_iterations

Maximum SIP iterations

## solver_maximum_outer_iterations

Maximum outer iterations

## solver_maximum_inner_iterations

Maximum inner iterations

## solver_relaxation_relax

Relaxation (RELAX)

## solver_acceleration_accl

Acceleration (ACCL)

## solver_r_closure_fluxtol_m_s

R closure / FLUXTOL (m³/s)

## solver_pcg_preconditioner_npcond

PCG preconditioner (NPCOND)

## solver_polynomial_eigenvalue_option_nbpol

Polynomial eigenvalue option (NBPOL)

## solver_head_damping_damp

Head damping (DAMP)

## solver_sip_iteration_parameters_nparm

SIP iteration parameters (NPARM)

## solver_sip_seed_calculation_ipcalc

SIP seed calculation (IPCALC)

## solver_sip_seed_wseed

SIP seed (WSEED)

## solver_backtracking_residual_limit_m_s

Backtracking residual limit (m³/s)

## solver_xmd_head_closure_m

XMD head closure (m)

## solver_inner_head_closure_m

Inner head closure (m)

## solver_ims_residual_test

IMS residual test

## solver_ims_under_relaxation

IMS under-relaxation

## solver_under_relaxation_gamma

Under-relaxation gamma

## solver_dbd_theta

DBD theta

## solver_dbd_kappa

DBD kappa

## solver_dbd_momentum

DBD momentum

## npcond_help

1 = modified incomplete Cholesky; 2 = polynomial.

## nbpol_help

0 = calculate the eigenvalue estimate; 2 = assume an upper bound of 2. Used only with NPCOND=2.

## ipcalc_help

1 = calculate the seed; 0 = use WSEED.

## iacl_help

0 = CG; 1 = ORTHOMIN; 2 = Bi-CGSTAB inside XMD.

## ibotav_help

NWT bottom-head adjustment option; inactive for fully confined flow.

## thickfact_help

NWT saturation-smoothing interval as a fraction of layer thickness; relevant to convertible flow.
