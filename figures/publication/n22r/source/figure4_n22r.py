from __future__ import annotations
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(os.environ['N22R_RELEASE_ROOT'])
EXTRA = Path(os.environ['N22R_EXTRA_DATA'])
OUT = Path(os.environ['N22R_OUT'])
STYLE = Path(__file__).with_name('publication_n22r.mplstyle')
VECTOR_EXPORTS = ('.pdf', '.svg', '.eps')
plt.style.use(STYLE)
plt.rcParams.update({
    'font.size': 8.0,
    'axes.labelsize': 8.2,
    'axes.titlesize': 8.2,
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
    'savefig.pad_inches': 0,
})

FONT_FAMILY = os.environ.get('N22R_FONT_FAMILY', 'Arial')
plt.rcParams['font.family'] = FONT_FAMILY
if FONT_FAMILY.lower() == 'arial':
    plt.rcParams['font.sans-serif'] = ['Arial']

BLUE = '#0072B2'
VERM = '#D55E00'
DARK = '#222222'
MID = '#6F6F6F'
LIGHT = '#C8C8C8'
GRID = '#D8D8D8'
PALE_BLUE = '#A9D3E8'
PALE_VERM = '#F0B79C'
MM = 25.4

def inch(mm: float) -> float:
    return mm / MM

def panel_label(ax, letter: str, x=-0.10, y=1.035):
    ax.text(x, y, f'({letter})', transform=ax.transAxes, ha='left', va='bottom',
            fontsize=9.2, fontweight='bold', color=DARK, clip_on=False)

def panel_title(ax, title: str, x=0.0):
    ax.text(x, 1.015, title, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=8.2, color=DARK)

def finish(ax):
    ax.tick_params(direction='out', length=2.5, width=0.6, pad=2.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(DARK)
    ax.spines['bottom'].set_color(DARK)

shape = pd.read_csv(ROOT / 'data' / 'canonical' / 'shape_scaling_extended.csv')
metrics = pd.read_csv(ROOT / 'data' / 'canonical' / 'shape_scaling_metrics.csv')
elastic = pd.read_csv(EXTRA / 'n8_elastic_robustness_summary.csv')
modelcmp = pd.read_csv(EXTRA / 'n8_FEM_vs_VFF_comparison.csv')
matched = pd.read_csv(ROOT / 'data' / 'canonical' / 'matched_symmetry_final.csv')
rigid = matched[(matched.landscape == '2H_centered') & (matched.min_id.astype(str) == 'GLOBAL')].iloc[0]
Fp_rigid = float(rigid.Fc_plus)
Fm_rigid = float(rigid.Fc_minus)
rho_rigid = (Fp_rigid - Fm_rigid) / (Fp_rigid + Fm_rigid)

fig = plt.figure(figsize=(inch(177.8), inch(116.0)))
gs = fig.add_gridspec(2, 2, left=0.078, right=0.975, bottom=0.10, top=0.955,
                      wspace=0.28, hspace=0.40, height_ratios=[1.02, 0.98])
a = fig.add_subplot(gs[0,0])
b = fig.add_subplot(gs[0,1])
c = fig.add_subplot(gs[1,0])
d = fig.add_subplot(gs[1,1])

for family, filled, family_ls in [('hex', True, '-'), ('disk', False, ':')]:
    sub = shape[shape.family == family].copy()
    for col, color, marker in [('Fp_norm', BLUE, 'o'), ('Fm_norm', VERM, 's')]:
        for th, q in sub.groupby('Theta'):
            y = q[col].to_numpy(float)
            a.plot(np.full_like(y, float(th)), y, linestyle='none', marker=marker,
                   ms=2.6, mfc=((PALE_BLUE if col == 'Fp_norm' else PALE_VERM) if filled else 'white'),
                   mec=(PALE_BLUE if col == 'Fp_norm' else PALE_VERM), mew=0.55, zorder=1)
        g = sub.groupby('Theta')[col].mean().sort_index()
        a.plot(g.index.to_numpy(float), g.to_numpy(float), color=color,
               lw=1.35, ls=family_ls, marker=marker, ms=4.0,
               mfc=(color if filled else 'white'), mec=color, mew=0.8, zorder=4)

a.set_xlim(-0.5,20.5); a.set_ylim(0.82,1.012)
a.set_xticks([0,5,10,15,20])
a.set_xlabel(r'scaled twist $\Theta=\theta\sqrt{N}$ (deg)')
a.set_ylabel(r'normalized threshold $F_c(\Theta)/F_c(0)$')
a.grid(axis='y', color=GRID, lw=0.5)
leg_dir = [
    Line2D([0],[0], color=BLUE, marker='o', ls='-', lw=1.2, ms=3.8, label=r'$+y$'),
    Line2D([0],[0], color=VERM, marker='s', ls='--', lw=1.2, ms=3.6, label=r'$-y$'),
]
leg1 = a.legend(handles=leg_dir, loc='lower left', bbox_to_anchor=(0.00,0.00), ncol=2,
                handlelength=1.6, columnspacing=1.0, borderaxespad=0.2)
a.add_artist(leg1)
a.text(0.98,0.93,'filled = hex\nopen = disk', transform=a.transAxes,
       ha='right', va='top', fontsize=6.7, color=MID)
panel_label(a,'a'); panel_title(a,'compact contacts collapse under scaled twist'); finish(a)

rows=[]
for scope,label in [('hex','hex size'),('disk','disk size'),('hex_vs_disk','hex-disk mean')]:
    q=metrics[metrics.scope==scope]
    rows.append((label,100*q.Fp_max_rel.max(),100*q.Fm_max_rel.max()))
ypos=np.array([2,1,0],float)
for y,(label,vp,vm) in zip(ypos,rows):
    b.plot(vp,y,marker='o',ms=4.6,color=BLUE,linestyle='none',zorder=3)
    b.plot(vm,y,marker='s',ms=4.4,color=VERM,linestyle='none',zorder=3)
    b.plot([min(vp,vm),max(vp,vm)],[y,y],color=LIGHT,lw=1.0,zorder=1)
b.set_yticks(ypos,[r[0] for r in rows])
b.set_xlim(0,0.115); b.set_xticks([0,0.02,0.04,0.06,0.08,0.10])
b.set_xlabel(r'maximum deviation through $\Theta=20$ (%)')
b.grid(axis='x', color=GRID, lw=0.5)
b.legend(handles=leg_dir, loc='center right', handlelength=1.5, borderaxespad=0.2)
b.text(0.02,0.06,'deterministic sweep metric\n(not statistical uncertainty)',transform=b.transAxes,
       ha='left',va='bottom',fontsize=6.5,color=MID)
panel_label(b,'b'); panel_title(b,'residual size and shape dependence stays small'); finish(b)

xlabels=['0.5C','C','2C','100C','rigid']
x=np.arange(len(xlabels),dtype=float)
fem_cases=['C_half_1p5','C_nom_1p5','C_2x_1p5','C_100x_1p5']
fem=elastic[(elastic.model=='FEM') & (elastic.case.isin(fem_cases))].copy()
order={k:i for i,k in enumerate(fem_cases)}
fem['ord']=fem.case.map(order); fem=fem.sort_values('ord')
fp=np.r_[fem.Fp.to_numpy(float)/Fp_rigid,1.0]
fm=np.r_[fem.Fm.to_numpy(float)/Fm_rigid,1.0]
c.plot(x,fp,color=BLUE,marker='o',ms=4.2,mfc=BLUE,mec=BLUE,lw=1.3,zorder=3,label=r'$+y$ FEM')
c.plot(x,fm,color=VERM,marker='s',ms=4.0,mfc=VERM,mec=VERM,lw=1.2,ls='--',zorder=3,label=r'$-y$ FEM')
vff=elastic[(elastic.model=='VFF') & (elastic.theta==1.5)].copy()
for _,r in vff.iterrows():
    xi=0 if abs(float(r['case'].split('scale')[-1])-0.5)<1e-9 else 1
    c.plot(xi,float(r.Fp)/Fp_rigid,marker='o',ms=4.5,mfc='white',mec=BLUE,mew=1.0,linestyle='none',zorder=5)
    c.plot(xi,float(r.Fm)/Fm_rigid,marker='s',ms=4.3,mfc='white',mec=VERM,mew=1.0,linestyle='none',zorder=5)
c.axhline(1.0,color=LIGHT,lw=0.75,zorder=0)
c.set_xticks(x,xlabels); c.set_xlim(-0.35,4.35); c.set_ylim(0.895,1.006)
c.set_xlabel(r'in-plane stiffness condition, $\theta=1.5$°')
c.set_ylabel(r'$F_c/F_c^{\mathrm{rigid}}$')
c.text(0.98,0.16,'filled = FEM\nopen = nonlinear VFF',transform=c.transAxes,
       ha='right',va='bottom',fontsize=6.7,color=MID)
c.text(0.98,0.93,r'rigid reference = 1',transform=c.transAxes,ha='right',va='top',fontsize=6.6,color=MID)
panel_label(c,'c'); panel_title(c,'compliance renormalizes the absolute force scale'); finish(c)

rhof=np.r_[fem.rho.to_numpy(float),rho_rigid]
delta_f=100*(rhof/rho_rigid-1.0)
d.plot(x,delta_f,color=DARK,marker='o',ms=4.1,mfc=DARK,mec=DARK,lw=1.25,zorder=3,label='FEM')
for _,r in vff.iterrows():
    scale=float(r['case'].split('scale')[-1]); xi=0 if abs(scale-0.5)<1e-9 else 1
    dv=100*(float(r.rho)/rho_rigid-1.0)
    d.plot(xi,dv,marker='D',ms=4.2,mfc='white',mec=DARK,mew=0.9,linestyle='none',zorder=5)
d.axhline(0,color=LIGHT,lw=0.75,zorder=0)
d.set_xticks(x,xlabels); d.set_xlim(-0.35,4.35); d.set_ylim(-0.08,1.50)
d.set_xlabel(r'in-plane stiffness condition, $\theta=1.5$°')
d.set_ylabel(r'$100(\rho/\rho_{\mathrm{rigid}}-1)$ (%)')
d.text(0.03,0.08,'filled circle = FEM\nopen diamond = VFF',transform=d.transAxes,
       ha='left',va='bottom',fontsize=6.6,color=MID)
row15=modelcmp[np.isclose(modelcmp.theta,1.5)].iloc[0]
row30=modelcmp[np.isclose(modelcmp.theta,3.0)].iloc[0]
d.text(0.98,0.93,
       'FEM-VFF relative difference in $\\rho$\n'
       +fr'$0.014\%$ at 1.5°; $0.122\%$ at 3°',
       transform=d.transAxes,ha='right',va='top',fontsize=6.4,color=MID)
panel_label(d,'d'); panel_title(d,'directional split is stable across representations'); finish(d)

stem='Figure_4_compact_elastic_robustness_N22R'
OUT.mkdir(parents=True,exist_ok=True)
for ext in ['pdf','svg','eps']:
    fig.savefig(OUT/f'{stem}.{ext}',format=ext,bbox_inches=None,pad_inches=0)
fig.savefig(OUT/f'{stem}.png',format='png',dpi=300,bbox_inches=None,pad_inches=0)
plt.close(fig)
print(stem)
