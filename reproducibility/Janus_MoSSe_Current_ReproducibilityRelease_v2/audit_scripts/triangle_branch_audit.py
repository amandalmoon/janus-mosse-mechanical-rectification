from pathlib import Path
_RELEASE_ROOT = Path(__file__).resolve().parents[1]
import sys, numpy as np, pandas as pd
from scipy.optimize import root, least_squares
sys.path.insert(0,str(_RELEASE_ROOT/'source'))
import janus_fourier_landscapes_v12 as J
import new_physics_v18 as NP
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); A=np.column_stack([J.A1,J.A2]);AINV=np.linalg.inv(A)

def pdist(u,v):
 d=np.array(u)-np.array(v);d-=np.round(d);return np.linalg.norm(A@d)
def enum_mins(theta,pos,ngrid=17):
 S=J.contact_factors(theta,land.vectors,pos); sols=[]
 for u in np.linspace(0,1,ngrid,endpoint=False):
  for v in np.linspace(0,1,ngrid,endpoint=False):
   x0=A@np.array([u,v])
   def f(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
   def j(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
   rr=root(f,x0,jac=j,method='hybr',options={'xtol':1e-11,'maxfev':1000})
   if np.linalg.norm(f(rr.x))>1e-7: continue
   uv=AINV@rr.x;uv-=np.floor(uv);xy=A@uv
   if any(pdist(uv,q['uv'])<1e-5 for q in sols):continue
   U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,0);ev=np.linalg.eigvalsh(H)
   if ev[0]>1e-7:sols.append(dict(uv=uv,xy=xy,U=U,ev=ev))
 sols.sort(key=lambda q:q['U']);return S,sols

def fold(S,x0,sign):
 # force continuation to near stability loss, then least-squares augmented solve near connected branch
 x=np.array(x0,float); F=0.; step=.02; prev=(0,x)
 while F<5:
  Fn=F+step
  def ff(z): return J.contact_ugh(z[0],z[1],S,land,0,sign*Fn)[1]
  def jj(z): return J.contact_ugh(z[0],z[1],S,land,0,sign*Fn)[2]
  rr=root(ff,x,jac=jj,method='hybr',options={'xtol':1e-11,'maxfev':1000})
  if np.linalg.norm(ff(rr.x))>1e-6:
   guess=np.array([x[0],x[1],F+step/2]);break
  ev=np.linalg.eigvalsh(jj(rr.x));duv=AINV@(rr.x-x);duv-=np.round(duv);jump=np.linalg.norm(A@duv)
  if jump>.2:
   step/=2
   if step<1e-4:guess=np.array([x[0],x[1],F]);break
   continue
  if ev[0]<=0:
   guess=np.array([(x[0]+rr.x[0])/2,(x[1]+rr.x[1])/2,(F+Fn)/2]);break
  F=Fn;x=rr.x;prev=(F,x.copy())
 else:raise RuntimeError('no threshold')
 def aug(q):
  xx,yy,FM=q;U,g,H=J.contact_ugh(xx,yy,S,land,0,sign*FM);return np.array([g[0],g[1],np.linalg.det(H)])
 c=[]
 for dx in [0,.001,-.001,.01,-.01,.05,-.05]:
  ls=least_squares(aug,guess+[dx,0,0],xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=5000,x_scale='jac');q=ls.x
  U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]);ev=np.linalg.eigvalsh(H)
  if np.linalg.norm(aug(q))<1e-7 and q[2]>0 and ev[1]>1e-6:
   # branch closeness to last tracked equilibrium
   duv=AINV@(q[:2]-prev[1]);duv-=np.round(duv);dist=np.linalg.norm(A@duv)
   c.append((dist+0.02*abs(q[2]-prev[0]),q,ev))
 if not c: return np.nan
 c.sort(key=lambda q:q[0]);return c[0][1][2]

rows=[]
for phi in [20,25]:
 pos,R=NP.make_fixedN_triangle(phi,127)
 for th in [2.7,2.9,3.0]:
  S,mins=enum_mins(th,pos)
  print('\nphi',phi,'theta',th,'nmins',len(mins))
  for i,m in enumerate(mins):
   fp=fold(S,m['xy'],+1);fm=fold(S,m['xy'],-1)
   print(i,'U',m['U'],'uv',m['uv'],'Fp',fp,'Fm',fm)
   rows.append(dict(phi=phi,theta=th,min_id=i,U0=m['U'],u0=m['uv'][0],v0=m['uv'][1],Fp=fp,Fm=fm,delta=fp-fm,is_ground=(i==0)))
pd.DataFrame(rows).to_csv(str(_RELEASE_ROOT/'data'/'canonical'/'triangle_branch_families.csv'),index=False)
