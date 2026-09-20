from pathlib import Path
import sys,math
import numpy as np,pandas as pd
from scipy.optimize import root,least_squares
ROOT=Path('/mnt/data/janus_baseline_gate/release/Janus_MoSSe_AuditResolved_ReproducibilityRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');A=np.column_stack([J.A1,J.A2]);AINV=np.linalg.inv(A)

def make_disk(R):
 M=int(math.ceil(R+2)); pts=[]
 for q in range(-2*M,2*M+1):
  for r in range(-2*M,2*M+1):
   p=q*J.A1+r*J.A2
   if np.linalg.norm(p)<=R+1e-12: pts.append(p)
 pts=np.array(pts,float);pts-=pts.mean(axis=0);return pts
pos=make_disk(8); N=len(pos); theta=20/math.sqrt(N);S=J.contact_factors(theta,land.vectors,pos)

def pdist(uv1,uv2):
 d=np.asarray(uv1)-np.asarray(uv2);d-=np.round(d);return np.linalg.norm(A@d)
def enum(n=21):
 sols=[]
 for u in np.linspace(0,1,n,endpoint=False):
  for v in np.linspace(0,1,n,endpoint=False):
   x0=A@np.array([u,v])
   def f(z):return J.contact_ugh(z[0],z[1],S,land,0,0)[1]
   def j(z):return J.contact_ugh(z[0],z[1],S,land,0,0)[2]
   rr=root(f,x0,jac=j,method='hybr',options={'xtol':1e-12,'maxfev':1500})
   if np.linalg.norm(f(rr.x))>1e-8:continue
   uv=AINV@rr.x;uv-=np.floor(uv)
   if any(pdist(uv,s['uv'])<2e-6 for s in sols):continue
   xy=A@uv;U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,0);ev=np.linalg.eigvalsh(H)
   sols.append(dict(uv=uv,xy=xy,U=U,ev=ev,stable=ev[0]>1e-7))
 sols.sort(key=lambda q:q['U']);return sols

def fold(x0,sign,step=.01):
 x=np.array(x0,float);F=0;last=(0,x.copy())
 while F<5:
  Fn=F+step
  def f(z):return J.contact_ugh(z[0],z[1],S,land,0,sign*Fn)[1]
  def j(z):return J.contact_ugh(z[0],z[1],S,land,0,sign*Fn)[2]
  rr=root(f,x,jac=j,method='hybr',options={'xtol':1e-12,'maxfev':1500})
  if np.linalg.norm(f(rr.x))>1e-7:
   guess=np.array([x[0],x[1],F+step/2]);break
  uvstep=AINV@(rr.x-x);uvstep-=np.round(uvstep)
  if np.linalg.norm(A@uvstep)>.15:
   step/=2
   continue
  ev=np.linalg.eigvalsh(j(rr.x))
  if ev[0]<=0:
   guess=np.array([(x[0]+rr.x[0])/2,(x[1]+rr.x[1])/2,(F+Fn)/2]);break
  F=Fn;x=rr.x;last=(F,x.copy())
 def aug(q):
  U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]);return np.r_[g,np.linalg.det(H)]
 c=[]
 for dx in [0,.001,-.001,.01,-.01,.03,-.03,.08,-.08]:
  ls=least_squares(aug,guess+[dx,0,0],xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=7000,x_scale='jac')
  q=ls.x;U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]);ev=np.linalg.eigvalsh(H);res=np.linalg.norm(aug(q))
  if res<1e-7 and q[2]>0 and ev[1]>1e-6:c.append((abs(q[2]-last[0]),q,ev,res))
 c.sort(key=lambda z:z[0]);return c[0]
sols=enum(25)
print('N theta',N,theta)
for i,s in enumerate(sols):print(i,'U',s['U'],'uv',s['uv'],'ev',s['ev'],'stable',s['stable'])
mins=[s for s in sols if s['stable']]
for i,m in enumerate(mins):
 for sign in [+1,-1]:
  z=fold(m['xy'],sign);print('min',i,'sign',sign,'Fc',z[1][2],'xy',z[1][:2],'ev',z[2],'res',z[3])
ship=pd.read_csv(ROOT/'data/canonical/shape_scaling_extended.csv')
r=ship[(ship.family=='disk')&(ship['shape']=='R8')&(ship.Theta==20)].iloc[0]
print('SHIPPED',r[['Fp','Fm','rho']].to_dict())
# reproduce shipped chaining for R8 only across Thetas
from scipy.optimize import least_squares
def shipped_fold(theta,sign,zprev,pos):
 S2=J.contact_factors(theta,land.vectors,pos)
 def aug(q):
  x,y,F=q;U,g,H=J.contact_ugh(x,y,S2,land,0,sign*F);return np.array([g[0],g[1],np.linalg.det(H)])
 cands=[]
 for dx in [0,.001,-.001,.01,-.01]:
  ls=least_squares(aug,np.array(zprev)+[dx,0,0],xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=3000,x_scale='jac')
  q=ls.x;U,g,H=J.contact_ugh(q[0],q[1],S2,land,0,sign*q[2]);ev=np.linalg.eigvalsh(H)
  if np.linalg.norm(aug(q))<1e-7 and q[2]>0 and ev[1]>1e-6:cands.append((abs(q[2]-zprev[2])+np.linalg.norm(q[:2]-zprev[:2])*.02,q,ev))
 cands.sort(key=lambda t:t[0]);return cands[0][1]
zp=np.array([0.0151072601171,0.1812524912333,3.4851202323701]);zm=np.array([0.000055218493,-0.1736331839004,1.4222355051565])
for Th in [0,10,15,20]:
 th=Th/math.sqrt(N);zp=shipped_fold(th,+1,zp,pos);zm=shipped_fold(th,-1,zm,pos);print('chain',Th,'zp',zp,'zm',zm)
