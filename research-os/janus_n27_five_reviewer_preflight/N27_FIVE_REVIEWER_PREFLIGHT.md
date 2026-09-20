# N27 Five Reviewer Manuscript Preflight

**Audit date:** 2026-09-20  
**Mode:** manuscript-preflight  
**Manuscript branch:** `research-os/n27-five-reviewer-preflight`  
**Figure authority:** N25 exact head `4060d017a50c6387de45377621d9232529e7e4ad`  
**Review target:** assembled 19-page N27 manuscript with exact N25 Figures 1-7  
**Reviewer independence:** five first-pass lenses were derived independently from the manuscript/evidence packet before reconciliation.

## Gate status

**REVIEW COMPLETE — DOWNSTREAM SCIENTIFIC GATE NOT YET CLEARED.**

- BLOCKER: **0**
- MAJOR: **1 OPEN**
- MINOR: **1 OPEN**
- Accepted-with-boundary limitations: **3**
- Immediate literature/method/statistics findings repaired during preflight: **3**

The central reduced-model mechanism is not invalidated by this review. The open MAJOR is the gap between the internally validated GSFE-based finite-contact model and a material-level finite three-dimensional Janus MoSSe contact.

---

## 1. Source and context check

The audited manuscript contains the complete Abstract, Introduction, Methods, Results, Discussion, Conclusions, Data and Code Availability, 30 references, and Figures 1-7. The N25 figure source and final rendered artifact are traceable to exact head `4060d017a50c6387de45377621d9232529e7e4ad`.

The central computational evidence packet includes:

- published three-shell 2H MoSSe GSFE input and provenance checks;
- dense prepared-state branch continuation and stationary-point checks;
- translation-minimized inversion diagnostics;
- same-spectrum symmetrization and exact inversion;
- compact size/shape scaling;
- boundary-registry and edge-weight sensitivity;
- linear FEM and independently reconstructed nonlinear VFF in-plane relaxation;
- 91-point cycle-resolved deterministic winding map;
- representative relative-periodic shooting/Floquet tests;
- timestep, continuation, damping-drive, and basin robustness;
- stationary thermal trajectories with burn-in, block-stationarity, initialization-memory, independent-seed, bootstrap/Hotelling, sample-count, and timestep audits.

The manuscript itself explicitly excludes claims of a physical Janus-polarity reversal law, a universal edge-switch angle, a material-only dynamical phase diagram, a thermal critical temperature, or full three-dimensional atomistic validation.

---

## 2. Internal claim inventory

| Claim ID | Central claim | Type | Primary anchors |
|---|---|---|---|
| C1 | The published 2H MoSSe lateral GSFE contains non-removable registry inversion asymmetry. | Computational / mathematical | Methods 2.3; Results 3.1; Fig. 1 |
| C2 | The lowest-energy prepared zero-force family has strongly direction-split unguided depinning thresholds. | Computational | Methods 2.4; Results 3.2; Fig. 2 |
| C3 | Same-spectrum symmetrization removes the symmetry-respecting directional response and exact inversion swaps the static/dynamic response, identifying inversion-odd registry content as the directional source within the model. | Mechanistic / computational | Methods 2.3; Results 3.3; Fig. 3 |
| C4 | Compact contacts show theta*sqrt(N) similarity and the directional sign survives two tested in-plane relaxation representations. | Computational / robustness | Methods 2.5-2.6; Results 3.4; Fig. 4 |
| C5 | Rotated finite boundaries can change equilibrium registry-family selection and reverse the prepared response; the exact switch angle is edge-model sensitive. | Computational / mechanistic | Methods 2.5; Results 3.5; Fig. 5 |
| C6 | Under the declared reduced deterministic protocol, sampled zero-mean forcing produces integer lattice-vector locking and representative attracting relative-periodic states. | Computational / nonlinear dynamics | Methods 2.7; Results 3.6; Fig. 6 |
| C7 | Under the stationary stochastic protocol, exact target-winding identity is strongly mixed before the weaker mean directed current becomes statistically unresolved; the mean current remains nonzero through sampled T*=0.70. | Computational / statistical | Methods 2.8; Results 3.7; Fig. 7 |

---

## 3. Reviewer 1 — Domain Expert

### First-pass assessment

[Verified in source] The strongest scientific feature is that the manuscript does not infer directionality from the Janus label alone. It starts from a published MoSSe GSFE, measures its inversion content in translation-independent ways, and then intervenes on the same Fourier spectrum. This makes C3 substantially stronger than a comparison between unrelated materials or stackings.

[Verified in source] The prepared-state qualification is essential rather than cosmetic. At the reference twist the competing metastable family has the opposite signed threshold response, and rotated triangular boundaries can change which family is selected. The manuscript correctly avoids calling the effect an unconditional scalar material property.

[Inference] Within the reduced model, the mechanism chain
`registry inversion content -> prepared directional stability -> driven vector transport`
is physically coherent and internally discriminated.

### Domain-specific weakness

**The material-level validation hierarchy stops too early.** The finite contact is not a fully relaxed three-dimensional Janus MoSSe interface. The model does not include collective out-of-plane corrugation/buckling, reconstructed or chemically specific edges, defects, or load-dependent interlayer energetics. Two in-plane models help rule out a purely rigid-contact artifact, but they do not close this material-validity gap.

### What would change the judgment

A Janus-specific full-3D spot check at a small number of canonical conditions, using a validated atomistic/MLIP/first-principles representation and full relaxation, that preserves the prepared directional sign would materially strengthen the material-specific interpretation.

**Reviewer 1 weakness severity after reconciliation: MAJOR (N27-R01).**

---

## 4. Reviewer 2 — Method Reviewer

### First-pass assessment

[Verified in source] The study design is unusually explicit about direct versus proxy evidence.

- C2 is defined by branch following of the same prepared minimum rather than by choosing the last surviving basin.
- C3 uses matched same-spectrum interventions rather than a chemically different comparator.
- C6 separates finite-run winding assignment from representative Floquet certification.
- C7 uses trajectories, not cycles, as inferential units.

[Verified in source] During this preflight, Methods 2.7 was corrected to state the actual production algorithm: fixed-step classical fourth-order Runge-Kutta, 20 transient + 40 measured cycles, 4000 steps/cycle. The winding assignment is now described exactly as implemented: nearest-integer componentwise rounding in lattice coordinates with the real-space residual retained as a diagnostic rather than a tuned cutoff.

### Methodological weakness

The principal unresolved method question is again the **model regime**, not the numerical implementation. The additive local-GSFE finite-contact model plus in-plane relaxation is not independently benchmarked against a fully relaxed finite MoSSe contact in the same operating regime.

### Secondary bounded weakness

C5 is an equilibrium preparation-selection result. It does not compute an activation path, switching barrier, kinetic rate, or twist-sweep hysteresis. The manuscript already states this clearly, so the issue is accepted with boundary rather than treated as a defect in the stated equilibrium claim.

**Reviewer 2 weakness routing:** N27-R01 MAJOR; N27-R03 accepted with boundary.

---

## 5. Reviewer 3 — Statistics and Reproducibility

### First-pass assessment

[Verified in source] The stochastic section uses the correct independent unit: one trajectory summary. The high-temperature band has two independent N=500 seed ensembles pooled to N=1000, with 60 burn cycles and 100 measured cycles.

[Verified in source] Stationarity is supported by three different checks:

1. late 20-cycle block comparisons show no detected two-component drift at T*=0.50-0.70 in either seed ensemble;
2. orbit/ground/metastable initial-condition trajectories under common noise lose initialization memory before the measurement window;
3. dt=0.04, 0.02, and 0.01 estimates differ by at most about 1.12 combined standard errors in either current component at the audited high temperatures.

[Verified in source] The pooled zero-current test at T*=0.70 is far from its null boundary. The 50,000-resample bootstrap gives the reported marginal intervals, while the joint statistic is approximately 38.07.

### Multiplicity challenge and resolution

A reviewer could object that five high-temperature zero-current tests were presented without family-wise correction. This was checked during N27.

Using a Bonferroni correction over the five temperatures gives per-test alpha=0.01 and an exact finite-sample Hotelling T^2 threshold of approximately **9.26**. The smallest pooled statistic is approximately **38.05** at T*=0.70. Therefore every high-temperature zero-current rejection survives the conservative family-wise correction.

This robustness statement has now been added to Methods 2.8 and Results 3.7.

### Remaining statistical weakness

The data establish the observable hierarchy but do not decompose the residual high-temperature mean current into sign imbalance, unequal conditional displacement magnitudes, tail asymmetry, or their combination. Because the manuscript does **not** claim such a microscopic decomposition, this is a bounded follow-up issue rather than a threat to C7.

**Reviewer 3 weakness routing:** N27-R04 accepted with boundary.

---

## 6. Reviewer 4 — Skeptic

### Alternative interpretation 1: “intrinsic friction diode” is really a preparation effect

[Verified in source] A competing metastable family carries the opposite signed directional response. Therefore one cannot reinterpret the result as a preparation-independent scalar friction diode property of MoSSe.

The manuscript survives this objection because its title, Results, and Discussion consistently say **prepared-state**, not state independent.

### Alternative interpretation 2: finite-contact geometry or edge physics could reverse the result

[Verified in source] This alternative is partly true: rotated triangular boundaries can switch the equilibrium registry family and reverse the prepared sign. The manuscript turns this into an explicit result rather than hiding it.

The remaining skeptical concern is whether realistic three-dimensional relaxation or atomistic edge reconstruction would qualitatively change the finite-contact state ordering. That is not tested.

### Alternative interpretation 3: the vector map is a finite-time rounding artifact

[Verified in source] The cycle-resolved replay, sub-1e-9 single-cycle lattice residual, representative relative-periodic shooting, independent DOP853/Radau Floquet calculations, timestep refinement, continuation, and basin perturbations make this alternative unlikely within the declared deterministic model.

### Alternative interpretation 4: the high-T current is a pseudoreplication artifact

[Verified in source] It is not based on cycle-level pseudoreplication; trajectory summaries are the inferential unit. Independent seeds, stationarity checks, sample-count convergence, timestep compatibility, and family-wise multiplicity robustness all support the finite-range C7 statement.

### Decisive falsification test

The most discriminating remaining test is a **three-dimensional material-level finite-contact validation**. If a fully relaxed Janus-specific atomistic representation at the reference state removes or reverses the prepared +y/-y directional sign, the material-specific extrapolation of C2-C7 would be weakened even though the mathematical reduced-model results remain correct.

**Reviewer 4 weakness severity: MAJOR N27-R01.**

---

## 7. Reviewer 5 — Research Connector

### Prior-art positioning

The generic ingredients are not individually novel:

- directional friction/friction-diode effects in 2D interfaces;
- asymmetric potential-energy surfaces as a source of directional response;
- finite-contact edge/shape/twist scaling;
- generic two-dimensional ratchet/phase-locking;
- mechanically controlled stacking-state switching.

During this preflight a closer dynamical prior-art item was added as Ref. 30: finite graphene flakes can show directed off-axis motion through moire-superstructure dynamics under imposed shear. The manuscript now distinguishes that shear-driven atomistic phenomenon from its zero-mean sinusoidal, integer relative-periodic transport result.

### Connection-level conclusion

[Inference] The defensible contribution is therefore **combination-level and mechanism-specific**, not priority over generic friction diodes or mode locking:

published MoSSe lateral GSFE + prepared full-2D depinning + same-spectrum symmetry falsification + compact/boundary tests + zero-mean lattice-vector dynamics + stationary thermal hierarchy.

No direct match to that full combination was found in the updated search, but search failure is not proof of uniqueness and no “first” language is authorized.

### Weakness

The strongest external bridge is still computational rather than experimental. A full material-level validation or experimentally calibrated protocol would improve the connection from nonlinear-dynamics mechanism to nanoscale tribological device physics.

**Reviewer 5 weakness routing:** N27-R01 and N27-R05.

---

## 8. Changes made during the Five Reviewer preflight

Three concerns were resolved directly rather than left as review defects.

### FR-P01 — closest dynamic prior art
**Resolved.** Ref. 30 and explicit positioning were added for moire-driven directed finite-flake motion under shear.

### FR-P02 — deterministic production method reporting
**Resolved.** Methods 2.7 now states classical fixed-step RK4, 4000 steps/cycle, and the actual nearest-integer winding assignment plus residual diagnostic.

### FR-P03 — high-temperature multiple testing
**Resolved.** Bonferroni family-wise robustness was calculated and added. The conservative corrected threshold is 9.26; the weakest pooled T^2 is 38.05.

---

## 9. Contradiction map

| ID | Question | Lens A | Lens B | Conflict type | Source resolution | Resolution |
|---|---|---|---|---|---|---|
| CM-01 | Does C3 establish a physical Janus-polarity law? | Domain: strong same-spectrum mechanism discrimination | Skeptic: mathematical inversion need not equal physical polarity reversal | scope / mechanism | **Yes** | Manuscript explicitly restricts inversion to a mathematical symmetry control. |
| CM-02 | Is the 91-point map evidence of stable attractors everywhere? | Method: cycle-resolved integer locking is strong | Skeptic: rounding alone does not prove attractor stability | methodology | **Partial** | All 91 are finite-run cycle-locked; only representative plateaus are Floquet certified. Caption/Results state this explicitly. |
| CM-03 | Does boundary switching imply kinetic switching? | Domain: equilibrium registry competition is meaningful | Skeptic: no activation path or hysteresis is calculated | scope | **Yes for stated claim** | C5 is explicitly equilibrium/preparation-conditioned; kinetic switching remains outside scope. |
| CM-04 | Is the material-specific MoSSe framing fully validated? | Statistics/Method: numerical evidence is strong inside model | Domain/Skeptic: missing 3D finite-contact atomistic validation may alter material behavior | model validity | **No** | Open MAJOR N27-R01. |

---

## 10. Claim reliability

| Claim | Type | Reliability | Status | Reason |
|---|---|---|---|---|
| C1 GSFE inversion asymmetry | computational / mathematical | **High within source model** | Confirmed | two coordinate-independent diagnostics + implementation/provenance checks |
| C2 prepared directional depinning | computational | **High within reduced model** | Confirmed | dense branch following, competing-family checks, stationary-point audits |
| C3 same-spectrum mechanism | mechanistic / computational | **High within reduced model** | Confirmed | matched intervention removes global response; exact inversion swaps static/dynamic response |
| C4 compact scaling + in-plane robustness | computational | **High within tested model classes** | Confirmed with scope | exact/dense scaling tests + independent geometry family + FEM/VFF agreement |
| C5 boundary registry switching | mechanistic / computational | **Medium** | Confirmed with boundary | equilibrium crossing is robust to tested edge weights, but edge model is surrogate and kinetics are absent |
| C6 deterministic vector locking | computational nonlinear dynamics | **High within declared protocol** | Confirmed | 91-point cycle replay + representative cross-solver Floquet + timestep/continuation/basin checks |
| C7 stationary thermal hierarchy | computational / statistical | **High within sampled protocol** | Confirmed | stationary trajectory-level design, independent seeds, bootstrap/Hotelling, sample-count, timestep, multiplicity robustness |
| Material-level integrated prediction | computational / positioning | **Medium** | Demoted pending N27-R01 | reduced model is strong; 3D finite-contact Janus-specific validation is absent |

---

## 11. Missing sixth lens — Experimental translatability and dimensional calibration

The five standard reviewers underweight one question:

**Can an experimentalist construct and drive the modeled state in a quantitatively corresponding physical regime?**

This lens changes interpretation of the dynamical/thermal figures because (m^*, gamma^*, F_0^*, 	au^*, T^*) are reduced protocol parameters, not calibrated physical quantities.

Evidence needed:

- defensible physical mass/damping/force/time/temperature mapping;
- a preparation protocol that targets the stated registry family;
- experimental observables corresponding to the modeled center-of-mass registry and lattice-current components;
- validation that the finite contact remains in the assumed structural regime.

This does not invalidate C1-C7 as reduced-model results, but it controls whether they can be presented as device-scale predictions.

---

## 12. Research gaps

### Explicit gaps already acknowledged by the manuscript

1. **Physical polarity mapping:** exact registry inversion is not shown to equal experimental Janus-polarity reversal. [Discussion 4.4]
2. **Three-dimensional material validation:** collective out-of-plane corrugation, atomistic edges, defects, and load-dependent energetics are absent. [Methods 2.10; Discussion 4.4]
3. **Physical calibration:** reduced time, temperature, mass, damping, and force are not mapped to hertz, kelvin, or device-scale parameters. [Methods 2.10; Discussion 4.4]

### Hidden gaps inferred by the reviewers

4. [Inference] **Preparation kinetics:** equilibrium family selection does not establish a reachable switching path, barrier, rate, or hysteresis.
5. [Inference] **High-T current composition:** the residual stationary mean is statistically resolved, but the displacement-distribution feature carrying that mean is not decomposed.

---

## 13. Structured Research OS issues

Canonical machine-readable issue file: `review_issues.json`.

- **N27-R01 — MAJOR / OPEN:** material-model external validity.
- **N27-R02 — MINOR / OPEN:** immutable reproducibility archive identifier.
- **N27-R03 — MINOR / ACCEPTED_WITH_BOUNDARY:** preparation/switching kinetics.
- **N27-R04 — MINOR / ACCEPTED_WITH_BOUNDARY:** thermal distributional mechanism.
- **N27-R05 — MINOR / ACCEPTED_WITH_BOUNDARY:** dimensional/experimental calibration.

No BLOCKER was identified.

---

## 14. Exactly three next actions

1. **Run the N27-R01 material-validity discriminator.**  
   **Input:** canonical 2H MoSSe registry contract, reference prepared state at theta=1.5 degrees, and a validated Janus-specific 3D atomistic/MLIP/first-principles representation.  
   **Task:** fully relax 2-3 deliberately selected finite-contact cases and compare the +y/-y prepared-state sign and relative threshold scale against the reduced model.  
   **Decision criterion:** if the directional sign survives, close or demote N27-R01; if it reverses/disappears, revise the material-level claim architecture.

2. **Build an experimental-translatability contract without changing current claims.**  
   **Input:** independent physical mass, damping, energy/force, and time-scale information plus a plausible preparation protocol.  
   **Task:** map or explicitly bracket (m^*,gamma^*,F_0^*,	au^*,T^*) and identify directly measurable observables.  
   **Decision criterion:** either obtain a defensible physical mapping or preserve the reduced-unit boundary in the final paper and SI.

3. **Freeze the corrected N27 package and rerun downstream gates only after N27-R01 disposition.**  
   **Input:** N27 manuscript, exact N25 figures, validated review-issue file, and eventual immutable repository release.  
   **Task:** rebuild the final DOCX, rerun Five Reviewer on the scientific change, then run ACS Nano submission/compliance audit.  
   **Decision criterion:** 0 BLOCKER, 0 unresolved MAJOR affecting the retained headline claims, exact claim/figure/citation synchronization, and immutable reproducibility identifier present before submission.

---

## Final preflight conclusion

The manuscript is scientifically much stronger than a raw reduced-model simulation paper because it actively falsifies coordinate, preparation, symmetry, geometry, numerical, stochastic, and inferential alternatives. The Five Reviewer audit does **not** identify an internal contradiction that overturns the prepared-state rectification, sampled vector-locking, or stationary thermal-current conclusions within the declared model.

The unresolved question is the next model level: whether the same material-specific conclusions survive a genuinely three-dimensional finite Janus MoSSe representation. Until that is tested—or the framing is narrowed to a GSFE-anchored finite-contact model prediction—N27-R01 remains the single MAJOR scientific issue and the downstream scientific submission gate remains uncleared.
