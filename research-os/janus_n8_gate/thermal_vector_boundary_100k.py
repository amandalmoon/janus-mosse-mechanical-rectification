import numpy as np,pandas as pd
from pathlib import Path
ROOT=Path('/mnt/data/janus_n8_gate')
df=pd.read_csv(ROOT/'rigid_release/Janus_MoSSe_AuditResolved_ReproducibilityRelease/data/raw_thermal/free_thermal_trajectory_raw_canonical.csv')
rows=[]; B=100000
for T in [0.65,0.70]:
 g=df[df.T==T] if False else df[np.isclose(df['T'],T)]
 X=g[['mean_u','mean_v']].to_numpy(float); mean=X.mean(0); n=len(X)
 for seed in [20260919,8675309]:
  rng=np.random.default_rng(seed+int(T*100))
  bm=np.empty((B,2))
  for b0 in range(0,B,250):
   bs=min(250,B-b0); idx=rng.integers(0,n,size=(bs,n)); bm[b0:b0+bs]=X[idx].mean(1)
  C=np.cov(bm-mean,rowvar=False); Ci=np.linalg.inv(C)
  d=bm-mean; d2=np.einsum('bi,ij,bj->b',d,Ci,d)
  q95=np.quantile(d2,.95); zd2=mean@Ci@mean
  uci=np.quantile(bm[:,0],[.025,.975]);vci=np.quantile(bm[:,1],[.025,.975])
  rows.append(dict(T=T,seed=seed,mean_u=mean[0],mean_v=mean[1],u_lo=uci[0],u_hi=uci[1],v_lo=vci[0],v_hi=vci[1],zero_d2=zd2,q95=q95,zero_excluded=zd2>q95))
out=pd.DataFrame(rows); out.to_csv(ROOT/'n8_thermal_vector_boundary_100k.csv',index=False);print(out.to_string(index=False))
