# Five-Reviewer Audit Resolution Report

## Manuscript
**Unguided Full-2D Mechanical Rectification and Vector Mode Locking in Finite Janus MoSSe Contacts**

This report records the calculations performed after the Five Reviewer Paper Audit, the result of each falsification/robustness test, the corresponding manuscript change, and the small set of questions that cannot be answered from the present rigid published-GSFE input alone.

## Resolution status at a glance

| Audit issue | Resolution calculation | Outcome | Manuscript status |
|---|---|---|---|
| Global last-surviving minimum might not equal a physically prepared depinning branch | Enumerate all zero-force minima; follow each branch under +/- force; compare zero-force energy and branch fold | **Resolved.** For the compact N=127 hexagon, the lowest-energy branch is also the longest-lived branch for both signs at every sampled twist 0-3 deg. At 1.5 deg: F_c,+*=3.0711353385, F_c,-*=1.2586722985. | Headline thresholds redefined as **prepared ground-state branch-followed** thresholds; global envelope retained only as a diagnostic. |
| 3R symmetry controls were not matched to the same 2H spectrum | Construct same-2H inversion-centered symmetrized surface and exact spatial inversion | **Resolved.** Symmetrized global split = 6.57e-10; deterministic symmetric current norm = 8.51e-18. Exact inversion swaps thresholds to <2e-15 and reverses current to <2e-14. | Same-2H matched controls replace 3R-only causal attribution. |
| Coordinate-invariant asymmetry minimizer might be local | 181x181 translation grid plus multistart local refinement | **Resolved.** 2H A_min=0.04253608528, odd RMS=0.20624278237, multistart spread 8.33e-17; symmetric 3R controls are null. | Registry inversion-asymmetry claim retained with explicit global-search protocol. |
| Compact size law might be specific to small N or one shape | Extend hexagons to N=1261; add disk-like compact family to N=931 | **Resolved within rigid compact-contact scope.** At scaled Theta=20, cross-size deviations are <0.082% (hex) and <0.023% (disk); family means differ by about 0.10%. | Claim narrowed to compact self-similar contacts; exponent interpreted as 1/2 similarity with finite-size corrections. |
| Boundary sign reversal might be a global-envelope branch-selection artifact | Enumerate competing triangular registry minima and follow both force branches through high twist | **Corrected, not merely confirmed.** The physically prepared ground state switches between two registry families carrying opposite biases. Switches: 2.921278008 deg (20 deg cut), 2.847233122 deg (25 deg cut). | Old smooth global-envelope zero crossing removed. Main mechanism is now **ground-state registry switching**. |
| Exact boundary reversal angle might be overinterpreted | Vary outer-site local-GSFE weight from 0.5 to 1.5 | **Sensitivity quantified.** Registry competition persists, but switch angle shifts strongly (20 deg: 3.1701 -> 2.7779 deg; 25 deg: 3.0832 -> 2.7108 deg). | Exact switch twist explicitly labeled edge-model dependent; no material-constant claim. |
| Vector mode locking had been validated mainly on one period slice | 13 amplitudes x 7 periods = 91-point F0-period map | **Resolved for finite-run locking on sampled grid.** 91/91 sampled states meet the integer-winding tolerance; multiple vector states occur. | Manuscript separates finite-run map from rigorous Floquet proof of representative states. |
| Extremely small Floquet radius might be solver-conditioning artifact | DOP853 at two tolerances and Radau cross-check | **Resolved.** rho_F=6.31108124e-22 to 6.31109869e-22; closure <1.92e-11. | Last digits are not physically interpreted; only strong attraction / rho_F<1 is claimed. |
| Free thermal current lacked uncertainty and cycles could be pseudoreplicated | 1000 independent trajectories per T; all cycles clustered within trajectory; 10,000 trajectory bootstrap resamples | **Resolved.** Mean v current CI remains <0 through T*=0.60, includes 0 at T*=0.65. P(Delta y<0) remains >0.5 through T*=0.50; at 0.55 the CI touches neutrality. | Figure 6 and thermal text replaced by trajectory-cluster CIs; high-noise claims calibrated. |
| Reproducibility package was not yet self-contained | Ship core source snapshot, audit scripts, canonical CSVs, trajectory-level thermal data, figures, path-independent validator, hashes | **Resolved for numerical-contract validation.** `python validate_release.py` passes. | Data/code availability updated; no archival DOI is claimed until external deposition. |

## 1. Prepared-state branch continuation

The audit correctly identified a conceptual ambiguity in defining the depinning threshold as the largest force at which *any* metastable minimum survives. To determine whether this inflated the directional split, all stationary points in a primitive registry cell were enumerated and the stable zero-force minima were continued separately under positive and negative longitudinal loading.

For the N=127 compact hexagonal contact, two stable zero-force registry families are present throughout the sampled 0-3 deg range. At all 13 sampled twist angles, the family with the lower zero-force energy also survives to the larger force magnitude for **both** loading signs. Therefore the reported headline threshold is also the adiabatic depinning threshold of the prepared lowest-energy state for this family.

At theta=1.5 deg:

- prepared ground branch: F_c,+*=3.0711353385, F_c,-*=1.2586722985;
- metastable branch: F_c,+*=0.211059 (approximately), F_c,-*=0.611697 (approximately).

This eliminates the main reviewer concern that the large rho value arose by taking unrelated last-surviving basins in opposite directions.

## 2. Matched symmetry falsification

Two controls were generated from the **same** centered 2H Fourier spectrum:

1. a matched symmetrized surface obtained by removing the odd component about the translation-minimized inversion center;
2. the exact spatial inversion of the centered 2H surface.

The symmetrized surface contains two inversion-related degenerate minima. A single selected minimum may have asymmetric branch thresholds, but its inversion partner has them swapped. Consequently the correct null quantity is the symmetry-paired/global envelope or a symmetry-balanced preparation ensemble. That envelope is direction-degenerate to 6.57e-10, and the deterministic symmetric-preparation current norm is 8.51e-18.

For the exact inversion, the original thresholds are exchanged to machine precision and the vector current reverses. This is the strongest internal symmetry contract in the manuscript and replaces the weaker inference based only on different 3R stackings.

## 3. Registry-asymmetry global search

The origin-optimized odd-power functional was evaluated on a 181x181 translation grid and refined from multiple starting points. The asymmetric 2H surface gives

- A_min = 0.04253608528;
- odd RMS fraction = 0.20624278237;
- multistart objective spread = 8.33e-17.

The two inversion-symmetric 3R controls are zero to numerical precision. Thus the coordinate-invariant registry-asymmetry result is not a local-optimizer artifact.

## 4. Size and shape robustness

The scaled-twist test was expanded beyond the original N=37-469 hexagonal sequence:

- hexagonal compact family: N up to 1261;
- disk-like compact family: N up to 931.

At Theta=20, the maximum cross-size relative deviations are about 0.0818% / 0.0800% for forward/reverse hexagonal thresholds and 0.0230% / 0.0222% for disk-like contacts. The mean hex/disk scaled curves differ by only about 0.10% at that scaled angle.

The result is therefore best stated as **compact self-similar finite-contact scaling in theta sqrt(N)**. The fitted 0.503-type exponents are not treated as new universal critical exponents; they approach the expected inverse-linear-size exponent 1/2 as small contacts are removed.

## 5. Boundary reversal: corrected physical interpretation

The branch-resolved triangular calculation changed the interpretation of the high-twist reversal. For both 20 deg and 25 deg cuts there are two competing zero-force registry minima, A and B. Their branch-followed threshold differences have opposite signs. As twist increases, their zero-force energies cross and the identity of the prepared ground state switches.

The ground-state switches occur at:

- 20 deg cut: theta = 2.92127800838 deg;
- 25 deg cut: theta = 2.84723312226 deg.

Immediately across these crossings the prepared-ground-state directional split jumps from roughly +0.67/+0.70 to roughly -0.67/-0.70. Hence the physically meaningful reversal is not a smooth crossing of a global last-surviving-minimum envelope. It is a **registry-state switch** between competing prepared states.

A boundary-site weighting sensitivity test shows that the existence of the competition is robust to a simple edge-energy perturbation, while the numerical switch angle is not. This is now stated explicitly in the manuscript.

## 6. Vector mode-locking breadth and Floquet conditioning

At theta=1.5 deg, the unguided model was scanned on a 13 x 7 grid:

- F0*=1.0 to 4.0 in steps of 0.25;
- period tau*=20, 30, 40, 50, 60, 70, 80.

All 91 sampled finite-run states satisfy the integer-winding tolerance, with multiple vector windings including (0,0), (1,-1), (1,-2), (2,-3), and (3,-5). The manuscript does **not** equate this finite-run criterion with an independent Floquet proof at every point.

For the representative theta=1.5 deg, F0*=2, tau*=40 state, three independent variational integrations give a spectral radius near 6.3111e-22 and state closure below 2e-11. The only physically important conclusion retained is rho_F<1 and strong attraction.

## 7. Thermal uncertainty and the correct independent unit

The free thermal calculation was rerun using 1000 independent trajectories at each canonical temperature. Each trajectory contributes an aggregate over its measured cycles, and bootstrap resampling is performed at the **trajectory** level rather than treating cycles as independent replicates.

Selected results:

| T* | mean lattice-v / cycle | 95% cluster-bootstrap CI | P(Delta y<0) | 95% CI |
|---:|---:|---:|---:|---:|
| 0.02 | -2.4280 | [-2.4411, -2.4147] | 0.9984 | [0.9976, 0.9991] |
| 0.10 | -1.3536 | [-1.3820, -1.3242] | 0.8158 | [0.8082, 0.8232] |
| 0.32 | -0.3468 | [-0.3968, -0.2963] | 0.5552 | [0.5452, 0.5651] |
| 0.50 | -0.1442 | [-0.2083, -0.0788] | 0.5176 | [0.5079, 0.5274] |
| 0.60 | -0.0859 | [-0.1550, -0.0157] | 0.5059 | [0.4965, 0.5151] |
| 0.65 | -0.0652 | [-0.1365, +0.0076] | 0.5067 | [0.4971, 0.5162] |
| 0.70 | -0.0399 | [-0.1175, +0.0390] | 0.5012 | [0.4916, 0.5110] |

Thus the mean vector current is statistically resolved as negative through T*=0.60 in this protocol and is no longer resolved at T*=0.65. The stricter cycle-sign probability remains resolved above 0.5 through T*=0.50, while the 0.55 interval reaches neutrality. Exact deterministic winding identity is far more noise-sensitive and is not used as a high-temperature fidelity claim.

## 8. Higher-order stability point

Generic depinning folds were checked for nonzero soft-mode cubic derivative. One isolated point near theta=2.97338566 deg, F*=1.91007353 has vanishing transverse quadratic/cubic structure while the hard Hessian eigenvalue remains positive. It remains labeled a **higher-order stability degeneracy**, not a generic saddle-node. No stronger catastrophe classification is claimed without dedicated two-parameter normal-form continuation.

## 9. Reproducibility closure

The audit-resolved release contains the main manuscript, Supplementary Information, the scientific source snapshot, exact analysis scripts, canonical tables, raw trajectory-level thermal aggregates, final figures, environment/configuration context, a path-independent validator, and SHA-256 hashes.

`python validate_release.py` checks the following contracts directly from the shipped tables:

- prepared ground state is lower-energy and longer-lived for both signs on the sampled reference branch;
- N=127 theta=1.5 deg headline thresholds;
- same-2H symmetry-null and exact-inversion swap/current reversal;
- global registry-asymmetry optimization;
- two-family compact size collapse;
- ground-state boundary registry switching and sign reversal;
- 91-point vector finite-run locking plus representative winding;
- cross-integrator Floquet stability;
- thermal cluster-bootstrap conclusion at T*=0.50/0.55 and 0.60/0.65.

The release validator passes in the current environment.

## 10. Questions that cannot be solved from the present input without inventing physics

The following are **not internal manuscript contradictions** and were not fabricated away:

1. **Relaxed/elastic edges and nonlocal edge energetics.** The present finite contact is a rigid sitewise local-GSFE model. The edge-weight test is a sensitivity analysis, not a substitute for atomistic relaxation.
2. **Physical polarity-to-GSFE mapping.** A quantitative P_z reversal/tuning law requires paired polarity-resolved first-principles surfaces or equivalent atomistic data.
3. **Load dependence.** The published input used here does not provide a full normal-load-dependent GSFE family.
4. **Experimental mass, damping, time and temperature mapping.** These are not derived from the same first-principles calculation and must be independently calibrated before physical-unit operating predictions are made.
5. **Experimental validation.** No numerical reanalysis can substitute for measured depinning thresholds or vector transport.

These limitations are now explicit scope boundaries in the manuscript. They no longer support hidden extrapolations.

## Final audit-resolution conclusion

All concerns that can be decided using the existing published-GSFE reduced model have been recalculated rather than handled by wording alone. The most consequential outcomes are:

- the original headline free-contact depinning split survives a prepared-state branch audit;
- mechanism attribution now passes matched same-2H symmetrization and exact-inversion contracts;
- the boundary-reversal mechanism was **corrected** from a smooth global-envelope crossing to a ground-state registry switch;
- compact theta sqrt(N) scaling survives larger sizes and a second compact shape family;
- vector locking is broadened to a 91-point F0-period grid while rigorous Floquet claims remain representative rather than universal;
- thermal robustness is now reported with trajectory-cluster uncertainty and an explicit loss-of-resolution criterion;
- unresolved questions now require genuinely new material/experimental input rather than additional manipulation of the present data.
