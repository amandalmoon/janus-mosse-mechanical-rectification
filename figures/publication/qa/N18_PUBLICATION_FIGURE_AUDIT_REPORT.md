# N18 Publication Figure Audit Report

## Status

**Publication Figure Designer gate: VENUE_HANDOFF_READY**  
**ACS Nano figure venue gate: CONDITIONAL_READY**

The full main-text Figure 1-6 set was rebuilt and audited as a single evidence system after the scientific layer passed. Scientific claims, numerical evidence, and captions were preserved; the redesign targets cross-figure consistency, panel hierarchy, accessibility, final-size legibility, and provenance.

## Figure contracts and claim mapping

- FIG-01 -> M0, C1, C4: registry inversion asymmetry and matched symmetry contracts.
- FIG-02 -> C2, C5: prepared-branch full-2D directional depinning.
- FIG-03 -> C6, C7: compact-contact Theta=sqrt(N) similarity and shape robustness.
- FIG-04 -> C8, C9: boundary-driven equilibrium registry competition and edge-model sensitivity.
- FIG-05 -> C13, C14: sampled vector locking and representative Floquet attraction.
- FIG-06 -> C15-C18: stationary thermal drift versus loss of exact winding identity.

All six manifests classify provenance as `SIMULATION_EXECUTED` and passed deterministic metadata audit.

## Main revisions

### Figure 1
- Shared normalization and one shared colorbar for asymmetric and matched-symmetrized GSFE surfaces.
- Corrected energy colorbar notation to `U/E0`.
- Rebalanced panel labels and threshold-control encoding.

### Figure 2
- Matched y-axis range for +y and -y threshold panels.
- Stable blue/orange/gray semantics across prepared/competing families.
- Panel D wording explicitly scoped to the prepared ground branch.

### Figure 3
- Stable direction encoding (+y solid blue, -y dashed orange) with marker redundancy for shape family.
- Aligned finite-size/family-difference presentation around the sub-0.1% scale.

### Figure 4
- Equilibrium character of registry switching made visually explicit.
- Family A/B identity uses line style/marker while boundary orientation uses color/marker, preventing ambiguous legend decoding.

### Figure 5
- Integer mode maps changed to discrete, accessible ordered color maps with integer colorbars.
- Replaced dual-y-axis Floquet panel with stacked mini-axes for solver-relative deviation and relative-periodic closure.
- Leading Floquet scale shown as attraction evidence only, not a ranking metric.

### Figure 6
- Standardized typography and series semantics with the full figure set.
- Clearly separates (a) stationary component currents, (b) joint zero-current inference, and (c) cycle-level sign/target-winding probabilities.
- No visual element implies a thermal critical temperature.

## Integrity and final-size QA

- No values were invented or interpolated to complete panels.
- Source paths are recorded per panel in FIG-01 through FIG-06 manifests.
- Uncertainty is shown only where an audited trajectory-level interval exists and is defined in the caption/manifest.
- Current TIFF derivatives are RGB, 600 dpi.
- Canonical SVG, EPS, TIFF, PNG, and plotting source are retained.
- Canonical PNG hashes match the six media payloads embedded in the final figure-gated manuscript.
- All 15 manuscript pages were visually inspected after figure insertion. A final consistency check found one pre-existing Table 3 phrase that had broadened the Five Reviewer scope (`two independent in-plane models`); it was narrowed without new science to `two distinct in-plane representations with shared GSFE/elastic targets`. Only page 12 changed after this repair; all other rendered pages are byte-identical to the already-inspected v6 render.

## Remaining condition

Literal Arial is absent from the current runtime, so the venue gate cannot be upgraded to PUBLICATION_READY. SVG masters explicitly declare Arial, but the current local EPS/TIFF/PNG derivatives use Arimo fallback. Final upload artwork should be opened/re-exported on an Arial-equipped workstation and visually rechecked at final size.

## Next Research OS handoff

The scientific figure set is ready for the ACS Nano venue/submission layer. The next venue tasks are TOC graphic, final SI/reference/declaration checks, submission-package assembly, final PDF render, visual QA, and ACS Nano Submission Audit.
