from __future__ import annotations
import os, argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd

STYLE=Path(__file__).with_name('publication_n22r.mplstyle'); plt.style.use(STYLE)
plt.rcParams.update({'font.size':8.0,'axes.labelsize':8.3,'axes.titlesize':8.4,'xtick.labelsize':7.4,'ytick.labelsize':7.4,'legend.fontsize':7.2,'axes.linewidth':0.65,'lines.linewidth':1.2,'lines.markersize':4.0,'legend.frameon':False,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','savefig.bbox':None,'savefig.pad_inches':0.0})
FONT_FAMILY=os.environ.get('N22R_FONT_FAMILY','Arial'); plt.rcParams['font.family']=FONT_FAMILY
if FONT_FAMILY.lower()=='arial': plt.rcParams['font.sans-serif']=['Arial']
else:
    plt.rcParams['font.sans-serif']=[FONT_FAMILY]; plt.rcParams['mathtext.fontset']='dejavusans'
DARK='#222222'; MID='#666666'; LIGHT='#C9C9C9'; TEAL='#2A9D8F'; PURPLE='#8064A2'; MM=25.4

def inch(mm): return mm/MM

def panel_label(ax,letter,x=-0.055,y=1.030): ax.text(x,y,f'({letter})',transform=ax.transAxes,ha='left',va='bottom',fontsize=9.3,fontweight='bold',color=DARK,clip_on=False)
def panel_title(ax,title,x=0.060,y=1.015): ax.text(x,y,title,transform=ax.transAxes,ha='left',va='bottom',fontsize=8.4,color=DARK,clip_on=False)
def finish(ax):
    ax.tick_params(direction='out',length=2.5,width=0.6,pad=2.0); ax.spines['left'].set_color(DARK); ax.spines['bottom'].set_color(DARK)
def grid_edges(v):
    v=np.asarray(v,float); d=np.diff(v)
    if not np.allclose(d,d[0]): raise ValueError('regular grid required')
    return np.r_[v[0]-d[0]/2,v+d[0]/2]
def discrete_from(name,n,lo=0.18,hi=0.88,reverse=False):
    base=plt.get_cmap(name); vals=np.linspace(lo,hi,n)
    if reverse: vals=vals[::-1]
    return ListedColormap(base(vals))
def save(fig,out,stem):
    out.mkdir(parents=True,exist_ok=True)
    for ext in ['pdf','svg','eps']: fig.savefig(out/f'{stem}.{ext}',format=ext,bbox_inches=None,pad_inches=0)
    fig.savefig(out/f'{stem}.png',format='png',dpi=300,bbox_inches=None,pad_inches=0); plt.close(fig)

def make_figure(release,out):
    vm=pd.read_csv(release/'data'/'canonical'/'vector_mode_map_F0_period.csv'); fl=pd.read_csv(release/'data'/'canonical'/'floquet_conditioning_check.csv')
    F=np.array(sorted(vm.F0.unique()),float); P=np.array(sorted(vm.period.unique()),float)
    if len(vm)!=len(F)*len(P) or not bool(vm.locked.all()): raise AssertionError('vector-mode map contract changed')
    m=vm.pivot(index='period',columns='F0',values='m').loc[P,F].to_numpy(float); n=vm.pivot(index='period',columns='F0',values='n').loc[P,F].to_numpy(float)
    pinned=(m==0)&(n==0)
    if int(pinned.sum())!=21: raise AssertionError('pinned-state count changed')
    if (int(np.nanmin(m)),int(np.nanmax(m)))!=(0,10) or (int(np.nanmin(n)),int(np.nanmax(n)))!=(-9,0): raise AssertionError('winding range changed')
    fe,pe=grid_edges(F),grid_edges(P)

    fig=plt.figure(figsize=(inch(177.8),inch(124.0)))
    gs=fig.add_gridspec(2,2,left=0.080,right=0.935,bottom=0.105,top=0.925,wspace=0.30,hspace=0.48)
    a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1],sharex=a,sharey=a); c=fig.add_subplot(gs[1,0]); sub=gs[1,1].subgridspec(2,1,hspace=0.12); d1=fig.add_subplot(sub[0,0]); d2=fig.add_subplot(sub[1,0],sharex=d1)

    specs=[(a,m,'a',r'winding $m$ over drive map',0,10,'YlGnBu',False,[0,2,4,6,8,10]),(b,n,'b',r'winding $n$ over drive map',-9,0,'PuRd',True,[-9,-6,-3,0])]
    for ax,Z,letter,title,vmin,vmax,cmap_name,rev,ticks in specs:
        levels=np.arange(vmin-0.5,vmax+1.5,1.0); cmap=discrete_from(cmap_name,len(levels)-1,reverse=rev); norm=BoundaryNorm(levels,cmap.N)
        mesh=ax.pcolormesh(fe,pe,Z,cmap=cmap,norm=norm,shading='flat',edgecolors='white',linewidth=0.50,rasterized=False)
        py,px=np.where(pinned); ax.plot(F[px],P[py],linestyle='none',marker='x',color=DARK,ms=3.5,mew=0.75,zorder=5)
        ax.add_patch(Rectangle((1.875,35.0),0.25,10.0,fill=False,edgecolor=DARK,linewidth=1.15,zorder=6))
        ax.set_xlim(fe[0],fe[-1]); ax.set_ylim(pe[0],pe[-1]); ax.set_xlabel(r'rocking amplitude $F_0^*$'); ax.set_ylabel(r'period $\tau^*$'); ax.set_xticks(np.arange(1.0,4.01,0.5)); ax.set_yticks(np.arange(20,81,10))
        cb=fig.colorbar(mesh,ax=ax,fraction=0.048,pad=0.018,ticks=ticks); cb.ax.tick_params(labelsize=7.2,width=0.5,length=2.0)
        panel_label(ax,letter); panel_title(ax,title); finish(ax)
    b.tick_params(labelleft=False); b.set_ylabel('')

    q=vm[np.isclose(vm.period,40.0)].sort_values('F0')
    c.plot(q.F0,q.m,marker='o',ms=4.1,mfc=TEAL,mec=TEAL,color=TEAL,lw=1.10,label=r'$m$')
    c.plot(q.F0,q.n,marker='s',ms=3.9,mfc='white',mec=PURPLE,color=PURPLE,lw=1.05,ls='--',label=r'$n$')
    c.axhline(0,color=LIGHT,lw=0.7); c.axvspan(1.94,2.06,color='#F2F2F2',zorder=0)
    c.text(2.10,-5.20,'Floquet sample',fontsize=7.2,color=MID,ha='left',va='bottom')
    c.set_xlim(0.90,4.10); c.set_ylim(-5.7,6.7); c.set_xticks(np.arange(1.0,4.01,0.5)); c.set_xlabel(r'$F_0^*$ at $\tau^*=40$'); c.set_ylabel('integer winding / cycle'); c.legend(loc='upper left',ncol=2,columnspacing=1.0,handlelength=1.8,borderaxespad=0.25)
    panel_label(c,'c'); panel_title(c,r'vector staircase at $\tau^*=40$'); finish(c)

    labels=[r'DOP853'+'\n'+r'$10^{-9}$',r'DOP853'+'\n'+r'$10^{-11}$',r'Radau'+'\n'+r'$10^{-9}$']; x=np.arange(len(fl),dtype=float)
    ref=(fl.method=='DOP853')&(np.abs(fl.rtol.to_numpy(float)-1e-11)<1e-15)
    if int(ref.sum())!=1: raise AssertionError('Floquet reference row changed')
    rho_ref=float(fl.loc[ref,'rho'].iloc[0]); ppm=(fl.rho.to_numpy(float)/rho_ref-1)*1e6; clo=fl.closure.to_numpy(float)*1e11
    if float(np.max(np.abs(ppm)))>2.765: raise AssertionError('Floquet spread changed')
    d1.plot(x,ppm,linestyle='none',marker='o',mfc=DARK,mec=DARK,color=DARK,ms=4.3); d1.axhline(0,color=LIGHT,lw=0.7); d1.set_ylabel(r'$\rho_F$ rel. dev. (ppm)'); d1.set_ylim(-0.25,max(3.15,float(ppm.max())*1.10)); d1.tick_params(labelbottom=False)
    panel_label(d1,'d',x=-0.075,y=1.055); panel_title(d1,'Floquet consistency across solvers',x=0.075,y=1.035); finish(d1)
    d2.plot(x,clo,linestyle='none',marker='s',mfc='white',mec=MID,color=MID,ms=4.1); d2.set_ylabel(r'closure ($10^{-11}$)'); d2.set_xticks(x,labels); d2.set_ylim(0,max(2.15,float(clo.max())*1.10)); finish(d2)
    save(fig,out,'Figure_6_vector_mode_locking_N22R')

def main():
    p=argparse.ArgumentParser(); p.add_argument('--release',type=Path,required=True); p.add_argument('--out',type=Path,required=True); a=p.parse_args(); make_figure(a.release,a.out); return 0
if __name__=='__main__': raise SystemExit(main())
