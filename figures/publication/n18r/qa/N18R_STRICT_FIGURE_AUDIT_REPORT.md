# N18R Strict Figure Redesign Audit

## Scope

This gate reopens the publication-figure layer after the stricter publication-figure contract was introduced. Scientific simulation outputs are frozen; only evidence-preserving visual representation, figure provenance, and venue handoff are changed.

## FACT

- Figures 1-6 were rebuilt from the frozen current reproducibility release.
- Every evidence-bearing panel is tagged \`SIMULATION_EXECUTED\`; no placeholder or illustrative numerical values are used as evidence.
- Each figure now has a strict figure contract/manifest with panel role, question, evidence IDs, source paths, uncertainty handling, processing notes, final physical size, design system, exports, caption, and categorical QA.
- All figures are rendered at exactly 504 pt (177.8 mm) width. Heights are 374.173, 351.496, 340.157, 342.992, 351.496, and 289.134 pt for Figures 1-6 respectively.
- Minimum declared final text size is 7.0 pt. Primary line width is 1.2 pt; axes are 0.65 pt; all visible reference/grid lines are at least 0.55 pt.
- The strict plot-source audit passes.
- The strict benchmark package audit passes for all six figures with file existence checks.
- Final-size 96 dpi renders were opened and inspected for all six figures. No clipping, overlap, missing marks, ambiguous color-only critical encoding, or unreadable annotations were observed.
- Current ACS Nano guidance was rechecked on 2026-09-20. The online Author Guidelines report an update date of 2026-08-27. The ACS Nano checklist still specifies Arial lettering, >=6 pt final lettering, >=0.5 pt lines, final published size, and EPS for vector graphics.

## Major redesign changes

### Figure 1
Shared GSFE scale; direct log10 odd-RMS comparison with an explicitly disclosed zero-display floor; paired thresholds expose symmetry degeneracy and inversion swapping directly.

### Figure 2
Matched +y/-y threshold panels, direct branch labels, and positive energy/stability margins expose the prepared-state selection logic.

### Figure 3
Family-level collapse is separated from residual finite-size and shape deviations while retaining all sampled compact-contact evidence.

### Figure 4
Edge orientation is color-coded, registry family is marker/line-coded, the sign switch is not connected across the family discontinuity, and the original 0-3 degree range is shown explicitly.

### Figure 5
Integer winding maps use discrete color states, pinned (0,0) states remain visible, and Floquet solvers are categorical rather than spuriously connected. This exposes a downstream manuscript wording issue: “transport over all 91 sampled points” is too strong because pinned states are included.

### Figure 6
Stationary mean current and trajectory-level 95% intervals are the hero evidence; low-T N=500 and pooled high-T N=1000 are visually distinct; the Hotelling threshold and exact-winding probability hierarchy are explicit without implying a critical temperature.

## INFERENCE

The redesigned set carries the same scientific claims with stronger claim-to-panel traceability and lower risk of visual overstatement. No scientific-result regression was introduced by the redesign.

## SPECULATION

None.

## Benchmark gate

**BENCHMARK_PASS — Figures 1-6**

## Venue gate

**WARN / NOT YET PUBLICATION_READY in the local benchmark render**

Literal Arial is not installed in the local execution environment, so the benchmark render uses Arimo without relabeling it. The repository handoff renders the same source on a Windows environment containing literal Arial and requires a second final-size visual inspection before venue PASS.

## Next gate

\`ACS Nano figure venue handoff -> manuscript integration -> refreshed reproducibility/submission package\`
