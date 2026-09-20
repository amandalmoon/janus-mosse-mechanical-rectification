from pathlib import Path
_RELEASE_ROOT = Path(__file__).resolve().parents[1]
import sys, os, math
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
sys.path.insert(0,str(_RELEASE_ROOT/'source'))
import janus_fourier_landscapes_v12 as J
# load centered/sym/inv constructors without executing bottom
ns={}
code=open(_RELEASE_ROOT/'audit_scripts'/'matched_symmetry_audit.py').read().split('rows=[]')[0]
exec(code,ns)
centered, sym, inv = ns['centered'], ns['sym'], ns['inv']
A=np.column_stack([J.A1,J.A2])
OUT=_RELEASE_ROOT/'figures'; OUT.mkdir(parents=True,exist_ok=True)
RED='#B24A4A'; DARK='#262626'; GRAY='#777777'; LIGHT='#D9D9D9'; PALE='#F4EAEA'; BLUEGRAY='#5B6573'
plt.rcParams.update({'font.family':'Liberation Serif','font.size':8.4,'axes.titlesize':9,'axes.labelsize':8.5,'legend.fontsize':7.0,'xtick.labelsize':7.3,'ytick.labelsize':7.3,'axes.linewidth':0.8,'lines.linewidth':1.3,'savefig.bbox':'tight','mathtext.fontset':'dejavuserif'})

def panel(ax,label):
    ax.text(-0.13,1.05,f'({label})',transform=ax.transAxes,ha='left',va='top',fontweight='bold',fontsize=9)

def save(fig,name):
    fig.savefig(OUT/name,dpi=450,bbox_inches='tight',pad_inches=0.04)
    plt.close(fig)

# Figure 1
u=np.linspace(0,1,201); v=np.linspace(0,1,201); U,V=np.meshgrid(u,v,indexing='xy')
XY=np.stack([U+0.5*V,(np.sqrt(3)/2)*V],axis=-1)
def gridpot(L): return L.potential(XY[...,0],XY[...,1])
Z1=gridpot(centered); Z2=gridpot(sym)
fig,axs=plt.subplots(2,2,figsize=(7.2,5.4),constrained_layout=True)
for ax,Z,title,lab in [(axs[0,0],Z1,'Centered asymmetric 2H GSFE','a'),(axs[0,1],Z2,'Matched same-2H symmetrized GSFE','b')]:
    im=ax.contourf(U,V,Z,levels=24,cmap='RdBu_r'); ax.set_xlabel(r'$u$ along $\mathbf{a}_1$');ax.set_ylabel(r'$v$ along $\mathbf{a}_2$');ax.set_title(title); panel(ax,lab)
    cb=fig.colorbar(im,ax=ax,fraction=.046,pad=.03); cb.set_label(r'$u/E_0$')
ad=pd.read_csv(str(_RELEASE_ROOT/'data'/'canonical'/'asymmetry_global_check.csv'))
labels=['3R asym.','3R sym. I','3R sym. II','2H asym.']; vals=ad['rms'].values
ax=axs[1,0]; x=np.arange(4); ax.bar(x,vals,color=[GRAY,LIGHT,LIGHT,RED],edgecolor=DARK,linewidth=.6); ax.set_yscale('symlog',linthresh=1e-16); ax.set_ylim(-1e-17,.3); ax.set_xticks(x,labels,rotation=12); ax.set_ylabel('translation-minimized odd RMS fraction'); ax.set_title('Coordinate-invariant registry asymmetry'); panel(ax,'c')
md=pd.read_csv(str(_RELEASE_ROOT/'data'/'canonical'/'matched_symmetry_final.csv')); G=md[md.min_id.astype(str)=='GLOBAL']
order=['2H_centered','2H_matched_symmetrized','2H_exact_inverted']; names=['original','matched sym.','exact inversion']; idx=np.arange(3); width=.34
ax=axs[1,1]; gp=G.set_index('landscape').loc[order]
ax.bar(idx-width/2,gp.Fc_plus,width,color=RED,label=r'$F_{c,+}$'); ax.bar(idx+width/2,gp.Fc_minus,width,color=DARK,label=r'$F_{c,-}$'); ax.set_xticks(idx,names);ax.set_ylabel(r'branch/global threshold $F_c^*$'); ax.set_title('Matched symmetry contract at $\theta=1.5^\circ$'); ax.legend(frameon=False,ncol=2,loc='upper center'); panel(ax,'d')
for j,k in enumerate(order):
    r=gp.loc[k]
    ax.text(j,max(r.Fc_plus,r.Fc_minus)+.09,f'({int(r.m_round)},{int(r.n_round)})',ha='center',va='bottom',fontsize=7)
save(fig,'Figure_1_symmetry_contracts.png')

# Figure 2 branch resolved
fd=pd.read_csv('/mnt/data/janus_audit/free_fold_nondegeneracy.csv'); fd=fd[fd.theta<=3.000001]
bs=pd.read_csv(str(_RELEASE_ROOT/'data'/'canonical'/'branch_family_summary.csv'))
fig,axs=plt.subplots(2,2,figsize=(7.2,5.0),constrained_layout=True)
ax=axs[0,0]; ax.plot(fd.theta,fd.Ff,color=RED,label='ground-state branch'); pp=bs[bs.sign==1]; ax.plot(pp.theta,pp.Fc_meta,'o--',color=GRAY,ms=3,label='metastable branch'); ax.set(xlabel=r'twist $\theta$ (deg)',ylabel=r'$F_{c,+}^*$',title='Positive-y branch-followed depinning'); ax.legend(frameon=False);panel(ax,'a')
ax=axs[0,1]; ax.plot(fd.theta,fd.Fr,color=DARK,label='ground-state branch'); pp=bs[bs.sign==-1]; ax.plot(pp.theta,pp.Fc_meta,'o--',color=GRAY,ms=3,label='metastable branch');ax.set(xlabel=r'twist $\theta$ (deg)',ylabel=r'$F_{c,-}^*$',title='Negative-y branch-followed depinning');ax.legend(frameon=False);panel(ax,'b')
# energy families, use sign + rows only
pe=bs[bs.sign==1]; ax=axs[1,0]; ax.plot(pe.theta,pe.U_ground,color=RED,label='ground minimum'); ax.plot(pe.theta,pe.U_meta,color=DARK,ls='--',label='metastable minimum');ax.set(xlabel=r'twist $\theta$ (deg)',ylabel=r'zero-force energy $U^*$',title='Prepared ground state remains lowest');ax.legend(frameon=False);panel(ax,'c')
ax=axs[1,1]; pplus=bs[bs.sign==1]; pminus=bs[bs.sign==-1]; ax.plot(pplus.theta,pplus.Fc_ground-pplus.Fc_meta,color=RED,label='+y');ax.plot(pminus.theta,pminus.Fc_ground-pminus.Fc_meta,color=DARK,label='-y');ax.axhline(0,color=GRAY,lw=.8);ax.set(xlabel=r'twist $\theta$ (deg)',ylabel=r'$F_c^{ground}-F_c^{meta}$',title='Ground-state branch is the last survivor');ax.legend(frameon=False);panel(ax,'d')
save(fig,'Figure_2_branch_resolved_depinning.png')

# Figure 3 size/shape scaling
ss=pd.read_csv(str(_RELEASE_ROOT/'data'/'canonical'/'shape_scaling_extended.csv')); sm=pd.read_csv(str(_RELEASE_ROOT/'data'/'canonical'/'shape_scaling_metrics.csv'))
fig,axs=plt.subplots(2,2,figsize=(7.2,5.0),constrained_layout=True)
for family,ax,lab,title in [('hex',axs[0,0],'a','Compact hexagons: extended size collapse'),('disk',axs[0,1],'b','Disk-like compact contacts: collapse')]:
    sub=ss[ss.family==family]
    for N,g in sub.groupby('N'):
        ax.plot(g.Theta,g.Fp_norm,color=RED,alpha=.45,lw=.9)
        ax.plot(g.Theta,g.Fm_norm,color=DARK,alpha=.35,lw=.9,ls='--')
    ax.set(xlabel=r'scaled twist $\Theta=\theta\sqrt{N}$ (deg)',ylabel=r'$F_c(\Theta)/F_c(0)$',title=title);ax.set_ylim(.81,1.01);panel(ax,lab)
    if family=='hex': ax.text(.03,.08,'solid: +y\ndashed: -y',transform=ax.transAxes,fontsize=7)
ax=axs[1,0]
for scope,color,marker in [('hex',RED,'o'),('disk',DARK,'s')]:
    q=sm[sm.scope==scope]; ax.plot(q.Theta,100*q.Fp_max_rel,color=color,marker=marker,label=f'{scope} +y');ax.plot(q.Theta,100*q.Fm_max_rel,color=color,marker=marker,ls='--',label=f'{scope} -y')
ax.set(xlabel=r'$\Theta$',ylabel='max cross-size deviation (%)',title='Collapse error remains sub-percent');ax.legend(frameon=False,ncol=2);panel(ax,'c')
ax=axs[1,1]; q=sm[sm.scope=='hex_vs_disk']; ax.plot(q.Theta,100*np.abs(q.Fp_mean),color=RED,marker='o',label='+y');ax.plot(q.Theta,100*np.abs(q.Fm_mean),color=DARK,marker='s',label='-y');ax.set(xlabel=r'$\Theta$',ylabel='hex-vs-disk mean difference (%)',title='Compact-shape family means nearly coincide');ax.legend(frameon=False);panel(ax,'d')
save(fig,'Figure_3_extended_size_shape_similarity.png')

# Figure 4 boundary ground-state switching
tr=pd.read_csv(str(_RELEASE_ROOT/'data'/'canonical'/'triangle_ground_switch.csv')); ew=pd.read_csv(str(_RELEASE_ROOT/'data'/'canonical'/'edge_weight_ground_switch.csv'))
fig,axs=plt.subplots(2,2,figsize=(7.2,5.0),constrained_layout=True)
ax=axs[0,0]
for phi,color in [(20,RED),(25,DARK)]:
    q=tr[tr.phi==phi]; ax.plot(q.theta,q.UB-q.UA,'o-',ms=3,color=color,label=fr'$\phi_e={phi}^\circ$'); ax.axvline(q.energy_switch.iloc[0],color=color,ls=':',lw=.9)
ax.axhline(0,color=GRAY,lw=.8);ax.set(xlabel=r'twist $\theta$ (deg)',ylabel=r'$U_B-U_A$',title='Competing zero-force registry minima');ax.legend(frameon=False);panel(ax,'a')
ax=axs[0,1]
for phi,color in [(20,RED),(25,DARK)]:
    q=tr[tr.phi==phi]; ax.plot(q.theta,q.FAplus-q.FAminus,'o--',ms=2.5,color=color,alpha=.7); ax.plot(q.theta,q.FBplus-q.FBminus,'s-',ms=2.5,color=color,label=fr'$\phi_e={phi}^\circ$')
ax.axhline(0,color=GRAY,lw=.8);ax.set(xlabel=r'$\theta$ (deg)',ylabel=r'branch split $\Delta F_c^*$',title='Inversion-related branch families carry opposite bias');ax.legend(frameon=False);panel(ax,'b')
ax=axs[1,0]
for phi,color in [(20,RED),(25,DARK)]:
    q=tr[tr.phi==phi]; # split at switch to avoid connecting jump
    sw=q.energy_switch.iloc[0]
    q1=q[q.theta<sw]; q2=q[q.theta>=sw]
    ax.plot(q1.theta,q1.ground_delta,'o-',ms=3,color=color);ax.plot(q2.theta,q2.ground_delta,'s-',ms=3,color=color,label=fr'$\phi_e={phi}^\circ$');ax.axvline(sw,color=color,ls=':',lw=.9)
ax.axhline(0,color=GRAY,lw=.8);ax.set(xlabel=r'$\theta$ (deg)',ylabel=r'ground-state $\Delta F_c^*$',title='Ground-state registry switch reverses direction');ax.legend(frameon=False);panel(ax,'c')
ax=axs[1,1]
for phi,color,marker in [(20,RED,'o'),(25,DARK,'s')]:
    q=ew[ew.phi==phi];ax.plot(q.edge_weight,q.ground_switch_deg,marker=marker,color=color,label=fr'$\phi_e={phi}^\circ$')
ax.axhline(3,color=GRAY,ls=':',lw=.8);ax.set(xlabel='outer-site energy weight',ylabel='ground-state switch twist (deg)',title='Switch location is edge-model sensitive');ax.legend(frameon=False);panel(ax,'d')
save(fig,'Figure_4_boundary_registry_switching.png')

# Figure 5 vector mode map
vm=pd.read_csv(str(_RELEASE_ROOT/'data'/'canonical'/'vector_mode_map_F0_period.csv')); fl=pd.read_csv(str(_RELEASE_ROOT/'data'/'canonical'/'floquet_conditioning_check.csv'))
Fvals=sorted(vm.F0.unique()); Pvals=sorted(vm.period.unique())
def pivot(col): return vm.pivot(index='period',columns='F0',values=col).loc[Pvals,Fvals].values
fig,axs=plt.subplots(2,2,figsize=(7.2,5.0),constrained_layout=True)
for ax,Z,title,lab in [(axs[0,0],pivot('m'),'Winding $m$ along $\mathbf{a}_1$','a'),(axs[0,1],pivot('n'),'Winding $n$ along $\mathbf{a}_2$','b')]:
    im=ax.imshow(Z,origin='lower',aspect='auto',extent=[min(Fvals)-.125,max(Fvals)+.125,min(Pvals)-5,max(Pvals)+5],cmap='RdGy_r',interpolation='nearest'); ax.set(xlabel=r'rocking amplitude $F_0^*$',ylabel=r'period $\tau^*$',title=title); fig.colorbar(im,ax=ax,fraction=.046,pad=.03);panel(ax,lab)
ax=axs[1,0]; q=vm[vm.period==40];ax.step(q.F0,q.m,where='mid',color=RED,label='m');ax.step(q.F0,q.n,where='mid',color=DARK,label='n');ax.set(xlabel=r'$F_0^*$ at $\tau^*=40$',ylabel='lattice winding / cycle',title='Representative vector staircase');ax.legend(frameon=False);panel(ax,'c')
ax=axs[1,1]; methods=[f"DOP853\n1e-9",f"DOP853\n1e-11",f"Radau\n1e-9"]; ref=float(fl.rho.iloc[1]); ppm=(fl.rho/ref-1)*1e6; xx=np.arange(len(fl)); ax.plot(xx,ppm,'o-',color=RED,label=r'$\rho_F$ deviation'); ax.axhline(0,color=GRAY,ls=':',lw=.8); ax.set_xticks(xx,methods); ax.set_ylabel(r'$\rho_F$ deviation (ppm)'); ax.set_title('Floquet cross-solver consistency'); ax2=ax.twinx(); ax2.plot(xx,fl.closure*1e11,'s--',color=DARK,label='closure'); ax2.set_ylabel(r'closure ($10^{-11}$)'); panel(ax,'d')
save(fig,'Figure_5_vector_mode_map_floquet.png')

# Figure 6 thermal CIs
th=pd.read_csv(str(_RELEASE_ROOT/'data'/'canonical'/'free_thermal_cluster_ci_canonical.csv'))
fig,axs=plt.subplots(1,3,figsize=(7.2,2.45),constrained_layout=True)
ax=axs[0]; y=th.mean_v; lo=y-th.mean_v_ci_lo; hi=th.mean_v_ci_hi-y;ax.errorbar(th['T'],y,yerr=[lo,hi],fmt='o-',color=RED,capsize=2);ax.axhline(0,color=GRAY,ls=':',lw=.8);ax.set(xlabel=r'$T^*$',ylabel=r'mean lattice-$v$ / cycle',title='Vector current with trajectory-cluster CI');panel(ax,'a')
ax=axs[1];y=th.P_neg_y;lo=y-th.P_neg_y_ci_lo;hi=th.P_neg_y_ci_hi-y;ax.errorbar(th['T'],y,yerr=[lo,hi],fmt='o-',color=DARK,capsize=2);ax.axhline(.5,color=GRAY,ls=':',lw=.8);ax.set(xlabel=r'$T^*$',ylabel=r'$P(\Delta y<0)$',title='Cycle-direction probability');ax.set_ylim(.47,1.02);panel(ax,'b')
ax=axs[2];y=th.P_target;lo=y-th.P_target_ci_lo;hi=th.P_target_ci_hi-y;ax.errorbar(th['T'],y,yerr=[lo,hi],fmt='o-',color=RED,capsize=2);ax.set(xlabel=r'$T^*$',ylabel=r'$P[(m,n)=(1,-1)]$',title='Exact winding identity is fragile');ax.set_ylim(-.002,.095);panel(ax,'c')
save(fig,'Figure_6_thermal_cluster_uncertainty.png')
print('wrote',OUT)
