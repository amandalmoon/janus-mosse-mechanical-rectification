# N27 Immutable Reproducibility Release Manifest

**Release label:** N27-SCIENTIFIC-FREEZE-2026-09-20  
**Release type:** content-addressed Git commit + SHA-256-verified reproducibility bundle  
**Scientific freeze:** PASS

## Frozen scientific authorities

- Frozen manuscript Git blob: `2ee160a40e07bb2d51be6845e780c7f349bc4386`
- N25 figure authority commit: `4060d017a50c6387de45377621d9232529e7e4ad`
- N25 final figure artifact ID: `10602481122`
- N25 artifact digest: `sha256:f56ddfc07e9951bb15cd7206de626e4d0d7287a832f1a00dea6ca83a15e3a195`
- Five Reviewer re-audit: `N27_FIVE_REVIEWER_REAUDIT_BOUNDARY.md`
- Scientific freeze record: `N27_SCIENTIFIC_FREEZE.md`

## Final manuscript assembly

- File: `Janus_MoSSe_N27_ScientificFreeze_Final.docx`
- SHA-256: `ce16d631ff481b0095131c7a5c448ba27b4002ad7f47a0fa0822037454296829`
- QA render PDF SHA-256: `a60ce011a289c272c7865483f2938eeb27eaaab082108b5df5272453bff90af6`
- Pages: 20
- Figures: 7
- Word-native OMML objects: 356
- Accessibility audit: 0 high / 0 medium / 0 low

## Identifier policy

The immutable identifier for this release is the Git commit SHA that creates this manifest. Git commit identity is content-addressed and cannot be changed without producing a different identifier.

A DOI has **not** been minted. No DOI should be inserted into the manuscript unless an external archival service actually issues one.

## Bundle contract

The reproducibility bundle assembled from this release contains:

1. the repository source archive at the immutable release commit;
2. the final frozen DOCX above;
3. the exact N25 final figure ZIP artifact;
4. the QA render PDF;
5. a machine-readable SHA-256 checksum file;
6. a release README describing provenance and scope.

The bundle SHA-256 is computed after packaging and is recorded in the downstream Research OS release record.

## Scientific scope

This release freezes the manuscript as a published-GSFE-anchored finite-contact model study. It does not add or imply full three-dimensional material validation, experimental calibration, or a physical polarity-reversal law.
