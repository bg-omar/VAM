# sst_canon_evidence.py
import os, glob, re
import numpy as np
import pandas as pd

# Optional pybind11 bindings; NumPy fallbacks if missing
try:
    from sstbindings import fourier_knot_eval, biot_savart_velocity_grid, curl3d_central
    HAVE_VAM = True
except Exception:
    HAVE_VAM = False

# ---------- Parsing ----------
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
            if len(parts)==6:
                for key,val in zip(arrays, map(float, parts)): arrays[key].append(val)
    if arrays['a_x']:
        knots.append((header, {k: np.array(v, float) for k,v in arrays.items()}))
    return knots

def base_id(fname):
    s = os.path.basename(fname).replace("knot.","").replace(".fseries","")
    m = re.match(r"(\d+(?:a|n)?_\d+)", s)  # strips trailing p/d/r/s/z
    return m.group(1) if m else s

# ---------- Geometry on Σ_t ----------
def eval_fourier_block(coeffs, s):
    if HAVE_VAM:
        x,y,z = fourier_knot_eval(coeffs['a_x'], coeffs['b_x'],
                                  coeffs['a_y'], coeffs['b_y'],
                                  coeffs['a_z'], coeffs['b_z'], s.astype(float))
        return np.asarray(x), np.asarray(y), np.asarray(z)
    j = np.arange(1, coeffs['a_x'].size+1, float)[:,None]
    sj = j * s[None,:]
    def series(ax,bx): return (ax[:,None]*np.cos(sj) + bx[:,None]*np.sin(sj)).sum(axis=0)
    return series(coeffs['a_x'],coeffs['b_x']), series(coeffs['a_y'],coeffs['b_y']), series(coeffs['a_z'],coeffs['b_z'])

def resample_by_arclength(x,y,z, M=2000):
    P = np.stack([x,y,z], 1)
    d = np.linalg.norm(np.diff(P, axis=0, append=P[:1]), axis=1)
    s = np.concatenate([[0.0], np.cumsum(d)])[:-1]; s /= s[-1]
    u = np.linspace(0.0, 1.0, M, endpoint=False)
    def interp(col): return np.interp(u, s, col, period=1.0)
    return interp(x), interp(y), interp(z)

# ---------- Fields (swirl flow and vorticity) ----------
def biot_savart_swirl(poly, grid_points, eps=None):
    if HAVE_VAM:
        return biot_savart_velocity_grid(poly.astype(float), grid_points.astype(float))
    if eps is None:
        ux = np.unique(grid_points[:,0])
        h = np.min(np.diff(ux)) if ux.size>1 else 1e-3
        eps = 0.75*h
    eps2 = eps*eps
    vel = np.zeros_like(grid_points, float)
    N = poly.shape[0]
    for i in range(N):
        r0, r1 = poly[i], poly[(i+1)%N]
        dl = r1 - r0
        rmid = 0.5*(r0 + r1)
        R = grid_points - rmid
        invR3 = 1.0 / (np.linalg.norm(R, axis=1)**2 + eps2)**1.5
        vel += np.cross(dl, R) * invR3[:,None]
    return vel * (1.0/(4.0*np.pi))

def curl3d_central_fallback(velocity, shape, spacing):
    if HAVE_VAM:
        return np.asarray(curl3d_central(velocity.reshape(*shape,3).astype(float), float(spacing))).reshape(-1,3)
    vx = velocity[:,0].reshape(shape); vy = velocity[:,1].reshape(shape); vz = velocity[:,2].reshape(shape)
    h2 = 2*spacing
    cx = (np.roll(vz,-1,1)-np.roll(vz,1,1))/h2 - (np.roll(vy,-1,2)-np.roll(vy,1,2))/h2
    cy = (np.roll(vx,-1,2)-np.roll(vx,1,2))/h2 - (np.roll(vz,-1,0)-np.roll(vz,1,0))/h2
    cz = (np.roll(vy,-1,0)-np.roll(vy,1,0))/h2 - (np.roll(vx,-1,1)-np.roll(vx,1,1))/h2
    return np.stack([cx,cy,cz], -1).reshape(-1,3)

# ---------- Grid on Σ_t with fixed physical Ω ----------
def make_leaf_grid(N, h, r_phys=0.90):
    axis = h*(np.arange(N) - N//2)
    X,Y,Z = np.meshgrid(axis, axis, axis, indexing='ij')
    pts = np.stack([X.ravel(),Y.ravel(),Z.ravel()], -1)
    n = int(round(r_phys/h))
    sl = slice(N//2 - n, N//2 + n)
    Xf,Yf,Zf = np.meshgrid(axis[sl], axis[sl], axis[sl], indexing='ij')
    r2 = (Xf**2 + Yf**2 + Zf**2).ravel()
    return pts, (N,N,N), r2, sl

# ---------- Swirl-helicity asymmetry ----------
def a_SST_for_file(path, N, h, r_phys=0.90):
    blocks = parse_fseries_multi(path)
    header, coeffs = max(blocks, key=lambda b: b[1]['a_x'].size)
    s = np.linspace(0, 2*np.pi, 1000, endpoint=False, dtype=float)
    x,y,z = eval_fourier_block(coeffs, s)
    x,y,z = resample_by_arclength(x,y,z, M=2000)
    poly = np.stack([x,y,z], 1)
    gp, shape, r2, sl = make_leaf_grid(N, h, r_phys)
    vel  = biot_savart_swirl(poly, gp)
    vort = curl3d_central_fallback(vel, shape, h)
    v_sub = vel.reshape(*shape,3)[sl, :, :][:, sl, :][:, :, sl].reshape(-1,3)
    w_sub = vort.reshape(*shape,3)[sl, :, :][:, sl, :][:, :, sl].reshape(-1,3)
    Hc = np.einsum('ij,ij->', v_sub, w_sub, dtype=float)
    Hm = np.sum(np.linalg.norm(w_sub, axis=1)**2 * r2, dtype=float)
    a = 0.5*(Hc/Hm - 1.0)
    return a, Hc, Hm

# ---------- Labels ----------
def classify(a64, sig):
    delta = abs(a64 + 0.5)
    if delta <= 0.015 and sig <= 0.02: return "near-amphichiral"
    if delta > 0.02 and sig <= 0.02:  return "chiral (converged)"
    if sig <= 0.05:                   return "tentative"
    return "unstable"

if __name__ == "__main__":
    paths = sorted(glob.glob("knot.*.fseries"))
    rows = []
    for p in paths:
        a32,_,_ = a_SST_for_file(p, 32, 0.10)
        a48,_,_ = a_SST_for_file(p, 48, 0.08)
        a64,_,_ = a_SST_for_file(p, 64, 0.06)
        sig = abs(a64 - a48)
        label = classify(a64, sig)
        print(f"{os.path.basename(p)}  a32={a32:.6f}  a48={a48:.6f}  a64={a64:.6f}  σ={sig:.5f}  → {label}")
        rows.append({"file": os.path.basename(p), "base": base_id(p),
                     "a32": a32, "a48": a48, "a64": a64, "sigma": sig, "label": label})
    df = pd.DataFrame(rows).sort_values(["base","file"])
    df.to_csv("SST_helicity_canon.csv", index=False)

    # LaTeX longtable for supplement
    df["Delta_from_-0.5"] = (df["a64"] + 0.5).abs()
    with open("SST_helicity_canon_table.tex","w") as f:
        f.write("\\begin{longtable}{llrrrrrl}\\toprule\n")
        f.write("file & base & $a_{32}$ & $a_{48}$ & $a_{64}$ & $\\sigma$ & $|a_{64}+0.5|$ & label \\\\\n\\midrule\n")
        for _,r in df.iterrows():
            f.write(f"{r.file} & {r.base} & {r.a32:.6f} & {r.a48:.6f} & {r.a64:.6f} & {r.sigma:.5f} & {r.Delta_from_-0.5:.5f} & {r.label} \\\\\n")
        f.write("\\bottomrule\\end{longtable}\n")
    print("Wrote SST_helicity_canon.csv and SST_helicity_canon_table.tex")