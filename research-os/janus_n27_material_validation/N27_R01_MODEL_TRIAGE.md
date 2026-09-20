# N27-R01 Atomistic/MLIP Feasibility Triage

**Date:** 2026-09-20  
**Purpose:** choose an admissible execution route for the N27-R01 three-dimensional material-validity discriminator without treating elemental coverage as model validation.

## Result

**No immediately admissible off-the-shelf Janus-MoSSe bilayer potential was identified.**

This does not mean no such model exists. It means the sources checked here do not provide a model already demonstrated to reproduce the specific Janus MoSSe interlayer registry asymmetry required by the current claim.

## Candidate evidence

### 1. Shaidu et al. 2025 dispersion-aware multilayer-TMD NNP

Source: Y. Shaidu, M. H. Naik, S. G. Louie, J. B. Neaton, *npj Computational Materials* 11, 273 (2025), DOI 10.1038/s41524-025-01761-9.

Verified scope from the paper:

- transition metals Mo/W and chalcogens S/Se/Te;
- monolayers, homobilayers, heterostructures, and substrate interactions;
- validation against interlayer-spacing/sliding PES and twisted-TMD reconstruction;
- datasets reported as available upon request.

Limitation for N27-R01:

The demonstrated training/validation set is built around conventional MX2 TMD layers such as MoS2, MoSe2, MoTe2, WS2, and WSe2. Janus MoSSe mixed-face environments and the specific inversion-asymmetric 2H MoSSe registry contract used here are not an explicitly demonstrated validation target.

**Disposition:** possible BR-B candidate only after Janus-specific admission testing; not admissible by elemental coverage alone.

### 2. Jiang-family Stillinger-Weber intralayer potential

Janus MoSSe molecular-dynamics studies have used the Jiang SW family for in-plane monolayer mechanics; e.g. F. Yang et al., *Nanomaterials* 12, 1910 (2022), DOI 10.3390/nano12111910.

Strength:

- practical atomistic representation of Janus MoSSe intralayer elasticity and large-deformation mechanics.

Limitation:

- this is not a Janus-specific interlayer registry potential;
- it cannot by itself test the present registry-asymmetry mechanism.

**Disposition:** admissible only as an intralayer component of BR-A after reproducing the manuscript elastic contract.

### 3. Angeli et al. 2022 MoSSe GSFE

M. Angeli, G. R. Schleder, E. Kaxiras, *Phys. Rev. B* 106, 235159 (2022), DOI 10.1103/PhysRevB.106.235159.

Important scope clarification:

The source DFT samples lateral registry while allowing the interlayer separation to relax at each registry. Thus the present GSFE already includes local vertical-separation relaxation.

What remains missing is not local z optimization but collective finite-contact corrugation/buckling and edge-coupled reconstruction.

**Disposition:** mandatory interlayer registry benchmark for BR-A/BR-B.

### 4. Cai et al. 2019 MoSSe bilayer sliding under vertical separation

H. Cai et al., *Nano Energy* (2019), DOI 10.1016/j.nanoen.2018.11.027.

Relevant role:

First-principles MoSSe bilayer calculations evaluate sliding energetics as interlayer separation is varied, providing an independent vertical-sensitivity constraint on the interlayer landscape.

**Disposition:** use as an independent z-dependent admission benchmark where exact published values are available; otherwise obtain a small fresh DFT reference grid rather than guessing an LJ form.

### 5. Xu et al. 2026 Janus-containing moire reconstruction

B. Xu et al., arXiv:2607.23103 (submitted 25 July 2026).

Relevant role:

MoSSe/MoS2 experiment + DFT shows that Janus-induced interlayer physics can promote collective atomic reconstruction in small-twist moire bilayers.

This is not the same MoSSe/MoSSe interface and does not directly test the manuscript claim, but it makes collective reconstruction a credible material-level confounder.

**Disposition:** supports the scientific necessity of N27-R01.

## Current execution environment

Repository release requirements are limited to NumPy, Pandas, SciPy, Numba, and Matplotlib.

The active container check on 2026-09-20 found:

- ASE: unavailable
- LAMMPS Python module: unavailable
- MACE / mace-torch: unavailable
- NequIP: unavailable
- GPAW: unavailable
- pymatgen: unavailable
- PyTorch: available (CPU)

Therefore a decisive atomistic branch should not be simulated opportunistically in the current environment using a substitute model.

## Recommended route

**BR-A — validated split 3D model** is the preferred first execution branch.

1. retain an independently validated Janus MoSSe intralayer model;
2. construct or obtain a Janus-specific registry-dependent interlayer model with explicit z dependence;
3. validate held-out registry/z states against DFT;
4. run only CASE-3D-01, CASE-3D-02, and CASE-3D-CTRL from the frozen execution contract;
5. escalate to BR-C direct first-principles spot checks if model admission fails or independent models disagree.

A simple SW + Lennard-Jones combination is **not** designated a decisive closure model because it does not independently reproduce the inversion-asymmetric Janus interlayer registry contract.

## Gate implication

The literature/model triage is sufficient to choose the branch architecture but insufficient to authorize execution.

**MODEL TRIAGE: PASS**  
**ATOMISTIC EXECUTION: BLOCKED pending DEC-N27-R01 approval and an admitted/provisioned model environment.**
