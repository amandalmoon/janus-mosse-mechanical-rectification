from pathlib import Path
import numpy as np,pandas as pd, math
from scipy.stats import f
OUT=Path('/mnt/data/janus_redteam_gate/rtb01')
TEMPS=[.50,.55,.60,.65,.70];N=500;C=160;seed=2026091900
windows={'b10_m20':(10,30),'b30_m20':(30,50),'b60_m20':(60,80),'b100_m20':(100,120),'b140_m20':(140,160)}
def hotell(X):
 n,p=X.shape;m=X.mean(0);S=np.cov(X,rowvar=False,ddof=1);Si=np.linalg.inv(S);T2=float(n*m@Si@m);crit=float(p*(n-1)/(n-p)*f.ppf(.95,p,n-p));return m,S,T2,crit,T2>crit
def boot(X,seed,B=10000):
 n=len(X);m=X.mean(0);rng=np.random.default_rng(seed);bm=np.empty((B,2))
 for b0 in range(0,B,250):
  bs=min(250,B-b0);idx=rng.integers(0,n,size=(bs,n));bm[b0:b0+bs]=X[idx].mean(1)
 C=np.cov(bm-m,rowvar=False);Ci=np.linalg.inv(C);d=bm-m;d2=np.einsum('bi,ij,bj->b',d,Ci,d);q=float(np.quantile(d2,.95));z=float(m@Ci@m);return z,q,z>q
rows=[];dr=[];cy=[]
for ti,T in enumerate(TEMPS):
 p=OUT/f'cycles_T{T:.2f}_N{N}_C{C}_orbit_seed{seed}.npz'
 z=np.load(p);u=z['u'];v=z['v'];blocks={}
 for c in range(C):
  cy.append(dict(T=T,cycle=c+1,mean_u=u[:,c].mean(),mean_v=v[:,c].mean(),se_u=u[:,c].std(ddof=1)/math.sqrt(N),se_v=v[:,c].std(ddof=1)/math.sqrt(N)))
 for name,(a,b) in windows.items():
  X=np.column_stack([u[:,a:b].mean(1),v[:,a:b].mean(1)]);blocks[name]=X;m,S,T2,crit,exc=hotell(X);bz,bq,bex=(np.nan,np.nan,np.nan)
  if a>=60:bz,bq,bex=boot(X,20260919+ti*100+a)
  pneg=(v[:,a:b]<0).mean();ru=np.rint(u[:,a:b]);rv=np.rint(v[:,a:b]);pt=((ru==1)&(rv==-1)).mean()
  rows.append(dict(T=T,window=name,burn=a,measure=b-a,n=N,mean_u=m[0],mean_v=m[1],norm=np.linalg.norm(m),se_u=np.sqrt(S[0,0]/N),se_v=np.sqrt(S[1,1]/N),hotelling_T2=T2,crit95=crit,zero_excluded_hotelling=exc,bootstrap_zero_d2=bz,bootstrap_q95=bq,zero_excluded_bootstrap=bex,P_neg_y=pneg,P_target=pt))
 for n1,n2 in [('b30_m20','b60_m20'),('b60_m20','b100_m20'),('b100_m20','b140_m20')]:
  D=blocks[n2]-blocks[n1];m,S,T2,crit,exc=hotell(D)
  dr.append(dict(T=T,from_window=n1,to_window=n2,delta_u=m[0],delta_v=m[1],delta_norm=np.linalg.norm(m),se_delta_u=np.sqrt(S[0,0]/N),se_delta_v=np.sqrt(S[1,1]/N),paired_T2=T2,crit95=crit,drift_detected=exc))
pd.DataFrame(rows).to_csv(OUT/'orbit_block_stationarity_N500.csv',index=False);pd.DataFrame(dr).to_csv(OUT/'orbit_paired_drift_N500.csv',index=False);pd.DataFrame(cy).to_csv(OUT/'orbit_cycle_means_N500.csv',index=False)
print('BLOCKS')
print(pd.DataFrame(rows).to_string(index=False))
print('\nDRIFT')
print(pd.DataFrame(dr).to_string(index=False))
