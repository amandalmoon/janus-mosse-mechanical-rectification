# N22 Architecture-Aligned Figure Contract Master Spec

## Authority

This figure set implements the frozen N21 scientific argument architecture:

1. credibility/setup;
2. prepared-state depinning phenomenon;
3. same-spectrum mechanism validation;
4. compact geometry + in-plane robustness;
5. boundary registry competition;
6. vector mode locking;
7. thermal hierarchy.

The prior N18R figure set remains historical source material but is superseded as the manuscript storyboard.

## Global design contract

- target role: ACS Nano main-text, double-column figures;
- final width: 177.8 mm for all main figures;
- minimum visible text: 7.0 pt;
- minimum visible line: 0.55 pt;
- quantitative evidence: SIMULATION_EXECUTED only;
- illustrative content is explicitly identified and cannot carry numerical claims;
- +y uses blue/circle/solid semantics where direction is compared;
- -y uses vermillion/square/dashed semantics where direction is compared;
- line/marker redundancy is used for compared series;
- categorical conditions are not connected with false continuous axes;
- integer winding maps use discrete integer colour scales;
- uncertainty is shown whenever it is part of the inferential claim;
- every figure has a machine-readable manifest and editable source;
- local benchmark rendering may use a fallback sans-serif font; literal Arial is verified only in the later venue-handoff preflight.

## Figure contracts

### FIG-01 — Credible inversion-asymmetric registry input
Question: Is the material/model starting point credible and genuinely inversion asymmetric?
Claims: M0, C1, C5.
Panels: illustrative finite-contact preparation; published 2H GSFE; translation-minimized asymmetry diagnostics.
Boundary: lateral registry asymmetry is not a physical polarity-reversal law.

### FIG-02 — Prepared-state unguided depinning
Question: Does the prepared family exhibit direction-split full-2D depinning?
Claims: C2, C3.
Panels: +y branches; -y branches; energy margin; stability margins and isolated higher-order point.
Boundary: prepared-state/loading-axis conditioned.

### FIG-03 — Same-spectrum mechanism isolation
Question: Do controlled symmetry interventions remove and reverse the response?
Claim: C4.
Panels: intervention definition; paired static thresholds; deterministic winding vectors; numerical symmetry residuals.
Boundary: mathematical mechanism controls only.

### FIG-04 — Compact geometry and in-plane compliance robustness
Question: Is the response an artifact of one rigid compact contact?
Claims: C6, C7, C20, C21.
Panels: compact scaled-twist collapse; residual size/shape deviations; normalized force-scale renormalization; normalized directional split across FEM/VFF.
Boundary: no arbitrary-edge or full 3D atomistic generalization.

### FIG-05 — Boundary-driven registry switching
Question: Can boundary geometry change the selected registry and reverse the sign?
Claims: C8, C9.
Panels: energy crossings; opposite family bias; discontinuous equilibrium prepared-state sign switch; edge-weight sensitivity.
Boundary: no barrier/hysteresis/twist-sweep claim.

### FIG-06 — Vector-locked relative-periodic states
Question: What states arise under zero-mean rocking and are representative transporting states attracting?
Claims: C13, C14.
Panels: discrete m map; discrete n map; sampled tau*=40 staircase; Floquet/closure cross-solver validation.
Boundary: sampled protocol-specific map, not a continuous phase diagram.

### FIG-07 — Thermal survival hierarchy
Question: What survives thermal noise after exact winding identity is mixed?
Claims: C15-C19.
Panels: mean-current components with trajectory-level intervals; joint zero-current rejection; cycle-sign bias versus exact target winding.
Boundary: no critical temperature or extrapolation beyond T*=0.70.

## Benchmark gate

The current publication-figure-designer deterministic source audit and package audit were run on all seven local manifests with --gate benchmark --check-files.

Result: **7/7 PACKAGE_RESULT: PASS**.

All seven 300 dpi final-physical-size PNG renders were opened and inspected after the final iteration. No clipping, overlap, broken legends, missing evidence, or ambiguous series semantics remained.

## Next handoff

The figure-design stage is complete at **BENCHMARK_PASS**. A Windows CI job performs the literal-Arial technical preflight and artifact export, but final ACS Nano venue acceptance remains deferred to the later acs-nano-submission stage in the user-defined workflow.
