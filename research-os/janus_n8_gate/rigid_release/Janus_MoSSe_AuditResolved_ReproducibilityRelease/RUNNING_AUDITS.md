# Running the audit-resolution calculations

The fastest integrity test is:

```bash
python validate_release.py
```

The canonical result tables are already shipped under `data/canonical/`. The following scripts regenerate the principal deterministic analyses. They write back into `data/canonical/` and use the source snapshot under `source/`.

```bash
python audit_scripts/asymmetry_global_check.py
python audit_scripts/resolve_branch_topology.py
python audit_scripts/matched_symmetry_final.py
python audit_scripts/shape_scaling_audit.py
python audit_scripts/triangle_ground_switch.py
python audit_scripts/edge_weight_ground_switch.py
python audit_scripts/vector_mode_map.py
python audit_scripts/floquet_conditioning_audit.py
```

`matched_symmetry_final.py` and the vector/Floquet calculations can take appreciably longer than the quick validator because they perform direct dynamical integration.

## Thermal reruns

The thermal simulation uses 1000 independent trajectories per requested temperature. A single temperature can be regenerated with, for example:

```bash
TEMP_SINGLE=0.10 TSET=T010 python audit_scripts/thermal_cluster_audit.py
```

For the canonical high-noise boundary checks:

```bash
TEMP_SINGLE=0.60 TSET=T060 python audit_scripts/thermal_cluster_audit.py
TEMP_SINGLE=0.65 TSET=T065 python audit_scripts/thermal_cluster_audit.py
```

To reconstruct confidence intervals from the shipped trajectory-level aggregates without rerunning Langevin dynamics:

```bash
python recompute_thermal_summary.py
```

The exact unmodified working scripts are retained under `provenance_scripts/`; `audit_scripts/` contains path-normalized release copies.
