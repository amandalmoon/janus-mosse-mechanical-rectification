from __future__ import annotations
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ['N22R_RELEASE_ROOT'])
DATA = ROOT / 'data' / 'canonical'
OUT = Path(os.environ['N22R_OUT'])
STYLE = HERE / 'publication_n22r.mplstyle'
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

DARK = '#222222'
MID = '#666666'
LIGHT = '#C9C9C9'
VERY_LIGHT = '#F2F2F2'
ORIENT_20 = '#527F7E'
ORIENT_25 = '#806884'
MM_PER_IN = 25.4


def inch(mm: float) -> float:
    return mm / MM_PER_IN


def panel_label(ax, letter: str, x: float = -0.055, y: float = 1.045) -> None:
    ax.text(
        x, y, f'({letter})', transform=ax.transAxes,
        ha='left', va='bottom', fontsize=9.3,
        fontweight='bold', color=DARK, clip_on=False,
    )


def panel_title(ax, title: str, x: float = 0.055, y: float = 1.025) -> None:
    ax.text(
        x, y, title, transform=ax.transAxes,
        ha='left', va='bottom', fontsize=8.4,
        color=DARK, clip_on=False,
    )


def finish(ax) -> None:
    ax.tick_params(direction='out', length=2.5, width=0.6, pad=2.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(DARK)
    ax.spines['bottom'].set_color(DARK)


def savefig(fig, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f'{stem}.pdf', format='pdf', bbox_inches=None, pad_inches=0)
    fig.savefig(OUT / f'{stem}.svg', format='svg', bbox_inches=None, pad_inches=0)
    fig.savefig(OUT / f'{stem}.eps', format='eps', bbox_inches=None, pad_inches=0)
    fig.savefig(OUT / f'{stem}.png', format='png', dpi=300, bbox_inches=None, pad_inches=0)
    plt.close(fig)


def main() -> None:
    tr = pd.read_csv(DATA / 'triangle_ground_switch.csv')
    ew = pd.read_csv(DATA / 'edge_weight_ground_switch.csv')

    # Orthogonal categorical grammar:
    # orientation -> color + line style
    # registry family -> marker shape + fill
    styles = {
        20: dict(color=ORIENT_20, linestyle='-', label=r'$\phi_e=20$°'),
        25: dict(color=ORIENT_25, linestyle=(0, (4, 2)), label=r'$\phi_e=25$°'),
    }

    fig = plt.figure(figsize=(inch(177.8), inch(116.0)))
    gs = fig.add_gridspec(
        2, 2,
        left=0.083, right=0.982, bottom=0.105, top=0.925,
        wspace=0.30, hspace=0.48,
    )
    a = fig.add_subplot(gs[0, 0])
    b = fig.add_subplot(gs[0, 1])
    c = fig.add_subplot(gs[1, 0])
    d = fig.add_subplot(gs[1, 1])

    # (a) Energy crossing establishes the orientation color/line grammar once.
    for phi in (20, 25):
        st = styles[phi]
        q = tr[tr.phi == phi].sort_values('theta')
        sw = float(q.energy_switch.iloc[0])
        du = q.UB - q.UA
        a.plot(
            q.theta, du,
            color=st['color'], ls=st['linestyle'],
            marker='o', ms=3.8, mfc='white', mec=st['color'], mew=0.8,
            label=st['label'],
        )
        a.axvline(sw, color=st['color'], ls=':', lw=0.75)
    a.axhline(0, color=LIGHT, lw=0.75)
    a.set_xlim(2.825, 2.945)
    a.set_xlabel(r'twist $\theta$ (deg)')
    a.set_ylabel(r'$U_B-U_A$')
    panel_label(a, 'a')
    panel_title(a, 'registry-energy crossings')
    finish(a)

    orientation_handles = [
        Line2D([0], [0], color=ORIENT_20, ls='-', lw=1.3, label=r'$\\phi_e=20$°'),
        Line2D([0], [0], color=ORIENT_25, ls=(0, (4, 2)), lw=1.3, label=r'$\\phi_e=25$°'),
    ]
    fig.legend(
        handles=orientation_handles, loc='upper center',
        bbox_to_anchor=(0.50, 0.988), ncol=2,
        handlelength=2.1, columnspacing=1.6, frameon=False,
    )

    # (b) Family is encoded independently by marker/line grammar.
    for phi in (20, 25):
        st = styles[phi]
        q = tr[tr.phi == phi].sort_values('theta')
        da = q.FAplus - q.FAminus
        db = q.FBplus - q.FBminus
        b.plot(
            q.theta, da,
            color=st['color'], ls='--',
            marker='o', ms=3.7, mfc='white', mec=st['color'], mew=0.8,
        )
        b.plot(
            q.theta, db,
            color=st['color'], ls='-',
            marker='s', ms=3.7, mfc=st['color'], mec=st['color'],
        )
    b.axhline(0, color=LIGHT, lw=0.75)
    b.set_xlim(2.825, 2.945)
    b.set_ylim(-0.78, 0.78)
    b.set_xlabel(r'twist $\theta$ (deg)')
    b.set_ylabel(r'family split $\Delta F_c^*$')
    family_handles = [
        Line2D(
            [0], [0], color=DARK, ls='--', marker='o',
            mfc='white', mec=DARK, mew=0.8, label='family A',
        ),
        Line2D(
            [0], [0], color=DARK, ls='-', marker='s',
            mfc=DARK, mec=DARK, label='family B',
        ),
    ]
    b.legend(
        handles=family_handles, loc='center',
        ncol=2, columnspacing=1.0, handlelength=1.7,
    )
    panel_label(b, 'b')
    panel_title(b, 'competing families carry opposite bias')
    finish(b)

    # (c) Preparation selection uses the same family marker grammar:
    # open circle = A, filled square = B.
    for phi in (20, 25):
        st = styles[phi]
        q = tr[tr.phi == phi].sort_values('theta')
        sw = float(q.energy_switch.iloc[0])
        pre = q[q.theta < sw]
        post = q[q.theta >= sw]
        c.plot(
            pre.theta, pre.ground_delta,
            color=st['color'], ls=st['linestyle'],
            marker='o', ms=3.8, mfc='white', mec=st['color'], mew=0.8,
        )
        c.plot(
            post.theta, post.ground_delta,
            color=st['color'], ls=st['linestyle'],
            marker='s', ms=3.8, mfc=st['color'], mec=st['color'],
        )
        c.axvline(sw, color=st['color'], ls=':', lw=0.75)
    c.axhline(0, color=LIGHT, lw=0.75)
    c.set_xlim(2.825, 2.945)
    c.set_ylim(-0.82, 0.82)
    c.set_xlabel(r'twist $\theta$ (deg)')
    c.set_ylabel(r'prepared $\Delta F_c^*$')
    panel_label(c, 'c')
    panel_title(c, 'equilibrium preparation reverses the sign')
    finish(c)

    # (d) Edge sensitivity reuses only the orientation grammar.
    for phi in (20, 25):
        st = styles[phi]
        q = ew[ew.phi == phi].sort_values('edge_weight')
        d.plot(
            q.edge_weight, q.ground_switch_deg,
            color=st['color'], ls=st['linestyle'],
            marker='o', ms=4.0, mfc='white', mec=st['color'], mew=0.8,
        )
    d.axhline(3.0, color=MID, ls=':', lw=0.8)
    d.axhspan(3.0, 3.21, color=VERY_LIGHT, zorder=0)
    d.set_ylim(2.68, 3.21)
    d.set_xlim(0.46, 1.54)
    d.set_xlabel('outer-site energy weight')
    d.set_ylabel('equilibrium switch twist (deg)')
    panel_label(d, 'd')
    panel_title(d, 'switch location is edge-model sensitive')
    finish(d)

    savefig(fig, 'Figure_5_boundary_registry_switching_N22R')


if __name__ == '__main__':
    main()
