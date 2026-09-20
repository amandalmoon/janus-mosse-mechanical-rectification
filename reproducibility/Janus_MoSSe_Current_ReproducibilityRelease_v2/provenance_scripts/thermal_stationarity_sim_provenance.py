from pathlib import Path
import sys,math,time,argparse,numpy as np
from numba import njit,prange
from scipy.optimize import root
ap=argparse.ArgumentParser();ap.add_argument('--T',type=float,required=True);ap.add_argument('--N',type=int,default=500);ap.add_argument('--cycles',type=int,default=160);ap.add_argument('--seed',type=int,default=2026091900);ap.add_argument('--start',choices=['orbit','ground','meta'],default='orbit');args=ap.parse_args()
OUT=Path('/mnt/data/janus_redteam_gate/rtb01');OUT.mkdir(parents=True,exist_ok=True)
SRC=Path('/mnt/data/janus_n8_gate/rigid_release/Janus_MoSSe_AuditResolved_ReproducibilityRelease/source');sys.path.insert(0,str(SRC));import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');pos=J.make_hexagonal_flake(6);theta=1.5;F0=2.;period=40.;gamma=4.;S=J.contact_factors(theta,land.vectors,pos);vr=np.asarray(land.vectors,float);cc=np.asarray(land.c_cos,float);ss=np.asarray(land.c_sin,float);sr=np.asarray(S.real,float);si=np.asarray(S.imag,float)
def f0(x):return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
def j0(x):return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
ground=root(f0,np.zeros(2),jac=j0).x
@njit
def grad(x,y):
 gx=0.;gy=0.
 for k in range(vr.shape[0]):
  Gx=vr[k,0];Gy=vr[k,1];q=Gx*x+Gy*y;cq=math.cos(q);sq=math.sin(q);re=sr[k]*cq-si[k]*sq;im=sr[k]*sq+si[k]*cq;aa=-cc[k]*im+ss[k]*re;gx+=aa*Gx;gy+=aa*Gy
 return gx,gy
@njit
def detstate():
 spc=4000;dt=period/spc;om=2*math.pi/period;x=ground[0];y=ground[1];vx=0.;vy=0.
 def der(t,x,y,vx,vy):
  gx,gy=grad(x,y);return vx,vy,-gx-gamma*vx,F0*math.sin(om*t)-gy-gamma*vy
 for i in range(200*spc):
  t=i*dt;a,b,c1,d=der(t,x,y,vx,vy);a2,b2,c2,d2=der(t+dt/2,x+a*dt/2,y+b*dt/2,vx+c1*dt/2,vy+d*dt/2);a3,b3,c3,d3=der(t+dt/2,x+a2*dt/2,y+b2*dt/2,vx+c2*dt/2,vy+d2*dt/2);a4,b4,c4,d4=der(t+dt,x+a3*dt,y+b3*dt,vx+c3*dt,vy+d3*dt);x+=dt*(a+2*a2+2*a3+a4)/6;y+=dt*(b+2*b2+2*b3+b4)/6;vx+=dt*(c1+2*c2+2*c3+c4)/6;vy+=dt*(d+2*d2+2*d3+d4)/6
 return x,y,vx,vy
@njit(parallel=True)
def ens_cycle(ntraj,seed,T,ncycles,xinit,yinit,vxinit,vyinit):
 dt=.02;spc=int(round(period/dt));tot=ncycles*spc;om=2*math.pi/period;oc=math.exp(-gamma*dt);sig=math.sqrt(T*(1-oc*oc));out_u=np.empty((ntraj,ncycles));out_v=np.empty((ntraj,ncycles))
 for r in prange(ntraj):
  np.random.seed(seed+r);x=xinit;y=yinit;X=xinit;Y=yinit;vx=vxinit;vy=vyinit;xp=X;yp=Y
  for i in range(tot):
   t=i*dt;gx,gy=grad(x,y);fy=F0*math.sin(om*t);vx+=.5*dt*(-gx);vy+=.5*dt*(fy-gy);dx=.5*dt*vx;dy=.5*dt*vy;x+=dx;y+=dy;X+=dx;Y+=dy;vv=2*y/math.sqrt(3);uu=x-.5*vv;iu=round(uu);iv=round(vv);x-=iu+.5*iv;y-=math.sqrt(3)/2*iv;vx=oc*vx+sig*np.random.randn();vy=oc*vy+sig*np.random.randn();dx=.5*dt*vx;dy=.5*dt*vy;x+=dx;y+=dy;X+=dx;Y+=dy;vv=2*y/math.sqrt(3);uu=x-.5*vv;iu=round(uu);iv=round(vv);x-=iu+.5*iv;y-=math.sqrt(3)/2*iv;t2=(i+1)*dt;gx,gy=grad(x,y);fy=F0*math.sin(om*t2);vx+=.5*dt*(-gx);vy+=.5*dt*(fy-gy)
   if (i+1)%spc==0:
    cyc=(i+1)//spc;ddx=X-xp;ddy=Y-yp;xp=X;yp=Y;vv=2*ddy/math.sqrt(3);uu=ddx-.5*vv;out_u[r,cyc-1]=uu;out_v[r,cyc-1]=vv
 return out_u,out_v
st=detstate();A=np.column_stack([J.A1,J.A2]);uv=np.linalg.solve(A,np.array(st[:2]));xy=np.array(st[:2])-A@np.round(uv);orbit=(xy[0],xy[1],st[2],st[3]);meta=(.5,1/(2*math.sqrt(3)),0.,0.);starts={'orbit':orbit,'ground':(ground[0],ground[1],0.,0.),'meta':meta};s0=starts[args.start]
ens_cycle(2,1,args.T,2,*s0)
t=time.time();u,v=ens_cycle(args.N,args.seed,args.T,args.cycles,*s0);dt=time.time()-t
p=OUT/f'cycles_T{args.T:.2f}_N{args.N}_C{args.cycles}_{args.start}_seed{args.seed}.npz';np.savez_compressed(p,u=u,v=v,T=args.T,N=args.N,cycles=args.cycles,start=args.start,seed=args.seed);print(p);print('sec',dt,'overall',u.mean(),v.mean())
