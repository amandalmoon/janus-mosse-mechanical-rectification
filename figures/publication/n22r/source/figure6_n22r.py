from __future__ import annotations
import argparse
import os
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd

STYLE = Path(__file__).with_name('publication_n22r.mplstyle')
plt.style.use(STYLE)
plt.rcParams.update({
    'font.size': 8.0,
    'axes.labelsize': 8.2,
    'axes.titlesize': 8.1,
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
    'savefig.pad_inches': 0.0,
})

FONT_FAMILY = os.environ.get('N22R_FONT_FAMILY', 'Arial')
plt.rcParams['font.family'] = FONT_FAMILY
if FONT_FAMILY.lower() == 'arial':
    plt.rcParams['font.sans-serif'] = ['Arial']

TEAL = '#009E73'
PURPLE = '#CC79A7'
DARK = '#222222'
MID = '#6F6F6F'
LIGHT = '#C9C9C9'
MM = 25.4

def inch(mm: float) -> float:
    return mm / MM

def panel_label(ax, letter: str, x: float = -0.08, y: float = 1.04) -> None:
    ax.text(x, y, f'({letter})', transform=ax.transAxes, ha='left', va='bottom',
            fontsize=9.2, fontweight='bold', color=DARK, clip_on=False)

def panel_title(ax, title: str, x: float = 0.0) -> None:
    ax.text(x, 1.02, title, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=8.1, color=DARK, clip_on=False)

def finish(ax) -> None:
    ax.tick_params(direction='out', length=2.5, width=0.6, pad=2.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(DARK)
    ax.spines['bottom'].set_color(DARK)

def grid_edges(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    d = np.diff(values)
    if not np.allclose(d, d[0]):
        raise ValueError('This figure expects regular sampled axes.')
    step = d[0]
    return np.r_[values[0] - step / 2, values + step / 2]

def discrete_semantic(n_levels: int, color: str, reverse: bool = False):
    base = matplotlib.colors.LinearSegmentedColormap.from_list(
        'semantic', ['#F7F7F7', color]
    )
    vals = base(np.linspace(0.08, 0.94, n_levels))
    if reverse:
        vals = vals[::-1]
    return matplotlib.colors.ListedColormap(vals)

def save_figure(fig, out: Path, stem: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for ext in ['pdf', 'svg', 'eps']:
        fig.savefig(out / f'{stem}.{ext}', format=ext, bbox_inches=None, pad_inches=0)
    fig.savefig(out / f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
    plt.close(fig)

def make_figure(release: Path, out: Path) -> None:
    vm = pd.read_csv(release / 'data' / 'canonical' / 'vector_mode_map_F0_period.csv')
    F = np.array(sorted(vm.F0.unique()), dtype=float)
    P = np.array(sorted(vm.period.unique()), dtype=float)
    if len(vm) != len(F) * len(P):
        raise AssertionError('vector-mode map is not a complete sampled grid')
    if not bool(vm.locked.all()):
        raise AssertionError('Displayed grid contains an unlocked point')

    m_values = vm.pivot(index='period', columns='F0', values='m').loc[P, F].to_numpy(dtype=float)
    n_values = vm.pivot(index='period', columns='F0', values='n').loc[P, F].to_numpy(dtype=float)
    pinned = (m_values == 0) & (n_values == 0)
    m_min, m_max = int(np.nanmin(m_values)), int(np.nanmax(m_values))
    n_min, n_max = int(np.nanmin(n_values)), int(np.nanmax(n_values))
    f_edges = grid_edges(F)
    p_edges = grid_edges(P)

    fig = plt.figure(figsize=(inch(177.8), inch(112.0)))
    gs = fig.add_gridspec(
        2, 2, left=0.075, right=0.945, bottom=0.10, top=0.95,
        height_ratios=[1.02, 0.78], wspace=0.30, hspace=0.42,
    )
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1], sharex=ax_a, sharey=ax_a)
    ax_c = fig.add_subplot(gs[1, :])

    specs = [
        (ax_a, m_values, 'a', 'Winding map: $m$', m_min, m_max, TEAL, False),
        (ax_b, n_values, 'b', 'Winding map: $n$', n_min, n_max, PURPLE, True),
    ]
    for ax, Z, letter, title, vmin, vmax, color, reverse in specs:
        levels = np.arange(vmin - 0.5, vmax + 1.5, 1.0)
        cmap = discrete_semantic(len(levels) - 1, color, reverse=reverse)
        norm = BoundaryNorm(levels, cmap.N)
        mesh = ax.pcolormesh(
            f_edges, p_edges, Z, cmap=cmap, norm=norm, shading='flat',
            edgecolors='white', linewidth=0.45, rasterized=False,
        )
        py, px = np.where(pinned)
        ax.plot(F[px], P[py], linestyle='none', marker='x', color=DARK,
                ms=3.0, mew=0.65, zorder=5)
        ax.add_patch(Rectangle((2.0 - 0.125, 40.0 - 5.0), 0.25, 10.0,
                               fill=False, edgecolor=DARK, linewidth=1.1, zorder=6))
        ax.set_xlim(f_edges[0], f_edges[-1])
        ax.set_ylim(p_edges[0], p_edges[-1])
        ax.set_xlabel(r'rocking amplitude $F_0^*$')
        ax.set_ylabel(r'period $\tau^*$')
        ax.set_xticks(np.arange(1.0, 4.01, 0.5))
        ax.set_yticks(np.arange(20, 81, 10))
        cb = fig.colorbar(mesh, ax=ax, fraction=0.048, pad=0.018,
                          ticks=np.arange(vmin, vmax + 1, 1))
        cb.ax.tick_params(labelsize=7.0, width=0.5, length=2.0)
        panel_label(ax, letter)
        panel_title(ax, title)
        finish(ax)

    ax_b.tick_params(labelleft=False)
    ax_b.set_ylabel('')

    # (c) Representative one-dimensional slice through the mode maps.
    q = vm[np.isclose(vm.period, 40.0)].sort_values('F0')
    ax_c.plot(q.F0, q.m, marker='o', ms=4.0, mfc=TEAL, mec=TEAL,
              color=TEAL, lw=1.15, label=r'$m$')
    ax_c.plot(q.F0, q.n, marker='s', ms=3.8, mfc='white', mec=PURPLE,
              color=PURPLE, lw=1.05, ls='--', label=r'$n$')
    ax_c.axhline(0, color=LIGHT, lw=0.75)
    ax_c.axvline(2.0, color=LIGHT, lw=0.8, ls=':')
    sample = q[np.isclose(q.F0, 2.0)]
    if len(sample) == 1:
        row = sample.iloc[0]
        ax_c.plot([2.0], [float(row.m)], marker='o', ms=5.2,
                  mfc='none', mec=DARK, mew=1.0, linestyle='none', zorder=6)
        ax_c.plot([2.0], [float(row.n)], marker='s', ms=5.0,
                  mfc='none', mec=DARK, mew=1.0, linestyle='none', zorder=6)
        ax_c.text(2.06, 5.55, 'Floquet sample', fontsize=6.7, color=MID,
                  ha='left', va='top')

    ax_c.set_xlim(0.90, 4.10)
    ax_c.set_ylim(-5.7, 6.7)
    ax_c.set_xticks(np.arange(1.0, 4.01, 0.5))
    ax_c.set_xlabel(r'$F_0^*$ at $\tau^*=40$')
    ax_c.set_ylabel('integer winding / cycle')
    ax_c.legend(loc='upper left', ncol=2, columnspacing=1.0, handlelength=1.8)
    panel_label(ax_c, 'c', x=-0.04)
    panel_title(ax_c, 'Vector winding staircase')
    finish(ax_c)

    save_figure(fig, out, 'Figure_6_vector_mode_locking_N22R')

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--release', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    make_figure(args.release, args.out)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
