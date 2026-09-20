from __future__ import annotations
import os

import argparse
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

BLUE = '#0072B2'
VERM = '#D55E00'
DARK = '#222222'
MID = '#6F6F6F'
LIGHT = '#C9C9C9'
VERY_LIGHT = '#EFEFEF'
MM_PER_IN = 25.4

def inch(mm: float) -> float:
    return mm / MM_PER_IN

def panel_label(ax, letter: str, x: float = -0.10, y: float = 1.03) -> None:
    ax.text(x, y, f'({letter})', transform=ax.transAxes, ha='left', va='bottom',
            fontsize=9.2, fontweight='bold', color=DARK, clip_on=False)

def panel_title(ax, title: str) -> None:
    ax.text(0.0, 1.015, title, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=8.1, color=DARK)

def finish(ax) -> None:
    ax.tick_params(direction='out', length=2.5, width=0.6, pad=2.0)
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
    vals = base(np.linspace(0.10, 0.92, n_levels))
    if reverse:
        vals = vals[::-1]
    return matplotlib.colors.ListedColormap(vals)

def save_figure(fig, out: Path, stem: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f'{stem}.pdf', format='pdf', bbox_inches=None, pad_inches=0)
    fig.savefig(out / f'{stem}.svg', format='svg', bbox_inches=None, pad_inches=0)
    fig.savefig(out / f'{stem}.eps', format='eps', bbox_inches=None, pad_inches=0)
    fig.savefig(out / f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
    plt.close(fig)

def make_figure(release: Path, out: Path) -> None:
    vm = pd.read_csv(release / 'data' / 'canonical' / 'vector_mode_map_F0_period.csv')
    fl = pd.read_csv(release / 'data' / 'canonical' / 'floquet_conditioning_check.csv')
    F = np.array(sorted(vm.F0.unique()), dtype=float)
    P = np.array(sorted(vm.period.unique()), dtype=float)
    if len(vm) != len(F) * len(P):
        raise AssertionError('vector-mode map is not a complete sampled grid')
    if not bool(vm.locked.all()):
        raise AssertionError('Figure contract assumes all displayed grid points satisfy the declared lock criterion')
    m_values = vm.pivot(index='period', columns='F0', values='m').loc[P, F].to_numpy(dtype=float)
    n_values = vm.pivot(index='period', columns='F0', values='n').loc[P, F].to_numpy(dtype=float)
    pinned = ((m_values == 0) & (n_values == 0))
    m_min, m_max = int(np.nanmin(m_values)), int(np.nanmax(m_values))
    n_min, n_max = int(np.nanmin(n_values)), int(np.nanmax(n_values))
    if (m_min, m_max) != (0, 10):
        raise AssertionError(f'unexpected m range: {(m_min, m_max)}')
    if (n_min, n_max) != (-9, 0):
        raise AssertionError(f'unexpected n range: {(n_min, n_max)}')
    f_edges = grid_edges(F); p_edges = grid_edges(P)

    fig = plt.figure(figsize=(inch(177.8), inch(124.0)))
    gs = fig.add_gridspec(2, 2, left=0.075, right=0.935, bottom=0.105, top=0.955,
                          wspace=0.30, hspace=0.40)
    ax_a = fig.add_subplot(gs[0, 0]); ax_b = fig.add_subplot(gs[0, 1], sharex=ax_a, sharey=ax_a)
    ax_c = fig.add_subplot(gs[1, 0])
    sub = gs[1, 1].subgridspec(2, 1, hspace=0.10)
    ax_d1 = fig.add_subplot(sub[0, 0]); ax_d2 = fig.add_subplot(sub[1, 0], sharex=ax_d1)

    specs = [
        (ax_a, m_values, 'a', r'sampled winding $m$ along $\mathbf{a}_1$', m_min, m_max, BLUE, False),
        (ax_b, n_values, 'b', r'sampled winding $n$ along $\mathbf{a}_2$', n_min, n_max, VERM, True),
    ]
    for ax, Z, letter, title, vmin, vmax, semantic_color, reverse in specs:
        levels = np.arange(vmin - 0.5, vmax + 1.5, 1.0)
        cmap = discrete_semantic(len(levels) - 1, semantic_color, reverse=reverse)
        norm = BoundaryNorm(levels, cmap.N)
        mesh = ax.pcolormesh(f_edges, p_edges, Z, cmap=cmap, norm=norm, shading='flat',
                             edgecolors='white', linewidth=0.50, rasterized=False)
        py, px = np.where(pinned)
        ax.plot(F[px], P[py], linestyle='none', marker='x', color=DARK, ms=3.2, mew=0.65, zorder=5)
        ax.add_patch(Rectangle((2.0 - 0.125, 40.0 - 5.0), 0.25, 10.0,
                               fill=False, edgecolor=DARK, linewidth=1.15, zorder=6))
        ax.set_xlim(f_edges[0], f_edges[-1]); ax.set_ylim(p_edges[0], p_edges[-1])
        ax.set_xlabel(r'rocking amplitude $F_0^*$'); ax.set_ylabel(r'period $\tau^*$')
        ax.set_xticks(np.arange(1.0, 4.01, 0.5)); ax.set_yticks(np.arange(20, 81, 10))
        cb = fig.colorbar(mesh, ax=ax, fraction=0.048, pad=0.018, ticks=np.arange(vmin, vmax + 1, 1))
        cb.ax.tick_params(labelsize=7.0, width=0.5, length=2.0)
        panel_label(ax, letter); panel_title(ax, title); finish(ax)
    ax_b.tick_params(labelleft=False); ax_b.set_ylabel('')
    ax_a.text(0.97, 0.945, r'$\times$ pinned $(0,0)$: 21/91', transform=ax_a.transAxes,
              ha='right', va='top', fontsize=7.0, color=DARK,
              bbox=dict(facecolor='white', edgecolor='none', pad=0.8, alpha=0.92))

    q = vm[np.isclose(vm.period, 40.0)].sort_values('F0')
    ax_c.plot(q.F0, q.m, marker='o', ms=4.0, mfc=BLUE, mec=BLUE, color=BLUE, lw=1.10, label=r'$m$')
    ax_c.plot(q.F0, q.n, marker='s', ms=3.8, mfc='white', mec=VERM, color=VERM, lw=1.05, ls='--', label=r'$n$')
    ax_c.axhline(0, color=LIGHT, lw=0.7); ax_c.axvline(2.0, color=LIGHT, lw=0.8, ls=':')
    ax_c.text(2.08, 3.05, 'Floquet-tested\n$(1,-1)$ sample', fontsize=7.0, color=DARK, ha='left', va='center')
    ax_c.text(0.02, 0.04, 'markers = sampled amplitudes; lines guide the eye',
              transform=ax_c.transAxes, fontsize=6.8, color=MID, ha='left', va='bottom')
    ax_c.set_xlim(0.90, 4.10); ax_c.set_ylim(-5.7, 6.7)
    ax_c.set_xticks(np.arange(1.0, 4.01, 0.5)); ax_c.set_xlabel(r'$F_0^*$ at $\tau^*=40$')
    ax_c.set_ylabel('integer winding / cycle')
    ax_c.legend(loc='upper left', ncol=2, columnspacing=1.2, handlelength=2.0)
    panel_label(ax_c, 'c'); panel_title(ax_c, 'sampled vector staircase'); finish(ax_c)

    labels = [r'DOP853' + '\n' + r'$10^{-9}$', r'DOP853' + '\n' + r'$10^{-11}$', r'Radau' + '\n' + r'$10^{-9}$']
    x = np.arange(len(fl), dtype=float)
    ref_mask = (fl.method == 'DOP853') & (np.abs(fl.rtol.to_numpy(dtype=float) - 1e-11) < 1e-15)
    if int(ref_mask.sum()) != 1:
        raise AssertionError('Floquet reference solver row is ambiguous')
    rho_ref = float(fl.loc[ref_mask, 'rho'].iloc[0])
    ppm = (fl.rho.to_numpy(dtype=float) / rho_ref - 1.0) * 1e6
    closure_1e11 = fl.closure.to_numpy(dtype=float) * 1e11

    ax_d1.plot(x, ppm, linestyle='none', marker='o', color=DARK, ms=4.2)
    ax_d1.axhline(0, color=LIGHT, lw=0.7)
    ax_d1.set_ylabel(r'$\rho_F$ rel. dev. (ppm)')
    ax_d1.set_ylim(-0.25, max(3.15, float(ppm.max()) * 1.10))
    ax_d1.text(0.98, 0.84, r'$\rho_{F,ref}=6.31108124\times10^{-22}$  << 1',
               transform=ax_d1.transAxes, ha='right', va='top', fontsize=7.0, color=DARK)
    ax_d1.text(0.98, 0.56, 'max cross-solver spread = 2.764 ppm',
               transform=ax_d1.transAxes, ha='right', va='top', fontsize=6.8, color=MID)
    ax_d1.tick_params(labelbottom=False)
    panel_label(ax_d1, 'd', x=-0.11, y=1.08); panel_title(ax_d1, 'representative-orbit Floquet validation'); finish(ax_d1)

    ax_d2.plot(x, closure_1e11, linestyle='none', marker='s', mfc='white', mec=MID, color=MID, ms=4.0)
    ax_d2.set_ylabel(r'closure ($10^{-11}$)'); ax_d2.set_xticks(x, labels)
    ax_d2.set_ylim(0, max(2.15, float(closure_1e11.max()) * 1.10))
    ax_d2.text(0.98, 0.86, 'relative-periodic residual', transform=ax_d2.transAxes,
               ha='right', va='top', fontsize=6.8, color=MID)
    finish(ax_d2)

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
