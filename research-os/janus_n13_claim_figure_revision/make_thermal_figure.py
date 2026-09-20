import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image

ROOT = Path('/mnt/data/janus_redteam_gate/rtb01')
OUT = Path('/mnt/data/janus_n13_claim_figure_revision')

full = pd.read_csv(ROOT/'thermal_stationary_series_N500.csv')
pooled = pd.read_csv(ROOT/'stationary_current_two_seed_pooled.csv')
pooled = pooled[pooled['seed'].astype(str) == 'pooled'].copy()
boot = pd.read_csv(ROOT/'stationary_thermal_bootstrap_50k.csv')
sign = pd.read_csv(ROOT/'stationary_sign_target_bootstrap.csv')

# Composite series: full-grid N=500 for low T, pooled two-seed N=1000 for high T.
low = full[full['T'] < 0.5].copy()
high = pooled.merge(boot[['T','u_ci_lo','u_ci_hi','v_ci_lo','v_ci_hi']], on='T', how='left')
comp_T = np.concatenate([low['T'].to_numpy(), high['T'].to_numpy()])
comp_u = np.concatenate([low['mean_u'].to_numpy(), high['mean_u'].to_numpy()])
comp_v = np.concatenate([low['mean_v'].to_numpy(), high['mean_v'].to_numpy()])
comp_u_lo = np.concatenate([low['u_ci_lo'].to_numpy(), high['u_ci_lo'].to_numpy()])
comp_u_hi = np.concatenate([low['u_ci_hi'].to_numpy(), high['u_ci_hi'].to_numpy()])
comp_v_lo = np.concatenate([low['v_ci_lo'].to_numpy(), high['v_ci_lo'].to_numpy()])
comp_v_hi = np.concatenate([low['v_ci_hi'].to_numpy(), high['v_ci_hi'].to_numpy()])

# Probabilities: full-grid N=500 at low T; pooled high-T stationary bootstrap at high T.
prob_T = np.concatenate([low['T'].to_numpy(), sign['T'].to_numpy()])
prob_neg = np.concatenate([low['P_v_negative_cycle'].to_numpy(), sign['Pneg'].to_numpy()])
prob_target = np.concatenate([low['P_target_cycle'].to_numpy(), sign['Ptarget'].to_numpy()])

# ACS Nano working graphics settings. Local environment lacks literal Arial; Arimo is a metric-compatible stand-in.
plt.rcParams.update({
    'font.family': ['Arial', 'Arimo', 'Liberation Sans', 'sans-serif'],
    'font.size': 7.0,
    'axes.titlesize': 8.0,
    'axes.labelsize': 7.5,
    'xtick.labelsize': 6.5,
    'ytick.labelsize': 6.5,
    'legend.fontsize': 6.3,
    'axes.linewidth': 0.7,
    'lines.linewidth': 1.0,
    'lines.markersize': 3.8,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'svg.fonttype': 'none',
    'ps.fonttype': 42,
})

# Match the existing manuscript aspect ratio so package-level image replacement is distortion-free.
aspect = 3813/1265
width = 7.0
height = width/aspect
fig, axes = plt.subplots(1, 3, figsize=(width, height), constrained_layout=True)

# (a) component means with trajectory-level 95% intervals
ax = axes[0]
yerr_u = np.vstack([comp_u-comp_u_lo, comp_u_hi-comp_u])
yerr_v = np.vstack([comp_v-comp_v_lo, comp_v_hi-comp_v])
ax.errorbar(comp_T, comp_u, yerr=yerr_u, marker='o', linestyle='-', capsize=1.6, label=r'$\langle u\rangle$')
ax.errorbar(comp_T, comp_v, yerr=yerr_v, marker='s', linestyle='--', capsize=1.6, label=r'$\langle v\rangle$')
ax.axhline(0, lw=0.7, ls=':')
ax.set_xlabel(r'$T^{*}$')
ax.set_ylabel('mean lattice displacement / cycle')
ax.legend(frameon=False, loc='best', handlelength=2.0)
ax.text(0.015, 0.97, '(a)', transform=ax.transAxes, va='top', ha='left', fontsize=8.5, fontweight='bold')

# (b) high-T joint zero-current test; ratio > 1 excludes zero vector under the declared test.
ax = axes[1]
ratio = pooled['T2'].to_numpy()/pooled['crit'].to_numpy()
ax.plot(pooled['T'], ratio, marker='o', linestyle='-')
ax.axhline(1.0, lw=0.8, ls=':')
ax.set_xlabel(r'$T^{*}$')
ax.set_ylabel(r'$T_H^2/T_{0.95}^2$')
ax.set_xlim(0.49,0.71)
ax.set_ylim(0, max(ratio)*1.08)
ax.text(0.015, 0.97, '(b)', transform=ax.transAxes, va='top', ha='left', fontsize=8.5, fontweight='bold')
ax.text(0.50, 0.08, 'zero-current rejection threshold', transform=ax.transAxes, ha='center', va='bottom', fontsize=6.2)

# (c) cycle direction vs exact deterministic winding identity
ax = axes[2]
ax.plot(prob_T, prob_neg, marker='o', linestyle='-', label=r'$P(v_{\rm cycle}<0)$')
ax.plot(prob_T, prob_target, marker='s', linestyle='--', label=r'$P[(m,n)=(1,-1)]$')
ax.axhline(0.5, lw=0.7, ls=':')
ax.set_xlabel(r'$T^{*}$')
ax.set_ylabel('probability')
ax.set_ylim(-0.02,1.04)
ax.legend(frameon=False, loc='best', handlelength=2.0)
ax.text(0.015, 0.97, '(c)', transform=ax.transAxes, va='top', ha='left', fontsize=8.5, fontweight='bold')

for ax in axes:
    ax.tick_params(direction='out', length=2.5)

# Canonical editable/vector output.
svg = OUT/'Figure_6_thermal_stationary_hierarchy.svg'
eps = OUT/'Figure_6_thermal_stationary_hierarchy.eps'
png_hi = OUT/'Figure_6_thermal_stationary_hierarchy_hi.png'
tif = OUT/'Figure_6_thermal_stationary_hierarchy.tif'
fig.savefig(svg, format='svg')
fig.savefig(eps, format='eps')
fig.savefig(png_hi, format='png', dpi=600)
fig.savefig(tif, format='tiff', dpi=600, pil_kwargs={'compression':'tiff_lzw'})
plt.close(fig)

# For current DOCX, keep exact legacy pixel geometry to avoid distortion in package-level replacement.
img = Image.open(png_hi).convert('RGB')
img = img.resize((3813,1265), Image.Resampling.LANCZOS)
png_docx = OUT/'Figure_6_thermal_stationary_hierarchy.png'
img.save(png_docx, dpi=(600,600), optimize=True)

# Editable SVG declares Arial for final venue export; local raster preview uses Arimo fallback.
text = svg.read_text(encoding='utf-8')
text = text.replace('Arimo', 'Arial').replace('Liberation Sans', 'Arial')
svg.write_text(text, encoding='utf-8')

# Data used for the figure.
pd.DataFrame({
    'T': comp_T, 'mean_u': comp_u, 'u_ci_lo':comp_u_lo, 'u_ci_hi':comp_u_hi,
    'mean_v':comp_v, 'v_ci_lo':comp_v_lo, 'v_ci_hi':comp_v_hi,
    'source': ['N500_stationary']*len(low)+['N1000_pooled_two_seed']*len(high)
}).to_csv(OUT/'Figure_6_panel_a_data.csv', index=False)
pd.DataFrame({'T':pooled['T'], 'hotelling_T2':pooled['T2'], 'crit95':pooled['crit'], 'ratio':ratio}).to_csv(OUT/'Figure_6_panel_b_data.csv', index=False)
pd.DataFrame({'T':prob_T,'P_vcycle_negative':prob_neg,'P_target_winding':prob_target,
              'source':['N500_stationary']*len(low)+['N1000_pooled_two_seed']*len(sign)}).to_csv(OUT/'Figure_6_panel_c_data.csv', index=False)
print('created', png_docx)
