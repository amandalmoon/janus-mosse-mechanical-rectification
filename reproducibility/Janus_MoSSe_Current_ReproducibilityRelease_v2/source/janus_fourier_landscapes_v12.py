"""General Fourier registry landscapes for phenomenological and literature-DFT Janus models.

The literature parameterization follows Angeli, Schleder & Kaxiras,
Phys. Rev. B 106, 235159 (2022), with the phase convention corrected in
Phys. Rev. B 109, 199902(E) (2024).  The GSFE is represented as

  Omega(r) = sum_l sum_j W_l exp[i g_j^l.r + i(-1)^j phi_l].

Pairing +/- reciprocal vectors and dividing by E0=6 W1 gives a real,
dimensionless three-vector representation per shell:

  u(r) = sum_l (W_l/(3 W1)) sum_{m=1}^3 cos(G_{l,m}.r + phi_l).

This module does not claim that the DFT data determine the dissipative
Langevin parameters.  It only replaces the local registry landscape.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import numpy as np

A1 = np.array([1.0, 0.0])
A2 = np.array([0.5, np.sqrt(3.0) / 2.0])
G0 = 4.0 * np.pi / np.sqrt(3.0)

# First shell used in the legacy manuscript. These are b2, -(b1+b2), b1.
SHELL1 = np.array([
    [0.0, G0],
    [-np.sqrt(3.0) / 2.0 * G0, -0.5 * G0],
    [ np.sqrt(3.0) / 2.0 * G0, -0.5 * G0],
], dtype=float)

# Second triangular-lattice reciprocal shell |G|=sqrt(3) G0.
# The three positive representatives are related by C3 and sum to zero.
SHELL2 = np.array([
    [np.sqrt(3.0) * G0, 0.0],
    [-0.5 * np.sqrt(3.0) * G0,  1.5 * G0],
    [-0.5 * np.sqrt(3.0) * G0, -1.5 * G0],
], dtype=float)

# Third shell |G|=2 G0.
SHELL3 = 2.0 * SHELL1
SHELLS = (SHELL1, SHELL2, SHELL3)


@dataclass(frozen=True)
class FourierLandscape:
    name: str
    vectors: np.ndarray        # (n_terms, 2)
    c_cos: np.ndarray          # coefficient multiplying cos(G.r)
    c_sin: np.ndarray          # coefficient multiplying sin(G.r)
    energy_unit_meV: float | None = None
    source_note: str = ""

    def potential(self, x, y):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        out = np.zeros(np.broadcast(x, y).shape, dtype=float)
        for G, c, s in zip(self.vectors, self.c_cos, self.c_sin):
            q = G[0] * x + G[1] * y
            out += c * np.cos(q) + s * np.sin(q)
        return out

    @property
    def n_terms(self):
        return len(self.c_cos)


def _from_shell_phase(name: str, W_meV, phi_deg, note: str = "") -> FourierLandscape:
    W = np.asarray(W_meV, dtype=float)
    phi = np.radians(np.asarray(phi_deg, dtype=float))
    if W.shape != (3,) or phi.shape != (3,):
        raise ValueError("W and phi must each have length three")
    if W[0] <= 0:
        raise ValueError("W1 must be positive for normalization")
    vectors = []
    cc = []
    ss = []
    # Omega/(6 W1) -> each paired cosine term has amplitude W_l/(3 W1).
    for shell, wl, ph in zip(SHELLS, W, phi):
        amp = wl / (3.0 * W[0])
        for G in shell:
            vectors.append(G)
            # cos(q + ph) = cos(ph) cos(q) - sin(ph) sin(q)
            cc.append(amp * math.cos(ph))
            ss.append(-amp * math.sin(ph))
    return FourierLandscape(
        name=name,
        vectors=np.asarray(vectors, dtype=float),
        c_cos=np.asarray(cc, dtype=float),
        c_sin=np.asarray(ss, dtype=float),
        energy_unit_meV=float(6.0 * W[0]),
        source_note=note,
    )


def phenomenological(a1_odd=0.4, a2_odd=0.4, name="phenomenological"):
    vectors = []
    cc = []
    ss = []
    for G in SHELL1:
        vectors.append(G); cc.append(-1.0/3.0); ss.append(a1_odd/3.0)
    for G in SHELL3:
        vectors.append(G); cc.append(0.0); ss.append(a2_odd/3.0)
    return FourierLandscape(name, np.asarray(vectors), np.asarray(cc), np.asarray(ss), None,
                            "Legacy dimensionless phenomenological landscape")


def symmetric_control():
    return phenomenological(0.0, 0.0, "phenomenological_symmetric")


# Published GSFE coefficients from Table II of Angeli et al. (2022),
# using the 2024 erratum phase convention. Only configurations used in v12
# are encoded here. Energies W_l are meV.
DFT_TABLE = {
    "3R_MoSSe_Se-S-Se-S": {
        "W": (8.7, 0.2, 0.1), "phi": (1.0, 0.2, 2.6),
        "note": "3R MoSSe asymmetric vertical ordering, Table II",
    },
    "3R_MoSSe_S-Se-Se-S": {
        "W": (7.4, 1.0, 0.1), "phi": (0.0, 180.0, 180.0),
        "note": "3R MoSSe symmetric vertical ordering, Table II",
    },
    "3R_MoSSe_Se-S-S-Se": {
        "W": (6.1, 0.2, 0.2), "phi": (0.0, 0.0, 0.0),
        "note": "3R MoSSe symmetric vertical ordering, Table II",
    },
    "2H_MoSSe_Se-S-Se-S": {
        "W": (7.9, 0.1, 0.1), "phi": (131.9, 1.2, 85.4),
        "note": "2H MoSSe asymmetric vertical ordering, Table II",
    },
}


def dft_landscape(key: str) -> FourierLandscape:
    d = DFT_TABLE[key]
    return _from_shell_phase(key, d["W"], d["phi"], d["note"])


def make_hexagonal_flake(shell=6):
    pts = []
    for q in range(-shell, shell + 1):
        for r in range(-shell, shell + 1):
            if max(abs(q), abs(r), abs(q + r)) <= shell:
                pts.append(q * A1 + r * A2)
    pts = np.asarray(pts, dtype=float)
    pts -= pts.mean(axis=0)
    return pts


def rotation_matrix(theta_deg):
    th = np.radians(theta_deg)
    return np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])


def contact_factors(theta_deg: float, vectors: np.ndarray, positions=None):
    if positions is None:
        positions = make_hexagonal_flake(6)
    R = rotation_matrix(theta_deg)
    delta = positions @ R.T - positions
    phases = delta @ np.asarray(vectors).T
    return np.mean(np.exp(1j * phases), axis=0)


def contact_ugh(x: float, y: float, factors: np.ndarray, landscape: FourierLandscape,
                k_perp: float = 0.0, force_y: float = 0.0):
    """Return guided contact potential, gradient and Hessian."""
    U = 0.0
    g = np.zeros(2, dtype=float)
    H = np.zeros((2, 2), dtype=float)
    for G, c, s, S in zip(landscape.vectors, landscape.c_cos, landscape.c_sin, factors):
        q = G[0] * x + G[1] * y
        z = S * np.exp(1j * q)
        re, im = z.real, z.imag
        U += c * re + s * im
        a = -c * im + s * re
        b = -c * re - s * im
        g += a * G
        H += b * np.outer(G, G)
    U += 0.5 * k_perp * x * x - force_y * y
    g[0] += k_perp * x
    g[1] -= force_y
    H[0, 0] += k_perp
    return float(U), g, H


def local_phase_diagnostics():
    rows = []
    for key, d in DFT_TABLE.items():
        W = np.asarray(d["W"], float)
        phi = np.asarray(d["phi"], float)
        for l in range(3):
            rad = np.radians(phi[l])
            rows.append({
                "configuration": key,
                "shell": l + 1,
                "G_over_G1": (1.0, np.sqrt(3.0), 2.0)[l],
                "W_meV": W[l],
                "phi_deg": phi[l],
                "even_origin_coeff_meV": W[l] * np.cos(rad),
                "odd_origin_coeff_meV": -W[l] * np.sin(rad),
                "abs_odd_over_abs_even": abs(np.tan(rad)) if abs(np.cos(rad)) > 1e-14 else np.inf,
                "chi_translation_invariant": np.sin(3.0 * rad),
                "W_over_W1": W[l] / W[0],
                "energy_unit_6W1_meV": 6.0 * W[0],
            })
    return rows


if __name__ == "__main__":
    import pandas as pd
    out = Path(__file__).resolve().parent.parent / "data" / "dft_fourier_phase_diagnostics_v12.csv"
    pd.DataFrame(local_phase_diagnostics()).to_csv(out, index=False)
    print(pd.DataFrame(local_phase_diagnostics()).to_string(index=False))
