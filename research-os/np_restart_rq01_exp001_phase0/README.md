# NP-RESTART RQ-01 / EXP-001 Phase-0

This directory is a **separate research branch archive** for the equilibrium-response restart project. It is intentionally isolated from the frozen N29 manuscript/results.

## Branch status

- Git branch: `research/exp001-phase0-equilibrium-response`
- Branch created from repository `main` at: `81e984fadbf3580112557e4e4a3ec7fc81e6f722`
- Frozen N29 science reference commit: `327c58e2684398ba7bc11205865f8222066c3539`
- N29 static VFF source: `research-os/janus_n8_gate/vff_reconstruction.py`
- N29 conservative GSFE source: `reproducibility/Janus_MoSSe_Current_ReproducibilityRelease_v2/source/janus_fourier_landscapes_v12.py`

The branch head is used only as a storage/work branch. Scientific inputs that inherit N29 physics must be traced to the frozen science commit above rather than silently inheriting later repository changes.

## Frozen first research objective

**RQ-01.** Under a declared two-dimensional finite-contact model and bath condition, can pre-sliding equilibrium response predict the energy dissipated by a small prescribed oscillatory displacement, and what is the minimal reduced dissipative model required?

The first execution branch is **EXP-001 Phase-0 only**:

1. reproduce the frozen N29 VFF static baseline;
2. verify the COM/internal mass transform;
3. verify internal Langevin fluctuation-dissipation behavior;
4. run a constrained-equilibrium pilot only to estimate correlation time and production length;
5. stop before any driven validation trajectory is inspected;
6. freeze predictor-generation settings before proceeding.

## Explicit exclusions

This branch does **not** claim or search for:
- corner-to-edge crossover;
- free-running winding or ratchet transport;
- a new friction law;
- non-Markovianity merely because scalar damping fails;
- Kelvin/Hz/nN calibration;
- a revision of any frozen N29 scientific result.

## Files

- `THEORY-01_equilibrium_response_model.md` — frozen theory contract and M0→M3 hierarchy.
- `DESIGN-01_preregistered_small_oscillation_test.md` — preregistered discovery/confirmation protocol.
- `EXP-001_PHASE0_PLAN.md` — implementation-only Phase-0 execution contract.
- `GATE_REPORT.md` — current Research OS gate state.
- `research_state.json` — durable research state.
- `artifact_registry.json` — lineage/status for this branch.
- `DEC-001_exp001_phase0_approval.json` — explicit human approval record.

No driven result should be committed under this directory before EXP-001 Phase-0 passes and predictor settings are frozen.
