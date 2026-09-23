# NP-RESTART-01 Gate Report — 2026-09-23

## CURRENT STAGE

Execution / data preparation — EXP-001 Phase-0 completed; Phase-1 production freeze pending.

## LAST VALID GATE

**GATE-EXP001-P0 — PASS.**

## CURRENT GATE STATUS

**PARTIAL for downstream work.** Phase-0 itself passed. The previous human approval was explicitly bounded to Phase-0, so production equilibrium response and any scientific driven validation remain blocked until the Phase-1 production/predictor settings are frozen and approved.

## VERIFIED

- Frozen N29 nonlinear VFF baseline reproduced at N=127, theta=1.5 deg.
- F_c,+* = 2.935400391, F_c,-* = 1.190478516, rho = 0.422921253.
- 342 bonds, 648 angles, 251 internal DOF; rigid-mode residual = 4.146e-15.
- COM/internal equal-site-mass transform verified over 100 random trials; max absolute kinetic-energy mismatch = 1.137e-13.
- Internal-only Langevin bath at T*=0.01, zeta_b*=1 passes kinetic equipartition pilot; max four-seed error = 2.486%.
- Half-time-step FDT check error = -0.053%.
- Extended constrained-equilibrium pilot completed with two independent 100-time-unit trajectories.
- Planning memory cutoff = 9.768 reduced time units; preregistered 200 tau production rule implies >=1953.6 time units per production trajectory.
- Pilot force ACF contains long oscillatory recurrences. This is **not** evidence for a single-exponential memory law or for non-Markovian new physics.
- One-period implementation-only energy-accounting diagnostic closes the first law with relative residual 1.685e-04.
- No scientific driven validation, M0/M1/M2/M3 model selection, corner-edge analysis, winding analysis, or new-physics claim was performed.
- The VFF and GSFE repository files on this branch are byte-for-byte identical to the frozen science commit versions used for provenance comparison.

## TENTATIVE / REJECTED

- Any single relaxation-time interpretation of the pilot ACF: **REJECTED at Phase-0** because recurrences remain.
- Scalar/tensor/memory sufficiency: **PENDING**.
- Equilibrium prediction of driven loss: **PENDING**.
- New physics / non-Markovian claim: **NOT AUTHORIZED**.

## DIRTY ARTIFACTS

None in the frozen N29 chain.

## BLOCKERS + OWNER

No Phase-0 scientific blocker remains.

Downstream owner: experiment/simulation design. Phase-1 cannot start until its production settings and predictor artifact schema are frozen under a new human approval.

## NEXT GATE

**GATE-PHASE1-PRODUCTION-FREEZE**

## NEXT ACTION

Freeze, before any scientific driven trajectory is inspected:

1. production seed list and trajectory count;
2. production length (must satisfy the preregistered >=200 tau rule or document a stricter convergence-based replacement);
3. correlation/window estimator and tail/recurrence policy;
4. response/predictor artifact schema and uncertainty calculation;
5. frequency-grid rule if the pilot does not support a unique tau-based mapping.

## HUMAN APPROVAL NEEDED

**YES.** Previous authorization covered EXP-001 Phase-0 only.
