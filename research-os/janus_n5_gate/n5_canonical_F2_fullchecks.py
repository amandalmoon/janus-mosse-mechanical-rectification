from pathlib import Path
import sys, math, numpy as np, pandas as pd
from scipy.optimize import root
from scipy.integrate import solve_ivp
from numba import njit
ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); pos=J.make_hexagonal_flake(6); theta=1.5; gamma=4.
S=J.contact_factors(theta,land.vectors,pos); vr=np.asarray(land.vectors,float); c=np.asarray(land.c_cos,float); s=np.asarray(land.c_sin,float); sr=S.real.copy();si=S.imag.copy()
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)
def f0(z): return J.contact_ugh(z[0],z[1],S,land,0,0)[1]
def j0(z): return J.contact_ugh(z[0],z[1],S,land,0,0)[2]
x0=root(f0,np.zeros(2),jac=j0,tol=1e-13).x
@njit
def gh_num(x,y,vr,c,s,sr,si):
    gx=gy=hxx=hxy=hyy=0.
    for k in range(vr.shape[0]):
        Gx=vr[k,0];Gy=vr[k,1];q=Gx*x+Gy*y;cq=math.cos(q);sq=math.sin(q)
        re=sr[k]*cq-si[k]*sq;im=sr[k]*sq+si[k]*cq
        aa=-c[k]*im+s[k]*re;bb=-c[k]*re-s[k]*im
        gx+=aa*Gx;gy+=aa*Gy;hxx+=bb*Gx*Gx;hxy+=bb*Gx*Gy;hyy+=bb*Gy*Gy
    return gx,gy,hxx,hxy,hyy
@njit
def deriv_num(t,z,F0,P,gamma,vr,c,s,sr,si):
    gx,gy,_,_,_=gh_num(z[0],z[1],vr,c,s,sr,si)
    return np.array([z[2],z[3],-gx-gamma*z[2],F0*math.sin(2*math.pi*t/P)-gy-gamma*z[3]])
@njit
def rk4_cycles(z0,F0,P,gamma,spc,ncy,vr,c,s,sr,si):
    z=z0.copy();dt=P/spc;step=0
    for cyc in range(ncy):
        for j in range(spc):
            t=step*dt
            k1=deriv_num(t,z,F0,P,gamma,vr,c,s,sr,si)
            k2=deriv_num(t+dt/2,z+dt*k1/2,F0,P,gamma,vr,c,s,sr,si)
            k3=deriv_num(t+dt/2,z+dt*k2/2,F0,P,gamma,vr,c,s,sr,si)
            k4=deriv_num(t+dt,z+dt*k3,F0,P,gamma,vr,c,s,sr,si)
            z += dt*(k1+2*k2+2*k3+k4)/6;step+=1
    return z
@njit
def measured_winding(z0,F0,P,gamma,spc,neq,nmeas,vr,c,s,sr,si):
    z=z0.copy();dt=P/spc;step=0
    for cyc in range(neq):
        for j in range(spc):
            t=step*dt;k1=deriv_num(t,z,F0,P,gamma,vr,c,s,sr,si);k2=deriv_num(t+dt/2,z+dt*k1/2,F0,P,gamma,vr,c,s,sr,si);k3=deriv_num(t+dt/2,z+dt*k2/2,F0,P,gamma,vr,c,s,sr,si);k4=deriv_num(t+dt,z+dt*k3,F0,P,gamma,vr,c,s,sr,si);z+=dt*(k1+2*k2+2*k3+k4)/6;step+=1
    zm=z.copy()
    for cyc in range(nmeas):
        for j in range(spc):
            t=step*dt;k1=deriv_num(t,z,F0,P,gamma,vr,c,s,sr,si);k2=deriv_num(t+dt/2,z+dt*k1/2,F0,P,gamma,vr,c,s,sr,si);k3=deriv_num(t+dt/2,z+dt*k2/2,F0,P,gamma,vr,c,s,sr,si);k4=deriv_num(t+dt,z+dt*k3,F0,P,gamma,vr,c,s,sr,si);z+=dt*(k1+2*k2+2*k3+k4)/6;step+=1
    d=(z[:2]-zm[:2])/nmeas
    u,v= d[0]-d[1]/math.sqrt(3.0), 2*d[1]/math.sqrt(3.0) # AINV for a1=(1,0), a2=(.5,sqrt3/2)
    mi=round(u);ni=round(v); resx=(u-mi)+.5*(v-ni);resy=(math.sqrt(3)/2)*(v-ni)
    return z,u,v,mi,ni,math.sqrt(resx*resx+resy*resy)

def gh(x,y):
    gx,gy,hxx,hxy,hyy=gh_num(float(x),float(y),vr,c,s,sr,si)
    return np.array([gx,gy]),np.array([[hxx,hxy],[hxy,hyy]])

def floquet_for(zstar,F0,P,w,method,rtol,atol,maxstep):
    def rhs(t,Y):
        z=Y[:4];M=Y[4:].reshape(4,4);g,H=gh(z[0],z[1]);ext=F0*math.sin(2*math.pi*t/P)
        dz=np.array([z[2],z[3],-g[0]-gamma*z[2],ext-g[1]-gamma*z[3]])
        JJ=np.array([[0,0,1,0],[0,0,0,1],[-H[0,0],-H[0,1],-gamma,0],[-H[1,0],-H[1,1],0,-gamma]])
        return np.concatenate([dz,(JJ@M).ravel()])
    Y0=np.concatenate([zstar,np.eye(4).ravel()])
    sol=solve_ivp(rhs,[0,P],Y0,method=method,rtol=rtol,atol=atol,max_step=maxstep)
    M=sol.y[4:,-1].reshape(4,4);eig=np.linalg.eigvals(M); ae=np.sort(np.abs(eig))[::-1]
    ze=sol.y[:4,-1];cl=np.linalg.norm(np.r_[ze[:2]-zstar[:2]-A@w,ze[2:]-zstar[2:]])
    return ae,cl,len(sol.t),M

reps=[('canonical_w11',2.0,40.,(1,-1))]
time_rows=[]; orbit_rows=[]; floq_rows=[]; basin_rows=[]
for name,F0,P,wexp in reps:
    zinit=np.array([x0[0],x0[1],0.,0.])
    # time-step independent finite-run check
    for spc in [1000,2000,4000,8000]:
        zend,u,v,m,n,res=measured_winding(zinit,F0,P,gamma,spc,20,40,vr,c,s,sr,si)
        time_rows.append([name,F0,P,spc,u,v,int(m),int(n),res,int((int(m),int(n))==wexp)])
    # strong relaxation, fixed one-cycle closure
    zstar=rk4_cycles(zinit,F0,P,gamma,4000,200,vr,c,s,sr,si)
    z1=rk4_cycles(zstar,F0,P,gamma,8000,1,vr,c,s,sr,si)
    dR=z1[:2]-zstar[:2];uv=AINV@dR;w=np.rint(uv).astype(int)
    closure_fixed=np.linalg.norm(np.r_[dR-A@w,z1[2:]-zstar[2:]])
    orbit_rows.append([name,F0,P,zstar[0],zstar[1],zstar[2],zstar[3],uv[0],uv[1],w[0],w[1],closure_fixed,int(tuple(w)==wexp)])
    for method,rtol,atol,maxstep in [('DOP853',1e-9,1e-11,0.05),('DOP853',1e-11,1e-13,0.025),('Radau',1e-9,1e-11,0.05)]:
        ae,cl,steps,M=floquet_for(zstar,F0,P,w,method,rtol,atol,maxstep)
        floq_rows.append([name,F0,P,method,rtol,atol,maxstep,steps,*ae,cl])
    # 27 local basin probes: lattice position du,dv +-0.05 and vy +-0.1
    for du in [-0.05,0.,0.05]:
      for dv in [-0.05,0.,0.05]:
       for dvy in [-0.1,0.,0.1]:
        dzpos=A@np.array([du,dv]); zp=zstar.copy();zp[0]+=dzpos[0];zp[1]+=dzpos[1];zp[3]+=dvy
        zend,u,v,m,n,res=measured_winding(zp,F0,P,gamma,2000,10,20,vr,c,s,sr,si)
        basin_rows.append([name,F0,P,du,dv,dvy,u,v,int(m),int(n),res,int((int(m),int(n))==wexp)])

pd.DataFrame(time_rows,columns=['name','F0','period','steps_per_cycle','u','v','m','n','lock_residual','expected_winding']).to_csv('/mnt/data/janus_n5_gate/n5_timestep_canonical_F2.csv',index=False)
pd.DataFrame(orbit_rows,columns=['name','F0','period','x','y','vx','vy','u_onecycle','v_onecycle','m','n','fixed_RK4_closure','expected_winding']).to_csv('/mnt/data/janus_n5_gate/n5_relative_periodic_canonical_F2.csv',index=False)
pd.DataFrame(floq_rows,columns=['name','F0','period','method','rtol','atol','max_step','solver_steps','mu1_abs','mu2_abs','mu3_abs','mu4_abs','closure']).to_csv('/mnt/data/janus_n5_gate/n5_floquet_canonical_F2.csv',index=False)
pd.DataFrame(basin_rows,columns=['name','F0','period','du','dv','dvy','u','v','m','n','lock_residual','expected_winding']).to_csv('/mnt/data/janus_n5_gate/n5_basin_canonical_F2.csv',index=False)
print('TIMESTEP')
print(pd.DataFrame(time_rows,columns=['name','F0','period','spc','u','v','m','n','res','ok']).to_string(index=False))
print('ORBITS')
print(pd.DataFrame(orbit_rows,columns=['name','F0','period','x','y','vx','vy','u','v','m','n','closure','ok'])[['name','F0','period','u','v','m','n','closure','ok']].to_string(index=False))
fd=pd.DataFrame(floq_rows,columns=['name','F0','period','method','rtol','atol','max_step','steps','rho','mu2','mu3','mu4','closure'])
print('FLOQUET');print(fd[['name','method','rtol','rho','mu2','mu3','mu4','closure']].to_string(index=False))
bd=pd.DataFrame(basin_rows,columns=['name','F0','period','du','dv','dvy','u','v','m','n','res','ok'])
print('BASIN summary');print(bd.groupby('name').agg(pass_count=('ok','sum'),total=('ok','size'),max_res=('res','max')).to_string())
