# EXP-001 Phase-0 — Implementation and Equilibrium Pilot Plan

## Authorization boundary

Human approval authorizes **Phase-0 only**. No production equilibrium-response claim, no predictor comparison, and no driven validation may be interpreted before this phase passes.

## Objective

Establish that the existing N29 VFF static model can be extended to internal-coordinate Langevin dynamics without changing its frozen conservative baseline or smuggling the old COM damping into the new model.

## Required checks

### P0.1 — frozen static baseline reproduction

At N=127, theta=1.5 deg, nominal VFF stiffness:
- reproduce the zero-force ground state from the frozen N29 science source;
- reproduce bond count = 342;
- reproduce angle count = 648;
- reproduce rigid-mode projection residual at numerical precision;
- reproduce ground-state gradient/Hessian checks;
- retain the exact published/corrected GSFE source used by the frozen N29 science commit.

Failure blocks all dynamics.

### P0.2 — coordinate and mass transform

For random site velocities satisfying the projected internal-coordinate constraint, independently verify

```
sum_i 1/2 |v_i|^2
=
1/2 N |qdot|^2 + 1/2 |adot|^2
```

to floating-point precision.

No fitted mass parameter is allowed.

### P0.3 — internal Langevin FDT

With q constrained at q0 and the interface conservative model fixed:
- couple bath only to internal coordinates;
- no direct COM damping/noise;
- verify stationary internal kinetic-energy statistics against the declared reduced temperature;
- verify zero mean internal velocity;
- verify result at primary `zeta_b*=1, T*=0.01`;
- use a half-time-step subset if discretization bias is visible.

Any material bias unresolved by time-step reduction blocks Phase-1.

### P0.4 — constrained-equilibrium pilot

Purpose: estimate correlation structure only.

Allowed outputs:
- force time series `Fx,Fy`;
- force covariance;
- rough integrated-correlation/memory times;
- internal kinetic/potential energy;
- bath heat;
- mode projections for diagnostics.

Forbidden uses:
- no headline scientific claim;
- no model selection;
- no driven-data comparison;
- no tuning of a future predictor to a driven result.

Pilot determines production trajectory length using the frozen rule in DESIGN-01.

### P0.5 — energy-accounting implementation test

Before production:
- verify bath heat bookkeeping in a linear test system;
- verify full-contact stored-energy accounting under the smallest diagnostic prescribed oscillation;
- this diagnostic is implementation-only and must not be used to select M0–M3 or to tune response parameters.

## Phase-0 deliverables

- `EXP-001_P0_STATIC_BASELINE.json`
- `EXP-001_P0_MASS_TRANSFORM.json`
- `EXP-001_P0_FDT.json`
- `EXP-001_P0_PILOT_SUMMARY.json`
- `EXP-001_P0_ENERGY_ACCOUNTING.json`
- exact run configuration and seeds
- source commit IDs and SHA-256 checksums
- a Phase-0 gate report

## Stop condition

If any required check fails, preserve the failed artifact and stop. Do not repair by changing the scientific question, bath, amplitude, or conservative model until the failure has an identified owner and the design gate is revisited.
