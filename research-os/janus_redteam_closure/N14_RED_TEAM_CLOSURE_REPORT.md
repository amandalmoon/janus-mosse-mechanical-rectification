# N14 Short Red-Team Closure

**Scope:** read-only closure audit of `Janus_MoSSe_ThermalStationary_Manuscript_v3.docx`, `Janus_MoSSe_ThermalStationary_SI_v3.docx`, Figure 6, Table 3, and Claim-Evidence Matrix v2.

**Decision:** `NOT_CLOSED_YET`

**Blockers:** 0

**Unresolved Major scope issues:** 5

**Minor cleanup issues:** 1

The thermal stationarity blocker `RT-B01` is closed. The remaining problems are manuscript-scope wording issues that can be resolved from already verified Red-Team evidence; no new calculation is required for the closure actions below.

## 1. Legacy thermal-boundary wording

### Result: PARTIAL PASS / strict-cleanup criterion fails

Current scientific claims are corrected everywhere that matters numerically:

- Abstract: stationary mean vector remains nonzero through sampled `T*=0.70`; no extinction scale inferred.
- Results 3.7: long-window `60 burn + 100 measured` protocol; no critical boundary inferred.
- Figure 6: no 0.65/0.70 extinction boundary; panel (b) explicitly says zero-current rejection is not a thermal critical scale.
- Table 3: stationary current nonzero through sampled `T*=0.70`; no extinction temperature established.

However, two historical references to the retired short-window boundary remain in publication-facing prose:

1. **Main Discussion P94:** “The earlier 0.60/0.65/0.70 detectability boundaries obtained from short observation windows are therefore retired.”
2. **SI S8 P40:** “The earlier 10-burn + 10-measure pilot boundaries shift with observation length and are therefore retired rather than interpreted as physical thermal thresholds.”

These statements are scientifically correct, but they fail the user's strict criterion that old-boundary wording should not remain in the manuscript/SI. Preserve that history in Research OS audit artifacts instead of the submission-facing manuscript.

**Issue:** `RTC-MIN01` — remove the two historical boundary sentences from publication-facing text.

## 2. Figure 6 / Table 3 / SI S8 / C15-C19 synchronization

### Result: PASS

The evidence chain is internally synchronized.

### C15 — exact winding identity vs mean drift

- Figure 6(c): exact target winding is small at high T while cycle-sign bias remains weakly nonzero.
- SI S8a/S8b: target probability is about `0.011-0.016` over pooled `T*=0.50-0.70`.
- C15: identical interpretation and scope.

### C16 — v component

At `T*=0.70`, pooled two-seed `N=1000` values agree:

- Figure 6(a): `mean v = -0.0764475`, 95% interval `[-0.100881,-0.051955]`.
- SI S8b: `-0.07645`, `[-0.10088,-0.05195]`.
- Table 3: same rounded values.
- C16: same values and interpretation.

### C17 — full 2D mean vector

At `T*=0.70`:

- Figure 6(a): `(u,v)=(0.036998,-0.076448)`.
- Figure 6(b): Hotelling ratio `T_H^2/T_crit^2 = 6.326 > 1`.
- SI S8b: `(0.03700,-0.07645)`, ratio `6.33`, zero vector excluded.
- Table 3: same vector and component intervals.
- C17: same vector; reports the equivalent unnormalized test statistic versus threshold rather than the ratio.

No contradiction is present.

### C18 — cycle-sign statistic

At `T*=0.70`:

- Figure 6(c): `P(v_cycle<0)=0.50802`, target winding `0.01116`.
- C18: same values.
- Main Results P80: same values and trajectory-level interval.

### C19 — timestep compatibility

- SI S8 P40 and C19 both state targeted `dt=0.04, 0.02, 0.01` reruns at `T*=0.60,0.65,0.70` differ by no more than `1.12` combined SE in either mean-current component.

### Important non-conflict

SI Table S8a uses the single `N=500` stationary series, whereas Figure 6 high-T points and Table S8b use pooled two-seed `N=1000` estimates. The labels make this distinction explicit. The numerical difference is therefore intentional, not an inconsistency.

## 3. Closure of previous Red-Team Major issues

### RT-M01 — damping dependence

**Status: NOT SUFFICIENTLY CLOSED — MAJOR**

Current prose declares `m*=1, gamma*=4` in Methods/SI and states that no complete operating diagram is inferred outside the tested drive/damping range. This is necessary but not sufficient because the verified Red-Team sweep shows the canonical winding is strongly damping dependent:

- `gamma*=1 -> (1,-10)`
- `gamma*=2 -> (1,-3)`
- `gamma*=3 -> (2,-2)`
- `gamma*=4-6 -> (1,-1)`
- `gamma*=8-10 -> (0,0)`

The manuscript should explicitly state that the vector-locking map is a result of the declared reduced dynamical protocol, not a material-only MoSSe prediction.

**Resolution type:** writing-only, using existing verified evidence.

### RT-M02 — force/loading-direction dependence

**Status: NOT SUFFICIENTLY CLOSED — MAJOR**

Methods clearly define positive/negative-y loading, but headline prose still allows a reader to infer broad direction-independent rectification. The verified direction scan at `theta=1.5 deg` shows strong angular dependence:

- one symmetry-axis orientation: `|rho| ≈ 1.63e-4` (nearly zero),
- tested strong-rectification axis near 30 deg: `|rho| ≈ 0.4186`.

The manuscript should explicitly say that the reported threshold split is for the chosen crystallographic loading axis and is not rotationally invariant.

**Resolution type:** writing-only, using existing verified evidence.

### RT-M03 — preparation dependence

**Status: PARTIALLY CLOSED, BUT STILL MAJOR**

The manuscript consistently defines the headline result as ground-state prepared and continues the competing metastable family separately. SI Table S2 already contains the critical counterexample at `theta=1.5 deg`:

- ground branch: `Delta F_c = +1.81246`,
- competing metastable branch: `Delta F_c = -0.400639`.

Thus the same GSFE can carry opposite directional signs depending on the prepared zero-force basin. Main-text wording should make this explicit. “Intrinsic” must remain conditional on ground-state preparation, fixed twist, and the declared loading axis.

**Resolution type:** writing-only, using existing verified evidence.

### RT-M04 — boundary switch vs twist-sweep dynamics

**Status: NOT SUFFICIENTLY CLOSED — MAJOR**

Current text correctly defines the triangular reversal from a zero-force A/B ground-state energy crossing and states that the angle is edge-model dependent. But phrases such as “ground-state registry switch” and “can reverse the prepared bias” can still be read as a dynamical twist-sweep prediction.

No A-to-B barrier, kinetic switching path, twist-sweep protocol, or hysteresis was computed. The manuscript should state explicitly that this is **equilibrium re-preparation at fixed twist**, not a demonstrated twist-sweep switching event.

**Resolution type:** writing-only unless the authors want to make a kinetic switching claim; the latter would require upstream calculations.

### RT-M05 — fixed rotation and COM/body-force loading

**Status: NOT SUFFICIENTLY CLOSED — MAJOR**

Methods say that imposed twist remains an external coordinate and rigid rotation is projected out, and loading is represented by a longitudinal force tilt. The limitations section does not yet make the mechanical consequence explicit.

The current model does not include:

- rotational relaxation or applied torque,
- finite-stiffness spring pulling,
- edge pulling or center pulling,
- load-distribution-induced stress localization.

The manuscript should explicitly scope thresholds and trajectories to a fixed-twist, uniform COM/body-force protocol.

**Resolution type:** writing-only for scope limitation; alternative loading models would require upstream work.

### RT-M06 — elasticity independence

**Status: CLOSED — PASS**

This issue is now adequately limited.

Main Discussion P90 explicitly says the linear FEM and nonlinear bond-angle network are “two distinct internal representations that share the same GSFE and target elastic constants.” SI S11-S12 further states that neither constitutes full 3D atomistic validation and rejects the public empirical candidate as a quantitative replacement.

The remaining claim — that the directional split survives the **tested in-plane compliance representations** — is appropriately scoped.

## Closure decision

### Scientific blocker count

`0`

`RT-B01` is closed.

### Major wording/scope issues remaining

`5` — RT-M01 through RT-M05.

These do not require new simulation to close if the manuscript only narrows its claims to the evidence already obtained.

### Recommended gate decision

`DO NOT FREEZE FOR FIVE REVIEWER YET.`

Perform one **targeted scope-only revision** first:

1. delete the two residual legacy thermal-boundary history sentences from publication-facing text;
2. add explicit damping-protocol dependence;
3. add loading-axis dependence;
4. state the opposite-sign metastable preparation result;
5. distinguish equilibrium boundary re-preparation from kinetic twist-sweep switching;
6. state fixed twist + uniform COM/body-force loading explicitly.

Then rerun this short closure. If those six checks pass with no new contradiction, the manuscript is ready for the independent Five Reviewer Paper Audit.
