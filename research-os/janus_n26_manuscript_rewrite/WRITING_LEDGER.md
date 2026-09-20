# N26 Manuscript Writing Ledger

## Authority and freeze state

- Branch base: N25 exact figure head \`4060d017a50c6387de45377621d9232529e7e4ad\`.
- Argument authority: \`research-os/janus_n21_argument_architecture/\`.
- Numerical/claim authority: \`research-os/janus_n17_upstream_strengthening/CLAIM_EVIDENCE_MATRIX_v3.csv\`.
- Figure authority: N25 seven-figure set, all \`BENCHMARK_PASS\`.
- Scientific stop gate: N17 PASS; no scientific blocker/major/moderate open.
- Remaining non-scientific item: archival DOI/identifier (\`FR-R01\`, venue layer).

## Claim ledger for main text

| Claim IDs | Planned section | Allowed statement | Mandatory boundary |
|---|---|---|---|
| M0, C5 | Methods 2.1–2.2; Results 1 | Published 2H MoSSe Fourier GSFE anchors an unguided prepared-state reduced model. | Printed-precision audit is not a DFT-fit covariance; complete dynamics are not first-principles. |
| C1 | Results 1 | Registry-space inversion asymmetry is non-removable under translation. | Do not identify it with physical out-of-plane polarity reversal. |
| C2, C3 | Results 2 | Lowest-energy prepared branch has direction-split full-2D depinning; generic boundary segments are fold-like. | State/loading-axis/reduced-model conditioned; isolated higher-order point is not a generic saddle-node. |
| C4 | Results 3 | Same-spectrum symmetrization removes global bias/current; exact inversion swaps/reverses them. | Mathematical same-spectrum intervention, not demonstrated experimental polarity reversal. |
| C6, C7 | Results 4 | Tested compact hex/disk contacts follow \(\Theta=\theta\sqrt N\) similarity. | Not arbitrary shapes/edges; 0.5036 is not a new critical exponent. |
| C20, C21 | Results 4 | FEM and nonlinear VFF soften absolute thresholds but preserve sign at tested stiffnesses. | In-plane only; not full 3D atomistics. |
| C8, C9 | Results 5 | Boundary orientation can switch the equilibrium prepared registry family and reverse bias. | Exact switch angle is edge-model sensitive; no path/hysteresis claim. |
| C13, C14 | Results 6 | 91 sampled points are cycle-resolved integer locked for \(m^*=1,\gamma^*=4\); representative plateaus are Floquet-attracting. | Not a continuous phase diagram; not all 91 independently Floquet-certified; damping reorganizes windings. |
| C15–C19 | Results 7 | Exact winding identity is fragile, while stationary directed mean current remains nonzero through sampled \(T^*=0.70\). | No critical temperature or extrapolation beyond 0.70; trajectory is inference unit. |
| C22–C25 | Discussion 4 | Explicit limits on material constants, 3D atomistics, polarity mapping, and experimental calibration. | These are boundaries, not hidden assumptions. |
| N1, N2 | Introduction/Conclusion | Combination-level contribution only. | No “first friction diode/ratchet/mode-locking” claim. |

## Number ledger

| ID | Canonical value / range | Source contract | Planned use |
|---|---|---|---|
| N-M0-1 | \(W=(7.9,0.1,0.1)\) meV; \(\phi=(131.9,1.2,85.4)^\circ\) | M0 | Methods, Results 1 |
| N-M0-2 | source-resolution joint LHS: \(\Delta F_c^*=1.77264\)–1.84708; \(\rho=0.41716\)–0.42002 | M0/FR-M01 | Results/Discussion if needed |
| N-C1 | \(A_{\min}=0.04253608528083\); odd RMS 0.20624278237270; \(\chi_1=0.583541211356\) | C1 | Results 1 |
| N-C2 | at \(1.5^\circ\): \(F_{c,+}^*=3.0711353385\), \(F_{c,-}^*=1.2586722985\), \(\rho=0.418601\) | C2 | Results 2 |
| N-C3 | higher-order point \(\theta\approx2.9733856558^\circ\), \(F_+^*\approx1.9100735315\), hard mode ~6.9138 | C3 | Results 2 / SI |
| N-C6 | characteristic-angle exponent ~0.5036, approaching ~0.5013 when small N removed | C6 | Results 4 |
| N-C7 | max compact deviations through \(\Theta=20\): hex <=0.0818%/+ and 0.0800%/−; disk <=0.0230%/+ and 0.0222%/−; family mean difference <=~0.105% | C7 | Results 4 |
| N-C8 | switch angles: 2.921278008381° (20°), 2.847233122262° (25°) | C8 | Results 5 |
| N-C9 | weighted switch ranges: 20° 2.7779–3.1701°; 25° 2.7108–3.0832° | C9 | Results 5 |
| N-C13 | 91/91 sampled points cycle locked; max single-cycle residual ~9.55e-10 | C13 | Results 6 |
| N-C14 | canonical closure ~2e-11; \(\rho_F\approx6.31\times10^{-22}\); six representative states \(\rho_F<1\); 24/24 timestep and 162/162 basin probes pass | C14 | Results 6 |
| N-FR-M02 | 72 gamma×drive points; only 1/12 drive points preserves gamma=4 winding for all tested gamma | FR-M02/C13 | Results 6 / Discussion 3 |
| N-C16 | at \(T^*=0.70\): mean \(v=-0.07645\), 95% CI [-0.10088,-0.05195] | C16 | Results 7 |
| N-C17 | at 0.70: mean \((u,v)=(0.036998,-0.076448)\); u CI [0.01265,0.06132], v CI [-0.10088,-0.05195]; Hotelling/Mahalanobis 38.07 vs 95% threshold 6.04 | C17 | Results 7 |
| N-FR-S01 | >=95% decision stability by N=100,200,200,300,500 at T*=0.50,0.55,0.60,0.65,0.70 | FR-S01/C17 | Results 7 / SI |
| N-C18 | \(P(v_{\rm cycle}<0)=0.51933\) [0.51632,0.52237] at 0.50 and 0.50802 [0.50506,0.51100] at 0.70; target winding ~0.011 at 0.70 | C18 | Results 7 |
| N-C19 | targeted dt reruns differ by <=1.12 combined SE in either component | C19 | Results 7 / SI |
| N-C20 | nominal FEM at 1.5°: 2.934302 / 1.190210, \(\rho=0.422860\) | C20 | Results 4 |
| N-C21 | nominal VFF at 1.5°: 2.935400 / 1.190479, \(\rho=0.422921\) | C21 | Results 4 |

## Symbol ledger

| Symbol | Meaning | Domain / unit |
|---|---|---|
| \(\mathbf r\) | local registry coordinate | reduced triangular-lattice coordinates |
| \(\mathbf R=(x,y)\) | finite-contact center-of-mass registry | 2D |
| \(\mathbf r_i\) | site reference coordinate | triangular lattice |
| \(\theta\) | imposed relative twist | degrees unless stated |
| \(N\) | number of sites in contact | integer |
| \(u(\mathbf r)\) | normalized local GSFE | normalized by \(6W_1\) |
| \(U_N(\mathbf R;\theta)\) | finite-contact rigid GSFE per site | dimensionless |
| \(\mathbf G_{\ell m}\) | reciprocal vector in shell \(\ell\) | reciprocal-lattice units |
| \(W_\ell,\phi_\ell\) | published Fourier amplitude and phase | meV, degrees |
| \(S_{\mathbf G}\) | finite-contact structure factor | dimensionless |
| \(\Theta=\theta\sqrt N\) | compact-contact similarity coordinate | deg \(\sqrt{\rm site}\) as plotted convention |
| \(A_{\rm odd},A_{\min}\) | normalized odd Fourier power and its translation minimum | dimensionless |
| \(\chi_1\) | translation-invariant first-shell triad phase diagnostic | dimensionless |
| \(F_y,F_{c,\pm}\) | applied longitudinal force and prepared depinning thresholds | reduced force |
| \(\rho\) | normalized threshold split | dimensionless |
| \(m^*,\gamma^*\) | reduced mass and damping | reduced |
| \(F_0^*,\tau^*\) | rocking amplitude and period | reduced |
| \((m,n)\) | integer lattice winding per drive cycle | integers |
| \(\rho_F\) | Floquet spectral radius | dimensionless |
| \(T^*\) | reduced thermal-noise scale | reduced |
| \(\boldsymbol{\xi}(t)\) | unit white noise | \(\langle\xi_\mu(t)\xi_\nu(t')\rangle=\delta_{\mu\nu}\delta(t-t')\) |
| \(k_\perp^*\) | optional transverse guide stiffness | reduced |

## Retired prose that must not re-enter N26

- “mean \(v\) is unresolved at \(T^*=0.65\)” — superseded by stationary 60+100 protocol.
- “zero current is included at \(T^*=0.70\)” — superseded; pooled stationary N=1000 excludes zero through 0.70.
- 10-burn/10-measure thermal inference — historical only.
- every depinning point is a generic saddle-node — false at the isolated higher-order point.
- every point in a continuous \((F_0,\tau)\) plane is locked — unsupported.
- exact GSFE inversion equals physical Janus-polarity reversal — not established.
- rigid \(F_c\) is a universal experimental material constant — rejected.
- \(\eta\) susceptibility / \(\eta\approx0.5\) optimum — rejected.
- generic “first friction diode/ratchet/mode locking” novelty language — rejected.
