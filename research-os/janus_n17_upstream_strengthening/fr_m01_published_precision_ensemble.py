from pathlib import Path
import sys, math, json, time
import numpy as np, pandas as pd
from scipy.optimize import root
from scipy.stats import qmc
from numba import njit, prange
OUT=Path('/mnt/data/janus_n17_upstream_strengthening'); SRC=Path('/mnt/data/janus_n11_citation_novelty/source_provenance_corrected');sys.path.insert(0,str(SRC))
import janus_fourier_landscapes_v12 as J
base=np.array([7.9,.1,.1,131.9,1.2,85.4],float); half=np.array([.05,.05,.05,.05,.05,.05],float)
pos=J.make_hexagonal_flake(6); nom=J._from_shell_phase('nom',base[:3],base[3:]); S=J.contact_factors(1.5,nom.vectors,pos); xseed=np.array([1.5,.8660254037844386])

def eq_newton(land,xy,Fy):
 xy=xy.copy()
 for _ in range(40):
  _,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,Fy);gn=np.linalg.norm(g)
  if gn<1e-10:return True,xy
  try:st=np.linalg.solve(H,g)
  except:return False,xy
  al=1.;ok=False
  for __ in range(15):
   tr=xy-al*st; gn2=np.linalg.norm(J.contact_ugh(tr[0],tr[1],S,land,0,Fy)[1])
   if gn2<gn:xy=tr;ok=True;break
   al*=.5
  if not ok:return False,xy
 return False,xy

def fc_dir(land,xy0,sgn):
 xy=xy0.copy();rec=[]
 for f in np.arange(0,4.2,.02):
  ok,nxy=eq_newton(land,xy,sgn*f)
  if not ok:break
  xy=nxy; _,_,H=J.contact_ugh(xy[0],xy[1],S,land,0,sgn*f);ev=np.linalg.eigvalsh(H);rec.append((float(f),xy.copy(),ev))
  if ev[0]<5e-4:break
 near=min(rec[-15:],key=lambda z:abs(z[2][0]))
 def fun(z):
  _,g,H=J.contact_ugh(z[0],z[1],S,land,0,0); return np.array([g[0],np.linalg.det(H)])
 cand=[]
 for dx in [-.02,0,.02]:
  for dy in [-.02,0,.02]:
   rr=root(fun,near[1]+[dx,dy],tol=1e-11);res=np.linalg.norm(fun(rr.x));_,g,H=J.contact_ugh(rr.x[0],rr.x[1],S,land,0,0);fc=float(sgn*g[1]);ev=np.linalg.eigvalsh(H)
   if res<1e-6 and fc>0 and ev[1]>1e-5:cand.append((abs(fc-near[0]),fc))
 if not cand: raise RuntimeError('fold')
 cand.sort();return cand[0][1]

def evaluate(v,label):
 land=J._from_shell_phase(label,v[:3],v[3:]);rg=root(lambda z:J.contact_ugh(z[0],z[1],S,land,0,0)[1],xseed,jac=lambda z:J.contact_ugh(z[0],z[1],S,land,0,0)[2],tol=1e-11);xy=rg.x
 fp=fc_dir(land,xy,+1);fm=fc_dir(land,xy,-1)
 return dict(label=label,**{k:x for k,x in zip(['W1','W2','W3','phi1','phi2','phi3'],v)},ground_x=xy[0],ground_y=xy[1],Fplus=fp,Fminus=fm,Delta=fp-fm,rho=(fp-fm)/(fp+fm))
rows=[evaluate(base,'nominal')]
# central finite differences at publication rounding half intervals
for j,nm in enumerate(['W1','W2','W3','phi1','phi2','phi3']):
 for s in [-1,1]:
  v=base.copy();v[j]+=s*half[j];rows.append(evaluate(v,f'{nm}_{s:+d}half'))
# 16 LHS validation points across full published rounding hyperrectangle
X=qmc.scale(qmc.LatinHypercube(6,seed=2026091901).random(16),base-half,base+half)
for i,v in enumerate(X):rows.append(evaluate(v,f'lhs_{i:02d}'))
df=pd.DataFrame(rows);df.to_csv(OUT/'fr_m01_published_precision_static.csv',index=False)
# numerical gradients and linear worst-case bounds
gr=[]
for j,nm in enumerate(['W1','W2','W3','phi1','phi2','phi3']):
 lo=df[df.label==f'{nm}_-1half'].iloc[0];hi=df[df.label==f'{nm}_+1half'].iloc[0]
 for metric in ['Fplus','Fminus','Delta','rho']:
  gr.append(dict(parameter=nm,metric=metric,derivative=(hi[metric]-lo[metric])/(2*half[j]),half_interval=half[j],max_linear_contribution=abs((hi[metric]-lo[metric])/2)))
grad=pd.DataFrame(gr);grad.to_csv(OUT/'fr_m01_published_precision_gradients.csv',index=False)
nomr=df.iloc[0]
bounds={}
for metric in ['Fplus','Fminus','Delta','rho']:
 rad=grad[grad.metric==metric].max_linear_contribution.sum();bounds[metric]={'nominal':float(nomr[metric]),'linear_hyperrect_min':float(nomr[metric]-rad),'linear_hyperrect_max':float(nomr[metric]+rad),'lhs_min':float(df[df.label.str.startswith('lhs')][metric].min()),'lhs_max':float(df[df.label.str.startswith('lhs')][metric].max())}

# Canonical winding on nominal + 16 LHS points only.
sel=pd.concat([df.iloc[[0]],df[df.label.str.startswith('lhs')]],ignore_index=True)
vr=np.asarray(nom.vectors,float);sr=np.asarray(S.real,float);si=np.asarray(S.imag,float);cc=[];ss=[]
for _,r in sel.iterrows():
 l=J._from_shell_phase('q',[r.W1,r.W2,r.W3],[r.phi1,r.phi2,r.phi3]);cc.append(l.c_cos);ss.append(l.c_sin)
cc=np.asarray(cc);ss=np.asarray(ss);x0s=sel[['ground_x','ground_y']].to_numpy()
@njit
def gradf(x,y,c,s):
 gx=0.;gy=0.
 for k in range(vr.shape[0]):
  Gx=vr[k,0];Gy=vr[k,1];q=Gx*x+Gy*y;cq=math.cos(q);sq=math.sin(q);re=sr[k]*cq-si[k]*sq;im=sr[k]*sq+si[k]*cq;aa=-c[k]*im+s[k]*re;gx+=aa*Gx;gy+=aa*Gy
 return gx,gy
@njit
def step(z,t,dt,c,s):
 F0=2.;P=40.;gam=4.;om=2*math.pi/P;x,y,vx,vy=z;gx,gy=gradf(x,y,c,s);k1=np.array([vx,vy,-gx-gam*vx,F0*math.sin(om*t)-gy-gam*vy]);q=z+dt*k1/2;gx,gy=gradf(q[0],q[1],c,s);k2=np.array([q[2],q[3],-gx-gam*q[2],F0*math.sin(om*(t+dt/2))-gy-gam*q[3]]);q=z+dt*k2/2;gx,gy=gradf(q[0],q[1],c,s);k3=np.array([q[2],q[3],-gx-gam*q[2],F0*math.sin(om*(t+dt/2))-gy-gam*q[3]]);q=z+dt*k3;gx,gy=gradf(q[0],q[1],c,s);k4=np.array([q[2],q[3],-gx-gam*q[2],F0*math.sin(om*(t+dt))-gy-gam*q[3]]);return z+dt*(k1+2*k2+2*k3+k4)/6
@njit(parallel=True)
def runs(cc,ss,x0s):
 out=np.zeros((len(cc),5));spc=1500;dt=40./spc;sq3=math.sqrt(3.)
 for i in prange(len(cc)):
  z=np.array([x0s[i,0],x0s[i,1],0.,0.]);nstep=0
  for cyc in range(35):
   for _ in range(spc):z=step(z,nstep*dt,dt,cc[i],ss[i]);nstep+=1
  su=0.;sv=0.;same=1.;m0=999;n0=999
  for cyc in range(15):
   q=z.copy()
   for _ in range(spc):z=step(z,nstep*dt,dt,cc[i],ss[i]);nstep+=1
   dx=z[0]-q[0];dy=z[1]-q[1];v=2*dy/sq3;u=dx-.5*v;m=round(u);n=round(v)
   if cyc==0:m0=m;n0=n
   elif m!=m0 or n!=n0:same=0
   su+=u;sv+=v
  out[i]=[su/15,sv/15,round(su/15),round(sv/15),same]
 return out
A=runs(cc,ss,x0s);dyn=pd.DataFrame(A,columns=['u','v','m','n','all_same']);dyn.insert(0,'label',sel.label);dyn.to_csv(OUT/'fr_m01_published_precision_dynamics.csv',index=False)
summary={'contract':'publication rounding-resolution propagation only; not statistical fit uncertainty','n_lhs_validation':16,'bounds':bounds,'lhs_all_Delta_positive':bool((df[df.label.str.startswith('lhs')].Delta>0).all()),'dynamics_all_cycle_locked':bool((dyn.all_same==1).all()),'dynamics_winding_pairs':sorted([list(x) for x in {(int(m),int(n)) for m,n in dyn[['m','n']].to_numpy()}]),'source_fit_uncertainty_available':False,'remaining_limitation':'The accessed primary publication reports rounded Fourier coefficients but no coefficient covariance or machine-readable 9x9 GSFE raw-energy table. Actual DFT/fit uncertainty is therefore NOT_ASSESSABLE from public inputs; manuscript claims must remain conditional on the published Fourier model.'}
(OUT/'fr_m01_published_precision_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
