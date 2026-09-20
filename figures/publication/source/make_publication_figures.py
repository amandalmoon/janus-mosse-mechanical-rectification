from pathlib import Path
import sys, math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.lines import Line2D

ROOT = Path('/mnt/data/janus_n17_repro_release/Janus_MoSSe_Current_ReproducibilityRelease_v2')
OUT = Path('/mnt/data/janus_n18_publication_figures/figures')
OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
ns = {'__file__': str(ROOT/'audit_scripts'/'matched_symmetry_audit.py')}
code = (ROOT/'audit_scripts'/'matched_symmetry_audit.py').read_text().split('rows=[]')[0]
exec(code, ns)
centered, sym, inv = ns['centered'], ns['sym'], ns['inv']

# Cross-figure publication style. Local container has no literal Arial;
# the raster preview uses Arimo and editable SVG family declarations are patched to Arial.
BLUE = '#0072B2'
ORANGE = '#D55E00'
DARK = '#222222'
GRAY = '#777777'
LIGHT = '#D9D9D9'
PALE = '#EFEFEF'

plt.rcParams.update({
    'font.family': ['Arial', 'Arimo', 'Liberation Sans', 'sans-serif'],
    'font.size': 7.5,
    'axes.titlesize': 8.2,
    'axes.labelsize': 7.7,
    'legend.fontsize': 7.0,
    'xtick.labelsize': 7.0,
    'ytick.labelsize': 7.0,
    'axes.linewidth': 0.75,
    'lines.linewidth': 1.05,
    'lines.markersize': 3.6,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'svg.fonttype': 'none',
    'ps.fonttype': 42,
    'mathtext.fontset': 'dejavusans',
    'savefig.bbox': 'tight',
})


def panel(ax, label, x=-0.13, y=1.04):
    ax.text(x, y, f'({label})', transform=ax.transAxes, ha='left', va='top',
            fontweight='bold', fontsize=9.0, clip_on=False)


def finish_axes(ax):
    ax.tick_params(direction='out', length=2.5)


def patch_svg_font(path: Path):
    txt = path.read_text(encoding='utf-8')
    txt = txt.replace('Arimo', 'Arial').replace('Liberation Sans', 'Arial')
    path.write_text(txt, encoding='utf-8')


def save_all(fig, stem, dpi=600):
    svg = OUT/f'{stem}.svg'
    eps = OUT/f'{stem}.eps'
    tif = OUT/f'{stem}.tif'
    png = OUT/f'{stem}.png'
    fig.savefig(svg, format='svg', pad_inches=0.04)
    fig.savefig(eps, format='eps', pad_inches=0.04)
    fig.savefig(tif, format='tiff', dpi=dpi, pil_kwargs={'compression':'tiff_lzw'}, pad_inches=0.04)
    fig.savefig(png, format='png', dpi=dpi, pad_inches=0.04)
    plt.close(fig)
    patch_svg_font(svg)

# ---------- Figure 1 ----------
u = np.linspace(0, 1, 201)
v = np.linspace(0, 1, 201)
U, V = np.meshgrid(u, v, indexing='xy')
XY = np.stack([U + 0.5*V, (np.sqrt(3)/2)*V], axis=-1)
def gridpot(L): return L.potential(XY[...,0], XY[...,1])
Z1, Z2 = gridpot(centered), gridpot(sym)
vmax = max(np.max(np.abs(Z1)), np.max(np.abs(Z2)))
levels = np.linspace(-vmax, vmax, 25)
fig, axs = plt.subplots(2, 2, figsize=(7.0, 5.25054), constrained_layout=True)
ims = []
for ax, Z, title, lab in [
    (axs[0,0], Z1, 'Centered asymmetric 2H GSFE', 'a'),
    (axs[0,1], Z2, 'Matched same-2H symmetrized GSFE', 'b')]:
    im = ax.contourf(U, V, Z, levels=levels, cmap='RdBu_r', extend='both')
    ims.append(im)
    ax.set_xlabel(r'$u$ along $\mathbf{a}_1$')
    ax.set_ylabel(r'$v$ along $\mathbf{a}_2$')
    ax.set_title(title)
    panel(ax, lab, x=-0.16, y=1.04)
    finish_axes(ax)
# one shared scale for direct comparison
cb = fig.colorbar(ims[0], ax=[axs[0,0], axs[0,1]], fraction=.035, pad=.025)
cb.set_label(r'$U/E_0$')

ad = pd.read_csv(ROOT/'data'/'canonical'/'asymmetry_global_check.csv')
labels = ['3R asym.', '3R sym. I', '3R sym. II', '2H asym.']
vals = ad['rms'].values
ax = axs[1,0]
x = np.arange(4)
ax.bar(x, vals, color=[GRAY, LIGHT, LIGHT, BLUE], edgecolor=DARK, linewidth=.6)
ax.set_yscale('symlog', linthresh=1e-16)
ax.set_ylim(-1e-17, .3)
ax.set_xticks(x, labels, rotation=12)
ax.set_ylabel('translation-minimized odd RMS fraction')
ax.set_title('Coordinate-invariant registry asymmetry')
panel(ax, 'c'); finish_axes(ax)

md = pd.read_csv(ROOT/'data'/'canonical'/'matched_symmetry_final.csv')
G = md[md.min_id.astype(str) == 'GLOBAL']
order = ['2H_centered','2H_matched_symmetrized','2H_exact_inverted']
names = ['original','matched sym.','exact inversion']
idx = np.arange(3); width = .34
ax = axs[1,1]
gp = G.set_index('landscape').loc[order]
ax.bar(idx-width/2, gp.Fc_plus, width, color=BLUE, label=r'$F_{c,+}$')
ax.bar(idx+width/2, gp.Fc_minus, width, color=ORANGE, label=r'$F_{c,-}$')
ax.set_xticks(idx, names)
ax.set_ylabel(r'branch/global threshold $F_c^*$')
ax.set_title(r'Matched symmetry contract at $\theta=1.5^\circ$')
ax.legend(frameon=False, ncol=2, loc='upper center')
panel(ax, 'd'); finish_axes(ax)
for j, k in enumerate(order):
    r = gp.loc[k]
    ax.text(j, max(r.Fc_plus, r.Fc_minus)+.08,
            f'({int(r.m_round)},{int(r.n_round)})', ha='center', va='bottom', fontsize=7.0)
save_all(fig, 'Figure_1_symmetry_contracts')

# ---------- Figure 2 ----------
fd = pd.read_csv(ROOT/'data'/'canonical'/'free_fold_nondegeneracy.csv')
fd = fd[fd.theta <= 3.000001]
bs = pd.read_csv(ROOT/'data'/'canonical'/'branch_family_summary.csv')
fig, axs = plt.subplots(2, 2, figsize=(7.0, 4.85979), constrained_layout=True)
ax = axs[0,0]
ax.plot(fd.theta, fd.Ff, color=BLUE, label='ground-state branch')
pp = bs[bs.sign == 1]
ax.plot(pp.theta, pp.Fc_meta, 'o--', color=GRAY, ms=3.0, label='metastable branch')
ax.set(xlabel=r'twist $\theta$ (deg)', ylabel=r'$F_{c,+}^*$', title='Positive-y branch-followed depinning')
ax.set_ylim(0, 3.6)
ax.legend(frameon=False); panel(ax,'a'); finish_axes(ax)

ax = axs[0,1]
ax.plot(fd.theta, fd.Fr, color=ORANGE, label='ground-state branch')
pp = bs[bs.sign == -1]
ax.plot(pp.theta, pp.Fc_meta, 'o--', color=GRAY, ms=3.0, label='metastable branch')
ax.set(xlabel=r'twist $\theta$ (deg)', ylabel=r'$F_{c,-}^*$', title='Negative-y branch-followed depinning')
ax.set_ylim(0, 3.6)
ax.legend(frameon=False); panel(ax,'b'); finish_axes(ax)

pe = bs[bs.sign == 1]
ax = axs[1,0]
ax.plot(pe.theta, pe.U_ground, color=BLUE, label='ground minimum')
ax.plot(pe.theta, pe.U_meta, color=GRAY, ls='--', label='metastable minimum')
ax.set(xlabel=r'twist $\theta$ (deg)', ylabel=r'zero-force energy $U^*$', title='Prepared ground state remains lowest')
ax.legend(frameon=False); panel(ax,'c'); finish_axes(ax)

ax = axs[1,1]
pplus = bs[bs.sign == 1]; pminus = bs[bs.sign == -1]
ax.plot(pplus.theta, pplus.Fc_ground-pplus.Fc_meta, color=BLUE, label='+y')
ax.plot(pminus.theta, pminus.Fc_ground-pminus.Fc_meta, color=ORANGE, ls='--', label='-y')
ax.axhline(0, color=GRAY, lw=.7)
ax.set(xlabel=r'twist $\theta$ (deg)', ylabel=r'$F_c^{ground}-F_c^{meta}$', title='Prepared ground branch survives longer')
ax.legend(frameon=False); panel(ax,'d'); finish_axes(ax)
save_all(fig, 'Figure_2_branch_resolved_depinning')

# ---------- Figure 3 ----------
ss = pd.read_csv(ROOT/'data'/'canonical'/'shape_scaling_extended.csv')
sm = pd.read_csv(ROOT/'data'/'canonical'/'shape_scaling_metrics.csv')
fig, axs = plt.subplots(2, 2, figsize=(7.0, 4.85979), constrained_layout=True)
for family, ax, lab, title in [
    ('hex', axs[0,0], 'a', 'Compact hexagons: extended size collapse'),
    ('disk', axs[0,1], 'b', 'Disk-like compact contacts: collapse')]:
    sub = ss[ss.family == family]
    for N, g in sub.groupby('N'):
        ax.plot(g.Theta, g.Fp_norm, color=BLUE, alpha=.42, lw=.9)
        ax.plot(g.Theta, g.Fm_norm, color=ORANGE, alpha=.42, lw=.9, ls='--')
    ax.set(xlabel=r'scaled twist $\Theta=\theta\sqrt{N}$ (deg)', ylabel=r'$F_c(\Theta)/F_c(0)$', title=title)
    ax.set_ylim(.81, 1.01)
    panel(ax, lab); finish_axes(ax)
    if family == 'hex':
        handles = [Line2D([0],[0], color=BLUE, lw=1.2, label='+y'),
                   Line2D([0],[0], color=ORANGE, lw=1.2, ls='--', label='-y')]
        ax.legend(handles=handles, frameon=False, loc='lower left')

ax = axs[1,0]
for scope, marker in [('hex','o'),('disk','s')]:
    q = sm[sm.scope == scope]
    ax.plot(q.Theta, 100*q.Fp_max_rel, color=BLUE, marker=marker, label=f'{scope} +y')
    ax.plot(q.Theta, 100*q.Fm_max_rel, color=ORANGE, marker=marker, ls='--', label=f'{scope} -y')
ax.set(xlabel=r'$\Theta$', ylabel='max cross-size deviation (%)', title='Collapse error remains sub-percent')
ax.set_ylim(-.002, .09)
ax.legend(frameon=False, ncol=2); panel(ax,'c'); finish_axes(ax)

ax = axs[1,1]
q = sm[sm.scope == 'hex_vs_disk']
ax.plot(q.Theta, 100*np.abs(q.Fp_mean), color=BLUE, marker='o', label='+y')
ax.plot(q.Theta, 100*np.abs(q.Fm_mean), color=ORANGE, marker='s', ls='--', label='-y')
ax.set(xlabel=r'$\Theta$', ylabel='hex-vs-disk mean difference (%)', title='Compact-shape family means nearly coincide')
ax.set_ylim(-.002, .09)
ax.legend(frameon=False); panel(ax,'d'); finish_axes(ax)
save_all(fig, 'Figure_3_extended_size_shape_similarity')

# ---------- Figure 4 ----------
tr = pd.read_csv(ROOT/'data'/'canonical'/'triangle_ground_switch.csv')
ew = pd.read_csv(ROOT/'data'/'canonical'/'edge_weight_ground_switch.csv')
fig, axs = plt.subplots(2, 2, figsize=(7.0, 4.85979), constrained_layout=True)
styles = [(20, BLUE, 'o'), (25, ORANGE, 's')]
ax = axs[0,0]
for phi, color, marker in styles:
    q = tr[tr.phi == phi]
    ax.plot(q.theta, q.UB-q.UA, marker=marker, ms=3, color=color, label=fr'$\phi_e={phi}^\circ$')
    ax.axvline(q.energy_switch.iloc[0], color=color, ls=':', lw=.8)
ax.axhline(0, color=GRAY, lw=.7)
ax.set(xlabel=r'twist $\theta$ (deg)', ylabel=r'$U_B-U_A$', title='Competing zero-force registry minima')
ax.legend(frameon=False); panel(ax,'a'); finish_axes(ax)

ax = axs[0,1]
for phi, color, marker in styles:
    q = tr[tr.phi == phi]
    ax.plot(q.theta, q.FAplus-q.FAminus, marker='o', ls='--', ms=2.6, color=color, alpha=.72)
    ax.plot(q.theta, q.FBplus-q.FBminus, marker='s', ls='-', ms=2.6, color=color)
ax.axhline(0, color=GRAY, lw=.7)
ax.set(xlabel=r'$\theta$ (deg)', ylabel=r'branch split $\Delta F_c^*$', title='Registry families carry opposite bias')
legend_handles = [
    Line2D([0],[0], color=BLUE, marker='o', lw=1, label=r'$\phi_e=20^\circ$'),
    Line2D([0],[0], color=ORANGE, marker='s', lw=1, label=r'$\phi_e=25^\circ$'),
    Line2D([0],[0], color=DARK, marker='o', ls='--', lw=1, label='family A'),
    Line2D([0],[0], color=DARK, marker='s', ls='-', lw=1, label='family B')]
ax.legend(handles=legend_handles, frameon=False, loc='center', ncol=2, columnspacing=1.2, handlelength=1.8)
panel(ax,'b'); finish_axes(ax)

ax = axs[1,0]
for phi, color, marker in styles:
    q = tr[tr.phi == phi]
    sw = q.energy_switch.iloc[0]
    q1 = q[q.theta < sw]; q2 = q[q.theta >= sw]
    ax.plot(q1.theta, q1.ground_delta, marker='o', ms=3, color=color)
    ax.plot(q2.theta, q2.ground_delta, marker='s', ms=3, color=color, label=fr'$\phi_e={phi}^\circ$')
    ax.axvline(sw, color=color, ls=':', lw=.8)
ax.axhline(0, color=GRAY, lw=.7)
ax.set(xlabel=r'$\theta$ (deg)', ylabel=r'prepared ground-state $\Delta F_c^*$', title='Prepared sign across equilibrium registry crossing')
ax.legend(frameon=False); panel(ax,'c'); finish_axes(ax)

ax = axs[1,1]
for phi, color, marker in styles:
    q = ew[ew.phi == phi]
    ax.plot(q.edge_weight, q.ground_switch_deg, marker=marker, color=color, label=fr'$\phi_e={phi}^\circ$')
ax.axhline(3, color=GRAY, ls=':', lw=.7)
ax.set(xlabel='outer-site energy weight', ylabel='equilibrium switch twist (deg)', title='Switch location is edge-model sensitive')
ax.legend(frameon=False); panel(ax,'d'); finish_axes(ax)
save_all(fig, 'Figure_4_boundary_registry_switching')

# ---------- Figure 5 ----------
vm = pd.read_csv(ROOT/'data'/'canonical'/'vector_mode_map_F0_period.csv')
fl = pd.read_csv(ROOT/'data'/'canonical'/'floquet_conditioning_check.csv')
Fvals = sorted(vm.F0.unique()); Pvals = sorted(vm.period.unique())
def pivot(col): return vm.pivot(index='period', columns='F0', values=col).loc[Pvals, Fvals].values

fig = plt.figure(figsize=(7.0, 4.86129), constrained_layout=True)
gs = fig.add_gridspec(2, 2)
ax_a = fig.add_subplot(gs[0,0])
ax_b = fig.add_subplot(gs[0,1])
ax_c = fig.add_subplot(gs[1,0])
gsd = gs[1,1].subgridspec(2,1, hspace=0.08)
ax_d1 = fig.add_subplot(gsd[0,0])
ax_d2 = fig.add_subplot(gsd[1,0], sharex=ax_d1)

for ax, Z, title, lab, cmap_name, vmin_i, vmax_i in [
    (ax_a, pivot('m'), r'Winding $m$ along $\mathbf{a}_1$', 'a', 'viridis', 0, 10),
    (ax_b, pivot('n'), r'Winding $n$ along $\mathbf{a}_2$', 'b', 'cividis', -9, 0)]:
    boundaries = np.arange(vmin_i-0.5, vmax_i+1.5, 1)
    cmap = plt.get_cmap(cmap_name, len(boundaries)-1)
    norm = BoundaryNorm(boundaries, cmap.N)
    im = ax.imshow(Z, origin='lower', aspect='auto',
                   extent=[min(Fvals)-.125, max(Fvals)+.125, min(Pvals)-5, max(Pvals)+5],
                   cmap=cmap, norm=norm, interpolation='nearest')
    ax.set(xlabel=r'rocking amplitude $F_0^*$', ylabel=r'period $\tau^*$', title=title)
    cb = fig.colorbar(im, ax=ax, fraction=.046, pad=.025, ticks=np.arange(vmin_i, vmax_i+1, 1))
    cb.ax.tick_params(labelsize=7.0)
    panel(ax, lab); finish_axes(ax)

q = vm[vm.period == 40]
ax_c.step(q.F0, q.m, where='mid', color=BLUE, label='m')
ax_c.step(q.F0, q.n, where='mid', color=ORANGE, ls='--', label='n')
ax_c.set(xlabel=r'$F_0^*$ at $\tau^*=40$', ylabel='lattice winding / cycle', title='Representative vector staircase')
ax_c.legend(frameon=False); panel(ax_c,'c'); finish_axes(ax_c)

methods = ["DOP853\n1e-9", "DOP853\n1e-11", "Radau\n1e-9"]
ref = float(fl.rho.iloc[1])
ppm = (fl.rho/ref - 1)*1e6
xx = np.arange(len(fl))
ax_d1.plot(xx, ppm, 'o-', color=BLUE)
ax_d1.axhline(0, color=GRAY, ls=':', lw=.7)
ax_d1.set_ylabel(r'$\rho_F$ rel. dev. (ppm)')
ax_d1.set_title('Floquet cross-solver consistency')
ax_d1.text(.98, .90, r'$\rho_F\approx6.31\times10^{-22}$', transform=ax_d1.transAxes,
           ha='right', va='top', fontsize=7.0)
panel(ax_d1, 'd', x=-0.13, y=1.12)
finish_axes(ax_d1)
plt.setp(ax_d1.get_xticklabels(), visible=False)

ax_d2.plot(xx, fl.closure*1e11, 's--', color=ORANGE)
ax_d2.set_ylabel(r'closure ($10^{-11}$)')
ax_d2.set_xticks(xx, methods)
finish_axes(ax_d2)
# tighten mini-panel label hierarchy
for ax in [ax_d1, ax_d2]:
    ax.tick_params(axis='x', labelsize=7.0)
    ax.tick_params(axis='y', labelsize=7.0)
save_all(fig, 'Figure_5_vector_mode_map_floquet')

# ---------- Figure 6 ----------
full = pd.read_csv(ROOT/'data'/'canonical'/'thermal_stationary_series_N500.csv')
pooled = pd.read_csv(ROOT/'data'/'canonical'/'stationary_current_two_seed_pooled.csv')
pooled = pooled[pooled['seed'].astype(str) == 'pooled'].copy()
boot = pd.read_csv(ROOT/'data'/'canonical'/'stationary_thermal_bootstrap_50k.csv')
sign = pd.read_csv(ROOT/'data'/'canonical'/'stationary_sign_target_bootstrap.csv')
low = full[full['T'] < 0.5].copy()
high = pooled.merge(boot[['T','u_ci_lo','u_ci_hi','v_ci_lo','v_ci_hi']], on='T', how='left')
comp_T = np.concatenate([low['T'].to_numpy(), high['T'].to_numpy()])
comp_u = np.concatenate([low['mean_u'].to_numpy(), high['mean_u'].to_numpy()])
comp_v = np.concatenate([low['mean_v'].to_numpy(), high['mean_v'].to_numpy()])
comp_u_lo = np.concatenate([low['u_ci_lo'].to_numpy(), high['u_ci_lo'].to_numpy()])
comp_u_hi = np.concatenate([low['u_ci_hi'].to_numpy(), high['u_ci_hi'].to_numpy()])
comp_v_lo = np.concatenate([low['v_ci_lo'].to_numpy(), high['v_ci_lo'].to_numpy()])
comp_v_hi = np.concatenate([low['v_ci_hi'].to_numpy(), high['v_ci_hi'].to_numpy()])
prob_T = np.concatenate([low['T'].to_numpy(), sign['T'].to_numpy()])
prob_neg = np.concatenate([low['P_v_negative_cycle'].to_numpy(), sign['Pneg'].to_numpy()])
prob_target = np.concatenate([low['P_target_cycle'].to_numpy(), sign['Ptarget'].to_numpy()])

fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.32232), constrained_layout=True)
ax = axes[0]
yerr_u = np.vstack([comp_u-comp_u_lo, comp_u_hi-comp_u])
yerr_v = np.vstack([comp_v-comp_v_lo, comp_v_hi-comp_v])
ax.errorbar(comp_T, comp_u, yerr=yerr_u, marker='o', linestyle='-', capsize=1.7, color=BLUE, label=r'$\langle u\rangle$')
ax.errorbar(comp_T, comp_v, yerr=yerr_v, marker='s', linestyle='--', capsize=1.7, color=ORANGE, label=r'$\langle v\rangle$')
ax.axhline(0, color=GRAY, lw=.7, ls=':')
ax.set_xlabel(r'$T^{*}$'); ax.set_ylabel('mean lattice displacement / cycle')
ax.legend(frameon=False, loc='best', handlelength=2.0)
panel(ax,'a',x=-.14,y=1.04); finish_axes(ax)

ax = axes[1]
ratio = pooled['T2'].to_numpy()/pooled['crit'].to_numpy()
ax.plot(pooled['T'], ratio, marker='o', linestyle='-', color=BLUE)
ax.axhline(1.0, color=GRAY, lw=.8, ls=':')
ax.set_xlabel(r'$T^{*}$'); ax.set_ylabel(r'$T_H^2/T_{0.95}^2$')
ax.set_xlim(.49,.71); ax.set_ylim(0, max(ratio)*1.08)
ax.text(.50, .08, 'zero-current rejection threshold', transform=ax.transAxes,
        ha='center', va='bottom', fontsize=7.0)
panel(ax,'b',x=-.14,y=1.04); finish_axes(ax)

ax = axes[2]
ax.plot(prob_T, prob_neg, marker='o', linestyle='-', color=BLUE, label=r'$P(v_{cycle}<0)$')
ax.plot(prob_T, prob_target, marker='s', linestyle='--', color=ORANGE, label=r'$P[(m,n)=(1,-1)]$')
ax.axhline(.5, color=GRAY, lw=.7, ls=':')
ax.set_xlabel(r'$T^{*}$'); ax.set_ylabel('probability'); ax.set_ylim(-.02,1.04)
ax.legend(frameon=False, loc='best', handlelength=2.0)
panel(ax,'c',x=-.14,y=1.04); finish_axes(ax)
save_all(fig, 'Figure_6_thermal_stationary_hierarchy')

print('WROTE', OUT)
