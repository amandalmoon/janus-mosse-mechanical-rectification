# N19 - ACS Nano Initial Submission Audit

**Audit date:** 2026-09-19  
**Target:** ACS Nano, Article, initial submission / Fast Format  
**Current overall status:** `NOT_READY - AUTHOR/METADATA BLOCKERS ONLY`  
**Scientific layer:** `PASS`  
**Publication-figure scientific layer:** `PASS / VENUE_HANDOFF_READY`  
**Manuscript structural layer:** `PASS`  

## Official rule verification

Current ACS Nano Author Guidelines were rechecked on 2026-09-19. The page reports **Last updated July 03, 2026**. The current official web guidance is used when it differs from the older Author Checklist snapshot. The Article requirements relevant here are: an approximately 250-word abstract without references, 5-7 lowercase keywords, an unheaded Introduction generally <=1000 words, Results/Discussion, Conclusions, Methods at the end of the text, and a graphical TOC. Initial submissions may use ACS Fast Format; figures/tables/equations are embedded near relevance, references may use any complete consistent style including titles, and Supporting Information is submitted separately.

## 1. Manuscript structure

**PASS**

- Title: 13 words; no `First`/`Novel`; title case; uses the accepted `2D` form.
- Abstract: **235 words**, no citations, no novelty wording.
- Keywords: **7**, all lowercase.
- Introduction: **466 words**, no `Introduction` heading.
- Main sections: unnumbered.
- Results, Discussion, Conclusions, and Methods are present.
- Methods is the final scientific text section; back matter follows.
- Figures/tables/equations remain embedded near their discussion.
- Supporting Information is a separate file.
- Supporting Information description is placed before Acknowledgments and References, following the current 2026 web guidance.
- `Data Availability Statement` is present.
- AI-assisted-use disclosure is present in the Methods/reproducibility text and Acknowledgments.

### QA correction made during N19

The section heading `Two distinct in-plane relaxation models...` was narrowed to `Two distinct in-plane relaxation representations...` to preserve the Five-Reviewer scope boundary that FEM and VFF share the same GSFE/elastic targets. This is a wording correction only; no result changed.

## 2. Citations and references

**PASS FOR INITIAL FAST FORMAT / REVISION POLISH STILL AVAILABLE**

- In-text references are superscript numbers without brackets.
- Citation numbers appear after adjacent punctuation.
- Citation order was recomputed after moving Methods to the required end-of-text location.
- The reference list contains 26 individually numbered references in first-citation order.
- Journal-article titles are present.
- The three references that previously used truncated author lists below the >20-author threshold were expanded.
- All references retain DOI or stable preprint metadata where available.
- Current Fast Format permits any complete, consistent initial reference style. Exact CASSI abbreviations/title-case/punctuation can therefore be finalized at revision without blocking initial submission.

## 3. Supporting Information

**PASS**

- Separate DOCX and PDF are present.
- Five pages visually inspected.
- A split table-row defect in Table S2 was corrected by preventing row splitting; no row now breaks across pages.
- No clipping, overlapping text, broken tables, or missing glyphs were observed in the final render.
- SI contains the branch, symmetry, scaling, boundary, Floquet, thermal, elasticity, and reproducibility audits claimed in the manuscript.

## 4. Figures and artwork

**SCIENTIFIC PASS; `REVISION_STAGE_MAJOR` FOR LITERAL ARIAL EXPORT**

- Figures 1-6 passed the Publication Figure Designer scientific/visual gate in N18.
- Final-size figure design uses >=7 pt lettering and >=0.6 pt lines.
- Color is not the sole critical encoding.
- Captions are present and figures are cited in order.
- Current local EPS/TIFF/PNG derivatives render with **Arimo** because literal Arial is not installed in this environment. Do not relabel the font. Before revised-manuscript/final-artwork upload, re-export the vector masters in an environment with literal Arial or outline the verified Arial text. This issue is not a scientific blocker.

## 5. Graphical TOC

**TECHNICAL PASS / AUTHOR CONFIRMATION REQUIRED**

- Size: **9.0 cm x 4.0 cm**.
- TIFF: **600 dpi, RGB**.
- EPS derivative included.
- Minimal/no text, no logo.
- No third-party/stock/published artwork is embedded.
- Graphic is illustrative and not presented as evidence.
- Because AI-assisted programmatic preparation was used, the authors must review and affirmatively adopt it as their original manuscript artwork and confirm that the manuscript AI disclosure accurately covers this use before upload.

## 6. Cover letter

**BLOCKED BY AUTHOR-SUPPLIED METADATA**

A one-page ACS Nano cover-letter draft is prepared with the scientific fit and SI description completed. It intentionally leaves placeholders for:

- corresponding author name/contact;
- coauthor names;
- preprint status;
- prior editor discussion;
- Review-Only Material status;
- authorship/originality/exclusivity confirmation.

No personal or administrative information was guessed.

## 7. Mandatory metadata / declarations still missing

These items prevent an actual upload and are therefore the only current `BLOCKER` class:

1. **Author list and order** in the manuscript/submission system.
2. **Affiliations** and corresponding-author mailing address/email; coauthor contact metadata.
3. **All-author consent** and exclusive-submission confirmation.
4. **Funding sources and grant/award numbers**, or an explicit author confirmation that no external funding applies; ACS requires funding to be reported in both manuscript and submission system.
5. **Conflict-of-interest / competing financial interest statement** supplied by the authors.
6. **Preprint status, prior ACS Nano editor discussion, and Review-Only Material status** for the cover letter.
7. **TOC author adoption/originality confirmation.**

Optional/recommended follow-up: 6-8 reviewer suggestions; ORCID linking through ACS; public repository DOI/URL for the reproducibility package.

## 8. Deterministic manifest audit

The ACS Nano structural audit script returns:

`CONDITIONAL_READY` - 0 deterministic blockers, 6 majors.

All six majors are the known figure-font issue (`Arimo` rather than literal `Arial`). The deterministic schema does not encode missing author/funding/COI metadata, so the manual overall gate is correctly stricter: **NOT_READY** until author input is supplied.

## 9. Visual QA

**PASS**

- Main manuscript: **16 pages**, all inspected; no clipping, overlap, broken figures/tables, missing glyphs, or orphaned captions observed.
- SI: **5 pages**, all inspected after the Table S2 row-split repair.
- Cover-letter draft: **1 page**, inspected and clean.
- TOC graphic: inspected at native export; layout is clean and unclipped.

## Gate decision

`N19 ACS Nano initial-submission package = NOT_READY (author/administrative metadata blockers only)`

No additional simulation, statistical analysis, literature search, or scientific rewriting is required to clear this gate. The next action is author-supplied metadata/declaration completion, followed by a very short final submission audit and upload-package freeze.
