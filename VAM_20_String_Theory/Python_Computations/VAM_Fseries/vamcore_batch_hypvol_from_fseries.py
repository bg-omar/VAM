#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# vam_batch_hypvol_from_fseries.py  (VAMbindings-ready)
#
# Optional VAM C++ accelerations (if present in sstbindings):
#   • hyperbolic_volume_from_pd(...)  -> ./src/hyperbolic_volume.cpp
#       C++ binding: ./src_bindings/py_hyperbolic_volume.cpp
#       Example:     ./examples/hyperbolic_volume_example.py
#   • pd_from_curve(P3, tries, seed)  -> ./src/knot_pd.cpp
#       C++ binding: ./src_bindings/py_knot_pd.cpp
#       Example:     ./examples/knot_pd_example.py
#
# If these bindings are not available, this script falls back to the
# pure-Python implementations bundled below (no third-party deps).
# -----------------------------------------------------------------------------

import os, glob, csv, math, random, argparse, sys

# ---------------------------------------------
# Optional numpy acceleration (safe fallback)
# ---------------------------------------------
try:
    import numpy as np
    HAVE_NP = True
except Exception:
    HAVE_NP = False

# ---------------------------------------------
# Try C++-backed VAMbindings (optional)
# ---------------------------------------------
_VAM_PD = None
_VAM_HYPVOL = None
try:
    from sstbindings import hyperbolic_volume_from_pd as _VAM_HYPVOL  # optional
except Exception:
    _VAM_HYPVOL = None

try:
    # If your build exposes a faster PD extractor:
    from sstbindings import pd_from_curve as _VAM_PD  # optional
except Exception:
    _VAM_PD = None

# Put this near the top of your script for a self-check:
def _selfcheck():
    # A tiny PD of the figure-eight (4_1) in alternating layout is notoriously convention-sensitive.
    # So we only check that the "try both" path gets ~2.03 on *some* valid 4_1 PD.
    # If you have a trusted PD_41 list, plug it here to lock the convention.
    print("Self-check: pass a known 4_1 PD when available to pin convention.")

# ---------------------------------------------
# Pure-Python hyperbolic volume engine (fallback)
# ---------------------------------------------
if _VAM_HYPVOL is None:
    try:
        from vam_hypvol_no_deps import hyperbolic_volume_from_pd as _PY_HYPVOL
    except ImportError:
        print("ERROR: Place vam_hypvol_no_deps.py next to this script or provide sstbindings.hyperbolic_volume_from_pd.", file=sys.stderr)
        sys.exit(1)
else:
    _PY_HYPVOL = None

def _hyperbolic_volume_from_pd(pd, verbose=False):
    if _VAM_HYPVOL is not None:
        return _VAM_HYPVOL(pd)  # C++ path
    return _PY_HYPVOL(pd, verbose=verbose)  # Python path

def _vol_try_both_conventions(pd):
    # A: (b,d) are over (your current assumption)
    # B: (a,c) are over (swap under/over per crossing)
    def swap(pd_): return [(b,a,d,c) for (a,b,c,d) in pd_]

    vA = float("inf")
    vB = float("inf")
    try: vA = _hyperbolic_volume_from_pd(pd, verbose=False)
    except Exception: pass
    try: vB = _hyperbolic_volume_from_pd(swap(pd), verbose=False)
    except Exception: pass

    best = min(v for v in (vA, vB) if math.isfinite(v))
    return best if math.isfinite(best) else float('nan')

# ---------------------------------------------
# Load .fseries and evaluate the curve
# ---------------------------------------------
def load_fseries(path):
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
        return [[0.0]*6]
    return rows

def eval_series(coeffs, M):
    """
    coeffs: list of [Ax,Bx, Ay,By, Az,Bz] per harmonic index n (row n -> harmonic n)
    return: list/array of 3D points r_k for k=0..M-1 on t in [0,2π)
    """
    N = len(coeffs)
    if HAVE_NP:
        coeffs = np.asarray(coeffs, dtype=float)
        n = np.arange(N).reshape(-1, 1)
        t = (2*math.pi) * np.arange(M).reshape(1, -1) / M
        cos_nt = np.cos(n*t); sin_nt = np.sin(n*t)
        Ax,Bx,Ay,By,Az,Bz = (coeffs[:,0:1], coeffs[:,1:2], coeffs[:,2:3],
                             coeffs[:,3:4], coeffs[:,4:5], coeffs[:,5:6])
        x = (Ax*cos_nt + Bx*sin_nt).sum(axis=0)
        y = (Ay*cos_nt + By*sin_nt).sum(axis=0)
        z = (Az*cos_nt + Bz*sin_nt).sum(axis=0)
        return np.stack([x,y,z], axis=1)
    else:
        pts = []
        for k in range(M):
            t = 2*math.pi*k/M
            coss = [math.cos(n*t) for n in range(N)]
            sinn = [math.sin(n*t) for n in range(N)]
            x = sum(coeffs[n][0]*coss[n] + coeffs[n][1]*sinn[n] for n in range(N))
            y = sum(coeffs[n][2]*coss[n] + coeffs[n][3]*sinn[n] for n in range(N))
            z = sum(coeffs[n][4]*coss[n] + coeffs[n][5]*sinn[n] for n in range(N))
            pts.append((x,y,z))
        return pts

# ---------------------------------------------
# Projection + crossing detection → PD code
# (pure-Python fallback; optionally replaced by _VAM_PD)
# ---------------------------------------------
def _unit_random_dir():
    # random unit vector (Gaussian)
    x, y, z = random.gauss(0,1), random.gauss(0,1), random.gauss(0,1)
    nrm = math.sqrt(x*x + y*y + z*z) + 1e-18
    return (x/nrm, y/nrm, z/nrm)

def _orthonormal_basis(n):
    nx,ny,nz = n
    ax,ay,az = (1.0,0.0,0.0) if abs(nx) < 0.9 else (0.0,1.0,0.0)
    ux,uy,uz = ny*az - nz*ay, nz*ax - nx*az, nx*ay - ny*ax
    un = math.sqrt(ux*ux+uy*uy+uz*uz)+1e-18
    ux,uy,uz = ux/un, uy/un, uz/un
    vx,vy,vz = ny*uz - nz*uy, nz*ux - nx*uz, nx*uy - ny*ux
    return (ux,uy,uz), (vx,vy,vz)

def _dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

def preprocess_curve(P3):
    """
    Center and normalize curve to unit RMS radius.
    Accepts list/ndarray (N,3) and returns same type as input (numpy if available).
    """
    if HAVE_NP and isinstance(P3, np.ndarray):
        c = P3.mean(axis=0)
        Q = P3 - c
        r = np.sqrt((Q**2).sum(axis=1).mean()) + 1e-18
        return Q / r
    else:
        # Python list path
        cx = sum(p[0] for p in P3)/len(P3)
        cy = sum(p[1] for p in P3)/len(P3)
        cz = sum(p[2] for p in P3)/len(P3)
        Q = [(p[0]-cx, p[1]-cy, p[2]-cz) for p in P3]
        r2 = sum(px*px+py*py+pz*pz for (px,py,pz) in Q)/len(Q)
        r = math.sqrt(r2) + 1e-18
        return [(px/r, py/r, pz/r) for (px,py,pz) in Q]


def project_curve(P3, n):
    u, v = _orthonormal_basis(n)
    if HAVE_NP and isinstance(P3, np.ndarray):
        X = P3 @ np.array([u[0],u[1],u[2]])
        Y = P3 @ np.array([v[0],v[1],v[2]])
        D = P3 @ np.array([n[0],n[1],n[2]])
        P2 = np.stack([X,Y], axis=1)
        return P2, D
    else:
        P2, D = [], []
        for p in P3:
            px,py,pz = p
            P2.append((_dot(p,u), _dot(p,v)))
            D.append(_dot(p,n))
        return P2, D

def _seg_intersection(p1, p2, q1, q2, eps=1e-12):
    x1,y1 = p1; x2,y2 = p2
    x3,y3 = q1; x4,y4 = q2
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if abs(den) < eps:
        return None
    lam = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
    mu  = ((x1-x3)*(y1-y2) - (y1-y3)*(x1-x2)) / den
    if lam <= eps or lam >= 1-eps: return None
    if mu  <= eps or mu  >= 1-eps: return None
    return (lam, mu)

def build_pd_from_projection(P2, D, depth_dir, min_angle_deg=1.0, depth_tol=1e-6):
    N = len(P2)
    crossings = []
    for i in range(N):
        p1 = P2[i]
        p2 = P2[(i+1)%N]
        for j in range(i+2, N):
            if j == i or j == (i-1)%N or (i==0 and j==N-1):
                continue
            q1 = P2[j]
            q2 = P2[(j+1)%N]
            ans = _seg_intersection(p1,p2,q1,q2)
            if not ans:
                continue
            lam, mu = ans
            Di = D[i] + lam*(D[(i+1)%N]-D[i])
            Dj = D[j] + mu*(D[(j+1)%N]-D[j])
            if abs(Di - Dj) < depth_tol:
                continue
            over = 'i' if Di > Dj else 'j'
            dx_i = p2[0]-p1[0]; dy_i = p2[1]-p1[1]
            dx_j = q2[0]-q1[0]; dy_j = q2[1]-q1[1]
            dotv = dx_i*dx_j + dy_i*dy_j
            n_i = math.hypot(dx_i,dy_i)+1e-18
            n_j = math.hypot(dx_j,dy_j)+1e-18
            cosang = max(-1.0, min(1.0, dotv/(n_i*n_j)))
            ang = math.degrees(math.acos(abs(cosang)))
            if ang < min_angle_deg:
                continue
            x = p1[0] + lam*(p2[0]-p1[0]); y = p1[1] + lam*(p2[1]-p1[1])
            crossings.append(dict(i=i, lam=lam, j=j, mu=mu, over=over, depth_gap=abs(Di-Dj), pt=(x,y)))
    if not crossings:
        raise ValueError("No crossings detected (projection not generic).")

    events = []
    for cid, c in enumerate(crossings):
        s_i = (c['i'] + c['lam'])/N
        s_j = (c['j'] + c['mu'])/N
        events.append(dict(s=s_i, cross_id=cid, on='i', seg_index=c['i'], t_on_seg=c['lam'], over_event=(c['over']=='i')))
        events.append(dict(s=s_j, cross_id=cid, on='j', seg_index=c['j'], t_on_seg=c['mu'], over_event=(c['over']=='j')))

    events.sort(key=lambda e: e['s'])
    for k in range(1, len(events)):
        if abs(events[k]['s'] - events[k-1]['s']) < 1e-12:
            events[k]['s'] += 1e-9

    L = len(events)
    for idx,e in enumerate(events):
        e['incoming_label'] = (idx if idx>0 else L)
        e['outgoing_label'] = (idx+1 if idx+1<=L else 1)

    pd = []
    for cid in range(len(crossings)):
        evs = [e for e in events if e['cross_id']==cid]
        if len(evs) != 2:
            continue
        e1, e2 = evs
        if e1['over_event'] and not e2['over_event']:
            b, d = e1['incoming_label'], e1['outgoing_label']
            a, c = e2['incoming_label'], e2['outgoing_label']
        elif e2['over_event'] and not e1['over_event']:
            b, d = e2['incoming_label'], e2['outgoing_label']
            a, c = e1['incoming_label'], e1['outgoing_label']
        else:
            continue
        pd.append((a,b,c,d))

    counts = {}
    for (a,b,c,d) in pd:
        for lab in (a,b,c,d):
            counts[lab] = counts.get(lab,0)+1
    ok = all(cnt==2 for cnt in counts.values())
    if not ok or len(counts) != L:
        raise ValueError("PD validation failed (labels not paired exactly twice); try a different projection.")
    return pd

def _pd_from_curve_py(P3, tries=40, samples_2d=None, seed=12345):
    rng = random.Random(seed)
    best = None
    best_score = -1.0
    for t in range(tries):
        n = (rng.gauss(0,1), rng.gauss(0,1), rng.gauss(0,1))
        nrm = math.sqrt(n[0]*n[0] + n[1]*n[1] + n[2]*n[2]) + 1e-18
        n = (n[0]/nrm, n[1]/nrm, n[2]/nrm)
        P2, D = project_curve(P3, n)
        try:
            pd = build_pd_from_projection(P2, D, n, min_angle_deg=1.0, depth_tol=1e-6)
            score = len(pd)
            if score > best_score:
                best_score = score
                best = (pd, n)
        except Exception:
            continue
    if best is None:
        raise ValueError("Failed to extract PD from any projection.")
    return best[0]

def pd_from_curve(P3, tries=40, samples_2d=None, seed=12345):
    if _VAM_PD is not None:
        return _VAM_PD(P3, tries, seed)  # C++ path

    rng = random.Random(seed)
    best_pd, best_score = None, float("+inf")
    for _ in range(tries):
        # random unit direction
        n = (rng.gauss(0,1), rng.gauss(0,1), rng.gauss(0,1))
        nrm = math.sqrt(n[0]*n[0] + n[1]*n[1] + n[2]*n[2]) + 1e-18
        n = (n[0]/nrm, n[1]/nrm, n[2]/nrm)

        P2, D = project_curve(P3, n)
        try:
            # tighten to avoid near-tangencies
            pd = build_pd_from_projection(P2, D, n, min_angle_deg=8.0, depth_tol=3e-5)
        except Exception:
            continue

        # score: fewer crossings is better
        sc = len(pd)
        if sc < best_score:
            best_score, best_pd = sc, pd

    if best_pd is None:
        raise ValueError("Failed to extract PD from any projection.")
    return best_pd



# ---------------------------------------------
# Batch driver
# ---------------------------------------------
def parse_knot_id(path):
    base = os.path.basename(path)
    name, _ = os.path.splitext(base)
    parent = os.path.basename(os.path.dirname(path))
    if "_" in parent:
        return parent
    return name

def process_file(path, samples=1600, tries=40):
    coeffs = load_fseries(path)
    P3 = eval_series(coeffs, samples)
    P3 = preprocess_curve(P3)


    try:
        pd = pd_from_curve(P3, tries=tries)
        vol = _vol_try_both_conventions(pd)
        return dict(status="ok", volume=vol, n_crossings=len(pd), message="")
    except Exception as e:
        return dict(status="fail", volume=float('nan'), n_crossings=0, message=str(e))

def main():
    ap = argparse.ArgumentParser(description="Batch hyperbolic volume for ./knots/*/*.fseries (VAMbindings optional accel)")
    ap.add_argument("--root", type=str, default="./knots", help="Root directory containing subfolders per knot")
    ap.add_argument("--out",  type=str, default="./knots/hypvol_results.csv", help="Output CSV path")
    ap.add_argument("--samples", type=int, default=1600, help="Samples along the curve (t-grid)")
    ap.add_argument("--tries",   type=int, default=40,   help="Random projection tries")
    args = ap.parse_args()

    pattern = os.path.join(args.root, "*", "*.fseries")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No files matched: {pattern}")
        return

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["knot_id","file","n_crossings","volume","projection_tries","status","message"])
        for path in files:
            kid = parse_knot_id(path)
            res = process_file(path, samples=args.samples, tries=args.tries)
            w.writerow([kid, path, res["n_crossings"], f"{res['volume']:.12f}" if math.isfinite(res['volume']) else "",
                        args.tries, res["status"], res["message"]])
            print(f"[{res['status']}] {kid}: volume={res['volume']}  crossings={res['n_crossings']}  {os.path.relpath(path)}")
    print("Wrote:", args.out)

if __name__ == "__main__":
    main()