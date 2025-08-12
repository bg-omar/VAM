from math import pi, log2
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# --- angles ---
a, ap = 0.0, pi/2
b, bp =  pi/4, -pi/4

def measure_counts(phi_a, phi_b, shots):
    qc = QuantumCircuit(2,2)
    qc.h(0); qc.cx(0,1)
    qc.rz(phi_a,0); qc.h(0)   # measure σ_φa
    qc.rz(phi_b,1); qc.h(1)   # measure σ_φb
    qc.measure([0,1],[0,1])
    sim = AerSimulator()
    return sim.run(qc, shots=shots).result().get_counts()

def corr_E(counts):
    s = sum(counts.values())
    if s == 0:
        return 0.0
    return (counts.get('00',0)+counts.get('11',0)
            -counts.get('01',0)-counts.get('10',0))/s

def chsh_from_counts(Cab, Cabp, Capb, Capbp):
    return abs(corr_E(Cab) + corr_E(Cabp) + corr_E(Capb) - corr_E(Capbp))

def mutual_information(joint):
    # joint dict: {(sa,sb,E): count}, sa∈{'a','ap'}, sb∈{'b','bp'}, E∈{0,1}
    N = sum(joint.values()); p = {k:v/N for k,v in joint.items()}
    pE, pS = {}, {}
    for (sa,sb,e),v in p.items():
        pE[e] = pE.get(e,0)+v
        pS[(sa,sb)] = pS.get((sa,sb),0)+v
    I = 0.0
    for (sa,sb,e),v in p.items():
        if v>0:
            I += v*log2(v/(pS[(sa,sb)]*pE[e]))
    return I

def run_experiment(delta=0.0, shots=20000, seed=123):
    """
    delta in [0, 0.5). E~Bern(1/2). Given E,
      P(sa='a' ) = 0.5 + (+/-) delta  with sign + for E=0, - for E=1
      P(sb='b' ) = 0.5 + (+/-) delta  with same sign
    Ensures all four pairs have nonzero probability.
    """
    rng = np.random.default_rng(seed)
    Cab, Cabp, Capb, Capbp = {}, {}, {}, {}
    joint = {}

    def add_counts(dest, angs, nshots):
        if nshots <= 0: return
        counts = measure_counts(*angs, shots=nshots)
        for k,v in counts.items():
            dest[k] = dest.get(k,0)+v

    # allocate shots by sampling; then top-up to avoid empties
    for _ in range(shots):
        E = rng.integers(0,2)
        pa = 0.5 + (delta if E==0 else -delta)
        pb = 0.5 + (delta if E==0 else -delta)
        sa = 'a' if rng.random()<pa else 'ap'
        sb = 'b' if rng.random()<pb else 'bp'

        if   sa=='a'  and sb=='b':   dest, angs = Cab,   (a,b)
        elif sa=='a'  and sb=='bp':  dest, angs = Cabp,  (a,bp)
        elif sa=='ap' and sb=='b':   dest, angs = Capb,  (ap,b)
        else:                        dest, angs = Capbp, (ap,bp)

        add_counts(dest, angs, 1)
        joint[(sa,sb,E)] = joint.get((sa,sb,E),0)+1

    # top-up any empty cell with a few shots so CHSH is defined
    for dest, angs in [(Cab,(a,b)), (Cabp,(a,bp)), (Capb,(ap,b)), (Capbp,(ap,bp))]:
        if sum(dest.values()) == 0:
            add_counts(dest, angs, 64)

    S = chsh_from_counts(Cab, Cabp, Capb, Capbp)
    I = mutual_information(joint)
    return S, I

for d in [0.0, 0.05, 0.10, 0.20, 0.30]:
    S, I = run_experiment(delta=d, shots=20000)
    print(f"delta={d:0.2f}  S≈{S:0.4f}  I≈{I:0.4f} bits")


    # fixed CHSH angles
a, ap = 0.0, pi/2
b, bp =  pi/4, -pi/4

def run_experiment(eps=0.0, shots=4096):
    """
    eps = 0: settings independent of E.
    eps -> 0.5: settings almost fully determined by E.
    Construction:
      Draw E ~ Bern(1/2).
      Given E=0: choose (a,b) with prob 1-eps, else (a,b') with eps.
      Given E=1: choose (a',b) with prob 1-eps, else (a',b') with eps.
    """
    rng = np.random.default_rng(123)
    joint = {}  # counts for mutual information
    # accumulate counts for each pair needed in CHSH
    Cab   = {}
    Cabp  = {}
    Capb  = {}
    Capbp = {}
    for _ in range(shots):
        E = rng.integers(0,2)
        if E==0:
            if rng.random() < 1-eps:
                sa, sb = 'a','b';  pa, pb = a,b
                dest = Cab
            else:
                sa, sb = 'a','bp'; pa, pb = a,bp
                dest = Cabp
        else:
            if rng.random() < 1-eps:
                sa, sb = 'ap','b';  pa, pb = ap,b
                dest = Capb
            else:
                sa, sb = 'ap','bp'; pa, pb = ap,bp
                dest = Capbp

        # one shot for this (sa,sb); do a small batch to reduce variance
        counts = measure_counts(pa, pb, shots=1)
        # merge into the appropriate accumulator
        for k,v in counts.items():
            dest[k] = dest.get(k,0)+v
        joint[(sa,sb,E)] = joint.get((sa,sb,E),0)+1

    S = chsh_from_counts(Cab, Cabp, Capb, Capbp)
    I = mutual_information(joint)
    return S, I, {'Cab':Cab,'Cabp':Cabp,'Capb':Capb,'Capbp':Capbp}

# sweep eps and print S and I
for eps in [0.0, 0.05, 0.10, 0.20, 0.30, 0.40]:
    S, I, _ = run_experiment(eps=eps, shots=20000)
    print(f"eps={eps:0.2f}  S≈{S:0.4f}   I(settings;E)≈{I:0.4f} bits")


    from math import pi, cos, sin
import numpy as np

def E_classical(theta_a, theta_b, kappa=0.0, shots=200000, seed=0):
    """
    Local deterministic model:
      A = sign( u · e(theta_a) ),  B = -sign( u · e(theta_b) )
    Hidden axis u on the unit circle. Measurement dependence:
      p(u | a,b) ∝ 1 + kappa * sign(u·e(a)) * sign(u·e(b))
    kappa in [0,1). kappa=0 gives S<=2; increasing kappa lifts S toward 2.828.
    """
    rng = np.random.default_rng(seed)
    def sample_u(a,b):
        while True:
            phi = rng.random()*2*pi
            w = 1 + kappa * np.sign(cos(phi-a)) * np.sign(cos(phi-b))
            if rng.random() < w/2:   # since w∈{0,2}
                return phi

    good = bad = 0
    for _ in range(shots):
        phi = sample_u(theta_a, theta_b)
        A = 1 if cos(phi-theta_a)>=0 else -1
        B = -1 if cos(phi-theta_b)>=0 else  1
        if A==B: good += 1
        else:    bad  += 1
    return (good - bad)/(good + bad)

def chsh_classical(kappa):
    a, ap = 0.0, pi/2
    b, bp =  pi/4, -pi/4
    return abs(E_classical(a,b,kappa)
               + E_classical(a,bp,kappa)
               + E_classical(ap,b,kappa)
               - E_classical(ap,bp,kappa))

for k in [0.0, 0.1, 0.3, 0.5, 0.8]:
    print(f"kappa={k:.1f}  S≈{chsh_classical(k):.3f}")