from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
import pandas as pd
import os, shutil

MAIN_IN='/mnt/data/janus_n8_gate/workflow/Janus_MoSSe_WorkflowValidated_Draft.docx'
SI_IN='/mnt/data/janus_n8_gate/workflow/Janus_MoSSe_WorkflowValidated_SI_Draft.docx'
OUTDIR='/mnt/data/janus_n10_rewrite'
MAIN_OUT=f'{OUTDIR}/Janus_MoSSe_ClaimFrozen_Manuscript_v1.docx'
SI_OUT=f'{OUTDIR}/Janus_MoSSe_ClaimFrozen_SI_v1.docx'
FIG6=f'{OUTDIR}/Figure_6_thermal_vector_hierarchy.png'

os.makedirs(OUTDIR, exist_ok=True)


def replace_para(p, text):
    # Preserve paragraph properties/style; replace run content only.
    for r in list(p.runs):
        p._p.remove(r._r)
    run=p.add_run(text)
    return run


def set_cell(cell, text, font_size=None, bold=False, center_short=False):
    cell.text = str(text)
    for p in cell.paragraphs:
        p.paragraph_format.space_after = Pt(0)
        if center_short:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = bold
            if font_size:
                r.font.size = Pt(font_size)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def insert_paragraph_after_table(doc, table, text):
    p=doc.add_paragraph(text)
    table._tbl.addnext(p._p)
    return p


def insert_table_after_paragraph(doc, paragraph, rows, cols, style='Table Grid'):
    tbl=doc.add_table(rows=rows, cols=cols)
    if style:
        tbl.style=style
    paragraph._p.addnext(tbl._tbl)
    return tbl


def format_table(tbl, font_size=8.5):
    for ri,row in enumerate(tbl.rows):
        for cell in row.cells:
            cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for p in cell.paragraphs:
                p.paragraph_format.space_after=Pt(0)
                if ri==0:
                    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.size=Pt(font_size)
                    if ri==0:
                        r.bold=True

# -------- MAIN --------
doc=Document(MAIN_IN)
P=doc.paragraphs

replace_para(P[1], 'A DFT-anchored finite-contact model with prepared-state, symmetry, statistical, and in-plane relaxation falsification tests')

replace_para(P[3], (
"Twist suppresses interfacial corrugation in many incommensurate two-dimensional contacts, but a laterally inversion-asymmetric registry landscape can make finite-contact pinning direction dependent. We analyze the corrected published three-shell generalized stacking-fault-energy (GSFE) landscape of 2H Janus MoSSe using an unguided finite contact whose center of mass is free in the full two-dimensional registry plane. Headline depinning thresholds are followed from the lowest-energy zero-force minimum; a 491-point dense/adaptive continuation over theta=0-3 deg, supplemented by independent stationary-point enumerations, finds no prepared-state branch exchange. For the N=127 reference contact at theta=1.5 deg, the rigid prepared branch loses metastability at F_c,+*=3.071135 and F_c,-*=1.258672. Same-spectrum controls isolate the symmetry origin: matched symmetrization gives a direction-degenerate global envelope and zero deterministic current, whereas exact spatial inversion swaps the thresholds and reverses the vector current to numerical precision. Compact hexagonal and disk-like contacts collapse under the similarity coordinate theta sqrt(N), with characteristic-angle exponents near 0.5036 converging toward the inverse-linear-size value 1/2 as the smallest contacts are removed. Rotated triangular boundaries instead produce competition between registry minima, so a ground-state switch can reverse the prepared directional bias while its exact twist remains edge-model dependent. Under zero-mean forcing, all 91 sampled amplitude-period points repeat a single integer winding cycle-by-cycle after transients; the canonical (1,-1) state and representative additional plateaus are attracting relative-periodic orbits under cross-solver Floquet tests. Thermal noise rapidly mixes exact winding identity: the lattice-v component remains resolved through T*=0.60, while a joint two-component bootstrap still excludes the zero-current vector at T*=0.65 but not at 0.70. Linear finite-element and independently reconstructed nonlinear bond-angle models soften the absolute thresholds but preserve the directional split. The result is therefore a DFT-anchored reduced-model mechanism with explicit preparation, symmetry, statistical, and in-plane robustness tests, not a fully three-dimensional atomistic or physically calibrated device prediction."
))

replace_para(P[6], (
"Twisted van der Waals interfaces are a canonical setting for structural lubricity because registry forces from different parts of a finite contact partially cancel as the local phase winds across the interface [1-4]. Finite size, contact shape, boundaries, and elastic relaxation nevertheless remain active variables and can alter both the magnitude and topology of the effective sliding landscape [5-8]. Once the local registry energy lacks inversion symmetry, the same finite-contact interference that suppresses corrugation can therefore act differently under opposite loading directions."
))
replace_para(P[7], (
"Janus transition-metal dichalcogenides provide a natural materials setting for testing this possibility. Replacing the two chalcogen planes by different species produces an out-of-plane polar monolayer and modifies stacking-dependent interlayer energetics [9-11,14]. Out-of-plane polarity and lateral registry-space inversion, however, are distinct symmetry statements. A defensible mechanical-rectification mechanism must begin from the actual lateral energy landscape rather than assuming that the Janus label alone implies a friction diode. The corrected three-shell GSFE reported for bilayer Janus MoSSe by Angeli, Schleder, and Kaxiras [12,13] supplies a material-anchored conservative input for such a test."
))
replace_para(P[8], (
"Directional friction and friction-diode behavior have already been demonstrated in two-dimensional interfaces [15], and unbiased rocking, current reversal, and phase locking are established nonlinear-transport phenomena [19,20]. First-principles-informed stochastic friction models likewise show why a static energy surface and a dynamical friction observable should not be conflated [16]. The contribution sought here is therefore narrower than a generic 'first friction diode' or 'first ratchet' claim: we ask whether the corrected MoSSe GSFE supports a branch-resolved, full-2D prepared-state stability asymmetry, whether that asymmetry survives matched same-spectrum falsification and finite-contact robustness tests, and whether the same landscape supports lattice-vector relative-periodic transport under zero-mean forcing."
))
replace_para(P[9], (
"We separate material symmetry, state preparation, geometry, nonlinear dynamics, stochastic transport, and internal compliance. A translation-minimized diagnostic first tests whether the published GSFE has nonremovable registry inversion asymmetry; registry-origin shifts are then used as a falsification test for coordinate-dependent odd-sector interpretations. Headline static thresholds follow the lowest-energy zero-force minimum under quasi-static positive- and negative-y loading, with competing metastable branches continued separately. Finite-size calculations are extended across compact hexagonal and disk-like families, while rotated triangular boundaries are treated as a competing-registry problem. Deterministic transport is mapped over drive amplitude and period, representative plateaus are tested as attracting relative-periodic orbits, thermal transport is inferred from trajectory-level statistics, and in-plane model-form dependence is tested with both a linear finite-element membrane and a nonlinear bond-angle network. Transverse confinement is retained only as a secondary pathway-control comparison."
))

replace_para(P[19], (
"Separating a Fourier series into cosine and sine coefficients at one chosen registry origin does not by itself define a material observable, because those coefficients mix under translation. We therefore translate the origin by a and minimize the total squared inversion-odd coefficient over the primitive cell, using a 181 x 181 registry grid followed by multiple independent local refinements. If c_alpha(a) and s_alpha(a) are the translated even and odd coefficients, Eq. (4) defines A_odd(a) and A_min=min_a A_odd(a); the reported odd RMS fraction is sqrt(A_min). As an independent phase diagnostic, we use the normalized complex-amplitude triad invariant chi_1=Im[(C_1 C_2 C_3)/|C_1 C_2 C_3|] for the first reciprocal shell. Because G_1+G_2+G_3=0, the triad product is translation invariant; in the equal-phase representation used for the published coefficients it reduces to sin(3 phi_1). Registry-origin shifts are also used as a falsification test: physical thresholds must remain invariant even though an origin-fixed cosine/sine decomposition need not."
))
replace_para(P[20], (
"Two matched controls are constructed from the same translation-centered 2H Fourier spectrum. In the matched symmetrized surface the centered odd coefficients are set to zero; in the exact-inversion surface those odd coefficients change sign. The symmetrized landscape contains an inversion-paired pair of degenerate minima, so branch-specific thresholds need not be individually direction-degenerate; symmetry requires the paired/global envelope to be degenerate. Exact inversion imposes the stronger contracts F_c,+[U_inv]=F_c,-[U], F_c,-[U_inv]=F_c,+[U], and reversal of the lattice-vector current. A centered homotopy U_eta=U_even+eta U_odd is retained only as an SI mechanism-isolation diagnostic. No derivative with respect to eta, intermediate eta optimum, or mapping between eta and physical polarization is interpreted as a material law."
))
replace_para(P[23], (
"Pinned states are full two-dimensional local minima satisfying grad U_N=(0,F_y) with a positive-definite Hessian H. The operational threshold used for all headline claims is branch-followed: at F_y=0 the lowest-energy minimum is identified, and that same minimum is continued quasi-statically under positive or negative force until its stability is lost. Representative 21 x 21 registry-seed enumerations find six stationary points and two stable minima per primitive cell. After an initial 0.25-deg survey, both zero-force minima and their positive/negative loading thresholds were tracked on a 491-point dense/adaptive theta grid from 0 to 3 deg, with 16 independent 21 x 21 stationary-point checkpoints concentrated near the isolated high-order boundary point. Throughout that numerically resolved interval the prepared ground-state family remains lower in zero-force energy and longer lived under both loading directions. This is a numerical interval verification, not an interval-arithmetic proof over every real theta. The older last-stable-minimum-anywhere quantity is retained only as a diagnostic envelope."
))
replace_para(P[26], (
"The inverse-linear-size test uses ten compact hexagonal contacts N=37, 61, 91, 127, 169, 217, 271, 331, 397 and 469. Characteristic angles are obtained by directly solving F_c(theta_q)=q F_c(0) for q=0.95, 0.90, 0.85 and 0.80 rather than by interpolation. A separate shape/size robustness calculation extends the compact hexagonal family to N=127, 217, 331, 469, 631, 817, 1027 and 1261 and adds disk-like compact contacts N=127, 241, 367, 517, 721 and 931. The extended families are evaluated on a dense scaled-twist grid Theta=theta sqrt(N)=0,1,...,20 deg. Boundary sensitivity is treated separately with fixed-N=127 triangular contacts. For the 20 and 25 deg cuts, both low-energy registry-minimum families are continued and the zero-force ground state is selected before loading. Their zero-force energy crossing defines a prepared-state registry switch. As a sensitivity analysis rather than a microscopic edge model, the 48 outer sites are assigned relative local-GSFE weights from 0.5 to 1.5 while interior sites retain unit weight."
))
replace_para(P[30], (
"The nominal monolayer constants are a=3.25 A, C11=119.3 N/m and C12=27.5 N/m from first-principles calculations for Janus MoSSe [17], giving C66=(C11-C12)/2=45.9 N/m. We test C/2, 2C, an independent literature-level elastic pair (C11=126.8 N/m, C12=27.4 N/m), and a 100C rigid-limit check. Tier 1.5 replaces the linear constitutive discretization by a geometrically nonlinear triangular-site valence-force model containing 342 nearest-neighbor bond-stretching terms and 648 local 60-deg angle terms. Its documented coefficients, k_s=5.289992 eV/A^2 and k_theta=2.334491 eV/rad^2 at nominal stiffness, were independently reconstructed and verified to reproduce C11=119.3 N/m, C12=27.5 N/m and C66=45.9 N/m before the N=127 branches were recomputed. The same rigid modes are projected out. These tests address collective in-plane compliance only; they do not add out-of-plane buckling, atomistic edge reconstruction, or nonlocal edge chemistry."
))
replace_para(P[33], (
"with m*=1 and gamma*=4. The canonical operating point theta=1.5 deg, F0*=2.0 and tau*=40 is supplemented by a 13 x 7 amplitude-period grid: F0*=1.0-4.0 in steps of 0.25 and tau*=20, 30, 40, 50, 60, 70 and 80. Each grid point uses 20 transient and 40 measured cycles with 4000 steps per cycle. The original finite-run classification requires the mean lattice displacement per cycle to lie within 1e-4 of an integer pair (m,n). A stricter cycle-resolved rerun then checks whether every measured cycle repeats the same integer winding. Representative plateaus spanning pinned, low-winding, and high-winding states are tested more strongly by one-period relative-lattice closure, cross-solver Floquet multipliers, time-step refinement, increasing/decreasing amplitude continuation, and position/velocity basin perturbations."
))
replace_para(P[34], (
"For the canonical (1,-1) orbit, the monodromy matrix is integrated independently with DOP853 at two tolerance levels and with Radau. The three calculations agree on the leading Floquet spectral radius at approximately 6.31e-22 and give one-cycle state closures of order 1e-11. The same cross-solver criterion rho_F<1 is applied to selected additional plateaus, including (0,0), (1,-2), (2,-3), (3,-4), and a high-winding (2,-7) state. The extreme numerical magnitude of any individual multiplier is used only as evidence of strong contraction, not as a separately measurable physical quantity."
))
replace_para(P[37], (
"integrated with BAOAB. For the unguided system a scalar half-cycle label is insufficient because trajectories move across both lattice directions. The primary thermal audit uses 1000 independent trajectories per temperature, dt=0.02, 10 burn cycles and 10 measured cycles. All cycle data from a trajectory are first reduced to trajectory-level observables; bootstrap resampling is then performed over trajectories, preventing cycle-level pseudoreplication. Pointwise component intervals use 10,000 cluster-bootstrap resamples, while P(Delta y<0) is checked with 100,000 resamples near its high-temperature boundary. Because the deterministic state is a two-component lattice current, the high-temperature audit also bootstraps the mean vector (u,v) jointly: a two-component 95% region and simultaneous component intervals test whether the zero-current vector is excluded at T*=0.60, 0.65 and 0.70. We separately report mean u and v, continuous mean Delta y, P(Delta y<0), and the probability that a cycle is assigned to the deterministic target (m,n)=(1,-1). Targeted dt=0.04, 0.02 and 0.01 simulations are used as low-noise discretization checks."
))
replace_para(P[42], (
"The published-GSFE engine, analytic gradient and Hessian, and canonical unguided release were regenerated from clean directories and checked against independent reference implementations. The final evidence package includes dense prepared-branch continuation; same-2H symmetrization and exact-inversion contracts; registry-origin and odd-sector gauge audits; exact characteristic-angle and dense hexagonal/disk scaling; competing-registry boundary and edge-weight analyses; cycle-resolved 91-point vector locking; multi-plateau Floquet, time-step, basin and amplitude-continuation checks; trajectory-level thermal raw data with component and joint-vector bootstraps; fresh linear-elastic continuation; and the independently reconstructed nonlinear bond-angle source and outputs. Scripts, raw/summary CSV and JSON files, environment information, Gate reports, and manuscript/Supplementary Information sources are retained with the submission materials."
))

replace_para(P[47], (
"The translation-minimized search gives A_min=0.0425361 for the asymmetric 2H MoSSe landscape, corresponding to an odd RMS fraction 0.206243. A 181 x 181 grid plus independent local refinements converges to the same minimum with a multistart spread below 8.4e-17. The first-shell complex-amplitude triad invariant is chi_1=0.583541 and remains unchanged under random registry translations to about 1e-15. Two symmetric 3R controls have minimized odd-power fractions at numerical zero, while an asymmetric 3R configuration retains a smaller finite odd RMS fraction 0.01745. Registry-space inversion asymmetry, rather than the label 2H or 3R by itself, is therefore the relevant conservative property. A separate 26-origin falsification leaves the physical theta=1.5 deg threshold split invariant to below 1e-14 but changes the eta=0 reference topology and the small-eta response. We therefore reject arbitrary-origin d(Delta F_c)/d eta and any intermediate eta optimum as material observables; the only retained eta path is an A_min-centered computational homotopy in the SI."
))
replace_para(P[54], (
"The full-2D directional split survives the stricter prepared-state definition. The N=127 primitive cell contains two stable zero-force minima. On the 491-point dense/adaptive theta grid from 0 to 3 deg, the energy margin U_meta-U_ground, the positive-loading lifetime margin F_c,+^ground-F_c,+^meta, and the negative-loading lifetime margin F_c,-^ground-F_c,-^meta remain positive at every point. Their minimum values occur at the high-twist end and remain 0.17313, 1.70275 and 0.26086, respectively. Sixteen independent 21 x 21 stationary-point checkpoints also recover exactly two stable zero-force minima. At theta=1.5 deg the ground-state thresholds are F_c,+*=3.071135 and F_c,-*=1.258672, whereas the higher-energy minimum loses stability at 0.211059 and 0.611697. The headline split is therefore not produced by selecting different last-surviving metastable basins in the two directions."
))
replace_para(P[60], (
"The original ten-contact hexagonal calculation gives characteristic-angle fits theta_q proportional to N^-alpha with alpha=0.50357-0.50365 across q=0.80-0.95 and both loading directions, with R^2 at least 0.999993. Removing the smallest contacts drives the fitted exponent monotonically toward 1/2; for N>=217 the corresponding range is 0.50127-0.50130. The result is therefore interpreted as inverse-linear-size structure-factor scaling with finite-size corrections, not as a new universal exponent. The extended audit strengthens that interpretation: compact hexagons N=127-1261 and disk-like contacts N=127-931 were evaluated on every integer Theta from 0 to 20 deg. At Theta=20 the maximum cross-size deviations are 0.0818% (+y) and 0.0800% (-y) for hexagons and 0.0230% and 0.0222% for disks; no larger hidden deviation appears at intermediate Theta."
))
replace_para(P[61], (
"The two compact-shape families nearly coincide as well. Across the dense Theta=0-20 grid, the largest difference between their family-mean normalized thresholds occurs at Theta=20 and is 0.1048% for +y and 0.1022% for -y, while the normalized splitting differs by only about 2.5e-5 in absolute terms. High-Theta spot checks for the smallest contacts also confirm that the reported thresholds remain prepared-ground-state stability losses even when theta exceeds the original 0-3 deg N=127 audit window. Thus theta sqrt(N) is a robust similarity coordinate for the tested compact rigid families, not a claim for arbitrary edges, reconstructed boundaries, or deformable flakes."
))
replace_para(P[65], (
"The linear membrane extension changes the absolute pinning scale but does not remove the headline directional split. A fresh nominal-stiffness rerun at theta=1.5 deg gives F_c,+*=2.934302 and F_c,-*=1.190210, corresponding to rho=0.422860. Relative to the rigid values, the thresholds decrease by about 4.46% and 5.44%, while rho changes by about 1%. The maximum principal strains at the last stable states are 0.328% and 0.459%, with nodal displacements below 0.06 A. The C/2 bracket gives 2.807397 and 1.135229 with rho=0.424125; 2C gives 3.001636 and 1.222534 with rho=0.421172. An independent elastic-constant pair gives 2.944409 and 1.194897, and a 100C calculation recovers the rigid thresholds within about 0.06%."
))
replace_para(P[66], (
"The nonlinear discrete model provides a distinct constitutive/discretization check while sharing the same GSFE and target elastic constants. Reconstructing the documented 342-bond/648-angle model independently yields C11=119.299994 N/m, C12=27.500000 N/m and C66=45.899997 N/m under homogeneous-strain tests. At theta=1.5 deg the reconstructed model gives F_c,+*=2.935400 and F_c,-*=1.190479 with rho=0.422921, differing from the fresh linear membrane by only about 0.037%, 0.023% and 0.014% in F_c,+, F_c,- and rho. The largest bond strain and local angle change at the last stable states remain below 0.40% and 0.40 deg. At theta=3 deg the nonlinear model gives 1.574365 and 0.631006 with rho=0.427755, again close to the linear-membrane result while retaining the directional sign. The in-plane robustness result is therefore not a linear-FEM discretization artifact, but it is still not a collective three-dimensional atomistic relaxation."
))
replace_para(P[69], (
"The switch position is not a universal material constant. In the boundary-weight sensitivity test, changing the relative local-GSFE weight of the 48 outer sites from 0.5 to 1.5 moves the 20 deg crossing from 3.1701 to 2.7779 deg and the 25 deg crossing from 3.0832 to 2.7108 deg. In all ten tested weight/cut combinations the A/B energy crossing persists and the two registry families carry opposite directional biases, but the crossing does not lie inside the nominal 0-3 deg window for every weight. The robust reduced-model statement is therefore the competing-registry mechanism and sign exchange, not a universal reversal angle or a guarantee that a chosen finite twist window contains the switch. Relaxed or reconstructed edges require new atomistic or elastic input."
))
replace_para(P[73], (
"At theta=1.5 deg, zero-mean longitudinal forcing produces genuinely two-dimensional lattice transport without a guide. The canonical point F0*=2.0, tau*=40 advances by (m,n)=(1,-1) per cycle. More broadly, all 91 sampled combinations in the F0*=1.0-4.0 and tau*=20-80 grid reproduce integer lattice transport. The stricter cycle-resolved rerun shows that, after transients, every one of the 40 measured cycles at every sampled point repeats the same winding pair; the largest single-cycle lattice-lock residual is below 1e-9. A denser tau*=40 amplitude scan resolves finite-width plateaus including (0,0), (1,-1), (1,-2), (2,-3), (3,-4) and higher windings. This establishes broad sampled vector locking without implying that every point in continuous parameter space is locked or that each sampled attractor is unique."
))
replace_para(P[74], (
"The canonical (1,-1) plateau satisfies the stronger relative-periodic-orbit tests. Its one-cycle closure is of order 1e-11, and independent DOP853 and Radau integrations give rho_F approximately 6.31e-22. Five additional plateaus spanning (0,0), (1,-2), (2,-3), (3,-4) and (2,-7) also have rho_F<1 under the same cross-solver test. Across these six representative states, 24/24 time-step checks preserve the expected winding and 162/162 local position/velocity perturbations return to the same winding. Increasing and decreasing amplitude continuation at tau*=40 agree at all 61 sampled amplitudes. We interpret these results as attraction and local basin robustness of representative relative-periodic states, not as a proof of global attractor uniqueness or a complete continuous phase diagram."
))
replace_para(P[79], (
"Thermal robustness is quantified from 1000 independent trajectories per temperature, with the trajectory rather than the individual cycle used as the inference unit. Exact deterministic winding identity is fragile: over the sampled nonzero temperatures T*=0.02-0.70, the cycle-level probability assigned to the target (1,-1) cell remains below 0.081. This does not imply loss of directed transport, because noisy cycles can occupy neighboring lattice-vector channels while retaining a nonzero mean vector current."
))
replace_para(P[80], (
"The hierarchy of observables is explicit. The mean lattice-v translation remains below zero through T*=0.60, where its 95% pointwise cluster-bootstrap interval is [-0.1550,-0.0157], but its interval includes zero at T*=0.65. The second current component remains positive enough that the full two-component mean vector is still statistically separated from zero at T*=0.65: a 100,000-resample joint bootstrap gives mean (u,v)=(0.0950,-0.0652), and the zero vector lies outside the 95% joint region; simultaneous component intervals are u in [0.0091,0.1810] and v in [-0.1480,0.0177]. At T*=0.70 the joint test no longer excludes zero. The cycle-sign statistic is less robust: P(Delta y<0) is clearly above 0.5 through T*=0.50, is marginal at T*=0.55, and is unresolved by T*=0.60. These are observable-specific finite-sample boundaries, not a sharp thermal critical temperature."
))
replace_para(P[83], (
"Figure 6. Thermal hierarchy from trajectory-level inference. (a) Mean lattice-coordinate currents <u> and <v> with pointwise 95% trajectory-cluster bootstrap intervals. (b) Joint two-component zero-current test at high temperature; values above unity exclude the zero vector from the 95% bootstrap region, which remains true at T*=0.65 but not at 0.70. (c) P(Delta y<0) decays toward 0.5 while the exact deterministic target-winding probability remains small, demonstrating that exact mode identity is more fragile than directed vector transport."
))
replace_para(P[88], (
"The principal result is branch-resolved as well as fully two-dimensional. The corrected published MoSSe GSFE and finite-contact geometry are sufficient, within the local-GSFE reduced model, to produce a direction-split stability boundary when loading begins from the zero-force ground state. Dense/adaptive prepared-branch verification rules out a switch to a different metastable basin as the source of the headline split, while same-spectrum symmetrization and exact inversion remove or reverse the directional observables as symmetry requires. The registry-origin audit adds a complementary negative result: the physical asymmetry is invariant, but an arbitrary cosine/sine odd-sector continuation is not. Consequently the mechanism is attributed to nonremovable registry inversion asymmetry, not to a gauge-dependent eta susceptibility or optimum."
))
replace_para(P[92], (
"The theta sqrt(N) similarity is substantially more robust than in the initial ten-size calculation. Larger hexagons and an independent disk-like compact family remain collapsed to about 0.1% or better across a dense Theta=0-20 grid, supporting the structure-factor interpretation for compact rigid contacts. Boundary orientation behaves differently. Sufficiently rotated triangular cuts bring two registry minima into competition; their zero-force energy crossing changes the prepared ground state and reverses its branch-followed directional bias. The A/B competition and crossing persist across the tested surrogate outer-site weights, but the switch angle - and whether it falls inside the nominal 0-3 deg interval - is edge-model dependent. The qualitative registry competition is therefore a reduced-model prediction, whereas the numerical reversal angle is not a universal material constant."
))
replace_para(P[94], (
"A static threshold inequality does not by itself determine a rocking-ratchet phase diagram. The 91-point F0-tau scan is stronger than a mean-displacement classification because every sampled state repeats one winding cycle-by-cycle after transients, and representative plateaus spanning several windings are independently verified as attracting relative-periodic states. Thermal trajectories then separate four notions of robustness: exact target-winding identity is lost first; the negative-y cycle-sign bias becomes unresolved by T*=0.60; the v component of the mean current becomes unresolved at T*=0.65; and the full two-component mean vector remains statistically nonzero at 0.65 but not at 0.70. These are pointwise and joint finite-sample statements under the present protocol, not a universal thermal critical temperature or a complete operating diagram outside the tested drive, damping and reduced-temperature ranges."
))
replace_para(P[96], (
"The material conclusion can now be stated more sharply. Translation-minimized optimization shows that the corrected 2H MoSSe GSFE is genuinely inversion asymmetric in registry space, and the reciprocal-triad phase diagnostic provides an independent translation-invariant check. Matched same-2H symmetrization and exact inversion satisfy the expected static and dynamical contracts to numerical precision, which is stronger causal evidence within the reduced model than comparing only chemically different stackings. What remains unknown is the map from a physical experimental polarization change P_z to the complete set of GSFE amplitudes and phases. Exact spatial inversion is therefore a mathematical symmetry control, not a demonstrated polarization reversal. A quantitative polarity-to-rectification law requires paired polarity-resolved first-principles surfaces or equivalent atomistic input."
))
replace_para(P[98], (
"Three model-input limitations remain central. First, the source DFT GSFE relaxes the interlayer separation independently at each aligned registry [12], but the finite-contact model still represents the interface as a sitewise local-registry sum. Collective out-of-plane corrugation or buckling, atomistic edge reconstruction and chemistry, defects, and nonlocal edge energetics are absent. The in-plane calculations show why a higher model level matters: absolute thresholds shift with compliance even when the directional ratio survives. A public empirical SW plus registry-dependent interlayer candidate is therefore retained only as a qualitative stress test because it fails the corrected higher-harmonic GSFE contract. Second, load-dependent registry energetics, dissipation, participating mass, and laboratory state preparation are not supplied by the present GSFE; reduced temperature and time must not be converted into kelvin or physical frequency without independent calibration. Third, physical polarity reversal is not represented by eta scaling or the matched mathematical inversion control. Beyond these material-input limitations, the isolated higher-order stability point near theta=2.9734 deg merits a dedicated two-parameter normal-form study, and the continuous amplitude-period phase diagram may contain unsampled multistability or bifurcation structure."
))
replace_para(P[100], (
"A finite contact constructed from the corrected published 2H Janus MoSSe GSFE exhibits branch-followed full two-dimensional mechanical rectification without an added transverse guide. At theta=1.5 deg the prepared N=127 rigid thresholds are F_c,+*=3.071135 and F_c,-*=1.258672, and dense/adaptive continuation over 0-3 deg finds no exchange between the prepared ground family and the competing metastable family. Translation-minimized asymmetry diagnostics and matched same-2H controls identify registry-space inversion asymmetry as the relevant conservative ingredient: symmetrization removes the global directional bias and deterministic current, whereas exact inversion swaps the thresholds and reverses the lattice-vector current. The theta sqrt(N) similarity extends across larger hexagonal and disk-like compact contacts, while rotated triangular boundaries create competing registry minima whose ground-state switch can reverse the prepared response at an edge-model-dependent twist. Zero-mean forcing generates multiple oblique integer transport states; all 91 sampled points repeat one winding cycle-by-cycle, and representative plateaus are attracting relative-periodic orbits. Thermal noise destroys exact winding identity well before directed transport: the v component is resolved through T*=0.60, while the joint two-component mean current remains separated from zero at T*=0.65 but not at 0.70. Fresh linear-FEM and independently reconstructed nonlinear bond-angle calculations soften the absolute thresholds but preserve the directional split. The resulting evidence supports a self-consistent DFT-anchored reduced-model mechanism with explicit preparation, symmetry, geometry, dynamical, statistical and in-plane-relaxation falsification tests, while full three-dimensional Janus-specific atomistic relaxation, load/polarity-resolved energetics, experimental edge structure and physical dynamical calibration remain open."
))
replace_para(P[102], (
"The accompanying numerical materials contain the canonical unguided rigid-model release, the linear elastic-validation package, the independently reconstructed nonlinear bond-angle source and outputs, the Tier-2 interlayer-potential prescreen, and the Gate-level audit records used to freeze manuscript claims. The rigid and audit packages include the corrected published-GSFE engine; dense prepared-branch enumeration and continuation; matched symmetry and exact-inversion controls; registry-origin and odd-sector gauge checks; exact characteristic-angle and extended size/shape analyses; boundary-registry and edge-weight audits; cycle-resolved amplitude-period locking; representative Floquet, basin, time-step and continuation checks; trajectory-level thermal raw data; component and joint-vector bootstrap summaries; and manuscript/Supplementary Information sources. The empirical interlayer prescreen remains explicitly no-go for quantitative atomistic validation. No archival DOI is claimed until external repository deposition is completed."
))

# Update Table 1 protocols
T1=doc.tables[11]
rowmap={T1.rows[i].cells[0].text.strip():T1.rows[i] for i in range(1,len(T1.rows))}
set_cell(rowmap['Branch audit'].cells[1], '491-point dense/adaptive theta scan; 16 independent 21 x 21 stationary-point checkpoints')
set_cell(rowmap['Branch audit'].cells[2], 'Prepared-state / global-envelope ambiguity')
set_cell(rowmap['Size / shape'].cells[1], 'Exact q=0.80-0.95 characteristic angles; extended hex N=127-1261 and disk N=127-931; dense Theta=0-20')
set_cell(rowmap['Rocking map'].cells[1], 'theta=1.5 deg; F0*=1-4; tau*=20-80; 91 points; 40 measured cycles; cycle-resolved winding audit')
set_cell(rowmap['Rocking map'].cells[2], 'Sampled vector locking + representative Floquet states')
set_cell(rowmap['Thermal inference'].cells[1], '1000 trajectories/T; dt=0.02; 10+10 cycles; trajectory-cluster component and joint-vector bootstraps')
set_cell(rowmap['Thermal inference'].cells[2], 'Observable-specific current uncertainty')
set_cell(rowmap['In-plane relaxation hierarchy'].cells[1], 'N=127 free-edge linear FEM plus independently reconstructed nonlinear bond-angle VFF; stiffness brackets and rigid-limit checks')

# Update Table 3
T3=doc.tables[13]
rmap={T3.rows[i].cells[0].text.strip():T3.rows[i] for i in range(1,len(T3.rows))}
set_cell(rmap['2H registry asymmetry'].cells[1], 'A_min=0.0425361; odd RMS=0.206243; chi_1=0.583541; physical split invariant under registry-origin shifts')
set_cell(rmap['2H registry asymmetry'].cells[2], 'Origin-independent asymmetry; eta material-law interpretation rejected')
set_cell(rmap['Extended size/shape'].cells[1], 'hex N<=1261; disk N<=931; dense Theta=0-20; max within-family error <0.1%')
set_cell(rmap['Vector locking'].cells[1], '91/91 sampled points repeat one winding cycle-by-cycle; canonical and selected plateaus have rho_F<1')
set_cell(rmap['Vector locking'].cells[2], 'Broad sampled locking + representative attracting relative-periodic states')
set_cell(rmap['Thermal current'].cells[1], 'mean-v resolved through T*=0.60; joint 2D zero vector excluded at 0.65 and included at 0.70')
set_cell(rmap['Thermal current'].cells[2], 'Observable-specific trajectory-cluster inference; no sharp thermal critical T')
set_cell(rmap['In-plane relaxation, theta=1.5 deg'].cells[1], 'FEM: 2.934302 / 1.190210, rho=0.422860; nonlinear VFF: 2.935400 / 1.190479, rho=0.422921')

# Replace Figure 6 image preserving roughly original dimensions
p=P[82]
for r in list(p.runs):
    p._p.remove(r._r)
r=p.add_run()
r.add_picture(FIG6, width=Inches(6.15))
p.alignment=WD_ALIGN_PARAGRAPH.CENTER

doc.save(MAIN_OUT)

# -------- SI --------
si=Document(SI_IN)
P=si.paragraphs
replace_para(P[2], (
"This Supplementary Information records the numerical falsification and robustness calculations supporting the claim-frozen manuscript. It distinguishes prepared-state branch-followed observables from global diagnostic envelopes; documents same-spectrum symmetry controls and registry-origin gauge tests; extends size and shape checks; resolves the triangular-boundary reversal as a competing-registry ground-state switch; strengthens deterministic rocking from mean locking to cycle-resolved winding and representative multi-plateau Floquet tests; treats thermal trajectories with trajectory-level component and joint-vector inference; and compares a linear finite-element membrane with an independently reconstructed nonlinear bond-angle relaxation model. A separate Tier-2 empirical interlayer-potential prescreen is retained as a no-go record rather than quantitative atomistic validation."
))
replace_para(P[7], (
"The original concern was that a threshold defined by the last stable minimum anywhere in the registry cell could select different metastable basins under opposite loading. We therefore enumerate the zero-force minima and continue each family separately. At theta=0, 1.5 and 3 deg the primitive cell contains six stationary points, including two stable minima. The lower-energy family is the prepared ground state and the higher-energy family is retained as a competing metastable control. After the initial coarse survey, both families and their positive/negative stability boundaries are tracked over a 491-point dense/adaptive theta grid from 0 to 3 deg, with 16 independent 21 x 21 stationary-point checkpoints."
))
replace_para(P[10], (
"Across all 491 continuation points, U_meta-U_ground, F_c,+^ground-F_c,+^meta and F_c,-^ground-F_c,-^meta remain positive. Their minimum values are 0.173130, 1.702747 and 0.260865, respectively, all at the high-twist end of the interval. The 16 independent checkpoints each recover exactly two stable zero-force minima. The maximum zero-force root residual is 1.33e-15, the maximum fold residual is 5.41e-8 and the minimum hard fold eigenvalue is 6.806. This numerically resolves the 0-3 deg prepared-state interval at high density; it is not an interval-arithmetic proof over every real theta."
))
replace_para(P[19], (
"A brute 181 x 181 translation grid followed by multiple independent local refinements yields the same 2H A_min to numerical precision. The first-shell phase diagnostic is more precisely the normalized imaginary part of the complex-amplitude triad product, chi_1=Im[(C_1 C_2 C_3)/|C_1 C_2 C_3|]; because G_1+G_2+G_3=0 it is invariant under registry translation and reduces to sin(3 phi_1) in the equal-phase representation. In 1000 random translations the maximum chi_1 variation is below 1e-15. A complementary 26-origin test shows why an arbitrary cosine/sine continuation is not a material law: the physical eta=1 threshold split changes by less than 9.8e-15 across origins, but the eta=0 ground-state topology changes (17 origins with one stable ground minimum, 9 with an inversion-degenerate pair) and the small-eta response changes with origin. At the published origin a local fit gives d(Delta F_c)/d eta approximately 2.833, whereas at the A_min center the prepared-ground observable has a finite branch-selection jump at eta=0. Therefore no eta susceptibility or intermediate eta optimum is interpreted physically. An A_min-centered eta homotopy is retained only as a coordinate-covariant mechanism-isolation path, with no mapping to experimental polarization."
))
replace_para(P[23], (
"The hexagonal family contains N=127, 217, 331, 469, 631, 817, 1027 and 1261, and the disk-like family contains N=127, 241, 367, 517, 721 and 931. A later dense rerun evaluates every integer Theta from 0 to 20, not only the four summary values in Table S4. The worst within-family deviations still occur at Theta=20 and remain below 0.1%, while the hexagon-disk family-mean difference remains about 0.10%. Independent high-Theta prepared-state spot checks for the smallest contacts also confirm that the reported folds remain connected to the zero-force ground branch. These calculations support theta sqrt(N) similarity for the tested compact rigid families, not arbitrary boundary geometries or deformable contacts."
))
replace_para(P[29], (
"The edge-weight test is intentionally not an atomistic edge-relaxation model. Across all ten tested cut/weight combinations the A/B energy crossing persists, both candidate registries are stable zero-force minima at the crossing, and the two families retain opposite directional biases. What is not robust is the numerical switch angle or its placement inside a chosen finite twist window: for example, at weight 0.5 the 20 and 25 deg crossings move to 3.1701 and 3.0832 deg, outside the nominal 0-3 deg interval. The reduced-model claim is therefore competing-registry switching with edge-sensitive location, not a universal reversal twist."
))
replace_para(P[31], (
"The deterministic map contains 91 amplitude-period points. The original mean-displacement classification gives an integer pair at all 91 points with maximum mean lattice-rounding residual 3.916e-12. A stricter rerun resolves all 40 measured cycles separately and finds that every sampled point repeats one and the same winding pair cycle-by-cycle after transients; the maximum single-cycle rounding residual is below 1e-9. The sampled map contains 23 distinct winding pairs. A dense tau*=40 amplitude scan further resolves finite-width plateaus including (0,0), (1,-1), (1,-2), (2,-3), (3,-4) and higher windings."
))
replace_para(P[34], (
"The canonical (1,-1) leading multiplier agrees across explicit high-order and implicit stiff solvers, so only rho_F<1 is interpreted physically. The same test was extended to five additional plateau representatives. Using the tighter DOP853 solve, the leading spectral radii are approximately 1.39e-31 for (0,0), 4.62e-24 for (1,-1) at F0*=1.9625, 5.69e-20 for (1,-2), 9.47e-17 for (2,-3), 5.21e-13 for (3,-4), and 1.62e-15 for the high-winding (2,-7) state at tau*=70; Radau confirms rho_F<1 in every case. Across these six states, 24/24 time-step tests and 162/162 local basin perturbations recover the expected winding. Increasing and decreasing amplitude continuation at tau*=40 agree at all 61 sampled amplitudes. These checks establish representative local attraction, not global attractor uniqueness."
))
replace_para(P[38], (
"Each trajectory contains 10 burn cycles and 10 measured cycles. The canonical component intervals use 10,000 trajectory-level cluster-bootstrap resamples; cycles from one trajectory are never treated as independent replicates. The mean-v interval excludes zero through T*=0.60 and includes zero at T*=0.65. Because the deterministic current is two-dimensional, a separate high-temperature joint bootstrap evaluates the mean vector (u,v). At T*=0.60 and 0.65 the zero vector remains outside the 95% joint region, whereas at T*=0.70 it is included; 100,000-resample reruns with two independent seeds reproduce the 0.65/0.70 classification. Simultaneous two-component intervals at T*=0.65 are u in [0.0091,0.1810] and v in [-0.1480,0.0177]. The cycle-sign statistic is distinct: P(Delta y<0) is robust through 0.50, marginal at 0.55 and unresolved by 0.60. Exact target-winding probability is low at all nonzero sampled temperatures. No sharp thermal critical temperature is inferred from these observable-specific boundaries."
))
replace_para(P[42], (
"At theta=1.5 deg a fresh nominal linear-membrane rerun gives F_c,+*=2.934302, F_c,-*=1.190210 and rho=0.422860; C/2 gives 2.807397, 1.135229 and 0.424125; 2C gives 3.001636, 1.222534 and 0.421172; the alternative elastic constants give 2.944409, 1.194897 and 0.422658; and 100C recovers 3.069751, 1.257886 and 0.418673. At theta=3 deg the nominal values are 1.573022 and 0.631274 with rho=0.427233. Thus in-plane relaxation renormalizes absolute thresholds while preserving the directional sign over the tested stiffness range. The nonlinear bond-angle model is independently reconstructed from the documented 342-bond/648-angle network and calibrated coefficients before comparison."
))
replace_para(P[44], (
"The independently reconstructed nonlinear triangular-site model reproduces the target homogeneous elastic constants to numerical precision. At theta=1.5 deg the nominal branch gives F_c,+*=2.935400, F_c,-*=1.190479 and rho=0.422921; the half-stiffness branch gives 2.810107, 1.135693 and 0.424353. At theta=3 deg the nominal nonlinear result is 1.574365, 0.631006 and 0.427755. These values remain within about 0.13% of the corresponding fresh linear-FEM thresholds. At theta=1.5 deg nominal stiffness the largest last-stable-state bond strain is below 0.40% and the largest local angle change below 0.40 deg."
))
replace_para(P[51], (
"The audit resolves the computational ambiguities that can be decided with the corrected GSFE and shows that the headline directional split survives two in-plane compliance representations. Remaining inputs are a Janus-specific full-three-dimensional atomistic potential that passes the corrected 2H GSFE contract; collective finite-flake corrugation/buckling and edge reconstruction; load-dependent stacking energetics; polarity-resolved first-principles surfaces; dissipative and inertial calibration; laboratory state preparation; and experiment. The exact triangular switch angle is especially edge-model sensitive, and reduced temperature or period must not be converted into kelvin or physical frequency without independent calibration."
))
replace_para(P[53], (
"The accompanying materials retain the canonical unguided rigid-model release and add the Gate-level prepared-branch, symmetry/gauge, size/shape, boundary, deterministic-locking, thermal, and elasticity audits used to freeze manuscript claims. The final package also archives the independently reconstructed nonlinear VFF source, fresh linear/VFF result tables, joint-vector thermal bootstrap tables, and the rewritten manuscript/SI sources. The Tier-2 empirical interlayer candidate remains explicitly no-go for quantitative atomistic use because its corrected higher-harmonic GSFE spectrum fails the predeclared Janus-specific contract."
))

# Update S3 table header
S3=si.tables[2]
set_cell(S3.rows[0].cells[3], 'triad invariant chi_1', font_size=8.5, bold=True, center_short=True)

# Update S8 existing table title remains component table; add S8b after table 7
# Create S7b after existing Table S7 (table index 6) and before paragraph 34 logically.
base=si.tables[6]
cap=si.add_paragraph('Table S7b. Cross-solver Floquet stability of representative plateaus.')
base._tbl.addnext(cap._p)
flq=pd.read_csv('/mnt/data/janus_n5_gate/n5_newton_shooting_floquet.csv')
# tighter DOP rows
sel=flq[(flq['method']=='DOP853') & (flq['rtol']<1e-10)].copy()
wind={'pinned':'(0,0)','w11':'(1,-1)','w12':'(1,-2)','w23':'(2,-3)','w34':'(3,-4)','w27_high':'(2,-7)'}
tbl=si.add_table(rows=1, cols=6); tbl.style='Table Grid'; cap._p.addnext(tbl._tbl)
headers=['state','F0*','tau*','winding','rho_F','closure']
for j,h in enumerate(headers): set_cell(tbl.rows[0].cells[j],h,font_size=8,bold=True,center_short=True)
for _,r in sel.iterrows():
    row=tbl.add_row().cells
    vals=[r['name'],f"{r['F0']:.4f}",f"{r['period']:.0f}",wind[r['name']],f"{r['mu1_abs']:.3e}",f"{r['closure']:.3e}"]
    for j,v in enumerate(vals): set_cell(row[j],v,font_size=8,center_short=(j!=0))
format_table(tbl,8)

# Existing S8 caption clarify component table
replace_para(P[36], 'Table S8a. Free-contact thermal component and directional statistics (n=1000 independent trajectories per T*).')
# Add S8b after existing table 7
base8=si.tables[7]
cap8=si.add_paragraph('Table S8b. High-temperature joint two-component current audit.')
base8._tbl.addnext(cap8._p)
t8=si.add_table(rows=1,cols=7); t8.style='Table Grid'; cap8._p.addnext(t8._tbl)
heads=['T*','mean u','mean v','sim. 95% CI u','sim. 95% CI v','zero vector','joint decision']
for j,h in enumerate(heads): set_cell(t8.rows[0].cells[j],h,font_size=7.5,bold=True,center_short=True)
joint=pd.read_csv('/mnt/data/janus_n8_gate/n8_thermal_vector_simultaneous_ci_100k.csv')
for _,r in joint.iterrows():
    row=t8.add_row().cells
    vals=[f"{r['T']:.2f}",f"{r['mean_u']:.4f}",f"{r['mean_v']:.4f}",f"[{r['u_sim_lo']:.4f},{r['u_sim_hi']:.4f}]",f"[{r['v_sim_lo']:.4f},{r['v_sim_hi']:.4f}]",'excluded' if r['zero_excluded'] else 'included','resolved' if r['zero_excluded'] else 'unresolved']
    for j,v in enumerate(vals): set_cell(row[j],v,font_size=7.5,center_short=True)
format_table(t8,7.5)

# Update S9 linear table
S9=si.tables[8]
vals={
'Rigid, 1.5 deg':['3.071135','1.258672','0.418601','0'],
'Elastic C, 1.5 deg':['2.934302','1.190210','0.422860','0.459%'],
'Elastic C/2, 1.5 deg':['2.807397','1.135229','0.424125','0.824%'],
'Elastic 2C, 1.5 deg':['3.001636','1.222534','0.421172','0.244%'],
'Elastic C, 3 deg':['1.573022','0.631274','0.427233','0.864%'],
'Elastic C/2, 3 deg':['1.244897','0.516821','0.413276','1.597%'],
'Rigid-limit 100C, 1.5 deg':['3.069751','1.257886','0.418673','0.0052%'],
}
for row in S9.rows[1:]:
    key=row.cells[0].text.strip()
    if key in vals:
        for j,v in enumerate(vals[key],start=1): set_cell(row.cells[j],v,font_size=8.2,center_short=True)

# Update S10 nonlinear table
S10=si.tables[9]
vals2={
'theta=1.5, C/2':['2.810107','1.135693','0.424353','+0.0966%','+0.0390%','positive'],
'theta=1.5, C':['2.935400','1.190479','0.422921','+0.0374%','+0.0226%','positive'],
'theta=3.0, C':['1.574365','0.631006','0.427755','+0.0854%','-0.0425%','positive'],
}
for row in S10.rows[1:]:
    key=row.cells[0].text.strip()
    if key in vals2:
        for j,v in enumerate(vals2[key],start=1): set_cell(row.cells[j],v,font_size=8,center_short=(j!=0))

si.save(SI_OUT)

print(MAIN_OUT)
print(SI_OUT)
