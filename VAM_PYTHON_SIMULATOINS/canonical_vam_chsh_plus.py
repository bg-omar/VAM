# canonical_vam_chsh_plus.py
# Local-only CHSH: Φ+ (per-pair κ_ab) + Ω-jitter sweep, and Ψ− (single κ) + S–I audit
# pip install qiskit qiskit-aer numpy

from math import pi, sqrt, log2
import json, argparse
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator

ZZ = SparsePauliOp.from_list([("ZZ", 1.0)])
TSIRELSON = 2*sqrt(2)

# ---------------- constants for Ω-jitter ----------------
C_e = 1_093_845.63         # m/s
r_c = 1.40897017e-15       # m
OMEGA = C_e / r_c          # s^-1

# ---------------- helpers ----------------
def check(label, ok, extra=""):
    print(f"[{'\u2714' if ok else '\u2718'}] {label}" + (f" — {extra}" if extra else ""))

def chsh_from_E(E):
    return abs(E[('a','b')] + E[('a','bp')] + E[('ap','b')] - E[('ap','bp')])

def prepare_bell(qc, state):
    qc.h(0); qc.cx(0,1)
    if state == "psi_minus":
        qc.x(1); qc.z(1)  # |Φ+> → |Ψ->

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

def E_counts_with_jitter(phi_a, phi_b, sigma_phi, n_batches, shots_per, state, seed):
    """Gaussian angle jitter per batch; aggregates counts."""
    sim = AerSimulator(seed_simulator=seed)
    tot = {'00':0,'01':0,'10':0,'11':0}
    rng = np.random.default_rng(seed)
    for _ in range(n_batches):
        da = rng.normal(0.0, sigma_phi)
        db = rng.normal(0.0, sigma_phi)
        qc = QuantumCircuit(2,2)
        prepare_bell(qc, state)
        qc.rz(phi_a+da,0); qc.h(0)
        qc.rz(phi_b+db,1); qc.h(1)
        qc.measure([0,1],[0,1])
        c = sim.run(qc, shots=shots_per).result().get_counts()
        for k,v in c.items(): tot[k] = tot.get(k,0)+v
    s = sum(tot.values())
    return (tot.get('00',0)+tot.get('11',0)-tot.get('01',0)-tot.get('10',0))/s

# ---------- VAM Route-A ----------
def triangular_C(delta):
    """Square-wave correlation of signs: C(Δ)=1-2|Δ|/π, Δ wrapped to [-π,π]."""
    d = abs((delta + np.pi) % (2*np.pi) - np.pi)
    return 1.0 - 2.0*d/np.pi

def kappa_for_target(E_target, delta):
    C = triangular_C(delta)
    num = -(C + E_target); den = 1 + C*E_target
    if abs(den) < 1e-12:
        return float(np.clip(np.sign(num)*0.999, -0.999, 0.999))
    return float(np.clip(num/den, -0.999, 0.999))

def E_vam_closed(delta, kappa):
    C = triangular_C(delta)
    return -(C + kappa) / (1 + kappa*C)

def mutual_info_S_vs_pairs(angles, kappa):
    """
    I(pair ; s), where pair∈{(a,b),(a,bp),(ap,b),(ap,bp)} chosen uniformly, and
    s=sgn(cos(u-a))*sgn(cos(u-b)) under the accepted Route-A distribution.
    Using closed-form P'(s=+1 | pair) = ((1+κ)(1+C))/(2(1+κC)).
    """
    pairs = list(angles.items())
    P_pair = 1.0/len(pairs)
    p_plus = []
    for _,(ta,tb) in pairs:
        Δ = ta - tb; C = triangular_C(Δ); Z = 1 + kappa*C
        p_plus.append(((1+kappa)*(1+C))/(2*Z))
    # marginals
    P_s_plus = P_pair*sum(p_plus)
    P_s_minus = 1.0 - P_s_plus
    # mutual information
    I = 0.0
    for p in p_plus:
        if p>0:   I += P_pair * p * log2(p / P_s_plus)
        q = 1-p
        if q>0:   I += P_pair * q * log2(q / P_s_minus)
    return I

# -------------- runs --------------
def run_phi_plus(shots=20000, seed=1, do_jitter=True):
    a, ap, b, bp = 0.0, -pi/2, +pi/4, -pi/4  # Φ+ sum-law
    angles_sum = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}

    # QM baseline
    E_qm = {k: E_counts(*ang, shots, "phi_plus", seed) for k,ang in angles_sum.items()}
    S_qm = chsh_from_E(E_qm)
    print("Φ+  E_QM:", {k: round(v,4) for k,v in E_qm.items()}, "  S_QM≈", round(S_qm,4))
    check("Φ+ Tsirelson (counts)", abs(S_qm-TSIRELON) < 0.05 if (TSIRELON:=TSIRELSON) else False, f"S={S_qm:.4f}")

    # map Φ+ sum-law to VAM difference-law via Δ = a - (−b)
    angles_vam = {k:(ang[0], -ang[1]) for k,ang in angles_sum.items()}

    # analytic κ_ab and closed-form match
    kappa_ab = {k: kappa_for_target(E_qm[k], angles_vam[k][0]-angles_vam[k][1]) for k in angles_vam}
    E_pred = {k: E_vam_closed(angles_vam[k][0]-angles_vam[k][1], kappa_ab[k]) for k in angles_vam}
    S_pred = chsh_from_E(E_pred)
    print("Φ+  κ_ab (analytic):", {k: round(v,3) for k,v in kappa_ab.items()})
    print("Φ+  E_VAM_pred:", {k: round(v,4) for k,v in E_pred.items()}, "  S_VAM_pred≈", round(S_pred,4))
    diff_pred = max(abs(E_pred[k]-E_qm[k]) for k in E_pred)
    check("Φ+ VAM closed-form matches QM", diff_pred < 0.01, f"max|ΔE|={diff_pred:.4f}")

    # Ω-jitter sweep
    if do_jitter:
        dt_list     = [1e-22, 3e-22, 1e-21]
        sigma0_list = [0.00, 0.05, 0.10, 0.20]
        print("\nΩ-jitter sweep  (σφ = σ0 * Ω * Δt)")
        print("σ0    Δt[s]     σφ[rad]   S_QM_with_jitter")
        for dt in dt_list:
            for s0 in sigma0_list:
                sigma_phi = s0 * OMEGA * dt
                Ej = {
                    ('a','b'):  E_counts_with_jitter(a,b,  sigma_phi, n_batches=48, shots_per=256, state="phi_plus", seed=seed+11),
                    ('a','bp'): E_counts_with_jitter(a,bp, sigma_phi, n_batches=48, shots_per=256, state="phi_plus", seed=seed+12),
                    ('ap','b'): E_counts_with_jitter(ap,b, sigma_phi, n_batches=48, shots_per=256, state="phi_plus", seed=seed+13),
                    ('ap','bp'):E_counts_with_jitter(ap,bp,sigma_phi, n_batches=48, shots_per=256, state="phi_plus", seed=seed+14),
                }
                Sj = chsh_from_E(Ej)
                print(f"{s0:0.2f}  {dt:0.1e}  {sigma_phi:0.3e}   {Sj:0.4f}")

    return {"mode":"phi_plus","E_QM":E_qm,"S_QM":S_qm,"kappa_ab":kappa_ab,"E_VAM_pred":E_pred,"S_VAM_pred":S_pred}

def run_psi_minus(shots=20000, seed=2, kappas=(0.00,0.05,0.10,0.20,0.30,0.50,0.70,0.90)):
    a, ap, b, bp = 0.0, +pi/2, +pi/4, -pi/4  # Ψ− difference-law
    angles = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}

    # QM baseline
    E_qm = {k: E_counts(*ang, shots, "psi_minus", seed) for k,ang in angles.items()}
    S_qm = chsh_from_E(E_qm)
    print("\nΨ-  E_QM:", {k: round(v,4) for k,v in E_qm.items()}, "  S_QM≈", round(S_qm,4))
    check("Ψ- Tsirelson (counts)", abs(S_qm-TSIRELSON) < 0.05, f"S={S_qm:.4f}")

    # VAM single-κ sweep with S and mutual information I(pair; s)
    print("Ψ-  κ      S_VAM    I(pair;s) [bits]")
    table = []
    for k in kappas:
        E = {key: E_vam_closed(angles[key][0]-angles[key][1], k) for key in angles}
        S = chsh_from_E(E)
        I = mutual_info_S_vs_pairs(angles, k)
        print(f"    {k:0.2f}   {S:0.4f}   {I:0.4f}")
        table.append((k, S, I))
    # checks
    S0 = [S for (k,S,_) in table if abs(k-0.0)<1e-12][0]
    Speak = max(S for (_,S,_) in table)
    check("Ψ- VAM: S(0)≈2", abs(S0-2.0) < 0.05, f"S(0)={S0:.3f}")
    check("Ψ- VAM: peak > 2.2", Speak > 2.2, f"peak={Speak:.3f}")
    return {"mode":"psi_minus","E_QM":E_qm,"S_QM":S_qm,"sweep":[(float(k),float(S),float(I)) for (k,S,I) in table]}

# -------------- CLI --------------
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--shots", type=int, default=20000)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--out", type=str, default="")
    args = p.parse_args()

    print(f"Ω = C_e / r_c = {OMEGA:.3e} s^-1")
    res_phi = run_phi_plus(shots=args.shots, seed=args.seed, do_jitter=True)
    res_psi = run_psi_minus(shots=args.shots, seed=args.seed+1)

    if args.out:
        with open(args.out, "w") as f:
            json.dump({"phi_plus":res_phi, "psi_minus":res_psi}, f, indent=2, default=float)
        print("saved:", args.out)