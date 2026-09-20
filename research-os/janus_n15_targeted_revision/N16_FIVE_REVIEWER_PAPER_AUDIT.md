# N16 Five Reviewer Paper Audit

## 0. Source & Context Check

- **Source reviewed:** full main manuscript (`Janus_MoSSe_RedTeamScoped_Manuscript_v4`) plus full Supplementary Information (`Janus_MoSSe_RedTeamScoped_SI_v4`).
- **Paper title:** *Unguided Full-2D Mechanical Rectification and Vector Mode Locking in Finite Janus MoSSe Contacts*. [Main p.1]
- **Authors / final venue / publication year:** not supplied in the manuscript source packet; source verification required.
- **Research context:** the project tests whether the published Janus MoSSe GSFE, when integrated over a finite contact, supports prepared-state directional depinning and zero-mean vector transport, while explicitly auditing symmetry, preparation, finite size/boundaries, thermal stationarity, and in-plane compliance. [Main pp.1-5]
- **External literature check in this pass:** not re-run. Literature positioning below is therefore either `[원문 확인: 저자 서술]` from the manuscript/reference list or `[추론]`; no new novelty verdict is imported as reviewer ground truth.
- **Source completeness constraints:** the manuscript states that numerical release packages accompany the work, but the Five Reviewer source packet used here contains manuscript + SI rather than the full executable release, so code-level reproducibility is not independently rerun in this reviewer pass. [Data and Code Availability, Main p.14]

---

## 1. Domain Expert

### Core claim in field language

[원문 확인] The paper proposes a **state-conditioned, anisotropic depinning mechanism in a finite incommensurate contact**: a laterally inversion-asymmetric MoSSe registry-energy landscape yields different branch-followed stability-loss thresholds under opposite loading along one chosen crystallographic axis; the same reduced landscape also supports oblique lattice-vector mode locking under unbiased periodic forcing. [Abstract, Main p.1; Results 3.2, p.7; Results 3.6, pp.9-10]

The strongest physically defensible formulation is not “MoSSe is a universal friction diode,” but rather: **within the specified finite-contact reduced model, registry-space inversion asymmetry is necessary for the observed directional response under the tested preparation and loading protocol.** The manuscript itself now makes this scope explicit. [Discussion 4.1, p.12; Conclusion, pp.13-14]

### Position in the field

[원문 확인: 저자 서술] The manuscript correctly treats generic structural-lubricity scaling, edge effects, friction diodes, and phase locking as prior art, and narrows its contribution to the combined material-anchored chain linking published MoSSe GSFE, prepared-state 2D depinning, matched symmetry controls, finite-contact geometry, and lattice-vector transport. [Introduction, pp.1-2; Discussion 4.2-4.4, pp.12-13]

[추론] That positioning is technically more credible than a component-level novelty claim because the main ingredients individually have established precedents in the cited literature. However, without a new independent literature search in this reviewer pass, the exact novelty of the *combined chain* remains a literature-audit question rather than a fact established by the paper itself. [Introduction, p.1; References, pp.14-15]

### Physical plausibility

[원문 확인] The static mechanism is physically coherent inside the model: the lowest-energy zero-force basin at theta=1.5 deg has F_c,+*=3.071135 and F_c,-*=1.258672, while the competing metastable basin has the opposite signed split. [Results 3.2, p.7; SI Table S1, p.1]

[원문 확인] The same-spectrum controls are unusually valuable: matched symmetrization makes the paired/global threshold envelope direction-degenerate, whereas exact spatial inversion swaps thresholds and reverses deterministic current. [Results 3.1, p.6; SI Table S2, pp.1-2]

This is strong evidence that **registry inversion asymmetry is a necessary conservative ingredient in this reduced landscape**. It is not evidence that experimental out-of-plane polarization alone determines the sign; the manuscript correctly separates those statements. [Discussion 4.4, p.13]

### Immediate expert questions

1. **How much of the mechanism survives material-level relaxation beyond the local GSFE approximation?** The contact is built as a sitewise sum of a registry surface whose local interlayer separation was relaxed, but collective out-of-plane corrugation, reconstructed edges, and nonlocal interactions are absent. [Methods 2.1, p.2; Discussion 4.5, p.13; SI S12, p.5]
2. **How experimentally accessible is the assumed preparation?** The ground-state and metastable basins have opposite rectification signs, so laboratory history is not a nuisance parameter but part of the observable definition. [Results 3.2, p.7; SI Table S1, p.1]
3. **How specific is the response to the loading geometry?** A force-direction scan gives nearly zero rectification on one tested symmetry-axis orientation and ~0.4186 on a strong orientation. [Results 3.2, p.7]
4. **How specific is the dynamical phase map to dissipation?** The verified damping sweep changes winding substantially and eventually pins the state. [Discussion 4.3, p.13; SI S7, p.3]

### Material weakness

[추론] The paper's strongest mechanism statement is still one modeling level above a material prediction. The symmetry falsification is excellent **within the imported GSFE model**, but the study does not yet show that the same branch hierarchy, sign, and dynamical response survive a Janus-specific fully relaxed finite-flake model. [Methods 2.6, pp.3-4; Discussion 4.5, p.13; SI S11-S12, p.5]

**What would change the judgment:** a Janus-specific interlayer potential or direct first-principles/MLIP finite-flake calculation that passes the stated GSFE contract and reproduces the branch-sign hierarchy under at least two mechanically distinct loading protocols. [SI S11-S12, p.5]

---

## 2. Method Reviewer

### Study reconstruction

- **Independent/control variables:** twist angle; loading sign/direction; prepared zero-force basin; finite-contact size/shape; triangular cut orientation/edge weighting; drive amplitude F0* and period tau*; damping gamma* in a targeted sensitivity sweep; reduced temperature T*; in-plane stiffness/model representation. [Methods 2.2-2.9, pp.2-5; SI S5-S10, pp.2-4]
- **Primary dependent variables:** branch-followed depinning thresholds F_c,+*, F_c,-* and normalized split rho; zero-force family energy ordering; lattice winding (m,n); relative-periodic closure/Floquet multiplier; trajectory-level mean vector current; cycle-sign/target-winding probabilities. [Methods 2.4, 2.7, 2.8, pp.3-4]
- **Computational unit:** a finite N-site contact for static calculations; a trajectory for thermal inference. [Methods 2.2, p.2; Methods 2.8, p.4]
- **Key controls:** same-spectrum symmetrization, exact spatial inversion, 3R material controls, competing metastable branch, size/shape extensions, boundary weights, solver/time-step/basin checks, two in-plane compliance representations. [Results 3.1-3.7, pp.6-11; SI S1-S12]

### What the design identifies well

[원문 확인] The switch from “last surviving minimum anywhere” to **branch-followed prepared-state depinning** is methodologically important. The dense/adaptive 491-point continuation and independent stationary-point checkpoints directly address basin-selection ambiguity over 0-3 deg. [Methods 2.4, p.3; Results 3.2, p.7]

[원문 확인] The symmetry controls are appropriately matched to the mechanism question: they alter inversion structure without replacing the material spectrum by a chemically unrelated interface. [Methods 2.3, p.3; Results 3.1, p.6]

[원문 확인] The deterministic transport claims are also stronger than a mean-displacement classification because all 91 sampled points were rerun cycle-by-cycle, and representative plateaus received cross-solver Floquet, time-step, continuation, and basin tests. [Results 3.6, pp.9-10; SI S7, p.3]

### Missing or limited controls

1. **Mechanical loading control remains limited.** Static and dynamic loading use a spatially uniform COM/body-force tilt at fixed imposed twist. No finite-stiffness spring pull, edge pull, center pull, torque, or rotational relaxation is simulated. [Methods 2.4, p.3; Discussion 4.5, p.13; SI S12, p.5]
2. **The two in-plane relaxations are not independent material models.** They share the same GSFE and target elastic constants, so agreement rules out one discretization/constitutive artifact but not a shared input error. [Methods 2.6, pp.3-4; Results 3.4, pp.8-9]
3. **Boundary switching is equilibrium family selection, not a switching kinetics experiment.** No A→B barrier, twist ramp, or hysteresis is computed. [Results 3.5, p.9; SI S6, pp.2-3]
4. **Dynamical-map completeness is deliberately limited.** Only representative plateaus have Floquet/basin validation; all 91 points are cycle-resolved but not all are globally certified unique attractors. [Results 3.6, pp.9-10]

### Direct vs proxy measurements

- Branch loss from Hessian stability is a **direct model observable** for the defined quasistatic depinning criterion. [Methods 2.4, p.3]
- The reduced-model threshold is only a **proxy for experimental friction** because loading stiffness, dissipative calibration, participating mass, edge stress localization, and physical time/temperature are not calibrated. [Discussion 4.5, p.13]
- Floquet rho_F<1 is a **direct local stability diagnostic** of the selected relative-periodic orbit, but not a global basin/uniqueness measurement. [Methods 2.7, p.4; Results 3.6, p.10]

### Reproducibility

[원문 확인] The paper provides unusually specific numerical protocols and states that raw/summary outputs and releases accompany the submission. [Methods 2.10, p.5; Data and Code Availability, p.14]

[확인 못 함] The executable release, dependency lock/environment file, seeds, and canonical commands are not part of the manuscript+SI packet used in this reviewer pass, so **end-to-end reproduction from the paper alone is not verified here**. [Data and Code Availability, p.14]

### Material weakness

[추론] The major method risk is not internal numerical sloppiness but **shared-model closure**: many falsification layers operate downstream of the same published local GSFE representation. A common missing physical ingredient could survive all of them. [Methods 2.1-2.8, pp.2-4]

**What would change the judgment:** reproduce the static sign and at least one dynamical plateau in a higher-fidelity finite-flake model that independently represents edge reconstruction/out-of-plane relaxation and a nonuniform pulling protocol.

---

## 3. Statistics & Reproducibility Reviewer

### Unit of analysis and dependence

[원문 확인] The thermal section correctly uses the **trajectory** as the inferential unit rather than treating cycles from one trajectory as independent replicates. [Methods 2.8, p.4; Results 3.7, pp.10-11]

[원문 확인] The full T*=0.02-0.70 series uses N=500 trajectories per temperature after 60 burn + 100 measured cycles; T*=0.50-0.70 is independently repeated with a second N=500 seed ensemble and pooled for high-temperature joint-current inference. [Methods 2.8, p.4; SI Tables S8a-S8b, pp.3-4]

### Statistical adequacy

[원문 확인] The paper reports trajectory-level bootstrap intervals and a two-component Hotelling test at high T, plus late-block stationarity, initialization-memory, independent-seed, and timestep checks. [Results 3.7, pp.10-11; SI S8, pp.3-4]

This is a substantial improvement over a cycle-level analysis because it addresses pseudoreplication and finite burn-in. The thermal wording is appropriately effect-size based: the paper does **not** infer an extinction temperature from the sampled significance pattern. [Results 3.7, p.11]

### Statistical weaknesses

1. **No prospective precision/power target is reported.** N=500 or pooled N=1000 is large, but the manuscript does not state a predeclared CI width or effect-size criterion that determined sample size. [Methods 2.8, p.4; SI S8, pp.3-4]
2. **Across-temperature multiplicity is not controlled familywise.** The paper avoids turning these repeated tests into a critical-temperature claim, which limits the consequence, but statements such as “nonzero through the largest sampled T*” are still based on multiple sampled temperatures. [Results 3.7, p.11; Table 3, pp.11-12]
3. **The deterministic 91-point grid is a structured parameter scan, not a random sample.** Descriptions such as “broad sampled locking” are valid, but any area/frequency interpretation of locked states in continuous parameter space would require adaptive boundary estimation and uncertainty. [Results 3.6, pp.9-10]
4. **The force-direction and damping sensitivity scans are targeted, not exhaustive.** They are sufficient to falsify invariance but not to characterize a complete anisotropy surface or dynamical phase diagram. [Results 3.2, p.7; Discussion 4.3, p.13]

### Reproducibility weakness

[확인 못 함] The paper says release artifacts are retained, but this reviewer packet does not expose the raw trajectories, exact random seeds, or executable environment. Therefore reproducibility is **documented but not independently demonstrated in this pass**. [Methods 2.10, p.5; Data and Code Availability, p.14]

**What would change the judgment:** include a machine-readable environment/lockfile, canonical run commands, seed manifest, and one deterministic CI-style script that recomputes Table S8b/Figure 6 from raw trajectory summaries.

---

## 4. Skeptic

### Alternative hypothesis 1: preparation-conditioned basin physics, not an intrinsic device diode

[원문 확인] At theta=1.5 deg the prepared ground branch has Delta F_c*=+1.812463, while the competing metastable basin has Delta F_c*≈-0.400638. [Results 3.2, p.7; SI Table S1, p.1]

[추론] A laboratory contact that is not reliably re-prepared into the lowest zero-force basin could therefore show a different sign or a history-dependent mixture. The manuscript now acknowledges state conditioning, but experimentally “intrinsic rectification” would still require a demonstrated state-preparation protocol.

### Alternative hypothesis 2: protocol anisotropy, not a material-wide rectification law

[원문 확인] A tested symmetry-axis loading orientation gives |rho|≈1.63×10^-4, while a strong tested direction gives |rho|≈0.4186. [Results 3.2, p.7]

[추론] The headline effect may be best viewed as an **anisotropic response channel of a particular finite geometry**, rather than a single material scalar. The conclusion now correctly limits the result to the chosen loading axis. [Conclusion, pp.13-14]

### Alternative hypothesis 3: reduced-dynamics tuning determines the observed winding staircase

[원문 확인] At fixed theta=1.5 deg, F0*=2, tau*=40, the asymptotic winding varies from (1,-10), (1,-3), (2,-2), (1,-1), to pinned (0,0) across the tested gamma* sweep. [Discussion 4.3, p.13; SI S7, p.3]

[추론] The vector staircase is therefore not a material phase diagram of MoSSe; it is a response of the material-anchored conservative landscape coupled to a chosen reduced dissipative model.

### Causal-overclaim check

No unqualified statement such as “physical Janus polarity causes the experimental diode” was found. The strongest causal wording is bounded to the model, e.g. the conclusion says registry-space inversion asymmetry is the “causal conservative ingredient within the reduced model.” [Conclusion, p.13]

[추론] This phrasing is defensible as a **within-model intervention claim** because same-spectrum symmetrization nulls the global bias and exact inversion reverses it. It should not be generalized beyond the tested model class. [Results 3.1, p.6]

### Decisive falsification experiment

**Test:** build a Janus-MoSSe finite-flake model with independently validated full 3D interlayer/intralayer physics; prepare both zero-force basins; apply at least two mechanical driving protocols (uniform body force and finite-stiffness edge/center spring) and allow rotational relaxation. Recompute directional stability and one canonical rocking state.

- **Falsifies/strongly weakens the present mechanism:** the prepared-ground threshold split changes sign or collapses under realistic relaxation while the imported local-GSFE model predicts a robust sign; or the inversion/symmetrization contract no longer tracks directionality.
- **Rescues/strengthens it:** the ground-state sign, inversion reversal, and at least one oblique locked state persist across the higher-fidelity model and both loading protocols.

### Material weakness

The paper has performed many **internal falsification tests**, but the decisive external-model falsification has not yet been run. [Discussion 4.5, p.13; SI S11-S12, p.5]

---

## 5. My Research Connector

### Intersection with the user's research objective

[원문 확인] The project is already organized around a defensible claim hierarchy: prepared-state static rectification, symmetry causality within the model, finite-contact scaling/boundary competition, deterministic vector locking, stationary thermal drift, and in-plane robustness. [Table 3, pp.11-12]

For an ACS Nano-targeted computational paper, the most useful feature is that **negative and scope-defining results are already integrated into the scientific story** rather than hidden: metastable sign reversal, axis dependence, damping dependence, edge sensitivity, and failure of the Tier-2 atomistic candidate all constrain the headline claim. [Results 3.2-3.6, pp.7-10; Discussion 4.1-4.5, pp.12-13; SI S11, p.5]

### Methods immediately reusable in this project

1. **Prepared-branch continuation instead of global envelopes** — transferable as-is for the current model. [Methods 2.4, p.3]
2. **Matched same-spectrum symmetry controls** — transferable as-is for model-internal mechanism isolation. [Methods 2.3, p.3]
3. **Cycle-resolved winding + representative Floquet checks** — transferable as the correct evidence ladder for deterministic locking, provided future parameter extensions keep the same classification tolerance and solver audits. [Methods 2.7, p.4; SI S7, p.3]
4. **Trajectory-cluster thermal inference** — transferable as-is for this reduced stochastic model; physical temperature mapping still requires independent calibration. [Methods 2.8, p.4; SI S8, pp.3-4]
5. **Hard GSFE contract for future atomistic/MLIP models** — immediately useful as a predeclared acceptance test, but the numerical tolerances remain a project design choice rather than a universally established material standard. [SI S11, p.5]

### Transfer risks

- Do not reuse the current gamma*, mass, T*, or tau* as physical MoSSe constants. [Methods 2.7-2.8, p.4; Discussion 4.5, p.13]
- Do not reuse the exact triangular switch angle outside the tested edge surrogate. [Results 3.5, p.9]
- Do not treat agreement between FEM and VFF as independent atomistic validation. [Results 3.4, pp.8-9]

### Gap the project can realistically fill next

The highest-value extension is not another denser rigid scan. It is a **mechanically distinct, higher-fidelity finite-flake validation** of the already-frozen mechanism: full/collective relaxation + nonuniform pulling + preparation control. That directly tests the remaining shared-model vulnerability. [Discussion 4.5, p.13; SI S11-S12, p.5]

### Citation drafts proportionate to evidence

**Introduction-style:**
> A reduced finite-contact analysis of a published Janus MoSSe stacking-energy landscape shows that prepared-state directional depinning can emerge from registry-space inversion asymmetry, while the magnitude and even sign remain conditioned on preparation and loading geometry. [Results 3.1-3.2, pp.6-7]

**Discussion-style:**
> Within a fixed-twist reduced model, same-spectrum symmetrization removes the global directional bias and exact inversion reverses it, supporting registry inversion asymmetry as a necessary conservative ingredient; whether the same mechanism survives fully relaxed finite-flake mechanics remains unresolved. [Results 3.1, p.6; Discussion 4.5, p.13]

### Material weakness / transfer risk

The temptation will be to treat the extensive internal audit as equivalent to external material validation. It is not. The next project decision should prioritize **model-level independence**, not more precision inside the current GSFE closure.

---

# A. Contradiction Map

| ID | 쟁점(반드시 질문형 한 줄) | 관점 A와 주장 | 관점 B와 주장 | 충돌 유형(①사실 ②해석 ③범위 ④방법론) | 원문이 이 충돌을 해소해주는가(✅줌·⚠️부분·❌안줌, 해당 시 근거 위치) | 해소 방법(내가 할 일 한 줄) | 우선순위 |
|---|---|---|---|---|---|---|---|
| CM-1 | 같은-spectrum 대조군으로 “원인”까지 말할 수 있는가? | Domain Expert: reduced model 안에서는 necessary conservative ingredient를 강하게 지지 | Skeptic: 공통 GSFE closure 바깥의 물리적 원인까지는 입증하지 못함 | ③범위 | ⚠️부분 — symmetrization/inversion은 모델 내에서 판정하지만 full-3D finite-flake 검증은 없음 [Results 3.1 p.6; Discussion 4.5 p.13] | 본문은 “within the reduced model/necessary conservative ingredient” 범위를 유지하고 higher-fidelity validation을 다음 실험으로 둔다 | ⚪ 낮음 |
| CM-2 | 현재 vector-locking map을 MoSSe의 재료 phase diagram으로 해석할 수 있는가? | Domain Expert: material-anchored nonlinear response로 의미 있음 | Statistics/Skeptic: gamma* sweep가 winding을 크게 바꾸므로 protocol-specific map임 | ③범위 | ✅줌 — 원문이 damping dependence와 protocol conditioning을 명시 [Discussion 4.3 p.13; SI S7 p.3] | 현재 범위 유지; venue-facing summary에서도 material-only phase diagram 표현 금지 | 🟡 중간 |
| CM-3 | 두 relaxation model의 일치가 독립 검증인가? | Method Reviewer: 서로 다른 constitutive/discretization artifact는 줄임 | Skeptic: same GSFE와 target elastic constants를 공유하므로 shared-input error를 배제하지 못함 | ④방법론 | ⚠️부분 — 원문이 shared inputs와 full-3D 부재를 명시 [Results 3.4 pp.8-9; Discussion 4.1 p.12] | “independent material validation”이 아니라 “two-representation in-plane robustness”로 유지 | ⚪ 낮음 |
| CM-4 | thermal current가 T*=0.70까지 nonzero라는 결론을 얼마나 일반화할 수 있는가? | Statistics: trajectory-level N과 stationarity/seed/timestep checks는 강함 | Skeptic: reduced temperature, one dynamical protocol, finite sampled T range라 physical thermal scale은 아님 | ③범위 | ✅줌 — 원문이 extinction temperature/Kelvin mapping을 명시적으로 부정 [Results 3.7 p.11; Discussion 4.5 p.13] | 현 finite-protocol wording 유지 | 🟡 중간 |
| CM-5 | 코드/데이터 재현성이 실제로 검증됐는가? | Method Reviewer: 상세 protocol과 release statement가 충분히 구체적 | Statistics Reviewer: 현재 reviewer source packet에는 executable release가 없어 end-to-end 재현을 확인하지 못함 | ④방법론 | ❌안줌 — manuscript+SI만으로 release 실행 상태는 판정 불가 [Methods 2.10 p.5; Data and Code Availability p.14] | 제출 직전 canonical release ZIP/commit, environment lock, seed manifest, one-command validation을 독립 실행 | 🔴 높음 |

**CM-5가 직접 영향을 주는 이유:** 이 연구의 강점이 수치 falsification과 auditability 자체이므로, 실행 가능한 release가 검증되지 않으면 핵심 신뢰도와 reviewer 대응 능력이 동시에 약해집니다.

### Research Gap 후보

- **CM-5:** 원고가 선언한 reproducibility release를 제3자가 실제로 같은 환경에서 실행했을 때 주요 표/그림/threshold가 재생성되는가?

---

# B. Claim Reliability Table

| ID | 주장(내 언어로 재진술) | 근거 위치(Fig·Table·섹션 번호, 없으면 "없음") | 근거 유형(직접 측정 / 통계 추론 / 모델·시뮬레이션 / 선행연구 인용 / 저자 해석 / 근거 없음) | 지지 관점 | 반박 관점 | 신뢰도(🟢High/🟡Medium/🔴Low) | 상태(Confirmed/Corrected/Demoted) | 내 검증 액션(한 문장, 없으면 "없음") |
|---|---|---|---|---|---|---|---|---|
| CR-1 | 준비된 ground basin은 theta=1.5 deg의 선택된 y축에서 큰 양의 directional threshold split을 보인다 | Results 3.2 p.7; Fig.2; SI Table S1 | 모델·시뮬레이션 | Domain, Method | Skeptic: basin/axis conditioned | 🟡Medium | Confirmed | fully relaxed finite-flake + second loading protocol에서 sign 재검증 |
| CR-2 | 같은 2H Fourier spectrum에서 inversion asymmetry를 제거하면 global directional bias가 사라지고 exact inversion은 sign을 뒤집는다 | Results 3.1 p.6; Fig.1; SI Table S2 | 모델·시뮬레이션 | Domain, Method, Skeptic | Skeptic: model closure 밖 causality는 미검증 | 🟡Medium | Confirmed | higher-fidelity model에서 동일 symmetry contract 반복 |
| CR-3 | compact rigid contacts는 tested range에서 theta sqrt(N) similarity를 매우 잘 따른다 | Results 3.3 p.8; Fig.3; SI Table S4 | 모델·시뮬레이션 | Domain, Method | Skeptic: arbitrary/reconstructed/deformable edges로 일반화 불가 | 🟡Medium | Confirmed | irregular/reconstructed boundary family를 사전정의해 out-of-family test |
| CR-4 | fixed-twist re-preparation을 하면 triangular boundary의 registry-energy crossing이 directional sign을 바꿀 수 있다 | Results 3.5 p.9; Fig.4; SI Tables S5-S6 | 모델·시뮬레이션 | Domain, Method | Skeptic: kinetic switching/hysteresis 아님 | 🟡Medium | Confirmed | barrier + continuous twist-ramp/hysteresis 계산 |
| CR-5 | 선언된 m*=1, gamma*=4 protocol의 91 sampled points 모두 measured cycle마다 동일 integer winding을 반복한다 | Results 3.6 pp.9-10; Fig.5; SI S7 | 모델·시뮬레이션 | Domain, Method | Statistics/Skeptic: continuous space/unique attractor 아님 | 🟡Medium | Confirmed | adaptive tongue-boundary mapping + multistability search |
| CR-6 | 대표 plateau들은 relative-periodic closure와 cross-solver Floquet rho_F<1로 locally attracting이다 | Results 3.6 p.10; Fig.5d; SI Tables S7-S7b | 모델·시뮬레이션 | Domain, Method | Skeptic: representative only, global uniqueness 아님 | 🟡Medium | Confirmed | additional boundary/near-transition plateau Floquet checks |
| CR-7 | stationarity-audited reduced thermal protocol에서 weak mean vector drift는 sampled T*=0.70까지 0과 구별된다 | Results 3.7 pp.10-11; Fig.6; Table 3; SI Tables S8a-S8b | 통계 추론 / 모델·시뮬레이션 | Statistics, Method | Skeptic: physical Kelvin boundary 아님 | 🟡Medium | Confirmed | predeclared precision target + one additional hotter T band only if claim expansion is desired |
| CR-8 | linear FEM과 nonlinear bond-angle relaxation 모두 directional split sign을 보존한다 | Results 3.4 pp.8-9; Table 3; SI Tables S9-S10 | 모델·시뮬레이션 | Domain, Method | Skeptic: shared GSFE/constants, not atomistic-independent | 🟡Medium | Demoted | Janus-specific full-3D finite-flake potential로 독립 검증 |

### 인용 금지 목록

이번 source packet의 핵심 8개 claim 중 `🔴 Low`로 분류된 항목은 없습니다. 다만 **다음 표현은 established fact로 확장 인용하면 안 됩니다**: “experimental Janus polarity law,” “universal loading-axis-independent diode,” “material-only nonlinear phase diagram,” “thermal critical temperature,” “fully atomistic validation.” 원문 자체가 이들을 limitation으로 배제합니다. [Discussion 4.3-4.5, p.13]

---

# C. 빠진 여섯 번째 관점 — Experimental Nanotribology / Device Realization Reviewer

기존 다섯 관점은 모델 타당성, 수치 방법, 통계, 반증, 연구 연결을 충분히 보지만, **실험적으로 어떤 물체를 어떻게 준비하고 구동하고 읽을 것인가**를 상대적으로 덜 묻습니다.

이 관점이 묻는 핵심은 다음입니다.

- ground/metastable basin을 실제로 선택/검증할 수 있는가?
- twist를 고정하면서 lateral force axis를 정밀하게 정의할 수 있는가?
- uniform COM/body-force 모델과 실제 AFM/mesa edge drive의 차이가 sign을 바꾸는가?
- reduced time/temperature/damping을 어떤 측정 가능량으로 calibration할 것인가?

**결정을 바꿀 수 있는 위험:** 모델에서 가장 큰 static split이 실험적으로 접근 가능한 preparation/loading geometry에서 재현되지 않으면, 논문의 현재 mechanism paper로서의 가치는 남더라도 device implication은 크게 약해집니다. [Results 3.2 p.7; Discussion 4.5 p.13]

**필요한 evidence:** 최소한 한 개의 realistic driving geometry에서의 higher-fidelity simulation, basin-identification protocol, force/velocity scale calibration, 그리고 예상 observable (lateral-force loop, switching displacement, or winding signature)의 실험 설계.

---

# D. Research Gap

### 명시적 gap 3개

1. **Janus-specific full-3D finite-flake validation 부재.** collective corrugation/buckling, reconstructed edges, nonlocal edge energetics를 포함하는 potential이 필요하다고 명시한다. [Discussion 4.5, p.13; SI S11-S12, p.5]
2. **물리적 dissipation/inertia/time/temperature calibration 부재.** reduced gamma*, mass, T*, tau*를 Kelvin/physical frequency로 바꿀 수 없다고 명시한다. [Discussion 4.5, p.13]
3. **kinetic boundary switching/hysteresis 부재.** triangular registry crossing은 fixed-twist equilibrium re-preparation 결과이며 barrier/twist sweep/hysteresis는 계산하지 않았다. [Results 3.5, p.9; SI S6, pp.2-3]

### 숨은 gap 2개

1. **[추론] Reproducibility release의 제3자 실행 검증이 paper-level evidence chain에 아직 결합되지 않았다.** 원고는 package 존재를 선언하지만 reviewer packet만으로 canonical commands/environment/seeds가 실제 실행되는지 판정할 수 없다. [Methods 2.10, p.5; Data and Code Availability, p.14]
2. **[추론] Preparation protocol의 experimental identifiability가 아직 정의되지 않았다.** ground와 metastable basin이 opposite sign을 가지므로, 실험에서 basin을 식별하지 못하면 ensemble-averaged response가 headline sign과 다를 수 있다. [Results 3.2, p.7; SI Table S1, p.1]

---

# E. 다음 액션 3개

1. **Canonical reproducibility release 독립 재실행**
   - **입력:** 최종 code/data bundle, environment/lockfile, seed manifest, canonical run commands.
   - **작업:** clean environment에서 최소 Table S1, Fig.5 canonical orbit, Table S8b/Fig.6, FEM/VFF headline rows를 one-command validation으로 재생성한다.
   - **판정 기준:** manuscript values와 predeclared tolerance 내 일치; 실패 시 submission blocker.
   - **해결 대상:** CM-5, hidden gap 1.

2. **Preparation-identifiability pilot 설계/시뮬레이션**
   - **입력:** theta=1.5 deg ground/metastable minima, realistic weak spring or finite-rate relaxation protocol.
   - **작업:** 서로 다른 initialization/annealing/load-history에서 최종 basin occupancy와 signed Delta F_c를 계산한다.
   - **판정 기준:** ground-state preparation이 높은 확률로 재현되는지, 아니면 mixed-sign ensemble이 필요한지.
   - **해결 대상:** CR-1, hidden gap 2.

3. **Higher-fidelity mechanical falsification preflight**
   - **입력:** SI S11의 GSFE acceptance contract, 후보 Janus-specific MLIP/DFT finite-flake pathway, 두 loading protocols(body-force vs spring/edge drive).
   - **작업:** 먼저 후보 potential이 GSFE contract를 통과하는지 검사하고, 통과한 경우 N~127-scale에서 static sign만 smoke-test한다.
   - **판정 기준:** ground-state sign과 inversion relation이 유지되면 full campaign 진행; 실패하면 material-mechanism claim을 further demote.
   - **해결 대상:** CR-2, CR-8, explicit gap 1.

---

## Overall reviewer synthesis

The paper is **internally much stronger than a typical reduced-model mechanics manuscript** because it exposes and tests preparation, gauge, boundary, dynamical, thermal, and in-plane-model failure modes rather than reporting only a favorable curve. The five-reviewer audit finds **no new internal numerical contradiction that invalidates the current scoped claims**. The dominant remaining vulnerability is **external model independence and executable reproducibility**, not another missing decimal place in the current GSFE-based model.

For the present claim scope, no scientific Blocker is identified from manuscript/SI alone. Before venue handoff, the most consequential practical check is an independent clean-environment replay of the canonical release. Higher-fidelity material validation remains the central scientific extension, but the manuscript already labels it as future validation rather than pretending it is complete.
