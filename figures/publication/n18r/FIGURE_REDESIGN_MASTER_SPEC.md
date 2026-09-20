# N18R Strict Publication-Figure Redesign Master Spec

Target manuscript: *Unguided Full-2D Mechanical Rectification and Vector Mode Locking in Finite Janus MoSSe Contacts*  
Target venue: ACS Nano Article  
Figure benchmark: \`evidence-dense-physics-v1\` from the updated Publication Figure Designer skill.

## Cross-figure design contract

- Final role: main-text, double-column quantitative figures.
- Final width: 177.8 mm.
- Minimum benchmark text: 7.0 pt; panel labels 9.2 pt; primary lines 1.2 pt; minimum line/spine 0.65 pt.
- Current benchmark-render font: **Arimo**. Literal Arial is not installed in the execution environment and is **not** faked by renaming font metadata. ACS Nano venue QA therefore remains \`WARN\` until a literal-Arial re-export is performed.
- \`+y\` / positive-direction quantities: blue circle / solid line.
- \`-y\` / negative-direction quantities: vermilion square / dashed line.
- Ground/prepared vs metastable branches: solid versus open-marker/dashed semantics.
- Reference/zero/switch guides: thin gray or condition-colored dotted lines, visually subordinate to evidence.
- Quantitative figures use executed simulation outputs only (\`SIMULATION_EXECUTED\`). No placeholder or illustrative values are permitted in evidence panels.
- Vector-friendly masters: PDF + SVG + EPS. PNG is a QA preview. TIFF is not generated at this benchmark stage because the figure set is vector-native.

## FIG-01 — Registry asymmetry and matched symmetry contracts

**Core conclusion.** The published 2H MoSSe registry landscape has a non-removable inversion-odd component, while same-spectrum symmetrization removes directional splitting and exact spatial inversion swaps it.

**Panel contract.**
- A — context: centered asymmetric 2H GSFE on the declared lattice coordinates.
- B — control: matched inversion-even GSFE on the exact same color scale.
- C — hero: translation-minimized odd RMS across 2H/3R controls on a log10 display. Exact zero is placed at a 1e-18 display floor and explicitly labeled \`0\`; this is a plotting device, not replacement evidence.
- D — validation: paired global \`F_c,+\` / \`F_c,-\` thresholds for original, symmetrized, and exact-inversion landscapes; winding pairs are labeled directly.

**Reviewer risks.** Matched symmetrization and exact spatial inversion are mathematical controls; they do not establish a physical polarity-reversal law.

## FIG-02 — Branch-resolved unguided depinning

**Core conclusion.** For the declared prepared state, the ground-state branch remains both the lower-energy zero-force minimum and the longer-lived pinned branch throughout the sampled 0–3 deg twist range.

**Panel contract.**
- A — hero: positive-y ground and metastable branch-followed thresholds.
- B — validation: negative-y ground and metastable thresholds on the same vertical scale.
- C — control: direct energy margin \`U_meta - U_ground\`; positive margin makes the preparation criterion visible without mental subtraction.
- D — validation: direct stability margin \`F_c^ground - F_c^meta\` for both directions.

**Reviewer risks.** The result is prepared-state and loading-protocol conditioned; the thresholds are not parameter-free material constants.

## FIG-03 — Finite-size and compact-shape similarity

**Core conclusion.** Tested compact hexagonal and disk-like contact families collapse closely under \`Theta = theta sqrt(N)\` over the sampled range, with residual finite-size and shape differences below about 0.1% through \`Theta=20\`.

**Panel contract.**
- A — hero: hex family, raw size-family points plus mean curve and min-max envelope.
- B — validation: independent disk-like family with the same encoding and scale.
- C — robustness: maximum within-family cross-size deviation for both directions.
- D — robustness: absolute difference between hex and disk family means.

**Reviewer risks.** This is a tested compact-family similarity coordinate, not evidence for a universal exponent or arbitrary boundary shapes.

## FIG-04 — Boundary-induced registry competition

**Core conclusion.** Rotated triangular boundaries create two stable registry families with opposite directional bias; selecting the lower-energy family reverses the prepared response at an equilibrium crossing, while the crossing angle is edge-model sensitive.

**Panel contract.**
- A — mechanism: \`U_B-U_A\` around the two equilibrium crossings.
- B — mechanism: branch splittings of families A and B, with family encoded by marker/line style and edge orientation by color.
- C — hero: prepared ground-state split on either side of the crossing, with no line drawn across the discontinuous family switch.
- D — robustness: switch angle versus outer-site energy weight; the original 0–3 deg window is explicitly marked.

**Reviewer risks.** The switch is an equilibrium fixed-twist re-preparation result. No twist-sweep path, barrier, torque, or hysteresis calculation is implied.

## FIG-05 — Two-dimensional vector mode locking

**Core conclusion.** The sampled amplitude-period grid contains reproducible integer winding states, including pinned \`(0,0)\` states, and representative transporting plateaus are strongly attracting under independent Floquet checks.

**Panel contract.**
- A — hero: discrete integer \`m\` map.
- B — validation: discrete integer \`n\` map on matched geometry.
- C — mechanism: \`tau*=40\` vector staircase with sampled markers.
- D — validation: categorical solver/tolerance comparison of Floquet spectral-radius deviation and relative-periodic closure.

**Reviewer risks.** The 91 points are a sampled map, not a continuous phase diagram or proof of global uniqueness. The word \`transport\` must not be used to imply that the pinned \`(0,0)\` states move.

## FIG-06 — Stationary thermal hierarchy

**Core conclusion.** Thermal noise rapidly destroys exact deterministic winding identity, while a weaker stationary directed mean current remains statistically resolved through the largest sampled temperature \`T*=0.70\`.

**Panel contract.**
- A — hero: mean lattice-current components with trajectory-level 95% intervals. Open markers are single-seed \`N=500\`; filled high-temperature markers are pooled two-seed \`N=1000\`.
- B — statistical validation: high-temperature Hotelling zero-current rejection ratio relative to the declared 95% threshold.
- C — mechanism: cycle-level directional probability versus exact target-winding probability; high-temperature points include bootstrap 95% intervals.

**Reviewer risks.** No extinction temperature, equilibrium transition, or thermal critical scale is claimed. Low- and high-temperature sample sizes are visibly distinguished.

## Benchmark gate

Each figure must pass:

1. scientific communication;
2. evidence visibility;
3. panel logic;
4. visual hierarchy;
5. typography/readability;
6. statistical completeness;
7. reproducibility/provenance;
8. final-size readability;
9. venue handoff metadata completeness.

The benchmark render can be \`BENCHMARK_PASS\` while ACS Nano venue QA remains \`WARN\` solely because literal Arial is unavailable. \`PUBLICATION_READY\` is prohibited until venue-specific font/export compliance is independently verified.
