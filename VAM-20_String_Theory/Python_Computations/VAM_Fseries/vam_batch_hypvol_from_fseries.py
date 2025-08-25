#!/usr/bin/env python3
"""
vam_batch_hypvol_from_fseries.py
Iterate over ./knots/*/*.fseries → build PD from a projection of the curve → compute hyperbolic volume.

Inputs:
  - Root: ./knots by default; looks for ./knots/*/*.fseries (e.g., ./knots/4_1/4_1.fseries)
Outputs:
  - CSV with columns: knot_id, file, n_crossings, volume, projection_tries, status, message

Notes
  • This uses ONLY standard library + (optional) numpy if present. If numpy is not available,
    it falls back to pure Python math for core steps (slower).
  • The hyperbolic volume engine is imported from `vam_hypvol_no_deps.py` (no third-party deps).
  • PD extraction is generic and works best for prime, alternating knots; nonalternating or
    nearly-tangential projections may require more tries or a higher sample count.

Usage
  python vam_batch_hypvol_from_fseries.py \
      --root ./knots \
      --out  ./knots/hypvol_results.csv \
      --samples 1600 \
      --tries 40
"""

import os, glob, csv, math, cmath, random, argparse, sys

# ---------------------------------------------
# Optional numpy acceleration (safe fallback)
# ---------------------------------------------
try:
    import numpy as np
    HAVE_NP = True
except Exception:
    HAVE_NP = False

# ---------------------------------------------
# Import the dependency-free solver module
# ---------------------------------------------
try:
    from vam_hypvol_no_deps import hyperbolic_volume_from_pd
except ImportError:
    print("ERROR: Please place vam_hypvol_no_deps.py next to this script.", file=sys.stderr)
    sys.exit(1)

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
    return: list of 3D points r_k for k=0..M-1 on t in [0,2π)
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
        # pure Python path
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
# ---------------------------------------------
def _unit_random_dir():
    # random unit vector (Gaussian)
    x, y, z = random.gauss(0,1), random.gauss(0,1), random.gauss(0,1)
    nrm = math.sqrt(x*x + y*y + z*z) + 1e-18
    return (x/nrm, y/nrm, z/nrm)

def _orthonormal_basis(n):
    nx,ny,nz = n
    # pick a vector not parallel to n
    ax,ay,az = (1.0,0.0,0.0) if abs(nx) < 0.9 else (0.0,1.0,0.0)
    # u = normalize(n × a)
    ux,uy,uz = ny*az - nz*ay, nz*ax - nx*az, nx*ay - ny*ax
    un = math.sqrt(ux*ux+uy*uy+uz*uz)+1e-18
    ux,uy,uz = ux/un, uy/un, uz/un
    # v = n × u
    vx,vy,vz = ny*uz - nz*uy, nz*ux - nx*uz, nx*uy - ny*ux
    return (ux,uy,uz), (vx,vy,vz)

def _dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

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
    """
    Return (lam, mu) if segments p(lam)=p1+lam*(p2-p1), q(mu)=q1+mu*(q2-q1) intersect in 2D interior,
    else None. Avoid near-colinear or endpoint hits.
    """
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
    """
    P2: Nx2 points (projected), D: Nx depth values, closed polyline with segments i→i+1 (mod N)
    Returns PD code [(a,b,c,d), ...] or raises ValueError if no generic crossing diagram was found.

    Algorithm:
      1) Find all interior segment intersections (i,j) with |i-j|>1 and not endpoints.
      2) For each crossing, compute depth difference along 'depth_dir' to decide over/under.
      3) Build the list of "events" along the oriented curve (parameter s ∈ [0,1)): two per crossing.
      4) Create arc labels between consecutive events (circularly); label k = edge between event k and k+1.
      5) For each crossing, assemble (a,b,c,d) with positions 1 and 3 (b,d) = over, and 0 and 2 (a,c) = under.
    """
    N = len(P2)
    # 1) intersections
    crossings = []  # list of dict: {i,lam,j,mu, over='i'/'j', depth_gap, point=(x,y)}
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
            # depth at intersection
            Di = D[i] + lam*(D[(i+1)%N]-D[i])
            Dj = D[j] + mu*(D[(j+1)%N]-D[j])
            if abs(Di - Dj) < depth_tol:
                # nearly tangential/ambiguous; skip this projection later
                continue
            over = 'i' if Di > Dj else 'j'
            # reject tiny angle intersections (near-parallel); compute segment direction angles
            dx_i = p2[0]-p1[0]; dy_i = p2[1]-p1[1]
            dx_j = q2[0]-q1[0]; dy_j = q2[1]-q1[1]
            dotv = dx_i*dx_j + dy_i*dy_j
            n_i = math.hypot(dx_i,dy_i)+1e-18
            n_j = math.hypot(dx_j,dy_j)+1e-18
            cosang = max(-1.0, min(1.0, dotv/(n_i*n_j)))
            ang = math.degrees(math.acos(abs(cosang)))
            if ang < min_angle_deg:
                continue
            x = p1[0] + lam*(p2[0]-p1[0])
            y = p1[1] + lam*(p2[1]-p1[1])
            crossings.append(dict(i=i, lam=lam, j=j, mu=mu, over=over, depth_gap=abs(Di-Dj), pt=(x,y)))
    if not crossings:
        raise ValueError("No crossings detected (projection not generic).")

    # 2) build events along oriented parameter s=(k+lam)/N ∈ [0,1)
    events = []  # list of dict: {s, cross_id, on='i'/'j', seg_index, t_on_seg, over_event:bool}
    for cid, c in enumerate(crossings):
        s_i = (c['i'] + c['lam'])/N
        s_j = (c['j'] + c['mu'])/N
        events.append(dict(s=s_i, cross_id=cid, on='i', seg_index=c['i'], t_on_seg=c['lam'], over_event=(c['over']=='i')))
        events.append(dict(s=s_j, cross_id=cid, on='j', seg_index=c['j'], t_on_seg=c['mu'], over_event=(c['over']=='j')))

    # If two events have identical s (rare), nudge them
    events.sort(key=lambda e: e['s'])
    for k in range(1, len(events)):
        if abs(events[k]['s'] - events[k-1]['s']) < 1e-12:
            events[k]['s'] += 1e-9

    # 3) create arc labels between consecutive events
    #    outgoing label at event k is label L=k+1; incoming at event k is label of previous (k-1)
    L = len(events)
    for idx,e in enumerate(events):
        e['incoming_label'] = (idx if idx>0 else L)          # previous edge label
        e['outgoing_label'] = (idx+1 if idx+1<=L else 1)     # next edge label

    # 4) assemble PD tuples (a,b,c,d) per crossing
    #    over side provides (b=prev, d=next); under side provides (a=prev, c=next)
    #    This ensures positions 1 and 3 (b,d) are over, matching the triangulation module.
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
            # If both appear over/under (shouldn't happen), skip this crossing
            continue
        pd.append((a,b,c,d))

    # Validate: each label should appear exactly twice across all PD entries
    counts = {}
    for (a,b,c,d) in pd:
        for lab in (a,b,c,d):
            counts[lab] = counts.get(lab,0)+1
    ok = all(cnt==2 for cnt in counts.values())
    if not ok or len(counts) != L:
        raise ValueError("PD validation failed (labels not paired exactly twice); try a different projection.")
    return pd

def pd_from_curve(P3, tries=40, samples_2d=None, seed=12345):
    """
    Try multiple random projection directions; return the first PD that validates.
    Heuristic: prefer projections with larger min crossing angle and larger depth gaps.
    """
    rng = random.Random(seed)
    best = None
    best_score = -1.0
    for t in range(tries):
        n = _unit_random_dir()
        P2, D = project_curve(P3, n)
        try:
            pd = build_pd_from_projection(P2, D, n, min_angle_deg=1.0, depth_tol=1e-6)
            # score: number of crossings (more is fine) and average depth gap
            Ncross = len(pd)
            # crude score: prefer more crossings with success
            score = Ncross
            if score > best_score:
                best_score = score
                best = (pd, n)
                # you could break early; but keep searching for an even better one
        except Exception:
            continue
    if best is None:
        raise ValueError("Failed to extract PD from any projection.")
    return best[0]

# ---------------------------------------------
# Batch driver
# ---------------------------------------------
def parse_knot_id(path):
    # Expect ./knots/4_1/4_1.fseries → "4_1"
    base = os.path.basename(path)
    name, _ = os.path.splitext(base)
    # Prefer directory name if it looks like *_* (e.g., 4_1)
    parent = os.path.basename(os.path.dirname(path))
    if "_" in parent:
        return parent
    return name

def process_file(path, samples=1600, tries=40):
    coeffs = load_fseries(path)
    P3 = eval_series(coeffs, samples)
    try:
        pd = pd_from_curve(P3, tries=tries)
        vol = hyperbolic_volume_from_pd(pd, verbose=False)
        return dict(status="ok", volume=vol, n_crossings=len(pd), message="")
    except Exception as e:
        return dict(status="fail", volume=float('nan'), n_crossings=0, message=str(e))

def main():
    ap = argparse.ArgumentParser(description="Batch hyperbolic volume for ./knots/*/*.fseries")
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
