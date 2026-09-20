import sys, math
from pathlib import Path
import numpy as np, pandas as pd
from scipy.optimize import root, least_squares
from numba import njit
sys.path.insert(0,'/mnt/data/janus_resolve/Janus_mechanical_rectification_v18_ProfessorCorrected_release/source')
import janus_fourier_landscapes_v12 as J

A=np.column_stack([J.A1,J.A2]); AINV=np.linalg.inv(A)
base=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); positions=J.make_hexagonal_flake(6)
# translation-minimizing inversion center from independent gauge audit
uv_center=np.array([0.6666666660695574,0.16666666850152867]); a=A@uv_center

def translate_landscape(land,a,name):
    delta=land.vectors@a
    c=land.c_cos*np.cos(delta)+land.c_sin*np.sin(delta)
    s=-land.c_cos*np.sin(delta)+land.c_sin*np.cos(delta)
    return J.FourierLandscape(name,np.array(land.vectors),np.array(c),np.array(s),land.energy_unit_meV,land.source_note)

centered=translate_landscape(base,a,'2H_centered')
sym=J.FourierLandscape('2H_matched_symmetrized',np.array(centered.vectors),np.array(centered.c_cos),np.zeros_like(centered.c_sin),centered.energy_unit_meV,'2H symmetrized at translation-minimized inversion center')
inv=J.FourierLandscape('2H_exact_inverted',np.array(centered.vectors),np.array(centered.c_cos),-np.array(centered.c_sin),centered.energy_unit_meV,'Exact spatial inversion of centered 2H landscape')


def pdist(uv1,uv2):
    d=np.asarray(uv1)-np.asarray(uv2); d-=np.round(d); return np.linalg.norm(A@d)

def enumerate_minima(theta,land,ngrid=19):
    S=J.contact_factors(theta,land.vectors,positions); sols=[]
    for u in np.linspace(0,1,ngrid,endpoint=False):
      for v in np.linspace(0,1,ngrid,endpoint=False):
        x0=A@np.array([u,v])
        def f(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[1]
        def jac(x): return J.contact_ugh(x[0],x[1],S,land,0,0)[2]
        rr=root(f,x0,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':1000})
        if np.linalg.norm(f(rr.x))>1e-7: continue
        uv=AINV@rr.x; uv-=np.floor(uv); xy=A@uv
        if any(pdist(uv,q['uv'])<1e-5 for q in sols): continue
        U,g,H=J.contact_ugh(xy[0],xy[1],S,land,0,0); ev=np.linalg.eigvalsh(H)
        if ev[0]>1e-7: sols.append(dict(uv=uv,xy=xy,U=U,ev=ev))
    sols.sort(key=lambda q:q['U']); return sols

def branch_fold(theta,land,x0,sign,maxF=6,step=.05):
    S=J.contact_factors(theta,land.vectors,positions)
    x=np.array(x0,float); F=0
    def eq(F,xguess):
      def f(z): return J.contact_ugh(z[0],z[1],S,land,0,sign*F)[1]
      def jac(z): return J.contact_ugh(z[0],z[1],S,land,0,sign*F)[2]
      rr=root(f,xguess,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':1000})
      if np.linalg.norm(f(rr.x))>1e-6: return None,None
      return rr.x,np.linalg.eigvalsh(jac(rr.x))
    x,ev=eq(0,x)
    last=(0,x,ev)
    while F<maxF:
      Fn=F+step; xn,en=eq(Fn,x)
      if xn is None:
        # fold between F and Fn; augmented least squares from last stable
        guess=np.array([x[0],x[1],F+step/2])
        break
      duv=AINV@(xn-x); duv-=np.round(duv)
      if np.linalg.norm(A@duv)>.2:
        step/=2
        if step<1e-4: guess=np.array([x[0],x[1],F]); break
        continue
      if en[0]<=0:
        guess=np.array([(x[0]+xn[0])/2,(x[1]+xn[1])/2,(F+Fn)/2]); break
      F,x,ev=Fn,xn,en; last=(F,x,ev)
    else: raise RuntimeError('no fold')
    def aug(q):
      xx,yy,FF=q; U,g,H=J.contact_ugh(xx,yy,S,land,0,sign*FF); return np.array([g[0],g[1],np.linalg.det(H)])
    cands=[]
    for dx in [0,.001,-.001,.01,-.01,.05,-.05]:
      ls=least_squares(aug,guess+[dx,0,0],xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=5000,x_scale='jac')
      q=ls.x; U,g,H=J.contact_ugh(q[0],q[1],S,land,0,sign*q[2]); eig=np.linalg.eigvalsh(H)
      if np.linalg.norm(aug(q))<1e-7 and q[2]>0 and eig[1]>1e-6:
        cands.append((abs(q[2]-last[0]),q,eig))
    if not cands: raise RuntimeError(('fold solve failed',land.name,sign,guess))
    cands.sort(key=lambda t:t[0]); _,q,eig=cands[0]
    return float(q[2]),q[:2],eig

@njit
def rk4_run(vr,c,s,sr,si,F0,period,n_eq,n_meas,spc,x0,y0):
    gamma=4.; mass=1.; dt=period/spc; omega=2*math.pi/period
    x=x0;y=y0;vx=0.;vy=0.; xmark=x0;ymark=y0
    def grad(x,y):
      gx=0.;gy=0.
      for t in range(vr.shape[0]):
        Gx=vr[t,0];Gy=vr[t,1]; q=Gx*x+Gy*y; cq=math.cos(q);sq=math.sin(q)
        re=sr[t]*cq-si[t]*sq; im=sr[t]*sq+si[t]*cq
        aa=-c[t]*im+s[t]*re; gx+=aa*Gx; gy+=aa*Gy
      return gx,gy
    def deriv(t,x,y,vx,vy):
      gx,gy=grad(x,y); return vx,vy,(-gx-gamma*vx)/mass,(F0*math.sin(omega*t)-gy-gamma*vy)/mass
    total=(n_eq+n_meas)*spc
    for i in range(total):
      t=i*dt
      a,b,c1,d=deriv(t,x,y,vx,vy)
      a2,b2,c2,d2=deriv(t+dt/2,x+a*dt/2,y+b*dt/2,vx+c1*dt/2,vy+d*dt/2)
      a3,b3,c3,d3=deriv(t+dt/2,x+a2*dt/2,y+b2*dt/2,vx+c2*dt/2,vy+d2*dt/2)
      a4,b4,c4,d4=deriv(t+dt,x+a3*dt,y+b3*dt,vx+c3*dt,vy+d3*dt)
      x+=dt*(a+2*a2+2*a3+a4)/6; y+=dt*(b+2*b2+2*b3+b4)/6
      vx+=dt*(c1+2*c2+2*c3+c4)/6; vy+=dt*(d+2*d2+2*d3+d4)/6
      if i==(n_eq*spc-1): xmark=x;ymark=y
    return x, y, (x-xmark)/n_meas, (y-ymark)/n_meas, vx, vy

def rocking(theta,land,F0=2.,period=40,spc=4000):
    mins=enumerate_minima(theta,land,17); m=mins[0]; S=J.contact_factors(theta,land.vectors,positions)
    out=rk4_run(np.asarray(land.vectors,float),np.asarray(land.c_cos,float),np.asarray(land.c_sin,float),np.asarray(S.real,float),np.asarray(S.imag,float),F0,period,40,80,spc,m['xy'][0],m['xy'][1])
    xf,yf,dx,dy,vx,vy=out
    duv=AINV@np.array([dx,dy])
    return dict(dx_per_cycle=dx,dy_per_cycle=dy,u_per_cycle=duv[0],v_per_cycle=duv[1],m_round=int(round(duv[0])),n_round=int(round(duv[1])),u_err=abs(duv[0]-round(duv[0])),v_err=abs(duv[1]-round(duv[1])))

rows=[]
for L in [centered,sym,inv]:
    mins=enumerate_minima(1.5,L,21)
    print('\n',L.name,'minima',[(m['uv'],m['U']) for m in mins])
    fp,_,_=branch_fold(1.5,L,mins[0]['xy'],+1); fm,_,_=branch_fold(1.5,L,mins[0]['xy'],-1)
    rr=rocking(1.5,L)
    row=dict(landscape=L.name,Fc_plus=fp,Fc_minus=fm,delta_F=fp-fm,rho=(fp-fm)/(fp+fm),**rr)
    rows.append(row); print(row)

# exact symmetry contracts
D=pd.DataFrame(rows)
orig=D[D.landscape=='2H_centered'].iloc[0]; invr=D[D.landscape=='2H_exact_inverted'].iloc[0]; sy=D[D.landscape=='2H_matched_symmetrized'].iloc[0]
contracts={
 'sym_static_split_abs':abs(sy.delta_F),
 'inversion_threshold_swap_plus_abs':abs(invr.Fc_plus-orig.Fc_minus),
 'inversion_threshold_swap_minus_abs':abs(invr.Fc_minus-orig.Fc_plus),
 'inversion_current_u_sum_abs':abs(invr.u_per_cycle+orig.u_per_cycle),
 'inversion_current_v_sum_abs':abs(invr.v_per_cycle+orig.v_per_cycle),
 'sym_current_norm':float(np.hypot(sy.u_per_cycle,sy.v_per_cycle)),
}
print('contracts',contracts)
D.to_csv('/mnt/data/janus_resolve/matched_symmetry_static_dynamic.csv',index=False)
pd.DataFrame([contracts]).to_csv('/mnt/data/janus_resolve/matched_symmetry_contracts.csv',index=False)
