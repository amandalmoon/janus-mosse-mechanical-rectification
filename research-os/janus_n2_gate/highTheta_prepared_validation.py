from pathlib import Path
import sys,math
import numpy as np,pandas as pd
from scipy.optimize import root
ROOT=Path('/mnt/data/janus_n2_gate/release/Janus_MoSSe_CanonicalUnguided_BaselineRelease');sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');A=np.column_stack([J.A1,J.A2]);AINV=np.linalg.inv(A)
dense=pd.read_csv('/mnt/data/janus_n2_gate/n2_original_hex_dense_theta_scaled.csv')
def xy(uv):return A@np.asarray(uv,float)
def wrap(z):
 u=AINV@np.asarray(z,float);return u-np.floor(u)
def pdist(a,b):
 d=np.asarray(a)-np.asarray(b);d-=np.round(d);return np.linalg.norm(A@d)
def enum(theta,pos,Fy,ngrid=17):
 S=J.contact_factors(theta,land.vectors,pos);roots=[]
 for u in np.linspace(0,1,ngrid,endpoint=False):
  for v in np.linspace(0,1,ngrid,endpoint=False):
   z0=xy((u,v))
   def fun(z):return J.contact_ugh(z[0],z[1],S,land,0,Fy)[1]
   def jac(z):return J.contact_ugh(z[0],z[1],S,land,0,Fy)[2]
   rr=root(fun,z0,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':700})
   if np.linalg.norm(fun(rr.x))>1e-7:continue
   uv=wrap(rr.x)
   if any(pdist(uv,r['uv'])<2e-6 for r in roots):continue
   zz=xy(uv);U,g,H=J.contact_ugh(zz[0],zz[1],S,land,0,Fy);ev=np.linalg.eigvalsh(H)
   roots.append(dict(uv=uv,U=U,ev0=ev[0],ev1=ev[1]))
 roots.sort(key=lambda r:r['U']);return roots
rows=[]
for N,sh in [(37,3),(61,4),(91,5)]:
 pos=J.make_hexagonal_flake(sh)
 for Th in [23.,24.,30.]:
  if Th==23 and N!=37: continue
  r=dense[(dense.N==N)&(dense.Theta==Th)].iloc[0]
  theta=float(r.theta_deg)
  z0=enum(theta,pos,0,ngrid=19);mins0=[x for x in z0 if x['ev0']>1e-7]
  for sign,col in [(+1,'Fp'),(-1,'Fm')]:
   Fc=float(r[col]);delta=min(0.01,0.005*Fc)
   rb=enum(theta,pos,sign*(Fc-delta),ngrid=19);ra=enum(theta,pos,sign*(Fc+delta),ngrid=19)
   mb=[x for x in rb if x['ev0']>1e-7];ma=[x for x in ra if x['ev0']>1e-7]
   rows.append(dict(N=N,Theta=Th,theta_deg=theta,sign=sign,Fc_dense=Fc,delta=delta,n_min0=len(mins0),ground_gap=(mins0[1]['U']-mins0[0]['U']) if len(mins0)>1 else np.nan,n_min_below=len(mb),min_soft_below=min([x['ev0'] for x in mb],default=np.nan),n_min_above=len(ma),min_soft_above=min([x['ev0'] for x in ma],default=np.nan),pass_contract=(len(mins0)>=1 and len(mb)>=1 and len(ma)==0)))
pd.DataFrame(rows).to_csv('/mnt/data/janus_n2_gate/n2_highTheta_prepared_validation.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))
