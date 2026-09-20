# ACS Nano Figure-Set Preflight

**Audit date:** 2026-09-19  
**Target:** ACS Nano Article  
**Scientific figure gate:** VENUE_HANDOFF_READY  
**ACS Nano venue status:** CONDITIONAL_READY

## Official sources checked

- ACS Nano Author Guidelines (last updated July 03, 2026): https://researcher-resources.acs.org/publish/author_guidelines?coden=ancac3
- ACS Nano Author Checklist: https://pubsapp.acs.org/paragonplus/submission/ancac3/ancac3_checklist.pdf

## Current official graphics requirements used

- Figures and tables cited in order; figures require captions.
- ACS Nano checklist: use Arial lettering; lettering >= 6 pt; lines >= 0.5 pt at final published size.
- ACS general graphics sizing: single-column up to 3.33 in; double-column 4.167-7.0 in; max depth 9.167 in including caption.
- General minimum raster resolution: 1200 dpi line art, 600 dpi grayscale, 300 dpi color.
- Do not rely on color alone when categorical identity matters; use symbols, labels, line styles, or other redundant cues.

## Figure-set result

| Figure | Claims | Scientific QA | Final-size visual QA | Manifest | Venue |
|---|---|---|---|---|---|
| FIG-01 | M0;C1;C4 | PASS | PASS | PASS | CONDITIONAL_READY |
| FIG-02 | C2;C5 | PASS | PASS | PASS | CONDITIONAL_READY |
| FIG-03 | C6;C7 | PASS | PASS | PASS | CONDITIONAL_READY |
| FIG-04 | C8;C9 | PASS | PASS | PASS | CONDITIONAL_READY |
| FIG-05 | C13;C14 | PASS | PASS | PASS | CONDITIONAL_READY |
| FIG-06 | C15;C16;C17;C18 | PASS | PASS | PASS | CONDITIONAL_READY |

## Passed items

- All six figures are generated from current executed simulation/audit artifacts; no placeholder or illustrative numerical evidence is used.
- All six are designed as double-column figures at approximately 504 pt (7.0 in) maximum width.
- Figure manifests specify 7 pt minimum text and >=0.6 pt minimum line width, exceeding ACS Nano checklist minima.
- Quantitative series use marker/line-style redundancy where categorical identity matters; ordered heat maps use explicit integer colorbars and accessible colormaps.
- Figure 1 uses a shared normalization/colorbar for directly comparable energy surfaces.
- Figures 2-4 use aligned scales where direct comparison is intended.
- Figure 5 separates Floquet relative deviation from closure rather than using a dual y-axis.
- Figure 6 distinguishes stationary mean drift, joint zero-current inference, and cycle-level identity loss without implying a thermal critical temperature.
- TIFF derivatives are RGB at 600 dpi. SVG and EPS vector exports plus 600-dpi PNG previews are retained.
- Every figure has a claim-linked manifest and passed deterministic manifest QA.
- All six canonical PNGs embedded in the manuscript are byte-identical to the corresponding document media payloads.
- The 15-page manuscript was rendered after insertion and visually checked; no clipping, overlap, caption separation, broken table, or missing figure was observed.

## Remaining venue condition

The execution environment does not contain literal Arial; `fc-match Arial` resolves to Arimo. The SVG masters have been explicitly declared with `font-family: Arial`, so they are suitable for final opening/re-export on a workstation with Arial installed. The current EPS/TIFF/PNG derivatives were rendered with the Arimo fallback and therefore are **not certified as the final ACS Nano upload artwork**. Re-export from the SVG masters on an Arial-equipped system, then repeat final-size visual QA before submission. No font files are included in the package.

## Gate

**Scientific design:** PASS / VENUE_HANDOFF_READY  
**ACS Nano figure compliance:** CONDITIONAL_READY  
**Blocker type:** venue-font/export environment only; no scientific figure blocker remains.
