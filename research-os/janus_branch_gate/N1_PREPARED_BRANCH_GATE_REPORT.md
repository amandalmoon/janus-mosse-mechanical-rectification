# N1 Prepared-Metastable-Branch Gate

Date: 2026-09-19

## Question
Does the N=127 unguided full-2D depinning threshold follow the physically prepared zero-force metastable branch, or is it an unphysical global envelope assembled from whichever minimum survives longest at each load?

## Independent reconstruction
Only the surviving published-GSFE Fourier core (`janus_fourier_landscapes_v12.py`) was used. Prior branch-audit CSVs/reports were not used as numerical inputs.

1. At each theta = 0, 0.25, ..., 3 deg, enumerate stationary points in one primitive registry cell from a 21x21 seed grid.
2. Classify stationary points by the full 2x2 Hessian.
3. Identify the lower-energy stable zero-force minimum as the prepared ground branch; retain the other stable minimum as a metastable control.
4. Continue each minimum separately under +y and -y load.
5. Refine the loss-of-stability point from gx=0 and det(H)=0, with force inferred from gy.
6. Compare the prepared branch threshold with the maximum threshold over the two zero-force stable families (diagnostic global envelope).
7. At theta=0, 1.5, 3 deg, independently enumerate all stationary points just below and just above the prepared threshold.
8. Independently locate the known higher-order point near theta=2.9734 deg and test whether it belongs to the prepared branch.

## Gate results

- 13/13 twist values contain exactly two stable zero-force minima.
- 13/13: the same family is lower in zero-force energy.
- 13/13: that lower-energy family has the larger +y stability threshold.
- 13/13: that lower-energy family has the larger -y stability threshold.
- Therefore, over this sampled N=127 compact-hexagon family, the diagnostic global envelope equals the prepared-ground threshold for both loading directions.
- This equality is an empirical result of this family; it is not a valid general definition of physical depinning.

### Representative theta=1.5 deg

Prepared ground branch:
- Fc,+ = 3.07113533853926
- Fc,- = 1.25867229849995
- U0 = -0.559658194102772

Competing metastable branch:
- Fc,+ = 0.211058643419429
- Fc,- = 0.611697272231306
- U0 = -0.251473743395188

Thus the large directional split is not formed by taking unrelated final basins in the two directions.

## Full-2D stability-boundary checks

Across all 52 independently refined folds (13 theta x 2 zero-force minima x 2 force directions):
- maximum augmented fold residual = 1.08318e-11
- minimum hard Hessian eigenvalue = 6.80594 > 0

At theta=0, 1.5, 3 deg and both force signs, 21x21 global stationary-point enumeration at Fc-1e-4 finds one stable minimum, while enumeration at Fc+1e-4 finds zero stable minima. This verifies actual loss of metastability in the unrestricted 2D registry plane at these representative points.

## Isolated nongeneric point

Independent solve gives:
- theta = 2.97338565582526 deg
- F+ = 1.91007353149670
- (x,y) = (1.00000000000000, 0.204641213088198)
- Hxx = 2.23e-15
- Hxy = -6.67e-15
- Hyy = 6.91380821266585
- soft eigenvector approximately (-1, 0)
- |soft-vector dot force direction| = 9.64e-16
- soft cubic derivative is numerically zero (about 1e-13 at stable finite-difference steps)

Stationary-point enumeration gives one stable minimum just below this force and none just above it. Continuation from the prepared zero-force ground state approaches this point to periodic registry distance 1.96e-6, so the point is on the prepared branch.

Therefore this is a genuine full-2D depinning/stability boundary point, but it is not a generic one-parameter saddle-node/fold. The global manuscript terminology must be `depinning/stability boundary`; `generic fold/saddle-node` may be used only away from this isolated higher-order degeneracy.

## N1 claim status

**PASS, with wording constraint.**

Defensible claim:

> The headline N=127 thresholds are adiabatic, branch-followed loss-of-metastability thresholds of the lowest-energy zero-force registry state in the unrestricted two-dimensional contact. Over theta=0-3 deg sampled every 0.25 deg, the prepared ground-state family is also the longest-lived stable family for both loading directions, so the older global-envelope values coincide numerically with the prepared thresholds for this compact-hexagon family. The boundary is generically fold-like, with an isolated higher-order stability degeneracy near theta=2.97338566 deg.

Not defensible:

> The physical threshold is defined as the largest force at which any stable minimum exists.

or

> Every point on the boundary is a generic saddle-node.

## Files

- `stationary_points_21x21.csv`: all independently enumerated zero-force stationary points.
- `branch_folds_independent.csv`: branch-specific fold refinements and genericity diagnostics.
- `prepared_vs_global_summary.csv`: 13-point prepared-vs-global comparison.
- `global_envelope_spotcheck.csv`: all-minimum enumeration just below/above representative thresholds.
- `nongeneric_point_audit.json`: isolated higher-order point audit.
- `nongeneric_point_stability_check.csv`: just-below/above stationary-point enumeration at that point.
- `special_branch_link.json`: link of the higher-order point to the prepared ground-state branch.
- `independent_prepared_branch_audit.py`, `nongeneric_point_audit.py`: independent reconstruction scripts.
