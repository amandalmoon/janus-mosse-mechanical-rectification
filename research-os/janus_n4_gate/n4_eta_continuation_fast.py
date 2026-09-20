import sys, math, json
from pathlib import Path
import numpy as np, pandas as pd
from scipy.optimize import root, least_squares
sys.path.insert(0,'/mnt/data/janus_n4_gate')
from n4_core import *
OUT=Path('/mnt/data/janus_n4_gate')
SCAN=pd.read_csv(OUT/'n4_gauge_scan.csv')
idx_orig=int(SCAN.index[(SCAN.u.abs()<1e-12)&(SCAN.v.abs()<1e-12)][0])
idx_center=int(SCAN.index[SCAN.is_amin_center.astype(bool)][0])
idx_min=int(SCAN.slope_fd_005.idxmin()); idx_max=int(SCAN.slope_fd_005.idxmax()); idx_zero=int(SCAN.slope_fd_005.abs().idxmin())
selected=[]
for idx,label in [(idx_orig,'published_origin'),(idx_center,'Amin_center'),(idx_min,'min_slope_tested'),(idx_max,'max_slope_tested'),(idx_zero,'near_zero_slope_tested')]:
    if idx not in [i for i,_ in selected]: selected.append((idx,label))

def fold_aug_from_seed(land, sign, seed):
    S=J.contact_factors(THETA,land.vectors,POS)
    def aug(q):
        xx,yy,F=q; U,g,H=J.contact_ugh(xx,yy,S,land,0,sign*F); return np.array([g[0],g[1],np.linalg.det(H)])
    ls=least_squares(aug,seed,xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=1200,x_scale='jac')
    q=ls.x; U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]); ev=np.linalg.eigvalsh(H); res=float(np.linalg.norm(aug(q)))
    if res>2e-6 or q[2]<=0 or ev[1]<1e-5: return None
    return q,ev,res

def zero_root_from_seed(land,seed):
    S=J.contact_factors(THETA,land.vectors,POS)
    f=lambda z:J.contact_ugh(z[0],z[1],S,land,0,0)[1]
    jac=lambda z:J.contact_ugh(z[0],z[1],S,land,0,0)[2]
    rr=root(f,seed,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':800})
    if np.linalg.norm(f(rr.x))>1e-7:return None
    U,g,H=J.contact_ugh(rr.x[0],rr.x[1],S,land,0,0);ev=np.linalg.eigvalsh(H)
    if ev[0]<=1e-7:return None
    return rr.x,float(U),ev

def pdxy(x1,x2):
    duv=AINV@(np.asarray(x1)-np.asarray(x2));duv-=np.round(duv);return float(np.linalg.norm(A@duv))

rows=[]; checks=[]; summaries=[]
etas=np.round(np.arange(1.0,0.0,-0.025),6)
for idx,label in selected:
    uv=SCAN.loc[idx,['u','v']].to_numpy(float); tr=translate_landscape(BASE,A@uv,label)
    L=scale_odd(tr,1.0); mins=enumerate_minima(L,ngrid=13); ground=mins[0]
    fpp=branch_fold(L,ground['xy'],+1); fmm=branch_fold(L,ground['xy'],-1)
    xg=ground['xy'].copy(); seedp=np.r_[fpp['xy'],fpp['Fc']]; seedm=np.r_[fmm['xy'],fmm['Fc']]
    for eta in etas:
        L=scale_odd(tr,float(eta))
        if eta<1:
            zr=zero_root_from_seed(L,xg)
            if zr is None:
                mins=enumerate_minima(L,ngrid=11); xg=mins[0]['xy'].copy()
            else: xg=zr[0]
        # Every 0.1 (and eta .025/.05) independently verify tracked min is actual ground.
        if abs((eta*10)-round(eta*10))<1e-8 or eta in (0.025,0.05):
            mins=enumerate_minima(L,ngrid=11); g=mins[0]
            dist=pdxy(xg,g['xy']);
            # If ground switches, reset the branch and folds from actual ground.
            if dist>1e-4:
                xg=g['xy'].copy(); fpp=branch_fold(L,xg,+1); fmm=branch_fold(L,xg,-1); seedp=np.r_[fpp['xy'],fpp['Fc']]; seedm=np.r_[fmm['xy'],fmm['Fc']]
            checks.append(dict(label=label,eta=eta,nmin=len(mins),ground_U=g['U'],tracked_ground_dist=dist,energy_gap=(mins[1]['U']-mins[0]['U'] if len(mins)>1 else np.nan)))
        rp=fold_aug_from_seed(L,+1,seedp); rm=fold_aug_from_seed(L,-1,seedm)
        if rp is None or rm is None:
            fpp=branch_fold(L,xg,+1); fmm=branch_fold(L,xg,-1); seedp=np.r_[fpp['xy'],fpp['Fc']];seedm=np.r_[fmm['xy'],fmm['Fc']]
            rp=(seedp,None,fpp['res']); rm=(seedm,None,fmm['res'])
        qp,evp,rp_res=rp; qm,evm,rm_res=rm
        seedp=qp.copy(); seedm=qm.copy()
        Fp=float(qp[2]);Fm=float(qm[2]);D=Fp-Fm
        rows.append(dict(label=label,gauge_index=idx,u=uv[0],v=uv[1],eta=eta,Fp=Fp,Fm=Fm,Delta=D,rho=D/(Fp+Fm),fold_res=max(rp_res,rm_res)))
    qdf=pd.DataFrame([r for r in rows if r['label']==label]).sort_values('eta')
    # prepend symmetry null at 0 only for delta/rho; Fp/Fm left NaN because value is gauge-dependent and not needed here.
    rows.append(dict(label=label,gauge_index=idx,u=uv[0],v=uv[1],eta=0.0,Fp=np.nan,Fm=np.nan,Delta=0.0,rho=0.0,fold_res=np.nan))
    qdf=pd.DataFrame([r for r in rows if r['label']==label]).sort_values('eta')
    opt=qdf.loc[qdf.Delta.idxmax()]
    # local slope from continuation points eta 0.025,0.05,0.075,0.1; antisymmetry means D(-eta)=-D(eta), fit through origin.
    local=qdf[(qdf.eta>0)&(qdf.eta<=0.100001)]
    x=local.eta.to_numpy();y=local.Delta.to_numpy();slope=float(np.dot(x,y)/np.dot(x,x)); fit=slope*x; r2=float(1-np.sum((y-fit)**2)/np.sum((y-y.mean())**2))
    summaries.append(dict(label=label,gauge_index=idx,u=uv[0],v=uv[1],odd_fraction=odd_fraction(tr),slope=slope,slope_R2=r2,eta_opt_grid=float(opt.eta),Delta_opt=float(opt.Delta),Delta_eta1=float(qdf[qdf.eta==1].Delta.iloc[0])))
    print(label,'slope',slope,'opt',float(opt.eta),'Dopt',float(opt.Delta),flush=True)

DF=pd.DataFrame(rows).sort_values(['label','eta']);DF.to_csv(OUT/'n4_selected_eta_curves.csv',index=False)
CK=pd.DataFrame(checks);CK.to_csv(OUT/'n4_eta_ground_tracking_checks.csv',index=False)
SM=pd.DataFrame(summaries);SM.to_csv(OUT/'n4_selected_gauge_summary.csv',index=False)
print(SM.to_string(index=False))
