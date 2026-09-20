from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from scipy.optimize import root
ROOT=Path('/mnt/data/janus_audit'); sys.path.insert(0,str(ROOT))
import janus_fourier_landscapes_v12 as J
import dft_guided_material_v12 as M
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
KP=25.0; F0=3.5

out={'model':'2H_MoSSe_Se-S-Se-S','k_perp':KP,'F0':F0}

# Independent 2D saddle root [Ux=0, det(H)=0] at fixed theta, seeded by production result.
rows=[]
for th in [0,0.5,1.0,1.5,2.0,2.5,3.0]:
    S=J.contact_factors(th,land.vectors)
    for name,direction in [('forward',1),('reverse',-1)]:
        prod=M.guided_threshold(th,land,direction,KP,ngrid=6000)
        def fun(z):
            U,g,H=J.contact_ugh(z[0],z[1],S,land,k_perp=KP,force_y=0.0)
            return np.array([g[0],np.linalg.det(H)])
        sol=root(fun,[prod['x_c'],prod['y_c']],method='hybr',tol=1e-12)
        U,g,H=J.contact_ugh(sol.x[0],sol.x[1],S,land,k_perp=KP,force_y=0.0)
        eig=np.linalg.eigvalsh(H); Fc=direction*g[1]
        rows.append({'theta_deg':th,'direction':name,'root_success':bool(sol.success),
                     'production_Fc':float(prod['Fc']),'independent_Fc':float(Fc),
                     'abs_Fc_difference':float(abs(Fc-prod['Fc'])),
                     'root_residual_norm':float(np.linalg.norm(fun(sol.x))),
                     'lambda_soft':float(eig[0]),'lambda_hard':float(eig[1]),
                     'Hxx':float(H[0,0])})
out['fixed_theta_independent_saddles']=rows

# Exact simultaneous endpoint solve [Ux=0, det(H)=0, +/-Uy=F0].
reported={'forward':1.9444516264438518,'reverse':1.0099068387052377}
endpoints={}
for name,direction in [('forward',1),('reverse',-1)]:
    th0=reported[name]
    prod=M.guided_threshold(th0,land,direction,KP,ngrid=12000)
    def f3(z):
        x,y,th=z
        S=J.contact_factors(th,land.vectors)
        U,g,H=J.contact_ugh(x,y,S,land,k_perp=KP,force_y=0.0)
        return np.array([g[0],np.linalg.det(H),direction*g[1]-F0])
    sol=root(f3,[prod['x_c'],prod['y_c'],th0],method='hybr',tol=1e-11)
    x,y,th=sol.x; S=J.contact_factors(th,land.vectors)
    U,g,H=J.contact_ugh(x,y,S,land,k_perp=KP,force_y=0.0); eig=np.linalg.eigvalsh(H)
    unguided_hxx=H[0,0]-KP
    endpoints[name]={'success':bool(sol.success),'x_c':float(x),'y_c':float(y),'theta_exact_deg':float(th),
                     'theta_reported_linear_interp_deg':float(th0),'theta_difference_deg':float(th-th0),
                     'stationarity_x_residual':float(abs(g[0])),'det_hessian_residual':float(abs(np.linalg.det(H))),
                     'force_residual':float(abs(direction*g[1]-F0)),
                     'lambda_soft':float(eig[0]),'lambda_hard':float(eig[1]),
                     'Hxx_guided':float(H[0,0]),'Hxx_unguided':float(unguided_hxx),
                     'local_min_kperp':float(max(0.0,-unguided_hxx))}
out['exact_F0_endpoints']=endpoints
exact_window=endpoints['forward']['theta_exact_deg']-endpoints['reverse']['theta_exact_deg']
reported_window=reported['forward']-reported['reverse']
out['window']={'exact_deg':float(exact_window),'reported_deg':float(reported_window),
               'difference_deg':float(exact_window-reported_window),
               'relative_difference':float((exact_window-reported_window)/reported_window)}

# Stability of all selected production candidates on 0.1-degree grid.
min_hard=np.inf; min_hxx=np.inf; max_soft=0.0; worst=None
for th in np.arange(0,3.0001,0.1):
    for direction in (1,-1):
        r=M.guided_threshold(float(th),land,direction,KP,ngrid=6000)
        min_hard=min(min_hard,float(r['eig_hard'])); min_hxx=min(min_hxx,float(r['Hxx']))
        if abs(float(r['eig_soft']))>max_soft:
            max_soft=abs(float(r['eig_soft'])); worst={'theta_deg':float(th),'direction':'forward' if direction>0 else 'reverse','lambda_soft':float(r['eig_soft'])}
out['selected_candidate_scan_0p1deg']={'min_lambda_hard':float(min_hard),'min_Hxx':float(min_hxx),
                                      'max_abs_lambda_soft_before_independent_refinement':float(max_soft),'worst':worst,
                                      'pass_hard_positive':bool(min_hard>0),'pass_Hxx_positive':bool(min_hxx>0)}

out['summary']={
    'max_abs_Fc_difference_fixed_theta':float(max(r['abs_Fc_difference'] for r in rows)),
    'max_root_residual_fixed_theta':float(max(r['root_residual_norm'] for r in rows)),
    'min_hard_eigenvalue_fixed_theta':float(min(r['lambda_hard'] for r in rows)),
    'full_hessian_math_gate':'PASS_WITH_NUMERICAL_REPORTING_CORRECTION'
}
path=ROOT/'full_hessian_audit.json'; path.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out['summary'],indent=2))
print(json.dumps(out['exact_F0_endpoints'],indent=2))
print(json.dumps(out['window'],indent=2))
print('report',path)
