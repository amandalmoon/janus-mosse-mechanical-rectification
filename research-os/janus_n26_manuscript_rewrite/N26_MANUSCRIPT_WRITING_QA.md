# N26 Manuscript Writing QA

## Current state

- Draft branch: \`research-os/n26-manuscript-rewrite\`
- Upstream figure head: \`4060d017a50c6387de45377621d9232529e7e4ad\`
- Argument authority: N21 argument architecture
- Claim/numerical authority: N17 Claim-Evidence Matrix v3
- Figure authority: N25 seven-figure BENCHMARK_PASS set
- Current prose coverage:
  - Title / keywords: drafted
  - Abstract: drafted
  - Introduction: drafted
  - Methods 2.1–2.10: drafted
  - Results 3.1–3.7: drafted in FIG-01→FIG-07 order
  - Discussion 4.1–4.4: drafted
  - Conclusions: drafted
  - Data/code availability: not yet reassembled
  - Reference list: not yet reassembled
  - Final citation audit: pending
  - DOCX/venue formatting: intentionally downstream

## Paragraph-logic audit

Academic Writing Toolkit returned 12 medium "short paragraph" findings. Manual inspection shows all 12 are equation lead-ins or display-equation blocks, not prose-logic failures:

- similarity-coordinate equation
- pinned-state condition
- normalized split definition
- characteristic-angle equation
- Langevin equation and noise covariance
- transverse-guide equation
- Results equations for \(A_{\min}\), depinning thresholds, symmetry-null threshold, boundary switches, and high-\(T^*\) mean vector

No paragraph was revised solely to silence these equation-layout false positives.

## Claim-language audit

The draft was checked for known retired/forbidden language. No active violation was found.

Occurrences of potentially risky terms are boundary statements, not claims:
- "critical temperature" appears only in explicit negations ("does not define", "No thermal critical temperature").
- "universal material constant" appears only as a rejection.
- "parameter-free" appears only in a scope negation.
- "proof" appears only in "not a proof" scope statements.
- "all 91 ... Floquet" regex matches are false positives: the prose explicitly distinguishes 91/91 cycle locking from Floquet certification of representative plateaus.

The following retired claims are absent:
- 10-burn/10-measure thermal inference as current evidence
- mean \(v\) unresolved at \(T^*=0.65\)
- zero current included at \(T^*=0.70\)
- every threshold point is a generic saddle-node
- exact GSFE inversion is physical Janus-polarity reversal
- \(\eta\) susceptibility or an \(\eta\approx0.5\) material optimum
- a generic "first friction diode/ratchet/mode-locking" novelty claim

## Thermal authority check

N26 uses only the stationary long-window authority:
- \(dt=0.02\)
- 60 burn cycles
- 100 measured cycles
- full \(T^*=0.02\)–0.70 series: \(N=500\) trajectories per temperature
- independent second \(N=500\) seed for \(T^*=0.50\)–0.70
- pooled high-\(T^*\) \(N=1000\)
- trajectory is the inferential unit
- at \(T^*=0.70\), pooled mean \((u,v)=(0.036998,-0.076448)\)
- zero-current vector excluded through every sampled high-\(T^*\) point 0.50–0.70
- sample-count convergence from FR-S01 retained
- no thermal critical temperature inferred

## Open writing-layer tasks

1. Reassemble the existing verified reference list and run citation consistency audit.
2. Synchronize captions against the exact N25 manifests after prose freeze.
3. Add Data and Code Availability wording, leaving archival DOI as \`FR-R01 OPEN_VENUE\`.
4. Run a citation/novelty audit after prose stabilization.
5. Only after those steps, assemble the formatted DOCX and start Five Reviewer review.

No scientific upstream task is currently reopened.
