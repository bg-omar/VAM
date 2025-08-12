# vam_qc_chsh_both.py
# Local-only: CHSH on Aer + VAM Route-A (both "sum" and "difference" laws)
# pip install qiskit qiskit-aer numpy

from math import pi
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator

rng = np.random.default_rng(0)
ZZ = SparsePauliOp.from_list([("ZZ", 1.0)])

# ---------- Quantum utilities ----------
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

def chsh_from_E(E):
    return abs(E[('a','b')] + E[('a','bp')] + E[('ap','b')] - E[('ap','bp')])

# ---------- VAM Route-A (hidden-axis with measurement dependence) ----------
def E_vam_pair(theta_a, theta_b, kappa, shots=200000):
    """
    Exact MC without rejection.
    For Δ = a - b', with b' = -b in the Φ+ mapping:
      C(Δ) = triangular_C(Δ)
      P'(s=+1) = ((1+kappa)*(1+C))/ (2*(1+kappa*C))
      P'(s=-1) = ((1-kappa)*(1-C))/ (2*(1+kappa*C))
    Then E = -⟨s⟩ under P'.
    """
    delta = theta_a - theta_b
    C = triangular_C(delta)
    Z = 1.0 + kappa*C
    p_plus = ((1.0 + kappa)*(1.0 + C)) / (2.0 * Z)
    # sample s ∈ {+1,-1}
    u = rng.random(shots)
    s = np.where(u < p_plus, 1.0, -1.0)
    return -float(s.mean())



def triangular_C(delta):
    """C(Δ) = E[ sA*sB ] for sA=sgn(cos(u-a)), sB=sgn(cos(u-b)), u~Unif[0,2π)."""
    d = abs((delta + np.pi) % (2*np.pi) - np.pi)  # wrap to [-π,π]
    d = abs(d)
    if d <= np.pi/2:
        return 1.0 - 4.0*d/np.pi
    else:
        return -3.0 + 4.0*d/np.pi

def kappa_for_target(E_target, delta):
    """
    VAM Route-A analytic relation:
      E_vam(Δ,κ) = -(C(Δ) + κ) / (1 + κ C(Δ))
    Solve for κ: κ = -(C + E_target) / (1 + C*E_target)
    """
    C = triangular_C(delta)
    num = -(C + E_target)
    den =  (1 + C*E_target)
    # guard against numerical edge
    if abs(den) < 1e-12:
        return np.sign(num) * 0.999
    k = num / den
    return float(np.clip(k, -0.999, 0.999))

def sweep_kappa_S(kappas, angles, shots_per_pair=40000):
    out = []
    for k in kappas:
        E = {key: E_vam_pair(*angles[key], kappa=k, shots=shots_per_pair) for key in angles}
        out.append((k, chsh_from_E(E)))
    return out

# ---------- Main ----------
if __name__ == "__main__":
    # ===== Mode A: Φ⁺ (sum law). Per-pair κ_ab to match quantum table exactly. =====
    STATE_SUM = "phi_plus"
    a, ap, b, bp = 0.0, -pi/2, +pi/4, -pi/4            # E_QM = cos(a+b)
    angles_sum = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}

    # Quantum (Aer)
    E_qm_sum = {('a','b'):E_counts(a,b, 20000, STATE_SUM),
                ('a','bp'):E_counts(a,bp,20000, STATE_SUM),
                ('ap','b'):E_counts(ap,b,20000, STATE_SUM),
                ('ap','bp'):E_counts(ap,bp,20000, STATE_SUM)}
    S_qm_sum = chsh_from_E(E_qm_sum)
    print("Φ+  E_QM:", {k: round(v,4) for k,v in E_qm_sum.items()}, "  S_QM≈", round(S_qm_sum,4))

    # Quantum (Aer) already computed: E_qm_sum
    # Map Φ+ sum-law to VAM difference-law via (a, -b) so Δ = a + b
    # Φ+ uses sum law E_QM = cos(a+b). Map to VAM Δ = a - (-b).
    angles_vam_sum = {k: (ang[0], -ang[1]) for k, ang in angles_sum.items()}




    # Compute κ_ab analytically from the measured quantum E’s
    kappa_ab = {}
    for key, (ta, tb) in angles_vam_sum.items():
        delta = ta - tb                      # Δ for VAM
        kappa_ab[key] = kappa_for_target(E_qm_sum[key], delta)

    # Deterministic prediction check (no Monte Carlo needed):
    def E_vam_closed(E_target, delta):
        C = triangular_C(delta)
        k = kappa_for_target(E_target, delta)
        return -(C + k) / (1 + k*C)

    E_pred = {}
    for key, (ta, tb) in angles_vam_sum.items():
        delta = ta - tb
        E_pred[key] = E_vam_closed(E_qm_sum[key], delta)

    S_pred = abs(E_pred[('a','b')] + E_pred[('a','bp')] + E_pred[('ap','b')] - E_pred[('ap','bp')])

    print("Φ+  κ_ab (analytic):", {k: round(v, 3) for k, v in kappa_ab.items()})
    print("Φ+  E_VAM_pred (closed-form):", {k: round(v,4) for k,v in E_pred.items()},
          "  S_VAM_pred≈", round(S_pred, 4))

    # Optional: Monte Carlo confirmation of the same κ_ab
    E_vam_fit = {k: E_vam_pair(*angles_vam_sum[k], kappa=kappa_ab[k], shots=200_000)
                 for k in angles_vam_sum}
    S_vam_fit = abs(E_vam_fit[('a','b')] + E_vam_fit[('a','bp')]
                    + E_vam_fit[('ap','b')] - E_vam_fit[('ap','bp')])
    print("Φ+  E_VAM_fit (MC):", {k: round(v,4) for k,v in E_vam_fit.items()},
          "  S_VAM_fit≈", round(S_vam_fit, 4))

    # closed-form vs MC must match within ~0.01
    for key,(ta,tb) in angles_vam_sum.items():
        Δ = ta - tb
        C = triangular_C(Δ)
        κ = kappa_ab[key]
        E_closed = -(C + κ)/(1 + κ*C)
        E_mc     = E_vam_pair(ta, tb, κ, shots=200_000)
        print(key, "Δ=", round(Δ,3), "E_closed=", round(E_closed,4), "E_mc=", round(E_mc,4))

    # ===== Mode B: Ψ⁻ (difference law). Single κ sweep. =====
    STATE_DIFF = "psi_minus"
    a, ap, b, bp = 0.0, +pi/2, +pi/4, -pi/4            # E_QM = -cos(a-b)
    angles_diff = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}

    # Quantum (Aer)
    E_qm_diff = {('a','b'):E_counts(a,b, 20000, STATE_DIFF),
                 ('a','bp'):E_counts(a,bp,20000, STATE_DIFF),
                 ('ap','b'):E_counts(ap,b,20000, STATE_DIFF),
                 ('ap','bp'):E_counts(ap,bp,20000, STATE_DIFF)}
    S_qm_diff = chsh_from_E(E_qm_diff)
    print("Ψ-  E_QM:", {k: round(v,4) for k,v in E_qm_diff.items()}, "  S_QM≈", round(S_qm_diff,4))

    # Single-κ VAM sweep on the same angles (difference law)
    kappas = [0.00, 0.10, 0.20, 0.30, 0.50, 0.70, 0.90]
    sweep = sweep_kappa_S(kappas, angles_diff, shots_per_pair=40000)
    print("Ψ-  S_VAM(κ):", [(k, round(S,4)) for k,S in sweep])