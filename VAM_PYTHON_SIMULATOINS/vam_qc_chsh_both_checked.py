# vam_qc_chsh_both_checked.py
# Local-only: CHSH on Aer + VAM Route-A (sum-law Φ+ with per-pair κ; difference-law Ψ− with single κ)
# Prints ✓ PASS / ✗ FAIL for each milestone.
# pip install qiskit qiskit-aer numpy

from math import pi, sqrt
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator

rng = np.random.default_rng(0)
ZZ = SparsePauliOp.from_list([("ZZ", 1.0)])
TSIRELSON = 2*sqrt(2)

# ---------- helpers ----------
def check(label, ok, extra=""):
    print(f"[{'\u2714' if ok else '\u2718'}] {label}" + (f" — {extra}" if extra else ""))

def chsh_from_E(E):
    return abs(E[('a','b')] + E[('a','bp')] + E[('ap','b')] - E[('ap','bp')])

def prepare_bell(qc, state="phi_plus"):
    qc.h(0); qc.cx(0,1)
    if state == "psi_minus":
        qc.x(1); qc.z(1)  # |Φ+> → |Ψ->

def E_counts(phi_a, phi_b, shots=20000, state="phi_plus"):
    qc = QuantumCircuit(2,2)
    prepare_bell(qc, state)
    qc.rz(phi_a,0); qc.h(0)
    qc.rz(phi_b,1); qc.h(1)
    qc.measure([0,1],[0,1])
    c = AerSimulator().run(qc, shots=shots).result().get_counts()
    s = sum(c.values())
    return (c.get('00',0)+c.get('11',0)-c.get('01',0)-c.get('10',0))/s

def E_statevector(phi_a, phi_b, state="phi_plus"):
    qc = QuantumCircuit(2)
    prepare_bell(qc, state)
    qc.rz(phi_a,0); qc.h(0)
    qc.rz(phi_b,1); qc.h(1)
    return float(np.real(Statevector.from_instruction(qc).expectation_value(ZZ)))

# ---------- VAM Route-A ----------
def triangular_C(delta):
    # d = abs((delta + np.pi) % (2*np.pi) - np.pi)    # wrap to [-π,π]
    # if d <= np.pi/2:   return 1.0 - 4.0*d/np.pi
    # else:              return -3.0 + 4.0*d/np.pi
    # wrap Δ to [-π, π]
    d = abs((delta + np.pi) % (2*np.pi) - np.pi)
    # correct square-wave correlation
    return 1.0 - 2.0*d/np.pi

def kappa_for_target(E_target, delta):
    C = triangular_C(delta)
    num = -(C + E_target)
    den =  (1 + C*E_target)
    if abs(den) < 1e-12:
        return float(np.clip(np.sign(num)*0.999, -0.999, 0.999))
    return float(np.clip(num/den, -0.999, 0.999))

def E_vam_pair(theta_a, theta_b, kappa, shots=200000):
    """
    Exact MC without rejection.
    For Δ = a - b', with b' = -b in the Φ+ mapping:
      C(Δ) = triangular_C(Δ)
      P'(s=+1) = ((1+kappa)*(1+C))/ (2*(1+kappa*C))
      P'(s=-1) = ((1-kappa)*(1-C))/ (2*(1+kappa*C))
    Then E = -⟨s⟩ under P'.
    """
    # delta = theta_a - theta_b
    # C = triangular_C(delta)
    # Z = 1.0 + kappa*C
    # p_plus = ((1.0 + kappa)*(1.0 + C)) / (2.0 * Z)
    # # sample s ∈ {+1,-1}
    # u = rng.random(shots)
    # s = np.where(u < p_plus, 1.0, -1.0)
    # return -float(s.mean())
    """
    Exact MC from the accepted s-distribution for any Δ and κ:
      C = 1 - 2|Δ|/π,  Z = 1 + κC,
      P'(s=+1) = ((1+κ)(1+C)) / (2 Z),
      P'(s=-1) = ((1-κ)(1-C)) / (2 Z),
      E = -⟨s⟩ under P'.
    """
    delta = theta_a - theta_b
    C = triangular_C(delta)
    Z = 1.0 + kappa*C
    p_plus = ((1.0 + kappa)*(1.0 + C)) / (2.0*Z)
    u = rng.random(shots)
    s = np.where(u < p_plus, 1.0, -1.0)
    return -float(s.mean())


# ---------- Main ----------
if __name__ == "__main__":
    # ===== Mode A: Φ+ (sum law). Per-pair κ_ab to match quantum table. =====
    STATE_SUM = "phi_plus"
    a, ap, b, bp = 0.0, -pi/2, +pi/4, -pi/4            # E_QM = cos(a+b)
    angles_sum = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}

    # CHSH angles for RZ;H mapping
    a  = 0.0
    ap = -np.pi/2   # <-- flip sign
    b  =  np.pi/4
    bp = -np.pi/4

    angles = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}

    # Quantum (Aer)
    E_qm_sum = {('a','b'):E_counts(a,b, 20000, STATE_SUM),
                ('a','bp'):E_counts(a,bp,20000, STATE_SUM),
                ('ap','b'):E_counts(ap,b,20000, STATE_SUM),
                ('ap','bp'):E_counts(ap,bp,20000, STATE_SUM)}
    S_qm_sum = chsh_from_E(E_qm_sum)
    print("Φ+  E_QM:", {k: round(v,4) for k,v in E_qm_sum.items()}, "  S_QM≈", round(S_qm_sum,4))
    check("Φ+ Tsirelson (counts)", abs(S_qm_sum-TSIRELSON) < 0.05, f"S={S_qm_sum:.4f}")

    # Map Φ+ sum-law to VAM difference-law via Δ = a - (−b)
    angles_vam_sum = {k: (ang[0], -ang[1]) for k,ang in angles_sum.items()}

    # Analytic κ_ab to reproduce each pair exactly
    kappa_ab = {}
    E_pred = {}
    for key,(ta,tb) in angles_vam_sum.items():
        delta = ta - tb
        kappa_ab[key] = kappa_for_target(E_qm_sum[key], delta)
        # closed-form predicted E (should equal target exactly)
        C = triangular_C(delta); κ = kappa_ab[key]
        E_pred[key] = -(C + κ)/(1 + κ*C)

    for key,(ta,tb) in angles_vam_sum.items():
        delta = ta - tb
        C = triangular_C(delta); κ = kappa_ab[key]
        E_closed = -(C + κ)/(1 + κ*C)
        E_mc     = E_vam_pair(ta, tb, κ, shots=200_000)
        print(key, "Δ=", round(delta,3), "E_closed=", round(E_closed,4), "E_mc=", round(E_mc,4))

    S_pred = chsh_from_E(E_pred)
    print("Φ+  κ_ab (analytic):", {k: round(v,3) for k,v in kappa_ab.items()})
    print("Φ+  E_VAM_pred (closed-form):", {k: round(v,4) for k,v in E_pred.items()},
          "  S_VAM_pred≈", round(S_pred,4))
    # Pred must match measured within shot noise
    diff_pred = max(abs(E_pred[k]-E_qm_sum[k]) for k in E_pred)
    check("Φ+ VAM closed-form matches QM", diff_pred < 0.01, f"max|ΔE|={diff_pred:.4f}")

    # MC confirmation (can be slower; reduce shots if needed)
    E_mc = {k: E_vam_pair(*angles_vam_sum[k], kappa=kappa_ab[k], shots=200_000)
            for k in angles_vam_sum}
    S_mc = chsh_from_E(E_mc)
    print("Φ+  E_VAM_fit (MC):", {k: round(v,4) for k,v in E_mc.items()},
          "  S_VAM_fit≈", round(S_mc,4))
    diff_mc = max(abs(E_mc[k]-E_pred[k]) for k in E_mc)
    check("Φ+ VAM MC ≈ closed-form", diff_mc < 0.02, f"max|ΔE|={diff_mc:.4f}")

    # ===== Mode B: Ψ− (difference law). Single κ sweep. =====
    STATE_DIFF = "psi_minus"
    a, ap, b, bp = 0.0, +pi/2, +pi/4, -pi/4            # E_QM = -cos(a-b)
    angles_diff = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}

    E_qm_diff = {('a','b'):E_counts(a,b, 20000, STATE_DIFF),
                 ('a','bp'):E_counts(a,bp,20000, STATE_DIFF),
                 ('ap','b'):E_counts(ap,b,20000, STATE_DIFF),
                 ('ap','bp'):E_counts(ap,bp,20000, STATE_DIFF)}
    S_qm_diff = chsh_from_E(E_qm_diff)
    print("Ψ-  E_QM:", {k: round(v,4) for k,v in E_qm_diff.items()}, "  S_QM≈", round(S_qm_diff,4))
    check("Ψ- Tsirelson (counts)", abs(S_qm_diff-TSIRELSON) < 0.05, f"S={S_qm_diff:.4f}")

    # Single-κ sweep
    kappas = [0.00, 0.10, 0.20, 0.30, 0.50, 0.70, 0.90]
    def S_vam_for_k(k):
        E = {key: E_vam_pair(*angles_diff[key], kappa=k, shots=40000) for key in angles_diff}
        return chsh_from_E(E)
    sweep = [(k, round(S_vam_for_k(k),4)) for k in kappas]
    print("Ψ-  S_VAM(κ):", sweep)

    # Checks on the sweep: S(0)≈2, peak > 2.2, monotone rise at small κ
    S0 = S_vam_for_k(0.0)
    Speak = max(S for _,S in sweep)
    check("Ψ- VAM: S(0)≈2", abs(S0-2.0) < 0.05, f"S(0)={S0:.3f}")
    check("Ψ- VAM: peak > 2.2", Speak > 2.2, f"peak={Speak:.3f}")