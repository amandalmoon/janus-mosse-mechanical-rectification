from n22_common import *

# Explicit publication-source contract for deterministic linting.
plt.style.use(STYLE)
apply_common_rc()
PUBLICATION_VECTOR_EXPORTS = ('.pdf', '.svg', '.eps')
SAVEFIG_EXPORTER = save

def figure5(release,out):
    tr=pd.read_csv(release/'data'/'canonical'/'triangle_ground_switch.csv'); ew=pd.read_csv(release/'data'/'canonical'/'edge_weight_ground_switch.csv')
    fig=plt.figure(figsize=(inch(177.8),inch(121))); gs=fig.add_gridspec(2,2,left=0.085,right=0.985,bottom=0.10,top=0.955,wspace=0.28,hspace=0.40)
    a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1]); c=fig.add_subplot(gs[1,0]); d=fig.add_subplot(gs[1,1]); styles=[(20,BLUE,'o'),(25,VERM,'s')]
    for phi,col,mk in styles:
        q=tr[tr.phi==phi]; sw=float(q.energy_switch.iloc[0]); a.plot(q.theta,q.UB-q.UA,color=col,marker=mk,ms=3.6,label=fr'$\phi_e={phi}^\circ$'); a.axvline(sw,color=col,ls=':',lw=0.8)
    a.axhline(0,color=LIGHT,lw=0.8); a.set_xlabel(r'twist $\theta$ (deg)'); a.set_ylabel(r'$U_B-U_A$'); a.legend(loc='lower left'); panel_label(a,'a'); panel_title(a,'registry-energy crossings'); finish(a)
    for phi,col,mk in styles:
        q=tr[tr.phi==phi]; b.plot(q.theta,q.FAplus-q.FAminus,color=col,marker='o',mfc='white',ms=3.3,ls='--'); b.plot(q.theta,q.FBplus-q.FBminus,color=col,marker='s',ms=3.3,ls='-')
    b.axhline(0,color=LIGHT,lw=0.8); b.set_xlabel(r'twist $\theta$ (deg)'); b.set_ylabel(r'branch split $\Delta F_c^*$'); b.legend(handles=[Line2D([0],[0],color=DARK,marker='o',mfc='white',ls='--',label='family A'),Line2D([0],[0],color=DARK,marker='s',ls='-',label='family B'),Line2D([0],[0],color=BLUE,lw=2,label=r'$\phi_e=20^\circ$'),Line2D([0],[0],color=VERM,lw=2,label=r'$\phi_e=25^\circ$')],loc='center',ncol=2,columnspacing=0.9,handlelength=1.6); panel_label(b,'b'); panel_title(b,'opposite bias of competing families'); finish(b)
    for phi,col,mk in styles:
        q=tr[tr.phi==phi].sort_values('theta'); sw=float(q.energy_switch.iloc[0]); pre=q[q.theta<sw]; post=q[q.theta>=sw]; c.plot(pre.theta,pre.ground_delta,color=col,marker='o',ms=3.5); c.plot(post.theta,post.ground_delta,color=col,marker='s',ms=3.5,label=fr'$\phi_e={phi}^\circ$'); c.axvline(sw,color=col,ls=':',lw=0.8)
    c.axhline(0,color=LIGHT,lw=0.8); c.set_xlabel(r'twist $\theta$ (deg)'); c.set_ylabel(r'prepared $\Delta F_c^*$'); c.legend(loc='center right'); panel_label(c,'c'); panel_title(c,'equilibrium preparation reverses the sign'); finish(c)
    for phi,col,mk in styles:
        q=ew[ew.phi==phi]; d.plot(q.edge_weight,q.ground_switch_deg,color=col,marker=mk,ms=3.8,label=fr'$\phi_e={phi}^\circ$')
    d.axhline(3,color=MID,ls=':',lw=0.8); d.axhspan(3,max(3.20,float(ew.ground_switch_deg.max())+0.02),color=VERY_LIGHT,zorder=0); d.text(0.53,3.035,'outside original 0–3° window',fontsize=7,color=MID,va='bottom'); d.set_ylim(2.68,3.21); d.set_xlabel('outer-site energy weight'); d.set_ylabel('equilibrium switch twist (deg)'); d.legend(loc='upper right'); panel_label(d,'d'); panel_title(d,'switch angle is edge-model sensitive'); finish(d)
    save(fig,out,'Figure_5_boundary_registry_switching_N22')

def figure6(release,out):
    vm=pd.read_csv(release/'data'/'canonical'/'vector_mode_map_F0_period.csv'); fl=pd.read_csv(release/'data'/'canonical'/'floquet_conditioning_check.csv')
    F=np.array(sorted(vm.F0.unique())); P=np.array(sorted(vm.period.unique())); pivot=lambda col: vm.pivot(index='period',columns='F0',values=col).loc[P,F].to_numpy()
    fig=plt.figure(figsize=(inch(177.8),inch(124))); gs=fig.add_gridspec(2,2,left=0.075,right=0.925,bottom=0.105,top=0.955,wspace=0.29,hspace=0.38)
    a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1],sharex=a,sharey=a); c=fig.add_subplot(gs[1,0]); sub=gs[1,1].subgridspec(2,1,hspace=0.08); d1=fig.add_subplot(sub[0,0]); d2=fig.add_subplot(sub[1,0],sharex=d1)
    for ax,Z,letter,title,cmap_name,vmin,vmax in [(a,pivot('m'),'a',r'$m$ along $\mathbf{a}_1$','Blues',0,9),(b,pivot('n'),'b',r'$n$ along $\mathbf{a}_2$','Oranges_r',-9,0)]:
        bounds=np.arange(vmin-0.5,vmax+1.5,1); cmap=plt.get_cmap(cmap_name,len(bounds)-1); norm=BoundaryNorm(bounds,cmap.N); im=ax.imshow(Z,origin='lower',aspect='auto',extent=[F.min()-0.125,F.max()+0.125,P.min()-5,P.max()+5],cmap=cmap,norm=norm,interpolation='nearest'); ax.set_xlabel(r'rocking amplitude $F_0^*$'); ax.set_ylabel(r'period $\tau^*$'); cb=fig.colorbar(im,ax=ax,fraction=0.045,pad=0.018,ticks=np.arange(vmin,vmax+1,1)); cb.ax.tick_params(labelsize=7,width=0.5,length=2); panel_label(ax,letter); panel_title(ax,title); finish(ax)
    b.tick_params(labelleft=False); b.set_ylabel('')
    q=vm[vm.period==40].sort_values('F0'); c.step(q.F0,q.m,where='mid',color=BLUE,marker='o',ms=3.2,label=r'$m$'); c.step(q.F0,q.n,where='mid',color=VERM,ls='--',marker='s',ms=3.0,label=r'$n$'); c.axhline(0,color=LIGHT,lw=0.7); c.set_xlabel(r'$F_0^*$ at $\tau^*=40$'); c.set_ylabel('winding / cycle'); c.legend(loc='upper left',ncol=2); panel_label(c,'c'); panel_title(c,'sampled vector staircase'); finish(c)
    x=np.arange(len(fl)); ref=float(fl.loc[(fl.method=='DOP853')&np.isclose(fl.rtol,1e-11),'rho'].iloc[0]); ppm=(fl.rho.to_numpy()/ref-1)*1e6; labels=['DOP853\n$10^{-9}$','DOP853\n$10^{-11}$','Radau\n$10^{-9}$']
    d1.plot(x,ppm,linestyle='none',marker='o',color=BLUE,ms=4.2); d1.axhline(0,color=LIGHT,lw=0.7); d1.set_ylabel(r'$\rho_F$ rel. dev. (ppm)'); d1.text(0.98,0.84,r'$\rho_F\approx6.31\times10^{-22}$',transform=d1.transAxes,ha='right',va='top',fontsize=7); d1.tick_params(labelbottom=False); panel_label(d1,'d',x=-0.11,y=1.08); panel_title(d1,'cross-solver Floquet consistency'); finish(d1)
    d2.plot(x,fl.closure.to_numpy()*1e11,linestyle='none',marker='s',color=VERM,ms=4); d2.set_ylabel(r'closure ($10^{-11}$)'); d2.set_xticks(x,labels); d2.set_ylim(0,max(fl.closure*1e11)*1.25); finish(d2)
    save(fig,out,'Figure_6_vector_mode_locking_N22')

def figure7(release,out):
    full=pd.read_csv(release/'data'/'canonical'/'thermal_stationary_series_N500.csv'); pooled=pd.read_csv(release/'data'/'canonical'/'stationary_current_two_seed_pooled.csv'); pooled=pooled[pooled.seed.astype(str)=='pooled'].copy(); boot=pd.read_csv(release/'data'/'canonical'/'stationary_thermal_bootstrap_50k.csv'); sign=pd.read_csv(release/'data'/'canonical'/'stationary_sign_target_bootstrap.csv')
    low=full[full['T']<0.5].copy(); high=pooled.merge(boot[['T','u_ci_lo','u_ci_hi','v_ci_lo','v_ci_hi']],on='T',how='left')
    fig=plt.figure(figsize=(inch(177.8),inch(102))); gs=fig.add_gridspec(2,2,left=0.09,right=0.985,bottom=0.12,top=0.955,height_ratios=[1.18,1],wspace=0.30,hspace=0.48); a=fig.add_subplot(gs[0,:]); b=fig.add_subplot(gs[1,0]); c=fig.add_subplot(gs[1,1])
    for col,mk,lab,lm,llo,lhi,hm,hlo,hhi in [(BLUE,'o',r'$\langle u\rangle$',low.mean_u,low.u_ci_lo,low.u_ci_hi,high.mean_u,high.u_ci_lo,high.u_ci_hi),(VERM,'s',r'$\langle v\rangle$',low.mean_v,low.v_ci_lo,low.v_ci_hi,high.mean_v,high.v_ci_lo,high.v_ci_hi)]:
        a.errorbar(low['T'],lm,yerr=np.vstack([lm-llo,lhi-lm]),marker=mk,mfc='white',mec=col,color=col,ls='-',lw=1.05,capsize=1.7,label=lab); a.errorbar(high['T'],hm,yerr=np.vstack([hm-hlo,hhi-hm]),marker=mk,mfc=col,mec=col,color=col,ls='-',lw=1.05,capsize=1.7)
    a.axhline(0,color=LIGHT,lw=0.8); a.axvspan(0.49,0.71,color=VERY_LIGHT,zorder=0); a.text(0.595,0.88,'pooled two-seed band: N=1000',transform=a.get_xaxis_transform(),ha='center',va='top',fontsize=7,color=MID); a.set_xlim(0,0.72); a.set_xlabel(r'reduced temperature $T^*$'); a.set_ylabel('mean lattice current'); a.text(0.53,0.10,'open: N=500   filled: pooled N=1000',transform=a.transAxes,fontsize=7,color=MID,ha='center'); a.legend(loc='upper right',bbox_to_anchor=(0.995,0.96)); panel_label(a,'a',x=-0.065); panel_title(a,'stationary mean current with trajectory-level 95% intervals'); finish(a)
    ratio=pooled.T2.to_numpy()/pooled.crit.to_numpy(); b.plot(pooled['T'],ratio,color=DARK,marker='o',ms=3.8); b.axhline(1,color=VERM,lw=0.9,ls='--'); b.set_xlim(0.495,0.705); b.set_xticks(pooled['T'].to_numpy(),[f'{t:.2f}' for t in pooled['T']]); b.set_ylim(0,max(ratio)*1.08); b.set_xlabel(r'$T^*$'); b.set_ylabel(r'$T_H^2/T_{0.95}^2$'); b.text(0.698,1.35,'threshold = 1',fontsize=7,color=VERM,ha='right',va='bottom'); panel_label(b,'b'); panel_title(b,'joint current remains separated from zero'); finish(b)
    c.plot(low['T'],low.P_v_negative_cycle,color=BLUE,marker='o',mfc='white',ms=3.2,lw=1,label=r'$P(v_{cycle}<0)$'); c.plot(low['T'],low.P_target_cycle,color=VERM,marker='s',mfc='white',ms=3,lw=1,ls='--',label=r'$P[(m,n)=(1,-1)]$'); c.errorbar(sign['T'],sign.Pneg,yerr=np.vstack([sign.Pneg-sign.Pneg_ci_lo,sign.Pneg_ci_hi-sign.Pneg]),color=BLUE,marker='o',mfc=BLUE,mec=BLUE,lw=1,capsize=1.5); c.errorbar(sign['T'],sign.Ptarget,yerr=np.vstack([sign.Ptarget-sign.Ptarget_ci_lo,sign.Ptarget_ci_hi-sign.Ptarget]),color=VERM,marker='s',mfc=VERM,mec=VERM,lw=1,ls='--',capsize=1.5); c.axhline(0.5,color=LIGHT,lw=0.8,ls=':'); c.set_xlim(0,0.72); c.set_ylim(-0.02,1.02); c.set_xlabel(r'$T^*$'); c.set_ylabel('cycle probability'); c.legend(loc='upper right'); panel_label(c,'c'); panel_title(c,'directional bias outlives exact mode identity'); finish(c)
    save(fig,out,'Figure_7_thermal_hierarchy_N22')
