# N24 Five Reviewer Paper Audit — Architecture-Aligned Janus MoSSe Manuscript

## 0. Source & Context Check

- Source packet: N23 architecture-aligned scientific prose; current verified Methods, Data Availability, references, and reproducibility records; N21 Claim–Evidence Matrix/argument architecture; N22 seven-figure contracts and QA.
- Title: Unguided Full-2D Mechanical Rectification and Vector Mode Locking in Finite Janus MoSSe Contacts.
- Venue target: ACS Nano Article.
- Paper type: computational/physical-model study.
- External literature check in this audit: not independently repeated. Novelty statements below distinguish internal positioning from externally verified novelty.
- User research context: this manuscript itself is the active research project; the practical goal is a scientifically bounded, reproducible submission rather than expansion of the claim set.

## 1. Domain Expert

[원문 확인] The paper's central physical claim is not that Janus polarity automatically creates a friction diode. It is that the published 2H MoSSe lateral GSFE contains non-removable registry-space inversion asymmetry and that, for a declared zero-force preparation of a finite unguided contact, this asymmetric landscape supports direction-split depinning and protocol-conditioned vector transport. Same-spectrum symmetrization removes the global directional response, whereas exact mathematical inversion reverses it. [Results 1–3; Figs 1–3]

[원문 확인] The manuscript explicitly limits the static threshold to a prepared state and loading axis, and distinguishes compact-contact similarity from boundary-induced registry-family switching. [Results 2,4,5; Figs 2,4,5]

[원문 확인] The 91-point amplitude-period map contains both pinned and transporting integer winding states, and representative transporting plateaus rather than the whole map receive Floquet validation. [Results 6; Fig 6; Methods: Zero-mean two-dimensional rocking]

[원문 확인] Thermal results separate exact winding identity from stationary directed current; the latter remains statistically resolved through the largest sampled T*=0.70. [Results 7; Fig 7; Methods: Thermal dynamics]

Strength: the paper's strongest conceptual feature is the sequence asymmetric registry input -> prepared-state depinning -> same-spectrum intervention -> robustness -> dynamics.

Weakness: the mechanistic interpretation remains a reduced-model mechanism. The paper does not validate collective out-of-plane corrugation, atomistic edge reconstruction, or a physical polarity-reversed GSFE. [Methods: In-plane relaxation hierarchy; Discussion: Model and physical-mapping boundaries]

Novelty: [확인 못 함] The exact combination claim has not been independently reverse-searched in this audit. The manuscript correctly avoids a first-ever claim, so this is a positioning uncertainty rather than evidence against the numerical result.

## 2. Method Reviewer

Independent reconstruction:
- Independent variables / controls: twist angle, loading sign, compact size/shape, symmetry intervention, triangular edge orientation/outer-site weight, rocking amplitude/period/damping, reduced temperature, in-plane stiffness/representation. [Methods]
- Primary dependent quantities: branch-followed depinning thresholds, directional split, registry-family energy, winding pair, Floquet spectral radius/closure, stationary mean lattice current, cycle-sign probability, target-winding probability. [Methods; Results]
- Computational unit: finite N-site contact for deterministic calculations; independent stochastic trajectory for thermal inference. [Methods]
- Key controls: 3R asymmetry controls; matched inversion-even 2H surface; exact spatial inversion; metastable branch tracking; compact hex/disk families; FEM stiffness sweep and nonlinear VFF; edge-weight sensitivity; cross-solver Floquet checks; thermal second-seed and timestep checks. [Methods; Figs 1–7]

[원문 확인] The branch-followed threshold definition is appropriate for a state-conditioned claim because it follows the same zero-force minimum under opposite loading instead of switching to a global envelope after the fact. [Methods: Unguided full-2D depinning]

[원문 확인] The higher-order degeneracy near theta≈2.9734 deg is not forced into generic fold terminology. [Methods: stability boundaries; Results 2]

[추론] The same-spectrum interventions provide strong mechanism discrimination within this model class. They still do not identify a laboratory polarization-switching operation.

Weakness 1: uniform center-of-mass/body-force loading and fixed twist omit spring pulling, localized loading, torque, rotational relaxation, and preparation kinetics. [Methods: depinning; Discussion 4]

Weakness 2: outer-site weighting is explicitly a sensitivity model rather than a microscopic edge Hamiltonian. The existence of boundary-state competition is better supported than any exact switching angle. [Methods: Finite-size and boundary protocols; Results 5]

Weakness 3: the FEM/VFF pair tests in-plane compliance only. The phrase "rule out the strongest version of a rigid-contact artifact" is rhetorically stronger than needed; "the directional sign survives two tested in-plane representations" is more directly tied to the evidence. [Results 4; Methods: In-plane relaxation hierarchy]

## 3. Statistics & Reproducibility Reviewer

[원문 확인] Thermal inference uses the trajectory as the statistical unit rather than treating cycles as independent replicates. The main series uses N=500 trajectories per temperature after 60 burn and 100 measured cycles, while T*=0.50–0.70 is independently replicated with a second N=500 ensemble and pooled to N=1000. [Methods: Thermal dynamics; Results 7]

[원문 확인] The high-temperature conclusion is supported both component-wise by trajectory bootstrap intervals and jointly by Hotelling inference. At T*=0.70, the reported pooled mean is approximately (0.036998,-0.076448), and the reported component bootstrap intervals exclude zero. [Results 7; Fig 7]

[원문 확인] Numerical robustness includes second-seed replication, initialization-memory checks, block-drift/stationarity checks, and targeted BAOAB timestep comparisons. [Methods: Thermal dynamics; Reproducibility and numerical checks]

[원문 확인] Deterministic winding classifications are followed by stricter cycle-resolved checks, and representative plateaus receive cross-solver Floquet, closure, timestep, continuation, and basin checks. [Methods: Zero-mean rocking]

Weakness 1: no prospective power or precision calculation for N=500/1000 is stated. This does not invalidate the narrow confidence-interval claim, but the trajectory counts are empirically chosen rather than justified from a target precision. [Methods: Thermal dynamics]

Weakness 2: several thermal observables and temperatures are inspected. The main claim can be anchored to the endpoint T*=0.70 and the joint-vector test, but the manuscript does not state a familywise multiple-testing plan. Avoid turning the collection of per-temperature diagnostics into a global significance claim. [Methods: Thermal dynamics; Results 7]

Weakness 3: Data Availability says the materials are retained with the submission package but no archival DOI is yet claimed. A clean package exists, but long-term third-party reproducibility is not fully secured until immutable deposition. [Data Availability Statement]

## 4. Skeptic

Alternative hypothesis A: the observed sign is primarily a preparation/basin-selection effect rather than an intrinsic property of the material landscape. [Results 2,5]
The manuscript partly addresses this by declaring preparation, tracking both stable families, and showing that different families can carry opposite splits. This narrows the claim to prepared-state rectification rather than refuting preparation dependence. [Results 2,5]

Alternative hypothesis B: the sign arises from a rigid finite-flake approximation and would disappear after internal relaxation. [Results 4]
FEM and nonlinear VFF weaken this alternative for in-plane relaxation because both preserve the sign while shifting absolute thresholds. They do not falsify an out-of-plane/atomistic-edge alternative. [Results 4; Methods: In-plane relaxation hierarchy]

Alternative hypothesis C: the symmetry controls are mathematical identities that do not prove a realizable material switching mechanism.
The manuscript agrees with this limitation. Exact inversion is used as mechanism discrimination, not as evidence that physical Janus polarization reversal produces the same surface. [Results 3; Discussion 4]

Potential overclaim: no explicit claim that physical polarity reversal has been demonstrated was found. The main wording risk is subtler: "isolate ... as the directional source" can be read too causally outside the reduced-model scope. The body text's "support attribution ... within the declared reduced model" is the safer formulation. [Results 3 heading/body]

Decisive falsification experiment: calculate paired, polarity-resolved first-principles lateral GSFE surfaces, or use a validated Janus-specific high-fidelity model that reproduces the current GSFE harmonics, then run the same prepared-state continuation without imposing mathematical inversion. If the physical polarity-switched surface fails to reverse or strongly alter the directional response in the predicted way, the material-level polarity interpretation is falsified; the current reduced-model symmetry result can still survive.

Weakness: no such polarity-resolved material-level falsification is currently available. [Discussion 4]

## 5. My Research Connector

Because this is the user's own active manuscript, the relevant question is what transfers immediately into submission and what should remain future work.

Immediately transferable: N21 argument order; N22 figure sequence; branch-followed preparation contract; same-spectrum controls; compact-versus-boundary geometry split; trajectory-level thermal inference; explicit C22–C25 limitation language.

Requires adaptation / should not be promoted: exact inversion as physical polarity switching; reduced m*, gamma*, tau*, or T* as laboratory quantities; outer-site weights as microscopic edge parameters; VFF as full atomistic validation.

Useful gap for a later project: paired polarity-resolved first-principles GSFE or an independently validated Janus-specific interatomic model would turn the current mathematical inversion test into a material-level test.

Introduction citation draft: "Prior work establishes strong stacking- and moiré-dependent energetics in Janus MoSSe, motivating a direct test of whether the published lateral registry landscape can support prepared-state directional mechanics rather than inferring rectification from the Janus label alone." [Introduction; Methods: Published MoSSe GSFE]

Discussion citation draft: "Within the present reduced finite-contact model, same-spectrum symmetrization removes the directional response and exact spatial inversion reverses it, supporting registry inversion asymmetry as the model-level source while leaving physical polarity reversal unestablished." [Results 3; Fig 3]

Weakness / transfer risk: final Introduction positioning still depends on an external closest-prior-art reverse search if any stronger novelty language is considered.

# A. Contradiction Map

| ID | 쟁점(반드시 질문형 한 줄) | 관점 A와 주장 | 관점 B와 주장 | 충돌 유형(①사실 ②해석 ③범위 ④방법론) | 원문이 이 충돌을 해소해주는가(✅줌·⚠️부분·❌안줌, 해당 시 근거 위치) | 해소 방법(내가 할 일 한 줄) | 우선순위 |
|---|---|---|---|---|---|---|---|
| X1 | 대칭 제어가 "원인"을 어디까지 식별하는가? | Domain: reduced model 내부에서는 강한 mechanism discrimination | Skeptic: 실험적 polarity operation의 인과성은 식별하지 못함 | ③범위 | ⚠️부분 — Results 3와 Discussion 4가 물리적 polarity mapping을 명시적으로 제외 | heading/body에서 model-level source / supports attribution within the reduced model로 통일 | ⚪ 낮음 |
| X2 | FEM/VFF가 rigid-contact artifact를 충분히 배제하는가? | Method: 두 in-plane representation에서 sign이 유지됨 | Skeptic: out-of-plane/edge reconstruction 대안은 남음 | ③범위 | ⚠️부분 — Methods: In-plane relaxation hierarchy에서 in-plane only를 명시 | rule-out wording을 tested-scope wording으로 축소 | ⚪ 낮음 |
| X3 | T*=0.70에서 transport가 살아 있다고 말할 수 있는가? | Domain: stationary mean vector는 통계적으로 resolved | Statistics: exact winding/개별 sign effect와 joint mean을 분리해야 함 | ②해석 | ✅줌 — Results 7/Fig 7이 exact winding, P(v<0), joint mean을 분리 | "mean current resolved; exact mode identity mixed"로 유지 | ⚪ 낮음 |
| X4 | 현재 패키지만으로 장기 재현성이 충분한가? | Method: 상세 protocol과 clean-rerun evidence가 있음 | Reproducibility: archival DOI가 없어 immutable third-party access는 미완료 | ④방법론 | ⚠️부분 — Reproducibility/Data Availability가 package 존재와 DOI 미완료를 모두 밝힘 | 제출 전 또는 출판 과정에서 immutable repository deposition | ⚪ 낮음 |
| X5 | 조합형 contribution의 novelty를 확정할 수 있는가? | Domain/Connector: 현재 조합은 차별화되어 보이나 외부 재검증 안 됨 | Skeptic: 내부 evidence로 novelty는 증명 불가 | ③범위 | ❌안줌 — manuscript 자체로 closest-prior-art exhaustiveness를 판정할 수 없음 | exact-combination + component + adjacent-term reverse search를 최종 1회 실행 | 🔴 높음 |

X5가 이 연구에 직접 영향을 주는 이유: Introduction/cover letter에서 novelty 범위를 한 단계라도 넓히려면 closest-prior-art 검증이 필요하고, 검증 없이 강한 novelty 문구를 쓰면 submission-stage claim boundary를 깨뜨린다.

Research Gap 후보:
- X5: Janus MoSSe lateral-registry asymmetry + unguided prepared-state depinning + same-spectrum symmetry controls + vector mode locking의 정확한 조합에 대해 closest prior art가 어디까지 존재하는가?

# B. Claim Reliability Table

| ID | 주장(내 언어로 재진술) | 근거 위치 | 근거 유형 | 지지 관점 | 반박 관점 | 신뢰도 | 상태 | 내 검증 액션 |
|---|---|---|---|---|---|---|---|---|
| R1 | published 2H GSFE의 lateral inversion asymmetry는 registry-origin 이동으로 제거되지 않는다 | Results 1; Fig 1; Methods: Coordinate-invariant registry asymmetry | 모델·시뮬레이션 | Domain, Method | Skeptic: material polarity와는 별개 | 🟡Medium | Confirmed | 없음 |
| R2 | 선언된 ground-state preparation은 ±y에서 서로 다른 unguided depinning threshold를 가진다 | Results 2; Fig 2; Methods: Unguided full-2D depinning | 모델·시뮬레이션 | Domain, Method | Skeptic: preparation-conditioned | 🟡Medium | Confirmed | 없음 |
| R3 | same-spectrum symmetrization/inversion은 reduced model에서 directional response를 제거/반전한다 | Results 3; Fig 3 | 모델·시뮬레이션 | Domain, Method | Skeptic: physical polarity causality 아님 | 🟡Medium | Demoted (within-model scope) | causal wording을 reduced-model attribution으로 제한 |
| R4 | compact-size/shape 및 두 in-plane relaxation representation에서 directional sign이 유지된다 | Results 4; Fig 4; Methods: Finite-size; In-plane relaxation | 모델·시뮬레이션 | Domain, Method | Skeptic: full 3D/edge는 미검증 | 🟡Medium | Demoted (tested-scope robustness) | arbitrary-shape/full-atomistic wording 금지 |
| R5 | triangular boundary state selection은 opposite-bias registry family 사이의 prepared-state sign reversal을 만들 수 있다 | Results 5; Fig 5 | 모델·시뮬레이션 | Domain, Method | Method: exact angle edge-model sensitive | 🟡Medium | Confirmed | 없음 |
| R6 | zero-mean rocking sampled grid에는 pinned와 transporting integer winding states가 있고 representative transport orbit은 attracting이다 | Results 6; Fig 6; Methods: Rocking/Floquet | 모델·시뮬레이션 | Domain, Method | Skeptic: protocol-specific/sample map only | 🟡Medium | Confirmed | 없음 |
| R7 | exact winding이 강하게 섞인 뒤에도 stationary mean vector는 T*=0.70까지 통계적으로 nonzero이다 | Results 7; Fig 7; Methods: Thermal dynamics | 통계 추론 + 시뮬레이션 | Domain, Statistics | Statistics: n precision justification/multiplicity boundary | 🟡Medium | Confirmed | CI precision/multiplicity sensitivity를 supplemental audit로 고정 |
| R8 | 이 정확한 조합형 contribution은 기존 문헌에서 새로운 위치를 차지한다 | Introduction positioning; 직접 외부 검증 없음 | 저자 해석 / 선행연구 인용 | Connector | Domain, Skeptic: reverse search pending | 🔴Low | Demoted | final closest-prior-art reverse search |

인용 금지 목록:
- R8 — 외부 closest-prior-art 검증이 완료되지 않았으므로 first, unprecedented, 또는 확정적 novelty 사실로 인용 금지. 현재 manuscript는 강한 first claim을 피하고 있으며, 그 상태를 유지해야 한다. [Introduction contribution paragraph]

# C. 빠진 여섯 번째 관점 — High-fidelity model validation reviewer

기존 다섯 관점은 reduced-model 내부 검증과 문헌/통계 범위를 잘 다루지만 모델 계층 간 transfer validity를 독립된 주제로 충분히 다루지 않는다. 이 관점은 현재 GSFE 기반 sitewise model에서 살아남은 sign과 state-selection mechanism이 collective corrugation, realistic edge chemistry, and polarity-resolved atomic relaxation이 들어간 상위 모델에서도 유지되는가를 묻는다.

이 관점이 바꿀 결정은 실험 예측의 강도다. 현재 결과는 reduced-model mechanism으로 제출 가능하지만, device-level 또는 physical-polarity law로 확장하려면 paired polarity-resolved GSFE나 validated Janus-specific interatomic model이 필요하다.

필요 evidence: current three-shell GSFE harmonics를 정량 재현하는 independent high-fidelity model + finite-contact relaxation + matched preparation protocol.

# D. Research Gap

명시적 gap 3개:
1. Full 3D atomistic finite-contact validation 부재. Collective buckling/corrugation, atomistic edge reconstruction, defects, and nonlocal edge energetics는 현재 hierarchy에 포함되지 않는다. [Discussion: Model and physical-mapping boundaries; Methods: In-plane relaxation hierarchy]
2. Physical Janus polarity reversal mapping 부재. Exact spatial inversion은 mathematical control이며 paired polarity-resolved first-principles GSFE가 없다. [Results 3; Discussion: Model and physical-mapping boundaries]
3. Experimental time/temperature/force calibration 부재. Reduced m*, gamma*, tau*, T*를 Hz/K/device force로 직접 변환할 calibration이 없다. [Methods: Rocking/Thermal dynamics; Discussion: Model and physical-mapping boundaries]

숨은 gap 2개:
1. [추론] Exact-combination novelty의 final reverse-search가 아직 고정되지 않았다. Manuscript는 first claim을 피하지만, contribution positioning을 확정하려면 closest-prior-art search가 필요하다. [Introduction contribution paragraph; N21 novelty boundary]
2. [추론] Thermal ensemble size에 대한 prospective precision rationale가 없다. N=500/1000에서 현재 CI는 계산되어 있지만, 목표 CI width 또는 power를 먼저 정해 trajectory count를 결정했다는 근거는 없다. [Methods: Thermal dynamics; Results 7]

# E. 다음 액션 3개

1. Literature search: exact-combination, component, adjacent-term, and closest-prior-art reverse search를 Consensus/Exa/Scholar 경로로 수행한다. 입력은 N21의 N2 positioning 문장과 현재 refs 1–26; 출력은 strongest closest prior art / overlap / remaining contribution / forbidden novelty wording 표이며 R8/N2를 VERIFIED 또는 계속 UNCERTAIN으로 결정한다.
2. Reanalysis: 기존 T*=0.50–0.70 trajectory-level 데이터로 N 대비 bootstrap CI-width curve와, 필요하면 high-T endpoint family에 대한 multiplicity-sensitive 보조 분석을 수행한다. 출력은 현재 N=500/1000이 mean-vector conclusion에 주는 precision과 R7 wording 유지/축소 결정이다.
3. Protocol preregistration/pilot design: paired polarity-resolved GSFE 또는 validated high-fidelity Janus model을 위한 최소 falsification protocol을 문서화한다. 입력은 current GSFE harmonics, C4 symmetry contracts, current preparation/loading protocol; 출력은 pass/fail criteria가 명시된 후속-validation plan이며 C24의 future-work boundary를 고정한다.

## Audit verdict

No scientific Blocker identified for the current bounded reduced-model manuscript.

Targeted revision is required for two Major wording/precision issues:
- M1: replace "rule out the strongest version of a rigid-contact artifact" with tested-scope wording.
- M2: replace the thermal sentence implying eventual loss of statistical resolution with wording that stops at the observed boundary T*=0.70.

One external-literature handoff remains:
- L1: final closest-prior-art reverse search before any stronger novelty positioning.
