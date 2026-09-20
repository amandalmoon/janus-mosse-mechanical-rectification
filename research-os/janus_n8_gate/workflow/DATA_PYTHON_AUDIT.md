# Data/Python statistical and numerical audit

This audit independently recomputes the statistical summaries used in the revised manuscript from the stored trajectory-level and summary CSV files.

## Thermal inference
- Independent trajectory-cluster bootstrap: 10,000 replicates at each temperature, n=1000 independent trajectories/T.
- Mean vector current 95% CI excludes zero through T*=0.60; the first sampled temperature whose CI includes zero is T*=0.65.
- P(Delta y<0) 95% CI remains strictly above 0.5 through T*=0.55; the first sampled point that touches/crosses 0.5 is T*=0.60.
- The independently bootstrapped CI endpoints differ from the archived canonical endpoints by at most 0.002823, consistent with Monte-Carlo bootstrap variation.

## Deterministic robustness
- Branch preparation: 13 sampled twists from 0.00 to 3.00 deg; ground-state branch is both lower in zero-force energy and longer-lived in both force directions at every sampled point: True.
- Vector map: 91/91 sampled amplitude-period points satisfy the finite-run integer-lock criterion; 23 distinct integer winding pairs; max residual=3.916e-12.
- Floquet: three independent integrations have relative spectral-radius span 2.764e-06; max one-cycle closure=1.915e-11.

## Symmetry and finite-size contracts
- Same-2H symmetrized global static split=6.574e-10; symmetric current norm=8.510e-18.
- Exact inversion threshold-swap errors: +=2.220e-16, -=1.776e-15; current reversal component-sum errors=9.548e-15, 1.665e-14.
- At Theta=20, cross-size maximum relative deviations: hex F+=0.0818%, F-=0.0800%; disk F+=0.0230%, F-=0.0222%.

## Elastic model-form cross-check
- Nonlinear VFF at theta=1.5 deg: F+=2.935449, F-=1.190527, rho=0.422911.
- Difference from linear FEM: F+=+0.0433%, F-=+0.0410%, rho=+0.0022%.
- At theta=3 deg: F+=1.574316, F-=0.630957, rho=0.427774; directional sign remains positive.

## Interpretation guardrails
- These checks validate numerical/statistical claims within the reduced published-GSFE and in-plane-relaxation models.
- They do not convert reduced T* to kelvin, establish a physical damping/mass, or replace the still-pending Janus-specific full-3D atomistic/MLIP validation.
- Boundary switch angles remain edge-model sensitive and should not be described as material constants.
