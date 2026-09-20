# N26 Caption-to-N25 Source Synchronization

**Audit date:** 2026-09-20  
**N25 exact source head:** `4060d017a50c6387de45377621d9232529e7e4ad`  
**N26 manuscript branch:** `research-os/n26-manuscript-rewrite`

## Decision

**PASS.** Manuscript Figure 1-7 captions now describe the actual N25 source panels rather than the older N22 layout assumptions.

## Source authority

The N22 manifests remain the scientific evidence contract, but N25 changed visual structure in several figures without creating a separate `n22r/manifests` directory. Caption synchronization therefore used both:
1. N22 claim/evidence manifests, and
2. the exact N25 plotting source at the head above.

No figure claim, numerical result, or evidence role was changed.

## Figure-by-figure synchronization

| Figure | N25 source reality | Manuscript correction |
|---|---|---|
| FIG-01 | 3 panels: finite-contact schematic; 2H GSFE landscape; translation-minimized odd-RMS comparison | Caption fixed to three-panel structure; schematic explicitly non-evidentiary; plotting-floor zero retained as display-only |
| FIG-02 | Higher-order stability point is marked in panel (a); panel (d) is the prepared-branch survival margin | Removed any implication that the nongeneric marker lives in panel (d); caption now follows exact source |
| FIG-03 | Panel (a) is a matched three-landscape small-multiple set, not a text/schematic definition panel | Caption now describes original/symmetrized/inverted landscapes on one scale; panel (d) described as normalized symmetry-contract residuals |
| FIG-04 | Panel (d) plots percent change of rho relative to rigid, with FEM/VFF representation markers | Caption now describes the plotted quantity rather than only the qualitative conclusion |
| FIG-05 | Panels are U_B-U_A crossing, family split, prepared split, and switch twist vs outer-site weight | Caption wording aligned exactly to these four panel jobs |
| FIG-06 | Panel (d) is cross-solver consistency for the canonical (1,-1) orbit; additional plateau Floquet evidence is not plotted there | Caption now explicitly prevents the panel from implying Floquet certification of all 91 sampled states |
| FIG-07 | N25 redesign has four standalone panels: current overview, high-T 95% intervals, joint zero-current statistic, sign-vs-target hierarchy | Caption updated from older three-panel/inset grammar; stationary 60+100 protocol and N=500/N=1000 semantics are explicit |

## Boundary checks

- No caption claims physical polarity reversal.
- No caption turns sampled mode locking into a continuous phase diagram.
- No caption turns representative Floquet checks into 91-state certification.
- No caption infers a thermal critical temperature.
- No caption treats the edge-switch angle as a universal material constant.
- No caption upgrades in-plane FEM/VFF to full 3D atomistic validation.

**Caption-source synchronization gate: PASS.**
