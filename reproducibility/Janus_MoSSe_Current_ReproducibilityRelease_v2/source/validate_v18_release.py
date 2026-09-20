"""Numerical-contract checks for v18 new-physics outputs."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parent.parent
D=ROOT/'data'/'canonical'; R=ROOT/'reports'
roots=pd.read_csv(D/'v18_size_scaling_roots.csv')
edge=pd.read_csv(D/'v18_edge_factorization_metrics.csv')
edgefine=pd.read_csv(D/'v18_edge_zero_crossing_refinement.csv')
floq=pd.read_csv(D/'v18_relative_periodic_floquet.csv')
cont=pd.read_csv(D/'v18_amplitude_continuation.csv')
basin=pd.read_csv(D/'v18_mode_basin_probe.csv')
col=pd.read_csv(D/'v18_size_similarity_collapse.csv')
assert len(roots)==10 and roots.N.min()==37 and roots.N.max()==469
p=np.polyfit(np.log(roots.N),np.log(roots.W_D_abs_deg),1)
pred=np.polyval(p,np.log(roots.N)); r2=1-np.sum((np.log(roots.W_D_abs_deg)-pred)**2)/np.sum((np.log(roots.W_D_abs_deg)-np.log(roots.W_D_abs_deg).mean())**2)
assert abs((-p[0])-0.50313325)<2e-5 and r2>0.99999
# collapse
mx=0
for c in ['Fc_forward','Fc_reverse']:
    piv=col.pivot(index='Theta_scaled',columns='N',values=c); m=piv.mean(axis=1); rel=piv.sub(m,axis=0).abs().div(m.abs(),axis=0); mx=max(mx,float(np.nanmax(rel.to_numpy())))
assert mx<0.003
assert edge.max_factorization_error_percent.max()>9.0 and edge.max_factorization_error_percent.min()<2.5
roots_edge={}
for phi,g in edgefine.groupby('edge_phi_deg'):
    x=g.theta_deg.to_numpy(float); y=g.rho.to_numpy(float); root=np.nan
    for i in range(len(x)-1):
        if y[i]==0 or y[i]*y[i+1]<0:
            root=float(x[i] if y[i]==0 else x[i]-y[i]*(x[i+1]-x[i])/(y[i+1]-y[i])); break
    roots_edge[int(phi)]=root
assert 2.94<roots_edge[20]<2.98 and 2.87<roots_edge[25]<2.91
assert floq.poincare_residual.max()<2e-10 and floq.floquet_spectral_radius.max()<2e-13
pp=cont.pivot(index='F0',columns='branch',values='winding').dropna(); assert len(pp)==101 and int((pp.up!=pp.down).sum())==0
for _,g in basin.groupby('F0'): assert g.winding.nunique()==1
metrics={'size_exponent_alpha':float(-p[0]),'size_scaling_log_R2':float(r2),'similarity_max_rel_deviation_percent':100*mx,
         'edge_factorization_error_min_percent':float(edge.max_factorization_error_percent.min()),'edge_factorization_error_max_percent':float(edge.max_factorization_error_percent.max()),
         'edge_zero_crossing_phi20_deg':float(roots_edge[20]),'edge_zero_crossing_phi25_deg':float(roots_edge[25]),
         'max_poincare_residual':float(floq.poincare_residual.max()),'max_floquet_spectral_radius':float(floq.floquet_spectral_radius.max()),
         'continuation_mismatches':int((pp.up!=pp.down).sum()),'basin_mismatches':int(sum(g.winding.nunique()!=1 for _,g in basin.groupby('F0')))}
(R/'V18_VALIDATION_METRICS.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
print('v18 validation PASS')
print(json.dumps(metrics,indent=2))
