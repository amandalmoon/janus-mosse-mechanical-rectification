from pathlib import Path
import sys, math, json
import numpy as np, pandas as pd
from scipy.optimize import root, least_squares
ROOT=Path('/mnt/data/janus_baseline_gate/release/Janus_MoSSe_AuditResolved_ReproducibilityRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)

def make_disk(R):
    M=int(math.ceil(R+2)); pts=[]
    for q in range(-2*M,2*M+1):
      for r in range(-2*M,2*M+1):
        p=q*J.A1+r*J.A2
        if np.linalg.norm(p)<=R+1e-12: pts.append(p)
    pts=np.array(pts,float); pts-=pts.mean(axis=0); return pts

def wrap_uv(xy):
    uv=AINV@np.asarray(xy,float); return uv-np.floor(uv)
def pdist_xy(xy1,xy2):
    d=AINV@(np.asarray(xy1)-np.asarray(xy2)); d-=np.round(d); return float(np.linalg.norm(A@d))

def ground_min(theta,pos,ngrid=11):
    S=J.contact_factors(theta,land.vectors,pos); sols=[]
    for u in np.linspace(0,1,ngrid,endpoint=False):
      for v in np.linspace(0,1,ngrid,endpoint=False):
        x0=A@np.array([u,v])
        def f(z):return J.contact_ugh(z[0],z[1],S,land,0,0)[1]
        def j(z):return J.contact_ugh(z[0],z[1],S,land,0,0)[2]
        rr=root(f,x0,jac=j,method='hybr',options={'xtol':1e-11,'maxfev':800})
        if np.linalg.norm(f(rr.x))>1e-7: continue
        uv=wrap_uv(rr.x); xy=A@uv
        if any(pdist_xy(xy,q['xy'])<2e-6 for q in sols): continue
        U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,0); ev=np.linalg.eigvalsh(H)
        if ev[0]>1e-7: sols.append(dict(xy=xy,uv=uv,U=float(U),eig=float(ev[0])))
    sols.sort(key=lambda q:q['U'])
    if not sols: raise RuntimeError(('no minima',theta,len(pos)))
    return sols[0],sols

def shipped_fold(theta,sign,zprev,pos):
    S=J.contact_factors(theta,land.vectors,pos)
    def aug(q):
      x,y,F=q;U,g,H=J.contact_ugh(x,y,S,land,0,sign*F);return np.array([g[0],g[1],np.linalg.det(H)])
    cands=[]
    for dx in [0,.001,-.001,.01,-.01]:
      ls=least_squares(aug,np.array(zprev)+[dx,0,0],xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=3000,x_scale='jac')
      q=ls.x; U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]); ev=np.linalg.eigvalsh(H)
      if np.linalg.norm(aug(q))<1e-7 and q[2]>0 and ev[1]>1e-6:
        cands.append((abs(q[2]-zprev[2])+np.linalg.norm(q[:2]-zprev[:2])*.02,q,ev))
    if not cands: raise RuntimeError(('shipped fold fail',theta,sign,len(pos)))
    cands.sort(key=lambda t:t[0]); return cands[0][1]

def track_ground_to_fraction(theta,pos,ground_xy,sign,Fc,fold_xy):
    S=J.contact_factors(theta,land.vectors,pos); x=np.array(ground_xy,float); maxjump=0.; mineig=1e99; maxres=0.
    # Smooth schedule increasingly concentrated near the fold.
    fracs=np.r_[np.linspace(0,0.90,19)[1:],np.linspace(0.91,0.99,9),[0.995,0.998,0.999]]
    Fprev=0.0
    for frac in fracs:
      F=float(frac*Fc)
      # Tangent predictor from H dx/dF = sign * e_y on the equilibrium branch.
      _,_,Hprev=J.contact_ugh(x[0],x[1],S,land,0,sign*Fprev)
      try:
        pred=x+(F-Fprev)*np.linalg.solve(Hprev,np.array([0.0,sign]))
      except np.linalg.LinAlgError:
        pred=x
      def f(z):return J.contact_ugh(z[0],z[1],S,land,0,sign*F)[1]
      def j(z):return J.contact_ugh(z[0],z[1],S,land,0,sign*F)[2]
      rr=root(f,pred,jac=j,method='hybr',options={'xtol':1e-11,'maxfev':1000})
      res=float(np.linalg.norm(f(rr.x))); maxres=max(maxres,res)
      if res>1e-6:return dict(connected=False,reason='root_fail',final_dist=np.nan,maxjump=maxjump,mineig=mineig,maxres=maxres)
      jump=pdist_xy(rr.x,x);maxjump=max(maxjump,jump)
      if jump>0.15:return dict(connected=False,reason='branch_jump',final_dist=np.nan,maxjump=maxjump,mineig=mineig,maxres=maxres)
      ev=np.linalg.eigvalsh(j(rr.x)); mineig=min(mineig,float(ev[0]))
      if ev[0]<=0:return dict(connected=False,reason='unstable_before_fold',final_dist=np.nan,maxjump=maxjump,mineig=mineig,maxres=maxres)
      x=rr.x; Fprev=F
    dist=pdist_xy(x,fold_xy)
    return dict(connected=bool(dist<0.08),reason='ok' if dist<0.08 else 'far_from_fold',final_dist=dist,maxjump=maxjump,mineig=mineig,maxres=maxres)

shapes=[]
for sh in [6,8,10,12,14,16,18,20]:shapes.append(('hex',f'shell{sh}',J.make_hexagonal_flake(sh)))
for R in [6,8,10,12,14,16]:shapes.append(('disk',f'R{R}',make_disk(R)))
rows=[]
for fam,name,pos in shapes:
    N=len(pos)
    zp=np.array([0.0151072601171,0.1812524912333,3.4851202323701]); zm=np.array([0.000055218493,-0.1736331839004,1.4222355051565])
    for Th in [0,10,15,20]:
      th=Th/math.sqrt(N); zp=shipped_fold(th,+1,zp,pos); zm=shipped_fold(th,-1,zm,pos)
      gm,mins=ground_min(th,pos,11 if N>600 else 13)
      for sign,z in [(+1,zp),(-1,zm)]:
        q=track_ground_to_fraction(th,pos,gm['xy'],sign,float(z[2]),z[:2])
        rows.append(dict(family=fam,shape=name,N=N,Theta=Th,theta=th,n_minima=len(mins),ground_u=gm['uv'][0],ground_v=gm['uv'][1],sign=sign,Fc=float(z[2]),fold_x=float(z[0]),fold_y=float(z[1]),**q))
    print(fam,name,N)
df=pd.DataFrame(rows);df.to_csv('/mnt/data/janus_baseline_gate/shape_branch_connectivity.csv',index=False)
summary=dict(rows=len(df),all_connected=bool(df.connected.all()),max_final_dist=float(df.final_dist.max()),max_branch_jump=float(df.maxjump.max()),min_pre_fold_eigenvalue=float(df.mineig.min()),max_equilibrium_residual=float(df.maxres.max()),min_n_minima=int(df.n_minima.min()),max_n_minima=int(df.n_minima.max()))
Path('/mnt/data/janus_baseline_gate/shape_branch_connectivity_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
if not summary['all_connected']:
    print(df[~df.connected].to_string(index=False))
