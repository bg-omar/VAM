from math import pi
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator

ZZ = SparsePauliOp.from_list([("ZZ", 1.0)])


def prepare_bell(qc, kind="phi_plus"):
    qc.h(0); qc.cx(0,1)
    if kind == "psi_minus":
        qc.x(1); qc.z(1)  # |Φ+> → |Ψ-> up to global phase


def E_statevector(phi_a, phi_b):
    qc = QuantumCircuit(2)
    qc.h(0); qc.cx(0,1)        # |Φ+>
    qc.rz(phi_a,0); qc.h(0)    # measure σ_φa
    qc.rz(phi_b,1); qc.h(1)    # measure σ_φb
    psi = Statevector.from_instruction(qc)
    return float(np.real(psi.expectation_value(ZZ)))  # = cos(phi_a - phi_b)

def E_counts(phi_a, phi_b, shots=20000):
    qc = QuantumCircuit(2,2)
    qc.h(0); qc.cx(0,1)
    qc.rz(phi_a,0); qc.h(0)
    qc.rz(phi_b,1); qc.h(1)
    qc.measure([0,1],[0,1])    # q0->c0 (right), q1->c1 (left)
    c = AerSimulator().run(qc, shots=shots).result().get_counts()
    s = sum(c.values())
    return (c.get('00',0)+c.get('11',0) - c.get('01',0)-c.get('10',0))/s

# CHSH angles for Φ+ with E = cos(phi_a + phi_b)
a  = 0.0
ap = -np.pi/2     # <- was +π/2; flip sign
b  =  np.pi/4
bp = -np.pi/4


Eab_sv  = E_statevector(a,b)
Eabp_sv = E_statevector(a,bp)
Eapb_sv = E_statevector(ap,b)
Eapbp_sv= E_statevector(ap,bp)

print("SV  :", Eab_sv, Eabp_sv, Eapb_sv, Eapbp_sv,
      "S≈", abs(Eab_sv+Eabp_sv+Eapb_sv - Eapbp_sv))  # ≈ 2.828

Eab    = E_counts(a,b)
Eabp   = E_counts(a,bp)
Eapb   = E_counts(ap,b)
Eapbp  = E_counts(ap,bp)

print("Counts:", Eab, Eabp, Eapb, Eapbp,
      "S≈", abs(Eab+Eabp+Eapb - Eapbp))  # should match SV within shot noise


import numpy as np
from math import pi
rng = np.random.default_rng(0)

targets = {('a','b'):Eab_sv, ('a','bp'):Eabp_sv, ('ap','b'):Eapb_sv, ('ap','bp'):Eapbp_sv}
angles  = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}

def E_vam(theta_a, theta_b, kappa, shots=200000):
    good = bad = 0
    for _ in range(shots):
        # sample hidden axis u with weight 1 + κ sA sB, sA=sign(cos(u-a)), sB=sign(cos(u-b))
        while True:
            u = rng.random()*2*pi
            sA = 1 if np.cos(u-theta_a)>=0 else -1
            sB = 1 if np.cos(u-theta_b)>=0 else -1
            if rng.random() < (1 + kappa*(sA*sB))/2:
                A, B = sA, -sB
                break
        if A==B: good += 1
        else:    bad  += 1
    return (good-bad)/(good+bad)

def fit_kappa():
    grid = np.linspace(0, 0.95, 20)
    best = (1e9, None)
    for k in grid:
        mse = 0.0
        for key in angles:
            Ev = E_vam(*angles[key], kappa=k, shots=60000)
            mse += (Ev - targets[key])**2
        mse /= 4
        if mse < best[0]:
            best = (mse, k)
    return best

mse,k = fit_kappa()
Ev = {key: E_vam(*angles[key], kappa=k, shots=200000) for key in angles}
S_vam = abs(Ev[('a','b')] + Ev[('a','bp')] + Ev[('ap','b')] - Ev[('ap','bp')])

print(f"kappa≈{k:.2f}  VAM E’s: {Ev}  S_VAM≈{S_vam:.4f}  MSE≈{mse:.4e}")


qc = QuantumCircuit(2,2)
prepare_bell(qc, kind="psi_minus")
# measure with RZ(φ); H as before
# angles: a=0, ap=+π/2, b=+π/4, bp=−π/4  → S≈2.828