from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
RAW=ROOT/'data'/'raw_thermal'/'free_thermal_trajectory_raw_canonical.csv'
OUT=ROOT/'data'/'canonical'/'free_thermal_cluster_ci_recomputed.csv'
NBOOT=10000
SEED=20260917

df=pd.read_csv(RAW)
rng=np.random.default_rng(SEED)
rows=[]
for T,g in df.groupby('T',sort=True):
    g=g.sort_values('traj').reset_index(drop=True)
    # Each row already aggregates all measured cycles of one independent trajectory.
    mv=g['mean_v'].to_numpy(float)
    pn=g['frac_neg_y'].to_numpy(float)
    pt=g['frac_target'].to_numpy(float)
    n=len(g)
    idx=rng.integers(0,n,size=(NBOOT,n))
    bmv=mv[idx].mean(axis=1); bpn=pn[idx].mean(axis=1); bpt=pt[idx].mean(axis=1)
    rows.append(dict(T=float(T),n=n,mean_v=mv.mean(),P_neg_y=pn.mean(),P_target=pt.mean(),
                     mean_v_ci_lo=np.quantile(bmv,.025),mean_v_ci_hi=np.quantile(bmv,.975),
                     P_neg_y_ci_lo=np.quantile(bpn,.025),P_neg_y_ci_hi=np.quantile(bpn,.975),
                     P_target_ci_lo=np.quantile(bpt,.025),P_target_ci_hi=np.quantile(bpt,.975)))
pd.DataFrame(rows).to_csv(OUT,index=False)
print(OUT)
