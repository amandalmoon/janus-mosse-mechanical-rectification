from pathlib import Path
import json, sys
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import janus_fourier_landscapes_v12 as J
import dft_guided_material_v12 as M

old_theta=1.4771792325745448
exact_theta=1.4772214046124086
temps=[0.005,0.01,0.015,0.02,0.03,0.04,0.05,0.06,0.08,0.10,0.12,0.16]
ntraj=1000;base_seed=20260913
m=J.dft_landscape('2H_MoSSe_Se-S-Se-S')

def fit_sig(T,D):
    T=np.asarray(T,float);D=np.asarray(D,float)
    def model(t,t50,width): return 1/(1+np.exp((t-t50)/width))
    popt,_=curve_fit(model,T,D,p0=[.054,.018],bounds=([0,.001],[.2,.2]),maxfev=10000)
    fit=model(T,*popt); r2=1-np.sum((D-fit)**2)/np.sum((D-D.mean())**2)
    return float(popt[0]),float(popt[1]),float(r2)

def run(theta,label):
    arr=M._arrays(theta,m);x0,y0=M.zero_minimum(theta,m,25.)
    rows=[]
    for ti,T in enumerate(temps):
        ps=[];ks=[]
        for direction in (+1,-1):
            seed=base_seed+100000*ti+(0 if direction>0 else 500)
            shifts=M._baoab_halfcycle(ntraj,seed,x0,y0,direction,float(T),*arr,3.5,20.,.005,25.,10.)
            k=int(np.sum((shifts*direction)>0)); p=k/ntraj
            ks.append(k);ps.append(p)
        D=abs(ps[0]-ps[1])
        rows.append({'label':label,'theta_deg':theta,'T_star':T,'k_forward':ks[0],'k_reverse':ks[1],
                     'p_forward':ps[0],'p_reverse':ps[1],'D':D})
        print(label,T,ks,ps,D,flush=True)
    df=pd.DataFrame(rows); t50,w,r2=fit_sig(df.T_star,df.D)
    return df,{'theta_deg':theta,'T50':t50,'width':w,'R2':r2}

old,so=run(old_theta,'old_midpoint')
ex,se=run(exact_theta,'exact_midpoint')
merged=old.merge(ex,on='T_star',suffixes=('_old','_exact'))
for col in ['k_forward','k_reverse','p_forward','p_reverse','D']:
    merged['delta_'+col]=merged[col+'_exact']-merged[col+'_old']
merged.to_csv(HERE/'thermal_midpoint_old_vs_exact.csv',index=False)
summary={'old':so,'exact':se,'delta_T50':se['T50']-so['T50'],'delta_width':se['width']-so['width'],
         'max_abs_delta_D':float(np.max(np.abs(merged.delta_D))),
         'temperatures_with_any_count_change':int(np.sum((merged.delta_k_forward!=0)|(merged.delta_k_reverse!=0))),
         'total_abs_count_changes':int(np.sum(np.abs(merged.delta_k_forward)+np.abs(merged.delta_k_reverse)))}
Path(HERE/'thermal_midpoint_dependency.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
