# N4 Odd-Sector / Registry-Origin Gate Report

## Decision

**Gate result: PASS as a falsification audit, with the original N4 material-law claim rejected.**

The physically meaningful result is the coordinate-invariant registry asymmetry of the published 2H GSFE. The old continuation `U_eta = U_even + eta U_odd` is not a material susceptibility unless the origin/gauge construction is explicitly fixed. Even after a translation-minimized gauge is imposed, `eta` remains a mathematical homotopy rather than a physical polarization coordinate.

## 1. Fourier translation algebra
For

`u(r) = sum_alpha [c_alpha cos(G_alpha.r) + s_alpha sin(G_alpha.r)]`,

a registry-origin shift by `a` rotates the coefficient pair with `delta_alpha = G_alpha.a`:

`c'_alpha = c_alpha cos(delta_alpha) + s_alpha sin(delta_alpha)`

`s'_alpha = s_alpha cos(delta_alpha) - c_alpha sin(delta_alpha)`.

Therefore the separate cosine/even and sine/odd sectors are not coordinate-invariant. This identity was checked symbolically with Wolfram Language.

Writing `C_alpha = c_alpha - i s_alpha` gives `C'_alpha = C_alpha exp(i G_alpha.a)`. For a C3 reciprocal triad with `G1+G2+G3=0`, the product `C1 C2 C3` is exactly translation invariant. Hence the first-shell diagnostic quoted as `sin(3 phi_1)` is valid when understood as the normalized imaginary part of this triad product, not as a common single-vector phase after arbitrary translation.

Numerically, 1000 random registry translations gave

- `chi1 = 0.583541211356118`
- maximum translation error = `9.992e-16`.

## 2. Coordinate-invariant asymmetry survives
The independent origin minimization gives

- `A_min = 0.04253608528083`
- `sqrt(A_min) = 0.20624278237270`.

By contrast, at the originally published registry origin the origin-fixed odd-power fraction is `0.553981419` (RMS `0.744299280`). This large difference is exactly why an origin-fixed sine amplitude is not a material observable.

## 3. Physical eta=1 thresholds are gauge invariant
Across 26 tested registry origins, the physical `eta=1` landscape was only reparameterized. The spread of the branch-followed physical threshold split was

`max(Delta F_c)-min(Delta F_c) = 9.770e-15`.

Thus the physical N=127, theta=1.5 deg result is origin invariant while the decomposed even/odd coefficients are not.

## 4. eta=0 topology itself depends on the arbitrary symmetrization center
Among the 26 tested gauges:

- 17 produced one self-inversion stable ground minimum at `eta=0`;
- 9 produced two exactly degenerate inversion-related stable minima.

At the published origin the `eta=0` surface has one stable minimum and its two directional thresholds are equal, so the positive-eta curve is locally smooth. A fit through `eta=0.025, 0.05, 0.075, 0.10` gives

`d DeltaF / d eta ~= 2.833382128` with `R^2=0.999999764`.

This number is nevertheless gauge-fixed, not a material susceptibility.

At the translation-minimized `A_min` center the symmetric surface instead has two degenerate ground minima. Their branch-specific threshold splits are `+/- 1.124231291`. An infinitesimal positive odd perturbation selects one member of that pair, and already at `eta=0.025` the prepared-ground split is `1.142632733`.

Therefore the prepared-state observable has a finite one-sided limit rather than a linear response about zero. **A derivative `d DeltaF_c/d eta |_(eta=0)` does not exist for this canonical centered prepared-state construction.**

## 5. The old intermediate optimum is not invariant
For the unguided published-origin path, the sampled maximum is at `eta=0.925`; a local quadratic interpolation gives approximately `eta=0.925435`. At the translation-minimized center the positive-eta curve instead increases through the tested interval and its maximum on `[0,1]` is the physical endpoint `eta=1`.

This independently agrees with the earlier guided-gauge audit, which found that changing registry origin moved the apparent optimum over a broad range. The old `eta ~ 0.5` optimum is therefore not a material result.

## 6. Can a centered eta path be retained at all?
Yes, but only with a much narrower interpretation. If one first defines a translation-minimized center and transports the same minimizer branch under coordinate changes, the centered coefficients transform covariantly. Twenty random reparameterizations gave maximum transported-center error `1.883e-09` lattice units and coefficient differences below `4.347e-09`.

There are four symmetry-equivalent `A_min` centers in the primitive cell. Repeating the `eta=0.5` calculation at those centers gives the same physical thresholds to numerical precision (differences at the few-1e-8 level in the current fold solver). Therefore an `A_min`-centered eta homotopy can be used as a reproducible **mechanism-isolation diagnostic**.

It still cannot be called a physical polarization coordinate, a material susceptibility, or a material optimum.

## Final N4 claim map

- Coordinate-invariant `A_min` / odd RMS: **VERIFIED**.
- Triad-product phase diagnostic (`sin(3 phi_1)` in the equal-phase representation): **VERIFIED**, with the invariant-product interpretation.
- Arbitrary-origin `d DeltaF_c/d eta`: **REJECTED as a material susceptibility**.
- `eta ~ 0.5` intermediate optimum: **REJECTED as a material optimum**.
- Linear response around `eta=0` in the canonical unguided prepared-state model: **REJECTED** because the centered symmetric surface has degenerate ground states and a finite branch-selection jump.
- `A_min`-centered eta path: **RETAIN only as a computational homotopy / SI mechanism diagnostic**.
- Mapping `eta` to experimental Janus polarization `P_z`: **NOT ESTABLISHED**.

## Manuscript action
The current workflow-validated manuscript is already aligned with this conclusion: the main text should rely on coordinate-invariant asymmetry and same-spectrum symmetrization/exact-inversion contracts. Any old statements such as `d DeltaF_c/d eta = 2.8322` or `eta_opt ~ 0.5` should not return to the Abstract, Results headline, or Conclusion. If the eta path is shown at all, move the translation-minimized-centered version to the SI and label it explicitly as a mathematical mechanism diagnostic.
