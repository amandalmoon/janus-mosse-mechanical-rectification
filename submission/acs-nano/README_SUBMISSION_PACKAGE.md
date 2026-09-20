# ACS Nano initial-submission package - Janus MoSSe

This folder is the N19 venue-layer package prepared from the scientifically frozen manuscript and N18 figure set.

## Core files

- `ACS_Nano_Initial_Submission_Manuscript.docx` - current initial-submission manuscript.
- `ACS_Nano_Initial_Submission_Manuscript.pdf` - visual-QA render.
- `ACS_Nano_Supporting_Information.docx` - separate SI.
- `ACS_Nano_Supporting_Information.pdf` - visual-QA render.
- `cover_letter/ACS_Nano_Cover_Letter_DRAFT.docx` - one-page draft with author metadata placeholders.
- `toc/ACS_Nano_TOC_Graphic.tif` and `.eps` - graphical TOC.
- `artwork/figures/` - Figures 1-6 in editable/vector and raster derivatives.
- `../../reproducibility/Janus_MoSSe_Current_ReproducibilityRelease_v2/` - canonical expanded reproducibility release.
- GitHub Actions workflow `Submission Evidence Package` - builds `Janus_MoSSe_Current_ReproducibilityRelease_v2.zip`, verifies its SHA-256, extracts it into a fresh directory, and reruns the current validators before publishing the ZIP as a workflow artifact.
- `SUBMISSION_METADATA_REQUIRED.md` - mandatory remaining author inputs.
- `qa/ACS_NANO_INITIAL_SUBMISSION_AUDIT_REPORT.md` - final N19 audit.
- `qa/submission_manifest.json` and `qa/deterministic_submission_audit.json` - structured venue audit.

## Reproducibility-delivery policy

The repository intentionally does **not** commit redundant ZIP bundles. The expanded release is the version-controlled scientific authority. A submission-ready ZIP is generated from the exact checked-out release by `.github/workflows/submission-evidence-package.yml`, then replayed from a fresh extraction before it is exposed as a downloadable GitHub Actions artifact.

This avoids a stale committed ZIP diverging from the current expanded release while still producing the single-file package required for submission or external handoff.

## Current gate

`NOT_READY - AUTHOR/METADATA BLOCKERS ONLY`

The scientific, document-structure, and reproducibility-integrity gates are complete. Do not upload until the fields in `SUBMISSION_METADATA_REQUIRED.md` are supplied/confirmed by the authors and inserted into the manuscript/cover letter/submission system where applicable.

## Final-artwork note

The current environment lacks literal Arial. Figures are scientifically and visually approved but local EPS/TIFF derivatives use Arimo fallback. Re-export in literal Arial (or verified outlined Arial) before revised-manuscript/final-artwork delivery.
