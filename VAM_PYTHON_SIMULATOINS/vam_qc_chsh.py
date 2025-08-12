# vam_qc_chsh.py
# Single-file benchmark: Quantum CHSH on Aer + VAM Route-A replica and sweep
# Requires: qiskit, qiskit-aer, numpy

from math import pi, log2
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator

rng = np.random.default_rng(0)
ZZ = SparsePauliOp.from_list([("ZZ", 1.0)])

# ---------------------------
# Quantum (Aer) CHSH utilities
# ---------------------------

def qc_E_counts(phi_a, phi_b, shots=20000):
    """E = <Z⊗Z> from counts after measuring σ_φ on each qubit via RZ(φ); H; measure Z."""
    qc = QuantumCircuit(2, 2)
    qc.h(0); qc.cx(0, 1)               # |Φ+> = (|00>+|11>)/√2
    qc.rz(phi_a, 0); qc.h(0)           # measure σ_φa
    qc.rz(phi_b, 1); qc.h(1)           # measure σ_φb
    qc.measure([0, 1], [0, 1])         # q0->c0 (right), q1->c1 (left)
    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()
    s = sum(counts.values())
    return (counts.get('00', 0) + counts.get('11', 0)
            - counts.get('01', 0) - counts.get('10', 0)) / s

def qc_E_statevector(phi_a, phi_b):
    """Analytic check: for this mapping E = cos(phi_a - phi_b)."""
    qc = QuantumCircuit(2)
    qc.h(0); qc.cx(0, 1)
    qc.rz(phi_a, 0); qc.h(0)
    qc.rz(phi_b, 1); qc.h(1)
    psi = Statevector.from_instruction(qc)
    val = float(np.real(psi.expectation_value(ZZ)))
    return val

def qc_chsh(a, ap, b, bp, shots=20000):
    Eab   = qc_E_counts(a,  b,  shots)
    Eabp  = qc_E_counts(a,  bp, shots)
    Eapb  = qc_E_counts(ap, b,  shots)
    Eapbp = qc_E_counts(ap, bp, shots)
    S = abs(Eab + Eabp + Eapb - Eapbp)
    return {"E": {('a','b'):Eab, ('a','bp'):Eabp, ('ap','b'):Eapb, ('ap','bp'):Eapbp}, "S": S}

# ---------------------------
# VAM Route-A model (local deterministic with measurement-dependence)
# ---------------------------

def E_vam_pair(theta_a, theta_b, kappa, shots=200000):
    """
    Hidden axis u ∈ [0,2π).
    Outcomes: A = sign(cos(u-a)), B = -sign(cos(u-b)).
    Measurement-dependence: p(u|a,b) ∝ 1 + κ * sign(cos(u-a))*sign(cos(u-b)).
    κ ∈ [0,1). κ=0 gives classical S<=2. κ↑ reproduces quantum-like correlations.
    """
    good = bad = 0
    for _ in range(shots):
        while True:
            u = rng.random() * 2 * pi
            sA = 1 if np.cos(u - theta_a) >= 0 else -1
            sB = 1 if np.cos(u - theta_b) >= 0 else -1
            w = 1 + kappa * (sA * sB)      # ∈ {0,2}
            if rng.random() < w / 2:
                A, B = sA, -sB
                break
        if A == B: good += 1
        else:      bad  += 1
    return (good - bad) / (good + bad)

def fit_global_kappa(targets, angles, grid=np.linspace(0,0.95,19)):
    """Fit a single κ to all four target E’s by grid search on κ."""
    best = (1e9, None)
    for k in grid:
        mse = 0.0
        for key in angles:
            Ev = E_vam_pair(angles[key][0], angles[key][1], kappa=k, shots=60000)
            mse += (Ev - targets[key])**2
        mse /= len(angles)
        if mse < best[0]:
            best = (mse, k)
    return best  # (mse, kappa)

# ---------------------------
# Route-A global sweep: S vs κ and I(settings;sign(u-a)sign(u-b))
# ---------------------------

def chsh_from_E(E):
    return abs(E[('a','b')] + E[('a','bp')] + E[('ap','b')] - E[('ap','bp')])

def sweep_kappa_S_and_I(kappas, a, ap, b, bp, shots_per_pair=20000):
    """
    For presentation: uniform random over the four pairs; for each pair, draw u from p(u|a,b; κ).
    Compute CHSH S and a crude mutual information between the setting pair and s≡signA*signB.
    """
    pairs = [(a,b,'a','b'), (a,bp,'a','bp'), (ap,b,'ap','b'), (ap,bp,'ap','bp')]
    out = []
    for k in kappas:
        E = {('a','b'):0.0, ('a','bp'):0.0, ('ap','b'):0.0, ('ap','bp'):0.0}
        joint = {}  # ((sa,sb), s=±1) histogram
        for (ta,tb,sa,sb) in pairs:
            good = bad = 0
            for _ in range(shots_per_pair):
                while True:
                    u = rng.random()*2*pi
                    sA = 1 if np.cos(u - ta) >= 0 else -1
                    sB = 1 if np.cos(u - tb) >= 0 else -1
                    s  = sA * sB
                    if rng.random() < (1 + k * s)/2:
                        A, B = sA, -sB
                        break
                if A == B: good += 1
                else:      bad  += 1
                joint[((sa,sb), s)] = joint.get(((sa,sb), s), 0) + 1
            E[(sa,sb)] = (good - bad)/(good + bad)
        # mutual information I( (sa,sb); s )
        N = sum(joint.values())
        p = {k: v/N for k,v in joint.items()}
        pS = {}; pPair = {}
        for (pair,s),v in p.items():
            pS[s] = pS.get(s,0)+v
            pPair[pair] = pPair.get(pair,0)+v
        I = 0.0
        for (pair,s),v in p.items():
            I += 0 if v==0 else v * log2(v/(pPair[pair]*pS[s]))
        out.append((k, chsh_from_E(E), I))
    return out

# ---------------------------
# Main run
# ---------------------------

if __name__ == "__main__":
    # CHSH angles for the RZ;H mapping: E = cos(phi_a - phi_b)
    a, ap = 0.0, pi/2
    b, bp =  pi/4, -pi/4

    # 1) Quantum benchmark on Aer
    sv_check = (
        qc_E_statevector(a,b),
        qc_E_statevector(a,bp),
        qc_E_statevector(ap,b),
        qc_E_statevector(ap,bp)
    )
    print("Statevector E’s (ideal):", [round(x,4) for x in sv_check],
          "  S≈", round(abs(sum(sv_check[:3]) - sv_check[3]), 4))

    res = qc_chsh(a, ap, b, bp, shots=20000)
    print("Quantum counts E’s:", {k: round(v,4) for k,v in res["E"].items()},
          "  S_QM≈", round(res["S"], 4))

    # 2) VAM Route-A: fit a single κ to match the four quantum E’s
    angles  = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}
    targets = res["E"]  # use measured E’s from Aer
    mse, kappa = fit_global_kappa(targets, angles)
    Ev = {key: E_vam_pair(*angles[key], kappa=kappa, shots=200000) for key in angles}
    S_vam = chsh_from_E(Ev)
    print(f"VAM fit: kappa≈{kappa:.2f},  MSE≈{mse:.4e},  E’s:",
          {k: round(v,4) for k,v in Ev.items()}, "  S_VAM≈", round(S_vam,4))

    # 3) Route-A sweep: show S increasing with κ and report a small mutual information
    kappas = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
    sweep = sweep_kappa_S_and_I(kappas, a, ap, b, bp, shots_per_pair=8000)
    print("κ  ,  S_classical(κ) ,  I(settings; sA*sB) [bits]")
    for k, S, I in sweep:
        print(f"{k:0.2f} ,   {S:0.4f}        ,   {I:0.4f}")