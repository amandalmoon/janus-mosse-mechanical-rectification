from pathlib import Path
import sys, math, numpy as np, pandas as pd
from numba import njit, prange
from scipy.optimize import root
ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); pos=J.make_hexagonal_flake(6); theta=1.5
S=J.contact_factors(theta,land.vectors,pos); vr=np.asarray(land.vectors,float); c=np.asarray(land.c_cos,float); s=np.asarray(land.c_sin,float); sr=S.real.copy(); si=S.imag.copy()
def f0(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
def j0(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
x0=root(f0,np.zeros(2),jac=j0,tol=1e-12).x
@njit
def grad(x,y,vr,c,s,sr,si):
    gx=0.;gy=0.
    for k in range(vr.shape[0]):
        Gx=vr[k,0];Gy=vr[k,1];q=Gx*x+Gy*y;cq=math.cos(q);sq=math.sin(q)
        re=sr[k]*cq-si[k]*sq; im=sr[k]*sq+si[k]*cq; aa=-c[k]*im+s[k]*re
        gx+=aa*Gx;gy+=aa*Gy
    return gx,gy
@njit
def step(x,y,vx,vy,t,dt,F0,P,vr,c,s,sr,si):
    gm=4.; om=2*math.pi/P
    gx,gy=grad(x,y,vr,c,s,sr,si); a=vx;b=vy;c1=-gx-gm*vx;d=F0*math.sin(om*t)-gy-gm*vy
    gx2,gy2=grad(x+a*dt/2,y+b*dt/2,vr,c,s,sr,si); a2=vx+c1*dt/2;b2=vy+d*dt/2;c2=-gx2-gm*a2;d2=F0*math.sin(om*(t+dt/2))-gy2-gm*b2
    gx3,gy3=grad(x+a2*dt/2,y+b2*dt/2,vr,c,s,sr,si); a3=vx+c2*dt/2;b3=vy+d2*dt/2;c3=-gx3-gm*a3;d3=F0*math.sin(om*(t+dt/2))-gy3-gm*b3
    gx4,gy4=grad(x+a3*dt,y+b3*dt,vr,c,s,sr,si); a4=vx+c3*dt;b4=vy+d3*dt;c4=-gx4-gm*a4;d4=F0*math.sin(om*(t+dt))-gy4-gm*b4
    return x+dt*(a+2*a2+2*a3+a4)/6,y+dt*(b+2*b2+2*b3+b4)/6,vx+dt*(c1+2*c2+2*c3+c4)/6,vy+dt*(d+2*d2+2*d3+d4)/6
@njit(parallel=True)
def batch(Fs,Ps,spc,vr,c,s,sr,si,x0,y0):
    n=len(Fs);out=np.zeros((n,8));sq3=math.sqrt(3.)
    for z in prange(n):
        F0=Fs[z];P=Ps[z];dt=P/spc;x=x0;y=y0;vx=0.;vy=0.;stepn=0;xm=x;ym=y
        for cyc in range(60):
            for j in range(spc):
                t=stepn*dt;x,y,vx,vy=step(x,y,vx,vy,t,dt,F0,P,vr,c,s,sr,si);stepn+=1
            if cyc==19: xm=x;ym=y
        dx=(x-xm)/40.;dy=(y-ym)/40.;vv=2*dy/sq3;uu=dx-.5*vv;mi=round(uu);ni=round(vv)
        du=uu-mi;dv=vv-ni;rx=du+.5*dv;ry=(sq3/2)*dv;res=math.sqrt(rx*rx+ry*ry)
        out[z]=[F0,P,uu,vv,mi,ni,res,dy]
    return out
Fs=[];Ps=[]
for P in [40.,70.]:
    for F in np.round(np.arange(1.0,4.0001,.025),3): Fs.append(F);Ps.append(P)
arr=batch(np.array(Fs),np.array(Ps),2000,vr,c,s,sr,si,x0[0],x0[1])
df=pd.DataFrame(arr,columns=['F0','period','u','v','m','n','res','dy'])
df.to_csv('/mnt/data/janus_n5_gate/n5_dense_plateau_scan.csv',index=False)
# contiguous intervals in grid
rows=[]
for P,g in df.groupby('period'):
    g=g.sort_values('F0').reset_index(drop=True); st=0
    for i in range(1,len(g)+1):
        if i==len(g) or (int(g.loc[i,'m']),int(g.loc[i,'n']))!=(int(g.loc[st,'m']),int(g.loc[st,'n'])):
            rows.append([P,int(g.loc[st,'m']),int(g.loc[st,'n']),g.loc[st,'F0'],g.loc[i-1,'F0'],i-st,(g.loc[st,'F0']+g.loc[i-1,'F0'])/2,float(g.loc[st:i-1,'res'].max())])
            st=i
ints=pd.DataFrame(rows,columns=['period','m','n','Fmin_grid','Fmax_grid','n_grid','Fmid','max_res'])
ints.to_csv('/mnt/data/janus_n5_gate/n5_dense_plateau_intervals.csv',index=False)
print(ints.to_string(index=False))
