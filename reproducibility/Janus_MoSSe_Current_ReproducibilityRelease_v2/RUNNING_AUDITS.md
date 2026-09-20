# Running current audit checks

Fast integrity checks:

```bash
python validate_release.py
python validate_canonical_baseline.py
python recompute_stationary_thermal.py
```

Current thermal raw trajectory aggregates are in `data/raw_thermal_stationary/stationary_thermal_trajectory_raw.csv`; cycle-level NPZ files used to form those aggregates are retained in the same directory.

Provenance scripts for the long-window thermal simulation/analysis are retained under `provenance_scripts/`. The manuscript-facing release validator is path independent.
