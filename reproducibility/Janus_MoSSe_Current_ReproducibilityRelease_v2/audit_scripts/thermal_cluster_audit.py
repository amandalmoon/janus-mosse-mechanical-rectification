"""RETIRED HISTORICAL THERMAL AUDIT.

This script preserves the superseded 10-burn/10-measure calculation for
provenance only. It is not manuscript evidence and must not be used for the
current thermal claim. Current evidence uses dt=0.02, 60 burn cycles and
100 measured cycles with the stationary long-window pipeline.
Outputs from this historical script are redirected to data/legacy_thermal_10x10.
"""
from pathlib import Path
_RELEASE_ROOT = Path(__file__).resolve().parents[1]
import sys, math, time
from pathlib import Path
import numpy as np, pandas as pd
from numba import njit, prange
from scipy.optimize import root
sys.path.insert(0,str(_RELEASE_ROOT/'source'))
import janus_fourier_landscapes_v12 as J

land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); positions=J.make_hexagonal_flake(6)
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A); theta=1.5; F0=2.0; period=40.; gamma=4.; mass=1.;
S=J.contact_factors(theta,land.vectors,positions)
vr=np.asarray(land.vectors,float); cc=np.asarray(land.c_cos,float); ss=np.asarray(land.c_sin,float); sr=np.asarray(S.real,float); si=np.asarray(S.imag,float)

# global zero-force minimum near origin
def f0(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
def j0(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
rr=root(f0,np.zeros(2),jac=j0,method='hybr'); x0,y0=rr.x

@njit
def grad(x,y,vr,c,s,sr,si):
    gx=0.;gy=0.
    for k in range(vr.shape[0]):
        Gx=vr[k,0];Gy=vr[k,1]; q=Gx*x+Gy*y; cq=math.cos(q);sq=math.sin(q)
        re=sr[k]*cq-si[k]*sq; im=sr[k]*sq+si[k]*cq
        aa=-c[k]*im+s[k]*re; gx+=aa*Gx; gy+=aa*Gy
    return gx,gy

@njit
def deterministic_state(x0,y0,vr,c,s,sr,si,F0,period,spc,ncycles):
    dt=period/spc; om=2*math.pi/period; x=x0;y=y0;vx=0.;vy=0.
    def deriv(t,x,y,vx,vy):
        gx,gy=grad(x,y,vr,c,s,sr,si)
        return vx,vy,-gx-gamma*vx,F0*math.sin(om*t)-gy-gamma*vy
    for i in range(ncycles*spc):
        t=i*dt
        a,b,c1,d=deriv(t,x,y,vx,vy)
        a2,b2,c2,d2=deriv(t+dt/2,x+a*dt/2,y+b*dt/2,vx+c1*dt/2,vy+d*dt/2)
        a3,b3,c3,d3=deriv(t+dt/2,x+a2*dt/2,y+b2*dt/2,vx+c2*dt/2,vy+d2*dt/2)
        a4,b4,c4,d4=deriv(t+dt,x+a3*dt,y+b3*dt,vx+c3*dt,vy+d3*dt)
        x+=dt*(a+2*a2+2*a3+a4)/6; y+=dt*(b+2*b2+2*b3+b4)/6
        vx+=dt*(c1+2*c2+2*c3+c4)/6; vy+=dt*(d+2*d2+2*d3+d4)/6
    return x,y,vx,vy

@njit(parallel=True)
def baoab_ensemble(ntraj,base_seed,T,dt,burn_cycles,measure_cycles,xinit,yinit,vxinit,vyinit,vr,c,s,sr,si,F0,period):
    spc=int(round(period/dt)); total=(burn_cycles+measure_cycles)*spc
    om=2*math.pi/period; oc=math.exp(-gamma*dt); sig=math.sqrt(T*(1-oc*oc))
    mean_u=np.empty(ntraj); mean_v=np.empty(ntraj); mean_dy=np.empty(ntraj); pneg=np.empty(ntraj); ptarget=np.empty(ntraj); mean_res=np.empty(ntraj)
    for r in prange(ntraj):
        np.random.seed(base_seed+r)
        x=xinit;y=yinit; X=xinit;Y=yinit;vx=vxinit;vy=vyinit
        xprev=0.;yprev=0.; su=0.;sv=0.;sdy=0.;neg=0.;targ=0.;sres=0.;kmeas=0
        for i in range(total):
            t=i*dt
            gx,gy=grad(x,y,vr,c,s,sr,si)
            fy=F0*math.sin(om*t)
            vx += .5*dt*(-gx)
            vy += .5*dt*(fy-gy)
            dxh=.5*dt*vx; dyh=.5*dt*vy; x += dxh; y += dyh; X += dxh; Y += dyh
            # wrap force-evaluation coordinates by a lattice vector; keep X,Y unwrapped
            vv=2*y/math.sqrt(3.0); uu=x-.5*vv; iu=round(uu); iv=round(vv); x-=iu+.5*iv; y-=(math.sqrt(3.0)/2)*iv
            vx=oc*vx+sig*np.random.randn(); vy=oc*vy+sig*np.random.randn()
            dxh=.5*dt*vx; dyh=.5*dt*vy; x += dxh; y += dyh; X += dxh; Y += dyh
            vv=2*y/math.sqrt(3.0); uu=x-.5*vv; iu=round(uu); iv=round(vv); x-=iu+.5*iv; y-=(math.sqrt(3.0)/2)*iv
            t2=(i+1)*dt
            gx,gy=grad(x,y,vr,c,s,sr,si)
            fy2=F0*math.sin(om*t2)
            vx += .5*dt*(-gx)
            vy += .5*dt*(fy2-gy)
            # cycle boundary
            if (i+1)%spc==0:
                cyc=(i+1)//spc
                if cyc==burn_cycles:
                    xprev=X;yprev=Y
                elif cyc>burn_cycles:
                    dx=X-xprev; dy=Y-yprev; xprev=X;yprev=Y
                    # fractional components: A^-1 [dx,dy]; for triangular A, v=2dy/sqrt3, u=dx-v/2
                    vv=2*dy/math.sqrt(3.0); uu=dx-.5*vv
                    su+=uu;sv+=vv;sdy+=dy; kmeas+=1
                    if dy<0: neg+=1
                    mu=round(uu); nv=round(vv)
                    if mu==1 and nv==-1: targ+=1
                    du=uu-mu; dv=vv-nv
                    # Cartesian residual of fractional rounding
                    rx=du+.5*dv; ry=(math.sqrt(3.0)/2)*dv
                    sres+=math.sqrt(rx*rx+ry*ry)
        mean_u[r]=su/kmeas;mean_v[r]=sv/kmeas;mean_dy[r]=sdy/kmeas;pneg[r]=neg/kmeas;ptarget[r]=targ/kmeas;mean_res[r]=sres/kmeas
    return mean_u,mean_v,mean_dy,pneg,ptarget,mean_res

# compile and deterministic orbit at phase 0 after 200 cycles
st=deterministic_state(x0,y0,vr,cc,ss,sr,si,F0,period,4000,200)
# shift deterministic orbit point by an exact lattice vector to keep coordinates numerically small
uv=AINV@np.array(st[:2]); uvshift=np.round(uv); xywrap=np.array(st[:2])-A@uvshift; st=(float(xywrap[0]),float(xywrap[1]),st[2],st[3])
print('det state wrapped',st,'shift',uvshift)
# verify one deterministic period displacement separately by starting this state and run one cycle? state includes unbounded translation, okay potential periodic.

import os
SET=os.environ.get('TSET','A')
ONE=os.environ.get('TEMP_SINGLE'); TL=os.environ.get('TEMP_LIST')
TEMPS=([float(x) for x in TL.split(',')] if TL else ([float(ONE)] if ONE else ([0.02,0.06,0.16,0.32] if SET=='A' else [0.04,0.10,0.24,0.50])))
N=1000; DT=.02; BURN=10; MEAS=10
LEGACY_DATA=_RELEASE_ROOT/'data'/'legacy_thermal_10x10'; LEGACY_DATA.mkdir(parents=True,exist_ok=True)
rows=[]; allraw=[]
for ti,T in enumerate(TEMPS):
    t0=time.time()
    out=baoab_ensemble(N,2026091700+ti*100000,T,DT,BURN,MEAS,*st,vr,cc,ss,sr,si,F0,period)
    mu,mv,mdy,pneg,ptarg,mres=out
    print('T',T,'sec',time.time()-t0,'meanv',mv.mean(),'pneg',pneg.mean())
    # cluster bootstrap over trajectories (each trajectory summary is one unit)
    rng=np.random.default_rng(2026091800+ti)
    B=10000
    boot_v=np.empty(B); boot_neg=np.empty(B); boot_targ=np.empty(B)
    # chunks to keep memory moderate
    for b0 in range(0,B,500):
        bs=min(500,B-b0); idx=rng.integers(0,N,size=(bs,N))
        boot_v[b0:b0+bs]=mv[idx].mean(axis=1)
        boot_neg[b0:b0+bs]=pneg[idx].mean(axis=1)
        boot_targ[b0:b0+bs]=ptarg[idx].mean(axis=1)
    row=dict(T=T,n=N,dt=DT,burn_cycles=BURN,measure_cycles=MEAS,
             mean_u=mu.mean(),mean_v=mv.mean(),mean_dy=mdy.mean(),P_neg_y=pneg.mean(),P_target=ptarg.mean(),mean_round_residual=mres.mean(),
             mean_v_ci_lo=np.quantile(boot_v,.025),mean_v_ci_hi=np.quantile(boot_v,.975),
             P_neg_y_ci_lo=np.quantile(boot_neg,.025),P_neg_y_ci_hi=np.quantile(boot_neg,.975),
             P_target_ci_lo=np.quantile(boot_targ,.025),P_target_ci_hi=np.quantile(boot_targ,.975))
    rows.append(row)
    for i in range(N): allraw.append(dict(T=T,traj=i,mean_u=mu[i],mean_v=mv[i],mean_dy=mdy[i],frac_neg_y=pneg[i],frac_target=ptarg[i],mean_round_residual=mres[i]))
    pd.DataFrame(rows).to_csv(str(LEGACY_DATA/f'free_thermal_cluster_ci_{SET}.csv'),index=False)
    pd.DataFrame(allraw).to_csv(str(LEGACY_DATA/f'free_thermal_trajectory_raw_{SET}.csv'),index=False)

pd.DataFrame(rows).to_csv(str(LEGACY_DATA/f'free_thermal_cluster_ci_{SET}.csv'),index=False)
pd.DataFrame(allraw).to_csv(str(LEGACY_DATA/f'free_thermal_trajectory_raw_{SET}.csv'),index=False)
print(pd.DataFrame(rows).to_string(index=False))
