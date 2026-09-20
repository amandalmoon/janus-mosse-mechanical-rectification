import sys, math, numpy as np, pandas as pd
from scipy.optimize import least_squares, brentq
sys.path.insert(0,'/mnt/data/janus_resolve/Janus_mechanical_rectification_v18_ProfessorCorrected_release/source')
import janus_fourier_landscapes_v12 as J
sys.path.insert(0,'/mnt/data/janus_resolve/Janus_mechanical_rectification_v18_ProfessorCorrected_release/source')
import new_physics_v18 as NP
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S')

def boundary_mask(pos):
    n=len(pos); out=np.zeros(n,dtype=bool)
    for i in range(n):
        d=np.linalg.norm(pos-pos[i],axis=1)
        neigh=np.sum((d>1e-6)&(np.abs(d-1.0)<1e-6))
        if neigh<6: out[i]=True
    return out

def weighted_factors(theta,pos,w):
    R=J.rotation_matrix(theta); delta=pos@R.T-pos; ph=delta@land.vectors.T
    z=np.exp(1j*ph); return np.sum(w[:,None]*z,axis=0)/np.sum(w)

def fold(theta,sign,S,zprev):
    def aug(q):
        x,y,F=q; U,g,H=J.contact_ugh(x,y,S,land,0,sign*F); return np.array([g[0],g[1],np.linalg.det(H)])
    cands=[]
    for dx in [0,.001,-.001,.01,-.01,.05,-.05]:
      ls=least_squares(aug,np.array(zprev)+[dx,0,0],xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=3000,x_scale='jac')
      q=ls.x; U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]); ev=np.linalg.eigvalsh(H)
      if np.linalg.norm(aug(q))<1e-7 and q[2]>0 and ev[1]>1e-6: cands.append((abs(q[2]-zprev[2])+0.02*np.linalg.norm(q[:2]-zprev[:2]),q))
    if not cands: raise RuntimeError((theta,sign))
    cands.sort(key=lambda x:x[0]); return cands[0][1]

rows=[]; roots=[]
for phi in [20,25]:
    pos,R=NP.make_fixedN_triangle(phi,127); edge=boundary_mask(pos); print('phi',phi,'edge sites',edge.sum(),'N',len(pos))
    for ew in [0.5,0.75,1.0,1.25,1.5]:
      weights=np.ones(len(pos));weights[edge]=ew
      zp=np.array([0.01,0.20,2.0]); zm=np.array([0.0,-0.17,1.0])
      loc=[]
      for th in np.arange(2.65,3.1001,.025):
        S=weighted_factors(float(th),pos,weights)
        zp=fold(float(th),+1,S,zp);zm=fold(float(th),-1,S,zm)
        delta=zp[2]-zm[2];loc.append((th,zp[2],zm[2],delta))
        rows.append(dict(phi=phi,edge_weight=ew,edge_sites=int(edge.sum()),theta=th,Fp=zp[2],Fm=zm[2],delta=delta))
      rootv=np.nan
      for a,b in zip(loc[:-1],loc[1:]):
        if a[3]*b[3]<0:
          rootv=a[0]-a[3]*(b[0]-a[0])/(b[3]-a[3]);break
      roots.append(dict(phi=phi,edge_weight=ew,zero_crossing_deg=rootv))
      print(phi,ew,'root',rootv)
pd.DataFrame(rows).to_csv('/mnt/data/janus_resolve/edge_weight_curves.csv',index=False)
pd.DataFrame(roots).to_csv('/mnt/data/janus_resolve/edge_weight_zero_crossings.csv',index=False)
