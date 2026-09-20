from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.linalg import null_space
from scipy.optimize import root, minimize
from scipy.spatial import Delaunay

HERE = Path(__file__).resolve().parent
RELEASE = Path('/mnt/data/janus_work/release/Janus_MoSSe_AuditResolved_ReproducibilityRelease')
SRC = RELEASE / 'source'
sys.path.insert(0, str(SRC))
import janus_fourier_landscapes_v12 as J  # noqa: E402

NPM_TO_MEV_PER_A2 = 62.41509074460763

@dataclass
class ElasticParams:
    a_ang: float = 3.25
    c11_npm: float = 119.3
    c12_npm: float = 27.5
    stiffness_scale: float = 1.0

class ElasticContact:
    def __init__(self, theta_deg: float, ep: ElasticParams):
        self.theta=float(theta_deg); self.ep=ep
        self.land=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
        self.E0=float(self.land.energy_unit_meV)
        self.pos=J.make_hexagonal_flake(6); self.N=len(self.pos)
        R=J.rotation_matrix(self.theta)
        self.delta=self.pos@R.T-self.pos
        self.G=np.asarray(self.land.vectors,float)
        self.cc=np.asarray(self.land.c_cos,float)
        self.ss=np.asarray(self.land.c_sin,float)
        self.Gouter=np.einsum('ti,tj->tij',self.G,self.G)
        self.Q=self._internal_basis(); self.nint=self.Q.shape[1]; self.ndof=2+self.nint
        self.Qb=self.Q.reshape(self.N,2,self.nint)
        self.Kfull=self._fem_K_meV()
        self.Kred=(self.Q.T@self.Kfull@self.Q)/(self.N*self.E0)

    def _internal_basis(self):
        C=np.zeros((3,2*self.N),float)
        C[0,0::2]=1; C[1,1::2]=1
        C[2,0::2]=-self.pos[:,1]; C[2,1::2]=self.pos[:,0]
        return null_space(C)

    def _fem_K_meV(self):
        tri=Delaunay(self.pos)
        K=np.zeros((2*self.N,2*self.N),float)
        c11=self.ep.c11_npm*self.ep.stiffness_scale*NPM_TO_MEV_PER_A2
        c12=self.ep.c12_npm*self.ep.stiffness_scale*NPM_TO_MEV_PER_A2
        c66=0.5*(c11-c12)
        D=np.array([[c11,c12,0],[c12,c11,0],[0,0,c66]],float)
        a2=self.ep.a_ang**2
        for nodes in tri.simplices:
            xy=self.pos[nodes]
            x1,y1=xy[0]; x2,y2=xy[1]; x3,y3=xy[2]
            det=(x2-x1)*(y3-y1)-(x3-x1)*(y2-y1)
            area=abs(det)/2
            b1,b2,b3=y2-y3,y3-y1,y1-y2
            c1,c2,c3=x3-x2,x1-x3,x2-x1
            B=np.array([[b1,0,b2,0,b3,0],[0,c1,0,c2,0,c3],[c1,b1,c2,b2,c3,b3]],float)/det
            Ke=a2*area*(B.T@D@B)
            dofs=np.array([[2*n,2*n+1] for n in nodes]).ravel()
            K[np.ix_(dofs,dofs)]+=Ke
        return K

    def unpack(self,z):
        q=np.asarray(z[:2],float); a=np.asarray(z[2:],float)
        d=np.einsum('nia,a->ni',self.Qb,a)
        return q,a,d

    def local(self,r,need_h=False):
        ph=r@self.G.T
        co=np.cos(ph); si=np.sin(ph)
        U=co@self.cc+si@self.ss
        aa=(-si*self.cc+co*self.ss)
        g=aa@self.G
        if not need_h: return U,g,None
        bb=(-co*self.cc-si*self.ss)
        H=np.einsum('nt,tij->nij',bb,self.Gouter)
        return U,g,H

    def eval(self,z,force_y=0.0,need_h=False):
        q,a,d=self.unpack(z)
        r=q[None,:]+self.delta+d
        Uloc,gloc,Hloc=self.local(r,need_h)
        E=float(Uloc.mean()+0.5*a@self.Kred@a-force_y*q[1])
        gq=gloc.mean(axis=0); gq[1]-=force_y
        ga=np.einsum('nia,ni->a',self.Qb,gloc)/self.N+self.Kred@a
        g=np.r_[gq,ga]
        if not need_h: return E,g,None
        Hqq=Hloc.mean(axis=0)
        Hqa=np.einsum('nij,nja->ia',Hloc,self.Qb)/self.N
        Haa=np.einsum('nia,nij,njb->ab',self.Qb,Hloc,self.Qb,optimize=True)/self.N+self.Kred
        H=np.block([[Hqq,Hqa],[Hqa.T,Haa]])
        return E,g,H

    def strain_metrics(self,z):
        _,_,d=self.unpack(z)
        tri=Delaunay(self.pos); vals=[]
        for nodes in tri.simplices:
            xy=self.pos[nodes]
            x1,y1=xy[0]; x2,y2=xy[1]; x3,y3=xy[2]
            det=(x2-x1)*(y3-y1)-(x3-x1)*(y2-y1)
            b1,b2,b3=y2-y3,y3-y1,y1-y2
            c1,c2,c3=x3-x2,x1-x3,x2-x1
            B=np.array([[b1,0,b2,0,b3,0],[0,c1,0,c2,0,c3],[c1,b1,c2,b2,c3,b3]],float)/det
            exx,eyy,gxy=B@d[nodes].reshape(-1); exy=gxy/2
            vals.append(np.linalg.eigvalsh([[exx,exy],[exy,eyy]]))
        vals=np.asarray(vals); disp=np.linalg.norm(d,axis=1)
        return dict(disp_rms_A=float(self.ep.a_ang*np.sqrt(np.mean(disp**2))),
                    disp_max_A=float(self.ep.a_ang*np.max(disp)),
                    principal_strain_max_abs=float(np.max(np.abs(vals))))


def uv_to_xy(uv):
    return np.column_stack([J.A1,J.A2])@np.asarray(uv,float)

def wrap_uv(xy):
    A=np.column_stack([J.A1,J.A2]); u=np.linalg.solve(A,np.asarray(xy,float)); return u-np.floor(u)

def pdist(u,v):
    A=np.column_stack([J.A1,J.A2]); d=np.asarray(u)-np.asarray(v); d-=np.round(d); return np.linalg.norm(A@d)

def rigid_minima(theta,ngrid=17):
    S=J.contact_factors(theta,J.dft_landscape('2H_MoSSe_Se-S-Se-S').vectors,J.make_hexagonal_flake(6))
    land=J.dft_landscape('2H_MoSSe_Se-S-Se-S'); roots=[]
    for u in np.linspace(0,1,ngrid,endpoint=False):
        for v in np.linspace(0,1,ngrid,endpoint=False):
            x0=uv_to_xy((u,v))
            fun=lambda xy:J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0,0)[1]
            jac=lambda xy:J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0,0)[2]
            rr=root(fun,x0,jac=jac,method='hybr',options={'xtol':1e-11,'maxfev':300})
            if np.linalg.norm(fun(rr.x))>1e-7: continue
            uv=wrap_uv(rr.x)
            if any(pdist(uv,r['uv'])<2e-6 for r in roots): continue
            xy=uv_to_xy(uv); U,g,H=J.contact_ugh(float(xy[0]),float(xy[1]),S,land,0,0)
            ev=np.linalg.eigvalsh(H); roots.append(dict(uv=uv,xy=xy,U=U,ev=ev))
    return sorted([r for r in roots if r['ev'][0]>1e-7],key=lambda r:r['U'])


def minimize_state(model,z0,F,maxiter=800):
    fun=lambda z:model.eval(z,F,False)[0]
    jac=lambda z:model.eval(z,F,False)[1]
    rr=minimize(fun,z0,jac=jac,method='L-BFGS-B',options={'ftol':1e-14,'gtol':2e-9,'maxiter':maxiter,'maxls':40,'maxcor':20})
    E,g,H=model.eval(rr.x,F,True); ev=np.linalg.eigvalsh(H)
    return rr,E,g,H,ev


def zero_ground(model):
    sols=[]
    for i,m in enumerate(rigid_minima(model.theta,17)):
        z=np.zeros(model.ndof); z[:2]=m['xy']
        rr,E,g,H,ev=minimize_state(model,z,0.0,1200)
        sols.append((E,i,rr.x.copy(),float(np.linalg.norm(g)),ev,rr.success))
    sols.sort(key=lambda x:x[0]); return sols[0],sols


def branch_test(model,zseed,sign,F,ref_q):
    fun=lambda z:model.eval(z,sign*F,False)[1]
    jac=lambda z:model.eval(z,sign*F,True)[2]
    rr=root(fun,zseed,jac=jac,method='hybr',options={'xtol':2e-9,'maxfev':300})
    E,g,H=model.eval(rr.x,sign*F,True); ev=np.linalg.eigvalsh(H)
    q=rr.x[:2]; jump=float(np.linalg.norm(q-ref_q))
    stable=(np.linalg.norm(g)<2e-6 and ev[0]>1e-7 and jump<0.45 and abs(q[1])<20)
    return stable,rr.x,E,g,ev,jump,rr.message


def threshold(model,z0,sign,step=0.10,tol=5e-4,maxF=5.0):
    Flo=0.; zlo=z0.copy(); qlo=zlo[:2].copy(); trace=[]
    F=step; Fhi=None
    while F<=maxF+1e-12:
        ok,z,E,g,ev,jump,msg=branch_test(model,zlo,sign,F,qlo)
        trace.append(dict(F=F,ok=ok,eigmin=ev[0],grad=np.linalg.norm(g),jump=jump))
        if ok:
            Flo=F; zlo=z.copy(); qlo=zlo[:2].copy(); F+=step
        else:
            Fhi=F; break
    if Fhi is None: raise RuntimeError('threshold not found')
    while Fhi-Flo>tol:
        Fm=(Flo+Fhi)/2
        ok,z,E,g,ev,jump,msg=branch_test(model,zlo,sign,Fm,qlo)
        if ok:
            Flo=Fm; zlo=z.copy(); qlo=zlo[:2].copy()
        else: Fhi=Fm
    E,g,H=model.eval(zlo,sign*Flo,True); ev=np.linalg.eigvalsh(H)
    return dict(Fc_lo=Flo,Fc_hi=Fhi,Fc_est=(Flo+Fhi)/2,eigmin_at_lo=float(ev[0]),**model.strain_metrics(zlo)),pd.DataFrame(trace),zlo


def run_case(label,scale,c11,c12,a=3.25,theta=1.5):
    model=ElasticContact(theta,ElasticParams(a,c11,c12,scale))
    ground,allsol=zero_ground(model); E0,bid,z0,gn,ev,succ=ground
    out=dict(case=label,theta_deg=theta,stiffness_scale=scale,c11_npm=c11,c12_npm=c12,a_ang=a,
             zero_E=E0,zero_branch_id=bid,zero_grad=gn,zero_eigmin=float(ev[0]),**{f'zero_{k}':v for k,v in model.strain_metrics(z0).items()})
    traces=[]
    for sign,name in [(1,'plus'),(-1,'minus')]:
        res,tr,z=threshold(model,z0,sign)
        out.update({f'{name}_{k}':v for k,v in res.items()}); tr['direction']=name; tr['case']=label; traces.append(tr)
    Fp=out['plus_Fc_est']; Fm=out['minus_Fc_est']; out['delta_Fc']=Fp-Fm; out['rho']=(Fp-Fm)/(Fp+Fm)
    return out,pd.concat(traces,ignore_index=True)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--outdir',default=str(HERE/'output')); ap.add_argument('--quick',action='store_true'); args=ap.parse_args()
    outdir=Path(args.outdir); outdir.mkdir(parents=True,exist_ok=True)
    cases=[('two_layer_effective',0.5,119.3,27.5),('nominal_one_layer',1.0,119.3,27.5),('stiffness_2x',2.0,119.3,27.5),('alt_elastic_literature',1.0,126.8,27.4)]
    if args.quick: cases=cases[:1]
    rows=[]; trs=[]
    for c in cases:
        print('RUN',c,flush=True); row,tr=run_case(*c); rows.append(row); trs.append(tr)
        print({k:row[k] for k in ['case','plus_Fc_est','minus_Fc_est','rho','zero_disp_max_A','plus_principal_strain_max_abs','minus_principal_strain_max_abs']},flush=True)
    df=pd.DataFrame(rows); trdf=pd.concat(trs,ignore_index=True)
    rp=3.0711353385; rm=1.2586722985; rr=(rp-rm)/(rp+rm)
    df['rigid_plus_Fc']=rp; df['rigid_minus_Fc']=rm; df['rigid_rho']=rr
    df['plus_change_pct']=100*(df['plus_Fc_est']/rp-1); df['minus_change_pct']=100*(df['minus_Fc_est']/rm-1); df['rho_change_pct']=100*(df['rho']/rr-1); df['rectification_sign_survives']=df['delta_Fc']>0
    df.to_csv(outdir/'elastic_relaxation_thresholds.csv',index=False); trdf.to_csv(outdir/'elastic_relaxation_continuation_traces.csv',index=False)
    (outdir/'elastic_relaxation_summary.json').write_text(json.dumps({'rigid_baseline':{'plus':rp,'minus':rm,'rho':rr},'cases':df.to_dict('records')},indent=2),encoding='utf-8')
    print('\n',df[['case','plus_Fc_est','minus_Fc_est','rho','plus_change_pct','minus_change_pct','zero_disp_max_A','plus_principal_strain_max_abs','minus_principal_strain_max_abs','rectification_sign_survives']].to_string(index=False),flush=True)
    import matplotlib.pyplot as plt
    fig,axs=plt.subplots(1,2,figsize=(9.2,3.6)); x=np.arange(len(df)); w=.34
    axs[0].bar(x-w/2,df.plus_Fc_est,w,label='+y'); axs[0].bar(x+w/2,df.minus_Fc_est,w,label='-y'); axs[0].axhline(rp,ls='--',lw=1,label='rigid +y'); axs[0].axhline(rm,ls=':',lw=1,label='rigid -y'); axs[0].set_xticks(x,df.case,rotation=22,ha='right'); axs[0].set_ylabel('Prepared-state threshold $F_c^*$'); axs[0].set_title('In-plane elastic relaxation, $\\theta=1.5^\\circ$'); axs[0].legend(fontsize=8)
    axs[1].plot(x,df.rho,'o-',label='elastic'); axs[1].axhline(rr,ls='--',lw=1,label='rigid'); axs[1].set_xticks(x,df.case,rotation=22,ha='right'); axs[1].set_ylabel('Normalized splitting $\\rho$'); axs[1].set_title('Directional splitting'); axs[1].legend(fontsize=8); fig.tight_layout(); fig.savefig(outdir/'elastic_relaxation_validation.png',dpi=220,bbox_inches='tight'); plt.close(fig)

if __name__=='__main__': main()
