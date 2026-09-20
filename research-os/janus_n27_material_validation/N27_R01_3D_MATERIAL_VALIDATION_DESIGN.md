# N27-R01 3D Material-Validity Discriminator — Simulation Design

**Design date:** 2026-09-20  
**Issue:** N27-R01 — material-model external validity  
**Owner:** experiment/simulation  
**Research OS stage:** review-repair -> experiment/simulation design  
**Execution status:** **NOT STARTED — HUMAN BRANCH GATE PENDING**

## 1. Decision question

Does the headline prepared-state directional sign survive when the finite Janus MoSSe contact is allowed to relax in three dimensions with atomistically meaningful intralayer mechanics and a Janus-specific interlayer registry contract?

The primary object is not exact agreement of absolute thresholds. The discriminator is whether the material-level extension preserves or destroys the reduced-model mechanism under a pre-registered canonical protocol.

Primary endpoint:

[
Delta F_c^{3D}=F_{c,+}^{3D}-F_{c,-}^{3D}.
]

The current reduced model has (Delta F_c>0) at the canonical (N=127,	heta=1.5^circ) prepared ground-state contact.

## 2. Why this branch is necessary

The present GSFE already contains **local registry-by-registry vertical-separation relaxation** inherited from the source DFT calculation. N27-R01 is therefore not a complaint that the current model has “no z relaxation.” The missing physics is collective finite-contact three-dimensional response: out-of-plane corrugation/buckling, coupling of neighboring registry regions, atomistic edge relaxation/chemistry, and possible load-dependent interlayer reorganization.

Relevant source constraints:

- Angeli, Schleder, and Kaxiras, *Phys. Rev. B* 106, 235159 (2022), DOI 10.1103/PhysRevB.106.235159 — material-specific MoSSe GSFE and registry-by-registry relaxed interlayer separation.
- Cai et al., *Nano Energy* (2019), DOI 10.1016/j.nanoen.2018.11.027 — first-principles MoSSe bilayer sliding energetics under different interlayer separations.
- Shaidu et al., *npj Comput. Mater.* 11, 273 (2025), DOI 10.1038/s41524-025-01761-9 — transferable dispersion-aware multilayer-TMD NNP for Mo/W with S/Se/Te, but Janus MoSSe is not an explicitly demonstrated validation target.
- Yang et al., *Nanomaterials* 12, 1910 (2022), DOI 10.3390/nano12111910 — SW-based Janus MoSSe intralayer mechanics; useful for the intralayer layer only, not a sufficient interlayer validation.
- Xu et al., arXiv:2607.23103 (2026) — experimental/DFT evidence that Janus-containing moire bilayers can reconstruct collectively at small twist, strengthening the need for this discriminator.

No off-the-shelf potential is admitted solely because its element set contains Mo, S, and Se.

## 3. Bounded branch budget

Only three model routes are permitted.

### BR-A — preferred: validated split 3D model

- intralayer: Janus MoSSe model independently checked against the manuscript’s elastic contract;
- interlayer: Janus-specific registry-dependent (U(mathbf r,z)) fitted/validated to MoSSe DFT references;
- finite contact: full xyz relaxation of the top Janus flake, with the bottom interface represented explicitly or by a validated registry-dependent substrate interaction.

This route is preferred because it directly targets the missing collective-z degree of freedom without requiring a broad new materials campaign.

### BR-B — transferable multilayer-TMD NNP

A published Mo/W-S/Se/Te multilayer NNP may be used only if its actual model weights are available **and** it passes the Janus-specific admission tests below. Elemental coverage alone does not establish Janus transferability.

### BR-C — escalation: direct first-principles spot check

If BR-A and BR-B disagree or cannot pass the admission gate, perform a deliberately small first-principles validation rather than tuning a potential until the desired sign appears.

No fourth branch is allowed without a new human decision.

## 4. Potential admission gate — GATE-MODEL-3D

A candidate 3D model must pass **all** applicable checks before the finite-contact directional test.

### 4.1 Intralayer contract

At zero load, the candidate Janus MoSSe layer must:

1. relax to the correct 2H topology without reconstruction to another phase;
2. reproduce the reference in-plane lattice constant and (C_{11},C_{12}) used by the current FEM/VFF hierarchy to within **5%**;
3. have no obvious mechanical instability in the small-strain Hessian/phonon proxy used by the chosen implementation.

The 5% tolerance is an internal admission criterion, not a claimed material uncertainty.

### 4.2 Interlayer registry contract

Against an independent validation set not used for post hoc parameter rescue, the candidate must:

1. preserve the ordering of the benchmark low/high-energy registries;
2. reproduce the sign of the translation-minimized inversion-odd diagnostic and the sign of the first-shell triad invariant;
3. achieve normalized energy RMSE <= **10% of the DFT GSFE corrugation** over the validation set;
4. reproduce the DFT trend that compression increases the relevant MoSSe sliding barrier;
5. yield a stable equilibrium interlayer separation for every validation registry.

If published data are insufficient to define the z-dependent validation set without uncontrolled figure digitization, the branch must obtain a small fresh DFT reference grid before admission. Missing reference data are not to be replaced by an assumed Lennard-Jones form.

### 4.3 Independence rule

The points used to tune a new (U(mathbf r,z)) are training/calibration points. The admission score must be computed on held-out registries and/or held-out z offsets. A fit to the same points on which it is judged does not close N27-R01.

## 5. Minimal new DFT reference grid if required

This is the preferred small-data contract if no sufficiently validated Janus interlayer model is available.

Use the same 2H MoSSe chemical orientation as the manuscript and evaluate a pre-registered set of registry/z states:

- three physically distinct high-symmetry registry classes;
- five z offsets around each relaxed separation: approximately (-0.30,-0.15,0,+0.15,+0.30) Å;
- energies and atomic forces retained;
- one additional off-symmetry registry per shell reserved as a held-out validation point.

The exact electronic-structure functional, dispersion treatment, k mesh, cutoff, dipole correction, convergence tolerances, and pseudopotential identifiers must be frozen before calculation and recorded verbatim. The DFT level should be chosen to remain compatible with the source GSFE as far as practical; any unavoidable method change is a separate model discrepancy, not silently merged into the same validation score.

## 6. Finite-contact test set — fixed before execution

### CASE-3D-01 — primary canonical discriminator

- chemistry/orientation: same 2H Janus MoSSe registry contract as the manuscript;
- contact: compact (N=127) reference family;
- imposed twist: (	heta=1.5^circ);
- transverse guide: none;
- preparation: lowest-energy stable zero-force state under the 3D model;
- loading: uniform longitudinal (+y) and (-y), branch-followed from the **same prepared state**;
- internal degrees of freedom: full allowed xyz relaxation of the mobile finite contact;
- output: (F_{c,+}^{3D},F_{c,-}^{3D},Delta F_c^{3D},ho^{3D}), prepared-state identity, and smallest projected stability eigenvalue along each branch.

### CASE-3D-02 — pre-registered off-canonical robustness point

Same protocol at (	heta=2.0^circ).

This angle is selected in advance because it is separated from the isolated higher-order boundary near (2.97338566^circ) while probing a noncanonical twist. It is not selected after seeing the 3D result.

### CASE-3D-CTRL — inversion/code control

Apply exact lateral registry inversion to the admitted interlayer model while leaving the numerical protocol unchanged.

Expected code-level contract:

[
F_{c,+}[U_{m inv}] simeq F_{c,-}[U],qquad
F_{c,-}[U_{m inv}] simeq F_{c,+}[U].
]

Failure of this control blocks physical interpretation and routes the problem to implementation/model verification.

### Explicitly deferred

The triangular boundary switch, thermal dynamics, and the full 91-point rocking map are **not** part of the first 3D branch. They are downstream only if CASE-3D-01 passes and the result would materially affect those claims.

## 7. Quasistatic threshold protocol

For each physical case:

1. minimize the zero-force 3D contact from multiple nearby perturbations sufficient to identify the lowest-energy stable prepared state;
2. freeze the prepared family identity;
3. continue that family under (+y) and (-y) loading without basin switching;
4. at each load step, converge forces and energy to predeclared tolerances;
5. monitor the smallest projected Hessian/stability eigenvalue using an iterative method appropriate to the model;
6. bracket and refine the first loss of stability;
7. repeat with a factor-of-two tighter force-step/refinement schedule.

The threshold is accepted only when the refined value changes by < **1%** and the directional sign is unchanged.

Rigid translations and any intentionally fixed global rotation/twist are projected from the stability problem so that trivial modes are not mistaken for depinning.

## 8. Primary decision rules

### MATERIAL_SIGN_SURVIVES

Required:

1. GATE-MODEL-3D passes;
2. CASE-3D-CTRL passes;
3. CASE-3D-01 has (F_{c,+}^{3D}>F_{c,-}^{3D}) with a split larger than the numerical refinement uncertainty;
4. the same sign is retained at CASE-3D-02;
5. the prepared zero-force family remains well defined and stable.

Consequence:

- N27-R01 may be demoted from MAJOR after Claim-Evidence review;
- absolute-threshold agreement is reported as a separate quantitative result rather than required for sign-level closure.

### MATERIAL_SIGN_FAILS

Triggered if an admitted 3D model produces a converged sign reversal or a split statistically/numerically indistinguishable from zero at CASE-3D-01.

Consequence:

- material-level C2–C7 become DIRTY;
- the paper must be narrowed to the GSFE reduced-model mechanism or scientifically redesigned;
- no parameter retuning is allowed to “recover” the preferred sign.

### MATERIAL_VALIDATION_INCONCLUSIVE

Triggered if:

- no candidate model passes GATE-MODEL-3D;
- admitted models disagree on the primary sign;
- finite-contact results depend qualitatively on an unresolved substrate/edge representation;
- numerical convergence cannot resolve the sign.

Consequence:

- N27-R01 remains OPEN;
- route to BR-C or narrow material wording;
- do not average conflicting models into an artificial consensus.

## 9. Negative-result preservation

All attempted candidate models, failed admission tests, and sign-changing cases must remain in the provenance record.

Forbidden:

- selecting only the potential that preserves the headline sign;
- tuning z stiffness, edge parameters, force cutoff, or registry phase after inspecting the desired endpoint;
- adding extra twists until a favorable example is found;
- treating a failed Janus-specific validation as a plotting or prose problem.

## 10. Provenance requirements

Record for every execution:

- exact code commit;
- potential/model name, version, file hash, and license/source;
- training/calibration dataset identity;
- DFT input/output hashes for any new reference points;
- atomistic structure files before and after relaxation;
- minimizer, force/stress tolerances, neighbor cutoffs, cell/boundary conditions;
- continuation step sizes and refinement levels;
- projected-eigenvalue solver settings;
- CPU/GPU type and software versions;
- complete raw threshold branches, including failures.

No main-text claim may depend on an unversioned local model file.

## 11. Dependency invalidation policy

**Design alone does not dirty the existing N25/N26 scientific artifacts.**

If new 3D data are executed and materially change a headline claim, propagate DIRTY status from the new experiment through:

[
EXP	ext{-}N27	ext{-}R01
ightarrow CLAIM	ext{-}C2ldots C7
ightarrow ARG/N25 Figures
ightarrow N27 Manuscript
ightarrow Five Reviewer.
]

If the 3D branch only confirms the sign without changing plotted numerical values or claim scope, the existing figures need not automatically be regenerated; Claim-Evidence and manuscript scope still require explicit revalidation.

## 12. Current feasibility

The current reproducibility environment is NumPy/Pandas/SciPy/Numba/Matplotlib only. ASE, LAMMPS, MACE/NequIP, GPAW, and pymatgen are not present in the active execution environment.

Therefore this design is **execution-ready as a scientific contract, but the decisive atomistic branch is not executable in the current container without a separately provisioned atomistic/DFT environment and an admitted Janus-specific model**.

## 13. Gate decision

**GATE-DESIGN: PASS**

The protocol, primary endpoint, controls, failure criteria, branch budget, and provenance plan are fixed sufficiently to prevent post hoc claim rescue.

**HUMAN GATE — MATERIAL NEW BRANCH: PENDING**

No new 3D scientific data are authorized by this design document alone.
