# Manuscript Integrity Gate

## Scope

This gate checks whether the current GitHub repository can independently support the manuscript/SI provenance claims before the project advances to final ACS Nano submission QA.

## FACT

- The current `main` branch contains only:
  - `.gitattributes`
  - `.gitignore`
  - `README.md`
  - `docs/RESEARCH_OS_PIPELINE.md`
- The repository README describes `archive/`, `reproducibility/`, and `submission/` as repository layout components, but those directories are not present on the current `main` tree.
- The manuscript states that scripts, raw/summary CSV and JSON files, environment information, Gate reports, and manuscript/SI sources are retained with the submission materials.
- The Supporting Information states that the accompanying materials retain the canonical unguided rigid-model release, Gate-level audits, nonlinear VFF source, fresh linear/VFF tables, joint-vector thermal bootstrap tables, and manuscript/SI sources.

## INFERENCE

The manuscript/SI can be internally consistent while the repository still fails a provenance gate. Repository-level reproducibility cannot be marked VERIFIED until the canonical evidence package, or a stable external deposition linked by immutable identifier, is present and traceable.

## SPECULATION

None.

## Document-level consistency status

The current manuscript and SI agree on the central reported values checked in this gate:

| Claim | Main manuscript | Supporting Information | Status |
|---|---|---|---|
| Prepared N=127, theta=1.5 deg thresholds | F_c,+*=3.071135; F_c,-*=1.258672 | same | SUPPORTED |
| Matched symmetrized global thresholds | 1.767700 / 1.767700; split ~6.6e-10 | same | SUPPORTED |
| Exact inversion threshold swap | 1.258672 / 3.071135 | same | SUPPORTED |
| Compact-contact similarity | hex N<=1261; disk N<=931; max within-family error <0.1% | same | SUPPORTED |
| Triangular registry switches | 2.921278 deg (20 deg cut); 2.847233 deg (25 deg cut) | same | SUPPORTED |
| Deterministic locking | 91/91 sampled points cycle-resolved integer winding | same | SUPPORTED |
| Thermal current at T*=0.70 | pooled <u,v>=(0.03700,-0.07645); zero vector excluded | same | SUPPORTED |
| Linear FEM at theta=1.5 deg | 2.934302 / 1.190210; rho=0.422860 | same | SUPPORTED |
| Nonlinear VFF at theta=1.5 deg | 2.935400 / 1.190479; rho=0.422921 | same | SUPPORTED |

These statuses mean document-to-document consistency only. They do not substitute for raw execution provenance.

## BLOCKERS

1. Canonical reproducibility artifacts are not committed on the current repository tree.
2. The README currently describes repository layout and completed audit state more strongly than the repository contents demonstrate.
3. No immutable external repository DOI is yet recorded.
4. No machine-readable evidence manifest currently maps frozen manuscript claims to code version, data files, environment, and execution outputs.

## NEXT GATE

`REPOSITORY PROVENANCE GATE`

Pass conditions:

- canonical code and data package is present in-repo or linked to an immutable external deposition;
- each evidence bundle records provenance class, code commit, environment, seed/parameters where applicable, and checksums;
- claim-evidence matrix points to concrete files, not prose-only summaries;
- rejected/superseded claims remain archived rather than overwritten;
- a clean replay can be associated with an exact commit and evidence manifest.

## NEXT ACTION

Populate the evidence package and convert the claim-evidence matrix from document-level support to file-level traceability.
