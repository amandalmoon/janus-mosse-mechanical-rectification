from n18r_common import *

def figure5(root: Path, out: Path) -> None:
    vm=pd.read_csv(root/'data'/'canonical'/'vector_mode_map_F0_period.csv')
    fl=pd.read_csv(root/'data'/'canonical'/'floquet_conditioning_check.csv')
    Fvals=np.array(sorted(vm.F0.unique()),dtype=float); Pvals=np.array(sorted(vm.period.unique()),dtype=float)
    def pivot(col): return vm.pivot(index='period',columns='F0',values=col).loc[Pvals,Fvals].to_numpy()

    fig=plt.figure(figsize=(inch(177.8),inch(124.0)))
    gs=fig.add_gridspec(2,2,left=0.075,right=0.985,bottom=0.105,top=0.955,wspace=0.27,hspace=0.38)
    a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1],sharex=a,sharey=a); c=fig.add_subplot(gs[1,0])
    sub=gs[1,1].subgridspec(2,1,hspace=0.08)
    d1=fig.add_subplot(sub[0,0]); d2=fig.add_subplot(sub[1,0],sharex=d1)

    for ax,Z,letter,title,cmap_name,vmin_i,vmax_i in [
        (a,pivot('m'),'a',r'$m$ along $\mathbf{a}_1$','Blues',0,9),
        (b,pivot('n'),'b',r'$n$ along $\mathbf{a}_2$','Oranges_r',-9,0)]:
        bounds=np.arange(vmin_i-0.5,vmax_i+1.5,1)
        cmap=plt.get_cmap(cmap_name,len(bounds)-1)
        norm=BoundaryNorm(bounds,cmap.N)
        im=ax.imshow(Z,origin='lower',aspect='auto',
                     extent=[Fvals.min()-0.125,Fvals.max()+0.125,Pvals.min()-5,Pvals.max()+5],
                     cmap=cmap,norm=norm,interpolation='nearest')
        ax.set_xlabel(r'rocking amplitude $F_0^*$'); ax.set_ylabel(r'period $\tau^*$')
        cb=fig.colorbar(im,ax=ax,fraction=0.045,pad=0.018,ticks=np.arange(vmin_i,vmax_i+1,1))
        cb.ax.tick_params(labelsize=7.0,width=0.5,length=2)
        panel_label(ax,letter); panel_title(ax,title); finish(ax)
    b.tick_params(labelleft=False); b.set_ylabel('')

    q=vm[vm.period==40].sort_values('F0')
    c.step(q.F0,q.m,where='mid',color=BLUE,marker='o',ms=3.2,label=r'$m$')
    c.step(q.F0,q.n,where='mid',color=VERM,ls='--',marker='s',ms=3.0,label=r'$n$')
    c.axhline(0,color=LIGHT,lw=0.7)
    c.set_xlabel(r'$F_0^*$ at $\tau^*=40$'); c.set_ylabel('winding / cycle')
    c.legend(loc='upper left',ncol=2); panel_label(c,'c'); panel_title(c,'representative vector staircase'); finish(c)

    methods=['DOP853\n$10^{-9}$','DOP853\n$10^{-11}$','Radau\n$10^{-9}$']
    x=np.arange(len(fl))
    ref=float(fl.loc[(fl.method=='DOP853') & (np.isclose(fl.rtol,1e-11)),'rho'].iloc[0])
    ppm=(fl.rho.to_numpy()/ref-1)*1e6
    d1.plot(x,ppm,linestyle='none',marker='o',color=BLUE,ms=4.2)
    d1.axhline(0,color=LIGHT,lw=0.7)
    d1.set_ylabel(r'$\rho_F$ rel. dev. (ppm)')
    d1.text(0.98,0.84,r'$\rho_F\approx6.31\times10^{-22}$',transform=d1.transAxes,
            ha='right',va='top',fontsize=7.0,color=DARK)
    d1.tick_params(labelbottom=False)
    panel_label(d1,'d',x=-0.11,y=1.08); panel_title(d1,'cross-solver Floquet consistency'); finish(d1)

    d2.plot(x,fl.closure.to_numpy()*1e11,linestyle='none',marker='s',color=VERM,ms=4.0)
    d2.set_ylabel(r'closure ($10^{-11}$)'); d2.set_xticks(x,methods)
    d2.set_ylim(0, max(fl.closure*1e11)*1.25)
    finish(d2)
    save_figure(fig,out,'Figure_5_vector_mode_map_floquet_N18R')


def figure6(root: Path, out: Path) -> None:
    full=pd.read_csv(root/'data'/'canonical'/'thermal_stationary_series_N500.csv')
    pooled=pd.read_csv(root/'data'/'canonical'/'stationary_current_two_seed_pooled.csv')
    pooled=pooled[pooled.seed.astype(str)=='pooled'].copy()
    boot=pd.read_csv(root/'data'/'canonical'/'stationary_thermal_bootstrap_50k.csv')
    sign=pd.read_csv(root/'data'/'canonical'/'stationary_sign_target_bootstrap.csv')

    low=full[full['T']<0.5].copy()
    high=pooled.merge(boot[['T','u_ci_lo','u_ci_hi','v_ci_lo','v_ci_hi']],on='T',how='left')

    fig=plt.figure(figsize=(inch(177.8),inch(102.0)))
    gs=fig.add_gridspec(2,2,left=0.075,right=0.985,bottom=0.12,top=0.955,height_ratios=[1.18,1],
                        wspace=0.28,hspace=0.48)
    a=fig.add_subplot(gs[0,:]); b=fig.add_subplot(gs[1,0]); c=fig.add_subplot(gs[1,1])

    for comp,col,mk,lab,low_mean,low_lo,low_hi,high_mean,high_lo,high_hi in [
        ('u',BLUE,'o',r'$\langle u\rangle$',low.mean_u,low.u_ci_lo,low.u_ci_hi,high.mean_u,high.u_ci_lo,high.u_ci_hi),
        ('v',VERM,'s',r'$\langle v\rangle$',low.mean_v,low.v_ci_lo,low.v_ci_hi,high.mean_v,high.v_ci_lo,high.v_ci_hi)]:
        a.errorbar(low['T'],low_mean,yerr=np.vstack([low_mean-low_lo,low_hi-low_mean]),
                   marker=mk,mfc='white',mec=col,color=col,ls='-',lw=1.05,capsize=1.7,label=lab)
        a.errorbar(high['T'],high_mean,yerr=np.vstack([high_mean-high_lo,high_hi-high_mean]),
                   marker=mk,mfc=col,mec=col,color=col,ls='-',lw=1.05,capsize=1.7)
    a.axhline(0,color=LIGHT,lw=0.8)
    a.axvspan(0.49,0.71,color=VERY_LIGHT,zorder=0)
    a.text(0.60,0.94,'pooled two-seed band: N=1000',transform=a.get_xaxis_transform(),
           ha='center',va='top',fontsize=7.0,color=MID)
    a.set_xlim(0,0.72); a.set_xlabel(r'reduced temperature $T^*$')
    a.set_ylabel('mean lattice displacement / cycle')
    a.text(0.325, float(low.mean_u.iloc[-1])+0.10, r'$\langle u\rangle$', color=BLUE, fontsize=7.0, ha='left')
    a.text(0.325, float(low.mean_v.iloc[-1])-0.08, r'$\langle v\rangle$', color=VERM, fontsize=7.0, ha='left', va='top')
    a.text(0.53, 0.10, 'open: N=500   filled: pooled N=1000', transform=a.transAxes,
           fontsize=7.0, color=MID, ha='center')
    panel_label(a,'a',x=-0.055); panel_title(a,'stationary mean current with trajectory-level 95% intervals'); finish(a)

    ratio=pooled['T2'].to_numpy()/pooled['crit'].to_numpy()
    b.plot(pooled['T'],ratio,color=DARK,marker='o',ms=3.8)
    b.axhline(1,color=VERM,lw=0.9,ls='--')
    b.set_xlim(0.495,0.705); b.set_ylim(0,max(ratio)*1.08)
    b.set_xlabel(r'$T^*$'); b.set_ylabel(r'$T_H^2/T_{0.95}^2$')
    b.text(0.698,1.35,'threshold = 1',fontsize=7.0,color=VERM,ha='right',va='bottom')
    b.annotate(f'{ratio[-1]:.2f}×',xy=(pooled['T'].iloc[-1],ratio[-1]),xytext=(-18,7),textcoords='offset points',
               fontsize=7.0,color=DARK)
    panel_label(b,'b'); panel_title(b,'joint current remains separated from zero'); finish(b)

    c.plot(low['T'],low.P_v_negative_cycle,color=BLUE,marker='o',mfc='white',ms=3.2,lw=1.0,
           label=r'$P(v_{cycle}<0)$')
    c.plot(low['T'],low.P_target_cycle,color=VERM,marker='s',mfc='white',ms=3.0,lw=1.0,ls='--',
           label=r'$P[(m,n)=(1,-1)]$')
    c.errorbar(sign['T'],sign.Pneg,yerr=np.vstack([sign.Pneg-sign.Pneg_ci_lo,sign.Pneg_ci_hi-sign.Pneg]),
               color=BLUE,marker='o',mfc=BLUE,mec=BLUE,lw=1.0,capsize=1.5)
    c.errorbar(sign['T'],sign.Ptarget,yerr=np.vstack([sign.Ptarget-sign.Ptarget_ci_lo,sign.Ptarget_ci_hi-sign.Ptarget]),
               color=VERM,marker='s',mfc=VERM,mec=VERM,lw=1.0,ls='--',capsize=1.5)
    c.axhline(0.5,color=LIGHT,lw=0.8,ls=':')
    c.set_xlim(0,0.72); c.set_ylim(-0.02,1.02)
    c.set_xlabel(r'$T^*$'); c.set_ylabel('cycle probability')
    c.legend(loc='upper right')
    panel_label(c,'c'); panel_title(c,'directional bias survives after exact winding identity is lost'); finish(c)
    save_figure(fig,out,'Figure_6_thermal_stationary_hierarchy_N18R')
