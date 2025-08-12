from math import pi
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# ---------- Quantum side ----------
def counts_E(phi_a, phi_b, shots=20000):
    qc = QuantumCircuit(2,2)
    qc.h(0); qc.cx(0,1)          # |Φ+>
    qc.rz(phi_a,0); qc.h(0)      # measure σ_φa
    qc.rz(phi_b,1); qc.h(1)      # measure σ_φb
    qc.measure([0,1],[0,1])
    sim = AerSimulator()
    c = sim.run(qc, shots=shots).result().get_counts()
    s = sum(c.values())
    return ((c.get('00',0)+c.get('11',0)) - (c.get('01',0)+c.get('10',0)))/s

# Tsirelson-optimal angles for polarization
a, ap = 0.0, pi/4
b, bp =  pi/8, -pi/8

E_qm = {
    ('a','b'):   counts_E(a,b),
    ('a','bp'):  counts_E(a,bp),
    ('ap','b'):  counts_E(ap,b),
    ('ap','bp'): counts_E(ap,bp),
}
S_qm = abs(E_qm[('a','b')] + E_qm[('a','bp')] + E_qm[('ap','b')] - E_qm[('ap','bp')])

# ---------- VAM Route-A side (per-pair fit) ----------
rng = np.random.default_rng(1)

def E_vam_pair(theta_a, theta_b, kappa, shots=200000):
    good = bad = 0
    for _ in range(shots):
        # rejection sample u with weight 1 + kappa * sA*sB, where sA=sign(cos(u-a)), sB=sign(cos(u-b))
        while True:
            u = rng.random()*2*pi
            sA = 1 if np.cos(u - theta_a) >= 0 else -1
            sB = 1 if np.cos(u - theta_b) >= 0 else -1
            w = 1 + kappa*(sA*sB)     # ∈ {0,2}
            if rng.random() < w/2:    # accept
                A = sA
                B = -sB
                break
        if A == B: good += 1
        else:      bad  += 1
    return (good - bad)/(good + bad)

def fit_kappa(theta_a, theta_b, target_E):
    # monotone in kappa for fixed (a,b): binary search
    lo, hi = 0.0, 0.999
    for _ in range(20):
        mid = 0.5*(lo+hi)
        Emid = E_vam_pair(theta_a, theta_b, mid, shots=80000)
        if (Emid - target_E) * (E_vam_pair(theta_a, theta_b, lo, shots=40000) - target_E) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo+hi)

pairs = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}
kappa = {}
E_vam = {}
for key,(ta,tb) in pairs.items():
    kappa[key] = fit_kappa(ta,tb, E_qm[key])
    E_vam[key] = E_vam_pair(ta,tb, kappa[key], shots=200000)

S_vam = abs(E_vam[('a','b')] + E_vam[('a','bp')] + E_vam[('ap','b')] - E_vam[('ap','bp')])

print("Quantum E’s:", E_qm, "   S_QM≈", round(S_qm,4))
print("VAM-fit  E’s:", E_vam, "   S_VAM≈", round(S_vam,4))
print("Fitted κ per pair:", kappa)