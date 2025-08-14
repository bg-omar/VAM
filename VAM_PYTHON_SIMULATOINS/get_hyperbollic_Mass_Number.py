# Parse Fourier series files as coefficient matrices and evaluate 3D curves.
# Then compute: closure error, length, writhe (Gauss double integral, discretized),
# estimate min crossing number via multi-direction projections,
# and compute Hvortex_X and Hvortex_Vol plus VAM masses using user's constants.

import numpy as np, math, os, pandas as pd
import IPython.display as display

# Files
files = [
    "./knots/4_1/knot.4_1.fseries",
    "./knots/4_1/knot.4_1d.fseries",
    "./knots/4_1/knot.4_1p.fseries",
    "./knots/4_1/knot.4_1z.fseries",
]

# Load helper from previous cell context (redefine if needed)
def load_matrix(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]
    data = []
    for line in lines:
        try:
            row = [float(x) for x in line.replace(",", " ").split()]
            data.append(row)
        except ValueError:
            pass
    maxlen = max(len(r) for r in data) if data else 0
    data = [r + [float('nan')] * (maxlen - len(r)) for r in data]
    return np.array(data, dtype=float)

def eval_series(coeffs, t):
    """
    coeffs: array of shape (N, 6): [Ax, Bx, Ay, By, Az, Bz] per harmonic index n
    t: array of shape (M,)
    Returns r(t) and r'(t)
    Interpretation: row k corresponds to harmonic n=k (including k=0).
    """
    N = coeffs.shape[0]
    # Prepare cos/sin arrays for n=0..N-1
    # For n=0: cos(0)=1, sin(0)=0
    n = np.arange(N).reshape(-1, 1)  # (N,1)
    nt = n * t.reshape(1, -1)        # (N,M)
    cos_nt = np.cos(nt)
    sin_nt = np.sin(nt)
    Ax, Bx, Ay, By, Az, Bz = [coeffs[:,i].reshape(-1,1) for i in range(6)]
    # Position
    x = (Ax * cos_nt + Bx * sin_nt).sum(axis=0)
    y = (Ay * cos_nt + By * sin_nt).sum(axis=0)
    z = (Az * cos_nt + Bz * sin_nt).sum(axis=0)
    r = np.stack([x,y,z], axis=1)  # (M,3)
    # Derivative wrt t: d/dt [A cos(nt)+B sin(nt)] = -n A sin(nt) + n B cos(nt)
    # n is (N,1), broadcast over M
    x_t = ((-n * Ax) * sin_nt + (n * Bx) * cos_nt).sum(axis=0)
    y_t = ((-n * Ay) * sin_nt + (n * By) * cos_nt).sum(axis=0)
    z_t = ((-n * Az) * sin_nt + (n * Bz) * cos_nt).sum(axis=0)
    r_t = np.stack([x_t,y_t,z_t], axis=1)  # (M,3)
    return r, r_t

def curve_length(r_t, dt):
    # Length = ∫ |r'(t)| dt
    speeds = np.linalg.norm(r_t, axis=1)
    return float(np.sum(speeds) * dt)

def writhe_gauss(r, r_t, dt):
    """
    Discretized Gauss double integral for writhe.
    Wr ≈ (1/(4π)) Σ_i Σ_j [ ((r'_i × r'_j)·(r_i - r_j)) / |r_i - r_j|^3 ] dt^2
    Avoid i=j and near neighbors by masking small separations.
    """
    M = r.shape[0]
    # Subsample to reduce O(M^2) cost if needed
    # Use all points up to 600 if larger
    maxM = 600
    if M > maxM:
        idx = np.linspace(0, M-1, maxM, dtype=int)
        r = r[idx]
        r_t = r_t[idx]
        M = maxM
        dt = 2*math.pi / M
    # Build pairwise arrays
    Ri = r[:,None,:]          # (M,1,3)
    Rj = r[None,:,:]          # (1,M,3)
    dR = Ri - Rj              # (M,M,3)
    dist = np.linalg.norm(dR, axis=2)  # (M,M)
    # Avoid singularity on diagonal
    eps_mask = dist > 1e-6
    # Tangent cross products
    Ti = r_t[:,None,:]        # (M,1,3)
    Tj = r_t[None,:,:]        # (1,M,3)
    cross = np.cross(Ti, Tj)  # (M,M,3)
    num = (cross * dR).sum(axis=2)     # (M,M)
    kernel = np.zeros_like(num)
    kernel[eps_mask] = num[eps_mask] / (dist[eps_mask]**3)
    Wr = (dt*dt) * kernel.sum() / (4*math.pi)
    return float(Wr)

def random_unit_vectors(k):
    v = np.random.normal(size=(k,3))
    v /= np.linalg.norm(v, axis=1, keepdims=True) + 1e-12
    return v

def estimate_crossing_number(r, directions=20):
    """
    Project the curve to 2D planes orthogonal to random directions and count segment intersections.
    Return minimal crossing count observed.
    """
    M = r.shape[0]
    # Segment endpoints
    P = r
    Q = np.roll(r, -1, axis=0)
    segs3D = np.stack([P, Q], axis=1)  # (M,2,3)
    min_cross = None
    # Orthonormal basis construction
    for d in random_unit_vectors(directions):
        # construct orthonormal frame (u,v,w) where w=d
        w = d / (np.linalg.norm(d) + 1e-12)
        tmp = np.array([1.0,0.0,0.0])
        if abs(np.dot(tmp,w)) > 0.9:
            tmp = np.array([0.0,1.0,0.0])
        u = np.cross(w, tmp)
        u /= np.linalg.norm(u) + 1e-12
        v = np.cross(w, u)
        # Project points
        P2 = np.stack([P@u, P@v], axis=1)
        Q2 = np.stack([Q@u, Q@v], axis=1)
        # Count 2D segment intersections (exclude adjacent and same segments)
        count = 0
        for i in range(M):
            p1, p2 = P2[i], Q2[i]
            for j in range(i+2, M):  # skip adjacent (i,i+1); last with first handled by modulo
                if j == (i-1) % M:   # also skip previous adjacent
                    continue
                q1, q2 = P2[j], Q2[j]
                # Fast bbox check
                if (max(p1[0], p2[0]) < min(q1[0], q2[0]) or
                    max(q1[0], q2[0]) < min(p1[0], p2[0]) or
                    max(p1[1], p2[1]) < min(q1[1], q2[1]) or
                    max(q1[1], q2[1]) < min(p1[1], p2[1])):
                    continue
                # Orientation test
                def orient(a,b,c):
                    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
                o1 = orient(p1,p2,q1)
                o2 = orient(p1,p2,q2)
                o3 = orient(q1,q2,p1)
                o4 = orient(q1,q2,p2)
                if (o1==0 and o2==0 and o3==0 and o4==0):
                    # Colinear; treat as no crossing for robustness
                    continue
                if (o1*o2<0) and (o3*o4<0):
                    count += 1
        if min_cross is None or count < min_cross:
            min_cross = count
    return int(min_cross if min_cross is not None else 0)

# Physical constants for mass computation (from previous cell)
C_e = 1_093_845.63
r_c = 1.40897017e-15
rho_fluid = 7.0e-7
rho_energy = 3.49924562e35
c = 299_792_458.0
alpha = 1/137.035999084
phi = (1+5**0.5)/2
E_density_fluid = 0.5 * rho_fluid * C_e**2
tube_area = math.pi * r_c**2
K_fluid = (4/(alpha*phi)) * (E_density_fluid / c**2) * tube_area   # kg/m
K_energy = (4/(alpha*phi)) * (rho_energy / c**2) * tube_area       # kg/m

VOL_BASELINE_VALUE = 2.029883212819307 # Vol(4_1)

# Evaluation parameters
M_samples = 1200
t = np.linspace(0, 2*math.pi, M_samples, endpoint=False)
dt = 2*math.pi / M_samples
b0 = 3

rows = []

for path in files:
    if not os.path.exists(path):
        continue
    coeffs = load_matrix(path)
    r, r_t = eval_series(coeffs, t)
    # Closure error
    closure = float(np.linalg.norm(r[0]-r[-1]))
    # Length
    L = curve_length(r_t, dt)
    # Writhe
    Wr = writhe_gauss(r, r_t, dt)
    # Sigma from writhe (tolerance near 0 => amphichiral/unknown)
    tol = 5e-3
    if abs(Wr) <= tol:
        sigma = 0
    else:
        sigma = 1 if Wr > 0 else -1
    # Crossing number estimate (approximate)
    min_cross = estimate_crossing_number(r, directions=24)
    # H_vortex_X
    HvX = sigma * max(min_cross - b0, 0)
    # Hyperbolic-volume normalized H (if 4_1, we know it's amphichiral => sigma=0)
    HvVol = sigma * (1.0)  # for 4_1 only; if sigma==0, this equals 0
    # Masses using tube model (per meter coefficients)
    xi = 1.0
    M_fluid = xi * (HvX if HvX!=0 else HvVol) * K_fluid * L
    M_energy = xi * (HvX if HvX!=0 else HvVol) * K_energy * L
    rows.append({
        "file": os.path.basename(path),
        "rows_coeff": coeffs.shape[0],
        "closure_error": closure,
        "length_m": L,
        "writhe": Wr,
        "sigma_from_writhe": sigma,
        "min_crossing_est": int(min_cross),
        "Hvortex_X": HvX,
        "Hvortex_Vol(assuming Vol/Vol(4_1)=1)": HvVol,
        "K_fluid_kg_per_m": K_fluid,
        "K_energy_kg_per_m": K_energy,
        "mass_fluid_kg": M_fluid,
        "mass_energy_kg": M_energy
    })

df = pd.DataFrame(rows)
display.display("Fourier-series-derived invariants (prototype)", df)

# Save CSV
out_path = "knots/4_1/fseries_4_1_results.csv"
df.to_csv(out_path, index=False)