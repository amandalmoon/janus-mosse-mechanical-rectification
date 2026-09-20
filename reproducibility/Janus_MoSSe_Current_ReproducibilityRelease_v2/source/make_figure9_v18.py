from pathlib import Path
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data'/'canonical'; FIG=ROOT/'figures'; FIG.mkdir(exist_ok=True)
roots=pd.read_csv(DATA/'v18_size_scaling_roots.csv')
col=pd.read_csv(DATA/'v18_size_similarity_collapse.csv')
edge=pd.read_csv(DATA/'v18_edge_factorization_curves.csv')
edge_m=pd.read_csv(DATA/'v18_edge_factorization_metrics.csv')
cont=pd.read_csv(DATA/'v18_amplitude_continuation.csv')
floq=pd.read_csv(DATA/'v18_relative_periodic_floquet.csv')
base=pd.read_csv(DATA/'v15_force_twist_factorization.csv')

plt.rcParams.update({'font.size':8.3,'axes.labelsize':8.5,'legend.fontsize':6.8,'xtick.labelsize':7.5,'ytick.labelsize':7.5,'font.family':'DejaVu Serif'})
fig,axs=plt.subplots(2,2,figsize=(7.2,5.7),constrained_layout=True)

# a size law
ax=axs[0,0]
x=roots.N.to_numpy(float); y=roots.W_D_abs_deg.to_numpy(float)
p=np.polyfit(np.log(x),np.log(y),1); xx=np.geomspace(x.min(),x.max(),300); yy=np.exp(p[1])*xx**p[0]
ax.loglog(x,y,'o',ms=4.0,label='DFT finite contacts')
ax.loglog(xx,yy,'-',lw=1.4,label=rf'$W_D\propto N^{{{p[0]:.3f}}}$')
ax.set_xlabel('contact size $N$'); ax.set_ylabel(r'$W_D$ (deg)')
ax.legend(frameon=False,loc='upper right')
ax.text(0.04,0.08,rf'$R^2_{{\log}}={1-np.sum((np.log(y)-np.polyval(p,np.log(x)))**2)/np.sum((np.log(y)-np.log(y).mean())**2):.6f}$'+'\n'+rf'$W_D\sqrt{{N}}={roots.W_sqrtN.mean():.3f}\pm{roots.W_sqrtN.std(ddof=1):.3f}^\circ$',transform=ax.transAxes,va='bottom')

# b similarity collapse
ax=axs[0,1]
Ns=sorted(col.N.unique())
for N in Ns:
    g=col[col.N==N]
    ax.plot(g.Theta_scaled,g.Fc_forward,lw=1.05,label=f'N={N}')
    ax.plot(g.Theta_scaled,g.Fc_reverse,lw=1.05,ls='--')
ax.set_xlabel(r'scaled twist $\Theta=\theta\sqrt{N}$ (deg)')
ax.set_ylabel(r'guided threshold $F_c^*$')
ax.legend(frameon=False,ncol=2,loc='upper right')
ax.text(0.04,0.06,'solid: forward\ndashed: reverse',transform=ax.transAxes,va='bottom')

# c edge-induced factorization breaking
ax=axs[1,0]
for phi in sorted(edge.edge_phi_deg.unique()):
    g=edge[edge.edge_phi_deg==phi]
    ax.plot(g.theta_deg,g.rho,lw=1.1,label=rf'$\phi_e={int(phi)}^\circ$')
ax.plot(base.theta_deg,base.rho,'k--',lw=1.1,label='hexagonal N=127')
ax.set_xlabel(r'twist $\theta$ (deg)'); ax.set_ylabel(r'normalized splitting $\rho(\theta)$')
ax.legend(frameon=False,ncol=2,loc='upper right')
inax=inset_axes(ax,width='43%',height='36%',loc='lower left',borderpad=1.15)
inax.plot(edge_m.edge_phi_deg,edge_m.max_factorization_error_percent,'o-',ms=3,lw=1)
inax.set_xlabel(r'$\phi_e$ (deg)',fontsize=6.5); inax.set_ylabel('max err. (%)',fontsize=6.5); inax.tick_params(labelsize=6)

# d nonlinear stability
ax=axs[1,1]
up=cont[cont.branch=='up'].sort_values('F0'); dn=cont[cont.branch=='down'].sort_values('F0')
ax.step(up.F0,up.winding,where='mid',lw=1.25,label='increasing $F_0^*$')
ax.plot(dn.F0,dn.winding,'o',ms=1.8,mfc='none',label='decreasing $F_0^*$')
ax.set_xlabel(r'rocking amplitude $F_0^*$'); ax.set_ylabel('winding / cycle')
ax.set_ylim(-4.5,.5); ax.legend(frameon=False,loc='lower left')
fin=inset_axes(ax,width='37%',height='34%',loc='upper right',borderpad=1.0)
fin.semilogy(floq.F0,floq.floquet_spectral_radius,'s-',ms=2.8,lw=.8)
fin.set_xlabel(r'$F_0^*$',fontsize=6.3); fin.set_ylabel(r'$\rho_F$',fontsize=6.3); fin.tick_params(labelsize=5.7); fin.set_ylim(1e-32,1e-10)
ax.text(0.49,0.08,'up/down mismatch: 0/101\nbasin mismatch: 0/24',transform=ax.transAxes,fontsize=6.0,va='bottom')

for lab,ax in zip(['(a)','(b)','(c)','(d)'],axs.flat):
    ax.text(0.02,0.97,lab,transform=ax.transAxes,ha='left',va='top',fontweight='bold',bbox=dict(facecolor='white',edgecolor='none',pad=1.2))
    ax.tick_params(direction='in',top=True,right=True)

pdf=FIG/'Figure_9_v18.pdf'; png=FIG/'Figure_9_v18.png'
fig.savefig(pdf,bbox_inches='tight')
fig.savefig(png,dpi=700,bbox_inches='tight')
print(pdf); print(png)
