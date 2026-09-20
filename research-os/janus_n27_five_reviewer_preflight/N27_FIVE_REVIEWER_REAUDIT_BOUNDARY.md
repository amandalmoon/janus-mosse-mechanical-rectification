# N27 Five Reviewer Re-Audit After GSFE-Scope Boundary

**Audit date:** 2026-09-20  
**Mode:** re-audit / manuscript-preflight  
**Current manuscript branch:** research-os/n27-five-reviewer-preflight  
**Figure authority:** N25 exact head 4060d017a50c6387de45377621d9232529e7e4ad  
**Prior audit:** N27_FIVE_REVIEWER_PREFLIGHT.md  
**Boundary decision:** DEC-N27-R01-BOUNDARY

## Re-audit verdict

**GATE-REVIEW: PASS**

- BLOCKER: **0**
- unresolved MAJOR: **0**
- OPEN MINOR: **1** — archival repository identifier only
- ACCEPTED_WITH_BOUNDARY MINOR limitations: **4**
- scientific results removed: **0**
- Figures removed: **0**

The previous MAJOR N27-R01 is no longer a MAJOR defect because the manuscript no longer presents the finite-contact calculation as a fully three-dimensional material prediction. The retained headline is now explicitly a **published-GSFE-anchored finite-contact model claim** in the title, abstract, introduction, Discussion 4.4, and Conclusions.

This is a scope correction, not evidence that full 3D relaxation has been performed.

---

## 1. Source and context check

[Verified in source] The revised title is:

**GSFE-Anchored Prepared-State Mechanical Rectification and Vector Mode Locking in Finite Janus MoSSe Contacts**

[Verified in source] The Abstract now states that the result is a state-, axis-, and protocol-conditioned prediction of a GSFE-anchored finite-contact model and explicitly excludes collective out-of-plane reconstruction, atomistically reconstructed edges, and dimensional calibration from the claimed scope.

[Verified in source] Introduction, Discussion 4.4, and Conclusions repeat the same boundary. In particular, the final claim is explicitly restricted to a published-GSFE-anchored finite-contact hierarchy and does not extend to arbitrary fully three-dimensional contacts.

No numerical evidence, figure data, thermal protocol, deterministic map, or reference value was changed by this scope repair.

---

## 2. Central claim inventory after revision

| Claim | Retained wording after boundary repair | Type |
|---|---|---|
| C1 | The published 2H MoSSe GSFE contains non-removable registry inversion asymmetry. | computational / mathematical |
| C2 | Within the GSFE-anchored finite-contact model, the lowest-energy prepared family has direction-split unguided depinning. | computational |
| C3 | Same-spectrum symmetrization and exact inversion discriminate inversion-odd registry content as the directional source **within the model**. | mechanistic / computational |
| C4 | Compact-contact similarity and directional-sign preservation hold across the tested rigid/FEM/VFF hierarchy. | computational / robustness |
| C5 | Tested triangular boundaries can change equilibrium prepared registry family and reverse the model response; exact switch angles are edge-model sensitive. | computational / mechanistic |
| C6 | Under the declared reduced deterministic protocol, sampled zero-mean forcing gives cycle-resolved integer winding and representative Floquet-attracting relative-periodic states. | computational nonlinear dynamics |
| C7 | Under the declared stationary stochastic protocol, exact winding identity is strongly mixed while the mean current remains statistically nonzero through sampled T*=0.70. | computational / statistical |

There is no retained headline claim that arbitrary 3D experimental MoSSe contacts must reproduce C2-C7.

---

# Reviewer 1 — Domain Expert

## Independent assessment

[Verified in source] The manuscript now clearly distinguishes **material anchoring** from **material-level complete prediction**. The material-specific ingredient is the published MoSSe lateral GSFE and its symmetry content; the finite-contact dynamics and mechanics are explicitly model predictions built on that surface.

[Verified in source] The core physical mechanism remains coherent: translation-independent registry asymmetry, prepared-state branch selection, symmetry intervention, compact-contact interference, and driven lattice transport form a consistent chain inside the stated model.

[Inference] The previous request for full 3D atomistics arose because the earlier wording could be read as a stronger finite-material prediction. Once the headline is explicitly narrowed, lack of collective out-of-plane reconstruction no longer invalidates the claim actually being made.

### Strongest remaining weakness

The model cannot determine whether a real finite MoSSe flake with collective corrugation, reconstructed edges, defects, and a particular substrate/loading geometry will preserve the same directional sign.

**Severity:** MINOR / ACCEPTED_WITH_BOUNDARY (N27-R01).

**What would change the judgment:** re-expanding the title/abstract/conclusion to claim arbitrary material-level finite-contact behavior would immediately reopen this as MAJOR.

---

# Reviewer 2 — Method Reviewer

## Independent assessment

[Verified in source] The numerical design identifies the quantities it actually claims:

- prepared branch is fixed before +y/-y loading;
- competing metastable families are tracked rather than silently substituted;
- same-spectrum symmetry controls target the proposed mechanism;
- 91-point finite-run cycle locking is distinguished from representative Floquet certification;
- the deterministic production method now states fixed-step RK4, 4000 steps/cycle, and nearest-integer winding assignment;
- thermal inference uses trajectories as independent units.

These methods are adequate for the revised reduced-model claim.

### Strongest remaining weakness

The registry-family reversal in Figure 5 is an **equilibrium selection** result, not a kinetic switching law. No barrier, path, rate, or hysteresis is calculated.

The manuscript explicitly says so; therefore this is not a defect in the stated equilibrium claim.

**Severity:** MINOR / ACCEPTED_WITH_BOUNDARY (N27-R03).

---

# Reviewer 3 — Statistics & Reproducibility

## Independent assessment

[Verified in source] The stochastic evidence remains strong:

- 60 burn + 100 measured cycles;
- N=500 trajectories per temperature;
- independent second N=500 ensemble at T*=0.50–0.70;
- pooled high-T N=1000;
- trajectory-level bootstrap/Hotelling inference;
- block-stationarity and initialization-memory checks;
- timestep compatibility;
- trajectory-count decision-stability audit.

[Verified in source] The five high-temperature joint tests also survive Bonferroni family-wise correction: the corrected Hotelling threshold is approximately 9.26, while the weakest pooled statistic is approximately 38.05 at T*=0.70.

### Strongest remaining weakness

The paper does not decompose the residual high-temperature mean current into sign-probability imbalance, unequal conditional jump magnitudes, tail asymmetry, or combinations thereof.

Because no microscopic decomposition is claimed, this remains a follow-up mechanism question, not a statistical failure of C7.

**Severity:** MINOR / ACCEPTED_WITH_BOUNDARY (N27-R04).

### Reproducibility note

The code/data package is described and versioned in the repository, but an immutable archive DOI is still absent.

**Severity:** MINOR / OPEN (N27-R02), submission-layer owner.

---

# Reviewer 4 — Skeptic

## Independent assessment

### Alternative 1 — “This is only a chosen-state artifact.”

[Verified in source] Preparation dependence is real: another zero-force family can carry the opposite directional split. The paper now treats this as part of the physics and consistently uses **prepared-state** language.

This alternative therefore narrows interpretation but does not contradict C2.

### Alternative 2 — “Unmodeled 3D reconstruction could change the material response.”

[Verified in source] Yes; the paper now says exactly that and no longer claims otherwise.

For the revised claim—behavior of the published-GSFE-anchored finite-contact model—this is an external-validity boundary rather than a falsifier of the calculation.

### Alternative 3 — “91-state locking is just rounding.”

[Verified in source] Cycle-resolved replay, sub-1e-9 residual scale, representative shooting/Floquet calculations, cross-solver checks, timestep refinement, continuation, and local basin perturbations make this explanation insufficient for the declared protocol.

### Alternative 4 — “The high-temperature result is pseudoreplication.”

[Verified in source] Trajectories, not cycles, are the inference units; this objection is not supported.

### Strongest remaining weakness

Experimental preparation and dimensional calibration are not yet supplied, so the reduced parameters cannot be interpreted as a ready device recipe.

**Severity:** MINOR / ACCEPTED_WITH_BOUNDARY (N27-R05).

---

# Reviewer 5 — Research Connector

## Independent assessment

[Verified in source] The manuscript now positions generic ingredients conservatively:

- directional friction is not claimed as new;
- Janus structural asymmetry as a sliding-friction control variable is not claimed as new;
- generic 2D ratchet/mode locking is not claimed as new;
- registry-state switching in layered materials is not claimed as new;
- finite-flake directed motion prior art is cited.

[Inference] The defensible research contribution remains the **integrated model chain**:

published MoSSe GSFE  
→ prepared full-2D depinning  
→ same-spectrum symmetry discrimination  
→ compact/boundary tests  
→ zero-mean vector transport  
→ stationary thermal hierarchy.

### Strongest remaining weakness

The link to an experimentally executable SPM/tribology protocol is still prospective rather than demonstrated.

That limits translational reach but does not weaken the revised model-level scientific claim.

**Severity:** MINOR / ACCEPTED_WITH_BOUNDARY (N27-R05).

---

# Contradiction map

| ID | Question | Reviewer positions | Source resolution | Final disposition |
|---|---|---|---|---|
| CM-R1 | Does absence of 3D atomistics invalidate the headline? | Domain/Skeptic: would matter for a material-complete claim; Method: current evidence is sufficient for a reduced-model claim | **Yes after revision** | headline narrowed; N27-R01 accepted with boundary |
| CM-R2 | Does Figure 5 establish kinetic switching? | Domain: equilibrium state change is meaningful; Method/Skeptic: no kinetic path | **Yes** | equilibrium-only wording retained; MINOR boundary |
| CM-R3 | Are all 91 deterministic states Floquet certified? | Method: all are cycle-resolved locked; Skeptic: Floquet only representative | **Yes** | wording/caption distinguish the two evidence levels |
| CM-R4 | Is T*=0.70 current statistically resolved? | Statistics: yes; Skeptic: dependence/multiplicity could threaten | **Yes** | trajectory-level inference + independent seeds + Bonferroni robustness preserve result |

No unresolved contradiction reaches MAJOR severity for the retained claims.

---

# Claim reliability after boundary repair

| Claim | Reliability | Re-audit status |
|---|---|---|
| C1 GSFE inversion asymmetry | **High within source GSFE** | CONFIRMED |
| C2 prepared directional depinning | **High within finite-contact model** | CONFIRMED |
| C3 same-spectrum mechanism discrimination | **High within finite-contact model** | CONFIRMED |
| C4 compact scaling + in-plane model robustness | **High within tested model classes** | CONFIRMED WITH SCOPE |
| C5 boundary registry-family selection | **Medium** | CONFIRMED WITH BOUNDARY |
| C6 deterministic vector locking | **High within declared protocol** | CONFIRMED |
| C7 stationary thermal hierarchy | **High within sampled protocol** | CONFIRMED |
| arbitrary fully 3D material prediction | **Not claimed** | OUTSIDE SCOPE |

---

# Missing sixth lens — experimental observability

The underweighted question remains:

> Which laboratory observable most directly corresponds to the model’s prepared branch and opposite-direction depinning threshold?

This does not alter the present claim but should guide the next project. A scanning-probe/lateral-force or force-spectroscopy protocol with controlled preparation, loading direction, and twist would be the natural experimental bridge. Quantitative use requires force/time/damping calibration.

---

# Research gaps

## Explicitly acknowledged

1. Physical polarity reversal is not identified with mathematical GSFE inversion.
2. Collective 3D corrugation/reconstructed edges/defects are outside the model.
3. Reduced dynamical and thermal parameters are not dimensionally calibrated.

## Reviewer-inferred

4. [Inference] Equilibrium registry-family crossing does not establish preparation kinetics.
5. [Inference] The distributional origin of the residual high-T current remains unresolved.

All five are either outside the retained claim or already encoded as explicit boundaries.

---

# Structured issue summary

- N27-R01 — **MINOR / ACCEPTED_WITH_BOUNDARY** — 3D material external validity.
- N27-R02 — **MINOR / OPEN** — immutable archive DOI/release identifier.
- N27-R03 — **MINOR / ACCEPTED_WITH_BOUNDARY** — preparation/switching kinetics.
- N27-R04 — **MINOR / ACCEPTED_WITH_BOUNDARY** — high-T current decomposition.
- N27-R05 — **MINOR / ACCEPTED_WITH_BOUNDARY** — dimensional/experimental calibration.

**BLOCKER = 0**  
**unresolved MAJOR = 0**

---

# Exactly three next actions

1. **Freeze the boundary-corrected scientific manuscript.**  
   Input: revised N27 manuscript + N25 figures + accepted limitation decision.  
   Output criterion: title/abstract/results/discussion/conclusion remain synchronized to the GSFE-anchored scope.

2. **Create the immutable reproducibility release.**  
   Input: exact source/data/config/manuscript release.  
   Output criterion: archival DOI or equivalent immutable identifier closes N27-R02.

3. **Run the ACS Nano venue/compliance layer.**  
   Input: scientifically frozen N27 package.  
   Output criterion: venue formatting, SI, data/code statement, TOC graphic, reference and rendered-document gates pass without upgrading scientific claims.

---

# Final re-audit conclusion

The previous MAJOR was not resolved by pretending that 3D atomistics had been performed. It was resolved by aligning the claim with the evidence actually available.

The manuscript now claims a **GSFE-anchored finite-contact mechanism** and explicitly excludes arbitrary fully three-dimensional material behavior. Under that corrected scope, the missing 3D layer is a future validation direction rather than missing evidence for the headline computational claim.

**Five Reviewer re-audit result: PASS — 0 BLOCKER, 0 unresolved MAJOR.**
