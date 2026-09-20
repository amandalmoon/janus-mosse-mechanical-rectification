# Submission Evidence Artifact Gate

Status: **PENDING CI**

This gate exists because the repository storage policy keeps the reproducibility release expanded rather than committing redundant ZIP bundles.

The `Submission Evidence Package` workflow must:

1. checkout Git LFS payloads;
2. pass the current release, canonical baseline, stationary thermal, and pre-submission integrity checks;
3. verify the release SHA-256 manifest;
4. build `Janus_MoSSe_Current_ReproducibilityRelease_v2.zip` without generated `__pycache__` or `.pyc` artifacts;
5. extract that ZIP into a fresh directory;
6. rerun all current validators and the SHA-256 manifest check from the extracted package;
7. publish the ZIP and its SHA-256 sidecar as a GitHub Actions artifact.

This file is updated to PASS only after an exact-head workflow run succeeds and the artifact is visible through the GitHub Actions API.
