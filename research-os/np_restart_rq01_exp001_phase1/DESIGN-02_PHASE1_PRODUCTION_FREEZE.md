# DESIGN-02 — Phase-1 Production / Predictor Freeze

## Purpose

Produce a reproducible constrained-equilibrium response estimate at the N29 reference contact before any scientific driven-validation trajectory is inspected.

This document freezes production cost, force-correlation estimation, recurrence-tail handling, uncertainty, predictor construction, and frequency selection.

## Frozen physical system

Inherited unchanged from DESIGN-01 / Phase-0:

- N = 127 compact hexagon
- theta = 1.5 deg
- published 2H Janus MoSSe GSFE used by frozen N29
- nominal nonlinear VFF internal mechanics
- prepared lowest-energy zero-force VFF minimum q0
- internal bath only
- zeta_b* = 1.0
- T* = 0.01
- no direct COM damping or COM noise
- constrained COM during equilibrium production
- integration time step = 0.000576312996712703 unless the predeclared half-dt sensitivity branch is triggered

The Phase-0 planning force ACF showed oscillatory recurrences. Therefore no single-exponential memory model and no unique physical memory time are assumed.

## Primary production ensemble

### Primary seeds

Exactly 8 independent trajectories:

- 2026092311
- 2026092312
- 2026092313
- 2026092314
- 2026092315
- 2026092316
- 2026092317
- 2026092318

### Equilibration

Each trajectory:

- fixed q = q0
- 200 reduced time units of burn-in
- burn-in samples discarded

The 200-unit burn exceeds 20 times the Phase-0 planning cutoff (9.768), but this numerical relation is only a conservative equilibration rule and is not interpreted as a physical single relaxation time.

### Primary production length

Each trajectory:

- 2500 reduced time units of production after burn-in

This exceeds the preregistered Phase-0 minimum `200 * 9.768 = 1953.6`.

### Sampling

Use the Phase-0 force-sampling cadence:

- integration dt = 0.000576312996712703
- record every 17 integration steps
- sample dt = 0.00979732094411595

Record at every stored sample:

- Fx, Fy generalized COM force
- total conservative potential energy
- internal kinetic energy
- accumulated bath heat increment
- selected diagnostic mode projections
- structural drift diagnostics

Raw integration states need not be committed to GitHub; raw arrays must be retained as immutable binary artifacts with SHA-256 hashes and a GitHub manifest.

## Precision-extension rule

Driven data are not consulted.

After the primary 8 trajectories are complete, the equilibrium estimator is audited. If any mandatory equilibrium-response convergence criterion below fails, add exactly four preregistered seeds:

- 2026092319
- 2026092320
- 2026092321
- 2026092322

for a maximum of 12 trajectories at 2500 production units each.

If mandatory criteria still fail with 12 trajectories, extend all 12 production trajectories to 5000 reduced time units total.

If mandatory criteria still fail after the 12 x 5000 state, Phase-1 is BLOCKED and requires human review. No further adaptive expansion is allowed automatically.

## Force-correlation estimator

### Blocking

Each 2500-unit trajectory is partitioned into five non-overlapping 500-unit production blocks.

Blocks are numerical stabilization units only. **Trajectory remains the inferential unit.**

### Correlation construction

Within each block:

1. subtract the block mean force;
2. estimate all four lagged covariance components:
   - C_xx(t)
   - C_xy(t)
   - C_yx(t)
   - C_yy(t)
3. use FFT convolution with unbiased `1/(n-lag)` normalization;
4. retain lags to L_max = 250 reduced time units.

The per-trajectory correlation is the arithmetic mean of its block-level correlations.

The ensemble estimator is the arithmetic mean across independent trajectories.

Keep C_xy and C_yx separately in the raw processed artifact. The dissipative Hermitian response may use their equilibrium symmetrized combination, but the antisymmetric residual must be reported as a diagnostic rather than silently discarded.

## Lag-cutoff / recurrence-tail policy

Because Phase-0 showed oscillatory tails, a single cutoff is not inferred from the first zero or first small-ACF crossing.

Compute the response for these predeclared maximum lags:

- L = 100
- L = 150
- L = 200
- L = 250

Primary numerical transform at each L:

- unit weight for t <= 0.8 L
- half-cosine taper over 0.8 L < t <= L
- zero beyond L
- trapezoidal quadrature in time

Sensitivity transform:

- rectangular truncation at L = 250

The taper is a numerical truncation device, not a physical memory model.

## Equilibrium zero-frequency Markov estimator

A constant tensor `Gamma0` is declared **resolved** only if the zero-frequency response:

1. is finite for L = 150, 200, 250;
2. changes from L=200 to L=250 by no more than one combined trajectory-bootstrap standard error for each independent tensor component;
3. is consistent between the first four and second four primary trajectories within two combined standard errors;
4. has no unresolved systematic drift under the half-dt sensitivity subset if that subset is triggered.

If these conditions fail, `Gamma0` is marked **UNRESOLVED**, not zero and not failed.

The scalar predictor is

`gamma0 = trace(Gamma0) / 2`

only when `Gamma0` is resolved.

## Frequency-dependent response estimator

Construct the equilibrium dissipative response on a fixed candidate frequency grid.

### Candidate frequency band

Let:

- `omega_max` = largest internal harmonic frequency at q0 from the Phase-0 Hessian estimate
- `Omega_floor = 2*pi/L_max`
- `Omega_ceiling = 0.25 * omega_max`

For the Phase-0 values this corresponds approximately to:

- Omega_floor ~= 0.02513
- Omega_ceiling ~= 21.69

Use 81 logarithmically spaced candidate frequencies over this closed interval.

No driven data may change this grid.

### Frequency-point stability

A candidate frequency is called **equilibrium-resolved** only if, for the dissipative projected responses needed in x and y:

1. L=200 and L=250 estimates differ by <= 1 combined bootstrap standard error;
2. the final L=250 estimate is finite;
3. the response is not rendered indeterminate by uncertainty so large that its sign/positive-semidefinite consistency cannot be assessed;
4. first-four vs second-four trajectory estimates agree within 2 combined standard errors.

Report unresolved frequencies explicitly.

## Five driven-test frequencies to be frozen from equilibrium only

After the equilibrium estimator is complete, identify the largest contiguous band of equilibrium-resolved candidate frequencies.

Requirements:

- band must span at least a factor of 8 in Omega;
- lower and upper endpoints must both satisfy the stability criteria above.

If no such band exists after the allowed precision extensions, Phase-1 is BLOCKED and Phase-3 driven validation does not start.

If a valid band exists, choose exactly five logarithmically spaced frequencies from its lower to upper endpoint and snap each to the nearest candidate-grid point.

These five frequencies are then frozen.

Assignment inherited from DESIGN-01:

- discovery frequencies: indices 1, 3, 4
- held-out frequencies: indices 2, 5

No frequency may be substituted after driven validation is inspected.

## Uncertainty

### Inferential unit

Independent equilibrium trajectory.

### Primary uncertainty

20,000-resample nonparametric bootstrap over trajectories.

For every bootstrap replicate:

- resample trajectories with replacement;
- recompute ensemble C_ij(t);
- recompute lag-windowed response;
- recompute Gamma0 / G(Omega) if defined.

Report:

- point estimate
- bootstrap standard error
- percentile 95% interval

Block-level variation is diagnostic only and is not counted as independent sample size.

### Precision-extension trigger

The allowed extra four seeds are triggered if either:

- any mandatory lag/frequency stability criterion above fails; or
- at any of the five to-be-frozen frequency points, the 95% CI half-width for either required projected dissipative response exceeds 50% of its absolute point estimate **and** the estimate is not statistically compatible with zero.

Near-zero response is not forced into a relative-error criterion.

## Stationarity / numerical diagnostics

Mandatory diagnostics:

- first half vs second half of each trajectory for force mean and internal kinetic energy;
- first four vs second four primary trajectories;
- internal kinetic equipartition;
- structural drift away from q0 internal basin;
- half-dt sensitivity on seeds 2026092311 and 2026092312 for at least 500 production time units;
- response stability under L = 100,150,200,250;
- rectangular-vs-taper sensitivity at L=250.

Any failure is preserved and routed upstream. It is not repaired by changing frequencies after viewing driven data.

## Predictor artifact freeze

Before Phase-3, save one immutable predictor artifact containing:

- exact upstream commit and source hashes
- q0 and physical/reduced model configuration
- dt / sample dt
- production seeds and lengths
- C_ij(t) estimate and trajectory-level uncertainty
- all cutoff variants
- Gamma0 and gamma0, or explicit UNRESOLVED status
- complex/frequency-dependent response on the 81-point grid
- five selected validation frequencies
- preregistered amplitudes and directions from DESIGN-01
- W predictions for M0, M1 and M3 wherever those models are defined
- uncertainty on each predicted W
- all diagnostics and extension decisions
- SHA-256 of the complete predictor package

No model is declared superior until independent driven validation is performed.

## Phase-1 stop rules

Stop and return to human review if:

- 12 trajectories x 5000 time units still fail mandatory equilibrium convergence;
- a contiguous resolved frequency band spanning factor >= 8 cannot be obtained;
- the internal bath fails FDT or half-dt checks at production scale;
- the internal state leaves the intended constrained-equilibrium basin;
- source/provenance hashes differ unexpectedly.

Success at this gate means only: **a pre-driven equilibrium predictor can be frozen reproducibly.**
