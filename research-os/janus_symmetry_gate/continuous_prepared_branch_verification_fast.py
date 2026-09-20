from __future__ import annotations
import sys, json, time
from pathlib import Path
import numpy as np, pandas as pd
from scipy.optimize import root
ROOT=Path(__file__).resolve().parent; CORE=ROOT/'core'; sys.path.insert(0,str(CORE))
import janus_fourier_landscapes_v12 as J
LAND=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)
# Adaptive-style deterministic mesh: baseline 0.01 deg, 0.002 deg in [2.75,2.94), 0.0005 deg in [2.94,3].
g1=np.arange(0.0,2.7500001,0.01)
g2=np.arange(2.752,2.9400001,0.002)
g3=np.arange(2.9405,3.0000001,0.0005)
TH=np.concatenate([g1,g2,g3])
CHECK=[0,.5,1,1.5,2,2.5,2.75,2.9,2.94,2.96,2.97,2.973,2.974,2.98,2.99,3]

def wrap(x):
 uv=AINV@np.asarray(x,float); uv-=np.floor(uv); return A@uv

def pdelta(a,b):
 uv=AINV@(np.asarray(a,float)-np.asarray(b,float)); uv-=np.round(uv); return A@uv

def pdist(a,b): return float(np.linalg.norm(pdelta(a,b)))

def eval_S(S,xy,F=0): return J.contact_ugh(float(xy[0]),float(xy[1]),S,LAND,0.0,float(F))

def stationary_S(S,seed,F=0):
 def f(z): return eval_S(S,z,F)[1]
 def j(z): return eval_S(S,z,F)[2]
 rr=root(f,np.asarray(seed,float),jac=j,method='hybr',tol=1e-12); res=float(np.linalg.norm(f(rr.x)))
 if res>5e-9: raise RuntimeError(('stationary',res,rr.message))
 U,g,H=eval_S(S,rr.x,F); return np.asarray(rr.x,float),float(U),np.linalg.eigvalsh(H),res

def enum(theta,n=21):
 S=J.contact_factors(float(theta),LAND.vectors); out=[]
 for u in np.linspace(0,1,n,endpoint=False):
  for v in np.linspace(0,1,n,endpoint=False):
   seed=A@np.array([u,v])
   try: xy,U,eig,res=stationary_S(S,seed,0)
   except Exception: continue
   w=wrap(xy)
   if any(pdist(w,q['xy'])<3e-6 for q in out): continue
   U,g,H=eval_S(S,w,0); out.append({'xy':w,'U':float(U),'eig':np.linalg.eigvalsh(H)})
 out.sort(key=lambda q:q['U']); return out

def fold_S(S,seed,fc_prev,direction):
 def feq(z):
  U,g,H=eval_S(S,z,0); return np.array([g[0],np.linalg.det(H)])
 # first try direct warm start
 starts=[np.asarray(seed,float)]
 best=None
 for k,st in enumerate(starts):
  rr=root(feq,st,method='hybr',tol=1e-12); res2=float(np.linalg.norm(feq(rr.x)))
  if res2<=2e-7:
   U,g,H=eval_S(S,rr.x,0); fc=float(direction*g[1]); eig=np.linalg.eigvalsh(H)
   if fc>=-1e-8 and eig[1]>1e-7:
    Ut,gt,Ht=eval_S(S,rr.x,direction*fc); fullres=float(np.linalg.norm(np.r_[gt,np.linalg.det(Ht)]))
    best=(rr.x.copy(),fc,eig,fullres,pdist(rr.x,seed))
 # fallback multistart only if direct suspicious
 if best is None or abs(best[1]-fc_prev)>0.08 or best[4]>0.03:
  c=[]
  for dx,dy in [(0,0),(.001,0),(-.001,0),(0,.001),(0,-.001),(.005,0),(-.005,0),(0,.005),(0,-.005)]:
   rr=root(feq,np.asarray(seed,float)+[dx,dy],method='hybr',tol=1e-12); res2=float(np.linalg.norm(feq(rr.x)))
   if res2>2e-7: continue
   U,g,H=eval_S(S,rr.x,0); fc=float(direction*g[1]); eig=np.linalg.eigvalsh(H)
   if fc < -1e-8 or eig[1]<=1e-7: continue
   Ut,gt,Ht=eval_S(S,rr.x,direction*fc); fullres=float(np.linalg.norm(np.r_[gt,np.linalg.det(Ht)])); d=pdist(rr.x,seed)
   score=abs(fc-fc_prev)+.1*d+1e3*fullres
   c.append((score,rr.x.copy(),fc,eig,fullres,d))
  if not c: raise RuntimeError('fold fallback failed')
  c.sort(key=lambda x:x[0]); _,xy,fc,eig,fullres,d=c[0]; best=(xy,fc,eig,fullres,d)
 return best

# init by independent enumeration theta=0
mins=[q for q in enum(0,21) if q['eig'][0]>1e-7]; mins.sort(key=lambda q:q['U']); assert len(mins)==2
old=pd.read_csv(ROOT/'branch_folds_independent.csv')
state={'ground':{'xy':mins[0]['xy'].copy()},'meta':{'xy':mins[1]['xy'].copy()}}
for oldbr,newbr in [('ground','ground'),('metastable','meta')]:
 sub=old[(old.branch==oldbr)&np.isclose(old.theta_deg,0)]
 for d,l in [(1,'plus'),(-1,'minus')]:
  r=sub[sub.direction==('+y' if d>0 else '-y')].iloc[0]; state[newbr]['f'+l]=np.array([r.fold_x,r.fold_y]); state[newbr]['Fc'+l]=float(r.Fc)

rows=[]; max0=0; maxfr=0; minhard=1e99; maxjump=0; start=time.time()
for i,th in enumerate(TH):
 S=J.contact_factors(float(th),LAND.vectors); rec={'theta_deg':float(th)}
 for br in ['ground','meta']:
  if i>0:
   oldxy=state[br]['xy'].copy(); xy,U,eig,res=stationary_S(S,oldxy,0); state[br]['xy']=xy; max0=max(max0,res); maxjump=max(maxjump,pdist(xy,oldxy))
  U,g,H=eval_S(S,state[br]['xy'],0); eig=np.linalg.eigvalsh(H); rec['U_'+br]=U; rec['zero_eig_'+br]=eig[0]
  for d,l in [(1,'plus'),(-1,'minus')]:
   oldxy=state[br]['f'+l].copy(); xy,fc,eig,fr,jump=fold_S(S,oldxy,state[br]['Fc'+l],d)
   state[br]['f'+l]=xy; state[br]['Fc'+l]=fc; maxfr=max(maxfr,fr); minhard=min(minhard,eig[1]); maxjump=max(maxjump,jump)
   rec['Fc_'+br+'_'+l]=fc; rec['hard_'+br+'_'+l]=eig[1]; rec['soft_'+br+'_'+l]=eig[0]
 rec['DeltaU0']=rec['U_meta']-rec['U_ground']; rec['DeltaF_plus']=rec['Fc_ground_plus']-rec['Fc_meta_plus']; rec['DeltaF_minus']=rec['Fc_ground_minus']-rec['Fc_meta_minus']; rows.append(rec)
 if i%100==0: print(i,len(TH),th,rec['DeltaU0'],rec['DeltaF_plus'],rec['DeltaF_minus'],flush=True)

df=pd.DataFrame(rows); df.to_csv(ROOT/'continuous_prepared_branch_dense.csv',index=False)
# independent checkpoint enumeration
chk=[]
for th in CHECK:
 sols=enum(th,21); ms=[q for q in sols if q['eig'][0]>1e-7]; ms.sort(key=lambda q:q['U'])
 # direct dense interpolation nearest for margin comparison
 r=df.iloc[int(np.argmin(abs(df.theta_deg.to_numpy()-th)))]
 chk.append({'theta_deg':th,'n_stationary':len(sols),'n_stable_minima':len(ms),'DeltaU_enum':ms[1]['U']-ms[0]['U'] if len(ms)==2 else np.nan,'nearest_dense_theta':r.theta_deg,'DeltaU_dense':r.DeltaU0,'DeltaF_plus_dense':r.DeltaF_plus,'DeltaF_minus_dense':r.DeltaF_minus})
check=pd.DataFrame(chk); check.to_csv(ROOT/'continuous_stationary_checkpoints.csv',index=False)
# prior match
prior=pd.read_csv(ROOT/'prepared_vs_global_summary.csv'); cmp=[]
for _,o in prior.iterrows():
 r=df.iloc[int(np.argmin(abs(df.theta_deg.to_numpy()-o.theta_deg)))]
 cmp.append({'theta_deg':o.theta_deg,'dU_abs':abs((o.U_meta-o.U_ground)-r.DeltaU0),'dFp_abs':abs((o.ground_Fc_plus-o.meta_Fc_plus)-r.DeltaF_plus),'dFm_abs':abs((o.ground_Fc_minus-o.meta_Fc_minus)-r.DeltaF_minus),'groundFp_abs':abs(o.ground_Fc_plus-r.Fc_ground_plus),'groundFm_abs':abs(o.ground_Fc_minus-r.Fc_ground_minus)})
cmp=pd.DataFrame(cmp); cmp.to_csv(ROOT/'continuous_vs_prior_025deg.csv',index=False)
met={}
for c in ['DeltaU0','DeltaF_plus','DeltaF_minus']:
 a=df[c].to_numpy(); th=df.theta_deg.to_numpy(); j=int(np.argmin(a)); da=np.abs(np.diff(a));
 met[c]={'min':float(a[j]),'theta_at_min_deg':float(th[j]),'max':float(a.max()),'all_positive':bool((a>0).all()),'max_adjacent_change':float(da.max()),'safety_ratio_min_over_max_adjacent_change':float(a[j]/da.max()),'n_positive_slopes':int((np.diff(a)>1e-10).sum())}
summary={'grid':{'n_points':len(df),'scheme':'0.01 deg to 2.75; 0.002 deg to 2.94; 0.0005 deg to 3.0','n_checkpoints':len(check)},'margins':met,'all_dense_positive':bool((df[['DeltaU0','DeltaF_plus','DeltaF_minus']]>0).all().all()),'all_checkpoints_exactly_two_stable_minima':bool((check.n_stable_minima==2).all()),'max_zero_root_residual':max0,'max_fold_residual':maxfr,'min_hard_eigenvalue':minhard,'max_periodic_tracking_jump':maxjump,'prior_match_max_abs':{x:float(cmp[x].max()) for x in cmp.columns if x!='theta_deg'},'known_nongeneric_point_deg':2.9733856558,'interpretation':'dense/adaptive numerical continuation plus independent 21x21 stationary-point checkpoints; not formal interval arithmetic proof'}
summary['gate']='PASS' if summary['all_dense_positive'] and summary['all_checkpoints_exactly_two_stable_minima'] and maxfr<1e-7 and minhard>1e-6 else 'FAIL'
(ROOT/'continuous_branch_verification_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2)); print('elapsed',time.time()-start)
