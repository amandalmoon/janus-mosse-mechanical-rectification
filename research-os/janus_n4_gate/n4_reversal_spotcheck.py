import sys, pandas as pd, numpy as np
sys.path.insert(0,'/mnt/data/janus_n4_gate')
from n4_core import *
scan=pd.read_csv('/mnt/data/janus_n4_gate/n4_gauge_scan.csv')
sel=[('min_slope_tested',int(scan.slope_fd_005.idxmin())),('max_slope_tested',int(scan.slope_fd_005.idxmax())),('published_origin',0)]
rows=[]
for label,idx in sel:
 uv=scan.loc[idx,['u','v']].to_numpy(float);tr=translate_landscape(BASE,A@uv,label)
 for eta in [0.1,0.5,1.0]:
  p=prepared_thresholds(scale_odd(tr,eta),ngrid=9);m=prepared_thresholds(scale_odd(tr,-eta),ngrid=9)
  rows.append(dict(label=label,u=uv[0],v=uv[1],eta=eta,Fp_plus=p['Fp'],Fm_plus=p['Fm'],Fp_minus=m['Fp'],Fm_minus=m['Fm'],swap_plus=abs(m['Fp']-p['Fm']),swap_minus=abs(m['Fm']-p['Fp']),delta_antisym=abs(m['Delta']+p['Delta'])))
  print(rows[-1],flush=True)
pd.DataFrame(rows).to_csv('/mnt/data/janus_n4_gate/n4_eta_reversal_spotcheck.csv',index=False)
