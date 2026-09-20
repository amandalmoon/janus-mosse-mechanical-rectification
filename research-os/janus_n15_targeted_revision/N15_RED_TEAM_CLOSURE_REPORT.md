# N15 Red-Team Closure Rerun

**Scope:** targeted closure rerun after the N14 scope-only manuscript revision. The scientific calculations are unchanged; this pass checks only the three closure criteria requested by the user.

**Decision:** `CLOSED`

**Scientific blockers:** 0

**Unresolved Red-Team major issues:** 0

**Unresolved closure minor issues:** 0

## 1. Legacy thermal-boundary wording

**PASS.** Submission-facing main text and SI no longer contain the retired short-window 0.60/0.65/0.70 detectability-boundary history. The long-window stationary protocol is described directly, without retaining the superseded pilot-boundary narrative. Figure 6 and Table 3 likewise contain no retired extinction boundary.

## 2. Figure 6 / Table 3 / SI S8 / C15-C19 synchronization

**PASS.** The evidence chain remains numerically synchronized after the wording-only revision.

At `T*=0.70`, the pooled two-seed stationary estimate is:

- mean `(u,v) = (0.0369977, -0.0764475)`;
- 95% component intervals: `u [0.01265, 0.06132]`, `v [-0.10088, -0.05195]`;
- SI S8b Hotelling ratio: `6.33`, zero vector excluded;
- `P(v_cycle<0)=0.50802`;
- exact target-winding probability `P[(m,n)=(1,-1)]=0.01116`.

These values agree among the canonical Figure 6 source CSVs, manuscript Table 3, SI Table S8b / S8 text, and Claim-Evidence Matrix entries C15-C19. No new thermal claim was introduced in the closure revision.

## 3. Previous Red-Team Major limitations

### RT-M01 — damping dependence

**CLOSED.** Methods now state that `m*=1, gamma*=4` are reduced dynamical parameters and that the map is protocol conditioned. Discussion and SI additionally report the verified damping sweep: `(1,-10)`, `(1,-3)`, `(2,-2)` at `gamma*=1,2,3`; `(1,-1)` for `gamma*=4-6`; pinned `(0,0)` for `gamma*=8-10`. The manuscript explicitly rejects a material-only MoSSe phase-diagram interpretation.

### RT-M02 — loading-axis dependence

**CLOSED.** Introduction, Results, Discussion, Abstract, and Conclusion now state that the reported `+/-y` result is a chosen crystallographic loading-axis protocol, not a rotationally invariant friction scalar. The verified direction scan is summarized in Results: `|rho|~1.63e-4` on a symmetry-axis orientation and `|rho|~0.4186` on the tested strong-rectification orientation.

### RT-M03 — preparation dependence

**CLOSED.** Results now state explicitly that, at `theta=1.5 deg`, the ground-state branch has `Delta F_c=+1.812463`, whereas the competing metastable branch has `Delta F_c=-0.400638`. The headline response is therefore labeled ground-state-preparation conditioned rather than basin independent.

### RT-M04 — boundary-switch dynamics

**CLOSED.** The boundary result is now described as equilibrium family selection under independent fixed-twist re-preparation. The main text and SI explicitly state that no A-to-B transition path, activation barrier, continuous twist sweep, or hysteresis was calculated. The result is not presented as a kinetic switching prediction.

### RT-M05 — fixed rotation and COM/body-force loading

**CLOSED.** Methods and Limitations now state that the thresholds/dynamics use fixed imposed twist and a spatially uniform center-of-mass/body-force protocol. Rotational relaxation/applied torque, finite-stiffness spring pulling, edge pulling, center pulling, and corresponding load localization are explicitly outside the model.

### RT-M06 — elasticity independence

**CLOSED (unchanged).** The manuscript continues to state that the linear FEM and nonlinear bond-angle network share the same GSFE and target elastic constants and do not constitute independent full-3D atomistic validation.

## Visual/document QA

The revised main manuscript (15 pages) and SI (5 pages) were rendered after the final edit and every page was visually inspected. No clipping, overlap, broken table, orphaned caption, or missing glyph was observed.

## Gate decision

`RED_TEAM_CLOSED`

The manuscript now satisfies the short Red-Team closure gate and may proceed to an **independent Five Reviewer Paper Audit**. The reviewer pass must be performed from the manuscript/SI evidence packet without treating this closure decision or writer confidence as reviewer ground truth.
