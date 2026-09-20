from __future__ import annotations
import sys, json, math, time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import root

ROOT=Path(__file__).resolve().parent
CORE=ROOT/'core'
sys.path.insert(0,str(CORE))
import janus_fourier_landscapes_v12 as J

LAND=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)

# Dense production verification grid. 0--2.75 in 0.005 deg, then 2.75--3 in 0.001 deg.
grid1=np.arange(0.0,2.7500001,0.005)
grid2=np.arange(2.751,3.0000001,0.001)
THETAS=np.concatenate([grid1,grid2])

# Full stationary-point enumeration checkpoints, independent of continuation.
CHECKPOINTS=np.unique(np.concatenate([
    np.arange(0.0,3.0001,0.1),
    np.array([2.90,2.94,2.95,2.96,2.97,2.973,2.974,2.98,2.99,3.0])
]))

def wrap_xy(xy):
    uv=AINV@np.asarray(xy,float); uv=uv-np.floor(uv); return A@uv

def periodic_delta(a,b):
    duv=AINV@(np.asarray(a,float)-np.asarray(b,float)); duv=duv-np.round(duv); return A@duv

def periodic_dist(a,b):
    return float(np.linalg.norm(periodic_delta(a,b)))

def ugh(theta,xy,force_y=0.0):
    S=J.contact_factors(float(theta),LAND.vectors)
    return J.contact_ugh(float(xy[0]),float(xy[1]),S,LAND,k_perp=0.0,force_y=float(force_y))

def solve_stationary(theta,xy0,force_y=0.0,tol=2e-10):
    S=J.contact_factors(float(theta),LAND.vectors)
    def fun(z): return J.contact_ugh(z[0],z[1],S,LAND,k_perp=0.0,force_y=force_y)[1]
    def jac(z): return J.contact_ugh(z[0],z[1],S,LAND,k_perp=0.0,force_y=force_y)[2]
    rr=root(fun,np.asarray(xy0,float),jac=jac,method='hybr',tol=1e-12)
    res=float(np.linalg.norm(fun(rr.x)))
    if (not rr.success) and res>tol: raise RuntimeError(f'stationary fail theta={theta} res={res} msg={rr.message}')
    if res>tol: raise RuntimeError(f'stationary residual theta={theta} res={res}')
    U,g,H=J.contact_ugh(rr.x[0],rr.x[1],S,LAND,k_perp=0.0,force_y=force_y)
    return np.asarray(rr.x,float),float(U),np.linalg.eigvalsh(H),res

def enumerate_stationary(theta,force_y=0.0,nseed=21,tol=2e-9):
    S=J.contact_factors(float(theta),LAND.vectors); sols=[]
    for u in np.linspace(0,1,nseed,endpoint=False):
        for v in np.linspace(0,1,nseed,endpoint=False):
            x0=A@np.array([u,v])
            def fun(z): return J.contact_ugh(z[0],z[1],S,LAND,k_perp=0.0,force_y=force_y)[1]
            def jac(z): return J.contact_ugh(z[0],z[1],S,LAND,k_perp=0.0,force_y=force_y)[2]
            rr=root(fun,x0,jac=jac,method='hybr',tol=1e-11)
            if np.linalg.norm(fun(rr.x))>tol: continue
            w=wrap_xy(rr.x)
            if any(periodic_dist(w,q['xy'])<3e-6 for q in sols): continue
            U,g,H=J.contact_ugh(w[0],w[1],S,LAND,k_perp=0.0,force_y=force_y)
            sols.append({'xy':w,'U':float(U),'eig':np.linalg.eigvalsh(H),'res':float(np.linalg.norm(g))})
    sols.sort(key=lambda q:q['U']); return sols

def fold_eq(theta,z):
    S=J.contact_factors(float(theta),LAND.vectors)
    U,g,H=J.contact_ugh(z[0],z[1],S,LAND,k_perp=0.0,force_y=0.0)
    return np.array([g[0],np.linalg.det(H)],float)

def solve_fold_track(theta,xy_seed,fc_seed,direction):
    # Multiple continuation-near starts to robustly cross the isolated nongeneric point.
    starts=[]
    xy_seed=np.asarray(xy_seed,float)
    for dx,dy in [(0,0),(1e-4,0),(-1e-4,0),(0,1e-4),(0,-1e-4),(5e-4,0),(-5e-4,0),(0,5e-4),(0,-5e-4)]:
        starts.append(xy_seed+np.array([dx,dy]))
    cands=[]
    for st in starts:
        rr=root(lambda z:fold_eq(theta,z),st,method='hybr',tol=1e-12)
        res=float(np.linalg.norm(fold_eq(theta,rr.x)))
        if res>2e-7: continue
        U0,g0,H=ugh(theta,rr.x,0.0)
        fc=float(direction*g0[1]); eig=np.linalg.eigvalsh(H)
        if fc < -1e-8 or eig[1] <= 1e-8: continue
        full=ugh(theta,rr.x,direction*fc)
        fullres=float(np.linalg.norm(np.r_[full[1],np.linalg.det(full[2])]))
        d=periodic_dist(rr.x,xy_seed)
        score=abs(fc-fc_seed)+0.1*d+1e3*fullres
        cands.append((score,rr.x.copy(),fc,eig,fullres,d))
    if not cands:
        raise RuntimeError(f'fold tracking failed theta={theta} direction={direction}')
    cands.sort(key=lambda q:q[0]); return cands[0][1:]

# Initialize from independent 0.25-deg audit at theta=0.
oldb=pd.read_csv(ROOT/'branch_folds_independent.csv')
olds=pd.read_csv(ROOT/'prepared_vs_global_summary.csv')
r0=olds[np.isclose(olds.theta_deg,0.0)].iloc[0]
# zero-force branch seeds by independent enumeration, sorted energy
sol0=enumerate_stationary(0.0,0.0,21); mins0=[q for q in sol0 if q['eig'][0]>1e-7]
assert len(mins0)==2
mins0.sort(key=lambda q:q['U'])
state={
 'ground': {'xy0':mins0[0]['xy'].copy()},
 'meta': {'xy0':mins0[1]['xy'].copy()},
}
for br in ['ground','metastable']:
    bname='ground' if br=='ground' else 'meta'
    sub=oldb[(oldb.branch==br)&np.isclose(oldb.theta_deg,0.0)]
    for direction,lab in [(+1,'plus'),(-1,'minus')]:
        rr=sub[sub.direction==('+y' if direction>0 else '-y')].iloc[0]
        state[bname][f'fold_{lab}']=np.array([rr.fold_x,rr.fold_y],float)
        state[bname][f'fc_{lab}']=float(rr.Fc)

rows=[]; max_zero_res=0.; max_fold_res=0.; min_hard=1e99; max_track_jump=0.
t0=time.time()
for idx,th in enumerate(THETAS):
    # track zero-force minima. At theta=0 keep initialization; thereafter solve from previous.
    if idx>0:
        for br in ['ground','meta']:
            xy,U,eig,res=solve_stationary(th,state[br]['xy0'],0.0)
            jump=periodic_dist(xy,state[br]['xy0']); max_track_jump=max(max_track_jump,jump)
            state[br]['xy0']=xy
            max_zero_res=max(max_zero_res,res)
    vals={}
    for br in ['ground','meta']:
        U,g,H=ugh(th,state[br]['xy0'],0.0); eig0=np.linalg.eigvalsh(H)
        vals[f'U_{br}']=U; vals[f'zero_eigmin_{br}']=eig0[0]
        for direction,lab in [(+1,'plus'),(-1,'minus')]:
            xy,fc,eig,res,d=solve_fold_track(th,state[br][f'fold_{lab}'],state[br][f'fc_{lab}'],direction)
            state[br][f'fold_{lab}']=xy; state[br][f'fc_{lab}']=fc
            vals[f'Fc_{br}_{lab}']=fc; vals[f'hard_{br}_{lab}']=eig[1]; vals[f'soft_{br}_{lab}']=eig[0]
            max_fold_res=max(max_fold_res,res); min_hard=min(min_hard,eig[1]); max_track_jump=max(max_track_jump,d)
    vals['theta_deg']=float(th)
    vals['DeltaU0']=vals['U_meta']-vals['U_ground']
    vals['DeltaF_plus']=vals['Fc_ground_plus']-vals['Fc_meta_plus']
    vals['DeltaF_minus']=vals['Fc_ground_minus']-vals['Fc_meta_minus']
    rows.append(vals)
    if idx%100==0: print(f'{idx+1}/{len(THETAS)} theta={th:.3f} dU={vals["DeltaU0"]:.6g} dFp={vals["DeltaF_plus"]:.6g} dFm={vals["DeltaF_minus"]:.6g}',flush=True)

df=pd.DataFrame(rows)
df.to_csv(ROOT/'continuous_prepared_branch_dense.csv',index=False)

# Independent 21x21 enumeration checkpoints: exactly two stable minima and continuation match.
checks=[]
for th in CHECKPOINTS:
    # nearest dense tracked row
    i=int(np.argmin(np.abs(df.theta_deg.to_numpy()-th))); r=df.iloc[i]
    sols=enumerate_stationary(float(th),0.0,21); mins=[q for q in sols if q['eig'][0]>1e-7]; mins.sort(key=lambda q:q['U'])
    # solve tracked zero-force minima at exact checkpoint using nearest tracked coordinates reconstructed via enumeration matching by energy.
    # Ground/meta tracked identity should equal the two energy-ordered minima because DeltaU>0 throughout.
    checks.append({
        'theta_deg':float(th),'n_stationary':len(sols),'n_stable_minima':len(mins),
        'U_ground_enum':mins[0]['U'] if len(mins)>0 else np.nan,
        'U_meta_enum':mins[1]['U'] if len(mins)>1 else np.nan,
        'DeltaU_enum':mins[1]['U']-mins[0]['U'] if len(mins)>1 else np.nan,
        'dense_nearest_theta':float(r.theta_deg),
        'DeltaU_dense':float(r.DeltaU0),
        'DeltaF_plus_dense':float(r.DeltaF_plus),
        'DeltaF_minus_dense':float(r.DeltaF_minus),
        'ground_energy_match_abs':abs(mins[0]['U']-r.U_ground) if len(mins)>0 and abs(r.theta_deg-th)<1e-9 else np.nan,
        'meta_energy_match_abs':abs(mins[1]['U']-r.U_meta) if len(mins)>1 and abs(r.theta_deg-th)<1e-9 else np.nan,
    })
checkdf=pd.DataFrame(checks); checkdf.to_csv(ROOT/'continuous_stationary_checkpoints.csv',index=False)

# Off-grid midpoint stress check: evaluate branch quantities at midpoints of the 20 intervals with smallest safety margin.
# Seed each evaluation from linearly closest dense states by solving zero-force minima from enumeration; folds are initialized by neighboring dense fold approximations unavailable in df.
# Here the dense spacing itself is <=0.005 deg; use direct independent branch audit helper-like enumeration+force continuation only on selected intervals.
# We focus on positivity safety via adjacent variation ratio and all checkpoint enumeration.

# Margins and numerical safety metrics.
metrics={}
for col in ['DeltaU0','DeltaF_plus','DeltaF_minus']:
    arr=df[col].to_numpy(float); th=df.theta_deg.to_numpy(float)
    j=int(np.argmin(arr)); metrics[col]={
        'min':float(arr[j]),'theta_at_min_deg':float(th[j]),'max':float(arr.max()),
        'all_positive':bool(np.all(arr>0)),
        'max_adjacent_abs_change':float(np.max(np.abs(np.diff(arr)))),
        'min_margin_over_max_adjacent_change':float(arr[j]/np.max(np.abs(np.diff(arr)))) if np.max(np.abs(np.diff(arr)))>0 else float('inf'),
        'n_nonmonotone_increases':int(np.sum(np.diff(arr)>1e-9)),
    }

# Compare exact 0.25-deg points to earlier independent audit.
comp=[]
for _,old in olds.iterrows():
    th=float(old.theta_deg); r=df.iloc[int(np.argmin(abs(df.theta_deg.to_numpy()-th)))]
    comp.append({
      'theta_deg':th,
      'dU_abs':abs((old.U_meta-old.U_ground)-r.DeltaU0),
      'dFp_abs':abs((old.ground_Fc_plus-old.meta_Fc_plus)-r.DeltaF_plus),
      'dFm_abs':abs((old.ground_Fc_minus-old.meta_Fc_minus)-r.DeltaF_minus),
      'groundFp_abs':abs(old.ground_Fc_plus-r.Fc_ground_plus),
      'groundFm_abs':abs(old.ground_Fc_minus-r.Fc_ground_minus),
    })
compdf=pd.DataFrame(comp); compdf.to_csv(ROOT/'continuous_vs_prior_025deg.csv',index=False)

summary={
 'grid':{'n_points':int(len(df)),'theta_min_deg':float(df.theta_deg.min()),'theta_max_deg':float(df.theta_deg.max()),
         'step_deg_0_to_2p75':0.005,'step_deg_2p751_to_3':0.001,
         'n_full_21x21_checkpoints':int(len(checkdf))},
 'margins':metrics,
 'all_dense_positive':bool((df[['DeltaU0','DeltaF_plus','DeltaF_minus']]>0).all().all()),
 'all_checkpoint_two_stable_minima':bool((checkdf.n_stable_minima==2).all()),
 'max_zero_force_root_residual':float(max_zero_res),
 'max_fold_full_residual':float(max_fold_res),
 'min_hard_fold_eigenvalue':float(min_hard),
 'max_periodic_tracking_jump':float(max_track_jump),
 'prior_0p25_max_abs_diff':{c:float(compdf[c].max()) for c in compdf.columns if c!='theta_deg'},
 'nongeneric_point_note':'Known isolated higher-order stability degeneracy near theta=2.9733856558 deg remains on the prepared ground forward boundary; boundary remains real but is not a generic fold at that isolated point.',
 'interpretation':'Numerical continuous-interval verification, not a formal interval-arithmetic proof.',
}
summary['gate']='PASS' if (summary['all_dense_positive'] and summary['all_checkpoint_two_stable_minima'] and max_fold_res<1e-7 and min_hard>1e-6) else 'FAIL'
(ROOT/'continuous_branch_verification_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('\nSUMMARY')
print(json.dumps(summary,indent=2))
print(f'elapsed_sec={time.time()-t0:.2f}')
