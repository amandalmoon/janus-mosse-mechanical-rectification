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
MID = '#707070'
PALE = '#9A9A9A'
LIGHT = '#C8C8C8'
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
    styles = {
        20: dict(color=DARK, linestyle='-', label=r'$\phi_e=20^\circ$'),
        25: dict(color=PALE, linestyle=(0, (4, 2)), label=r'$\phi_e=25^\circ$'),
    }

    fig = plt.figure(figsize=(inch(177.8), inch(116.0)))
    gs = fig.add_gridspec(2, 2, left=0.085, right=0.985, bottom=0.105, top=0.955,
                          wspace=0.29, hspace=0.42)
    a = fig.add_subplot(gs[0, 0])
    b = fig.add_subplot(gs[0, 1])
    c = fig.add_subplot(gs[1, 0])
    d = fig.add_subplot(gs[1, 1])

    for phi in (20, 25):
        st = styles[phi]
        q = tr[tr.phi == phi].sort_values('theta')
        sw = float(q.energy_switch.iloc[0])
        du = q.UB - q.UA
        a.plot(q.theta, du, color=st['color'], ls=st['linestyle'], marker='o', ms=3.5,
               mfc='white', mec=st['color'], label=st['label'])
        a.axvline(sw, color=st['color'], ls=':', lw=0.75)
        a.annotate(f'{sw:.3f}°', (sw, 0), xytext=(3, 6), textcoords='offset points',
                   color=st['color'], fontsize=7.0, ha='left', va='bottom')
    a.axhline(0, color=LIGHT, lw=0.75)
    a.set_xlim(2.825, 2.945)
    a.set_xlabel(r'twist $\theta$ (deg)')
    a.set_ylabel(r'$U_B-U_A$')
    a.legend(loc='upper left')
    panel_label(a, 'a'); panel_title(a, 'registry-energy crossings'); finish(a)

    for phi in (20, 25):
        st = styles[phi]
        q = tr[tr.phi == phi].sort_values('theta')
        da = q.FAplus - q.FAminus
        db = q.FBplus - q.FBminus
        b.plot(q.theta, da, color=st['color'], ls='--', marker='o', ms=3.4,
               mfc='white', mec=st['color'])
        b.plot(q.theta, db, color=st['color'], ls='-', marker='s', ms=3.4,
               mfc=st['color'], mec=st['color'])
    b.axhline(0, color=LIGHT, lw=0.75)
    b.set_xlim(2.825, 2.945)
    b.set_ylim(-0.78, 0.78)
    b.set_xlabel(r'twist $\theta$ (deg)')
    b.set_ylabel(r'family split $\Delta F_c^*$')
    family_handles = [
        Line2D([0], [0], color=DARK, ls='--', marker='o', mfc='white', mec=DARK,
               label='family A'),
        Line2D([0], [0], color=DARK, ls='-', marker='s', mfc=DARK, mec=DARK,
               label='family B'),
    ]
    b.legend(handles=family_handles, loc='center', ncol=2, columnspacing=1.0, handlelength=1.7)
    b.text(0.02, 0.97, r'$20^\circ$', transform=b.transAxes, color=DARK, fontsize=7.0,
           ha='left', va='top')
    b.text(0.98, 0.97, r'$25^\circ$', transform=b.transAxes, color=PALE, fontsize=7.0,
           ha='right', va='top')
    panel_label(b, 'b'); panel_title(b, 'competing families carry opposite bias'); finish(b)

    for phi in (20, 25):
        st = styles[phi]
        q = tr[tr.phi == phi].sort_values('theta')
        sw = float(q.energy_switch.iloc[0])
        pre = q[q.theta < sw]
        post = q[q.theta >= sw]
        c.plot(pre.theta, pre.ground_delta, color=st['color'], ls=st['linestyle'], marker='o',
               ms=3.5, mfc='white', mec=st['color'])
        c.plot(post.theta, post.ground_delta, color=st['color'], ls=st['linestyle'], marker='s',
               ms=3.5, mfc=st['color'], mec=st['color'], label=st['label'])
        c.axvline(sw, color=st['color'], ls=':', lw=0.75)
    c.axhline(0, color=LIGHT, lw=0.75)
    c.set_xlim(2.825, 2.945)
    c.set_ylim(-0.82, 0.82)
    c.set_xlabel(r'twist $\theta$ (deg)')
    c.set_ylabel(r'prepared $\Delta F_c^*$')
    c.legend(loc='center right')
    c.text(0.03, 0.88, 'A selected', transform=c.transAxes, fontsize=7.0, color=MID)
    c.text(0.75, 0.10, 'B selected', transform=c.transAxes, fontsize=7.0, color=MID)
    panel_label(c, 'c'); panel_title(c, 'equilibrium preparation reverses the sign'); finish(c)

    for phi, marker in ((20, 'o'), (25, 'D')):
        st = styles[phi]
        q = ew[ew.phi == phi].sort_values('edge_weight')
        d.plot(q.edge_weight, q.ground_switch_deg, color=st['color'], ls=st['linestyle'],
               marker=marker, ms=3.8, mfc='white', mec=st['color'], label=st['label'])
    d.axhline(3.0, color=MID, ls=':', lw=0.8)
    d.axhspan(3.0, 3.21, color=VERY_LIGHT, zorder=0)
    d.text(0.52, 3.028, 'outside original 0–3° window', fontsize=7.0, color=MID,
           va='bottom', ha='left')
    d.set_ylim(2.68, 3.21)
    d.set_xlim(0.46, 1.54)
    d.set_xlabel('outer-site energy weight')
    d.set_ylabel('equilibrium switch twist (deg)')
    d.legend(loc='upper right')
    panel_label(d, 'd'); panel_title(d, 'switch location is edge-model sensitive'); finish(d)

    savefig(fig, 'Figure_5_boundary_registry_switching_N22R')

if __name__ == '__main__':
    main()
