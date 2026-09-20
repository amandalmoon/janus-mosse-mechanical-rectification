from pathlib import Path
_RELEASE_ROOT = Path(__file__).resolve().parents[1]
# Final matched-symmetry contracts using the helper definitions from matched_symmetry_audit.py
exec(open(_RELEASE_ROOT/'audit_scripts'/'matched_symmetry_audit.py').read().split('rows=[]')[0])
import pandas as pd, numpy as np
rows=[]
for L in [centered,sym,inv]:
    mins=enumerate_minima(1.5,L,21)
    branch=[]
    for i,m in enumerate(mins):
        fp,_,_=branch_fold(1.5,L,m['xy'],+1); fm,_,_=branch_fold(1.5,L,m['xy'],-1)
        branch.append((i,m,fp,fm))
        rows.append(dict(landscape=L.name,min_id=i,u0=m['uv'][0],v0=m['uv'][1],U0=m['U'],Fc_plus=fp,Fc_minus=fm,delta_F=fp-fm))
    global_p=max(z[2] for z in branch); global_m=max(z[3] for z in branch)
    rr=rocking(1.5,L)
    rows.append(dict(landscape=L.name,min_id='GLOBAL',u0=np.nan,v0=np.nan,U0=min(z[1]['U'] for z in branch),Fc_plus=global_p,Fc_minus=global_m,delta_F=global_p-global_m,**rr))

df=pd.DataFrame(rows)
G=df[df.min_id=='GLOBAL'].set_index('landscape')
o=G.loc['2H_centered']; s=G.loc['2H_matched_symmetrized']; iv=G.loc['2H_exact_inverted']
contracts=dict(
    sym_global_static_split_abs=abs(s.Fc_plus-s.Fc_minus),
    inv_threshold_swap_plus_abs=abs(iv.Fc_plus-o.Fc_minus),
    inv_threshold_swap_minus_abs=abs(iv.Fc_minus-o.Fc_plus),
    inv_current_u_sum_abs=abs(iv.u_per_cycle+o.u_per_cycle),
    inv_current_v_sum_abs=abs(iv.v_per_cycle+o.v_per_cycle),
    sym_current_norm=float(np.hypot(s.u_per_cycle,s.v_per_cycle)),
)
print(df.to_string(index=False)); print(contracts)
df.to_csv(str(_RELEASE_ROOT/'data'/'canonical'/'matched_symmetry_final.csv'),index=False)
pd.DataFrame([contracts]).to_csv(str(_RELEASE_ROOT/'data'/'canonical'/'matched_symmetry_final_contracts.csv'),index=False)
