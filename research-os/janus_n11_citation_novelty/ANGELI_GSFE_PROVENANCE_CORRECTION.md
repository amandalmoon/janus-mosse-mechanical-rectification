# Angeli GSFE provenance correction

## Decision

**CORRECTION REQUIRED AND APPLIED.** An earlier source comment and manuscript shorthand attributed the Fourier phase convention to the 2024 Angeli Erratum. The published Erratum does not make that correction. It corrects inverse-effective-mass table labeling/caption information, Brillouin-zone path information, and one Supplemental interface label.

## What remains valid

The numerical GSFE implementation is unchanged. The 2022 paper states that the scalar continuum potentials are represented on six reciprocal vectors per shell and that C3 symmetry plus reality reduce the shell coefficients to an amplitude and phase. The six vectors split into two C3 triads related by G -> -G. For a real scalar energy, the complex coefficients of opposite reciprocal vectors are conjugates. Choosing one triad as the positive representatives therefore yields

    Omega_l(r) = 2 W_l sum_{m=1}^3 cos(G_lm . r + phi_l),

and after normalization by E0 = 6 W1,

    u_l(r) = [W_l/(3 W1)] sum_{m=1}^3 cos(G_lm . r + phi_l).

This is exactly the real three-vector-per-shell form implemented by the production code. Choosing the conjugate triad corresponds to phi_l -> -phi_l, i.e. spatial inversion. The exact-inversion gate already verifies that this operation swaps directional thresholds/current as symmetry requires.

## Source roles after correction

- **Angeli et al. 2022, PRB 106, 235159:** primary source for the GSFE Fourier form, coefficients, DFT registry sampling, and relaxation protocol.
- **Angeli et al. 2024, PRB 109, 199902(E):** cited only to state the actual erratum scope; it is not the source of the phase pairing used in code.

## Numerical consequence

None. No W_l, phi_l, reciprocal vector, normalization, threshold, trajectory, or figure datum is changed. This is a provenance/documentation correction, not a numerical model correction.
