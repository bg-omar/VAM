
import numpy as np
import math
import matplotlib.pyplot as plt

from test_base import BaseTest

def dagger(A): return A.conj().T
def comm(A,B): return A @ B - B @ A

def boson_ops(N):
    a = np.zeros((N,N), dtype=complex)
    for n in range(1,N):
        a[n-1,n] = math.sqrt(n)
    adag = a.conj().T
    n_op = adag @ a
    return a, adag, n_op, np.eye(N, dtype=complex)

def two_level_ops():
    sz = np.array([[1,0],[0,-1]], dtype=complex)
    sp = np.array([[0,1],[0,0]], dtype=complex)
    sm = np.array([[0,0],[1,0]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    return sz, sp, sm, I2

def kron(*ops):
    out = np.array([[1]], dtype=complex)
    for A in ops:
        out = np.kron(out, A)
    return out

def lindblad(cops, rho):
    acc = np.zeros_like(rho, dtype=complex)
    for L in cops:
        LdL = dagger(L) @ L
        acc += L @ rho @ dagger(L) - 0.5*(LdL @ rho + rho @ LdL)
    return acc

def rk4_step(rho, dt, H, c_ops):
    def rhs(r): return -1j*(H@r - r@H) + lindblad(c_ops, r)
    k1 = rhs(rho)
    k2 = rhs(rho + 0.5*dt*k1)
    k3 = rhs(rho + 0.5*dt*k2)
    k4 = rhs(rho + dt*k3)
    return rho + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

class JCSingle(BaseTest):
    name = "Electron–Swirl: Single-Mode (JC)"
    description = ("Jaynes–Cummings + Lindblad. Electron (2-level) resonantly coupled to one swirl mode. "
                   "Shows Rabi exchange, damping, and heat currents to baths.")

    def default_params(self):
        return dict(
            Nb=8, Delta=1.0, Omega=1.0, g=0.08,
            kappa=0.02, n_th=0.3, gamma_rel=0.004, gamma_phi=0.002,
            t_max=400.0, dt=0.5, init_state="excited"
        )

    def run(self, params, figure):
        Nb = int(params["Nb"]); Delta = float(params["Delta"]); Omega = float(params["Omega"]); g = float(params["g"])
        kappa = float(params["kappa"]); n_th = float(params["n_th"])
        gamma_rel = float(params["gamma_rel"]); gamma_phi = float(params["gamma_phi"])
        t_max = float(params["t_max"]); dt = float(params["dt"]); init_state = str(params["init_state"])

        # Operators
        sz, sp, sm, I2 = two_level_ops()
        a, adag, nb, IN = boson_ops(Nb)
        szF = kron(sz, IN); spF = kron(sp, IN); smF = kron(sm, IN)
        aF = kron(I2, a); adagF = kron(I2, adag); nbF = kron(I2, nb)
        H = 0.5*Delta*szF + Omega*nbF + g*(spF@aF + smF@adagF)

        c_ops = []
        if kappa>0:
            c_ops.append(math.sqrt(kappa*(n_th+1))*aF)
            if n_th>0: c_ops.append(math.sqrt(kappa*n_th)*adagF)
        if gamma_rel>0: c_ops.append(math.sqrt(gamma_rel)*smF)
        if gamma_phi>0: c_ops.append(math.sqrt(gamma_phi/2.0)*szF)

        # Initial state
        e = np.array([1,0], dtype=complex); gvec = np.array([0,1], dtype=complex)
        vac = np.zeros((Nb,), dtype=complex); vac[0]=1.0
        if init_state=="excited":
            psi0 = np.kron(e, vac)
        elif init_state=="plus":
            psi0 = (np.kron(e, vac)+np.kron(gvec, vac))/math.sqrt(2.0)
        else:
            psi0 = np.kron(e, vac)
        rho = np.outer(psi0, psi0.conj())

        times = np.arange(0.0, t_max+dt, dt)
        P_e, n_b = [], []
        E_e, E_b = [], []
        Pe = kron(np.array([[1,0],[0,0]], dtype=complex), IN)
        He = 0.5*Delta*szF; Hb = Omega*nbF

        for t in times:
            P_e.append(float(np.trace(Pe@rho).real))
            n_b.append(float(np.trace(nbF@rho).real))
            E_e.append(float(np.trace(He@rho).real))
            E_b.append(float(np.trace(Hb@rho).real))
            rho = rk4_step(rho, dt, H, c_ops)

        figure.clf()
        ax1 = figure.add_subplot(211)
        ax1.plot(times, P_e, label="P_e")
        ax1.plot(times, n_b, label="n_b")
        ax1.set_xlabel("time"); ax1.set_ylabel("pop / occ"); ax1.set_title("Populations")
        ax1.legend()

        ax2 = figure.add_subplot(212)
        ax2.plot(times, E_e, label="E_e")
        ax2.plot(times, E_b, label="E_b")
        ax2.set_xlabel("time"); ax2.set_ylabel("energy"); ax2.set_title("Energies")
        ax2.legend()

        figure.tight_layout()
        return {"times": times.tolist(), "P_e": P_e, "n_b": n_b, "E_e": E_e, "E_b": E_b}

# Entry point for discovery
TEST_CLASS = JCSingle
