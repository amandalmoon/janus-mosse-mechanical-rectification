from __future__ import annotations

import argparse
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.lines import Line2D
from PIL import Image

STYLE = Path(__file__).with_name('publication_n18r.mplstyle')
plt.style.use(STYLE)

plt.rcParams.update({
    'font.size': 8.0,
    'axes.labelsize': 8.2,
    'axes.titlesize': 8.2,
    'xtick.labelsize': 7.3,
    'ytick.labelsize': 7.3,
    'legend.fontsize': 7.1,
    'axes.linewidth': 0.65,
    'lines.linewidth': 1.2,
    'lines.markersize': 3.7,
    'legend.frameon': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'svg.fonttype': 'none',
    'savefig.bbox': None,
    'savefig.pad_inches': 0.0,
    'mathtext.fontset': 'dejavusans',
})

BLUE = '#0072B2'
VERM = '#D55E00'
GREEN = '#009E73'
PURPLE = '#CC79A7'
BLUE_LIGHT = '#DDECF4'
VERM_LIGHT = '#F5E1D8'
GREEN_LIGHT = '#E2F2EC'
DARK = '#222222'
MID = '#6E6E6E'
LIGHT = '#C8C8C8'
VERY_LIGHT = '#ECECEC'
GRID = '#D8D8D8'

MM_PER_IN = 25.4

def inch(mm: float) -> float:
    return mm / MM_PER_IN


def panel_label(ax, letter: str, x: float = -0.11, y: float = 1.035) -> None:
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
    pdf = out / f'{stem}.pdf'
    svg = out / f'{stem}.svg'
    eps = out / f'{stem}.eps'
    png = out / f'{stem}.png'
    fig.savefig(pdf, format='pdf', bbox_inches=None, pad_inches=0)
    fig.savefig(svg, format='svg', bbox_inches=None, pad_inches=0)
    fig.savefig(eps, format='eps', bbox_inches=None, pad_inches=0)
    fig.savefig(png, format='png', dpi=300, bbox_inches=None, pad_inches=0)
    plt.close(fig)
