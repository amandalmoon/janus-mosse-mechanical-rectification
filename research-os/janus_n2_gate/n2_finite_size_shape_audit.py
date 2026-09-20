from pathlib import Path
import sys, math, json
import numpy as np
import pandas as pd
from scipy.optimize import least_squares, root
from scipy.stats import linregress

ROOT=Path('/mnt/data/janus_n2_gate/release/Janus_MoSSe_CanonicalUnguided_BaselineRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J

OUT=Path('/mnt/data/janus_n2_gate')
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)
ZP0=np.array([0.015107260117101675,0.1812524912332831,3.4851202323700723])
ZM0=np.array([0.000055218492948535126,-0.17363318390044577,1.4222355051564721])


def make_disk(R):
    M=int(math.ceil(R+2)); pts=[]
    for q in range(-2*M,2*M+1):
        for r in range(-2*M,2*M+1):
            p=q*J.A1+r*J.A2
            if np.linalg.norm(p)<=R+1e-12: pts.append(p)
    pts=np.array(pts,float); pts-=pts.mean(axis=0); return pts


def fold(theta,sign,zprev,pos):
    S=J.contact_factors(float(theta),land.vectors,pos)
    def aug(q):
        x,y,F=q
        U,g,H=J.contact_ugh(float(x),float(y),S,land,0.0,sign*float(F))
        return np.array([g[0],g[1],np.linalg.det(H)])
    cands=[]
    starts=[]
    for dx in [0,.001,-.001,.01,-.01]:
        starts.append(np.array(zprev,float)+[dx,0,0])
    for st in starts:
        ls=least_squares(aug,st,xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=3000,x_scale='jac')
        q=ls.x
        U,g,H=J.contact_ugh(float(q[0]),float(q[1]),S,land,0.0,sign*float(q[2]))
        ev=np.linalg.eigvalsh(H)
        res=np.linalg.norm(aug(q))
        if res<1e-7 and q[2]>0 and ev[1]>1e-6:
            score=abs(q[2]-zprev[2])+np.linalg.norm(q[:2]-zprev[:2])*.02
            cands.append((score,q,ev,res))
    if not cands:
        raise RuntimeError(('fold_failed',theta,sign,len(pos)))
    cands.sort(key=lambda t:t[0])
    _,q,ev,res=cands[0]
    return q,ev,res


def exact_characteristic(pos,sign,targetF,theta_lo,theta_hi,zlo,zhi):
    # Solve gx=0, gy=0, detH=0 with F fixed and theta unknown.
    # Multiple starts inside the dense-grid bracket; choose lowest residual inside bracket.
    def aug(w):
        x,y,theta=w
        S=J.contact_factors(float(theta),land.vectors,pos)
        U,g,H=J.contact_ugh(float(x),float(y),S,land,0.0,sign*float(targetF))
        return np.array([g[0],g[1],np.linalg.det(H)])
    cands=[]
    fracs=[0.0,0.25,0.5,0.75,1.0]
    for f in fracs:
        th=theta_lo+f*(theta_hi-theta_lo)
        xy=(1-f)*zlo[:2]+f*zhi[:2]
        st=np.array([xy[0],xy[1],th])
        lo=np.array([-np.inf,-np.inf,theta_lo-1e-10])
        hi=np.array([ np.inf, np.inf,theta_hi+1e-10])
        ls=least_squares(aug,st,bounds=(lo,hi),xtol=2e-13,ftol=2e-13,gtol=2e-13,max_nfev=5000,x_scale='jac')
        w=ls.x; res=np.linalg.norm(aug(w))
        S=J.contact_factors(float(w[2]),land.vectors,pos)
        U,g,H=J.contact_ugh(float(w[0]),float(w[1]),S,land,0.0,sign*float(targetF))
        ev=np.linalg.eigvalsh(H)
        if res<2e-7 and ev[1]>1e-6 and theta_lo-1e-8<=w[2]<=theta_hi+1e-8:
            cands.append((res,w,ev))
    if not cands:
        raise RuntimeError(('char_failed',len(pos),sign,targetF,theta_lo,theta_hi))
    cands.sort(key=lambda t:t[0])
    res,w,ev=cands[0]
    return w,ev,res


def uv_to_xy(uv): return A@np.asarray(uv,float)
def wrap_uv(xy):
    uv=AINV@np.asarray(xy,float); return uv-np.floor(uv)
def pdist(uv1,uv2):
    d=np.asarray(uv1)-np.asarray(uv2); d-=np.round(d); return np.linalg.norm(A@d)


def enumerate_stationary(theta,pos,ngrid=17):
    S=J.contact_factors(float(theta),land.vectors,pos); roots=[]
    for u in np.linspace(0,1,ngrid,endpoint=False):
        for v in np.linspace(0,1,ngrid,endpoint=False):
            x0=uv_to_xy((u,v))
            def fun(xy): return J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0.0,0.0)[1]
            def jac(xy): return J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0.0,0.0)[2]
            rr=root(fun,x0,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':500})
            if np.linalg.norm(fun(rr.x))>1e-7: continue
            uv=wrap_uv(rr.x)
            if any(pdist(uv,r['uv'])<2e-6 for r in roots): continue
            xy=uv_to_xy(uv); U,g,H=J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0.0,0.0)
            ev=np.linalg.eigvalsh(H)
            roots.append({'uv':uv,'U':float(U),'ev':ev})
    roots.sort(key=lambda r:r['U']); return roots


def branch_fold_from_min(theta,pos,uv0,sign,step=0.02,maxF=5.0):
    S=J.contact_factors(float(theta),land.vectors,pos)
    x=uv_to_xy(uv0).astype(float); F=0.; last=None
    while F<=maxF+1e-12:
        def fun(xy): return J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0.0,sign*F)[1]
        def jac(xy): return J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0.0,sign*F)[2]
        # root(hybr) can report failure despite a converged tiny-residual solution; accept by residual.
        rr=root(fun,x,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':500})
        res0=np.linalg.norm(fun(rr.x))
        if res0>1e-7:
            ls=least_squares(fun,x,jac=jac,xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=1000)
            if np.linalg.norm(fun(ls.x))>1e-7: break
            x=ls.x
        else:
            x=rr.x
        U,g,H=J.contact_ugh(float(x[0]),float(x[1]),S,land,0.0,sign*F); ev=np.linalg.eigvalsh(H)
        if ev[0]>1e-6: last=(F,x.copy())
        if ev[0]<1e-5 and F>step: break
        F+=step
    if last is None: raise RuntimeError(('no_stable',theta,len(pos),sign))
    Fg,xg=last
    zseed=np.array([xg[0],xg[1],max(Fg,1e-6)])
    q,ev,res=fold(theta,sign,zseed,pos)
    return q,res

# A. Original ten-hex dense scaled-twist grid.
orig_shells=list(range(3,13))
orig_rows=[]; fold_state={}
Thetas=np.arange(0.,30.0001,1.0)
for sh in orig_shells:
    pos=J.make_hexagonal_flake(sh); N=len(pos)
    zp=ZP0.copy(); zm=ZM0.copy(); F0p=F0m=None
    states_p={};states_m={}
    for Th in Thetas:
        theta=float(Th/math.sqrt(N))
        zp,evp,rp=fold(theta,+1,zp,pos); zm,evm,rm=fold(theta,-1,zm,pos)
        states_p[float(Th)]=zp.copy();states_m[float(Th)]=zm.copy()
        if Th==0: F0p=zp[2];F0m=zm[2]
        orig_rows.append(dict(shell=sh,N=N,Theta=Th,theta_deg=theta,Fp=zp[2],Fm=zm[2],Fp_norm=zp[2]/F0p,Fm_norm=zm[2]/F0m,rho=(zp[2]-zm[2])/(zp[2]+zm[2]),hard_p=evp[1],hard_m=evm[1],res_p=rp,res_m=rm))
    fold_state[(N,+1)]=states_p;fold_state[(N,-1)]=states_m
    print('dense original',N)
orig=pd.DataFrame(orig_rows); orig.to_csv(OUT/'n2_original_hex_dense_theta_scaled.csv',index=False)

# Collapse metrics across original 10 sizes.
collapse=[]
for limit in [18,24,30]:
    sub=orig[orig.Theta<=limit+1e-12]
    mxp=mxm=mxr=0.0
    worstp=worstm=worstr=None
    for Th,q in sub.groupby('Theta'):
        for key in ['Fp_norm','Fm_norm','rho']:
            mean=float(q[key].mean()); vals=np.abs(q[key]-mean)/abs(mean); idx=vals.idxmax(); val=float(vals.loc[idx])
            if key=='Fp_norm' and val>mxp: mxp=val;worstp=(Th,int(q.loc[idx,'N']))
            if key=='Fm_norm' and val>mxm: mxm=val;worstm=(Th,int(q.loc[idx,'N']))
            if key=='rho' and val>mxr: mxr=val;worstr=(Th,int(q.loc[idx,'N']))
    collapse.append(dict(Theta_limit=limit,Fp_max_rel=mxp,Fm_max_rel=mxm,rho_max_rel=mxr,Fp_worst=str(worstp),Fm_worst=str(worstm),rho_worst=str(worstr)))
pd.DataFrame(collapse).to_csv(OUT/'n2_original_hex_collapse_metrics.csv',index=False)

# B. Exact characteristic angles and power-law fits.
qs=[0.95,0.90,0.85,0.80]
char=[]
for sh in orig_shells:
    pos=J.make_hexagonal_flake(sh);N=len(pos)
    for sign,label,F0col,normcol in [(+1,'plus',ZP0[2],'Fp_norm'),(-1,'minus',ZM0[2],'Fm_norm')]:
        g=orig[orig.N==N].sort_values('Theta')
        for qtar in qs:
            target=float(qtar*F0col)
            vals=g[normcol].to_numpy(); ths=g.Theta.to_numpy()
            idx=np.where(vals<=qtar)[0]
            if len(idx)==0: raise RuntimeError(('no bracket',N,label,qtar,vals[-1]))
            hi_i=int(idx[0]); lo_i=max(0,hi_i-1)
            Thlo=float(ths[lo_i]); Thhi=float(ths[hi_i])
            theta_lo=Thlo/math.sqrt(N);theta_hi=Thhi/math.sqrt(N)
            zlo=fold_state[(N,sign)][Thlo];zhi=fold_state[(N,sign)][Thhi]
            w,ev,res=exact_characteristic(pos,sign,target,theta_lo,theta_hi,zlo,zhi)
            char.append(dict(N=N,shell=sh,direction=label,q=qtar,theta_q_deg=w[2],Theta_q=w[2]*math.sqrt(N),target_F=target,hard=ev[1],res=res,bracket_Theta_lo=Thlo,bracket_Theta_hi=Thhi))
            print('char',N,label,qtar,w[2]*math.sqrt(N))
char=pd.DataFrame(char);char.to_csv(OUT/'n2_characteristic_angles_exact.csv',index=False)

fits=[];conv=[]
for direction in ['plus','minus']:
    for qtar in qs:
        d=char[(char.direction==direction)&(char.q==qtar)].sort_values('N')
        lr=linregress(np.log(d.N),np.log(d.theta_q_deg))
        alpha=-lr.slope
        fits.append(dict(direction=direction,q=qtar,Nmin=int(d.N.min()),Nmax=int(d.N.max()),n=len(d),alpha=alpha,R2=lr.rvalue**2,stderr=lr.stderr,C=math.exp(lr.intercept),alpha_minus_half=alpha-.5))
        Ns=d.N.to_numpy()
        for imin in range(0,6):
            dd=d.iloc[imin:]
            lr2=linregress(np.log(dd.N),np.log(dd.theta_q_deg)); a=-lr2.slope
            conv.append(dict(direction=direction,q=qtar,Nmin=int(dd.N.min()),n=len(dd),alpha=a,R2=lr2.rvalue**2,stderr=lr2.stderr,alpha_minus_half=a-.5))
pd.DataFrame(fits).to_csv(OUT/'n2_characteristic_powerlaw_fits.csv',index=False)
pd.DataFrame(conv).to_csv(OUT/'n2_alpha_convergence.csv',index=False)

# C. Dense extended shape grid 0<=Theta<=20.
shapes=[]
for sh in [6,8,10,12,14,16,18,20]: shapes.append(('hex',f'shell{sh}',J.make_hexagonal_flake(sh)))
for R in [6,8,10,12,14,16]: shapes.append(('disk',f'R{R}',make_disk(R)))
ext_rows=[]
for fam,name,pos in shapes:
    N=len(pos);zp=ZP0.copy();zm=ZM0.copy();F0p=F0m=None
    for Th in np.arange(0.,20.0001,1.0):
        theta=float(Th/math.sqrt(N));zp,evp,rp=fold(theta,+1,zp,pos);zm,evm,rm=fold(theta,-1,zm,pos)
        if Th==0:F0p=zp[2];F0m=zm[2]
        ext_rows.append(dict(family=fam,shape=name,N=N,Theta=Th,theta_deg=theta,Fp=zp[2],Fm=zm[2],Fp_norm=zp[2]/F0p,Fm_norm=zm[2]/F0m,rho=(zp[2]-zm[2])/(zp[2]+zm[2]),hard_p=evp[1],hard_m=evm[1],res_p=rp,res_m=rm))
    print('dense extended',fam,name,N)
ext=pd.DataFrame(ext_rows);ext.to_csv(OUT/'n2_extended_shape_dense.csv',index=False)

shape_metrics=[]
for Th in sorted(ext.Theta.unique()):
    h=ext[(ext.family=='hex')&(ext.Theta==Th)];d=ext[(ext.family=='disk')&(ext.Theta==Th)]
    row={'Theta':Th}
    for fam,qdf in [('hex',h),('disk',d)]:
        for key in ['Fp_norm','Fm_norm','rho']:
            mean=float(qdf[key].mean()); rel=float(np.max(np.abs(qdf[key]-mean)/abs(mean)))
            row[f'{fam}_{key}_maxrel']=rel;row[f'{fam}_{key}_mean']=mean
    for key in ['Fp_norm','Fm_norm','rho']:
        hm=float(h[key].mean());dm=float(d[key].mean());row[f'family_{key}_reldiff']=abs(hm-dm)/abs(hm)
    shape_metrics.append(row)
shape_metrics=pd.DataFrame(shape_metrics);shape_metrics.to_csv(OUT/'n2_extended_shape_dense_metrics.csv',index=False)

# D. High-Theta prepared-state spot checks for sizes whose Theta=30 exceeds 3 degrees.
high_checks=[]
for sh in [3,4,5]:
    pos=J.make_hexagonal_flake(sh);N=len(pos)
    for Th in [24.,30.]:
        theta=Th/math.sqrt(N)
        roots=enumerate_stationary(theta,pos,ngrid=19)
        mins=[r for r in roots if r['ev'][0]>1e-7]
        if not mins: raise RuntimeError(('no minima',N,Th))
        ground=mins[0]
        for sign in [+1,-1]:
            zbranch,res=branch_fold_from_min(theta,pos,ground['uv'],sign,step=.02,maxF=5.)
            zdense=fold_state[(N,sign)][Th]
            high_checks.append(dict(N=N,shell=sh,Theta=Th,theta_deg=theta,n_stationary=len(roots),n_minima=len(mins),ground_U=ground['U'],gap_U=(mins[1]['U']-mins[0]['U']) if len(mins)>1 else np.nan,sign=sign,F_branch=zbranch[2],F_dense=zdense[2],abs_diff=abs(zbranch[2]-zdense[2]),branch_res=res,hard_dense=np.nan))
            print('highcheck',N,Th,sign,abs(zbranch[2]-zdense[2]))
pd.DataFrame(high_checks).to_csv(OUT/'n2_highTheta_prepared_branch_checks.csv',index=False)

# E. Summary / gate.
fitdf=pd.DataFrame(fits);convdf=pd.DataFrame(conv);coldf=pd.DataFrame(collapse)
summary={
 'original_hex_sizes': sorted(orig.N.unique().astype(int).tolist()),
 'dense_Theta_range':[0,30],
 'collapse': coldf.to_dict(orient='records'),
 'characteristic_fits': fitdf.to_dict(orient='records'),
 'alpha_convergence_q090_plus': convdf[(convdf.direction=='plus')&(convdf.q==.90)].to_dict(orient='records'),
 'alpha_convergence_q090_minus': convdf[(convdf.direction=='minus')&(convdf.q==.90)].to_dict(orient='records'),
 'extended_shape_max': {
    'hex_Fp_maxrel':float(shape_metrics.hex_Fp_norm_maxrel.max()),
    'hex_Fm_maxrel':float(shape_metrics.hex_Fm_norm_maxrel.max()),
    'disk_Fp_maxrel':float(shape_metrics.disk_Fp_norm_maxrel.max()),
    'disk_Fm_maxrel':float(shape_metrics.disk_Fm_norm_maxrel.max()),
    'hex_disk_Fp_reldiff':float(shape_metrics.family_Fp_norm_reldiff.max()),
    'hex_disk_Fm_reldiff':float(shape_metrics.family_Fm_norm_reldiff.max()),
    'hex_disk_rho_reldiff':float(shape_metrics.family_rho_reldiff.max()),
 },
 'highTheta_prepared_max_abs_F_diff':float(pd.DataFrame(high_checks).abs_diff.max()),
 'highTheta_min_energy_gap':float(pd.DataFrame(high_checks).gap_U.min()),
 'max_characteristic_residual':float(char.res.max()),
 'min_characteristic_hard_mode':float(char.hard.min()),
}
(OUT/'n2_audit_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
