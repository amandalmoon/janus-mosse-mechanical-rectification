from pathlib import Path
import json, math
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
B=Path('/mnt/data/janus_n2_gate')
fits=pd.read_csv(B/'n2_characteristic_powerlaw_fits.csv')
conv=pd.read_csv(B/'n2_alpha_convergence.csv')
char=pd.read_csv(B/'n2_characteristic_angles_exact.csv')
coll=pd.read_csv(B/'n2_original_hex_collapse_metrics.csv')
shape=pd.read_csv(B/'n2_extended_shape_dense_metrics.csv')
high=pd.read_csv(B/'n2_highTheta_prepared_validation.csv')
# correction sensitivity
corr=[]
for (d,q),g in char.groupby(['direction','q']):
    y=g.Theta_q.to_numpy()
    for form,x in [('1/sqrtN',1/np.sqrt(g.N.to_numpy())),('1/N',1/g.N.to_numpy())]:
        lr=linregress(x,y);pred=lr.intercept+lr.slope*x
        corr.append(dict(direction=d,q=q,form=form,Theta_inf=lr.intercept,c=lr.slope,R2=lr.rvalue**2,rmse=float(np.sqrt(np.mean((y-pred)**2)))))
pd.DataFrame(corr).to_csv(B/'n2_finite_size_correction_sensitivity.csv',index=False)
# plots
q90=conv[conv.q==.90]
fig,ax=plt.subplots(figsize=(6.4,4.2))
for d,g in q90.groupby('direction'):
    ax.plot(g.Nmin,g.alpha,marker='o',label=d)
ax.axhline(.5,linestyle='--',linewidth=1)
ax.set_xlabel('minimum contact size retained, $N_{min}$')
ax.set_ylabel(r'fitted $\alpha$ in $\theta_q\propto N^{-\alpha}$')
ax.legend();fig.tight_layout();fig.savefig(B/'N2_alpha_convergence.png',dpi=220);plt.close(fig)
fig,ax=plt.subplots(figsize=(6.4,4.2))
ax.plot(shape.Theta,100*shape.family_Fp_norm_reldiff,label='+y')
ax.plot(shape.Theta,100*shape.family_Fm_norm_reldiff,label='-y')
ax.set_xlabel(r'scaled twist $\Theta=\theta\sqrt{N}$ (deg)')
ax.set_ylabel('hexagon-disk family-mean difference (%)')
ax.legend();fig.tight_layout();fig.savefig(B/'N2_shape_family_difference.png',dpi=220);plt.close(fig)
fig,ax=plt.subplots(figsize=(6.4,4.2))
for d,g in char[char.q==.90].groupby('direction'):
    x=1/g.N.to_numpy(); y=g.Theta_q.to_numpy(); lr=linregress(x,y)
    ax.plot(x,y,'o',label=f'{d} data')
    xx=np.linspace(0,x.max(),200);ax.plot(xx,lr.intercept+lr.slope*xx,label=f'{d} 1/N fit')
ax.set_xlabel('$1/N$')
ax.set_ylabel(r'$\Theta_{0.90}=\theta_{0.90}\sqrt{N}$ (deg)')
ax.legend();fig.tight_layout();fig.savefig(B/'N2_scaled_characteristic_correction.png',dpi=220);plt.close(fig)
# corrected summary
summary={
 'gate':'PASS',
 'scope':'rigid compact self-similar contacts; hexagonal and disk-like families tested',
 'original_hex_N':[37,61,91,127,169,217,271,331,397,469],
 'collapse_metrics':coll.to_dict(orient='records'),
 'characteristic_alpha_range_all_sizes':[float(fits.alpha.min()),float(fits.alpha.max())],
 'characteristic_R2_min':float(fits.R2.min()),
 'q090_plus_alpha':float(fits[(fits.direction=='plus')&(fits.q==.90)].alpha.iloc[0]),
 'q090_minus_alpha':float(fits[(fits.direction=='minus')&(fits.q==.90)].alpha.iloc[0]),
 'q090_plus_alpha_Nmin217':float(conv[(conv.direction=='plus')&(conv.q==.90)&(conv.Nmin==217)].alpha.iloc[0]),
 'q090_minus_alpha_Nmin217':float(conv[(conv.direction=='minus')&(conv.q==.90)&(conv.Nmin==217)].alpha.iloc[0]),
 'alpha_range_Nmin217':[float(conv[conv.Nmin==217].alpha.min()),float(conv[conv.Nmin==217].alpha.max())],
 'max_characteristic_residual':float(char.res.max()),
 'min_characteristic_hard_mode':float(char.hard.min()),
 'extended_dense_Theta_range':[0,20],
 'extended_shape_max':{
  'hex_plus_within':float(shape.hex_Fp_norm_maxrel.max()),'hex_minus_within':float(shape.hex_Fm_norm_maxrel.max()),
  'disk_plus_within':float(shape.disk_Fp_norm_maxrel.max()),'disk_minus_within':float(shape.disk_Fm_norm_maxrel.max()),
  'hex_disk_plus_between':float(shape.family_Fp_norm_reldiff.max()),'hex_disk_minus_between':float(shape.family_Fm_norm_reldiff.max()),
  'hex_disk_rho_between':float(shape.family_rho_reldiff.max())},
 'prepared_highTheta_checks':{'n':int(len(high)),'all_pass':bool(high.pass_contract.all()),'min_zero_force_ground_gap':float(high.ground_gap.min()),'min_soft_mode_below_fold':float(high.min_soft_below.min())},
 'interpretation':'theta*sqrt(N) similarity with small finite-size corrections; 0.5036 is not a universal critical exponent'
}
(B/'n2_audit_summary_corrected.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
# report
report=f'''# N2 Finite-Size / Compact-Shape Robustness Gate\n\n## Decision\n**PASS within the rigid compact-contact model.**\n\nThe tested result is not a new universal exponent. The supported statement is that compact self-similar contacts exhibit an inverse-linear-size similarity controlled by `Theta = theta sqrt(N)`, with small finite-size corrections. The result has been checked for the original ten compact hexagons and independently for larger hexagonal and disk-like families.\n\n## 1. Canonical baseline\nAll calculations use the canonical unguided prepared-state contract: corrected 2H MoSSe three-shell GSFE, `k_perp=0`, and branch-followed depinning from the lowest-energy stable zero-force minimum.\n\n## 2. Original ten-hex dense collapse\nSizes: `N = 37, 61, 91, 127, 169, 217, 271, 331, 397, 469`. Each forward and reverse fold was continued on a dense scaled-twist grid `Theta=0..30` in unit increments.\n\n| scaled range | max rel. deviation +y | max rel. deviation -y | max rel. deviation rho |\n|---|---:|---:|---:|\n| Theta <= 18 | {100*coll.iloc[0].Fp_max_rel:.4f}% | {100*coll.iloc[0].Fm_max_rel:.4f}% | {coll.iloc[0].rho_max_rel:.3e} |\n| Theta <= 24 | {100*coll.iloc[1].Fp_max_rel:.4f}% | {100*coll.iloc[1].Fm_max_rel:.4f}% | {coll.iloc[1].rho_max_rel:.3e} |\n| Theta <= 30 | {100*coll.iloc[2].Fp_max_rel:.4f}% | {100*coll.iloc[2].Fm_max_rel:.4f}% | {coll.iloc[2].rho_max_rel:.3e} |\n\nThe worst deviations occur for the smallest contact, N=37, as expected for finite-size corrections.\n\n## 3. Exact characteristic-angle scaling\nFor `q = 0.95, 0.90, 0.85, 0.80`, each characteristic angle was solved directly from the full fold equations at fixed `F = q F_c(0)`, rather than interpolated from the dense curves. The largest nonlinear residual was `{char.res.max():.3e}` and the smallest hard Hessian mode was `{char.hard.min():.6f}`.\n\nAcross all eight direction/q fits,\n\n- alpha range (all ten sizes): `{fits.alpha.min():.9f}` to `{fits.alpha.max():.9f}`\n- minimum log-log R^2: `{fits.R2.min():.9f}`\n- q=0.90: alpha_plus = `{summary['q090_plus_alpha']:.9f}`, alpha_minus = `{summary['q090_minus_alpha']:.9f}`.\n\n### Removal of small contacts\nFor q=0.90, keeping only `N >= 217` gives\n\n- alpha_plus = `{summary['q090_plus_alpha_Nmin217']:.9f}`\n- alpha_minus = `{summary['q090_minus_alpha_Nmin217']:.9f}`.\n\nAcross all q and both directions with `N >= 217`, alpha lies between `{summary['alpha_range_Nmin217'][0]:.9f}` and `{summary['alpha_range_Nmin217'][1]:.9f}`. This monotonic approach toward 0.5 is the central reason to interpret the approximately 0.5036 full-range fit as a finite-size estimate of the expected 1/2 law, not as a distinct critical exponent.\n\nAn empirical `Theta_q = Theta_inf + c/N` sensitivity fit describes the ten-size correction extremely well (R^2 about 0.99996 for every q/direction), but no universal 1/N correction law is claimed without an analytic derivation.\n\n## 4. Extended compact-shape test on a dense scaled grid\nHexagons: `N=127..1261` (8 sizes). Disks: `N=127..931` (6 sizes). Unlike the earlier four-point check, this audit evaluates every integer `Theta` from 0 through 20.\n\nMaximum deviations over the whole dense interval:\n\n- hex within-family: +y `{100*summary['extended_shape_max']['hex_plus_within']:.4f}%`, -y `{100*summary['extended_shape_max']['hex_minus_within']:.4f}%`\n- disk within-family: +y `{100*summary['extended_shape_max']['disk_plus_within']:.4f}%`, -y `{100*summary['extended_shape_max']['disk_minus_within']:.4f}%`\n- hex-vs-disk family means: +y `{100*summary['extended_shape_max']['hex_disk_plus_between']:.4f}%`, -y `{100*summary['extended_shape_max']['hex_disk_minus_between']:.4f}%`\n- relative family difference in rho: `{summary['extended_shape_max']['hex_disk_rho_between']:.3e}`.\n\nAll maxima occur at Theta=20, so there is no hidden intermediate-Theta loss of collapse.\n\n## 5. Prepared-state validity beyond 3 degrees for the smallest contacts\nThe scaled interval Theta<=30 implies actual twists above 3 degrees for N=37, 61 and 91. These cannot be justified solely by the previous N=127 0-3 degree branch audit. We therefore independently enumerated stationary points and tested the dense-fold threshold immediately below and above the fold at N=37 (Theta=23,24,30), N=61 (24,30), and N=91 (24,30), in both force directions.\n\nAll `{len(high)}/{len(high)}` contracts passed: two zero-force stable minima are present, the lower-energy state remains separated from its competitor by at least `{high.ground_gap.min():.6f}`, at least one stable minimum remains immediately below the reported prepared threshold, and no stable minimum remains immediately above it. The minimum soft-mode curvature at the below-fold probe is `{high.min_soft_below.min():.6f}`. Thus the wide scaled-range collapse is not being generated by an unverified last-surviving branch for the small-N endpoints.\n\n## 6. Claim status\n### VERIFIED within model scope\n- forward and reverse threshold surfaces collapse under `Theta = theta sqrt(N)` for the tested compact hexagonal sequence;\n- exact characteristic angles scale approximately as `N^-1/2`;\n- the fitted exponent moves toward 1/2 when small contacts are removed;\n- larger compact hexagonal and disk-like families agree to about 0.1% through Theta=20;\n- the normalized directional split is even more size/shape invariant than the absolute thresholds;\n- small-N high-Theta endpoints remain prepared-state depinning thresholds in the tested checks.\n\n### NOT SUPPORTED / do not claim\n- a new universal critical exponent 0.5036;\n- shape independence for arbitrary compact geometries;\n- applicability to rotated/non-self-similar boundaries (handled separately in N3);\n- applicability to deformable or reconstructed contacts without the elasticity/atomistic robustness gates.\n\n## Recommended manuscript sentence\n> For compact self-similar rigid contacts, the forward and reverse prepared-state depinning surfaces are governed primarily by the scaled twist Theta = theta sqrt(N). Exact characteristic-angle fits over N=37-469 give alpha approximately 0.5036, while systematically excluding the smallest contacts drives alpha toward 1/2. Independent larger hexagonal and disk-like families agree at the approximately 0.1% level through Theta=20, supporting inverse-linear-size structure-factor similarity with finite-size corrections rather than a distinct universal exponent.\n'''
(B/'N2_FINITE_SIZE_SHAPE_GATE_REPORT.md').write_text(report,encoding='utf-8')
print(report)
