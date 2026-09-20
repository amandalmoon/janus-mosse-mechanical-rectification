from pathlib import Path
import sys, math, numpy as np, pandas as pd
from numba import njit, prange
from scipy.optimize import root
ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); pos=J.make_hexagonal_flake(6); theta=1.5
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A); S=J.contact_factors(theta,land.vectors,pos)
vr=np.asarray(land.vectors,float); c=np.asarray(land.c_cos,float); s=np.asarray(land.c_sin,float); sr=np.asarray(S.real,float); si=np.asarray(S.imag,float)
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
def rk4_step(x,y,vx,vy,t,dt,F0,period,gamma,vr,c,s,sr,si):
    om=2*math.pi/period
    gx,gy=grad(x,y,vr,c,s,sr,si)
    a=vx;b=vy;c1=-gx-gamma*vx;d=F0*math.sin(om*t)-gy-gamma*vy
    gx2,gy2=grad(x+a*dt/2,y+b*dt/2,vr,c,s,sr,si)
    a2=vx+c1*dt/2;b2=vy+d*dt/2;c2=-gx2-gamma*a2;d2=F0*math.sin(om*(t+dt/2))-gy2-gamma*b2
    gx3,gy3=grad(x+a2*dt/2,y+b2*dt/2,vr,c,s,sr,si)
    a3=vx+c2*dt/2;b3=vy+d2*dt/2;c3=-gx3-gamma*a3;d3=F0*math.sin(om*(t+dt/2))-gy3-gamma*b3
    gx4,gy4=grad(x+a3*dt,y+b3*dt,vr,c,s,sr,si)
    a4=vx+c3*dt;b4=vy+d3*dt;c4=-gx4-gamma*a4;d4=F0*math.sin(om*(t+dt))-gy4-gamma*b4
    return (x+dt*(a+2*a2+2*a3+a4)/6,
            y+dt*(b+2*b2+2*b3+b4)/6,
            vx+dt*(c1+2*c2+2*c3+c4)/6,
            vy+dt*(d+2*d2+2*d3+d4)/6)
@njit(parallel=True)
def audit(Fs,Ps,spc,n_eq,n_meas,x0,y0,vr,c,s,sr,si):
    n=len(Fs); out=np.zeros((n,14)); gamma=4.
    sq3=math.sqrt(3.0)
    for z in prange(n):
        F0=Fs[z];period=Ps[z];dt=period/spc
        x=x0;y=y0;vx=0.;vy=0.; prevx=x;prevy=y
        # transient whole cycles
        step=0
        for cyc in range(n_eq):
            for j in range(spc):
                t=step*dt
                x,y,vx,vy=rk4_step(x,y,vx,vy,t,dt,F0,period,gamma,vr,c,s,sr,si); step+=1
        prevx=x;prevy=y
        sumu=sumv=0.; sumu2=sumv2=0.; maxres=0.; first_m=999.;first_n=999.; same=1.; max_statecycle=0.
        for cyc in range(n_meas):
            sx=x;sy=y; svx=vx; svy=vy
            for j in range(spc):
                t=step*dt
                x,y,vx,vy=rk4_step(x,y,vx,vy,t,dt,F0,period,gamma,vr,c,s,sr,si); step+=1
            dx=x-sx;dy=y-sy
            vv=2*dy/sq3; uu=dx-.5*vv
            mi=round(uu);ni=round(vv)
            du=uu-mi;dv=vv-ni;rx=du+.5*dv;ry=(sq3/2)*dv;res=math.sqrt(rx*rx+ry*ry)
            if res>maxres:maxres=res
            if cyc==0: first_m=mi;first_n=ni
            elif mi!=first_m or ni!=first_n: same=0.
            sumu+=uu;sumv+=vv;sumu2+=uu*uu;sumv2+=vv*vv
            # relative state closure cycle-to-cycle for the observed integer winding
            ex=dx-(mi+.5*ni); ey=dy-(sq3/2)*ni
            rr=math.sqrt(ex*ex+ey*ey+(vx-svx)*(vx-svx)+(vy-svy)*(vy-svy))
            if rr>max_statecycle:max_statecycle=rr
        mu=sumu/n_meas;mv=sumv/n_meas
        std_u=math.sqrt(max(0.,sumu2/n_meas-mu*mu));std_v=math.sqrt(max(0.,sumv2/n_meas-mv*mv))
        mi=round(mu);ni=round(mv);du=mu-mi;dv=mv-ni;rx=du+.5*dv;ry=(sq3/2)*dv;meanres=math.sqrt(rx*rx+ry*ry)
        out[z]=[F0,period,mu,mv,mi,ni,meanres,maxres,std_u,std_v,same,first_m,first_n,max_statecycle]
    return out
Fgrid=np.round(np.arange(1.0,4.0001,.25),2); Pgrid=np.array([20.,30.,40.,50.,60.,70.,80.])
Fs=[];Ps=[]
for P in Pgrid:
    for F in Fgrid: Fs.append(F);Ps.append(P)
arr=audit(np.array(Fs),np.array(Ps),4000,20,40,x0[0],x0[1],vr,c,s,sr,si)
cols=['F0','period','u_mean','v_mean','m_mean','n_mean','mean_lock_residual','max_cycle_lock_residual','std_u_cycle','std_v_cycle','all_cycles_same_winding','cycle_m','cycle_n','max_onecycle_relative_state_residual']
df=pd.DataFrame(arr,columns=cols)
df.to_csv('/mnt/data/janus_n5_gate/n5_cycle_resolved_91.csv',index=False)
print('all mean locked',int((df.mean_lock_residual<1e-4).sum()),'of',len(df),'max mean res',df.mean_lock_residual.max())
print('all same cycle winding',int(df.all_cycles_same_winding.sum()),'of',len(df))
print('max cycle lock res',df.max_cycle_lock_residual.max())
print('max cycle std',max(df.std_u_cycle.max(),df.std_v_cycle.max()))
print('max onecycle relative state residual',df.max_onecycle_relative_state_residual.max())
print('non-period1 candidates:')
print(df[df.all_cycles_same_winding<0.5].to_string(index=False))
