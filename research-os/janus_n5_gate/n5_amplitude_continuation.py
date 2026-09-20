from pathlib import Path
import sys,math,numpy as np,pandas as pd
from scipy.optimize import root
from numba import njit
ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease');sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');pos=J.make_hexagonal_flake(6);theta=1.5;P=40.;gamma=4.;spc=4000
S=J.contact_factors(theta,land.vectors,pos);vr=np.asarray(land.vectors,float);c=np.asarray(land.c_cos,float);s=np.asarray(land.c_sin,float);sr=S.real.copy();si=S.imag.copy()
def f0(x):return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
def j0(x):return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
x0=root(f0,np.zeros(2),jac=j0,tol=1e-12).x
@njit
def grad(x,y,vr,c,s,sr,si):
 g0=g1=0.
 for k in range(vr.shape[0]):
  Gx=vr[k,0];Gy=vr[k,1];q=Gx*x+Gy*y;cq=math.cos(q);sq=math.sin(q);re=sr[k]*cq-si[k]*sq;im=sr[k]*sq+si[k]*cq;aa=-c[k]*im+s[k]*re;g0+=aa*Gx;g1+=aa*Gy
 return g0,g1
@njit
def step(z,t,dt,F0):
 x,y,vx,vy=z;om=2*math.pi/P;gx,gy=grad(x,y,vr,c,s,sr,si);k1=np.array([vx,vy,-gx-gamma*vx,F0*math.sin(om*t)-gy-gamma*vy]);q=z+dt*k1/2;gx,gy=grad(q[0],q[1],vr,c,s,sr,si);k2=np.array([q[2],q[3],-gx-gamma*q[2],F0*math.sin(om*(t+dt/2))-gy-gamma*q[3]]);q=z+dt*k2/2;gx,gy=grad(q[0],q[1],vr,c,s,sr,si);k3=np.array([q[2],q[3],-gx-gamma*q[2],F0*math.sin(om*(t+dt/2))-gy-gamma*q[3]]);q=z+dt*k3;gx,gy=grad(q[0],q[1],vr,c,s,sr,si);k4=np.array([q[2],q[3],-gx-gamma*q[2],F0*math.sin(om*(t+dt))-gy-gamma*q[3]]);return z+dt*(k1+2*k2+2*k3+k4)/6
@njit
def run_amp(z0,F0,neq,nmeas):
 z=z0.copy();dt=P/spc;stepn=0
 for cyc in range(neq):
  for j in range(spc):z=step(z,stepn*dt,dt,F0);stepn+=1
 zm=z.copy()
 for cyc in range(nmeas):
  for j in range(spc):z=step(z,stepn*dt,dt,F0);stepn+=1
 d=(z[:2]-zm[:2])/nmeas;v=2*d[1]/math.sqrt(3);u=d[0]-.5*v;m=round(u);n=round(v);du=u-m;dv=v-n;res=math.sqrt((du+.5*dv)**2+((math.sqrt(3)/2)*dv)**2);return z,u,v,m,n,res
Fgrid=np.round(np.arange(1.,4.0001,.05),2)
rows=[]
# inc
z=np.array([x0[0],x0[1],0.,0.])
for i,F in enumerate(Fgrid):
 z,u,v,m,n,res=run_amp(z,F,20 if i==0 else 10,20);rows.append(['inc',F,u,v,int(m),int(n),res,*z])
# dec: settle at high amplitude from ground first
z=np.array([x0[0],x0[1],0.,0.])
for i,F in enumerate(Fgrid[::-1]):
 z,u,v,m,n,res=run_amp(z,F,40 if i==0 else 10,20);rows.append(['dec',F,u,v,int(m),int(n),res,*z])
df=pd.DataFrame(rows,columns=['direction','F0','u','v','m','n','res','x','y','vx','vy']);df.to_csv('/mnt/data/janus_n5_gate/n5_amplitude_continuation_61x2.csv',index=False)
a=df[df.direction=='inc'].sort_values('F0');b=df[df.direction=='dec'].sort_values('F0');cmp=a[['F0','m','n']].merge(b[['F0','m','n']],on='F0',suffixes=('_inc','_dec'));cmp['match']=(cmp.m_inc==cmp.m_dec)&(cmp.n_inc==cmp.n_dec);cmp.to_csv('/mnt/data/janus_n5_gate/n5_amplitude_continuation_compare.csv',index=False)
print('matches',cmp.match.sum(),'of',len(cmp),'max res',df.res.max());print(cmp[~cmp.match].to_string(index=False))
print(cmp.to_string(index=False))
