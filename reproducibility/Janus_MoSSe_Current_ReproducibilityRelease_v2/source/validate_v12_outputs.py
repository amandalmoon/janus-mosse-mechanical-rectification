from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'


def close(a, b, tol, msg):
    if abs(float(a) - float(b)) > tol:
        raise AssertionError(f'{msg}: {a} vs {b} (tol={tol})')


def main():
    diag = pd.read_csv(DATA/'dft_fourier_phase_diagnostics_v12.csv')
    win = pd.read_csv(DATA/'dft_2H_MoSSe_guided_diode_window_k25_v12.csv').iloc[0]
    hess = pd.read_csv(DATA/'dft_2H_MoSSe_guided_fullhessian_k25_v12.csv')
    controls = pd.read_csv(DATA/'dft_3R_MoSSe_guided_threshold_controls_v12.csv')
    dt = pd.read_csv(DATA/'dft_2H_MoSSe_rocking_dt_validation_k25_v12.csv')
    tw = pd.read_csv(DATA/'dft_2H_MoSSe_thermal_diode_windows_k25_v12.csv')
    hi = pd.read_csv(DATA/'dft_2H_MoSSe_highT_energyunit_proxy_k25_v12.csv')

    # Published-Fourier diagnostics reconstructed with the erratum convention.
    row2h = diag[(diag.configuration=='2H_MoSSe_Se-S-Se-S') & (diag.shell==1)].iloc[0]
    row3rs = diag[(diag.configuration=='3R_MoSSe_S-Se-Se-S') & (diag.shell==1)].iloc[0]
    close(row2h.chi_translation_invariant, 0.5835412113561176, 1e-12, '2H chi1')
    if abs(float(row3rs.chi_translation_invariant)) > 1e-12:
        raise AssertionError('3R symmetric chi1 must vanish')
    close(row2h.energy_unit_6W1_meV, 47.4, 1e-12, '2H DFT energy unit')

    # Static material-case window and full-Hessian stability.
    close(win.theta_c_forward_deg, 1.9444516264438518, 2e-6, 'forward theta_c')
    close(win.theta_c_reverse_deg, 1.0099068387052377, 2e-6, 'reverse theta_c')
    close(win.window_abs_deg, 0.9345447877386142, 3e-6, 'DFT material diode window')
    if not np.all(hess.eig_hard.to_numpy(float) > 0):
        raise AssertionError('nonsoft Hessian eigenvalue must stay positive')
    if not np.all(np.abs(hess.eig_soft.to_numpy(float)) < 2e-5):
        raise AssertionError('soft Hessian eigenvalue is not numerically zero')
    if not np.all(hess.k_perp.to_numpy(float) > hess.min_kperp_from_Hxx.to_numpy(float)):
        raise AssertionError('k_perp=25 does not stabilize all DFT critical states')
    close(hess[hess.direction=='reverse'].iloc[0].min_kperp_from_Hxx, 19.296836967564904, 2e-6,
          'reverse minimum guide stiffness')

    # Exact forward/reverse degeneracy of the published symmetric 3R control.
    sym = controls[controls.landscape=='3R_MoSSe_S-Se-Se-S']
    pf = sym.pivot(index='theta_deg', columns='direction', values='Fc').dropna()
    split = np.max(np.abs(pf['forward'] - pf['reverse']))
    if split > 2e-10:
        raise AssertionError(f'3R symmetric forward/reverse split too large: {split}')

    # Deterministic mode locking must survive dt refinement and a half-period phase shift (F0 -> -F0).
    for th, amp, expected in [(1.5,3.5,-2.0),(1.0,4.0,-3.0),(0.5,4.0,-2.0),(2.0,3.5,-3.0)]:
        g = dt[(np.isclose(dt.theta_deg,th)) & (np.isclose(np.abs(dt.F0),amp))]
        if len(g) != 8:
            raise AssertionError(f'missing dt/phase rows for theta={th}, |F0|={amp}')
        if np.max(np.abs(g.periods_per_cycle.to_numpy(float)-expected)) > 2e-9:
            raise AssertionError(f'mode locking not invariant for theta={th}, |F0|={amp}')

    # Thermal material-window fits.
    t5 = tw[np.isclose(tw.T_star,0.005)].iloc[0]
    t10 = tw[np.isclose(tw.T_star,0.010)].iloc[0]
    close(t5.W50_abs_deg, 0.9466385095389849, 2e-6, 'T*=0.005 W50')
    close(t10.W50_abs_deg, 1.055328507492319, 2e-6, 'T*=0.010 W50')
    for r in (t5,t10):
        if not (r.W50_ci_low < r.W50_abs_deg < r.W50_ci_high):
            raise AssertionError('thermal W50 estimate outside bootstrap CI')

    # DFT-energy-unit high-noise proxy: both directions are effectively switched throughout the grid.
    h300 = hi[np.isclose(hi.T_star, 0.5454008393670885)]
    mins = h300.groupby('direction').p_escape.min()
    if float(mins.min()) < 0.98:
        raise AssertionError(f'high-T proxy not saturated enough: {mins.to_dict()}')

    print('v12 validation PASSED')
    print(f'3R symmetric max threshold split = {split:.3e}')
    print(f"2H material static window = {win.window_abs_deg:.6f} deg")
    print(f"2H material reverse k_perp,min = {hess[hess.direction=='reverse'].iloc[0].min_kperp_from_Hxx:.6f}")
    print(f'Thermal W50: {t5.W50_abs_deg:.6f} deg (T*=0.005), {t10.W50_abs_deg:.6f} deg (T*=0.010)')
    print(f'300 K energy-unit proxy min switching probability = {mins.min():.5f}')

if __name__ == '__main__':
    main()
