# Janus MoSSe Current Reproducibility Release v2

This package accompanies the current claim-frozen manuscript **Unguided Full-2D Mechanical Rectification and Vector Mode Locking in Finite Janus MoSSe Contacts**.

## Current scientific contract

- Headline static thresholds use the lowest-energy zero-force prepared branch in the unguided full-2D contact.
- Same-spectrum symmetrization nulls the global directional bias; exact spatial inversion swaps thresholds/current.
- Compact rigid contacts are tested under theta*sqrt(N) similarity; triangular boundary reversal is an equilibrium prepared-registry crossing with edge-sensitive location.
- The 91-point vector-locking map is conditional on the declared m*=1, gamma*=4 reduced dynamical protocol.
- Thermal inference uses **dt=0.02, 60 burn cycles, 100 measured cycles**. The full T*=0.02-0.70 series uses N=500 trajectories; T*=0.50-0.70 is independently repeated with a second N=500 ensemble. The pooled mean vector remains statistically nonzero through the largest sampled T*=0.70. No extinction temperature is inferred.
- Linear FEM and nonlinear bond-angle relaxation are two in-plane representations sharing the same GSFE and target elastic constants; they are not full 3D atomistic validation.

## Quick checks

```bash
python validate_release.py
python validate_canonical_baseline.py
python recompute_stationary_thermal.py
```

The validator checks the current stationary thermal contract and rejects the retired 10-burn/10-measure thermal-boundary formulation.

## Current, legacy, and provenance-only code

- Current clean checks are the three top-level validators/recomputations listed above plus `pre_submission_integrity_check.py`.
- `config/canonical_unguided.json` is the headline baseline contract.
- `source/canonical_analysis_v17.py` and `config/production.json` are retained as **legacy guided v17/v18 provenance**; the script now writes only under `data/legacy_guided_v17/`.
- `audit_scripts/thermal_cluster_audit.py` is the explicitly **retired 10-burn/10-measure** calculation and writes only under `data/legacy_thermal_10x10/`.
- `provenance_scripts/` preserves original execution provenance and may contain historical absolute working paths. Those files are not clean-run entry points; path-independent manuscript-facing validation is provided at the release root.
- The GSFE source documentation follows the manuscript citation audit: the 2024 Erratum does **not** modify the published GSFE coefficients or conjugate phase pairing.
