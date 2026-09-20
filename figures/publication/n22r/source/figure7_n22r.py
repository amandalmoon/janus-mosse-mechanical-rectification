from __future__ import annotations
import os

import argparse
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

GREEN = '#009E73'
PURPLE = '#CC79A7'
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

    dt_max = (
        dtz.assign(max_abs_z=np.maximum(np.abs(dtz.z_u), np.abs(dtz.z_v)))
           .groupby('T', as_index=False)['max_abs_z'].max()
           .sort_values('T')
    )
    if float(dt_max.max_abs_z.max()) > 1.12 + 1e-9:
        raise AssertionError('Targeted timestep compatibility contract changed')

    fig = plt.figure(figsize=(inch(177.8), inch(116.0)))
    gs = fig.add_gridspec(
        2, 2, left=0.085, right=0.985, bottom=0.105, top=0.955,
        height_ratios=[1.20, 1.00], wspace=0.31, hspace=0.43,
    )
    ax_a = fig.add_subplot(gs[0, :]); ax_b = fig.add_subplot(gs[1, 0]); ax_c = fig.add_subplot(gs[1, 1])

    low_specs = [
        (GREEN, 'o', '-', r'mean $u$', 'mean_u', 'u_ci_lo', 'u_ci_hi'),
        (PURPLE, 's', '--', r'mean $v$', 'mean_v', 'v_ci_lo', 'v_ci_hi'),
    ]
    for color, marker, ls, label, mean_col, lo_col, hi_col in low_specs:
        m = low[mean_col].to_numpy(float); lo = low[lo_col].to_numpy(float); hi = low[hi_col].to_numpy(float)
        ax_a.errorbar(low['T'], m, yerr=ci_err(m, lo, hi), marker=marker, mfc='white', mec=color, mew=0.9,
                      color=color, ls=ls, lw=1.10, ms=3.8, capsize=1.6, label=label)
        hm = high[mean_col].to_numpy(float); hlo = high[lo_col].to_numpy(float); hhi = high[hi_col].to_numpy(float)
        ax_a.errorbar(high['T'], hm, yerr=ci_err(hm, hlo, hhi), marker=marker, mfc=color, mec=color,
                      color=color, ls=ls, lw=1.10, ms=3.8, capsize=1.6)

    ax_a.axhline(0, color=LIGHT, lw=0.75); ax_a.axvspan(0.49, 0.71, color=VERY_LIGHT, zorder=0)
    ax_a.set_xlim(0.0, 0.72); ax_a.set_ylim(-2.60, 1.40)
    ax_a.set_xlabel(r'reduced temperature $T^*$'); ax_a.set_ylabel('mean lattice displacement / cycle')
    ax_a.legend(loc='lower left', ncol=2, columnspacing=1.25, handlelength=2.1)
    ax_a.text(0.475, 0.08, 'open: N=500   filled: pooled N=1000',
              transform=ax_a.transAxes, ha='center', va='bottom', fontsize=7.0, color=MID)
    panel_label(ax_a, 'a', x=-0.055)
    panel_title(ax_a, 'stationary mean displacement with trajectory-level 95% intervals')
    finish(ax_a)

    ax_az = inset_axes(ax_a, width='34%', height='53%', loc='upper right', borderpad=0.95)
    ax_az.set_facecolor('white')
    for color, marker, ls, _, mean_col, lo_col, hi_col in low_specs:
        hm = high[mean_col].to_numpy(float); hlo = high[lo_col].to_numpy(float); hhi = high[hi_col].to_numpy(float)
        ax_az.errorbar(high['T'], hm, yerr=ci_err(hm, hlo, hhi), marker=marker, mfc=color, mec=color,
                       color=color, ls=ls, lw=0.95, ms=3.2, capsize=1.5)
    ax_az.axhline(0, color=LIGHT, lw=0.65); ax_az.set_xlim(0.49, 0.71); ax_az.set_ylim(-0.19, 0.115)
    ax_az.set_xticks([0.50, 0.60, 0.70]); ax_az.set_yticks([-0.15, -0.05, 0.05, 0.10])
    ax_az.tick_params(labelsize=7.0, direction='out', length=2.0, width=0.55, pad=1.5)
    ax_az.set_title('pooled high-$T^*$ zoom', fontsize=7.0, pad=2.0, color=DARK)
    ax_az.text(0.97, 0.06, 'pooled trajectory-level 95% CIs',
               transform=ax_az.transAxes, ha='right', va='bottom', fontsize=7.0, color=MID)

    ratio = pooled['T2'].to_numpy(float) / pooled['crit'].to_numpy(float)
    ax_b.plot(pooled['T'], ratio, color=DARK, marker='o', ms=4.0, lw=1.15)
    ax_b.axhline(1.0, color=MID, lw=0.85, ls='--')
    ax_b.set_xlim(0.49, 0.71); ax_b.set_xticks(expected_high_t, [f'{t:.2f}' for t in expected_high_t])
    ax_b.set_ylim(0, max(ratio) * 1.08); ax_b.set_xlabel(r'$T^*$'); ax_b.set_ylabel(r'$T_H^2/T_{0.95}^2$')
    ax_b.text(0.70, 1.6, '95% threshold = 1', ha='right', va='bottom', fontsize=7.0, color=MID)
    ax_b.annotate(f'{ratio[-1]:.2f}', (0.70, ratio[-1]), xytext=(-5, 5),
                  textcoords='offset points', ha='right', va='bottom', fontsize=7.0, color=DARK)
    panel_label(ax_b, 'b'); panel_title(ax_b, 'joint current remains separated from zero'); finish(ax_b)

    ax_bi = inset_axes(ax_b, width='39%', height='41%', loc='upper right', borderpad=1.10)
    ax_bi.plot(dt_max['T'], dt_max.max_abs_z, marker='D', linestyle='none',
               mfc='white', mec=MID, mew=0.8, color=MID, ms=3.1)
    ax_bi.set_xlim(0.585, 0.715); ax_bi.set_ylim(0.0, 1.30)
    ax_bi.set_xticks([0.60, 0.70]); ax_bi.set_yticks([0.0, 0.6, 1.2])
    ax_bi.tick_params(labelsize=7.0, direction='out', length=1.8, width=0.5, pad=1.2)
    ax_bi.set_title(r'dt robustness: max $|z|$', fontsize=7.0, pad=1.5, color=MID)
    ax_bi.text(0.96, 0.08, r'$\leq 1.12$', transform=ax_bi.transAxes,
               ha='right', va='bottom', fontsize=7.0, color=MID)

    ax_c.plot(low['T'], low.P_v_negative_cycle, color=PURPLE, marker='s', mfc='white', mec=PURPLE, mew=0.9,
              ms=3.5, lw=1.0, ls='-', label=r'$P(v_{\mathrm{cycle}}<0)$')
    ax_c.plot(low['T'], low.P_target_cycle, color=DARK, marker='D', mfc='white', mec=DARK, mew=0.8,
              ms=3.2, lw=1.0, ls='--', label=r'$P[(m,n)=(1,-1)]$')
    pneg = sign.Pneg.to_numpy(float); ptar = sign.Ptarget.to_numpy(float)
    ax_c.errorbar(sign['T'], pneg,
                  yerr=ci_err(pneg, sign.Pneg_ci_lo.to_numpy(float), sign.Pneg_ci_hi.to_numpy(float)),
                  color=PURPLE, marker='s', mfc=PURPLE, mec=PURPLE, ms=3.5, lw=1.0, ls='-', capsize=1.5)
    ax_c.errorbar(sign['T'], ptar,
                  yerr=ci_err(ptar, sign.Ptarget_ci_lo.to_numpy(float), sign.Ptarget_ci_hi.to_numpy(float)),
                  color=DARK, marker='D', mfc=DARK, mec=DARK, ms=3.2, lw=1.0, ls='--', capsize=1.5)
    ax_c.axhline(0.5, color=LIGHT, lw=0.8, ls=':')
    ax_c.set_xlim(0.0, 0.72); ax_c.set_ylim(-0.02, 1.02)
    ax_c.set_xlabel(r'$T^*$'); ax_c.set_ylabel('cycle probability')
    ax_c.legend(loc='upper right', handlelength=2.1)
    panel_label(ax_c, 'c'); panel_title(ax_c, 'cycle-sign bias vs exact target winding'); finish(ax_c)

    ax_ci = inset_axes(ax_c, width='45%', height='39%', loc='center right', borderpad=1.0)
    excess = pneg - 0.5; ex_lo = sign.Pneg_ci_lo.to_numpy(float) - 0.5; ex_hi = sign.Pneg_ci_hi.to_numpy(float) - 0.5
    ax_ci.errorbar(sign['T'], excess, yerr=ci_err(excess, ex_lo, ex_hi),
                   color=PURPLE, marker='s', mfc=PURPLE, mec=PURPLE, ms=2.9, lw=0.9, capsize=1.3)
    ax_ci.axhline(0, color=LIGHT, lw=0.65); ax_ci.set_xlim(0.49, 0.71); ax_ci.set_ylim(0.0, 0.024)
    ax_ci.set_xticks([0.50, 0.60, 0.70]); ax_ci.set_yticks([0.00, 0.01, 0.02])
    ax_ci.tick_params(labelsize=7.0, direction='out', length=1.8, width=0.5, pad=1.2)
    ax_ci.set_title(r'high-$T^*$ sign excess', fontsize=7.0, pad=1.5, color=MID)

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
