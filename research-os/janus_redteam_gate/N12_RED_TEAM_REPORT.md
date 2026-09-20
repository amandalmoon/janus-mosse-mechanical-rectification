# N12 Red Team Report — Janus MoSSe Manuscript

## Verdict

**CURRENT STAGE:** Red Team  
**RED TEAM GATE:** **BLOCKED**  
**Blocking issue:** `RT-B01` — thermal stationarity / burn-in convergence.  
**Manuscript status:** Do **not** send the present v2 directly to the Five Reviewer Paper Audit as the scientifically frozen draft. The static/symmetry/finite-size core remains intact, but the current high-temperature mean-vector claim is no longer verified under a longer equilibration test.

The Red Team treated the manuscript as read-only and attacked hidden assumptions, alternative mechanisms, numerical/statistical convergence, model-input validity, dynamical parameter dependence, state preparation, and mechanical boundary conditions.

---

## RT-B01 — BLOCKER: the T*=0.65 full-vector current claim fails a longer burn-in test

### Manuscript claim under attack

The current Abstract, Results 3.7, Discussion 4.3 and Conclusion state that the full two-component mean current vector remains statistically resolved at `T*=0.65` and becomes unresolved at `T*=0.70` under the stated finite-sample protocol.

### Why this was attacked

The production thermal protocol uses only 10 burn cycles before the 10 measured cycles. In a noisy multi-channel rocking system, 10 cycles may be insufficient for the periodically driven stochastic distribution to lose memory of the deterministic initial locked orbit. A trajectory-level bootstrap cannot repair a nonstationary initialization bias.

### Red-Team test

The same BAOAB model, `theta=1.5 deg`, `F0*=2`, `tau*=40`, `m*=1`, `gamma*=4`, `dt=0.02` and `N=1000` independent noise trajectories were rerun with 60 burn cycles before 10 measured cycles.

- `T*=0.65`, burn=60:
  - mean `(u,v)=(0.021794,-0.057146)`
  - SEs `(0.037483,0.039088)`
  - Hotelling `T^2=2.1690 < 6.0155`
  - bootstrap zero distance `d^2=2.1598 < q_0.95=6.0930`
  - **zero vector is not excluded**.

- `T*=0.60`, burn=60:
  - mean `(u,v)=(0.046885,-0.067288)`
  - SEs `(0.035786,0.036604)`
  - Hotelling `T^2=3.5955 < 6.0155`
  - bootstrap zero distance `d^2=3.6056 < q_0.95=6.0138`
  - **zero vector is not excluded**.

- `T*=0.55`, burn=60:
  - mean `(u,v)=(0.052250,-0.094316)`
  - Hotelling `T^2=7.6539 > 6.0155`
  - bootstrap zero distance `d^2=7.7740 > q_0.95=5.8282`
  - **zero vector is excluded**.

The initialization itself is not the problem: a separate `T*=0` BAOAB test at `dt=0.04,0.02,0.01` returns the deterministic `(1,-1)` orbit exactly. The issue is stochastic equilibration / stationary-periodic convergence.

### Consequence

The current `T*=0.65 resolved / T*=0.70 unresolved` thermal boundary is **REJECTED as claim-frozen evidence**. Even `T*=0.60` is not stable under the 60-cycle burn test. `T*=0.55` survives this particular longer-burn test, but it should not yet be promoted to the new frozen boundary until a declared burn-length convergence protocol is completed (for example 30/60/100 cycles with block/stationarity diagnostics).

### Required upstream resolution

Return to **Simulation -> Statistics -> Robustness** for the thermal branch:

1. predeclare burn lengths and a stationarity/convergence criterion;
2. rerun the high-temperature band with enough independent trajectories at converged burn length;
3. compare multiple starting states or show loss of initialization dependence;
4. report effect size and uncertainty, not only significance;
5. regenerate the thermal figure/table and Claim-Evidence records;
6. only then revise Abstract/Results/Discussion/Conclusion.

---

## RT-M01 — MAJOR: the vector-locking result is strongly damping-dependent

The manuscript correctly declares `m*=1` and `gamma*=4` as reduced parameters, but the dynamical story is much less parameter-robust than the headline can suggest.

At the canonical `theta=1.5 deg`, `F0*=2`, `tau*=40` point, a new damping sweep gives:

| gamma* | long-time result |
|---:|---|
| 0.5 | not period-1 under this test |
| 1 | `(1,-10)` |
| 2 | `(1,-3)` |
| 3 | `(2,-2)` |
| 4 | `(1,-1)` |
| 5 | `(1,-1)` |
| 6 | `(1,-1)` |
| 8 | `(0,0)` |
| 10 | `(0,0)` |

Thus the canonical winding and even moving-versus-pinned state are not material-only consequences of the GSFE. They are properties of the **specified reduced dynamical protocol**.

**Required action:** either add a damping/mass sensitivity map or narrow every dynamical claim to `m*=1, gamma*=4` and avoid implying an experimentally calibrated MoSSe mode-locking phase diagram.

---

## RT-M02 — MAJOR: static rectification is strongly scan-direction selective

The manuscript studies only `+/-y` loading. A new full-2D static direction scan at `N=127`, `theta=1.5 deg` shows that the prepared-ground threshold asymmetry is almost zero along one crystallographic symmetry axis and maximal near the tested axis.

Representative values:

| loading-axis angle | rho |
|---:|---:|
| 0 deg | `+1.63e-4` |
| 10 deg | `-0.1103` |
| 20 deg | `-0.2326` |
| 30 deg | `-0.4186` |
| 40 deg | `-0.2330` |
| 50 deg | `-0.1106` |
| 60 deg | `-1.63e-4` |

The tested `+/-y` direction is symmetry-equivalent to the strongly rectifying direction, not a direction-independent property.

**Consequence:** the existence of directional rectification survives, but broad wording such as “the contact rectifies mechanically” should be understood as **axis-conditioned**. An angular/polar threshold map would materially strengthen the paper and remove a potential cherry-pick criticism.

---

## RT-M03 — MAJOR: the sign is preparation dependent

At `theta=1.5 deg`, the lower-energy prepared branch has

`Delta F_c = +1.812463`,

whereas the competing metastable zero-force minimum has

`Delta F_c = 0.211059 - 0.611697 = -0.400638`.

Therefore the *same material landscape* supports opposite directional signs depending on which zero-force basin is prepared. The manuscript is transparent about branch-following, but the experimental preparation rule remains unspecified.

**Consequence:** “intrinsic” cannot mean preparation-independent directionality. It can only mean that a transverse guide is unnecessary **conditional on ground-state preparation at fixed twist and loading axis**.

**Required action:** quantify the inter-minimum barrier/preparation kinetics or keep every headline directionality claim explicitly state-conditioned.

---

## RT-M04 — MAJOR: the boundary sign reversal is an equilibrium re-preparation result, not yet a twist-sweep prediction

The triangular A/B zero-force energy crossing proves that the equilibrium ground-state label changes. It does **not** prove that a contact already occupying A will switch to B at the crossing during a twist sweep. A finite A->B barrier can generate hysteresis and postpone or suppress the actual state change.

The current edge-weight test moves the equilibrium crossing but does not calculate the A/B transition barrier or twist-sweep kinetics.

**Required action:** either compute barrier/hysteresis across the crossing or rename the claim as an **equilibrium / ground-state-reprepared registry-switch reversal**.

---

## RT-M05 — MAJOR: “unguided” is translational, not fully mechanically unconstrained

The center of mass is free in the 2D registry plane, but two strong mechanical constraints remain:

1. twist angle is imposed and has no rotational degree of freedom or torque relaxation;
2. the force is a uniform COM/body-force tilt, not a finite-stiffness spring, edge pull, or center pull.

Both are known to matter in finite vdW sliding contacts. They can alter stress localization, pathway selection, rotational alignment, and depinning.

**Required action:** make `fixed twist` and `uniform-force loading` part of the headline model definition and limitations. A spring/edge-driven or rotational test would be a stronger upstream validation if the paper intends experimental-device language.

---

## RT-M06 — MAJOR: FEM/VFF agreement is useful but not fully independent material validation

The linear FEM and nonlinear bond-angle model share:

- the same local GSFE;
- the same finite-contact geometry;
- the same target small-strain elastic constants;
- the same projected rigid modes.

At the nominal `theta=1.5 deg` endpoint the reported distortions are sub-percent, so close agreement between a nonlinear network and its matched linear continuum limit is expected. The comparison rules out a narrow linear-discretization artifact, but it does not strongly probe out-of-plane reconstruction, nonlocal edge mechanics, or atomistic chemistry.

**Required action:** retain this as **in-plane representation robustness**; do not describe it as independent atomistic/material validation.

---

## RT-R01 — residual material-input uncertainty, but the new stress test is favorable

A remaining weakness is that the published three-shell Fourier coefficients are treated as exact; the raw 9x9 DFT-fit covariance/error model is not available in the current evidence chain.

As an adversarial internal stress test, the Red Team varied:

- `phi_1` by `+/-2, +/-5, +/-10 deg`;
- `phi_2` and `phi_3` by `+/-5, +/-10 deg`;
- the second/third-shell amplitudes together from `0x` to `5x` their published values.

Across all tested variants, the prepared static split kept the same sign, with `rho` ranging approximately `0.361-0.456`.

This makes a fragile-fit explanation less plausible, but it is **not** formal propagation of DFT uncertainty. The manuscript should continue to say “conditional on the published Fourier parameterization.”

---

## Adversarial tests that the paper survived

### RT-P01 — drive phase and initial zero-force basin

For eight forcing phases and both stable zero-force minima, representative states `(1,-1)`, `(1,-2)`, `(2,-3)`, `(3,-4)`, `(2,-7)` plus transition-adjacent points all converged to the same expected winding after transients. This weakens the criticism that the representative deterministic locking is merely a phase-of-drive or initial-basin artifact.

### RT-P02 — zero-noise BAOAB consistency

At `T*=0`, BAOAB reproduces `(1,-1)` at `dt=0.04, 0.02, 0.01`. The thermal blocker is therefore not caused by a deterministic-limit mismatch between integrators.

### RT-P03 — moderate Fourier-parameter stress test

The static directional sign survived every tested coefficient perturbation. This supports qualitative robustness of the rigid static mechanism, while leaving source-level DFT uncertainty formally open.

---

## Red-Team status by manuscript layer

- **Static prepared-state depinning:** survives Red Team, with state-preparation and loading-direction scope required.
- **Same-spectrum inversion controls:** survives, but causal language should refer to the symmetry source of the ensemble/ground-state response rather than all possible single-basin deterministic responses.
- **Compact finite-size similarity:** no new blocker found.
- **Boundary reversal:** survives only as an equilibrium ground-state-reprepared result until transition barriers/hysteresis are checked.
- **Deterministic mode locking:** numerically valid at the declared `m*=1, gamma*=4` protocol; strong damping dependence prevents broader material-level interpretation.
- **Thermal current:** **BLOCKED** pending stationarity/burn-length convergence.
- **In-plane relaxation:** useful robustness evidence, but not independent full atomistic validation.
- **Novelty:** no new novelty contradiction beyond the already frozen `LIKELY NOVEL` combination-level status.

---

## Next Gate

The correct next action is **not yet Five Reviewer Paper Audit**.

Route `RT-B01` upstream:

`Simulation -> Statistics -> Robustness -> Verified Results -> thermal Figure/Table -> Claim-Evidence Matrix -> manuscript thermal revision -> short Red-Team closure check`

Only after `RT-B01` is closed should the scientifically frozen manuscript proceed to the independent Five Reviewer Paper Audit.
