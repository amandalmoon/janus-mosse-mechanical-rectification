from pathlib import Path
import sys, math, numpy as np, pandas as pd
from scipy.optimize import root
from scipy.integrate import solve_ivp
ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');pos=J.make_hexagonal_flake(6);theta=1.5;gamma=4.
S=J.contact_factors(theta,land.vectors,pos);vr=np.asarray(land.vectors,float);c=np.asarray(land.c_cos,float);s=np.asarray(land.c_sin,float);sr=S.real.copy();si=S.imag.copy();A=np.column_stack([J.A1,J.A2])
# load initial zstars from previous audit
orbits=pd.read_csv('/mnt/data/janus_n5_gate/n5_relative_periodic_orbits.csv')

def gh(x,y):
    gx=gy=hxx=hxy=hyy=0.
    for k in range(len(vr)):
        Gx,Gy=vr[k];q=Gx*x+Gy*y;cq=math.cos(q);sq=math.sin(q);re=sr[k]*cq-si[k]*sq;im=sr[k]*sq+si[k]*cq
        aa=-c[k]*im+s[k]*re;bb=-c[k]*re-s[k]*im
        gx+=aa*Gx;gy+=aa*Gy;hxx+=bb*Gx*Gx;hxy+=bb*Gx*Gy;hyy+=bb*Gy*Gy
    return np.array([gx,gy]),np.array([[hxx,hxy],[hxy,hyy]])

def integrate_state(z0,F0,P,rtol=2e-12,atol=2e-14,method='DOP853'):
    def rhs(t,z):
        g,_=gh(z[0],z[1]);return [z[2],z[3],-g[0]-gamma*z[2],F0*math.sin(2*math.pi*t/P)-g[1]-gamma*z[3]]
    sol=solve_ivp(rhs,[0,P],z0,method=method,rtol=rtol,atol=atol,max_step=0.02)
    return sol.y[:,-1],len(sol.t)

def integrate_aug(z0,F0,P,method,rtol,atol,maxstep):
    def rhs(t,Y):
        z=Y[:4];M=Y[4:].reshape(4,4);g,H=gh(z[0],z[1]);
        dz=np.array([z[2],z[3],-g[0]-gamma*z[2],F0*math.sin(2*math.pi*t/P)-g[1]-gamma*z[3]])
        JJ=np.array([[0,0,1,0],[0,0,0,1],[-H[0,0],-H[0,1],-gamma,0],[-H[1,0],-H[1,1],0,-gamma]])
        return np.concatenate([dz,(JJ@M).ravel()])
    sol=solve_ivp(rhs,[0,P],np.concatenate([z0,np.eye(4).ravel()]),method=method,rtol=rtol,atol=atol,max_step=maxstep)
    ze=sol.y[:4,-1];M=sol.y[4:,-1].reshape(4,4);return ze,M,len(sol.t)
rows=[]; frows=[]
for _,r in orbits.iterrows():
    name=r['name'];F0=float(r.F0);P=float(r.period);w=np.array([int(r.m),int(r.n)]);shift=np.r_[A@w,[0.,0.]]
    zguess=np.array([r.x,r.y,r.vx,r.vy],float)
    calls=[0]
    def fun(z):
        calls[0]+=1; ze,_=integrate_state(z,F0,P);return ze-z-shift
    sol=root(fun,zguess,method='hybr',tol=1e-10,options={'maxfev':100})
    z=sol.x; res=fun(z); ze,_=integrate_state(z,F0,P);cl=np.linalg.norm(ze-z-shift)
    rows.append([name,F0,P,*w,sol.success,sol.nfev,np.linalg.norm(res),cl,*z])
    for method,rtol,atol,maxstep in [('DOP853',1e-10,1e-12,.04),('DOP853',1e-12,1e-14,.02),('Radau',1e-10,1e-12,.04)]:
        ze,M,nstep=integrate_aug(z,F0,P,method,rtol,atol,maxstep);ev=np.linalg.eigvals(M);ae=np.sort(np.abs(ev))[::-1];cl2=np.linalg.norm(ze-z-shift)
        frows.append([name,method,rtol,atol,maxstep,nstep,*ae,cl2])
pd.DataFrame(rows,columns=['name','F0','period','m','n','root_success','nfev','root_residual','closure','x','y','vx','vy']).to_csv('/mnt/data/janus_n5_gate/n5_shooting_orbits.csv',index=False)
pd.DataFrame(frows,columns=['name','method','rtol','atol','max_step','steps','mu1_abs','mu2_abs','mu3_abs','mu4_abs','closure']).to_csv('/mnt/data/janus_n5_gate/n5_shooting_floquet.csv',index=False)
print(pd.DataFrame(rows,columns=['name','F0','period','m','n','root_success','nfev','root_residual','closure','x','y','vx','vy'])[['name','m','n','root_success','nfev','root_residual','closure']].to_string(index=False))
print(pd.DataFrame(frows,columns=['name','method','rtol','atol','max_step','steps','rho','mu2','mu3','mu4','closure'])[['name','method','rtol','rho','closure']].to_string(index=False))
