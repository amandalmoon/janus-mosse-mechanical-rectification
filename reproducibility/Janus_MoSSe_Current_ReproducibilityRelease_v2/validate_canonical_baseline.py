from pathlib import Path
import json, csv, math, re, subprocess, sys
ROOT=Path(__file__).resolve().parent
D=ROOT/'data'/'canonical'
BASE=json.loads((ROOT/'config'/'canonical_unguided.json').read_text())

def check(c,msg):
    if not c: raise AssertionError(msg)
def f(x): return float(x)
def rows(name):
    with open(D/name,newline='',encoding='utf-8') as fh: return list(csv.DictReader(fh))

check(BASE['material']['key']=='2H_MoSSe_Se-S-Se-S','wrong material')
check(BASE['contact']['N']==127 and BASE['contact']['shell']==6,'wrong reference contact')
check(float(BASE['contact']['k_perp'])==0.0,'headline baseline must be unguided')
check(BASE['preparation']['global_last_surviving_envelope']=='diagnostic_only','global envelope policy')

headline=['branch_audit.py','shape_scaling_audit.py','triangle_ground_switch.py','vector_mode_map.py','thermal_cluster_audit.py','matched_symmetry_final.py','matched_symmetry_audit.py']
for name in headline:
    txt=(ROOT/'audit_scripts'/name).read_text()
    check('dft_guided_material' not in txt,f'{name}: guided engine imported in headline analysis')

legacy=json.loads((ROOT/'config'/'production.json').read_text())
check(float(legacy['k_perp'])==25.0,'legacy guided-config fingerprint changed')

# Shape prepared-branch endpoint checks (independent fold solves at Theta=0 and 20).
ep=rows('baseline_shape_prepared_endpoint_check.csv')
check(len(ep)==28,'endpoint shape audit should contain 14 shapes x 2 scaled angles')
check(max(abs(f(r['dFp'])) for r in ep)<1e-10,'shape + threshold not prepared branch')
check(max(abs(f(r['dFm'])) for r in ep)<1e-10,'shape - threshold not prepared branch')
check(all(int(f(r['n_minima']))==2 for r in ep),'unexpected zero-force minima count')

# Full 14-shape x 4-Theta x 2-sign connectivity audit.
cn=rows('baseline_shape_branch_connectivity.csv')
check(len(cn)==112,'connectivity audit should contain 112 cases')
check(all(r['connected']=='True' for r in cn),'a shipped size/shape fold is not connected to prepared ground state')
check(max(f(r['maxres']) for r in cn)<1e-9,'shape equilibrium continuation residual too large')
check(min(f(r['mineig']) for r in cn)>0,'shape branch lost stability before shipped fold')

# Boundary A/B are actual stable zero-force stationary states around both ground-state switches.
tr=rows('baseline_triangle_stationary_check.csv')
check(len(tr)==12,'triangle stationary audit incomplete')
check(all(r['stable']=='True' for r in tr),'triangle A/B preparation is not stationary/stable')
check(max(f(r['grad_norm']) for r in tr)<1e-12,'triangle stationary residual')

# Existing release contract must still pass.
p=subprocess.run([sys.executable,str(ROOT/'validate_release.py')],cwd=ROOT,capture_output=True,text=True)
check(p.returncode==0,'base release validation failed: '+p.stdout+p.stderr)
print('CANONICAL UNGUIDED BASELINE VALIDATION: PASS')
print('config/canonical_unguided.json is authoritative for headline physics')
print('config/production.json is legacy guided provenance only (k_perp=25)')
