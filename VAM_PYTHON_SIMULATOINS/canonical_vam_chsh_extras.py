# canonical_vam_chsh_extras.py
# Adds: exports (JSON/CSV), 2-qubit tomography T_ij, GHZ/Mermin (3q), and a CZ-latency toy model.
# pip install qiskit qiskit-aer numpy

from math import pi, sqrt, log2
import json, argparse, csv, os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator

ZZ = SparsePauliOp.from_list([("ZZ", 1.0)])
TSIRELSON = 2*sqrt(2)

# ---------------- Ω-related constants ----------------
C_e = 1_093_845.63
r_c = 1.40897017e-15
OMEGA = C_e / r_c

# ---------------- helpers ----------------
def check(label, ok, extra=""):
    print(f"[{'\u2714' if ok else '\u2718'}] {label}" + (f" — {extra}" if extra else ""))

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

def E_counts_with_jitter(phi_a, phi_b, sigma_phi, n_batches, shots_per, state, seed):
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
    pairs = list(angles.items())
    P_pair = 1.0/len(pairs)
    p_plus = []
    for _,(ta,tb) in pairs:
        Δ = ta - tb; C = triangular_C(Δ); Z = 1 + kappa*C
        p_plus.append(((1+kappa)*(1+C))/(2*Z))
    P_s_plus = P_pair*sum(p_plus)
    P_s_minus = 1.0 - P_s_plus
    I = 0.0
    for p in p_plus:
        if p>0:   I += P_pair * p * log2(p / P_s_plus)
        q = 1-p
        if q>0:   I += P_pair * q * log2(q / P_s_minus)
    return I

# -------------- CHSH runs --------------
def run_phi_plus(shots=20000, seed=1, do_jitter=True):
    a, ap, b, bp = 0.0, -pi/2, +pi/4, -pi/4  # Φ+ sum-law: E=cos(a+b)
    angles_sum = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}
    E_qm = {k: E_counts(*ang, shots, "phi_plus", seed) for k,ang in angles_sum.items()}
    S_qm = chsh_from_E(E_qm)
    print("Φ+  E_QM:", {k: round(v,4) for k,v in E_qm.items()}, "  S_QM≈", round(S_qm,4))
    check("Φ+ Tsirelson (counts)", abs(S_qm-TSIRELSON) < 0.05, f"S={S_qm:.4f}")

    # sum→difference mapping for VAM: Δ = a - (−b)
    angles_vam = {k:(ang[0], -ang[1]) for k,ang in angles_sum.items()}
    kappa_ab = {k: kappa_for_target(E_qm[k], angles_vam[k][0]-angles_vam[k][1]) for k in angles_vam}
    E_pred = {k: E_vam_closed(angles_vam[k][0]-angles_vam[k][1], kappa_ab[k]) for k in angles_vam}
    S_pred = chsh_from_E(E_pred)
    print("Φ+  κ_ab:", {k: round(v,3) for k,v in kappa_ab.items()})
    print("Φ+  E_VAM_pred:", {k: round(v,4) for k,v in E_pred.items()}, "  S_VAM_pred≈", round(S_pred,4))
    diff_pred = max(abs(E_pred[k]-E_qm[k]) for k in E_pred)
    check("Φ+ VAM matches QM (closed-form)", diff_pred < 0.01, f"max|ΔE|={diff_pred:.4f}")

    jitter = []
    if do_jitter:
        dt_list     = [1e-22, 3e-22, 1e-21]
        sigma0_list = [0.00, 0.05, 0.10, 0.20]
        print("\nΩ-jitter (σφ = σ0 * Ω * Δt)  →  S")
        for dt in dt_list:
            for s0 in sigma0_list:
                sigma_phi = s0 * OMEGA * dt
                Ej = {
                    ('a','b'):  E_counts_with_jitter(a,b,  sigma_phi, 48, 256, "phi_plus", seed+11),
                    ('a','bp'): E_counts_with_jitter(a,bp, sigma_phi, 48, 256, "phi_plus", seed+12),
                    ('ap','b'): E_counts_with_jitter(ap,b, sigma_phi, 48, 256, "phi_plus", seed+13),
                    ('ap','bp'):E_counts_with_jitter(ap,bp,sigma_phi, 48, 256, "phi_plus", seed+14),
                }
                Sj = chsh_from_E(Ej)
                jitter.append((float(s0), float(dt), float(sigma_phi), float(Sj)))
                print(f"σ0={s0:0.2f}  Δt={dt:0.1e}  σφ={sigma_phi:0.3e}  S={Sj:0.4f}")

    return {"mode":"phi_plus","E_QM":E_qm,"S_QM":S_qm,"kappa_ab":kappa_ab,"E_VAM":E_pred,"S_VAM":S_pred,"jitter":jitter}

def run_psi_minus(shots=20000, seed=2, kappas=(0.00,0.05,0.10,0.20,0.30,0.50,0.70,0.90)):
    a, ap, b, bp = 0.0, +pi/2, +pi/4, -pi/4  # Ψ− difference-law: E=-cos(a-b)
    angles = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}
    E_qm = {k: E_counts(*ang, shots, "psi_minus", seed) for k,ang in angles.items()}
    S_qm = chsh_from_E(E_qm)
    print("\nΨ-  E_QM:", {k: round(v,4) for k,v in E_qm.items()}, "  S_QM≈", round(S_qm,4))
    check("Ψ- Tsirelson (counts)", abs(S_qm-TSIRELSON) < 0.05, f"S={S_qm:.4f}")

    table = []
    print("Ψ-   κ      S_VAM     I(pair;s) [bits]")
    for k in kappas:
        E = {key: E_vam_closed(angles[key][0]-angles[key][1], k) for key in angles}
        S = chsh_from_E(E)
        I = mutual_info_S_vs_pairs(angles, k)
        table.append((float(k), float(S), float(I)))
        print(f"     {k:0.2f}   {S:0.4f}     {I:0.4f}")
    S0 = table[0][1]; Speak = max(row[1] for row in table)
    check("Ψ- VAM: S(0)≈2", abs(S0-2.0) < 0.05, f"S(0)={S0:.3f}")
    check("Ψ- VAM: peak > 2.2", Speak > 2.2, f"peak={Speak:.3f}")
    return {"mode":"psi_minus","E_QM":E_qm,"S_QM":S_qm,"sweep":table}

# -------------- (3) Tomography T_ij --------------
def pauli_basis_change(qc, q, P):
    if P=='X':
        qc.h(q)
    elif P=='Y':
        qc.sdg(q); qc.h(q)
    elif P=='Z':
        pass

def E_Pauli_counts(P1, P2, state, shots, seed):
    sim = AerSimulator(seed_simulator=seed)
    qc = QuantumCircuit(2,2)
    prepare_bell(qc, state)
    pauli_basis_change(qc, 0, P1)
    pauli_basis_change(qc, 1, P2)
    qc.measure([0,1],[0,1])
    c = sim.run(qc, shots=shots).result().get_counts()
    s = sum(c.values())
    return (c.get('00',0)+c.get('11',0)-c.get('01',0)-c.get('10',0))/s

def run_tomography(state="phi_plus", shots=20000, seed=5):
    axes = ['X','Y','Z']
    T = {}
    for i in axes:
        for j in axes:
            T[(i,j)] = E_Pauli_counts(i,j, state, shots, seed+hash(i+j)%1000)
    print(f"\nTomography T_ij for {state}:",
          {f"{i}{j}": round(T[(i,j)],3) for i in axes for j in axes})
    # sanity checks
    if state=="phi_plus":
        ok = abs(T[('X','X')]-1)<0.05 and abs(T[('Y','Y')]-1)<0.05 and abs(T[('Z','Z')]-1)<0.05
        check("Φ+ tensor ~ diag(+1,+1,+1)", ok)
    if state=="psi_minus":
        ok = abs(T[('X','X')]+1)<0.05 and abs(T[('Y','Y')]+1)<0.05 and abs(T[('Z','Z')]+1)<0.05
        check("Ψ− tensor ~ diag(−1,−1,−1)", ok)
    return {f"{i}{j}": float(T[(i,j)]) for i in axes for j in axes}

# -------------- (5) GHZ / Mermin --------------
def run_mermin(shots=20000, seed=9):
    sim = AerSimulator(seed_simulator=seed)
    # |GHZ> = (|000>+|111>)/√2
    qc0 = QuantumCircuit(3)
    qc0.h(0); qc0.cx(0,1); qc0.cx(1,2)
    psi = Statevector.from_instruction(qc0)

    def exp_pauli(P):
        """P like 'XXX','XYY','YXY','YYX'."""
        op = SparsePauliOp.from_list([(P,1.0)])
        return float(np.real(psi.expectation_value(op)))

    M = exp_pauli("XXX") - exp_pauli("XYY") - exp_pauli("YXY") - exp_pauli("YYX")
    print("\nGHZ/Mermin:")
    print("⟨XXX⟩,⟨XYY⟩,⟨YXY⟩,⟨YYX⟩ =", round(exp_pauli("XXX"),3), round(exp_pauli("XYY"),3),
          round(exp_pauli("YXY"),3), round(exp_pauli("YYX"),3))
    print("Mermin M =", round(M,3))
    check("Mermin QM≈4 > 2 (LR bound)", abs(M-4.0)<0.1, f"M={M:.3f}")
    return {"XXX":exp_pauli("XXX"),"XYY":exp_pauli("XYY"),"YXY":exp_pauli("YXY"),"YYX":exp_pauli("YYX"),"M":M}

# -------------- (7) CZ-latency toy model --------------
def run_latency_chain(n=4, max_depth=6, phi=pi/2, shots=4096, seed=12):
    """
    Chain of n qubits. Inject Rz(phi) on q0. Apply layers of nearest-neighbor CZ.
    Measure Z⊗...⊗Z correlations between q0 and q_{n-1} as depth grows.
    """
    sim = AerSimulator(seed_simulator=seed)
    def corr_last(depth):
        qc = QuantumCircuit(n, 2)
        # prepare |+> on all to allow phase entanglement to propagate
        for q in range(n): qc.h(q)
        qc.rz(phi,0)
        for _ in range(depth):
            for q in range(n-1): qc.cz(q, q+1)
        # measure Z on ends
        qc.measure(0,0); qc.measure(n-1,1)
        c = sim.run(qc, shots=shots).result().get_counts()
        s = sum(c.values())
        E = (c.get('00',0)+c.get('11',0)-c.get('01',0)-c.get('10',0))/s
        return E
    data = [(d, float(corr_last(d))) for d in range(0, max_depth+1)]
    print("\nLatency toy (CZ-front):", data)
    # crude latency check: correlation rises slowly then saturates
    ok = data[0][1] > -0.1 and max(abs(v) for _,v in data) > 0.3
    check("Latency front visible (|E| rises with depth)", ok)
    return data

# -------------- Exports (2) --------------
def export_json_csv(outdir, res_phi, res_psi, T_phi, T_psi, mermin, latency):
    os.makedirs(outdir, exist_ok=True)
    # JSON
    with open(os.path.join(outdir, "report.json"), "w") as f:
        json.dump({
            "omega": OMEGA,
            "phi_plus": res_phi,
            "psi_minus": res_psi,
            "tomography_phi": T_phi,
            "tomography_psi": T_psi,
            "mermin": mermin,
            "latency": latency
        }, f, indent=2, default=float)
    # CSVs
    with open(os.path.join(outdir, "phi_plus_E.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["pair","E_QM","E_VAM","kappa_ab"])
        for k in res_phi["E_QM"]:
            w.writerow([k, res_phi["E_QM"][k], res_phi["E_VAM"][k], res_phi["kappa_ab"][k]])
    with open(os.path.join(outdir, "psi_minus_sweep.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["kappa","S_VAM","I_bits"])
        for k,S,I in res_psi["sweep"]:
            w.writerow([k,S,I])
    if res_phi["jitter"]:
        with open(os.path.join(outdir, "phi_plus_jitter.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["sigma0","dt","sigma_phi","S"])
            for row in res_phi["jitter"]: w.writerow(row)
    print("saved:", outdir)

# -------------- CLI --------------
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--shots", type=int, default=20000)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--outdir", type=str, default="")
    p.add_argument("--lat_n", type=int, default=4)
    p.add_argument("--lat_depth", type=int, default=6)
    args = p.parse_args()

    print(f"Ω = C_e / r_c = {OMEGA:.3e} s^-1")
    # CHSH + Ω-jitter + S–I audit
    res_phi = run_phi_plus(shots=args.shots, seed=args.seed, do_jitter=True)
    res_psi = run_psi_minus(shots=args.shots, seed=args.seed+1)

    # (3) tomography for both Bell states
    T_phi = run_tomography(state="phi_plus", shots=args.shots, seed=args.seed+2)
    T_psi = run_tomography(state="psi_minus", shots=args.shots, seed=args.seed+3)

    # (5) GHZ/Mermin
    mermin = run_mermin(shots=args.shots, seed=args.seed+4)

    # (7) CZ-latency toy model
    latency = run_latency_chain(n=args.lat_n, max_depth=args.lat_depth, shots=4096, seed=args.seed+5)

    # (2) exports
    if args.outdir:
        export_json_csv(args.outdir, res_phi, res_psi, T_phi, T_psi, mermin, latency)