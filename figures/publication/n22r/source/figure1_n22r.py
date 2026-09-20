from __future__ import annotations
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Arc
from scipy.spatial import ConvexHull

ROOT = Path(os.environ['N22R_RELEASE_ROOT'])
OUT = Path(os.environ['N22R_OUT'])
STYLE = Path(__file__).with_name('publication_n22r.mplstyle')
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

BLUE='#0072B2'; VERM='#D55E00'; DARK='#222222'; MID='#6F6F6F'; LIGHT='#C8C8C8'; GRID='#D8D8D8'; PALE='#DDECF4'
MM=25.4

def inch(mm): return mm/MM

def panel_label(ax, letter, x=-0.10, y=1.03):
    ax.text(x,y,f'({letter})',transform=ax.transAxes,ha='left',va='bottom',fontsize=9.2,fontweight='bold',color=DARK,clip_on=False)

def panel_title(ax,title,x=0.0):
    ax.text(x,1.015,title,transform=ax.transAxes,ha='left',va='bottom',fontsize=8.2,color=DARK)

def finish(ax):
    ax.tick_params(direction='out',length=2.5,width=0.6,pad=2)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(DARK); ax.spines['bottom'].set_color(DARK)

sys.path.insert(0,str(ROOT/'source'))
import janus_fourier_landscapes_v12 as J
L=J.dft_landscape('2H_MoSSe_Se-S-Se-S')
ad=pd.read_csv(ROOT/'data'/'canonical'/'asymmetry_global_check.csv')

fig=plt.figure(figsize=(inch(177.8),inch(78.0)))
gs=fig.add_gridspec(1,3,left=0.048,right=0.968,bottom=0.19,top=0.86,wspace=0.46,width_ratios=[1.08,1.16,1.30])
a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1]); c=fig.add_subplot(gs[0,2])

# Panel A: actual model geometry from the canonical shell-6 N=127 contact.
pos=J.make_hexagonal_flake(6)
theta=1.5
R=J.rotation_matrix(theta)
posr=pos@R.T
# faint substrate triangular lattice directions
extent=6.5
for k in np.arange(-7,8,1):
    y=k*np.sqrt(3)/2
    a.plot([-extent,extent],[y,y],color='#EEEEEE',lw=0.55,zorder=0)
    # families at +/-60 degrees
    xx=np.array([-extent,extent])
    a.plot(xx, np.sqrt(3)*xx + k*np.sqrt(3), color='#F1F1F1',lw=0.55,zorder=0)
    a.plot(xx,-np.sqrt(3)*xx + k*np.sqrt(3), color='#F1F1F1',lw=0.55,zorder=0)
# actual sites and hull
h=ConvexHull(posr)
cycle=np.r_[h.vertices,h.vertices[0]]
a.scatter(posr[:,0],posr[:,1],s=5.0,facecolor=PALE,edgecolor=BLUE,linewidth=0.50,zorder=2)
a.plot(posr[cycle,0],posr[cycle,1],color=BLUE,lw=1.15,zorder=3)
a.scatter([0],[0],s=18,color=DARK,zorder=5)
# loading direction +/-y uses the paper-wide directional color registry
for y2, col, lab in ((4.25, BLUE, r'$+y$'), (-4.25, VERM, r'$-y$')):
    a.add_patch(FancyArrowPatch((0,0),(0,y2),arrowstyle='-|>',mutation_scale=10,color=col,lw=1.15,zorder=5))
    a.text(0.28, y2 - 0.10*np.sign(y2), lab, color=col, fontsize=7.2, va='center')
# COM freedom shown as orthogonal double arrows near center-right
a.annotate('',xy=(3.20,0.65),xytext=(1.65,0.65),arrowprops=dict(arrowstyle='<->',color=DARK,lw=0.75))
a.annotate('',xy=(2.42,1.42),xytext=(2.42,-0.12),arrowprops=dict(arrowstyle='<->',color=DARK,lw=0.75))
a.text(3.05,-0.72,'COM free $(x,y)
# model contract text
a.text(0.97,0.82,r'$N=127
a.text(0.50,-0.035,'prepared state:\nlowest-energy zero-force minimum',transform=a.transAxes,ha='center',va='top',fontsize=6.3,color=MID,clip_on=False,
       bbox=dict(facecolor='white',edgecolor='none',pad=0.5,alpha=0.92))
a.set_aspect('equal'); a.set_xlim(-6.45,6.45); a.set_ylim(-5.85,5.85); a.axis('off')
panel_label(a,'a',x=-0.035); panel_title(a,'unguided $N=127$ contact',x=0.12)

# Panel B: published 2H GSFE from canonical Fourier coefficients.
u=np.linspace(0,1,241); v=np.linspace(0,1,241); U,V=np.meshgrid(u,v,indexing='xy')
XY=np.stack([U+0.5*V,(np.sqrt(3)/2)*V],axis=-1)
Z=L.potential(XY[...,0],XY[...,1]); vmax=float(np.max(np.abs(Z)))
im=b.contourf(U,V,Z,levels=np.linspace(-vmax,vmax,25),cmap='RdBu_r',extend='both')
b.contour(U,V,Z,levels=[0.0],colors=[DARK],linewidths=0.75)
b.text(0.66,0.69,'+',transform=b.transAxes,ha='center',va='center',fontsize=8.0,color='white',fontweight='bold')
b.text(0.10,0.90,'−',transform=b.transAxes,ha='center',va='center',fontsize=8.6,color=DARK,fontweight='bold')
b.text(0.92,0.11,'−',transform=b.transAxes,ha='center',va='center',fontsize=8.6,color=DARK,fontweight='bold')
b.set_xlabel(r'$u$ along $\mathbf{a}_1$'); b.set_ylabel(r'$v$ along $\mathbf{a}_2$'); b.set_aspect('equal',adjustable='box')
cb=fig.colorbar(im,ax=b,fraction=0.046,pad=0.035); cb.set_label(r'$U/E_0$'); cb.ax.tick_params(labelsize=7.0,width=0.5,length=2)
b.text(0.03,0.04,r'$E_0=6W_1$'+'\n'+r'$W=(7.9,0.1,0.1)$ meV',transform=b.transAxes,fontsize=6.6,color=DARK,ha='left',va='bottom',bbox=dict(facecolor='white',edgecolor='none',pad=1.2))
panel_label(b,'b',x=-0.10); panel_title(b,'published 2H MoSSe GSFE',x=0.07); finish(b)

# Panel C: translation-minimized inversion-odd content.
order=['2H_MoSSe_Se-S-Se-S','3R_MoSSe_Se-S-Se-S','3R_MoSSe_S-Se-Se-S','3R_MoSSe_Se-S-S-Se']
lab={'2H_MoSSe_Se-S-Se-S':'2H asym.','3R_MoSSe_Se-S-Se-S':'3R asym.','3R_MoSSe_S-Se-Se-S':'3R sym. I','3R_MoSSe_Se-S-S-Se':'3R sym. II'}
q=ad.set_index('key').loc[order]; y=np.arange(len(q))[::-1]
vals=q.rms.to_numpy(float); floor=1e-18; lv=np.log10(np.where(vals>0,vals,floor))
cols=[DARK,'#444444',MID,'#8A8A8A']; marks=['o','s','^','v']
for yi,val,x,col,mk in zip(y,vals,lv,cols,marks):
    c.plot(x,yi,marker=mk,ms=5.1,color=col,linestyle='none')
    txt='0' if val==0 else (f'{val:.1e}' if val<1e-12 else f'{val:.3f}')
    c.annotate(txt,(x,yi),xytext=(5,0),textcoords='offset points',va='center',fontsize=7.0,color=DARK)
c.set_yticks(y,[lab[k] for k in order]); c.set_xlim(-18.7,0.8); c.set_xticks([-18,-12,-6,0])
c.set_xlabel(r'$\log_{10}$ translation-minimized odd RMS'); c.grid(axis='x',color=GRID,lw=0.55)
row=q.loc['2H_MoSSe_Se-S-Se-S']; c.text(0.98,0.04,fr'$A_{{min}}={row.opt_min:.5f}$'+'\n'+fr'$\chi_1={row.chi1:.3f}$',transform=c.transAxes,fontsize=7.0,color=DARK,ha='right',va='bottom')
panel_label(c,'c',x=-0.11); panel_title(c,'non-removable odd sector',x=0.06); finish(c)

stem='Figure_1_credibility_registry_asymmetry_N22R'
for ext in ['pdf','svg','eps']:
    fig.savefig(OUT/f'{stem}.{ext}',format=ext,bbox_inches=None,pad_inches=0)
fig.savefig(OUT/f'{stem}.png',format='png',dpi=300,bbox_inches=None,pad_inches=0)
plt.close(fig)
print(stem)
,fontsize=6.7,color=DARK,ha='center',va='top',
       bbox=dict(facecolor='white',edgecolor='none',pad=0.8,alpha=0.92))
# model contract text
a.text(0.97,0.91,r'$N=127$'+'\n'+'k_perp = 0'+'\n'+r'$\theta=1.5$° reference',transform=a.transAxes,ha='right',va='top',fontsize=6.7,color=DARK,bbox=dict(facecolor='white',edgecolor='none',pad=1.2))
a.text(0.50,0.018,'prepared state:\nlowest-energy zero-force minimum',transform=a.transAxes,ha='center',va='bottom',fontsize=6.3,color=MID,bbox=dict(facecolor='white',edgecolor='none',pad=0.5))
a.set_aspect('equal'); a.set_xlim(-6.45,6.45); a.set_ylim(-5.85,5.85); a.axis('off')
panel_label(a,'a',x=-0.035); panel_title(a,'unguided $N=127$ contact',x=0.12)

# Panel B: published 2H GSFE from canonical Fourier coefficients.
u=np.linspace(0,1,241); v=np.linspace(0,1,241); U,V=np.meshgrid(u,v,indexing='xy')
XY=np.stack([U+0.5*V,(np.sqrt(3)/2)*V],axis=-1)
Z=L.potential(XY[...,0],XY[...,1]); vmax=float(np.max(np.abs(Z)))
im=b.contourf(U,V,Z,levels=np.linspace(-vmax,vmax,25),cmap='RdBu_r',extend='both')
b.contour(U,V,Z,levels=[0.0],colors=[DARK],linewidths=0.75)
b.text(0.66,0.69,'+',transform=b.transAxes,ha='center',va='center',fontsize=8.0,color='white',fontweight='bold')
b.text(0.10,0.90,'−',transform=b.transAxes,ha='center',va='center',fontsize=8.6,color=DARK,fontweight='bold')
b.text(0.92,0.11,'−',transform=b.transAxes,ha='center',va='center',fontsize=8.6,color=DARK,fontweight='bold')
b.set_xlabel(r'$u$ along $\mathbf{a}_1$'); b.set_ylabel(r'$v$ along $\mathbf{a}_2$'); b.set_aspect('equal',adjustable='box')
cb=fig.colorbar(im,ax=b,fraction=0.046,pad=0.035); cb.set_label(r'$U/E_0$'); cb.ax.tick_params(labelsize=7.0,width=0.5,length=2)
b.text(0.03,0.04,r'$E_0=6W_1$'+'\n'+r'$W=(7.9,0.1,0.1)$ meV',transform=b.transAxes,fontsize=6.6,color=DARK,ha='left',va='bottom',bbox=dict(facecolor='white',edgecolor='none',pad=1.2))
panel_label(b,'b',x=-0.10); panel_title(b,'published 2H MoSSe GSFE',x=0.07); finish(b)

# Panel C: translation-minimized inversion-odd content.
order=['2H_MoSSe_Se-S-Se-S','3R_MoSSe_Se-S-Se-S','3R_MoSSe_S-Se-Se-S','3R_MoSSe_Se-S-S-Se']
lab={'2H_MoSSe_Se-S-Se-S':'2H asym.','3R_MoSSe_Se-S-Se-S':'3R asym.','3R_MoSSe_S-Se-Se-S':'3R sym. I','3R_MoSSe_Se-S-S-Se':'3R sym. II'}
q=ad.set_index('key').loc[order]; y=np.arange(len(q))[::-1]
vals=q.rms.to_numpy(float); floor=1e-18; lv=np.log10(np.where(vals>0,vals,floor))
cols=[DARK,'#444444',MID,'#8A8A8A']; marks=['o','s','^','v']
for yi,val,x,col,mk in zip(y,vals,lv,cols,marks):
    c.plot(x,yi,marker=mk,ms=5.1,color=col,linestyle='none')
    txt='0' if val==0 else (f'{val:.1e}' if val<1e-12 else f'{val:.3f}')
    c.annotate(txt,(x,yi),xytext=(5,0),textcoords='offset points',va='center',fontsize=7.0,color=DARK)
c.set_yticks(y,[lab[k] for k in order]); c.set_xlim(-18.7,0.8); c.set_xticks([-18,-12,-6,0])
c.set_xlabel(r'$\log_{10}$ translation-minimized odd RMS'); c.grid(axis='x',color=GRID,lw=0.55)
row=q.loc['2H_MoSSe_Se-S-Se-S']; c.text(0.98,0.04,fr'$A_{{min}}={row.opt_min:.5f}$'+'\n'+fr'$\chi_1={row.chi1:.3f}$',transform=c.transAxes,fontsize=7.0,color=DARK,ha='right',va='bottom')
panel_label(c,'c',x=-0.11); panel_title(c,'non-removable odd sector',x=0.06); finish(c)

stem='Figure_1_credibility_registry_asymmetry_N22R'
for ext in ['pdf','svg','eps']:
    fig.savefig(OUT/f'{stem}.{ext}',format=ext,bbox_inches=None,pad_inches=0)
fig.savefig(OUT/f'{stem}.png',format='png',dpi=300,bbox_inches=None,pad_inches=0)
plt.close(fig)
print(stem)
+'\n'+'k_perp = 0'+'\n'+r'$\theta=1.5$° reference',transform=a.transAxes,ha='right',va='top',fontsize=6.7,color=DARK,
       bbox=dict(facecolor='white',edgecolor='none',pad=1.2,alpha=0.92))
a.text(0.50,0.018,'prepared state:\nlowest-energy zero-force minimum',transform=a.transAxes,ha='center',va='bottom',fontsize=6.3,color=MID,bbox=dict(facecolor='white',edgecolor='none',pad=0.5))
a.set_aspect('equal'); a.set_xlim(-6.45,6.45); a.set_ylim(-5.85,5.85); a.axis('off')
panel_label(a,'a',x=-0.035); panel_title(a,'unguided $N=127$ contact',x=0.12)

# Panel B: published 2H GSFE from canonical Fourier coefficients.
u=np.linspace(0,1,241); v=np.linspace(0,1,241); U,V=np.meshgrid(u,v,indexing='xy')
XY=np.stack([U+0.5*V,(np.sqrt(3)/2)*V],axis=-1)
Z=L.potential(XY[...,0],XY[...,1]); vmax=float(np.max(np.abs(Z)))
im=b.contourf(U,V,Z,levels=np.linspace(-vmax,vmax,25),cmap='RdBu_r',extend='both')
b.contour(U,V,Z,levels=[0.0],colors=[DARK],linewidths=0.75)
b.text(0.66,0.69,'+',transform=b.transAxes,ha='center',va='center',fontsize=8.0,color='white',fontweight='bold')
b.text(0.10,0.90,'−',transform=b.transAxes,ha='center',va='center',fontsize=8.6,color=DARK,fontweight='bold')
b.text(0.92,0.11,'−',transform=b.transAxes,ha='center',va='center',fontsize=8.6,color=DARK,fontweight='bold')
b.set_xlabel(r'$u$ along $\mathbf{a}_1$'); b.set_ylabel(r'$v$ along $\mathbf{a}_2$'); b.set_aspect('equal',adjustable='box')
cb=fig.colorbar(im,ax=b,fraction=0.046,pad=0.035); cb.set_label(r'$U/E_0$'); cb.ax.tick_params(labelsize=7.0,width=0.5,length=2)
b.text(0.03,0.04,r'$E_0=6W_1$'+'\n'+r'$W=(7.9,0.1,0.1)$ meV',transform=b.transAxes,fontsize=6.6,color=DARK,ha='left',va='bottom',bbox=dict(facecolor='white',edgecolor='none',pad=1.2))
panel_label(b,'b',x=-0.10); panel_title(b,'published 2H MoSSe GSFE',x=0.07); finish(b)

# Panel C: translation-minimized inversion-odd content.
order=['2H_MoSSe_Se-S-Se-S','3R_MoSSe_Se-S-Se-S','3R_MoSSe_S-Se-Se-S','3R_MoSSe_Se-S-S-Se']
lab={'2H_MoSSe_Se-S-Se-S':'2H asym.','3R_MoSSe_Se-S-Se-S':'3R asym.','3R_MoSSe_S-Se-Se-S':'3R sym. I','3R_MoSSe_Se-S-S-Se':'3R sym. II'}
q=ad.set_index('key').loc[order]; y=np.arange(len(q))[::-1]
vals=q.rms.to_numpy(float); floor=1e-18; lv=np.log10(np.where(vals>0,vals,floor))
cols=[DARK,'#444444',MID,'#8A8A8A']; marks=['o','s','^','v']
for yi,val,x,col,mk in zip(y,vals,lv,cols,marks):
    c.plot(x,yi,marker=mk,ms=5.1,color=col,linestyle='none')
    txt='0' if val==0 else (f'{val:.1e}' if val<1e-12 else f'{val:.3f}')
    c.annotate(txt,(x,yi),xytext=(5,0),textcoords='offset points',va='center',fontsize=7.0,color=DARK)
c.set_yticks(y,[lab[k] for k in order]); c.set_xlim(-18.7,0.8); c.set_xticks([-18,-12,-6,0])
c.set_xlabel(r'$\log_{10}$ translation-minimized odd RMS'); c.grid(axis='x',color=GRID,lw=0.55)
row=q.loc['2H_MoSSe_Se-S-Se-S']; c.text(0.98,0.04,fr'$A_{{min}}={row.opt_min:.5f}$'+'\n'+fr'$\chi_1={row.chi1:.3f}$',transform=c.transAxes,fontsize=7.0,color=DARK,ha='right',va='bottom')
panel_label(c,'c',x=-0.11); panel_title(c,'non-removable odd sector',x=0.06); finish(c)

stem='Figure_1_credibility_registry_asymmetry_N22R'
for ext in ['pdf','svg','eps']:
    fig.savefig(OUT/f'{stem}.{ext}',format=ext,bbox_inches=None,pad_inches=0)
fig.savefig(OUT/f'{stem}.png',format='png',dpi=300,bbox_inches=None,pad_inches=0)
plt.close(fig)
print(stem)
,fontsize=6.7,color=DARK,ha='center',va='top',
       bbox=dict(facecolor='white',edgecolor='none',pad=0.8,alpha=0.92))
# model contract text
a.text(0.97,0.91,r'$N=127$'+'\n'+'k_perp = 0'+'\n'+r'$\theta=1.5$° reference',transform=a.transAxes,ha='right',va='top',fontsize=6.7,color=DARK,bbox=dict(facecolor='white',edgecolor='none',pad=1.2))
a.text(0.50,0.018,'prepared state:\nlowest-energy zero-force minimum',transform=a.transAxes,ha='center',va='bottom',fontsize=6.3,color=MID,bbox=dict(facecolor='white',edgecolor='none',pad=0.5))
a.set_aspect('equal'); a.set_xlim(-6.45,6.45); a.set_ylim(-5.85,5.85); a.axis('off')
panel_label(a,'a',x=-0.035); panel_title(a,'unguided $N=127$ contact',x=0.12)

# Panel B: published 2H GSFE from canonical Fourier coefficients.
u=np.linspace(0,1,241); v=np.linspace(0,1,241); U,V=np.meshgrid(u,v,indexing='xy')
XY=np.stack([U+0.5*V,(np.sqrt(3)/2)*V],axis=-1)
Z=L.potential(XY[...,0],XY[...,1]); vmax=float(np.max(np.abs(Z)))
im=b.contourf(U,V,Z,levels=np.linspace(-vmax,vmax,25),cmap='RdBu_r',extend='both')
b.contour(U,V,Z,levels=[0.0],colors=[DARK],linewidths=0.75)
b.text(0.66,0.69,'+',transform=b.transAxes,ha='center',va='center',fontsize=8.0,color='white',fontweight='bold')
b.text(0.10,0.90,'−',transform=b.transAxes,ha='center',va='center',fontsize=8.6,color=DARK,fontweight='bold')
b.text(0.92,0.11,'−',transform=b.transAxes,ha='center',va='center',fontsize=8.6,color=DARK,fontweight='bold')
b.set_xlabel(r'$u$ along $\mathbf{a}_1$'); b.set_ylabel(r'$v$ along $\mathbf{a}_2$'); b.set_aspect('equal',adjustable='box')
cb=fig.colorbar(im,ax=b,fraction=0.046,pad=0.035); cb.set_label(r'$U/E_0$'); cb.ax.tick_params(labelsize=7.0,width=0.5,length=2)
b.text(0.03,0.04,r'$E_0=6W_1$'+'\n'+r'$W=(7.9,0.1,0.1)$ meV',transform=b.transAxes,fontsize=6.6,color=DARK,ha='left',va='bottom',bbox=dict(facecolor='white',edgecolor='none',pad=1.2))
panel_label(b,'b',x=-0.10); panel_title(b,'published 2H MoSSe GSFE',x=0.07); finish(b)

# Panel C: translation-minimized inversion-odd content.
order=['2H_MoSSe_Se-S-Se-S','3R_MoSSe_Se-S-Se-S','3R_MoSSe_S-Se-Se-S','3R_MoSSe_Se-S-S-Se']
lab={'2H_MoSSe_Se-S-Se-S':'2H asym.','3R_MoSSe_Se-S-Se-S':'3R asym.','3R_MoSSe_S-Se-Se-S':'3R sym. I','3R_MoSSe_Se-S-S-Se':'3R sym. II'}
q=ad.set_index('key').loc[order]; y=np.arange(len(q))[::-1]
vals=q.rms.to_numpy(float); floor=1e-18; lv=np.log10(np.where(vals>0,vals,floor))
cols=[DARK,'#444444',MID,'#8A8A8A']; marks=['o','s','^','v']
for yi,val,x,col,mk in zip(y,vals,lv,cols,marks):
    c.plot(x,yi,marker=mk,ms=5.1,color=col,linestyle='none')
    txt='0' if val==0 else (f'{val:.1e}' if val<1e-12 else f'{val:.3f}')
    c.annotate(txt,(x,yi),xytext=(5,0),textcoords='offset points',va='center',fontsize=7.0,color=DARK)
c.set_yticks(y,[lab[k] for k in order]); c.set_xlim(-18.7,0.8); c.set_xticks([-18,-12,-6,0])
c.set_xlabel(r'$\log_{10}$ translation-minimized odd RMS'); c.grid(axis='x',color=GRID,lw=0.55)
row=q.loc['2H_MoSSe_Se-S-Se-S']; c.text(0.98,0.04,fr'$A_{{min}}={row.opt_min:.5f}$'+'\n'+fr'$\chi_1={row.chi1:.3f}$',transform=c.transAxes,fontsize=7.0,color=DARK,ha='right',va='bottom')
panel_label(c,'c',x=-0.11); panel_title(c,'non-removable odd sector',x=0.06); finish(c)

stem='Figure_1_credibility_registry_asymmetry_N22R'
for ext in ['pdf','svg','eps']:
    fig.savefig(OUT/f'{stem}.{ext}',format=ext,bbox_inches=None,pad_inches=0)
fig.savefig(OUT/f'{stem}.png',format='png',dpi=300,bbox_inches=None,pad_inches=0)
plt.close(fig)
print(stem)
