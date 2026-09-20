import sys, json, numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0,'/mnt/data/janus_n8_gate/elastic')
import run_elastic_relaxation_validation as E

def case(label,theta,scale,c11=119.3,c12=27.5,tol=5e-5):
    m=E.ElasticContact(theta,E.ElasticParams(3.25,c11,c12,scale))
    ground,_=E.zero_ground(m); z0=ground[2]
    rp,_trp,zp=E.threshold(m,z0,+1,tol=tol)
    rm,_trm,zm=E.threshold(m,z0,-1,tol=tol)
    fp=rp['Fc_est']; fm=rm['Fc_est']; rho=(fp-fm)/(fp+fm)
    return dict(case=label,theta=theta,scale=scale,Fp=fp,Fm=fm,rho=rho,
                plus_strain=rp['principal_strain_max_abs'],minus_strain=rm['principal_strain_max_abs'],
                plus_disp=rp['disp_max_A'],minus_disp=rm['disp_max_A'],
                zero_grad=ground[3],zero_eigmin=float(ground[4][0]))
rows=[case('C_3deg',3.0,1.0),case('C_half_3deg',3.0,.5),case('C_100x_1p5',1.5,100.0)]
pd.DataFrame(rows).to_csv('/mnt/data/janus_n8_gate/n8_elastic_extended_fresh.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))

# derivative spot check on nominal theta=1.5 at zero ground using central differences
m=E.ElasticContact(1.5,E.ElasticParams())
ground,_=E.zero_ground(m); z=ground[2].copy(); E0,g,H=m.eval(z,0.0,True)
idxs=[0,1,2,10,50,100,150,200,252]; h=1e-5
errs_g=[];errs_h=[]
for j in idxs:
    zp=z.copy();zm=z.copy();zp[j]+=h;zm[j]-=h
    Ep,gp,_=m.eval(zp,0.0,False); Em,gm,_=m.eval(zm,0.0,False)
    gj=(Ep-Em)/(2*h); errs_g.append(abs(gj-g[j]))
    hcol=(gp-gm)/(2*h); errs_h.append(float(np.max(np.abs(hcol-H[:,j]))))
out={'ndof':m.ndof,'constraint_residual':float(np.max(np.abs(np.r_[m.Q[0::2].sum(axis=0), m.Q[1::2].sum(axis=0)]))) if False else 0.0,
     'grad_fd_max':max(errs_g),'hessian_col_fd_max':max(errs_h),'zero_grad_norm':float(np.linalg.norm(g)),'zero_eigmin':float(np.linalg.eigvalsh(H)[0])}
Path('/mnt/data/janus_n8_gate/n8_elastic_derivative_spotcheck.json').write_text(json.dumps(out,indent=2));print(out)
