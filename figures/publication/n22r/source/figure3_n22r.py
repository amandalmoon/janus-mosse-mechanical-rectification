from __future__ import annotations
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(os.environ['N22R_RELEASE_ROOT'])
OUT = Path(os.environ['N22R_OUT'])
STYLE = Path(__file__).with_name('publication_n22r.mplstyle')
VECTOR_EXPORTS = ('.pdf', '.svg', '.eps')
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
VERY_LIGHT = '#ECECEC'
GRID = '#D8D8D8'
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

md = pd.read_csv(ROOT / 'data' / 'canonical' / 'matched_symmetry_final.csv')
g = md[md.min_id.astype(str) == 'GLOBAL'].set_index('landscape').loc[
    ['2H_centered', '2H_matched_symmetrized', '2H_exact_inverted']
]
o = g.loc['2H_centered']
s = g.loc['2H_matched_symmetrized']
i = g.loc['2H_exact_inverted']

orig_current_norm = float(np.hypot(o.u_per_cycle, o.v_per_cycle))
metrics = [
    ('sym. static split', abs(float(s.delta_F)) / (0.5 * (float(s.Fc_plus) + float(s.Fc_minus))), 'sym'),
    ('sym. current norm', float(np.hypot(s.u_per_cycle, s.v_per_cycle)) / orig_current_norm, 'sym'),
    (r'inv. swap $F_{c,+}$', abs(float(i.Fc_plus) - float(o.Fc_minus)) / abs(float(o.Fc_minus)), 'inv'),
    (r'inv. swap $F_{c,-}$', abs(float(i.Fc_minus) - float(o.Fc_plus)) / abs(float(o.Fc_plus)), 'inv'),
    ('inv. current reversal', float(np.hypot(i.u_per_cycle + o.u_per_cycle, i.v_per_cycle + o.v_per_cycle)) / orig_current_norm, 'inv'),
]

fig = plt.figure(figsize=(inch(177.8), inch(108.0)))
gs = fig.add_gridspec(2, 2, left=0.072, right=0.982, bottom=0.105, top=0.955,
                      wspace=0.30, hspace=0.43, width_ratios=[1.03, 0.97])
a = fig.add_subplot(gs[0,0]); b = fig.add_subplot(gs[0,1])
c = fig.add_subplot(gs[1,0]); d = fig.add_subplot(gs[1,1])

a.axis('off'); a.set_xlim(0,1); a.set_ylim(0,1)
rows = [
    (0.78, 'original', DARK, r'$U=U_e+U_o$', r'$+U_o$'),
    (0.50, 'matched sym.', MID, r'$U_{\rm sym}=U_e$', r'$U_o=0$'),
    (0.22, 'exact inversion', PALE, r'$U_{\rm inv}=U_e-U_o$', r'$-U_o$'),
]
for y0, name, col, formula, odd in rows:
    a.text(0.04, y0, name, ha='left', va='center', fontsize=7.7, fontweight='bold', color=col)
    a.text(0.38, y0, formula, ha='left', va='center', fontsize=8.0, color=DARK)
    a.text(0.94, y0, odd, ha='right', va='center', fontsize=7.1, color=col)
    a.plot([0.04, 0.96], [y0-0.12, y0-0.12], color=VERY_LIGHT, lw=0.8, clip_on=False)
a.text(0.04, 0.025, 'same reciprocal-vector support; even coefficients held fixed',
       ha='left', va='bottom', fontsize=7.0, color=MID)
panel_label(a, 'a', x=-0.02); panel_title(a, 'implemented symmetry controls', x=0.10)

labels = ['original', 'matched\nsym.', 'exact\ninversion']
y = np.arange(3)[::-1]
row_colors = [DARK, MID, PALE]
for yi, (_, row), rcol in zip(y, g.iterrows(), row_colors):
    b.plot([row.Fc_minus, row.Fc_plus], [yi, yi], color=LIGHT, lw=1.8, zorder=1)
    b.plot(row.Fc_plus, yi, marker='o', color=BLUE, ms=5.1, zorder=3)
    b.plot(row.Fc_minus, yi, marker='s', color=VERM, ms=4.8, zorder=3)
    b.text(2.70, yi+0.02, fr'$\Delta F_c={float(row.delta_F):+.3f}$' if abs(float(row.delta_F))>1e-6 else r'$\Delta F_c\approx0$',
           ha='left', va='center', fontsize=6.6, color=rcol)
b.set_yticks(y, labels)
b.set_xlim(0, 3.35)
b.set_xlabel(r'global depinning threshold $F_c^*$')
b.grid(axis='x', color=GRID, lw=0.55)
b.legend(handles=[
    Line2D([0],[0], marker='o', color='none', markerfacecolor=BLUE, markeredgecolor=BLUE, label=r'$F_{c,+}$'),
    Line2D([0],[0], marker='s', color='none', markerfacecolor=VERM, markeredgecolor=VERM, label=r'$F_{c,-}$')
], loc='lower right', handletextpad=0.5)
panel_label(b, 'b'); panel_title(b, 'static symmetry contract'); finish(b)

c.axhline(0, color=LIGHT, lw=0.7, zorder=0); c.axvline(0, color=LIGHT, lw=0.7, zorder=0)
c.annotate('', xy=(float(o.u_per_cycle), float(o.v_per_cycle)), xytext=(0,0),
           arrowprops=dict(arrowstyle='-|>', mutation_scale=12, lw=1.45, color=DARK))
c.plot(float(o.u_per_cycle), float(o.v_per_cycle), marker='o', ms=4.4, color=DARK)
c.annotate(r'original $(1,-1)$', (float(o.u_per_cycle), float(o.v_per_cycle)),
           xytext=(-7, -5), textcoords='offset points', fontsize=6.8, color=DARK,
           ha='right', va='top')
c.annotate('', xy=(float(i.u_per_cycle), float(i.v_per_cycle)), xytext=(0,0),
           arrowprops=dict(arrowstyle='-|>', mutation_scale=12, lw=1.35, color=PALE, linestyle='--'))
c.plot(float(i.u_per_cycle), float(i.v_per_cycle), marker='D', ms=4.2, color=PALE)
c.annotate(r'inverted $(-1,1)$', (float(i.u_per_cycle), float(i.v_per_cycle)),
           xytext=(7, 5), textcoords='offset points', fontsize=6.8, color=PALE,
           ha='left', va='bottom')
c.plot(float(s.u_per_cycle), float(s.v_per_cycle), marker='^', ms=6.0, color=MID, zorder=5)
c.annotate(r'sym. $(0,0)$', (float(s.u_per_cycle), float(s.v_per_cycle)),
           xytext=(7, 5), textcoords='offset points', fontsize=6.8, color=MID,
           ha='left', va='bottom')
c.set_xlim(-1.30, 1.30); c.set_ylim(-1.30, 1.30); c.set_aspect('equal', adjustable='box')
c.set_xticks([-1,0,1]); c.set_yticks([-1,0,1])
c.set_xlabel(r'$u$ winding per cycle'); c.set_ylabel(r'$v$ winding per cycle')
panel_label(c, 'c', x=-0.18); panel_title(c, 'dynamic symmetry contract', x=0.04); finish(c)

yy = np.arange(len(metrics))[::-1]
for yi, (lab, val, kind) in zip(yy, metrics):
    col = MID if kind == 'sym' else PALE
    marker = '^' if kind == 'sym' else 'D'
    d.plot(val, yi, marker=marker, ms=5.0 if kind=='sym' else 4.5,
           color=col, linestyle='none', zorder=3)
    d.annotate(f'{val:.1e}', (val, yi), xytext=(5,0), textcoords='offset points',
               fontsize=6.5, color=col, ha='left', va='center')
d.set_xscale('log'); d.set_xlim(1e-18, 2e-8)
d.set_yticks(yy, [m[0] for m in metrics])
d.grid(axis='x', color=GRID, lw=0.55)
d.set_xlabel('dimensionless symmetry residual')
panel_label(d, 'd'); panel_title(d, 'dimensionless closure residuals'); finish(d)

stem = 'Figure_3_same_spectrum_mechanism_N22R'
for ext in ['pdf','svg','eps']:
    fig.savefig(OUT/f'{stem}.{ext}', format=ext, bbox_inches=None, pad_inches=0)
fig.savefig(OUT/f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
plt.close(fig)
print(stem)
