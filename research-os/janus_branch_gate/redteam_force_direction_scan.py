from pathlib import Path
import sys,math,numpy as np,pandas as pd
from scipy.optimize import root
ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); pos=J.make_hexagonal_flake(6); theta=1.5
S=J.contact_factors(theta,land.vectors,pos); A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)
def ugh(xy): return J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0,0)
def pdelta(a,b):
    d=np.asarray(a)-np.asarray(b); uv=AINV@d; uv-=np.round(uv); return A@uv
# ground from stationary audit coordinate
x0=np.array([1.5,math.sqrt(3)/2])
# refine
rr=root(lambda z:ugh(z)[1],x0,jac=lambda z:ugh(z)[2],tol=1e-12);x0=rr.x

def eq_newton(xy,Fvec,maxit=50):
    xy=xy.copy()
    for _ in range(maxit):
        U,g,H=ugh(xy); gt=g-Fvec; gn=np.linalg.norm(gt)
        if gn<1e-11:return True,xy
        try:step=np.linalg.solve(H,gt)
        except: return False,xy
        alpha=1.0; accepted=False
        for __ in range(20):
            tr=xy-alpha*step; gn2=np.linalg.norm(ugh(tr)[1]-Fvec)
            if gn2<gn: xy=tr;accepted=True;break
            alpha*=.5
        if not accepted:return False,xy
    return np.linalg.norm(ugh(xy)[1]-Fvec)<1e-8,xy

def threshold(d, fmax=5., df=.01):
    xy=x0.copy(); rec=[]; f=0.
    while f<=fmax+1e-12:
        ok,nxy=eq_newton(xy,f*d)
        if not ok:break
        if f>0 and np.linalg.norm(pdelta(nxy,xy))>.18:break
        xy=nxy;U,g,H=ugh(xy);ev=np.linalg.eigvalsh(H);rec.append((f,xy.copy(),ev.copy()))
        if ev[0]<2e-4:break
        f+=df
    near=min(rec[-20:],key=lambda z:abs(z[2][0]))
    n=np.array([-d[1],d[0]])
    def fun(z):
        U,g,H=ugh(z); return np.array([n@g,np.linalg.det(H)])
    cand=[]
    for dx,dy in [(0,0),(.01,0),(-.01,0),(0,.01),(0,-.01),(.02,.02),(-.02,-.02)]:
        z0=near[1]+[dx,dy]; r=root(fun,z0,method='hybr',tol=1e-12);res=np.linalg.norm(fun(r.x))
        if res>1e-7:continue
        U,g,H=ugh(r.x);ev=np.linalg.eigvalsh(H);fc=float(d@g)
        if fc<-1e-7 or ev[1]<=1e-7:continue
        full=np.linalg.norm(g-fc*d);dist=np.linalg.norm(pdelta(r.x,near[1]));score=abs(fc-near[0])+.05*dist
        cand.append((score,full,fc,ev[1],r.x))
    if not cand: raise RuntimeError(('fold fail',d,near[0]))
    cand.sort(key=lambda x:(x[0],x[1]));return cand[0][2],cand[0][1],cand[0][3]
rows=[]
for deg in np.arange(0,60.0001,5):
    a=math.radians(deg); d=np.array([math.cos(a),math.sin(a)])
    fp,rp,hp=threshold(d); fm,rm,hm=threshold(-d)
    rho=(fp-fm)/(fp+fm)
    rows.append(dict(axis_deg=deg,Fplus=fp,Fminus=fm,Delta=fp-fm,rho=rho,res_plus=rp,res_minus=rm,hard_min=min(hp,hm)))
df=pd.DataFrame(rows);df.to_csv('/mnt/data/janus_branch_gate/redteam_force_direction_scan.csv',index=False)
print(df.to_string(index=False))
print('rho min/max',df.rho.min(),df.rho.max(),'abs min',df.rho.abs().min())
