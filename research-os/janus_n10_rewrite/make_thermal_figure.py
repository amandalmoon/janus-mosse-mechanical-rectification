import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

raw = pd.read_csv('/mnt/data/janus_n10_rewrite/free_thermal_trajectory_raw_canonical.csv')
joint = pd.read_csv('/mnt/data/janus_n8_gate/n8_thermal_vector_joint_audit.csv')

Ts = np.sort(raw['T'].unique())
rng = np.random.default_rng(20260919)
rows=[]
B=10000
for T in Ts:
    g=raw[raw.T==T] if False else raw[raw['T']==T]
    arr=g[['mean_u','mean_v','frac_neg_y','frac_target']].to_numpy(float)
    n=len(arr)
    means=arr.mean(axis=0)
    # vectorized bootstrap in chunks to avoid large memory
    sums=[]
    chunk=1000
    for s in range(0,B,chunk):
        b=min(chunk,B-s)
        idx=rng.integers(0,n,size=(b,n))
        sums.append(arr[idx].mean(axis=1))
    bs=np.vstack(sums)
    lo=np.quantile(bs,0.025,axis=0)
    hi=np.quantile(bs,0.975,axis=0)
    rows.append([T,*means,*lo,*hi])
cols=['T','mean_u','mean_v','Pneg','Ptarget','u_lo','v_lo','Pneg_lo','Ptarget_lo','u_hi','v_hi','Pneg_hi','Ptarget_hi']
sumdf=pd.DataFrame(rows,columns=cols)
sumdf.to_csv('/mnt/data/janus_n10_rewrite/thermal_summary_for_figure.csv',index=False)

fig, axes = plt.subplots(1,3,figsize=(12,4.1))
ax=axes[0]
ax.errorbar(sumdf['T'], sumdf.mean_u, yerr=[sumdf.mean_u-sumdf.u_lo, sumdf.u_hi-sumdf.mean_u], marker='o', capsize=2, label=r'$\langle u\rangle$')
ax.errorbar(sumdf['T'], sumdf.mean_v, yerr=[sumdf.mean_v-sumdf.v_lo, sumdf.v_hi-sumdf.mean_v], marker='s', capsize=2, label=r'$\langle v\rangle$')
ax.axhline(0,linewidth=0.8)
ax.set_xlabel(r'$T^*$')
ax.set_ylabel('mean lattice displacement / cycle')
ax.set_title('(a) Component currents')
ax.legend(frameon=False,fontsize=8)

ax=axes[1]
j=joint[joint['T']>=0.50].copy()
# use first bootstrap seed distance ratio when available, otherwise Hotelling ratio
ratio=[]
for _,r in j.iterrows():
    if np.isfinite(r.get('seed1_zero_d2',np.nan)) and np.isfinite(r.get('seed1_q95',np.nan)):
        ratio.append(r['seed1_zero_d2']/r['seed1_q95'])
    else:
        ratio.append(r['hotelling_T2']/r['hotelling_crit95'])
ax.plot(j['T'],ratio,marker='o')
ax.axhline(1,linewidth=0.8)
ax.set_xlabel(r'$T^*$')
ax.set_ylabel(r'joint zero-vector test $d_0^2/q_{0.95}$')
ax.set_title('(b) Joint 2D current')
ax.text(0.655,1.05,'zero excluded',fontsize=8)
ax.text(0.665,0.55,'zero not excluded at 0.70',fontsize=8)

ax=axes[2]
ax.errorbar(sumdf['T'],sumdf.Pneg,yerr=[sumdf.Pneg-sumdf.Pneg_lo,sumdf.Pneg_hi-sumdf.Pneg],marker='o',capsize=2,label=r'$P(\Delta y<0)$')
ax.plot(sumdf['T'],sumdf.Ptarget,marker='s',label=r'$P[(m,n)=(1,-1)]$')
ax.axhline(0.5,linewidth=0.8)
ax.set_xlabel(r'$T^*$')
ax.set_ylabel('probability')
ax.set_ylim(-0.03,1.04)
ax.set_title('(c) Direction vs exact winding')
ax.legend(frameon=False,fontsize=8)

fig.tight_layout(pad=1.0,w_pad=1.6)
fig.savefig('/mnt/data/janus_n10_rewrite/Figure_6_thermal_vector_hierarchy.png',dpi=320,bbox_inches='tight')
plt.close(fig)
