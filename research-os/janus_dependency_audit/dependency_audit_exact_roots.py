from __future__ import annotations
import json, math, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from matplotlib.path import Path as MplPath

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import janus_fourier_landscapes_v12 as J
import dft_guided_material_v12 as M

OUT=HERE
KP=25.0
F0=3.5
material=J.dft_landscape('2H_MoSSe_Se-S-Se-S')

# ---------- generic threshold for arbitrary finite-contact site set ----------
def arrays_positions(theta, land, positions):
    S=J.contact_factors(theta, land.vectors, positions=positions)
    return (np.asarray(land.vectors,float),np.asarray(land.c_cos,float),np.asarray(land.c_sin,float),
            np.asarray(S.real,float),np.asarray(S.imag,float))

def scalar_transverse(y,arr,kp=KP):
    vr,c,s,sr,si=arr
    x,gy,hxx,hxy,hyy=M._transverse_eq(float(y),vr,c,s,sr,si,kp,0.0)
    return x,gy,hxx,hxy,hyy

def guided_threshold_positions(theta,land,direction,positions,kp=KP,ngrid=6000):
    arr=arrays_positions(theta,land,positions)
    ys=np.linspace(0,M.L,ngrid,endpoint=False)
    xs,gy,hxx,det=M._threshold_grid(ys,*arr,kp)
    score=gy if direction>0 else -gy
    i=int(np.argmax(score)); dy=M.L/ngrid; y0=float(ys[i])
    from scipy.optimize import minimize_scalar
    def obj(y):
        x,g,hx,hxy,hyy=scalar_transverse(y,arr,kp)
        return -g if direction>0 else g
    res=minimize_scalar(obj,bounds=(y0-2.5*dy,y0+2.5*dy),method='bounded',options={'xatol':1e-13})
    y=float(res.x); x,g,hx,hxy,hyy=scalar_transverse(y,arr,kp)
    H=np.array([[hx,hxy],[hxy,hyy]],float)
    ev=np.linalg.eigvalsh(H)
    Fc=float(g if direction>0 else -g)
    return {'theta_deg':float(theta),'direction':'forward' if direction>0 else 'reverse','Fc':Fc,
            'x_c':float(x),'y_c':float(y%M.L),'eig_soft':float(ev[0]),'eig_hard':float(ev[1]),
            'det_hessian':float(np.linalg.det(H)),'Hxx':float(hx),'Hxy':float(hxy),'Hyy':float(hyy)}

# Cache expensive threshold calls per positions identity/land coeffs/theta/direction.
_cache={}
def tval(theta,direction,positions,land=material,ngrid=6000):
    # position signature sufficiently exact for in-process cache
    sig=(len(positions),round(float(np.sum(positions[:,0]**2+positions[:,1]**2)),12),
         round(float(np.sum(positions[:,0]**3+0.37*positions[:,1]**3)),12))
    lsig=(tuple(np.round(land.c_cos,14)),tuple(np.round(land.c_sin,14)))
    key=(sig,lsig,round(float(theta),12),int(direction),int(ngrid))
    if key not in _cache:
        _cache[key]=guided_threshold_positions(theta,land,direction,positions,KP,ngrid)['Fc']
    return _cache[key]

def bracket_root(func,lo=0.0,hi=5.0,step=0.1):
    x0=lo; f0=func(x0)
    x=x0+step
    while x<=hi+1e-12:
        f=func(x)
        if f0==0: return (x0,x0)
        if f0*f<0: return (x0,x)
        x0,f0=x,f; x+=step
    raise RuntimeError('root not bracketed')

def exact_crossing(positions,direction,level=F0,land=material,lo=0,hi=5):
    f=lambda th:tval(th,direction,positions,land)-level
    a,b=bracket_root(f,lo,hi,.1)
    if a==b: return a
    return float(brentq(f,a,b,xtol=2e-13,rtol=1e-14,maxiter=100))

def old_linear_from_exact(exact,positions,direction,level=F0,land=material,step=.025):
    a=math.floor((exact+1e-12)/step)*step
    if abs(exact-a)<1e-11: return exact
    b=a+step
    fa=tval(a,direction,positions,land); fb=tval(b,direction,positions,land)
    return float(a+(b-a)*(level-fa)/(fb-fa))

def log_power_fit(N,W):
    x=np.log(np.asarray(N,float)); y=np.log(np.asarray(W,float))
    slope,inter=np.polyfit(x,y,1); pred=inter+slope*x
    ssr=float(np.sum((y-pred)**2)); sst=float(np.sum((y-y.mean())**2))
    return {'alpha':float(-slope),'prefactor':float(np.exp(inter)),'R2_log':float(1-ssr/sst)}

# ---------- 1. reference endpoint ----------
refpos=J.make_hexagonal_flake(6)
ref={}
for d,name in [(+1,'forward'),(-1,'reverse')]:
    ex=exact_crossing(refpos,d,hi=3.0)
    old=old_linear_from_exact(ex,refpos,d)
    ref[name]={'old_linear':old,'exact':ex,'delta_deg':ex-old}
ref['W_D_old']=abs(ref['forward']['old_linear']-ref['reverse']['old_linear'])
ref['W_D_exact']=abs(ref['forward']['exact']-ref['reverse']['exact'])
ref['W_D_delta']=ref['W_D_exact']-ref['W_D_old']

# ---------- 2. size scaling, old linear vs exact ----------
size_rows=[]
for shell in range(3,13):
    pos=J.make_hexagonal_flake(shell); N=len(pos)
    exf=exact_crossing(pos,+1,hi=5.0); exr=exact_crossing(pos,-1,hi=5.0)
    oldf=old_linear_from_exact(exf,pos,+1); oldr=old_linear_from_exact(exr,pos,-1)
    wo=abs(oldf-oldr); we=abs(exf-exr)
    size_rows.append({'shell':shell,'N':N,'theta_f_old':oldf,'theta_r_old':oldr,'W_D_old':wo,
                      'theta_f_exact':exf,'theta_r_exact':exr,'W_D_exact':we,
                      'delta_W_D':we-wo,'W_DsqrtN_old':wo*math.sqrt(N),'W_DsqrtN_exact':we*math.sqrt(N)})
    print('SIZE',N,'old/exact W',wo,we,flush=True)
size_df=pd.DataFrame(size_rows)
size_df.to_csv(OUT/'size_scaling_old_vs_exact.csv',index=False)
fit_old=log_power_fit(size_df.N,size_df.W_D_old)
fit_exact=log_power_fit(size_df.N,size_df.W_D_exact)
size_summary={
    'fit_old':fit_old,'fit_exact':fit_exact,
    'alpha_delta':fit_exact['alpha']-fit_old['alpha'],
    'mean_WDsqrtN_old':float(size_df.W_DsqrtN_old.mean()),
    'sd_WDsqrtN_old':float(size_df.W_DsqrtN_old.std(ddof=1)),
    'mean_WDsqrtN_exact':float(size_df.W_DsqrtN_exact.mean()),
    'sd_WDsqrtN_exact':float(size_df.W_DsqrtN_exact.std(ddof=1)),
    'max_abs_WD_change_deg':float(np.max(np.abs(size_df.delta_W_D))),
    'max_rel_WD_change':float(np.max(np.abs(size_df.delta_W_D/size_df.W_D_old)))
}

# ---------- 3. factorization/rho surface metrics ----------
thetas=np.arange(0,3.0001,.025)
fr=[]
for th in thetas:
    ff=M.guided_threshold(float(th),material,+1,KP)['Fc']; rr=M.guided_threshold(float(th),material,-1,KP)['Fc']
    fr.append((th,ff,rr))
fdf=pd.DataFrame(fr,columns=['theta_deg','forward','reverse'])
fcmean=.5*(fdf.forward+fdf.reverse)
rho=(fdf.forward-fdf.reverse)/(fdf.forward+fdf.reverse)
rhobar=float(rho.mean())
factf=fcmean*(1+rhobar); factr=fcmean*(1-rhobar)
relf=np.abs(factf-fdf.forward)/np.abs(fdf.forward); relr=np.abs(factr-fdf.reverse)/np.abs(fdf.reverse)
factor_summary={
    'rho_mean':rhobar,'rho_sd_sample':float(rho.std(ddof=1)),
    'rho_min':float(rho.min()),'rho_max':float(rho.max()),
    'factorization_max_relerr_forward_percent':float(100*relf.max()),
    'factorization_max_relerr_reverse_percent':float(100*relr.max()),
    'band_area_force_deg':float(np.trapezoid(np.abs(fdf.forward-fdf.reverse),fdf.theta_deg)),
    'endpoint_patch_dependency':'none: metrics use direct threshold surface values on fixed theta grid'
}
fdf.assign(rho=rho).to_csv(OUT/'factorization_recomputed.csv',index=False)
print('FACTOR',factor_summary,flush=True)

# ---------- 4. odd-sector continuation ----------
from dataclasses import replace
def odd_scaled_landscape(base,lam):
    return replace(base,name=f'{base.name}_oddscale_{lam:+.6f}',c_sin=np.asarray(base.c_sin,float)*float(lam))
coarse=.025; dense=.0025; half=.15
left=np.arange(-1.0,-half-.5*coarse,coarse)
center=np.arange(-half,half+.5*dense,dense)
right=np.arange(half+coarse,1.0+.5*coarse,coarse)
lambdas=np.concatenate([left,center,right])
oddrows=[]
for ii,lam in enumerate(lambdas):
    land=odd_scaled_landscape(material,float(lam))
    ff=M.guided_threshold(1.5,land,+1,KP)['Fc']; rr=M.guided_threshold(1.5,land,-1,KP)['Fc']
    delta=ff-rr
    oddrows.append({'eta':lam,'Fc_forward':ff,'Fc_reverse':rr,'DeltaFc':delta,'rho':delta/(ff+rr)})
    if ii%40==0: print('ODD',ii,'/',len(lambdas),flush=True)
odf=pd.DataFrame(oddrows); odf.to_csv(OUT/'odd_sector_recomputed.csv',index=False)
local=odf[np.abs(odf.eta)<=.1500001]; x=local.eta.to_numpy(float); y=local.DeltaFc.to_numpy(float)
slope=float(np.dot(x,y)/np.dot(x,x)); pred=slope*x
r2=float(1-np.sum((y-pred)**2)/np.sum((y-y.mean())**2))
pos=odf[odf.eta>=0]; opt=pos.iloc[int(np.argmax(pos.DeltaFc.to_numpy(float)))]
odd_summary={'slope':slope,'R2':r2,'eta_opt':float(opt.eta),'DeltaFc_at_opt':float(opt.DeltaFc),'rho_at_opt':float(opt.rho),
             'endpoint_patch_dependency':'none: fixed theta=1.5 direct guided_threshold calls'}
print('ODDSUM',odd_summary,flush=True)

# ---------- 5. reconstruct v18 fixed-N triangle family and recompute edge metrics ----------
def tri_vertices(R,phi_deg):
    ph=math.radians(phi_deg)
    # circumradius R, equilateral triangle centered at origin
    return np.array([[R*math.cos(ph+2*k*math.pi/3),R*math.sin(ph+2*k*math.pi/3)] for k in range(3)])

def make_oriented_triangle_target(phi_deg,target=127):
    a1=J.A1; a2=J.A2
    pts=[]
    for q in range(-20,21):
        for r in range(-20,21): pts.append(q*a1+r*a2)
    pts=np.asarray(pts,float)
    candidates=[]
    # nominal R from continuum density, search exact-N plateaus; favor R closest 9.2
    for R in np.linspace(7.5,11.0,3501):
        path=MplPath(tri_vertices(R,phi_deg))
        mask=path.contains_points(pts,radius=1e-10); sub=pts[mask]
        if len(sub)==target: candidates.append((abs(R-9.2),R,sub))
    if not candidates:
        # fallback closest count
        best=None
        for R in np.linspace(7.5,11.0,3501):
            path=MplPath(tri_vertices(R,phi_deg)); sub=pts[path.contains_points(pts,radius=1e-10)]
            score=(abs(len(sub)-target),abs(R-9.2))
            if best is None or score<best[0]: best=(score,R,sub)
        R,sub=best[1],best[2]
    else:
        _,R,sub=min(candidates,key=lambda z:z[0])
    sub=sub.copy(); sub-=sub.mean(axis=0)
    return sub,float(R)

edge_rows=[]; edge_summary={}; edge_reconstruction_ok=True
for phi in [5,10,15,20,25]:
    pos,R=make_oriented_triangle_target(phi,127)
    if len(pos)!=127: edge_reconstruction_ok=False
    ers=[]
    for th in np.arange(0,3.0001,.1):
        ff=tval(float(th),+1,pos); rr=tval(float(th),-1,pos)
        ers.append((th,ff,rr))
        edge_rows.append({'phi_deg':phi,'R':R,'N':len(pos),'theta_deg':th,'Fc_forward':ff,'Fc_reverse':rr,
                          'rho':(ff-rr)/(ff+rr),'DeltaFc':ff-rr})
    ed=pd.DataFrame(ers,columns=['theta','f','r']); erho=(ed.f-ed.r)/(ed.f+ed.r); rb=float(erho.mean())
    meanfc=.5*(ed.f+ed.r); ef=meanfc*(1+rb); er=meanfc*(1-rb)
    maxerr=float(100*max((np.abs(ef-ed.f)/np.abs(ed.f)).max(),(np.abs(er-ed.r)/np.abs(ed.r)).max()))
    # exact F0 window using direct roots
    try:
        tf=exact_crossing(pos,+1,hi=5); tr=exact_crossing(pos,-1,hi=5); wd=abs(tf-tr)
    except Exception as e:
        tf=tr=wd=float('nan')
    # exact sign root for delta near high twist if present
    def delta(th): return tval(th,+1,pos)-tval(th,-1,pos)
    signroot=None
    vals=[(x,delta(x)) for x in np.arange(2.5,3.0001,.05)]
    for (a,fa),(b,fb) in zip(vals[:-1],vals[1:]):
        if fa==0: signroot=a; break
        if fa*fb<0:
            signroot=float(brentq(delta,a,b,xtol=2e-13,rtol=1e-14)); break
    edge_summary[str(phi)]={'R':R,'N':len(pos),'rho_mean':rb,'max_factorization_error_percent':maxerr,
                            'theta_f_F0_exact':tf,'theta_r_F0_exact':tr,'W_D_F0_exact':wd,
                            'sign_reversal_theta_exact':signroot}
    print('EDGE',phi,edge_summary[str(phi)],flush=True)
pd.DataFrame(edge_rows).to_csv(OUT/'edge_reconstruction_recomputed.csv',index=False)

# Compare reconstructed edge roots to published guided v18 replay anchors to certify geometry reconstruction.
published_edge_roots={20:2.963732,25:2.890673}
edge_root_diffs={}
for phi,pub in published_edge_roots.items():
    got=edge_summary[str(phi)]['sign_reversal_theta_exact']
    edge_root_diffs[str(phi)]=None if got is None else float(got-pub)
edge_certified=edge_reconstruction_ok and all(edge_root_diffs[str(k)] is not None and abs(edge_root_diffs[str(k)])<5e-3 for k in published_edge_roots)

summary={
    'reference_endpoint':ref,
    'size_scaling':size_summary,
    'factorization':factor_summary,
    'odd_sector':odd_summary,
    'edge':{'reconstruction_certified_against_published_guided_roots':edge_certified,
            'published_root_anchors_deg':published_edge_roots,'root_differences_deg':edge_root_diffs,
            'metrics':edge_summary},
    'dependency_verdict':{
        'W_D':'DIRECTLY DEPENDENT on crossing interpolation; exact-root patch changes values slightly',
        'size_scaling_exponent_and_WDsqrtN':'DEPENDENT because built from W_D endpoints for every N; recomputed exact values required',
        'rho_and_factorization':'INDEPENDENT of endpoint interpolation; computed from direct Fc surfaces at fixed theta',
        'scaled_surface_collapse':'INDEPENDENT of endpoint interpolation; direct Fc(theta,N) surface observable',
        'edge_factorization_and_sign_reversal':'INDEPENDENT of F0 endpoint interpolation; direct threshold-surface/rho zeros; F0 edge-window widths are dependent',
        'odd_sector_continuation':'INDEPENDENT of endpoint interpolation; fixed theta direct thresholds'
    }
}
with open(OUT/'dependency_audit_exact_roots.json','w') as f: json.dump(summary,f,indent=2)
print('\nFINAL SUMMARY')
print(json.dumps(summary,indent=2))
