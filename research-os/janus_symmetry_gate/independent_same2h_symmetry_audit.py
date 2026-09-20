from __future__ import annotations
import json, math, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize, root
from numba import njit

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import janus_fourier_landscapes_v12 as J

THETA=1.5
F0=2.0
PERIOD=40.0
MASS=1.0
GAMMA=4.0
N_EQ=20
N_MEAS=40
SPC=4000
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)
BASE=J.dft_landscape('2H_MoSSe_Se-S-Se-S')


def translated_coeffs(land,a):
    d=land.vectors@np.asarray(a,float)
    c=land.c_cos*np.cos(d)+land.c_sin*np.sin(d)
    s=-land.c_cos*np.sin(d)+land.c_sin*np.cos(d)
    return c,s

def odd_fraction_uv(uv):
    a=A@np.asarray(uv,float)
    c,s=translated_coeffs(BASE,a)
    return float(np.sum(s*s)/np.sum(c*c+s*s))

# 181x181 grid, then multiple local refinements.
grid=[]
best=(1e99,None)
for u in np.linspace(0,1,181,endpoint=False):
    for v in np.linspace(0,1,181,endpoint=False):
        z=odd_fraction_uv((u,v))
        if z<best[0]: best=(z,np.array([u,v]))
# refine best plus symmetry-shifted nearby starts
starts=[best[1]]
rng=np.random.default_rng(20260919)
for _ in range(16): starts.append(rng.random(2))
refs=[]
for st in starts:
    rr=minimize(odd_fraction_uv,st,method='Nelder-Mead',options={'xatol':1e-13,'fatol':1e-15,'maxiter':10000})
    uv=np.mod(rr.x,1.0); val=odd_fraction_uv(uv); refs.append((val,uv))
refs.sort(key=lambda x:x[0])
amin=float(refs[0][0]); uv_center=refs[0][1]; a_center=A@uv_center
spread=float(max(v for v,_ in refs if v<amin+1e-10)-min(v for v,_ in refs if v<amin+1e-10)) if refs else np.nan
c0,s0=translated_coeffs(BASE,a_center)

CENTER=J.FourierLandscape('2H_centered',BASE.vectors.copy(),c0.copy(),s0.copy(),BASE.energy_unit_meV,'same 2H translated to minimized odd-power center')
SYM=J.FourierLandscape('2H_matched_symmetrized',BASE.vectors.copy(),c0.copy(),np.zeros_like(s0),BASE.energy_unit_meV,'same centered 2H with odd coefficients zeroed')
INV=J.FourierLandscape('2H_exact_inverted',BASE.vectors.copy(),c0.copy(),-s0.copy(),BASE.energy_unit_meV,'exact spatial inversion of centered 2H')


def wrap(x):
    uv=AINV@np.asarray(x,float); uv-=np.floor(uv); return A@uv

def pdelta(a,b):
    uv=AINV@(np.asarray(a,float)-np.asarray(b,float)); uv-=np.round(uv); return A@uv

def pdist(a,b): return float(np.linalg.norm(pdelta(a,b)))

def eval_land(S,land,xy,F=0.0):
    return J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0.0,float(F))

def enumerate_stationary(land,theta=THETA,force_y=0.0,nseed=21):
    S=J.contact_factors(float(theta),land.vectors); out=[]
    for u in np.linspace(0,1,nseed,endpoint=False):
        for v in np.linspace(0,1,nseed,endpoint=False):
            seed=A@np.array([u,v])
            def fun(z): return eval_land(S,land,z,force_y)[1]
            def jac(z): return eval_land(S,land,z,force_y)[2]
            rr=root(fun,seed,jac=jac,method='hybr',tol=1e-12)
            if np.linalg.norm(fun(rr.x))>2e-9: continue
            w=wrap(rr.x)
            if any(pdist(w,q['xy'])<3e-6 for q in out): continue
            U,g,H=eval_land(S,land,w,force_y); eig=np.linalg.eigvalsh(H)
            out.append({'xy':w,'U':float(U),'eig':eig,'res':float(np.linalg.norm(g))})
    out.sort(key=lambda q:q['U'])
    return out

def solve_equilibrium(S,land,xy0,F):
    xy=np.asarray(xy0,float).copy()
    for _ in range(100):
        U,g,H=eval_land(S,land,xy,F); gn=float(np.linalg.norm(g))
        if gn<1e-11: return True,xy,gn
        try: step=np.linalg.solve(H,g)
        except np.linalg.LinAlgError: step=np.linalg.pinv(H)@g
        sn=np.linalg.norm(step)
        if sn>0.06: step*=0.06/sn
        alpha=1.0; ok=False
        for _ in range(15):
            trial=xy-alpha*step; gt=eval_land(S,land,trial,F)[1]
            if np.linalg.norm(gt)<gn: xy=trial;ok=True;break
            alpha*=0.5
        if not ok: return False,xy,gn
    return False,xy,float(np.linalg.norm(eval_land(S,land,xy,F)[1]))

def branch_fold(land,xy0,direction,theta=THETA):
    S=J.contact_factors(float(theta),land.vectors)
    xy=np.asarray(xy0,float).copy(); rec=[]
    # continue in force to seed fold
    for f in np.arange(0,5.0001,0.01):
        ok,newxy,res=solve_equilibrium(S,land,xy,direction*f)
        if not ok: break
        if f>0 and pdist(newxy,xy)>0.18: break
        xy=newxy
        U,g,H=eval_land(S,land,xy,direction*f); eig=np.linalg.eigvalsh(H)
        rec.append((float(f),xy.copy(),eig.copy()))
        if eig[0]<2e-4: break
    if len(rec)<2: raise RuntimeError('continuation failed')
    near=min(rec[-30:] if len(rec)>30 else rec,key=lambda z:abs(z[2][0]))
    def feq(z):
        U,g,H=eval_land(S,land,z,0.0); return np.array([g[0],np.linalg.det(H)])
    cand=[]
    for dx,dy in [(0,0),(.002,0),(-.002,0),(0,.002),(0,-.002),(.01,0),(-.01,0),(0,.01),(0,-.01)]:
        rr=root(feq,near[1]+[dx,dy],method='hybr',tol=1e-12)
        res=float(np.linalg.norm(feq(rr.x)))
        if res>1e-7: continue
        U,g,H=eval_land(S,land,rr.x,0.0); fc=float(direction*g[1]); eig=np.linalg.eigvalsh(H)
        if fc<0 or eig[1]<=1e-7: continue
        Ut,gt,Ht=eval_land(S,land,rr.x,direction*fc)
        full=float(np.linalg.norm(np.r_[gt,np.linalg.det(Ht)]))
        score=abs(fc-near[0])+0.05*pdist(rr.x,near[1])+1000*full
        cand.append((score,fc,rr.x.copy(),eig,full))
    if not cand: raise RuntimeError('fold refine failed')
    cand.sort(key=lambda x:x[0]); _,fc,xyf,eig,res=cand[0]
    return {'Fc':float(fc),'xy':xyf,'eig':eig,'res':float(res),'ncont':len(rec)}

# Pointwise symmetry identities, local and finite-contact.
rng=np.random.default_rng(20260920)
local_sym=local_inv=0.0
contact_sym=contact_inv=0.0
Ssym=J.contact_factors(THETA,SYM.vectors)
Sorig=J.contact_factors(THETA,CENTER.vectors)
Sinv=J.contact_factors(THETA,INV.vectors)
for _ in range(10000):
    uv=rng.uniform(-2,2,2); r=A@uv
    local_sym=max(local_sym,abs(float(SYM.potential(r[0],r[1]))-float(SYM.potential(-r[0],-r[1]))))
    local_inv=max(local_inv,abs(float(INV.potential(r[0],r[1]))-float(CENTER.potential(-r[0],-r[1]))))
    us=eval_land(Ssym,SYM,r,0)[0]; usm=eval_land(Ssym,SYM,-r,0)[0]
    uinv=eval_land(Sinv,INV,r,0)[0]; uom=eval_land(Sorig,CENTER,-r,0)[0]
    contact_sym=max(contact_sym,abs(us-usm)); contact_inv=max(contact_inv,abs(uinv-uom))

# Static branch audit at theta=1.5.
stat_rows=[]; static_summary={}
mins_by={}
for land in [CENTER,SYM,INV]:
    sols=enumerate_stationary(land); mins=[q for q in sols if q['eig'][0]>1e-7]; mins.sort(key=lambda q:q['U']); mins_by[land.name]=mins
    for i,q in enumerate(mins):
        fp=branch_fold(land,q['xy'],+1); fm=branch_fold(land,q['xy'],-1)
        stat_rows.append({'surface':land.name,'minimum':i,'U0':q['U'],'x0':q['xy'][0],'y0':q['xy'][1],
                          'Fc_plus':fp['Fc'],'Fc_minus':fm['Fc'],'DeltaFc':fp['Fc']-fm['Fc'],
                          'plus_hard':fp['eig'][1],'minus_hard':fm['eig'][1],
                          'plus_res':fp['res'],'minus_res':fm['res']})
    rows=[x for x in stat_rows if x['surface']==land.name]
    static_summary[land.name]={'n_stable_minima':len(mins),
        'global_plus':max(x['Fc_plus'] for x in rows),'global_minus':max(x['Fc_minus'] for x in rows),
        'ground_plus':rows[0]['Fc_plus'],'ground_minus':rows[0]['Fc_minus'],'U0_ground':rows[0]['U0']}
static_df=pd.DataFrame(stat_rows); static_df.to_csv(ROOT/'same2h_static_branch_contracts.csv',index=False)

# Dynamics: independent full-2D unguided RK4.
@njit
def grad_xy(x,y,vr,c,s,sr,si):
    gx=0.0;gy=0.0
    for t in range(vr.shape[0]):
        Gx=vr[t,0];Gy=vr[t,1];q=Gx*x+Gy*y; cq=math.cos(q);sq=math.sin(q)
        re=sr[t]*cq-si[t]*sq; im=sr[t]*sq+si[t]*cq
        a=-c[t]*im+s[t]*re;gx+=a*Gx;gy+=a*Gy
    return gx,gy

@njit
def rk4_vector(vr,c,s,sr,si,x0,y0,F0,period,n_eq,n_meas,spc):
    dt=period/spc; om=2*math.pi/period
    x=x0;y=y0;vx=0.0;vy=0.0;xm=x0;ym=y0
    total=(n_eq+n_meas)*spc
    for i in range(total):
        t=i*dt
        def der(tt,xx,yy,vxx,vyy):
            gx,gy=grad_xy(xx,yy,vr,c,s,sr,si)
            return vxx,vyy,(-gx-GAMMA*vxx)/MASS,(F0*math.sin(om*tt)-gy-GAMMA*vyy)/MASS
        a,b,c1,d=der(t,x,y,vx,vy)
        a2,b2,c2,d2=der(t+dt/2,x+a*dt/2,y+b*dt/2,vx+c1*dt/2,vy+d*dt/2)
        a3,b3,c3,d3=der(t+dt/2,x+a2*dt/2,y+b2*dt/2,vx+c2*dt/2,vy+d2*dt/2)
        a4,b4,c4,d4=der(t+dt,x+a3*dt,y+b3*dt,vx+c3*dt,vy+d3*dt)
        x+=dt*(a+2*a2+2*a3+a4)/6; y+=dt*(b+2*b2+2*b3+b4)/6
        vx+=dt*(c1+2*c2+2*c3+c4)/6; vy+=dt*(d+2*d2+2*d3+d4)/6
        if i==n_eq*spc-1: xm=x;ym=y
    return x,y,vx,vy,xm,ym

def dyn_one(land,xy0,spc=SPC):
    Sf=J.contact_factors(THETA,land.vectors)
    x,y,vx,vy,xm,ym=rk4_vector(np.asarray(land.vectors,float),np.asarray(land.c_cos,float),np.asarray(land.c_sin,float),
                                np.asarray(Sf.real,float),np.asarray(Sf.imag,float),float(xy0[0]),float(xy0[1]),F0,PERIOD,N_EQ,N_MEAS,spc)
    duv=AINV@np.array([x-xm,y-ym])/N_MEAS
    nearest=np.rint(duv); err=float(np.linalg.norm(duv-nearest))
    return {'m_mean':float(duv[0]),'n_mean':float(duv[1]),'m_int':int(nearest[0]),'n_int':int(nearest[1]),'locking_error':err,
            'xf':x,'yf':y,'vxf':vx,'vyf':vy}

dyn=[]
# unique-ground original and inversion
for land in [CENTER,INV]:
    q=mins_by[land.name][0]; rr=dyn_one(land,q['xy']); dyn.append({'surface':land.name,'preparation':'ground',**rr})
# both degenerate symmetric minima
for i,q in enumerate(mins_by[SYM.name]):
    rr=dyn_one(SYM,q['xy']); dyn.append({'surface':SYM.name,'preparation':f'minimum_{i}',**rr})
dyn_df=pd.DataFrame(dyn); dyn_df.to_csv(ROOT/'same2h_dynamical_contracts.csv',index=False)

# symmetric balanced current = equal average of the inversion-paired preparations
sd=dyn_df[dyn_df.surface==SYM.name]
sym_mean=np.array([sd.m_mean.mean(),sd.n_mean.mean()])
orig=dyn_df[dyn_df.surface==CENTER.name].iloc[0]; inv=dyn_df[dyn_df.surface==INV.name].iloc[0]
current_reversal=np.array([orig.m_mean+inv.m_mean,orig.n_mean+inv.n_mean])

# timestep checks for main symmetry contractions
step_rows=[]
for spc in [1000,2000,4000,8000]:
    ro=dyn_one(CENTER,mins_by[CENTER.name][0]['xy'],spc)
    ri=dyn_one(INV,mins_by[INV.name][0]['xy'],spc)
    rs=[dyn_one(SYM,q['xy'],spc) for q in mins_by[SYM.name]]
    sb=np.mean([[x['m_mean'],x['n_mean']] for x in rs],axis=0)
    cr=np.array([ro['m_mean']+ri['m_mean'],ro['n_mean']+ri['n_mean']])
    step_rows.append({'steps_per_cycle':spc,'orig_m':ro['m_mean'],'orig_n':ro['n_mean'],'inv_m':ri['m_mean'],'inv_n':ri['n_mean'],
                      'reversal_norm':float(np.linalg.norm(cr)),'sym_balanced_norm':float(np.linalg.norm(sb)),
                      'orig_lock_err':ro['locking_error'],'inv_lock_err':ri['locking_error']})
pd.DataFrame(step_rows).to_csv(ROOT/'same2h_timestep_contracts.csv',index=False)

# contracts
sg=static_summary
sym_split=abs(sg[SYM.name]['global_plus']-sg[SYM.name]['global_minus'])
swap1=abs(sg[INV.name]['ground_plus']-sg[CENTER.name]['ground_minus'])
swap2=abs(sg[INV.name]['ground_minus']-sg[CENTER.name]['ground_plus'])
# original centering should not alter previous physical thresholds; reference from N1 audit
refp=3.0711353385; refm=1.2586722985
summary={
 'inversion_center':{'uv':uv_center.tolist(),'xy':a_center.tolist(),'A_min':amin,'odd_RMS':math.sqrt(amin),'local_refinement_spread':spread},
 'pointwise_identities':{'local_sym_even_max_abs':local_sym,'local_inv_identity_max_abs':local_inv,'contact_sym_even_max_abs':contact_sym,'contact_inv_identity_max_abs':contact_inv},
 'static':{'centered_ground_plus':sg[CENTER.name]['ground_plus'],'centered_ground_minus':sg[CENTER.name]['ground_minus'],
           'centered_vs_prior_max_abs':max(abs(sg[CENTER.name]['ground_plus']-refp),abs(sg[CENTER.name]['ground_minus']-refm)),
           'sym_global_plus':sg[SYM.name]['global_plus'],'sym_global_minus':sg[SYM.name]['global_minus'],'sym_global_split':sym_split,
           'inverted_ground_plus':sg[INV.name]['ground_plus'],'inverted_ground_minus':sg[INV.name]['ground_minus'],
           'inversion_swap_errors':[swap1,swap2],
           'max_fold_residual':float(static_df[['plus_res','minus_res']].to_numpy().max()),
           'min_hard_eigenvalue':float(static_df[['plus_hard','minus_hard']].to_numpy().min())},
 'dynamics':{'theta_deg':THETA,'F0':F0,'period':PERIOD,'n_eq':N_EQ,'n_meas':N_MEAS,'steps_per_cycle':SPC,
             'original_winding':[int(orig.m_int),int(orig.n_int)],'inverted_winding':[int(inv.m_int),int(inv.n_int)],
             'current_reversal_vector':current_reversal.tolist(),'current_reversal_norm':float(np.linalg.norm(current_reversal)),
             'sym_balanced_current':sym_mean.tolist(),'sym_balanced_current_norm':float(np.linalg.norm(sym_mean)),
             'max_locking_error':float(dyn_df.locking_error.max())},
}
summary['gate_checks']={
 'A_min_match':abs(amin-0.04253608528)<5e-11,
 'sym_local_even':local_sym<1e-12,
 'inv_local_exact':local_inv<1e-12,
 'sym_contact_even':contact_sym<1e-12,
 'inv_contact_exact':contact_inv<1e-12,
 'sym_static_degenerate':sym_split<1e-7,
 'exact_inversion_threshold_swap':max(swap1,swap2)<1e-7,
 'exact_inversion_current_reversal':float(np.linalg.norm(current_reversal))<1e-10,
 'sym_balanced_zero_current':float(np.linalg.norm(sym_mean))<1e-10,
 'fold_numerics':summary['static']['max_fold_residual']<1e-7 and summary['static']['min_hard_eigenvalue']>1e-6,
}
summary['gate']='PASS' if all(summary['gate_checks'].values()) else 'FAIL'
(ROOT/'same2h_symmetry_audit_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
print('\nSTATIC\n',static_df.to_string(index=False))
print('\nDYNAMICS\n',dyn_df.to_string(index=False))
