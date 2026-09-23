# NP-RESTART-01 Gate Report — 2026-09-23

## CURRENT STAGE

Execution / data preparation — EXP-001 Phase-0 authorized.

## LAST VALID GATE

GATE-DESIGN — PASS for the bounded Phase-0 branch.

## CURRENT GATE STATUS

PARTIAL. Human approval authorizes implementation and Phase-0 checks only. Scientific production and driven validation remain blocked until Phase-0 passes and predictor-generation settings are frozen.

## VERIFIED

- RQ-01 is frozen: predict small prescribed-oscillation energy loss from pre-sliding equilibrium response.
- First branch excludes corner-edge crossover and free-running transport.
- N29 remains a frozen upstream reference only.
- Dynamic coordinate/mass convention: total reduced potential `N*U_per-site`, mass matrix `diag(N,N,I_internal)`.
- COM receives no direct bath in the first branch.
- Nested response models M0 scalar -> M1 tensor -> M2 spatial -> M3 memory are fixed.
- Cycle-loss theory contract has passed algebraic/numerical sanity checks.
- Human has explicitly approved EXP-001 Phase-0 and requested separate GitHub storage.

## PENDING

- frozen VFF static reproduction under the new execution harness;
- mass-transform numerical test;
- internal Langevin FDT check;
- constrained-equilibrium pilot;
- correlation-time estimate;
- production trajectory length;
- predictor freeze;
- all scientific M0/M1/M3 results.

## REJECTED / NOT ALLOWED

- new physics before null-model discrimination;
- corner-to-edge crossover in EXP-001 Phase-0;
- material-specific physical damping in SI units;
- free-running winding/ratchet transport;
- non-Markovianity merely because a scalar fit fails;
- modifying frozen N29 scientific results.

## DIRTY ARTIFACTS

None in N29. This branch is isolated.

## BLOCKERS

B-003 — Phase-0 implementation checks not yet executed; owner: simulation/data workflow.

## NEXT GATE

GATE-EXP001-P0.

## NEXT ACTION

Implement and execute P0.1–P0.5 only. Preserve failures. Stop before production equilibrium response or driven validation.
