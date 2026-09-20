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
EXTRA = Path(os.environ['N22R_EXTRA_DATA'])
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
PALE_BLUE = '#B9DCEB'
PALE_VERM = '#F2C3AE'
MM = 25.4

def inch(mm: float) -> float:
    return mm / MM

def panel_label(ax, letter: str, x: float = -0.08, y: float = 1.04) -> None:
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

shape = pd.read_csv(ROOT / 'data' / 'canonical' / 'shape_scaling_extended.csv')
elastic = pd.read_csv(EXTRA / 'n8_elastic_robustness_summary.csv')
matched = pd.read_csv(ROOT / 'data' / 'canonical' / 'matched_symmetry_final.csv')
rigid = matched[(matched.landscape == '2H_centered') & (matched.min_id.astype(str) == 'GLOBAL')].iloc[0]
Fp_rigid = float(rigid.Fc_plus)
Fm_rigid = float(rigid.Fc_minus)
rho_rigid = (Fp_rigid - Fm_rigid) / (Fp_rigid + Fm_rigid)

fig = plt.figure(figsize=(inch(177.8), inch(108.0)))
gs = fig.add_gridspec(
    2, 2,
    left=0.078, right=0.982, bottom=0.105, top=0.95,
    width_ratios=[1.55, 1.0], hspace=0.42, wspace=0.34,
)
ax_a = fig.add_subplot(gs[:, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[1, 1])

# (a) Hero: scaled-twist collapse across contact shape and size.
for family, filled, family_ls in [('hex', True, '-'), ('disk', False, ':')]:
    sub = shape[shape.family == family].copy()
    for col, color, marker, pale in [
        ('Fp_norm', BLUE, 'o', PALE_BLUE),
        ('Fm_norm', VERM, 's', PALE_VERM),
    ]:
        for theta, q in sub.groupby('Theta'):
            vals = q[col].to_numpy(float)
            ax_a.plot(np.full_like(vals, float(theta)), vals, linestyle='none', marker=marker,
                      ms=2.6, mfc=(pale if filled else 'white'), mec=pale,
                      mew=0.55, zorder=1)
        g = sub.groupby('Theta')[col].mean().sort_index()
        ax_a.plot(g.index.to_numpy(float), g.to_numpy(float),
                  color=color, lw=1.35, ls=family_ls, marker=marker, ms=4.1,
                  mfc=(color if filled else 'white'), mec=color, mew=0.85, zorder=4)

ax_a.set_xlim(-0.5, 20.5)
ax_a.set_ylim(0.82, 1.012)
ax_a.set_xticks([0, 5, 10, 15, 20])
ax_a.set_xlabel(r'scaled twist $\Theta=\theta\sqrt{N}$ (deg)')
ax_a.set_ylabel(r'normalized threshold $F_c(\Theta)/F_c(0)$')
ax_a.grid(axis='y', color=GRID, lw=0.5)

direction_legend = [
    Line2D([0], [0], color=BLUE, marker='o', ls='-', lw=1.2, ms=3.8,
           mfc=BLUE, mec=BLUE, label=r'$+y$'),
    Line2D([0], [0], color=VERM, marker='s', ls='--', lw=1.2, ms=3.6,
           mfc=VERM, mec=VERM, label=r'$-y$'),
]
shape_legend = [
    Line2D([0], [0], color=DARK, marker='o', ls='-', mfc=DARK, mec=DARK,
           label='hex'),
    Line2D([0], [0], color=DARK, marker='o', ls=':', mfc='white', mec=DARK,
           label='disk'),
]
leg1 = ax_a.legend(handles=direction_legend, loc='lower left', ncol=2,
                   handlelength=1.6, columnspacing=1.0, borderaxespad=0.25)
ax_a.add_artist(leg1)
ax_a.legend(handles=shape_legend, loc='upper right', ncol=2,
            handlelength=1.5, columnspacing=0.9, borderaxespad=0.25)
panel_label(ax_a, 'a', x=-0.055)
panel_title(ax_a, 'Scaled-twist collapse')
finish(ax_a)

# (b) Compliance mainly renormalizes the force scale.
xlabels = ['0.5C', 'C', '2C', '100C', 'rigid']
x = np.arange(len(xlabels), dtype=float)
fem_cases = ['C_half_1p5', 'C_nom_1p5', 'C_2x_1p5', 'C_100x_1p5']
fem = elastic[(elastic.model == 'FEM') & (elastic.case.isin(fem_cases))].copy()
order = {k: i for i, k in enumerate(fem_cases)}
fem['ord'] = fem.case.map(order)
fem = fem.sort_values('ord')

fp = np.r_[fem.Fp.to_numpy(float) / Fp_rigid, 1.0]
fm = np.r_[fem.Fm.to_numpy(float) / Fm_rigid, 1.0]
ax_b.plot(x, fp, color=BLUE, marker='o', ms=4.0, mfc=BLUE, mec=BLUE, lw=1.25, zorder=3)
ax_b.plot(x, fm, color=VERM, marker='s', ms=3.8, mfc=VERM, mec=VERM,
          lw=1.15, ls='--', zorder=3)

vff = elastic[(elastic.model == 'VFF') & (elastic.theta == 1.5)].copy()
for _, row in vff.iterrows():
    scale = float(row['case'].split('scale')[-1])
    xi = 0 if abs(scale - 0.5) < 1e-9 else 1
    ax_b.plot(xi, float(row.Fp) / Fp_rigid, marker='o', ms=4.5,
              mfc='white', mec=BLUE, mew=1.0, linestyle='none', zorder=5)
    ax_b.plot(xi, float(row.Fm) / Fm_rigid, marker='s', ms=4.3,
              mfc='white', mec=VERM, mew=1.0, linestyle='none', zorder=5)

ax_b.axhline(1.0, color=LIGHT, lw=0.75, zorder=0)
ax_b.set_xticks(x, xlabels)
ax_b.set_xlim(-0.35, 4.35)
ax_b.set_ylim(0.895, 1.006)
ax_b.set_ylabel(r'$F_c/F_c^{\mathrm{rigid}}$')
ax_b.legend(handles=[
    Line2D([0], [0], marker='o', color=BLUE, mfc=BLUE, mec=BLUE, ls='-', label=r'$+y$ FEM'),
    Line2D([0], [0], marker='s', color=VERM, mfc=VERM, mec=VERM, ls='--', label=r'$-y$ FEM'),
    Line2D([0], [0], marker='o', color='none', mfc='white', mec=DARK, ls='none', label='VFF points'),
], loc='lower left', fontsize=6.6, handlelength=1.6, borderaxespad=0.2)
panel_label(ax_b, 'b', x=-0.12)
panel_title(ax_b, 'Compliance-renormalized thresholds')
finish(ax_b)

# (c) Directional split remains stable.
rhof = np.r_[fem.rho.to_numpy(float), rho_rigid]
delta_f = 100 * (rhof / rho_rigid - 1.0)
ax_c.plot(x, delta_f, color=DARK, marker='o', ms=4.0, mfc=DARK, mec=DARK, lw=1.25,
          zorder=3, label='FEM')
for _, row in vff.iterrows():
    scale = float(row['case'].split('scale')[-1])
    xi = 0 if abs(scale - 0.5) < 1e-9 else 1
    dv = 100 * (float(row.rho) / rho_rigid - 1.0)
    ax_c.plot(xi, dv, marker='D', ms=4.2, mfc='white', mec=DARK, mew=0.9,
              linestyle='none', zorder=5)

ax_c.axhline(0, color=LIGHT, lw=0.75, zorder=0)
ax_c.set_xticks(x, xlabels)
ax_c.set_xlim(-0.35, 4.35)
ax_c.set_ylim(-0.08, 1.50)
ax_c.set_xlabel(r'in-plane stiffness, $\theta=1.5$°')
ax_c.set_ylabel(r'$100(\rho/\rho_{\mathrm{rigid}}-1)$ (%)')
ax_c.legend(handles=[
    Line2D([0], [0], color=DARK, marker='o', mfc=DARK, mec=DARK, label='FEM'),
    Line2D([0], [0], color='none', marker='D', mfc='white', mec=DARK, label='VFF'),
], loc='upper right', ncol=2, handletextpad=0.4, columnspacing=0.9)
panel_label(ax_c, 'c', x=-0.12)
panel_title(ax_c, 'Directional-split robustness')
finish(ax_c)

stem = 'Figure_4_compact_elastic_robustness_N22R'
OUT.mkdir(parents=True, exist_ok=True)
for ext in ['pdf', 'svg', 'eps']:
    fig.savefig(OUT / f'{stem}.{ext}', format=ext, bbox_inches=None, pad_inches=0)
fig.savefig(OUT / f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
plt.close(fig)
print(stem)
