"""Release validator for the v17 Janus MoSSe mechanical-rectification package."""
from __future__ import annotations
from pathlib import Path
import json
import math
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data" / "canonical"
REPORTS = ROOT / "reports"
sys.path.insert(0, str(HERE))
import janus_fourier_landscapes_v12 as J  # noqa: E402
import dft_guided_material_v12 as M  # noqa: E402

REFERENCE = {
    "theta_c_reverse_deg": 1.0099068387052377,
    "theta_c_forward_deg": 1.9444516264438518,
    "guided_window_deg": 0.9345447877386142,
    "rho_mean": 0.10328916625342521,
    "rho_std_sample": 0.0013642697166123072,
    "factorization_max_relerr_forward_percent": 0.24927494792070476,
    "factorization_max_relerr_reverse_percent": 0.30841598722172214,
    "odd_sector_slope": 2.8322126801610468,
    "odd_sector_R2": 0.99999984833088,
    "lambda_opt": 0.5,
    "DeltaFc_at_lambda_opt": 1.3786473706164728,
    "mode_map_points": 231,
    "mode_max_abs_winding": 6,
    "mode_reversal_mismatches": 0,
    "thermal_T_half": 0.053817314435530096,
    "thermal_T_half_CI_low": 0.05253507486816466,
    "thermal_T_half_CI_high": 0.05510670801431791,
}


def assert_close(name, got, expected, atol=5e-7, rtol=5e-7):
    if not math.isclose(float(got), float(expected), abs_tol=atol, rel_tol=rtol):
        raise AssertionError(f"{name}: got {got!r}, expected {expected!r}")


def finite_difference_audit():
    land = J.dft_landscape("2H_MoSSe_Se-S-Se-S")
    theta = 1.37
    factors = J.contact_factors(theta, land.vectors)
    x, y = 0.071, 0.432
    kp, force_y = 25.0, 1.4
    U, grad, H = J.contact_ugh(x, y, factors, land, kp, force_y)
    h = 1e-5
    def f(xx, yy): return J.contact_ugh(xx, yy, factors, land, kp, force_y)[0]
    gfd = np.array([(f(x+h,y)-f(x-h,y))/(2*h), (f(x,y+h)-f(x,y-h))/(2*h)])
    Hfd = np.empty((2,2), float)
    Hfd[0,0]=(f(x+h,y)-2*f(x,y)+f(x-h,y))/h**2
    Hfd[1,1]=(f(x,y+h)-2*f(x,y)+f(x,y-h))/h**2
    Hfd[0,1]=Hfd[1,0]=(f(x+h,y+h)-f(x+h,y-h)-f(x-h,y+h)+f(x-h,y-h))/(4*h*h)
    return {
        "gradient_max_abs_error": float(np.max(np.abs(grad-gfd))),
        "hessian_max_abs_error": float(np.max(np.abs(H-Hfd))),
        "hessian_symmetry_error": float(np.max(np.abs(H-H.T))),
    }


def main():
    metrics_path = REPORTS / "MANUSCRIPT_NUMERIC_METRICS.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    for k, v in REFERENCE.items():
        if isinstance(v, int):
            if int(metrics[k]) != v:
                raise AssertionError(f"{k}: got {metrics[k]}, expected {v}")
        else:
            assert_close(k, metrics[k], v)

    mode = pd.read_csv(DATA / "v15_mode_locking_reversal_check.csv")
    if len(mode) != 231:
        raise AssertionError(f"mode map has {len(mode)} rows, expected 231")
    if int(mode.integer_reversal_mismatch.astype(bool).sum()) != 0:
        raise AssertionError("odd-sector reversal mismatch found")
    if float(mode.locking_error.max()) >= 1e-4:
        raise AssertionError("integer locking tolerance failed")

    lambda_winding = pd.read_csv(DATA / "v17_lambda_winding.csv").sort_values("lambda").reset_index(drop=True)
    if len(lambda_winding) != 21:
        raise AssertionError(f"lambda winding scan has {len(lambda_winding)} rows, expected 21")
    rev_lw = lambda_winding.iloc[::-1].reset_index(drop=True)
    if int(np.sum(lambda_winding.winding_integer.to_numpy() != -rev_lw.winding_integer.to_numpy())) != 0:
        raise AssertionError("lambda winding staircase is not inversion-antisymmetric")
    if float(lambda_winding.locking_error.max()) >= 1e-4:
        raise AssertionError("lambda winding integer-locking tolerance failed")
    zero = lambda_winding.loc[np.isclose(lambda_winding["lambda"], 0.0)].iloc[0]
    if int(zero.winding_integer) != 0:
        raise AssertionError("lambda=0 winding must vanish")

    thermal = pd.read_csv(DATA / "v15_thermal_midwindow_fidelity.csv")
    expected_D = {0.01:0.987, 0.02:0.919, 0.05:0.501, 0.10:0.147, 0.16:0.032}
    for T, D in expected_D.items():
        got=float(thermal.loc[np.isclose(thermal.T_star,T),"D"].iloc[0])
        assert_close(f"D({T})", got, D, atol=1e-12, rtol=0)

    sym = J.dft_landscape("3R_MoSSe_S-Se-Se-S")
    splits=[]
    for theta in (0.0, 0.75, 1.5, 2.25, 3.0):
        fp=M.guided_threshold(theta,sym,+1,25.0)["Fc"]
        fr=M.guided_threshold(theta,sym,-1,25.0)["Fc"]
        splits.append(abs(fp-fr))
    audit=finite_difference_audit()
    audit["symmetric_control_max_threshold_split"] = float(max(splits))
    (REPORTS / "PHYSICS_SELF_AUDIT.json").write_text(json.dumps(audit,indent=2),encoding="utf-8")

    if audit["gradient_max_abs_error"] > 5e-7:
        raise AssertionError(audit)
    if audit["hessian_max_abs_error"] > 5e-5:
        raise AssertionError(audit)
    if audit["symmetric_control_max_threshold_split"] > 1e-10:
        raise AssertionError(audit)

    print("v17 release validation: PASS")
    print(json.dumps(audit, indent=2))

if __name__ == "__main__":
    main()
