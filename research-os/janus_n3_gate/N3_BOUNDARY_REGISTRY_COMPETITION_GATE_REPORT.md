# N3 Boundary Registry Competition Gate Report

## Verdict

**PASS, with a scope refinement for the edge-weight sensitivity statement.**

The nominal 20° and 25° triangular contacts do not reverse their prepared-state directional response through a smooth zero of a single threshold envelope. Two coexisting zero-force registry minima, A and B, remain stable through the transition, their energies cross, and they carry opposite branch-followed directional splittings. Selecting the lower-energy zero-force state therefore produces a discontinuous prepared-state sign change at the registry-energy crossing.

## 1. Nominal prepared-state switches

| cut | prepared energy switch (deg) | smooth global-envelope zero (deg) | offset (deg) | DeltaF_A at switch | DeltaF_B at switch |
|---|---:|---:|---:|---:|---:|
| 20° | 2.921278008381 | 2.913346601887 | 0.007931406 | +0.665271 | -0.669050 |
| 25° | 2.847233122262 | 2.839400614994 | 0.007832507 | +0.699754 | -0.703441 |

The response jump is -1.334321 for the 20° cut and -1.403194 for the 25° cut. The zero-force energy crossings are transverse, with d(U_A-U_B)/dtheta = 0.216197 and 0.224319 per degree, respectively.

The older smooth global-envelope zero crossing precedes the physically prepared switch by about 0.008°. It is therefore a distinct diagnostic quantity, not the preparation-defined reversal angle.

## 2. Stationary-point completeness near the switches

A 21x21 primitive-cell stationary-point enumeration was repeated at the nominal switch and at ±0.002°. Every checkpoint contains exactly two stable minima, corresponding to the A and B registry families. The maximum stationary residual is 1.395e-15, and the minimum stable Hessian eigenvalue is 5.939152.

No third stable minimum undercuts the A/B pair near either nominal transition.

## 3. Boundary orientation scope

For the fixed-N=127 triangular family, the A/B zero-force energy crossing occurs at:

| cut | first A/B crossing (deg) | inside 0-3°? |
|---|---:|---|
| 5° | 3.966207672 | no |
| 10° | 3.256546314 | no |
| 15° | 3.053753241 | no |
| 20° | 2.921278008 | yes |
| 25° | 2.847233122 | yes |

Thus only the 20° and 25° cuts switch prepared registry within the stated 0-3° nominal scan. The 15° family crosses only just above 3°, while the 5° and 10° families cross later.

## 4. Outer-site weighting sensitivity

The 48 outer sites were assigned relative local-GSFE weights 0.5, 0.75, 1.0, 1.25, and 1.5, with interior sites fixed at unity. For all ten (cut, weight) combinations:

- the A/B energy crossing persists;
- A and B are stationary and stable at the crossing;
- a 21x21 global search finds exactly two stable minima at the crossing;
- branch A carries positive DeltaF and branch B carries negative DeltaF;
- the augmented-fold residual stays below the numerical contract.

| cut | edge weight | switch (deg) | inside 0-3° | DeltaF_A | DeltaF_B |
|---|---:|---:|---|---:|---:|
| 20° | 0.50 | 3.170095 | no | +0.668679 | -0.672282 |
| 20° | 0.75 | 3.026591 | no | +0.666656 | -0.670349 |
| 20° | 1.00 | 2.921278 | yes | +0.665271 | -0.669050 |
| 20° | 1.25 | 2.841009 | yes | +0.664301 | -0.668143 |
| 20° | 1.50 | 2.777914 | yes | +0.663606 | -0.667488 |
| 25° | 0.50 | 3.083165 | no | +0.702558 | -0.706137 |
| 25° | 0.75 | 2.947202 | yes | +0.700830 | -0.704468 |
| 25° | 1.00 | 2.847233 | yes | +0.699754 | -0.703441 |
| 25° | 1.25 | 2.770909 | yes | +0.699056 | -0.702770 |
| 25° | 1.50 | 2.710829 | yes | +0.698590 | -0.702311 |

The full switch ranges are 2.7779-3.1701° for the 20° cut and 2.7108-3.0832° for the 25° cut.

### Important scope correction

The qualitative **registry competition and A/B crossing** are robust across all tested weights, but occurrence of the crossing **inside the original 0-3° window is not**. For the 20° cut, only 3/5 tested weights switch by 3°; for the 25° cut, 4/5 do. Weak edge weighting moves the switch to 3.1701° (20°, weight 0.5), 3.0266° (20°, 0.75), and 3.0832° (25°, 0.5).

Therefore the strongest supported wording is:

> Boundary rotation creates competition between registry families carrying opposite directional biases. Their ground-state crossing can reverse the prepared response, but the switch angle—and whether it falls within a chosen finite twist window—is strongly edge-model dependent.

It is too strong to imply that the sign reversal necessarily occurs within 0-3° for all plausible edge-weight perturbations.

## 5. Numerical contracts

- maximum A/B stationary gradient residual across all tested edge weights: 1.840e-15
- minimum zero-force stable Hessian eigenvalue: 5.929398
- maximum fold residual: 3.580e-14
- minimum hard fold eigenvalue: 8.376838

## Claim status

**VERIFIED within the rigid fixed-N triangular boundary model:**

- coexistence of two prepared registry minima;
- transverse zero-force energy crossing at nominal 20° and 25° cuts;
- opposite branch-followed directional biases of the two families;
- prepared-state sign change caused by ground-state registry switching;
- distinction from the smooth global last-surviving-minimum envelope;
- strong edge-model sensitivity of the switch location.

**NOT established:**

- a universal switch angle;
- persistence of the switch inside 0-3° under all edge models;
- behavior of reconstructed, chemically specific, deformable, or fully atomistic edges.

## Gate

**N3 = VERIFIED within the tested rigid boundary model, with the switch-angle claim explicitly treated as edge-model dependent.**
