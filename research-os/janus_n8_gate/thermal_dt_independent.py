from pathlib import Path
import sys,math,time
import numpy as np,pandas as pd
from numba import njit,prange
from scipy.optimize import root
SRC=Path('/mnt/data/janus_n8_gate/rigid_release/Janus_MoSSe_AuditResolved_ReproducibilityRelease/source');sys.path.insert(0,str(SRC))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');positions=J.make_hexagonal_flake(6);theta=1.5;F0=2.;period=40.;gamma=4.
S=J.contact_factors(theta,land.vectors,positions);vr=np.asarray(land.vectors,float);cc=np.asarray(land.c_cos,float);ss=np.asarray(land.c_sin,float);sr=np.asarray(S.real,float);si=np.asarray(S.imag,float)
def f0(x):return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
def j0(x):return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
rr=root(f0,np.zeros(2),jac=j0,method='hybr');x0,y0=rr.x
@njit
def grad(x,y,vr,c,s,sr,si):
 gx=0.;gy=0.
 for k in range(vr.shape[0]):
  Gx=vr[k,0];Gy=vr[k,1];q=Gx*x+Gy*y;cq=math.cos(q);sq=math.sin(q);re=sr[k]*cq-si[k]*sq;im=sr[k]*sq+si[k]*cq;aa=-c[k]*im+s[k]*re;gx+=aa*Gx;gy+=aa*Gy
 return gx,gy
@njit
def detstate(x0,y0,vr,c,s,sr,si):
 spc=4000;dt=period/spc;om=2*math.pi/period;x=x0;y=y0;vx=0.;vy=0.
 def der(t,x,y,vx,vy):
  gx,gy=grad(x,y,vr,c,s,sr,si);return vx,vy,-gx-gamma*vx,F0*math.sin(om*t)-gy-gamma*vy
 for i in range(200*spc):
  t=i*dt;a,b,c1,d=der(t,x,y,vx,vy);a2,b2,c2,d2=der(t+dt/2,x+a*dt/2,y+b*dt/2,vx+c1*dt/2,vy+d*dt/2);a3,b3,c3,d3=der(t+dt/2,x+a2*dt/2,y+b2*dt/2,vx+c2*dt/2,vy+d2*dt/2);a4,b4,c4,d4=der(t+dt,x+a3*dt,y+b3*dt,vx+c3*dt,vy+d3*dt);x+=dt*(a+2*a2+2*a3+a4)/6;y+=dt*(b+2*b2+2*b3+b4)/6;vx+=dt*(c1+2*c2+2*c3+c4)/6;vy+=dt*(d+2*d2+2*d3+d4)/6
 return x,y,vx,vy
@njit(parallel=True)
def ens(ntraj,seed,T,dt,xinit,yinit,vxinit,vyinit,vr,c,s,sr,si):
 spc=int(round(period/dt));burn=10;meas=10;tot=(burn+meas)*spc;om=2*math.pi/period;oc=math.exp(-gamma*dt);sig=math.sqrt(T*(1-oc*oc));mu=np.empty(ntraj);mv=np.empty(ntraj);pt=np.empty(ntraj)
 for r in prange(ntraj):
  np.random.seed(seed+r);x=xinit;y=yinit;X=xinit;Y=yinit;vx=vxinit;vy=vyinit;xp=0.;yp=0.;su=0.;sv=0.;tar=0.;k=0
  for i in range(tot):
   t=i*dt;gx,gy=grad(x,y,vr,c,s,sr,si);fy=F0*math.sin(om*t);vx+=.5*dt*(-gx);vy+=.5*dt*(fy-gy);dx=.5*dt*vx;dy=.5*dt*vy;x+=dx;y+=dy;X+=dx;Y+=dy;vv=2*y/math.sqrt(3);uu=x-.5*vv;iu=round(uu);iv=round(vv);x-=iu+.5*iv;y-=math.sqrt(3)/2*iv;vx=oc*vx+sig*np.random.randn();vy=oc*vy+sig*np.random.randn();dx=.5*dt*vx;dy=.5*dt*vy;x+=dx;y+=dy;X+=dx;Y+=dy;vv=2*y/math.sqrt(3);uu=x-.5*vv;iu=round(uu);iv=round(vv);x-=iu+.5*iv;y-=math.sqrt(3)/2*iv;t2=(i+1)*dt;gx,gy=grad(x,y,vr,c,s,sr,si);fy=F0*math.sin(om*t2);vx+=.5*dt*(-gx);vy+=.5*dt*(fy-gy)
   if (i+1)%spc==0:
    cyc=(i+1)//spc
    if cyc==burn:xp=X;yp=Y
    elif cyc>burn:
     ddx=X-xp;ddy=Y-yp;xp=X;yp=Y;vv=2*ddy/math.sqrt(3);uu=ddx-.5*vv;su+=uu;sv+=vv;k+=1
     if round(uu)==1 and round(vv)==-1:tar+=1
  mu[r]=su/k;mv[r]=sv/k;pt[r]=tar/k
 return mu,mv,pt
st=detstate(x0,y0,vr,cc,ss,sr,si);A=np.column_stack([J.A1,J.A2]);uv=np.linalg.solve(A,np.array(st[:2]));xy=np.array(st[:2])-A@np.round(uv);st=(xy[0],xy[1],st[2],st[3])
# compile
ens(2,1,1e-4,.04,*st,vr,cc,ss,sr,si)
rows=[];N=300
for T in [1e-4,1e-3,5e-3]:
 for dt in [.04,.02,.01]:
  t=time.time();mu,mv,pt=ens(N,2026091900,T,dt,*st,vr,cc,ss,sr,si);rows.append(dict(T=T,dt=dt,n=N,mean_u=mu.mean(),se_u=mu.std(ddof=1)/np.sqrt(N),mean_v=mv.mean(),se_v=mv.std(ddof=1)/np.sqrt(N),Ptarget=pt.mean(),seconds=time.time()-t));print(rows[-1],flush=True)
df=pd.DataFrame(rows);df.to_csv('/mnt/data/janus_n8_gate/n8_thermal_dt_independent.csv',index=False)
