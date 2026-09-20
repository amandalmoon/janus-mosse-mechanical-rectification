from __future__ import annotations
import sys, math, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import root, least_squares, brentq

ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
import new_physics_v18 as NP

OUT=Path('/mnt/data/janus_n3_gate')
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)
xyA=A@np.array([0.0,0.0]); xyB=A@np.array([1/3,1/3])

def boundary_mask(pos):
    out=[]
    for i in range(len(pos)):
        d=np.linalg.norm(pos-pos[i],axis=1)
        neigh=np.sum((d>1e-6)&(np.abs(d-1)<1e-6))
        out.append(neigh<6)
    return np.asarray(out,bool)

def weighted_S(theta,pos,w=None):
    if w is None:
        return J.contact_factors(theta,land.vectors,pos)
    R=J.rotation_matrix(theta); delta=pos@R.T-pos; ph=delta@land.vectors.T
    return np.sum(w[:,None]*np.exp(1j*ph),axis=0)/np.sum(w)

def ugh(theta,pos,xy,Fy=0.0,w=None):
    S=weighted_S(theta,pos,w)
    return J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0,float(Fy))

def energy(theta,pos,xy,w=None): return float(ugh(theta,pos,xy,0,w)[0])

def pxy(x):
    uv=AINV@np.asarray(x,float); uv-=np.floor(uv); return A@uv,uv

def pdist_uv(u,v):
    d=np.asarray(u)-np.asarray(v); d-=np.round(d); return float(np.linalg.norm(A@d))

def enumerate_minima(theta,pos,w=None,ngrid=21):
    S=weighted_S(theta,pos,w); sols=[]
    for u in np.linspace(0,1,ngrid,endpoint=False):
        for v in np.linspace(0,1,ngrid,endpoint=False):
            x0=A@np.array([u,v])
            def f(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
            def j(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
            rr=root(f,x0,jac=j,method='hybr',options={'xtol':1e-11,'maxfev':1200})
            if not rr.success and np.linalg.norm(f(rr.x))>1e-7: continue
            if np.linalg.norm(f(rr.x))>1e-7: continue
            xy,uv=pxy(rr.x)
            if any(pdist_uv(uv,q['uv'])<2e-5 for q in sols): continue
            U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,0); ev=np.linalg.eigvalsh(H)
            if ev[0]>1e-7:
                sols.append({'uv':uv,'xy':xy,'U':float(U),'eig0':float(ev[0]),'eig1':float(ev[1]),'grad':float(np.linalg.norm(g))})
    sols.sort(key=lambda q:q['U'])
    return sols

def branch_fold(theta,pos,x0,sign,w=None,step0=0.02,Fmax=5.0):
    S=weighted_S(theta,pos,w); x=np.asarray(x0,float).copy(); F=0.; step=step0; prev=(0.,x.copy())
    guess=None
    while F<Fmax:
        Fn=F+step
        def ff(z): return J.contact_ugh(z[0],z[1],S,land,0,sign*Fn)[1]
        def jj(z): return J.contact_ugh(z[0],z[1],S,land,0,sign*Fn)[2]
        rr=root(ff,x,jac=jj,method='hybr',options={'xtol':1e-11,'maxfev':1200})
        resid=np.linalg.norm(ff(rr.x))
        if resid>1e-6:
            if step>5e-4:
                step*=0.5; continue
            guess=np.array([x[0],x[1],F+step/2]); break
        ev=np.linalg.eigvalsh(jj(rr.x)); duv=AINV@(rr.x-x); duv-=np.round(duv); jump=np.linalg.norm(A@duv)
        if jump>.15:
            if step>5e-4:
                step*=0.5; continue
            guess=np.array([x[0],x[1],F]); break
        if ev[0]<=0:
            guess=np.array([(x[0]+rr.x[0])/2,(x[1]+rr.x[1])/2,(F+Fn)/2]); break
        F=Fn; x=rr.x; prev=(F,x.copy())
    if guess is None: raise RuntimeError('no fold bracket')
    def aug(q):
        xx,yy,FM=q; U,g,H=J.contact_ugh(xx,yy,S,land,0,sign*FM)
        return np.array([g[0],g[1],np.linalg.det(H)])
    cand=[]
    for dx in [0,.001,-.001,.01,-.01,.05,-.05]:
        for dy in [0,.001,-.001]:
            ls=least_squares(aug,guess+np.array([dx,dy,0]),xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=5000,x_scale='jac')
            q=ls.x; U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]); ev=np.linalg.eigvalsh(H)
            res=float(np.linalg.norm(aug(q)))
            if res<1e-7 and q[2]>0 and ev[1]>1e-6:
                duv=AINV@(q[:2]-prev[1]); duv-=np.round(duv); dist=float(np.linalg.norm(A@duv))
                score=dist+0.02*abs(q[2]-prev[0])
                cand.append((score,q,ev,res))
    if not cand: raise RuntimeError(f'fold fail theta={theta} sign={sign}')
    cand.sort(key=lambda z:z[0]); _,q,ev,res=cand[0]
    return {'Fc':float(q[2]),'x':float(q[0]),'y':float(q[1]),'soft':float(ev[0]),'hard':float(ev[1]),'resid':res}

def branch_contract(theta,pos,w=None):
    U_A=energy(theta,pos,xyA,w); U_B=energy(theta,pos,xyB,w)
    fAp=branch_fold(theta,pos,xyA,+1,w); fAm=branch_fold(theta,pos,xyA,-1,w)
    fBp=branch_fold(theta,pos,xyB,+1,w); fBm=branch_fold(theta,pos,xyB,-1,w)
    return dict(UA=U_A,UB=U_B,
                FAplus=fAp['Fc'],FAminus=fAm['Fc'],FBplus=fBp['Fc'],FBminus=fBm['Fc'],
                deltaA=fAp['Fc']-fAm['Fc'],deltaB=fBp['Fc']-fBm['Fc'],
                hard_min=min(fAp['hard'],fAm['hard'],fBp['hard'],fBm['hard']),
                fold_resid_max=max(fAp['resid'],fAm['resid'],fBp['resid'],fBm['resid']))

# 1) all orientation energy crossings; same unweighted A/B families
orientation_rows=[]
for phi in [5,10,15,20,25]:
    pos,R=NP.make_fixedN_triangle(phi,127)
    def de(th): return energy(th,pos,xyA)-energy(th,pos,xyB)
    grid=np.linspace(0,4,801); roots=[]
    vals=[de(t) for t in grid]
    for a,b,fa,fb in zip(grid[:-1],grid[1:],vals[:-1],vals[1:]):
        if fa==0: roots.append(float(a))
        elif fa*fb<0: roots.append(float(brentq(de,a,b,xtol=5e-14,rtol=1e-14)))
    orientation_rows.append({'phi_deg':phi,'radius_a':R,'dE_theta0':de(0),'dE_theta3':de(3),'roots_0_4':';'.join(f'{x:.12f}' for x in roots),'first_root_deg':roots[0] if roots else np.nan,'root_inside_0_3':bool(roots and roots[0]<=3)})
pd.DataFrame(orientation_rows).to_csv(OUT/'n3_orientation_energy_crossings.csv',index=False)

# 2) exact unweighted switch contracts for phi 20/25; dense checkpoints around energy crossing
switch_rows=[]; stat_rows=[]; global_rows=[]
summary={}
for phi in [20,25]:
    pos,R=NP.make_fixedN_triangle(phi,127)
    def de(th): return energy(th,pos,xyA)-energy(th,pos,xyB)
    rootE=brentq(de,2.7,3.05,xtol=5e-14,rtol=1e-14)
    # derivative at crossing
    h=1e-5; slope=(de(rootE+h)-de(rootE-h))/(2*h)
    c0=branch_contract(rootE,pos)
    # prepared just either side
    for off in [-0.02,-0.005,-0.001,0.0,0.001,0.005,0.02]:
        th=rootE+off; c=branch_contract(th,pos)
        ground='A' if c['UA']<c['UB'] else ('B' if c['UB']<c['UA'] else 'degenerate')
        if ground=='A': gp,gm,gd=c['FAplus'],c['FAminus'],c['deltaA']
        elif ground=='B': gp,gm,gd=c['FBplus'],c['FBminus'],c['deltaB']
        else: gp=gm=gd=np.nan
        globalp=max(c['FAplus'],c['FBplus']); globalm=max(c['FAminus'],c['FBminus'])
        switch_rows.append({'phi_deg':phi,'theta_deg':th,'theta_minus_switch':off,'energy_switch_deg':rootE,
                            **c,'ground':ground,'ground_Fplus':gp,'ground_Fminus':gm,'ground_delta':gd,
                            'global_Fplus':globalp,'global_Fminus':globalm,'global_delta':globalp-globalm})
    # stationary enumeration at +/- and exact root
    for off in [-0.002,0.0,0.002]:
        th=rootE+off; mins=enumerate_minima(th,pos,None,21)
        for i,m in enumerate(mins):
            # distances to A/B
            uvA=np.array([0.,0.]); uvB=np.array([1/3,1/3])
            stat_rows.append({'phi_deg':phi,'theta_deg':th,'offset':off,'min_rank':i,'n_minima':len(mins),
                              'U':m['U'],'eig_min':m['eig0'],'grad_resid':m['grad'],
                              'dist_to_A':pdist_uv(m['uv'],uvA),'dist_to_B':pdist_uv(m['uv'],uvB)})
    # exact smooth global-envelope zero crossing using cached fold evaluations
    cache={}
    def gdelta(th):
        key=round(float(th),12)
        if key not in cache:
            c=branch_contract(float(th),pos); cache[key]=max(c['FAplus'],c['FBplus'])-max(c['FAminus'],c['FBminus'])
        return cache[key]
    # locate bracket around known nearby region
    gg=np.linspace(rootE-0.05,rootE+0.02,15); rg=None
    for a,b in zip(gg[:-1],gg[1:]):
        if gdelta(a)==0 or gdelta(a)*gdelta(b)<0:
            rg=a if gdelta(a)==0 else brentq(gdelta,a,b,xtol=2e-10,rtol=1e-10,maxiter=60); break
    if rg is None: rg=np.nan
    global_rows.append({'phi_deg':phi,'prepared_energy_switch_deg':rootE,'global_envelope_zero_deg':rg,'difference_deg':rootE-rg if np.isfinite(rg) else np.nan})
    summary[str(phi)]={'energy_switch_deg':rootE,'energy_crossing_slope_per_deg':slope,
                       'deltaA_at_switch':c0['deltaA'],'deltaB_at_switch':c0['deltaB'],
                       'prepared_jump_delta':c0['deltaB']-c0['deltaA'],
                       'global_zero_deg':rg,'prepared_minus_global_deg':rootE-rg if np.isfinite(rg) else None}

pd.DataFrame(switch_rows).to_csv(OUT/'n3_prepared_vs_global_switch.csv',index=False)
pd.DataFrame(stat_rows).to_csv(OUT/'n3_stationary_minima_near_switch.csv',index=False)
pd.DataFrame(global_rows).to_csv(OUT/'n3_global_vs_prepared_roots.csv',index=False)

# 3) edge-weight sensitivity: roots + branch signs either side + enumeration at switch
weight_rows=[]; weight_stat=[]
for phi in [20,25]:
    pos,R=NP.make_fixedN_triangle(phi,127); edge=boundary_mask(pos)
    for ew in [0.5,0.75,1.0,1.25,1.5]:
        w=np.ones(len(pos)); w[edge]=ew
        def de(th): return energy(th,pos,xyA,w)-energy(th,pos,xyB,w)
        grid=np.linspace(2.4,3.35,191); rE=None
        for a,b in zip(grid[:-1],grid[1:]):
            fa,fb=de(a),de(b)
            if fa==0 or fa*fb<0:
                rE=float(a if fa==0 else brentq(de,a,b,xtol=5e-13,rtol=1e-13)); break
        if rE is None: continue
        # exact branch contract at crossing and at +/-0.001
        c0=branch_contract(rE,pos,w)
        cm=branch_contract(rE-0.001,pos,w); cp=branch_contract(rE+0.001,pos,w)
        gd_minus=cm['deltaA'] if cm['UA']<cm['UB'] else cm['deltaB']
        gd_plus=cp['deltaA'] if cp['UA']<cp['UB'] else cp['deltaB']
        # verify A/B stationary and stable at crossing
        for label,xy in [('A',xyA),('B',xyB)]:
            U,g,H=ugh(rE,pos,xy,0,w); ev=np.linalg.eigvalsh(H)
            weight_stat.append({'phi_deg':phi,'edge_weight':ew,'theta_switch_deg':rE,'family':label,
                                'grad_resid':float(np.linalg.norm(g)),'eig_min':float(ev[0]),'U':float(U)})
        # enumeration count at root, lower resolution but global 21x21
        mins=enumerate_minima(rE,pos,w,21)
        weight_rows.append({'phi_deg':phi,'edge_weight':ew,'edge_sites':int(edge.sum()),'switch_deg':rE,
                            'deltaA_at_switch':c0['deltaA'],'deltaB_at_switch':c0['deltaB'],
                            'prepared_delta_below':gd_minus,'prepared_delta_above':gd_plus,
                            'sign_reversal':bool(gd_minus*gd_plus<0),'n_stable_minima_at_switch':len(mins),
                            'energy_gap_at_root':de(rE),'hard_min':c0['hard_min'],'fold_resid_max':c0['fold_resid_max']})
pd.DataFrame(weight_rows).to_csv(OUT/'n3_edge_weight_sensitivity.csv',index=False)
pd.DataFrame(weight_stat).to_csv(OUT/'n3_edge_weight_stationarity.csv',index=False)

# summary contracts
wr=pd.DataFrame(weight_rows); sr=pd.DataFrame(switch_rows); st=pd.DataFrame(stat_rows); gr=pd.DataFrame(global_rows); ori=pd.DataFrame(orientation_rows)
summary['contracts']={
    'orientation_roots_inside_0_3':ori.loc[ori.root_inside_0_3,'phi_deg'].astype(int).tolist(),
    'stationary_check_nrows':int(len(st)),
    'stationary_all_two_minima':bool((st.groupby(['phi_deg','theta_deg']).n_minima.first()==2).all()),
    'weight_sign_reversal_all':bool(wr.sign_reversal.all()),
    'edge_weight_switch_min_deg':float(wr.switch_deg.min()),
    'edge_weight_switch_max_deg':float(wr.switch_deg.max()),
    'edge_weight_n_stable_minima_all_two':bool((wr.n_stable_minima_at_switch==2).all()),
    'max_weight_stationary_grad':float(pd.DataFrame(weight_stat).grad_resid.max()),
    'min_weight_stationary_eig':float(pd.DataFrame(weight_stat).eig_min.min()),
    'max_fold_resid':float(wr.fold_resid_max.max()),
    'min_fold_hard':float(wr.hard_min.min()),
}
(OUT/'n3_audit_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
