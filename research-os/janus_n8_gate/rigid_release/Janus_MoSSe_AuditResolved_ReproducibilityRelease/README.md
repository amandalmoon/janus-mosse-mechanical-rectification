# Janus MoSSe Audit-Resolved Reproducibility Release

This package accompanies the audit-resolved manuscript **Unguided Full-2D Mechanical Rectification and Vector Mode Locking in Finite Janus MoSSe Contacts**.

## Scientific scope
The conservative material input is the corrected published three-shell GSFE parameterization for Janus MoSSe. The contact is a rigid finite cluster. The main audit-resolved conclusions are:

1. the published 2H registry landscape retains nonzero inversion-odd content after optimizing the registry origin;
2. for compact N=127 contacts, the lowest-energy zero-force registry branch remains the longest-lived branch for both force signs over the sampled 0-3 deg twist range, so the headline depinning split is not a last-surviving-metastable-basin artifact;
3. matched same-2H symmetrization gives a symmetry-null global envelope/current, while exact spatial inversion swaps the two directional thresholds and reverses the vector current;
4. compact hexagonal and disk-like families collapse under the scaled twist theta*sqrt(N), consistent with an inverse-linear-size 1/2 law rather than a new universal exponent;
5. for rotated triangular contacts, the physically prepared ground-state directional reversal is caused by a switch between competing registry minima, and its exact angle is edge-model dependent;
6. zero-mean unguided forcing produces finite-run integer vector windings on the sampled F0-period grid; a representative (1,-1) orbit is independently Floquet-stable;
7. trajectory-cluster bootstrap uncertainty shows that the mean vector current remains statistically negative through T*=0.60 in the sampled protocol, but not at T*=0.65; exact deterministic winding identity is much more fragile.

## Important scope limits
The package does **not** claim to supply missing material inputs. In particular, it does not provide polarity-resolved first-principles GSFE surfaces, relaxed/elastic edge calculations, load-dependent GSFE, experimentally calibrated effective mass or damping, or an experimental time/temperature mapping. Those require new external calculations or measurements and are treated as limitations rather than silently inferred.

## Layout
- `manuscript/` — main DOCX and Supplementary Information.
- `source/` — source snapshot of the published-GSFE numerical engine inherited from the prior canonical release.
- `audit_scripts/` — path-normalized copies of the scripts used for the audit-resolution calculations.
- `provenance_scripts/` — exact unmodified working snapshots retained for provenance.
- `data/canonical/` — canonical audit-resolved numerical tables used in the manuscript.
- `data/raw_thermal/` — one row per independent thermal trajectory for the canonical temperature grid; each row aggregates that trajectory's measured cycles.
- `figures/` — manuscript Figures 1-6.
- `validate_release.py` — path-independent validation of the shipped numerical contracts.
- `recompute_thermal_summary.py` — path-independent trajectory-cluster bootstrap reconstruction from the canonical raw thermal table.
- `config/production.json` and `requirements.txt` — inherited numerical environment/configuration context.
- `reports/AUDIT_RESOLUTION_REPORT.md` — reviewer-issue resolution ledger.

## Quick validation
From the package root:

```bash
python validate_release.py
```

Expected output:

```text
AUDIT-RESOLVED RELEASE VALIDATION: PASS
```

To reconstruct the thermal confidence intervals from trajectory-level data:

```bash
python recompute_thermal_summary.py
```

The expensive dynamical simulations are represented by the path-normalized audit scripts plus the shipped source snapshot and canonical raw/results tables. Exact unmodified working scripts are separately retained in `provenance_scripts/`. The two root-level utilities are intentionally path-independent and are the quickest release-integrity checks.
