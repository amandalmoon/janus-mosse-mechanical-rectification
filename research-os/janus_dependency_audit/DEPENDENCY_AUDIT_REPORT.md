# Janus MoSSe Exact-Root Endpoint Dependency Audit

## Scope
Patch the guided static `F0*=3.5` endpoint calculation from 0.025-degree linear interpolation to exact scalar root refinement of the actual full-Hessian threshold solver, then trace and recompute downstream observables.

## Endpoint patch
The patched driver uses the sampled curve only to locate a sign-changing bracket. It then solves

`M.guided_threshold(theta, material, direction, k_perp)["Fc"] - F0 = 0`

with Brent's method (`xtol=2e-13`, `rtol=1e-14`).

### N=127 reference
| quantity | old linear | exact root | exact-old |
|---|---:|---:|---:|
| theta_c,+ (deg) | 1.944451626443851 | 1.944469329617526 | +1.770317e-05 |
| theta_c,- (deg) | 1.009906838705237 | 1.009973479607291 | +6.664090e-05 |
| W_D (deg) | 0.934544787738614 | 0.934495850010235 | -4.893773e-05 |

Relative change in W_D: about -5.24e-5 (-0.00524%).

The old deterministic midpoint was 1.477179232574545 deg. The exact midpoint is 1.477221404612409 deg, a shift of +4.217204e-05 deg.

## Dependency audit

### 1. W_D
**Directly dependent.** Replace the N=127 reference value by `0.934495850010235 deg` if reporting more than 3 decimals. At three decimals both old and exact values remain `0.934 deg`.

### 2. Finite-size W_D scaling
Recomputed for the ten compact hexagons N=37,61,91,127,169,217,271,331,397,469.

| metric | hypothetical all-linear endpoints | exact-root endpoints |
|---|---:|---:|
| alpha in W_D ~ N^-alpha | 0.503131586270 | 0.503133244573 |
| log-log R^2 | 0.999994866829 | 0.999994817616 |
| mean W_D sqrt(N) (deg) | 10.5336847091 | 10.5333897270 |
| sample SD W_D sqrt(N) (deg) | 0.0294654418 | 0.0294951598 |
| maximum per-size |delta W_D| (deg) | - | 7.73835e-05 |
| maximum relative per-size W_D change | - | 1.21126e-04 |

The current v18 clean-replay reports alpha=0.5031332447 and the compact manuscript reports 10.5334 +/- 0.0295 deg. These agree with the exact-root recalculation, not the all-linear counterfactual. Therefore the **current finite-size headline is already exact-root consistent and does not need a numerical change**.

### 3. rho and force-twist factorization
**Independent of F0 endpoint interpolation.** They are calculated directly from `Fc,+ (theta)` and `Fc,- (theta)` on the fixed 0-3 deg theta grid.

Fresh recomputation:
- mean rho = 0.103289166253425
- sample SD = 0.001364269716612
- rho range = [0.101689842437393, 0.106046262498247]
- max forward factorization residual = 0.249274947921%
- max reverse factorization residual = 0.308415987222%
- band area = 2.108449024026 force-deg

These reproduce the manuscript values. Endpoint patch delta = exactly zero by dependency structure.

### 4. Scaled-surface collapse
**Independent of F0 endpoint interpolation.** It is a comparison of the direct threshold surfaces `Fc(theta,N)` after the theta -> theta sqrt(N) coordinate transform. The v18 clean replay gives 0.254202% maximum relative deviation. The endpoint patch does not alter any sampled threshold-surface value.

### 5. Edge factorization / sign reversal
The reported sign-reversal roots solve `Delta Fc(theta)=Fc,+-Fc,-=0`, not `Fc=F0`. Therefore **the sign-reversal roots and edge factorization metrics are independent of the F0 endpoint interpolation patch**. Current v18 clean replay values remain:
- 20 deg cut: 2.963732 deg
- 25 deg cut: 2.890673 deg

A separate independent reconstruction of the exact v18 triangular geometry was attempted from manuscript-level geometry descriptions, but it did not reproduce these anchors; the original v18 edge-construction source is not separately available in the accessible Library. Consequently no substitute reconstructed edge numbers are used here.

The edge-specific **F0=3.5 window widths**, if quoted, are endpoint quantities and should use exact roots in the edge module as well.

### 6. Odd-sector continuation
**Independent of F0 endpoint interpolation.** It runs at fixed theta=1.5 deg and calls the full threshold solver directly for each eta.

Fresh recomputation:
- d(Delta Fc)/d eta at eta=0 = 2.83221268016105
- local R^2 = 0.99999984833088
- positive optimum eta = 0.50
- Delta Fc(eta=0.50) = 1.37864737061647
- rho(eta=0.50) = 0.280902077089547

No numerical change from the endpoint patch.

## Additional hidden downstream dependency: thermal midpoint — CLOSED
The thermal-fidelity stage is configured at the old static midpoint `theta_mid=1.4771792325745448 deg`. The exact midpoint is `1.4772214046124086 deg`, a shift of `+4.217204e-05 deg`.

A paired replay was run with the same BAOAB implementation, 1000 trajectories per direction per temperature, the same 12-temperature grid, and the same seed schedule. **All forward and reverse switching counts were identical at all 12 temperatures.** Therefore:
- temperatures with any count change = 0/12
- max |delta D| = 0
- fitted T1/2 is unchanged (`0.0538173743571` before manuscript rounding)
- because the binomial counts and bootstrap seed are unchanged, the bootstrap confidence interval is also unchanged.

Thus the midpoint is formally downstream but numerically inert under the current stochastic resolution.

## Package references that also require updating after the patch
The old endpoint constants are hard-coded in multiple non-solver locations in the v17/v12 reference package:
- Figure 7/8 vertical endpoint lines.
- `validate_v17_release.py` reference dictionary.
- `validate_v12_outputs.py` endpoint/window reference values and reverse k_perp reference.
- `dft_guided_material_v12.py` smoke-test endpoint tuple.
- production config `thermal_mid_theta_deg` if thermal fidelity is to remain defined at the deterministic midpoint.

The numerical physics surfaces, rho/factorization, odd-sector continuation, mode map, and edge sign roots do not require regeneration solely because of the static endpoint patch.

## Gate verdict
- Static endpoint solver: PATCH REQUIRED and implemented in audit copy.
- N=127 endpoint/window reporting: UPDATE REQUIRED.
- Finite-size headline: PASS; already exact-root consistent.
- rho/factorization: PASS; unchanged.
- scaled-surface collapse: PASS; unchanged.
- edge sign reversal: PASS with respect to this dependency; unchanged.
- odd-sector continuation: PASS with respect to this dependency; unchanged.
- thermal midpoint/fidelity: PASS; exact-midpoint paired replay produced identical switching counts and therefore identical fit/bootstrap inputs.
