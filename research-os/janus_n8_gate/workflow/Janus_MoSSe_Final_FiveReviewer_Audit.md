# Five Reviewer Paper Audit — Workflow-Validated Janus MoSSe Manuscript

**Audited manuscript:** *Unguided Full-2D Mechanical Rectification and Vector Mode Locking in Finite Janus MoSSe Contacts*  
**Subtitle:** *A DFT-anchored finite-contact model with branch-resolved, statistical, and elastic robustness tests*

## 0. Evidence scope

[원문 확인] The audited manuscript now separates the imported corrected 2H MoSSe GSFE, prepared-state static depinning, matched symmetry controls, finite-size/boundary geometry, deterministic vector locking, thermal inference, and two in-plane relaxation representations. The companion SI records the branch audit, symmetry contracts, finite-size/shape tests, boundary sensitivity, Floquet conditioning, trajectory-cluster bootstrap, nonlinear valence-force cross-check, and the Tier-2 atomistic-potential no-go prescreen. [Methods 2.1–2.10; Results 3.1–3.7; SI S2–S11]

[외부 검증] The literature positioning was checked through Consensus/Exa and then Scite. The corrected Angeli GSFE source and erratum are retained together; prior friction-diode, structural-lubricity, elasticity/relaxation, stochastic-friction, and ratchet literature are explicitly acknowledged. The generic existence of a 2D friction diode is therefore not treated as the novelty. [Introduction; Refs. 1–21]

---

# 1. Domain Expert

### Core claim in field language

[원문 확인] The paper establishes a **DFT-anchored reduced finite-contact bifurcation model** in which an inversion-asymmetric 2H MoSSe registry potential produces unequal prepared-state loss-of-metastability forces under opposite longitudinal loading. At `N=127`, `theta=1.5 deg`, the rigid ground-state branch loses stability at `F_c,+*=3.071135` and `F_c,-*=1.258672`, giving `rho=0.418601`. The same branch remains lower in zero-force energy and longer-lived than the competing metastable branch over the sampled `0–3 deg` interval. [Results 3.2; Fig. 2; Table 3; SI S2]

[원문 확인] The causal attribution is strengthened by **same-spectrum controls**: the matched symmetrized landscape has a direction-degenerate global envelope and zero deterministic current, while exact spatial inversion swaps the two thresholds and reverses the lattice current to numerical precision. [Results 3.1; Fig. 1; Table 2; SI S3]

### Position in the literature

[외부 검증] Structural lubricity, finite-contact scaling, edge effects, and elastic relaxation are established subjects; asymmetric sliding landscapes have also already been used to obtain friction-diode behavior. Directed transport and phase locking under unbiased periodic forcing are established ratchet phenomena. The defensible novelty is therefore the **combination** of the corrected Janus MoSSe GSFE with unrestricted full-2D prepared-state depinning, same-spectrum symmetry falsification, compact-contact similarity, boundary registry-state switching, and lattice-vector mode locking. [Introduction; Refs. 1–8, 12–20]

### Physical plausibility

The mechanism is physically coherent at the reduced-model level. A finite contact averages registry forces through a structure factor; the corrected GSFE retains non-removable lateral inversion asymmetry; opposite loading directions therefore need not encounter equivalent prepared-state stability boundaries. The exact-inversion and symmetrization contracts are particularly strong because they operate on the same Fourier spectrum rather than comparing chemically different stackings. [Methods 2.2–2.4; Results 3.1–3.2]

The new relaxation hierarchy also improves plausibility. Absolute thresholds move when in-plane compliance is allowed, but the normalized directional split survives both a linear free-edge membrane and a nonlinear bond-angle discretization calibrated to the same elastic constants. [Results 3.4; SI S9–S10]

### Material weakness that can change interpretation

[원문 확인] The finite interface is still a local-registry construction built from an aligned-bilayer GSFE. The source DFT already relaxes interlayer separation at each lateral registry, but the manuscript still lacks collective finite-flake out-of-plane corrugation, atomistic edge reconstruction/chemistry, defects, and nonlocal edge energetics. [Methods 2.1, 2.6; Discussion 4.5]

This is not a cosmetic limitation: the paper itself shows that in-plane compliance can shift absolute thresholds by ~16–19% at `theta=3 deg`, and boundary-switch angles move by several tenths of a degree when outer-site weighting changes. [Results 3.4–3.5; SI S6, S9]

**Domain Expert decision:** the reduced-model mechanism is physically credible and substantially better controlled than earlier versions, but a real-material “fully relaxed MoSSe nanofriction diode” interpretation remains premature.

---

# 2. Method Reviewer

### Reconstructed computational design

- **Primary material input:** corrected three-shell 2H Se-S-Se-S MoSSe GSFE. [Methods 2.1]
- **Computational unit:** a finite contact, primarily `N=127`, with COM registry free in two dimensions. [Methods 2.2]
- **Primary static outcome:** prepared-ground-state branch-followed `F_c,+`, `F_c,-`, and `rho`. [Methods 2.4]
- **Primary static controls:** matched same-2H symmetrization, exact inversion, competing zero-force minima, symmetric 3R control. [Methods 2.3; Results 3.1]
- **Geometry interventions:** contact size/shape and triangular cut orientation. [Methods 2.5]
- **Model-form interventions:** linear membrane and nonlinear discrete in-plane relaxation. [Methods 2.6]
- **Dynamic intervention:** zero-mean sinusoidal longitudinal forcing over an amplitude-period grid. [Methods 2.7]
- **Thermal outcome:** trajectory-level mean vector current, continuous displacement, cycle-sign probability, and target winding assignment. [Methods 2.8]

### What is now methodologically strong

[원문 확인] The former “last stable minimum anywhere” ambiguity has been resolved by preparing the lowest-energy zero-force minimum and following that branch separately in both loading directions. The competing family is explicitly continued rather than silently ignored. [Methods 2.4; Results 3.2; SI S2]

[원문 확인] The same-spectrum symmetry controls are well designed. They test the mechanism without changing chemistry or first-shell amplitude structure unnecessarily. Exact inversion provides a strong algebraic/numerical contract: threshold swap and current reversal. [Methods 2.3; Results 3.1]

[원문 확인] The deterministic mode-locking claim is no longer based on a single trajectory: the sampled map, time-step refinement, basin perturbations, continuation, one-period closure, and cross-integrator Floquet calculation all support the representative orbit. [Methods 2.7; Results 3.6; SI S7]

### Missing control / remaining method risk

The largest missing control remains the one the manuscript now explicitly recognizes: **a Janus-specific full-3D atomistic potential must first reproduce the corrected 2H Se-S-Se-S GSFE before being used to relax the finite contact**. [Discussion 4.5; SI S11]

The Tier-2 public SW+KC prescreen was handled correctly as a no-go: it preserves the dominant asymmetry and rectification sign but overestimates the second and third GSFE harmonics, so it is not used as quantitative atomistic validation. [SI S11]

A second residual limitation is that the complete bifurcation topology is not obtained through global two-parameter pseudo-arclength continuation in `(theta,F)`. The sampled branch audit is strong for the headline range, but the isolated higher-order degeneracy near `theta≈2.9734 deg` still deserves a dedicated normal-form/unfolding analysis. [Results 3.2; Discussion 4.5]

**Method Reviewer decision:** computational design is now internally coherent and reproducible within the stated model hierarchy. Full 3D material validation remains the main next methodological layer.

---

# 3. Statistics & Reproducibility Reviewer

### Unit of analysis and uncertainty

[원문 확인] The thermal analysis uses `1000` independent trajectories per sampled temperature; each trajectory has 10 burn cycles and 10 measured cycles. Bootstrap resampling occurs at the **trajectory** level, so cycles within one trajectory are not treated as independent replicates. [Methods 2.8; Results 3.7; SI S8]

[원문 확인] The manuscript reports **pointwise** confidence intervals rather than implying a simultaneous familywise band across all temperatures. This distinction is now stated explicitly. [Discussion 4.3; SI S8]

### Independent statistical reanalysis

The stored raw trajectory summaries were independently reprocessed with a separate 10,000-replicate trajectory-cluster bootstrap. The independently generated interval endpoints differed from the archived canonical endpoints by at most ~`0.00282`, consistent with Monte-Carlo bootstrap variation. A 100,000-resample boundary check gave:

- `T*=0.50`: `P(Delta y<0)` CI `[0.5079, 0.5273]`
- `T*=0.55`: `[0.5001, 0.5197]` — marginal
- `T*=0.60`: `[0.4964, 0.5153]` — unresolved
- `T*=0.65`: `[0.4971, 0.5163]` — unresolved

The mean lattice-v current remains pointwise resolved through `T*=0.60`, and its CI first includes zero at the sampled point `T*=0.65`. [Results 3.7; SI S8; independent Data/Python audit]

### Deterministic numerical reproducibility

[원문 확인] The clean numerical engine reports finite-difference gradient and Hessian errors of `1.64e-9` and `1.71e-6`. The matched symmetry contracts close at roughly `1e-10–1e-18`, and DOP853/Radau agree on the representative Floquet spectral radius within ~`2.8e-6` relative. [Methods 2.10; Results 3.1, 3.6; SI S3, S7]

### Statistical/reproducibility weakness

The thermal scan does **not** define a formally estimated transition temperature with simultaneous uncertainty. Statements such as “resolved through `T*=0.60` but not at `0.65`” are correct for the sampled pointwise intervals; they should not be promoted into a sharp universal `T_c`. Also, the current package still lacks an external archival DOI. [Discussion 4.3; Data and code availability]

**Statistics & Reproducibility decision:** no remaining pseudoreplication problem is evident in the reported thermal inference. The principal remaining statistical scope issue is the difference between pointwise sampled inference and a continuous/simultaneous operating boundary.

---

# 4. Skeptic

Assume the headline interpretation is wrong.

### Alternative hypothesis 1 — rectification is a local-GSFE artifact

The same finite-contact asymmetry could disappear after collective three-dimensional relaxation because nonlocal elastic reconstruction can reshape the effective PES. The two in-plane models reduce this concern but cannot eliminate it because both reuse the same local GSFE and target elastic constants. [Results 3.4; Discussion 4.5]

**Decisive falsification:** use a Janus-specific MLIP only after it passes the predeclared corrected-GSFE contract, then relax all atomic `x,y,z` coordinates of the finite flake at constrained COM registry and recompute `F_c,+/-`. A sign collapse or near-zero `rho` would materially weaken the proposed mechanism.

### Alternative hypothesis 2 — vector locking is a special slice, not a general phase

All 91 sampled `(F0,tau)` points at `theta=1.5 deg`, `gamma*=4` are integer locked, but that does not prove a broad phase in `(F0,tau,theta,gamma)` space. [Results 3.6]

**Decisive falsification:** repeat the map at several theta and gamma values, with adaptive refinement near state boundaries. If locking disappears outside a very narrow slice, the language should be reduced to “locking at the tested slice.”

### Alternative hypothesis 3 — boundary reversal is an edge-model choice

The ground-state registry switching mechanism is real within the reduced triangular model, but the exact switch angle moves by ~0.37–0.39 deg over the tested outer-site weighting range. [Results 3.5; SI S6]

This does not falsify the mechanism, but it does falsify any interpretation of `2.921278 deg` or `2.847233 deg` as material constants. The manuscript now states this correctly.

### Causal-overclaim check

No remaining sentence was found that equates mathematical exact inversion of the GSFE with physical reversal of Janus polarization. The manuscript explicitly states that `P_z -> -P_z` requires paired polarity-resolved first-principles surfaces. [Discussion 4.4–4.5]

**Skeptic decision:** the strongest remaining attack is model transferability to full 3D Janus MoSSe, not an internal contradiction in the current calculations.

---

# 5. My Research Connector

For the user's project, the manuscript's reusable methodological core is now clear:

1. **Coordinate-invariant symmetry diagnosis** rather than an origin-fixed sine/cosine interpretation. [Methods 2.3]
2. **Prepared-state branch continuation** rather than a global last-surviving-minimum threshold. [Methods 2.4]
3. **Matched same-spectrum falsification controls** before assigning mechanism. [Results 3.1]
4. **Vector lattice transport** rather than forcing a free 2D system into a scalar switching observable. [Methods 2.7–2.8]
5. **A model hierarchy with hard gates:** rigid GSFE → in-plane relaxation → Janus-specific GSFE-qualified MLIP → full 3D finite-flake relaxation. [Discussion 4.5; SI S9–S11]

The main transfer risk is to treat a generic TMD force field as if it were automatically valid for asymmetric Janus MoSSe. The manuscript's no-go prescreen is therefore not a failed side calculation; it is a useful methodological result that prevents model selection based on whether a desired rectification signal happens to appear.

**Introduction citation draft:** “Finite-contact structural lubricity is controlled not only by twist but also by contact size, shape, boundary pinning, and elastic reconstruction, motivating a branch-resolved treatment when the underlying registry landscape lacks inversion symmetry.”

**Discussion citation draft:** “Within a corrected-GSFE finite-contact model, the directional stability split survives two distinct in-plane compliance representations, while quantitative transfer to real finite MoSSe remains contingent on a Janus-specific three-dimensional atomistic model that reproduces the corrected registry spectrum.”

**My Research Connector decision:** the current paper is a coherent computational-physics paper; its most valuable next step is not another reduced-model figure but the predeclared MLIP gate followed by constrained full-3D relaxation.

---

# A. Contradiction Map

| ID | 쟁점(반드시 질문형 한 줄) | 관점 A와 주장 | 관점 B와 주장 | 충돌 유형(①사실 ②해석 ③범위 ④방법론) | 원문이 이 충돌을 해소해주는가(✅줌·⚠️부분·❌안줌, 해당 시 근거 위치) | 해소 방법(내가 할 일 한 줄) | 우선순위 |
|---|---|---|---|---|---|---|---|
| X1 | 두 in-plane relaxation 결과만으로 실제 fully relaxed MoSSe에서도 정류가 유지된다고 볼 수 있는가? | Domain/Method: 두 다른 in-plane 표현에서 sign과 rho가 유지됨 | Skeptic: 둘 다 동일 local GSFE를 공유하고 collective z/edge reconstruction은 없음 | ③범위·④방법론 | ⚠️부분 — Results 3.4, Discussion 4.5가 in-plane 범위와 미검증 3D 물리를 명시 | Janus-specific GSFE contract를 통과한 MLIP로 constrained full-3D N=127 relaxation | ⚪ 낮음 |
| X2 | triangular switch angle을 재료 고유의 정확한 값으로 볼 수 있는가? | Results: nominal model에서 20/25-deg cut의 정확한 crossing 계산 | Skeptic: outer-site weight만 바꿔도 수 tenths of a degree 이동 | ③범위 | ✅줌 — Results 3.5와 SI S6가 exact angle은 universal constant가 아니라고 명시 | relaxed-edge model에서 mechanism만 재검증하고 정확각 claim은 유지하지 않음 | ⚪ 낮음 |
| X3 | 91/91 integer-lock 결과가 연속 parameter space 전체의 broad locking phase를 증명하는가? | Dynamics: sampled `(F0,tau)` grid 전체가 integer-lock tolerance 통과 | Skeptic: theta=1.5, gamma*=4 slice뿐이며 grid 사이 경계는 미탐색 | ③범위 | ✅줌 — Results 3.6가 “sampled region”으로 제한하고 continuous-space claim을 하지 않음 | 후속에서 `(F0,tau,theta,gamma)` adaptive map | ⚪ 낮음 |
| X4 | thermal directionality의 소실점을 T*=0.60–0.65 사이의 sharp transition으로 볼 수 있는가? | Statistics: mean-current pointwise CI는 0.60까지 zero 제외, 0.65에서 포함 | Skeptic/Stats: pointwise sampled intervals는 연속 Tc나 simultaneous band가 아님 | ③범위·④방법론 | ✅줌 — Discussion 4.3/SI S8에 pointwise이며 simultaneous band가 아니라고 명시 | 필요 시 dense T-grid + simultaneous/bootstrap transition estimator 사전등록 | ⚪ 낮음 |
| X5 | exact GSFE inversion이 실제 Janus polarization reversal을 증명하는가? | Symmetry control: inversion은 threshold/current를 정확히 반전 | Domain/Skeptic: mathematical inversion과 physical Pz reversal은 다른 조작 | ②해석·③범위 | ✅줌 — Discussion 4.4–4.5가 polarity-to-GSFE law 미확립을 명시 | paired polarity-resolved DFT GSFE 계산 | ⚪ 낮음 |

**Research Gap 후보:** 이 최종 원고에서는 위 핵심 충돌들이 모두 적어도 부분적으로 원문에서 범위가 규정되어 있어 `❌안줌` 행은 없습니다.

---

# B. Claim Reliability Table

> 이 skill의 High 기준은 직접 측정 + 적절한 control + effect size + replication을 모두 요구합니다. 본 논문은 계산 논문이므로, 내부 검증이 매우 강하더라도 중심 모델 claim은 보수적으로 `🟡 Medium`으로 유지합니다.

| ID | 주장(내 언어로 재진술) | 근거 위치(Fig·Table·섹션 번호, 없으면 "없음") | 근거 유형(직접 측정 / 통계 추론 / 모델·시뮬레이션 / 선행연구 인용 / 저자 해석 / 근거 없음) | 지지 관점 | 반박 관점 | 신뢰도(🟢High/🟡Medium/🔴Low) | 상태(Confirmed/Corrected/Demoted) | 내 검증 액션(한 문장, 없으면 "없음") |
|---|---|---|---|---|---|---|---|---|
| C1 | corrected 2H MoSSe GSFE는 registry-origin 이동으로 제거되지 않는 inversion asymmetry를 가진다 | Results 3.1; Fig.1; SI S4 | 모델·시뮬레이션 | Domain, Method, Skeptic | full DFT surface 자체는 external input | 🟡Medium | Confirmed | atomistic gate에서 odd sector를 독립 재현 |
| C2 | 준비된 ground-state finite contact는 guide 없이 full-2D directional depinning을 보인다 | Results 3.2; Fig.2; Table 3; SI S2 | 모델·시뮬레이션 | Domain, Method | Skeptic: full-3D reconstruction 미검증 | 🟡Medium | Confirmed | GSFE-qualified full-3D relaxation |
| C3 | compact contacts의 twist response는 tested families에서 theta sqrt(N)로 잘 collapse한다 | Results 3.3; Fig.3; SI S5 | 모델·시뮬레이션 | Domain, Statistics | arbitrary/deformable shape로 일반화 불가 | 🟡Medium | Confirmed | relaxed compact contacts에서 scaling 재검증 |
| C4 | rotated triangular boundaries는 registry ground-state switch를 통해 directional sign을 뒤집을 수 있다 | Results 3.5; Fig.4; SI S6 | 모델·시뮬레이션 | Domain, Method | Skeptic: switch angle edge-model sensitive | 🟡Medium | Demoted (exact angle not material constant) | atomistic relaxed-edge calculation |
| C5 | tested drive-period slice에는 여러 oblique integer-locked states가 있고 대표 (1,-1) orbit은 attracting이다 | Results 3.6; Fig.5; SI S7 | 모델·시뮬레이션 | Domain, Method, Stats | Skeptic: only one theta/gamma slice | 🟡Medium | Confirmed | theta/gamma 확장 map |
| C6 | present thermal protocol에서 mean vector current는 sampled T*=0.60까지 pointwise resolved되고 0.65에서 unresolved된다 | Results 3.7; Fig.6; SI S8 | 통계 추론 + 모델·시뮬레이션 | Statistics, Domain | Skeptic: sharp Tc 아님 | 🟡Medium | Corrected (pointwise scope) | dense T-grid 또는 simultaneous inference |
| C7 | tested in-plane compliance는 absolute threshold를 바꾸지만 directional splitting의 sign과 rho를 크게 훼손하지 않는다 | Results 3.4; Table 3; SI S9–S10 | 모델·시뮬레이션 | Domain, Method | Skeptic: shared GSFE; z/edge missing | 🟡Medium | Confirmed within in-plane scope | full-3D Janus-qualified MLIP validation |

**인용 금지 목록:** 핵심 C1–C7에는 `🔴 Low`가 없습니다. 다만 “physical polarization reversal이 rectification을 반드시 반전시킨다”, “300 K에서 작동한다”, “nominal triangular switch angle이 material constant다”, “full 3D MoSSe에서 이미 검증됐다”는 문장은 현 논문의 확립된 결과로 인용하면 안 됩니다.

---

# C. 빠진 여섯 번째 관점 — Atomistic Model-Validation / Force-Field Transferability Reviewer

이 reviewer가 묻는 것은 “계산을 더 많이 했는가?”가 아니라 **새 atomistic model이 우리가 필요한 Janus chemical/registry space에서 실제로 신뢰할 수 있는가?**입니다.

일반 TMD MLIP가 평균 test MAE가 낮더라도 Janus Se-S-Se-S의 inversion-odd sector 또는 작은 higher harmonics를 틀릴 수 있습니다. 이번 empirical SW+KC prescreen이 바로 그 위험을 보여줍니다: dominant first harmonic과 전체 shape correlation은 괜찮았지만 W2/W3가 corrected DFT보다 크게 과대평가되어 quantitative no-go가 됐습니다. [SI S11]

따라서 full-3D calculation 전에 필요한 evidence는 predeclared Janus-specific contract입니다: 31×31 이상 registry map, registry별 interlayer-distance relaxation, D6/translation alignment, W1/phi1, odd RMS, full-shape correlation/RMSE, higher-shell error를 모두 검사해야 합니다. 이것을 통과한 모델만 finite flake에 적용해야 합니다.

---

# D. Research Gap

### 명시적 gap 3개

1. **Full 3D finite-contact relaxation gap:** collective corrugation/buckling, atomistic edge reconstruction/chemistry, defects, nonlocal edge energetics가 없다. [Discussion 4.5; SI S12]
2. **Physical dynamics/load calibration gap:** load-dependent GSFE, participating mass, damping, physical temperature/time/frequency mapping이 없다. [Discussion 4.5]
3. **Polarity-to-GSFE gap:** physical `P_z -> -P_z`가 전체 GSFE Fourier spectrum과 rectification을 어떻게 바꾸는지 paired first-principles input이 없다. [Discussion 4.4–4.5]

### 숨은 gap 2개

1. **[추론] Full dynamical phase-space gap:** deterministic map은 `theta=1.5 deg`, `gamma*=4` slice이므로 `(F0,tau,theta,gamma)`의 global topology와 multistability boundaries는 아직 미확립이다. [Methods 2.7; Results 3.6]
2. **[추론] Simultaneous thermal operating-window gap:** 온도별 trajectory bootstrap은 적절하지만 pointwise CI이므로 전체 temperature curve에 대한 simultaneous confidence band나 formally estimated transition point는 제공하지 않는다. [Methods 2.8; Discussion 4.3; SI S8]

---

# E. 다음 액션 3개

| 이번 주 액션 | 필요한 입력/material/data | 산출물 / 판정 기준 | 해결하는 claim/gap |
|---|---|---|---|
| **1. Janus-specific MLIP GSFE gate 실행** | Shaidu-type dispersion-aware TMD checkpoint 또는 다른 candidate MLIP, corrected Angeli+Erratum target | 2H Se-S-Se-S 31×31 GSFE + registry별 z-relaxation. 사전등록 기준(W1<=10%, phi1<=5deg, odd RMS<=10%, r>=0.98, normalized RMSE<=0.05, higher shells preferably <=0.2 meV)을 통과해야 PASS | C1, C2, explicit gap 1 |
| **2. Gate 통과 모델로 constrained full-3D N=127 relaxation** | PASS MLIP, theta=1.5 deg부터 시작 | COM registry를 constraint하고 모든 atomic x,y,z relaxation 후 F_c,+/-, rho, z corrugation, edge displacement 산출. Directional sign 유지 여부가 핵심 decision | C2, C4, C7, explicit gap 1 |
| **3. Paired load/polarity GSFE pilot** | 최소 2–4 normal-load/interlayer conditions + physically reversed Janus orientation의 first-principles surfaces | U(r;load,polarity), odd sector, Delta F_c의 load/polarity dependence. Physical reversal에서 sign relation이 성립하는지 판정 | explicit gaps 2–3 |

---

# Final audit decision

**현재 원고는 이전 버전의 주요 내부 모순을 해결한, 상당히 강한 DFT-anchored reduced-model computational paper입니다.** Prepared-state ambiguity, gauge-dependent asymmetry interpretation, matched-control deficiency, cycle-level pseudoreplication, finite-size over-interpretation, boundary-reversal mechanism, Floquet conditioning, 그리고 linear-elastic discretization 의존성은 모두 크게 보완됐습니다.

다만 **실제 fully relaxed Janus MoSSe finite contact에 대한 정량적 material prediction**으로 제출하려면 아직 `Major Revision`에 해당합니다. 가장 큰 이유는 단 하나의 일관된 다음 단계로 압축됩니다: **corrected Janus GSFE contract를 먼저 통과하는 atomistic/ML potential을 확보하고, 그 뒤에 full-3D finite-flake relaxation을 수행해야 합니다.**

반대로 논문의 scope를 현재 제목/부제와 Discussion처럼 **“corrected-DFT-GSFE-anchored finite-contact model with explicit robustness tests”**로 유지한다면, 중심 계산 주장들은 서로 정합적이며 남은 문제들은 명시된 model-input limitations로 관리되고 있습니다.
