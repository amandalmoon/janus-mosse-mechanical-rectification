from pathlib import Path
_RELEASE_ROOT = Path(__file__).resolve().parents[1]
import sys, numpy as np, pandas as pd
from scipy.optimize import least_squares, root
sys.path.insert(0,str(_RELEASE_ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); pos=J.make_hexagonal_flake(6)
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)

def solve_fold(theta,sign,zprev, landscape=land, positions=pos):
    S=J.contact_factors(theta,landscape.vectors,positions)
    def aug(q):
        x,y,F=q; U,g,H=J.contact_ugh(float(x),float(y),S,landscape,0.0,sign*float(F)); return np.array([g[0],g[1],np.linalg.det(H)])
    seeds=[]
    for dx in [0,.001,-.001,.01,-.01,.05,-.05]:
        for dy in [0,.002,-.002]:
            s=np.array(zprev,float)+[dx,dy,0]; seeds.append(s)
    cands=[]
    for seed in seeds:
        ls=least_squares(aug,seed,xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=4000,x_scale='jac')
        q=ls.x
        U,g,H=J.contact_ugh(float(q[0]),float(q[1]),S,landscape,0.0,sign*float(q[2]))
        ev=np.linalg.eigvalsh(H)
        res=np.linalg.norm(aug(q))
        if res<1e-7 and q[2]>0 and ev[1]>1e-6:
            # periodic spatial closeness to prior fold branch
            duv=AINV@(q[:2]-np.array(zprev[:2])); duv-=np.round(duv)
            dist=np.linalg.norm(A@duv)
            cands.append((dist + .05*abs(q[2]-zprev[2]),res,q,ev))
    if not cands: raise RuntimeError((theta,sign,zprev))
    cands.sort(key=lambda x:(x[0],x[1])); _,res,q,ev=cands[0]
    return q,ev,res

def zero_min_info(theta,uv,landscape=land,positions=pos):
    S=J.contact_factors(theta,landscape.vectors,positions); x0=A@np.asarray(uv,float)
    def f(x): return J.contact_ugh(x[0],x[1],S,landscape,0.0,0.0)[1]
    def j(x): return J.contact_ugh(x[0],x[1],S,landscape,0.0,0.0)[2]
    rr=root(f,x0,jac=j,method='hybr',options={'xtol':1e-12,'maxfev':1000})
    U,g,H=J.contact_ugh(rr.x[0],rr.x[1],S,landscape,0.0,0.0)
    uvv=AINV@rr.x; uvv-=np.floor(uvv)
    return rr.x,uvv,U,np.linalg.eigvalsh(H)

# two zero-force minima families: ground around (0,0), metastable around (1/3,1/3)
init={
('ground',+1): np.array([0.0151072601171,0.1812524912333,3.4851202323701]),
('ground',-1): np.array([0.000055218493,-0.1736331839004,1.4222355051565]),
('meta',+1): np.array([0.5000221562361,0.3544964448830,0.1956730084059]),
('meta',-1): np.array([0.5071798515504,0.2254465493927,0.5678970777535]),
}
rows=[]
for th in np.arange(0,3.00001,.25):
    for branch,uv0 in [('ground',(0,0)),('meta',(1/3,1/3))]:
        x0,uv,U0,ev0=zero_min_info(float(th),uv0)
        for sign in [+1,-1]:
            z,ev,res=solve_fold(float(th),sign,init[(branch,sign)])
            init[(branch,sign)]=z
            rows.append(dict(theta=th,branch=branch,sign=sign,Fc=z[2],fold_x=z[0],fold_y=z[1],fold_hard=ev[1],fold_residual=res,zero_u=uv[0],zero_v=uv[1],zero_U=U0,zero_eigmin=ev0[0]))

df=pd.DataFrame(rows)
# show whether ground is global lowest and higher depinning threshold in each direction
pivot=df.pivot_table(index=['theta','sign'],columns='branch',values=['Fc','zero_U']).reset_index()
pivot.columns=['theta','sign','Fc_ground','Fc_meta','U_ground','U_meta']
pivot['ground_lower_energy']=pivot.U_ground < pivot.U_meta
pivot['ground_lasts_longer']=pivot.Fc_ground > pivot.Fc_meta
print(pivot.to_string(index=False))
print('all ground lower',pivot.ground_lower_energy.all(),'all ground threshold higher',pivot.ground_lasts_longer.all())
df.to_csv(str(_RELEASE_ROOT/'data'/'canonical'/'branch_family_continuation.csv'),index=False)
pivot.to_csv(str(_RELEASE_ROOT/'data'/'canonical'/'branch_family_summary.csv'),index=False)
