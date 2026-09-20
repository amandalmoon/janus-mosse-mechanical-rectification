from __future__ import annotations
import sys, math, json
from dataclasses import replace
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import root, least_squares, minimize

OUT=Path('/mnt/data/janus_n4_gate')
SRC=OUT/'release/Janus_MoSSe_CanonicalUnguided_BaselineRelease/source'
sys.path.insert(0,str(SRC))
import janus_fourier_landscapes_v12 as J

THETA=1.5
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)
BASE=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
POS=J.make_hexagonal_flake(6)
DEN=float(np.sum(BASE.c_cos**2+BASE.c_sin**2))


def translate_landscape(land,a,name='translated'):
    d=land.vectors@np.asarray(a,float)
    c=land.c_cos*np.cos(d)+land.c_sin*np.sin(d)
    s=-land.c_cos*np.sin(d)+land.c_sin*np.cos(d)
    return J.FourierLandscape(name,np.array(land.vectors),np.array(c),np.array(s),land.energy_unit_meV,land.source_note)

def scale_odd(land,eta,name='eta'):
    return replace(land,name=name,c_sin=np.asarray(land.c_sin,float)*float(eta))

def periodic_distance(uv1,uv2):
    d=np.asarray(uv1,float)-np.asarray(uv2,float); d-=np.round(d)
    return float(np.linalg.norm(A@d))

def enumerate_minima(land,ngrid=11):
    S=J.contact_factors(THETA,land.vectors,POS); sols=[]
    for u in np.linspace(0,1,ngrid,endpoint=False):
        for v in np.linspace(0,1,ngrid,endpoint=False):
            x0=A@np.array([u,v])
            def f(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
            def jac(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
            rr=root(f,x0,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':800})
            if np.linalg.norm(f(rr.x))>1e-7: continue
            uv=AINV@rr.x; uv-=np.floor(uv); xy=A@uv
            if any(periodic_distance(uv,q['uv'])<1e-5 for q in sols): continue
            U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,0); ev=np.linalg.eigvalsh(H)
            if ev[0]>1e-7:
                sols.append(dict(uv=uv,xy=xy,U=float(U),eig=ev))
    sols.sort(key=lambda q:q['U'])
    return sols

def branch_fold(land,x0,sign,step=.08,maxF=6.0):
    S=J.contact_factors(THETA,land.vectors,POS); x=np.array(x0,float); F=0.0
    def eq(F,xguess):
        def f(z): return J.contact_ugh(z[0],z[1],S,land,0,sign*F)[1]
        def jac(z): return J.contact_ugh(z[0],z[1],S,land,0,sign*F)[2]
        rr=root(f,xguess,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':1000})
        res=np.linalg.norm(f(rr.x))
        if res>1e-6: return None,None,res
        return rr.x,np.linalg.eigvalsh(jac(rr.x)),res
    x,ev,_=eq(0,x)
    if x is None: raise RuntimeError('zero-force continuation start failed')
    last=(0.0,x.copy(),ev.copy())
    local_step=float(step)
    while F<maxF:
        Fn=F+local_step; xn,en,_=eq(Fn,x)
        if xn is None or en[0]<=0:
            guess=np.array([x[0],x[1],F+0.5*local_step]); break
        duv=AINV@(xn-x); duv-=np.round(duv)
        if np.linalg.norm(A@duv)>.2:
            local_step/=2
            if local_step<1e-4:
                guess=np.array([x[0],x[1],F]); break
            continue
        F,x,ev=Fn,xn,en; last=(F,x.copy(),ev.copy())
    else: raise RuntimeError('no fold')
    def aug(q):
        xx,yy,FF=q; U,g,H=J.contact_ugh(xx,yy,S,land,0,sign*FF)
        return np.array([g[0],g[1],np.linalg.det(H)])
    cands=[]
    for dx in [0,.001,-.001,.01,-.01,.05,-.05]:
        ls=least_squares(aug,guess+[dx,0,0],xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=5000,x_scale='jac')
        q=ls.x; U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]); eig=np.linalg.eigvalsh(H)
        res=float(np.linalg.norm(aug(q)))
        if res<1e-7 and q[2]>0 and eig[1]>1e-6:
            cands.append((abs(q[2]-last[0]),q,eig,res))
    if not cands: raise RuntimeError(('fold solve failed',sign,land.name,guess.tolist()))
    cands.sort(key=lambda t:t[0]); _,q,eig,res=cands[0]
    return dict(Fc=float(q[2]),xy=q[:2].copy(),eig=eig.copy(),res=res)

def prepared_thresholds(land,ngrid=11):
    mins=enumerate_minima(land,ngrid)
    if not mins: raise RuntimeError('no stable minima')
    g=mins[0]
    fp=branch_fold(land,g['xy'],+1); fm=branch_fold(land,g['xy'],-1)
    return dict(Fp=fp['Fc'],Fm=fm['Fc'],Delta=fp['Fc']-fm['Fc'],rho=(fp['Fc']-fm['Fc'])/(fp['Fc']+fm['Fc']),U0=g['U'],nmin=len(mins),fold_res=max(fp['res'],fm['res']),hard_min=min(fp['eig'][1],fm['eig'][1]))

def symmetric_global_thresholds(land,ngrid=17):
    mins=enumerate_minima(land,ngrid)
    vals=[]
    for m in mins:
        fp=branch_fold(land,m['xy'],+1); fm=branch_fold(land,m['xy'],-1)
        vals.append((m['U'],fp['Fc'],fm['Fc']))
    emin=min(v[0] for v in vals)
    deg=[v for v in vals if abs(v[0]-emin)<1e-8]
    Fp=max(v[1] for v in deg); Fm=max(v[2] for v in deg)
    return dict(Fp=Fp,Fm=Fm,Delta=Fp-Fm,rho=(Fp-Fm)/(Fp+Fm),U0=emin,nmin=len(mins),ndeg=len(deg))

def odd_fraction(land):
    return float(np.sum(land.c_sin**2)/np.sum(land.c_cos**2+land.c_sin**2))

# Find the translation-minimized odd-power center independently.
def objective_uv(uv):
    a=A@(np.asarray(uv)%1)
    return odd_fraction(translate_landscape(BASE,a))
# coarse + multi-start
us=np.linspace(0,1,121,endpoint=False); best=(1e9,None)
for u in us:
    for v in us:
        z=objective_uv([u,v])
        if z<best[0]: best=(z,(u,v))
cands=[]
for st in [best[1],(0,0),(.5,.5),(2/3,1/6),(1/3,1/3),(.25,.75),(.8,.2)]:
    rr=minimize(objective_uv,st,method='Nelder-Mead',options={'xatol':1e-13,'fatol':1e-15,'maxiter':5000})
    cands.append((rr.fun,rr.x%1))
cands.sort(key=lambda x:x[0]); AMIN=float(cands[0][0]); UVC=np.array(cands[0][1])

# Translation-invariant triad product phase check for shell 1.
def triad_chi(land):
    # complex amplitude C=c-is so c cos q+s sin q=Re[C exp(iq)]
    C=np.asarray(land.c_cos[:3])-1j*np.asarray(land.c_sin[:3])
    P=np.prod(C)
    return float(np.imag(P/abs(P)))
chi_ref=triad_chi(BASE)
rng=np.random.default_rng(20260919)
triad_rows=[]
for i in range(1000):
    uv=rng.random(2); L=translate_landscape(BASE,A@uv)
    triad_rows.append(dict(i=i,u=uv[0],v=uv[1],chi1=triad_chi(L),err=triad_chi(L)-chi_ref))
pd.DataFrame(triad_rows).to_csv(OUT/'n4_triad_invariant_random.csv',index=False)

# Gauge scan: enough to falsify invariance of eta path, not claimed as exhaustive origin optimization.
gauge_uv=[]
vals=[0.0,0.125,0.25,0.375,0.5]
for u in vals:
    for v in vals: gauge_uv.append((u,v))
gauge_uv.append(tuple(UVC))
# unique
seen=set(); gauges=[]
for uv in gauge_uv:
    key=tuple(np.round(np.asarray(uv)%1,10))
    if key not in seen: seen.add(key);gauges.append(np.array(key))

scan=[]
for gi,uv in enumerate(gauges):
    tr=translate_landscape(BASE,A@uv,f'gauge_{gi}')
    dm=prepared_thresholds(scale_odd(tr,-0.05),ngrid=9)['Delta']
    dp=prepared_thresholds(scale_odd(tr,+0.05),ngrid=9)['Delta']
    slope=(dp-dm)/0.1
    phys=prepared_thresholds(scale_odd(tr,1.0),ngrid=9)
    scan.append(dict(gauge=gi,u=uv[0],v=uv[1],is_amin_center=bool(np.linalg.norm((uv-UVC)-np.round(uv-UVC))<1e-7),origin_fixed_odd_fraction=odd_fraction(tr),origin_fixed_odd_rms=math.sqrt(odd_fraction(tr)),slope_fd_005=slope,Fp_eta1=phys['Fp'],Fm_eta1=phys['Fm'],Delta_eta1=phys['Delta'],rho_eta1=phys['rho'],fold_res=phys['fold_res']))
    print('scan',gi,uv,'slope',slope,'phys',phys['Delta'],flush=True)
SCAN=pd.DataFrame(scan)
SCAN.to_csv(OUT/'n4_gauge_scan.csv',index=False)

# select representative gauges: original, A_min center, min slope, max slope, near-zero slope
idx_orig=int(SCAN.index[(abs(SCAN.u)<1e-12)&(abs(SCAN.v)<1e-12)][0])
idx_center=int(SCAN.index[SCAN.is_amin_center][0])
idx_min=int(SCAN.slope_fd_005.idxmin()); idx_max=int(SCAN.slope_fd_005.idxmax()); idx_zero=int((SCAN.slope_fd_005.abs()).idxmin())
selected=[]
for idx,label in [(idx_orig,'published_origin'),(idx_center,'Amin_center'),(idx_min,'min_slope_tested'),(idx_max,'max_slope_tested'),(idx_zero,'near_zero_slope_tested')]:
    if idx not in [x[0] for x in selected]: selected.append((idx,label))

curve_rows=[]; contract_rows=[]; sel_summary=[]
etas=np.round(np.arange(0,1.0001,0.025),6)
for idx,label in selected:
    uv=SCAN.loc[idx,['u','v']].to_numpy(float); tr=translate_landscape(BASE,A@uv,label)
    # exact symmetry null at eta=0 via degenerate/global envelope
    z=symmetric_global_thresholds(scale_odd(tr,0.0),ngrid=17)
    curve_rows.append(dict(label=label,gauge_index=int(idx),u=uv[0],v=uv[1],eta=0.0,prep='paired_global_symmetry_null',**z))
    for eta in etas[1:]:
        q=prepared_thresholds(scale_odd(tr,float(eta)),ngrid=11)
        curve_rows.append(dict(label=label,gauge_index=int(idx),u=uv[0],v=uv[1],eta=float(eta),prep='ground',**q))
    qdf=pd.DataFrame([r for r in curve_rows if r['label']==label])
    imax=int(qdf.Delta.idxmax()); opt=qdf.loc[imax]
    # refined local susceptibility from +-0.025, +-0.05, +-0.1, constrained through origin
    xs=np.array([-0.1,-0.05,-0.025,0.025,0.05,0.1]); ys=[]
    for eta in xs:
        q=prepared_thresholds(scale_odd(tr,float(eta)),ngrid=11); ys.append(q['Delta'])
    ys=np.asarray(ys); slope=float(np.dot(xs,ys)/np.dot(xs,xs)); fit=slope*xs
    r2=float(1-np.sum((ys-fit)**2)/np.sum((ys-ys.mean())**2))
    # inversion/reversal contract at selected eta values
    maxrev=0.0
    for eta in [0.1,0.5,1.0]:
        qp=prepared_thresholds(scale_odd(tr,eta),ngrid=11); qm=prepared_thresholds(scale_odd(tr,-eta),ngrid=11)
        e1=abs(qm['Fp']-qp['Fm']);e2=abs(qm['Fm']-qp['Fp']);e3=abs(qm['Delta']+qp['Delta']);maxrev=max(maxrev,e1,e2,e3)
        contract_rows.append(dict(label=label,u=uv[0],v=uv[1],eta=eta,Fp_plus=qp['Fp'],Fm_plus=qp['Fm'],Fp_minus=qm['Fp'],Fm_minus=qm['Fm'],swap_err_plus=e1,swap_err_minus=e2,delta_antisym_err=e3))
    sel_summary.append(dict(label=label,gauge_index=int(idx),u=uv[0],v=uv[1],origin_fixed_odd_fraction=odd_fraction(tr),slope=slope,slope_R2=r2,eta_opt_grid=float(opt.eta),Delta_opt_grid=float(opt.Delta),rho_opt_grid=float(opt.rho),Delta_eta1=float(qdf.iloc[-1].Delta),sym_eta0_split=float(z['Delta']),max_eta_reversal_contract_err=maxrev))
    print('selected',label,'slope',slope,'opt',float(opt.eta),float(opt.Delta),flush=True)

CURVE=pd.DataFrame(curve_rows); CURVE.to_csv(OUT/'n4_selected_eta_curves.csv',index=False)
CON=pd.DataFrame(contract_rows); CON.to_csv(OUT/'n4_eta_reversal_contracts.csv',index=False)
SEL=pd.DataFrame(sel_summary); SEL.to_csv(OUT/'n4_selected_gauge_summary.csv',index=False)

# Summary
base_phys=prepared_thresholds(BASE,ngrid=17)
summary={
 'theta_deg':THETA,
 'N':int(len(POS)),
 'A_min':AMIN,
 'odd_rms_min':math.sqrt(AMIN),
 'A_min_center_uv':UVC.tolist(),
 'published_origin_odd_fraction':odd_fraction(BASE),
 'published_origin_odd_rms':math.sqrt(odd_fraction(BASE)),
 'triad_chi1_ref':chi_ref,
 'triad_chi1_expected_sin3phi':float(math.sin(3*math.radians(J.DFT_TABLE['2H_MoSSe_Se-S-Se-S']['phi'][0]))),
 'triad_chi1_max_random_translation_error':float(np.max(np.abs(pd.DataFrame(triad_rows).err))),
 'physical_Fp':base_phys['Fp'],'physical_Fm':base_phys['Fm'],'physical_Delta':base_phys['Delta'],
 'eta1_Fp_gauge_spread':float(SCAN.Fp_eta1.max()-SCAN.Fp_eta1.min()),
 'eta1_Fm_gauge_spread':float(SCAN.Fm_eta1.max()-SCAN.Fm_eta1.min()),
 'eta1_Delta_gauge_spread':float(SCAN.Delta_eta1.max()-SCAN.Delta_eta1.min()),
 'tested_gauge_count':int(len(SCAN)),
 'tested_slope_min_fd005':float(SCAN.slope_fd_005.min()),
 'tested_slope_max_fd005':float(SCAN.slope_fd_005.max()),
 'selected_slope_min':float(SEL.slope.min()),
 'selected_slope_max':float(SEL.slope.max()),
 'selected_eta_opt_min':float(SEL.eta_opt_grid.min()),
 'selected_eta_opt_max':float(SEL.eta_opt_grid.max()),
 'max_sym_eta0_split':float(SEL.sym_eta0_split.abs().max()),
 'max_eta_reversal_contract_err':float(SEL.max_eta_reversal_contract_err.max()),
 'decision':'eta continuation is gauge/origin dependent; retain only as gauge-fixed diagnostic, not material susceptibility or physical optimum'
}
(OUT/'n4_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
