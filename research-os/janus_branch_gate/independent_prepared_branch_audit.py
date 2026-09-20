from __future__ import annotations
import sys, math, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import root

ROOT=Path(__file__).resolve().parent
CORE=ROOT/'core'
sys.path.insert(0,str(CORE))
import janus_fourier_landscapes_v12 as J

LAND=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
A=np.column_stack([J.A1,J.A2])
AINV=np.linalg.inv(A)
THETAS=np.arange(0.0,3.0001,0.25)


def wrap_xy(xy):
    uv=AINV@np.asarray(xy,float)
    uv=uv-np.floor(uv)
    return A@uv


def periodic_delta(a,b):
    duv=AINV@(np.asarray(a)-np.asarray(b))
    duv=duv-np.round(duv)
    return A@duv


def ugh(theta,xy,force_y=0.0):
    S=J.contact_factors(float(theta),LAND.vectors)
    return J.contact_ugh(float(xy[0]),float(xy[1]),S,LAND,k_perp=0.0,force_y=float(force_y))


def enumerate_stationary(theta, force_y=0.0, nseed=21, tol=1e-9):
    S=J.contact_factors(float(theta),LAND.vectors)
    sols=[]
    for u in np.linspace(0,1,nseed,endpoint=False):
        for v in np.linspace(0,1,nseed,endpoint=False):
            x0=A@np.array([u,v])
            def fun(z):
                return J.contact_ugh(z[0],z[1],S,LAND,k_perp=0.0,force_y=force_y)[1]
            def jac(z):
                return J.contact_ugh(z[0],z[1],S,LAND,k_perp=0.0,force_y=force_y)[2]
            rr=root(fun,x0,jac=jac,method='hybr',tol=1e-11)
            if np.linalg.norm(fun(rr.x))>tol:
                continue
            w=wrap_xy(rr.x)
            # dedup modulo lattice
            if any(np.linalg.norm(periodic_delta(w,q['xy']))<2e-6 for q in sols):
                continue
            U,g,H=J.contact_ugh(w[0],w[1],S,LAND,k_perp=0.0,force_y=force_y)
            eig=np.linalg.eigvalsh(H)
            sols.append({'xy':w,'U':float(U),'eig':eig,'H':H,'gradnorm':float(np.linalg.norm(g))})
    sols.sort(key=lambda q:q['U'])
    return sols


def solve_equilibrium_newton(S, xy0, force_y, maxiter=80):
    xy=np.asarray(xy0,float).copy()
    for _ in range(maxiter):
        U,g,H=J.contact_ugh(xy[0],xy[1],S,LAND,k_perp=0.0,force_y=force_y)
        gn=float(np.linalg.norm(g))
        if gn<1e-11:
            return True,xy,gn
        try:
            step=np.linalg.solve(H,g)
        except np.linalg.LinAlgError:
            step=np.linalg.pinv(H)@g
        sn=float(np.linalg.norm(step))
        if sn>0.08:
            step*=0.08/sn
        # backtracking on gradient norm
        accepted=False
        alpha=1.0
        for _ in range(12):
            trial=xy-alpha*step
            gt=J.contact_ugh(trial[0],trial[1],S,LAND,k_perp=0.0,force_y=force_y)[1]
            if np.linalg.norm(gt) < gn:
                xy=trial; accepted=True; break
            alpha*=0.5
        if not accepted:
            return False,xy,gn
    g=J.contact_ugh(xy[0],xy[1],S,LAND,k_perp=0.0,force_y=force_y)[1]
    return np.linalg.norm(g)<1e-8,xy,float(np.linalg.norm(g))


def continue_equilibrium(theta, xy0, direction, fmax=5.0, step=0.01):
    S=J.contact_factors(float(theta),LAND.vectors)
    xy=np.asarray(xy0,float).copy()
    rec=[]
    f=0.0
    while f<=fmax+1e-12:
        ok,newxy,gn=solve_equilibrium_newton(S,xy,direction*f)
        if not ok or gn>1e-8:
            break
        delta=np.linalg.norm(periodic_delta(newxy,xy))
        if f>0 and delta>0.18:
            break
        xy=newxy.copy()
        U,g,H=J.contact_ugh(xy[0],xy[1],S,LAND,k_perp=0.0,force_y=direction*f)
        eig=np.linalg.eigvalsh(H)
        rec.append((f,xy.copy(),float(U),eig.copy(),float(np.linalg.det(H))))
        if eig[0] < 2e-4:
            break
        f += step
    return rec

def solve_fold(theta, xy0, direction, f0):
    S=J.contact_factors(float(theta),LAND.vectors)
    # At a fold of U(x,y)-direction*f*y, H is independent of f.
    # Solve gx=0 and det(H)=0 in registry coordinates; then infer f=direction*gy.
    def fun2(z):
        U,g,H=J.contact_ugh(z[0],z[1],S,LAND,k_perp=0.0,force_y=0.0)
        return np.array([g[0],np.linalg.det(H)])
    candidates=[]
    offsets=[(0,0),(0.01,0),(-0.01,0),(0,0.01),(0,-0.01),(0.02,0.02),(-0.02,-0.02)]
    for dx,dy in offsets:
        rr=root(fun2,[xy0[0]+dx,xy0[1]+dy],method='hybr',tol=1e-12)
        res=np.linalg.norm(fun2(rr.x))
        if res>1e-7:
            continue
        x,y=rr.x
        U0,g0,H=J.contact_ugh(x,y,S,LAND,k_perp=0.0,force_y=0.0)
        f=float(direction*g0[1])
        eig=np.linalg.eigvalsh(H)
        if f < -1e-7 or eig[1] <= 1e-7:
            continue
        # confirm full tilted equilibrium residual
        Ut,gt,Ht=J.contact_ugh(x,y,S,LAND,k_perp=0.0,force_y=direction*f)
        fullres=float(np.linalg.norm([gt[0],gt[1],np.linalg.det(Ht)]))
        # branch proximity modulo lattice and force proximity
        dxy=float(np.linalg.norm(periodic_delta([x,y],xy0)))
        candidates.append((abs(f-f0)+0.05*dxy,fullres,np.array([x,y]),f,float(Ut),eig,H))
    if not candidates:
        raise RuntimeError(f'fold solve failed theta={theta} dir={direction} f0={f0}')
    candidates.sort(key=lambda q:(q[0],q[1]))
    score,res,xy,f,U,eig,H=candidates[0]
    return res,abs(f-f0),xy,f,U,eig,H

def cubic_and_force_coupling(theta, xy, H, h=2e-5):
    # soft eigenvector at the fold
    vals,vecs=np.linalg.eigh(H)
    v=vecs[:,0]
    S=J.contact_factors(float(theta),LAND.vectors)
    def soft_curv(s):
        _,_,Hs=J.contact_ugh(xy[0]+s*v[0],xy[1]+s*v[1],S,LAND,k_perp=0.0,force_y=0.0)
        return float(v@Hs@v)
    cubic=(soft_curv(h)-soft_curv(-h))/(2*h)
    coupling=abs(float(v[1]))
    return float(cubic),coupling,v


branch_rows=[]
stationary_rows=[]
summary=[]
for theta in THETAS:
    sols=enumerate_stationary(theta,0.0,21)
    mins=[q for q in sols if q['eig'][0]>1e-7]
    # record all stationary points
    for i,q in enumerate(sols):
        stationary_rows.append({'theta_deg':theta,'stationary_index':i,'U0':q['U'],
                                'x':q['xy'][0],'y':q['xy'][1],
                                'eig1':q['eig'][0],'eig2':q['eig'][1],
                                'stable_minimum':bool(q['eig'][0]>1e-7)})
    if len(mins)!=2:
        raise RuntimeError(f'theta={theta}: expected 2 stable minima, got {len(mins)} from {len(sols)} stationary points')
    mins.sort(key=lambda q:q['U'])
    # labels by zero-force energy, ground first
    folds={}
    for bi,q in enumerate(mins):
        label='ground' if bi==0 else 'metastable'
        for direction in (+1,-1):
            rec=continue_equilibrium(theta,q['xy'],direction,5.0,0.01)
            if len(rec)<2:
                raise RuntimeError(f'continuation too short theta={theta} branch={label} dir={direction}')
            # choose record with smallest |lambda_soft| near end as augmented-fold seed
            near=min(rec[-20:] if len(rec)>20 else rec,key=lambda z:abs(z[3][0]))
            res,fdiff,xyf,fc,Uf,eig,H=solve_fold(theta,near[1],direction,near[0])
            cubic,coupling,v=cubic_and_force_coupling(theta,xyf,H)
            folds[(label,direction)]=fc
            branch_rows.append({
                'theta_deg':theta,'branch':label,'U0':q['U'],'x0':q['xy'][0],'y0':q['xy'][1],
                'direction':'+y' if direction>0 else '-y','Fc':fc,'fold_x':xyf[0],'fold_y':xyf[1],
                'fold_residual':res,'lambda_soft':eig[0],'lambda_hard':eig[1],
                'soft_cubic':cubic,'force_coupling_abs_vy':coupling,
                'continued_points':len(rec),'seed_force':near[0]
            })
    gp=folds[('ground',+1)]; gm=folds[('ground',-1)]
    mp=folds[('metastable',+1)]; mm=folds[('metastable',-1)]
    summary.append({'theta_deg':theta,'U_ground':mins[0]['U'],'U_meta':mins[1]['U'],
                    'ground_Fc_plus':gp,'ground_Fc_minus':gm,'meta_Fc_plus':mp,'meta_Fc_minus':mm,
                    'ground_lower_energy':mins[0]['U']<mins[1]['U'],
                    'ground_longer_plus':gp>mp,'ground_longer_minus':gm>mm,
                    'global_envelope_plus':max(gp,mp),'global_envelope_minus':max(gm,mm),
                    'global_equals_ground_plus':abs(max(gp,mp)-gp)<1e-8,
                    'global_equals_ground_minus':abs(max(gm,mm)-gm)<1e-8})

stationary_df=pd.DataFrame(stationary_rows)
branch_df=pd.DataFrame(branch_rows)
summary_df=pd.DataFrame(summary)
stationary_df.to_csv(ROOT/'stationary_points_21x21.csv',index=False)
branch_df.to_csv(ROOT/'branch_folds_independent.csv',index=False)
summary_df.to_csv(ROOT/'prepared_vs_global_summary.csv',index=False)

# Stronger global-envelope spot checks: enumerate all stationary points just below/above the ground threshold
spot=[]
for theta in [0.0,1.5,3.0]:
    row=summary_df[np.isclose(summary_df.theta_deg,theta)].iloc[0]
    for direction,col in [(+1,'ground_Fc_plus'),(-1,'ground_Fc_minus')]:
        fc=float(row[col])
        for tag,f in [('below',fc-1e-4),('above',fc+1e-4)]:
            sols=enumerate_stationary(theta,direction*f,21)
            stable=[q for q in sols if q['eig'][0]>1e-7]
            spot.append({'theta_deg':theta,'direction':'+y' if direction>0 else '-y','side':tag,
                         'force_mag':f,'n_stationary':len(sols),'n_stable_minima':len(stable),
                         'min_soft_eig_stable':min([q['eig'][0] for q in stable],default=np.nan)})
pd.DataFrame(spot).to_csv(ROOT/'global_envelope_spotcheck.csv',index=False)

# Aggregate checks
rep15=summary_df[np.isclose(summary_df.theta_deg,1.5)].iloc[0]
max_fold_res=float(branch_df.fold_residual.max())
min_hard=float(branch_df.lambda_hard.min())
all_pass=bool(summary_df[['ground_lower_energy','ground_longer_plus','ground_longer_minus','global_equals_ground_plus','global_equals_ground_minus']].all().all())
result={
  'n_theta':len(summary_df),
  'theta_grid':[float(x) for x in THETAS],
  'all_two_minima':bool((stationary_df[stationary_df.stable_minimum].groupby('theta_deg').size()==2).all()),
  'all_ground_lower_and_longer_both_directions':all_pass,
  'theta1p5':{
    'ground_Fc_plus':float(rep15.ground_Fc_plus),'ground_Fc_minus':float(rep15.ground_Fc_minus),
    'meta_Fc_plus':float(rep15.meta_Fc_plus),'meta_Fc_minus':float(rep15.meta_Fc_minus),
    'U_ground':float(rep15.U_ground),'U_meta':float(rep15.U_meta)},
  'max_augmented_fold_residual':max_fold_res,
  'min_hard_fold_eigenvalue':min_hard,
  'global_spotcheck_above_has_no_stable_minimum':bool((pd.DataFrame(spot).query("side=='above'").n_stable_minima==0).all()),
  'gate':'PASS' if all_pass and max_fold_res<1e-7 and min_hard>1e-6 else 'FAIL'
}
(ROOT/'branch_gate_summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
print(summary_df.to_string(index=False))
