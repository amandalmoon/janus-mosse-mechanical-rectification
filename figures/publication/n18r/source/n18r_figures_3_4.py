from n18r_common import *

def collapse_panel(ax, sub: pd.DataFrame, family_label: str, letter: str) -> None:
    grouped = sub.groupby('Theta')
    theta = np.array(sorted(sub.Theta.unique()), dtype=float)
    for direction, col, ls, marker, label in [
        ('Fp_norm', BLUE, '-', 'o', r'$+y$'),
        ('Fm_norm', VERM, '--', 's', r'$-y$')]:
        means = grouped[direction].mean().reindex(theta).to_numpy()
        lo = grouped[direction].min().reindex(theta).to_numpy()
        hi = grouped[direction].max().reindex(theta).to_numpy()
        ax.fill_between(theta, lo, hi, color=(BLUE_LIGHT if col == BLUE else VERM_LIGHT), linewidth=0)
        for _, g in sub.groupby('N'):
            ax.plot(g.Theta, g[direction], linestyle='none', marker=marker, ms=2.8,
                    mfc='white', mec=(BLUE if col == BLUE else VERM), mew=0.55)
        ax.plot(theta, means, color=col, ls=ls, marker=marker, ms=3.4, lw=1.35, label=label)
    ax.set_xlim(-0.6,20.6); ax.set_ylim(0.82,1.01)
    ax.set_xlabel(r'scaled twist $\Theta=\theta\sqrt{N}$ (deg)')
    ax.set_ylabel(r'$F_c(\Theta)/F_c(0)$')
    ax.legend(loc='lower left', ncol=2)
    panel_label(ax, letter); panel_title(ax, family_label); finish(ax)


def figure3(root: Path, out: Path) -> None:
    ss = pd.read_csv(root / 'data' / 'canonical' / 'shape_scaling_extended.csv')
    sm = pd.read_csv(root / 'data' / 'canonical' / 'shape_scaling_metrics.csv')
    fig = plt.figure(figsize=(inch(177.8), inch(120.0)))
    gs = fig.add_gridspec(2,2,left=0.085,right=0.985,bottom=0.10,top=0.955,wspace=0.27,hspace=0.38)
    a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1],sharey=a)
    c=fig.add_subplot(gs[1,0]); d=fig.add_subplot(gs[1,1])
    collapse_panel(a, ss[ss.family=='hex'], 'compact hexagons', 'a')
    collapse_panel(b, ss[ss.family=='disk'], 'disk-like compact contacts', 'b')
    b.tick_params(labelleft=False); b.set_ylabel('')

    for scope, mk, label in [('hex','o','hex'),('disk','s','disk')]:
        q=sm[sm.scope==scope]
        c.plot(q.Theta,100*q.Fp_max_rel,color=BLUE,marker=mk,ms=3.8,label=f'{label} +y')
        c.plot(q.Theta,100*q.Fm_max_rel,color=VERM,marker=mk,ms=3.6,ls='--',label=f'{label} -y')
    c.set_xlim(-0.6,20.6); c.set_ylim(0,0.09)
    c.set_xlabel(r'$\Theta$'); c.set_ylabel('maximum cross-size deviation (%)')
    c.legend(loc='upper left', ncol=2, columnspacing=1.0)
    c.annotate('max = 0.0818%', xy=(20, 100*sm[(sm.scope=='hex')&(sm.Theta==20)].Fp_max_rel.iloc[0]),
               xytext=(12.2,0.073), arrowprops=dict(arrowstyle='-', color=MID, lw=0.7),
               fontsize=7.0, color=DARK)
    panel_label(c,'c'); panel_title(c,'residual size dependence'); finish(c)

    q=sm[sm.scope=='hex_vs_disk']
    d.plot(q.Theta,100*np.abs(q.Fp_mean),color=BLUE,marker='o',ms=3.8,label=r'$+y$')
    d.plot(q.Theta,100*np.abs(q.Fm_mean),color=VERM,marker='s',ms=3.6,ls='--',label=r'$-y$')
    d.set_xlim(-0.6,20.6); d.set_ylim(0,0.10)
    d.set_xlabel(r'$\Theta$'); d.set_ylabel('hex-vs-disk mean difference (%)')
    d.legend(loc='upper left', ncol=2)
    d.annotate('max ≈ 0.087%', xy=(20,100*abs(q[q.Theta==20].Fp_mean.iloc[0])),
               xytext=(11.5,0.078), arrowprops=dict(arrowstyle='-', color=MID, lw=0.7),
               fontsize=7.0, color=DARK)
    panel_label(d,'d'); panel_title(d,'compact-shape agreement'); finish(d)
    save_figure(fig,out,'Figure_3_extended_size_shape_similarity_N18R')


def figure4(root: Path, out: Path) -> None:
    tr=pd.read_csv(root/'data'/'canonical'/'triangle_ground_switch.csv')
    ew=pd.read_csv(root/'data'/'canonical'/'edge_weight_ground_switch.csv')
    fig=plt.figure(figsize=(inch(177.8),inch(121.0)))
    gs=fig.add_gridspec(2,2,left=0.085,right=0.985,bottom=0.10,top=0.955,wspace=0.28,hspace=0.40)
    a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1]); c=fig.add_subplot(gs[1,0]); d=fig.add_subplot(gs[1,1])
    styles=[(20,BLUE,'o'),(25,VERM,'s')]

    for phi,col,mk in styles:
        q=tr[tr.phi==phi]
        sw=float(q.energy_switch.iloc[0])
        a.plot(q.theta,q.UB-q.UA,color=col,marker=mk,ms=3.6,label=fr'$\phi_e={phi}^\circ$')
        a.axvline(sw,color=col,ls=':',lw=0.8)
    a.axhline(0,color=LIGHT,lw=0.8)
    a.set_xlabel(r'twist $\theta$ (deg)'); a.set_ylabel(r'$U_B-U_A$')
    a.legend(loc='lower left'); panel_label(a,'a'); panel_title(a,'registry-energy crossings'); finish(a)

    for phi,col,mk in styles:
        q=tr[tr.phi==phi]
        b.plot(q.theta,q.FAplus-q.FAminus,color=col,marker='o',mfc='white',ms=3.3,ls='--')
        b.plot(q.theta,q.FBplus-q.FBminus,color=col,marker='s',ms=3.3,ls='-')
    b.axhline(0,color=LIGHT,lw=0.8)
    b.set_xlabel(r'twist $\theta$ (deg)'); b.set_ylabel(r'branch split $\Delta F_c^*$')
    b.legend(handles=[
        Line2D([0],[0],color=DARK,marker='o',mfc='white',ls='--',label='family A'),
        Line2D([0],[0],color=DARK,marker='s',ls='-',label='family B'),
        Line2D([0],[0],color=BLUE,lw=2,label=r'$\phi_e=20^\circ$'),
        Line2D([0],[0],color=VERM,lw=2,label=r'$\phi_e=25^\circ$')],
        loc='center',ncol=2,columnspacing=0.9,handlelength=1.6)
    panel_label(b,'b'); panel_title(b,'opposite bias of competing families'); finish(b)

    for phi,col,mk in styles:
        q=tr[tr.phi==phi].sort_values('theta')
        sw=float(q.energy_switch.iloc[0])
        pre=q[q.theta<sw]; post=q[q.theta>=sw]
        c.plot(pre.theta,pre.ground_delta,color=col,marker='o',ms=3.5)
        c.plot(post.theta,post.ground_delta,color=col,marker='s',ms=3.5,label=fr'$\phi_e={phi}^\circ$')
        c.axvline(sw,color=col,ls=':',lw=0.8)
    c.axhline(0,color=LIGHT,lw=0.8)
    c.set_xlabel(r'twist $\theta$ (deg)'); c.set_ylabel(r'prepared $\Delta F_c^*$')
    c.legend(loc='center right'); panel_label(c,'c'); panel_title(c,'equilibrium preparation reverses the sign'); finish(c)

    for phi,col,mk in styles:
        q=ew[ew.phi==phi]
        d.plot(q.edge_weight,q.ground_switch_deg,color=col,marker=mk,ms=3.8,label=fr'$\phi_e={phi}^\circ$')
    d.axhline(3.0,color=MID,ls=':',lw=0.8)
    d.axhspan(3.0, max(3.20,float(ew.ground_switch_deg.max())+0.02), color=VERY_LIGHT, zorder=0)
    d.text(0.53,3.035,'outside original 0–3° window',fontsize=7.0,color=MID,va='bottom')
    d.set_ylim(2.68,3.21)
    d.set_xlabel('outer-site energy weight'); d.set_ylabel('equilibrium switch twist (deg)')
    d.legend(loc='upper right'); panel_label(d,'d'); panel_title(d,'switch angle is edge-model sensitive'); finish(d)
    save_figure(fig,out,'Figure_4_boundary_registry_switching_N18R')
