# VAM Fourier-Series Batch Processor GUI
# - Auto-scan on startup and when the root folder changes
# - Instant preview on selecting a row
# - Optional column cleanup (drop all-NaN and constant columns) before saving/showing results
#
# Requirements: Python 3.9+, numpy, pandas, tkinter, matplotlib

import os, sys, math, glob, csv, threading, traceback, struct
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Matplotlib for preview plots
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------- VAM constants (user-provided) ----------
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

# ---------- Core computations ----------
def load_matrix_fseries(path):
    """Load .fseries coefficients. Pad/truncate to 6 columns, fill missing with 0.0 (not NaN)."""
    rows = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            parts = ln.replace(",", " ").split()
            vals = []
            for x in parts[:6]:
                try:
                    vals.append(float(x))
                except Exception:
                    vals.append(0.0)
            while len(vals) < 6:
                vals.append(0.0)
            rows.append(vals)
    if not rows:
        return np.zeros((0,6), dtype=float)
    arr = np.asarray(rows, dtype=float)
    arr[~np.isfinite(arr)] = 0.0
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

def resample_closed_polyline(points, M):
    """Resample a closed polyline to M points, uniformly in arclength."""
    P = np.asarray(points, dtype=float)
    if P.shape[0] < 3:
        raise ValueError("Need at least 3 points in .short")
    # Ensure closed by appending first if not close
    if np.linalg.norm(P[0]-P[-1]) > 1e-12:
        P = np.vstack([P, P[0]])
    seg = P[1:] - P[:-1]
    seglen = np.linalg.norm(seg, axis=1)
    s = np.concatenate([[0.0], np.cumsum(seglen)])
    L = s[-1]
    if L <= 0:
        raise ValueError("Zero length polyline")
    u = np.linspace(0, L, M+1)[:-1]  # M points, periodic
    r = np.empty((M,3), dtype=float)
    j = 0
    for i,ui in enumerate(u):
        while j+1 < s.size and ui > s[j+1]:
            j += 1
        if j >= seg.shape[0]:
            j = seg.shape[0]-1
        t = (ui - s[j]) / (seglen[j] if seglen[j] > 0 else 1.0)
        r[i] = P[j] + t * seg[j]
    return r

def derivatives_from_uniform_samples(r):
    """Central-difference derivative r'(t) assuming uniform t-grid on [0,2pi)."""
    M = r.shape[0]
    dt = 2*math.pi / M
    rp = np.roll(r, -1, axis=0)
    rm = np.roll(r, 1, axis=0)
    r_t = (rp - rm) / (2*dt)
    return r_t, dt

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

# --- STL loader (ASCII or binary; minimal) ---
def load_stl(path, max_tris=200000):
    with open(path, "rb") as f:
        head = f.read(80)
        rest = f.read()
    # Try binary STL
    if len(rest) >= 4:
        num_tris = struct.unpack("<I", rest[:4])[0]
        expected = 4 + num_tris*50
        if len(rest) >= expected:
            tris = []
            off = 4
            n = min(num_tris, max_tris)
            for _ in range(n):
                chunk = rest[off:off+50]
                if len(chunk) < 50:
                    break
                data = struct.unpack("<12fH", chunk)
                v1 = data[3:6]; v2 = data[6:9]; v3 = data[9:12]
                tris.append([v1, v2, v3])
                off += 50
            return np.array(tris, dtype=float)  # (T,3,3)
    # Fallback: ASCII STL
    try:
        text = (head + rest).decode("utf-8", errors="ignore")
    except Exception:
        text = ""
    verts = []
    for line in text.splitlines():
        line = line.strip().lower()
        if line.startswith("vertex"):
            parts = line.split()
            if len(parts) >= 4:
                try:
                    x,y,z = float(parts[1]), float(parts[2]), float(parts[3])
                    verts.append((x,y,z))
                except Exception:
                    pass
    tris = []
    for i in range(0, len(verts), 3):
        tris.append(verts[i:i+3])
    if tris:
        return np.array(tris, dtype=float)
    raise ValueError("Failed to parse STL (binary or ASCII)")

# ---------- Batch engine ----------
def run_batch(root_dir, out_csv, scale=1.0, xi=1.0, b0=3.0, samples=1500,
              wr_maxM=520, cr_dirs=28, cr_maxM=260, sigma_mode="meta",
              meta_csv="", wr_tol=5e-3, emit_meta_path=""):
    # Recursively find *.fseries and *.short
    files = sorted(glob.glob(os.path.join(root_dir, "**", "*.fseries"), recursive=True))
    files += sorted(glob.glob(os.path.join(root_dir, "**", "*.short"), recursive=True))
    if not files:
        raise RuntimeError(f"No .fseries or .short files found under: {root_dir}")

    # Emit meta skeleton if requested
    if emit_meta_path:
        ids = discover_ids(files)
        with open(emit_meta_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["knot_id","chiral","sigma","type","hyperbolic_volume"])
            for kid in ids:
                w.writerow([kid, "", "", "", ""])

    # Load meta if provided
    meta = None
    if meta_csv and os.path.exists(meta_csv):
        meta = pd.read_csv(meta_csv)
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

    rows = []
    root_abs = os.path.abspath(root_dir)

    for path in files:
        ext = os.path.splitext(path)[1].lower()
        relpath = os.path.relpath(path, root_abs)
        knot_id = parse_knot_id_from_filename(path)

        # Evaluate r(t), r'(t)
        if ext == ".fseries":
            t = np.linspace(0, 2*math.pi, samples, endpoint=False)
            coeffs = load_matrix_fseries(path)
            r, r_t = eval_series(coeffs, t)
            dt = 2*math.pi / samples
        elif ext == ".short":
            points = []
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln:
                        continue
                    try:
                        xyz = [float(x) for x in ln.replace(",", " ").split()[:3]]
                        if len(xyz) == 3:
                            points.append(xyz)
                    except Exception:
                        pass
            if len(points) < 3:
                # skip file
                print(f"Skipping {relpath}: not enough points")
                continue
            r = resample_closed_polyline(points, samples)
            r_t, dt = derivatives_from_uniform_samples(r)
        else:
            continue  # ignore other types here

        closure = float(np.linalg.norm(r[0]-r[-1]))
        # polygonal length proxy in series units
        L_series = float(np.sum(np.linalg.norm(np.roll(r, -1, axis=0)-r, axis=1)))
        Wr = writhe_gauss(r, r_t, dt, maxM=wr_maxM)
        cr_est = estimate_crossing_number(r, directions=cr_dirs, maxM=cr_maxM)

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

        if sigma_mode == "meta":
            if isinstance(sigma_meta, float) and np.isnan(sigma_meta):
                sigma = 0.0 if abs(Wr) <= wr_tol else (1.0 if Wr>0 else -1.0)
                sigma_source = "writhe_fallback"
            else:
                try:
                    sigma = float(sigma_meta)
                except Exception:
                    sigma = 0.0 if abs(Wr) <= wr_tol else (1.0 if Wr>0 else -1.0)
                    sigma_source = "writhe_fallback"
                else:
                    sigma_source = "meta"
        else:
            sigma = 0.0 if abs(Wr) <= wr_tol else (1.0 if Wr>0 else -1.0)
            sigma_source = "writhe"

        HvX = sigma * max(cr_est - b0, 0.0)
        HvVol = np.nan
        if not np.isnan(vol_meta) and sigma != 0.0:
            HvVol = sigma * (vol_meta / VOL_BASELINE_VALUE)

        # Physical scaling
        L_phys = scale * L_series
        H_used = HvX if np.isnan(HvVol) else HvVol
        M_fluid = xi * H_used * K_fluid * L_phys
        M_energy = xi * H_used * K_energy * L_phys

        rows.append({
            "file": os.path.basename(path),
            "relative_path": relpath,
            "ext": ext,
            "knot_id": knot_id,
            "closure_error": closure,
            "length_series_units": L_series,
            "scale_m_per_unit": scale,
            "length_m": L_phys,
            "writhe": Wr,
            "crossing_est": int(cr_est),
            "sigma": sigma,
            "sigma_source": sigma_source,
            "Hvortex_X(b0={:.0f})".format(b0): HvX,
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
    df.to_csv(out_csv, index=False)
    return df

# DataFrame cleaning
def clean_dataframe(df: pd.DataFrame):
    # Drop all-NaN columns
    df2 = df.dropna(axis=1, how="all").copy()

    # Identify constant columns (single unique value or all values equal ignoring NaN)
    keep_cols = {"file","relative_path","ext","knot_id"}  # always keep identifiers
    const_cols = []
    for col in df2.columns:
        if col in keep_cols:
            continue
        series = df2[col]
        # consider NaNs equal by dropping them first
        vals = series.dropna().unique()
        if len(vals) <= 1:
            const_cols.append(col)

    if const_cols:
        df2 = df2.drop(columns=const_cols)

    return df2

# Quick single-file preview helper (lightweight)
def quick_preview_any(path, profile, b0=3.0, wr_tol=5e-3):
    ext = os.path.splitext(path)[1].lower()
    prof = profile
    if ext == ".fseries":
        coeffs = load_matrix_fseries(path)
        if coeffs.size == 0:
            raise RuntimeError("Empty .fseries")
        t = np.linspace(0, 2*math.pi, prof["samples"], endpoint=False)
        r, r_t = eval_series(coeffs, t)
        dt = 2*math.pi / prof["samples"]
    elif ext == ".short":
        pts = []
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    xyz = [float(x) for x in ln.replace(",", " ").split()[:3]]
                    if len(xyz) == 3:
                        pts.append(xyz)
                except Exception:
                    pass
        if len(pts) < 3:
            raise RuntimeError("Not enough points in .short")
        r = resample_closed_polyline(pts, prof["samples"])
        r_t, dt = derivatives_from_uniform_samples(r)
    elif ext == ".stl":
        tris = load_stl(path)
        return {"stl_tris": tris.shape[0]}
    else:
        raise RuntimeError(f"Unsupported extension: {ext}")

    if not np.all(np.isfinite(r)):
        raise RuntimeError("Non-finite coordinates (check coefficients/points)")

    closure = float(np.linalg.norm(r[0]-r[-1]))
    L_series = float(np.sum(np.linalg.norm(np.roll(r, -1, axis=0)-r, axis=1)))
    Wr = writhe_gauss(r, r_t, dt, maxM=prof["wr_maxM"])
    cr_est = estimate_crossing_number(r, directions=prof["cr_dirs"], maxM=prof["cr_maxM"])
    sigma_est = 0.0 if abs(Wr) <= wr_tol else (1.0 if Wr>0 else -1.0)
    HvX = sigma_est * max(cr_est - b0, 0.0)
    return {
        "closure_error": closure,
        "length_series_units": L_series,
        "writhe": Wr,
        "crossing_est": int(cr_est),
        "sigma_from_writhe": sigma_est,
        "Hvortex_X_est(b0={:.0f})".format(b0): HvX,
        "r": r, "r_t": r_t
    }

# Quick status check for scan
def quick_status(path):
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".fseries":
            coeffs = load_matrix_fseries(path)
            if coeffs.size == 0:
                return "empty_fseries"
            if not np.any(np.abs(coeffs) > 0):
                return "all_zero_coeffs"
            return "ok"
        elif ext == ".short":
            pts = []
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln:
                        continue
                    parts = ln.replace(",", " ").split()
                    if len(parts) >= 3:
                        try:
                            x,y,z = float(parts[0]), float(parts[1]), float(parts[2])
                            pts.append((x,y,z))
                        except Exception:
                            pass
            if len(pts) < 3:
                return "insufficient_points"
            P = np.asarray(pts, dtype=float)
            if not np.all(np.isfinite(P)):
                return "nonfinite_points"
            return "ok"
        elif ext == ".stl":
            base = os.path.splitext(path)[0]
            sib = None
            for cand_ext in (".short", ".fseries"):
                cand = base + cand_ext
                if os.path.exists(cand):
                    sib = cand; break
            return "stl_curve_ok" if sib else "stl_no_sibling_curve"
        else:
            return "ignored"
    except Exception as e:
        return f"error:{type(e).__name__}"

# ---------- GUI ----------
QUALITY_PROFILES = {
    "Ultra Fast": dict(samples=600,  wr_maxM=240, cr_dirs=10, cr_maxM=160),
    "Fast":       dict(samples=900,  wr_maxM=360, cr_dirs=14, cr_maxM=200),
    "Balanced":   dict(samples=1500, wr_maxM=520, cr_dirs=28, cr_maxM=260),
    "High Quality": dict(samples=2400, wr_maxM=700, cr_dirs=48, cr_maxM=360),
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VAM Fourier-Series Processor")
        self.geometry("1320x880")
        self.resizable(True, True)

        # Defaults to knots\ under CWD
        default_root = os.path.join(os.getcwd(), "knots")
        default_out = os.path.join(default_root, "fseries_batch_results.csv")
        default_meta = os.path.join(default_root, "knot_meta.csv")
        default_emit = os.path.join(default_root, "knot_meta_skeleton.csv")

        # Variables
        self.var_root = tk.StringVar(value=default_root)
        self.var_out = tk.StringVar(value=default_out)
        self.var_meta = tk.StringVar(value=default_meta)
        self.var_emit_meta = tk.StringVar(value=default_emit)

        self.var_scale = tk.DoubleVar(value=1.0)
        self.var_xi = tk.DoubleVar(value=1.0)
        self.var_b0 = tk.DoubleVar(value=3.0)
        self.var_samples = tk.IntVar(value=1500)
        self.var_wr_maxM = tk.IntVar(value=520)
        self.var_cr_dirs = tk.IntVar(value=28)
        self.var_cr_maxM = tk.IntVar(value=260)
        self.var_wr_tol = tk.DoubleVar(value=5e-3)
        self.var_sigma_mode = tk.StringVar(value="meta")  # 'meta' or 'writhe'
        self.var_quality = tk.StringVar(value="Balanced")
        self.var_plot_preview = tk.BooleanVar(value=True)
        self.var_clean_cols = tk.BooleanVar(value=True)  # drop all-NaN & constants

        self.last_df = None  # store last results dataframe
        self._scan_after_id = None  # debounce id

        # Build UI
        self._build_widgets()

        # Bind root changes to auto-rescan (debounced)
        self.var_root.trace_add("write", self._on_root_change)

        # Auto-scan on boot
        self.after(200, self.on_scan)

    def _build_widgets(self):
        pad = {'padx': 6, 'pady': 4}

        # Paths frame
        frm_paths = ttk.LabelFrame(self, text="Paths")
        frm_paths.pack(fill="x", **pad)

        ttk.Label(frm_paths, text="Knot root folder:").grid(row=0, column=0, sticky="w")
        e_root = ttk.Entry(frm_paths, textvariable=self.var_root, width=80)
        e_root.grid(row=0, column=1, sticky="we")
        ttk.Button(frm_paths, text="Browse…", command=self.browse_root).grid(row=0, column=2, sticky="we", padx=4)

        ttk.Label(frm_paths, text="Output CSV:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frm_paths, textvariable=self.var_out, width=80).grid(row=1, column=1, sticky="we")
        ttk.Button(frm_paths, text="Save As…", command=self.browse_out).grid(row=1, column=2, sticky="we", padx=4)

        ttk.Label(frm_paths, text="Meta CSV (optional):").grid(row=2, column=0, sticky="w")
        ttk.Entry(frm_paths, textvariable=self.var_meta, width=80).grid(row=2, column=1, sticky="we")
        ttk.Button(frm_paths, text="Browse…", command=self.browse_meta).grid(row=2, column=2, sticky="we", padx=4)

        ttk.Label(frm_paths, text="Emit meta skeleton to (optional):").grid(row=3, column=0, sticky="w")
        ttk.Entry(frm_paths, textvariable=self.var_emit_meta, width=80).grid(row=3, column=1, sticky="we")
        ttk.Button(frm_paths, text="Save As…", command=self.browse_emit_meta).grid(row=3, column=2, sticky="we", padx=4)

        for i in range(3):
            frm_paths.columnconfigure(i, weight=1 if i==1 else 0)

        # Options frame
        frm_opts = ttk.LabelFrame(self, text="Options")
        frm_opts.pack(fill="x", **pad)

        # Row 0
        ttk.Label(frm_opts, text="Quality:").grid(row=0, column=0, sticky="w")
        cmb = ttk.Combobox(frm_opts, textvariable=self.var_quality, state="readonly",
                           values=list(QUALITY_PROFILES.keys()), width=18)
        cmb.grid(row=0, column=1, sticky="w")
        cmb.bind("<<ComboboxSelected>>", self.on_quality_change)

        ttk.Label(frm_opts, text="Scale (m per series unit):").grid(row=0, column=2, sticky="w")
        ttk.Entry(frm_opts, textvariable=self.var_scale, width=10).grid(row=0, column=3, sticky="w")
        ttk.Label(frm_opts, text="ξ (coherence):").grid(row=0, column=4, sticky="w")
        ttk.Entry(frm_opts, textvariable=self.var_xi, width=10).grid(row=0, column=5, sticky="w")

        # Row 1
        ttk.Label(frm_opts, text="b₀ (crossing offset):").grid(row=1, column=0, sticky="w")
        ttk.Entry(frm_opts, textvariable=self.var_b0, width=10).grid(row=1, column=1, sticky="w")
        ttk.Label(frm_opts, text="Samples (t-grid):").grid(row=1, column=2, sticky="w")
        ttk.Entry(frm_opts, textvariable=self.var_samples, width=10).grid(row=1, column=3, sticky="w")
        ttk.Label(frm_opts, text="Wr max points:").grid(row=1, column=4, sticky="w")
        ttk.Entry(frm_opts, textvariable=self.var_wr_maxM, width=10).grid(row=1, column=5, sticky="w")

        # Row 2
        ttk.Label(frm_opts, text="Crossing dirs:").grid(row=2, column=0, sticky="w")
        ttk.Entry(frm_opts, textvariable=self.var_cr_dirs, width=10).grid(row=2, column=1, sticky="w")
        ttk.Label(frm_opts, text="Crossing max points:").grid(row=2, column=2, sticky="w")
        ttk.Entry(frm_opts, textvariable=self.var_cr_maxM, width=10).grid(row=2, column=3, sticky="w")
        ttk.Label(frm_opts, text="Wr tolerance:").grid(row=2, column=4, sticky="w")
        ttk.Entry(frm_opts, textvariable=self.var_wr_tol, width=10).grid(row=2, column=5, sticky="w")

        ttk.Checkbutton(frm_opts, text="Plot preview", variable=self.var_plot_preview).grid(row=3, column=0, sticky="w")
        ttk.Checkbutton(frm_opts, text="Clean columns (drop all-NaN & constants)", variable=self.var_clean_cols).grid(row=3, column=1, columnspan=3, sticky="w")

        for j in range(6):
            frm_opts.columnconfigure(j, weight=1 if j%2==1 else 0)

        # Actions frame
        frm_actions = ttk.LabelFrame(self, text="Actions")
        frm_actions.pack(fill="x", **pad)
        ttk.Button(frm_actions, text="Emit Meta Skeleton", command=self.on_emit_meta).grid(row=0, column=0, padx=4, pady=6, sticky="w")
        ttk.Button(frm_actions, text="Scan for Files", command=self.on_scan).grid(row=0, column=1, padx=4, pady=6, sticky="w")
        # Keep button in case; but instant preview also bound to selection
        ttk.Button(frm_actions, text="Preview Selected", command=self.on_preview_selected).grid(row=0, column=2, padx=4, pady=6, sticky="w")
        ttk.Button(frm_actions, text="Run Batch", command=self.on_run).grid(row=0, column=3, padx=4, pady=6, sticky="w")
        ttk.Button(frm_actions, text="Show Results Window", command=self.on_show_results).grid(row=0, column=4, padx=4, pady=6, sticky="w")

        self.progress = ttk.Progressbar(frm_actions, mode="indeterminate")
        self.progress.grid(row=0, column=5, padx=8, pady=6, sticky="we")
        frm_actions.columnconfigure(5, weight=1)

        # Split pane: left file list, right preview/log
        paned = ttk.Panedwindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, **pad)

        # Left: file list with status
        frm_left = ttk.LabelFrame(paned, text="Discovered files")
        self.tree = ttk.Treeview(frm_left, columns=("ext","knot_id","relpath","status"), show="headings", height=20)
        for col, text, w in (("ext","ext",60), ("knot_id","knot_id",120), ("relpath","relative path",640), ("status","status",160)):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="w")
        vsb = ttk.Scrollbar(frm_left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.tag_configure("status_err", foreground="red")
        self.tree.tag_configure("status_warn", foreground="orange")
        self.tree.tag_configure("status_ok", foreground="gray20")
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        paned.add(frm_left, weight=2)

        # Instant preview on selection
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # Right: preview (plot) + log
        frm_right = ttk.LabelFrame(paned, text="Preview & Log")
        self.fig = Figure(figsize=(5,4), dpi=100)
        self.ax3d = self.fig.add_subplot(111, projection="3d")
        self.ax3d.set_xlabel("X"); self.ax3d.set_ylabel("Y"); self.ax3d.set_zlabel("Z")
        self.canvas = FigureCanvasTkAgg(self.fig, master=frm_right)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # Log under the plot
        self.txt = tk.Text(frm_right, height=10)
        self.txt.pack(fill="x", expand=False)

        paned.add(frm_right, weight=3)

        # Footer
        footer = ttk.Frame(self)
        footer.pack(fill="x", **pad)
        ttk.Label(footer, text=f"K_fluid={K_fluid:.6e} kg/m,  K_energy={K_energy:.6e} kg/m").pack(side="left")

        # Apply initial quality
        self.apply_quality_profile(self.var_quality.get())

    # ---- UI helpers & events ----
    def _on_root_change(self, *_):
        # Debounced auto-scan when root path changes
        if self._scan_after_id is not None:
            try:
                self.after_cancel(self._scan_after_id)
            except Exception:
                pass
            self._scan_after_id = None
        self._scan_after_id = self.after(600, self.on_scan)

    def browse_root(self):
        d = filedialog.askdirectory(title="Select knot root folder", initialdir=self.var_root.get())
        if d:
            self.var_root.set(d)  # triggers auto-scan

    def browse_out(self):
        p = filedialog.asksaveasfilename(title="Save results CSV as", defaultextension=".csv",
                                         filetypes=[("CSV","*.csv"), ("All files","*.*")],
                                         initialdir=self.var_root.get())
        if p:
            self.var_out.set(p)

    def browse_meta(self):
        p = filedialog.askopenfilename(title="Select meta CSV",
                                       filetypes=[("CSV","*.csv"), ("All files","*.*")],
                                       initialdir=self.var_root.get())
        if p:
            self.var_meta.set(p)

    def browse_emit_meta(self):
        p = filedialog.asksaveasfilename(title="Save meta skeleton as", defaultextension=".csv",
                                         filetypes=[("CSV","*.csv"), ("All files","*.*")],
                                         initialdir=self.var_root.get())
        if p:
            self.var_emit_meta.set(p)

    def log(self, msg):
        self.txt.insert("end", msg + "\n")
        self.txt.see("end")
        self.update_idletasks()

    def set_busy(self, busy=True):
        if busy:
            self.progress.start(80)
        else:
            self.progress.stop()

    def on_quality_change(self, _evt=None):
        self.apply_quality_profile(self.var_quality.get())

    def apply_quality_profile(self, name):
        prof = QUALITY_PROFILES.get(name, QUALITY_PROFILES["Balanced"])
        self.var_samples.set(prof["samples"])
        self.var_wr_maxM.set(prof["wr_maxM"])
        self.var_cr_dirs.set(prof["cr_dirs"])
        self.var_cr_maxM.set(prof["cr_maxM"])
        self.log(f"Quality → {name}: samples={prof['samples']}, wr_maxM={prof['wr_maxM']}, cr_dirs={prof['cr_dirs']}, cr_maxM={prof['cr_maxM']}")

    # ---- Actions ----
    def on_emit_meta(self):
        try:
            root = self.var_root.get().strip()
            emit_path = self.var_emit_meta.get().strip()
            if not root:
                messagebox.showwarning("Missing", "Please select a knot root folder.")
                return
            if not emit_path:
                messagebox.showwarning("Missing", "Please choose where to save the meta skeleton.")
                return
            self.set_busy(True)
            self.log("Scanning for *.fseries / *.short...")
            files = sorted(glob.glob(os.path.join(root, "**", "*.fseries"), recursive=True))
            files += sorted(glob.glob(os.path.join(root, "**", "*.short"), recursive=True))
            if not files:
                self.log("No .fseries or .short files found.")
                messagebox.showinfo("Done", "No .fseries or .short files found.")
                return
            ids = []
            seen = set()
            for p in files:
                kid = parse_knot_id_from_filename(p)
                if kid not in seen:
                    seen.add(kid); ids.append(kid)
            with open(emit_path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["knot_id","chiral","sigma","type","hyperbolic_volume"])
                for kid in ids:
                    w.writerow([kid, "", "", "", ""])
            self.log(f"Wrote meta skeleton: {emit_path}  (ids: {len(ids)})")
            messagebox.showinfo("Done", f"Meta skeleton written:\n{emit_path}\nIDs: {len(ids)}")
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed: {e}")
        finally:
            self.set_busy(False)

    def on_scan(self):
        try:
            root = self.var_root.get().strip()
            if not root:
                messagebox.showwarning("Missing", "Please select a knot root folder.")
                return
            self.set_busy(True)
            self.log("Scanning recursively for *.fseries / *.short / *.stl ...")
            files = []
            files += sorted(glob.glob(os.path.join(root, "**", "*.fseries"), recursive=True))
            files += sorted(glob.glob(os.path.join(root, "**", "*.short"), recursive=True))
            files += sorted(glob.glob(os.path.join(root, "**", "*.stl"), recursive=True))
            self.tree.delete(*self.tree.get_children())
            root_abs = os.path.abspath(root)
            for p in files:
                rel = os.path.relpath(p, root_abs)
                kid = parse_knot_id_from_filename(p)
                ext = os.path.splitext(p)[1].lower()
                status = quick_status(p)
                tag = "status_ok"
                if status.startswith("error") or status in ("empty_fseries","insufficient_points","nonfinite_points"):
                    tag = "status_err"
                elif status in ("stl_no_sibling_curve","all_zero_coeffs"):
                    tag = "status_warn"
                self.tree.insert("", "end", values=(ext, kid, rel, status), tags=(tag,))
            self.log(f"Discovered files: {len(files)} (problematic rows are colored)")
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"Scan failed:\n{e}")
        finally:
            self.set_busy(False)

    def _on_tree_select(self, _evt=None):
        # Instant preview when a row is selected
        self.on_preview_selected()

    def on_preview_selected(self):
        try:
            sel = self.tree.selection()
            if not sel:
                return
            item = self.tree.item(sel[0])
            ext, kid, rel, status = item["values"]
            root = self.var_root.get().strip()
            path = os.path.join(root, rel)
            prof = QUALITY_PROFILES.get(self.var_quality.get(), QUALITY_PROFILES["Balanced"])
            self.set_busy(True)
            self.log(f"Previewing: {rel}  [status={status}]")

            self.ax3d.clear()
            self.ax3d.set_xlabel("X"); self.ax3d.set_ylabel("Y"); self.ax3d.set_zlabel("Z")

            if ext == ".stl":
                tris = load_stl(path)
                for tri in tris[:2000]:
                    X = [tri[0][0], tri[1][0], tri[2][0], tri[0][0]]
                    Y = [tri[0][1], tri[1][1], tri[2][1], tri[0][1]]
                    Z = [tri[0][2], tri[1][2], tri[2][2], tri[0][2]]
                    self.ax3d.plot(X, Y, Z, linewidth=0.5)
                base = os.path.splitext(path)[0]
                sib = None
                for cand_ext in (".short", ".fseries"):
                    cand = base + cand_ext
                    if os.path.exists(cand):
                        sib = cand; break
                if sib:
                    d = quick_preview_any(sib, prof, b0=float(self.var_b0.get()), wr_tol=float(self.var_wr_tol.get()))
                    self.log("---- Preview (from sibling curve) ----")
                    for k in ["closure_error","length_series_units","writhe","crossing_est","sigma_from_writhe"]:
                        if k in d:
                            self.log(f"{k}: {d[k]}")
                else:
                    self.log("No sibling .short/.fseries found for invariants.")
            else:
                d = quick_preview_any(path, prof, b0=float(self.var_b0.get()), wr_tol=float(self.var_wr_tol.get()))
                if self.var_plot_preview.get() and "r" in d:
                    r = d["r"]
                    self.ax3d.plot(r[:,0], r[:,1], r[:,2], linewidth=1.0)
                self.log("---- Preview ----")
                for k in ["closure_error","length_series_units","writhe","crossing_est","sigma_from_writhe","Hvortex_X_est(b0={:.0f})".format(float(self.var_b0.get()))]:
                    if k in d:
                        self.log(f"{k}: {d[k]}")

            self.canvas.draw()
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"Preview failed:\n{e}")
        finally:
            self.set_busy(False)

    def on_run(self):
        threading.Thread(target=self._run_batch_thread, daemon=True).start()

    def _run_batch_thread(self):
        try:
            root = self.var_root.get().strip()
            out_csv = self.var_out.get().strip()
            meta_csv = self.var_meta.get().strip()
            emit_meta = self.var_emit_meta.get().strip()

            if not root:
                messagebox.showwarning("Missing", "Please select a knot root folder.")
                return
            if not out_csv:
                messagebox.showwarning("Missing", "Please choose an output CSV path.")
                return

            kwargs = dict(
                root_dir=root,
                out_csv=out_csv,
                scale=float(self.var_scale.get()),
                xi=float(self.var_xi.get()),
                b0=float(self.var_b0.get()),
                samples=int(self.var_samples.get()),
                wr_maxM=int(self.var_wr_maxM.get()),
                cr_dirs=int(self.var_cr_dirs.get()),
                cr_maxM=int(self.var_cr_maxM.get()),
                sigma_mode=self.var_sigma_mode.get(),
                meta_csv=meta_csv,
                wr_tol=float(self.var_wr_tol.get()),
                emit_meta_path=emit_meta
            )

            self.set_busy(True)
            self.log("Starting batch...")
            for k,v in kwargs.items():
                self.log(f"  {k} = {v}")
            df = run_batch(**kwargs)

            # Clean columns if requested
            if self.var_clean_cols.get():
                df = clean_dataframe(df)

            # Save and show
            df.to_csv(out_csv, index=False)
            self.last_df = df
            self.log(f"Processed rows: {len(df)}")
            self.log(f"Wrote results: {out_csv}")
            messagebox.showinfo("Done", f"Processed rows: {len(df)}\nSaved: {out_csv}")
            self.show_results_window(df)
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"Batch failed:\n{e}")
        finally:
            self.set_busy(False)

    def on_show_results(self):
        if self.last_df is None:
            out_csv = self.var_out.get().strip()
            if os.path.exists(out_csv):
                try:
                    df = pd.read_csv(out_csv)
                    self.last_df = df
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load results CSV:\n{e}")
                    return
            else:
                messagebox.showinfo("Results", "No results to show yet.")
                return
        self.show_results_window(self.last_df)

    def show_results_window(self, df: pd.DataFrame):
        top = tk.Toplevel(self)
        top.title("Batch Results")
        top.geometry("1200x600")

        # Toolbar
        bar = ttk.Frame(top)
        bar.pack(fill="x")
        ttk.Button(bar, text="Save As…", command=lambda: self.save_df_as(df)).pack(side="left", padx=4, pady=4)
        ttk.Button(bar, text="Close", command=top.destroy).pack(side="right", padx=4, pady=4)

        # Table
        cols = list(df.columns)
        tree = ttk.Treeview(top, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=140, anchor="w")
        vsb = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(top, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        max_rows = 5000
        data = df.head(max_rows).itertuples(index=False, name=None)
        for row in data:
            tree.insert("", "end", values=row)

        if len(df) > max_rows:
            note = ttk.Label(top, text=f"Showing first {max_rows} rows of {len(df)} (open the CSV for full data).")
            note.pack(side="bottom", anchor="w", padx=6, pady=4)

    def save_df_as(self, df: pd.DataFrame):
        p = filedialog.asksaveasfilename(title="Save results as", defaultextension=".csv",
                                         filetypes=[("CSV","*.csv"), ("All files","*.*")],
                                         initialdir=self.var_root.get())
        if p:
            try:
                df.to_csv(p, index=False)
                messagebox.showinfo("Saved", f"Results saved:\n{p}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{e}")

def discover_ids(files):
    ids = []
    seen = set()
    for f in files:
        kid = parse_knot_id_from_filename(f)
        if kid not in seen:
            seen.add(kid); ids.append(kid)
    return ids

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()