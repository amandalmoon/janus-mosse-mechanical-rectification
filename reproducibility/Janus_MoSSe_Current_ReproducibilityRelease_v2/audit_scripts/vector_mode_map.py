from pathlib import Path
_RELEASE_ROOT = Path(__file__).resolve().parents[1]
import sys, math, numpy as np, pandas as pd
from numba import njit, prange
from scipy.optimize import root
sys.path.insert(0,str(_RELEASE_ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); pos=J.make_hexagonal_flake(6); theta=1.5
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A); S=J.contact_factors(theta,land.vectors,pos)
vr=np.asarray(land.vectors,float); c=np.asarray(land.c_cos,float); s=np.asarray(land.c_sin,float); sr=np.asarray(S.real,float); si=np.asarray(S.imag,float)
def f0(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
def j0(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
x0=root(f0,np.zeros(2),jac=j0).x

@njit
def grad(x,y,vr,c,s,sr,si):
    gx=0.;gy=0.
    for k in range(vr.shape[0]):
        Gx=vr[k,0];Gy=vr[k,1];q=Gx*x+Gy*y;cq=math.cos(q);sq=math.sin(q)
        re=sr[k]*cq-si[k]*sq; im=sr[k]*sq+si[k]*cq; aa=-c[k]*im+s[k]*re
        gx+=aa*Gx;gy+=aa*Gy
    return gx,gy

@njit(parallel=True)
def batch(Fs,Ps,spc,n_eq,n_meas,x0,y0,vr,c,s,sr,si):
    n=len(Fs); out=np.zeros((n,8))
    gamma=4.
    for z in prange(n):
        F0=Fs[z];period=Ps[z];dt=period/spc;om=2*math.pi/period
        x=x0;y=y0;vx=0.;vy=0.; xm=x0;ym=y0
        total=(n_eq+n_meas)*spc
        for i in range(total):
            t=i*dt
            gx,gy=grad(x,y,vr,c,s,sr,si)
            a=vx;b=vy;c1=-gx-gamma*vx;d=F0*math.sin(om*t)-gy-gamma*vy
            gx2,gy2=grad(x+a*dt/2,y+b*dt/2,vr,c,s,sr,si)
            a2=vx+c1*dt/2;b2=vy+d*dt/2;c2=-gx2-gamma*a2;d2=F0*math.sin(om*(t+dt/2))-gy2-gamma*b2
            gx3,gy3=grad(x+a2*dt/2,y+b2*dt/2,vr,c,s,sr,si)
            a3=vx+c2*dt/2;b3=vy+d2*dt/2;c3=-gx3-gamma*a3;d3=F0*math.sin(om*(t+dt/2))-gy3-gamma*b3
            gx4,gy4=grad(x+a3*dt,y+b3*dt,vr,c,s,sr,si)
            a4=vx+c3*dt;b4=vy+d3*dt;c4=-gx4-gamma*a4;d4=F0*math.sin(om*(t+dt))-gy4-gamma*b4
            x+=dt*(a+2*a2+2*a3+a4)/6;y+=dt*(b+2*b2+2*b3+b4)/6
            vx+=dt*(c1+2*c2+2*c3+c4)/6;vy+=dt*(d+2*d2+2*d3+d4)/6
            if i==n_eq*spc-1: xm=x;ym=y
        dx=(x-xm)/n_meas;dy=(y-ym)/n_meas
        vv=2*dy/math.sqrt(3.0);uu=dx-.5*vv;mi=round(uu);ni=round(vv)
        du=uu-mi;dv=vv-ni;rx=du+.5*dv;ry=(math.sqrt(3.0)/2)*dv;res=math.sqrt(rx*rx+ry*ry)
        out[z]=[F0,period,uu,vv,mi,ni,res,dy]
    return out

Fgrid=np.round(np.arange(1.0,4.0001,.25),2)
Pgrid=np.array([20.,30.,40.,50.,60.,70.,80.])
Fs=[];Ps=[]
for P in Pgrid:
  for F in Fgrid: Fs.append(F);Ps.append(P)
arr=batch(np.array(Fs),np.array(Ps),4000,20,40,x0[0],x0[1],vr,c,s,sr,si)
df=pd.DataFrame(arr,columns=['F0','period','u_per_cycle','v_per_cycle','m','n','lock_residual','dy_per_cycle'])
df['locked']=df.lock_residual<1e-4
print('cases',len(df),'locked',df.locked.sum(),'maxres',df.lock_residual.max())
print('unique windings',sorted(set(zip(df.m.astype(int),df.n.astype(int)))))
print(df.pivot(index='period',columns='F0',values='n').to_string())
df.to_csv(str(_RELEASE_ROOT/'data'/'canonical'/'vector_mode_map_F0_period.csv'),index=False)
