from __future__ import annotations
import os,sys,math,time,json
os.environ['JAX_ENABLE_X64']='True'
import numpy as np,pandas as pd
from scipy.linalg import null_space
from scipy.optimize import root,minimize
from pathlib import Path
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp
SRC=Path('/mnt/data/janus_n8_gate/rigid_release/Janus_MoSSe_AuditResolved_ReproducibilityRelease/source')
sys.path.insert(0,str(SRC))
import janus_fourier_landscapes_v12 as J

class VFFContact:
    def __init__(self,theta_deg,scale=1.0,a_ang=3.25,ks=5.289992,kt=2.334491):
        self.theta=float(theta_deg); self.scale=float(scale); self.a_ang=float(a_ang);self.ks=ks*scale;self.kt=kt*scale
        self.land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); self.E0=float(self.land.energy_unit_meV)
        self.pos=np.asarray(J.make_hexagonal_flake(6),float); self.N=len(self.pos)
        R=J.rotation_matrix(self.theta); self.delta=self.pos@R.T-self.pos
        C=np.zeros((3,2*self.N)); C[0,0::2]=1;C[1,1::2]=1;C[2,0::2]=-self.pos[:,1];C[2,1::2]=self.pos[:,0]
        self.Q=null_space(C); self.nint=self.Q.shape[1]; self.ndof=2+self.nint
        # bonds + adjacent 60deg angles
        bonds=[]
        neigh=[[] for _ in range(self.N)]
        for i in range(self.N):
            for j in range(i+1,self.N):
                if abs(np.linalg.norm(self.pos[j]-self.pos[i])-1.0)<1e-8:
                    bonds.append((i,j));neigh[i].append(j);neigh[j].append(i)
        ang=[]
        for c in range(self.N):
            ns=neigh[c]
            for ia in range(len(ns)):
                for ib in range(ia+1,len(ns)):
                    v1=self.pos[ns[ia]]-self.pos[c];v2=self.pos[ns[ib]]-self.pos[c]
                    co=np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)); th=np.degrees(np.arccos(np.clip(co,-1,1)))
                    if abs(th-60)<1e-7: ang.append((ns[ia],c,ns[ib]))
        assert len(bonds)==342 and len(ang)==648,(len(bonds),len(ang))
        self.bonds=np.asarray(bonds,int); self.angles=np.asarray(ang,int)
        # jax constants
        self.jQ=jnp.asarray(self.Q); self.jpos=jnp.asarray(self.pos);self.jdelta=jnp.asarray(self.delta)
        self.jb=jnp.asarray(self.bonds); self.ja=jnp.asarray(self.angles)
        self.jG=jnp.asarray(np.asarray(self.land.vectors,float));self.jcc=jnp.asarray(np.asarray(self.land.c_cos,float));self.jss=jnp.asarray(np.asarray(self.land.c_sin,float))
        def energy(z,F):
            q=z[:2]; aa=z[2:]; d=(self.jQ@aa).reshape((self.N,2))
            r=q[None,:]+self.jdelta+d
            ph=r@self.jG.T; Uloc=jnp.cos(ph)@self.jcc+jnp.sin(ph)@self.jss
            # physical deformed coordinates for elastic energy
            xp=self.a_ang*(self.jpos+d)
            bi=self.jb[:,0];bj=self.jb[:,1]; dv=xp[bj]-xp[bi]; ll=jnp.sqrt(jnp.sum(dv*dv,axis=1))
            Eb=0.5*self.ks*jnp.sum((ll-self.a_ang)**2) # eV
            ai=self.ja[:,0]; ac=self.ja[:,1]; ak=self.ja[:,2]
            v1=xp[ai]-xp[ac];v2=xp[ak]-xp[ac]
            n1=jnp.sqrt(jnp.sum(v1*v1,axis=1));n2=jnp.sqrt(jnp.sum(v2*v2,axis=1));co=jnp.sum(v1*v2,axis=1)/(n1*n2)
            co=jnp.clip(co,-0.999999999999,0.999999999999); th=jnp.arccos(co)
            Ea=0.5*self.kt*jnp.sum((th-jnp.pi/3)**2) # eV
            Eel=(Eb+Ea)*1000.0/(self.N*self.E0)
            return jnp.mean(Uloc)+Eel-F*q[1]
        self._e=jax.jit(energy); self._vg=jax.jit(jax.value_and_grad(energy)); self._h=jax.jit(jax.hessian(energy,argnums=0))
        # warm compile
        z0=np.zeros(self.ndof); self.eval(z0,0,True)
    def eval(self,z,F=0.0,need_h=False):
        z=np.asarray(z,float)
        E,g=self._vg(jnp.asarray(z),float(F)); H=self._h(jnp.asarray(z),float(F)) if need_h else None
        return float(E),np.asarray(g,float),None if H is None else np.asarray(H,float)
    def metrics(self,z):
        z=np.asarray(z,float);d=(self.Q@z[2:]).reshape(self.N,2);xp=self.a_ang*(self.pos+d)
        ll=np.linalg.norm(xp[self.bonds[:,1]]-xp[self.bonds[:,0]],axis=1); bond=np.max(np.abs(ll/self.a_ang-1))
        v1=xp[self.angles[:,0]]-xp[self.angles[:,1]];v2=xp[self.angles[:,2]]-xp[self.angles[:,1]]
        co=np.sum(v1*v2,axis=1)/(np.linalg.norm(v1,axis=1)*np.linalg.norm(v2,axis=1));th=np.arccos(np.clip(co,-1,1))
        ad=np.max(np.abs(np.degrees(th-np.pi/3))); disp=np.max(np.linalg.norm(d,axis=1))*self.a_ang
        return dict(max_bond_strain=float(bond),max_angle_change_deg=float(ad),max_disp_A=float(disp))

def uv_to_xy(uv): return np.column_stack([J.A1,J.A2])@np.asarray(uv,float)
def wrap_uv(xy):
 A=np.column_stack([J.A1,J.A2]);u=np.linalg.solve(A,np.asarray(xy,float));return u-np.floor(u)
def pdist(u,v):
 A=np.column_stack([J.A1,J.A2]);d=np.asarray(u)-np.asarray(v);d-=np.round(d);return np.linalg.norm(A@d)
def rigid_minima(theta,ngrid=15):
 land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');S=J.contact_factors(theta,land.vectors,J.make_hexagonal_flake(6));roots=[]
 for u in np.linspace(0,1,ngrid,endpoint=False):
  for v in np.linspace(0,1,ngrid,endpoint=False):
   x0=uv_to_xy((u,v));fun=lambda xy:J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0,0)[1];jac=lambda xy:J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0,0)[2]
   rr=root(fun,x0,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':300})
   if np.linalg.norm(fun(rr.x))>1e-7: continue
   uv=wrap_uv(rr.x)
   if any(pdist(uv,r['uv'])<2e-6 for r in roots):continue
   xy=uv_to_xy(uv);U,g,H=J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0,0);ev=np.linalg.eigvalsh(H);roots.append(dict(uv=uv,xy=xy,U=U,ev=ev))
 return sorted([r for r in roots if r['ev'][0]>1e-7],key=lambda r:r['U'])
def zero_ground(m):
 sols=[]
 for i,r in enumerate(rigid_minima(m.theta)):
  z=np.zeros(m.ndof);z[:2]=r['xy']; fun=lambda zz:m.eval(zz,0,False)[0];jac=lambda zz:m.eval(zz,0,False)[1]
  rr=minimize(fun,z,jac=jac,method='L-BFGS-B',options={'ftol':1e-14,'gtol':2e-9,'maxiter':1500,'maxls':40,'maxcor':20})
  E,g,H=m.eval(rr.x,0,True);sols.append((E,i,rr.x.copy(),np.linalg.norm(g),np.linalg.eigvalsh(H),rr.success))
 sols.sort(key=lambda x:x[0]);return sols[0]
def branch(m,zseed,sign,F,refq):
 fun=lambda z:m.eval(z,sign*F,False)[1];jac=lambda z:m.eval(z,sign*F,True)[2]
 rr=root(fun,zseed,jac=jac,method='hybr',options={'xtol':2e-9,'maxfev':300});E,g,H=m.eval(rr.x,sign*F,True);ev=np.linalg.eigvalsh(H);jump=np.linalg.norm(rr.x[:2]-refq)
 ok=np.linalg.norm(g)<3e-6 and ev[0]>1e-7 and jump<0.45 and abs(rr.x[1])<20
 return ok,rr.x,ev,np.linalg.norm(g),jump
def threshold(m,z0,sign,step=.1,tol=1e-4,maxF=5):
 Flo=0;zlo=z0.copy();qlo=zlo[:2].copy();F=step;Fhi=None
 while F<=maxF+1e-12:
  ok,z,ev,gn,j=branch(m,zlo,sign,F,qlo)
  if ok:Flo=F;zlo=z;qlo=z[:2].copy();F+=step
  else:Fhi=F;break
 if Fhi is None:raise RuntimeError('no threshold')
 while Fhi-Flo>tol:
  fm=(Flo+Fhi)/2;ok,z,ev,gn,j=branch(m,zlo,sign,fm,qlo)
  if ok:Flo=fm;zlo=z;qlo=z[:2].copy()
  else:Fhi=fm
 return (Flo+Fhi)/2,zlo,m.metrics(zlo)
def run(theta,scale):
 t=time.time();m=VFFContact(theta,scale);ground=zero_ground(m);z0=ground[2];fp,zp,mp=threshold(m,z0,+1);fm,zm,mm=threshold(m,z0,-1);rho=(fp-fm)/(fp+fm)
 return dict(theta=theta,scale=scale,Fp=fp,Fm=fm,rho=rho,zero_grad=ground[3],zero_eigmin=float(ground[4][0]),plus_bond=mp['max_bond_strain'],minus_bond=mm['max_bond_strain'],plus_angle_deg=mp['max_angle_change_deg'],minus_angle_deg=mm['max_angle_change_deg'],plus_disp_A=mp['max_disp_A'],minus_disp_A=mm['max_disp_A'],seconds=time.time()-t)
if __name__=='__main__':
 rows=[]
 for th,sc in [(1.5,1.0),(1.5,.5),(3.0,1.0)]:
  print('RUN',th,sc,flush=True);r=run(th,sc);rows.append(r);print(r,flush=True)
 df=pd.DataFrame(rows);df.to_csv('/mnt/data/janus_n8_gate/n8_vff_reconstructed.csv',index=False);print(df.to_string(index=False))
