# N16 Five Reviewer Paper Audit

## 0. Source & Context Check

- **Title:** *Unguided Full-2D Mechanical Rectification and Vector Mode Locking in Finite Janus MoSSe Contacts* [Main p.1]
- **Authors:** source verification required; the supplied manuscript does not display an author line. [Main p.1]
- **Venue / year:** the working target is ACS Nano from the Research OS context; the manuscript itself is an unpublished draft and does not state a publication year.
- **Source completeness:** full main manuscript (15 rendered pages) + full Supporting Information (5 rendered pages), including six main figures, three main tables, SI Tables S1-S11, Methods, Results, Discussion, Conclusion, and Data/Code Availability.
- **User research context:** this is the user's own Janus MoSSe finite-contact mechanics/tribology project, currently in pre-submission scientific review for an ACS Nano target.
- **External literature independently checked in this audit:** yes, narrowly for closest prior-art positioning. Generic friction-diode/dissymmetry prior art is independently confirmed (Chen et al., ACS Appl. Mater. Interfaces 2026, DOI 10.1021/acsami.6c00303; Lu et al., Nano Lett. 2025, DOI 10.1021/acs.nanolett.5c01360), and finite twisted-contact edge/shape scaling prior art is independently confirmed (Koren & Duerig, Phys. Rev. B 2016, DOI 10.1103/PhysRevB.94.045401; Yan et al., JMPS 2024, DOI 10.1016/j.jmps.2024.105555; Liu 2026 preprint, arXiv:2609.08063).
- **Main audit boundary:** this review judges the supplied reduced-model paper as written. It does not treat the prior Research OS gate decisions as reviewer ground truth.

---

## 1. Domain Expert

### Core claim in field language

[원문 확인] The paper takes a DFT-derived periodic interlayer registry potential for 2H Janus MoSSe, forms finite twisted contacts by coherent phase summation over lattice sites, and asks whether broken inversion symmetry in registry space survives finite-contact cancellation strongly enough to generate direction-dependent metastability loss. It then connects the same conservative landscape to state-conditioned depinning, geometry-dependent registry selection, and periodically driven lattice-vector transport. [Methods pp.2-4; Results pp.6-11]

The strongest field-level statement is not “MoSSe is a friction diode.” It is: **within a local-GSFE finite-contact model, a non-removable inversion-asymmetric registry potential acts as the conservative symmetry-breaking ingredient for directional stability loss, while the quantitative response depends strongly on preparation, loading axis, contact boundary, and dynamical protocol.** [Results pp.6-10; Discussion pp.12-13]

### Position in prior-work landscape

[외부 검증] Generic directional friction and friction-diode behavior in 2D interfaces is not new: Chen et al. (2026) explicitly report intrinsic friction-diode behavior from asymmetric sliding potential-energy surfaces, and Lu et al. (2025) report friction dissymmetry on h-BCN. Finite-contact twist/shape/edge scaling is also established by Koren & Duerig (2016), Yan et al. (2024), and newer edge-energy work. Therefore the paper is correct to avoid a generic “first friction diode,” “first edge scaling,” or “first ratchet” claim. [Introduction pp.1-2]

[추론] The most defensible contribution is the **specific integration** of published Janus-MoSSe GSFE coefficients with (i) branch-followed prepared-state full-2D stability, (ii) same-spectrum symmetry interventions, (iii) compact-contact and competing-registry boundary tests, and (iv) relative-periodic vector transport plus stationarity-audited thermal current. I did not identify a single prior paper containing this full chain in the fresh closest-prior search; that supports cautious “combined contribution” language, not a first-ever claim.

### Physical plausibility

[원문 확인] The symmetry logic is physically plausible and unusually well controlled for a reduced model. Translation-minimized odd content is nonzero, a matched same-spectrum symmetrization eliminates the global directional bias, and exact inversion swaps static thresholds and reverses the deterministic lattice current. [Results p.6; Fig.1; Table 2]

[원문 확인] The paper also demonstrates that the effect is not a scalar material constant: the competing metastable basin has the opposite signed threshold split, a force-direction scan changes |rho| from approximately 1.6e-4 to approximately 0.419, and a damping sweep changes the driven winding qualitatively. [Results p.7; Discussion p.13; SI Table S2; SI S7 p.3]

### Assumptions an expert will immediately question

1. [원문 확인] The twisted finite interface is represented by a **sitewise local-registry sum of an aligned-registry GSFE**, while collective out-of-plane moire relaxation, buckling, atomistic edge reconstruction, and nonlocal edge energetics are absent. [Methods pp.2-4; Discussion p.13; SI S12 p.5]
2. [원문 확인] The source GSFE coefficients are treated as fixed inputs. The paper does not propagate uncertainty from the original 9x9 DFT sampling/Fourier fit into the predicted thresholds, switch angles, or vector-locking observables. [Methods p.2]
3. [원문 확인] Static thresholds use fixed twist plus a uniform center-of-mass/body-force tilt rather than a finite-stiffness spring, edge pull, center pull, or torque-controlled setup. [Methods p.3; Discussion p.13]
4. [원문 확인] No physical mapping from vertical Janus polarity reversal to the full lateral GSFE coefficient set is established. [Discussion p.13]

### Material weakness

**Weakness D1 — the paper validates a reduced interfacial mechanism more strongly than it validates a material-level prediction.** The same-spectrum controls make the *reduced-model symmetry mechanism* convincing, but the local-GSFE approximation and missing 3D relaxation remain the largest barrier to claiming that the same quantitative rectification survives in a realistic finite Janus MoSSe flake. [Discussion pp.12-13; SI S11-S12 p.5]

What would change this judgment: a Janus-specific full-3D atomistic/MLIP model that first passes the paper's predeclared GSFE contract, then reproduces the directional sign under at least one realistic loading protocol.

---

## 2. Method Reviewer

### Reconstructed design

- **Independent variables / controls:** twist angle; force sign and in-plane force orientation; contact size/shape; triangular cut orientation and surrogate edge weight; zero-force prepared basin; symmetry manipulation of the GSFE; transverse guide strength; drive amplitude/period; damping in the targeted sensitivity sweep; reduced temperature; in-plane stiffness/model form. [Methods pp.2-5; SI S2-S10]
- **Dependent variables:** branch-followed depinning forces F_c,+ and F_c,-; normalized split rho; zero-force energy ordering; integer winding (m,n); relative-periodic closure; Floquet spectral radius; trajectory-level mean lattice current; cycle-sign probability; target-winding probability; elastic strain/displacement. [Methods pp.3-4; Results pp.7-11]
- **Computational unit:** finite N-site contact for deterministic calculations; an independent stochastic trajectory for thermal inference. [Methods pp.3-4]
- **Primary controls:** same-spectrum symmetrized GSFE, exact inverted GSFE, competing metastable branch, multiple compact shape families, edge-weight sensitivity, timestep/solver checks, initial-state-memory tests, two in-plane constitutive/discretization models. [Results pp.6-12; SI]

### Strong design choices

[원문 확인] The switch from “last stable minimum anywhere” to a prepared branch is methodologically important and removes a real metastable-basin ambiguity. The 491-point continuation and independent stationary-point checkpoints support the claimed interval numerically. [Results p.7; Fig.2; SI S2 pp.1-2]

[원문 확인] The matched symmetry controls are better than comparing different materials/stackings because they intervene on the same Fourier spectrum and test exact threshold/current transformation contracts. [Methods p.3; Results p.6]

[원문 확인] The deterministic dynamics are not certified by integer rounding alone: selected states also receive relative-periodic closure, cross-solver Floquet, timestep, local-basin, and continuation checks. [Methods p.4; Results pp.9-10; SI S7 p.3]

### Measurement directness

- Prepared depinning thresholds: **direct within the declared model** (stability loss of a continued equilibrium), but proxy for experimental friction. [Methods p.3]
- Registry inversion asymmetry: **direct mathematical property of the fitted GSFE representation**, not direct measurement of a physical polarization-switching law. [Methods pp.2-3; Discussion p.13]
- Winding/Floquet state: **direct model dynamical observable**. [Results pp.9-10]
- Thermal current: **direct stochastic-model observable** at the trajectory level. [Methods p.4; Fig.6]
- “Friction diode” relevance: **proxy/interpretive** because the work does not simulate an experimental spring-driven friction-force measurement. [Discussion p.13]

### Missing controls / methodological weaknesses

**Weakness M1 — no uncertainty propagation from the source GSFE fit.** The manuscript audits coordinate choice, symmetry surgery, finite-contact geometry, solver/timestep effects, and elastic compliance, but the actual DFT/Fourier parameter uncertainty is not carried through the pipeline. [Methods p.2]

Why it matters: W2 and W3 are small (0.1 meV each), while directional asymmetry depends on phase structure. A fit-uncertainty or raw-grid-resampling analysis would tell whether the predicted directional sign/magnitude is well separated from uncertainty in the ab initio input.

**Weakness M2 — robustness axes are mostly tested one at a time.** The damping sweep is at one canonical (theta,F0,tau); the loading-axis scan is static at theta=1.5 deg; preparation dependence is static; the 91-point dynamical map fixes gamma*=4. [Results p.7; Discussion p.13; SI S7 p.3]

Why it matters: nonlinear plateaus can reorganize when parameters interact. The current text correctly scopes the claims, but it does not establish robustness of the dynamic topology under joint perturbations.

### Reproducibility from the paper alone

[원문 확인] The paper gives central equations, key parameter grids, tolerances, branch rules, sample sizes, and many audit outputs. [Methods pp.2-5; SI]

[원문 확인] The Data and Code Availability statement says numerical packages accompany the work, but no archival DOI is yet claimed. [Main p.14]

Judgment: **high internal reproducibility intent, but not fully archival reproducibility yet.** A reader with only the PDF would still need the supplied code/data package for exact contact generation, all continuation logic, seed values, and the complete figure-generation path.

---

## 3. Statistics & Reproducibility Reviewer

### Unit of analysis and pseudoreplication

[원문 확인] The thermal analysis explicitly uses the **trajectory** as the inferential unit rather than treating 100 cycles from one trajectory as independent samples. This is the correct choice and directly addresses cycle-level pseudoreplication. [Methods p.4; Results pp.10-11; SI S8 pp.3-4]

[원문 확인] The full temperature series uses N=500 independent trajectories per T*, while the high-temperature band T*=0.50-0.70 has a second independent N=500 ensemble and pooled N=1000 inference. [Methods p.4; Fig.6; SI Table S8b]

### Statistical procedures

[원문 확인] High-temperature mean-vector inference uses trajectory bootstrap and Hotelling statistics; late-block drift and initialization memory are separately checked; targeted timestep reruns test effect-size compatibility. [Methods p.4; Results pp.10-11; SI S8]

[원문 확인] At T*=0.70 the pooled mean is approximately (0.03700,-0.07645), component intervals exclude zero, and the joint zero vector is rejected under the declared test. [Fig.6; Table 3; SI Table S8b]

### Strengths

- The inferential unit is declared and appropriate. [Methods p.4]
- Effect sizes and intervals are reported, not just binary significance. [Fig.6; SI S8]
- Independent seed replication is concentrated where the signal is weakest. [Methods p.4]
- The manuscript no longer turns finite-observation significance into a “critical temperature.” [Results pp.10-11; Discussion p.13]

### Weaknesses

**Weakness S1 — no prospective sample-size or precision criterion is reported.** N=500 and pooled N=1000 produce narrow intervals, but the manuscript does not state how those N values were chosen or what CI width/effect-size precision was targeted. [Methods p.4; SI S8]

This does not invalidate the reported intervals, but it limits a reader's ability to distinguish preplanned precision from an analysis size chosen after inspecting the signal.

**Weakness S2 — no familywise multiplicity framework is used across temperatures/observables.** The paper mitigates this by treating the temperature points as an effect-size series and explicitly refusing to infer a critical boundary, so this is not a fatal problem. [Results pp.10-11]

**Weakness S3 — the reproducibility release is not yet archived with an immutable identifier.** The manuscript says there is no repository DOI yet. [Data and Code Availability p.14]

### Statistical verdict

The thermal evidence is **credible for the stated finite-protocol claims**. The major remaining statistical improvement is a small, transparent precision/N-convergence analysis rather than a different hypothesis test.

---

## 4. Skeptic

### Alternative hypothesis 1: “Rectification” is mainly a chosen state-and-axis effect, not a robust material tendency

[원문 확인] The ground branch at theta=1.5 deg has Delta F_c=+1.812463, while the competing metastable basin has Delta F_c=-0.400638. [Results p.7; SI Table S2]

[원문 확인] A force-direction scan changes |rho| from approximately 1.63e-4 to approximately 0.4186. [Results p.7]

[추론] A skeptic can therefore explain much of the headline effect as **conditional selection of a favorable basin and loading axis**. The paper now acknowledges exactly this conditioning, so this alternative weakens a broad “material diode constant” interpretation but does not contradict the narrower mechanism claim.

### Alternative hypothesis 2: Driven transport is primarily a damping/forcing phenomenon

[원문 확인] At fixed theta=1.5 deg, F0*=2, tau*=40, changing gamma* changes the asymptotic winding from (1,-10) to (1,-3), (2,-2), (1,-1), and finally pinned (0,0). [Discussion p.13; SI S7 p.3]

[추론] The same conservative GSFE can therefore support very different driven states. The lattice-vector ratchet map is not an intrinsic material fingerprint; it is a property of the **material-anchored potential plus the declared dynamical protocol**. The paper now states this correctly.

### Abstract/Discussion claim versus direct evidence

I do **not** find an unqualified causal sentence that exceeds the current reduced-model evidence. The potentially strongest wording is the statement that registry-space inversion asymmetry is the “causal conservative ingredient within the reduced model.” [Conclusion pp.13-14] The matched symmetrization and exact inversion controls provide an actual model intervention, so the causal language is defensible **only with that qualifier**. [Fig.1; Table 2]

### Decisive falsification experiment

Run a Janus-specific full-3D finite-contact model that passes the paper's GSFE contract, with:

1. free rotational relaxation;
2. at least one finite-stiffness spring or edge-pulling protocol;
3. the same two competing zero-force registry preparations;
4. the same force-direction scan.

**Falsifies/strongly weakens the mechanism transfer:** the directional sign disappears or changes unpredictably for the validated full-3D model across realistic loading protocols even though the aligned-registry GSFE asymmetry is preserved.

**Rescues/strengthens it:** the prepared-ground-state sign and inversion-control transformation survive, while only magnitudes and switch angles renormalize.

### Main weakness

**Weakness K1 — the strongest untested assumption is multiscale transfer from a local aligned-registry GSFE sum to a finite twisted, mechanically loaded interface.** [Methods pp.2-4; Discussion p.13] The internal controls make numerical artifact explanations increasingly implausible, but they cannot substitute for one higher-fidelity mechanical realization.

---

## 5. My Research Connector

### Intersection with the user's research objective

[원문 확인] This manuscript is already structured around the user's stated Research OS objective: establish a defensible computational mechanism before venue formatting, preserve rejected hypotheses, and keep claims narrower than evidence. The paper explicitly demotes global-envelope thresholds, eta-susceptibility claims, universal exponents, kinetic twist-switching language, and thermal critical-boundary language. [Methods/Results throughout; Discussion pp.12-13]

The current project is therefore no longer mainly at risk from an internal numerical inconsistency; it is at risk from **external-validity and editorial-impact questions**: “Does a reduced local-GSFE mechanism, however carefully audited, clear the material-realism bar for ACS Nano?”

### What can be borrowed immediately / preserved

1. **Prepared-branch contract:** zero-force basin enumeration -> ground-state selection -> branch continuation -> Hessian stability loss. This should remain the canonical static protocol. [Methods p.3; Results p.7]
2. **Same-spectrum symmetry falsification:** centered symmetrization + exact inversion is one of the paper's strongest causal-design elements and should not be diluted in revision. [Methods p.3; Fig.1]
3. **Thermal stationarity protocol:** trajectory-level inference, 60 burn + 100 measured cycles, independent high-T seed replication, memory-loss and late-block checks. [Methods p.4; SI S8]
4. **Boundary claim boundary:** equilibrium fixed-twist re-preparation only; no kinetic switching/hysteresis. [Results p.9; Discussion p.12]
5. **Dynamical scope:** m*=1, gamma*=4 map with a separate damping sensitivity sweep. [Methods p.4; Discussion p.13]

### What requires adaptation, not direct transfer

- The current uniform COM/body-force thresholds cannot be presented as AFM lateral-force thresholds without adding a spring/loading model. [Methods p.3; Discussion p.13]
- Reduced T* and tau* cannot be mapped to kelvin or Hz without dissipative/inertial calibration. [Discussion p.13]
- The same-spectrum inversion control cannot be presented as physical polarization reversal. [Discussion p.13]

### Realistic gaps this project could fill next

The single highest-value scientific extension is **one validated higher-fidelity mechanical layer**, not another large family of reduced-model scans. A successful Janus-specific MLIP/DFT-trained model that passes the current GSFE contract and reproduces the sign under relaxed finite-flake loading would materially change the paper's external-validity status.

### Introduction citation draft for later use

> A recent DFT-anchored finite-contact analysis of Janus MoSSe showed that registry-space inversion asymmetry can generate preparation- and loading-axis-dependent directional depinning in a full two-dimensional reduced model, while explicitly separating this effect from generic friction-diode and edge-scaling prior art. [Use only after publication; current manuscript Results 3.1-3.2]

### Discussion citation draft for later use

> The same study further found that the directional sign survives two tested in-plane compliance representations, but remains sensitive to prepared registry, loading direction, damping protocol, and edge model, underscoring the need for higher-fidelity finite-contact validation before treating the reduced thresholds as material constants. [Use only after publication; Discussion 4.1-4.5]

### Transfer risk

The main risk is overinvesting in more reduced-model robustness scans that do not address the remaining reviewer concern: transfer from the fitted local GSFE to a realistic finite contact.

---

# A. Contradiction Map

| ID | 쟁점(반드시 질문형 한 줄) | 관점 A와 주장 | 관점 B와 주장 | 충돌 유형(①사실 ②해석 ③범위 ④방법론) | 원문이 이 충돌을 해소해주는가(✅줌·⚠️부분·❌안줌, 해당 시 근거 위치) | 해소 방법(내가 할 일 한 줄) | 우선순위 |
|---|---|---|---|---|---|---|---|
| CM1 | same-spectrum symmetry control이 실제 MoSSe에서의 원인까지 충분히 확정하는가? | Domain Expert: reduced model 안에서는 강한 causal intervention이다. | Skeptic: full-3D finite contact로 transfer되기 전에는 material-level mechanism까지 확정할 수 없다. | ③범위 | ⚠️부분 — 원문은 “within the reduced model”과 full-3D 미검증을 명시한다. [Fig.1; Discussion 4.1, 4.5] | Janus-specific higher-fidelity model에서 동일 sign/inversion contract를 재검증 | ⚪ 낮음 |
| CM2 | T*=0.70까지의 nonzero mean current를 “thermal robustness”라고 불러도 되는가? | Statistics Reviewer: declared stationary protocol에서는 effect와 CI가 직접 지지된다. | Skeptic: T*가 물리 온도가 아니고 동역학도 gamma-specific이므로 material thermal robustness로 일반화하면 안 된다. | ③범위 | ✅줌 — 원문은 reduced T*, finite protocol, no extinction/Kelvin scale을 명시한다. [Fig.6; Discussion 4.3, 4.5] | 현재 scope 유지; physical-temperature 표현으로 확대하지 않기 | 🟡 중간 |
| CM3 | triangular “registry switch”를 실제 twist-controlled switching mechanism으로 볼 수 있는가? | Research Connector: geometry-controlled sign reversal은 설계 단서가 된다. | Method/Skeptic: 계산은 fixed-twist equilibrium re-preparation이며 kinetic switch/hysteresis가 아니다. | ③범위 | ✅줌 — 원문이 transition path/barrier/hysteresis 미계산을 명시한다. [Results 3.5 p.9; Discussion 4.2 p.12] | 현 equilibrium wording 유지; kinetic claim을 하려면 barrier/twist-sweep 계산 추가 | 🟡 중간 |
| CM4 | FEM+nonlinear VFF의 일치가 독립적인 material validation인가? | Domain Expert: constitutive/discretization robustness에는 의미가 있다. | Skeptic: 두 모델이 같은 GSFE와 목표 탄성상수를 공유하므로 atomistic independence는 아니다. | ④방법론 | ✅줌 — 원문이 shared GSFE/constants와 full-3D 미검증을 명시한다. [Discussion 4.1 p.12; SI S9-S12 pp.4-5] | “two in-plane representations” 이상으로 확대하지 않기 | 🟡 중간 |

### Research Gap 후보

`❌안줌`으로 판정된 Contradiction Map 행은 없음. 아래 D절의 hidden gaps는 별도의 설계/검증 공백에서 도출한다.

---

# B. Claim Reliability Table

> 이 논문은 계산/시뮬레이션 논문이므로, 주어진 rubric의 `🟢 High = direct measurement data` 조건을 충족하는 claim은 없다. 아래 `🟡 Medium`은 “근거가 약하다”는 뜻이 아니라, **모델·시뮬레이션 증거라는 범위를 반영한 등급**이다.

| ID | 주장(내 언어로 재진술) | 근거 위치(Fig·Table·섹션 번호, 없으면 "없음") | 근거 유형(직접 측정 / 통계 추론 / 모델·시뮬레이션 / 선행연구 인용 / 저자 해석 / 근거 없음) | 지지 관점 | 반박 관점 | 신뢰도(🟢High/🟡Medium/🔴Low) | 상태(Confirmed/Corrected/Demoted) | 내 검증 액션(한 문장, 없으면 "없음") |
|---|---|---|---|---|---|---|---|---|
| CR1 | published 2H GSFE는 registry-space inversion asymmetry를 갖고, same-spectrum control에서 directional response가 사라지거나 뒤집힌다. | Fig.1; Table 2; Results 3.1 p.6 | 모델·시뮬레이션 | Domain, Method, Skeptic | Skeptic: material transfer는 미확정 | 🟡Medium | Confirmed | full-3D validated potential에서 inversion/control contract 재검증 |
| CR2 | chosen +/-y axis와 ground-state preparation에서 N=127 contact는 unequal branch-followed depinning thresholds를 갖는다. | Results 3.2 p.7; Fig.2; SI Table S1/S2 | 모델·시뮬레이션 | Domain, Method, Statistics | Skeptic: state/axis conditioned | 🟡Medium | Demoted (state/axis scope) | 현재 scope 유지; realistic loading에서 sign 확인 |
| CR3 | tested compact hex/disk contacts의 threshold는 theta sqrt(N) similarity를 약 0.1% 수준으로 따른다. | Fig.3; Results 3.3 p.8; SI Table S4 | 모델·시뮬레이션 | Domain, Method | Skeptic: arbitrary edge/deformable contact로 일반화 불가 | 🟡Medium | Confirmed | 없음 |
| CR4 | rotated triangular boundaries에서 competing zero-force registries의 equilibrium energy crossing이 prepared directional sign을 바꿀 수 있다. | Fig.4; Results 3.5 p.9; SI Tables S5-S6 | 모델·시뮬레이션 | Domain, Research Connector | Method, Skeptic: kinetic switching 아님; edge-sensitive | 🟡Medium | Demoted (equilibrium-only) | kinetic claim 필요 시 barrier/hysteresis 계산 |
| CR5 | m*=1, gamma*=4에서 sampled F0-tau grid의 91/91 points가 cycle-resolved integer winding을 보이고 selected plateaus는 attracting relative-periodic states다. | Fig.5; Results 3.6 pp.9-10; SI S7 | 모델·시뮬레이션 | Domain, Method | Skeptic: damping-specific; continuous plane 미보장 | 🟡Medium | Demoted (protocol-specific) | gamma x (F0,tau) interaction map 일부 추가 |
| CR6 | stationary reduced thermal protocol에서 mean vector current는 sampled T*=0.70까지 nonzero이며 exact deterministic winding identity는 크게 혼합된다. | Fig.6; Table 3; Results 3.7 pp.10-11; SI Table S8b | 통계 추론 + 모델·시뮬레이션 | Statistics, Method | Skeptic: physical kelvin scale 아님 | 🟡Medium | Confirmed | N/precision convergence를 한 번 정량화 |
| CR7 | two tested in-plane compliance representations는 absolute thresholds를 낮추지만 directional sign을 보존한다. | Results 3.4 pp.8-9; Table 3; SI S9-S10 | 모델·시뮬레이션 | Domain, Method | Skeptic: shared GSFE/constants; no 3D validation | 🟡Medium | Demoted (in-plane-only) | Janus-specific full-3D model로 sign 재검증 |

### 인용 금지 목록

`🔴 Low`로 분류된 central claim은 없음. 다만 CR1, CR2, CR4, CR5, CR7은 표의 scope qualifier를 제거한 채 더 넓은 material/experimental fact로 인용하면 안 된다.

---

# C. 빠진 여섯 번째 관점 — Multiscale Coarse-Graining Reviewer

이 관점은 “코드가 맞는가?”나 “통계가 맞는가?”보다 한 단계 위에서, **aligned-registry DFT energy surface를 finite twisted contact의 local additive energy로 사용하는 coarse-graining 자체가 어느 오차 범위에서 정당한가**를 묻는다.

### 이 관점이 새로 묻는 것

- 9x9 aligned-registry sampling에서 얻은 Fourier coefficients의 fit residual/covariance가 finite-contact cancellation 후 threshold asymmetry에 어떻게 증폭되는가? [Methods 2.1 p.2]
- local-registry additivity가 twist-induced collective relaxation과 nonlocal moire elasticity를 무시할 때, directional sign과 boundary registry competition 중 무엇이 가장 먼저 깨지는가? [Methods 2.2, 2.6; Discussion 4.5]
- source GSFE가 local vertical relaxation을 이미 포함한 상태에서 finite flake in-plane/3D relaxation을 추가할 때 이중계산 또는 누락되는 relaxation channel은 없는가? [Methods 2.1, 2.6]

### 바꿀 수 있는 결정

현재 논문이 ACS Nano에서 “strong reduced-model mechanism paper”로 충분한지, 아니면 한 단계 높은 multiscale validation이 제출 전 필수인지에 대한 판단이 달라진다.

### 필요한 evidence

가장 직접적인 것은 (i) source 9x9 DFT grid/Fourier fit residual 또는 coefficient uncertainty, (ii) 그 uncertainty를 threshold/rho로 전파한 sensitivity distribution, (iii) 최소 한 개 Janus-specific relaxed higher-fidelity finite-contact benchmark이다.

---

# D. Research Gap

## 명시적 gap 3개

1. **Janus-specific full-3D finite-contact validation 부재.** Collective corrugation/buckling, atomistic edge reconstruction, defects, and nonlocal edge energetics are not included; a Janus-specific potential must pass the GSFE contract before quantitative atomistic validation. [Discussion 4.5 p.13; SI S11-S12 p.5]
2. **Physical calibration 부재.** Dissipation, participating mass, laboratory preparation, and mapping of reduced T*/time to kelvin/frequency are not supplied by the GSFE. [Discussion 4.5 p.13; SI S12 p.5]
3. **Physical polarity-to-GSFE law 부재.** Exact inversion is a mathematical control, not a demonstrated polarization reversal; polarity-resolved first-principles surfaces are still required. [Discussion 4.4-4.5 p.13]

## 숨은 gap 2개

1. **[추론] Source GSFE coefficient/fitting uncertainty has not been propagated into the final observables.** The manuscript imports fixed W_l and phi_l from the published fit and performs extensive downstream numerical audits, but no covariance/resampling/error envelope from the original 9x9 DFT registry data is carried into F_c, rho, switch angles, or winding maps. [Methods 2.1 p.2; Results 3.1-3.7]
2. **[추론] Robustness axes may interact nonlinearly, but the current audits are mostly one-factor-at-a-time.** Force direction, preparation, damping, boundary weight, F0/tau, and elasticity are each probed, yet no joint map tests whether their interactions create new sign reversals/multistability. [Results 3.2-3.6 pp.7-10; SI S6-S7]

---

# E. 다음 액션 3개

1. **GSFE-input uncertainty propagation pilot**
   - **Task:** obtain the original/accessible 9x9 registry energies or, if raw values remain unavailable, define a predeclared coefficient perturbation ensemble around W_l and phi_l; rerun the N=127 theta=1.5 static threshold and same-spectrum control for at least several hundred parameter draws.
   - **Input:** published GSFE coefficients; raw registry grid if obtainable; existing threshold solver.
   - **Output / decision criterion:** distribution of Delta F_c and rho; report whether the ground-state sign remains unchanged for >=95% of the declared input-uncertainty ensemble.
   - **Resolves:** Weakness M1 / hidden gap 1 / CR1-CR2 external-validity uncertainty.

2. **Targeted joint damping-drive robustness map**
   - **Task:** rerun a compact subgrid at gamma*={3,4,5,6,8} across the existing tau*=40 amplitude slice plus one additional period (for example tau*=60), using the same cycle-resolved locking criterion.
   - **Input:** existing deterministic dynamics code and canonical plateau continuation.
   - **Output / decision criterion:** identify whether the major winding plateaus persist as finite regions or collapse to gamma*=4-specific islands; update the claim only if the same winding families persist across neighboring gamma values.
   - **Resolves:** Weakness M2 / CR5 / hidden gap 2.

3. **Thermal precision/N-convergence audit**
   - **Task:** from the existing stationary trajectory pools, subsample N={100,250,500,750,1000} repeatedly at T*=0.60,0.65,0.70 and track mean-vector CI width and zero-vector decision stability.
   - **Input:** existing two-seed high-temperature raw trajectories; no new simulation required for the first pass.
   - **Output / decision criterion:** a precision curve showing CI width versus N and the minimum N at which the qualitative zero-vector decision is stable in >=95% of resamples.
   - **Resolves:** Weakness S1 and strengthens CR6 without inventing a physical critical temperature.

---

## Overall Five-Reviewer Synthesis

No reviewer identified a current internal scientific **Blocker** in the scoped reduced-model claims. The manuscript's strongest improvement is that it now exposes, rather than hides, state, axis, damping, boundary, and loading-protocol dependence.

The remaining scientific risk is concentrated in **model-input / multiscale external validity**, not in the already-audited continuation, symmetry, thermal-statistics, or solver logic. The paper is therefore best read as a carefully falsified **DFT-anchored reduced-model mechanism study**, not a calibrated prediction of experimental friction or a full atomistic Janus device simulation.

### Reviewer-stage disposition

- **Scientific Blockers:** 0
- **Major upstream improvements:** 2
  - GSFE fit/input uncertainty propagation.
  - joint damping-drive robustness beyond a single gamma slice.
- **Moderate reproducibility/statistics improvement:** 1
  - thermal N/precision convergence.
- **Writing-only major issue requiring immediate correction:** 0
- **Venue/submission issue to close later:** archival code/data identifier and final ACS Nano package.

The manuscript may proceed to **targeted revision only if the authors choose to strengthen these upstream items before venue handoff**. Under the current claim boundaries, the Five Reviewer audit does not require a new prose-only correction before the next scientific decision gate.
