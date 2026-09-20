from __future__ import annotations
import argparse
import os
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
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
VERY_LIGHT = '#F2F2F2'
MM = 25.4

def inch(mm: float) -> float:
    return mm / MM

def panel_label(ax, letter: str, x: float = -0.07, y: float = 1.04) -> None:
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

def save_figure(fig, out: Path, stem: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for ext in ['pdf', 'svg', 'eps']:
        fig.savefig(out / f'{stem}.{ext}', format=ext, bbox_inches=None, pad_inches=0)
    fig.savefig(out / f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
    plt.close(fig)

def ci_err(mean: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> np.ndarray:
    return np.vstack([mean - lo, hi - mean])

def make_figure(release: Path, out: Path) -> None:
    base = release / 'data' / 'canonical'
    full = pd.read_csv(base / 'thermal_stationary_series_N500.csv')
    pooled_all = pd.read_csv(base / 'stationary_current_two_seed_pooled.csv')
    boot = pd.read_csv(base / 'stationary_thermal_bootstrap_50k.csv')
    sign = pd.read_csv(base / 'stationary_sign_target_bootstrap.csv')

    low = full[full['T'] < 0.5].copy().sort_values('T')
    pooled = pooled_all[pooled_all.seed.astype(str) == 'pooled'].copy().sort_values('T')
    high = pooled.merge(
        boot[['T', 'u_ci_lo', 'u_ci_hi', 'v_ci_lo', 'v_ci_hi', 'zero_excluded']],
        on='T', how='inner', validate='one_to_one',
    )
    sign = sign.sort_values('T')

    expected_high_t = np.array([0.50, 0.55, 0.60, 0.65, 0.70])
    if not np.allclose(high['T'].to_numpy(float), expected_high_t):
        raise AssertionError('Unexpected pooled high-temperature grid')
    if not bool(sign['Pneg_above_half'].all()):
        raise AssertionError('Displayed sign bootstrap does not remain above 0.5')

    fig = plt.figure(figsize=(inch(177.8), inch(86.0)))
    gs = fig.add_gridspec(
        1, 2, left=0.075, right=0.985, bottom=0.16, top=0.90,
        width_ratios=[1.62, 1.0], wspace=0.34,
    )
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])

    series = [
        (TEAL, 'o', '-', r'mean $u$', 'mean_u', 'u_ci_lo', 'u_ci_hi'),
        (PURPLE, 's', '--', r'mean $v$', 'mean_v', 'v_ci_lo', 'v_ci_hi'),
    ]
    for color, marker, ls, label, mean_col, lo_col, hi_col in series:
        m = low[mean_col].to_numpy(float)
        lo = low[lo_col].to_numpy(float)
        hi = low[hi_col].to_numpy(float)
        ax_a.errorbar(
            low['T'], m, yerr=ci_err(m, lo, hi),
            marker=marker, mfc='white', mec=color, mew=0.9,
            color=color, ls=ls, lw=1.10, ms=3.8, capsize=1.6, label=label,
        )

        hm = high[mean_col].to_numpy(float)
        hlo = high[lo_col].to_numpy(float)
        hhi = high[hi_col].to_numpy(float)
        ax_a.errorbar(
            high['T'], hm, yerr=ci_err(hm, hlo, hhi),
            marker=marker, mfc=color, mec=color,
            color=color, ls=ls, lw=1.10, ms=3.8, capsize=1.6,
        )

    ax_a.axhline(0, color=LIGHT, lw=0.75)
    ax_a.axvspan(0.49, 0.71, color=VERY_LIGHT, zorder=0)
    ax_a.set_xlim(0.0, 0.72)
    ax_a.set_ylim(-2.60, 1.40)
    ax_a.set_xlabel(r'reduced temperature $T^*$')
    ax_a.set_ylabel('mean lattice displacement / cycle')
    ax_a.legend(loc='lower left', ncol=2, columnspacing=1.0, handlelength=1.8,
                borderaxespad=0.25)
    panel_label(ax_a, 'a', x=-0.045)
    panel_title(ax_a, 'Thermal current hierarchy')
    finish(ax_a)

    ax_az = inset_axes(ax_a, width='39%', height='48%', loc='upper right', borderpad=0.95)
    ax_az.set_facecolor('white')
    for color, marker, ls, _, mean_col, lo_col, hi_col in series:
        hm = high[mean_col].to_numpy(float)
        hlo = high[lo_col].to_numpy(float)
        hhi = high[hi_col].to_numpy(float)
        ax_az.errorbar(
            high['T'], hm, yerr=ci_err(hm, hlo, hhi),
            marker=marker, mfc=color, mec=color,
            color=color, ls=ls, lw=0.95, ms=3.1, capsize=1.4,
        )
    ax_az.axhline(0, color=LIGHT, lw=0.65)
    ax_az.set_xlim(0.49, 0.71)
    ax_az.set_ylim(-0.19, 0.115)
    ax_az.set_xticks([0.50, 0.60, 0.70])
    ax_az.set_yticks([-0.15, -0.05, 0.05, 0.10])
    ax_az.tick_params(labelsize=6.8, direction='out', length=1.8, width=0.5, pad=1.2)
    ax_az.set_title(r'high-$T^*$ zoom', fontsize=6.9, pad=2.0, color=DARK)

    # (b) Directional sign persistence and exact-winding comparison.
    ax_b.plot(
        low['T'], low.P_v_negative_cycle,
        color=PURPLE, marker='s', mfc='white', mec=PURPLE, mew=0.9,
        ms=3.5, lw=1.0, ls='-', label=r'$P(v_{\mathrm{cycle}}<0)$',
    )
    ax_b.plot(
        low['T'], low.P_target_cycle,
        color=DARK, marker='D', mfc='white', mec=DARK, mew=0.8,
        ms=3.2, lw=1.0, ls='--', label=r'$P[(m,n)=(1,-1)]$',
    )

    pneg = sign.Pneg.to_numpy(float)
    ptar = sign.Ptarget.to_numpy(float)
    ax_b.errorbar(
        sign['T'], pneg,
        yerr=ci_err(pneg, sign.Pneg_ci_lo.to_numpy(float), sign.Pneg_ci_hi.to_numpy(float)),
        color=PURPLE, marker='s', mfc=PURPLE, mec=PURPLE,
        ms=3.5, lw=1.0, ls='-', capsize=1.5,
    )
    ax_b.errorbar(
        sign['T'], ptar,
        yerr=ci_err(ptar, sign.Ptarget_ci_lo.to_numpy(float), sign.Ptarget_ci_hi.to_numpy(float)),
        color=DARK, marker='D', mfc=DARK, mec=DARK,
        ms=3.2, lw=1.0, ls='--', capsize=1.5,
    )

    ax_b.axhline(0.5, color=LIGHT, lw=0.8, ls=':')
    ax_b.set_xlim(0.0, 0.72)
    ax_b.set_ylim(-0.02, 1.02)
    ax_b.set_xlabel(r'reduced temperature $T^*$')
    ax_b.set_ylabel('cycle probability')
    ax_b.legend(loc='upper right', handlelength=1.8, borderaxespad=0.25)
    panel_label(ax_b, 'b', x=-0.12)
    panel_title(ax_b, 'Directional sign persistence')
    finish(ax_b)

    save_figure(fig, out, 'Figure_7_thermal_hierarchy_N22R')

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--release', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    make_figure(args.release, args.out)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
