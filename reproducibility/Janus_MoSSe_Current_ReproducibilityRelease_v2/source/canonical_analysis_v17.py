"""Canonical v17 numerical analysis for the Janus MoSSe mechanical rectifier.

This module is a clean rebuild from the surviving v12 published-GSFE engine.
It does not claim to recover the lost v14 implementation.  Production settings
are frozen in ``config/production.json`` and outputs are written to
``data/canonical``.

The heavy stages (231-point mode map and 1000-trajectory thermal fidelity scan)
are deterministic given the frozen configuration but may take substantial CPU
time.  The provided release already contains the completed canonical outputs.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import argparse
import json
import math
import sys

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit, minimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONFIG_PATH = ROOT / "config" / "production.json"
DATA = ROOT / "data" / "canonical"
REPORTS = ROOT / "reports"
DATA.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(HERE))
import janus_fourier_landscapes_v12 as J  # noqa: E402
import dft_guided_material_v12 as M  # noqa: E402


def load_config(path: Path = CONFIG_PATH) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def odd_scaled_landscape(base: J.FourierLandscape, lam: float, name: str | None = None) -> J.FourierLandscape:
    """Scale only the inversion-odd sine coefficients of a Fourier landscape."""
    return replace(
        base,
        name=name or f"{base.name}_oddscale_{lam:+.6f}",
        c_sin=np.asarray(base.c_sin, float) * float(lam),
    )


def crossing_linear(theta, values, level: float) -> list[float]:
    theta = np.asarray(theta, float)
    values = np.asarray(values, float)
    d = values - level
    roots: list[float] = []
    for i in range(len(theta) - 1):
        if d[i] == 0:
            roots.append(float(theta[i]))
        if d[i] * d[i + 1] < 0:
            roots.append(float(theta[i] + (theta[i + 1] - theta[i]) * (-d[i]) / (d[i + 1] - d[i])))
    return roots


def logistic_probability(theta, theta50, width):
    z = np.clip((np.asarray(theta, float) - theta50) / width, -50, 50)
    return 1.0 / (1.0 + np.exp(-z))


def fit_binomial_logistic(theta, escapes, n):
    x = np.asarray(theta, float)
    k = np.asarray(escapes, float)
    n = np.asarray(n, float)
    p = k / n
    x0 = float(x[np.argmin(np.abs(p - 0.5))])

    def nll(q):
        xc, logw = q
        width = math.exp(logw)
        pp = np.clip(logistic_probability(x, xc, width), 1e-10, 1 - 1e-10)
        return float(-np.sum(k * np.log(pp) + (n - k) * np.log(1 - pp)))

    res = minimize(
        nll,
        [x0, math.log(0.08)],
        method="L-BFGS-B",
        bounds=[(x.min() - 0.3, x.max() + 0.3), (math.log(0.003), math.log(0.6))],
    )
    if not res.success:
        raise RuntimeError(res.message)
    return float(res.x[0]), float(math.exp(res.x[1])), float(res.fun)


def fit_fidelity_sigmoid(T, D):
    T = np.asarray(T, float)
    D = np.asarray(D, float)

    def model(t, t50, width):
        return 1.0 / (1.0 + np.exp((t - t50) / width))

    popt, _ = curve_fit(
        model,
        T,
        D,
        p0=[0.054, 0.018],
        bounds=([0.0, 0.001], [0.2, 0.2]),
        maxfev=10000,
    )
    fit = model(T, *popt)
    r2 = 1.0 - np.sum((D - fit) ** 2) / np.sum((D - D.mean()) ** 2)
    return float(popt[0]), float(popt[1]), float(r2), fit


def stage_static(cfg: dict) -> dict:
    material = J.dft_landscape(cfg["material_key"])
    sym = J.dft_landscape(cfg["symmetric_control_key"])
    kp = float(cfg["k_perp"])
    f0 = float(cfg["F0_static_cut"])
    thetas = np.arange(cfg["theta_min_deg"], cfg["theta_max_deg"] + 0.5 * cfg["theta_step_deg"], cfg["theta_step_deg"])

    pd.DataFrame(J.local_phase_diagnostics()).to_csv(DATA / "v15_material_fourier_phase_diagnostics.csv", index=False)
    curves = M.threshold_curves(material, thetas, kp=kp)
    curves.to_csv(DATA / "v15_material_threshold_curves.csv", index=False)

    piv = curves.pivot(index="theta_deg", columns="direction", values="Fc").reset_index()
    roots = {}
    for direction in ("forward", "reverse"):
        roots[direction] = crossing_linear(piv.theta_deg, piv[direction], f0)[0]

    hrows = []
    for direction, sgn in (("forward", +1), ("reverse", -1)):
        r = M.guided_threshold(roots[direction], material, sgn, kp, ngrid=12000)
        r["k_perp"] = kp
        r["Hxx_unguided_local"] = r["Hxx"] - kp
        r["k_perp_required_local"] = max(0.0, -r["Hxx_unguided_local"])
        hrows.append(r)
    hdf = pd.DataFrame(hrows)
    hdf.to_csv(DATA / "v15_material_fullhessian_at_crossings.csv", index=False)

    # Symmetric-control null test.
    control_rows = []
    for th in np.arange(0.0, 3.0001, 0.25):
        fp = M.guided_threshold(float(th), sym, +1, kp)["Fc"]
        fm = M.guided_threshold(float(th), sym, -1, kp)["Fc"]
        control_rows.append({"theta_deg": th, "Fc_forward": fp, "Fc_reverse": fm, "split": fp - fm})
    pd.DataFrame(control_rows).to_csv(DATA / "v17_symmetric_control_thresholds.csv", index=False)

    return {
        "theta_c_forward_deg": roots["forward"],
        "theta_c_reverse_deg": roots["reverse"],
        "guided_window_deg": abs(roots["forward"] - roots["reverse"]),
        "DFT_energy_unit_meV": material.energy_unit_meV,
        "DFT_chi1": abs(math.sin(math.radians(3.0 * J.DFT_TABLE[cfg["material_key"]]["phi"][0]))),
        "forward_nonsoft_Hessian_eigenvalue": float(hdf[hdf.direction == "forward"].iloc[0].eig_hard),
        "reverse_nonsoft_Hessian_eigenvalue": float(hdf[hdf.direction == "reverse"].iloc[0].eig_hard),
        "forward_kperp_required_at_crossing": float(hdf[hdf.direction == "forward"].iloc[0].k_perp_required_local),
        "reverse_kperp_required_at_crossing": float(hdf[hdf.direction == "reverse"].iloc[0].k_perp_required_local),
    }


def stage_factorization_and_confinement(cfg: dict) -> dict:
    curves = pd.read_csv(DATA / "v15_material_threshold_curves.csv")
    piv = curves.pivot(index="theta_deg", columns="direction", values="Fc").reset_index().sort_values("theta_deg")
    fc_mean = 0.5 * (piv.forward + piv.reverse)
    rho = (piv.forward - piv.reverse) / (piv.forward + piv.reverse)
    rhobar = float(rho.mean())
    fact_f = fc_mean * (1.0 + rhobar)
    fact_r = fc_mean * (1.0 - rhobar)
    rel_f = np.abs(fact_f - piv.forward) / np.abs(piv.forward)
    rel_r = np.abs(fact_r - piv.reverse) / np.abs(piv.reverse)
    out = pd.DataFrame({
        "theta_deg": piv.theta_deg,
        "Fc_forward": piv.forward,
        "Fc_reverse": piv.reverse,
        "Fc_mean": fc_mean,
        "rho": rho,
        "Fc_forward_factorized": fact_f,
        "Fc_reverse_factorized": fact_r,
        "relerr_forward": rel_f,
        "relerr_reverse": rel_r,
    })
    out.to_csv(DATA / "v15_force_twist_factorization.csv", index=False)
    band_area = float(np.trapezoid(np.abs(piv.forward - piv.reverse), piv.theta_deg))

    kp = float(cfg["k_perp"])
    conf_rows = []
    material = J.dft_landscape(cfg["material_key"])
    for th in piv.theta_deg.to_numpy(float):
        for direction, sgn in (("forward", +1), ("reverse", -1)):
            r = M.guided_threshold(float(th), material, sgn, kp)
            unguided_hxx = r["Hxx"] - kp
            conf_rows.append({
                "theta_deg": th,
                "direction": direction,
                "k_perp_required_local": max(0.0, -unguided_hxx),
                "Hxx_unguided": unguided_hxx,
                "Hxy_unguided": r["Hxy"],
                "Hyy_unguided": r["Hyy"],
            })
    conf = pd.DataFrame(conf_rows)
    conf.to_csv(DATA / "v15_confinement_stability_map.csv", index=False)

    return {
        "rho_mean": rhobar,
        "rho_std_sample": float(rho.std(ddof=1)),
        "factorization_max_relerr_forward_percent": float(100.0 * rel_f.max()),
        "factorization_max_relerr_reverse_percent": float(100.0 * rel_r.max()),
        "band_area_force_deg": band_area,
        "confinement_forward_kreq_min": float(conf[conf.direction == "forward"].k_perp_required_local.min()),
        "confinement_forward_kreq_max": float(conf[conf.direction == "forward"].k_perp_required_local.max()),
        "confinement_reverse_kreq_min": float(conf[conf.direction == "reverse"].k_perp_required_local.min()),
        "confinement_reverse_kreq_max": float(conf[conf.direction == "reverse"].k_perp_required_local.max()),
    }


def stage_odd_sector(cfg: dict) -> dict:
    material = J.dft_landscape(cfg["material_key"])
    theta = float(cfg["odd_sector_theta_deg"])
    kp = float(cfg["k_perp"])
    # Production grid: coarse 0.025 outside |lambda|<=0.15 and dense 0.0025 inside.
    coarse = float(cfg["lambda_step"])
    dense = float(cfg.get("lambda_dense_step", 0.0025))
    half = float(cfg.get("lambda_dense_halfwidth", 0.15))
    left = np.arange(float(cfg["lambda_min"]), -half - 0.5 * coarse, coarse)
    center = np.arange(-half, half + 0.5 * dense, dense)
    right = np.arange(half + coarse, float(cfg["lambda_max"]) + 0.5 * coarse, coarse)
    lambdas = np.concatenate([left, center, right])
    rows = []
    for lam in lambdas:
        land = odd_scaled_landscape(material, float(lam))
        ff = M.guided_threshold(theta, land, +1, kp)["Fc"]
        fr = M.guided_threshold(theta, land, -1, kp)["Fc"]
        delta = ff - fr
        rows.append({"lambda": lam, "Fc_forward": ff, "Fc_reverse": fr, "DeltaFc": delta,
                     "rho": delta / (ff + fr)})
    df = pd.DataFrame(rows)
    df.to_csv(DATA / "v15_odd_sector_scaling.csv", index=False)

    local = df[np.abs(df["lambda"]) <= 0.1500001]
    x = local["lambda"].to_numpy(float)
    y = local["DeltaFc"].to_numpy(float)
    slope = float(np.dot(x, y) / np.dot(x, x))
    fit = slope * x
    r2 = float(1.0 - np.sum((y - fit) ** 2) / np.sum((y - y.mean()) ** 2))
    opt = df.iloc[int(np.argmax(np.abs(df.DeltaFc.to_numpy(float))))]
    # The manuscript reports the positive-lambda local maximum; choose it explicitly.
    positive = df[df["lambda"] >= 0]
    opt = positive.iloc[int(np.argmax(positive.DeltaFc.to_numpy(float)))]
    return {
        "odd_sector_slope": slope,
        "odd_sector_R2": r2,
        "lambda_opt": float(opt["lambda"]),
        "DeltaFc_at_lambda_opt": float(opt.DeltaFc),
        "rho_at_lambda_opt": float(opt.rho),
    }



def stage_lambda_winding(cfg: dict) -> dict:
    """Rebuild the Figure-8(d) odd-sector winding staircase at the fixed drive point."""
    material = J.dft_landscape(cfg["material_key"])
    theta = float(cfg["mode_theta_deg"])
    kp = float(cfg["k_perp"])
    f0 = float(cfg["lambda_winding_F0"])
    period = float(cfg["lambda_winding_period"])
    n_eq = int(cfg["mode_transient_cycles"])
    n_meas = int(cfg["mode_measured_cycles"])
    spc = int(cfg["mode_steps_per_cycle"])
    rows = []
    for lam in cfg["lambda_winding_values"]:
        lam = float(lam)
        land = odd_scaled_landscape(material, lam)
        arr = M._arrays(theta, land)
        x0, y0 = M.zero_minimum(theta, land, kp)
        vel, cyc, xf, yf = M._rk4_run(*arr, f0, period, n_eq, n_meas, spc, kp, x0, y0)
        n = int(round(cyc))
        rows.append({
            "lambda": lam,
            "theta_deg": theta,
            "F0": f0,
            "period": period,
            "k_perp": kp,
            "n_eq": n_eq,
            "n_meas": n_meas,
            "steps_per_cycle": spc,
            "mean_velocity": vel,
            "periods_per_cycle": cyc,
            "winding_integer": n,
            "locking_error": abs(cyc - n),
            "x_final": xf,
            "y_final": yf,
        })
    df = pd.DataFrame(rows).sort_values("lambda").reset_index(drop=True)
    df.to_csv(DATA / "v17_lambda_winding.csv", index=False)
    # Because lambda -> -lambda exactly reverses the inversion-odd sector, the
    # fixed-drive winding staircase should be antisymmetric up to numerical error.
    rev = df.iloc[::-1].reset_index(drop=True)
    symmetry_err = float(np.max(np.abs(df.periods_per_cycle.to_numpy() + rev.periods_per_cycle.to_numpy())))
    mismatch = int(np.sum(df.winding_integer.to_numpy() != -rev.winding_integer.to_numpy()))
    return {
        "lambda_winding_points": int(len(df)),
        "lambda_winding_max_abs_winding": int(np.max(np.abs(df.winding_integer))),
        "lambda_winding_reversal_mismatches": mismatch,
        "lambda_winding_max_reversal_error": symmetry_err,
    }

def _mode_map_for_landscape(cfg: dict, land: J.FourierLandscape) -> pd.DataFrame:
    theta = float(cfg["mode_theta_deg"])
    kp = float(cfg["k_perp"])
    n_eq = int(cfg["mode_transient_cycles"])
    n_meas = int(cfg["mode_measured_cycles"])
    spc = int(cfg["mode_steps_per_cycle"])
    arr = M._arrays(theta, land)
    x0, y0 = M.zero_minimum(theta, land, kp)
    rows = []
    for amp in cfg["mode_amplitudes"]:
        for period in cfg["mode_periods"]:
            vel, cyc, xf, yf = M._rk4_run(*arr, float(amp), float(period), n_eq, n_meas, spc, kp, x0, y0)
            winding = int(round(cyc))
            rows.append({
                "theta_deg": theta, "F0": amp, "period": period, "k_perp": kp,
                "n_eq": n_eq, "n_meas": n_meas, "steps_per_cycle": spc,
                "mean_velocity": vel, "periods_per_cycle": cyc,
                "winding_integer": winding, "locking_error": abs(cyc - winding),
                "x_final": xf, "y_final": yf,
            })
    return pd.DataFrame(rows)


def stage_mode_locking(cfg: dict) -> dict:
    material = J.dft_landscape(cfg["material_key"])
    base = _mode_map_for_landscape(cfg, material)
    rev = _mode_map_for_landscape(cfg, odd_scaled_landscape(material, -1.0, material.name + "_odd_reversed"))
    base.to_csv(DATA / "v15_mode_locking_base_map.csv", index=False)
    rev.to_csv(DATA / "v15_mode_locking_reversed_map.csv", index=False)
    chk = base.copy()
    chk["periods_per_cycle_odd_reversed"] = rev.periods_per_cycle.to_numpy()
    chk["winding_integer_odd_reversed"] = rev.winding_integer.to_numpy()
    chk["locking_error_odd_reversed"] = rev.locking_error.to_numpy()
    chk["integer_reversal_mismatch"] = chk.winding_integer_odd_reversed.to_numpy() != -chk.winding_integer.to_numpy()
    chk["reversal_symmetry_error"] = np.abs(chk.periods_per_cycle_odd_reversed + chk.periods_per_cycle)
    chk.to_csv(DATA / "v15_mode_locking_reversal_check.csv", index=False)
    return {
        "mode_map_points": int(len(base)),
        "mode_max_abs_winding": int(np.max(np.abs(base.winding_integer))),
        "mode_max_locking_error": float(base.locking_error.max()),
        "mode_reversal_mismatches": int(chk.integer_reversal_mismatch.sum()),
        "mode_max_reversal_symmetry_error": float(chk.reversal_symmetry_error.max()),
    }


def stage_low_noise(cfg: dict) -> dict:
    material = J.dft_landscape(cfg["material_key"])
    thetas = np.asarray(cfg["low_noise_thetas_deg"], float)
    temps = tuple(float(x) for x in cfg["low_noise_temperatures"])
    ntraj = int(cfg["low_noise_ntraj"])
    df, _ = M.thermal_switching(material, thetas, float(cfg["F0_static_cut"]), temps=temps,
                                ntraj=ntraj, period=40.0, dt=float(cfg["thermal_dt"]), kp=float(cfg["k_perp"]))
    df.to_csv(DATA / "v15_low_noise_switching.csv", index=False)

    rng = np.random.default_rng(int(cfg["baoab_base_seed"]) + 900000)
    fitrows, boot_theta = [], {}
    B = int(cfg["bootstrap_refits"])
    for (T, direction), g in df.groupby(["T_star", "direction"], sort=True):
        g = g.sort_values("theta_deg")
        x = g.theta_deg.to_numpy(float); k = g.escaped.to_numpy(int); n = g.n.to_numpy(int)
        xc, width, nll = fit_binomial_logistic(x, k, n)
        p = k / n
        boots = []
        for _ in range(B):
            kb = rng.binomial(n, p)
            try:
                boots.append(fit_binomial_logistic(x, kb, n)[:2])
            except Exception:
                pass
        boots = np.asarray(boots, float)
        lo, hi = np.quantile(boots[:, 0], [0.025, 0.975])
        fitrows.append({"T_star": T, "direction": direction, "theta50_deg": xc, "width_deg": width,
                        "theta50_ci_low": lo, "theta50_ci_high": hi, "n_boot_ok": len(boots), "negloglik": nll})
        boot_theta[(T, direction)] = boots[:, 0]
    fits = pd.DataFrame(fitrows)
    fits.to_csv(DATA / "v15_low_noise_switching_logistic.csv", index=False)

    rows = []
    for T in sorted(fits.T_star.unique()):
        f = fits[(fits.T_star == T) & (fits.direction == "forward")].iloc[0]
        r = fits[(fits.T_star == T) & (fits.direction == "reverse")].iloc[0]
        bf = boot_theta[(T, "forward")]; br = boot_theta[(T, "reverse")]
        m = min(len(bf), len(br)); wb = np.abs(bf[:m] - br[:m])
        lo, hi = np.quantile(wb, [0.025, 0.975])
        rows.append({"T_star": T, "theta50_forward_deg": f.theta50_deg,
                     "theta50_reverse_deg": r.theta50_deg,
                     "W50_abs_deg": abs(f.theta50_deg - r.theta50_deg),
                     "W50_ci_low": lo, "W50_ci_high": hi})
    windows = pd.DataFrame(rows)
    windows.to_csv(DATA / "v15_low_noise_diode_windows.csv", index=False)
    metrics = {}
    for T in temps:
        row = windows[np.isclose(windows.T_star, T)].iloc[0]
        metrics[f"low_noise_W50_T{T:.3f}"] = float(row.W50_abs_deg)
    return metrics


def stage_thermal_fidelity(cfg: dict) -> dict:
    material = J.dft_landscape(cfg["material_key"])
    theta = float(cfg["thermal_mid_theta_deg"])
    kp = float(cfg["k_perp"])
    arr = M._arrays(theta, material)
    x0, y0 = M.zero_minimum(theta, material, kp)
    ntraj = int(cfg["thermal_ntraj_per_direction"])
    base_seed = int(cfg["baoab_base_seed"])
    temperatures = [float(x) for x in cfg["thermal_temperatures"]]
    rows = []
    for ti, T in enumerate(temperatures):
        counts = {}
        for direction in (+1, -1):
            seed = base_seed + 100000 * ti + (0 if direction > 0 else 500)
            shifts = M._baoab_halfcycle(ntraj, seed, x0, y0, direction, T, *arr,
                                        float(cfg["F0_static_cut"]), float(cfg["thermal_half_period"]),
                                        float(cfg["thermal_dt"]), kp, float(cfg["thermal_preeq"]))
            counts[direction] = int(np.sum((shifts * direction) > 0))
        pf = counts[+1] / ntraj; pr = counts[-1] / ntraj; Dval = abs(pf - pr)
        rows.append({"T_star": T, "p_forward": pf, "p_reverse": pr, "D": Dval,
                     "k_forward": counts[+1], "k_reverse": counts[-1],
                     "n_forward": ntraj, "n_reverse": ntraj})
    df = pd.DataFrame(rows)
    t50, width, r2, fit = fit_fidelity_sigmoid(df.T_star.to_numpy(), df.D.to_numpy())
    df["D_fit"] = fit
    df.to_csv(DATA / "v15_thermal_midwindow_fidelity.csv", index=False)

    rng = np.random.default_rng(int(cfg["bootstrap_seed"]))
    B = int(cfg["bootstrap_refits"])
    pf = df.p_forward.to_numpy(); pr = df.p_reverse.to_numpy(); T = df.T_star.to_numpy()
    vals = []
    for _ in range(B):
        kf = rng.binomial(ntraj, pf); kr = rng.binomial(ntraj, pr)
        Db = np.abs(kf / ntraj - kr / ntraj)
        try:
            bt50, _, _, _ = fit_fidelity_sigmoid(T, Db)
            vals.append(bt50)
        except Exception:
            pass
    vals = np.asarray(vals, float)
    lo, hi = np.quantile(vals, [0.025, 0.975])
    fit_df = pd.DataFrame([{
        "theta_mid_deg": theta, "T50": t50, "width": width, "R2": r2,
        "ci_low": lo, "ci_high": hi,
        "ntraj_per_direction_per_temperature": ntraj,
        "n_bootstrap_success": len(vals), "seed_baoab_base": base_seed,
        "seed_bootstrap": int(cfg["bootstrap_seed"]),
    }])
    fit_df.to_csv(DATA / "v15_thermal_fidelity_fit.csv", index=False)
    reps = {str(T): float(df.loc[np.isclose(df.T_star, T), "D"].iloc[0]) for T in (0.01, 0.02, 0.05, 0.1, 0.16)}
    return {
        "thermal_D_representative": reps,
        "thermal_T_half": t50,
        "thermal_T_half_CI_low": float(lo),
        "thermal_T_half_CI_high": float(hi),
        "thermal_fit_R2": r2,
    }


def run(stages: set[str]) -> dict:
    cfg = load_config()
    metrics: dict = {}
    if "static" in stages:
        metrics.update(stage_static(cfg))
    if "factorization" in stages:
        if not (DATA / "v15_material_threshold_curves.csv").exists():
            metrics.update(stage_static(cfg))
        metrics.update(stage_factorization_and_confinement(cfg))
    if "odd" in stages:
        metrics.update(stage_odd_sector(cfg))
    if "lambda_winding" in stages:
        metrics.update(stage_lambda_winding(cfg))
    if "mode" in stages:
        metrics.update(stage_mode_locking(cfg))
    if "low_noise" in stages:
        metrics.update(stage_low_noise(cfg))
    if "thermal" in stages:
        metrics.update(stage_thermal_fidelity(cfg))
    if metrics:
        path = REPORTS / "CANONICAL_RUN_PARTIAL_METRICS.json"
        path.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", action="append", choices=["static", "factorization", "odd", "lambda_winding", "mode", "low_noise", "thermal"])
    parser.add_argument("--all", action="store_true", help="Run every canonical stage, including expensive stochastic calculations")
    args = parser.parse_args()
    stages = set(args.stage or [])
    if args.all:
        stages = {"static", "factorization", "odd", "lambda_winding", "mode", "low_noise", "thermal"}
    if not stages:
        stages = {"static", "factorization", "odd"}
    metrics = run(stages)
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
