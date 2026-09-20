from pathlib import Path
_RELEASE_ROOT = Path(__file__).resolve().parents[1]
import sys, math, numpy as np, pandas as pd
from scipy.optimize import least_squares
sys.path.insert(0,str(_RELEASE_ROOT/'source'))
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

def fold(theta,sign,zprev,pos):
    S=J.contact_factors(theta,land.vectors,pos)
    def aug(q):
      x,y,F=q; U,g,H=J.contact_ugh(x,y,S,land,0,sign*F); return np.array([g[0],g[1],np.linalg.det(H)])
    cands=[]
    for dx in [0,.001,-.001,.01,-.01]:
      ls=least_squares(aug,np.array(zprev)+[dx,0,0],xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=3000,x_scale='jac')
      q=ls.x; U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]); ev=np.linalg.eigvalsh(H)
      if np.linalg.norm(aug(q))<1e-7 and q[2]>0 and ev[1]>1e-6:
        cands.append((abs(q[2]-zprev[2])+np.linalg.norm(q[:2]-zprev[:2])*.02,q,ev))
    if not cands: raise RuntimeError((theta,sign,len(pos)))
    cands.sort(key=lambda t:t[0]); return cands[0][1]

hex_shells=[6,8,10,12,14,16,18,20]
disk_R=[6,8,10,12,14,16]
shapes=[]
for sh in hex_shells: shapes.append(('hex',f'shell{sh}',J.make_hexagonal_flake(sh)))
for R in disk_R: shapes.append(('disk',f'R{R}',make_disk(R)))
Thetas=[0,10,15,20]
rows=[]
for family,name,pos in shapes:
    N=len(pos); zp=np.array([0.0151072601171,0.1812524912333,3.4851202323701]); zm=np.array([0.000055218493,-0.1736331839004,1.4222355051565])
    F0p=F0m=None
    for Th in Thetas:
      theta=Th/math.sqrt(N)
      zp=fold(theta,+1,zp,pos); zm=fold(theta,-1,zm,pos)
      if Th==0: F0p=zp[2];F0m=zm[2]
      rows.append(dict(family=family,shape=name,N=N,Theta=Th,theta_deg=theta,Fp=zp[2],Fm=zm[2],Fp_norm=zp[2]/F0p,Fm_norm=zm[2]/F0m,rho=(zp[2]-zm[2])/(zp[2]+zm[2])))
    print(family,name,N)
df=pd.DataFrame(rows)
# cross-size spread within family and between family means
metrics=[]
for fam in ['hex','disk']:
  sub=df[df.family==fam]
  for Th in Thetas:
    q=sub[sub.Theta==Th]
    metrics.append(dict(scope=fam,Theta=Th,Fp_mean=q.Fp_norm.mean(),Fp_max_rel=np.max(np.abs(q.Fp_norm-q.Fp_norm.mean())/q.Fp_norm.mean()),Fm_mean=q.Fm_norm.mean(),Fm_max_rel=np.max(np.abs(q.Fm_norm-q.Fm_norm.mean())/q.Fm_norm.mean()),rho_mean=q.rho.mean(),rho_max_rel=np.max(np.abs(q.rho-q.rho.mean())/abs(q.rho.mean()))))
# family mean difference
for Th in Thetas:
  h=df[(df.family=='hex')&(df.Theta==Th)]; d=df[(df.family=='disk')&(df.Theta==Th)]
  metrics.append(dict(scope='hex_vs_disk',Theta=Th,Fp_mean=h.Fp_norm.mean()-d.Fp_norm.mean(),Fp_max_rel=abs(h.Fp_norm.mean()-d.Fp_norm.mean())/h.Fp_norm.mean(),Fm_mean=h.Fm_norm.mean()-d.Fm_norm.mean(),Fm_max_rel=abs(h.Fm_norm.mean()-d.Fm_norm.mean())/h.Fm_norm.mean(),rho_mean=h.rho.mean()-d.rho.mean(),rho_max_rel=abs(h.rho.mean()-d.rho.mean())/abs(h.rho.mean())))
md=pd.DataFrame(metrics)
print(md.to_string(index=False))
df.to_csv(str(_RELEASE_ROOT/'data'/'canonical'/'shape_scaling_extended.csv'),index=False);md.to_csv(str(_RELEASE_ROOT/'data'/'canonical'/'shape_scaling_metrics.csv'),index=False)
