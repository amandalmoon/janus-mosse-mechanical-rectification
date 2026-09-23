# THEORY-01 — Equilibrium-Response Reduction Hierarchy

## Frozen research target

RQ-01: Under a declared two-dimensional finite-contact model and bath condition, can pre-sliding equilibrium response predict the energy dissipated by a small prescribed oscillatory displacement, and what is the minimal reduced dissipative model required?

This stage does not search for a new friction law. It compares nested reductions already permitted by linear-response / generalized-Langevin theory.

## Upstream N29 reference

Reference repository: amandalmoon/janus-mosse-mechanical-rectification  
Frozen N29 science commit: 327c58e2684398ba7bc11205865f8222066c3539  
Static in-plane model source: research-os/janus_n8_gate/vff_reconstruction.py  
Conservative GSFE source: reproducibility/Janus_MoSSe_Current_ReproducibilityRelease_v2/source/janus_fourier_landscapes_v12.py

N29 used the VFF/FEM hierarchy for static in-plane relaxation, while its rocking model used a separately declared COM mass and damping. THEORY-01 addresses only that missing reduction step; it does not change any frozen N29 result.

## Coordinates and energy convention

For N sites,

```
r_i = q + d_i,
d = Q a,
```

where `q=(q_x,q_y)` is the center-of-mass registry coordinate and `Q` spans the internal in-plane subspace after projecting the two rigid translations and infinitesimal rigid rotation, as in the existing N29 VFF implementation.

The existing VFF code returns an energy per site in units of E0. For dynamics we use the equivalent total reduced potential

```
U_tot(q,a) = N U_per-site(q,a).
```

If every contact node carries the same reduced site mass, orthogonality of Q gives

```
T = 1/2 N |qdot|^2 + 1/2 |adot|^2.
```

Thus the mass matrix in `(q,a)` coordinates is

```
M = diag(N,N,1,...,1).
```

This is a coordinate transformation of equal site masses, not a new phenomenological mass law.

## Bath contract

The center-of-mass coordinate receives no direct Langevin damping in this study.

Only internal coordinates are coupled to a declared equilibrium bath. The bath coupling `zeta_b` is a model input. The effective center-of-mass friction inferred from equilibrium response is an output and must not be conflated with `zeta_b`.

Primary reduced bath condition:
- `zeta_b*=1.0`
- `T*=0.01`

Sensitivity-only bath conditions:
- `zeta_b*=0.5, 2.0`
- `T*=0.005, 0.02`

Claims remain conditional on the declared bath unless robustness is explicitly shown.

## Equilibrium force response

During equilibrium-response measurement `q` is constrained at `q0` and only internal coordinates evolve.

```
delta F_i(t) = F_i(t) - <F_i>_q0
C_ij(t;q0) = <delta F_i(t) delta F_j(0)>_q0
```

A frequency-dependent equilibrium response estimator is constructed from the declared constrained equilibrium process. Its use as a reduced friction kernel is a predictor to be validated against independent driven simulations, not assumed exact for arbitrary amplitudes.

## Nested predictor hierarchy

### M0 — constant scalar Markov model

```
F_diss = -gamma0 v
gamma0 = 1/2 tr Gamma0
```

`Gamma0` is obtained from equilibrium low-frequency response, never fitted to driven data.

### M1 — constant tensor Markov model

```
F_diss = -Gamma0 v
```

### M2 — position-dependent Markov model

```
F_diss = -Gamma(q0) v
```

### M3 — frequency-dependent / memory response

```
F_i^diss(t) = -sum_j int_0^infinity K_ij(s;q0) v_j(t-s) ds
```

Interpretation is strictly nested: M0 failure is tested against M1 before memory; M1 failure is tested against spatial dependence before a non-Markovian interpretation.

## Primary validation observable

Prescribe

```
q(t) = q0 + A e cos(Omega t).
```

Driven observable:

```
W_drive = integral_cycle F_ext . dq.
```

Linear-response prediction:

```
W_pred = pi A^2 Omega e^T G(Omega;q0) e.
```

Constant scalar prediction:

```
W_scalar = pi A^2 Omega gamma0.
```

This is a prediction contract, not a new friction law.

## Limiting / sanity conditions

1. `A -> 0`: `W/A^2` approaches a finite limit in the linear-response regime.
2. `Omega -> 0` in a Markovian regime: `G(Omega) -> Gamma0`.
3. Isotropic scalar limit: `Gamma0 -> gamma0 I`.
4. No COM-internal coupling: internally mediated COM dissipation vanishes.
5. `zeta_b -> 0` for a finite nonresonant harmonic internal system: irreversible steady dissipation vanishes away from resonant secular excitation.
6. Under steady prescribed oscillation, cycle-averaged external work equals net heat removed by the bath within statistical error after stored-energy transients vanish.

## Interpretation rules

- M0 failure + M1 success => anisotropy is required; no memory claim.
- M1 failure + M2 success => registry dependence is required; no memory claim.
- M2 failure + M3 success => temporal memory/frequency dependence is required within the tested linear regime.
- M3 failure does not imply new physics. First test linear-response breakdown, heating, structural changes, bath artifacts, insufficient sampling, and numerical convergence.
- A successful equilibrium prediction is evidence of predictability, not a new fundamental law.
