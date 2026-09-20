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
