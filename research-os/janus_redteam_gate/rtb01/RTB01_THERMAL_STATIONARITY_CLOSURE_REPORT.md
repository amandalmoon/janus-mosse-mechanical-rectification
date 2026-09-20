# RT-B01 Thermal Stationarity Closure — Janus MoSSe

## Verdict

**CURRENT STAGE:** Simulation -> Statistics -> Robustness (Red-Team blocker closure)  
**ISSUE:** RT-B01 thermal stationarity / finite-observation dependence  
**GATE:** **PASS WITH CLAIM REDEFINITION**  
**OLD thermal boundary claims:** **RETIRED**  

The Red-Team finding was real: the original 10-burn + 10-measure protocol was too short to support a physical statement such as “full vector current is resolved at T*=0.65 and unresolved at T*=0.70.” The statistical decision changes with the observation window. After an explicit stationarity audit, the correct result is not a sharp thermal boundary. It is a monotonic decay of a small but nonzero stationary-periodic mean drift across the sampled range, while exact cycle-by-cycle winding identity has already been strongly mixed.

## Frozen protocol for blocker closure

The closure audit used the same canonical unguided reduced model and forcing:

- N = 127 compact hexagonal contact
- theta = 1.5 deg
- F0* = 2
- tau* = 40
- m* = 1
- gamma* = 4
- BAOAB thermal integrator
- production timestep dt = 0.02

Primary stationarity protocol:

- 160 total driven cycles per trajectory
- discard the first 60 cycles
- use the following 100 cycles as the trajectory-level measurement window
- N = 500 independent trajectories per seed
- two independent seed ensembles for the high-temperature band T* = 0.50, 0.55, 0.60, 0.65, 0.70
- inferential unit = one trajectory summary, never individual cycles

A single N=500 ensemble was also rerun over the full original temperature grid T*=0.02-0.70 to reconstruct the long-window thermal series.

## Stationarity criterion and initialization loss

Three independent checks were required.

1. **Late-block drift:** 20-cycle trajectory summaries from cycles 61-80, 101-120, and 141-160 were compared with paired two-dimensional Hotelling tests. For T*=0.50-0.70, neither the 60->100 nor the 100->140 block comparison detected a two-component drift in either independent seed ensemble.
2. **Initial-state memory:** using common noise streams, deterministic-orbit, zero-force ground-state, and zero-force metastable starts were compared at T*=0.60, 0.65 and 0.70. The three simulations became identical to <1e-10 in cycle displacement by cycle 38 at the latest and were identical to numerical roundoff throughout the 60-160 measurement range.
3. **Timestep compatibility:** at T*=0.60, 0.65 and 0.70, dt=0.04, 0.02 and 0.01 produced mean-current estimates that differed by no more than 1.12 combined standard errors in either component. Pointwise significance can still flip at the weakest signal because significance depends on sample size/measurement duration; the effect-size estimates are compatible.

These diagnostics support burn=60 as numerically adequate for the tested high-temperature range and show that the earlier problem was primarily finite observation/statistical power, not persistent initialization memory.

## Stationary mean current: two independent high-T seed ensembles

Each row below pools two independent N=500 trajectory ensembles after 60 burn cycles and 100 measured cycles.

| T* | <u> | <v> | ||<J>|| | ||<J>||/sqrt(2) | zero vector |
|---:|---:|---:|---:|---:|---|
| 0.50 | 0.080006 | -0.155086 | 0.174507 | 0.1234 | excluded |
| 0.55 | 0.061754 | -0.123656 | 0.138218 | 0.0977 | excluded |
| 0.60 | 0.051117 | -0.107197 | 0.118761 | 0.0840 | excluded |
| 0.65 | 0.042226 | -0.086898 | 0.096614 | 0.0683 | excluded |
| 0.70 | 0.036998 | -0.076448 | 0.084930 | 0.0601 | excluded |

A 50,000-resample trajectory bootstrap excludes the zero vector at every sampled high-temperature point. At T*=0.70 the marginal 95% bootstrap intervals are approximately

- <u>: [0.01265, 0.06132]
- <v>: [-0.10088, -0.05196]

with the joint zero-vector Mahalanobis distance 38.07 versus a 95% bootstrap contour threshold 6.04.

## Full long-window temperature series

A uniform N=500, burn=60, measure=100 rerun over T*=0.02-0.70 shows a monotonic decrease in mean-current magnitude across all sampled temperatures. The current magnitude falls from 2.692 at T*=0.02 to 0.0697 at T*=0.70 in this seed ensemble.

The exact deterministic (1,-1) winding is **not** thermally preserved. In the pooled high-T stationary protocol, the probability that an individual measured cycle rounds to the deterministic target winding is only about 1.1-1.6% over T*=0.50-0.70.

The cycle-sign probability P(v_cycle<0) is only weakly above one-half at high T*:

| T* | P(v_cycle<0) | 95% trajectory-bootstrap CI | P(target winding) |
|---:|---:|---:|---:|
| 0.50 | 0.51933 | [0.51632, 0.52237] | 0.01556 |
| 0.55 | 0.51480 | [0.51176, 0.51783] | 0.01403 |
| 0.60 | 0.51181 | [0.50882, 0.51482] | 0.01293 |
| 0.65 | 0.50969 | [0.50666, 0.51275] | 0.01168 |
| 0.70 | 0.50802 | [0.50506, 0.51100] | 0.01116 |

Thus the high-T transport is a weak statistical drift of a strongly mixed cycle-displacement distribution, not thermal preservation of the deterministic locked orbit.

## Why the old 0.65/0.70 boundary must be retired

The old protocol used 10 burn cycles and only 10 measured cycles per trajectory. The Red Team showed that with burn=60 and a 10-cycle measurement the zero-vector decision can still change from seed to seed near T*=0.65-0.70. Increasing the same stationary measurement window to 40-100 cycles steadily reduces trajectory-mean variance and resolves the small nonzero drift.

Therefore “resolved/unresolved at a particular T*” is not a material transition or a robust physical boundary; it is a finite-observation detectability statement that depends on N, measurement duration, and estimator precision.

**REJECTED wording:**

- “The full vector current is present through T*=0.65 but disappears at T*=0.70.”
- “The v-component loses directionality at T*=0.65.”
- “P(Delta y<0) becomes unbiased at T*=0.60.”
- Any interpretation of 0.60/0.65/0.70 as a critical thermal scale.

## Replacement claim contract

### FACT

Under the declared reduced model and the stationary numerical protocol (burn=60, measure=100, dt=0.02), the sampled mean lattice current decreases strongly with T* but remains nonzero through the largest tested value T*=0.70. The deterministic target winding probability is already only about 1% in the high-T band, so mean directed transport and exact mode identity are distinct observables.

### INFERENCE

The persistence of a weak mean drift despite near-balanced positive/negative cycle counts is consistent with asymmetric displacement magnitudes and/or nonidentical tails in the cycle-displacement distribution. This mechanism-level interpretation should not be stated more strongly without an explicit distributional decomposition.

### NOT ESTABLISHED

- no critical temperature for loss of current;
- no Kelvin-scale thermal prediction;
- no statement that the current remains nonzero for T*>0.70;
- no universal stationary distribution outside the tested reduced protocol;
- no equilibrium/thermodynamic phase transition.

## Claim-Evidence updates required

- **C15:** keep, but replace the 10+10 protocol with the converged stationarity protocol for the high-T claim.
- **C16:** retire the “v resolved through 0.60 / unresolved at 0.65” boundary claim.
- **C17:** retire the “full vector resolved at 0.65 / unresolved at 0.70” boundary claim. Replace with monotonic stationary-current decay and nonzero current through the largest sampled T*=0.70.
- **C18:** retire the old P(Delta y<0) detectability boundary; under the longer stationary protocol P(v_cycle<0) remains slightly above 0.5 through T*=0.70.
- **C19:** expand the timestep statement to distinguish low-T deterministic consistency from the new high-T effect-size compatibility test.

## RT-B01 closure status

**RT-B01: RESOLVED WITH CLAIM REDEFINITION.**

The original blocker is closed because burn-in convergence, start-state memory, independent seed replication, trajectory-level uncertainty, measurement-duration sensitivity, and high-T timestep compatibility have now been explicitly audited. The manuscript must not retain the old finite-observation thermal boundary language.

## Next Research OS action

1. update the Claim-Evidence Matrix thermal rows;
2. run ACS Nano Figure Preflight for the replacement thermal panel/table;
3. regenerate the thermal evidence figure from the stationary protocol;
4. targeted manuscript revision of Abstract / Results / Discussion / Conclusion / SI;
5. short Red-Team closure check;
6. only then proceed to Five Reviewer Paper Audit.
