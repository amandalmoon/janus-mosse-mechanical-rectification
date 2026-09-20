# N13 Claim-Evidence / ACS Nano Figure / Thermal Revision Report

**Date:** 2026-09-19  
**Current Research OS stage:** Claim-Evidence synchronization -> ACS Nano Figure Preflight -> Figure/Table regeneration -> targeted manuscript revision  
**Gate result:** **PASS** for scientific synchronization. **Figure 6 = CONDITIONAL_READY** for final ACS Nano packaging because the container lacks literal Arial; the source/export must be regenerated with Arial or outlined Arial at the venue layer.

## 1. Source of truth

This revision uses RT-B01 Thermal Stationarity Closure as the thermal source of truth. The previous short-window detectability boundaries are retired rather than shifted to a new critical temperature.

Canonical stationary protocol:

- N=127 compact hexagonal contact
- theta=1.5 deg, F0*=2, tau*=40, m*=1, gamma*=4
- BAOAB, dt=0.02
- 60 burn cycles + 100 measured cycles
- full T*=0.02-0.70 series: N=500 independent trajectories per T*
- high-temperature T*=0.50-0.70 band: second independent N=500 ensemble, pooled N=1000
- trajectory is the inferential unit

At T*=0.70, pooled N=1000 gives

- mean (u,v)=(0.036998,-0.076448)
- 50,000-resample trajectory-bootstrap 95% interval: u [0.01265,0.06132], v [-0.10088,-0.05195]
- zero-current vector excluded under the declared joint test
- P(v_cycle<0)=0.50802 [0.50506,0.51100]
- P[(m,n)=(1,-1)] about 0.01116

Therefore the supported interpretation is that exact deterministic mode identity is strongly mixed by noise while a weaker stationary mean drift remains nonzero through the largest sampled T*=0.70. No current-extinction temperature or behavior beyond T*=0.70 is established.

## 2. Claim-Evidence Matrix synchronization

Updated records:

- **M0:** Angeli GSFE provenance remains corrected: the 2024 Erratum is not described as a GSFE phase-convention correction.
- **C15:** exact winding identity is much less thermally robust than stationary directed mean current.
- **C16:** mean v remains negative and separated from zero through sampled T*=0.70; old 0.60/0.65 component boundary retired.
- **C17:** the full stationary two-component mean current remains nonzero through sampled T*=0.70; old 0.65/0.70 vector boundary retired.
- **C18:** P(v_cycle<0) approaches one-half but remains weakly above 0.5 through T*=0.70; old "unresolved by 0.60" wording retired.
- **C19:** high-temperature mean-current estimates are compatible across tested dt=0.04, 0.02 and 0.01, with no pairwise component difference larger than 1.12 combined SE.

Updated matrix artifacts: XLSX, CSV, JSON and human-readable Markdown.

## 3. ACS Nano Figure 6 preflight

Figure 6 was rebuilt as an evidence figure with three coordinated jobs:

- **(a)** stationary mean lattice-coordinate currents versus T*, with trajectory-level uncertainty;
- **(b)** high-temperature joint zero-current rejection ratio for the pooled two-seed ensembles;
- **(c)** cycle-sign probability versus exact deterministic target-winding probability.

The figure is designed for double-column placement at approximately 7 in width. Working text sizes are 6.3-8.5 pt at final size and lines are 0.7-1.0 pt, satisfying the current ACS Nano minimums of 6 pt lettering and 0.5 pt lines. Color encodings are backed by marker/line-style redundancy. PNG/TIF/EPS/SVG and the plotting script/data are archived.

**Remaining venue-layer condition:** ACS Nano requires Arial lettering. This runtime resolves Arial requests to Arimo, so final submission artwork must be regenerated with actual Arial or have text outlined using an approved final-production workflow. This is a venue-packaging issue, not a scientific blocker.

## 4. Manuscript and SI targeted revision

The main manuscript and SI were revised only where downstream thermal evidence changed or where a corresponding summary/table/caption had to stay synchronized.

Main manuscript updates include:

- Abstract thermal result
- thermal Methods protocol and inference unit
- Results 3.7
- Figure 6 and caption
- Table 1 thermal protocol
- Table 3 central thermal result
- Discussion thermal interpretation
- Conclusion
- data/code availability wording

SI updates include:

- S8 stationary protocol
- Table S8a full stationary series
- Table S8b pooled high-temperature joint-current audit
- stationarity, initial-state-memory, bootstrap/Hotelling and timestep statements

No old "0.60/0.65" or "0.65/0.70" thermal critical-boundary claim remains as an active manuscript conclusion.

## 5. Artifact and visual QA

- Main manuscript rendered to **15 pages** and every page was visually inspected.
- SI rendered to **5 pages** and every page was visually inspected.
- Table S8b originally split after its first data row; it was moved intact to the next page and re-rendered.
- No clipping, overlap, broken tables, missing glyphs, or figure/caption separation was observed in the final render.
- The embedded Figure 6 media object in the DOCX (`word/media/image24.png`) has the same SHA-256 hash as the canonical Figure 6 PNG: `2b075ece2e3cce6348026a4dd30d6b2c0ce4842104b30c9a21a0cf7511b0f94e`.

## 6. Claim status after N13

### VERIFIED WITH SCOPE
- Stationary thermal mean drift persists through the largest sampled T*=0.70 under the declared reduced protocol.
- Exact deterministic winding identity is already strongly mixed in the noisy regime.
- The result is stationary with respect to the tested burn-in/late-block and initial-state-memory checks.
- Targeted timestep reruns do not reveal a high-temperature timestep artifact over dt=0.04-0.01.

### REJECTED / RETIRED
- "v resolved through 0.60 and unresolved at 0.65."
- "full vector resolved at 0.65 and unresolved at 0.70."
- "P(Delta y<0) becomes unresolved by 0.60."
- any interpretation of finite-observation significance as a universal thermal critical temperature.

### OPEN
- behavior for T*>0.70;
- physical Kelvin/time calibration;
- dependence of the dynamical transport map on reduced damping/mass outside the declared operating protocol;
- physical twist-sweep hysteresis for boundary-registry switching;
- full 3D Janus-specific atomistic relaxation.

## 7. Next gate

**Short Red-Team closure.** Re-audit the revised manuscript/SI specifically for:

1. residual thermal contradictions or stale boundary language;
2. consistency of Figure 6/Table 3/SI S8 with C15-C19;
3. whether the existing Red-Team Major scope constraints (damping, forcing direction, preparation, boundary-switch dynamics, rotational/loading constraint, elasticity independence) are stated strongly enough to prevent overclaim.

If no scientific Blocker remains after that closure, proceed to the independent Five Reviewer Paper Audit.
