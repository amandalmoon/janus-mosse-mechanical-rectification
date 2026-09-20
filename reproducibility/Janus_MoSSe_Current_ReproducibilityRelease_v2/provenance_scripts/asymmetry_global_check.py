import sys, numpy as np, pandas as pd
from scipy.optimize import minimize
sys.path.insert(0,'/mnt/data/janus_resolve/Janus_mechanical_rectification_v18_ProfessorCorrected_release/source')
import janus_fourier_landscapes_v12 as J
A=np.column_stack([J.A1,J.A2])
keys=list(J.DFT_TABLE)
rows=[]
for key in keys:
 land=J.dft_landscape(key)
 denom=np.sum(land.c_cos**2+land.c_sin**2)
 def oddfrac(uv):
  a=A@(np.asarray(uv)%1);d=land.vectors@a
  sp=-land.c_cos*np.sin(d)+land.c_sin*np.cos(d)
  return np.sum(sp**2)/denom
 # brute grid 181x181 + multistart exact minimization
 us=np.linspace(0,1,181,endpoint=False); best=(1e9,None)
 for u in us:
  for v in us:
   val=oddfrac([u,v])
   if val<best[0]:best=(val,(u,v))
 cands=[]
 starts=[best[1],(0,0),(.5,.5),(1/3,1/3),(2/3,1/6),(.25,.75)]
 for st in starts:
  r=minimize(oddfrac,st,method='Nelder-Mead',options={'xatol':1e-13,'fatol':1e-15,'maxiter':5000})
  cands.append((r.fun,r.x%1))
 cands.sort(key=lambda x:x[0]); val,uv=cands[0]
 # analytic translation-invariant shell phase: arg product of complex amplitudes C_i in each triad; here all 3 same phase per shell -> sin(3phi)
 ph=np.radians(np.asarray(J.DFT_TABLE[key]['phi'],float)); chis=np.sin(3*ph)
 rows.append(dict(key=key,grid_min=best[0],opt_min=val,u=uv[0],v=uv[1],rms=np.sqrt(val),chi1=chis[0],chi2=chis[1],chi3=chis[2],multistart_spread=max(c[0] for c in cands)-min(c[0] for c in cands)))
 print(rows[-1])
pd.DataFrame(rows).to_csv('/mnt/data/janus_resolve/asymmetry_global_check.csv',index=False)
