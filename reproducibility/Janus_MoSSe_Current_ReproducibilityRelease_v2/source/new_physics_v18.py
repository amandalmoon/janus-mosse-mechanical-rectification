"""v18 new-physics extensions for the DFT-anchored Janus MoSSe rectifier.

This module adds two tests requested by the v17 peer-review audit:

1. finite-size/edge geometry robustness of the *material* DFT branch, and
2. nonlinear-dynamical validation of the guided integer winding states.

The calculations use the surviving v12 published-GSFE engine without altering
its local material parameters.  They therefore test consequences of the same
model rather than introducing a refitted potential.
"""
from __future__ import annotations

from pathlib import Path
import math
import sys
import json
import numpy as np
import pandas as pd
from matplotlib.path import Path as MplPath
from numba import njit
from scipy.optimize import minimize_scalar, brentq

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=ROOT/'data'/'canonical'; DATA.mkdir(parents=True,exist_ok=True)
REPORTS=ROOT/'reports'; REPORTS.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(HERE))
import janus_fourier_landscapes_v12 as J  # noqa:E402
import dft_guided_material_v12 as M  # noqa:E402

L=math.sqrt(3.0)
MASS=1.0
GAMMA=4.0
_CONFIG=json.loads((ROOT/'config'/'production.json').read_text(encoding='utf-8'))
_V18=_CONFIG.get('v18_new_physics',{})
MATERIAL_KEY=_CONFIG.get('material_key','2H_MoSSe_Se-S-Se-S')
KP=float(_CONFIG.get('k_perp',25.0))
FSTATIC=float(_CONFIG.get('F0_static_cut',3.5))


def _arrays_positions(theta, land, positions):
    S=J.contact_factors(float(theta),land.vectors,positions=np.asarray(positions,float))
    return (np.asarray(land.vectors,float),np.asarray(land.c_cos,float),np.asarray(land.c_sin,float),
            np.asarray(S.real,float),np.asarray(S.imag,float))


def guided_threshold_positions(theta,land,direction,positions,kp=KP,ngrid=3000):
    arr=_arrays_positions(theta,land,positions)
    ys=np.linspace(0,L,ngrid,endpoint=False)
    _,gy,_,_=M._threshold_grid(ys,*arr,float(kp))
    score=gy if direction>0 else -gy
    i=int(np.argmax(score)); dy=L/ngrid; y0=float(ys[i])
    def obj(y):
        x,g,hx,hxy,hyy=M._transverse_eq(float(y),*arr,float(kp),0.0)
        return -g if direction>0 else g
    res=minimize_scalar(obj,bounds=(y0-2.5*dy,y0+2.5*dy),method='bounded',options={'xatol':1e-12})
    x,g,hx,hxy,hyy=M._transverse_eq(float(res.x),*arr,float(kp),0.0)
    H=np.array([[hx,hxy],[hxy,hyy]])
    ev=np.linalg.eigvalsh(H)
    return {'theta_deg':float(theta),'direction':'forward' if direction>0 else 'reverse',
            'Fc':float(g if direction>0 else -g),'x_c':float(x),'y_c':float(res.x%L),
            'eig_soft':float(ev[0]),'eig_hard':float(ev[1])}


def _first_crossing(positions,direction,level=FSTATIC,kp=KP):
    land=J.dft_landscape(MATERIAL_KEY)
    grid=np.linspace(0.0,5.0,21)
    vals=[guided_threshold_positions(x,land,direction,positions,kp,ngrid=3000)['Fc']-level for x in grid]
    for a,b,fa,fb in zip(grid[:-1],grid[1:],vals[:-1],vals[1:]):
        if fa==0: return float(a)
        if fa*fb<0:
            return float(brentq(lambda th: guided_threshold_positions(th,land,direction,positions,kp,ngrid=3000)['Fc']-level,
                                float(a),float(b),xtol=2e-8,rtol=1e-11,maxiter=60))
    raise RuntimeError('No crossing found')


def stage_size_similarity():
    """Ten-size scaling of the material-case diode window and scaled-angle collapse."""
    land=J.dft_landscape(MATERIAL_KEY)
    rows=[]
    for shell in _V18.get('size_shells',list(range(3,13))):
        pos=J.make_hexagonal_flake(shell)
        tf=_first_crossing(pos,+1)
        tr=_first_crossing(pos,-1)
        rows.append({'shell':shell,'N':len(pos),'theta_c_forward_deg':tf,'theta_c_reverse_deg':tr,
                     'W_D_abs_deg':abs(tf-tr),'W_sqrtN':abs(tf-tr)*math.sqrt(len(pos))})
    roots=pd.DataFrame(rows)
    roots.to_csv(DATA/'v18_size_scaling_roots.csv',index=False)
    p=np.polyfit(np.log(roots.N.to_numpy(float)),np.log(roots.W_D_abs_deg.to_numpy(float)),1)
    pred=np.polyval(p,np.log(roots.N.to_numpy(float)))
    r2=1-np.sum((np.log(roots.W_D_abs_deg)-pred)**2)/np.sum((np.log(roots.W_D_abs_deg)-np.log(roots.W_D_abs_deg).mean())**2)

    # Direct similarity collapse.  Theta*sqrt(N) is the natural finite-contact variable.
    scaled=np.arange(float(_V18.get('similarity_scaled_twist_min',0.0)),
                     float(_V18.get('similarity_scaled_twist_max',18.0))+1e-10,
                     float(_V18.get('similarity_scaled_twist_step',0.5)))
    collapse=[]
    shells=tuple(_V18.get('similarity_shells',[3,5,7,9,12]))
    for shell in shells:
        pos=J.make_hexagonal_flake(shell); N=len(pos)
        for X in scaled:
            th=float(X/math.sqrt(N))
            ff=guided_threshold_positions(th,land,+1,pos,ngrid=3000)['Fc']
            fr=guided_threshold_positions(th,land,-1,pos,ngrid=3000)['Fc']
            rho=(ff-fr)/(ff+fr)
            collapse.append({'shell':shell,'N':N,'Theta_scaled':X,'theta_deg':th,
                             'Fc_forward':ff,'Fc_reverse':fr,'rho':rho})
    cdf=pd.DataFrame(collapse); cdf.to_csv(DATA/'v18_size_similarity_collapse.csv',index=False)
    # Cross-size deviation from the mean curve at each scaled angle.
    devs=[]
    for direction in ('Fc_forward','Fc_reverse'):
        piv=cdf.pivot(index='Theta_scaled',columns='N',values=direction)
        mean=piv.mean(axis=1)
        rel=(piv.sub(mean,axis=0).abs()).div(mean.abs(),axis=0)
        devs.extend(rel.to_numpy().ravel().tolist())
    rho_byN=cdf.groupby('N').rho.mean()
    return {'size_exponent_alpha':float(-p[0]),'size_scaling_log_R2':float(r2),
            'W_sqrtN_mean':float(roots.W_sqrtN.mean()),'W_sqrtN_std':float(roots.W_sqrtN.std(ddof=1)),
            'similarity_max_rel_deviation':float(np.nanmax(devs)),
            'rho_mean_across_sizes_min':float(rho_byN.min()),'rho_mean_across_sizes_max':float(rho_byN.max())}


def _triangle_vertices(radius,phi_deg):
    ph=math.radians(float(phi_deg))
    return np.array([[radius*math.cos(ph+math.pi/2+2*math.pi*i/3),
                      radius*math.sin(ph+math.pi/2+2*math.pi*i/3)] for i in range(3)])


def make_fixedN_triangle(phi_deg,target=127):
    pts=[]
    for q in range(-20,21):
        for r in range(-20,21): pts.append(q*J.A1+r*J.A2)
    pts=np.asarray(pts,float)
    best=None
    for R in np.linspace(8.5,9.8,2601):
        mask=MplPath(_triangle_vertices(R,phi_deg)).contains_points(pts,radius=1e-10)
        sub=pts[mask]
        score=(abs(len(sub)-target),abs(R-9.15))
        if best is None or score<best[0]: best=(score,R,sub)
        if len(sub)==target: break
    sub=best[2].copy(); sub-=sub.mean(axis=0)
    if len(sub)!=target:
        raise RuntimeError(f'Could not construct N={target} triangle at phi={phi_deg}; got {len(sub)}')
    return sub,float(best[1])


def stage_edge_factorization():
    """Fixed-N triangle edge rotation: an explicit test of separability breaking."""
    land=J.dft_landscape(MATERIAL_KEY)
    rows=[]; metrics=[]
    thetas=np.arange(float(_V18.get('edge_theta_min_deg',0.0)),
                     float(_V18.get('edge_theta_max_deg',3.0))+1e-10,
                     float(_V18.get('edge_theta_step_deg',0.1)))
    targetN=int(_V18.get('edge_target_N',127))
    for phi in _V18.get('edge_orientations_deg',[5,10,15,20,25]):
        pos,R=make_fixedN_triangle(phi,targetN)
        local=[]
        for th in thetas:
            ff=guided_threshold_positions(th,land,+1,pos,ngrid=3000)['Fc']
            fr=guided_threshold_positions(th,land,-1,pos,ngrid=3000)['Fc']
            rho=(ff-fr)/(ff+fr)
            local.append((float(th),ff,fr,rho))
        ld=pd.DataFrame(local,columns=['theta_deg','Fc_forward','Fc_reverse','rho'])
        rb=float(ld.rho.mean()); fm=.5*(ld.Fc_forward+ld.Fc_reverse)
        ef=np.abs(fm*(1+rb)-ld.Fc_forward)/np.abs(ld.Fc_forward)
        er=np.abs(fm*(1-rb)-ld.Fc_reverse)/np.abs(ld.Fc_reverse)
        # crossing interpolation on this 0.1-degree grid; enough for comparative edge metric.
        def cross(y):
            x=ld.theta_deg.to_numpy(); d=y.to_numpy()-FSTATIC
            for i in range(len(x)-1):
                if d[i]*d[i+1]<0: return float(x[i]+(x[i+1]-x[i])*(-d[i])/(d[i+1]-d[i]))
            return float('nan')
        tf=cross(ld.Fc_forward); tr=cross(ld.Fc_reverse)
        metrics.append({'edge_phi_deg':phi,'N':targetN,'triangle_radius_a':R,'rho_mean':rb,
                        'rho_std':float(ld.rho.std(ddof=1)),
                        'max_factorization_error_percent':float(100*max(ef.max(),er.max())),
                        'theta_c_forward_deg':tf,'theta_c_reverse_deg':tr,'W_D_abs_deg':abs(tf-tr)})
        for _,r in ld.iterrows(): rows.append({'edge_phi_deg':phi,'N':targetN,'triangle_radius_a':R,**r.to_dict()})
    pd.DataFrame(rows).to_csv(DATA/'v18_edge_factorization_curves.csv',index=False)
    mdf=pd.DataFrame(metrics); mdf.to_csv(DATA/'v18_edge_factorization_metrics.csv',index=False)

    # Refine the two high-rotation cases near the sign reversal.  This guards the
    # bulk-edge conclusion against interpolation on the coarser 0.1-degree scan.
    fine_rows=[]; zero_roots={}
    for phi in _V18.get('edge_refine_orientations_deg',[20,25]):
        pos,_=make_fixedN_triangle(phi,targetN)
        for th in np.arange(float(_V18.get('edge_refine_theta_min_deg',2.75)),
                            float(_V18.get('edge_refine_theta_max_deg',3.05))+1e-10,
                            float(_V18.get('edge_refine_theta_step_deg',0.025))):
            ff=guided_threshold_positions(float(th),land,+1,pos,ngrid=4000)['Fc']
            fr=guided_threshold_positions(float(th),land,-1,pos,ngrid=4000)['Fc']
            fine_rows.append({'edge_phi_deg':phi,'theta_deg':float(th),'Fc_forward':ff,'Fc_reverse':fr,
                              'rho':(ff-fr)/(ff+fr)})
    fdf=pd.DataFrame(fine_rows); fdf.to_csv(DATA/'v18_edge_zero_crossing_refinement.csv',index=False)
    for phi,g in fdf.groupby('edge_phi_deg'):
        x=g.theta_deg.to_numpy(float); y=g.rho.to_numpy(float); root=float('nan')
        for i in range(len(x)-1):
            if y[i]==0 or y[i]*y[i+1]<0:
                root=float(x[i] if y[i]==0 else x[i]-y[i]*(x[i+1]-x[i])/(y[i+1]-y[i]))
                break
        zero_roots[int(phi)]=root

    return {'edge_rho_min':float(mdf.rho_mean.min()),'edge_rho_max':float(mdf.rho_mean.max()),
            'edge_factorization_error_min_percent':float(mdf.max_factorization_error_percent.min()),
            'edge_factorization_error_max_percent':float(mdf.max_factorization_error_percent.max()),
            'edge_window_min_deg':float(mdf.W_D_abs_deg.min()),'edge_window_max_deg':float(mdf.W_D_abs_deg.max()),
            'edge_zero_crossing_phi20_deg':float(zero_roots[20]),
            'edge_zero_crossing_phi25_deg':float(zero_roots[25])}


# ---------- Nonlinear relative-periodic orbit / Floquet validation ----------
@njit
def _state_rhs(t,z,vr,c,s,sr,si,F0,omega,kp):
    x,y,vx,vy=z
    _,gx,gy,_,_,_=M._ugh(x,y,vr,c,s,sr,si,kp,0.0)
    dz=np.empty(4)
    dz[0]=vx; dz[1]=vy; dz[2]=(-gx-GAMMA*vx)/MASS; dz[3]=(F0*math.sin(omega*t)-gy-GAMMA*vy)/MASS
    return dz

@njit
def _state_step(t,z,dt,vr,c,s,sr,si,F0,omega,kp):
    k1=_state_rhs(t,z,vr,c,s,sr,si,F0,omega,kp)
    k2=_state_rhs(t+dt/2,z+k1*dt/2,vr,c,s,sr,si,F0,omega,kp)
    k3=_state_rhs(t+dt/2,z+k2*dt/2,vr,c,s,sr,si,F0,omega,kp)
    k4=_state_rhs(t+dt,z+k3*dt,vr,c,s,sr,si,F0,omega,kp)
    return z+dt*(k1+2*k2+2*k3+k4)/6

@njit
def _integrate_cycles(z0,F0,period,ncyc,spc,vr,c,s,sr,si,kp):
    z=z0.copy(); dt=period/spc; omega=2*math.pi/period
    for ic in range(ncyc):
        for j in range(spc):
            # Every completed drive cycle returns to the same phase.
            z=_state_step(j*dt,z,dt,vr,c,s,sr,si,F0,omega,kp)
    return z

@njit
def _aug_rhs(t,z,P,vr,c,s,sr,si,F0,omega,kp):
    x,y,vx,vy=z
    _,gx,gy,hxx,hxy,hyy=M._ugh(x,y,vr,c,s,sr,si,kp,0.0)
    dz=np.empty(4); dz[0]=vx; dz[1]=vy; dz[2]=(-gx-GAMMA*vx); dz[3]=(F0*math.sin(omega*t)-gy-GAMMA*vy)
    A=np.zeros((4,4)); A[0,2]=1; A[1,3]=1
    A[2,0]=-hxx; A[2,1]=-hxy; A[2,2]=-GAMMA
    A[3,0]=-hxy; A[3,1]=-hyy; A[3,3]=-GAMMA
    return dz,A@P

@njit
def _floquet_cycle(z0,F0,period,spc,vr,c,s,sr,si,kp):
    z=z0.copy(); P=np.eye(4); dt=period/spc; omega=2*math.pi/period
    for j in range(spc):
        t=j*dt
        z1,p1=_aug_rhs(t,z,P,vr,c,s,sr,si,F0,omega,kp)
        z2,p2=_aug_rhs(t+dt/2,z+z1*dt/2,P+p1*dt/2,vr,c,s,sr,si,F0,omega,kp)
        z3,p3=_aug_rhs(t+dt/2,z+z2*dt/2,P+p2*dt/2,vr,c,s,sr,si,F0,omega,kp)
        z4,p4=_aug_rhs(t+dt,z+z3*dt,P+p3*dt,vr,c,s,sr,si,F0,omega,kp)
        z += dt*(z1+2*z2+2*z3+z4)/6
        P += dt*(p1+2*p2+2*p3+p4)/6
    return z,P


def _relative_residual(z,z2):
    n=int(round((z2[1]-z[1])/L)); r=z2-z; r[1]-=n*L
    return n,float(np.linalg.norm(r))


def stage_mode_stability():
    land=J.dft_landscape(MATERIAL_KEY); theta=float(_V18.get('mode_theta_deg',1.5)); period=float(_V18.get('mode_period',40.0)); kp=KP
    arr=M._arrays(theta,land); xm,ym=M.zero_minimum(theta,land,kp)
    # High-resolution representative relative-periodic states spanning n=0,-1,-2,-3,-4.
    reps=tuple(float(x) for x in _V18.get('floquet_representative_F0',[3.0,3.35,3.50,3.85,4.025]))
    rows=[]
    for F0 in reps:
        z0=np.array([xm,ym,0.0,0.0])
        fspc=int(_V18.get('floquet_steps_per_cycle',4000)); ftrans=int(_V18.get('floquet_transient_cycles',200))
        z=_integrate_cycles(z0,float(F0),period,ftrans,fspc,*arr,kp)
        z2=_integrate_cycles(z,float(F0),period,1,fspc,*arr,kp)
        n,res=_relative_residual(z,z2)
        _,P=_floquet_cycle(z,float(F0),period,fspc,*arr,kp)
        eig=np.linalg.eigvals(P); rho=float(np.max(np.abs(eig)))
        rows.append({'F0':F0,'period':period,'theta_deg':theta,'winding':n,'poincare_residual':res,
                     'floquet_spectral_radius':rho,'mu1_real':eig[0].real,'mu1_imag':eig[0].imag,
                     'mu2_real':eig[1].real,'mu2_imag':eig[1].imag,
                     'mu3_real':eig[2].real,'mu3_imag':eig[2].imag,
                     'mu4_real':eig[3].real,'mu4_imag':eig[3].imag})
    rdf=pd.DataFrame(rows); rdf.to_csv(DATA/'v18_relative_periodic_floquet.csv',index=False)

    # Bidirectional continuation on a dense amplitude slice.  This tests hidden hysteresis.
    cont=[]
    amin=float(_V18.get('continuation_F0_min',2.5)); amax=float(_V18.get('continuation_F0_max',5.0)); astep=float(_V18.get('continuation_F0_step',0.025))
    upvals=np.arange(amin,amax+1e-10,astep); downvals=np.arange(amax,amin-1e-10,-astep)
    cfirst=int(_V18.get('continuation_first_cycles',120)); cfollow=int(_V18.get('continuation_follow_cycles',40)); cspc=int(_V18.get('continuation_steps_per_cycle',2000))
    for branch,vals in [('up',upvals),('down',downvals)]:
        z=np.array([xm,ym,0.0,0.0])
        for j,F0 in enumerate(vals):
            z=_integrate_cycles(z,float(F0),period,cfirst if j==0 else cfollow,cspc,*arr,kp)
            z2=_integrate_cycles(z,float(F0),period,1,cspc,*arr,kp)
            n,res=_relative_residual(z,z2)
            cont.append({'branch':branch,'F0':float(round(F0,6)),'winding':n,'poincare_residual':res,
                         'x':z[0],'y_mod_L':z[1]%L,'vx':z[2],'vy':z[3]})
            z[1]=z[1]%L
    cdf=pd.DataFrame(cont); cdf.to_csv(DATA/'v18_amplitude_continuation.csv',index=False)
    pp=cdf.pivot(index='F0',columns='branch',values='winding').dropna()
    mismatch=int(np.sum(pp['up'].to_numpy()!=pp['down'].to_numpy()))

    # Basin probe: transverse and registry-phase offsets for two representative running states.
    basin=[]
    bcycles=int(_V18.get('basin_cycles',120)); bspc=int(_V18.get('basin_steps_per_cycle',2000))
    for F0 in [float(x) for x in _V18.get('basin_F0',[3.5,3.85])]:
        for dx in [float(x) for x in _V18.get('basin_x_offsets_a',[-0.25,0.0,0.25])]:
            for frac in [float(x) for x in _V18.get('basin_registry_phases',[0.0,0.25,0.50,0.75])]:
                z0=np.array([xm+dx,ym+frac*L,0.0,0.0])
                z=_integrate_cycles(z0,F0,period,bcycles,bspc,*arr,kp)
                z2=_integrate_cycles(z,F0,period,1,bspc,*arr,kp)
                n,res=_relative_residual(z,z2)
                basin.append({'F0':F0,'x_offset_a':dx,'registry_phase':frac,'winding':n,'poincare_residual':res})
    bdf=pd.DataFrame(basin); bdf.to_csv(DATA/'v18_mode_basin_probe.csv',index=False)
    basin_mismatch=0
    for F0,g in bdf.groupby('F0'):
        mode=int(g.winding.mode().iloc[0]); basin_mismatch+=int(np.sum(g.winding.to_numpy()!=mode))
    return {'representative_max_poincare_residual':float(rdf.poincare_residual.max()),
            'representative_max_floquet_spectral_radius':float(rdf.floquet_spectral_radius.max()),
            'continuation_points_per_direction':int(len(pp)),
            'continuation_winding_mismatches':mismatch,
            'basin_cases':int(len(bdf)),'basin_winding_mismatches':basin_mismatch}


def _write_metrics(metrics):
    import json
    path=REPORTS/'V18_NEW_PHYSICS_METRICS.json'
    existing={}
    if path.exists():
        try: existing=json.loads(path.read_text(encoding='utf-8'))
        except Exception: existing={}
    existing.update(metrics)
    path.write_text(json.dumps(existing,indent=2),encoding='utf-8')
    print(json.dumps(existing,indent=2))

def main():
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--stage',choices=['size','edge','mode','all'],default='all')
    args=ap.parse_args()
    metrics={}
    if args.stage in ('size','all'): metrics.update(stage_size_similarity())
    if args.stage in ('edge','all'): metrics.update(stage_edge_factorization())
    if args.stage in ('mode','all'): metrics.update(stage_mode_stability())
    _write_metrics(metrics)

if __name__=='__main__': main()
