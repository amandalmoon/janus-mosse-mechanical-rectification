# Claim-Evidence Matrix

Status vocabulary: VERIFIED / SUPPORTED / TENTATIVE / PENDING / REJECTED.

At this stage, the manuscript and SI are available, but the canonical execution artifacts are not yet present in the repository. Therefore central scientific claims are marked SUPPORTED rather than VERIFIED.

| ID | Claim | Manuscript evidence | SI evidence | Required repository evidence | Status |
|---|---|---|---|---|---|
| C1 | Published 2H MoSSe GSFE is nonremovably inversion-asymmetric in registry space | A_min=0.0425361; odd RMS=0.206243; chi_1=0.583541 | S4 translation-minimized odd-power search and origin audit | asymmetry-search script, input GSFE coefficients, raw search outputs, translation tests | SUPPORTED |
| C2 | Prepared ground-state branch has directional depinning at N=127, theta=1.5 deg | F_c,+*=3.071135; F_c,-*=1.258672 | S2 branch audit | continuation code, branch enumeration data, fold residuals, exact run config | SUPPORTED |
| C3 | Same-spectrum symmetrization removes global directional bias and exact inversion swaps it | sym. 1.767700 / 1.767700; inversion 1.258672 / 3.071135 | S3 matched symmetry contracts | symmetrization/inversion generator, threshold outputs, current-reversal outputs | SUPPORTED |
| C4 | Compact hexagonal and disk-like families collapse under theta sqrt(N) over tested range | max within-family deviations <0.1% through Theta=20 | S5 extended compact-contact similarity | geometry generators, threshold tables, scaling-analysis script | SUPPORTED |
| C5 | Rotated triangular boundaries can reverse prepared-state sign through registry competition | switches at 2.921278 deg and 2.847233 deg | S6 boundary registry competition | boundary geometry files, A/B energy branches, weight-sensitivity outputs | SUPPORTED |
| C6 | Declared m*=1, gamma*=4 protocol supports sampled vector mode locking | 91/91 sampled points; representative Floquet rho_F<1 | S7 drive-period and Floquet conditioning | deterministic integrator, grid outputs, cycle-resolved winding tables, Floquet cross-solver logs | SUPPORTED |
| C7 | Thermal exact winding identity is fragile while mean vector drift remains nonzero through sampled T*=0.70 | pooled <u,v>=(0.03700,-0.07645) at 0.70; zero vector excluded | S8 trajectory-cluster inference | raw trajectories or reproducible compressed outputs, seeds, BAOAB config, bootstrap/Hotelling scripts | SUPPORTED |
| C8 | In-plane compliance softens absolute thresholds without removing directional split in two tested representations | FEM 2.934302 / 1.190210; VFF 2.935400 / 1.190479 at 1.5 deg | S9-S10 | FEM source/results, nonlinear VFF source/results, elasticity calibration tests | SUPPORTED |
| C9 | Current work is not a full 3D atomistic validation or calibrated device prediction | explicit limitation in Discussion/Conclusions | S11-S12 no-go and remaining limitations | Tier-2 prescreen outputs and no-go record | SUPPORTED |
| C10 | Manuscript claims are reproducible from a frozen evidence package | stated in reproducibility/data availability sections | S13 release contents | exact committed/deposited package plus checksum manifest and clean-replay record | PENDING |

## Gate rule

A claim moves from SUPPORTED to VERIFIED only when the repository or an immutable linked deposition contains the exact executable evidence needed to reproduce or independently check the stated result.
