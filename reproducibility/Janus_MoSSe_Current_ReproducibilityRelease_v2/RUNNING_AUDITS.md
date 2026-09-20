# Running current audit checks

Fast integrity checks:

```bash
python validate_release.py
python validate_canonical_baseline.py
python recompute_stationary_thermal.py
python pre_submission_integrity_check.py
```

Current thermal raw trajectory aggregates are in `data/raw_thermal_stationary/stationary_thermal_trajectory_raw.csv`; cycle-level NPZ files used to form those aggregates are retained in the same directory.

Provenance scripts for the long-window thermal simulation/analysis are retained under `provenance_scripts/`. The manuscript-facing release validator is path independent.

The pre-submission integrity check also rejects the stale Erratum attribution, protects the canonical data directory from the legacy guided v17 entry point, and requires the retired 10/10 thermal scripts to be explicitly labeled as historical provenance.
