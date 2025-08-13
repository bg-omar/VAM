# canonical_vam_chsh.py
# Local-only CHSH benchmarks: Φ+ (sum-law, per-pair κ_ab) and Ψ− (difference-law, single κ)
# Prints ✓/✗ checks and can write a JSON report.
# pip install qiskit qiskit-aer numpy

# ---------------------------------------------------------------------------
# Experiment map: Each item describes the meaning, what the code does, what it predicts,
# and whether it tests VAM, explains a QC anomaly, or makes a new prediction.
#
# 1) Ω-jitter sweep (Φ⁺)
#    Meaning: Model VAM’s swirl clock as phase jitter on measurement axes.
#    Does: Adds small random angle offsets tied to Ω = C * e / (r * c) and a chosen window Δt.
#          Computes S vs jitter level.
#    Predicts: A specific S(σ_ϕ) falloff curve and its scaling with Ω and Δt.
#              Lets you back-out an effective Δt from observed degradation.
#    Role: Verify VAM mechanism (time → phase). Also a QC anomaly explainer for nonstationary phase drift.
#
# 2) Export tables (E’s, S, κ_ab, S(κ))
#    Meaning: Reproducibility and parameter audit across runs, seeds, and machines.
#    Does: Writes JSON/CSV of quantum correlations, fitted VAM κ_ab, and sweeps.
#    Predicts: Stability bands. Flags day-to-day drift or setting-dependent biases.
#    Role: Verify VAM by showing consistent contextual fits; also QC anomaly detector (drift, crosstalk) when tables move systematically.
#
# 3) Correlation tensor tomography T_ij = ⟨σ_i ⊗ σ_j⟩
#    Meaning: Full two-qubit correlation geometry (X/Y/Z). In VAM: “swirl-axis” covariance.
#    Does: Measures nine expectation values, builds 3×3 T, compares to ideal Bell tensor, and to a VAM swirl-axis model.
#    Predicts: Specific anisotropy patterns under VAM phase/noise knobs.
#              Distinguishes phase jitter (XY plane) from amplitude errors (Z leakage).
#    Role: Verify VAM mapping of swirl geometry; QC anomaly explainer for coherent crosstalk vs depolarizing noise.
#
# 4) KCBS (qutrit contextuality)
#    Meaning: Single-system contextuality (no spacelike split). Five compatible tests violate a classical bound.
#    Does: Emulates a qutrit on two qubits, reproduces the KCBS sum with QM;
#          then builds a VAM family of context-conditioned priors to match or depart.
#    Predicts: When VAM Route-A lifts the KCBS sum, what mutual-information budget is needed.
#              Identifies regimes where VAM diverges from standard QM.
#    Role: New test of VAM beyond Bell. Can predict deviations if VAM imposes different context budgets than QM assumes.
#
# 5) GHZ/Mermin (three qubits)
#    Meaning: All-or-nothing nonlocality without inequalities.
#    Does: Prepares GHZ, measures Mermin operator; mirrors with a 3-party VAM prior family and checks algebraic parity constraints.
#    Predicts: Whether a single global VAM knob can satisfy all GHZ parities;
#              if not, quantifies the required context split across settings.
#    Role: Stress-test VAM. Also QC anomaly explainer for multi-qubit correlated errors (shared control lines, spectator effects).
#
# 6) Mutual-information audit I(settings; env/sign)
#    Meaning: Quantifies “measurement dependence” that VAM uses (Route-A).
#    Does: Estimates I between the chosen settings and a latent variable (e.g., the sign product used in the VAM sampler).
#          Plots S vs I.
#    Predicts: Minimal I needed to reach a target S.
#              Sets an empirical upper bound on allowable setting–environment correlation in a device.
#    Role: Verify VAM quantitatively. QC anomaly explainer for hidden selection bias or scheduler correlations between shots and settings.
#
# 7) Geometry/latency toy model
#    Meaning: Boundary-condition propagation in VAM vs circuit timing in QC.
#    Does: Simulates a short chain with a toggled edge condition; measures correlation fronts or latency in outcomes;
#          compares to VAM’s boundary-latency story.
#    Predicts: A finite response time or distance-dependent falloff.
#              Offers a signature separating pure phase noise from boundary-induced context.
#    Role: New, testable prediction for VAM (latency/propagation).
#          QC anomaly explainer for non-Markovian, layout-dependent errors.
# ---------------------------------------------------------------------------





from math import pi, sqrt
import json, argparse
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator

ZZ = SparsePauliOp.from_list([("ZZ", 1.0)])
TSIRELSON = 2*sqrt(2)

# ---------------- helpers ----------------
def check(label, ok, extra=""):
    print(f"[{'✓' if ok else '✗'}] {label}" + (f" — {extra}" if extra else ""))

def chsh_from_E(E):
    return abs(E[('a','b')] + E[('a','bp')] + E[('ap','b')] - E[('ap','bp')])

def prepare_bell(qc, state):
    qc.h(0); qc.cx(0,1)
    if state == "psi_minus":
        qc.x(1); qc.z(1)

def E_counts(phi_a, phi_b, shots, state, seed):
    sim = AerSimulator(seed_simulator=seed)
    qc = QuantumCircuit(2,2)
    prepare_bell(qc, state)
    qc.rz(phi_a,0); qc.h(0)
    qc.rz(phi_b,1); qc.h(1)
    qc.measure([0,1],[0,1])
    c = sim.run(qc, shots=shots).result().get_counts()
    s = sum(c.values())
    return (c.get('00',0)+c.get('11',0)-c.get('01',0)-c.get('10',0))/s

def E_statevector(phi_a, phi_b, state):
    qc = QuantumCircuit(2)
    prepare_bell(qc, state)
    qc.rz(phi_a,0); qc.h(0)
    qc.rz(phi_b,1); qc.h(1)
    return float(np.real(Statevector.from_instruction(qc).expectation_value(ZZ)))

# ---------- VAM Route-A ----------
def triangular_C(delta):
    d = abs((delta + np.pi) % (2*np.pi) - np.pi)    # Δ ∈ [-π,π]
    return 1.0 - 2.0*d/np.pi                        # correct square-wave correlation

def kappa_for_target(E_target, delta):
    C = triangular_C(delta)
    num = -(C + E_target); den = 1 + C*E_target
    if abs(den) < 1e-12:  # guard
        return float(np.clip(np.sign(num)*0.999, -0.999, 0.999))
    return float(np.clip(num/den, -0.999, 0.999))

def E_vam_pair(theta_a, theta_b, kappa, shots, rng):
    """Exact vectorized sampler from accepted s-distribution; works for any Δ, κ."""
    delta = theta_a - theta_b
    C = triangular_C(delta)
    Z = 1.0 + kappa*C
    p_plus = ((1.0 + kappa)*(1.0 + C)) / (2.0*Z)
    s = np.where(rng.random(shots) < p_plus, 1.0, -1.0)
    return -float(s.mean())

# -------------- runs --------------
def run_phi_plus(shots=20000, mc_shots=200000, seed=1):
    rng = np.random.default_rng(seed)
    a, ap, b, bp = 0.0, -pi/2, +pi/4, -pi/4  # Φ+ sum-law
    angles_sum = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}
    # QM
    E_qm = {k: E_counts(*ang, shots, "phi_plus", seed) for k,ang in angles_sum.items()}
    S_qm = chsh_from_E(E_qm)
    print("Φ+  E_QM:", {k: round(v,4) for k,v in E_qm.items()}, "  S_QM≈", round(S_qm,4))
    check("Φ+ Tsirelson (counts)", abs(S_qm-TSIRELSON) < 0.05, f"S={S_qm:.4f}")
    # map to VAM difference-law via Δ = a - (−b)
    angles_vam = {k:(ang[0], -ang[1]) for k,ang in angles_sum.items()}
    # analytic κ_ab and closed-form match
    kappa_ab = {k: kappa_for_target(E_qm[k], angles_vam[k][0] - angles_vam[k][1]) for k in angles_vam}
    E_pred = {}
    for k,(ta,tb) in angles_vam.items():
        Δ = ta - tb; C = triangular_C(Δ); κ = kappa_ab[k]
        E_pred[k] = -(C + κ)/(1 + κ*C)
    S_pred = chsh_from_E(E_pred)
    print("Φ+  κ_ab (analytic):", {k: round(v,3) for k,v in kappa_ab.items()})
    print("Φ+  E_VAM_pred:", {k: round(v,4) for k,v in E_pred.items()}, "  S_VAM_pred≈", round(S_pred,4))
    diff_pred = max(abs(E_pred[k]-E_qm[k]) for k in E_pred)
    check("Φ+ VAM closed-form matches QM", diff_pred < 0.01, f"max|ΔE|={diff_pred:.4f}")
    # MC confirmation
    E_mc = {k: E_vam_pair(*angles_vam[k], kappa_ab[k], mc_shots, rng) for k in angles_vam}
    S_mc = chsh_from_E(E_mc)
    print("Φ+  E_VAM_fit (MC):", {k: round(v,4) for k,v in E_mc.items()}, "  S_VAM_fit≈", round(S_mc,4))
    diff_mc = max(abs(E_mc[k]-E_pred[k]) for k in E_mc)
    check("Φ+ VAM MC ≈ closed-form", diff_mc < 0.02, f"max|ΔE|={diff_mc:.4f}")
    return {"mode":"phi_plus","E_QM":E_qm,"S_QM":S_qm,"kappa_ab":kappa_ab,"E_VAM_pred":E_pred,"S_VAM_pred":S_pred,"E_VAM_MC":E_mc,"S_VAM_MC":S_mc}

def run_psi_minus(shots=20000, mc_shots_list=(0.0,0.1,0.2,0.3,0.5,0.7,0.9), seed=2):
    a, ap, b, bp = 0.0, +pi/2, +pi/4, -pi/4  # Ψ− difference-law
    angles = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}
    # QM
    E_qm = {k: E_counts(*ang, shots, "psi_minus", seed) for k,ang in angles.items()}
    S_qm = chsh_from_E(E_qm)
    print("Ψ-  E_QM:", {k: round(v,4) for k,v in E_qm.items()}, "  S_QM≈", round(S_qm,4))
    check("Ψ- Tsirelson (counts)", abs(S_qm-TSIRELSON) < 0.05, f"S={S_qm:.4f}")
    # sweep κ
    rng = np.random.default_rng(seed+7)
    sweep = []
    for k in mc_shots_list:
        E = {key: E_vam_pair(*angles[key], k, 40000, rng) for key in angles}
        sweep.append((k, round(chsh_from_E(E),4)))
    print("Ψ-  S_VAM(κ):", sweep)
    S0 = [S for κ,S in sweep if abs(κ-0.0)<1e-9][0]
    Speak = max(S for _,S in sweep)
    check("Ψ- VAM: S(0)≈2", abs(S0-2.0) < 0.05, f"S(0)={S0:.3f}")
    check("Ψ- VAM: peak > 2.2", Speak > 2.2, f"peak={Speak:.3f}")
    return {"mode":"psi_minus","E_QM":E_qm,"S_QM":S_qm,"sweep":sweep}

# -------------- CLI --------------
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--shots", type=int, default=20000)
    p.add_argument("--mc_shots", type=int, default=200000)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--out", type=str, default="")
    args = p.parse_args()

    res1 = run_phi_plus(shots=args.shots, mc_shots=args.mc_shots, seed=args.seed)
    res2 = run_psi_minus(shots=args.shots, seed=args.seed+1)

    if args.out:
        with open(args.out, "w") as f:
            json.dump({"phi_plus":res1, "psi_minus":res2}, f, indent=2, default=lambda o: float(o))
        print("saved:", args.out)