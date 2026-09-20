# Submission Evidence Artifact Gate

Status: **PASS**

The repository keeps the reproducibility release expanded under version control rather than committing redundant ZIP bundles. The submission evidence ZIP is therefore a generated artifact whose source is the canonical expanded release.

## Verified deterministic build

GitHub Actions workflow: `Submission Evidence Package`

Verified run: **35480708622**  
Verified head: `b9d5022596fd70f882616935bcf7d5667dca03b1`  
Artifact ID: **10594974375**  
Artifact name: `Janus_MoSSe_Current_ReproducibilityRelease_v2`  
Inner submission ZIP SHA-256: `4e4eabe2f1b171b620a97a42790fffb590adc609396bdb1b5f29f9ff1b7a2ec5`  
GitHub artifact-wrapper digest: `sha256:232e54e7382aae4598216157887ec8274185f99f144001de8f30023799d8c9bd`  
Artifact retention through: **2026-12-19T01:10:41Z**

## Gate evidence

The successful workflow:

1. checked out Git LFS payloads;
2. passed `validate_release.py`;
3. passed `validate_canonical_baseline.py`;
4. recomputed the stationary thermal statistics from the shipped raw trajectory aggregates;
5. passed `pre_submission_integrity_check.py`;
6. passed the full 111-entry `SHA256SUMS.txt` verification;
7. verified that the manuscript and SI LFS objects were materialized rather than pointer files;
8. generated the ZIP with sorted entries, fixed ZIP timestamps and fixed permissions;
9. extracted the ZIP into a fresh directory;
10. reran all current validators and the SHA-256 manifest check from that extraction;
11. published the ZIP plus its SHA-256 sidecar as a GitHub Actions artifact.

The earlier non-deterministic packaging run 35480636437 is superseded by this fixed-timestamp build.

## Interpretation

**FACT:** the exact expanded release has passed both source-tree validation and fresh-extraction replay, and a single-file submission artifact is available.

**INFERENCE:** no scientific-result regression was introduced by the delivery-layer repair.

**SPECULATION:** none.

This closes the reproducibility-delivery layer. The remaining N19 blockers are author/administrative metadata and declarations, not scientific or reproducibility evidence.
