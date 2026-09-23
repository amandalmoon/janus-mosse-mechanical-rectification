"""EXP-001 Phase-0 reproducibility harness.

Scientific upstream is frozen by commit:
327c58e2684398ba7bc11205865f8222066c3539

The repository copies of the frozen VFF and GSFE source were verified byte-identical
on the EXP-001 branch at Phase-0 close. This harness keeps the Phase-0 dynamic
extension isolated from the N29 manuscript/results.

Scope: P0 implementation checks only. Do not use this file to perform or fit
scientific driven validation before the Phase-1 predictor freeze.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp
import numpy as np
from scipy.linalg import null_space
from scipy.optimize import minimize, root

ROOT = Path(__file__).resolve().parents[3]
GSFE_SRC = ROOT / "reproducibility" / "Janus_MoSSe_Current_ReproducibilityRelease_v2" / "source"
sys.path.insert(0, str(GSFE_SRC))
import janus_fourier_landscapes_v12 as J  # noqa: E402

THETA = 1.5
TSTAR = 0.01
ZETA_B = 1.0
SEEDS = (2026092301, 2026092302, 2026092303, 2026092304)


class VFFContact:
    """Dynamic extension of the frozen N29 nonlinear VFF conservative model."""

    def __init__(self, theta_deg=THETA, scale=1.0, a_ang=3.25, ks=5.289992, kt=2.334491):
        self.theta = float(theta_deg)
        self.scale = float(scale)
        self.a_ang = float(a_ang)
        self.ks = ks * scale
        self.kt = kt * scale
        self.land = J.dft_landscape("2H_MoSSe_Se-S-Se-S")
        self.E0 = float(self.land.energy_unit_meV)
        self.pos = np.asarray(J.make_hexagonal_flake(6), float)
        self.N = len(self.pos)
        R = J.rotation_matrix(self.theta)
        self.delta = self.pos @ R.T - self.pos

        C = np.zeros((3, 2 * self.N))
        C[0, 0::2] = 1
        C[1, 1::2] = 1
        C[2, 0::2] = -self.pos[:, 1]
        C[2, 1::2] = self.pos[:, 0]
        self.C = C
        self.Q = null_space(C)
        self.nint = self.Q.shape[1]
        self.ndof = 2 + self.nint

        bonds = []
        neigh = [[] for _ in range(self.N)]
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if abs(np.linalg.norm(self.pos[j] - self.pos[i]) - 1.0) < 1e-8:
                    bonds.append((i, j))
                    neigh[i].append(j)
                    neigh[j].append(i)
        angles = []
        for c in range(self.N):
            ns = neigh[c]
            for ia in range(len(ns)):
                for ib in range(ia + 1, len(ns)):
                    v1 = self.pos[ns[ia]] - self.pos[c]
                    v2 = self.pos[ns[ib]] - self.pos[c]
                    co = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                    th = np.degrees(np.arccos(np.clip(co, -1, 1)))
                    if abs(th - 60) < 1e-7:
                        angles.append((ns[ia], c, ns[ib]))
        assert len(bonds) == 342
        assert len(angles) == 648
        self.bonds = np.asarray(bonds, int)
        self.angles = np.asarray(angles, int)

        self.jQ = jnp.asarray(self.Q)
        self.jpos = jnp.asarray(self.pos)
        self.jdelta = jnp.asarray(self.delta)
        self.jb = jnp.asarray(self.bonds)
        self.ja = jnp.asarray(self.angles)
        self.jG = jnp.asarray(np.asarray(self.land.vectors, float))
        self.jcc = jnp.asarray(np.asarray(self.land.c_cos, float))
        self.jss = jnp.asarray(np.asarray(self.land.c_sin, float))

        def energy_per_site(z):
            q = z[:2]
            aa = z[2:]
            d = (self.jQ @ aa).reshape((self.N, 2))
            r = q[None, :] + self.jdelta + d
            ph = r @ self.jG.T
            Uloc = jnp.cos(ph) @ self.jcc + jnp.sin(ph) @ self.jss

            xp = self.a_ang * (self.jpos + d)
            bi, bj = self.jb[:, 0], self.jb[:, 1]
            dv = xp[bj] - xp[bi]
            ll = jnp.sqrt(jnp.sum(dv * dv, axis=1))
            Eb = 0.5 * self.ks * jnp.sum((ll - self.a_ang) ** 2)

            ai, ac, ak = self.ja[:, 0], self.ja[:, 1], self.ja[:, 2]
            v1, v2 = xp[ai] - xp[ac], xp[ak] - xp[ac]
            n1 = jnp.sqrt(jnp.sum(v1 * v1, axis=1))
            n2 = jnp.sqrt(jnp.sum(v2 * v2, axis=1))
            co = jnp.sum(v1 * v2, axis=1) / (n1 * n2)
            co = jnp.clip(co, -0.999999999999, 0.999999999999)
            th = jnp.arccos(co)
            Ea = 0.5 * self.kt * jnp.sum((th - jnp.pi / 3) ** 2)

            Eel = (Eb + Ea) * 1000.0 / (self.N * self.E0)
            return jnp.mean(Uloc) + Eel

        self.energy_per_site = energy_per_site
        self.vg = jax.jit(jax.value_and_grad(energy_per_site))
        self.hessian = jax.jit(jax.hessian(energy_per_site))

        def total_energy(q, a):
            return self.N * energy_per_site(jnp.concatenate([q, a]))

        self.total_energy = total_energy
        self.grad_a = jax.grad(total_energy, argnums=1)

    def eval(self, z, need_hessian=False):
        e, g = self.vg(jnp.asarray(z, float))
        H = self.hessian(jnp.asarray(z, float)) if need_hessian else None
        return float(e), np.asarray(g, float), None if H is None else np.asarray(H, float)


def uv_to_xy(uv):
    return np.column_stack([J.A1, J.A2]) @ np.asarray(uv, float)


def wrap_uv(xy):
    A = np.column_stack([J.A1, J.A2])
    u = np.linalg.solve(A, np.asarray(xy, float))
    return u - np.floor(u)


def periodic_distance(u, v):
    A = np.column_stack([J.A1, J.A2])
    d = np.asarray(u) - np.asarray(v)
    d -= np.round(d)
    return np.linalg.norm(A @ d)


def rigid_minima(theta, ngrid=15):
    land = J.dft_landscape("2H_MoSSe_Se-S-Se-S")
    S = J.contact_factors(theta, land.vectors, J.make_hexagonal_flake(6))
    roots = []
    for u in np.linspace(0, 1, ngrid, endpoint=False):
        for v in np.linspace(0, 1, ngrid, endpoint=False):
            x0 = uv_to_xy((u, v))
            fun = lambda xy: J.contact_ugh(float(xy[0]), float(xy[1]), S, land, 0, 0)[1]
            jac = lambda xy: J.contact_ugh(float(xy[0]), float(xy[1]), S, land, 0, 0)[2]
            rr = root(fun, x0, jac=jac, method="hybr", options={"xtol": 1e-11, "maxfev": 300})
            if np.linalg.norm(fun(rr.x)) > 1e-7:
                continue
            uv = wrap_uv(rr.x)
            if any(periodic_distance(uv, r["uv"]) < 2e-6 for r in roots):
                continue
            xy = uv_to_xy(uv)
            U, _, H = J.contact_ugh(float(xy[0]), float(xy[1]), S, land, 0, 0)
            roots.append({"uv": uv, "xy": xy, "U": U, "ev": np.linalg.eigvalsh(H)})
    return sorted((r for r in roots if r["ev"][0] > 1e-7), key=lambda r: r["U"])


def zero_ground(model):
    sols = []
    for i, r in enumerate(rigid_minima(model.theta)):
        z = np.zeros(model.ndof)
        z[:2] = r["xy"]
        fun = lambda zz: model.eval(zz, False)[0]
        jac = lambda zz: model.eval(zz, False)[1]
        rr = minimize(
            fun, z, jac=jac, method="L-BFGS-B",
            options={"ftol": 1e-14, "gtol": 2e-9, "maxiter": 1500, "maxls": 40, "maxcor": 20},
        )
        E, g, H = model.eval(rr.x, True)
        sols.append((E, i, rr.x.copy(), np.linalg.norm(g), np.linalg.eigvalsh(H), rr.success))
    return sorted(sols, key=lambda x: x[0])[0]


def mass_transform_error(model, qdot, adot):
    """Equal-site kinetic energy minus COM+internal-coordinate kinetic energy."""
    dv = (model.Q @ np.asarray(adot)).reshape(model.N, 2)
    site_v = np.asarray(qdot)[None, :] + dv
    direct = 0.5 * np.sum(site_v * site_v)
    reduced = 0.5 * model.N * np.dot(qdot, qdot) + 0.5 * np.dot(adot, adot)
    return float(direct - reduced)


def build_fixed_q_baoab(model, dt, zeta_b, temperature, total_steps):
    """Internal-only BAOAB process. The COM coordinate q is constrained."""
    grad_z = jax.grad(lambda z: model.N * model.energy_per_site(z))
    nint = model.nint
    c = math.exp(-zeta_b * dt)
    sigma = math.sqrt(temperature * (1 - c * c))

    @jax.jit
    def run(q, a0, v0, key):
        def one(carry, _):
            a, v, key = carry
            gz = grad_z(jnp.concatenate([q, a]))
            v = v - 0.5 * dt * gz[2:]
            a = a + 0.5 * dt * v

            key, sub = jax.random.split(key)
            v_before = v
            v = c * v + sigma * jax.random.normal(sub, (nint,), dtype=jnp.float64)
            heat = 0.5 * (jnp.dot(v, v) - jnp.dot(v_before, v_before))

            a = a + 0.5 * dt * v
            gz = grad_z(jnp.concatenate([q, a]))
            v = v - 0.5 * dt * gz[2:]
            q_force = -gz[:2]
            kinetic = 0.5 * jnp.dot(v, v)
            return (a, v, key), (q_force, kinetic, heat, jnp.mean(v * v))

        return jax.lax.scan(one, (a0, v0, key), xs=None, length=total_steps)

    return run


def recommended_phase0_dt(model, ground_z):
    """Same conservative rule used in the executed Phase-0 run."""
    Haa_total = model.N * model.eval(ground_z, True)[2][2:, 2:]
    omega_max = float(np.sqrt(max(np.linalg.eigvalsh(Haa_total).max(), 0.0)))
    return min(0.002, 0.05 / max(omega_max, 1e-12)), omega_max


if __name__ == "__main__":
    m = VFFContact()
    ground = zero_ground(m)
    dt, omega_max = recommended_phase0_dt(m, ground[2])
    print("N", m.N, "nint", m.nint, "dt", dt, "omega_max", omega_max)
    print("constraint residual", np.max(np.abs(m.C @ m.Q)))
    print("This harness intentionally stops before scientific driven validation.")
