# Manuscript Action Register After Gate 9

This register contains only changes required by the completed gates; it is not yet the manuscript rewrite.

## CRITICAL — Abstract
**Issue:** Thermal sentence currently says mean vector current resolved through T*=0.60 but not 0.65.

**Required change:** Split observables: v-component resolved through 0.60/unresolved at 0.65; joint 2D mean vector still resolved at 0.65 and unresolved at 0.70.

**Claim IDs:** C16,C17

## MAJOR — Methods 2.3
**Issue:** Triad diagnostic sin(3 phi1) can be read as a single-phase invariant.

**Required change:** Clarify it is the normalized imaginary part/phase of the first-shell complex-amplitude triad product, reducing to sin(3 phi1) in the equal-phase representation.

**Claim IDs:** C1

## MAJOR — Methods 2.4 / Results 3.2
**Issue:** Current text describes the branch audit mainly as a 0.25° grid.

**Required change:** Optionally update to the 491-point dense/adaptive interval verification over 0-3°, while retaining the caveat that this is numerical verification rather than interval-arithmetic proof.

**Claim IDs:** C2,C3

## MAJOR — Results 3.3
**Issue:** Current extended shape wording mentions only Theta=0,10,15,20 despite a later dense audit.

**Required change:** If desired, state that the larger hex/disk families were subsequently checked on a dense Theta=0..20 grid and retained the same <0.1% conclusion.

**Claim IDs:** C6,C7

## MAJOR — Discussion 4.2
**Issue:** “The switch survives a broad outer-site weighting sensitivity test” can imply the reversal remains within 0-3° for every weight.

**Required change:** Replace with: the A/B registry competition and crossing persist across tested edge weights, but the switch angle—and whether it falls inside 0-3°—is edge-model dependent.

**Claim IDs:** C8,C9

## MAJOR — Results 3.6
**Issue:** 91-point evidence is described as finite-run mean integer displacement only.

**Required change:** Strengthen carefully: 91/91 sampled points repeat the same integer winding cycle-by-cycle after transients; Floquet certification remains limited to the canonical orbit and selected representative plateaus.

**Claim IDs:** C13,C14

## CRITICAL — Results 3.7
**Issue:** Thermal interpretation conflates lattice-v with full vector current.

**Required change:** Use observable-specific wording and add the joint two-component 0.65/0.70 result; keep cycle-sign statistic separate.

**Claim IDs:** C15,C16,C17,C18

## CRITICAL — Figure 6 caption / Table 3
**Issue:** Current thermal summary labels the v-component boundary as the mean-vector-current boundary.

**Required change:** Label panel/table row explicitly as mean v; add or replace with a full-vector joint-bootstrap line showing zero-vector excluded at 0.65 and included at 0.70.

**Claim IDs:** C16,C17

## CRITICAL — Discussion 4.3
**Issue:** States mean vector current remains nonzero through T*=0.60, which is now incomplete.

**Required change:** Distinguish exact winding, cycle-sign, v-component, and joint 2D current. Do not infer a sharp thermal critical temperature.

**Claim IDs:** C15,C16,C17,C18

## CRITICAL — Conclusion
**Issue:** Current conclusion repeats “mean vector current remains resolved through 0.60 but not 0.65.”

**Required change:** Replace with the new joint-vector statement and preserve the no-critical-temperature caveat.

**Claim IDs:** C17

## MAJOR — Data and code availability / SI
**Issue:** Standalone nonlinear VFF source was absent from the accessible bundle, although the model was reconstructable.

**Required change:** Archive the independently reconstructed VFF source and the new N8 tables in the final reproducibility package.

**Claim IDs:** C21

## MAJOR — Legacy materials
**Issue:** Old eta susceptibility ~2.8322 and eta_opt~0.5 claims remain scientifically invalid if reintroduced.

**Required change:** Keep arbitrary-origin eta material-law claims retired. If eta appears, use only A_min-centered SI homotopy language.

**Claim IDs:** C10,C11,C12
