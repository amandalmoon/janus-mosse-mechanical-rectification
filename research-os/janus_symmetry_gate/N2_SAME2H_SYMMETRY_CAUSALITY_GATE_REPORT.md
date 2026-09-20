# Same-2H Symmetry Causality Gate

## Scope
Independent reconstruction from the surviving Angeli-anchored 2H MoSSe Fourier GSFE. The control surfaces are constructed from the **same centered 2H spectrum**, not from a different 3R stacking.

Controls:
1. `2H_centered`: original 2H GSFE translated to the translation-minimized odd-power center.
2. `2H_matched_symmetrized`: same centered cosine coefficients, all centered sine/odd coefficients set to zero.
3. `2H_exact_inverted`: same centered cosine coefficients, centered sine/odd coefficients multiplied by -1.

Reference contact: N=127 compact hexagon. Static contracts are evaluated at theta=1.5 deg. Deterministic rocking uses theta=1.5 deg, F0*=2, tau*=40, m*=1, gamma*=4, 20 transient cycles, 40 measured cycles, and 4000 RK4 steps/cycle unless otherwise stated.

## 1. Translation-minimized inversion center
A brute 181x181 fractional-cell search followed by 17 independent local refinements gives

- A_min = 0.04253608528083287
- odd RMS = sqrt(A_min) = 0.20624278237269994
- best center, one symmetry-equivalent representative: (u,v) = (0.66666666614, 0.66666666609)
- Cartesian center = (0.99999999919, 0.57735026869)
- multistart objective spread among equivalent minima = 2.15e-16

This independently reproduces the manuscript's coordinate-invariant asymmetry diagnostic.

## 2. Pointwise symmetry identities
Over 10,000 random local-registry points:

- max |u_sym(r)-u_sym(-r)| = 0 within floating-point evaluation
- max |u_inv(r)-u_orig(-r)| = 0 within floating-point evaluation

For the finite N=127 twisted contact at theta=1.5 deg:

- max |U_sym(R)-U_sym(-R)| = 1.11e-16
- max |U_inv(R)-U_orig(-R)| = 2.22e-16

An additional 0-3 deg sweep (121 twist values, 40 random registry points per twist) gives:

- max finite-contact symmetric identity error = 1.39e-16
- max finite-contact inversion identity error = 2.22e-16
- maximum imaginary part of the compact-contact structure factor = 1.11e-16

Thus the symmetry contracts are identities of the finite-contact potential, not only local-GSFE checks at one twist.

## 3. Static branch contracts at theta=1.5 deg

### Original centered 2H
Ground branch:
- Fc,+ = 3.071135338539257
- Fc,- = 1.258672298499954
- Delta Fc = +1.812463040039303

Competing metastable branch:
- Fc,+ = 0.211058643...
- Fc,- = 0.611697272...

The centered-ground thresholds reproduce the independent prepared-branch audit to <3.93e-11.

### Matched symmetrized same-2H
Two exactly degenerate zero-force minima are present.

Minimum 0:
- Fc,+ = 1.767702230451907
- Fc,- = 0.643470...

Minimum 1:
- Fc,+ = 0.643470...
- Fc,- = 1.767702230452023

Hence an individual selected member of the degenerate pair can have an asymmetric branch threshold, but the symmetry-respecting paired/global observable is

- global Fc,+ = 1.767702230451907
- global Fc,- = 1.767702230452023
- |global split| = 1.16e-13

This is the correct static null contract for a degenerate inversion-paired preparation.

### Exact inversion of the same 2H spectrum
Ground branch:
- Fc,+[U_inv] = 1.258672298499955
- Fc,-[U_inv] = 3.071135338539251

Swap errors:
- |Fc,+[U_inv] - Fc,-[U_orig]| = 6.66e-16
- |Fc,-[U_inv] - Fc,+[U_orig]| = 6.22e-15

The maximum augmented fold residual over all six tested branches is 3.75e-9 and the minimum hard Hessian eigenvalue is 10.9325 > 0.

## 4. Deterministic zero-mean rocking contract
At theta=1.5 deg, F0*=2, tau*=40:

Original centered 2H ground state:
- mean lattice displacement/cycle = (1.000000000000006, -1.000000000000010)
- winding = (1,-1)

Exact-inverted 2H ground state:
- mean lattice displacement/cycle = (-1.000000000000000, 1.000000000000000)
- winding = (-1,1)

Current-reversal residual vector:
- J_orig + J_inv = (6.22e-15, -9.77e-15)
- norm = 1.16e-14

Matched symmetrized same-2H:
- both inversion-related zero-force minima remain pinned at this representative drive
- equal-preparation mean current norm = 7.41e-17 at 4000 steps/cycle

The maximum integer-locking residual among the four simulations is 1.21e-14.

## 5. Time-step robustness
The symmetry contracts were repeated at 1000, 2000, 4000, and 8000 steps/cycle.

Across all four resolutions:
- original winding remains (1,-1)
- inverted winding remains (-1,1)
- current-reversal norm remains <=1.16e-14
- symmetric balanced-current norm remains <=1.31e-16

At 8000 steps/cycle the symmetric-current norm is 5.37e-18 and inversion-current reversal residual is 3.45e-15.

## 6. Interpretation
The static and deterministic directional response is therefore controlled by **registry-space inversion asymmetry of the same 2H GSFE within the tested reduced model**:

- removing the centered odd sector restores the symmetry-required direction-degenerate paired static response and zero deterministic current;
- exact spatial inversion swaps the forward/reverse depinning thresholds and reverses the lattice-vector current to numerical precision.

This is stronger than using chemically different 3R stackings as the causal control. The 3R cases remain useful external material-derived nulls, but they are not needed for the core symmetry attribution.

This does **not** establish a quantitative physical polarization law Pz -> rectification. A physical polarity reversal can change multiple Fourier amplitudes and phases and still requires a polarity-resolved first-principles GSFE pair.

## Gate
**PASS — SAME-2H SYMMETRY CAUSALITY CONTRACT VERIFIED WITHIN THE RIGID FINITE-CONTACT MODEL.**
