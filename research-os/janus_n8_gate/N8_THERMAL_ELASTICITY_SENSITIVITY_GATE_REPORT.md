# N8 Thermal / Elasticity / Sensitivity Gate Report

## Verdict

**PASS WITH CLAIM UPDATE** within the tested reduced-model scope.

The deterministic unguided prepared-state mechanism survives both (i) stochastic forcing with trajectory-level inference and (ii) two independent in-plane compliance representations. Absolute depinning forces are not robust material constants; the directional split is much more robust. A new joint-vector thermal audit changes the recommended thermal wording: the full two-component mean lattice current is statistically resolved at the sampled `T*=0.65` point and is unresolved at `T*=0.70`, even though the `v` component alone becomes unresolved already at `T*=0.65`.

---

## 1. Thermal inference: raw-data replay

Input: the canonical raw file with 1000 independent trajectories at each sampled temperature. Each trajectory contains 10 burn cycles and 10 measured cycles. Inference is performed at the trajectory level, not by treating cycles as independent replicates.

The shipped release validator passes, and recomputing its 10,000-resample cluster bootstrap from raw trajectory summaries reproduces the canonical scalar summaries.

### Existing one-component results

The lattice-`v` component remains negative with a 95% pointwise CI excluding zero through `T*=0.60`; at `T*=0.65` its interval includes zero. The high-resolution 100,000-resample `P(Delta y<0)` check remains above 0.5 at `T*=0.50`, is only marginally above 0.5 at `T*=0.55`, and is unresolved at `T*=0.60` and `0.65`.

Independent 100,000-resample checks performed here give:

| T* | P(Delta y<0) | 95% bootstrap CI | Status |
|---:|---:|---:|---|
| 0.50 | 0.5176 | [0.5079, 0.5274] | resolved |
| 0.55 | 0.5099 | [0.5001, 0.5197] | marginal |
| 0.60 | 0.5059 | [0.4964, 0.5154] | unresolved |
| 0.65 | 0.5067 | [0.4970, 0.5164] | unresolved |

### New two-component mean-vector audit

Because the deterministic mode is a lattice vector `(u,v)=(1,-1)`, a scalar `v` interval is not a complete confidence statement for the mean current vector. We therefore bootstrapped the two-dimensional trajectory means jointly.

At each temperature, a 95% simultaneous max-statistic rectangle was formed for `(mean_u, mean_v)` from 100,000 trajectory-cluster bootstrap resamples. This interval is simultaneous over the two components **within one temperature**, not familywise over the whole temperature scan.

| T* | mean u | mean v | simultaneous 95% u CI | simultaneous 95% v CI | zero vector? |
|---:|---:|---:|---:|---:|---|
| 0.60 | 0.090389 | -0.085895 | [0.009402, 0.171377] | [-0.165313, -0.006477] | excluded |
| 0.65 | 0.095014 | -0.065159 | [0.009053, 0.180975] | [-0.148036, 0.017718] | **excluded** |
| 0.70 | 0.069512 | -0.039861 | [-0.021611, 0.160636] | [-0.129302, 0.049579] | included |

A separate bootstrap Mahalanobis ellipse gives the same decision. At `T*=0.65`, two independent 100,000-resample runs give zero-vector Mahalanobis squared distances `6.3407` and `6.3403` versus 95% radii `5.9794` and `5.9948`; at `T*=0.70`, the zero vector lies inside the region.

**Updated thermal statement:** the last sampled temperature at which the **full two-component mean vector current** is resolved is `T*=0.65`; the first sampled point at which it is unresolved is `T*=0.70`. No exact continuous transition temperature is claimed.

This does **not** contradict the older `v`-component result. It shows that at `T*=0.65`, the longitudinal `v` component alone is unresolved while the joint current remains nonzero because the `u` component is still resolved.

### Exact winding identity versus directed transport

The deterministic target-cell probability is already small at all nonzero production temperatures (`P_target <= 0.0807` over the canonical table), whereas the mean vector current remains nonzero much farther into the noisy regime. This supports the separation:

`exact topological mode identity` < `directional vector-current robustness`.

### Independent timestep check

We independently reran 300 trajectories for `T*=1e-4, 1e-3, 5e-3` with `dt=0.04, 0.02, 0.01`. Across all pairwise timestep comparisons, the largest discrepancy was only `1.37` combined standard errors in `u` and `1.55` in `v`. Thus the low-noise mode mixing/current shift is not explained by integration step size over the tested range.

---

## 2. Linear in-plane elasticity: fresh rerun

The N=127 contact was re-run with a free-edge triangular finite-element membrane. The two rigid translations and infinitesimal rotation are projected out, giving 253 total equilibrium coordinates.

Fresh numerical checks:

- rigid-mode constraint residual: `4.146e-15`
- minimum projected elastic eigenvalue: `0.6701085`
- finite-difference energy/gradient max error: `1.08e-9`
- finite-difference gradient/Hessian-column max error: `8.60e-9`
- zero-force full-Hessian minimum eigenvalue: `0.752226`

At `theta=1.5 deg`:

| model | F_c,+* | F_c,-* | rho | change F+ vs rigid | change F- vs rigid |
|---|---:|---:|---:|---:|---:|
| rigid | 3.071135 | 1.258672 | 0.418601 | - | - |
| FEM C/2 | 2.807397 | 1.135229 | 0.424125 | -8.59% | -9.81% |
| FEM C | 2.934302 | 1.190210 | 0.422860 | -4.46% | -5.44% |
| FEM 2C | 3.001636 | 1.222534 | 0.421172 | -2.26% | -2.87% |
| alternative constants | 2.944409 | 1.194897 | 0.422658 | -4.13% | -5.07% |
| 100C rigid-limit | 3.069751 | 1.257886 | 0.418673 | -0.045% | -0.062% |

All tested cases retain `F_c,+ > F_c,-`. The 100C calculation returns to the rigid result to better than 0.07%, providing a strong numerical consistency check.

At `theta=3 deg`, nominal FEM gives approximately `F_c,+*=1.57302`, `F_c,-*=0.63127`, `rho=0.42723`; C/2 gives `1.24490`, `0.51682`, `rho=0.41328`. Thus absolute force renormalization grows strongly with twist, while the directional sign survives.

The zero-force branch ordering also survives compliance: two relaxed minima remain, and the same rigid ground-family seed remains the lower relaxed state in every tested stiffness/twist case. The relaxed energy gap stays large (`~0.17-0.31` in reduced units).

---

## 3. Nonlinear discrete VFF: independent reconstruction

The original nonlinear VFF source file is not present as a standalone file in the currently accessible Library bundles. We therefore did not treat its tabulated values as independently reproduced by code provenance alone.

However, the published model specification is sufficient to reconstruct the model unambiguously:

- 342 nearest-neighbor bond terms
- 648 local 60-degree angle terms
- `k_s=5.289992 eV/A^2`
- `k_theta=2.334491 eV/rad^2`
- the same rigid-mode projection and local GSFE

For the standard energy

`E_VFF = (k_s/2) sum_bonds (l-a)^2 + (k_theta/2) sum_angles (theta-pi/3)^2`,

an independent homogeneous-strain check yields

- `C11=119.299994 N/m`
- `C12=27.500000 N/m`
- `C66=45.899997 N/m`

which exactly identifies the intended calibration.

We then rebuilt the 253-DOF nonlinear problem using JAX automatic differentiation and repeated branch continuation.

| theta | stiffness | F_c,+* | F_c,-* | rho |
|---:|---:|---:|---:|---:|
| 1.5 | C | 2.935400 | 1.190479 | 0.422921 |
| 1.5 | C/2 | 2.810107 | 1.135693 | 0.424353 |
| 3.0 | C | 1.574365 | 0.631006 | 0.427755 |

These independently reconstructed values agree with the SI tabulation to about `5e-5` in the thresholds, consistent with the finite force-bisection tolerance.

Additional checks:

- VFF rigid-mode projection residual: `4.146e-15`
- finite-difference energy/gradient max error: `8.30e-11`
- finite-difference gradient/Hessian-column max error: `1.39e-8`
- nominal `theta=1.5` max bond strain: `0.396%`
- nominal `theta=1.5` max local angle change: `0.394 deg`

At `theta=1.5`, independently reconstructed VFF and fresh FEM differ by only `0.037%` in F+, `0.023%` in F-, and `0.014%` in rho. At `theta=3`, the respective differences remain below `0.13%`.

This strongly supports that the mechanism-level in-plane robustness is not an artifact of the linear FEM constitutive/discretization choice.

---

## 4. What is robust and what is not

### Verified within the tested reduced models

1. Deterministic unguided directionality survives finite thermal noise as a statistically resolved mean current over a broad range.
2. The full 2D mean vector remains resolved at the sampled `T*=0.65` point and is unresolved at `T*=0.70`.
3. Exact deterministic winding identity is much less thermally robust than mean transport.
4. Thermal conclusions are not caused by cycle pseudoreplication or the tested timestep range.
5. In-plane relaxation softens absolute thresholds but preserves the sign of the directional split.
6. The normalized split rho is substantially more robust than either absolute threshold.
7. FEM stiffness brackets, alternative elastic constants, and a 100C rigid-limit test all behave consistently.
8. An independently reconstructed nonlinear bond-angle model agrees closely with the linear FEM at matched elastic constants.

### Not established

- a physical Kelvin temperature or time scale (reduced m, gamma, T remain uncalibrated)
- a sharp thermal critical temperature between 0.65 and 0.70
- familywise simultaneous confidence over the entire temperature scan
- full 3D corrugation/buckling
- atomistic edge reconstruction or chemistry
- defects and nonlocal edge interactions
- load-dependent GSFE
- a Janus-specific atomistic/MLIP validation that passes the higher-harmonic GSFE contract

The existing public SW+KC candidate remains a qualitative mechanism stress test only, not a quantitative atomistic replacement.

---

## 5. Manuscript wording update

The old sentence

> the mean vector current remains statistically resolved through T*=0.60 but not T*=0.65

should be split into observable-specific statements:

> The lattice-v component has a pointwise 95% trajectory-cluster interval excluding zero through T*=0.60 and including zero at T*=0.65. A joint two-component bootstrap analysis of the mean lattice current, however, still excludes the zero vector at T*=0.65 and includes it at T*=0.70. The cycle-sign statistic P(Delta y<0) is clearly biased through T*=0.50, only marginal at T*=0.55, and unresolved by T*=0.60. No exact thermal transition is inferred between sampled temperatures.

The elasticity statement should remain mechanism-level:

> Allowing in-plane relaxation renormalizes absolute depinning thresholds but does not remove the prepared-state directional split in either a free-edge linear membrane or an independently reconstructed nonlinear bond-angle model. This is robustness to tested in-plane compliance, not a fully atomistically relaxed contact prediction.

---

## Gate status

**N8 THERMAL / ELASTICITY / SENSITIVITY GATE = PASS WITH THERMAL CLAIM UPDATE.**

The next Research-OS step should be a consolidated Claim-Evidence Matrix that incorporates N1-N5 plus this N8 correction before manuscript rewriting.
