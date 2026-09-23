# NP-RESTART RQ-01 / EXP-001

This directory is a **separate research branch archive** for the equilibrium-response restart project. It is intentionally isolated from the frozen N29 manuscript/results.

## Branch status

- Git branch: `research/exp001-phase0-equilibrium-response`
- Branch created from repository `main` at: `81e984fadbf3580112557e4e4a3ec7fc81e6f722`
- Frozen N29 science reference commit: `327c58e2684398ba7bc11205865f8222066c3539`
- N29 static VFF source: `research-os/janus_n8_gate/vff_reconstruction.py`
- N29 conservative GSFE source: `reproducibility/Janus_MoSSe_Current_ReproducibilityRelease_v2/source/janus_fourier_landscapes_v12.py`

The branch retains byte-identical copies of the frozen VFF and GSFE files above. Scientific inputs that inherit N29 physics are traced to the frozen commit rather than silently inheriting later repository changes.

## Frozen first research objective

**RQ-01.** Under a declared two-dimensional finite-contact model and bath condition, can pre-sliding equilibrium response predict the energy dissipated by a small prescribed oscillatory displacement, and what is the minimal reduced dissipative model required?

## EXP-001 Phase-0 status

**PASS.**

Completed:

1. frozen N29 nonlinear VFF static baseline reproduction;
2. COM/internal mass-transform verification;
3. internal-only Langevin FDT verification;
4. constrained-equilibrium correlation pilot;
5. implementation-only first-law energy-accounting check.

Phase-0 produced **no scientific driven-validation result** and no M0/M1/M2/M3 model-selection conclusion.

See:

- `EXP-001_PHASE0_EXECUTION_REPORT.md`
- `results/EXP-001_P0_GATE.json`
- `results/EXP-001_P0_PROVENANCE.json`
- `source/exp001_phase0_repro.py`

## Important pilot finding

The constrained force ACF contains oscillatory tails/recurrences. The planning cutoff `tau_mem = 9.768` is therefore used only to set a conservative production-length scale. It is **not** evidence that the response is single-exponential, Markovian, or non-Markovian.

Under the preregistered `>=200 tau` rule, Phase-1 production would require at least approximately `1953.6` reduced time units per production trajectory unless a stricter convergence-based rule is frozen instead.

## Explicit exclusions

This branch does **not** currently claim or search for:

- corner-to-edge crossover;
- free-running winding or ratchet transport;
- a new friction law;
- non-Markovianity merely because scalar damping fails;
- Kelvin/Hz/nN calibration;
- a revision of any frozen N29 scientific result.

## Current gate

Phase-0 is complete. **Phase-1 production remains human-gated.**

Before Phase-1, freeze:

1. production seed list / trajectory count;
2. production length;
3. ACF/window and recurrence-tail policy;
4. response/predictor artifact schema and uncertainty calculation;
5. frequency-grid rule.

No scientific driven validation is authorized before that freeze.
