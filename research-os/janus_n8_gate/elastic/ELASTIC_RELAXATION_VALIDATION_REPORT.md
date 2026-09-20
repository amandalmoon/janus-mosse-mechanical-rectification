# First Elastic-Relaxation Validation Report

## Manuscript
**Unguided Full-2D Mechanical Rectification and Vector Mode Locking in Finite Janus MoSSe Contacts**

## Status
**Tier-1 in-plane elastic robustness test: PASS.**

The audit-resolved rigid model had one clear unresolved model-input question: whether the headline directional depinning split survives once the finite contact is allowed to deform. This report addresses the first tractable part of that question by adding free-edge, in-plane linear elasticity while retaining exactly the same corrected published 2H MoSSe local GSFE used by the rigid calculation.

This is deliberately **not** claimed to be a fully relaxed atomistic MoSSe interface. Out-of-plane corrugation, atomistic edge reconstruction, defects, chemistry-specific nonlocal edge energetics, load-dependent GSFE, and physical dissipation/mass calibration remain outside this test.

## 1. Core reference set after compression

The manuscript bibliography was reduced from 43 references to the following 20 papers, chosen so that each retained citation supports a distinct part of the causal chain or a key limitation.

| # | Core reference | Role in the paper |
|---:|---|---|
| 1 | Wang, Khosravi, Vanossi & Tosatti, *Rev. Mod. Phys.* **96**, 011002 (2024) | Current framework for sliding, pinning, size, elasticity, defects and kinetic/static distinctions |
| 2 | Koren & Duerig, *Phys. Rev. B* **94**, 045401 (2016) | Finite-contact moire cancellation and incomplete-tile/rim scaling |
| 3 | Yan, Ouyang & Liu, *J. Mech. Phys. Solids* **170**, 105114 (2023) | Moire-boundary origin of finite-contact scaling |
| 4 | Verhoeven, Dienwiebel & Frenken, *Phys. Rev. B* **70**, 165418 (2004) | Rigid finite flake: orientation, size, shape, pulling direction |
| 5 | Yan et al., *J. Mech. Phys. Solids* **185**, 105555 (2024) | Shape-dependent friction scaling |
| 6 | Liao et al., *Nature Materials* **21**, 47-53 (2022) | Experimental/MD evidence for edge pinning in vdW contacts |
| 7 | Gao et al., *ACS Nano* **19**, 29255-29264 (2025) | Edge/corner elastic moire pinning |
| 8 | Minkin et al., *Phys. Rev. Materials* **9**, 024002 (2025) | Structural relaxation can strongly renormalize PES corrugation/topology |
| 9 | Lu et al., *Nature Nanotechnology* **12**, 744-749 (2017) | Experimental Janus MoSSe material basis |
| 10 | Zhang et al., *J. Am. Chem. Soc.* **142**, 17499-17507 (2020) | Polar Janus MoSSe interlayer coupling and spacing |
| 11 | Lin et al., *Nanoscale* **16**, 4841-4850 (2024) | Sliding ferroelectricity and twist in bilayer Janus MoSSe |
| 12 | Angeli, Schleder & Kaxiras, *Phys. Rev. B* **106**, 235159 (2022) | Published MoSSe three-shell GSFE/continuum input |
| 13 | Angeli, Schleder & Kaxiras, *Phys. Rev. B* **109**, 199902(E) (2024) | Essential correction/erratum to the GSFE convention |
| 14 | Li, Guo & Guo, *Friction* **10**, 1851-1858 (2022) | Janus-TMD sliding barriers under electric-field/load control |
| 15 | Chen et al., *ACS Appl. Mater. Interfaces* **18**, 21195-21203 (2026) | Closest prior art for intrinsic friction-diode behavior from asymmetric PES |
| 16 | Torche et al., *Adv. Mater. Interfaces* **9**, 2100914 (2022) | First-principles PES linked to stochastic friction dynamics |
| 17 | Guo, *Phys. Chem. Chem. Phys.* **20**, 7236-7242 (2018) | First-principles in-plane MoSSe elastic constants used in this validation |
| 18 | Dong, Lunghi & Sanvito, *J. Phys. Chem. Lett.* **14**, 6086-6091 (2023) | Direct evidence that stiffness can renormalize friction at fixed ISES |
| 19 | Hanggi & Marchesoni, *Rev. Mod. Phys.* **81**, 387-442 (2009) | Unbiased rocking/Brownian-motor framework |
| 20 | Barbi & Salerno, *Phys. Rev. E* **62**, 1988-1994 (2000) | Underdamped phase locking and current reversal |

The compressed set retains the material source, the corrected GSFE source, the nearest friction-diode prior art, the relevant finite-contact/edge/scaling literature, the elasticity challenge, and the nonlinear-transport literature without keeping multiple broad reviews that serve the same purpose.

## 2. Elastic model added for the first validation

### 2.1 Geometry and degrees of freedom

- Reference contact: the same compact **N=127** hexagonal site set used for the audit-resolved headline result.
- Each lattice site receives an in-plane displacement vector **d_i = (u_i, v_i)**.
- A free-edge triangular finite-element membrane is constructed from the contact lattice.
- The two rigid translations and the infinitesimal rigid-rotation mode are projected out of the internal displacement field, so the center-of-mass registry and imposed twist remain the external mechanical coordinates.
- Total equilibrium degrees of freedom: **253** = two center-of-mass registry coordinates + 251 internal in-plane coordinates.

### 2.2 Energy

The elastic extension minimizes

\[
E = \sum_i U_{\rm GSFE}(\mathbf R + \mathbf r_i^{\theta} + \mathbf d_i)
  + E_{\rm elastic}[\{\mathbf d_i\}]
  - F_y R_y,
\]

where the same corrected 2H MoSSe three-shell GSFE is used site by site. The membrane term is the standard small-strain 2D isotropic/hexagonal linear-elastic energy assembled over triangular elements.

### 2.3 Elastic constants

Nominal monolayer MoSSe values:

- lattice constant: **a = 3.25 A**;
- **C11 = 119.3 N/m**;
- **C12 = 27.5 N/m**;
- **C66 = (C11-C12)/2**.

Source: S.-D. Guo, *Phys. Chem. Chem. Phys.* **20**, 7236-7242 (2018), DOI **10.1039/C8CP00350E**.

Sensitivity cases were also run at **C/2**, **2C**, an alternative literature-level pair **C11=126.8 N/m, C12=27.4 N/m**, and **100C** as a numerical rigid-limit check. C/2 is a compliance bracket, not an exact two-layer atomistic model.

## 3. Numerical implementation checks

The implementation was checked independently before interpreting thresholds.

| Check | Result |
|---|---:|
| Equilibrium DOF | 253 |
| Rigid-mode constraint residual | 4.15e-15 |
| Projected elastic matrix minimum eigenvalue | 0.670109 |
| Sampled analytic energy-gradient maximum absolute error | 1.67e-10 |
| Sampled gradient/Hessian-column maximum absolute error | 1.29e-9 |
| Representative equilibrium full-Hessian minimum eigenvalue | 0.752226 |
| 100C recovery error, F_c,+ at theta=1.5 deg | 0.0459% |
| 100C recovery error, F_c,- at theta=1.5 deg | 0.0528% |

The force-controlled branch was followed as a local equilibrium branch using analytic gradients and Hessians. This avoids the failure mode of unconstrained minimization on a tilted periodic potential, where the optimizer can run into a neighboring translated state instead of following the prepared metastable branch.

## 4. Main result: theta = 1.5 deg

The audit-resolved rigid thresholds are

\[
F_{c,+}^* = 3.071135,\qquad F_{c,-}^* = 1.258672,\qquad \rho=0.418601.
\]

The in-plane elastic results are:

| Case | F_c,+* | F_c,-* | rho | Change in F_c,+ | Change in F_c,- | max principal strain |
|---|---:|---:|---:|---:|---:|---:|
| Rigid | 3.071135 | 1.258672 | 0.418601 | - | - | 0 |
| Nominal C | 2.934326 | 1.190186 | 0.422872 | -4.45% | -5.44% | 0.458% |
| C/2 | 2.807373 | 1.135205 | 0.424131 | -8.59% | -9.81% | 0.821% |
| 2C | 3.001758 | 1.222461 | 0.421213 | -2.26% | -2.88% | 0.242% |
| Alternative constants | 2.944336 | 1.194727 | 0.422707 | -4.13% | -5.08% | 0.424% |
| 100C rigid-limit | 3.069727 | 1.258008 | 0.418630 | -0.046% | -0.053% | 0.0052% |

The important result is not that the rigid threshold values are unchanged. They are not. In-plane relaxation systematically **softens the absolute depinning forces**. The robust result is that the two directions remain strongly inequivalent and the normalized splitting changes little: nominal elasticity changes rho by only **+1.02%** relative to the rigid value, and even the factor-of-four stiffness bracket C/2 to 2C retains the same directional sign and similar rho.

For nominal C, the maximum site displacement at the last stable branch point is approximately **0.050 A** for +y loading and **0.059 A** for -y loading, with sub-percent strains.

## 5. Twist dependence of the first elastic check

Representative points were also checked away from the headline twist.

| theta | Case | F_c,+* | F_c,-* | rho | Interpretation |
|---:|---|---:|---:|---:|---|
| 0 deg | nominal C | 3.484961 | 1.422070 | 0.420395 | Essentially the rigid result; internal relaxation vanishes by symmetry within numerical precision |
| 1.5 deg | nominal C | 2.934326 | 1.190186 | 0.422872 | Absolute thresholds soften by 4-5%; directional split survives |
| 3 deg | nominal C | 1.572852 | 0.631445 | 0.427078 | Elastic renormalization is stronger (about 16-19%), but sign remains positive |
| 3 deg | C/2 | 1.244727 | 0.516992 | 0.413082 | About 34% absolute softening, yet rho is almost identical to the rigid rho=0.412984 |

This is an important nuance for the paper. The rigid threshold numbers should **not** be interpreted as material constants. Elasticity becomes increasingly important with twist in the tested interval. However, the mechanism-level statement--a branch-followed directional split generated by the inversion-asymmetric registry landscape--survives this first relaxation degree of freedom.

## 6. Scientific interpretation

### What this test supports

1. The headline directionality is **not eliminated** by adding realistic-order in-plane MoSSe stiffness.
2. The sign of the directional split survives nominal C, C/2, 2C and the alternative elastic constants at theta=1.5 deg.
3. The normalized splitting rho is substantially more robust than either absolute depinning threshold.
4. The numerical implementation passes finite-difference derivative checks and converges back to the rigid model as stiffness is increased.

### What this test does not support

1. It does **not** prove that a fully atomistically relaxed MoSSe finite contact has the same thresholds.
2. It does not model out-of-plane buckling/corrugation, edge chemistry, edge reconstruction, defects or nonlocal edge interactions.
3. It does not resolve the precise high-twist triangular boundary switch, which is already known to be edge-model sensitive.
4. It does not generate physical damping, mass, temperature or time scales.
5. C/2 is a deliberate compliance sensitivity bracket, not a derived bilayer relative-elasticity law.

## 7. Decision

**Tier-1 validation decision: PASS, with a narrowed claim.**

A defensible manuscript statement is:

> Allowing the N=127 contact to relax in plane with first-principles-order MoSSe stiffness lowers the absolute depinning thresholds but preserves the branch-followed directional split. At theta=1.5 deg, nominal elasticity changes F_c,+* and F_c,-* by -4.45% and -5.44%, while rho changes from 0.41860 to 0.42287; a C/2-to-2C stiffness bracket retains the same sign. This supports mechanism-level robustness to in-plane compliance, but not atomistically relaxed edge or out-of-plane reconstruction.

The next validation should therefore move to a **registry-dependent atomistic/MLIP or first-principles relaxed finite interface**, with special attention to the edge and out-of-plane degrees of freedom. That is the first test capable of converting the current Tier-1 result into a genuinely relaxed-contact claim.

## 8. Files produced

- `run_elastic_relaxation_validation.py` -- elastic branch-continuation and analysis code.
- `elastic_relaxation_validation_summary.csv` -- canonical result table.
- `elastic_relaxation_validation_metadata.json` -- model and source metadata.
- `numerical_validation_checks.json` -- derivative/constraint/rigid-limit checks.
- `elastic_relaxation_validation.png` -- compact result figure.
- `Janus_MoSSe_AuditResolved_CoreRefs_ElasticValidation.docx` -- main manuscript with 20-reference bibliography and elastic result integrated.
- `Janus_MoSSe_AuditResolved_SI_ElasticValidation.docx` -- updated SI with the validation table and caveats.
