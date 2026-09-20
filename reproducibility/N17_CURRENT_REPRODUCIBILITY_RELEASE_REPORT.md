# N17 Current Reproducibility Release Rebuild + Clean Replay

## Gate

**PASS**

The previous canonical release was internally valid but stale relative to the current manuscript because it still encoded the retired 10-burn/10-measure thermal boundary. A new current release was rebuilt from the latest manuscript/SI, RT-B01 stationary thermal artifacts, current Figure 6, and current Red-Team scope audits.

## Changes

- replaced manuscript/SI with current Five-Reviewer-scoped manuscript v5 and Red-Team-scoped SI v4;
- replaced thermal Figure 6 with the stationary 60-burn/100-measure hierarchy;
- removed stale thermal canonical tables, stale raw-thermal directory, stale Figure 6, and stale audit-resolution report;
- added current stationary trajectory aggregates and cycle-level NPZ source data;
- added current force-direction, damping, preparation, and GSFE-parameter scope-audit CSVs;
- rewrote `validate_release.py` to enforce the current stationary contract at T*=0.70;
- added `recompute_stationary_thermal.py` for path-independent recomputation from shipped trajectory aggregates;
- regenerated SHA256 manifest.

## Clean replay

The zip was extracted into a fresh directory and checked independently.

- `sha256sum -c SHA256SUMS.txt`: PASS for all shipped files.
- `python validate_release.py`: `CURRENT RELEASE VALIDATION: PASS`.
- `python validate_canonical_baseline.py`: `CANONICAL UNGUIDED BASELINE VALIDATION: PASS`.
- `python recompute_stationary_thermal.py`: reproduces pooled T*=0.50-0.70 means and zero-vector rejection; at T*=0.70, mean (u,v)=(0.036997653872,-0.076447530209), Hotelling T2=38.054778 > 6.0155069, P(v_cycle<0)=0.50802, Ptarget=0.01116.

## Research OS status

The Five Reviewer reproducibility blocker CM-5 is closed. No scientific blocker remains from Red Team or Five Reviewer review. The manuscript can now proceed to the ACS Nano venue/submission layer, subject to venue-specific formatting/graphics/TOC/SI/declarations audit.
