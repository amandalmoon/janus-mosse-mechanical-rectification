# N17 Upstream Strengthening and Scientific Stop-Gate Report

## Gate decision

**SCIENTIFIC STOP GATE: PASS**

- Scientific blockers open: 0
- Scientific majors open: 0
- Scientific moderates open: 0
- Venue-only minors open: 1 (`FR-R01`, immutable archival DOI/identifier)

## FR-M01 - GSFE source-input uncertainty

Status: **CLOSED_WITH_SCOPE**.

The accessed Angeli primary-source materials report the three-shell GSFE coefficients at finite decimal precision and describe the underlying 9 x 9 registry sampling, but do not provide a fit covariance or a machine-readable raw 9 x 9 total-energy table. Actual statistical DFT/fit uncertainty is therefore `NOT_ASSESSABLE` from the accessed source material and is not fabricated.

A publication-resolution sensitivity audit instead varies each tabulated amplitude and phase over the half-unit interval implied by its printed precision. The first-order hyperrectangle gives `Delta F_c*=1.75899-1.86594` and `rho=0.41641-0.42079`; sixteen joint Latin-hypercube evaluations give `Delta F_c*=1.77264-1.84708` and `rho=0.41716-0.42002`. Every joint evaluation retains positive static rectification and the canonical deterministic test retains the `(1,-1)` winding. This is explicitly reported as a reporting-precision bound, not as DFT/fit uncertainty.

## FR-M02 - damping x drive interaction

Status: **CLOSED**.

A 72-point joint audit spans `gamma*=2,3,4,5,6,8`, `F0*=1.4,2.0,2.6,3.0`, and `tau*=30,40,60`. Every sampled state is cycle locked, but only 1 of 12 drive points preserves the `gamma*=4` winding across all tested damping values, and up to five distinct winding pairs occur at a single fixed drive point. The manuscript therefore treats the mode-locking map as protocol specific rather than a material-only phase diagram.

## FR-S01 - thermal sample-count precision

Status: **CLOSED**.

For each pooled `N=1000` high-temperature ensemble, 500 without-replacement subsamples were drawn at `N=50,100,200,300,500,750`. The minimum N at which at least 95% of subsamples reproduce zero-vector exclusion under the same 95% Hotelling criterion is 100 at `T*=0.50`, 200 at 0.55, 200 at 0.60, 300 at 0.65, and 500 at 0.70. The two-seed `N=1000` high-temperature analysis is therefore retained as a precision choice, not as a post hoc significance boundary.

## Writing and document QA

The newly added Methods/Results/Discussion/SI prose passed the connected paragraph-logic QA with zero issues. No new literature citation was introduced; the source-limit wording was rechecked against the Angeli primary-source materials.

The main manuscript was rendered to 16 pages and inspected page by page. The SI was re-laid out to avoid an orphaned thermal table and a caption-after-table split, re-rendered to 6 pages, and inspected page by page. No clipping, overlap, missing glyph, or broken table remains. A small multi-page continuation of Table S9 uses a repeated header and intact rows.

## Remaining venue item

`FR-R01` remains `OPEN_VENUE`: the code/data release does not yet have an immutable archival DOI/identifier. This is not a scientific blocker; it must be completed in the ACS Nano submission layer if an archival repository is used.

## Handoff

The scientifically strengthened manuscript, SI, and Claim-Evidence Matrix are ready for the ACS Nano venue/submission layer. Venue compliance is a separate judgment.
