from __future__ import annotations
import os
import argparse
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

STYLE = Path(__file__).with_name('publication_n22r.mplstyle')
plt.style.use(STYLE)
plt.rcParams.update({
    'font.size': 8.0,
    'axes.labelsize': 8.3,
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
    'savefig.pad_inches': 0.0,
})

FONT_FAMILY = os.environ.get('N22R_FONT_FAMILY', 'Arial')
plt.rcParams['font.family'] = FONT_FAMILY
if FONT_FAMILY.lower() == 'arial':
    plt.rcParams['font.sans-serif'] = ['Arial']
else:
    plt.rcParams['font.sans-serif'] = [FONT_FAMILY]
    plt.rcParams['mathtext.fontset'] = 'dejavusans'

GREEN = '#009E73'
PURPLE = '#CC79A7'
DARK = '#222222'
MID = '#666666'
LIGHT = '#C9C9C9'
GRID = '#DEDEDE'
MM_PER_IN = 25.4


def inch(mm: float) -> float:
    return mm / MM_PER_IN


def panel_label(ax, letter: str, x: float = -0.055, y: float = 1.045) -> None:
    ax.text(x, y, f'({letter})', transform=ax.transAxes, ha='left', va='bottom',
            fontsize=9.3, fontweight='bold', color=DARK, clip_on=False)


def panel_title(ax, title: str, x: float = 0.055, y: float = 1.025) -> None:
    ax.text(x, y, title, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=8.4, color=DARK, clip_on=False)


def finish(ax) -> None:
    ax.tick_params(direction='out', length=2.5, width=0.6, pad=2.0)
    ax.spines['left'].set_color(DARK)
    ax.spines['bottom'].set_color(DARK)


def save_figure(fig, out: Path, stem: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f'{stem}.pdf', format='pdf', bbox_inches=None, pad_inches=0)
    fig.savefig(out / f'{stem}.svg', format='svg', bbox_inches=None, pad_inches=0)
    fig.savefig(out / f'{stem}.eps', format='eps', bbox_inches=None, pad_inches=0)
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
    dtz = pd.read_csv(base / 'highT_dt_pairwise_z.csv')

    low = full[full['T'] < 0.5].copy().sort_values('T')
    pooled = pooled_all[pooled_all.seed.astype(str) == 'pooled'].copy().sort_values('T')
    high = pooled.merge(
        boot[['T', 'u_ci_lo', 'u_ci_hi', 'v_ci_lo', 'v_ci_hi', 'zero_excluded']],
        on='T', how='inner', validate='one_to_one'
    )
    sign = sign.sort_values('T')

    expected_high_t = np.array([0.50, 0.55, 0.60, 0.65, 0.70])
    if not np.allclose(high['T'].to_numpy(float), expected_high_t):
        raise AssertionError('Unexpected pooled high-temperature grid')
    if not bool(high['exclude0'].all()) or not bool(high['zero_excluded'].all()):
        raise AssertionError('Joint zero-current exclusion is not satisfied at every displayed pooled T*')
    if not bool(sign['Pneg_above_half'].all()):
        raise AssertionError('Displayed high-T sign bootstrap does not remain above 0.5 at all points')
    if not np.isclose(float(high.loc[np.isclose(high['T'], 0.70), 'mean_u'].iloc[0]), 0.036997653872049265):
        raise AssertionError('T*=0.70 pooled mean_u changed')
    if not np.isclose(float(high.loc[np.isclose(high['T'], 0.70), 'mean_v'].iloc[0]), -0.0764475302089921):
        raise AssertionError('T*=0.70 pooled mean_v changed')

    # Preserve numerical robustness as a hard source-level contract without
    # competing with the main thermal argument in the publication panel set.
    dt_max = (
        dtz.assign(max_abs_z=np.maximum(np.abs(dtz.z_u), np.abs(dtz.z_v)))
           .groupby('T', as_index=False)['max_abs_z'].max()
           .sort_values('T')
    )
    if float(dt_max.max_abs_z.max()) > 1.12 + 1e-9:
        raise AssertionError('Targeted timestep compatibility contract changed')

    fig = plt.figure(figsize=(inch(177.8), inch(116.0)))
    gs = fig.add_gridspec(
        2, 2, left=0.083, right=0.982, bottom=0.105, top=0.925,
        wspace=0.30, hspace=0.48,
    )
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])

    specs = [
        (GREEN, 'o', '-', r'$\langle u\rangle$', 'mean_u', 'u_ci_lo', 'u_ci_hi'),
        (PURPLE, 's', '--', r'$\langle v\rangle$', 'mean_v', 'v_ci_lo', 'v_ci_hi'),
    ]

    # (a) Overview: broad thermal decay only. High-T uncertainty is delegated to (b).
    for color, marker, ls, label, mean_col, *_ in specs:
        ax_a.plot(low['T'], low[mean_col], marker=marker, mfc='white', mec=color, mew=0.9,
                  color=color, ls=ls, lw=1.15, ms=4.0, label=label)
        ax_a.plot(high['T'], high[mean_col], marker=marker, mfc=color, mec=color,
                  color=color, ls=ls, lw=1.15, ms=4.0)
    ax_a.axhline(0, color=LIGHT, lw=0.75)
    ax_a.set_xlim(0.0, 0.72)
    ax_a.set_ylim(-2.58, 1.36)
    ax_a.set_xlabel(r'reduced temperature $T^*$')
    ax_a.set_ylabel('mean lattice displacement / cycle')
    ax_a.text(0.345, 0.18, r'$\langle u\rangle$', color=GREEN, fontsize=7.3, ha='left', va='center')
    ax_a.text(0.345, -0.36, r'$\langle v\rangle$', color=PURPLE, fontsize=7.3, ha='left', va='center')
    panel_label(ax_a, 'a')
    panel_title(ax_a, 'stationary current across temperature')
    finish(ax_a)

    # (b) High-T zoom: uncertainty is the sole visual job of this panel.
    for color, marker, ls, label, mean_col, lo_col, hi_col in specs:
        hm = high[mean_col].to_numpy(float)
        hlo = high[lo_col].to_numpy(float)
        hhi = high[hi_col].to_numpy(float)
        ax_b.errorbar(high['T'], hm, yerr=ci_err(hm, hlo, hhi), marker=marker,
                      mfc=color, mec=color, color=color, ls=ls, lw=1.10,
                      ms=4.0, capsize=2.0, capthick=0.75, label=label)
    ax_b.axhline(0, color=LIGHT, lw=0.75)
    ax_b.set_xlim(0.49, 0.735)
    ax_b.set_ylim(-0.19, 0.115)
    ax_b.set_xticks(expected_high_t)
    ax_b.set_yticks([-0.15, -0.10, -0.05, 0.00, 0.05, 0.10])
    ax_b.set_xlabel(r'$T^*$')
    ax_b.set_ylabel('mean displacement / cycle')
    ax_b.text(0.708, float(high['mean_u'].iloc[-1]), r'$\langle u\rangle$', color=GREEN, fontsize=7.3, ha='left', va='center')
    ax_b.text(0.708, float(high['mean_v'].iloc[-1]), r'$\langle v\rangle$', color=PURPLE, fontsize=7.3, ha='left', va='center')
    panel_label(ax_b, 'b')
    panel_title(ax_b, 'high-$T^*$ trajectory-level 95% intervals')
    finish(ax_b)

    # (c) Statistical exclusion: one scalar test, one threshold.
    ratio = pooled['T2'].to_numpy(float) / pooled['crit'].to_numpy(float)
    ax_c.plot(pooled['T'], ratio, color=DARK, marker='o', mfc=DARK, mec=DARK,
              ms=4.2, lw=1.15)
    ax_c.axhline(1.0, color=MID, lw=0.85, ls='--')
    ax_c.set_xlim(0.49, 0.71)
    ax_c.set_xticks(expected_high_t)
    ax_c.set_ylim(0, 41)
    ax_c.set_yticks([0, 10, 20, 30, 40])
    ax_c.set_xlabel(r'$T^*$')
    ax_c.set_ylabel(r'$T_H^2/T_{0.95}^2$')
    ax_c.text(0.695, 2.25, '95% threshold', ha='right', va='bottom',
              fontsize=7.2, color=MID)
    panel_label(ax_c, 'c')
    panel_title(ax_c, 'joint current remains separated from zero')
    finish(ax_c)

    # (d) Thermal hierarchy: exact target winding is lost well before sign bias.
    ax_d.plot(low['T'], low.P_v_negative_cycle, color=PURPLE, marker='s',
              mfc='white', mec=PURPLE, mew=0.9, ms=3.8, lw=1.05, ls='-',
              label=r'$P(v_{\mathrm{cycle}}<0)$')
    ax_d.plot(low['T'], low.P_target_cycle, color=DARK, marker='D',
              mfc='white', mec=DARK, mew=0.8, ms=3.4, lw=1.0, ls='--',
              label=r'$P[(m,n)=(1,-1)]$')
    pneg = sign.Pneg.to_numpy(float)
    ptar = sign.Ptarget.to_numpy(float)
    ax_d.errorbar(sign['T'], pneg,
                  yerr=ci_err(pneg, sign.Pneg_ci_lo.to_numpy(float), sign.Pneg_ci_hi.to_numpy(float)),
                  color=PURPLE, marker='s', mfc=PURPLE, mec=PURPLE,
                  ms=3.8, lw=1.05, ls='-', capsize=1.8, capthick=0.7)
    ax_d.errorbar(sign['T'], ptar,
                  yerr=ci_err(ptar, sign.Ptarget_ci_lo.to_numpy(float), sign.Ptarget_ci_hi.to_numpy(float)),
                  color=DARK, marker='D', mfc=DARK, mec=DARK,
                  ms=3.4, lw=1.0, ls='--', capsize=1.8, capthick=0.7)
    ax_d.axhline(0.5, color=LIGHT, lw=0.8, ls=':')
    ax_d.set_xlim(0.0, 0.72)
    ax_d.set_ylim(-0.02, 1.02)
    ax_d.set_xlabel(r'$T^*$')
    ax_d.set_ylabel('cycle probability')
    ax_d.legend(loc='upper right', handlelength=2.0)
    panel_label(ax_d, 'd')
    panel_title(ax_d, 'directional sign bias outlives exact winding')
    finish(ax_d)

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
