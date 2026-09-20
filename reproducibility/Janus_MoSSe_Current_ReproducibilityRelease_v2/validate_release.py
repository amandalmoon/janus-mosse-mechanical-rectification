from pathlib import Path
import csv, math, sys
ROOT=Path(__file__).resolve().parent
D=ROOT/'data'/'canonical'

def rows(name):
    with open(D/name,newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
def f(x): return float(x)
def near(x,y,tol,msg):
    if not math.isfinite(x) or abs(x-y)>tol: raise AssertionError(f'{msg}: {x} vs {y} tol {tol}')
def check(cond,msg):
    if not cond: raise AssertionError(msg)

# 1. Prepared ground-state branch is lower energy and lasts longer across the sampled hexagonal range.
r=rows('branch_family_summary.csv')
check(len(r)>=20,'branch summary incomplete')
check(all(x['ground_lower_energy']=='True' and x['ground_lasts_longer']=='True' for x in r),'ground-state branch contract failed')
sel=[x for x in r if abs(f(x['theta'])-1.5)<1e-12]
plus=[x for x in sel if int(float(x['sign']))==1][0]; minus=[x for x in sel if int(float(x['sign']))==-1][0]
near(f(plus['Fc_ground']),3.0711353385,5e-8,'F_c,+ ground')
near(f(minus['Fc_ground']),1.2586722985,5e-8,'F_c,- ground')

# 2. Matched symmetry contracts.
c=rows('matched_symmetry_final_contracts.csv')[0]
check(f(c['sym_global_static_split_abs'])<1e-8,'matched symmetrized global split not null')
check(f(c['inv_threshold_swap_plus_abs'])<1e-10 and f(c['inv_threshold_swap_minus_abs'])<1e-10,'inversion threshold swap failed')
check(f(c['inv_current_u_sum_abs'])<1e-10 and f(c['inv_current_v_sum_abs'])<1e-10,'inversion current reversal failed')
check(f(c['sym_current_norm'])<1e-10,'symmetric current not null')

# 3. Coordinate-invariant 2H asymmetry and symmetric 3R nulls.
a=rows('asymmetry_global_check.csv')
two=[x for x in a if x['key']=='2H_MoSSe_Se-S-Se-S'][0]
near(f(two['rms']),0.20624278237,5e-10,'2H odd RMS')
check(f(two['multistart_spread'])<1e-12,'asymmetry minimizer not stable')
for key in ['3R_MoSSe_S-Se-Se-S','3R_MoSSe_Se-S-S-Se']:
    x=[q for q in a if q['key']==key][0]; check(f(x['rms'])<1e-12,f'{key} not inversion symmetric')

# 4. Compact size similarity across two contact-shape families.
s=rows('shape_scaling_metrics.csv')
for scope in ['hex','disk']:
    t20=[x for x in s if x['scope']==scope and int(float(x['Theta']))==20][0]
    check(f(t20['Fp_max_rel'])<0.002 and f(t20['Fm_max_rel'])<0.002,f'{scope} scaled collapse too weak')

# 5. Boundary-induced ground-state registry switching.
t=rows('triangle_ground_switch.csv')
for phi,ref in [(20,2.92127800838),(25,2.84723312226)]:
    rr=[x for x in t if int(float(x['phi']))==phi]
    vals={round(f(x['energy_switch']),11) for x in rr}
    check(len(vals)==1,f'nonunique energy switch for phi={phi}')
    near(next(iter(vals)),ref,5e-9,f'ground-state switch phi={phi}')
    before=[x for x in rr if f(x['theta'])<ref][-1]
    after=[x for x in rr if f(x['theta'])>=ref][0]
    check(f(before['ground_delta'])>0 and f(after['ground_delta'])<0,f'ground-state directional reversal missing phi={phi}')

# 6. Vector mode map and representative mode.
v=rows('vector_mode_map_F0_period.csv')
check(len(v)==91,'vector mode map must contain 91 points')
check(all(x['locked']=='True' for x in v),'finite-run integer-lock criterion failed')
rep=[x for x in v if abs(f(x['F0'])-2)<1e-12 and abs(f(x['period'])-40)<1e-12][0]
near(f(rep['m']),1,1e-12,'representative m'); near(f(rep['n']),-1,1e-12,'representative n')
check(max(f(x['lock_residual']) for x in v)<1e-10,'mode-map rounding residual too large')

# 7. Floquet conditioning across independent integrators/tolerances.
fl=rows('floquet_conditioning_check.csv')
rhos=[f(x['rho']) for x in fl]
check(max(rhos)<1e-18,'representative orbit not strongly attracting')
check((max(rhos)-min(rhos))/sum(rhos)*len(rhos)<1e-4,'Floquet solver disagreement too large')
check(max(f(x['closure']) for x in fl)<3e-11,'relative orbit closure too large')

# 8. Current stationary thermal contract.
th=rows('thermal_stationary_canonical.csv')
by={round(f(x['T']),2):x for x in th}
check(int(float(by[0.02]['burn_cycles']))==60 and int(float(by[0.02]['measure_cycles']))==100,'stationary thermal window must be 60 burn + 100 measured')
check(int(float(by[0.70]['n']))==1000,'high-T pooled thermal count must be 1000 at T*=0.70')
near(f(by[0.70]['mean_u']),0.036997653872049265,5e-12,'stationary mean_u T*=0.70')
near(f(by[0.70]['mean_v']),-0.0764475302089921,5e-12,'stationary mean_v T*=0.70')
check(by[0.70]['zero_excluded']=='True','zero vector must be excluded at sampled T*=0.70')
near(f(by[0.70]['P_neg_y']),0.50802,5e-12,'P_neg_y T*=0.70')
near(f(by[0.70]['P_target']),0.01116,5e-12,'P_target T*=0.70')

# 9. Raw stationary trajectory aggregates reproduce canonical point estimates/counts.
RAW=ROOT/'data'/'raw_thermal_stationary'/'stationary_thermal_trajectory_raw.csv'
with open(RAW,newline='',encoding='utf-8') as fh: raw=list(csv.DictReader(fh))
for T,x in by.items():
    rr=[q for q in raw if abs(float(q['T'])-T)<1e-12]
    expected=1000 if T>=0.50 else 500
    check(len(rr)==expected,f'raw stationary trajectory count mismatch at T={T}')
    mu=sum(float(q['mean_u']) for q in rr)/len(rr); mv=sum(float(q['mean_v']) for q in rr)/len(rr)
    pn=sum(float(q['frac_neg_y']) for q in rr)/len(rr); pt=sum(float(q['frac_target']) for q in rr)/len(rr)
    near(mu,f(x['mean_u']),1e-12,f'raw/canonical mean_u T={T}')
    near(mv,f(x['mean_v']),1e-12,f'raw/canonical mean_v T={T}')
    near(pn,f(x['P_neg_y']),1e-12,f'raw/canonical P_neg_y T={T}')
    near(pt,f(x['P_target']),1e-12,f'raw/canonical P_target T={T}')

# 10. Scope audits required by the current manuscript are shipped.
for fn in ['redteam_force_direction_scan.csv','redteam_gamma_sweep.csv','redteam_phase_preparation_sweep.csv','redteam_gsfe_parameter_sensitivity.csv']:
    check((D/fn).exists(),f'missing current scope-audit file: {fn}')

print('CURRENT RELEASE VALIDATION: PASS')
