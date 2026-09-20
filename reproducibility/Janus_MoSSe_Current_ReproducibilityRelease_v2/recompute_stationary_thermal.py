from pathlib import Path
import csv, math
import numpy as np
from scipy.stats import f as fdist
ROOT=Path(__file__).resolve().parent
RAW=ROOT/'data'/'raw_thermal_stationary'/'stationary_thermal_trajectory_raw.csv'
rows=list(csv.DictReader(open(RAW,newline='',encoding='utf-8')))
Ts=sorted({round(float(r['T']),2) for r in rows})
print('T,n,mean_u,mean_v,T2,crit95,zero_excluded,P_neg_y,P_target')
for T in Ts:
    rr=[r for r in rows if abs(float(r['T'])-T)<1e-12]
    X=np.array([[float(r['mean_u']),float(r['mean_v'])] for r in rr])
    n=len(X); m=X.mean(0); S=np.cov(X,rowvar=False,ddof=1); T2=float(n*m@np.linalg.inv(S)@m); crit=float(2*(n-1)/(n-2)*fdist.ppf(.95,2,n-2))
    pn=np.mean([float(r['frac_neg_y']) for r in rr]); pt=np.mean([float(r['frac_target']) for r in rr])
    print(f'{T:.2f},{n},{m[0]:.12g},{m[1]:.12g},{T2:.8g},{crit:.8g},{T2>crit},{pn:.8g},{pt:.8g}')
