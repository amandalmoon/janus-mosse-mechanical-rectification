from __future__ import annotations
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(os.environ['N22R_RELEASE_ROOT'])
OUT = Path(os.environ['N22R_OUT'])
STYLE = Path(__file__).with_name('publication_n22r.mplstyle')
VECTOR_EXPORTS = ('.pdf', '.svg', '.eps')  # explicit publication export contract
plt.style.use(STYLE)
plt.rcParams.update({
    'font.size': 8.0,
    'axes.labelsize': 8.2,
    'axes.titlesize': 8.2,
    'xtick.labelsize': 7.3,
    'ytick.labelsize': 7.3,
    'legend.fontsize': 7.0,
    'axes.linewidth': 0.65,
    'lines.linewidth': 1.2,
    'lines.markersize': 3.7,
    'legend.frameon': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'svg.fonttype': 'none',
    'savefig.bbox': None,
    'savefig.pad_inches': 0,
})

FONT_FAMILY = os.environ.get('N22R_FONT_FAMILY', 'Arial')
plt.rcParams['font.family'] = FONT_FAMILY
if FONT_FAMILY.lower() == 'arial':
    plt.rcParams['font.sans-serif'] = ['Arial']

BLUE = '#0072B2'
VERM = '#D55E00'
DARK = '#222222'
MID = '#6F6F6F'
LIGHT = '#C8C8C8'
GRID = '#D8D8D8'
PALE_GREEN = '#E2F2EC'
PALE_BLUE = '#DDECF4'
MM = 25.4

def inch(mm: float) -> float:
    return mm / MM

def panel_label(ax, letter: str, x=-0.10, y=1.035):
    ax.text(x, y, f'({letter})', transform=ax.transAxes, ha='left', va='bottom',
            fontsize=9.2, fontweight='bold', color=DARK, clip_on=False)

def panel_title(ax, title: str, x=0.0):
    ax.text(x, 1.015, title, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=8.2, color=DARK)

def finish(ax):
    ax.tick_params(direction='out', length=2.5, width=0.6, pad=2.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(DARK)
    ax.spines['bottom'].set_color(DARK)

fd = pd.read_csv(ROOT / 'data' / 'canonical' / 'free_fold_nondegeneracy.csv')
fd = fd[fd.theta <= 3.000001].copy()
bs = pd.read_csv(ROOT / 'data' / 'canonical' / 'branch_family_summary.csv').copy()
ho = pd.read_csv(ROOT / 'data' / 'canonical' / 'free_cusp_like_point.csv').iloc[0]

p = bs[bs.sign == 1].copy()
n = bs[bs.sign == -1].copy()

fig = plt.figure(figsize=(inch(177.8), inch(116.0)))
gs = fig.add_gridspec(2, 2, left=0.075, right=0.975, bottom=0.095, top=0.955,
                      wspace=0.25, hspace=0.39, height_ratios=[1.02, 0.98])
a = fig.add_subplot(gs[0,0])
b = fig.add_subplot(gs[0,1], sharey=a)
c = fig.add_subplot(gs[1,0])
d = fig.add_subplot(gs[1,1])

# Panel A: +y branch-followed thresholds.
a.plot(fd.theta, fd.Ff, color=BLUE, lw=1.55, solid_capstyle='round', zorder=3)
a.plot(p.theta, p.Fc_meta, color=BLUE, lw=1.0, ls='--', marker='o', ms=3.8,
       mfc='white', mec=BLUE, mew=0.8, zorder=4)
a.axvline(1.5, color=LIGHT, lw=0.7, ls=':', zorder=0)
a.set_xlim(0, 3); a.set_ylim(0, 3.65)
a.set_xlabel(r'twist $\theta$ (deg)')
a.set_ylabel(r'branch-followed threshold $F_c^*$')
a.text(0.04, 0.91, 'ground', transform=a.transAxes, color=BLUE, fontsize=7.0,
       ha='left', va='top')
a.text(0.04, 0.17, 'metastable', transform=a.transAxes, color=BLUE, fontsize=7.0,
       ha='left', va='top')
a.text(1.5, 3.28, r'$\theta=1.5^\circ$', ha='center', va='bottom', fontsize=6.8, color=MID)
fref = float(np.interp(1.5, fd.theta.to_numpy(), fd.Ff.to_numpy()))
a.plot([1.5], [fref], marker='o', ms=4.2, mfc=BLUE, mec='white', mew=0.7, zorder=6)
a.text(0.97, 0.06, fr'$F_{{c,+}}^*={fref:.3f}$ at $1.5^\circ$',
       transform=a.transAxes, ha='right', va='bottom', fontsize=6.6, color=MID)
# Independent nondegeneracy audit: isolated higher-order point on the +y ground branch.
a.plot(float(ho.theta_deg), float(ho.F_star), marker='D', ms=4.4, color=DARK, zorder=7)
a.text(float(ho.theta_deg)-0.03, float(ho.F_star)-0.16, 'higher-order\npoint',
       ha='right', va='top', fontsize=6.4, color=DARK)
panel_label(a, 'a'); panel_title(a, r'$+y$ prepared-state depinning'); finish(a)

# Panel B: -y branch-followed thresholds.
b.plot(fd.theta, fd.Fr, color=VERM, lw=1.55, solid_capstyle='round', zorder=3)
b.plot(n.theta, n.Fc_meta, color=VERM, lw=1.0, ls='--', marker='s', ms=3.6,
       mfc='white', mec=VERM, mew=0.8, zorder=4)
b.axvline(1.5, color=LIGHT, lw=0.7, ls=':', zorder=0)
b.set_xlim(0, 3)
b.set_xlabel(r'twist $\theta$ (deg)')
b.tick_params(labelleft=False)
b.text(0.04, 0.46, 'ground', transform=b.transAxes, color=VERM, fontsize=7.0,
       ha='left', va='top')
b.text(0.04, 0.21, 'metastable', transform=b.transAxes, color=VERM, fontsize=7.0,
       ha='left', va='top')
rref = float(np.interp(1.5, fd.theta.to_numpy(), fd.Fr.to_numpy()))
b.plot([1.5], [rref], marker='s', ms=4.0, mfc=VERM, mec='white', mew=0.7, zorder=6)
b.text(0.97, 0.06, fr'$F_{{c,-}}^*={rref:.3f}$ at $1.5^\circ$',
       transform=b.transAxes, ha='right', va='bottom', fontsize=6.6, color=MID)
panel_label(b, 'b'); panel_title(b, r'$-y$ prepared-state depinning'); finish(b)

# Panel C: zero-force preparation energy margin.
margin_u = p.U_meta.to_numpy(float) - p.U_ground.to_numpy(float)
c.fill_between(p.theta, 0, margin_u, color=PALE_GREEN, linewidth=0, zorder=0)
c.plot(p.theta, margin_u, color=DARK, lw=1.25, marker='o', ms=3.4,
       mfc='white', mec=DARK, mew=0.7, zorder=3)
c.axhline(0, color=LIGHT, lw=0.7, zorder=0)
c.axvline(1.5, color=LIGHT, lw=0.7, ls=':', zorder=0)
c.set_xlim(0,3); c.set_ylim(0, max(margin_u)*1.13)
c.set_xlabel(r'twist $\theta$ (deg)')
c.set_ylabel(r'$U_{\mathrm{meta}}-U_{\mathrm{ground}}$')
imin = int(np.argmin(margin_u))
c.annotate(f'minimum margin = {margin_u[imin]:.3f}',
           xy=(float(p.theta.iloc[imin]), float(margin_u[imin])), xytext=(-5, 18),
           textcoords='offset points', ha='right', va='bottom', fontsize=6.8, color=DARK,
           arrowprops=dict(arrowstyle='-', color=MID, lw=0.6))
c.text(0.03,0.93,'positive throughout',transform=c.transAxes,ha='left',va='top',fontsize=6.8,color=DARK)
panel_label(c,'c'); panel_title(c,'prepared family remains lower in zero-force energy'); finish(c)

# Panel D: survival margin plus higher-order boundary nuance.
mp = p.Fc_ground.to_numpy(float) - p.Fc_meta.to_numpy(float)
mn = n.Fc_ground.to_numpy(float) - n.Fc_meta.to_numpy(float)
d.plot(p.theta, mp, color=BLUE, lw=1.25, marker='o', ms=3.5,
       mfc=BLUE, mec=BLUE, label=r'$+y$', zorder=3)
d.plot(n.theta, mn, color=VERM, lw=1.15, ls='--', marker='s', ms=3.4,
       mfc='white', mec=VERM, mew=0.8, label=r'$-y$', zorder=3)
d.axhline(0, color=LIGHT, lw=0.7, zorder=0)
d.axvline(1.5, color=LIGHT, lw=0.7, ls=':', zorder=0)
d.set_xlim(0,3); d.set_ylim(0, max(mp)*1.12)
d.set_xlabel(r'twist $\theta$ (deg)')
d.set_ylabel(r'$F_c^{\mathrm{ground}}-F_c^{\mathrm{meta}}$')
d.legend(loc='upper left', handlelength=2.0, borderaxespad=0.3)
d.text(0.73,0.34,'both margins > 0',transform=d.transAxes,
       ha='center',va='center',fontsize=6.8,color=DARK)
panel_label(d,'d'); panel_title(d,'prepared branch remains the last survivor'); finish(d)

stem = 'Figure_2_prepared_state_directional_depinning_N22R'
for ext in ['pdf','svg','eps']:
    fig.savefig(OUT/f'{stem}.{ext}', format=ext, bbox_inches=None, pad_inches=0)
fig.savefig(OUT/f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
plt.close(fig)
print(stem)
