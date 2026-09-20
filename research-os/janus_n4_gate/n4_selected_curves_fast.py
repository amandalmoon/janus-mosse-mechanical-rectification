import sys, json, math
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0,'/mnt/data/janus_n4_gate')
from n4_core import *
OUT=Path('/mnt/data/janus_n4_gate')
SCAN=pd.read_csv(OUT/'n4_gauge_scan.csv')
idx_orig=int(SCAN.index[(SCAN.u.abs()<1e-12)&(SCAN.v.abs()<1e-12)][0])
idx_center=int(SCAN.index[SCAN.is_amin_center.astype(bool)][0])
idx_min=int(SCAN.slope_fd_005.idxmin()); idx_max=int(SCAN.slope_fd_005.idxmax()); idx_zero=int(SCAN.slope_fd_005.abs().idxmin())
selected=[]
for idx,label in [(idx_orig,'published_origin'),(idx_center,'Amin_center'),(idx_min,'min_slope_tested'),(idx_max,'max_slope_tested'),(idx_zero,'near_zero_slope_tested')]:
    if idx not in [i for i,_ in selected]: selected.append((idx,label))
print('selected',selected)
curve_rows=[]; contract_rows=[]; sumrows=[]
base_grid=np.round(np.arange(0,1.0001,0.1),6)
for idx,label in selected:
    uv=SCAN.loc[idx,['u','v']].to_numpy(float); tr=translate_landscape(BASE,A@uv,label)
    z=symmetric_global_thresholds(scale_odd(tr,0.0),ngrid=13)
    vals={0.0:z}
    for eta in base_grid[1:]:
        vals[float(eta)]=prepared_thresholds(scale_odd(tr,float(eta)),ngrid=9)
    # refine around coarse maximum with 0.025 grid within +-0.1
    e0=max(vals,key=lambda e: vals[e]['Delta'])
    lo=max(0,e0-.1); hi=min(1,e0+.1)
    for eta in np.round(np.arange(lo,hi+1e-12,0.025),6):
        if float(eta) not in vals:
            vals[float(eta)]=prepared_thresholds(scale_odd(tr,float(eta)),ngrid=9)
    for eta,q in sorted(vals.items()):
        curve_rows.append(dict(label=label,gauge_index=idx,u=uv[0],v=uv[1],eta=eta,prep=('paired_global_symmetry_null' if eta==0 else 'ground'),**q))
    # susceptibility using +-0.025, +-0.05, +-0.1 with more robust enumeration
    xs=np.array([-0.1,-0.05,-0.025,0.025,0.05,0.1]); ys=[]
    for eta in xs:
        q=prepared_thresholds(scale_odd(tr,float(eta)),ngrid=11); ys.append(q['Delta'])
    ys=np.asarray(ys); slope=float(np.dot(xs,ys)/np.dot(xs,xs)); fit=slope*xs
    r2=float(1-np.sum((ys-fit)**2)/np.sum((ys-ys.mean())**2))
    # exact reversal checks
    maxerr=0
    for eta in [0.1,0.5,1.0]:
        qp=prepared_thresholds(scale_odd(tr,eta),ngrid=11); qm=prepared_thresholds(scale_odd(tr,-eta),ngrid=11)
        e1=abs(qm['Fp']-qp['Fm']); e2=abs(qm['Fm']-qp['Fp']); e3=abs(qm['Delta']+qp['Delta']); maxerr=max(maxerr,e1,e2,e3)
        contract_rows.append(dict(label=label,u=uv[0],v=uv[1],eta=eta,Fp_plus=qp['Fp'],Fm_plus=qp['Fm'],Fp_minus=qm['Fp'],Fm_minus=qm['Fm'],swap_err_plus=e1,swap_err_minus=e2,delta_antisym_err=e3))
    qdf=pd.DataFrame([r for r in curve_rows if r['label']==label])
    opt=qdf.loc[qdf.Delta.idxmax()]
    sumrows.append(dict(label=label,gauge_index=idx,u=uv[0],v=uv[1],origin_fixed_odd_fraction=odd_fraction(tr),origin_fixed_odd_rms=math.sqrt(odd_fraction(tr)),slope=slope,slope_R2=r2,eta_opt_grid=float(opt.eta),Delta_opt_grid=float(opt.Delta),rho_opt_grid=float(opt.rho),Delta_eta1=float(qdf[qdf.eta==1.0].Delta.iloc[0]),sym_eta0_split=float(z['Delta']),max_reversal_contract_err=maxerr))
    print(label,'slope',slope,'opt',float(opt.eta),'Dopt',float(opt.Delta),'D1',float(qdf[qdf.eta==1.0].Delta.iloc[0]),flush=True)
CURVE=pd.DataFrame(curve_rows); CURVE.to_csv(OUT/'n4_selected_eta_curves.csv',index=False)
CON=pd.DataFrame(contract_rows); CON.to_csv(OUT/'n4_eta_reversal_contracts.csv',index=False)
SEL=pd.DataFrame(sumrows); SEL.to_csv(OUT/'n4_selected_gauge_summary.csv',index=False)
# summary from existing gauge scan + selected curves + triad
tri=pd.read_csv(OUT/'n4_triad_invariant_random.csv')
summary={
 'theta_deg':THETA,'N':len(POS),'A_min':AMIN,'odd_rms_min':math.sqrt(AMIN),'A_min_center_uv':UVC.tolist(),
 'published_origin_odd_fraction':odd_fraction(BASE),'published_origin_odd_rms':math.sqrt(odd_fraction(BASE)),
 'triad_chi1_ref':chi_ref,'triad_chi1_expected_sin3phi':float(math.sin(3*math.radians(J.DFT_TABLE['2H_MoSSe_Se-S-Se-S']['phi'][0]))),'triad_chi1_max_random_translation_error':float(tri.err.abs().max()),
 'tested_gauge_count':int(len(SCAN)),'eta1_Fp_gauge_spread':float(SCAN.Fp_eta1.max()-SCAN.Fp_eta1.min()),'eta1_Fm_gauge_spread':float(SCAN.Fm_eta1.max()-SCAN.Fm_eta1.min()),'eta1_Delta_gauge_spread':float(SCAN.Delta_eta1.max()-SCAN.Delta_eta1.min()),
 'tested_slope_fd_min':float(SCAN.slope_fd_005.min()),'tested_slope_fd_max':float(SCAN.slope_fd_005.max()),
 'selected_slope_min':float(SEL.slope.min()),'selected_slope_max':float(SEL.slope.max()),'selected_eta_opt_min':float(SEL.eta_opt_grid.min()),'selected_eta_opt_max':float(SEL.eta_opt_grid.max()),
 'max_sym_eta0_split':float(SEL.sym_eta0_split.abs().max()),'max_eta_reversal_contract_err':float(SEL.max_reversal_contract_err.max()),
 'decision':'eta continuation is gauge/origin dependent; retain only as gauge-fixed diagnostic, not material susceptibility or physical optimum'
}
(OUT/'n4_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
