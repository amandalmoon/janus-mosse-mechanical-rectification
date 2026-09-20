from n22_common import *

# Explicit publication-source contract for deterministic linting.
plt.style.use(STYLE)
apply_common_rc()
PUBLICATION_VECTOR_EXPORTS = ('.pdf', '.svg', '.eps')
SAVEFIG_EXPORTER = save

def figure3(release,out):
    md=pd.read_csv(release/'data'/'canonical'/'matched_symmetry_final.csv')
    ct=pd.read_csv(release/'data'/'canonical'/'matched_symmetry_final_contracts.csv').iloc[0]
    g=md[md.min_id.astype(str)=='GLOBAL'].set_index('landscape').loc[['2H_centered','2H_matched_symmetrized','2H_exact_inverted']]
    fig=plt.figure(figsize=(inch(177.8),inch(108)))
    gs=fig.add_gridspec(2,2,left=0.075,right=0.985,bottom=0.105,top=0.955,wspace=0.34,hspace=0.42)
    a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1]); c=fig.add_subplot(gs[1,0]); d=fig.add_subplot(gs[1,1])

    # A: intervention definition (ILLUSTRATIVE only; quantitative evidence is B-D).
    a.axis('off'); a.set_xlim(0,1); a.set_ylim(0,1)
    rows=[
        (0.78,'original',r'$U=U_{even}+U_{odd}$','odd sector retained',DARK),
        (0.50,'matched sym.',r'$U_{sym}=U_{even}$','odd sector removed',GREEN),
        (0.22,'exact inversion',r'$U_{inv}(\mathbf{r})=U(-\mathbf{r})$','odd sector reversed',PURPLE),
    ]
    for y0,name,formula,note,col in rows:
        a.plot([0.04,0.96],[y0-0.095,y0-0.095],color=VERY_LIGHT,lw=0.8)
        a.text(0.06,y0,name,ha='left',va='center',fontsize=7.6,fontweight='bold',color=col)
        a.text(0.42,y0,formula,ha='left',va='center',fontsize=8.0,color=DARK)
        a.text(0.42,y0-0.065,note,ha='left',va='center',fontsize=7.0,color=MID)
    a.text(0.06,0.03,'same 2H spectral content; controlled symmetry interventions',ha='left',va='bottom',fontsize=7.0,color=MID)
    panel_label(a,'a',x=-0.035); panel_title(a,'mechanism-isolating symmetry interventions',x=0.10)

    names=['original','matched\nsym.','exact\ninversion']; y=np.arange(3)[::-1]
    for i,(_,row) in enumerate(g.iterrows()):
        yi=y[i]; b.plot([row.Fc_minus,row.Fc_plus],[yi,yi],color=LIGHT,lw=1.8,zorder=1); b.plot(row.Fc_plus,yi,'o',color=BLUE,ms=5,zorder=3); b.plot(row.Fc_minus,yi,'s',color=VERM,ms=4.8,zorder=3)
    b.set_yticks(y,names); b.set_xlim(0,3.5); b.set_xlabel(r'global threshold $F_c^*$'); b.grid(axis='x',color=GRID,lw=0.55)
    b.legend(handles=[Line2D([0],[0],marker='o',color='none',markerfacecolor=BLUE,markeredgecolor=BLUE,label=r'$F_{c,+}$'),Line2D([0],[0],marker='s',color='none',markerfacecolor=VERM,markeredgecolor=VERM,label=r'$F_{c,-}$')],loc='center right')
    panel_label(b,'b'); panel_title(b,'static symmetry contract'); finish(b)

    colors=[DARK,GREEN,PURPLE]
    for (name,row),col in zip(g.iterrows(),colors):
        m=float(row.m_round); n=float(row.n_round)
        if abs(m)<1e-12 and abs(n)<1e-12:
            c.plot(0,0,marker='^',ms=6,color=col,linestyle='none'); c.text(0.05,0.05,'sym.',fontsize=7,color=col,ha='left',va='bottom')
        else:
            c.arrow(0,0,m,n,width=0.015,head_width=0.14,head_length=0.16,length_includes_head=True,color=col)
            c.text(m*1.05,n*1.05,{'2H_centered':'original','2H_exact_inverted':'inverted'}[name],fontsize=7,color=col,ha='left' if m>=0 else 'right',va='bottom' if n>=0 else 'top')
    c.axhline(0,color=LIGHT,lw=0.7); c.axvline(0,color=LIGHT,lw=0.7); c.set_xlim(-1.35,1.35); c.set_ylim(-1.35,1.35); c.set_aspect('equal',adjustable='box'); c.set_xlabel(r'$m$ per cycle'); c.set_ylabel(r'$n$ per cycle')
    panel_label(c,'c'); panel_title(c,'dynamic inversion contract'); finish(c)

    vals=np.array([ct.sym_global_static_split_abs,ct.inv_threshold_swap_plus_abs,ct.inv_threshold_swap_minus_abs,ct.inv_current_u_sum_abs,ct.inv_current_v_sum_abs,ct.sym_current_norm],float)
    labs=[r'sym. $|\Delta F_c|$',r'inv. swap $F_+$',r'inv. swap $F_-$',r'inv. current $u$',r'inv. current $v$',r'sym. current norm']
    yy=np.arange(len(vals))[::-1]
    d.scatter(vals,yy,s=20,color=DARK,zorder=3); d.set_xscale('log'); d.set_xlim(1e-18,2e-8); d.set_yticks(yy,labs); d.grid(axis='x',color=GRID,lw=0.55); d.set_xlabel('absolute symmetry residual')
    panel_label(d,'d'); panel_title(d,'numerical falsification residuals'); finish(d)
    save(fig,out,'Figure_3_same_spectrum_mechanism_N22')

def figure4(release,extra,out):
    ss=pd.read_csv(release/'data'/'canonical'/'shape_scaling_extended.csv'); sm=pd.read_csv(release/'data'/'canonical'/'shape_scaling_metrics.csv')
    fem=pd.read_csv(extra/'n8_elastic_linear_tight.csv'); vff=pd.read_csv(extra/'n8_vff_reconstructed.csv')
    md=pd.read_csv(release/'data'/'canonical'/'matched_symmetry_final.csv'); rigid=md[(md.landscape=='2H_centered')&(md.min_id.astype(str)=='GLOBAL')].iloc[0]
    rigid_rho=float((rigid.Fc_plus-rigid.Fc_minus)/(rigid.Fc_plus+rigid.Fc_minus))
    fig=plt.figure(figsize=(inch(177.8),inch(120)))
    gs=fig.add_gridspec(2,2,left=0.075,right=0.985,bottom=0.10,top=0.955,wspace=0.30,hspace=0.40)
    a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1]); c=fig.add_subplot(gs[1,0]); d=fig.add_subplot(gs[1,1])

    # A: raw compact-family evidence plus family means.
    for fam,mk in [('hex','o'),('disk','s')]:
        sub=ss[ss.family==fam]
        for _,gN in sub.groupby('N'):
            a.plot(gN.Theta,gN.Fp_norm,linestyle='none',marker=mk,ms=2.4,mfc='white',mec=BLUE,mew=0.45,alpha=1)
            a.plot(gN.Theta,gN.Fm_norm,linestyle='none',marker=mk,ms=2.4,mfc='white',mec=VERM,mew=0.45,alpha=1)
        grouped=sub.groupby('Theta'); th=np.array(sorted(sub.Theta.unique()),dtype=float)
        for colname,col,ls in [('Fp_norm',BLUE,'-'),('Fm_norm',VERM,'--')]:
            means=grouped[colname].mean().reindex(th).to_numpy()
            a.plot(th,means,color=col,ls=ls if fam=='hex' else ':',marker=mk,ms=3.2,lw=1.15)
    a.set_xlim(-0.5,20.5); a.set_ylim(0.82,1.01); a.set_xlabel(r'$\Theta=\theta\sqrt{N}$ (deg)'); a.set_ylabel(r'$F_c(\Theta)/F_c(0)$')
    a.legend(handles=[Line2D([0],[0],color=BLUE,marker='o',lw=1.1,label='hex +y'),Line2D([0],[0],color=VERM,marker='o',ls='--',lw=1.1,label='hex -y'),Line2D([0],[0],color=BLUE,marker='s',ls=':',lw=1.1,label='disk +y'),Line2D([0],[0],color=VERM,marker='s',ls=':',lw=1.1,label='disk -y')],ncol=2,loc='lower left',columnspacing=0.9,handlelength=1.6)
    panel_label(a,'a'); panel_title(a,'compact families collapse under scaled twist'); finish(a)

    metrics=[]
    for scope,label in [('hex','hex size'),('disk','disk size')]:
        q=sm[sm.scope==scope]; metrics.append((label,float(100*q.Fp_max_rel.max()),float(100*q.Fm_max_rel.max())))
    q=sm[sm.scope=='hex_vs_disk']; metrics.append(('hex-disk mean',float(100*np.abs(q.Fp_mean).max()),float(100*np.abs(q.Fm_mean).max())))
    yy=np.arange(len(metrics))[::-1]
    for yi,(lab,vp,vm) in zip(yy,metrics):
        b.plot(vp,yi,'o',color=BLUE,ms=4.5); b.plot(vm,yi,'s',color=VERM,ms=4.2)
    b.set_yticks(yy,[x[0] for x in metrics]); b.set_xlim(0,0.115); b.set_xlabel(r'maximum deviation through $\Theta=20$ (%)'); b.grid(axis='x',color=GRID,lw=0.55)
    b.legend(handles=[Line2D([0],[0],marker='o',color='none',markerfacecolor=BLUE,markeredgecolor=BLUE,label='+y'),Line2D([0],[0],marker='s',color='none',markerfacecolor=VERM,markeredgecolor=VERM,label='-y')],loc='center right',ncol=1)
    panel_label(b,'b'); panel_title(b,'residual size and shape dependence'); finish(b)

    # C-D: ordered categorical stiffness conditions avoid a fake continuous rigid-limit axis.
    x=np.arange(5,dtype=float); labels=['0.5C','C','2C','100C','rigid']
    fem_cases=['C_half_1p5','C_nom_1p5','C_2x_1p5','C_100x_1p5']
    fem_rows=[fem[fem.case==k].iloc[0] for k in fem_cases]
    fp=[float(r.Fp)/float(rigid.Fc_plus) for r in fem_rows]+[1.0]
    fm=[float(r.Fm)/float(rigid.Fc_minus) for r in fem_rows]+[1.0]
    rr=[float(r.rho) for r in fem_rows]+[rigid_rho]
    c.plot(x,fp,color=BLUE,marker='o',ms=4.2,lw=1.0,label=r'$+y$ FEM')
    c.plot(x,fm,color=VERM,marker='s',ms=4.0,lw=1.0,ls='--',label=r'$-y$ FEM')
    for sc,xi in [(0.5,0),(1.0,1)]:
        r=vff[(np.isclose(vff.theta,1.5))&(np.isclose(vff.scale,sc))].iloc[0]
        c.plot(xi+0.10,float(r.Fp)/float(rigid.Fc_plus),'o',mfc='white',mec=BLUE,ms=4.2)
        c.plot(xi+0.10,float(r.Fm)/float(rigid.Fc_minus),'s',mfc='white',mec=VERM,ms=4.0)
    c.axhline(1,color=LIGHT,lw=0.8); c.set_xticks(x,labels); c.set_xlim(-0.35,4.35); c.set_ylim(0.88,1.015); c.set_xlabel('in-plane stiffness condition'); c.set_ylabel(r'$F_c/F_c^{rigid}$ at $\theta=1.5^\circ$')
    c.legend(loc='lower right',ncol=2); c.text(0.03,0.05,'open markers: VFF\nfilled markers: FEM',transform=c.transAxes,fontsize=7.0,color=MID,ha='left',va='bottom')
    panel_label(c,'c'); panel_title(c,'compliance renormalizes the force scale'); finish(c)

    d.plot(x,rr,color=GREEN,marker='o',ms=4.2,lw=1.0,label='FEM')
    for sc,xi in [(0.5,0),(1.0,1)]:
        r=vff[(np.isclose(vff.theta,1.5))&(np.isclose(vff.scale,sc))].iloc[0]
        d.plot(xi+0.10,float(r.rho),'s',mfc='white',mec=GREEN,color=GREEN,ms=4.3,linestyle='none')
    d.axhline(rigid_rho,color=LIGHT,lw=0.8); d.set_xticks(x,labels); d.set_xlim(-0.35,4.35); d.set_ylim(0.416,0.426); d.set_xlabel('in-plane stiffness condition'); d.set_ylabel(r'normalized split $\rho$')
    d.text(0.03,0.05,'open square: VFF\nfilled circle: FEM',transform=d.transAxes,fontsize=7.0,color=MID,ha='left',va='bottom')
    panel_label(d,'d'); panel_title(d,'directional split persists across representations'); finish(d)
    save(fig,out,'Figure_4_compact_elastic_robustness_N22')
