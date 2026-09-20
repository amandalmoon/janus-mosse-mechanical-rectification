# ACS Nano N27 Submission Audit

**Audit date:** 2026-09-20  
**Manuscript type:** Article  
**Submission stage:** Initial submission  
**Status:** **NOT_READY — venue/package blockers only**  
**Scientific freeze:** PASS; 0 open scientific BLOCKER; 0 open scientific MAJOR; 0 dirty scientific artifacts.

## Current official rule verification

- ACS Nano Author Guidelines: https://researcher-resources.acs.org/publish/author_guidelines?coden=ancac3
- Author Guidelines page: last updated July 03, 2026
- ACS Nano Author Checklist: https://pubsapp.acs.org/paragonplus/submission/ancac3/ancac3_checklist.pdf
- Verified on: 2026-09-20
- Verification status: CURRENT
- Bundled snapshot date: 2026-09-19
- Material rule deltas from bundled snapshot: none identified.

## Assets already passed

- Scientific freeze: PASS.
- Final DOCX render QA: PASS, 20 pages visually inspected.
- DOCX SHA-256: `ce16d631ff481b0095131c7a5c448ba27b4002ad7f47a0fa0822037454296829`.
- Immutable source identifier: Git commit `327c58e2684398ba7bc11205865f8222066c3539`.
- Reproducibility bundle SHA-256: `7436e985937e7cc9e2a5cac1f58affbd3e955dd2763eca9d69324c1fd0af34a8`.
- Abstract: 208 words, within the 250-word Article limit; no references; no novelty claim.
- Introduction: 587 words, within the general 1000-word limit.
- Current title: 13 words and contains neither “First” nor “Novel”.
- Figures 1–7: final-size 7-inch graphics, Arial lettering, minimum text >=7.0 pt, captions present, and cited in numerical order.
- Figures 2–7: minimum vector line width >=0.5 pt.
- Public content-addressed research snapshot exists.

## Blocking venue/package findings

### B1 — Title contains an unsupported acronym
Current title begins **GSFE-Anchored**. ACS Nano says titles should not contain acronyms/abbreviations outside limited common exceptions such as RNA, DNA, 2D, and 3D.

Required fix: spell out GSFE without changing scientific meaning.

Candidate: **Generalized Stacking-Fault Energy-Anchored Prepared-State Mechanical Rectification and Vector Mode Locking in Finite Janus MoSSe Contacts** (15 words).

### B2 — Author/title-page metadata absent
The manuscript contains no author list, affiliations, corresponding-author designation/contact, or e-mail address.

Required fix: insert exact author names/order, affiliations, and corresponding-author contact supplied by the authors.

### B3 — Keywords exceed Article limit
Current keyword count: 8. ACS Nano specifies 5–7 keywords for Articles and describes them as lowercase keywords.

Required fix: reduce to 5–7. Candidate:
`janus MoSSe; mechanical rectification; depinning; generalized stacking-fault energy; finite-contact scaling; vector mode locking; in-plane relaxation`

### B4 — Introduction heading is present
Current heading: `1. Introduction`.

Required fix: remove the Introduction heading while retaining the introductory text.

### B5 — Sections are numbered
ACS Nano Article sections are not numbered.

Required fix: remove numbering from Methods, Results, Discussion, Conclusions, and Data/Code headings.

### B6 — Methods is not the last text section
Current order places Methods before Results. ACS Nano requires Methods/Experimental Section as the last text section.

Required fix: move the complete Methods section after Conclusions and before back matter, without changing scientific content; then rerun equation/cross-reference/render QA.

### B7 — TOC graphic is missing
ACS Nano Articles require an original author-created graphical TOC entry.

Current rule: <=9.0 cm wide x 4.0 cm high, TIF or EPS, >=300 dpi at final size, minimal text, no logos, no licensed stock/adapted third-party art.

### B8 — Figure 1 contains a 0.45 pt vector line
Exact N25 EPS inspection found minimum `setlinewidth = 0.45 pt` in Figure 1. The checklist requires lines >=0.5 pt at final published size. Figures 2–7 meet or exceed 0.5 pt.

Required fix: update Figure 1 source, regenerate coordinated exports, rerun final-size/visual QA, and mark the set `VENUE_HANDOFF_READY`.

### B9 — Cover letter is absent
ACS Nano requires a cover letter for every manuscript submission.

Required content: manuscript title; corresponding-author name/contact; all coauthors; ACS Nano fit statement; SI/Review-Only Material description; prior ACS Nano editor discussion when applicable; preprint disclosure when applicable. The journal also urges 6–8 competent reviewer suggestions who are not at the same institution as any author.

## Conservative final-package fixes

### C1 — Citation display style
The frozen manuscript uses bracketed numeric citations. The checklist specifies superscript citations without brackets and after punctuation. Initial Fast Format also permits references in any complete, consistent style. Conservative final-package action: convert citations to ACS Nano superscript style in the venue derivative.

### C2 — Reference journal style
References are complete and numbered in citation order, but the final style pass should normalize title capitalization, CASSI journal abbreviations, punctuation, full page ranges, and >20-author handling.

### C3 — Data Availability metadata
Update the venue derivative to cite the public repository and immutable commit `327c58e2684398ba7bc11205865f8222066c3539`. ACS Nano applies ACS Research Data Policy Level 1 and encourages public sharing plus a Data Availability Statement.

### C4 — Acknowledgments/funding metadata
No Acknowledgments section is present. This is not automatically a defect if nothing applies; any funding, technical assistance, or required grants must be supplied by the authors before final submission.

### C5 — Supporting Information
No separate SI file is currently registered. SI is not mandatory merely because the study is computational. If SI is added, it must be uploaded separately and described in the manuscript. Current official sources contain inconsistent wording about SI paragraph order relative to Acknowledgments, so the submission-system instruction should be rechecked when SI is actually supplied.

## Figure venue audit

| Figure | Arial | Min text | Min line | EPS available | Final size | Venue finding |
|---|---:|---:|---:|---:|---:|---|
| FIG-01 | PASS | 7.0 pt | **0.45 pt** | PASS | 177.8 x 80.0 mm | **FAIL line-width gate** |
| FIG-02 | PASS | 7.2 pt | 0.60 pt | PASS | 177.8 x 116.0 mm | PASS |
| FIG-03 | PASS | 7.2 pt | 0.50 pt | PASS | 177.8 x 114.0 mm | PASS |
| FIG-04 | PASS | 7.2 pt | 0.50 pt | PASS | 177.8 x 116.0 mm | PASS |
| FIG-05 | PASS | 7.2 pt | 0.60 pt | PASS | 177.8 x 116.0 mm | PASS |
| FIG-06 | PASS | 7.2 pt | 0.50 pt | PASS | 177.8 x 124.0 mm | PASS |
| FIG-07 | PASS | 7.2 pt | 0.60 pt | PASS | 177.8 x 116.0 mm | PASS |

## Deterministic manifest audit

The official ACS Nano submission-manifest audit returned:
- status: `NOT_READY`
- structured blockers: 7
- structured major findings: 1

The structured findings cover keyword count/case, Introduction heading, section numbering, Methods position, missing TOC, figure-set venue gate, and Figure 1 line width. Manual current-rule review additionally identifies the unsupported title acronym, missing author/title-page metadata, and required cover letter.

## Final venue status

**ACS NANO SUBMISSION STATUS: NOT_READY**

This is entirely a **venue/package** result. Scientific freeze remains valid and is not reopened.

### Required repair order
1. Fix Figure 1 minimum line width and rerun Figure 1/final DOCX QA.
2. Create a venue-only manuscript derivative: spell out the title acronym, reduce keywords, remove heading/section numbering, move Methods last, normalize citation/reference styling, and update the Data Availability identifier.
3. Add exact author/affiliation/corresponding-author metadata, original TOC graphic, and required cover letter; rerun the deterministic ACS Nano manifest and page-by-page render audit.

Final submission remains a separate human gate.
