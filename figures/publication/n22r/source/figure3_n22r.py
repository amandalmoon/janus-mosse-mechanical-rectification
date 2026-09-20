from __future__ import annotations
import os, sys
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
plt.style.use(STYLE)
plt.rcParams.update({
    'font.size': 8.0,
    'axes.labelsize': 8.2,
    'axes.titlesize': 8.4,
    'xtick.labelsize': 7.4,
    'ytick.labelsize': 7.4,
    'legend.fontsize': 7.2,
    'axes.linewidth': 0.65,
    'lines.linewidth': 1.2,
    'lines.markersize': 4.0,
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
MID = '#666666'
LIGHT = '#C8C8C8'
GRID = '#D8D8D8'
SYM = '#527F7E'
INV = '#806884'
MM = 25.4

def inch(mm: float) -> float:
    return mm / MM

def panel_label(ax, letter: str, x=-0.09, y=1.04):
    ax.text(x, y, f'({letter})', transform=ax.transAxes, ha='left', va='bottom',
            fontsize=9.2, fontweight='bold', color=DARK, clip_on=False)

def panel_title(ax, title: str, x=0.02, y=1.025):
    ax.text(x, y, title, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=8.4, color=DARK)

def finish(ax):
    ax.tick_params(direction='out', length=2.5, width=0.6, pad=2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(DARK)
    ax.spines['bottom'].set_color(DARK)

sys.path.insert(0, str(ROOT / 'source'))
import janus_fourier_landscapes_v12 as J

A = np.column_stack([J.A1, J.A2])
base = J.dft_landscape('2H_MoSSe_Se-S-Se-S')
uv_center = np.array([0.6666666660695574, 0.16666666850152867])
a0 = A @ uv_center

def translate_landscape(land, a, name):
    delta = land.vectors @ a
    c = land.c_cos * np.cos(delta) + land.c_sin * np.sin(delta)
    s = -land.c_cos * np.sin(delta) + land.c_sin * np.cos(delta)
    return J.FourierLandscape(
        name, np.array(land.vectors), np.array(c), np.array(s),
        land.energy_unit_meV, land.source_note
    )

centered = translate_landscape(base, a0, '2H_centered')
sym = J.FourierLandscape(
    '2H_matched_symmetrized',
    np.array(centered.vectors),
    np.array(centered.c_cos),
    np.zeros_like(centered.c_sin),
    centered.energy_unit_meV,
    'matched symmetrization'
)
inv = J.FourierLandscape(
    '2H_exact_inverted',
    np.array(centered.vectors),
    np.array(centered.c_cos),
    -np.array(centered.c_sin),
    centered.energy_unit_meV,
    'exact inversion'
)
lands = [centered, sym, inv]

md = pd.read_csv(ROOT / 'data' / 'canonical' / 'matched_symmetry_final.csv')
g = md[md.min_id.astype(str) == 'GLOBAL'].set_index('landscape').loc[
    ['2H_centered', '2H_matched_symmetrized', '2H_exact_inverted']
]
o = g.loc['2H_centered']
s = g.loc['2H_matched_symmetrized']
i = g.loc['2H_exact_inverted']

orig_current_norm = float(np.hypot(o.u_per_cycle, o.v_per_cycle))
metrics = [
    ('sym. split', abs(float(s.delta_F)) / (0.5 * (float(s.Fc_plus) + float(s.Fc_minus))), 'sym'),
    ('sym. current', float(np.hypot(s.u_per_cycle, s.v_per_cycle)) / orig_current_norm, 'sym'),
    (r'inv. swap $+$', abs(float(i.Fc_plus) - float(o.Fc_minus)) / abs(float(o.Fc_minus)), 'inv'),
    (r'inv. swap $-$', abs(float(i.Fc_minus) - float(o.Fc_plus)) / abs(float(o.Fc_plus)), 'inv'),
    ('inv. current', float(np.hypot(i.u_per_cycle + o.u_per_cycle, i.v_per_cycle + o.v_per_cycle)) / orig_current_norm, 'inv'),
]

fig = plt.figure(figsize=(inch(177.8), inch(114.0)))
outer = fig.add_gridspec(
    2, 1, left=0.078, right=0.940, bottom=0.115, top=0.895,
    hspace=0.50, height_ratios=[1.02, 0.98]
)
agt = outer[0].subgridspec(1, 4, wspace=0.11, width_ratios=[1, 1, 1, 0.055])
axs = [fig.add_subplot(agt[0, j]) for j in range(3)]
cax = fig.add_subplot(agt[0, 3])
bot = outer[1].subgridspec(1, 3, wspace=0.47, width_ratios=[1.08, 0.92, 1.12])
b = fig.add_subplot(bot[0, 0])
c = fig.add_subplot(bot[0, 1])
d = fig.add_subplot(bot[0, 2])

# A: matched original / symmetrized / inverted landscapes on a common scale.
u = np.linspace(0, 1, 201)
v = np.linspace(0, 1, 201)
U, V = np.meshgrid(u, v, indexing='xy')
XY = np.stack([U + 0.5 * V, (np.sqrt(3) / 2) * V], axis=-1)
ZZ = [L.potential(XY[..., 0], XY[..., 1]) for L in lands]
vmax = max(float(np.max(np.abs(z))) for z in ZZ)
levels = np.linspace(-vmax, vmax, 25)
map_labels = [
    ('original', r'$+U_o$'),
    ('matched sym.', r'$U_o=0$'),
    ('exact inversion', r'$-U_o$'),
]
for idx, (ax, z, (name, odd)) in enumerate(zip(axs, ZZ, map_labels)):
    im = ax.contourf(U, V, z, levels=levels, cmap='BrBG', extend='both')
    ax.contour(U, V, z, levels=[0.0], colors=[DARK], linewidths=0.60)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    if idx == 0:
        ax.set_xlabel(r'$u$')
        ax.set_ylabel(r'$v$')
    else:
        ax.set_xlabel(r'$u$')
        ax.tick_params(labelleft=False)
        ax.set_yticklabels([])
    ax.set_title(name + '\n' + odd, fontsize=7.6, color=DARK, pad=4.0)
    ax.tick_params(direction='out', length=2.2, width=0.55, pad=1.5)
    for sp in ax.spines.values():
        sp.set_color(DARK)
        sp.set_linewidth(0.55)
cb = fig.colorbar(im, cax=cax, ticks=[-vmax, 0, vmax])
cax.set_title(r'$U/E_0$', fontsize=7.2, pad=3.0, color=DARK)
cb.ax.tick_params(labelsize=7.1, width=0.5, length=2, pad=1.5)
fig.text(0.035, 0.955, '(a)', ha='left', va='top', fontsize=9.2,
         fontweight='bold', color=DARK)

# B: static threshold pair. No endpoint prose is placed in the data region.
rows = [('original', o), ('matched sym.', s), ('exact inversion', i)]
y = np.arange(3)[::-1]
for yi, (_, row) in zip(y, rows):
    b.plot([row.Fc_minus, row.Fc_plus], [yi, yi], color=LIGHT, lw=1.55, zorder=1)
    b.plot(row.Fc_plus, yi, marker='o', ms=5.2, color=BLUE,
           mfc=BLUE, mec=BLUE, zorder=3)
    b.plot(row.Fc_minus, yi, marker='s', ms=4.9, color=VERM,
           mfc=VERM, mec=VERM, zorder=3)
b.set_yticks(y, ['original', 'sym.', 'inverted'])
b.set_ylim(-0.78, 2.55)
b.set_xlim(1.0, 3.25)
b.set_xticks([1.0, 1.5, 2.0, 2.5, 3.0])
b.set_xlabel(r'depinning threshold $F_c^*$')
b.grid(axis='x', color=GRID, lw=0.5)
handles = [
    Line2D([0], [0], marker='o', color='none', markerfacecolor=BLUE,
           markeredgecolor=BLUE, label='+y', markersize=4.6),
    Line2D([0], [0], marker='s', color='none', markerfacecolor=VERM,
           markeredgecolor=VERM, label='-y', markersize=4.4),
]
b.legend(handles=handles, loc='lower right', ncol=2, handletextpad=0.35,
         columnspacing=0.8, borderaxespad=0.25)
panel_label(b, 'b', x=-0.13)
panel_title(b, 'static thresholds', x=0.02)
finish(b)

# C: cycle-averaged winding under the canonical rocking protocol.
c.axhline(0, color=LIGHT, lw=0.7, zorder=0)
c.axvline(0, color=LIGHT, lw=0.7, zorder=0)
vecs = [
    ('original', o, DARK, 'o', '-'),
    ('sym.', s, SYM, '^', '-'),
    ('inverted', i, INV, 'D', '--'),
]
for name, row, col, mk, ls in vecs:
    x = float(row.u_per_cycle)
    yy = float(row.v_per_cycle)
    if abs(x) + abs(yy) < 1e-8:
        c.plot(x, yy, marker=mk, ms=6.0, mfc=col, mec=col, zorder=4)
    else:
        c.annotate(
            '', xy=(x, yy), xytext=(0, 0),
            arrowprops=dict(
                arrowstyle='-|>', mutation_scale=11, lw=1.35,
                color=col, linestyle=ls
            )
        )
        c.plot(x, yy, marker=mk, ms=4.4, mfc=col, mec=col, zorder=4)
c.text(0.98, 0.07, 'original', transform=c.transAxes, ha='right',
       va='bottom', fontsize=7.2, color=DARK)
c.text(0.04, 0.91, 'inverted', transform=c.transAxes, ha='left',
       va='top', fontsize=7.2, color=INV)
c.text(0.54, 0.54, 'sym.', transform=c.transAxes, ha='left',
       va='bottom', fontsize=7.2, color=SYM)
c.set_xlim(-1.25, 1.25)
c.set_ylim(-1.25, 1.25)
c.set_aspect('equal', adjustable='box')
c.set_xticks([-1, 0, 1])
c.set_yticks([-1, 0, 1])
c.set_xlabel(r'$u$ winding / cycle')
c.set_ylabel(r'$v$ winding / cycle')
panel_label(c, 'c', x=-0.13)
panel_title(c, 'rocking winding', x=0.02)
finish(c)

# D: dimensionless symmetry residuals. Point-value prose stays in the caption.
yd = np.arange(len(metrics))[::-1]
for yi, (_, val, kind) in zip(yd, metrics):
    col = SYM if kind == 'sym' else INV
    mk = '^' if kind == 'sym' else 'D'
    d.plot(val, yi, marker=mk, ms=5.4, mfc=col, mec=col,
           linestyle='none', zorder=3)
d.set_xscale('log')
d.set_xlim(1e-18, 2e-8)
d.set_xticks([1e-18, 1e-15, 1e-12, 1e-9])
d.set_yticks(yd, [m[0] for m in metrics])
d.grid(axis='x', color=GRID, lw=0.5)
d.set_xlabel('normalized symmetry residual')
panel_label(d, 'd', x=-0.14)
panel_title(d, 'closure residuals', x=0.02)
finish(d)

stem = 'Figure_3_same_spectrum_mechanism_N22R'
for ext in ['pdf', 'svg', 'eps']:
    fig.savefig(OUT / f'{stem}.{ext}', format=ext, bbox_inches=None, pad_inches=0)
fig.savefig(OUT / f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
plt.close(fig)
print(stem)
