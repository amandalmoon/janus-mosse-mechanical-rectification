# EXP-001 Phase-0 Execution Report

## Decision

**PASS within the preregistered Phase-0 boundary.** No production equilibrium-response predictor and no scientific driven validation were performed.

## Frozen upstream

- N29 science reference commit: `327c58e2684398ba7bc11205865f8222066c3539`
- Frozen VFF source: `research-os/janus_n8_gate/vff_reconstruction.py`
- Frozen GSFE source: `reproducibility/Janus_MoSSe_Current_ReproducibilityRelease_v2/source/janus_fourier_landscapes_v12.py`
- Discovery reference system: N=127, theta=1.5 deg, nominal nonlinear VFF.

## P0.1 — frozen VFF static baseline

PASS.

- N = 127; internal DOF = 251
- bonds / angles = 342 / 648
- rigid-mode projection residual = 4.146e-15
- zero-force gradient norm = 1.495e-07
- finite-difference energy-gradient max error = 8.302e-11
- finite-difference gradient-Hessian-column max error = 1.390e-08
- F_c,+* = 2.935400391
- F_c,-* = 1.190478516
- rho = 0.422921253

These reproduce the frozen independent nonlinear-VFF reference (2.935400, 1.190479, 0.422921) within the Phase-0 tolerance.

## P0.2 — mass transform

PASS. For 100 random projected internal velocity states,

`sum_i 1/2 |v_i|^2 = 1/2 N |qdot|^2 + 1/2 |adot|^2`

with maximum absolute error 1.137e-13. The implemented mass matrix is therefore `diag(N,N,1,...,1)` for equal reduced site masses and orthonormal projected internal coordinates.

## P0.3 — internal Langevin FDT

PASS for the Phase-0 pilot.

- primary T* = 0.01; zeta_b* = 1.0
- dt = 0.000576312996713
- estimated highest ground-state internal angular frequency = 86.758411
- four-seed maximum absolute kinetic-equipartition error = 2.486%
- four-seed mean relative error = -1.093%
- half-dt seed check relative error = -0.053%

The bath acts only on the 251 internal coordinates. No direct COM Langevin damping/noise was used.

## P0.4 — constrained equilibrium pilot

PASS as a planning pilot, not as a production response estimate.

Two independent 100-time-unit force trajectories were used for the extended planning ACF. The ensemble-mean force ACF gives:

- x sustained |ACF| < 0.05 for 1 time unit at t = 6.084
- y sustained |ACF| < 0.05 for 1 time unit at t = 9.768
- planning cutoff tau_mem = 9.768
- preregistered minimum production time from 200 tau = 1953.6 reduced time units per production trajectory.

**Caution:** the 40-time-unit ACF window still contains oscillatory recurrences (last-window |ACF| maxima about 0.158 in x and 0.139 in y). Therefore the pilot does not justify a single-exponential memory time or a Markov model. It only fixes a conservative production-length scale.

## P0.5 — energy-accounting implementation diagnostic

PASS. After fixed-q pre-equilibration, a one-period prescribed diagnostic oscillation with A=0.0025 and Omega=0.1 gave:

- first-law residual = -5.123e-05
- relative residual versus |W|+|Q| = 1.685e-04
- simulated period fraction = 1.000001513

This trajectory is bookkeeping-only. Its loss is not used to fit or select M0-M3 and is not a scientific driven-validation result.

## Gate interpretation

Phase-0 establishes that the frozen VFF baseline, coordinate/mass transformation, internal-only Langevin bath, and energy bookkeeping are internally consistent enough to proceed. It does **not** establish that equilibrium response predicts driven loss, that memory is required, or that a scalar/tensor model fails.

Before Phase-1 begins, the production trajectory count/length, ACF/window estimator, frequency-grid rule, and predictor-artifact schema must be frozen. No driven scientific validation is authorized by this report.
