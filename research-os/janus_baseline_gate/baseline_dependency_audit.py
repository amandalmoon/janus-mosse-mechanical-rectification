from pathlib import Path
import sys, math, json
import numpy as np
import pandas as pd
from scipy.optimize import root, least_squares

ROOT=Path('/mnt/data/janus_baseline_gate/release/Janus_MoSSe_AuditResolved_ReproducibilityRelease')
sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
import new_physics_v18 as NP

land=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)

def uv_to_xy(uv): return A@np.asarray(uv,float)
def wrap_uv(xy):
    uv=AINV@np.asarray(xy,float); return uv-np.floor(uv)
def pdist(uv1,uv2):
    d=np.asarray(uv1)-np.asarray(uv2); d-=np.round(d); return float(np.linalg.norm(A@d))

def enumerate_minima(theta,pos,ngrid=13):
    S=J.contact_factors(theta,land.vectors,pos); sols=[]
    for u in np.linspace(0,1,ngrid,endpoint=False):
      for v in np.linspace(0,1,ngrid,endpoint=False):
        x0=uv_to_xy((u,v))
        def f(z): return J.contact_ugh(z[0],z[1],S,land,0.0,0.0)[1]
        def jac(z): return J.contact_ugh(z[0],z[1],S,land,0.0,0.0)[2]
        rr=root(f,x0,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':700})
        if np.linalg.norm(f(rr.x))>1e-8: continue
        uv=wrap_uv(rr.x)
        if any(pdist(uv,q['uv'])<2e-6 for q in sols): continue
        xy=uv_to_xy(uv); U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,0); ev=np.linalg.eigvalsh(H)
        if ev[0]>1e-7: sols.append(dict(uv=uv,xy=xy,U=float(U),eig0=float(ev[0]),eig1=float(ev[1])))
    sols.sort(key=lambda q:q['U']); return sols

def fold(theta,pos,xy0,sign,step=.01,maxF=5.0):
    S=J.contact_factors(theta,land.vectors,pos); x=np.array(xy0,float); F=0.0; last=(F,x.copy())
    while F<maxF:
      Fn=F+step
      def f(z): return J.contact_ugh(z[0],z[1],S,land,0.0,sign*Fn)[1]
      def jac(z): return J.contact_ugh(z[0],z[1],S,land,0.0,sign*Fn)[2]
      rr=root(f,x,jac=jac,method='hybr',options={'xtol':1e-12,'maxfev':1500})
      if np.linalg.norm(f(rr.x))>1e-7:
        guess=np.array([x[0],x[1],F+step/2]); break
      uvstep=AINV@(rr.x-x); uvstep-=np.round(uvstep)
      if np.linalg.norm(A@uvstep)>.15:
        step/=2
        if step<1e-4:
          guess=np.array([x[0],x[1],F+step]); break
        continue
      ev=np.linalg.eigvalsh(jac(rr.x))
      if ev[0]<=0:
        guess=np.array([(x[0]+rr.x[0])/2,(x[1]+rr.x[1])/2,(F+Fn)/2]); break
      F=Fn; x=rr.x; last=(F,x.copy())
    else: raise RuntimeError('no fold')
    def aug(q):
      U,g,H=J.contact_ugh(q[0],q[1],S,land,0.0,sign*q[2]); return np.array([g[0],g[1],np.linalg.det(H)])
    c=[]
    for dx in [0,.001,-.001,.01,-.01,.03,-.03,.08,-.08]:
      ls=least_squares(aug,guess+[dx,0,0],xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=7000,x_scale='jac')
      q=ls.x; U,g,H=J.contact_ugh(q[0],q[1],S,land,0.0,sign*q[2]); ev=np.linalg.eigvalsh(H)
      res=float(np.linalg.norm(aug(q)))
      if res<1e-7 and q[2]>0 and ev[1]>1e-6: c.append((abs(q[2]-last[0]),q,ev,res))
    if not c: raise RuntimeError(('fold failed',theta,len(pos),sign))
    c.sort(key=lambda t:t[0]); _,q,ev,res=c[0]
    return dict(Fc=float(q[2]),x=float(q[0]),y=float(q[1]),hard=float(ev[1]),res=res)

# 1) Reference vector/thermal initial root vs independently enumerated ground minimum.
pos127=J.make_hexagonal_flake(6); theta=1.5; S=J.contact_factors(theta,land.vectors,pos127)
def f0(z): return J.contact_ugh(z[0],z[1],S,land,0,0)[1]
def j0(z): return J.contact_ugh(z[0],z[1],S,land,0,0)[2]
root0=root(f0,np.zeros(2),jac=j0,method='hybr',options={'xtol':1e-12}).x
mins=enumerate_minima(theta,pos127,17)
uvroot=wrap_uv(root0); dists=[pdist(uvroot,m['uv']) for m in mins]
iref=int(np.argmin(dists))
ref_check=dict(root_energy=float(J.contact_ugh(root0[0],root0[1],S,land,0,0)[0]),ground_energy=mins[0]['U'],matched_min_index=iref,distance_to_ground=float(dists[0]),distance_to_matched=float(dists[iref]),n_minima=len(mins))

# 2) Extended shape scaling: at Theta=0 and 20, enumerate minima and compare current shipped fold to prepared ground fold.
shape_csv=pd.read_csv(ROOT/'data/canonical/shape_scaling_extended.csv')
shape_rows=[]
def make_disk(R):
    M=int(math.ceil(R+2)); pts=[]
    for q in range(-2*M,2*M+1):
      for r in range(-2*M,2*M+1):
        p=q*J.A1+r*J.A2
        if np.linalg.norm(p)<=R+1e-12: pts.append(p)
    pts=np.array(pts,float); pts-=pts.mean(axis=0); return pts
shapes=[]
for sh in [6,8,10,12,14,16,18,20]: shapes.append(('hex',f'shell{sh}',J.make_hexagonal_flake(sh)))
for R in [6,8,10,12,14,16]: shapes.append(('disk',f'R{R}',make_disk(R)))
for fam,name,pos in shapes:
    N=len(pos)
    for Th in [0,10,15,20]:
      th=Th/math.sqrt(N)
      ms=enumerate_minima(th,pos,11 if N>600 else 13)
      g=ms[0]
      fp=fold(th,pos,g['xy'],+1); fm=fold(th,pos,g['xy'],-1)
      ship=shape_csv[(shape_csv.family==fam)&(shape_csv['shape']==name)&(np.isclose(shape_csv.Theta,Th))].iloc[0]
      shape_rows.append(dict(family=fam,shape=name,N=N,Theta=Th,theta=th,n_minima=len(ms),ground_U=g['U'],prepared_Fp=fp['Fc'],prepared_Fm=fm['Fc'],shipped_Fp=float(ship.Fp),shipped_Fm=float(ship.Fm),dFp=fp['Fc']-float(ship.Fp),dFm=fm['Fc']-float(ship.Fm)))
shape_df=pd.DataFrame(shape_rows)

# 3) Triangle A/B stationary-minimum check around canonical switches.
tri_rows=[]
for phi,sw in [(20,2.92127800838),(25,2.84723312226)]:
    pos,R=NP.make_fixedN_triangle(phi,127)
    for off in [-0.01,0,0.01]:
      th=sw+off; S=J.contact_factors(th,land.vectors,pos)
      for label,uv in [('A',np.array([0.,0.])),('B',np.array([1/3,1/3]))]:
        xy=A@uv; U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,0); ev=np.linalg.eigvalsh(H)
        tri_rows.append(dict(phi=phi,theta=th,label=label,R=R,U=float(U),grad_norm=float(np.linalg.norm(g)),eig_min=float(ev[0]),eig_max=float(ev[1]),stable=bool(ev[0]>0 and np.linalg.norm(g)<1e-7)))
tri_df=pd.DataFrame(tri_rows)

# summary
summary={
 'reference_initialization':ref_check,
 'shape_checks':{
   'rows':len(shape_df),
   'max_abs_dFp':float(shape_df.dFp.abs().max()),
   'max_abs_dFm':float(shape_df.dFm.abs().max()),
   'all_shipped_equal_prepared_1e-7':bool((shape_df.dFp.abs()<1e-7).all() and (shape_df.dFm.abs()<1e-7).all()),
   'min_number_of_zero_force_minima':int(shape_df.n_minima.min()),
   'max_number_of_zero_force_minima':int(shape_df.n_minima.max()),
 },
 'triangle_checks':{
   'max_grad_norm':float(tri_df.grad_norm.max()),
   'min_eig_min':float(tri_df.eig_min.min()),
   'all_AB_are_stationary_stable':bool(tri_df.stable.all()),
 }
}

OUT=Path('/mnt/data/janus_baseline_gate')
shape_df.to_csv(OUT/'shape_prepared_baseline_check.csv',index=False)
tri_df.to_csv(OUT/'triangle_stationary_baseline_check.csv',index=False)
with open(OUT/'baseline_dependency_audit_summary.json','w') as f: json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
print(shape_df[['family','shape','N','Theta','n_minima','dFp','dFm']].to_string(index=False))
print(tri_df.to_string(index=False))
