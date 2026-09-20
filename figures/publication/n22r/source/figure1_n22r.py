from __future__ import annotations
import os, sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from scipy.spatial import ConvexHull

ROOT = Path(os.environ['N22R_RELEASE_ROOT'])
OUT = Path(os.environ['N22R_OUT'])
STYLE = Path(__file__).with_name('publication_n22r.mplstyle')
plt.style.use(STYLE)
plt.rcParams.update({
    'font.size': 8.0,
    'axes.labelsize': 8.2,
    'axes.titlesize': 8.4,
    'xtick.labelsize': 7.3,
    'ytick.labelsize': 7.3,
    'legend.fontsize': 7.0,
    'axes.linewidth': 0.65,
    'lines.linewidth': 1.15,
    'lines.markersize': 4.0,
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

BLUE='#0072B2'; VERM='#D55E00'; DARK='#222222'; MID='#666666'; LIGHT='#C9C9C9'; GRID='#DDDDDD'; PALE='#F2F2F2'
MM=25.4

def inch(mm): return mm/MM

def panel_label(ax, letter, x=-0.08, y=1.025):
    ax.text(x,y,f'({letter})',transform=ax.transAxes,ha='left',va='bottom',fontsize=9.2,fontweight='bold',color=DARK,clip_on=False)

def panel_title(ax,title,x=0.03,y=1.012):
    ax.text(x,y,title,transform=ax.transAxes,ha='left',va='bottom',fontsize=8.5,color=DARK)

def finish(ax):
    ax.tick_params(direction='out',length=2.5,width=0.6,pad=2)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(DARK); ax.spines['bottom'].set_color(DARK)

sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
L=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
ad=pd.read_csv(ROOT/'data'/'canonical'/'asymmetry_global_check.csv')

fig=plt.figure(figsize=(inch(177.8),inch(80.0)))
gs=fig.add_gridspec(1,3,left=0.045,right=0.985,bottom=0.20,top=0.88,wspace=0.66,width_ratios=[1.00,1.00,1.30])
a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1]); c=fig.add_subplot(gs[0,2])

# (a) Actual shell-6 finite contact. Protocol details remain in the caption.
pos=J.make_hexagonal_flake(6)
theta=1.5
R=J.rotation_matrix(theta)
posr=pos@R.T
extent=6.4
for k in np.arange(-7,8,1):
    y=k*np.sqrt(3)/2
    a.plot([-extent,extent],[y,y],color='#EFEFEF',lw=0.45,zorder=0)
    xx=np.array([-extent,extent])
    a.plot(xx, np.sqrt(3)*xx+k*np.sqrt(3),color='#F3F3F3',lw=0.45,zorder=0)
    a.plot(xx,-np.sqrt(3)*xx+k*np.sqrt(3),color='#F3F3F3',lw=0.45,zorder=0)
h=ConvexHull(posr); cyc=np.r_[h.vertices,h.vertices[0]]
a.scatter(posr[:,0],posr[:,1],s=5.0,facecolor='white',edgecolor='#6E6E6E',linewidth=0.45,zorder=2)
a.plot(posr[cyc,0],posr[cyc,1],color='#4B4B4B',lw=1.2,zorder=3)
a.scatter([0],[0],s=17,color=DARK,zorder=5)
a.text(0.30,0.18,'COM',fontsize=7.1,color=DARK,ha='left',va='bottom')
for y2,col,lab,va,dy in [(4.35,BLUE,r'$+y$','bottom',0.05),(-4.35,VERM,r'$-y$','top',-0.05)]:
    a.add_patch(FancyArrowPatch((0,0),(0,y2),arrowstyle='-|>',mutation_scale=10.5,color=col,lw=1.25,zorder=5))
    a.text(0.24,y2+dy,lab,color=col,fontsize=7.5,ha='left',va=va)
a.set_aspect('equal'); a.set_xlim(-6.55,6.55); a.set_ylim(-5.65,5.65); a.axis('off')
panel_label(a,'a',x=-0.015); panel_title(a,'finite unguided contact',x=0.12)

# (b) DFT-anchored 2H GSFE. BrBG is used only as a continuous scalar map,
# separate from the paper-wide categorical direction colors.
u=np.linspace(0,1,241); v=np.linspace(0,1,241); U,V=np.meshgrid(u,v,indexing='xy')
XY=np.stack([U+0.5*V,(np.sqrt(3)/2)*V],axis=-1)
Z=L.potential(XY[...,0],XY[...,1]); vmax=float(np.max(np.abs(Z)))
levels=np.linspace(-vmax,vmax,25)
im=b.contourf(U,V,Z,levels=levels,cmap='BrBG',extend='both')
b.contour(U,V,Z,levels=[0.0],colors=[DARK],linewidths=0.75)
b.text(0.66,0.70,'+',transform=b.transAxes,ha='center',va='center',fontsize=8.2,color='white',fontweight='bold')
b.text(0.10,0.90,'−',transform=b.transAxes,ha='center',va='center',fontsize=8.6,color=DARK,fontweight='bold')
b.text(0.92,0.11,'−',transform=b.transAxes,ha='center',va='center',fontsize=8.6,color=DARK,fontweight='bold')
b.set_xlabel(r'$u$ along $\mathbf{a}_1$'); b.set_ylabel(r'$v$ along $\mathbf{a}_2$'); b.set_aspect('equal',adjustable='box')
cb=fig.colorbar(im,ax=b,fraction=0.040,pad=0.014,ticks=[-vmax,0,vmax])
cb.ax.set_title(r'$U/E_0
cb.ax.set_yticklabels([f'{-vmax:.2f}','0',f'{vmax:.2f}'])
panel_label(b,'b',x=-0.08,y=1.03); panel_title(b,'2H MoSSe GSFE input',x=0.07,y=1.015); finish(b)

# (c) Translation-minimized inversion-odd diagnostics on a true log axis.
order=['2H_MoSSe_Se-S-Se-S','3R_MoSSe_Se-S-Se-S','3R_MoSSe_S-Se-Se-S','3R_MoSSe_Se-S-S-Se']
lab={'2H_MoSSe_Se-S-Se-S':'2H asym.','3R_MoSSe_Se-S-Se-S':'3R asym.','3R_MoSSe_S-Se-Se-S':'3R sym. I','3R_MoSSe_Se-S-S-Se':'3R sym. II'}
q=ad.set_index('key').loc[order]
vals=q.rms.to_numpy(float)
zero_plot=1.25e-18
plotvals=np.where(vals>0,vals,zero_plot)
y=np.arange(4)[::-1]
c.axvspan(1e-18,1e-15,color=PALE,zorder=0)
c.text(2.8e-17,3.38,'numerical floor',ha='center',va='center',fontsize=7.0,color=MID)
marks=['o','s','^','v']; faces=[DARK,'#555555','white','white']; edges=[DARK,'#555555','#777777','#999999']
for yi,val,pv,mk,fc,ec in zip(y,vals,plotvals,marks,faces,edges):
    c.plot(pv,yi,marker=mk,ms=5.4,mfc=fc,mec=ec,mew=0.9,linestyle='none',zorder=3)
    if val==0:
        txt='0'; xtext=1.8e-18; ha='left'
    elif val < 1e-12:
        txt=f'{val:.1e}'; xtext=pv*2.1; ha='left'
    else:
        txt=f'{val:.3f}'; xtext=pv/1.55; ha='right'
    c.text(xtext,yi,txt,fontsize=7.0,color=DARK,ha=ha,va='center')
c.set_xscale('log'); c.set_xlim(5e-19,1)
c.set_yticks(y,[lab[k] for k in order])
c.set_xticks([1e-18,1e-12,1e-6,1])
c.set_xticklabels([r'$10^{-18}$',r'$10^{-12}$',r'$10^{-6}$',r'$10^{0}$'])
c.set_xlabel('translation-minimized odd RMS')
c.grid(axis='x',which='major',color=GRID,lw=0.55)
c.set_ylim(-0.35,3.55)
panel_label(c,'c',x=-0.055,y=1.025); panel_title(c,'inversion-odd content',x=0.07,y=1.012); finish(c)

stem='Figure_1_credibility_registry_asymmetry_N22R'
for ext in ['pdf','svg','eps']:
    fig.savefig(OUT/f'{stem}.{ext}',format=ext,bbox_inches=None,pad_inches=0)
fig.savefig(OUT/f'{stem}.png',format='png',dpi=300,bbox_inches=None,pad_inches=0)
plt.close(fig)
print(stem)
, fontsize=7.2, pad=2.5, color=DARK); cb.ax.tick_params(labelsize=7.0,width=0.5,length=2)
cb.ax.set_yticklabels([f'{-vmax:.2f}','0',f'{vmax:.2f}'])
panel_label(b,'b',x=-0.09,y=1.06); panel_title(b,'2H MoSSe GSFE input',x=0.06,y=1.045); finish(b)

# (c) Translation-minimized inversion-odd diagnostics on a true log axis.
order=['2H_MoSSe_Se-S-Se-S','3R_MoSSe_Se-S-Se-S','3R_MoSSe_S-Se-Se-S','3R_MoSSe_Se-S-S-Se']
lab={'2H_MoSSe_Se-S-Se-S':'2H asym.','3R_MoSSe_Se-S-Se-S':'3R asym.','3R_MoSSe_S-Se-Se-S':'3R sym. I','3R_MoSSe_Se-S-S-Se':'3R sym. II'}
q=ad.set_index('key').loc[order]
vals=q.rms.to_numpy(float)
zero_plot=1.25e-18
plotvals=np.where(vals>0,vals,zero_plot)
y=np.arange(4)[::-1]
c.axvspan(1e-18,1e-15,color=PALE,zorder=0)
c.text(2.8e-17,3.42,'numerical floor',ha='center',va='center',fontsize=7.0,color=MID)
marks=['o','s','^','v']; faces=[DARK,'#555555','white','white']; edges=[DARK,'#555555','#777777','#999999']
for yi,val,pv,mk,fc,ec in zip(y,vals,plotvals,marks,faces,edges):
    c.plot(pv,yi,marker=mk,ms=5.4,mfc=fc,mec=ec,mew=0.9,linestyle='none',zorder=3)
    if val==0:
        txt='0'; xtext=1.8e-18; ha='left'
    elif val < 1e-12:
        txt=f'{val:.1e}'; xtext=pv*2.1; ha='left'
    else:
        txt=f'{val:.3f}'; xtext=pv/1.55; ha='right'
    c.text(xtext,yi,txt,fontsize=7.0,color=DARK,ha=ha,va='center')
c.set_xscale('log'); c.set_xlim(5e-19,1)
c.set_yticks(y,[lab[k] for k in order])
c.set_xticks([1e-18,1e-12,1e-6,1])
c.set_xticklabels([r'$10^{-18}$',r'$10^{-12}$',r'$10^{-6}$',r'$10^{0}$'])
c.set_xlabel('translation-minimized odd RMS')
c.grid(axis='x',which='major',color=GRID,lw=0.55)
c.set_ylim(-0.35,3.55)
panel_label(c,'c',x=-0.065); panel_title(c,'inversion-odd content',x=0.05); finish(c)

stem='Figure_1_credibility_registry_asymmetry_N22R'
for ext in ['pdf','svg','eps']:
    fig.savefig(OUT/f'{stem}.{ext}',format=ext,bbox_inches=None,pad_inches=0)
fig.savefig(OUT/f'{stem}.png',format='png',dpi=300,bbox_inches=None,pad_inches=0)
plt.close(fig)
print(stem)
