# Janus MoSSe Mechanical Rectification — N26 Manuscript Draft

> **Drafting status:** claim-frozen prose reconstruction from the N21 argument architecture and the N25 benchmark-passed seven-figure set. Methods are drafted first by Research OS policy. Results, Discussion, Introduction, Abstract, and title will be added in that order. No new simulation or scientific claim is introduced here.

## 2. Model and Computational Methods

### 2.1. Published MoSSe generalized stacking-fault-energy landscape

The conservative interfacial input is the three-shell generalized stacking-fault-energy (GSFE) parameterization reported for the asymmetric 2H Se–S–Se–S stacking of Janus MoSSe by Angeli *et al.* [12]. For each reciprocal shell, the six reciprocal vectors form two \(C_3\)-related triads connected by \(\mathbf G\rightarrow-\mathbf G\). Because the registry energy is real, the associated Fourier amplitudes are conjugate pairs. Choosing one triad as the positive representatives gives the dimensionless local registry energy

\[
u(\mathbf r)=
\sum_{\ell=1}^{3}\frac{W_\ell}{3W_1}
\sum_{m=1}^{3}
\cos\!\left(\mathbf G_{\ell m}\!\cdot\!\mathbf r+\phi_\ell\right),
\tag{1}
\]

where energies are normalized by \(6W_1\). The published coefficients used throughout this work are

\[
(W_1,W_2,W_3)=(7.9,0.1,0.1)\ {\rm meV},
\qquad
(\phi_1,\phi_2,\phi_3)=(131.9^\circ,1.2^\circ,85.4^\circ).
\]

The conjugate reciprocal triad corresponds to \(\phi_\ell\rightarrow-\phi_\ell\), i.e., spatial inversion of the same Fourier spectrum. The 2024 Erratum to Ref. [12] does not report a correction to these GSFE coefficients or their conjugate phase pairing [13].

In the source first-principles calculation, the aligned bilayer was sampled on a \(9\times9\) lateral-displacement grid; at each registry the in-plane coordinates were fixed while the interlayer separation was relaxed before the stacking-dependent quantities were fitted [12]. Thus Eq. (1) contains local registry-by-registry vertical-separation relaxation inherited from the source GSFE, but it does not describe collective corrugation or buckling of a finite contact, atomistic edge reconstruction, defects, or nonlocal edge chemistry.

The tabulated Fourier parameters are available only at finite printed precision. We therefore treat Eq. (1) as the declared material input rather than inventing an unavailable fit covariance. A separate source-resolution audit varies each reported \(W_\ell\) and \(\phi_\ell\) over the half-unit interval implied by its printed precision (\(\pm0.05\) in the tabulated units). Those perturbations are used only as a reporting-precision sensitivity bound; they are not interpreted as a statistical DFT or fit-uncertainty distribution.

### 2.2. Finite unguided contact and twist averaging

The headline system is a finite, unguided two-dimensional contact. A contact contains \(N\) sites at triangular-lattice reference positions \(\mathbf r_i\), and the center-of-mass registry coordinate \(\mathbf R=(x,y)\) is free to move in the full two-dimensional primitive cell. At imposed relative twist \(\theta\), the rigid-contact energy per site is

\[
U_N(\mathbf R;\theta)=
\frac{1}{N}\sum_{i=1}^{N}
u\!\left[
\mathbf R+
(\mathcal R_\theta-\mathbf I)\mathbf r_i
\right],
\tag{2}
\]

where \(\mathcal R_\theta\) is the in-plane rotation matrix. For an individual reciprocal vector \(\mathbf G\), the finite-contact cancellation is summarized by the structure factor

\[
S_{\mathbf G}(\theta)=
\frac{1}{N}\sum_{i=1}^{N}
\exp\!\left[
i\mathbf G\!\cdot\!
(\mathcal R_\theta-\mathbf I)\mathbf r_i
\right].
\tag{3}
\]

For compact self-similar contacts the linear size scales as \(R_{\rm c}\propto\sqrt N\). At small twist,
\(\mathcal R_\theta-\mathbf I=\theta\mathbf J+O(\theta^2)\), so the phase accumulated across the contact scales as \(|\mathbf G|R_{\rm c}\theta\). This motivates the similarity coordinate

\[
\Theta=\theta\sqrt N,
\tag{4}
\]

which is tested directly rather than inferred from a fitted exponent alone.

Unless stated otherwise, the reference contact is the compact \(N=127\) hexagon and the added transverse confinement is zero, \(k_\perp^*=0\). The prepared state is always the lowest-energy stable zero-force minimum. In this manuscript, “unguided” refers only to the absence of an added transverse guide in the reduced GSFE model; it does not imply a parameter-free experimental device.

### 2.3. Coordinate-independent registry inversion asymmetry and matched controls

A sine/cosine decomposition about one arbitrarily chosen registry origin is not itself a coordinate-independent measure of inversion asymmetry because a translation mixes the two coefficient sets. For a translated origin \(\mathbf a\), let \(c_\alpha(\mathbf a)\) and \(s_\alpha(\mathbf a)\) denote the even and odd coefficients in a common reciprocal basis. We define the normalized odd power

\[
A_{\rm odd}(\mathbf a)=
\frac{\sum_\alpha s_\alpha(\mathbf a)^2}
{\sum_\alpha\left[c_\alpha(\mathbf a)^2+s_\alpha(\mathbf a)^2\right]},
\qquad
A_{\min}=\min_{\mathbf a} A_{\rm odd}(\mathbf a),
\tag{5}
\]

and report \(\sqrt{A_{\min}}\) as the translation-minimized odd-RMS fraction. The minimum is located using a \(181\times181\) registry grid followed by independent local refinements. As an independent phase diagnostic, the first-shell complex amplitudes \(C_1,C_2,C_3\) define

\[
\chi_1=
\operatorname{Im}
\left(
\frac{C_1C_2C_3}{|C_1C_2C_3|}
\right).
\tag{6}
\]

Because \(\mathbf G_1+\mathbf G_2+\mathbf G_3=0\), the triad product is invariant to a registry translation. In the equal-phase representation of the published first shell, Eq. (6) reduces to \(\sin(3\phi_1)\).

Two matched controls are built from the same translation-centered 2H spectrum. In the **symmetrized** control, the inversion-odd coefficients are set to zero while the even sector is retained. In the **exact-inversion** control, the odd coefficients change sign. The symmetrized surface can contain a degenerate inversion-related pair of minima; therefore a threshold attached to one arbitrarily selected member need not be direction-degenerate. The symmetry-null static observable is the paired/global envelope over the degenerate ground-state pair. Exact inversion imposes the stronger contracts

\[
F_{c,+}[U_{\rm inv}]=F_{c,-}[U],\qquad
F_{c,-}[U_{\rm inv}]=F_{c,+}[U],
\tag{7}
\]

together with reversal of the lattice-vector current under the same dynamical protocol.

For mechanism isolation in the Supporting Information, a centered interpolation
\(U_\eta=U_{\rm even}+\eta U_{\rm odd}\) is retained as a mathematical homotopy. We do not interpret \(d\Delta F_c/d\eta\), an intermediate value of \(\eta\), or \(\eta\rightarrow-\eta\) as a material susceptibility, an optimum, or a physical reversal of the Janus polarization.

### 2.4. Prepared-state depinning and stability boundaries

A spatially uniform longitudinal force \(F_y\) tilts the finite-contact energy as

\[
V(\mathbf R;F_y,\theta)=U_N(\mathbf R;\theta)-F_y y.
\tag{8}
\]

A pinned state is a full two-dimensional local minimum satisfying

\[
\nabla U_N(\mathbf R;\theta)=(0,F_y),
\qquad
\lambda_{\min}(\mathbf H)>0,
\tag{9}
\]

where \(\mathbf H=\nabla\nabla U_N\) is the \(2\times2\) Hessian. The force is a center-of-mass/body-force tilt at fixed imposed twist. Rotational relaxation or applied torque, finite-stiffness spring pulling, and edge- or center-localized pulling are outside the present protocol.

The headline threshold is **branch-followed**. At \(F_y=0\), the lowest-energy stable minimum is identified; that same minimum is continued quasi-statically under \(+y\) or \(-y\) loading until it loses stability. Competing zero-force minima are continued separately rather than allowing the threshold definition to switch basins. An initial survey is strengthened by a 491-point dense/adaptive continuation over \(0^\circ\le\theta\le3^\circ\), with 16 independent \(21\times21\) stationary-point enumerations concentrated around the isolated high-order boundary region. The resulting statement is a dense numerical interval verification, not an interval-arithmetic proof over every real \(\theta\).

Candidate generic folds are refined by solving the two equilibrium equations together with \(\det\mathbf H=0\). Accepted solutions have augmented residual below \(10^{-7}\) and a nonsoft Hessian eigenvalue larger than \(10^{-6}\); generic segments are further checked for nonzero cubic variation along the soft eigenvector and nonzero coupling to the force parameter. Because an isolated point near \(\theta=2.97338566^\circ\) violates the generic cubic condition, we use “depinning boundary” or “stability boundary” for the full curve and reserve “fold” for generic portions.

For compact notation we report

\[
\rho=
\frac{F_{c,+}-F_{c,-}}
{F_{c,+}+F_{c,-}},
\tag{10}
\]

but neither \(F_c\) nor \(\rho\) is treated as a universal experimental material constant.

### 2.5. Compact size/shape scaling and boundary-state competition

Two geometry classes are deliberately separated. The first tests self-similar compact contacts. The characteristic-angle calculation uses hexagonal contacts with
\(N=37,61,91,127,169,217,271,331,397,\) and \(469\). For \(q=0.95,0.90,0.85,\) and \(0.80\), the characteristic twist \(\theta_q\) is obtained by directly solving

\[
F_c(\theta_q)=qF_c(0)
\tag{11}
\]

rather than by interpolating between coarse samples. A second dense calculation extends the compact hexagonal family to
\(N=127,217,331,469,631,817,1027,1261\)
and introduces disk-like contacts with
\(N=127,241,367,517,721,931\).
Both families are evaluated at every integer \(\Theta\) from 0 to 20.

The second geometry class tests boundaries capable of changing the prepared registry state. Fixed-\(N=127\) triangular contacts are cut at different orientations relative to the lattice. For the \(20^\circ\) and \(25^\circ\) cases, both low-energy registry families are continued as functions of twist and their zero-force energies are compared before loading. Their crossing defines an equilibrium preparation switch. To test whether that switch is tied to one particular edge parameterization, the 48 outer sites are assigned local-GSFE weights from 0.5 to 1.5 while all interior sites retain unit weight. This weighting is a sensitivity model, not an atomistic description of edge chemistry. Accordingly, persistence of competing registry families and their crossing is considered meaningful within the reduced model, whereas the numerical switching angle is not treated as universal.

### 2.6. In-plane relaxation hierarchy

To test whether the directional response is an artifact of a perfectly rigid contact, we use two independent in-plane relaxation representations while retaining the same published GSFE as the interfacial energy.

The first representation is a free-edge triangular finite-element membrane for the \(N=127\) contact. Each site acquires a two-component internal displacement, while the center-of-mass registry and imposed twist remain external coordinates. The two rigid translations and infinitesimal rigid rotation are projected out, leaving \(2+(2N-3)=253\) equilibrium degrees of freedom when the two registry coordinates are included. The total energy has the form

\[
E_{\rm FEM}
=
\sum_i u(\mathbf r_i^{\,\rm loc})
+
\frac12\int_A
\boldsymbol{\varepsilon}:\mathbf C:\boldsymbol{\varepsilon}\,dA,
\tag{12}
\]

with isotropic in-plane elasticity. The nominal parameters are
\(a=3.25\) Å,
\(C_{11}=119.3\ {\rm N\,m^{-1}}\),
\(C_{12}=27.5\ {\rm N\,m^{-1}}\), and
\(C_{66}=(C_{11}-C_{12})/2=45.9\ {\rm N\,m^{-1}}\) [17].
We additionally test half and twice the nominal stiffness, an independent literature-level pair
\((C_{11},C_{12})=(126.8,27.4)\ {\rm N\,m^{-1}}\), and a \(100C\) rigid-limit check.

The second representation is a geometrically nonlinear triangular-site valence-force model containing 342 nearest-neighbor bond-stretching terms and 648 local \(60^\circ\) angle terms. Its independently reconstructed nominal coefficients,
\(k_s=5.289992\ {\rm eV\,\AA^{-2}}\) and
\(k_\theta=2.334491\ {\rm eV\,rad^{-2}}\),
reproduce the target homogeneous elastic constants before the depinning branches are recomputed. The same rigid modes are projected out. Agreement between the FEM and VFF calculations tests in-plane model-form sensitivity; neither representation adds out-of-plane buckling, collective interlayer corrugation, atomistic edge reconstruction, or full three-dimensional atomistics.

### 2.7. Zero-mean rocking and relative-periodic transport

Deterministic transport is generated by sinusoidal zero-mean forcing along the declared \(y\) direction,

\[
m^*\ddot{\mathbf R}
+\gamma^*\dot{\mathbf R}
=
-\nabla U_N(\mathbf R;\theta)
+
F_0^*
\sin\!\left(\frac{2\pi t}{\tau^*}\right)\hat{\mathbf y}.
\tag{13}
\]

The headline map uses the reduced dynamical parameters \(m^*=1\) and \(\gamma^*=4\). These parameters are part of the declared dynamical protocol; they are not supplied by the DFT GSFE. The canonical operating point is
\(\theta=1.5^\circ\),
\(F_0^*=2.0\), and
\(\tau^*=40\).
The sampled amplitude-period map contains
\(F_0^*=1.0,\ldots,4.0\) in steps of 0.25 and
\(\tau^*=20,30,40,50,60,70,80\), for 91 points in total. Each point is evolved for 20 transient cycles and 40 measured cycles with 4000 integration steps per cycle.

For each measured cycle, the unwrapped displacement is decomposed in the triangular-lattice basis,

\[
\Delta\mathbf R_{\rm cyc}
=m\,\mathbf a_1+n\,\mathbf a_2+\boldsymbol{\epsilon},
\tag{14}
\]

and an integer winding pair \((m,n)\) is assigned when the residual \(\boldsymbol{\epsilon}\) satisfies the numerical locking criterion. The stronger audit requires every measured cycle at a sampled point to repeat the same integer winding after transients.

Representative pinned, low-winding, and high-winding plateaus are then treated as relative-periodic orbits. A one-period shooting condition is solved modulo the lattice translation \((m,n)\), the monodromy matrix is propagated independently, and local attraction is assessed from the Floquet spectral radius \(\rho_F<1\). DOP853 at two tolerance levels and the implicit Radau solver provide cross-solver checks. Time-step refinement, increasing/decreasing amplitude continuation, and local position/velocity perturbations provide additional conditioning and basin tests. Floquet certification is applied to representative plateaus, not inferred for all 91 sampled states.

Because damping changes the winding structure rather than merely shifting one boundary, we also perform a compact joint damping-drive audit over
\(\gamma^*=2,3,4,5,6,8\),
\(F_0^*=1.4,2.0,2.6,3.0\), and
\(\tau^*=30,40,60\).
The headline amplitude-period map is therefore explicitly protocol-specific to \(m^*=1,\gamma^*=4\); it is not presented as a material-only dynamical phase diagram.

### 2.8. Stationary thermal dynamics and vector-current inference

Finite-temperature trajectories use the reduced two-dimensional Langevin equation

\[
m^*\ddot{\mathbf R}
+\gamma^*\dot{\mathbf R}
=
-\nabla U_N(\mathbf R;\theta)
+
F_0^*
\sin\!\left(\frac{2\pi t}{\tau^*}\right)\hat{\mathbf y}
+
\sqrt{2\gamma^*T^*}\,\boldsymbol{\xi}(t),
\tag{15}
\]

with independent unit white-noise components satisfying

\[
\langle \xi_\mu(t)\xi_\nu(t')\rangle
=
\delta_{\mu\nu}\delta(t-t').
\tag{16}
\]

Equation (15) is integrated with BAOAB. The production time step is \(dt=0.02\), and the stationary protocol discards 60 burn cycles before measuring 100 cycles. The full series \(T^*=0.02\)–0.70 uses 500 independent trajectories per temperature. The high-temperature range \(T^*=0.50\)–0.70 is independently repeated with a second 500-trajectory seed ensemble, giving a pooled \(N=1000\) for the high-\(T^*\) inference.

The trajectory, not the individual cycle, is the inferential unit. Cycle data are first reduced within each trajectory to the mean lattice-basis displacements \((\bar u,\bar v)\), the fraction \(P(v_{\rm cycle}<0)\), and the fraction assigned to the deterministic target winding \((m,n)=(1,-1)\). Stationarity is checked by comparing late 20-cycle blocks, and memory of deterministic-orbit, ground-state, and metastable initial conditions is tested under common-noise protocols. High-temperature component intervals are estimated by trajectory-level bootstrap, and the two-component mean vector is tested against the zero-current vector using the corresponding joint covariance/Hotelling statistic. Bootstrap inference is never performed by treating cycles from the same trajectory as independent replicates.

The pooled \(N=1000\) design is supplemented by an explicit trajectory-count precision audit. Without-replacement subsamples of the pooled high-temperature ensembles are used to determine the sample size at which at least 95% of subsamples reproduce the same zero-vector rejection decision. This threshold is reached by \(N=100,200,200,300,\) and \(500\) at \(T^*=0.50,0.55,0.60,0.65,\) and \(0.70\), respectively. Targeted independent runs at \(dt=0.04,0.02,\) and \(0.01\) test effect-size compatibility at high temperature. These checks support the quoted finite-range inference but do not constitute a proof of stochastic-integrator convergence for all observables or temperatures.

### 2.9. Engineered transverse confinement as a secondary control

A transverse guide is included only as a pathway-control comparison by adding

\[
U_{\rm guide}(x)=\frac12 k_\perp^*x^2
\tag{17}
\]

to the finite-contact energy. The branch-resolved search is then repeated at selected \(k_\perp^*\), with \(k_\perp^*=25\) retained as a representative guided comparison. This guide is not required for the headline rectification mechanism, and the sampled \(k_\perp^*\) values are not interpreted as a complete confinement phase diagram.

### 2.10. Numerical reproducibility and scope

The published-GSFE implementation, analytic gradient and Hessian, and the canonical unguided release were regenerated from clean directories and compared with independent reference implementations. The claim-frozen evidence package contains the dense prepared-branch continuation; stationary-point checkpoints; translation/gauge and same-spectrum symmetry audits; exact characteristic-angle and dense compact size/shape calculations; boundary-registry and edge-weight analyses; cycle-resolved 91-point winding map; representative shooting, Floquet, time-step, continuation, and basin checks; the joint damping-drive audit; stationary trajectory-level thermal data and bootstrap/Hotelling summaries; trajectory-count convergence; and fresh FEM and independently reconstructed nonlinear-VFF calculations.

The model hierarchy is intentionally bounded. The present work establishes reduced-model behavior anchored to the published lateral GSFE and tested against two in-plane relaxation representations. It does **not** supply a full three-dimensional atomistically relaxed finite MoSSe interface, a demonstrated physical mapping between mathematical GSFE inversion and reversal of Janus polarization, or a calibration that converts \(T^*\), \(\tau^*\), \(m^*\), \(\gamma^*\), and \(F_0^*\) into kelvin, hertz, physical mass, damping, or device force. Those quantities require independent atomistic or experimental input.


## 3. Results

### 3.1. The published 2H GSFE contains non-removable registry inversion asymmetry

The mechanism tested below depends first on whether the imported lateral energy landscape is itself inversion asymmetric in a coordinate-independent sense. We therefore begin with the published 2H Se–S–Se–S GSFE rather than with a phenomenological ratchet potential. The three-shell Fourier representation in Eq. (1), together with the \(N=127\) unguided contact and lowest-energy zero-force preparation, defines the reference model used throughout the main figures (Figure 1a,b). Independent complex and conjugate-paired implementations of the published coefficients agree at approximately \(10^{-13}\) or better, and the 2024 Erratum does not alter the GSFE coefficient set used here. Varying the printed amplitudes and phases over their reporting-resolution intervals also preserves the sign of the static directional split and the canonical \((1,-1)\) deterministic winding. This check bounds sensitivity to the published decimal precision; it does not replace the unavailable source-fit covariance or raw GSFE grid.

A registry-origin shift cannot remove the asymmetric component. Minimizing Eq. (5) over translations gives

\[
A_{\min}=0.0425361,
\qquad
\sqrt{A_{\min}}=0.206243,
\]

and independent local refinements converge to the same minimum with a multistart spread of order \(10^{-16}\). The first-shell triad invariant gives
\(\chi_1=0.583541\), with changes below \(10^{-15}\) under random registry translations. By contrast, the symmetric 3R controls have translation-minimized odd power at numerical zero, whereas the asymmetric 3R control retains a smaller but finite odd component (Figure 1c). The relevant conservative property is therefore the non-removable inversion asymmetry of the lateral registry landscape, not the 2H or 3R label by itself.

This conclusion is deliberately restricted to the lateral GSFE. It does not identify registry-space inversion with experimental reversal of the out-of-plane Janus polarization. The consequence of the registry asymmetry must instead be tested directly in the prepared finite contact.

**Figure 1. Credible model input and registry-space inversion asymmetry.** (a) Unguided finite-contact and preparation contract: the center-of-mass registry is free in two dimensions, loading is along the declared \(\pm y\) axis, and the prepared state is the lowest-energy zero-force stable minimum. The schematic is illustrative rather than numerical evidence. (b) Published three-shell 2H MoSSe GSFE used as the conservative input. (c) Translation-minimized odd-RMS diagnostic for the 2H landscape and published 3R controls, together with the coordinate-independent \(A_{\min}\) and \(\chi_1\) diagnostics. Lateral registry inversion is not equated with physical Janus-polarity reversal.

### 3.2. The prepared ground-state branch exhibits direction-split unguided depinning

We next ask whether the asymmetric registry landscape produces a directional static response when the contact is prepared in a physically declared state rather than when one simply searches for the last surviving minimum anywhere in the primitive cell. The \(N=127\) contact contains two stable zero-force minima. Dense continuation follows both families separately over \(0^\circ\le\theta\le3^\circ\). At every one of the 491 continuation points, the family selected as the zero-force ground state remains lower in energy than the competing metastable family and remains stable to larger force in both loading directions (Figure 2c,d). Independent \(21\times21\) stationary-point enumerations at 16 checkpoints likewise recover two stable zero-force minima. The directional split is therefore not generated by switching to different last-surviving basins under opposite loading directions.

At the reference twist \(\theta=1.5^\circ\), the prepared ground-state branch loses stability at

\[
F_{c,+}^*=3.071135,
\qquad
F_{c,-}^*=1.258672,
\]

so that
\(\Delta F_c^*=1.812463\) and \(\rho=0.418601\) (Figure 2a,b). The competing higher-energy zero-force minimum has the opposite signed response, with thresholds \(0.211059\) and \(0.611697\). Thus directionality is not a basin-independent scalar property of the GSFE; it is a response of a specified prepared registry family under a specified loading axis. The minimum ground-to-metastable energy margin and the minimum positive- and negative-loading survival margins remain positive throughout the dense \(0^\circ\)–\(3^\circ\) continuation, closing the preparation ambiguity for the headline branch.

The stability boundary is generically fold-like, but it is not uniformly a generic saddle-node. Near
\(\theta=2.97338566^\circ\) on the \(+y\) branch, the stability loss occurs at \(F^*\approx1.91007353\) with one soft mode and a positive orthogonal curvature of approximately 6.9138, while the generic cubic condition along the soft direction fails. We therefore describe the complete curve as a depinning or stability boundary and reserve fold terminology for its generic segments. The main result is the branch-followed directional splitting itself, not a universal bifurcation classification.

**Figure 2. Prepared-state directional depinning in the unguided contact.** (a,b) Positive- and negative-\(y\) stability thresholds followed from the lowest-energy zero-force family, with the competing metastable family represented separately and the isolated higher-order event marked without treating it as a generic fold. (c) Zero-force energy margin between the prepared and competing families. (d) Positive survival margin of the prepared family under both loading directions. The threshold comparison is state- and axis-conditioned.

### 3.3. Same-spectrum controls identify registry inversion asymmetry as the directional source

The prepared-state splitting establishes the phenomenon, but it does not by itself identify which part of the GSFE causes it. We therefore alter only the inversion content of the same translation-centered 2H Fourier spectrum. In the matched symmetrized surface, the inversion-odd coefficients are removed while the even sector is retained. The resulting landscape contains an exactly degenerate inversion-related pair of minima (Figure 3a). Individual members of this pair can retain asymmetric branch-specific thresholds, but the symmetry-respecting paired/global envelope is direction degenerate: at \(\theta=1.5^\circ\),

\[
F_{c,+}^*\simeq F_{c,-}^*\simeq1.767700,
\]

with a residual split of order \(10^{-9}\) or smaller. Under the canonical zero-mean rocking protocol, the corresponding deterministic current is zero to numerical precision.

Exact spatial inversion gives the complementary test. Without changing the Fourier amplitudes or reciprocal spectrum, inversion swaps the two prepared thresholds from
\((3.071135,1.258672)\) to
\((1.258672,3.071135)\)
and reverses the canonical lattice winding from \((1,-1)\) to \((-1,1)\) (Figure 3b,c). The threshold-swap errors are below \(2\times10^{-15}\), and the original and inverted lattice currents cancel to approximately \(10^{-14}\). Representative relative-periodic closure residuals remain at their numerical floor under the transformation (Figure 3d).

These matched interventions discriminate the mechanism within the reduced model: removing the non-removable inversion-odd registry content removes the global directional response, whereas reversing that content reverses both the static and dynamical response. The inference is a same-spectrum symmetry result. Exact mathematical inversion is not, by itself, evidence that an experimental reversal of Janus polarization would implement the same transformation.

**Figure 3. Same-spectrum symmetry controls for the directional mechanism.** (a) Matched registry landscapes for the original, symmetrized, and exactly inverted Fourier surfaces shown on a common scale. (b) Static threshold contract: symmetrization removes the paired/global directional split and exact inversion swaps the two thresholds. (c) Rocking-current contract: the original and inverted landscapes carry opposite lattice winding, while the matched symmetric control carries zero current. (d) Numerical closure diagnostics for the transformed relative-periodic states.

### 3.4. Compact-contact similarity and two in-plane relaxation models preserve the directional sign

A mechanism confined to one rigid \(N=127\) geometry would have limited significance, so we next test compact-contact scaling and internal compliance. For the original ten-contact hexagonal family, characteristic angles defined by Eq. (11) obey
\(\theta_q\propto N^{-\alpha}\)
with \(\alpha=0.50357\)–0.50365 across \(q=0.80\)–0.95 and both loading directions, with \(R^2\ge0.999993\). Removing the smallest contacts drives the fitted exponent toward the geometric value \(1/2\); for \(N\ge217\), \(\alpha=0.50127\)–0.50130. We therefore interpret the fit as inverse-linear-size structure-factor scaling with finite-size corrections rather than as a new critical exponent.

The stronger test is direct collapse in \(\Theta=\theta\sqrt N\). Across the dense \(\Theta=0\)–20 grid, the larger hexagonal family remains collapsed with maximum cross-size deviations of 0.0818% for \(+y\) and 0.0800% for \(-y\). The independently constructed disk-like family is tighter still, with corresponding maxima of 0.0230% and 0.0222%. The largest difference between the hexagonal and disk family-mean normalized thresholds is approximately 0.105% at \(\Theta=20\) (Figure 4a,b). The similarity therefore survives a change of compact perimeter over the tested families, but it is not asserted for arbitrary edges.

Allowing internal in-plane relaxation changes the absolute force scale more visibly than changing the compact perimeter. At \(\theta=1.5^\circ\), the nominal linear membrane gives

\[
F_{c,+}^*=2.934302,\qquad
F_{c,-}^*=1.190210,\qquad
\rho=0.422860,
\]

compared with the rigid values \(3.071135\), \(1.258672\), and \(0.418601\). Half and twice the nominal stiffness, an independent literature-level elastic pair, and a \(100C\) rigid-limit calculation all retain \(F_{c,+}>F_{c,-}\). The nonlinear bond-angle model gives
\(F_{c,+}^*=2.935400\),
\(F_{c,-}^*=1.190479\), and
\(\rho=0.422921\)
at the same twist and nominal matched stiffness (Figure 4c,d). Its deviations from the fresh linear-membrane values are only about 0.037%, 0.023%, and 0.014% in \(F_{c,+}\), \(F_{c,-}\), and \(\rho\), respectively.

The two internal representations therefore agree that in-plane compliance renormalizes the absolute pinning scale without removing the prepared-state directional sign over the tested stiffness range. This is a model-form robustness result for in-plane relaxation, not a full three-dimensional atomistic validation.

**Figure 4. Compact-contact and in-plane robustness of the prepared directional response.** (a) Normalized threshold collapse for self-similar compact contacts under the scaled twist \(\Theta=\theta\sqrt N\). (b) Residual size and shape dependence for the tested hexagonal and disk-like families. (c) Renormalization of the force scale by in-plane compliance. (d) Directional splitting retained by the rigid, linear-FEM, and nonlinear-VFF representations at matched conditions.

### 3.5. Boundary-driven registry competition can reverse the prepared response

The compact-contact collapse does not imply that all boundary modifications are perturbative. Rotated triangular contacts introduce a qualitatively different effect: two low-energy registry families coexist and carry opposite branch-followed directional biases. For the \(20^\circ\) and \(25^\circ\) cuts, their zero-force energies cross as twist increases (Figure 5a,b). Under the fixed-twist preparation protocol, that crossing changes which family is selected as the ground state and therefore reverses the sign of the prepared response (Figure 5c).

The equilibrium crossings occur at

\[
\theta_{\rm sw}=2.92127801^\circ
\quad (20^\circ\ {\rm cut}),
\qquad
\theta_{\rm sw}=2.84723312^\circ
\quad (25^\circ\ {\rm cut}).
\]

The two registry families carry opposite splittings of approximately \(\pm0.67\) and \(\pm0.70\) near the respective crossings. This sign change is therefore a state-selection effect, not a smooth zero of a single branch. No transition path, activation barrier, continuous twist-sweep protocol, or hysteresis calculation is used to infer kinetic switching.

The location of the crossing is substantially more sensitive to the edge model than the compact-contact similarity is to size. Varying the relative local-GSFE weight of the 48 outer sites from 0.5 to 1.5 moves the \(20^\circ\) crossing over \(2.7779^\circ\)–\(3.1701^\circ\) and the \(25^\circ\) crossing over \(2.7108^\circ\)–\(3.0832^\circ\) (Figure 5d). Competing A/B registry families and their crossing persist for all tested weights, but only 3 of 5 and 4 of 5 weights, respectively, place the crossing inside the nominal \(0^\circ\)–\(3^\circ\) window. The robust reduced-model statement is therefore boundary-controlled registry competition; the numerical reversal angle is not a universal material constant.

**Figure 5. Boundary-controlled registry competition and preparation switching.** (a) Zero-force energy difference between registry families for two triangular boundary orientations. (b) The competing families carry opposite directional splitting. (c) Equilibrium selection of the lower-energy family reverses the prepared response across the registry crossing. (d) Surrogate outer-site weighting shifts the crossing substantially, demonstrating that the quantitative switch angle is edge-model sensitive.

### 3.6. Zero-mean forcing produces protocol-specific vector-locked relative-periodic states

Having established the static mechanism and its geometric limits, we test whether the same unguided landscape organizes motion under zero-mean forcing. At the canonical point
\(\theta=1.5^\circ\),
\(F_0^*=2.0\), and
\(\tau^*=40\),
the contact advances by the lattice winding \((m,n)=(1,-1)\) per cycle. Across the complete 13-by-7 sampled amplitude-period grid, all 91 points are assigned an integer winding after transients, including both pinned and transporting states (Figure 6a,b). The stricter cycle-resolved replay confirms that every one of the 40 measured cycles at every sampled point repeats the same integer pair; the largest single-cycle lattice-rounding residual is approximately \(9.55\times10^{-10}\). A \(\tau^*=40\) slice resolves a staircase of finite-width winding states rather than a single transport mode (Figure 6c).

Representative plateaus satisfy stronger dynamical tests. For the canonical \((1,-1)\) state, one-period relative-lattice closure is of order \(2\times10^{-11}\), and independent DOP853 and Radau monodromy integrations give a leading Floquet spectral radius
\(\rho_F\approx6.31\times10^{-22}\) (Figure 6d). The extreme magnitude is used only as evidence of strong numerical contraction. Five additional representative plateaus, spanning pinned, low-winding, and higher-winding states, also satisfy \(\rho_F<1\) under the cross-solver test. Across the six representative states, 24 of 24 time-step checks retain the expected winding and 162 of 162 local position/velocity perturbations return to that winding. These tests establish local attraction for representative states; they do not certify every sampled state by Floquet analysis or prove global attractor uniqueness.

The map is also not a material-only phase diagram. A 72-point joint damping-drive audit over
\(\gamma^*=2,3,4,5,6,8\),
four amplitudes, and three periods shows that damping can reorganize the winding structure: only 1 of 12 sampled drive points preserves the \(\gamma^*=4\) winding across all tested damping values, and as many as five distinct winding pairs occur at one fixed drive point. The 91-point map should therefore be read as a reproducible property of the declared \(m^*=1,\gamma^*=4\) protocol.

**Figure 6. Deterministic vector mode locking under zero-mean forcing.** (a,b) Integer winding components \(m\) and \(n\) across the 91-point amplitude-period grid; pinned states are marked directly and the two winding components use ordered discrete scales. (c) Vector staircase along the \(\tau^*=40\) slice. (d) Cross-solver Floquet and relative-periodic consistency diagnostics for representative attracting states. The map is conditional on the declared reduced mass and damping.

### 3.7. Thermal noise destroys exact winding identity before erasing the stationary mean current

Thermal noise separates exact mode identity from directed transport. After 60 burn cycles and over 100 measured cycles, the full \(T^*=0.02\)–0.70 series uses 500 independent trajectories per temperature, while the high-temperature band is independently replicated and pooled to \(N=1000\). The probability that a noisy cycle remains in the deterministic target winding \((1,-1)\) is already small at nonzero temperature and is only about 0.011–0.016 across the pooled high-temperature band. In contrast, the mean lattice current decays continuously but remains directed (Figure 7a,b). Exact cycle identity is therefore a much more fragile observable than the stationary mean displacement per cycle.

The distinction remains statistically resolved at the largest sampled temperature. At \(T^*=0.70\), the pooled stationary estimate is

\[
(\langle u\rangle,\langle v\rangle)
=
(0.036998,-0.076448).
\]

A 50,000-resample trajectory bootstrap gives
\(u\in[0.01265,0.06132]\) and
\(v\in[-0.10088,-0.05195]\).
The corresponding zero-current Mahalanobis statistic is 38.07, compared with a 95% threshold of 6.04, so the zero vector is excluded. The same joint test excludes zero at every sampled high-temperature point from \(T^*=0.50\) through 0.70 (Figure 7c). Because trajectories, rather than cycles, are the resampling units, these intervals do not rely on cycle-level pseudoreplication.

A separate sample-count audit supports the pooled design. At least 95% of without-replacement subsamples reproduce the zero-vector rejection decision by
\(N=100,200,200,300,\) and \(500\)
for \(T^*=0.50,0.55,0.60,0.65,\) and \(0.70\), respectively. Thus the pooled \(N=1000\) high-temperature analysis is conservative relative to the observed decision-stability thresholds and is not a post hoc redefinition of the significance boundary.

The cycle-sign statistic provides a weaker but complementary view of the same hierarchy. The negative-\(v\) fraction decreases toward one-half from
\(0.51933\,[0.51632,0.52237]\) at \(T^*=0.50\)
to
\(0.50802\,[0.50506,0.51100]\) at \(T^*=0.70\),
while the target-winding probability at \(0.70\) is only about 0.011 (Figure 7d). Targeted \(dt=0.04,0.02,\) and \(0.01\) reruns at \(T^*=0.60,0.65,\) and 0.70 differ by no more than 1.12 combined standard errors in either current component. The validated conclusion is therefore finite and observable specific: exact winding identity is strongly mixed, but a weaker stationary directed mean current remains statistically nonzero through the largest sampled \(T^*=0.70\). No thermal critical temperature or behavior beyond the sampled range is inferred.

**Figure 7. Thermal hierarchy of mode identity and stationary directed current.** (a) Temperature evolution of the stationary mean lattice displacement per cycle. (b) Dedicated high-\(T^*\) view of trajectory-level 95% intervals for the two mean-current components. (c) Joint zero-current exclusion statistic relative to its 95% threshold. (d) Negative-\(v\) cycle probability compared with the probability of the exact deterministic target winding. Insets are avoided so that uncertainty, statistical exclusion, and mode-identity degradation remain separate visual jobs.


## 4. Discussion

### 4.1. A prepared-state finite-contact mechanism for directional depinning

The combined evidence supports a specific reduced-model mechanism rather than a generic association between the Janus label and directional friction. The published 2H MoSSe GSFE contains a translation-independent inversion-odd registry component; a finite contact averages that landscape through a twist-dependent structure factor; and state preparation selects one of the stable registry families before loading. For the lowest-energy zero-force family, the resulting full two-dimensional stability boundary is strongly split under the declared \(\pm y\) loading. Removing the inversion-odd content from the same Fourier spectrum removes the paired/global directional bias and deterministic current, whereas exact inversion swaps the thresholds and reverses the current. Taken together, the translation-minimized asymmetry test, prepared-branch continuation, and same-spectrum interventions support registry inversion asymmetry as the controlling conservative source of the directional response **within this finite-contact model**.

This mechanism is narrower than the statement that MoSSe has an “intrinsic friction diode.” The competing metastable minimum at \(\theta=1.5^\circ\) carries the opposite signed threshold split, so the response is explicitly preparation conditioned. The force-direction dependence is likewise anisotropic rather than a rotationally invariant friction scalar, and the deterministic winding pattern changes when the damping protocol is changed. Here “unguided” means that no transverse confining potential is required to obtain the effect in the baseline model; it does not mean state independent, axis independent, damping independent, or independent of the manner in which mechanical load is applied.

The in-plane relaxation hierarchy clarifies another aspect of this scope. Absolute rigid-contact thresholds are not material constants: nominal membrane compliance lowers both depinning forces, and the change becomes more important as twist increases. At the same time, the normalized directional split and its sign remain close to the rigid result over the tested stiffness bracket and agree closely between the linear membrane and independently reconstructed nonlinear bond-angle model. The present mechanism is therefore not eliminated by the tested in-plane compliance, but the calculation does not establish invariance to collective out-of-plane relaxation or atomistic edge reconstruction.

### 4.2. Compact similarity and boundary-state selection are distinct geometry regimes

The geometry results separate naturally into two regimes. Within self-similar compact contacts, twist mainly controls the phase accumulated across the contact, giving the geometric variable \(\Theta=\theta\sqrt N\). The direct collapse across larger hexagonal contacts and an independent disk-like family is stronger evidence for this interpretation than the fitted exponent alone. The approach of \(\alpha\) toward \(1/2\) as the smallest contacts are removed is consistent with inverse-linear-size structure-factor scaling with finite-size corrections. This result should not be described as a new universal exponent, nor should the approximately 0.1% agreement of the tested compact families be extrapolated to arbitrary boundaries.

Rotated triangular boundaries access a different mechanism. Rather than perturbing one compact-family threshold surface, they bring two stable registry families with opposite directional biases into competition. The equilibrium crossing between their zero-force energies changes the prepared state and can reverse the measured branch-followed response. The outer-site weighting audit then shows exactly which part of this statement is robust: the competing-family structure and energy crossing persist, but the numerical switching angle moves enough that it can leave a chosen \(0^\circ\)–\(3^\circ\) observation window. Compact \(\Theta\)-similarity and boundary-induced state selection are therefore complementary rather than contradictory results.

This distinction also limits the design implication. The model suggests that boundary engineering can control which registry family is prepared and hence the sign of the reduced-model rectification. It does not predict a universal reversal angle for a fabricated flake. A quantitative boundary design rule would require a realistic description of reconstructed edges, edge chemistry, nonlocal edge energetics, and possibly collective corrugation, followed by a preparation protocol that connects those energetics to an experimentally accessible state.

### 4.3. Static rectification, deterministic winding, and thermal current share a symmetry source but are not the same observable

The same-spectrum controls connect static directionality and dynamical current to a common symmetry source, but they do not make the two observables interchangeable. The static calculation identifies where one prepared minimum loses stability under constant loading. The rocking calculation instead selects relative-periodic attractors of a driven dissipative system. Consequently, the inequality \(F_{c,+}\ne F_{c,-}\) cannot by itself determine a winding pair or a complete amplitude-period phase diagram.

The deterministic calculations show that the declared \(m^*=1,\gamma^*=4\) protocol supports a broad sampled family of integer vector windings, and the representative Floquet calculations demonstrate local attraction rather than merely integer-valued finite-time averages. The joint damping-drive audit is equally important because it supplies the negative result needed to interpret the map correctly: damping can reorganize the winding structure substantially. The material-anchored GSFE supplies the conservative landscape, but the realized transport state depends on dissipation and forcing parameters that are not contained in that GSFE.

Thermal noise separates the hierarchy further. Exact target-winding identity is rapidly mixed, yet the mean two-component displacement per cycle remains statistically separated from zero through \(T^*=0.70\). The cycle-sign probability approaches one-half while retaining a small resolved bias, showing how a weak directed current can survive even when individual cycles are nearly balanced between signs and rarely reproduce the deterministic \((1,-1)\) mode. The sample-count convergence and time-step checks strengthen this finite-range statistical statement, but they do not define a thermal phase transition. In particular, significance at a finite trajectory count must not be converted into a critical temperature, and the reduced \(T^*\) scale cannot be expressed in kelvin without an independent physical calibration.

### 4.4. What is established about MoSSe—and what remains unresolved

The material-specific part of the argument is the published lateral GSFE and the symmetry information it contains. Translation-minimized optimization and the reciprocal-triad diagnostic independently show that the 2H MoSSe landscape used here has non-removable registry inversion asymmetry. Same-spectrum symmetrization and exact inversion then satisfy the expected static and dynamical contracts to numerical precision. This is stronger internal discrimination than comparing only different chemical stackings because the Fourier spectrum is held fixed while its inversion content is changed.

A physical Janus-polarity law, however, is not established. The model does not contain paired first-principles GSFE surfaces for experimentally reversed polarization states, and a physical operation that reverses \(P_z\) could alter several Fourier amplitudes and phases rather than implement exact spatial inversion. The mathematical transformation \(U(\mathbf r)\rightarrow U(-\mathbf r)\) is therefore a symmetry control, not a demonstrated experimental polarity switch. Establishing a quantitative \(P_z\)-to-rectification relation requires polarity-resolved first-principles or atomistic input.

The source-input uncertainty has a similarly explicit boundary. The published GSFE coefficients are available at finite decimal precision, but an underlying fit covariance and machine-readable raw \(9\times9\) energy grid were not available in the accessed source materials. Perturbing the coefficients over their printed-resolution intervals preserves the static sign, the normalized splitting, and the canonical winding; this demonstrates insensitivity to tabulation precision, not a statistical uncertainty distribution for the DFT fit.

Finally, the present mechanical hierarchy remains incomplete. The source GSFE includes local interlayer-separation relaxation at each aligned registry, and the current work adds rigid, linear in-plane, and nonlinear in-plane finite-contact models. It does not include collective out-of-plane buckling/corrugation, reconstructed atomistic edges, defects, load-dependent stacking energetics, or a validated Janus-specific full three-dimensional interatomic potential. Nor does the GSFE determine the physical mass, damping, applied-force scale, laboratory preparation procedure, or mapping from reduced time and temperature to hertz and kelvin. These missing inputs define the next validation layer rather than weaknesses that can be filled by additional prose.

## 5. Conclusions

A finite two-dimensional contact constructed from the published 2H Janus MoSSe GSFE exhibits a strong prepared-state directional stability split in the unguided reduced model. For the \(N=127\) reference contact at \(\theta=1.5^\circ\), the lowest-energy zero-force branch depins at \(F_{c,+}^*=3.071135\) and \(F_{c,-}^*=1.258672\). Dense continuation shows that this branch remains the zero-force ground family and the longer-lived pinned family in both loading directions over the tested \(0^\circ\)–\(3^\circ\) interval, while an isolated higher-order stability degeneracy limits generic fold terminology.

The mechanism is identified by symmetry rather than by the Janus label alone. Registry-origin minimization shows non-removable inversion-odd content in the published lateral landscape; matched same-spectrum symmetrization removes the paired/global directional response, and exact spatial inversion swaps the static thresholds and reverses the lattice current. For compact rigid contacts, the thresholds follow \(\theta\sqrt N\) similarity across tested hexagonal and disk-like families. In-plane compliance changes the absolute force scale but preserves the directional sign in both linear-FEM and nonlinear-VFF representations. By contrast, rotated triangular boundaries can change which registry family is prepared, producing an edge-sensitive equilibrium sign reversal.

Under the declared \(m^*=1,\gamma^*=4\) zero-mean rocking protocol, all 91 sampled amplitude-period points repeat an integer lattice winding cycle by cycle after transients, and representative plateaus satisfy relative-periodic closure and cross-solver Floquet attraction. The winding map is nevertheless protocol specific: a joint damping-drive audit shows that changing damping can reorganize the selected lattice vector. Thermal noise then destroys exact deterministic winding identity much more rapidly than it removes directed transport. After stationarity, independent-seed, trajectory-level inference, sample-count convergence, and time-step checks, the stationary mean current remains statistically nonzero through the largest sampled \(T^*=0.70\), while the exact \((1,-1)\) cycle probability is near 1% in the high-temperature band.

These results support a bounded combination claim: a DFT-anchored lateral-registry asymmetry can generate prepared-state unguided rectification and protocol-specific vector transport in a finite MoSSe contact, while compact scaling, boundary-state selection, thermal mode mixing, and in-plane compliance define distinct limits of that response. They do not establish a universal friction coefficient, a physical polarization-reversal law, full three-dimensional atomistic validation, a Kelvin-scale thermal boundary, or a material-only nonlinear phase diagram.
