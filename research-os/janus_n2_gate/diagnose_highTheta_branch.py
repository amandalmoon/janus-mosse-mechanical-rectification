from pathlib import Path
import sys,math
import numpy as np,pandas as pd
from scipy.optimize import root
ROOT=Path('/mnt/data/janus_n2_gate/release/Janus_MoSSe_CanonicalUnguided_BaselineRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)

def uv_to_xy(uv): return A@np.asarray(uv,float)
def wrap_uv(xy):
 uv=AINV@np.asarray(xy,float); return uv-np.floor(uv)
def pdist(a,b):
 d=np.asarray(a)-np.asarray(b);d-=np.round(d);return np.linalg.norm(A@d)
def enum(theta,pos,F,ngrid=21):
 S=J.contact_factors(theta,land.vectors,pos); roots=[]
 for u in np.linspace(0,1,ngrid,endpoint=False):
  for v in np.linspace(0,1,ngrid,endpoint=False):
   x0=uv_to_xy((u,v))
   def fun(x): return J.contact_ugh(x[0],x[1],S,land,0,F)[1]
   def jac(x): return J.contact_ugh(x[0],x[1],S,land,0,F)[2]
   rr=root(fun,x0,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':500})
   if np.linalg.norm(fun(rr.x))>1e-7: continue
   uv=wrap_uv(rr.x)
   if any(pdist(uv,r['uv'])<2e-6 for r in roots): continue
   xy=uv_to_xy(uv);U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,F);ev=np.linalg.eigvalsh(H)
   roots.append({'uv':uv,'U':U,'ev0':ev[0],'ev1':ev[1]})
 roots.sort(key=lambda r:r['U']);return roots

def fine_cont(theta,pos,sign,Fmax,step=0.001):
 S=J.contact_factors(theta,land.vectors,pos)
 # ground at F=0
 r0=enum(theta,pos,0,ngrid=21); mins=[r for r in r0 if r['ev0']>1e-7]; g=mins[0]
 x=uv_to_xy(g['uv']); prevuv=g['uv']; rows=[]
 for i in range(int(Fmax/step)+1):
  F=i*step
  def fun(xx): return J.contact_ugh(xx[0],xx[1],S,land,0,sign*F)[1]
  def jac(xx): return J.contact_ugh(xx[0],xx[1],S,land,0,sign*F)[2]
  rr=root(fun,x,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':1000})
  res=np.linalg.norm(fun(rr.x));uv=wrap_uv(rr.x);jump=pdist(uv,prevuv)
  if res>1e-6 or jump>0.08:
   rows.append((F,np.nan,np.nan,res,jump,False));break
  x=rr.x;prevuv=uv;U,gg,H=J.contact_ugh(x[0],x[1],S,land,0,sign*F);ev=np.linalg.eigvalsh(H)
  rows.append((F,ev[0],ev[1],res,jump,True))
  if ev[0]<0: break
 return g,pd.DataFrame(rows,columns=['F','eig0','eig1','res','jump','ok'])

cases=[(3,24.0),(5,30.0)]
allr=[]
for sh,Th in cases:
 pos=J.make_hexagonal_flake(sh);N=len(pos);theta=Th/math.sqrt(N)
 g,tr=fine_cont(theta,pos,+1,3.2,step=.001)
 tr.to_csv(f'/mnt/data/janus_n2_gate/fine_cont_N{N}_Th{int(Th)}.csv',index=False)
 print('\nCASE',N,Th,theta,'ground',g)
 print('tail stable-ish')
 print(tr.tail(20).to_string(index=False))
 # inspect enumeration around candidate low fold and dense high fold
 for F in ([.18,.20,.21,.211,.212,.22,2.64,2.66,2.68] if N==37 else [.16,.18,.19,.197,.198,.20,.22,2.18,2.20,2.22]):
  rr=enum(theta,pos,F,ngrid=21); mins=[r for r in rr if r['ev0']>1e-7]
  allr.append(dict(N=N,Theta=Th,theta=theta,F=F,nstat=len(rr),nmin=len(mins),min_eigs=';'.join(f'{r["ev0"]:.6g}' for r in mins),min_Us=';'.join(f'{r["U"]:.6g}' for r in mins)))
  print('F',F,'nmin',len(mins),'mins',[(r['U'],r['ev0'],r['uv']) for r in mins])
pd.DataFrame(allr).to_csv('/mnt/data/janus_n2_gate/highTheta_force_enumeration.csv',index=False)
