from __future__ import annotations
import os
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ['N22R_RELEASE_ROOT'])
DATA = ROOT / 'data' / 'canonical'
OUT = Path(os.environ['N22R_OUT'])
STYLE = HERE / 'publication_n22r.mplstyle'
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

DARK = '#222222'
MID = '#6F6F6F'
PALE = '#A6A6A6'
LIGHT = '#C8C8C8'
VERY_LIGHT = '#F2F2F2'
MM = 25.4

def inch(mm: float) -> float:
    return mm / MM

def panel_label(ax, letter: str, x: float = -0.09, y: float = 1.04) -> None:
    ax.text(x, y, f'({letter})', transform=ax.transAxes, ha='left', va='bottom',
            fontsize=9.2, fontweight='bold', color=DARK, clip_on=False)

def panel_title(ax, title: str, x: float = 0.07) -> None:
    ax.text(x, 1.02, title, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=8.1, color=DARK, clip_on=False)

def finish(ax) -> None:
    ax.tick_params(direction='out', length=2.5, width=0.6, pad=2.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(DARK)
    ax.spines['bottom'].set_color(DARK)

def savefig(fig, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ['pdf', 'svg', 'eps']:
        fig.savefig(OUT / f'{stem}.{ext}', format=ext, bbox_inches=None, pad_inches=0)
    fig.savefig(OUT / f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
    plt.close(fig)

def main() -> None:
    tr = pd.read_csv(DATA / 'triangle_ground_switch.csv')
    ew = pd.read_csv(DATA / 'edge_weight_ground_switch.csv')
    phi_style = {
        20: dict(color=DARK, linestyle='-', label=r'$\phi_e$ = 20°'),
        25: dict(color=PALE, linestyle='--', label=r'$\phi_e$ = 25°'),
    }

    fig = plt.figure(figsize=(inch(177.8), inch(78.0)))
    gs = fig.add_gridspec(
        1, 3, left=0.075, right=0.985, bottom=0.19, top=0.88,
        wspace=0.36, width_ratios=[1.00, 1.12, 0.96],
    )
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[0, 2])

    # (a) Registry-energy crossing is the trigger.
    for phi in (20, 25):
        st = phi_style[phi]
        q = tr[tr.phi == phi].sort_values('theta')
        sw = float(q.energy_switch.iloc[0])
        du = q.UB - q.UA
        ax_a.plot(q.theta, du, color=st['color'], ls=st['linestyle'],
                  marker='o', ms=3.4, mfc='white', mec=st['color'], mew=0.8)
        ax_a.axvline(sw, color=st['color'], ls=':', lw=0.75)
        ax_a.annotate(f'{phi}°', (float(q.theta.iloc[0]), float(du.iloc[0])),
                      xytext=(5, 4), textcoords='offset points',
                      fontsize=6.8, color=st['color'], ha='left', va='bottom')

    ax_a.axhline(0, color=LIGHT, lw=0.75)
    ax_a.set_xlim(2.825, 2.945)
    ax_a.set_xlabel(r'twist $\theta$ (deg)')
    ax_a.set_ylabel(r'$U_B-U_A$')
    panel_label(ax_a, 'a')
    panel_title(ax_a, 'Registry-energy crossings')
    finish(ax_a)

    # (b) Family-specific bias with selected branch encoded by marker fill.
    for phi in (20, 25):
        st = phi_style[phi]
        q = tr[tr.phi == phi].sort_values('theta')
        sw = float(q.energy_switch.iloc[0])
        da = q.FAplus - q.FAminus
        db = q.FBplus - q.FBminus

        ax_b.plot(q.theta, da, color=st['color'], ls='--', lw=1.05,
                  marker='o', ms=3.3, mfc='white', mec=st['color'], mew=0.8)
        ax_b.plot(q.theta, db, color=st['color'], ls='-', lw=1.10,
                  marker='s', ms=3.3, mfc='white', mec=st['color'], mew=0.8)

        pre = q.theta < sw
        post = ~pre
        ax_b.plot(q.loc[pre, 'theta'], da.loc[pre], linestyle='none',
                  marker='o', ms=4.0, mfc=st['color'], mec=st['color'], zorder=5)
        ax_b.plot(q.loc[post, 'theta'], db.loc[post], linestyle='none',
                  marker='s', ms=4.0, mfc=st['color'], mec=st['color'], zorder=5)
        ax_b.axvline(sw, color=st['color'], ls=':', lw=0.70)

    ax_b.axhline(0, color=LIGHT, lw=0.75)
    ax_b.set_xlim(2.825, 2.945)
    ax_b.set_ylim(-0.78, 0.78)
    ax_b.set_xlabel(r'twist $\theta$ (deg)')
    ax_b.set_ylabel(r'family split $\Delta F_c^*$')
    ax_b.text(2.875, 0.67, 'family A', fontsize=6.8, color=DARK, ha='center', va='center')
    ax_b.text(2.875, -0.69, 'family B', fontsize=6.8, color=DARK, ha='center', va='center')
    panel_label(ax_b, 'b')
    panel_title(ax_b, 'Competing-family bias')
    finish(ax_b)

    # (c) Interpretation boundary: switching location vs edge weighting.
    for phi, marker in ((20, 'o'), (25, 'D')):
        st = phi_style[phi]
        q = ew[ew.phi == phi].sort_values('edge_weight')
        ax_c.plot(q.edge_weight, q.ground_switch_deg, color=st['color'], ls=st['linestyle'],
                  marker=marker, ms=3.8, mfc='white', mec=st['color'], mew=0.8,
                  label=st['label'])
    ax_c.axhline(3.0, color=MID, ls=':', lw=0.8)
    ax_c.axhspan(3.0, 3.21, color=VERY_LIGHT, zorder=0)
    ax_c.set_ylim(2.68, 3.21)
    ax_c.set_xlim(0.46, 1.54)
    ax_c.set_xlabel('outer-site energy weight')
    ax_c.set_ylabel('switch twist (deg)')
    ax_c.legend(loc='upper right', handlelength=1.7)
    panel_label(ax_c, 'c')
    panel_title(ax_c, 'Switch-location sensitivity')
    finish(ax_c)

    savefig(fig, 'Figure_5_boundary_registry_switching_N22R')

if __name__ == '__main__':
    main()
