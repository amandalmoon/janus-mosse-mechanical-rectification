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
PALE = '#A0A0A0'
LIGHT = '#C8C8C8'
VERY_LIGHT = '#EFEFEF'
GRID = '#D8D8D8'
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

md = pd.read_csv(ROOT / 'data' / 'canonical' / 'matched_symmetry_final.csv')
g = md[md.min_id.astype(str) == 'GLOBAL'].set_index('landscape').loc[
    ['2H_centered', '2H_matched_symmetrized', '2H_exact_inverted']
]
o = g.loc['2H_centered']
s = g.loc['2H_matched_symmetrized']
i = g.loc['2H_exact_inverted']

fig = plt.figure(figsize=(inch(177.8), inch(92.0)))
gs = fig.add_gridspec(
    2, 2,
    left=0.075, right=0.982, bottom=0.12, top=0.94,
    height_ratios=[0.52, 1.48], wspace=0.30, hspace=0.42,
)
ax_a = fig.add_subplot(gs[0, :])
ax_b = fig.add_subplot(gs[1, 0])
ax_c = fig.add_subplot(gs[1, 1])

# (a) Compact symmetry-operation strip.
ax_a.axis('off')
ax_a.set_xlim(0, 1)
ax_a.set_ylim(0, 1)
cards = [
    (0.02, 0.31, 'Original', r'$U_e+U_o$', DARK),
    (0.345, 0.31, 'Symmetrized', r'$U_e$', MID),
    (0.67, 0.31, 'Inverted', r'$U_e-U_o$', PALE),
]
for x0, width, name, formula, color in cards:
    ax_a.add_patch(plt.Rectangle((x0, 0.17), width, 0.58, facecolor='white',
                                 edgecolor=LIGHT, linewidth=0.75))
    ax_a.text(x0 + 0.03, 0.59, name, ha='left', va='center',
              fontsize=7.7, fontweight='bold', color=color)
    ax_a.text(x0 + width / 2, 0.36, formula, ha='center', va='center',
              fontsize=9.0, color=DARK)
panel_label(ax_a, 'a', x=-0.015, y=0.93)
panel_title(ax_a, 'Symmetry controls', x=0.055)

# (b) Static depinning response as a paired/dumbbell comparison.
labels = ['Original', 'Symmetrized', 'Inverted']
rows = [o, s, i]
y = np.arange(3)[::-1]
for yi, row in zip(y, rows):
    fm = float(row.Fc_minus)
    fp = float(row.Fc_plus)
    ax_b.plot([min(fm, fp), max(fm, fp)], [yi, yi], color=LIGHT, lw=2.1, zorder=1)
    ax_b.plot(fp, yi, marker='o', ms=5.1, mfc=BLUE, mec=BLUE, linestyle='none', zorder=3)
    ax_b.plot(fm, yi, marker='s', ms=4.8, mfc='white', mec=VERM, mew=1.0,
              linestyle='none', zorder=3)

ax_b.set_yticks(y, labels)
ax_b.set_xlim(0.0, max(float(g.Fc_plus.max()), float(g.Fc_minus.max())) * 1.10)
ax_b.set_xlabel(r'global depinning threshold $F_c^*$')
ax_b.grid(axis='x', color=GRID, lw=0.5)
ax_b.legend(handles=[
    Line2D([0], [0], marker='o', color='none', markerfacecolor=BLUE,
           markeredgecolor=BLUE, label=r'$F_{c,+}$'),
    Line2D([0], [0], marker='s', color='none', markerfacecolor='white',
           markeredgecolor=VERM, label=r'$F_{c,-}$'),
], loc='lower right', ncol=2, columnspacing=1.0, handletextpad=0.4)
panel_label(ax_b, 'b')
panel_title(ax_b, 'Static depinning response')
finish(ax_b)

# (c) Dynamic response in winding space.
ax_c.axhline(0, color=LIGHT, lw=0.75, zorder=0)
ax_c.axvline(0, color=LIGHT, lw=0.75, zorder=0)

states = [
    ('Original', o, DARK, '-', 'o'),
    ('Symmetrized', s, MID, ':', '^'),
    ('Inverted', i, PALE, '--', 'D'),
]
offsets = {
    'Original': (-8, -6, 'right', 'top'),
    'Symmetrized': (7, 5, 'left', 'bottom'),
    'Inverted': (7, 5, 'left', 'bottom'),
}
for name, row, color, ls, marker in states:
    x = float(row.u_per_cycle)
    yv = float(row.v_per_cycle)
    if abs(x) + abs(yv) > 1e-12:
        ax_c.annotate('', xy=(x, yv), xytext=(0, 0),
                      arrowprops=dict(arrowstyle='-|>', mutation_scale=12,
                                      lw=1.35, color=color, linestyle=ls))
    ax_c.plot(x, yv, marker=marker, ms=5.0 if marker != '^' else 5.8,
              color=color, linestyle='none', zorder=4)
    dx, dy, ha, va = offsets[name]
    ax_c.annotate(name, (x, yv), xytext=(dx, dy), textcoords='offset points',
                  fontsize=6.9, color=color, ha=ha, va=va)

ax_c.set_xlim(-1.30, 1.30)
ax_c.set_ylim(-1.30, 1.30)
ax_c.set_aspect('equal', adjustable='box')
ax_c.set_xticks([-1, 0, 1])
ax_c.set_yticks([-1, 0, 1])
ax_c.set_xlabel(r'$u$ winding per cycle')
ax_c.set_ylabel(r'$v$ winding per cycle')
panel_label(ax_c, 'c')
panel_title(ax_c, 'Dynamic winding response')
finish(ax_c)

stem = 'Figure_3_same_spectrum_mechanism_N22R'
OUT.mkdir(parents=True, exist_ok=True)
for ext in ['pdf', 'svg', 'eps']:
    fig.savefig(OUT / f'{stem}.{ext}', format=ext, bbox_inches=None, pad_inches=0)
fig.savefig(OUT / f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
plt.close(fig)
print(stem)
