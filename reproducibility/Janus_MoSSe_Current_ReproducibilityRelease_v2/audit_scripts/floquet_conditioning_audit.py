from pathlib import Path
_RELEASE_ROOT = Path(__file__).resolve().parents[1]
import sys, math
import numpy as np
import pandas as pd
from scipy.optimize import root
from scipy.integrate import solve_ivp
from numba import njit
sys.path.insert(0,str(_RELEASE_ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); pos=J.make_hexagonal_flake(6)
theta=1.5; F0=2.; period=40.; gamma=4.
S=J.contact_factors(theta,land.vectors,pos)
vr=np.asarray(land.vectors,float); c=np.asarray(land.c_cos,float); s=np.asarray(land.c_sin,float); sr=S.real.copy(); si=S.imag.copy()
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)

@njit
def gh_num(x,y,vr,c,s,sr,si):
    gx=0.;gy=0.;hxx=0.;hxy=0.;hyy=0.
    for k in range(vr.shape[0]):
        Gx=vr[k,0]; Gy=vr[k,1]; q=Gx*x+Gy*y; cq=math.cos(q); sq=math.sin(q)
        re=sr[k]*cq-si[k]*sq; im=sr[k]*sq+si[k]*cq
        aa=-c[k]*im+s[k]*re; bb=-c[k]*re-s[k]*im
        gx+=aa*Gx; gy+=aa*Gy; hxx+=bb*Gx*Gx; hxy+=bb*Gx*Gy; hyy+=bb*Gy*Gy
    return gx,gy,hxx,hxy,hyy

def gh(x,y):
    gx,gy,hxx,hxy,hyy=gh_num(float(x),float(y),vr,c,s,sr,si)
    return np.array([gx,gy]), np.array([[hxx,hxy],[hxy,hyy]])
def f0(z): return gh(z[0],z[1])[0]
def j0(z): return gh(z[0],z[1])[1]
x0=root(f0,np.zeros(2),jac=j0,tol=1e-12).x

@njit
def deriv(t,z,F0,period,gamma,vr,c,s,sr,si):
    gx,gy,_,_,_=gh_num(z[0],z[1],vr,c,s,sr,si)
    return np.array([z[2],z[3],-gx-gamma*z[2],F0*math.sin(2*math.pi*t/period)-gy-gamma*z[3]])
@njit
def relax_num(z0,F0,period,gamma,spc,ncy,vr,c,s,sr,si):
    z=z0.copy(); dt=period/spc
    for i in range(spc*ncy):
        t=i*dt
        k1=deriv(t,z,F0,period,gamma,vr,c,s,sr,si)
        k2=deriv(t+dt/2,z+dt*k1/2,F0,period,gamma,vr,c,s,sr,si)
        k3=deriv(t+dt/2,z+dt*k2/2,F0,period,gamma,vr,c,s,sr,si)
        k4=deriv(t+dt,z+dt*k3,F0,period,gamma,vr,c,s,sr,si)
        z += dt*(k1+2*k2+2*k3+k4)/6
    return z
zstar=relax_num(np.array([x0[0],x0[1],0.,0.]),F0,period,gamma,4000,200,vr,c,s,sr,si)
z1=relax_num(zstar,F0,period,gamma,8000,1,vr,c,s,sr,si)
dR=z1[:2]-zstar[:2]; uv=AINV@dR; w=np.rint(uv).astype(int); res=np.linalg.norm(np.r_[dR-A@w,z1[2:]-zstar[2:]])
print('zstar',zstar,'w',w,'closure state norm',res)

def augmented_rhs(t,Y):
    z=Y[:4]; M=Y[4:].reshape(4,4)
    g,H=gh(z[0],z[1]); ext=F0*math.sin(2*math.pi*t/period)
    dz=np.array([z[2],z[3],-g[0]-gamma*z[2],ext-g[1]-gamma*z[3]])
    JJ=np.array([[0,0,1,0],[0,0,0,1],[-H[0,0],-H[0,1],-gamma,0],[-H[1,0],-H[1,1],0,-gamma]])
    return np.concatenate([dz,(JJ@M).ravel()])
rows=[]
for method,rtol,atol,maxstep in [('DOP853',1e-9,1e-11,.05),('DOP853',1e-11,1e-13,.025),('Radau',1e-9,1e-11,.05)]:
    Y0=np.concatenate([zstar,np.eye(4).ravel()])
    sol=solve_ivp(augmented_rhs,[0,period],Y0,method=method,rtol=rtol,atol=atol,max_step=maxstep)
    M=sol.y[4:,-1].reshape(4,4); eig=np.linalg.eigvals(M); abs_e=np.sort(np.abs(eig))[::-1]
    zend=sol.y[:4,-1]; closure=np.linalg.norm(np.r_[zend[:2]-zstar[:2]-A@w,zend[2:]-zstar[2:]])
    rows.append([method,rtol,atol,maxstep,len(sol.t),abs_e[0],abs_e[1],abs_e[2],abs_e[3],closure,abs(np.linalg.det(M))])
df=pd.DataFrame(rows,columns=['method','rtol','atol','max_step','steps','rho','eig2','eig3','eig4','closure','abs_det'])
print(df.to_string(index=False))
df.to_csv(str(_RELEASE_ROOT/'data'/'canonical'/'floquet_conditioning_check.csv'),index=False)
