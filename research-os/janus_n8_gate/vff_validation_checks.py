import sys,json,numpy as np,pandas as pd
from pathlib import Path
sys.path.insert(0,'/mnt/data/janus_n8_gate')
import vff_reconstruction as V
# continuum constants from energy form
ks=5.289992;kt=2.334491;a=3.25;conv=16.02176634;A0=np.sqrt(3)/2*a*a
vecs=np.array([[1,0],[.5,np.sqrt(3)/2],[-.5,np.sqrt(3)/2],[-1,0],[-.5,-np.sqrt(3)/2],[.5,-np.sqrt(3)/2]])*a
bonds=vecs[:3];pairs=[(i,(i+1)%6) for i in range(6)]
def E(strain):
 F=np.eye(2)+strain; vv=[F@v for v in vecs]
 eb=sum(.5*ks*(np.linalg.norm(F@v)-a)**2 for v in bonds)
 ea=sum(.5*kt*(np.arccos(np.clip(np.dot(vv[i],vv[j])/(np.linalg.norm(vv[i])*np.linalg.norm(vv[j])),-1,1))-np.pi/3)**2 for i,j in pairs)
 return eb+ea
h=1e-5;Z=np.zeros((2,2));e1=np.array([[1.,0],[0,0]]);e2=np.array([[0,0],[0,1.]]);sh=np.array([[0,.5],[.5,0]])
sec=lambda D:(E(h*D)-2*E(Z)+E(-h*D))/h**2/A0
C11=sec(e1)*conv; C12=(E(h*(e1+e2))-E(h*(e1-e2))-E(h*(-e1+e2))+E(-h*(e1+e2)))/(4*h*h*A0)*conv; C66=sec(sh)*conv
# derivative spot check at slightly perturbed state to avoid zero gradients only
m=V.VFFContact(1.5,1.0); g0=V.zero_ground(m); z=g0[2].copy();rng=np.random.default_rng(123);z[2:]+=rng.normal(scale=2e-5,size=m.nint)
E0,g,H=m.eval(z,0.0,True); inds=[0,1,2,10,50,100,150,200,252];hh=2e-6;ge=[];he=[]
for j in inds:
 zp=z.copy();zm=z.copy();zp[j]+=hh;zm[j]-=hh
 Ep,gp,_=m.eval(zp,0.0,False);Em,gm,_=m.eval(zm,0.0,False)
 ge.append(abs((Ep-Em)/(2*hh)-g[j]));he.append(np.max(np.abs((gp-gm)/(2*hh)-H[:,j])))
# rigid constraints C@Q
pos=m.pos;N=m.N;C=np.zeros((3,2*N));C[0,0::2]=1;C[1,1::2]=1;C[2,0::2]=-pos[:,1];C[2,1::2]=pos[:,0]
out={'bond_count':len(m.bonds),'angle_count':len(m.angles),'C11_Npm':C11,'C12_Npm':C12,'C66_Npm':C66,'constraint_residual':float(np.max(np.abs(C@m.Q))),'energy_gradient_fd_max':float(max(ge)),'gradient_hessian_col_fd_max':float(max(he)),'ground_grad_norm':float(g0[3]),'ground_hessian_min_eig':float(g0[4][0])}
Path('/mnt/data/janus_n8_gate/n8_vff_validation_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
