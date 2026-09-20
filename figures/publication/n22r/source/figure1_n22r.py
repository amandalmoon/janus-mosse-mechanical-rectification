from __future__ import annotations
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch
from scipy.spatial import ConvexHull

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
PALE = '#A8A8A8'
LIGHT = '#C8C8C8'
GRID = '#D8D8D8'
VERY_LIGHT = '#F2F2F2'
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

sys.path.insert(0, str(ROOT / 'source'))
import janus_fourier_landscapes_v12 as J

landscape = J.dft_landscape('2H_MoSSe_Se-S-Se-S')
asym = pd.read_csv(ROOT / 'data' / 'canonical' / 'asymmetry_global_check.csv')

fig = plt.figure(figsize=(inch(177.8), inch(72.0)))
gs = fig.add_gridspec(
    1, 3,
    left=0.045, right=0.985, bottom=0.18, top=0.86,
    wspace=0.52, width_ratios=[1.00, 1.23, 0.82],
)
ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])

# (a) Minimal model schematic.
pos = J.make_hexagonal_flake(6)
posr = pos @ J.rotation_matrix(1.5).T
extent = 6.5
for k in np.arange(-7, 8, 1):
    y0 = k * np.sqrt(3) / 2
    xx = np.array([-extent, extent])
    ax_a.plot(xx, np.full_like(xx, y0), color='#F0F0F0', lw=0.45, zorder=0)
    ax_a.plot(xx, np.sqrt(3) * xx + k * np.sqrt(3), color='#F3F3F3', lw=0.45, zorder=0)
    ax_a.plot(xx, -np.sqrt(3) * xx + k * np.sqrt(3), color='#F3F3F3', lw=0.45, zorder=0)

hull = ConvexHull(posr)
cycle = np.r_[hull.vertices, hull.vertices[0]]
ax_a.scatter(posr[:, 0], posr[:, 1], s=5.0, facecolor='white', edgecolor=MID, linewidth=0.5, zorder=2)
ax_a.plot(posr[cycle, 0], posr[cycle, 1], color=DARK, lw=1.15, zorder=3)
ax_a.scatter([0], [0], s=16, color=DARK, zorder=5)

for y2, color, label in ((4.2, BLUE, r'$+y$'), (-4.2, VERM, r'$-y$')):
    ax_a.add_patch(FancyArrowPatch((0, 0), (0, y2), arrowstyle='-|>', mutation_scale=10,
                                   color=color, lw=1.2, zorder=5))
    ax_a.text(0.30, y2 - 0.10 * np.sign(y2), label, color=color, fontsize=7.2, va='center')

ax_a.annotate('', xy=(3.20, 0.72), xytext=(1.70, 0.72),
              arrowprops=dict(arrowstyle='<->', color=DARK, lw=0.75))
ax_a.annotate('', xy=(2.45, 1.47), xytext=(2.45, -0.03),
              arrowprops=dict(arrowstyle='<->', color=DARK, lw=0.75))
ax_a.text(2.52, -0.28, 'COM', fontsize=6.8, color=DARK, ha='left', va='top')
ax_a.text(0.96, 0.92, r'$N=127$', transform=ax_a.transAxes, ha='right', va='top',
          fontsize=7.1, color=DARK)
ax_a.set_aspect('equal')
ax_a.set_xlim(-6.45, 6.45)
ax_a.set_ylim(-5.85, 5.85)
ax_a.axis('off')
panel_label(ax_a, 'a', x=-0.02)
panel_title(ax_a, 'Unguided Janus contact', x=0.10)

# (b) Published stacking-energy landscape.
u = np.linspace(0, 1, 241)
v = np.linspace(0, 1, 241)
U, V = np.meshgrid(u, v, indexing='xy')
XY = np.stack([U + 0.5 * V, (np.sqrt(3) / 2) * V], axis=-1)
Z = landscape.potential(XY[..., 0], XY[..., 1])
vmax = float(np.max(np.abs(Z)))
im = ax_b.contourf(U, V, Z, levels=np.linspace(-vmax, vmax, 25), cmap='RdBu_r', extend='both')
ax_b.contour(U, V, Z, levels=[0.0], colors=[DARK], linewidths=0.75)
ax_b.set_xlabel(r'$u$ along $\mathbf{a}_1$')
ax_b.set_ylabel(r'$v$ along $\mathbf{a}_2$')
ax_b.set_aspect('equal', adjustable='box')
cb = fig.colorbar(im, ax=ax_b, fraction=0.040, pad=0.020)
cb.set_label(r'$U/E_0$')
cb.ax.tick_params(labelsize=6.5, width=0.5, length=2)
panel_label(ax_b, 'b', x=-0.09)
panel_title(ax_b, '2H MoSSe GSFE', x=0.06)
finish(ax_b)

# (c) Compact inversion-odd diagnostic.
order = [
    '2H_MoSSe_Se-S-Se-S',
    '3R_MoSSe_Se-S-Se-S',
    '3R_MoSSe_S-Se-Se-S',
    '3R_MoSSe_Se-S-S-Se',
]
labels = {
    '2H_MoSSe_Se-S-Se-S': '2H asym.',
    '3R_MoSSe_Se-S-Se-S': '3R asym.',
    '3R_MoSSe_S-Se-Se-S': '3R sym. I',
    '3R_MoSSe_Se-S-S-Se': '3R sym. II',
}
q = asym.set_index('key').loc[order]
vals = q.rms.to_numpy(float)
floor = 1e-18
xvals = np.log10(np.where(vals > 0, vals, floor))
yvals = np.arange(len(q))[::-1]
colors = [DARK, '#555555', PALE, PALE]
markers = ['o', 's', '^', 'v']

ax_c.axvspan(-18.7, -17.35, color=VERY_LIGHT, zorder=0)
for yi, value, xv, color, marker in zip(yvals, vals, xvals, colors, markers):
    ax_c.plot([-18.0, xv], [yi, yi], color=LIGHT, lw=0.9, zorder=1)
    ax_c.plot(xv, yi, marker=marker, ms=5.0, color=color, linestyle='none', zorder=3)
    if value >= 1e-12:
        ax_c.annotate(f'{value:.3f}', (xv, yi), xytext=(5, 0), textcoords='offset points',
                      va='center', fontsize=6.8, color=DARK)

ax_c.set_yticks(yvals, [labels[k] for k in order])
ax_c.set_xlim(-18.7, 0.8)
ax_c.set_xticks([-18, -12, -6, 0])
ax_c.set_xlabel(r'$\log_{10}$ odd RMS')
ax_c.grid(axis='x', color=GRID, lw=0.5)
ax_c.text(-18.02, -0.47, 'numerical floor', fontsize=6.3, color=MID,
          ha='center', va='top', clip_on=False)
panel_label(ax_c, 'c', x=-0.13)
panel_title(ax_c, 'Inversion-odd content', x=0.03)
finish(ax_c)

stem = 'Figure_1_credibility_registry_asymmetry_N22R'
OUT.mkdir(parents=True, exist_ok=True)
for ext in ['pdf', 'svg', 'eps']:
    fig.savefig(OUT / f'{stem}.{ext}', format=ext, bbox_inches=None, pad_inches=0)
fig.savefig(OUT / f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
plt.close(fig)
print(stem)
