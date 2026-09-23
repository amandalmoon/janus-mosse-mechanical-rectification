# NP-RESTART RQ-01 / EXP-001 Phase-1

This branch inherits the verified EXP-001 Phase-0 state and is reserved for **equilibrium-response production only**.

- Branch: `research/exp001-phase1-equilibrium-response`
- Parent branch: `research/exp001-phase0-equilibrium-response`
- Frozen N29 science reference: `327c58e2684398ba7bc11205865f8222066c3539`
- Last valid upstream gate: `GATE-EXP001-P0 = PASS`

## Phase-1 objective

Generate production-quality constrained-equilibrium force response at the single preregistered reference state, without inspecting any scientific driven-validation trajectory.

The output of this phase is a **frozen equilibrium predictor artifact**, not a conclusion about scalar, tensor, or memory sufficiency.

## Current status

`GATE-PHASE1-PRODUCTION-FREEZE = PARTIAL`.

The production protocol below is frozen technically, but scientific execution remains human-gated until the user approves this exact production cost and estimator policy.

## Files

- `DESIGN-02_PHASE1_PRODUCTION_FREEZE.md`
- `PREDICTOR_ARTIFACT_SCHEMA.json`
- `GATE_PHASE1_PRODUCTION_FREEZE.md`
- `DEC-002_phase1_freeze_authorization.json`

## Forbidden in Phase-1

- prescribed oscillatory validation;
- any fitting to driven data;
- M0/M1/M3 winner selection;
- corner/edge interpretation;
- winding/ratchet transport;
- new-physics language.

If the equilibrium estimator does not converge under the frozen extension rules, Phase-1 stops rather than using driven data to repair it.
