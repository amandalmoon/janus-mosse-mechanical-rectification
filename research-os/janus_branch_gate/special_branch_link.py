import sys,json,numpy as np
from pathlib import Path
from scipy.optimize import root
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'core'))
import janus_fourier_landscapes_v12 as J
LAND=J.dft_landscape('2H_MoSSe_Se-S-Se-S');A=np.column_stack([J.A1,J.A2]);AI=np.linalg.inv(A)
th=2.9733856558252625; S=J.contact_factors(th,LAND.vectors)
def wrap(x):
 u=AI@x;u-=np.floor(u);return A@u
def pd(a,b):
 u=AI@(np.asarray(a)-np.asarray(b));u-=np.round(u);return A@u
sols=[]
for u in np.linspace(0,1,21,endpoint=False):
 for v in np.linspace(0,1,21,endpoint=False):
  z0=A@np.array([u,v])
  fun=lambda z:J.contact_ugh(z[0],z[1],S,LAND,0,0)[1]
  jac=lambda z:J.contact_ugh(z[0],z[1],S,LAND,0,0)[2]
  rr=root(fun,z0,jac=jac,method='hybr',tol=1e-11)
  if np.linalg.norm(fun(rr.x))>1e-8:continue
  w=wrap(rr.x)
  if any(np.linalg.norm(pd(w,q['xy']))<2e-6 for q in sols):continue
  U,g,H=J.contact_ugh(w[0],w[1],S,LAND,0,0);e=np.linalg.eigvalsh(H)
  sols.append({'xy':w,'U':float(U),'eig':e})
mins=sorted([q for q in sols if q['eig'][0]>1e-7],key=lambda q:q['U'])
# direct fold solve seeded near reported special point, and compare cell distance from ground family trajectory at F just below
F=1.9100735314967028
# solve prepared branch equilibrium at F-eps by Newton from ground zero state
def newton(xy,fy):
 xy=np.array(xy,float)
 for _ in range(100):
  U,g,H=J.contact_ugh(xy[0],xy[1],S,LAND,0,fy)
  if np.linalg.norm(g)<1e-12:return xy
  st=np.linalg.solve(H,g);n=np.linalg.norm(st)
  if n>.05:st*=.05/n
  xy-=st
 return xy
xprev=mins[0]['xy'].copy()
for f in np.arange(0,1.9001,.01): xprev=newton(xprev,f)
for f in [1.905,1.909,1.9099,1.9100,1.91006]: xprev=newton(xprev,f)
fold=np.array([1.0,0.20464121308819838])
out={'theta_deg':th,'n_stable_zero_force':len(mins),'ground_U0':mins[0]['U'],'meta_U0':mins[1]['U'],
     'prepared_branch_position_at_1p91006':[float(xprev[0]),float(xprev[1])],
     'periodic_distance_to_special_fold':float(np.linalg.norm(pd(xprev,fold))),
     'special_fold_force':F}
(ROOT/'special_branch_link.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
