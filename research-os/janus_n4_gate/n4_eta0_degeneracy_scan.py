import sys, pandas as pd, numpy as np
sys.path.insert(0,'/mnt/data/janus_n4_gate')
from n4_core import *
scan=pd.read_csv('/mnt/data/janus_n4_gate/n4_gauge_scan.csv')
rows=[]
for i,r in scan.iterrows():
 uv=np.array([r.u,r.v]);tr=translate_landscape(BASE,A@uv);L=scale_odd(tr,0)
 mins=enumerate_minima(L,ngrid=11)
 gap=(mins[1]['U']-mins[0]['U']) if len(mins)>1 else np.nan
 rows.append(dict(gauge=int(i),u=r.u,v=r.v,n_stable_minima=len(mins),U0=mins[0]['U'],gap12=gap,degenerate_pair=(len(mins)>1 and abs(gap)<1e-8)))
 print(rows[-1],flush=True)
pd.DataFrame(rows).to_csv('/mnt/data/janus_n4_gate/n4_eta0_degeneracy_scan.csv',index=False)
