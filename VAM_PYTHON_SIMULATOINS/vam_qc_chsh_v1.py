# vam_qc_chsh_v1.py
# Local-only benchmark: Quantum CHSH on Aer + VAM Route-A replica + VAM-Ω-driven phase jitter
# pip install qiskit qiskit-aer

from math import pi, log2
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator

rng = np.random.default_rng(0)
ZZ = SparsePauliOp.from_list([("ZZ", 1.0)])

# ---------------------------
# VAM constants and Ω
# ---------------------------
C_e = 1_093_845.63             # m/s
r_c = 1.40897017e-15           # m
rho_fluid = 7.0e-7             # kg/m^3
rho_energy = 3.49924562e35     # J/m^3
c = 299_792_458.0              # m/s
alpha = 1/137.035999084


phi  = (1 + 5**0.5) / 2
phi2 = np.exp(np.arcsinh(0.5))   # asinh, not sinh

print(phi, phi2, abs(phi - phi2))

# Fixed-point equation: varphi = coth(1.5 * ln(varphi))
def varphi_fixed_point(varphi):
    return 1 / np.tanh(1.5 * np.log(varphi))

OMEGA = C_e / r_c                    # s^-1  swirl clock frequency

# ---------------------------
# Quantum CHSH utilities (RZ;H mapping → E = cos(phi_a - phi_b))
# ---------------------------
def qc_E_counts(phi_a, phi_b, shots=20000):
    qc = QuantumCircuit(2, 2)
    qc.h(0); qc.cx(0, 1)               # |Φ+>
    qc.rz(phi_a, 0); qc.h(0)           # measure σ_φa
    qc.rz(phi_b, 1); qc.h(1)           # measure σ_φb
    qc.measure([0, 1], [0, 1])         # q0->c0 (right), q1->c1 (left)
    counts = AerSimulator().run(qc, shots=shots).result().get_counts()
    s = sum(counts.values())
    if s == 0: return 0.0
    return (counts.get('00', 0) + counts.get('11', 0)
            - counts.get('01', 0) - counts.get('10', 0)) / s

def qc_E_statevector(phi_a, phi_b):
    qc = QuantumCircuit(2)
    qc.h(0); qc.cx(0, 1)
    qc.rz(phi_a, 0); qc.h(0)
    qc.rz(phi_b, 1); qc.h(1)
    psi = Statevector.from_instruction(qc)
    return float(np.real(psi.expectation_value(ZZ)))  # = cos(phi_a - phi_b)

def qc_E_with_phase_jitter(phi_a, phi_b, sigma_phi, n_jitter=64, shots_per=256):
    """
    Per-jitter-sample angle noise: δa,δb ~ N(0, sigma_phi^2).
    Accumulate counts over many small batches to approximate per-shot jitter.
    """
    tot = {'00':0, '01':0, '10':0, '11':0}
    sim = AerSimulator()
    for _ in range(n_jitter):
        da = rng.normal(0.0, sigma_phi)
        db = rng.normal(0.0, sigma_phi)
        qc = QuantumCircuit(2, 2)
        qc.h(0); qc.cx(0, 1)
        qc.rz(phi_a + da, 0); qc.h(0)
        qc.rz(phi_b + db, 1); qc.h(1)
        qc.measure([0,1],[0,1])
        c = sim.run(qc, shots=shots_per).result().get_counts()
        for k,v in c.items(): tot[k] = tot.get(k,0) + v
    s = sum(tot.values())
    return (tot.get('00',0)+tot.get('11',0)-tot.get('01',0)-tot.get('10',0))/s

def chsh_from_E(E):
    return abs(E[('a','b')] + E[('a','bp')] + E[('ap','b')] - E[('ap','bp')])

# ---------------------------
# VAM Route-A (global κ)
# ---------------------------
def E_vam_pair(theta_a, theta_b, kappa, shots=200000):
    """
    Hidden axis u ∈ [0,2π).
    A = sign(cos(u-a)),  B = -sign(cos(u-b)).
    Measurement-dependence: p(u|a,b) ∝ 1 + κ * sign(cos(u-a)) * sign(cos(u-b)).
    """
    good = bad = 0
    for _ in range(shots):
        while True:
            u = rng.random()*2*pi
            sA = 1 if np.cos(u - theta_a) >= 0 else -1
            sB = 1 if np.cos(u - theta_b) >= 0 else -1
            if rng.random() < (1 + kappa*(sA*sB))/2:
                A, B = sA, -sB
                break
        if A==B: good += 1
        else:    bad  += 1
    return (good - bad)/(good + bad)

def fit_global_kappa(targets, angles, grid=np.linspace(0,0.95,19)):
    best = (1e9, None)
    for k in grid:
        mse = 0.0
        for key in angles:
            Ev = E_vam_pair(*angles[key], kappa=k, shots=60_000)
            mse += (Ev - targets[key])**2
        mse /= len(angles)
        if mse < best[0]: best = (mse, k)
    return best  # (mse, kappa)

def sweep_kappa_S(kappas, angles, shots_per_pair=40_000):
    out = []
    for k in kappas:
        E = {key: E_vam_pair(*angles[key], kappa=k, shots=shots_per_pair) for key in angles}
        out.append((k, chsh_from_E(E)))
    return out

def prepare_bell(qc, kind="phi_plus"):
    qc.h(0); qc.cx(0,1)
    if kind == "psi_minus":
        qc.x(1); qc.z(1)  # |Φ+> → |Ψ-> up to global phase

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    # CHSH angles for RZ;H mapping
    a  = 0.0
    ap = -np.pi/2   # <-- flip sign
    b  =  np.pi/4
    bp = -np.pi/4

    angles = {('a','b'):(a,b), ('a','bp'):(a,bp), ('ap','b'):(ap,b), ('ap','bp'):(ap,bp)}

    print(f"Ω = C_e / r_c = {OMEGA:.3e} s^-1")

    qc = QuantumCircuit(2,2)
    prepare_bell(qc, kind="psi_minus")
    print("targets:", np.cos(a+b), np.cos(a+bp), np.cos(ap+b), np.cos(ap+bp))


    # 1) Ideal statevector sanity check
    Esv = {
        ('a','b'):  qc_E_statevector(a,b),
        ('a','bp'): qc_E_statevector(a,bp),
        ('ap','b'): qc_E_statevector(ap,b),
        ('ap','bp'):qc_E_statevector(ap,bp),
    }
    print("Statevector E’s:", {k: round(v,4) for k,v in Esv.items()},
          "  S≈", round(chsh_from_E(Esv), 4))

    # 2) Aer counts without jitter
    Eqm = {
        ('a','b'):  qc_E_counts(a,b,  shots=20_000),
        ('a','bp'): qc_E_counts(a,bp, shots=20_000),
        ('ap','b'): qc_E_counts(ap,b, shots=20_000),
        ('ap','bp'):qc_E_counts(ap,bp,shots=20_000),
    }
    print("Aer counts E’s:", {k: round(v,4) for k,v in Eqm.items()},
          "  S_QM≈", round(chsh_from_E(Eqm), 4))

    # 3) VAM-phase jitter: σφ = σ0 * Ω * Δt  (user knobs: σ0 and Δt)
    dt_list    = [1e-22, 3e-22, 1e-21]      # seconds
    sigma0_list= [0.00, 0.05, 0.10, 0.20]   # dimensionless
    print("\nS vs VAM phase jitter  (σφ = σ0 * Ω * Δt)")
    print("σ0    Δt[s]     σφ[rad]   S_QM_with_jitter")
    for dt in dt_list:
        for s0 in sigma0_list:
            sigma_phi = s0 * OMEGA * dt
            Ej = {
                ('a','b'):  qc_E_with_phase_jitter(a,b,  sigma_phi, n_jitter=48, shots_per=256),
                ('a','bp'): qc_E_with_phase_jitter(a,bp, sigma_phi, n_jitter=48, shots_per=256),
                ('ap','b'): qc_E_with_phase_jitter(ap,b, sigma_phi, n_jitter=48, shots_per=256),
                ('ap','bp'):qc_E_with_phase_jitter(ap,bp,sigma_phi, n_jitter=48, shots_per=256),
            }
            Sj = chsh_from_E(Ej)
            print(f"{s0:0.2f}  {dt:0.1e}  {sigma_phi:0.3e}   {Sj:0.4f}")

    # 4) VAM Route-A: fit a single κ to match the no-jitter Aer E’s, then sweep κ
    mse, kappa = fit_global_kappa(Eqm, angles)
    Ev_fit = {key: E_vam_pair(*angles[key], kappa=kappa, shots=200_000) for key in angles}
    print(f"\nVAM Route-A fit: κ≈{kappa:.2f}  MSE≈{mse:.3e}  "
          f"S_VAM_fit≈{chsh_from_E(Ev_fit):.4f}")
    print("E_VAM_fit:", {k: round(v,4) for k,v in Ev_fit.items()})

    kappas = [0.00, 0.10, 0.20, 0.30, 0.50, 0.70, 0.90]
    sweep = sweep_kappa_S(kappas, angles, shots_per_pair=40_000)
    print("\nS vs κ (Route-A sweep)")
    print("κ      S_VAM")
    for k,Sv in sweep:
        print(f"{k:0.2f}   {Sv:0.4f}")