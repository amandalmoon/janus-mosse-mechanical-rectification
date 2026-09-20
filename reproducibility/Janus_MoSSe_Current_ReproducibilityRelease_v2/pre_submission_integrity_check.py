from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")

def check(cond, msg):
    if not cond:
        raise AssertionError(msg)

src = read("source/janus_fourier_landscapes_v12.py")
cfg = json.loads(read("config/canonical_unguided.json"))
legacy = read("source/canonical_analysis_v17.py")
old_audit = read("audit_scripts/thermal_cluster_audit.py")
old_prov = read("provenance_scripts/thermal_cluster_audit.py")
release_readme = read("README.md")
validator = read("validate_release.py")

check("phase convention corrected in" not in src.lower(),
      "stale claim that the 2024 Erratum corrected the GSFE phase convention")
check("does not modify the GSFE coefficients" in cfg["material"]["source"],
      "canonical config must state the corrected Erratum provenance")
check('DATA = ROOT / "data" / "legacy_guided_v17"' in legacy,
      "legacy guided v17 script must not write into manuscript-facing canonical data")
check("RETIRED HISTORICAL THERMAL AUDIT" in old_audit,
      "retired 10/10 thermal audit must be explicitly labeled")
check("data/legacy_thermal_10x10" in old_audit,
      "retired 10/10 audit must be isolated from current canonical outputs")
check("RETIRED ORIGINAL-PATH PROVENANCE SCRIPT" in old_prov,
      "historical original-path thermal script must be explicitly labeled")
check("60 burn cycles" in release_readme and "100 measured cycles" in release_readme,
      "release README must declare the current stationary thermal contract")
check("burn_cycles']))==60" in validator and "measure_cycles']))==100" in validator,
      "validator must enforce 60-burn/100-measure thermal evidence")
print("PRE-SUBMISSION INTEGRITY CHECK: PASS")
