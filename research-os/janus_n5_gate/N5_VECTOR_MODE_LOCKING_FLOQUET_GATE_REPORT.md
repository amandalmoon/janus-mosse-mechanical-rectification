# N5 Unguided 2D Vector Mode-Locking + Floquet Gate

## Scope
Canonical unguided baseline only: corrected 2H MoSSe GSFE, N=127 compact hexagon, theta=1.5 deg, k_perp=0, prepared from the lowest-energy zero-force minimum, m*=1, gamma*=4. The goal is to distinguish finite-run integer displacement from genuine attracting relative-periodic transport.

## Operational definitions
Let A=[a1 a2] be the direct-lattice matrix and z=(R,v) the 4D driven state. A period-1 relative orbit with lattice winding w=(m,n) satisfies

z(t+tau) = z(t) + (A w, 0, 0).

The one-period monodromy matrix M is obtained from the variational equation. The orbit is linearly attracting if

rho_F = max_i |mu_i(M)| < 1.

Finite-run integer locking and Floquet verification are kept distinct.

## 1. Fresh 91-point map replay
The canonical 13 x 7 grid (F0*=1.0...4.0 by 0.25; tau*=20...80) was regenerated with 20 transient + 40 measured cycles and 4000 RK4 steps/cycle.

- cases: 91
- finite-run mean locked: 91/91
- maximum mean lattice-lock residual: 3.9152e-12
- fresh CSV is byte-for-number identical to the shipped numerical table (all numeric differences 0).

Unique sampled windings include (0,0), (1,-1), (1,-2), (2,-3), (3,-5), and higher vector states up to the sampled high-amplitude/high-period regime.

## 2. Cycle-resolved falsification of an averaging artifact
The 91 cases were rerun while storing all 40 measured cycle displacements separately. This tests whether an integer *mean* could hide an alternating or higher-period sequence.

Results:

- same integer winding on every measured cycle: 91/91
- maximum single-cycle lattice-lock residual: 9.5530e-10
- maximum cycle-to-cycle u/v standard deviation: 1.686e-7
- maximum one-cycle relative-state residual over all measured cases: 1.5245e-9

No sampled point required an alternating two-cycle (or higher) winding sequence to explain its integer mean. This is stronger than the original mean-only map, but remains a finite-run numerical statement rather than a Floquet proof for all 91 points.

## 3. Dense staircase slices
Independent dense scans with delta F0=0.025 were run at tau*=40 and 70 (2000 steps/cycle for scouting, with representative states later rerun at 1000...8000 steps/cycle).

At tau*=40 the broad plateau intervals resolved on this grid are:

| winding | sampled F0 interval |
|---|---:|
| (0,0) | 1.000--1.575 |
| (1,-1) | 1.600--2.325 |
| (1,-2) | 2.350--2.775 |
| (2,-3) | 2.800--3.250 |
| (3,-4) | 3.350--3.450 |
| (4,-5) | 3.550--3.650 |

At higher amplitudes the staircase contains narrower interleaved states, so the sampled diagram must not be described as a simple monotone winding law.

## 4. Canonical representative point F0*=2, tau*=40
The original manuscript operating point was rerun independently.

- winding: (1,-1)
- winding unchanged at 1000, 2000, 4000, 8000 steps/cycle
- 27/27 local position/velocity basin probes recover (1,-1)
- fixed-step one-cycle relative-state closure after relaxation: 2.3712e-11

Independent monodromy integrations:

| solver | tolerance | rho_F | one-cycle closure |
|---|---:|---:|---:|
| DOP853 | rtol 1e-9 | 6.311081e-22 | 1.7864e-11 |
| DOP853 | rtol 1e-11 | 6.311081e-22 | 1.8029e-11 |
| Radau | rtol 1e-9 | 6.311099e-22 | 1.9146e-11 |

Relative spread of the leading spectral radius is 2.76e-6. Only rho_F<1 / strong attraction is interpreted; the extreme magnitude and subleading multipliers are not assigned separate physical meaning because the monodromy problem is strongly dissipative and numerically ill-conditioned in those tiny directions.

## 5. Multi-plateau relative-periodic orbit audit
Six plateau-interior states were chosen from the dense scans:

| label | F0* | tau* | winding | leading rho_F (cross-solver scale) |
|---|---:|---:|---:|---:|
| pinned | 1.2875 | 40 | (0,0) | ~1.39e-31 |
| w11 | 1.9625 | 40 | (1,-1) | ~4.62e-24 |
| w12 | 2.5625 | 40 | (1,-2) | ~5.69e-20 |
| w23 | 3.0250 | 40 | (2,-3) | ~9.47e-17 |
| w34 | 3.4000 | 40 | (3,-4) | ~5.21e-13 |
| w27_high | 3.6750 | 70 | (2,-7) | ~1.62e-15 |

For every state:

- the expected winding is recovered at 1000, 2000, 4000 and 8000 steps/cycle (24/24 timestep checks);
- DOP853 at two tolerances and Radau all give rho_F<1;
- 27/27 local basin probes recover the expected winding.

Total basin result: 162/162 passes. Maximum basin lock residual = 1.94e-13.

Newton/variational shooting reduced the one-period residuals of the representative states to solver-tolerance scale. The high-winding tau*=70 state is the least tightly conditioned, with the tight DOP853 closure about 9.2e-11 and cross-solver closures up to about 5.1e-10; its leading multiplier remains consistently ~1.618e-15 across solvers.

## 6. Amplitude continuation / hysteresis check at tau*=40
A 61-point amplitude sequence F0*=1.00...4.00 in steps of 0.05 was traversed in both increasing and decreasing directions with state continuation.

- increasing/decreasing winding matches: 61/61
- maximum lock residual across both sweeps: 1.19e-10

No hysteretic winding mismatch was found under this protocol. This does not exclude multistability under untested initial conditions, drive phases, periods, or perturbation sizes.

## 7. Interpretation
The evidence supports two claims at different strength levels:

1. **Broad sampled vector locking:** all 91 canonical grid points are finite-run integer locked, and cycle-resolved data show the same winding on every measured cycle.
2. **Attracting relative-periodic states:** the canonical (1,-1) orbit and six representative plateau states satisfy one-period closure and independent Floquet stability checks with rho_F<1, together with timestep and local-basin robustness.

The static directional threshold split does not by itself imply any particular winding map. The rocking phase structure is an additional nonlinear dynamical result of the same unguided material-anchored landscape.

## Claim boundaries
### VERIFIED within the tested reduced deterministic model
- zero-mean unguided forcing supports oblique lattice-vector transport;
- the canonical F0*=2, tau*=40 state is an attracting (1,-1) relative-periodic orbit;
- multiple distinct plateaus, including higher winding, are independently Floquet-stable;
- the 91-point sampled map is not an artifact of cycle averaging;
- the tau*=40 staircase is timestep-robust and shows no increasing/decreasing continuation mismatch under the tested protocol.

### NOT established
- every point in continuous (F0,tau) space is locked;
- every one of the 91 points has an independently cross-solver Floquet-certified orbit (only selected representatives do);
- global uniqueness of each attractor or complete basin volumes;
- experimental periods, forces, damping or masses, since the dynamical parameters remain reduced/dimensionless;
- novelty relative to the full ratchet/mode-locking literature; that remains a separate literature/novelty gate.

## Gate decision
**N5 DETERMINISTIC VECTOR MODE-LOCKING / FLOQUET GATE = PASS**

Recommended manuscript language: "The sampled amplitude-period grid contains robust integer vector-locked transport states. Cycle-resolved reruns show a single repeated winding on every measured cycle at all 91 sampled points, while the canonical (1,-1) orbit and representative additional plateaus are independently verified as attracting relative-periodic states by cross-solver Floquet analysis, timestep refinement, continuation, and local-basin tests."
