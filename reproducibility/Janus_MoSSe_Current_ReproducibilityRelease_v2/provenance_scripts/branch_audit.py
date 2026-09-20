import sys, math, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import root

SRC=Path('/mnt/data/janus_resolve/Janus_mechanical_rectification_v18_ProfessorCorrected_release/source')
sys.path.insert(0,str(SRC))
import janus_fourier_landscapes_v12 as J

A=np.column_stack([J.A1,J.A2])
AINV=np.linalg.inv(A)

land=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
pos=J.make_hexagonal_flake(6)


def factors(theta, landscape=land, positions=pos):
    return J.contact_factors(theta, landscape.vectors, positions)

def ugh_xy(xy, theta, force, landscape=land, positions=pos):
    S=J.contact_factors(theta, landscape.vectors, positions)
    return J.contact_ugh(float(xy[0]),float(xy[1]),S,landscape,0.0,float(force))

def wrap_uv_from_xy(xy):
    uv=AINV@np.asarray(xy,float)
    return uv-np.floor(uv)

def uv_to_xy(uv): return A@np.asarray(uv,float)

def periodic_dist(uv1,uv2):
    d=np.asarray(uv1)-np.asarray(uv2)
    d-=np.round(d)
    return np.linalg.norm(A@d)

def enumerate_stationary(theta, force=0.0, landscape=land, positions=pos, ngrid=17, tol=1e-8):
    S=J.contact_factors(theta, landscape.vectors, positions)
    roots=[]
    for u in np.linspace(0,1,ngrid,endpoint=False):
        for v in np.linspace(0,1,ngrid,endpoint=False):
            x0=uv_to_xy((u,v))
            def fun(xy):
                return J.contact_ugh(float(xy[0]),float(xy[1]),S,landscape,0.0,float(force))[1]
            def jac(xy):
                return J.contact_ugh(float(xy[0]),float(xy[1]),S,landscape,0.0,float(force))[2]
            rr=root(fun,x0,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':500})
            if not rr.success and np.linalg.norm(fun(rr.x))>1e-7: continue
            if np.linalg.norm(fun(rr.x))>1e-7: continue
            uv=wrap_uv_from_xy(rr.x)
            if any(periodic_dist(uv,r['uv'])<2e-6 for r in roots): continue
            xy=uv_to_xy(uv)
            U,g,H=J.contact_ugh(float(xy[0]),float(xy[1]),S,landscape,0.0,float(force))
            ev=np.linalg.eigvalsh(H)
            roots.append({'uv':uv,'xy':xy,'U':U,'ev':ev})
    roots.sort(key=lambda r:r['U'])
    return roots

def continue_branch(theta, uv0, sign=+1, landscape=land, positions=pos, step=0.02, maxF=5.0):
    S=J.contact_factors(theta, landscape.vectors, positions)
    x=uv_to_xy(uv0).astype(float)
    rows=[]
    F=0.0
    last_stable=None
    while F <= maxF+1e-12:
        def fun(xy): return J.contact_ugh(float(xy[0]),float(xy[1]),S,landscape,0.0,sign*F)[1]
        def jac(xy): return J.contact_ugh(float(xy[0]),float(xy[1]),S,landscape,0.0,sign*F)[2]
        rr=root(fun,x,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':500})
        if np.linalg.norm(fun(rr.x))>1e-7:
            break
        x=rr.x
        U,g,H=J.contact_ugh(float(x[0]),float(x[1]),S,landscape,0.0,sign*F)
        ev=np.linalg.eigvalsh(H)
        rows.append((F,x.copy(),ev.copy()))
        if ev[0]>1e-6:
            last_stable=(F,x.copy(),ev.copy())
        if ev[0] < 1e-5 and F>0.02:
            break
        F += step
    if last_stable is None:
        return None,rows
    Fg,xg,evg=last_stable
    # augmented fold solve: gx=0, gy-sign*F=0 is already embedded in g, detH=0
    z0=np.array([xg[0],xg[1],max(Fg,0.001)],float)
    def aug(z):
        x,y,Fm=z
        U,g,H=J.contact_ugh(float(x),float(y),S,landscape,0.0,sign*float(Fm))
        return np.array([g[0],g[1],np.linalg.det(H)])
    sols=[]
    for delta in [0,step,-step,2*step,-2*step,0.05,-0.05]:
        zz=z0.copy(); zz[2]=max(1e-6,z0[2]+delta)
        rr=root(aug,zz,method='hybr',options={'xtol':1e-12,'maxfev':2000})
        if np.linalg.norm(aug(rr.x))<1e-6 and rr.x[2]>0:
            U,g,H=J.contact_ugh(float(rr.x[0]),float(rr.x[1]),S,landscape,0.0,sign*float(rr.x[2]))
            ev=np.linalg.eigvalsh(H)
            if ev[1]>1e-5:
                sols.append((abs(rr.x[2]-Fg),rr.x.copy(),ev.copy()))
    if not sols:
        return None,rows
    sols.sort(key=lambda q:q[0])
    _,z,ev=sols[0]
    return {'Fc':float(z[2]),'x':float(z[0]),'y':float(z[1]),'eig_soft':float(ev[0]),'eig_hard':float(ev[1])},rows

allrows=[]
for theta in [0.0,1.5,3.0]:
    roots=enumerate_stationary(theta,0.0,ngrid=21)
    mins=[r for r in roots if r['ev'][0]>1e-7]
    print('theta',theta,'stationary',len(roots),'minima',len(mins))
    for i,m in enumerate(mins):
        print(' min',i,'uv',m['uv'],'U',m['U'],'ev',m['ev'])
        for sign in [+1,-1]:
            fd,trace=continue_branch(theta,m['uv'],sign=sign,step=0.01,maxF=5.0)
            print('  sign',sign,'fold',fd)
            allrows.append({'theta':theta,'min_id':i,'u0':m['uv'][0],'v0':m['uv'][1],'U0':m['U'],'sign':sign,**(fd or {'Fc':np.nan,'x':np.nan,'y':np.nan,'eig_soft':np.nan,'eig_hard':np.nan})})

out='/mnt/data/janus_resolve/branch_followed_thresholds.csv'
pd.DataFrame(allrows).to_csv(out,index=False)
print('wrote',out)
