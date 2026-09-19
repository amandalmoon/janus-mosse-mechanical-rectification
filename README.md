# Janus MoSSe Mechanical Rectification

Research OS archive for the Janus MoSSe finite-contact mechanical rectification project.

This repository preserves the scientific workflow, verification gates, manuscript history, reproducibility artifacts, publication figures, and ACS Nano submission preparation produced through the Research OS pipeline.

## Current status

- Scientific layer: passed through citation audit, Red Team, Five Reviewer audit, targeted revision, and reproducibility clean replay.
- Figure layer: publication-figure audit completed and handed off to ACS Nano venue preparation.
- Submission layer: ACS Nano initial submission package prepared, with final submission metadata still requiring author-side completion where applicable.

## Repository layout

- `archive/`: chronological gate bundles and provenance snapshots.
- `reproducibility/`: canonical current reproducibility release.
- `submission/`: current ACS Nano initial-submission artifacts.
- `docs/`: project-level provenance and status notes.

## Important scope notes

The project uses the published Janus MoSSe generalized stacking-fault-energy model as the conservative material input, then studies finite-contact prepared-state depinning, symmetry controls, size/shape scaling, boundary-registry competition, deterministic vector mode locking, thermal stationary drift, and in-plane relaxation checks.

The dynamical results are reduced-model results under declared dimensionless parameters and loading protocols; they are not calibrated experimental predictions in SI units. The two in-plane relaxation representations share the same GSFE and target elastic constants and are therefore cross-representation checks, not fully independent atomistic validation.

## Provenance

Current canonical artifacts are retained together with historical audit bundles so rejected or superseded claims remain traceable rather than silently disappearing.
