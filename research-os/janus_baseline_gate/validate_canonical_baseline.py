from pathlib import Path
import json, csv, re, sys, math
import pandas as pd
ROOT=Path('/mnt/data/janus_baseline_gate/release/Janus_MoSSe_AuditResolved_ReproducibilityRelease')
BASE=json.loads(Path('/mnt/data/janus_baseline_gate/canonical_unguided.json').read_text())

def check(c,msg):
    if not c: raise AssertionError(msg)
def near(a,b,t,msg):
    if not math.isfinite(a) or abs(a-b)>t: raise AssertionError(f'{msg}: {a} vs {b}')

check(BASE['material']['key']=='2H_MoSSe_Se-S-Se-S','material key')
check(BASE['contact']['N']==127 and BASE['contact']['shell']==6,'reference contact')
check(BASE['contact']['k_perp']==0.0,'headline baseline must be unguided')
check(BASE['preparation']['zero_force_state'].startswith('lowest-energy'),'prepared state definition')

# Headline scripts may use contact_ugh, but every direct call must pass k_perp=0/0.0.
headline=['branch_audit.py','shape_scaling_audit.py','triangle_ground_switch.py','vector_mode_map.py','thermal_cluster_audit.py','matched_symmetry_final.py','matched_symmetry_audit.py']
for name in headline:
    txt=(ROOT/'audit_scripts'/name).read_text()
    check('dft_guided_material' not in txt, f'{name}: guided engine imported into headline stage')
    # Direct explicit nonzero k_perp tokens are forbidden in the headline scripts.
    bad=re.findall(r'contact_ugh\([^\n]*?,\s*([1-9][0-9]*(?:\.[0-9]+)?)\s*,',txt)
    check(not bad,f'{name}: nonzero guide passed to contact_ugh {bad}')

# Legacy production config is explicitly not the baseline.
legacy=json.loads((ROOT/'config'/'production.json').read_text())
check(float(legacy['k_perp'])==25.0,'legacy config fingerprint changed; update policy if intentional')

# Release numerical contract.
import subprocess
p=subprocess.run([sys.executable,str(ROOT/'validate_release.py')],cwd=ROOT,text=True,capture_output=True)
check(p.returncode==0,'release validator failed: '+p.stdout+p.stderr)

# Independent dependency audit generated in this gate.
summ=json.loads(Path('/mnt/data/janus_baseline_gate/baseline_dependency_audit_summary.json').read_text())
ref=summ['reference_initialization']
near(ref['root_energy'],ref['ground_energy'],1e-12,'vector/thermal initial root is not ground state')
check(ref['matched_min_index']==0 and ref['distance_to_ground']<1e-10,'vector/thermal initial branch mismatch')
sc=summ['shape_checks']
check(sc['all_shipped_equal_prepared_1e-7'],'shape scaling contains a non-prepared branch')
check(sc['min_number_of_zero_force_minima']>=2,'shape stationary enumeration incomplete')
tc=summ['triangle_checks']
check(tc['all_AB_are_stationary_stable'],'triangle A/B are not stable stationary preparations')

print('CANONICAL UNGUIDED BASELINE VALIDATION: PASS')
print('legacy config/production.json: GUIDED PROVENANCE ONLY (k_perp=25), not baseline')
