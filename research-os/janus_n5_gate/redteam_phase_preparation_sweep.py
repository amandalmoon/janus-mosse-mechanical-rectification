from pathlib import Path
import sys,math,numpy as np,pandas as pd
from numba import njit,prange
ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); pos=J.make_hexagonal_flake(6); theta=1.5
A=np.column_stack([J.A1,J.A2]); S=J.contact_factors(theta,land.vectors,pos)
vr=np.asarray(land.vectors,float); c=np.asarray(land.c_cos,float); s=np.asarray(land.c_sin,float); sr=np.asarray(S.real,float); si=np.asarray(S.imag,float)
@njit
def grad(x,y,vr,c,s,sr,si):
    gx=0.;gy=0.
    for k in range(vr.shape[0]):
        Gx=vr[k,0];Gy=vr[k,1];q=Gx*x+Gy*y;cq=math.cos(q);sq=math.sin(q)
        re=sr[k]*cq-si[k]*sq;im=sr[k]*sq+si[k]*cq;aa=-c[k]*im+s[k]*re
        gx+=aa*Gx;gy+=aa*Gy
    return gx,gy
@njit
def step(x,y,vx,vy,t,dt,F0,P,phase,vr,c,s,sr,si):
    om=2*math.pi/P; gam=4.
    gx,gy=grad(x,y,vr,c,s,sr,si); a=vx;b=vy;c1=-gx-gam*vx;d=F0*math.sin(om*t+phase)-gy-gam*vy
    gx2,gy2=grad(x+a*dt/2,y+b*dt/2,vr,c,s,sr,si);a2=vx+c1*dt/2;b2=vy+d*dt/2;c2=-gx2-gam*a2;d2=F0*math.sin(om*(t+dt/2)+phase)-gy2-gam*b2
    gx3,gy3=grad(x+a2*dt/2,y+b2*dt/2,vr,c,s,sr,si);a3=vx+c2*dt/2;b3=vy+d2*dt/2;c3=-gx3-gam*a3;d3=F0*math.sin(om*(t+dt/2)+phase)-gy3-gam*b3
    gx4,gy4=grad(x+a3*dt,y+b3*dt,vr,c,s,sr,si);a4=vx+c3*dt;b4=vy+d3*dt;c4=-gx4-gam*a4;d4=F0*math.sin(om*(t+dt)+phase)-gy4-gam*b4
    return x+dt*(a+2*a2+2*a3+a4)/6,y+dt*(b+2*b2+2*b3+b4)/6,vx+dt*(c1+2*c2+2*c3+c4)/6,vy+dt*(d+2*d2+2*d3+d4)/6
@njit(parallel=True)
def batch(Fs,Ps,phis,xinit,yinit,spc,neq,nmeas,vr,c,s,sr,si):
    n=len(Fs); out=np.zeros((n,7)); sq3=math.sqrt(3.)
    for z in prange(n):
        F0=Fs[z];P=Ps[z];ph=phis[z];dt=P/spc;x=xinit[z];y=yinit[z];vx=0.;vy=0.;istep=0
        for cyc in range(neq):
            for j in range(spc):
                t=istep*dt;x,y,vx,vy=step(x,y,vx,vy,t,dt,F0,P,ph,vr,c,s,sr,si);istep+=1
        su=0.;sv=0.;maxres=0.;same=1.;fm=999;fn=999
        for cyc in range(nmeas):
            sx=x;sy=y
            for j in range(spc):
                t=istep*dt;x,y,vx,vy=step(x,y,vx,vy,t,dt,F0,P,ph,vr,c,s,sr,si);istep+=1
            dx=x-sx;dy=y-sy;vv=2*dy/sq3;uu=dx-.5*vv;mi=round(uu);ni=round(vv)
            du=uu-mi;dv=vv-ni;rr=math.sqrt((du+.5*dv)**2+(sq3*.5*dv)**2)
            if rr>maxres:maxres=rr
            if cyc==0:fm=mi;fn=ni
            elif mi!=fm or ni!=fn:same=0
            su+=uu;sv+=vv
        mu=su/nmeas;mv=sv/nmeas
        out[z]=[mu,mv,round(mu),round(mv),maxres,same,math.sqrt((mu-round(mu)+.5*(mv-round(mv)))**2+(sq3*.5*(mv-round(mv)))**2)]
    return out
# coordinates are exact stable representatives at theta=1.5 from stationary enumeration
starts=[('ground',1.5,0.8660254037844386),('meta',0.5,0.28867513459481287)]
points=[('canonical',2.0,40.),('w11mid',1.9625,40.),('w12',2.5625,40.),('w23',3.025,40.),('w34',3.4,40.),('w27',3.675,70.),('near_low_transition',1.60,40.),('near_mid_transition',2.35,40.)]
phases=np.arange(8)*math.pi/4
rows=[];Fs=[];Ps=[];Ph=[];Xs=[];Ys=[];meta=[]
for st,x,y in starts:
 for name,F,P in points:
  for ip,ph in enumerate(phases):
   Fs.append(F);Ps.append(P);Ph.append(ph);Xs.append(x);Ys.append(y);meta.append((st,name,ip,ph,F,P))
out=batch(np.array(Fs),np.array(Ps),np.array(Ph),np.array(Xs),np.array(Ys),4000,20,20,vr,c,s,sr,si)
for md,v in zip(meta,out):
 st,name,ip,ph,F,P=md; rows.append(dict(start=st,name=name,F0=F,period=P,phase_index=ip,phase_rad=ph,u=v[0],vv=v[1],m=int(v[2]),n=int(v[3]),max_cycle_res=v[4],all_cycles_same=bool(v[5]),mean_res=v[6]))
df=pd.DataFrame(rows);df.to_csv('/mnt/data/janus_n5_gate/redteam_phase_preparation_sweep.csv',index=False)
print(df.groupby(['name','start'])[['m','n']].agg(lambda x: sorted(set(x))).to_string())
print('\ncounts unique windings')
for (name,st),g in df.groupby(['name','start']):
 print(name,st, g.groupby(['m','n']).size().to_dict())
print('max residual',df.max_cycle_res.max(),'all same',df.all_cycles_same.all())
