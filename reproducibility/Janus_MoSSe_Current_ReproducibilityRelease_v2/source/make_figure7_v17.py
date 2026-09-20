"""Rebuild the DFT-material validation Figure 7 from canonical/recovered outputs."""
from __future__ import annotations
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "canonical"
FIG = ROOT / "figures"; FIG.mkdir(exist_ok=True)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import janus_fourier_landscapes_v12 as J
import dft_guided_material_v12 as M


def label(ax, s):
    ax.text(0.03, 0.95, s, transform=ax.transAxes, va="top", ha="left", fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.9, pad=1.4), zorder=20)


def main():
    diag = pd.read_csv(DATA / "v15_material_fourier_phase_diagnostics.csv")
    curves = pd.read_csv(DATA / "v15_material_threshold_curves.csv")
    low = pd.read_csv(DATA / "v15_low_noise_switching.csv")
    fit = pd.read_csv(DATA / "v15_low_noise_switching_logistic.csv")

    fig, axs = plt.subplots(2, 2, figsize=(9.2, 7.5), constrained_layout=True)
    ax=axs[0,0]
    keys=["3R_MoSSe_Se-S-Se-S","3R_MoSSe_S-Se-Se-S","3R_MoSSe_Se-S-S-Se","2H_MoSSe_Se-S-Se-S"]
    labs=["3R asym.","3R sym. I","3R sym. II","2H asym."]
    vals=[]
    for k in keys:
        g=diag[(diag.configuration==k)&(diag.shell==1)]
        vals.append(float(abs(g.chi_translation_invariant.iloc[0])))
    ax.bar(np.arange(4),vals,facecolor="white",edgecolor=["black","0.5","0.5","#b2182b"],linewidth=1.5)
    ax.set_xticks(np.arange(4),labs,rotation=15); ax.set_ylabel(r"$|\chi_1|=|\sin(3\phi_1)|$")
    label(ax,"(a)")

    ax=axs[0,1]
    for direction,ls,col in [("forward","-","black"),("reverse","--","#b2182b")]:
        g=curves[curves.direction==direction]
        ax.plot(g.theta_deg,g.Fc,ls=ls,color=col,lw=1.7,label=f"2H {direction}")
    sym=J.dft_landscape("3R_MoSSe_S-Se-Se-S")
    th=np.arange(0,3.0001,.1); rows=[]
    for t in th: rows.append(M.guided_threshold(float(t),sym,+1,25.0)["Fc"])
    ax.plot(th,rows,":",color="0.5",lw=1.7,label="3R symmetric control")
    ax.axhline(3.5,color="0.7",lw=0.8); ax.axvline(1.0099068387,color="#b2182b",ls=":",lw=1); ax.axvline(1.9444516264,color="black",ls=":",lw=1)
    ax.set(xlabel=r"twist $\theta$ (deg)",ylabel=r"guided depinning force $F_c^*$",xlim=(0,3))
    ax.legend(frameon=False,fontsize=8,loc="lower left"); label(ax,"(b)")

    # Material-case rocking response versus twist for the four production amplitudes.
    ax=axs[1,0]
    rock_path = ROOT / "legacy_v10_source" / "data" / "dft_2H_MoSSe_rocking_scan_k25_v12.csv"
    rock = pd.read_csv(rock_path)
    styles = {3.0:("0.5",":"), 3.5:("#b2182b","-"), 4.0:("black","--"), 4.5:("black","-.")}
    for amp in (3.0,3.5,4.0,4.5):
        g=rock[np.isclose(rock.F0,amp)].sort_values("theta_deg")
        col,ls=styles[amp]
        ax.plot(g.theta_deg,g.periods_per_cycle,ls=ls,color=col,lw=1.4,label=rf"$F_0^*={amp:.1f}$")
    ax.axhline(0,color="0.7",lw=.8)
    ax.set(xlabel=r"twist $\theta$ (deg)",ylabel="registry periods / cycle",xlim=(0,3))
    ax.legend(frameon=False,fontsize=7,loc="lower right",ncol=2); label(ax,"(c)")

    ax=axs[1,1]
    for T,ls in [(0.005,"-"),(0.010,"--")]:
        for direction,col in [("forward","black"),("reverse","#b2182b")]:
            g=low[(np.isclose(low.T_star,T))&(low.direction==direction)].sort_values("theta_deg")
            ax.plot(g.theta_deg,g.p_escape,"o",ms=3,mfc="white",color=col)
            fr=fit[(np.isclose(fit.T_star,T))&(fit.direction==direction)].iloc[0]
            xx=np.linspace(g.theta_deg.min(),g.theta_deg.max(),300)
            yy=1/(1+np.exp(-(xx-fr.theta50_deg)/fr.width_deg))
            ax.plot(xx,yy,color=col,ls=ls,lw=1.4,label=f"{direction}, T*={T:.3f}")
    ax.axhline(.5,color="0.7",lw=.8); ax.set(xlabel=r"twist $\theta$ (deg)",ylabel="half-cycle switching probability",ylim=(0,1.03))
    ax.legend(frameon=False,fontsize=7,loc="center right"); label(ax,"(d)")

    for ax in axs.flat: ax.tick_params(direction="in",top=True,right=True)
    fig.savefig(FIG/"Figure_7_v17.pdf",dpi=400,bbox_inches="tight")
    fig.savefig(FIG/"Figure_7_v17.png",dpi=400,bbox_inches="tight")
    print(FIG/"Figure_7_v17.png")

if __name__=="__main__": main()
