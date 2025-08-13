#!/usr/bin/env python3
# VAM Knot Workbench — Modular GUI for .fseries / .short / .stl
# - Left pane: recursive file browser + status
# - Right pane: dashboards (plugins) in a Notebook
#   * Batch/Results: compute invariants & VAM quantities (CSV)
#   * Spectrum: harmonic magnitudes & energy fraction
#   * Geometry: curvature / torsion stats
#
# Requirements: numpy, pandas, matplotlib, tkinter
#
# Extend by adding a new class inheriting DashboardPlugin and registering it in PLUGINS.

import os, sys, math, glob, csv, struct, traceback, threading
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------- VAM constants -----------------
C_e = 1_093_845.63
r_c = 1.40897017e-15
rho_fluid = 7.0e-7
rho_energy = 3.49924562e35
c = 299_792_458.0
alpha = 1/137.035999084
phi = (1+5**0.5)/2
VOL_BASELINE_VALUE = 2.029883212819307

E_density_fluid = 0.5 * rho_fluid * C_e**2
tube_area = math.pi * r_c**2
K_fluid = (4/(alpha*phi)) * (E_density_fluid / c**2) * tube_area
K_energy = (4/(alpha*phi)) * (rho_energy / c**2) * tube_area

# ----------------- Utility functions -----------------
def load_matrix_fseries(path):
    rows = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for ln in f:
            ln = ln.strip()
            if not ln: continue
            parts = ln.replace(",", " ").split()
            vals = []
            for x in parts[:6]:
                try: vals.append(float(x))
                except: vals.append(0.0)
            while len(vals) < 6: vals.append(0.0)
            rows.append(vals)
    if not rows: return np.zeros((0,6), dtype=float)
    arr = np.asarray(rows, dtype=float)
    arr[~np.isfinite(arr)] = 0.0
    return arr

def eval_series_derivs(coeffs, t, order=3):
    # Return r, r1, r2, r3 (up to 'order' where order in {1,2,3})
    if coeffs.size == 0:
        Z = np.zeros((t.size,3))
        return (Z,)* (order+1)
    N = coeffs.shape[0]
    n = np.arange(N).reshape(-1,1)
    nt = n * t.reshape(1,-1)
    cos_nt = np.cos(nt); sin_nt = np.sin(nt)
    Ax, Bx, Ay, By, Az, Bz = [coeffs[:,i].reshape(-1,1) for i in range(6)]
    # r
    x = (Ax*cos_nt + Bx*sin_nt).sum(axis=0)
    y = (Ay*cos_nt + By*sin_nt).sum(axis=0)
    z = (Az*cos_nt + Bz*sin_nt).sum(axis=0)
    r = np.stack([x,y,z], axis=1)
    # r'
    x1 = ((-n*Ax)*sin_nt + (n*Bx)*cos_nt).sum(axis=0)
    y1 = ((-n*Ay)*sin_nt + (n*By)*cos_nt).sum(axis=0)
    z1 = ((-n*Az)*sin_nt + (n*Bz)*cos_nt).sum(axis=0)
    r1 = np.stack([x1,y1,z1], axis=1)
    if order == 1: return r, r1
    # r''
    x2 = ((-n*n*Ax)*cos_nt + (-n*n*Bx)*sin_nt).sum(axis=0)
    y2 = ((-n*n*Ay)*cos_nt + (-n*n*By)*sin_nt).sum(axis=0)
    z2 = ((-n*n*Az)*cos_nt + (-n*n*Bz)*sin_nt).sum(axis=0)
    r2 = np.stack([x2,y2,z2], axis=1)
    if order == 2: return r, r1, r2
    # r'''
    x3 = ((n*n*n*Ax)*sin_nt + (-n*n*n*Bx)*cos_nt).sum(axis=0)
    y3 = ((n*n*n*Ay)*sin_nt + (-n*n*n*By)*cos_nt).sum(axis=0)
    z3 = ((n*n*n*Az)*sin_nt + (-n*n*n*Bz)*cos_nt).sum(axis=0)
    r3 = np.stack([x3,y3,z3], axis=1)
    return r, r1, r2, r3

def resample_closed_polyline(points, M):
    P = np.asarray(points, dtype=float)
    if P.shape[0] < 3: raise ValueError("Need at least 3 points in .short")
    if np.linalg.norm(P[0]-P[-1]) > 1e-12: P = np.vstack([P, P[0]])
    seg = P[1:] - P[:-1]
    seglen = np.linalg.norm(seg, axis=1)
    s = np.concatenate([[0.0], np.cumsum(seglen)])
    L = s[-1]
    if L <= 0: raise ValueError("Zero length polyline")
    u = np.linspace(0, L, M+1)[:-1]
    r = np.empty((u.size,3), dtype=float)
    j = 0
    for i,ui in enumerate(u):
        while j+1 < s.size and ui > s[j+1]: j += 1
        if j >= seg.shape[0]: j = seg.shape[0]-1
        t = (ui - s[j]) / (seglen[j] if seglen[j] > 0 else 1.0)
        r[i] = P[j] + t * seg[j]
    return r

def derivatives_from_uniform_samples(r):
    M = r.shape[0]
    dt = 2*math.pi / M
    rp = np.roll(r,-1,axis=0); rm = np.roll(r,1,axis=0)
    r_t = (rp - rm) / (2*dt)
    return r_t, dt

def writhe_gauss(r, r_t, dt, maxM=500):
    M = r.shape[0]
    if M > maxM:
        idx = np.linspace(0, M-1, maxM, dtype=int)
        r = r[idx]; r_t = r_t[idx]
        M = maxM; dt = 2*math.pi / M
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
    M = r.shape[0]
    if M > maxM:
        idx = np.linspace(0, M-1, maxM, dtype=int)
        r = r[idx]; M = maxM
    P = r; Q = np.roll(r, -1, axis=0)
    min_cross = None
    for d in random_unit_vectors(directions, seed=seed):
        w = d / (np.linalg.norm(d) + 1e-12)
        tmp = np.array([1.0,0.0,0.0])
        if abs(np.dot(tmp,w)) > 0.9: tmp = np.array([0.0,1.0,0.0])
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
                if j == (i-1) % M: continue
                q1, q2 = P2[j], Q2[j]
                if (pmaxx < min(q1[0], q2[0]) or max(q1[0], q2[0]) < pminx or
                        pmaxy < min(q1[1], q2[1]) or max(q1[1], q2[1]) < pminy):
                    continue
                def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
                o1 = orient(p1,p2,q1); o2 = orient(p1,p2,q2)
                o3 = orient(q1,q2,p1); o4 = orient(q1,q2,p2)
                if (o1==0 and o2==0 and o3==0 and o4==0): continue
                if (o1*o2<0) and (o3*o4<0): count += 1
        if (min_cross is None) or (count < min_cross): min_cross = count
    return int(min_cross if min_cross is not None else 0)

def parse_knot_id_from_filename(fname):
    base = os.path.basename(fname); name = os.path.splitext(base)[0]
    parts = name.split(".")
    for p in parts[::-1]:
        if "_" in p: return p
    return name

def load_stl(path, max_tris=200000):
    with open(path, "rb") as f:
        head = f.read(80); rest = f.read()
    if len(rest) >= 4:
        try:
            num_tris = struct.unpack("<I", rest[:4])[0]
            expected = 4 + num_tris*50
            if len(rest) >= expected:
                tris = []; off = 4; n = min(num_tris, max_tris)
                for _ in range(n):
                    chunk = rest[off:off+50]
                    if len(chunk) < 50: break
                    data = struct.unpack("<12fH", chunk)
                    v1 = data[3:6]; v2 = data[6:9]; v3 = data[9:12]
                    tris.append([v1, v2, v3]); off += 50
                return np.array(tris, dtype=float)
        except: pass
    try:
        text = (head + rest).decode("utf-8", errors="ignore")
    except: text = ""
    verts = []
    for line in text.splitlines():
        line = line.strip().lower()
        if line.startswith("vertex"):
            parts = line.split()
            if len(parts) >= 4:
                try: verts.append((float(parts[1]), float(parts[2]), float(parts[3])))
                except: pass
    tris = []
    for i in range(0, len(verts), 3): tris.append(verts[i:i+3])
    if tris: return np.array(tris, dtype=float)
    raise ValueError("Failed to parse STL")

def quick_status(path):
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".fseries":
            coeffs = load_matrix_fseries(path)
            if coeffs.size == 0: return "empty_fseries"
            if not np.any(np.abs(coeffs) > 0): return "all_zero_coeffs"
            return "ok"
        elif ext == ".short":
            pts = []
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln: continue
                    parts = ln.replace(",", " ").split()
                    if len(parts) >= 3:
                        try:
                            x,y,z = float(parts[0]), float(parts[1]), float(parts[2])
                            pts.append((x,y,z))
                        except: pass
            if len(pts) < 3: return "insufficient_points"
            P = np.asarray(pts, dtype=float)
            if not np.all(np.isfinite(P)): return "nonfinite_points"
            return "ok"
        elif ext == ".stl":
            base = os.path.splitext(path)[0]
            sib = None
            for cand_ext in (".short",".fseries"):
                cand = base + cand_ext
                if os.path.exists(cand): sib = cand; break
            return "stl_curve_ok" if sib else "stl_no_sibling_curve"
        else:
            return "ignored"
    except Exception as e:
        return f"error:{type(e).__name__}"

# ----------------- Plugin system -----------------
class DashboardPlugin:
    name = "Unnamed"
    def __init__(self, app): self.app = app
    def build(self, parent): pass
    def on_file_selected(self, path, ext): pass
    def on_scan_completed(self, files): pass

# ----------------- Main App -----------------
QUALITY_PROFILES = {
    "Ultra Fast": dict(samples=600,  wr_maxM=240, cr_dirs=10, cr_maxM=160),
    "Fast":       dict(samples=900,  wr_maxM=360, cr_dirs=14, cr_maxM=200),
    "Balanced":   dict(samples=1500, wr_maxM=520, cr_dirs=28, cr_maxM=260),
    "High Quality": dict(samples=2400, wr_maxM=700, cr_dirs=48, cr_maxM=360),
}

class Workbench(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VAM Knot Workbench")
        self.geometry("1380x900")
        self.resizable(True, True)

        default_root = os.path.join(os.getcwd(), "knots")
        default_out  = os.path.join(default_root, "fseries_batch_results.csv")
        default_meta = os.path.join(default_root, "knot_meta.csv")

        self.var_root = tk.StringVar(value=default_root)
        self.var_out = tk.StringVar(value=default_out)
        self.var_meta = tk.StringVar(value=default_meta)
        self.var_quality = tk.StringVar(value="Balanced")
        self.var_plot_preview = tk.BooleanVar(value=True)

        self.var_scale = tk.DoubleVar(value=1.0)
        self.var_xi = tk.DoubleVar(value=1.0)
        self.var_b0 = tk.DoubleVar(value=3.0)
        self.var_wr_tol = tk.DoubleVar(value=5e-3)

        self._scan_after_id = None

        self._build_ui()
        self._install_plugins()

        self.var_root.trace_add("write", self._on_root_change)
        self.after(200, self.scan_files)

    # --- UI skeleton ---
    def _build_ui(self):
        pad = {'padx': 6, 'pady': 4}
        top = ttk.Frame(self); top.pack(fill="x", **pad)
        ttk.Label(top, text="Root:").pack(side="left")
        ttk.Entry(top, textvariable=self.var_root, width=70).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(top, text="Browse…", command=self.browse_root).pack(side="left", padx=4)
        ttk.Label(top, text="Quality:").pack(side="left", padx=(16,4))
        cmb = ttk.Combobox(top, textvariable=self.var_quality, state="readonly",
                           values=list(QUALITY_PROFILES.keys()), width=16)
        cmb.pack(side="left")
        ttk.Checkbutton(top, text="Plot preview", variable=self.var_plot_preview).pack(side="left", padx=8)

        paned = ttk.Panedwindow(self, orient="horizontal"); paned.pack(fill="both", expand=True, **pad)
        # Left: file list
        left = ttk.LabelFrame(paned, text="Files")
        self.tree = ttk.Treeview(left, columns=("ext","knot_id","relpath","status"), show="headings")
        for col, text, w in (("ext","ext",60), ("knot_id","knot_id",120), ("relpath","relative path",640), ("status","status",160)):
            self.tree.heading(col, text=text); self.tree.column(col, width=w, anchor="w")
        vsb = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.tag_configure("status_err", foreground="red")
        self.tree.tag_configure("status_warn", foreground="orange")
        self.tree.tag_configure("status_ok", foreground="gray20")
        self.tree.pack(side="left", fill="both", expand=True); vsb.pack(side="right", fill="y")
        paned.add(left, weight=2)

        # Right: preview + notebook
        right = ttk.Frame(paned)
        # Preview figure
        self.fig = Figure(figsize=(5,4), dpi=100); self.ax3d = self.fig.add_subplot(111, projection="3d")
        self.ax3d.set_xlabel("X"); self.ax3d.set_ylabel("Y"); self.ax3d.set_zlabel("Z")
        self.canvas = FigureCanvasTkAgg(self.fig, master=right); self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Notebook
        self.nb = ttk.Notebook(right); self.nb.pack(fill="both", expand=True, pady=(6,0))

        paned.add(right, weight=3)

        # Events
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # Footer status
        self.status = ttk.Label(self, text=f"K_fluid={K_fluid:.6e} kg/m, K_energy={K_energy:.6e} kg/m")
        self.status.pack(fill="x", **pad)

    def browse_root(self):
        d = filedialog.askdirectory(title="Select knot root folder", initialdir=self.var_root.get())
        if d: self.var_root.set(d)

    def _on_root_change(self, *_):
        if self._scan_after_id is not None:
            try: self.after_cancel(self._scan_after_id)
            except: pass
        self._scan_after_id = self.after(600, self.scan_files)

    # --- File scanning / selection ---
    def scan_files(self):
        root = self.var_root.get().strip()
        if not root: return
        files = []
        files += sorted(glob.glob(os.path.join(root, "**", "*.fseries"), recursive=True))
        files += sorted(glob.glob(os.path.join(root, "**", "*.short"), recursive=True))
        files += sorted(glob.glob(os.path.join(root, "**", "*.stl"), recursive=True))
        self.tree.delete(*self.tree.get_children())
        root_abs = os.path.abspath(root)
        for p in files:
            rel = os.path.relpath(p, root_abs); kid = parse_knot_id_from_filename(p)
            ext = os.path.splitext(p)[1].lower(); status = quick_status(p)
            tag = "status_ok"
            if status.startswith("error") or status in ("empty_fseries","insufficient_points","nonfinite_points"): tag = "status_err"
            elif status in ("stl_no_sibling_curve","all_zero_coeffs"): tag = "status_warn"
            self.tree.insert("", "end", values=(ext, kid, rel, status), tags=(tag,))
        for plugin in self.plugins: plugin.on_scan_completed(files)

    def _on_tree_select(self, _evt=None):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])
        ext, kid, rel, status = item["values"]
        path = os.path.join(self.var_root.get(), rel)
        # Preview
        self.preview_path(path, ext)
        # Notify plugins
        for plugin in self.plugins: plugin.on_file_selected(path, ext)

    def preview_path(self, path, ext):
        prof = QUALITY_PROFILES.get(self.var_quality.get(), QUALITY_PROFILES["Balanced"])
        self.ax3d.clear(); self.ax3d.set_xlabel("X"); self.ax3d.set_ylabel("Y"); self.ax3d.set_zlabel("Z")
        try:
            if ext == ".stl":
                tris = load_stl(path)
                for tri in tris[:2000]:
                    X = [tri[0][0], tri[1][0], tri[2][0], tri[0][0]]
                    Y = [tri[0][1], tri[1][1], tri[2][1], tri[0][1]]
                    Z = [tri[0][2], tri[1][2], tri[2][2], tri[0][2]]
                    self.ax3d.plot(X,Y,Z, linewidth=0.5)
            elif ext in (".fseries",".short"):
                if not self.var_plot_preview.get():
                    pass
                else:
                    if ext == ".fseries":
                        coeffs = load_matrix_fseries(path)
                        t = np.linspace(0, 2*math.pi, prof["samples"], endpoint=False)
                        r, r_t = eval_series_derivs(coeffs, t, order=1)
                    else:
                        pts = []
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:
                            for ln in f:
                                ln = ln.strip()
                                if not ln: continue
                                parts = ln.replace(",", " ").split()
                                if len(parts)>=3:
                                    try: pts.append([float(parts[0]), float(parts[1]), float(parts[2])])
                                    except: pass
                        r = resample_closed_polyline(pts, prof["samples"])
                    self.ax3d.plot(r[:,0], r[:,1], r[:,2], linewidth=1.0)
        except Exception as e:
            print("Preview error:", e)
        self.canvas.draw()

    # --- Plugins ---
    def _install_plugins(self):
        self.plugins = []
        for P in PLUGINS:
            frame = ttk.Frame(self.nb)
            self.nb.add(frame, text=P.name)
            plugin = P(self)
            plugin.build(frame)
            self.plugins.append(plugin)

# ----------------- Plugins -----------------
class DashboardPlugin:
    name = "Unnamed"
    def __init__(self, app): self.app = app
    def build(self, parent): pass
    def on_file_selected(self, path, ext): pass
    def on_scan_completed(self, files): pass

class BatchResultsPlugin(DashboardPlugin):
    name = "Batch / Results"
    KEY_COLS = [
        "file","knot_id","harmonics_N","closure_error","length_series_units",
        "scale_m_per_unit","length_m","writhe","crossing_est","sigma","sigma_source",
        "Hvortex_X(b0={b0})","hyperbolic_volume_meta","Hvortex_Vol(Vol/Vol(4_1))",
        "xi","K_fluid_kg_per_m","K_energy_kg_per_m","mass_fluid_kg","mass_energy_kg",
        "type_meta","chiral_meta","looks_meta"
    ]

    def build(self, parent):
        self.parent = parent
        pad = {'padx': 6, 'pady': 4}
        row = ttk.Frame(parent); row.pack(fill="x", **pad)
        self.scale = tk.DoubleVar(value=self.app.var_scale.get())
        self.xi    = tk.DoubleVar(value=self.app.var_xi.get())
        self.b0    = tk.DoubleVar(value=self.app.var_b0.get())
        self.wr_tol= tk.DoubleVar(value=self.app.var_wr_tol.get())
        ttk.Label(row, text="Scale m/unit").pack(side="left"); ttk.Entry(row, textvariable=self.scale, width=10).pack(side="left")
        ttk.Label(row, text="ξ").pack(side="left", padx=(8,2)); ttk.Entry(row, textvariable=self.xi, width=8).pack(side="left")
        ttk.Label(row, text="b₀").pack(side="left", padx=(8,2)); ttk.Entry(row, textvariable=self.b0, width=8).pack(side="left")
        ttk.Label(row, text="Wr tol").pack(side="left", padx=(8,2)); ttk.Entry(row, textvariable=self.wr_tol, width=8).pack(side="left")
        ttk.Button(row, text="Run Batch", command=self.run_batch).pack(side="left", padx=10)
        ttk.Button(row, text="Show Results", command=self.show_results).pack(side="left")
        self.table_frame = ttk.Frame(parent); self.table_frame.pack(fill="both", expand=True, **pad)
        self.df = None

    def on_scan_completed(self, files): pass
    def on_file_selected(self, path, ext): pass

    def run_batch(self):
        threading.Thread(target=self._run_batch_thread, daemon=True).start()

    def _run_batch_thread(self):
        try:
            df = self._compute_batch()
            b0_key = f"Hvortex_X(b0={int(self.b0.get())})"
            key_cols = [c if c!="Hvortex_X(b0={b0})" else b0_key for c in self.KEY_COLS]
            df = self._clean_dataframe(df, key_cols)
            out_csv = self.app.var_out.get().strip()
            df.to_csv(out_csv, index=False)
            self.df = df
            messagebox.showinfo("Batch", f"Processed rows: {len(df)}\nSaved: {out_csv}")
            self._show_table(df, key_cols)
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Batch failed", str(e))

    def _compute_batch(self):
        root = self.app.var_root.get().strip()
        meta_csv = self.app.var_meta.get().strip()
        prof = QUALITY_PROFILES.get(self.app.var_quality.get(), QUALITY_PROFILES["Balanced"])
        samples = prof["samples"]
        wr_maxM = prof["wr_maxM"]; cr_dirs = prof["cr_dirs"]; cr_maxM = prof["cr_maxM"]

        files = []
        files += sorted(glob.glob(os.path.join(root, "**", "*.fseries"), recursive=True))
        files += sorted(glob.glob(os.path.join(root, "**", "*.short"), recursive=True))
        if not files: raise RuntimeError("No .fseries or .short files found")

        meta = None
        if meta_csv and os.path.exists(meta_csv):
            meta_raw = pd.read_csv(meta_csv)
            mc = {c.lower():c for c in meta_raw.columns}
            def col(name): return meta_raw[mc[name.lower()]] if name.lower() in mc else None
            std = pd.DataFrame()
            std["knot_id"] = col("knot_id").astype(str) if col("knot_id") is not None else ""
            std["chiral"]  = col("chiral").astype(str).str.lower() if col("chiral") is not None else ""
            std["sigma"]   = col("sigma") if col("sigma") is not None else np.nan
            std["type"]    = col("type")  if col("type")  is not None else ""
            std["hyperbolic_volume"] = col("hyperbolic_volume") if col("hyperbolic_volume") is not None else np.nan
            std["looks"]   = col("looks") if col("looks") is not None else ""
            meta = std.set_index("knot_id")

        rows = []
        for path in files:
            ext = os.path.splitext(path)[1].lower()
            knot_id = parse_knot_id_from_filename(path)
            harmonics_N = np.nan
            if ext == ".fseries":
                coeffs = load_matrix_fseries(path); harmonics_N = int(coeffs.shape[0])
                t = np.linspace(0, 2*math.pi, samples, endpoint=False)
                r, r_t = eval_series_derivs(coeffs, t, order=1)
                dt = 2*math.pi / samples
            elif ext == ".short":
                pts = []
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for ln in f:
                        ln = ln.strip()
                        if not ln: continue
                        parts = ln.replace(",", " ").split()
                        if len(parts)>=3:
                            try: pts.append([float(parts[0]), float(parts[1]), float(parts[2])])
                            except: pass
                if len(pts) < 3: continue
                r = resample_closed_polyline(pts, samples)
                r_t, dt = derivatives_from_uniform_samples(r)
            else:
                continue

            closure = float(np.linalg.norm(r[0]-r[-1]))
            L_series = float(np.sum(np.linalg.norm(np.roll(r, -1, axis=0)-r, axis=1)))
            Wr = writhe_gauss(r, r_t, dt, maxM=wr_maxM)
            cr_est = estimate_crossing_number(r, directions=cr_dirs, maxM=cr_maxM)

            sigma_meta = np.nan; chiral_meta = ""; vol_meta = np.nan; type_meta = ""; looks_meta = ""
            if meta is not None and knot_id in meta.index:
                rowm = meta.loc[knot_id]
                chiral_meta = str(rowm.get("chiral",""))
                type_meta = str(rowm.get("type",""))
                looks_meta = str(rowm.get("looks",""))
                try: sigma_meta = float(rowm.get("sigma", np.nan))
                except: sigma_meta = np.nan
                try: vol_meta = float(rowm.get("hyperbolic_volume", np.nan))
                except: vol_meta = np.nan

            wr_tol = self.app.var_wr_tol.get()
            if np.isnan(sigma_meta):
                sigma = 0.0 if abs(Wr) <= wr_tol else (1.0 if Wr>0 else -1.0)
                sigma_source = "writhe_fallback"
            else:
                try: sigma = float(sigma_meta); sigma_source = "meta"
                except: sigma = 0.0 if abs(Wr) <= wr_tol else (1.0 if Wr>0 else -1.0); sigma_source = "writhe_fallback"

            b0 = self.b0.get()
            HvX = sigma * max(cr_est - b0, 0.0)
            HvVol = np.nan
            if not np.isnan(vol_meta) and sigma != 0.0:
                HvVol = sigma * (vol_meta / VOL_BASELINE_VALUE)

            L_phys = self.scale.get() * L_series
            H_used = HvX if np.isnan(HvVol) else HvVol
            M_fluid = self.xi.get() * H_used * K_fluid * L_phys
            M_energy = self.xi.get() * H_used * K_energy * L_phys

            rows.append({
                "file": os.path.basename(path),
                "knot_id": knot_id,
                "harmonics_N": harmonics_N,
                "closure_error": closure,
                "length_series_units": L_series,
                "scale_m_per_unit": self.scale.get(),
                "length_m": L_phys,
                "writhe": Wr,
                "crossing_est": int(cr_est),
                "sigma": sigma,
                "sigma_source": sigma_source,
                f"Hvortex_X(b0={int(b0)})": HvX,
                "hyperbolic_volume_meta": vol_meta,
                "Hvortex_Vol(Vol/Vol(4_1))": HvVol,
                "xi": self.xi.get(),
                "K_fluid_kg_per_m": K_fluid,
                "K_energy_kg_per_m": K_energy,
                "mass_fluid_kg": M_fluid,
                "mass_energy_kg": M_energy,
                "type_meta": type_meta,
                "chiral_meta": chiral_meta,
                "looks_meta": looks_meta
            })
        return pd.DataFrame(rows)

    def _clean_dataframe(self, df, key_cols):
        df2 = df.copy()
        drop_all_nan = [c for c in df2.columns if c not in key_cols and df2[c].isna().all()]
        df2 = df2.drop(columns=drop_all_nan)
        const_cols = []
        for col in df2.columns:
            if col in key_cols: continue
            vals = df2[col].dropna().unique()
            if len(vals) <= 1: const_cols.append(col)
        if const_cols: df2 = df2.drop(columns=const_cols)
        return df2

    def _show_table(self, df, key_cols):
        for child in self.table_frame.winfo_children():
            child.destroy()
        cols = list(df.columns)
        tree = ttk.Treeview(self.table_frame, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c); tree.column(c, width=140, anchor="w")
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.pack(side="left", fill="both", expand=True); vsb.pack(side="right", fill="y"); hsb.pack(side="bottom", fill="x")
        for row in df.head(5000).itertuples(index=False, name=None):
            tree.insert("", "end", values=row)

    def show_results(self):
        if self.df is None:
            out_csv = self.app.var_out.get().strip()
            if os.path.exists(out_csv):
                try: self.df = pd.read_csv(out_csv)
                except Exception as e: return messagebox.showerror("Error", f"Failed to load: {e}")
            else:
                return messagebox.showinfo("Results", "No results to show yet.")
        b0_key = f"Hvortex_X(b0={int(self.b0.get())})"
        key_cols = [c if c!="Hvortex_X(b0={b0})" else b0_key for c in self.KEY_COLS]
        self._show_table(self.df, key_cols)

class SpectrumPlugin(DashboardPlugin):
    name = "Spectrum"
    def build(self, parent):
        self.parent = parent
        pad = {'padx': 6, 'pady': 4}
        self.info = ttk.Label(parent, text="Select a .fseries file to see harmonic magnitudes and energy.")
        self.info.pack(fill="x", **pad)
        self.fig = Figure(figsize=(5,3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def on_file_selected(self, path, ext):
        if ext != ".fseries":
            self.ax.clear(); self.ax.set_title("No .fseries selected"); self.canvas.draw(); return
        try:
            coeffs = load_matrix_fseries(path)
            if coeffs.size == 0:
                self.ax.clear(); self.ax.set_title("Empty .fseries"); self.canvas.draw(); return
            Ax, Bx, Ay, By, Az, Bz = [coeffs[:,i] for i in range(6)]
            mag = np.sqrt(Ax*Ax + Bx*Bx + Ay*Ay + By*By + Az*Az + Bz*Bz)
            energy = Ax*Ax + Bx*Bx + Ay*Ay + By*By + Az*Az + Bz*Bz
            cum = np.cumsum(energy) / (np.sum(energy) + 1e-18)
            idx95 = int(np.searchsorted(cum, 0.95)) + 1 if energy.size>0 else 0
            self.ax.clear()
            self.ax.bar(np.arange(len(mag)), mag)
            self.ax.set_xlabel("Harmonic n"); self.ax.set_ylabel("Magnitude")
            self.ax.set_title(f"Harmonic magnitudes (N={len(mag)}; N95≈{idx95})")
            self.canvas.draw()
        except Exception as e:
            self.ax.clear(); self.ax.set_title(f"Error: {e}"); self.canvas.draw()

class GeometryPlugin(DashboardPlugin):
    name = "Geometry"
    def build(self, parent):
        self.parent = parent
        pad = {'padx': 6, 'pady': 4}
        self.lbl = ttk.Label(parent, text="Select a curve (.fseries or .short) to compute curvature/torsion stats.")
        self.lbl.pack(fill="x", **pad)
        self.txt = tk.Text(parent, height=10); self.txt.pack(fill="x", expand=False, **pad)
        self.fig = Figure(figsize=(5,3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def on_file_selected(self, path, ext):
        try:
            prof = QUALITY_PROFILES.get(self.app.var_quality.get(), QUALITY_PROFILES["Balanced"])
            if ext == ".fseries":
                coeffs = load_matrix_fseries(path)
                if coeffs.size == 0: return
                t = np.linspace(0, 2*math.pi, prof["samples"], endpoint=False)
                r, r1, r2, r3 = eval_series_derivs(coeffs, t, order=3)
            elif ext == ".short":
                pts = []
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for ln in f:
                        ln = ln.strip()
                        if not ln: continue
                        parts = ln.replace(",", " ").split()
                        if len(parts)>=3:
                            try: pts.append([float(parts[0]), float(parts[1]), float(parts[2])])
                            except: pass
                if len(pts) < 3: return
                r = resample_closed_polyline(pts, prof["samples"])
                r1, dt = derivatives_from_uniform_samples(r)
                r2 = (np.roll(r1,-1,axis=0) - np.roll(r1,1,axis=0)) / (2*(2*math.pi/prof["samples"]))
                r3 = (np.roll(r2,-1,axis=0) - np.roll(r2,1,axis=0)) / (2*(2*math.pi/prof["samples"]))
            else:
                return
            cross12 = np.cross(r1, r2)
            v1 = np.linalg.norm(r1, axis=1)
            num_k = np.linalg.norm(cross12, axis=1)
            denom_k = (v1**3 + 1e-18)
            kappa = num_k / denom_k
            num_tau = np.einsum("ij,ij->i", cross12, r3)
            denom_tau = (np.linalg.norm(cross12, axis=1)**2 + 1e-18)
            tau = num_tau / denom_tau
            L_series = float(np.sum(np.linalg.norm(np.roll(r, -1, axis=0)-r, axis=1)))
            stats = {
                "samples": r.shape[0],
                "length_series_units": L_series,
                "kappa_min": float(np.min(kappa)),
                "kappa_max": float(np.max(kappa)),
                "radius_of_curvature_min": float(1.0/ (np.max(kappa)+1e-18)),
                "kappa_mean": float(np.mean(kappa)),
                "kappa_median": float(np.median(kappa)),
                "tau_mean": float(np.mean(tau)),
                "tau_median": float(np.median(tau)),
            }
            self.txt.delete("1.0", "end")
            for k,v in stats.items(): self.txt.insert("end", f"{k}: {v}\n")
            self.ax.clear()
            self.ax.plot(kappa); self.ax.set_xlabel("sample index"); self.ax.set_ylabel("curvature κ")
            self.ax.set_title("Curvature profile")
            self.canvas.draw()
        except Exception as e:
            self.txt.delete("1.0", "end"); self.txt.insert("end", f"Error: {e}\n")
            self.ax.clear(); self.ax.set_title("Error"); self.canvas.draw()

# Register plugins
PLUGINS = [BatchResultsPlugin, SpectrumPlugin, GeometryPlugin]

def main():
    app = Workbench()
    app.mainloop()

if __name__ == "__main__":
    main()