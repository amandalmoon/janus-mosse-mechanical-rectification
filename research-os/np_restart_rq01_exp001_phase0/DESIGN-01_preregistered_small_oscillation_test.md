# DESIGN-01 — Preregistered Small-Oscillation Prediction Test

## Purpose

Discriminate the minimal dissipative reduction needed to predict cycle energy loss without fitting any dissipative parameter to driven validation data.

## System frozen for discovery branch

- Contact: compact N=127 hexagon used by N29.
- Twist: theta = 1.5 deg.
- Conservative interaction: the same published 2H Janus MoSSe GSFE used in N29.
- Internal mechanics: existing N29 nonlinear VFF topology and coefficients.
- Internal rigid translations and infinitesimal rotation projected out exactly as in the static VFF validation.
- COM: constrained during equilibrium sampling; prescribed during driven validation.
- No direct COM bath.
- Primary internal bath: `zeta_b*=1.0, T*=0.01`.
- Reduced-model study only; no Kelvin/Hz/nN material calibration.

## Phase 0 — implementation checks

P0.1 Reproduce the frozen N29 VFF ground state at theta=1.5 deg within numerical tolerance.  
P0.2 Reproduce bond/angle counts (342 / 648), rigid-mode projection residual, and static Hessian checks.  
P0.3 Verify `M=diag(N,N,I_internal)` against direct equal-site kinetic energy for random internal velocities.  
P0.4 Verify fluctuation-dissipation for the isolated internal bath using equilibrium kinetic-energy statistics.  
P0.5 Verify cycle energy accounting in a linear toy model and in the full contact at the smallest prescribed drive.

Scientific execution is BLOCKED if any P0 check fails.

## Phase 1 — equilibrium response only

Reference registry `q0`: prepared lowest-energy zero-force VFF minimum at theta=1.5 deg.

Record:
- generalized COM force `Fx,Fy`;
- total potential energy;
- internal kinetic energy;
- bath heat increment;
- selected mode coordinates/projections needed for diagnosis.

No oscillatory COM drive is allowed in Phase 1.

### Sampling convergence

- pilot only estimates correlation times and production length;
- at least 8 independent equilibrium trajectories for production;
- each production trajectory length >= 200 estimated force-correlation times after equilibration;
- per-trajectory correlation functions combined with block/bootstrap uncertainty;
- half-time-step convergence subset;
- response integral/frequency spectrum stable to integration-window extension within uncertainty.

## Phase 2 — predictor freeze

Before any driven validation trajectory is inspected, save:
- `C_ij(t;q0)` with uncertainty;
- low-frequency `Gamma0` if stable;
- `gamma0 = tr(Gamma0)/2`;
- frequency-dependent `G(Omega;q0)`;
- predicted `W` for every preregistered drive condition;
- hash of predictor artifact.

An unconverged equilibrium estimator may be declared undefined. It must not be repaired by fitting driven data.

## Phase 3 — independent prescribed-drive validation

```
q(t)=q0+A e cos(Omega t)
```

Directions:
- `ex=(1,0)`
- `ey=(0,1)`
- `ed=(ex+ey)/sqrt(2)`

Amplitude set:
- `A = 0.0025, 0.005, 0.010, 0.020`

Frequency selection after Phase 1, without driven data:
- estimate `tau_mem`;
- test `Omega*tau_mem = 0.10, 0.25, 0.50, 1.00, 2.00`.

Fallback if no single `tau_mem`: five logarithmically spaced frequencies from the first resolved low-frequency plateau to the highest frequency below `0.25 omega_max`. Record fallback before driven data generation.

Measure:
- `W_drive` per cycle;
- force amplitude/phase;
- net bath heat per cycle;
- stored internal energy change per cycle;
- structural-state drift.

Trajectory, not cycle, is the inferential unit.

## Linear-response qualification

Fit

```
W(A) = c2 A^2 + c4 A^4.
```

A condition is linearly qualified only when the confidence interval of `c4` includes zero and the `A^2` predictor is statistically adequate over at least the three smallest amplitudes. Failed conditions go to a later nonlinear branch and are excluded from primary M0–M3 comparison.

## Model discrimination

1. M0 scalar constant.
2. M1 constant tensor.
3. M2 position-dependent tensor only after a separately approved multi-position branch.
4. M3 frequency-dependent memory response.

A more complex model is necessary only if a simpler model shows systematic residual structure beyond combined predictor/measurement uncertainty and the next model removes that structure on held-out conditions.

## Discovery / confirmation

Discovery:
- q0 = ground prepared registry;
- directions ex, ey;
- `Omega*tau_mem = 0.10, 0.50, 1.00`;
- all four amplitudes.

Held-out confirmation:
- direction ed;
- `Omega*tau_mem = 0.25, 2.00`;
- all four amplitudes.

Confirmation data are not used for model selection.

## Primary hypotheses

**H0-SCALAR:** a single equilibrium-derived scalar `gamma0` predicts `W_cycle` for every linearly qualified discovery and held-out condition within combined uncertainty.

**H1-TENSOR:** if H0-SCALAR fails, a constant equilibrium-derived tensor `Gamma0` removes directional residual structure without requiring frequency dependence.

**H2-MEMORY:** if H1-TENSOR fails specifically through frequency-structured residuals, equilibrium-derived `G(Omega)` predicts held-out losses.

There is deliberately no hypothesis that memory must be present.

## Stop / falsification rules

- If M0 succeeds on discovery and held-out conditions, stop escalation.
- If M1 succeeds, do not invoke memory.
- If M3 fails, route first to linearity, stationarity, structural drift, bath dependence, estimator convergence, and time-step checks.
- No corner/edge crossover claim in this branch.
- No free-running winding claim in this branch.

## Sensitivity controls

Only after the primary comparison is frozen:
- `zeta_b*=0.5, 2.0`;
- `T*=0.005, 0.02`;
- half time step;
- doubled equilibrium/drive observation length.

These controls test conditional robustness and are not used to tune the primary predictor.
