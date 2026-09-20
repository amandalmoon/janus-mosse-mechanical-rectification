import numpy as np, pandas as pd
from pathlib import Path
from scipy.stats import f
ROOT=Path('/mnt/data/janus_n8_gate')
RAW=ROOT/'rigid_release/Janus_MoSSe_AuditResolved_ReproducibilityRelease/data/raw_thermal/free_thermal_trajectory_raw_canonical.csv'
df=pd.read_csv(RAW)
rows=[]
B=10000
seeds=[271828,314159,161803]
for T,g in df.groupby('T',sort=True):
    X=g[['mean_u','mean_v']].to_numpy(float); n=len(X); p=2
    mean=X.mean(axis=0); S=np.cov(X,rowvar=False,ddof=1); Sinv=np.linalg.inv(S)
    T2=n*mean@Sinv@mean; crit=p*(n-1)/(n-p)*f.ppf(.95,p,n-p)
    seed_results=[]
    # joint bootstrap only near the transition; low-T is overwhelmingly nonzero and Hotelling is sufficient
    do_boot = T >= 0.50
    if do_boot:
        pn=g['frac_neg_y'].to_numpy(float)
        for seed in seeds:
            rng=np.random.default_rng(seed+int(round(100*T)))
            bm=np.empty((B,2)); bpn=np.empty(B)
            for b0 in range(0,B,250):
                bs=min(250,B-b0); idx=rng.integers(0,n,size=(bs,n))
                bm[b0:b0+bs]=X[idx].mean(axis=1); bpn[b0:b0+bs]=pn[idx].mean(axis=1)
            centered=bm-mean; C=np.cov(centered,rowvar=False,ddof=1); Cinv=np.linalg.inv(C)
            d2=np.einsum('bi,ij,bj->b',centered,Cinv,centered)
            q95=float(np.quantile(d2,.95)); zero_d2=float(mean@Cinv@mean)
            uci=np.quantile(bm[:,0],[.025,.975]); vci=np.quantile(bm[:,1],[.025,.975])
            se=np.sqrt(np.diag(C)); z=np.max(np.abs(centered/se),axis=1); qmax=float(np.quantile(z,.95))
            sim_lo=mean-qmax*se; sim_hi=mean+qmax*se
            pnci=np.quantile(bpn,[.025,.975])
            seed_results.append((seed,uci,vci,zero_d2,q95,sim_lo,sim_hi,pnci))
    if do_boot:
        u_lo=min(x[1][0] for x in seed_results); u_hi=max(x[1][1] for x in seed_results)
        v_lo=min(x[2][0] for x in seed_results); v_hi=max(x[2][1] for x in seed_results)
        ell_excl=all(x[3]>x[4] for x in seed_results)
        rect_excl=all(not (x[5][0] <= 0 <= x[6][0] and x[5][1] <= 0 <= x[6][1]) for x in seed_results)
        seedvals={f'seed{i+1}_zero_d2':seed_results[i][3] for i in range(3)}|{f'seed{i+1}_q95':seed_results[i][4] for i in range(3)}
    else:
        u_lo=u_hi=v_lo=v_hi=np.nan; ell_excl=rect_excl=np.nan; seedvals={}
    row=dict(T=T,n=n,mean_u=mean[0],mean_v=mean[1],norm=float(np.linalg.norm(mean)),
             u_ci_lo_union=u_lo,u_ci_hi_union=u_hi,v_ci_lo_union=v_lo,v_ci_hi_union=v_hi,
             hotelling_T2=T2,hotelling_crit95=crit,hotelling_zero_excluded=bool(T2>crit),
             bootstrap_ellipse_zero_excluded=ell_excl,simultaneous_rectangle_zero_excluded=rect_excl,
             Pneg=g['frac_neg_y'].mean(),Ptarget=g['frac_target'].mean(),**seedvals)
    rows.append(row)
out=pd.DataFrame(rows)
out.to_csv(ROOT/'n8_thermal_vector_joint_audit.csv',index=False)
print(out.to_string(index=False))
