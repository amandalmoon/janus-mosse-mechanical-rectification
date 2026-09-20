from __future__ import annotations
import os
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

ROOT = Path(os.environ['N22R_RELEASE_ROOT'])
OUT = Path(os.environ['N22R_OUT'])
STYLE = Path(__file__).with_name('publication_n22r.mplstyle')
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
PALE_FILL = '#F1F1F1'
MM = 25.4

def inch(mm: float) -> float:
    return mm / MM

def panel_label(ax, letter: str, x: float = -0.075, y: float = 1.04) -> None:
    ax.text(x, y, f'({letter})', transform=ax.transAxes, ha='left', va='bottom',
            fontsize=9.2, fontweight='bold', color=DARK, clip_on=False)

def panel_title(ax, title: str, x: float = 0.0) -> None:
    ax.text(x, 1.02, title, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=8.2, color=DARK, clip_on=False)

def finish(ax) -> None:
    ax.tick_params(direction='out', length=2.5, width=0.6, pad=2.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(DARK)
    ax.spines['bottom'].set_color(DARK)

fd = pd.read_csv(ROOT / 'data' / 'canonical' / 'free_fold_nondegeneracy.csv')
fd = fd[fd.theta <= 3.000001].copy()
bs = pd.read_csv(ROOT / 'data' / 'canonical' / 'branch_family_summary.csv').copy()
p = bs[bs.sign == 1].copy().sort_values('theta')
n = bs[bs.sign == -1].copy().sort_values('theta')

fig = plt.figure(figsize=(inch(177.8), inch(116.0)))
gs = fig.add_gridspec(
    2, 2,
    left=0.075, right=0.982, bottom=0.095, top=0.955,
    height_ratios=[1.26, 0.88], wspace=0.28, hspace=0.39,
)
ax_a = fig.add_subplot(gs[0, :])
ax_b = fig.add_subplot(gs[1, 0])
ax_c = fig.add_subplot(gs[1, 1])

# (a) Hero comparison: both loading directions and both branch families on one axis.
ax_a.plot(fd.theta, fd.Ff, color=BLUE, lw=1.55, zorder=4)
ax_a.plot(fd.theta, fd.Fr, color=VERM, lw=1.55, ls='--', zorder=4)
ax_a.plot(p.theta, p.Fc_meta, color=BLUE, lw=1.0, ls=':', marker='o', ms=3.5,
          mfc='white', mec=BLUE, mew=0.8, zorder=3)
ax_a.plot(n.theta, n.Fc_meta, color=VERM, lw=1.0, ls=':', marker='s', ms=3.4,
          mfc='white', mec=VERM, mew=0.8, zorder=3)
ax_a.axvline(1.5, color=LIGHT, lw=0.75, ls=':', zorder=0)
ax_a.set_xlim(-0.05, 3.05)
ax_a.set_ylim(0, 3.65)
ax_a.set_xlabel(r'twist $\theta$ (deg)')
ax_a.set_ylabel(r'branch-followed threshold $F_c^*$')
ax_a.grid(axis='y', color=GRID, lw=0.45)

legend_handles = [
    Line2D([0], [0], color=BLUE, lw=1.5, label=r'$+y$ prepared branch'),
    Line2D([0], [0], color=VERM, lw=1.5, ls='--', label=r'$-y$ prepared branch'),
    Line2D([0], [0], color=BLUE, lw=1.0, ls=':', marker='o', mfc='white', mec=BLUE,
           label=r'$+y$ competing branch'),
    Line2D([0], [0], color=VERM, lw=1.0, ls=':', marker='s', mfc='white', mec=VERM,
           label=r'$-y$ competing branch'),
]
ax_a.legend(handles=legend_handles, loc='upper right', ncol=2, columnspacing=1.2,
            handlelength=2.3, borderaxespad=0.25)
ax_a.text(1.5, 3.47, r'$\theta=1.5^\circ$', fontsize=6.8, color=MID,
          ha='center', va='top')
panel_label(ax_a, 'a', x=-0.04)
panel_title(ax_a, 'Directional depinning')
finish(ax_a)

# (b) Zero-force preparation energy margin.
margin_u = p.U_meta.to_numpy(float) - p.U_ground.to_numpy(float)
ax_b.fill_between(p.theta, 0, margin_u, color=PALE_FILL, linewidth=0, zorder=0)
ax_b.plot(p.theta, margin_u, color=DARK, lw=1.25, marker='o', ms=3.5,
          mfc='white', mec=DARK, mew=0.7, zorder=3)
ax_b.axhline(0, color=LIGHT, lw=0.75, zorder=0)
ax_b.axvline(1.5, color=LIGHT, lw=0.7, ls=':', zorder=0)
ax_b.set_xlim(-0.05, 3.05)
ax_b.set_ylim(0, max(margin_u) * 1.12)
ax_b.set_xlabel(r'twist $\theta$ (deg)')
ax_b.set_ylabel(r'$U_{\mathrm{meta}}-U_{\mathrm{ground}}$')
panel_label(ax_b, 'b')
panel_title(ax_b, 'Preparation energy margin')
finish(ax_b)

# (c) Prepared-branch survival margin.
mp = p.Fc_ground.to_numpy(float) - p.Fc_meta.to_numpy(float)
mn = n.Fc_ground.to_numpy(float) - n.Fc_meta.to_numpy(float)
ax_c.plot(p.theta, mp, color=BLUE, lw=1.25, marker='o', ms=3.7,
          mfc=BLUE, mec=BLUE, label=r'$+y$', zorder=3)
ax_c.plot(n.theta, mn, color=VERM, lw=1.15, ls='--', marker='s', ms=3.5,
          mfc='white', mec=VERM, mew=0.8, label=r'$-y$', zorder=3)
ax_c.axhline(0, color=LIGHT, lw=0.75, zorder=0)
ax_c.axvline(1.5, color=LIGHT, lw=0.7, ls=':', zorder=0)
ax_c.set_xlim(-0.05, 3.05)
ax_c.set_ylim(0, max(float(np.max(mp)), float(np.max(mn))) * 1.12)
ax_c.set_xlabel(r'twist $\theta$ (deg)')
ax_c.set_ylabel(r'$F_c^{\mathrm{ground}}-F_c^{\mathrm{meta}}$')
ax_c.legend(loc='upper right', ncol=2, handlelength=1.8, columnspacing=1.0)
panel_label(ax_c, 'c')
panel_title(ax_c, 'Prepared-branch survival')
finish(ax_c)

stem = 'Figure_2_prepared_state_directional_depinning_N22R'
OUT.mkdir(parents=True, exist_ok=True)
for ext in ['pdf', 'svg', 'eps']:
    fig.savefig(OUT / f'{stem}.{ext}', format=ext, bbox_inches=None, pad_inches=0)
fig.savefig(OUT / f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
plt.close(fig)
print(stem)
