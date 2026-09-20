import sys, math, numpy as np
from dataclasses import replace
from scipy.optimize import root, least_squares
from pathlib import Path
SRC=Path('/mnt/data/janus_n4_gate/release/Janus_MoSSe_CanonicalUnguided_BaselineRelease/source')
sys.path.insert(0,str(SRC))
import janus_fourier_landscapes_v12 as J
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)
base=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); pos=J.make_hexagonal_flake(6); theta=1.5

def translate(land,a):
 d=land.vectors@a
 c=land.c_cos*np.cos(d)+land.c_sin*np.sin(d)
 s=-land.c_cos*np.sin(d)+land.c_sin*np.cos(d)
 return J.FourierLandscape('tr',land.vectors.copy(),c,s,land.energy_unit_meV,land.source_note)
def scaleodd(land,eta): return replace(land,c_sin=land.c_sin*eta,name='eta')
def pdist(uv1,uv2):
 d=np.asarray(uv1)-np.asarray(uv2); d-=np.round(d); return np.linalg.norm(A@d)
def enumerate_minima(land,ngrid=11):
 S=J.contact_factors(theta,land.vectors,pos); sols=[]
 for u in np.linspace(0,1,ngrid,endpoint=False):
  for v in np.linspace(0,1,ngrid,endpoint=False):
   x0=A@np.array([u,v])
   f=lambda x:J.contact_ugh(x[0],x[1],S,land,0,0)[1]
   jac=lambda x:J.contact_ugh(x[0],x[1],S,land,0,0)[2]
   rr=root(f,x0,jac=jac,method='hybr',options={'xtol':1e-10,'maxfev':500})
   if np.linalg.norm(f(rr.x))>1e-7: continue
   uv=AINV@rr.x; uv-=np.floor(uv); xy=A@uv
   if any(pdist(uv,q['uv'])<1e-5 for q in sols): continue
   U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,0); ev=np.linalg.eigvalsh(H)
   if ev[0]>1e-7: sols.append(dict(uv=uv,xy=xy,U=U))
 sols.sort(key=lambda q:q['U']); return sols

def branch_fold(land,x0,sign,step=.08,maxF=5):
 S=J.contact_factors(theta,land.vectors,pos); x=np.array(x0,float); F=0.0
 def eq(F,xguess):
  f=lambda z:J.contact_ugh(z[0],z[1],S,land,0,sign*F)[1]
  jac=lambda z:J.contact_ugh(z[0],z[1],S,land,0,sign*F)[2]
  rr=root(f,xguess,jac=jac,method='hybr',options={'xtol':1e-10,'maxfev':600})
  if np.linalg.norm(f(rr.x))>1e-6:return None,None
  return rr.x,np.linalg.eigvalsh(jac(rr.x))
 x,ev=eq(0,x); last=(0,x,ev)
 while F<maxF:
  Fn=F+step; xn,en=eq(Fn,x)
  if xn is None or en[0]<=0:
   guess=np.array([x[0],x[1],F+step/2]);break
  duv=AINV@(xn-x);duv-=np.round(duv)
  if np.linalg.norm(A@duv)>.2:
   step/=2
   if step<1e-4:guess=np.array([x[0],x[1],F]);break
   continue
  F,x,ev=Fn,xn,en;last=(F,x,ev)
 else: raise RuntimeError('no fold')
 def aug(q):
  xx,yy,FF=q;U,g,H=J.contact_ugh(xx,yy,S,land,0,sign*FF);return np.r_[g,np.linalg.det(H)]
 cands=[]
 for dx in [0,.001,-.001,.01,-.01,.05,-.05]:
  ls=least_squares(aug,guess+[dx,0,0],xtol=2e-12,ftol=2e-12,gtol=2e-12,max_nfev=2000,x_scale='jac')
  q=ls.x; U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]);eig=np.linalg.eigvalsh(H)
  if np.linalg.norm(aug(q))<1e-6 and q[2]>0 and eig[1]>1e-6:cands.append((abs(q[2]-last[0]),q))
 if not cands: raise RuntimeError('fold fail')
 cands.sort(key=lambda t:t[0]); return cands[0][1][2]
def delta(land):
 mins=enumerate_minima(land); g=mins[0]
 fp=branch_fold(land,g['xy'],+1); fm=branch_fold(land,g['xy'],-1)
 return fp-fm,fp,fm,g['U'],len(mins)
for t in np.linspace(0,0.875,8):
 tr=translate(base,t*J.A2)
 vals=[]
 for e in [-.05,.05]:
  vals.append(delta(scaleodd(tr,e))[0])
 slope=(vals[1]-vals[0])/.1
 d1=delta(scaleodd(tr,1.0))[0]
 print(t,slope,d1,vals,flush=True)
