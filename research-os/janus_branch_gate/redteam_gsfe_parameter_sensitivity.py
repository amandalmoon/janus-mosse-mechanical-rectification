from pathlib import Path
import sys,math,numpy as np,pandas as pd
from scipy.optimize import root
ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease');sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
A=np.column_stack([J.A1,J.A2]);AINV=np.linalg.inv(A);pos=J.make_hexagonal_flake(6);theta=1.5

def pdelta(a,b):
 d=np.asarray(a)-np.asarray(b);uv=AINV@d;uv-=np.round(uv);return A@uv

def enumerate_min(land):
 S=J.contact_factors(theta,land.vectors,pos); sols=[]
 for u in np.linspace(0,1,15,endpoint=False):
  for v in np.linspace(0,1,15,endpoint=False):
   z=A@np.array([u,v]);rr=root(lambda q:J.contact_ugh(q[0],q[1],S,land,0,0)[1],z,jac=lambda q:J.contact_ugh(q[0],q[1],S,land,0,0)[2],tol=1e-11)
   if not rr.success:continue
   xy=rr.x;uv=AINV@xy;uv-=np.floor(uv);xy=A@uv; U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,0);ev=np.linalg.eigvalsh(H)
   if ev[0]<=1e-7:continue
   if all(np.linalg.norm(pdelta(xy,q[1]))>1e-5 for q in sols):sols.append((U,xy,ev))
 sols.sort(key=lambda q:q[0]);return S,sols

def eq_newton(S,land,xy,Fy):
 xy=xy.copy()
 for _ in range(60):
  U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,Fy);gn=np.linalg.norm(g)
  if gn<1e-11:return True,xy
  try:st=np.linalg.solve(H,g)
  except:return False,xy
  al=1.;ok=False
  for __ in range(20):
   tr=xy-al*st;gn2=np.linalg.norm(J.contact_ugh(tr[0],tr[1],S,land,0,Fy)[1])
   if gn2<gn:xy=tr;ok=True;break
   al*=.5
  if not ok:return False,xy
 return False,xy

def fc_dir(S,land,xy0,sgn):
 xy=xy0.copy();rec=[]
 for f in np.arange(0,5.0001,.01):
  ok,nxy=eq_newton(S,land,xy,sgn*f)
  if not ok:break
  if f>0 and np.linalg.norm(pdelta(nxy,xy))>.18:break
  xy=nxy;U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,sgn*f);ev=np.linalg.eigvalsh(H);rec.append((f,xy.copy(),ev))
  if ev[0]<2e-4:break
 near=min(rec[-20:],key=lambda z:abs(z[2][0]))
 def fun(z):
  U,g,H=J.contact_ugh(z[0],z[1],S,land,0,0);return [g[0],np.linalg.det(H)]
 cand=[]
 for off in [(0,0),(.01,0),(-.01,0),(0,.01),(0,-.01)]:
  rr=root(fun,near[1]+off,tol=1e-12);res=np.linalg.norm(fun(rr.x))
  if res>1e-7:continue
  U,g,H=J.contact_ugh(rr.x[0],rr.x[1],S,land,0,0);f=sgn*g[1];ev=np.linalg.eigvalsh(H)
  if f>=0 and ev[1]>1e-7:cand.append((abs(f-near[0]),f))
 if not cand:raise RuntimeError('fold')
 return min(cand)[1]

def eval_variant(label,W,phi):
 land=J._from_shell_phase(label,W,phi);S,mins=enumerate_min(land);g=mins[0];fp=fc_dir(S,land,g[1],+1);fm=fc_dir(S,land,g[1],-1);return dict(label=label,W1=W[0],W2=W[1],W3=W[2],phi1=phi[0],phi2=phi[1],phi3=phi[2],nmin=len(mins),gap=(mins[1][0]-mins[0][0]) if len(mins)>1 else np.nan,Fplus=fp,Fminus=fm,Delta=fp-fm,rho=(fp-fm)/(fp+fm))
baseW=[7.9,.1,.1];baseP=[131.9,1.2,85.4];rows=[]
for d in [-10,-5,-2,0,2,5,10]:
 p=baseP.copy();p[0]+=d;rows.append(eval_variant(f'phi1_{d:+g}',baseW,p))
for shell in [1,2]:
 for d in [-10,-5,5,10]:
  p=baseP.copy();p[shell]+=d;rows.append(eval_variant(f'phi{shell+1}_{d:+g}',baseW,p))
for mul in [0,0.5,2,5]:
 w=baseW.copy();w[1]=.1*mul;w[2]=.1*mul;rows.append(eval_variant(f'higherW_x{mul:g}',w,baseP))
df=pd.DataFrame(rows);df.to_csv('/mnt/data/janus_branch_gate/redteam_gsfe_parameter_sensitivity.csv',index=False);print(df[['label','nmin','gap','Fplus','Fminus','Delta','rho']].to_string(index=False));print('rho range',df.rho.min(),df.rho.max())
