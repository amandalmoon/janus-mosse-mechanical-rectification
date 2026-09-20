# Janus MoSSe Repository Migration Inventory

**Destination:** `amandalmoon/janus-mosse-mechanical-rectification`  
**GitHub writes performed:** **NO**  
**Generated:** 2026-09-19 23:07 KST

## Scope

This inventory scans the project artifacts currently materialized in the working environment from the Janus MoSSe Research OS run, including gate outputs, code, CSV/JSON evidence, manuscript/SI versions, reproducibility releases, publication figures, and ACS Nano submission artifacts. QA page renders and exact byte-for-byte duplicates are inventoried but excluded from migration by default.

## Counts

- Physical files scanned: **1656**
- KEEP: **567**
- ARCHIVE: **46**
- EXCLUDE: **1043**
- Exact-duplicate rows excluded: **653**
- Ephemeral QA/render rows excluded: **390**
- SHA-256 duplicate groups: **271**
- Non-identical target-path collisions: **0**

## Proposed Repository Layout

```text
submission/acs-nano/      current ACS Nano manuscript, SI, TOC, cover letter, QA
figures/publication/      current figures, source, manifests, figure QA
reproducibility/          current reproducibility release and rerun evidence
research-os/              stage-by-stage code/data/audits
archive/legacy/           superseded versions retained for provenance
provenance/source-inputs/ original source inputs
```

## Classification Policy

- **CURRENT / CURRENT_BUNDLE:** authoritative present-state artifacts.
- **SUPPORTING:** evidence, data, code, and audit artifacts worth preserving.
- **LEGACY:** superseded but scientifically/provenance-relevant versions; migrate under `archive/legacy/`.
- **ARCHIVE_BUNDLE:** historical ZIP bundle; preserve under archive unless exact duplicate.
- **EXACT_DUPLICATE:** same SHA-256 as a preferred copy; do not upload twice.
- **EPHEMERAL_QA:** rendered page PNGs, temporary equation renders, and similar regeneration-only files; do not upload.

## Required Artifact Checks

- [x] Current ACS manuscript DOCX
- [x] Current ACS SI DOCX
- [x] TOC EPS
- [x] TOC TIF
- [x] Current reproducibility bundle
- [x] Publication figure audit
- [x] Five Reviewer audit
- [x] Short Red Team closure
- [x] Publication Figure 1
- [x] Publication Figure 2
- [x] Publication Figure 3
- [x] Publication Figure 4
- [x] Publication Figure 5
- [x] Publication Figure 6

## Known Pending Items (not file loss)

1. ACS submission metadata still requires user-supplied author/contact/submission-system fields; do not infer them.
2. N18 figure QA recorded Arial fallback in the current environment; final ACS artwork derivatives should be re-exported in an Arial-capable environment before submission.

## Review Before Upload

Use `REPOSITORY_MIGRATION_MANIFEST.csv` as the authoritative proposed action list. Rows marked `KEEP` or `ARCHIVE` are upload candidates. Rows marked `EXCLUDE` remain documented in the full inventory but should not be committed. Check `MIGRATION_REVIEW_ISSUES.csv` before any GitHub write.
