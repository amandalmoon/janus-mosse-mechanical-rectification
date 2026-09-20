# Canonical Unguided Baseline Gate

## Decision

**PASS.** The audit-resolved Janus MoSSe headline calculations can be organized around one canonical model contract:

- corrected published three-shell `2H_MoSSe_Se-S-Se-S` GSFE;
- rigid N=127 compact hexagonal reference contact;
- no transverse guide (`k_perp = 0`);
- lowest-energy stable zero-force registry minimum as the prepared state;
- adiabatic continuation of that same state under longitudinal loading;
- global last-surviving-minimum envelopes retained only as diagnostics;
- mass `m*=1` and damping `gamma*=4` for the dynamical baseline.

The previous `config/production.json` is a legacy guided-v17/v18 configuration with `k_perp=25`. It is provenance, not the headline baseline. A separate `config/canonical_unguided.json` is therefore required to prevent configuration drift.

## Upstream gates inherited

1. Published Angeli three-shell material input: PASS.
2. Full-Hessian numerical implementation: PASS.
3. Prepared-state continuous interval verification: PASS.
4. Same-2H symmetry causality contract: PASS.

## Release integrity

The original audit-resolved package passes its own validator:

`AUDIT-RESOLVED RELEASE VALIDATION: PASS`

The canonicalized copy also passes the new headline-contract validator:

`CANONICAL UNGUIDED BASELINE VALIDATION: PASS`

## Dependency checks

### Reference initialization

At `theta=1.5 deg`, the zero-force root used by the vector and thermal scripts is exactly the independently enumerated lowest-energy minimum:

- root energy = `-0.5596581941027724`;
- independent ground energy = `-0.5596581941027724`;
- periodic distance to ground minimum = `0`;
- number of stable zero-force minima = `2`.

Thus vector and thermal calculations do not begin from the competing metastable family.

### Finite-size / shape calculations

The extended audit contains eight compact hexagons (`N=127...1261`) and six disk-like contacts (`N=127...931`).

Independent zero-force enumeration and ground-branch fold checks at `Theta=0` and `Theta=20` give:

- 28 shape/angle checks;
- exactly two stable zero-force minima in every check;
- maximum `|F_plus(prepared)-F_plus(shipped)| = 1.07e-14`;
- maximum `|F_minus(prepared)-F_minus(shipped)| = 1.78e-15`.

A separate branch-connectivity audit then follows all 14 shapes at `Theta = 0, 10, 15, 20` for both force signs (112 cases). Every shipped fold is continuously connected to the independently enumerated ground state:

- connected cases: `112 / 112`;
- maximum equilibrium residual along continuation: `3.96e-13`;
- minimum pre-fold soft eigenvalue: `0.07408 > 0`;
- maximum single continuation jump: `0.01233` lattice-length units;
- distance from the `0.999 F_c` continued state to the shipped fold: at most `0.00591` lattice-length units.

Therefore the extended size/shape collapse uses the same prepared-state meaning as the N=127 headline threshold.

### Boundary registry calculations

For both canonical high-angle boundary cases (`20 deg`, `25 deg` cuts), the two candidate registry states A and B were checked at the ground-state switch and at `+/-0.01 deg` around it.

All 12 tested states are genuine zero-force stationary stable minima:

- maximum gradient norm: `1.05e-15`;
- minimum Hessian eigenvalue: `5.89223 > 0`.

Thus the boundary calculation is not comparing arbitrary registry coordinates; it compares actual competing prepared minima and chooses the lower-energy one.

### Vector mode locking

`vector_mode_map.py` uses:

- the same 2H material;
- the same N=127 compact hexagon;
- `theta=1.5 deg`;
- `k_perp=0`;
- `m*=1`, `gamma*=4`;
- the zero-force ground minimum as the initial position.

Only `F0` and the period are scanned. Hence the vector map is a dynamical extension of the canonical unguided baseline rather than a separate model.

### Thermal calculation

`thermal_cluster_audit.py` uses the same material, N=127 contact, `theta=1.5 deg`, `F0=2`, period `40`, `gamma=4`, and `k_perp=0`. It first relaxes the deterministic trajectory from the same ground minimum and then adds BAOAB noise. Temperature is therefore the added variable, not a change of mechanical baseline.

### Guided calculations

No headline audit script imports the legacy guided engine. The guide is an explicitly separate device-control branch. The reference `k_perp=25` calculations must not define the static, size/shape, boundary, vector, or thermal headline quantities.

## Packaging correction

The release structure previously contained an ambiguity: `config/production.json` still stores the old guided `k_perp=25` settings. This does not contaminate the audit-resolved scripts, which are unguided, but it can mislead a future rerun or reviewer.

The canonicalized release therefore adds:

- `config/canonical_unguided.json` — authoritative headline contract;
- `validate_canonical_baseline.py` — fails closed if the headline model drifts away from the unguided prepared-state definition;
- explicit README language that `config/production.json` is legacy guided provenance only;
- branch-connectivity and boundary-stationarity evidence tables.

## Gate status

**CURRENT STAGE:** Canonical model freeze  
**VERIFIED:** material, preparation, unguided status, static branch meaning, size/shape branch inheritance, boundary preparation, vector initialization, thermal initialization.  
**SECONDARY ONLY:** guided confinement and elastic model-form extensions.  
**REJECTED AS HEADLINE BASELINE:** `k_perp=25` / old guided production configuration.  
**NEXT GATE:** finite-size/shape robustness should now be assessed using this frozen contract, without changing material, preparation, or confinement assumptions.
