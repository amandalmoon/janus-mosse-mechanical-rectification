from pathlib import Path
import sys,math,numpy as np,pandas as pd
from numba import njit,prange
from scipy.optimize import root
ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease');sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');pos=J.make_hexagonal_flake(6);S=J.contact_factors(1.5,land.vectors,pos)
vr=np.asarray(land.vectors,float);c=np.asarray(land.c_cos,float);s=np.asarray(land.c_sin,float);sr=np.asarray(S.real,float);si=np.asarray(S.imag,float)
def f0(x):return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
def j0(x):return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
x0=root(f0,np.zeros(2),jac=j0,tol=1e-12).x
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
def run(gs):
 out=np.zeros((len(gs),8));P=40.;F0=2.;spc=4000;dt=P/spc;sq3=math.sqrt(3.)
 for ii in prange(len(gs)):
  gam=gs[ii];z=np.array([x0[0],x0[1],0.,0.]);istep=0
  for cyc in range(40):
   for j in range(spc):z=step(z,istep*dt,dt,F0,P,gam);istep+=1
  su=0.;sv=0.;same=1.;fm=999;fn=999;mx=0.
  for cyc in range(20):
   s0=z.copy()
   for j in range(spc):z=step(z,istep*dt,dt,F0,P,gam);istep+=1
   dx=z[0]-s0[0];dy=z[1]-s0[1];vv=2*dy/sq3;uu=dx-.5*vv;m=round(uu);n=round(vv);du=uu-m;dv=vv-n;rr=math.sqrt((du+.5*dv)**2+(sq3*.5*dv)**2);mx=max(mx,rr)
   if cyc==0:fm=m;fn=n
   elif m!=fm or n!=fn:same=0
   su+=uu;sv+=vv
  mu=su/20;mv=sv/20;out[ii]=[gam,mu,mv,round(mu),round(mv),mx,same,math.hypot(mu-round(mu),mv-round(mv))]
 return out
g=np.array([0.5,1.,2.,3.,4.,5.,6.,8.,10.])
a=run(g);df=pd.DataFrame(a,columns=['gamma','u','v','m','n','max_cycle_res','all_same','simple_mean_res']);df.to_csv('/mnt/data/janus_n5_gate/redteam_gamma_sweep.csv',index=False);print(df.to_string(index=False))
