# N19R Manuscript Integration Report

## Scope

This gate integrates the N18R `PUBLICATION_READY` Figures 1-6 into the exact current ACS Nano manuscript and applies the wording correction exposed by the stricter Figure 5 contract.

## FACT

- N18R Figures 1-6 passed the strict publication-figure benchmark and ACS Nano venue handoff.
- The exact current repository manuscript DOCX has SHA-256 `b33049e120895ac4368c291fbfac3e3f3eb28f8b280728e2f8f7bc86d6e7862f`.
- The manuscript integration was performed from that exact input.
- Figures 1-6 were replaced with the approved N18R venue-render artwork.
- Captions were replaced with the approved N18R manifest captions.
- Three instances of overstrong Figure-5-related wording were corrected so that the 91-point map is described as **integer winding states including pinned and transporting states**, rather than transport at every sampled point.
- The integrated manuscript DOCX SHA-256 is `c93a3db7bd31c18e4ff0ffdb45d65e0ff39a225c924572a400a17f696967343b`.
- The integrated manuscript was rendered to 16 pages and every page was visually inspected. No clipping, overlap, missing figures, broken captions, broken tables, or missing glyphs were observed.
- The embedded manuscript figure width is 6.40 in. This preserves the 16-page layout while keeping the 7 pt N18R figure lettering above the ACS Nano 6 pt minimum after manuscript embedding. The standalone venue artwork remains at the approved 177.8 mm final size.
- A refreshed reproducibility release was constructed with the integrated manuscript and N18R manuscript-facing figures. The current-release validator, canonical baseline validator, stationary thermal recomputation, pre-submission integrity check, and all 111 SHA-256 manifest entries pass.
- The refreshed release was then packed deterministically and revalidated from a fresh extraction.
- Refreshed release ZIP SHA-256: `0fe30e220810eb31790db189d9144457d9c79a5e720ecff7f0345698d617644b`.

## INFERENCE

The N18R visual redesign and manuscript integration do not introduce a scientific-result regression. The one substantive prose change narrows the Figure 5 statement to the evidence actually visible in the winding map.

## SPECULATION

None.

## Repository binary handoff

The integration script is committed here so the transformation is reproducible. The generated DOCX, PDF, and refreshed ZIP are binary artifacts and must be synchronized to the Git LFS/submission-delivery layer before the repository itself can be called fully frozen at N19R.

Until that binary synchronization is completed, the repository-side N19R gate remains **HANDOFF_PENDING**, even though the locally generated artifacts and clean replay pass.

## Gate

**LOCAL_ARTIFACT_PASS / REPOSITORY_LFS_HANDOFF_PENDING**

## Next action

1. synchronize the integrated manuscript DOCX/PDF and refreshed reproducibility ZIP to the submission/LFS delivery layer;
2. rerun the deterministic submission-package audit;
3. complete author/administrative metadata;
4. perform the final ACS Nano submission audit and package freeze.
