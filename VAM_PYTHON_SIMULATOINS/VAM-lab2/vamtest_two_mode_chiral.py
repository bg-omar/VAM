
import numpy as np
import math
import matplotlib.pyplot as plt

from test_base import BaseTest

def dagger(A): return A.conj().T
def kron(*ops):
    out = np.array([[1]], dtype=complex)
    for A in ops: out = np.kron(out, A)
    return out

def lindblad(cops, rho):
    acc = np.zeros_like(rho, dtype=complex)
    for L in cops:
        LdL = dagger(L) @ L
        acc += L @ rho @ dagger(L) - 0.5*(LdL @ rho + rho @ LdL)
    return acc

def rk4_step(rho, dt, H, c_ops):
    def rhs(r): return -1j*(H@r - r@H) + lindblad(c_ops, r)
    k1 = rhs(r); k2 = rhs(r + 0.5*dt*k1); k3 = rhs(r + 0.5*dt*k2); k4 = rhs(r + dt*k3)
    return rho + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

def boson_ops(N):
    a = np.zeros((N,N), dtype=complex)
    for n in range(1,N): a[n-1,n] = math.sqrt(n)
    adag = a.conj().T
    n = adag@a
    return a, adag, n, np.eye(N, dtype=complex)

def two_level_ops():
    sz = np.array([[1,0],[0,-1]], dtype=complex)
    sp = np.array([[0,1],[0,0]], dtype=complex)
    sm = np.array([[0,0],[1,0]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    return sz, sp, sm, I2

class TwoModeChiral(BaseTest):
    name = "Two-Mode Swirl with Chirality"
    description = ("Electron coupled to two near-degenerate swirl modes (Ω1, Ω2=Ω1+δ) "
                   "with chiral mixing φ. Shows coherence-channel heat bump vs detuning and nonreciprocity.")

    def default_params(self):
        return dict(
            Nb=6, Delta=1.0, Omega1=1.0, delta=0.05, g1=0.07, g2=0.07,
            kappa1=0.02, kappa2=0.02, n_th=0.2, gamma_rel=0.004, gamma_phi=0.002,
            V12=0.02, phi=0.3, t_max=400.0, dt=0.5, sweep_delta=False
        )

    def build_H_and_cops(self, p):
        Nb = int(p["Nb"])
        sz, sp, sm, I2 = two_level_ops()
        a1, a1d, n1, IN = boson_ops(Nb)
        a2, a2d, n2, _  = boson_ops(Nb)

        # Spaces: qubit ⊗ b1 ⊗ b2
        szF = kron(sz, IN, IN); spF = kron(sp, IN, IN); smF = kron(sm, IN, IN)
        a1F = kron(I2, a1, IN); a1dF = kron(I2, a1d, IN); n1F = kron(I2, n1, IN)
        a2F = kron(I2, IN, a2); a2dF = kron(I2, IN, a2d); n2F = kron(I2, IN, n2)

        Delta = float(p["Delta"]); Omega1=float(p["Omega1"]); delta=float(p["delta"])
        g1=float(p["g1"]); g2=float(p["g2"]); V12=float(p["V12"]); phi=float(p["phi"])

        H = 0.5*Delta*szF + Omega1*n1F + (Omega1+delta)*n2F \
            + g1*(spF@a1F + smF@a1dF) + g2*(spF@a2F + smF@a2dF) \
            + V12*(np.exp(1j*phi)*a1dF@a2F + np.exp(-1j*phi)*a2dF@a1F)

        c_ops = []
        k1=float(p["kappa1"]); k2=float(p["kappa2"]); nth=float(p["n_th"])
        gr=float(p["gamma_rel"]); gp=float(p["gamma_phi"])
        if k1>0:
            c_ops.append(math.sqrt(k1*(nth+1))*a1F)
            if nth>0: c_ops.append(math.sqrt(k1*nth)*a1dF)
        if k2>0:
            c_ops.append(math.sqrt(k2*(nth+1))*a2F)
            if nth>0: c_ops.append(math.sqrt(k2*nth)*a2dF)
        if gr>0: c_ops.append(math.sqrt(gr)*smF)
        if gp>0: c_ops.append(math.sqrt(gp/2.0)*szF)

        return H, c_ops, {"n1F":n1F, "n2F":n2F, "a1F":a1F, "a2F":a2F}

    def run_once(self, p):
        Nb = int(p["Nb"])
        H, c_ops, ops = self.build_H_and_cops(p)

        # Initial |e,0,0>
        e = np.array([1,0], dtype=complex)
        vac = np.zeros((Nb,), dtype=complex); vac[0]=1.0
        psi0 = kron(e, vac, vac)
        rho = np.outer(psi0, psi0.conj())

        t_max=float(p["t_max"]); dt=float(p["dt"])
        times = np.arange(0.0, t_max+dt, dt)

        n1_series, n2_series = [], []
        for t in times:
            n1_series.append(float(np.trace(ops["n1F"]@rho).real))
            n2_series.append(float(np.trace(ops["n2F"]@rho).real))
            rho = rk4_step(rho, dt, H, c_ops)

        return times, n1_series, n2_series

    def run(self, params, figure):
        sweep = bool(params.get("sweep_delta", False))
        if not sweep:
            times, n1, n2 = self.run_once(params)
            figure.clf()
            ax = figure.add_subplot(111)
            ax.plot(times, n1, label="n1")
            ax.plot(times, n2, label="n2")
            ax.set_xlabel("time"); ax.set_ylabel("occupancy")
            ax.set_title("Two-mode swirl occupancies")
            ax.legend()
            figure.tight_layout()
            return {"times": times.tolist(), "n1": n1, "n2": n2}
        else:
            # Sweep δ to show Lorentzian-like coherence bump: integrate early-time energy in mode-2
            deltas = np.linspace(-0.2, 0.2, 41)
            bump = []
            for d in deltas:
                p2 = dict(params); p2["delta"]=float(d)
                times, n1, n2 = self.run_once(p2)
                # measure integrated occupancy of mode-2 over an initial window
                idx = int(min(len(times)-1, max(5, 60)))
                bump.append(float(np.trapz(n2[:idx], times[:idx])))
            figure.clf()
            ax = figure.add_subplot(111)
            ax.plot(deltas, bump, label="coherence heat proxy")
            ax.set_xlabel("detuning δ"); ax.set_ylabel("∫ n2 dt (early)")
            ax.set_title("Coherence-channel bump vs detuning")
            ax.legend()
            figure.tight_layout()
            return {"delta": deltas.tolist(), "bump": bump}

TEST_CLASS = TwoModeChiral
