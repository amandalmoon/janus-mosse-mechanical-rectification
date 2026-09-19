# Janus MoSSe Mechanical Rectification

Research OS archive for the Janus MoSSe finite-contact mechanical rectification project.

This repository is intended to preserve the scientific workflow, verification gates, manuscript history, reproducibility artifacts, publication figures, and ACS Nano submission preparation produced through the Research OS pipeline.

## Current status

- Manuscript stage: manuscript and Supporting Information are in the submission-writing/audit stage.
- Document consistency: central numerical claims checked so far are consistent between the current manuscript and SI.
- Repository provenance gate: **BLOCKED**. The canonical execution/reproducibility evidence package described by the manuscript/SI is not yet present on the current repository tree.
- Submission metadata: author-side metadata and final deposition identifiers remain incomplete where applicable.

See:
- `docs/MANUSCRIPT_INTEGRITY_GATE.md`
- `docs/CLAIM_EVIDENCE_MATRIX.md`
- `docs/REPOSITORY_EVIDENCE_MANIFEST.md`
- `docs/RESEARCH_OS_PIPELINE.md`

## Intended repository layout

- `archive/`: chronological gate bundles and provenance snapshots.
- `reproducibility/`: canonical current reproducibility release.
- `submission/`: current ACS Nano initial-submission artifacts.
- `docs/`: project-level provenance and status notes.

The first three directories are intended targets and must not be treated as present evidence until populated or replaced by an immutable external deposition reference.

## Important scope notes

The project uses the published Janus MoSSe generalized stacking-fault-energy model as the conservative material input, then studies finite-contact prepared-state depinning, symmetry controls, size/shape scaling, boundary-registry competition, deterministic vector mode locking, thermal stationary drift, and in-plane relaxation checks.

The dynamical results are reduced-model results under declared dimensionless parameters and loading protocols; they are not calibrated experimental predictions in SI units. The two in-plane relaxation representations share the same GSFE and target elastic constants and are therefore cross-representation checks, not fully independent atomistic validation.

## Provenance rule

Rejected and superseded claims should remain traceable rather than being silently deleted. A gate may be marked passed only when the corresponding evidence artifact is committed or immutably linked.
