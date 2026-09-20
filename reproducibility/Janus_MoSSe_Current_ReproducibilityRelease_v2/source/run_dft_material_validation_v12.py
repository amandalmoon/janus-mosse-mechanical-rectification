"""Reproduce the published-DFT MoSSe material-validation block (v12).

Outputs are written under ../data.  The script intentionally keeps the published
DFT GSFE separate from the phenomenological v9 mechanism study.  DFT supplies the
local registry landscape only; damping, mass and device forcing remain reduced
parameters.
"""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

import janus_fourier_landscapes_v12 as J
import dft_guided_material_v12 as M

ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)
KP=25.0
F0=3.5
BASE_SEED=20260913
BOOT=3000


def crossing(theta, Fc, level):
    theta=np.asarray(theta,float); Fc=np.asarray(Fc,float); d=Fc-level
    roots=[]
    for i in range(len(theta)-1):
        if d[i]==0: roots.append(float(theta[i]))
        if d[i]*d[i+1] < 0:
            roots.append(float(theta[i]+(theta[i+1]-theta[i])*(-d[i])/(d[i+1]-d[i])))
    return roots


def logistic(theta, theta50, width):
    z=np.clip((np.asarray(theta)-theta50)/width,-50,50)
    return 1/(1+np.exp(-z))


def fit_binomial(theta, escapes, n):
    x=np.asarray(theta,float); k=np.asarray(escapes,float); n=np.asarray(n,float)
    p=k/n; x0=float(x[np.argmin(np.abs(p-.5))])
    def nll(q):
        xc,logw=q; w=math.exp(logw)
        pp=np.clip(logistic(x,xc,w),1e-10,1-1e-10)
        return float(-np.sum(k*np.log(pp)+(n-k)*np.log(1-pp)))
    res=minimize(nll,[x0,math.log(.08)],method='L-BFGS-B',
                 bounds=[(x.min()-.3,x.max()+.3),(math.log(.003),math.log(.6))])
    if not res.success: raise RuntimeError(res.message)
    return float(res.x[0]),float(math.exp(res.x[1])),float(res.fun)


def static_block(material, sym, weak):
    thetas=np.arange(0,3.0001,.025)
    df=M.threshold_curves(material,thetas,kp=KP)
    df.to_csv(DATA/'dft_2H_MoSSe_guided_threshold_curves_k25_v12.csv',index=False)
    controls=pd.concat([
        M.threshold_curves(sym,np.arange(0,3.0001,.1),kp=KP),
        M.threshold_curves(weak,np.arange(0,3.0001,.1),kp=KP)],ignore_index=True)
    controls.to_csv(DATA/'dft_3R_MoSSe_guided_threshold_controls_v12.csv',index=False)
    vals={}
    for direction in ('forward','reverse'):
        g=df[df.direction==direction].sort_values('theta_deg')
        rr=crossing(g.theta_deg,g.Fc,F0)
        if not rr: raise RuntimeError(f'No F0 crossing for {direction}')
        vals[direction]=rr[0]
    window=pd.DataFrame([{'landscape':material.name,'k_perp':KP,'F0':F0,
        'theta_c_forward_deg':vals['forward'],'theta_c_reverse_deg':vals['reverse'],
        'window_abs_deg':abs(vals['forward']-vals['reverse']),
        'preferred_direction':'reverse' if vals['reverse']<vals['forward'] else 'forward'}])
    window.to_csv(DATA/'dft_2H_MoSSe_guided_diode_window_k25_v12.csv',index=False)
    hrows=[]
    for direction,sgn in [('forward',+1),('reverse',-1)]:
        r=M.guided_threshold(vals[direction],material,sgn,KP,ngrid=12000)
        # Subtract the guide from Hxx to expose the material/contact curvature.
        r['k_perp']=KP; r['Hxx_unGuided']=r['Hxx']-KP; r['min_kperp_from_Hxx']=max(0.0,-r['Hxx_unGuided'])
        hrows.append(r)
    pd.DataFrame(hrows).to_csv(DATA/'dft_2H_MoSSe_guided_fullhessian_k25_v12.csv',index=False)
    return df,controls,window


def rocking_batch(material):
    thetas=np.arange(0,3.0001,.1); amps=(3.0,3.5,4.0,4.5)
    cases=[]; sr=[]; si=[]; x0=[]; y0=[]; f0=[]
    vr=c=s=None
    for th in thetas:
        arr=M._arrays(float(th),material); vr,c,s=arr[:3]; xx,yy=M.zero_minimum(float(th),material,KP)
        for amp in amps:
            cases.append((float(th),float(amp))); sr.append(arr[3]); si.append(arr[4]); x0.append(xx); y0.append(yy); f0.append(amp)
    vel,cyc,xf,yf=M._rk4_batch(vr,c,s,np.asarray(sr),np.asarray(si),np.asarray(f0,float),40.,10,40,2000,KP,np.asarray(x0),np.asarray(y0))
    rows=[]
    for (th,amp),v,cp,x,y in zip(cases,vel,cyc,xf,yf):
        rows.append({'landscape':material.name,'theta_deg':th,'F0':amp,'period':40.0,'k_perp':KP,
                     'mean_velocity':v,'periods_per_cycle':cp,'x_final':x,'y_final':y,
                     'steps_per_cycle':2000,'n_eq':10,'n_meas':40})
    out=pd.DataFrame(rows); out.to_csv(DATA/'dft_2H_MoSSe_rocking_scan_k25_v12.csv',index=False)

    # High-precision representative time-step and half-period-phase checks.
    reps=[(1.5,3.5),(1.0,4.0),(0.5,4.0),(2.0,3.5)]; checks=[]
    for th,amp in reps:
        arr=M._arrays(th,material); xx,yy=M.zero_minimum(th,material,KP)
        for spc in (1000,2000,4000,8000):
            for sign in (+1,-1):
                v,cp,x,y=M._rk4_run(*arr,sign*amp,40.,20,80,spc,KP,xx,yy)
                checks.append({'theta_deg':th,'F0':sign*amp,'steps_per_cycle':spc,'dt':40/spc,
                               'mean_velocity':v,'periods_per_cycle':cp,'x_final':x,'y_final':y})
    pd.DataFrame(checks).to_csv(DATA/'dft_2H_MoSSe_rocking_dt_validation_k25_v12.csv',index=False)


def control_rocking(sym,weak):
    for land,name in [(sym,'dft_3R_symmetric_rocking_control_k25_v12.csv'),(weak,'dft_3R_weakodd_rocking_k25_v12.csv')]:
        rows=[]
        for th in np.arange(.5,2.5001,.5):
            arr=M._arrays(float(th),land); xx,yy=M.zero_minimum(float(th),land,KP)
            for amp in (3.0,3.5,4.0):
                v,cp,x,y=M._rk4_run(*arr,amp,40.,10,40,2000,KP,xx,yy)
                rows.append({'landscape':land.name,'theta_deg':th,'F0':amp,'mean_velocity':v,'periods_per_cycle':cp})
        pd.DataFrame(rows).to_csv(DATA/name,index=False)


def thermal_and_fits(material):
    grid=np.arange(.6,2.4001,.1)
    df,raw=M.thermal_switching(material,grid,F0,temps=(.005,.010),ntraj=160,period=40.,dt=.005,kp=KP)
    df.to_csv(DATA/'dft_2H_MoSSe_thermal_switching_k25_v12.csv',index=False)
    np.savez_compressed(DATA/'dft_2H_MoSSe_thermal_switching_raw_k25_v12.npz',
                        **{f'T{T}_th{th}_d{d}':v for (T,th,d),v in raw.items()})
    rng=np.random.default_rng(BASE_SEED+900000); fitrows=[]; boots={}
    for (T,label),g in df.groupby(['T_star','direction'],sort=True):
        g=g.sort_values('theta_deg'); x=g.theta_deg.to_numpy(float); k=g.escaped.to_numpy(int); n=g.n.to_numpy(int)
        xc,w,nll=fit_binomial(x,k,n); p=k/n; b=[]
        for _ in range(BOOT):
            kb=rng.binomial(n,p)
            try: b.append(fit_binomial(x,kb,n)[:2])
            except Exception: pass
        b=np.asarray(b,float); lo,hi=np.quantile(b[:,0],[.025,.975])
        fitrows.append({'T_star':T,'direction':label,'theta50_deg':xc,'width_deg':w,
                        'theta50_ci_low':lo,'theta50_ci_high':hi,'n_boot_ok':len(b),'negloglik':nll})
        boots[(T,label)]=b
    fits=pd.DataFrame(fitrows); fits.to_csv(DATA/'dft_2H_MoSSe_thermal_logistic_k25_v12.csv',index=False)
    rows=[]
    for T in sorted(fits.T_star.unique()):
        f=fits[(fits.T_star==T)&(fits.direction=='forward')].iloc[0]; r=fits[(fits.T_star==T)&(fits.direction=='reverse')].iloc[0]
        bf=boots[(T,'forward')][:,0]; br=boots[(T,'reverse')][:,0]; m=min(len(bf),len(br)); wb=np.abs(bf[:m]-br[:m])
        lo,hi=np.quantile(wb,[.025,.975])
        rows.append({'T_star':T,'theta50_forward_deg':f.theta50_deg,'theta50_reverse_deg':r.theta50_deg,
                     'W50_abs_deg':abs(f.theta50_deg-r.theta50_deg),'W50_ci_low':lo,'W50_ci_high':hi})
    pd.DataFrame(rows).to_csv(DATA/'dft_2H_MoSSe_thermal_diode_windows_k25_v12.csv',index=False)


def high_temperature_proxy(material):
    # E0=6W1=47.4 meV for the published 2H case; kBT at 300 K / E0.
    T300=0.5454008393670885; grid=np.arange(0,2.4001,.2)
    df,_=M.thermal_switching(material,grid,F0,temps=(.1,.25,T300),ntraj=160,period=40.,dt=.005,kp=KP)
    df.to_csv(DATA/'dft_2H_MoSSe_highT_energyunit_proxy_k25_v12.csv',index=False)


def main():
    pd.DataFrame(J.local_phase_diagnostics()).to_csv(DATA/'dft_fourier_phase_diagnostics_v12.csv',index=False)
    material=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
    sym=J.dft_landscape('3R_MoSSe_S-Se-Se-S')
    weak=J.dft_landscape('3R_MoSSe_Se-S-Se-S')
    static_block(material,sym,weak)
    rocking_batch(material); control_rocking(sym,weak)
    thermal_and_fits(material); high_temperature_proxy(material)
    # Import only after data generation to avoid circular startup work.
    import validate_v12_outputs
    validate_v12_outputs.main()

if __name__=='__main__':
    main()
