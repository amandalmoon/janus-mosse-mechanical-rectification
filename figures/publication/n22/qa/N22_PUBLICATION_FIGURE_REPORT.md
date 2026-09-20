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

## Exact-head technical preflight

Windows GitHub Actions run **35486368648** on N22 head `a1fd144bfecd13e5bbe13e7a92bab40d680e5c4f` completed successfully.

- literal Arial path: `C:\\Windows\\Fonts\\arial.ttf`;
- N22 manifest contract: PASS;
- architecture-aligned render: PASS;
- exact physical dimensions and exports: 7/7 PASS;
- Arial presence / no Arimo-Liberation fallback: 7/7 PASS;
- artifact ID: **10597586247**;
- artifact digest: `sha256:db358a3f76c2ad62a9f2416f95e505911a00f19d251004d7870dca05e7636b93`.

The resulting final-size Arial PNGs were opened and inspected after CI. All seven pass visual readability and integrity checks.

## Gate

**BENCHMARK_PASS + TECHNICAL_ARIAL_PREFLIGHT_PASS**

Final ACS Nano venue acceptance remains intentionally deferred to the later `acs-nano-submission` stage.

## Next action

Freeze N22 and hand the N21 architecture plus N22 figure contracts/captions to `research-os-manuscript-writer`.
