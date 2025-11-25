# canon_evidence.py
import os, glob, re
import numpy as np
import pandas as pd

# --- VAM bindings (optional) ---
try:
    from sstbindings import fourier_knot_eval, biot_savart_velocity_grid, curl3d_central
    HAVE_VAM = True
except Exception:
    HAVE_VAM = False

# ---------- IO ----------
def parse_fseries_multi(filename):
    knots, header = [], None
    arrays = {k: [] for k in ('a_x','b_x','a_y','b_y','a_z','b_z')}
    with open(filename) as f:
        for raw in f:
            line = raw.strip()
            if line.startswith('%'):
                if arrays['a_x']:
                    knots.append((header, {k: np.array(v, float) for k,v in arrays.items()}))
                    for v in arrays.values(): v.clear()
                header = line.lstrip('%').strip(); continue
            if not line and arrays['a_x']:
                knots.append((header, {k: np.array(v, float) for k,v in arrays.items()}))
                for v in arrays.values(): v.clear()
                header = None; continue
            parts = line.split()
            if len(parts) == 6:
                for key, val in zip(arrays, map(float, parts)):
                    arrays[key].append(val)
    if arrays['a_x']:
        knots.append((header, {k: np.array(v, float) for k,v in arrays.items()}))
    return knots

def base_id(fname):
    s = os.path.basename(fname).replace("knot.","").replace(".fseries","")
    m = re.match(r"(\d+(?:a|n)?_\d+)", s)  # strips trailing p/d/r/s/z if present
    return m.group(1) if m else s

# ---------- Geometry ----------
def eval_fourier_block(coeffs, s):
    if HAVE_VAM:
        x, y, z = fourier_knot_eval(coeffs['a_x'], coeffs['b_x'],
                                    coeffs['a_y'], coeffs['b_y'],
                                    coeffs['a_z'], coeffs['b_z'],
                                    s.astype(float))
        return np.asarray(x), np.asarray(y), np.asarray(z)
    # NumPy fallback (vectorized)
    j = np.arange(1, coeffs['a_x'].size+1, dtype=float)[:, None]
    sj = j * s[None, :]
    cosj, sinj = np.cos(sj), np.sin(sj)
    def series(ax,bx): return (ax[:,None]*cosj + bx[:,None]*sinj).sum(axis=0)
    return series(coeffs['a_x'], coeffs['b_x']), \
        series(coeffs['a_y'], coeffs['b_y']), \
        series(coeffs['a_z'], coeffs['b_z'])

def resample_by_arclength(x, y, z, M=2000):
    P = np.stack([x,y,z], axis=1)
    d = np.linalg.norm(np.diff(P, axis=0, append=P[:1]), axis=1)
    s = np.concatenate([[0.0], np.cumsum(d)])[:-1]
    s /= s[-1]  # [0,1)
    u = np.linspace(0.0, 1.0, M, endpoint=False)
    def interp(col): return np.interp(u, s, col, period=1.0)
    return interp(x), interp(y), interp(z)

# ---------- Fields ----------
def biot_savart_velocity(poly, grid_points, eps=None):
    if HAVE_VAM:
        return biot_savart_velocity_grid(poly.astype(float), grid_points.astype(float))
    # fallback with scale-aware core
    if eps is None:
        # infer spacing along x-axis
        ux = np.unique(grid_points[:,0])
        h = np.min(np.diff(ux)) if ux.size>1 else 1e-3
        eps = 0.75 * h
    eps2 = eps*eps
    vel = np.zeros_like(grid_points, dtype=float)
    N = poly.shape[0]
    for i in range(N):
        r0 = poly[i]; r1 = poly[(i+1)%N]
        dl = r1 - r0
        rmid = 0.5*(r0 + r1)
        R = grid_points - rmid
        invR3 = 1.0 / (np.linalg.norm(R, axis=1)**2 + eps2)**1.5
        vel += np.cross(dl, R) * invR3[:,None]
    return vel * (1.0/(4.0*np.pi))

def curl3d(velocity, shape, spacing):
    if HAVE_VAM:
        return np.asarray(curl3d_central(velocity.reshape(*shape,3).astype(float),
                                         float(spacing))).reshape(-1,3)
    vx, vy, vz = (velocity[:,0].reshape(shape),
                  velocity[:,1].reshape(shape),
                  velocity[:,2].reshape(shape))
    h2 = 2*spacing
    cx = (np.roll(vz,-1,1)-np.roll(vz,1,1))/h2 - (np.roll(vy,-1,2)-np.roll(vy,1,2))/h2
    cy = (np.roll(vx,-1,2)-np.roll(vx,1,2))/h2 - (np.roll(vz,-1,0)-np.roll(vz,1,0))/h2
    cz = (np.roll(vy,-1,0)-np.roll(vy,1,0))/h2 - (np.roll(vx,-1,1)-np.roll(vx,1,1))/h2
    return np.stack([cx,cy,cz], axis=-1).reshape(-1,3)

# ---------- Grid & mask ----------
def make_grid(grid_size, spacing, r_phys=0.90):
    grid_range = spacing*(np.arange(grid_size)-grid_size//2)
    X, Y, Z = np.meshgrid(grid_range, grid_range, grid_range, indexing='ij')
    grid_points = np.stack([X.ravel(),Y.ravel(),Z.ravel()], axis=-1)
    # interior slice for a fixed physical radius
    n = int(round(r_phys/spacing))
    interior = slice(grid_size//2 - n, grid_size//2 + n)
    Xf, Yf, Zf = np.meshgrid(grid_range[interior], grid_range[interior], grid_range[interior], indexing='ij')
    r_sq = (Xf**2 + Yf**2 + Zf**2).ravel()
    return grid_points, (grid_size,grid_size,grid_size), r_sq, interior

# ---------- Helicity ----------
def a_mu_for_file(path, grid_size, spacing, r_phys=0.90):
    blocks = parse_fseries_multi(path)
    header, coeffs = max(blocks, key=lambda b: b[1]['a_x'].size)
    s = np.linspace(0, 2*np.pi, 1000, endpoint=False, dtype=float)
    x, y, z = eval_fourier_block(coeffs, s)
    x, y, z = resample_by_arclength(x, y, z, M=2000)
    poly = np.stack([x,y,z], axis=1)
    gp, gs, r2, inner = make_grid(grid_size, spacing, r_phys)
    vel  = biot_savart_velocity(poly, gp, eps=None)        # eps≈0.75h inside
    vort = curl3d(vel, gs, spacing)
    v_sub = vel.reshape(*gs,3)[inner, :, :][:, inner, :][:, :, inner].reshape(-1,3)
    w_sub = vort.reshape(*gs,3)[inner, :, :][:, inner, :][:, :, inner].reshape(-1,3)
    Hc = np.einsum('ij,ij->', v_sub, w_sub, dtype=float)
    Hm = np.sum(np.linalg.norm(w_sub, axis=1)**2 * r2, dtype=float)
    return 0.5*(Hc/Hm - 1.0), Hc, Hm

# ---------- Batch + labels ----------
BANDS = {
    "near-amphi": 0.015,   # |a + 0.5| <= 0.015
    "border":     0.02     # for display/flagging
}

def classify(a64, sig):
    delta = abs(a64 + 0.5)
    if delta <= BANDS["near-amphi"] and sig <= 0.02:
        return "near-amphichiral"
    if delta > 0.02 and sig <= 0.02:
        return "chiral (converged)"
    if sig <= 0.05:
        return "tentative"
    return "unstable"

if __name__ == "__main__":
    paths = sorted(glob.glob("knot.*.fseries"))
    rows = []
    for path in paths:
        a32,_,_ = a_mu_for_file(path, 32, 0.10)
        a48,_,_ = a_mu_for_file(path, 48, 0.08)
        a64,_,_ = a_mu_for_file(path, 64, 0.06)
        sig = abs(a64 - a48)
        label = classify(a64, sig)
        rows.append({
            "file": os.path.basename(path),
            "base": base_id(path),
            "a32": a32, "a48": a48, "a64": a64,
            "sigma": sig, "label": label
        })
        print(f"{os.path.basename(path)}  a32={a32:.6f}  a48={a48:.6f}  a64={a64:.6f}  σ={sig:.5f}  → {label}")
    df = pd.DataFrame(rows).sort_values(["base","file"])
    df.to_csv("CANON_evidence_helicity.csv", index=False)

    # Emit a LaTeX longtable for the supplement
    def emoji(a64, sig):
        d = abs(a64 + 0.5)
        if sig>0.05: return "🔴"
        if d<=0.015 and sig<=0.02: return "🟢"
        if d>0.02 and sig<=0.02:   return "🟠"
        return "🟡"
    df_out = df.copy()
    df_out["Δ_from_-0.5"] = (df["a64"] + 0.5).abs()
    df_out["mark"] = [emoji(a,s) for a,s in zip(df["a64"], df["sigma"])]
    with open("CANON_evidence_table.tex","w") as f:
        f.write("\\begin{longtable}{llrrrrrl}\n\\toprule\n")
        f.write("file & base & $a_{32}$ & $a_{48}$ & $a_{64}$ & $\\sigma$ & $|a_{64}+0.5|$ & label \\\\\n\\midrule\n")
        for _,r in df_out.iterrows():
            f.write(f"{r.file} & {r.base} & {r.a32:.6f} & {r.a48:.6f} & {r.a64:.6f} & {r.sigma:.5f} & {r['Δ_from_-0.5']:.5f} & {r.label} {r.mark} \\\\\n")
        f.write("\\bottomrule\n\\end{longtable}\n")
    print("Wrote CANON_evidence_helicity.csv and CANON_evidence_table.tex")