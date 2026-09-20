"""Literature-DFT-anchored guided Janus simulations (v12).

Uses the published MoSSe GSFE Fourier amplitudes/phases from Angeli et al.
(PRB 106, 235159, 2022). The real implementation pairs conjugate reciprocal
triads as required by C3 symmetry and a real scalar energy. The 2024 Erratum
does not alter the GSFE coefficients or phase pairing. The DFT data
replace only the local registry landscape; m, gamma and rocking waveform remain
reduced device parameters.  The material-case transverse guide is k_perp*=25,
selected only after a full-Hessian stability audit showed that the reverse critical
state requires k_perp*>19.30.  The earlier phenomenological device remains k_perp*=15.
"""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np
import pandas as pd
from numba import njit, prange
from scipy.optimize import minimize_scalar, brentq
import janus_fourier_landscapes_v12 as J

ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)
L=math.sqrt(3.0)
KP=25.0
MASS=1.0
GAMMA=4.0
BASE_SEED=20260913

@njit
def _ugh(x,y,vr,c,s,sr,si,kp,force_y):
    U=0.0; gx=0.0; gy=0.0; hxx=0.0; hxy=0.0; hyy=0.0
    for t in range(vr.shape[0]):
        Gx=vr[t,0]; Gy=vr[t,1]
        q=Gx*x+Gy*y; cq=math.cos(q); sq=math.sin(q)
        re=sr[t]*cq-si[t]*sq
        im=sr[t]*sq+si[t]*cq
        U += c[t]*re+s[t]*im
        a=-c[t]*im+s[t]*re
        b=-c[t]*re-s[t]*im
        gx += a*Gx; gy += a*Gy
        hxx += b*Gx*Gx; hxy += b*Gx*Gy; hyy += b*Gy*Gy
    U += 0.5*kp*x*x-force_y*y
    gx += kp*x; gy -= force_y; hxx += kp
    return U,gx,gy,hxx,hxy,hyy

@njit
def _transverse_eq(y,vr,c,s,sr,si,kp,x0=0.0):
    x=x0
    for _ in range(60):
        U,gx,gy,hxx,hxy,hyy=_ugh(x,y,vr,c,s,sr,si,kp,0.0)
        if abs(gx)<1e-12: break
        if abs(hxx)<1e-9:
            step=0.02 if gx<0 else -0.02
        else:
            step=-gx/hxx
        if step>0.15: step=0.15
        if step<-0.15: step=-0.15
        x += step
        if x>1.0: x=1.0
        if x<-1.0: x=-1.0
    U,gx,gy,hxx,hxy,hyy=_ugh(x,y,vr,c,s,sr,si,kp,0.0)
    return x,gy,hxx,hxy,hyy

@njit(parallel=True)
def _threshold_grid(ys,vr,c,s,sr,si,kp):
    n=len(ys); xs=np.empty(n); gy=np.empty(n); hxx=np.empty(n); det=np.empty(n)
    for i in prange(n):
        x,g,hx,hxy,hyy=_transverse_eq(ys[i],vr,c,s,sr,si,kp,0.0)
        xs[i]=x; gy[i]=g; hxx[i]=hx; det[i]=hx*hyy-hxy*hxy
    return xs,gy,hxx,det

@njit(parallel=True)
def _zero_energy_grid(ys,vr,c,s,sr,si,kp):
    n=len(ys); xs=np.empty(n); us=np.empty(n)
    for i in prange(n):
        x,g,hx,hxy,hyy=_transverse_eq(ys[i],vr,c,s,sr,si,kp,0.0)
        U,gx,gy,hxx,hxy2,hyy2=_ugh(x,ys[i],vr,c,s,sr,si,kp,0.0)
        xs[i]=x; us[i]=U
    return xs,us

def _arrays(theta,land):
    S=J.contact_factors(theta,land.vectors)
    return (np.asarray(land.vectors,float),np.asarray(land.c_cos,float),np.asarray(land.c_sin,float),
            np.asarray(S.real,float),np.asarray(S.imag,float))

def _scalar_transverse(y,arr,kp=KP):
    vr,c,s,sr,si=arr
    x,gy,hxx,hxy,hyy=_transverse_eq(float(y),vr,c,s,sr,si,kp,0.0)
    return x,gy,hxx,hxy,hyy

def guided_threshold(theta,land,direction,kp=KP,ngrid=6000):
    arr=_arrays(theta,land)
    ys=np.linspace(0,L,ngrid,endpoint=False)
    xs,gy,hxx,det=_threshold_grid(ys,*arr,kp)
    score=gy if direction>0 else -gy
    i=int(np.argmax(score))
    dy=L/ngrid
    y0=ys[i]
    # Work on an unwrapped local interval; periodicity makes evaluation valid.
    def obj(y):
        x,g,hx,hxy,hyy=_scalar_transverse(y,arr,kp)
        return -g if direction>0 else g
    res=minimize_scalar(obj,bounds=(y0-2.5*dy,y0+2.5*dy),method='bounded',options={'xatol':1e-13})
    y=float(res.x); x,g,hx,hxy,hyy=_scalar_transverse(y,arr,kp)
    H=np.array([[hx,hxy],[hxy,hyy]])
    ev=np.linalg.eigvalsh(H)
    Fc=float(g if direction>0 else -g)
    return {'theta_deg':theta,'direction':'forward' if direction>0 else 'reverse','Fc':Fc,
            'x_c':x,'y_c':y%L,'eig_soft':ev[0],'eig_hard':ev[1],
            'det_hessian':float(np.linalg.det(H)),'Hxx':hx,'Hxy':hxy,'Hyy':hyy}

def threshold_curves(land,thetas=np.arange(0,5.0001,.025),kp=KP):
    rows=[]
    for th in thetas:
        rows.append({**guided_threshold(float(th),land,+1,kp), 'landscape':land.name})
        rows.append({**guided_threshold(float(th),land,-1,kp), 'landscape':land.name})
    return pd.DataFrame(rows)

def crossing(theta,Fc,F0):
    theta=np.asarray(theta,float); Fc=np.asarray(Fc,float)
    d=Fc-F0
    roots=[]
    for i in range(len(theta)-1):
        if d[i]==0: roots.append(theta[i])
        if d[i]*d[i+1]<0:
            roots.append(theta[i]+(theta[i+1]-theta[i])*(-d[i])/(d[i+1]-d[i]))
    return roots

@njit
def _grad(x,y,vr,c,s,sr,si,kp):
    U,gx,gy,hxx,hxy,hyy=_ugh(x,y,vr,c,s,sr,si,kp,0.0)
    return gx,gy

@njit
def _rk4_run(vr,c,s,sr,si,F0,period,n_eq,n_meas,steps_per_cycle,kp,x0,y0):
    dt=period/steps_per_cycle; omega=2*math.pi/period
    x=x0;y=y0;vx=0.0;vy=0.0; ymark=y0; tmark=0.0
    total=(n_eq+n_meas)*steps_per_cycle
    def deriv(t,x,y,vx,vy):
        gx,gy=_grad(x,y,vr,c,s,sr,si,kp)
        return vx,vy,(-gx-GAMMA*vx)/MASS,(F0*math.sin(omega*t)-gy-GAMMA*vy)/MASS
    for i in range(total):
        t=i*dt
        a,b,c1,d=deriv(t,x,y,vx,vy)
        a2,b2,c2,d2=deriv(t+dt/2,x+a*dt/2,y+b*dt/2,vx+c1*dt/2,vy+d*dt/2)
        a3,b3,c3,d3=deriv(t+dt/2,x+a2*dt/2,y+b2*dt/2,vx+c2*dt/2,vy+d2*dt/2)
        a4,b4,c4,d4=deriv(t+dt,x+a3*dt,y+b3*dt,vx+c3*dt,vy+d3*dt)
        x += dt*(a+2*a2+2*a3+a4)/6
        y += dt*(b+2*b2+2*b3+b4)/6
        vx += dt*(c1+2*c2+2*c3+c4)/6
        vy += dt*(d+2*d2+2*d3+d4)/6
        if i==n_eq*steps_per_cycle-1:
            ymark=y; tmark=(i+1)*dt
    duration=total*dt-tmark
    return (y-ymark)/duration,(y-ymark)/(L*n_meas),x,y

@njit(parallel=True)
def _rk4_batch(vr,c,s,sr_cases,si_cases,F0s,period,n_eq,n_meas,steps_per_cycle,kp,x0s,y0s):
    n=sr_cases.shape[0]
    vel=np.empty(n); cyc=np.empty(n); xf=np.empty(n); yf=np.empty(n)
    for i in prange(n):
        v,cp,x,y=_rk4_run(vr,c,s,sr_cases[i],si_cases[i],F0s[i],period,n_eq,n_meas,steps_per_cycle,kp,x0s[i],y0s[i])
        vel[i]=v;cyc[i]=cp;xf[i]=x;yf[i]=y
    return vel,cyc,xf,yf

def zero_minimum(theta,land,kp=KP):
    arr=_arrays(theta,land)
    ys=np.linspace(0,L,2400,endpoint=False)
    xs,us=_zero_energy_grid(ys,*arr,kp)
    i=int(np.argmin(us)); dy=L/len(ys); y0=float(ys[i])
    def obj(y):
        x,g,hx,hxy,hyy=_scalar_transverse(float(y),arr,kp)
        return _ugh(x,float(y),*arr,kp,0.0)[0]
    res=minimize_scalar(obj,bounds=(y0-2*dy,y0+2*dy),method='bounded',options={'xatol':1e-12})
    y=float(res.x)%L; x=_scalar_transverse(y,arr,kp)[0]
    return x,y

def rocking_scan(land,thetas,F0s=(3.0,3.5,4.0,4.5),period=40.0,kp=KP,spc=4000):
    rows=[]
    for th in thetas:
        arr=_arrays(float(th),land); x0,y0=zero_minimum(float(th),land,kp)
        for F0 in F0s:
            v,cperiod,x,y=_rk4_run(*arr,float(F0),period,20,80,spc,kp,x0,y0)
            rows.append({'landscape':land.name,'theta_deg':th,'F0':F0,'period':period,'k_perp':kp,
                         'mean_velocity':v,'periods_per_cycle':cperiod,'x_final':x,'y_final':y,'steps_per_cycle':spc})
    return pd.DataFrame(rows)

@njit(parallel=True)
def _baoab_halfcycle(ntraj,base_seed,x0,y0,direction,tstar,vr,c,s,sr,si,F0,half_period,dt,kp,preeq):
    npre=int(round(preeq/dt)); nrun=int(round(half_period/dt))
    cc=math.exp(-GAMMA*dt/MASS); sigma=math.sqrt((tstar/MASS)*(1-cc*cc))
    shifts=np.empty(ntraj,np.int64)
    for r in prange(ntraj):
        np.random.seed(base_seed+r)
        x=x0;y=y0;vx=0.0;vy=0.0
        for _ in range(npre):
            gx,gy=_grad(x,y,vr,c,s,sr,si,kp)
            vx += .5*dt*(-gx)/MASS; vy += .5*dt*(-gy)/MASS
            x += .5*dt*vx; y += .5*dt*vy
            vx=cc*vx+sigma*np.random.randn(); vy=cc*vy+sigma*np.random.randn()
            x += .5*dt*vx; y += .5*dt*vy
            gx,gy=_grad(x,y,vr,c,s,sr,si,kp)
            vx += .5*dt*(-gx)/MASS; vy += .5*dt*(-gy)/MASS
        for i in range(nrun):
            t=i*dt; ext=direction*F0*math.sin(math.pi*t/half_period)
            gx,gy=_grad(x,y,vr,c,s,sr,si,kp)
            vx += .5*dt*(-gx)/MASS; vy += .5*dt*(ext-gy)/MASS
            x += .5*dt*vx; y += .5*dt*vy
            vx=cc*vx+sigma*np.random.randn(); vy=cc*vy+sigma*np.random.randn()
            x += .5*dt*vx; y += .5*dt*vy
            t2=(i+1)*dt; ext2=direction*F0*math.sin(math.pi*t2/half_period)
            gx,gy=_grad(x,y,vr,c,s,sr,si,kp)
            vx += .5*dt*(-gx)/MASS; vy += .5*dt*(ext2-gy)/MASS
        shifts[r]=int(round((y-y0)/L))
    return shifts

def thermal_switching(land,thetas,F0,temps=(0.0025,0.005,0.01),ntraj=160,period=40.0,dt=.005,kp=KP):
    rows=[]; raw={}
    half=period/2
    for ti,T in enumerate(temps):
        for ai,th in enumerate(thetas):
            arr=_arrays(float(th),land); x0,y0=zero_minimum(float(th),land,kp)
            for direction in (+1,-1):
                seed=BASE_SEED+100000*ti+1000*ai+(0 if direction>0 else 500)
                shifts=_baoab_halfcycle(ntraj,seed,x0,y0,direction,float(T),*arr,float(F0),half,dt,kp,10.0)
                escaped=(shifts*direction)>0
                rows.append({'landscape':land.name,'T_star':T,'theta_deg':th,
                             'direction':'forward' if direction>0 else 'reverse','F0':F0,
                             'n':ntraj,'escaped':int(escaped.sum()),'p_escape':float(escaped.mean()),
                             'mean_signed_shift':float(np.mean(shifts*direction))})
                raw[(T,th,direction)]=shifts
    return pd.DataFrame(rows),raw

def main():
    """Run a compact material-case smoke test.

    The complete production regeneration, including bootstrap fitting and the
    high-temperature energy-unit proxy, is orchestrated by
    ``run_dft_material_validation_v12.py``.  Keeping the expensive workflow in a
    separate driver avoids accidental partial overwrites.
    """
    pd.DataFrame(J.local_phase_diagnostics()).to_csv(DATA/'dft_fourier_phase_diagnostics_v12.csv',index=False)
    material=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
    rows=[]
    for th in (1.0099068387052377, 1.9444516264438518):
        for direction in (+1,-1):
            rows.append(guided_threshold(th,material,direction,KP))
    smoke=pd.DataFrame(rows)
    print(smoke[['theta_deg','direction','Fc','eig_soft','eig_hard']].to_string(index=False))
    print('For the full v12 production rerun use: python run_dft_material_validation_v12.py')

if __name__=='__main__':
    main()
