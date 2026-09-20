from __future__ import annotations

import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon, FancyArrowPatch

STYLE = Path(__file__).with_name('publication_n22.mplstyle')
plt.style.use(STYLE)
def apply_common_rc():
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

apply_common_rc()

BLUE='#0072B2'; VERM='#D55E00'; GREEN='#009E73'; PURPLE='#CC79A7'
DARK='#222222'; MID='#707070'; LIGHT='#C8C8C8'; VERY_LIGHT='#EFEFEF'; GRID='#D8D8D8'
BLUE_LIGHT='#DDECF4'; VERM_LIGHT='#F5E1D8'; GREEN_LIGHT='#E2F2EC'
MM_PER_IN=25.4

def inch(mm): return mm/MM_PER_IN

def panel_label(ax, letter, x=-0.10, y=1.03):
    ax.text(x,y,f'({letter})',transform=ax.transAxes,ha='left',va='bottom',fontsize=9.2,fontweight='bold',color=DARK,clip_on=False)

def panel_title(ax,title,x=0.0):
    ax.text(x,1.015,title,transform=ax.transAxes,ha='left',va='bottom',fontsize=8.1,color=DARK)

def finish(ax):
    ax.tick_params(direction='out',length=2.5,width=0.6,pad=2.0)
    ax.spines['left'].set_color(DARK); ax.spines['bottom'].set_color(DARK)

def save(fig,out,stem):
    out.mkdir(parents=True,exist_ok=True)
    fig.savefig(out/f'{stem}.pdf',format='pdf',bbox_inches=None,pad_inches=0)
    fig.savefig(out/f'{stem}.svg',format='svg',bbox_inches=None,pad_inches=0)
    fig.savefig(out/f'{stem}.eps',format='eps',bbox_inches=None,pad_inches=0)
    fig.savefig(out/f'{stem}.png',format='png',dpi=300,bbox_inches=None,pad_inches=0)
    plt.close(fig)

def load_landscape(release):
    sys.path.insert(0,str(release/'source'))
    import janus_fourier_landscapes_v12 as J
    return J, J.dft_landscape('2H_MoSSe_Se-S-Se-S')
