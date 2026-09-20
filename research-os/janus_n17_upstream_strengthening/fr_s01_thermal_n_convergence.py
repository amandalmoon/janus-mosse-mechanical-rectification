from pathlib import Path
import numpy as np,pandas as pd,json,math
from scipy.stats import f
OUT=Path('/mnt/data/janus_n17_upstream_strengthening');RAW=Path('/mnt/data/janus_redteam_gate/rtb01')
rng=np.random.default_rng(2026091902);Ts=[.50,.55,.60,.65,.70];Ns=[50,100,200,300,500,750,1000];R=500
rows=[];fullrows=[]
for T in Ts:
    xs=[]
    for seed in [2026091900,2026101900]:
        z=np.load(RAW/f'cycles_T{T:.2f}_N500_C160_orbit_seed{seed}.npz')
        xs.append(np.c_[z['u'][:,60:160].mean(axis=1),z['v'][:,60:160].mean(axis=1)])
    X=np.vstack(xs);full=X.mean(axis=0);fullnorm=np.linalg.norm(full)
    fullrows.append(dict(T=T,N=1000,mean_u=full[0],mean_v=full[1],norm=fullnorm))
    for N in Ns:
        reps=1 if N==1000 else R; reject=[]; ciu=[];civ=[];reld=[];mus=[]
        for r in range(reps):
            ind=np.arange(1000) if N==1000 else rng.choice(1000,N,replace=False)
            Y=X[ind];mu=Y.mean(axis=0);S=np.cov(Y,rowvar=False,ddof=1);Sinv=np.linalg.pinv(S);T2=float(N*mu@Sinv@mu);crit=float(2*(N-1)/(N-2)*f.ppf(.95,2,N-2));reject.append(T2>crit)
            se=Y.std(axis=0,ddof=1)/math.sqrt(N);ciu.append(2*1.96*se[0]);civ.append(2*1.96*se[1]);reld.append(np.linalg.norm(mu-full)/(fullnorm+1e-15));mus.append(mu)
        mus=np.array(mus)
        rows.append(dict(T=T,N=N,reps=reps,reject_fraction=np.mean(reject),mean_ci_width_u=np.mean(ciu),mean_ci_width_v=np.mean(civ),median_relative_mean_error=np.median(reld),p90_relative_mean_error=np.quantile(reld,.9),mean_estimate_u=mus[:,0].mean(),mean_estimate_v=mus[:,1].mean()))
df=pd.DataFrame(rows);df.to_csv(OUT/'fr_s01_thermal_n_convergence.csv',index=False);pd.DataFrame(fullrows).to_csv(OUT/'fr_s01_full_pool_targets.csv',index=False)
need=[]
for T,g in df.groupby('T'):
    q=g[g.reject_fraction>=.95]
    need.append(dict(T=T,min_N_for_95pct_rejection_stability=int(q.N.min()) if len(q) else None,reject_fraction_at_N500=float(g[g.N==500].reject_fraction.iloc[0]),reject_fraction_at_N750=float(g[g.N==750].reject_fraction.iloc[0]),reject_full_N1000=bool(g[g.N==1000].reject_fraction.iloc[0])))
needdf=pd.DataFrame(need);needdf.to_csv(OUT/'fr_s01_thermal_precision_decision_summary.csv',index=False)
summary={'resamples_per_subsample_N':R,'Ns':Ns,'temperatures':Ts,'criterion':'fraction of without-replacement trajectory subsamples whose 95% Hotelling T2 test excludes the zero vector','min_N_for_95pct_rejection_stability':{str(r.T): (None if pd.isna(r.min_N_for_95pct_rejection_stability) else int(r.min_N_for_95pct_rejection_stability)) for _,r in needdf.iterrows()},'interpretation':'The pooled N=1000 high-temperature design is precision-motivated: lower N increasingly destabilizes the reject/non-reject decision at the weakest T*=0.70 signal. This is a precision/convergence audit, not a post hoc power calculation.'}
(OUT/'fr_s01_thermal_n_convergence_summary.json').write_text(json.dumps(summary,indent=2));print(df.to_string(index=False));print(json.dumps(summary,indent=2))
