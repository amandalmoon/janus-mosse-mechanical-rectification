# Janus MoSSe Mechanical Rectification

Research OS archive and current submission/reproducibility workspace for a computational study of directional depinning and vector mode locking in finite Janus MoSSe contacts.

## Repository map

- `submission/acs-nano/` — current ACS Nano manuscript, SI, TOC artwork, cover-letter materials, and submission QA.
- `figures/publication/` — current publication figures, source, manifests, and figure QA.
- `reproducibility/` — current reproducibility release in expanded form.
- `research-os/` — stage-by-stage simulations, numerical audits, statistics, robustness checks, and reports.
- `archive/legacy/` — superseded but provenance-relevant versions.
- `provenance/source-inputs/` — source inputs used during reconstruction/audit.
- `provenance/migration/` — inventory, duplicate ledger, migration decisions, and SHA-256 provenance.

## Storage policy

Redundant ZIP bundles are intentionally not committed. Their SHA-256 values and source paths are retained in `provenance/migration/EXCLUDED_BUNDLES.csv`; expanded contents are committed instead. Unique members found only inside historical ZIPs were extracted under `archive/legacy/bundle-extracted/`.

## Scientific authority

Use the current files under `submission/acs-nano/`, `figures/publication/`, and `reproducibility/` as the present-state artifacts. Files under `archive/legacy/` are not current scientific authority.
