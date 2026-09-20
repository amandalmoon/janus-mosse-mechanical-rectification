from n22_common import *

# Explicit publication-source contract for deterministic linting.
plt.style.use(STYLE)
apply_common_rc()
PUBLICATION_VECTOR_EXPORTS = ('.pdf', '.svg', '.eps')
SAVEFIG_EXPORTER = save

def figure1(release,out):
    J,L=load_landscape(release)
    ad=pd.read_csv(release/'data'/'canonical'/'asymmetry_global_check.csv')
    fig=plt.figure(figsize=(inch(177.8),inch(68)))
    gs=fig.add_gridspec(1,3,left=0.055,right=0.965,bottom=0.18,top=0.91,wspace=0.42,width_ratios=[1.0,1.15,1.25])
    a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1]); c=fig.add_subplot(gs[0,2])

    # A: explanatory model schematic (ILLUSTRATIVE, no quantitative evidence).
    a.set_aspect('equal'); a.set_xlim(-1.3,1.3); a.set_ylim(-1.3,1.3); a.axis('off')
    for yy in np.linspace(-1.0,1.0,7):
        a.plot([-1.15,1.15],[yy,yy],color='#E6E6E6',lw=0.5,zorder=0)
    for x0 in np.linspace(-1.5,1.5,8):
        a.plot([x0-0.7,x0+0.7],[-1.0,1.0],color='#EFEFEF',lw=0.45,zorder=0)
        a.plot([x0-0.7,x0+0.7],[1.0,-1.0],color='#EFEFEF',lw=0.45,zorder=0)
    ang=np.linspace(0,2*np.pi,7)[:-1]+np.pi/6+np.deg2rad(12)
    poly=np.c_[0.83*np.cos(ang),0.83*np.sin(ang)]
    a.add_patch(Polygon(poly,closed=True,facecolor=BLUE_LIGHT,edgecolor=BLUE,lw=1.2))
    a.scatter([0],[0],s=16,color=DARK,zorder=3)
    a.add_patch(FancyArrowPatch((0,0),(0,0.62),arrowstyle='-|>',mutation_scale=10,color=VERM,lw=1.1))
    a.add_patch(FancyArrowPatch((0,0),(0,-0.62),arrowstyle='-|>',mutation_scale=10,color=VERM,lw=1.1))
    a.text(0.08,0.64,r'$+y$',color=VERM,fontsize=7.2,ha='left'); a.text(0.08,-0.72,r'$-y$',color=VERM,fontsize=7.2,ha='left')
    a.annotate('',xy=(0.72,0.12),xytext=(0.42,-0.02),arrowprops=dict(arrowstyle='<->',color=DARK,lw=0.8))
    a.text(0.57,0.17,r'COM free in 2D',fontsize=7.0,color=DARK,ha='center')
    a.text(0,-1.12,'lowest-energy zero-force\nprepared state',ha='center',va='top',fontsize=7.0,color=MID)
    panel_label(a,'a',x=-0.06); panel_title(a,'unguided prepared contact',x=0.13)

    u=np.linspace(0,1,241); v=np.linspace(0,1,241); U,V=np.meshgrid(u,v,indexing='xy')
    XY=np.stack([U+0.5*V,(np.sqrt(3)/2)*V],axis=-1)
    Z=L.potential(XY[...,0],XY[...,1]); vmax=float(np.max(np.abs(Z)))
    im=b.contourf(U,V,Z,levels=np.linspace(-vmax,vmax,25),cmap='RdBu_r',extend='both')
    b.set_xlabel(r'$u$ along $\mathbf{a}_1$'); b.set_ylabel(r'$v$ along $\mathbf{a}_2$'); b.set_aspect('equal',adjustable='box')
    cb=fig.colorbar(im,ax=b,fraction=0.046,pad=0.035); cb.set_label(r'$U/E_0$'); cb.ax.tick_params(labelsize=7.0,width=0.5,length=2)
    panel_label(b,'b'); panel_title(b,'published 2H MoSSe GSFE'); finish(b)

    order=['2H_MoSSe_Se-S-Se-S','3R_MoSSe_Se-S-Se-S','3R_MoSSe_S-Se-Se-S','3R_MoSSe_Se-S-S-Se']
    lab={'2H_MoSSe_Se-S-Se-S':'2H asym.','3R_MoSSe_Se-S-Se-S':'3R asym.','3R_MoSSe_S-Se-Se-S':'3R sym. I','3R_MoSSe_Se-S-S-Se':'3R sym. II'}
    q=ad.set_index('key').loc[order]; y=np.arange(len(q))[::-1]
    vals=q.rms.to_numpy(float); floor=1e-18; lv=np.log10(np.where(vals>0,vals,floor))
    cols=[BLUE,DARK,MID,MID]; marks=['o','s','^','v']
    for yi,val,x,col,mk in zip(y,vals,lv,cols,marks):
        c.plot(x,yi,marker=mk,ms=5,color=col,linestyle='none')
        txt='0' if val==0 else (f'{val:.1e}' if val<1e-12 else f'{val:.3f}')
        c.annotate(txt,(x,yi),xytext=(5,0),textcoords='offset points',va='center',fontsize=7,color=DARK)
    c.set_yticks(y,[lab[k] for k in order]); c.set_xlim(-18.7,0.8); c.set_xticks([-18,-12,-6,0])
    c.set_xlabel(r'$\log_{10}$ translation-minimized odd RMS'); c.grid(axis='x',color=GRID,lw=0.55)
    row=q.loc['2H_MoSSe_Se-S-Se-S']; c.text(0.98,0.04,fr'$A_{{min}}={row.opt_min:.5f}$'+'\n'+fr'$\chi_1={row.chi1:.3f}$',transform=c.transAxes,fontsize=7.0,color=DARK,ha='right',va='bottom')
    panel_label(c,'c'); panel_title(c,'non-removable registry asymmetry'); finish(c)
    save(fig,out,'Figure_1_credibility_registry_asymmetry_N22')

def figure2(release,out):
    fd=pd.read_csv(release/'data'/'canonical'/'free_fold_nondegeneracy.csv'); fd=fd[fd.theta<=3.000001]
    bs=pd.read_csv(release/'data'/'canonical'/'branch_family_summary.csv')
    fig=plt.figure(figsize=(inch(177.8),inch(124)))
    gs=fig.add_gridspec(2,2,left=0.08,right=0.985,bottom=0.095,top=0.955,wspace=0.27,hspace=0.38)
    a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1],sharey=a); c=fig.add_subplot(gs[1,0]); d=fig.add_subplot(gs[1,1])
    for ax,sign,ground,color,letter,title in [(a,1,fd.Ff,BLUE,'a',r'$+y$ depinning'),(b,-1,fd.Fr,VERM,'b',r'$-y$ depinning')]:
        q=bs[bs.sign==sign]
        ax.plot(fd.theta,ground,color=color,lw=1.45)
        ax.plot(q.theta,q.Fc_meta,marker='o',ms=3.5,mfc='white',mec=color,color=color,ls='--',lw=1.0)
        ax.axvline(1.5,color=LIGHT,lw=0.8,ls=':'); ax.set_xlim(0,3); ax.set_ylim(0,3.65); ax.set_xlabel(r'twist $\theta$ (deg)')
        panel_label(ax,letter); panel_title(ax,title); finish(ax)
    a.set_ylabel(r'branch-followed threshold $F_c^*$'); b.tick_params(labelleft=False)
    a.legend(handles=[Line2D([0],[0],color=DARK,lw=1.4,label='prepared ground'),Line2D([0],[0],color=DARK,lw=1.0,ls='--',marker='o',mfc='white',ms=3.5,label='metastable')],loc='center right')
    q=bs[bs.sign==1].copy(); margin=q.U_meta-q.U_ground
    c.plot(q.theta,margin,marker='o',color=DARK,mfc='white',ms=3.5); c.axhline(0,color=LIGHT,lw=0.8); c.fill_between(q.theta,0,margin,where=margin>=0,color=GREEN_LIGHT,linewidth=0)
    c.axvline(1.5,color=LIGHT,lw=0.8,ls=':'); c.set_xlim(0,3); c.set_ylim(bottom=0); c.set_xlabel(r'twist $\theta$ (deg)'); c.set_ylabel(r'$U_{meta}-U_{ground}$')
    panel_label(c,'c'); panel_title(c,'prepared state remains lower in energy'); finish(c)
    p=bs[bs.sign==1]; n=bs[bs.sign==-1]; mp=p.Fc_ground-p.Fc_meta; mn=n.Fc_ground-n.Fc_meta
    d.plot(p.theta,mp,marker='o',color=BLUE,ms=3.4,label=r'$+y$'); d.plot(n.theta,mn,marker='s',color=VERM,ls='--',ms=3.3,label=r'$-y$')
    d.axhline(0,color=LIGHT,lw=0.8); d.axvline(1.5,color=LIGHT,lw=0.8,ls=':'); d.axvline(2.9733856558,color=PURPLE,lw=0.8,ls=':')
    d.annotate('higher-order\npoint',xy=(2.9734,float(np.interp(2.9734,p.theta,mp))),xytext=(-34,18),textcoords='offset points',fontsize=7.0,color=PURPLE,ha='right',arrowprops=dict(arrowstyle='-',color=PURPLE,lw=0.7))
    d.set_xlim(0,3); d.set_ylim(bottom=0); d.set_xlabel(r'twist $\theta$ (deg)'); d.set_ylabel(r'$F_c^{ground}-F_c^{meta}$'); d.legend(loc='upper right')
    panel_label(d,'d'); panel_title(d,'prepared branch remains last survivor'); finish(d)
    save(fig,out,'Figure_2_prepared_state_depinning_N22')
