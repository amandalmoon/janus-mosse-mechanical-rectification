# N20 Pre-Submission Reproducibility Integrity Recheck

## Trigger

A fresh read of the migrated repository was performed before accepting the N19 statement that only author metadata remained.

The uploaded manuscript PDF has SHA-256 `0ab24f532e49886c0145461bc68ecf71fde8d8efbeecc16bd3560810779348df`, exactly matching the Git LFS object recorded for the current N19 manuscript PDF. The audit therefore targets the actual current manuscript/package, not an older draft.

## Findings

### FACT

1. The current manuscript states that the 2024 Angeli Erratum does not change the GSFE Fourier coefficients or conjugate phase pairing.
2. The current reproducibility release still contained an older source comment claiming that the phase convention was corrected by the 2024 Erratum.
3. `config/canonical_unguided.json` repeated the same stale Erratum attribution.
4. The release contained two copies of a retired thermal script using `BURN=10; MEAS=10`, while the manuscript-facing thermal contract is 60 burn + 100 measured cycles.
5. `source/canonical_analysis_v17.py` defaulted to legacy `config/production.json` (k_perp=25) while writing to `data/canonical`, creating a risk of overwriting manuscript-facing unguided canonical outputs if run.
6. Historical provenance scripts retain original absolute working paths. They are useful provenance but are not clean-run entry points.

### INFERENCE

The scientific results are not invalidated by these findings: the corrected GSFE source differs in provenance text, not numerical coefficients, and the current validator already checks the 60/100 stationary thermal outputs. However, the repository did not yet meet the stricter Research OS requirement that the current evidence package be unambiguous and safely reproducible.

### SPECULATION

None.

## Repairs applied

- replaced the stale GSFE source commentary with the previously audited provenance-corrected N11 source;
- corrected the canonical config provenance string;
- isolated legacy guided v17 outputs under `data/legacy_guided_v17/`;
- explicitly labeled the old 10/10 thermal scripts as retired and redirected the active-folder copy to `data/legacy_thermal_10x10/`;
- documented the distinction between current clean checks and original-path provenance scripts;
- added `pre_submission_integrity_check.py`;
- restored `manuscript/Janus_MoSSe_Current_SupplementaryInformation.docx` as the exact Git LFS object already referenced by the release manifest (SHA-256 `04a5753b71bad758080496410969da740673a50b442fb50ed268a9257ad52f91`);
- removed generated `__pycache__` entries and accidental duplicate path forms from the release manifest;
- regenerated the release SHA-256 manifest;
- added the GitHub Actions `Reproducibility Gate` workflow.

## Clean execution evidence

The first CI execution (run 35480243674) established that all scientific validators passed but exposed a manifest/package defect: the SI file was absent, generated `__pycache__` files were incorrectly listed, and changed text files had stale/duplicate checksum entries.

After repairing those packaging defects, GitHub Actions run **35480474546** at exact branch head `155535d60b8981853c0b76561b0d19ddf6722112` completed successfully:

- `validate_release.py` → **CURRENT RELEASE VALIDATION: PASS**
- `validate_canonical_baseline.py` → **CANONICAL UNGUIDED BASELINE VALIDATION: PASS**
- `recompute_stationary_thermal.py` → completed successfully from the shipped raw trajectory aggregates
- `pre_submission_integrity_check.py` → **PRE-SUBMISSION INTEGRITY CHECK: PASS**
- `sha256sum -c SHA256SUMS.txt` → **PASS** for the full 111-entry release manifest

The successful clean run uses the repository checkout with Git LFS materialization and the pinned scientific Python requirements.

## Gate

**PASS**

N20 is closed. No scientific-result regression was detected. The current reproducibility release is internally consistent, the canonical unguided evidence is protected from the legacy guided pipeline, the current stationary thermal contract is machine-checked, the SI is present, and the release checksum manifest verifies cleanly.

The workflow therefore returns to the **N19 author-metadata completion gate**, followed by the final ACS Nano submission audit and package freeze.
