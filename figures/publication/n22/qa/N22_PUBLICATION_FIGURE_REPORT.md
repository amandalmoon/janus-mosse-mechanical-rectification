# N22 Publication Figure Designer Report

## Trigger

N21 froze a new scientific argument architecture before final figure design. The previous six-figure N18R set was therefore treated as reusable source material rather than a frozen manuscript sequence.

## FACT

- No new simulation was introduced.
- All quantitative panels use existing verified executed outputs.
- N22 implements the N21 seven-figure storyboard.
- Old N18R Figure 1 was separated into a credibility/setup figure and a later same-spectrum mechanism-validation figure.
- Compact size/shape evidence and in-plane-compliance evidence were combined into one robustness figure because they answer the same higher-level question.
- Boundary, vector-locking and thermal figures were renumbered to follow the argument chain.
- The Figure 6 wording explicitly distinguishes pinned (0,0) states from transporting integer-winding states.
- Figure 7 keeps trajectory-level uncertainty and joint current inference visually primary.
- The current publication-figure-designer source audit returns PASS for each plotting module.
- The current publication-figure-designer package audit returns PASS for all seven manifests at the benchmark gate.
- Export preflight confirms exact physical PDF canvases and 300 dpi PNG canvases for all seven figures.
- Final-size benchmark renders were visually inspected: 7/7 PASS.

## INFERENCE

The new figure order is a better match to the causal/argumentative burden of the paper: credibility precedes phenomenon, phenomenon precedes mechanism intervention, and robustness precedes dynamical implications.

## SPECULATION

None.

## Figure-level status

| Figure | Role | Scientific QA | Visual QA | Benchmark gate |
|---|---|---|---|---|
| FIG-01 | credibility/setup | PASS | PASS | PASS |
| FIG-02 | phenomenon | PASS | PASS | PASS |
| FIG-03 | mechanism validation | PASS | PASS | PASS |
| FIG-04 | robustness/generalization | PASS | PASS | PASS |
| FIG-05 | boundary implication | PASS | PASS | PASS |
| FIG-06 | deterministic dynamic implication | PASS | PASS | PASS |
| FIG-07 | thermal robustness | PASS | PASS | PASS |

## Gate

**BENCHMARK_PASS**

Literal-Arial rendering is a technical preflight, not the final ACS Nano submission gate. The user-defined workflow therefore proceeds to research-os-manuscript-writer only after exact-head figure CI is green.

## Next action

1. exact-head Windows render and output verification;
2. freeze N22 source/manifests;
3. hand the N21 architecture plus N22 captions/figures to research-os-manuscript-writer.
