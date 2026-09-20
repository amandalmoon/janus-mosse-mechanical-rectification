from pathlib import Path
import sys, math, numpy as np, pandas as pd
from scipy.integrate import solve_ivp
ROOT=Path('/mnt/data/janus_baseline_gate/Janus_MoSSe_CanonicalUnguided_BaselineRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');pos=J.make_hexagonal_flake(6);theta=1.5;gamma=4.
S=J.contact_factors(theta,land.vectors,pos);vr=np.asarray(land.vectors,float);c=np.asarray(land.c_cos,float);s=np.asarray(land.c_sin,float);sr=S.real.copy();si=S.imag.copy();A=np.column_stack([J.A1,J.A2])
orbits=pd.read_csv('/mnt/data/janus_n5_gate/n5_relative_periodic_orbits.csv')

def gh(x,y):
    Gx=vr[:,0];Gy=vr[:,1];q=Gx*x+Gy*y;cq=np.cos(q);sq=np.sin(q);re=sr*cq-si*sq;im=sr*sq+si*cq
    aa=-c*im+s*re;bb=-c*re-s*im
    g=np.array([np.sum(aa*Gx),np.sum(aa*Gy)])
    H=np.array([[np.sum(bb*Gx*Gx),np.sum(bb*Gx*Gy)],[np.sum(bb*Gx*Gy),np.sum(bb*Gy*Gy)]])
    return g,H

def aug(z0,F0,P,method='DOP853',rtol=1e-11,atol=1e-13,maxstep=.05):
    def rhs(t,Y):
        z=Y[:4];M=Y[4:].reshape(4,4);g,H=gh(z[0],z[1]);
        dz=np.array([z[2],z[3],-g[0]-gamma*z[2],F0*math.sin(2*math.pi*t/P)-g[1]-gamma*z[3]])
        Jm=np.array([[0,0,1,0],[0,0,0,1],[-H[0,0],-H[0,1],-gamma,0],[-H[1,0],-H[1,1],0,-gamma]])
        return np.r_[dz,(Jm@M).ravel()]
    sol=solve_ivp(rhs,[0,P],np.r_[z0,np.eye(4).ravel()],method=method,rtol=rtol,atol=atol,max_step=maxstep)
    return sol.y[:4,-1],sol.y[4:,-1].reshape(4,4),len(sol.t)
rows=[]; cross=[]
for _,r in orbits.iterrows():
    name=r['name'];F0=float(r.F0);P=float(r.period);w=np.array([int(r.m),int(r.n)]);shift=np.r_[A@w,[0.,0.]]
    z=np.array([r.x,r.y,r.vx,r.vy],float)
    hist=[]
    for it in range(4):
        ze,M,steps=aug(z,F0,P);R=ze-z-shift;nr=np.linalg.norm(R);hist.append(nr)
        if nr < 5e-11: break
        dz=np.linalg.solve(M-np.eye(4),-R)
        z=z+dz
    # evaluate 3 solver contracts at refined z
    for method,rtol,atol,maxstep in [('DOP853',1e-9,1e-11,.05),('DOP853',1e-11,1e-13,.025),('Radau',1e-9,1e-11,.05)]:
        ze,M,steps=aug(z,F0,P,method,rtol,atol,maxstep);R=ze-z-shift;ae=np.sort(np.abs(np.linalg.eigvals(M)))[::-1]
        cross.append([name,F0,P,method,rtol,steps,*ae,np.linalg.norm(R)])
    rows.append([name,F0,P,*w,len(hist),*hist,*z])
maxh=max(len(x[5:-4]) for x in rows)
# manual dataframe variable history up to 4
out=[]
for rr in rows:
    name,F0,P,m,n,nit,*rest=rr; z=rest[-4:]; hs=rest[:-4]; hs=hs+[np.nan]*(4-len(hs)); out.append([name,F0,P,m,n,nit,*hs,*z])
pd.DataFrame(out,columns=['name','F0','period','m','n','iterations','res0','res1','res2','res3','x','y','vx','vy']).to_csv('/mnt/data/janus_n5_gate/n5_newton_shooting_orbits.csv',index=False)
pd.DataFrame(cross,columns=['name','F0','period','method','rtol','steps','mu1_abs','mu2_abs','mu3_abs','mu4_abs','closure']).to_csv('/mnt/data/janus_n5_gate/n5_newton_shooting_floquet.csv',index=False)
print(pd.DataFrame(out,columns=['name','F0','period','m','n','iterations','res0','res1','res2','res3','x','y','vx','vy'])[['name','iterations','res0','res1','res2','res3']].to_string(index=False))
print(pd.DataFrame(cross,columns=['name','F0','period','method','rtol','steps','rho','mu2','mu3','mu4','closure'])[['name','method','rtol','rho','closure']].to_string(index=False))
