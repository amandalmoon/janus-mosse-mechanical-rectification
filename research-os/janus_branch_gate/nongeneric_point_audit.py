from __future__ import annotations
import sys,json
from pathlib import Path
import numpy as np
from scipy.optimize import root
import pandas as pd
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'core'))
import janus_fourier_landscapes_v12 as J
LAND=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)

def wrap(xy):
 uv=AINV@np.asarray(xy,float);uv-=np.floor(uv);return A@uv

def pdelta(a,b):
 uv=AINV@(np.asarray(a)-np.asarray(b));uv-=np.round(uv);return A@uv

def stationary(theta,force_y,nseed=21):
 S=J.contact_factors(theta,LAND.vectors);out=[]
 for u in np.linspace(0,1,nseed,endpoint=False):
  for v in np.linspace(0,1,nseed,endpoint=False):
   z0=A@np.array([u,v])
   fun=lambda z:J.contact_ugh(z[0],z[1],S,LAND,k_perp=0,force_y=force_y)[1]
   jac=lambda z:J.contact_ugh(z[0],z[1],S,LAND,k_perp=0,force_y=force_y)[2]
   rr=root(fun,z0,jac=jac,method='hybr',tol=1e-11)
   if np.linalg.norm(fun(rr.x))>1e-8: continue
   w=wrap(rr.x)
   if any(np.linalg.norm(pdelta(w,q['xy']))<2e-6 for q in out): continue
   U,g,H=J.contact_ugh(w[0],w[1],S,LAND,k_perp=0,force_y=force_y)
   e=np.linalg.eigvalsh(H)
   out.append({'xy':w,'U':float(U),'eig':e})
 return out

def eq3(z):
 x,y,th=z
 S=J.contact_factors(th,LAND.vectors)
 U,g,H=J.contact_ugh(x,y,S,LAND,k_perp=0,force_y=0)
 return np.array([g[0],H[0,0],H[0,1]])
sol=root(eq3,[1.0,0.204641,2.9733856558],method='hybr',tol=1e-12)
x,y,th=sol.x
S=J.contact_factors(th,LAND.vectors)
U,g,H=J.contact_ugh(x,y,S,LAND,k_perp=0,force_y=0)
F=float(g[1])
vals,vecs=np.linalg.eigh(H); v=vecs[:,0]
def softcurv(s):
 _,_,Hs=J.contact_ugh(x+s*v[0],y+s*v[1],S,LAND,k_perp=0,force_y=0)
 return float(v@Hs@v)
for h in [1e-3,3e-4,1e-4,3e-5,1e-5]:
 pass
cubics={str(h):(softcurv(h)-softcurv(-h))/(2*h) for h in [1e-3,3e-4,1e-4,3e-5,1e-5]}
# quartic derivative along soft direction via second derivative of curvature
h=1e-4
quartic=(softcurv(h)-2*softcurv(0)+softcurv(-h))/(h*h)
# full stationary enumeration just below/above boundary
checks=[]
for delta in [-1e-4,-1e-5,1e-5,1e-4]:
 sols=stationary(th,F+delta,21)
 st=[q for q in sols if q['eig'][0]>1e-7]
 checks.append({'deltaF':delta,'force':F+delta,'n_stationary':len(sols),'n_stable':len(st),
                'stable_min_soft':min([q['eig'][0] for q in st],default=None)})
out={'root_success':bool(sol.success),'root_residual':float(np.linalg.norm(eq3(sol.x))),
     'theta_deg':float(th),'x':float(x),'y':float(y),'F_plus':F,
     'Hxx':float(H[0,0]),'Hxy':float(H[0,1]),'Hyy':float(H[1,1]),
     'eig_soft':float(vals[0]),'eig_hard':float(vals[1]),
     'soft_vector':[float(v[0]),float(v[1])],'force_coupling_abs_vy':abs(float(v[1])),
     'cubic_estimates':cubics,'quartic_along_fixed_soft_direction':float(quartic),
     'stationary_checks':checks}
(ROOT/'nongeneric_point_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
pd.DataFrame(checks).to_csv(ROOT/'nongeneric_point_stability_check.csv',index=False)
print(json.dumps(out,indent=2))
