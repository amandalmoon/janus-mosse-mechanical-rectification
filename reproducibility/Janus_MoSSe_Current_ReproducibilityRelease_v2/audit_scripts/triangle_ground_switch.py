from pathlib import Path
_RELEASE_ROOT = Path(__file__).resolve().parents[1]
import sys, numpy as np, pandas as pd
from scipy.optimize import brentq, root, least_squares
sys.path.insert(0,str(_RELEASE_ROOT/'source'))
import janus_fourier_landscapes_v12 as J
import new_physics_v18 as NP
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');A=np.column_stack([J.A1,J.A2]);
xyA=A@np.array([0.,0.]);xyB=A@np.array([1/3,1/3])

def energy(theta,pos,xy):
 S=J.contact_factors(theta,land.vectors,pos);return J.contact_ugh(xy[0],xy[1],S,land,0,0)[0]

def fold(theta,pos,xy0,sign):
 S=J.contact_factors(theta,land.vectors,pos);x=np.array(xy0);F=0.;step=.02;last=(0,x.copy())
 while F<4:
  Fn=F+step
  def f(z):return J.contact_ugh(z[0],z[1],S,land,0,sign*Fn)[1]
  def j(z):return J.contact_ugh(z[0],z[1],S,land,0,sign*Fn)[2]
  rr=root(f,x,jac=j,method='hybr',options={'xtol':1e-11,'maxfev':1000})
  if np.linalg.norm(f(rr.x))>1e-6:
   guess=np.array([x[0],x[1],F+step/2]);break
  ev=np.linalg.eigvalsh(j(rr.x));
  if ev[0]<=0:
   guess=np.array([(x[0]+rr.x[0])/2,(x[1]+rr.x[1])/2,(F+Fn)/2]);break
  F=Fn;x=rr.x;last=(F,x.copy())
 def aug(q):
  xx,yy,FF=q;U,g,H=J.contact_ugh(xx,yy,S,land,0,sign*FF);return np.array([g[0],g[1],np.linalg.det(H)])
 c=[]
 for dx in [0,.001,-.001,.01,-.01,.05,-.05]:
  ls=least_squares(aug,guess+[dx,0,0],xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=5000,x_scale='jac');q=ls.x
  U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]);ev=np.linalg.eigvalsh(H)
  if np.linalg.norm(aug(q))<1e-7 and q[2]>0 and ev[1]>1e-6: c.append((abs(q[2]-last[0]),q))
 c.sort(key=lambda q:q[0]);return c[0][1][2]

rows=[]
for phi in [20,25]:
 pos,R=NP.make_fixedN_triangle(phi,127)
 def dE(th):return energy(th,pos,xyA)-energy(th,pos,xyB)
 grid=np.linspace(2.5,3.1,121);roots=[]
 for a,b in zip(grid[:-1],grid[1:]):
  if dE(a)*dE(b)<0:roots.append(brentq(dE,a,b,xtol=1e-12))
 print('phi',phi,'energy switch roots',roots)
 for r in roots:
  for off in [-0.01,-0.001,0,0.001,0.01]:
   th=r+off; UA=energy(th,pos,xyA);UB=energy(th,pos,xyB);ground='A' if UA<UB else ('B' if UB<UA else 'degenerate')
   FAplus=fold(th,pos,xyA,+1);FAminus=fold(th,pos,xyA,-1);FBplus=fold(th,pos,xyB,+1);FBminus=fold(th,pos,xyB,-1)
   gp,gm=(FAplus,FAminus) if ground=='A' else (FBplus,FBminus)
   rows.append(dict(phi=phi,theta=th,energy_switch=r,UA=UA,UB=UB,ground=ground,FAplus=FAplus,FAminus=FAminus,FBplus=FBplus,FBminus=FBminus,ground_Fplus=gp,ground_Fminus=gm,ground_delta=gp-gm,global_Fplus=max(FAplus,FBplus),global_Fminus=max(FAminus,FBminus),global_delta=max(FAplus,FBplus)-max(FAminus,FBminus)))
   print(phi,th,ground,'ground delta',gp-gm,'global delta',max(FAplus,FBplus)-max(FAminus,FBminus))
pd.DataFrame(rows).to_csv(str(_RELEASE_ROOT/'data'/'canonical'/'triangle_ground_switch.csv'),index=False)
