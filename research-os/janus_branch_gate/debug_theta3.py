import sys, numpy as np
from pathlib import Path
from scipy.optimize import root
sys.path.insert(0,'/mnt/data/janus_branch_gate/core')
import janus_fourier_landscapes_v12 as J
LAND=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
A=np.column_stack([J.A1,J.A2]); AI=np.linalg.inv(A)
def wrap(x):
 u=AI@x;u-=np.floor(u);return A@u
def pd(a,b):
 u=AI@(a-b);u-=np.round(u);return A@u
th=3.; S=J.contact_factors(th,LAND.vectors)
sols=[]
for u in np.linspace(0,1,21,endpoint=False):
 for v in np.linspace(0,1,21,endpoint=False):
  x0=A@np.array([u,v])
  fun=lambda z:J.contact_ugh(z[0],z[1],S,LAND,0,0)[1]
  rr=root(fun,x0,method='hybr',tol=1e-11)
  if np.linalg.norm(fun(rr.x))>1e-9: continue
  w=wrap(rr.x)
  if any(np.linalg.norm(pd(w,q[0]))<2e-6 for q in sols):continue
  U,g,H=J.contact_ugh(w[0],w[1],S,LAND,0,0);e=np.linalg.eigvalsh(H)
  sols.append((w,U,e))
for q in sorted(sols,key=lambda x:x[1]): print(q)
q=sorted([q for q in sols if q[2][0]>1e-7],key=lambda x:x[1])[0]
xy=q[0].copy();print('ground',xy)
for f in [0,.001,.005,.01,.02,.05,.1]:
 fun=lambda z:J.contact_ugh(z[0],z[1],S,LAND,0,f)[1]
 rr=root(fun,xy,method='hybr',tol=1e-11)
 print('f',f,'succ',rr.success,'norm',np.linalg.norm(fun(rr.x)),'raw',rr.x,'pdelta',np.linalg.norm(pd(rr.x,xy)))
 if np.linalg.norm(fun(rr.x))<1e-8:
  xy=rr.x.copy();U,g,H=J.contact_ugh(*xy,S,LAND,0,f);print(' eig',np.linalg.eigvalsh(H))
