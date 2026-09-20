from pathlib import Path
import sys,math,json
import numpy as np,pandas as pd
from numba import njit,prange
from scipy.optimize import root
OUT=Path('/mnt/data/janus_n17_upstream_strengthening');ROOT=Path('/mnt/data/janus_n11_citation_novelty/source_provenance_corrected');sys.path.insert(0,str(ROOT))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');pos=J.make_hexagonal_flake(6);S=J.contact_factors(1.5,land.vectors,pos)
vr=np.asarray(land.vectors,float);c=np.asarray(land.c_cos,float);s=np.asarray(land.c_sin,float);sr=np.asarray(S.real,float);si=np.asarray(S.imag,float)
def f0(x):return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
def j0(x):return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
x0=root(f0,np.array([1.5,.8660254037844386]),jac=j0,tol=1e-12).x
@njit
def grad(x,y):
 gx=0.;gy=0.
 for k in range(vr.shape[0]):
  Gx=vr[k,0];Gy=vr[k,1];q=Gx*x+Gy*y;cq=math.cos(q);sq=math.sin(q);re=sr[k]*cq-si[k]*sq;im=sr[k]*sq+si[k]*cq;aa=-c[k]*im+s[k]*re;gx+=aa*Gx;gy+=aa*Gy
 return gx,gy
@njit
def step(z,t,dt,F0,P,gamma):
 x,y,vx,vy=z;om=2*math.pi/P;gx,gy=grad(x,y);k1=np.array([vx,vy,-gx-gamma*vx,F0*math.sin(om*t)-gy-gamma*vy]);q=z+dt*k1/2;gx,gy=grad(q[0],q[1]);k2=np.array([q[2],q[3],-gx-gamma*q[2],F0*math.sin(om*(t+dt/2))-gy-gamma*q[3]]);q=z+dt*k2/2;gx,gy=grad(q[0],q[1]);k3=np.array([q[2],q[3],-gx-gamma*q[2],F0*math.sin(om*(t+dt/2))-gy-gamma*q[3]]);q=z+dt*k3;gx,gy=grad(q[0],q[1]);k4=np.array([q[2],q[3],-gx-gamma*q[2],F0*math.sin(om*(t+dt))-gy-gamma*q[3]]);return z+dt*(k1+2*k2+2*k3+k4)/6
@njit(parallel=True)
def run(gs,Fs,Ps):
 n=len(gs);out=np.zeros((n,9));sq3=math.sqrt(3.);spc=2000
 for ii in prange(n):
  gam=gs[ii];F0=Fs[ii];P=Ps[ii];dt=P/spc;z=np.array([x0[0],x0[1],0.,0.]);istep=0
  for cyc in range(40):
   for _ in range(spc):z=step(z,istep*dt,dt,F0,P,gam);istep+=1
  su=0.;sv=0.;same=1.;fm=999.;fn=999.;mx=0.
  for cyc in range(20):
   q=z.copy()
   for _ in range(spc):z=step(z,istep*dt,dt,F0,P,gam);istep+=1
   dx=z[0]-q[0];dy=z[1]-q[1];vv=2*dy/sq3;uu=dx-.5*vv;m=round(uu);nn=round(vv);du=uu-m;dv=vv-nn;rr=math.sqrt((du+.5*dv)**2+(sq3*.5*dv)**2);mx=max(mx,rr)
   if cyc==0:fm=m;fn=nn
   elif m!=fm or nn!=fn:same=0
   su+=uu;sv+=vv
  mu=su/20;mv=sv/20;out[ii]=[gam,F0,P,mu,mv,round(mu),round(mv),mx,same]
 return out

gammas=[2.,3.,4.,5.,6.,8.];Fvals=[1.4,2.0,2.6,3.0];Pvals=[30.,40.,60.]
g=[];F=[];P=[]
for tau in Pvals:
 for f in Fvals:
  for gam in gammas:g.append(gam);F.append(f);P.append(tau)
arr=run(np.array(g),np.array(F),np.array(P));df=pd.DataFrame(arr,columns=['gamma','F0','tau','u','v','m','n','max_cycle_res','all_same'])
df['integer_pair']=df.apply(lambda r:f"({int(r.m)},{int(r.n)})",axis=1);df.to_csv(OUT/'fr_m02_joint_gamma_drive_map.csv',index=False)
# gamma=4 reference winding at each drive point; see how many gamma values preserve it.
rows=[]
for (F0,tau),q in df.groupby(['F0','tau']):
 ref=q[q.gamma==4].iloc[0];pair=(int(ref.m),int(ref.n));matches=((q.m==pair[0])&(q.n==pair[1])&(q.all_same==1)).sum()
 rows.append(dict(F0=F0,tau=tau,reference_pair=f'({pair[0]},{pair[1]})',n_gamma=len(q),n_match_reference=int(matches),fraction_match_reference=float(matches/len(q)),n_unique_pairs=int(q.integer_pair.nunique()),all_cycle_locked=bool((q.all_same==1).all()),unique_pairs=';'.join(sorted(q.integer_pair.unique()))))
s=pd.DataFrame(rows).sort_values(['tau','F0']);s.to_csv(OUT/'fr_m02_drivepoint_summary.csv',index=False)
summary={'n_points':len(df),'gammas':gammas,'F0':Fvals,'tau':Pvals,'all_points_cycle_locked':bool((df.all_same==1).all()),'n_drivepoints':len(s),'drivepoints_invariant_across_all_gamma':int((s.fraction_match_reference==1).sum()),'median_fraction_preserve_gamma4_winding':float(s.fraction_match_reference.median()),'min_fraction_preserve_gamma4_winding':float(s.fraction_match_reference.min()),'max_unique_winding_pairs_at_one_drivepoint':int(s.n_unique_pairs.max()),'interpretation':'Damping and drive interact strongly: the integer winding map is not gamma-invariant. The canonical gamma=4 map remains a valid declared-protocol result, not a material-only phase diagram.'}
(OUT/'fr_m02_joint_gamma_drive_summary.json').write_text(json.dumps(summary,indent=2));print(df.to_string(index=False));print(json.dumps(summary,indent=2))
