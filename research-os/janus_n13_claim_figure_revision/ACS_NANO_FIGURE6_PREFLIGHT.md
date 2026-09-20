# ACS Nano Figure 6 Preflight - Stationary Thermal Hierarchy

**Mode:** figure-audit / preflight  
**Target:** ACS Nano Article  
**Official guidance checked:** 2026-09-19  
**ACS Nano Author Guidelines page:** https://researcher-resources.acs.org/publish/author_guidelines?coden=ancac3  
**Page status at check:** last updated 2026-08-27  
**ACS Nano Author Checklist:** https://pubsapp.acs.org/paragonplus/submission/ancac3/ancac3_checklist.pdf

## Status

**CONDITIONAL_READY**

The scientific layout, final-size geometry, line widths, label sizes, color redundancy, caption plan, and export set satisfy the current preflight contract. One packaging-layer issue remains: the container does not contain the literal Arial font required by the ACS Nano checklist. Local raster previews therefore use Arimo as a metric-compatible fallback. The editable SVG declares Arial and should be re-exported with actual Arial (or Arial text converted to outlines) during the final ACS Nano submission layer.

## Current ACS Nano graphics constraints used

- Arial lettering within graphics.
- Uniform lettering, no smaller than 6 pt at final published size.
- Lines no thinner than 0.5 pt at final published size.
- Figures submitted at final published size.
- Color photographic/raster material at least 300 dpi RGB; vector artwork preferably EPS under the ACS Nano checklist.
- ACS-wide size guidance: single column up to 3.33 in; double column 4.167-7.0 in; maximum depth 9.167 in including caption.

## Figure 6 contract

- **Scientific job:** show that the stationary mean lattice current decays strongly with reduced temperature while remaining statistically nonzero over the sampled stationary range, whereas exact deterministic winding identity is already strongly mixed.
- **Intended placement:** double column.
- **Final width:** 7.0 in.
- **Final height:** approximately 2.32 in, excluding caption.
- **Panel (a):** mean lattice-coordinate currents with trajectory-level 95% intervals. Full-grid low-temperature points use the stationary N=500 series; high-temperature points use two-seed pooled N=1000 estimates.
- **Panel (b):** high-temperature Hotelling zero-current rejection ratio, with 1 as the statistical threshold. This panel is a detectability diagnostic, not a physical critical-temperature estimator.
- **Panel (c):** negative-v cycle probability versus exact deterministic target-winding probability. This separates weak directional bias from preservation of the deterministic mode label.
- **Interpretation boundary:** no statement of current extinction, critical temperature, Kelvin-scale calibration, or behavior for T*>0.70.

## Compliance checks

| Check | Result |
|---|---|
| Double-column width <= 7.0 in | PASS |
| Panel/axis/legend text >= 6 pt | PASS (6.3-8.5 pt in working source) |
| Lines >= 0.5 pt | PASS (0.7-1.0 pt) |
| Panel labels consistent | PASS |
| Color-only encoding avoided | PASS (marker shape + line style redundancy) |
| RGB raster derivative available | PASS |
| Editable/vector source retained | PASS (SVG + EPS) |
| Caption can state N/protocol/error bars | PASS |
| No obsolete 0.65/0.70 boundary encoded | PASS |
| Literal Arial in final exported artwork | **PENDING** - local environment lacks Arial |

## Canonical outputs

- `Figure_6_thermal_stationary_hierarchy.svg` - editable source; Arial declared for final venue export.
- `Figure_6_thermal_stationary_hierarchy.eps` - current vector derivative; local font fallback remains.
- `Figure_6_thermal_stationary_hierarchy.tif` - 600 dpi RGB/LZW working raster derivative.
- `Figure_6_thermal_stationary_hierarchy.png` - manuscript insertion copy matched to the previous image aspect ratio.
- `Figure_6_panel_a_data.csv`, `Figure_6_panel_b_data.csv`, `Figure_6_panel_c_data.csv` - source data for each panel.

## Final venue-layer action

At the final `acs-nano-submission` packaging stage, open the canonical SVG on a system with Arial installed, verify the 6 pt minimum at 7.0 in width, then export the final EPS/TIF derivative. This is a typography/package requirement only and does not change the scientific content of the figure.
