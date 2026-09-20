from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np, pandas as pd
from scipy.optimize import root, least_squares, brentq
ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
import new_physics_v18 as NP
OUT=Path('/mnt/data/janus_n3_gate')
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)
xyA=A@np.array([0.,0.]); xyB=A@np.array([1/3,1/3])
def boundary_mask(pos):
 out=[]
 for i in range(len(pos)):
  d=np.linalg.norm(pos-pos[i],axis=1); out.append(np.sum((d>1e-6)&(np.abs(d-1)<1e-6))<6)
 return np.asarray(out,bool)
def S_w(theta,pos,w):
 R=J.rotation_matrix(theta); d=pos@R.T-pos; ph=d@land.vectors.T
 return np.sum(w[:,None]*np.exp(1j*ph),axis=0)/w.sum()
def eval_ugh(S,xy,Fy=0): return J.contact_ugh(xy[0],xy[1],S,land,0,Fy)
def energy(theta,pos,w,xy): return float(eval_ugh(S_w(theta,pos,w),xy,0)[0])
def fold(theta,pos,w,xy0,sign):
 S=S_w(theta,pos,w); x=np.array(xy0,float); F=0.; step=.025; prev=(0.,x.copy()); guess=None
 while F<5:
  Fn=F+step
  ff=lambda z:J.contact_ugh(z[0],z[1],S,land,0,sign*Fn)[1]
  jj=lambda z:J.contact_ugh(z[0],z[1],S,land,0,sign*Fn)[2]
  rr=root(ff,x,jac=jj,method='hybr',options={'xtol':1e-11,'maxfev':800}); res=np.linalg.norm(ff(rr.x))
  if res>1e-6:
   if step>.001: step*=.5; continue
   guess=np.array([x[0],x[1],F+step/2]); break
  ev=np.linalg.eigvalsh(jj(rr.x)); duv=AINV@(rr.x-x); duv-=np.round(duv); jump=np.linalg.norm(A@duv)
  if jump>.15:
   if step>.001: step*=.5; continue
   guess=np.array([x[0],x[1],F]); break
  if ev[0]<=0:
   guess=np.array([(x[0]+rr.x[0])/2,(x[1]+rr.x[1])/2,(F+Fn)/2]); break
  F=Fn;x=rr.x;prev=(F,x.copy())
 if guess is None: raise RuntimeError('no fold')
 def aug(q):
  _,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]); return np.r_[g,np.linalg.det(H)]
 cand=[]
 for dx in [0,.002,-.002,.01,-.01,.04,-.04]:
  ls=least_squares(aug,guess+np.array([dx,0,0]),xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=2500,x_scale='jac')
  q=ls.x; _,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]); ev=np.linalg.eigvalsh(H); res=np.linalg.norm(aug(q))
  if res<1e-7 and q[2]>0 and ev[1]>1e-6:
   duv=AINV@(q[:2]-prev[1]);duv-=np.round(duv);dist=np.linalg.norm(A@duv)
   cand.append((dist+.02*abs(q[2]-prev[0]),q,ev,res))
 if not cand: raise RuntimeError('no candidate')
 cand.sort(key=lambda z:z[0]); _,q,ev,res=cand[0]
 return float(q[2]),float(ev[1]),float(res)
def enum_mins(theta,pos,w,ngrid=21):
 S=S_w(theta,pos,w); sols=[]
 for u in np.linspace(0,1,ngrid,endpoint=False):
  for v in np.linspace(0,1,ngrid,endpoint=False):
   x0=A@np.array([u,v]); ff=lambda x:J.contact_ugh(x[0],x[1],S,land,0,0)[1]; jj=lambda x:J.contact_ugh(x[0],x[1],S,land,0,0)[2]
   rr=root(ff,x0,jac=jj,method='hybr',options={'xtol':1e-11,'maxfev':900})
   if np.linalg.norm(ff(rr.x))>1e-7:continue
   uv=AINV@rr.x;uv-=np.floor(uv);xy=A@uv
   dup=False
   for q in sols:
    d=uv-q['uv'];d-=np.round(d)
    if np.linalg.norm(A@d)<2e-5:dup=True;break
   if dup:continue
   U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,0);ev=np.linalg.eigvalsh(H)
   if ev[0]>1e-7:sols.append({'uv':uv,'U':float(U),'eig':float(ev[0])})
 sols.sort(key=lambda q:q['U']);return sols
rows=[]; stat=[]; enums=[]
for phi in [20,25]:
 pos,R=NP.make_fixedN_triangle(phi,127); edge=boundary_mask(pos)
 for ew in [.5,.75,1.,1.25,1.5]:
  w=np.ones(len(pos));w[edge]=ew
  de=lambda th:energy(th,pos,w,xyA)-energy(th,pos,w,xyB)
  grid=np.linspace(2.4,3.35,191);rE=None
  for a,b in zip(grid[:-1],grid[1:]):
   if de(a)==0 or de(a)*de(b)<0:
    rE=float(a if de(a)==0 else brentq(de,a,b,xtol=5e-13,rtol=1e-13));break
  if rE is None:raise RuntimeError('no energy root')
  vals={}
  hard=[];res=[]
  for fam,xy in [('A',xyA),('B',xyB)]:
   fp,hp,rp=fold(rE,pos,w,xy,+1); fm,hm,rm=fold(rE,pos,w,xy,-1)
   vals[f'{fam}plus']=fp;vals[f'{fam}minus']=fm;vals[f'delta{fam}']=fp-fm;hard += [hp,hm];res += [rp,rm]
   U,g,H=eval_ugh(S_w(rE,pos,w),xy,0);ev=np.linalg.eigvalsh(H)
   stat.append({'phi_deg':phi,'edge_weight':ew,'switch_deg':rE,'family':fam,'U':float(U),'grad_resid':float(np.linalg.norm(g)),'eig_min':float(ev[0])})
  h=1e-4;slope=(de(rE+h)-de(rE-h))/(2*h)
  rows.append({'phi_deg':phi,'edge_weight':ew,'edge_sites':int(edge.sum()),'switch_deg':rE,'inside_0_3':rE<=3,
               'dE_slope_per_deg':slope,**vals,'sign_opposite_at_switch':vals['deltaA']*vals['deltaB']<0,
               'hard_min':min(hard),'fold_resid_max':max(res)})
  if ew in [.5,1.,1.5]:
   mins=enum_mins(rE,pos,w,21)
   enums.append({'phi_deg':phi,'edge_weight':ew,'switch_deg':rE,'n_stable_minima':len(mins),'U0':mins[0]['U'] if mins else np.nan,'U1':mins[1]['U'] if len(mins)>1 else np.nan,'U2':mins[2]['U'] if len(mins)>2 else np.nan,'min_eig':min(q['eig'] for q in mins) if mins else np.nan})
pd.DataFrame(rows).to_csv(OUT/'n3_edge_weight_sensitivity.csv',index=False)
pd.DataFrame(stat).to_csv(OUT/'n3_edge_weight_stationarity.csv',index=False)
pd.DataFrame(enums).to_csv(OUT/'n3_edge_weight_global_enumeration.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))
print('\nENUM\n',pd.DataFrame(enums).to_string(index=False))
