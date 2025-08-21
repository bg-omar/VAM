import os, sys, math, glob, argparse
import numpy as np
import pandas as pd

# ---------- Constants: user-provided VAM parameters ----------
C_e = 1_093_845.63             # m/s
r_c = 1.40897017e-15           # m
rho_fluid = 7.0e-7             # kg/m^3
rho_energy = 3.49924562e35     # J/m^3
c = 299_792_458.0              # m/s
alpha = 1/137.035999084
phi = (1+5**0.5)/2
VOL_BASELINE_VALUE = 2.029883212819307  # Vol(4_1)

# Derived per-meter coefficients (kg/m)
E_density_fluid = 0.5 * rho_fluid * C_e**2
tube_area = math.pi * r_c**2
K_fluid = (4/(alpha*phi)) * (E_density_fluid / c**2) * tube_area   # kg/m
K_energy = (4/(alpha*phi)) * (rho_energy / c**2) * tube_area       # kg/m

# ---------- Utilities ----------
def load_matrix(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]
    data = []
    for ln in lines:
        try:
            row = [float(x) for x in ln.replace(",", " ").split()]
            data.append(row)
        except ValueError:
            # skip non-numeric lines
            pass
    if not data:
        return np.zeros((0,6), dtype=float)
    maxlen = max(len(r) for r in data)
    data = [r + [float('nan')] * (maxlen - len(r)) for r in data]
    arr = np.array(data, dtype=float)
    # Pad to 6 columns if necessary
    if arr.shape[1] < 6:
        pad = np.full((arr.shape[0], 6 - arr.shape[1]), np.nan, dtype=float)
        arr = np.concatenate([arr, pad], axis=1)
    return arr

def eval_series(coeffs, t):
    """Return r(t) and r'(t) from Fourier coefficients.
    coeffs shape: (N,6) columns [Ax, Bx, Ay, By, Az, Bz]; nth row -> harmonic n.
    """
    if coeffs.size == 0:
        return np.zeros((t.size,3)), np.zeros((t.size,3))
    N = coeffs.shape[0]
    n = np.arange(N).reshape(-1, 1)
    nt = n * t.reshape(1, -1)
    cos_nt = np.cos(nt); sin_nt = np.sin(nt)
    Ax, Bx, Ay, By, Az, Bz = [coeffs[:,i].reshape(-1,1) for i in range(6)]
    x = (Ax * cos_nt + Bx * sin_nt).sum(axis=0)
    y = (Ay * cos_nt + By * sin_nt).sum(axis=0)
    z = (Az * cos_nt + Bz * sin_nt).sum(axis=0)
    r = np.stack([x,y,z], axis=1)
    x_t = ((-n * Ax) * sin_nt + (n * Bx) * cos_nt).sum(axis=0)
    y_t = ((-n * Ay) * sin_nt + (n * By) * cos_nt).sum(axis=0)
    z_t = ((-n * Az) * sin_nt + (n * Bz) * cos_nt).sum(axis=0)
    r_t = np.stack([x_t,y_t,z_t], axis=1)
    return r, r_t

def curve_length(r_t, dt):
    return float(np.sum(np.linalg.norm(r_t, axis=1)) * dt)

def writhe_gauss(r, r_t, dt, maxM=500):
    """Discretized Gauss integral. Costs O(M^2); downsample to maxM points."""
    M = r.shape[0]
    if M > maxM:
        idx = np.linspace(0, M-1, maxM, dtype=int)
        r = r[idx]; r_t = r_t[idx]
        M = maxM
        dt = 2*math.pi / M
    Ri = r[:,None,:]; Rj = r[None,:,:]
    dR = Ri - Rj
    dist = np.linalg.norm(dR, axis=2)
    mask = dist > 1e-6
    Ti = r_t[:,None,:]; Tj = r_t[None,:,:]
    cross = np.cross(Ti, Tj)
    num = (cross * dR).sum(axis=2)
    kernel = np.zeros_like(num)
    kernel[mask] = num[mask] / (dist[mask]**3)
    Wr = (dt*dt) * kernel.sum() / (4*math.pi)
    return float(Wr)

def random_unit_vectors(k, seed=12345):
    rng = np.random.default_rng(seed)
    v = rng.normal(size=(k,3))
    v /= np.linalg.norm(v, axis=1, keepdims=True) + 1e-12
    return v

def estimate_crossing_number(r, directions=24, maxM=280, seed=12345):
    """Projection-based crossing estimator. Downsample to maxM for speed."""
    M = r.shape[0]
    if M > maxM:
        idx = np.linspace(0, M-1, maxM, dtype=int)
        r = r[idx]
        M = maxM
    P = r
    Q = np.roll(r, -1, axis=0)
    min_cross = None
    for d in random_unit_vectors(directions, seed=seed):
        w = d / (np.linalg.norm(d) + 1e-12)
        tmp = np.array([1.0,0.0,0.0])
        if abs(np.dot(tmp,w)) > 0.9:
            tmp = np.array([0.0,1.0,0.0])
        u = np.cross(w, tmp); u /= np.linalg.norm(u) + 1e-12
        v = np.cross(w, u)
        P2 = np.stack([P@u, P@v], axis=1)
        Q2 = np.stack([Q@u, Q@v], axis=1)
        count = 0
        for i in range(M):
            p1, p2 = P2[i], Q2[i]
            pminx, pmaxx = min(p1[0], p2[0]), max(p1[0], p2[0])
            pminy, pmaxy = min(p1[1], p2[1]), max(p1[1], p2[1])
            for j in range(i+2, M):
                if j == (i-1) % M:
                    continue
                q1, q2 = P2[j], Q2[j]
                if (pmaxx < min(q1[0], q2[0]) or max(q1[0], q2[0]) < pminx or
                    pmaxy < min(q1[1], q2[1]) or max(q1[1], q2[1]) < pminy):
                    continue
                def orient(a,b,c):
                    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
                o1 = orient(p1,p2,q1); o2 = orient(p1,p2,q2)
                o3 = orient(q1,q2,p1); o4 = orient(q1,q2,p2)
                if (o1==0 and o2==0 and o3==0 and o4==0):
                    continue
                if (o1*o2<0) and (o3*o4<0):
                    count += 1
        if (min_cross is None) or (count < min_cross):
            min_cross = count
    return int(min_cross if min_cross is not None else 0)

def parse_knot_id_from_filename(fname):
    base = os.path.basename(fname)
    name = os.path.splitext(base)[0]
    parts = name.split(".")
    for p in parts[::-1]:
        if "_" in p:
            return p
    return name

def main():
    ap = argparse.ArgumentParser(description="Batch *.fseries → VAM invariants and masses")
    ap.add_argument("--dir", type=str, default=".", help="Directory to scan for *.fseries")
    ap.add_argument("--out", type=str, default="fseries_batch_results.csv", help="Output CSV path")
    ap.add_argument("--scale", type=float, default=1.0, help="Meters per series unit (global scale)")
    ap.add_argument("--xi", type=float, default=1.0, help="Coherence factor xi (global)")
    ap.add_argument("--b0", type=float, default=3.0, help="Crossing baseline offset")
    ap.add_argument("--samples", type=int, default=1500, help="Time samples along curve (higher->more accurate)")
    ap.add_argument("--wr_maxM", type=int, default=520, help="Max points for writhe O(N^2) integral")
    ap.add_argument("--cr_dirs", type=int, default=28, help="Number of random directions for crossing estimate")
    ap.add_argument("--cr_maxM", type=int, default=260, help="Downsample points for crossing estimator")
    ap.add_argument("--sigma_mode", type=str, default="meta", choices=["meta","writhe"],
                    help="How to set sigma: 'meta' (from CSV) or 'writhe' (sign of Wr, |Wr|<tol→0)")
    ap.add_argument("--meta", type=str, default="", help="Optional CSV with columns: knot_id,chiral(yes/no),sigma(+1|-1|0),type,hyperbolic_volume")
    ap.add_argument("--wr_tol", type=float, default=5e-3, help="If sigma_mode=writhe, |Wr|<=tol → sigma=0")
    args = ap.parse_args()

    # Load meta if provided
    meta = None
    if args.meta and os.path.exists(args.meta):
        meta = pd.read_csv(args.meta)
        meta_cols = {c.lower():c for c in meta.columns}
        def col(name): 
            key = name.lower()
            return meta[meta_cols[key]] if key in meta_cols else None
        std = pd.DataFrame()
        std["knot_id"] = col("knot_id").astype(str) if col("knot_id") is not None else ""
        std["chiral"] = col("chiral").astype(str).str.lower() if col("chiral") is not None else ""
        std["sigma"] = col("sigma") if col("sigma") is not None else np.nan
        std["type"] = col("type") if col("type") is not None else ""
        std["hyperbolic_volume"] = col("hyperbolic_volume") if col("hyperbolic_volume") is not None else np.nan
        meta = std.set_index("knot_id")
    else:
        meta = None

    root_dir = os.path.join(os.getcwd(), "knots")
    # Scan directory
    # Recursively find *.fseries and *.short
    files = sorted(glob.glob(os.path.join(root_dir, "**", "*.fseries"), recursive=True))
    files += sorted(glob.glob(os.path.join(root_dir, "**", "*.short"), recursive=True))
    if not files:
        raise RuntimeError(f"No .fseries or .short files found under: {root_dir}")

    if not files:
        print("No .fseries files found in", args.dir)
        return

    # Time grid
    t = np.linspace(0, 2*math.pi, args.samples, endpoint=False)
    dt = 2*math.pi / args.samples

    rows = []
    for path in files:
        coeffs = load_matrix(path)
        r, r_t = eval_series(coeffs, t)
        closure = float(np.linalg.norm(r[0]-r[-1]))
        L_series = float(np.sum(np.linalg.norm(r_t, axis=1)) * dt)
        Wr = writhe_gauss(r, r_t, dt, maxM=args.wr_maxM)
        cr_est = estimate_crossing_number(r, directions=args.cr_dirs, maxM=args.cr_maxM)
        knot_id = parse_knot_id_from_filename(path)

        sigma_meta = np.nan; chiral_meta = ""; vol_meta = np.nan; type_meta = ""
        if meta is not None and knot_id in meta.index:
            rowm = meta.loc[knot_id]
            chiral_meta = str(rowm.get("chiral",""))
            type_meta = str(rowm.get("type",""))
            try:
                sigma_meta = float(rowm.get("sigma", np.nan))
            except Exception:
                sigma_meta = np.nan
            try:
                vol_meta = float(rowm.get("hyperbolic_volume", np.nan))
            except Exception:
                vol_meta = np.nan

        if args.sigma_mode == "meta":
            if isinstance(sigma_meta, float) and np.isnan(sigma_meta):
                sigma = 0.0 if abs(Wr) <= args.wr_tol else (1.0 if Wr>0 else -1.0)
                sigma_source = "writhe_fallback"
            else:
                try:
                    sigma = float(sigma_meta)
                except Exception:
                    sigma = 0.0 if abs(Wr) <= args.wr_tol else (1.0 if Wr>0 else -1.0)
                    sigma_source = "writhe_fallback"
                else:
                    sigma_source = "meta"
        else:
            sigma = 0.0 if abs(Wr) <= args.wr_tol else (1.0 if Wr>0 else -1.0)
            sigma_source = "writhe"

        HvX = sigma * max(cr_est - args.b0, 0.0)
        HvVol = np.nan
        if not np.isnan(vol_meta) and sigma != 0.0:
            HvVol = sigma * (vol_meta / VOL_BASELINE_VALUE)

        L_phys = args.scale * L_series
        xi = args.xi
        H_used = HvX if np.isnan(HvVol) else HvVol
        M_fluid = xi * H_used * K_fluid * L_phys
        M_energy = xi * H_used * K_energy * L_phys

        rows.append({
            "file": os.path.basename(path),
            "knot_id": knot_id,
            "harmonics_N": coeffs.shape[0],
            "closure_error": closure,
            "length_series_units": L_series,
            "scale_m_per_unit": args.scale,
            "length_m": L_phys,
            "writhe": Wr,
            "crossing_est": int(cr_est),
            "sigma": sigma,
            "sigma_source": sigma_source,
            "Hvortex_X(b0={:.0f})".format(args.b0): HvX,
            "hyperbolic_volume_meta": vol_meta,
            "Hvortex_Vol(Vol/Vol(4_1))": HvVol,
            "xi": xi,
            "K_fluid_kg_per_m": K_fluid,
            "K_energy_kg_per_m": K_energy,
            "mass_fluid_kg": M_fluid,
            "mass_energy_kg": M_energy,
            "type_meta": type_meta,
            "chiral_meta": chiral_meta
        })

    df = pd.DataFrame(rows)
    df.to_csv(args.out, index=False)
    print("Wrote:", args.out)
    print("Files processed:", len(files))
    print("Note: K_fluid = {:.6e} kg/m, K_energy = {:.6e} kg/m".format(K_fluid, K_energy))

if __name__ == "__main__":
    main()
