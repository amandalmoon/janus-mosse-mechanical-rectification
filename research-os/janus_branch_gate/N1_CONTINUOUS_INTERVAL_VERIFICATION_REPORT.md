# Continuous prepared-branch verification — N1 final numerical gate

## Scope
This audit upgrades the earlier 0.25-degree prepared-branch check to a dense/adaptive numerical continuation over 0 <= theta <= 3 deg for the N=127 compact rigid hexagonal contact. It tests whether the zero-force ground-state branch ever exchanges energetic order with the competing metastable branch, or becomes shorter-lived under either loading direction.

This is a **numerical continuous-interval verification**, not a formal interval-arithmetic proof.

## Mesh and independent completeness checks
- 491 continuation points.
- Mesh: 0.01 deg to 2.75; 0.002 deg to 2.94; 0.0005 deg to 3.0.
- 16 independent 21 x 21 primitive-cell stationary-point enumerations, concentrated both across the interval and around the known high-twist nongeneric point.
- Every independent checkpoint contains exactly two stable zero-force minima.
- Maximum zero-force stationary residual: 1.330e-15.
- Maximum augmented-fold residual: 5.410e-08.
- Minimum nonsoft Hessian eigenvalue among tracked folds: 6.805938571.
- Maximum periodic branch-tracking displacement between adjacent continuation points: 1.114e-03 lattice-length units.

## Positivity margins over the full tracked interval
| Margin | Minimum | theta of minimum | Maximum adjacent numerical change | Safety ratio |
|---|---:|---:|---:|---:|
| Delta U0 = U_meta - U_ground | 0.173130340444 | 3.000000 deg | 9.759e-04 | 177.4 |
| Delta F+ | 1.702747260989 | 3.000000 deg | 8.804e-03 | 193.4 |
| Delta F- | 0.260864555117 | 3.000000 deg | 2.719e-03 | 95.9 |

All three margins are positive at every continuation point. They decrease monotonically over the tested interval, and the smallest values occur at theta=3 deg rather than at an interior near-crossing.

## Cross-check against the prior 0.25-degree branch audit
Maximum absolute discrepancies at the 13 common old grid points:
- Delta U0: 1.887e-15
- Delta F+: 4.396e-14
- Delta F-: 8.027e-14
- ground F_c,+: 4.396e-14
- ground F_c,-: 8.438e-15

The dense continuation therefore reproduces the independent earlier audit to floating-point precision.

## High-twist nongeneric point
The known isolated higher-order stability degeneracy near theta = 2.9733856558 deg remains on the prepared ground-state forward stability boundary. The independent stationary-point checkpoints on both sides of this region retain exactly two zero-force stable minima and no branch-order exchange. This point remains a real loss-of-metastability boundary but should not be labeled a generic saddle-node exactly at the degeneracy.

## Gate result
**PASS**.

Within the rigid N=127 reduced model and the numerical tolerances above:
1. the same zero-force ground-state family remains the lowest-energy stable minimum throughout 0 <= theta <= 3 deg;
2. that family remains longer-lived than the competing metastable family under both +y and -y loading throughout the tracked interval;
3. no energetic branch crossing, force-threshold reordering, or hidden global-envelope branch switch is observed;
4. the old global envelope equals the prepared-ground threshold for this contact because the prepared branch is actually the longest-lived branch in both directions, not because the global-envelope definition is adopted as the physical observable.

Recommended manuscript wording: **"over the numerically continued 0–3 deg interval"** or **"throughout the numerically resolved 0–3 deg interval"**. Avoid wording that implies a formal analytic proof over a continuum.
