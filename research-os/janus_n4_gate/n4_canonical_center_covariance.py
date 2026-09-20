import sys, numpy as np, pandas as pd
from scipy.optimize import minimize
sys.path.insert(0,'/mnt/data/janus_n4_gate')
from n4_core import *
# canonical centered landscape
CAN=translate_landscape(BASE,A@UVC,'canonical_centered')
rng=np.random.default_rng(20260919)
rows=[]
for i in range(20):
 b_uv=rng.random(2); B=translate_landscape(BASE,A@b_uv,f'shift{i}')
 den=np.sum(B.c_cos**2+B.c_sin**2)
 def obj(uv):
  L=translate_landscape(B,A@(np.asarray(uv)%1)); return np.sum(L.c_sin**2)/den
 pred=(UVC-b_uv)%1
 cands=[]
 for st in [pred,(0,0),(.5,.5),rng.random(2),rng.random(2)]:
  rr=minimize(obj,st,method='Nelder-Mead',options={'xatol':1e-13,'fatol':1e-15,'maxiter':5000});cands.append((rr.fun,rr.x%1))
 cands.sort(key=lambda z:z[0]); val,uv=cands[0]; centered=translate_landscape(B,A@uv)
 # Compare centered coeffs to CAN, allowing exact direct equality in same reciprocal basis
 cc=np.max(np.abs(centered.c_cos-CAN.c_cos)); ss=np.max(np.abs(centered.c_sin-CAN.c_sin))
 duv=(uv-pred);duv-=np.round(duv)
 rows.append(dict(i=i,b_u=b_uv[0],b_v=b_uv[1],u_star=uv[0],v_star=uv[1],pred_u=pred[0],pred_v=pred[1],center_shift_error=np.linalg.norm(A@duv),Amin=val,max_cos_coeff_error=cc,max_sin_coeff_error=ss))
pd.DataFrame(rows).to_csv('/mnt/data/janus_n4_gate/n4_canonical_center_covariance.csv',index=False)
print(pd.DataFrame(rows).describe().to_string())
