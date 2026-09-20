from pathlib import Path
import sys, math, time
import numpy as np
import pandas as pd
from numba import njit, prange
from scipy.optimize import root
from scipy.stats import f

OUT=Path('/mnt/data/janus_redteam_gate/rtb01')
OUT.mkdir(parents=True,exist_ok=True)
SRC=Path('/mnt/data/janus_n8_gate/rigid_release/Janus_MoSSe_AuditResolved_ReproducibilityRelease/source')
sys.path.insert(0,str(SRC))
import janus_fourier_landscapes_v12 as J

land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');pos=J.make_hexagonal_flake(6)
theta=1.5;F0=2.;period=40.;gamma=4.
S=J.contact_factors(theta,land.vectors,pos)
vr=np.asarray(land.vectors,float);cc=np.asarray(land.c_cos,float);ss=np.asarray(land.c_sin,float);sr=np.asarray(S.real,float);si=np.asarray(S.imag,float)

def f0(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
def j0(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
ground=root(f0,np.zeros(2),jac=j0).x

@njit
def grad(x,y):
    gx=0.;gy=0.
    for k in range(vr.shape[0]):
        Gx=vr[k,0];Gy=vr[k,1];q=Gx*x+Gy*y
        cq=math.cos(q);sq=math.sin(q)
        re=sr[k]*cq-si[k]*sq;im=sr[k]*sq+si[k]*cq
        aa=-cc[k]*im+ss[k]*re;gx+=aa*Gx;gy+=aa*Gy
    return gx,gy

@njit
def detstate():
    spc=4000;dt=period/spc;om=2*math.pi/period
    x=ground[0];y=ground[1];vx=0.;vy=0.
    def der(t,x,y,vx,vy):
        gx,gy=grad(x,y)
        return vx,vy,-gx-gamma*vx,F0*math.sin(om*t)-gy-gamma*vy
    for i in range(200*spc):
        t=i*dt
        a,b,c1,d=der(t,x,y,vx,vy)
        a2,b2,c2,d2=der(t+dt/2,x+a*dt/2,y+b*dt/2,vx+c1*dt/2,vy+d*dt/2)
        a3,b3,c3,d3=der(t+dt/2,x+a2*dt/2,y+b2*dt/2,vx+c2*dt/2,vy+d2*dt/2)
        a4,b4,c4,d4=der(t+dt,x+a3*dt,y+b3*dt,vx+c3*dt,vy+d3*dt)
        x+=dt*(a+2*a2+2*a3+a4)/6;y+=dt*(b+2*b2+2*b3+b4)/6
        vx+=dt*(c1+2*c2+2*c3+c4)/6;vy+=dt*(d+2*d2+2*d3+d4)/6
    return x,y,vx,vy

@njit(parallel=True)
def ens_cycle(ntraj,seed,T,ncycles,xinit,yinit,vxinit,vyinit):
    dt=.02;spc=int(round(period/dt));tot=ncycles*spc;om=2*math.pi/period
    oc=math.exp(-gamma*dt);sig=math.sqrt(T*(1-oc*oc))
    out_u=np.empty((ntraj,ncycles));out_v=np.empty((ntraj,ncycles))
    for r in prange(ntraj):
        np.random.seed(seed+r)
        x=xinit;y=yinit;X=xinit;Y=yinit;vx=vxinit;vy=vyinit;xp=X;yp=Y
        for i in range(tot):
            t=i*dt;gx,gy=grad(x,y);fy=F0*math.sin(om*t)
            vx+=.5*dt*(-gx);vy+=.5*dt*(fy-gy)
            dx=.5*dt*vx;dy=.5*dt*vy;x+=dx;y+=dy;X+=dx;Y+=dy
            vv=2*y/math.sqrt(3);uu=x-.5*vv;iu=round(uu);iv=round(vv);x-=iu+.5*iv;y-=math.sqrt(3)/2*iv
            vx=oc*vx+sig*np.random.randn();vy=oc*vy+sig*np.random.randn()
            dx=.5*dt*vx;dy=.5*dt*vy;x+=dx;y+=dy;X+=dx;Y+=dy
            vv=2*y/math.sqrt(3);uu=x-.5*vv;iu=round(uu);iv=round(vv);x-=iu+.5*iv;y-=math.sqrt(3)/2*iv
            t2=(i+1)*dt;gx,gy=grad(x,y);fy=F0*math.sin(om*t2)
            vx+=.5*dt*(-gx);vy+=.5*dt*(fy-gy)
            if (i+1)%spc==0:
                cyc=(i+1)//spc
                ddx=X-xp;ddy=Y-yp;xp=X;yp=Y
                vv=2*ddy/math.sqrt(3);uu=ddx-.5*vv
                out_u[r,cyc-1]=uu;out_v[r,cyc-1]=vv
    return out_u,out_v

def hotell(X):
    n,p=X.shape; m=X.mean(0); S=np.cov(X,rowvar=False,ddof=1); Si=np.linalg.inv(S)
    T2=float(n*m@Si@m);crit=float(p*(n-1)/(n-p)*f.ppf(.95,p,n-p))
    return m,S,T2,crit,T2>crit

def paired_drift(X1,X2):
    return hotell(X2-X1)

def boot_zero(X,seed,B=20000):
    n=len(X);m=X.mean(0);rng=np.random.default_rng(seed);bm=np.empty((B,2))
    for b0 in range(0,B,250):
        bs=min(250,B-b0);idx=rng.integers(0,n,size=(bs,n));bm[b0:b0+bs]=X[idx].mean(1)
    C=np.cov(bm-m,rowvar=False,ddof=1);Ci=np.linalg.inv(C);d=bm-m;d2=np.einsum('bi,ij,bj->b',d,Ci,d)
    q95=float(np.quantile(d2,.95));z=float(m@Ci@m)
    return z,q95,z>q95

st=detstate();A=np.column_stack([J.A1,J.A2]);uv=np.linalg.solve(A,np.array(st[:2]));xy=np.array(st[:2])-A@np.round(uv);orbit=(xy[0],xy[1],st[2],st[3])
# compile
ens_cycle(2,1,.6,2,*orbit)
TEMPS=[.50,.55,.60,.65,.70];N=1000;NC=160
windows={'b10_m20':(10,30),'b30_m20':(30,50),'b60_m20':(60,80),'b100_m20':(100,120),'b140_m20':(140,160)}
rows=[];dr=[]
for ti,T in enumerate(TEMPS):
    p=OUT/f'cycles_T{T:.2f}_N{N}.npz'
    if p.exists():
        z=np.load(p);u=z['u'];v=z['v'];print('load',T)
    else:
        t0=time.time();u,v=ens_cycle(N,2026091900+ti*100000,T,NC,*orbit);np.savez_compressed(p,u=u,v=v);print('sim',T,'sec',time.time()-t0)
    blocks={}
    for name,(a,b) in windows.items():
        X=np.column_stack([u[:,a:b].mean(1),v[:,a:b].mean(1)]);blocks[name]=X
        m,S,T2,crit,exc=hotell(X)
        bz,bq,bexc=(np.nan,np.nan,np.nan)
        if name in ('b60_m20','b100_m20','b140_m20'):
            bz,bq,bexc=boot_zero(X,20260919+ti*100+int(a),B=20000)
        pneg=(v[:,a:b]<0).mean(1).mean()
        ru=np.rint(u[:,a:b]);rv=np.rint(v[:,a:b]);ptarg=((ru==1)&(rv==-1)).mean(1).mean()
        rows.append(dict(T=T,window=name,burn=a,measure=b-a,n=N,mean_u=m[0],mean_v=m[1],norm=float(np.linalg.norm(m)),se_u=np.sqrt(S[0,0]/N),se_v=np.sqrt(S[1,1]/N),hotelling_T2=T2,hotelling_crit95=crit,zero_excluded_hotelling=exc,bootstrap_zero_d2=bz,bootstrap_q95=bq,zero_excluded_bootstrap=bexc,P_neg_y=pneg,P_target=ptarg))
    for n1,n2 in [('b30_m20','b60_m20'),('b60_m20','b100_m20'),('b100_m20','b140_m20')]:
        m,S,T2,crit,exc=paired_drift(blocks[n1],blocks[n2]);dr.append(dict(T=T,from_window=n1,to_window=n2,delta_u=m[0],delta_v=m[1],delta_norm=float(np.linalg.norm(m)),se_delta_u=np.sqrt(S[0,0]/N),se_delta_v=np.sqrt(S[1,1]/N),paired_T2=T2,crit95=crit,drift_detected=exc))

pd.DataFrame(rows).to_csv(OUT/'orbit_block_stationarity.csv',index=False)
pd.DataFrame(dr).to_csv(OUT/'orbit_paired_drift.csv',index=False)
# cycle ensemble means for plotting/inspection
cyrows=[]
for ti,T in enumerate(TEMPS):
    z=np.load(OUT/f'cycles_T{T:.2f}_N{N}.npz');u=z['u'];v=z['v']
    for c in range(NC):
        cyrows.append(dict(T=T,cycle=c+1,mean_u=u[:,c].mean(),mean_v=v[:,c].mean(),se_u=u[:,c].std(ddof=1)/np.sqrt(N),se_v=v[:,c].std(ddof=1)/np.sqrt(N)))
pd.DataFrame(cyrows).to_csv(OUT/'orbit_cycle_means.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))
print('\nDRIFT')
print(pd.DataFrame(dr).to_string(index=False))
