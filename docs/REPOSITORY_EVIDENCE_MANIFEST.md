# Repository Evidence Manifest Specification

This file defines what must exist before the repository-level provenance gate can pass. It is a schema/specification, not evidence.

## Required top-level layout

```
archive/
reproducibility/
submission/
docs/
```

## Required metadata for every evidence bundle

- claim IDs supported
- provenance class: MEASURED / SIMULATION_EXECUTED / SYNTHETIC_TEST / ILLUSTRATIVE / PLACEHOLDER
- exact Git commit SHA
- code path / entry point
- data source and input file checksums
- environment lock or package versions
- random seed(s), if stochastic
- full parameter set
- output file checksums
- execution timestamp
- command or workflow used to reproduce
- expected validation thresholds
- PASS / FAIL / BLOCKED status
- supersedes / superseded-by relation when applicable

## Canonical reproducibility bundle

The canonical bundle should contain, at minimum, machine-readable evidence for:

1. published GSFE implementation and asymmetry diagnostics;
2. prepared-state branch enumeration/continuation and stability-boundary checks;
3. matched symmetrization and exact-inversion controls;
4. finite-size/shape similarity calculations;
5. triangular-boundary registry competition and edge-weight sensitivity;
6. deterministic rocking grid, cycle-resolved windings, and Floquet checks;
7. thermal trajectory-level inference, stationarity, independent-seed, bootstrap/Hotelling, and timestep checks;
8. linear FEM validation;
9. independently reconstructed nonlinear VFF validation;
10. Tier-2 interlayer-potential prescreen and explicit no-go record;
11. clean-replay report tied to the exact code/data commit used for the manuscript.

## Submission bundle

The submission bundle should identify the exact frozen versions of:

- main manuscript source and rendered PDF;
- Supporting Information source and rendered PDF;
- publication figures at final size;
- cover letter;
- citation audit;
- Red Team audit;
- Five Reviewer audit;
- final ACS Nano submission audit;
- data/reproducibility deposition identifier once available.

## Hard rule

`ILLUSTRATIVE` and `PLACEHOLDER` artifacts may be retained for history but must never be referenced as manuscript evidence.

No repository status line may say an audit or gate is passed unless the corresponding artifact is present or immutably linked.
