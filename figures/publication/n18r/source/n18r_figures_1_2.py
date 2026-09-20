from n18r_common import *

# Explicit publication-source contract for deterministic linting and handoff.
# Styling and export implementation remain centralized in n18r_common.
plt.style.use(STYLE)
PUBLICATION_VECTOR_EXPORTS = (".pdf", ".svg", ".eps")
SAVEFIG_EXPORTER = save_figure

def load_landscapes(root: Path):
    sys.path.insert(0, str(root / 'source'))
    import janus_fourier_landscapes_v12 as J  # type: ignore
    ns = {'__file__': str(root / 'audit_scripts' / 'matched_symmetry_audit.py')}
    code = (root / 'audit_scripts' / 'matched_symmetry_audit.py').read_text(encoding='utf-8').split('rows=[]')[0]
    exec(code, ns)
    return J, ns['centered'], ns['sym'], ns['inv']


def figure1(root: Path, out: Path) -> None:
    J, centered, sym, _ = load_landscapes(root)
    u = np.linspace(0, 1, 241)
    v = np.linspace(0, 1, 241)
    U, V = np.meshgrid(u, v, indexing='xy')
    XY = np.stack([U + 0.5*V, (np.sqrt(3)/2)*V], axis=-1)
    def gridpot(L):
        return L.potential(XY[..., 0], XY[..., 1])
    Z1, Z2 = gridpot(centered), gridpot(sym)
    vmax = float(max(np.max(np.abs(Z1)), np.max(np.abs(Z2))))
    levels = np.linspace(-vmax, vmax, 25)

    fig = plt.figure(figsize=(inch(177.8), inch(132.0)))
    gs = fig.add_gridspec(2, 2, left=0.085, right=0.925, bottom=0.085, top=0.96,
                          wspace=0.30, hspace=0.38)
    a = fig.add_subplot(gs[0, 0]); b = fig.add_subplot(gs[0, 1])
    c = fig.add_subplot(gs[1, 0]); d = fig.add_subplot(gs[1, 1])

    ims = []
    for ax, Z, letter, title in [
        (a, Z1, 'a', 'asymmetric 2H GSFE'),
        (b, Z2, 'b', 'matched inversion-even GSFE')]:
        im = ax.contourf(U, V, Z, levels=levels, cmap='RdBu_r', extend='both')
        ims.append(im)
        ax.set_xlabel(r'$u$ along $\mathbf{a}_1$')
        ax.set_ylabel(r'$v$ along $\mathbf{a}_2$')
        ax.set_aspect('equal', adjustable='box')
        panel_label(ax, letter); panel_title(ax, title); finish(ax)
    cb = fig.colorbar(ims[0], ax=[a, b], location='right', fraction=0.035, pad=0.018)
    cb.set_label(r'$U/E_0$')
    cb.ax.tick_params(labelsize=7.1, width=0.6, length=2.2)

    ad = pd.read_csv(root / 'data' / 'canonical' / 'asymmetry_global_check.csv')
    order_keys = ['2H_MoSSe_Se-S-Se-S', '3R_MoSSe_Se-S-Se-S', '3R_MoSSe_S-Se-Se-S', '3R_MoSSe_Se-S-S-Se']
    labmap = {
        '2H_MoSSe_Se-S-Se-S': '2H asym.',
        '3R_MoSSe_Se-S-Se-S': '3R asym.',
        '3R_MoSSe_S-Se-Se-S': '3R sym. I',
        '3R_MoSSe_Se-S-S-Se': '3R sym. II',
    }
    q = ad.set_index('key').loc[order_keys]
    y = np.arange(len(q))[::-1]
    vals = q['rms'].to_numpy(float)
    display_floor = 1e-18
    logvals = np.log10(np.where(vals > 0, vals, display_floor))
    colors = [BLUE, DARK, MID, MID]
    markers = ['o', 's', '^', 'v']
    for yi, val, lv, col, mk in zip(y, vals, logvals, colors, markers):
        c.plot(lv, yi, marker=mk, ms=5.0, color=col, mec=col, linestyle='none')
        txt = '0' if val == 0 else (f'{val:.1e}' if val < 1e-12 else f'{val:.3f}')
        c.annotate(txt, (lv, yi), xytext=(5, 0), textcoords='offset points',
                   va='center', ha='left', fontsize=7.0, color=DARK)
    c.set_yticks(y, [labmap[k] for k in order_keys])
    c.set_xlim(-18.7, -0.15)
    c.set_xticks([-18, -12, -6, 0])
    c.set_xlabel(r'$\log_{10}$ odd RMS fraction')
    c.set_ylim(-0.6, len(q)-0.4)
    c.grid(axis='x', color=GRID, linewidth=0.55)
    panel_label(c, 'c'); panel_title(c, 'non-removable registry asymmetry'); finish(c)

    md = pd.read_csv(root / 'data' / 'canonical' / 'matched_symmetry_final.csv')
    g = md[md.min_id.astype(str) == 'GLOBAL'].set_index('landscape').loc[
        ['2H_centered', '2H_matched_symmetrized', '2H_exact_inverted']]
    names = ['original', 'matched\nsym.', 'exact\ninversion']
    yy = np.arange(3)[::-1]
    for i, (_, row) in enumerate(g.iterrows()):
        yi = yy[i]
        d.plot([row.Fc_minus, row.Fc_plus], [yi, yi], color=LIGHT, lw=1.8, zorder=1)
        d.plot(row.Fc_plus, yi, 'o', color=BLUE, ms=5.0, zorder=3)
        d.plot(row.Fc_minus, yi, 's', color=VERM, ms=4.8, zorder=3)
        winding = f'({int(row.m_round)},{int(row.n_round)})'
        d.text(3.25, yi, winding, ha='left', va='center', fontsize=7.0, color=DARK)
    d.set_yticks(yy, names)
    d.set_xlim(0, 3.65)
    d.set_xlabel(r'global depinning threshold $F_c^*$')
    d.grid(axis='x', color=GRID, linewidth=0.55)
    d.text(0.60, 1.015, r'$\bullet\;F_{c,+}$', transform=d.transAxes,
           color=BLUE, fontsize=7.0, ha='left', va='bottom')
    d.text(0.79, 1.015, r'$\blacksquare\;F_{c,-}$', transform=d.transAxes,
           color=VERM, fontsize=7.0, ha='left', va='bottom')
    panel_label(d, 'd'); panel_title(d, 'symmetry-control thresholds'); finish(d)

    save_figure(fig, out, 'Figure_1_symmetry_contracts_N18R')


def figure2(root: Path, out: Path) -> None:
    fd = pd.read_csv(root / 'data' / 'canonical' / 'free_fold_nondegeneracy.csv')
    fd = fd[fd.theta <= 3.000001]
    bs = pd.read_csv(root / 'data' / 'canonical' / 'branch_family_summary.csv')

    fig = plt.figure(figsize=(inch(177.8), inch(124.0)))
    gs = fig.add_gridspec(2, 2, left=0.08, right=0.985, bottom=0.095, top=0.955,
                          wspace=0.27, hspace=0.38)
    a = fig.add_subplot(gs[0,0]); b = fig.add_subplot(gs[0,1], sharey=a)
    c = fig.add_subplot(gs[1,0]); d = fig.add_subplot(gs[1,1])

    for ax, sign, ground, color, letter, title in [
        (a, 1, fd.Ff, BLUE, 'a', r'$+y$ depinning'),
        (b, -1, fd.Fr, VERM, 'b', r'$-y$ depinning')]:
        q = bs[bs.sign == sign]
        ax.plot(fd.theta, ground, color=color, lw=1.45)
        ax.plot(q.theta, q.Fc_meta, marker='o', ms=3.6, mfc='white', mec=color,
                color=color, ls='--', lw=1.0)
        ax.axvline(1.5, color=LIGHT, lw=0.8, ls=':')
        ax.set_xlim(0, 3); ax.set_ylim(0, 3.65)
        ax.set_xlabel(r'twist $\theta$ (deg)')
        xlab = 2.22
        yg = float(np.interp(xlab, fd.theta.to_numpy(), np.asarray(ground)))
        ym = float(np.interp(xlab, q.theta.to_numpy(), q.Fc_meta.to_numpy()))
        ax.annotate('ground', (xlab, yg), xytext=(5, 5), textcoords='offset points',
                    fontsize=7.0, color=color, ha='left', va='bottom')
        ax.annotate('metastable', (xlab, ym), xytext=(5, 5), textcoords='offset points',
                    fontsize=7.0, color=color, ha='left', va='bottom')
        panel_label(ax, letter); panel_title(ax, title); finish(ax)
    a.set_ylabel(r'branch-followed threshold $F_c^*$')
    b.tick_params(labelleft=False)
    a.text(1.5, 3.18, r'$\theta=1.5^\circ$', ha='center', va='bottom', fontsize=7.0, color=MID)

    q = bs[bs.sign == 1].copy()
    margin_u = q.U_meta - q.U_ground
    c.plot(q.theta, margin_u, marker='o', color=DARK, mfc='white', ms=3.6)
    c.axhline(0, color=LIGHT, lw=0.8)
    c.fill_between(q.theta, 0, margin_u, where=margin_u>=0, color=GREEN_LIGHT, linewidth=0)
    c.axvline(1.5, color=LIGHT, lw=0.8, ls=':')
    c.set_xlim(0,3); c.set_ylim(bottom=0)
    c.set_xlabel(r'twist $\theta$ (deg)')
    c.set_ylabel(r'$U_{meta}-U_{ground}$')
    panel_label(c,'c'); panel_title(c,'prepared state remains lower in energy'); finish(c)

    p = bs[bs.sign == 1].copy(); n = bs[bs.sign == -1].copy()
    mp = p.Fc_ground - p.Fc_meta
    mn = n.Fc_ground - n.Fc_meta
    d.plot(p.theta, mp, marker='o', color=BLUE, ms=3.4, label=r'$+y$')
    d.plot(n.theta, mn, marker='s', color=VERM, ls='--', ms=3.3, label=r'$-y$')
    d.axhline(0, color=LIGHT, lw=0.8)
    d.axvline(1.5, color=LIGHT, lw=0.8, ls=':')
    d.set_xlim(0,3); d.set_ylim(bottom=0)
    d.set_xlabel(r'twist $\theta$ (deg)')
    d.set_ylabel(r'$F_c^{ground}-F_c^{meta}$')
    d.legend(loc='upper right')
    panel_label(d,'d'); panel_title(d,'prepared branch remains the last survivor'); finish(d)

    save_figure(fig, out, 'Figure_2_branch_resolved_depinning_N18R')
