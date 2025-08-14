# Parse the uploaded Fourier series files, reconstruct the 3D knot curves, and render them
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D projection)
import os
from pathlib import Path
import pandas as pd

# or in a Jupyter notebook:
import IPython.display as display


# --- Utilities ---
def load_fseries(path):
    """
    Load an .fseries file where each row corresponds to harmonic j
    with columns: a_x b_x a_y b_y a_z b_z.
    Lines starting with '%' are comments.
    Returns:
        j (np.ndarray): harmonic indices (0..M-1)
        A (np.ndarray): shape (M, 3) cosine coefficients for x,y,z
        B (np.ndarray): shape (M, 3) sine coefficients for x,y,z
    """
    # Read while ignoring comment lines starting with '%'
    raw = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            ls = line.strip()
            if not ls or ls.startswith('%'):
                continue
            parts = ls.split()
            # Accept both space and comma separated
            if len(parts) == 1 and (',' in parts[0]):
                parts = [p for p in parts[0].split(',') if p]
            # Expect 6 numeric columns per row
            if len(parts) < 6:
                continue
            try:
                nums = [float(p) for p in parts[:6]]
                raw.append(nums)
            except ValueError:
                continue
    data = np.array(raw, dtype=float)
    if data.ndim != 2 or data.shape[1] < 6:
        raise ValueError(f"File {path} does not have the expected 6-column numeric format.")
    A = data[:, [0, 2, 4]]  # a_x, a_y, a_z
    B = data[:, [1, 3, 5]]  # b_x, b_y, b_z
    j = np.arange(A.shape[0])  # j = 0..M-1
    return j, A, B

def eval_curve(j, A, B, s):
    """
    Evaluate x(s), y(s), z(s) from Fourier series:
        X_k(s) = sum_j [ A_{j,k} cos(j s) + B_{j,k} sin(j s) ], k in {x,y,z}
    Args:
        j: (M,)
        A: (M,3), B: (M,3)
        s: (T,)
    Returns:
        curve: (T,3)
    """
    js = np.outer(j, s)  # (M,T)
    cos_js = np.cos(js)
    sin_js = np.sin(js)
    # For each coord k: sum_j A_jk cos(js) + B_jk sin(js)
    # Compute in vectorized form
    X = cos_js.T @ A[:, 0] + sin_js.T @ B[:, 0]
    Y = cos_js.T @ A[:, 1] + sin_js.T @ B[:, 1]
    Z = cos_js.T @ A[:, 2] + sin_js.T @ B[:, 2]
    return np.vstack([X, Y, Z]).T  # (T,3)

def center_and_scale(P):
    """
    Center curve at origin and scale to unit max radius for consistent rendering.
    """
    C = P - P.mean(axis=0, keepdims=True)
    r = np.sqrt((C**2).sum(axis=1)).max()
    if r == 0:
        return C
    return C / r

def make_tube(P, radius=0.03, n_theta=24):
    """
    Build a simple tube (circular cross-section) around 3D curve P (T,3).
    Returns (X, Y, Z) arrays suitable for plot_surface.
    """
    T = len(P)
    # Tangents (central differences)
    dP = np.zeros_like(P)
    dP[1:-1] = (P[2:] - P[:-2]) * 0.5
    dP[0] = P[1] - P[0]
    dP[-1] = P[-1] - P[-2]
    # Normalize tangents
    tnorm = np.linalg.norm(dP, axis=1, keepdims=True) + 1e-12
    Tvec = dP / tnorm

    # Construct a normal / binormal frame using a fixed reference and Gram-Schmidt
    ref = np.array([0.0, 0.0, 1.0])
    # If tangent ~ ref, switch reference
    ref_alt = np.array([0.0, 1.0, 0.0])

    Nvec = np.zeros_like(Tvec)
    for i in range(len(P)):
        r = ref if abs(np.dot(Tvec[i], ref)) < 0.9 else ref_alt
        # Normal candidate perpendicular to Tvec[i]
        n = r - np.dot(r, Tvec[i]) * Tvec[i]
        n_norm = np.linalg.norm(n) + 1e-12
        n = n / n_norm
        Nvec[i] = n
    Bvec = np.cross(Tvec, Nvec)

    theta = np.linspace(0, 2*np.pi, n_theta, endpoint=True)  # include closure seam
    cos_t = np.cos(theta)[None, :]  # (1,n_theta)
    sin_t = np.sin(theta)[None, :]  # (1,n_theta)

    # Tube points: P + r*(cos theta * N + sin theta * B)
    X = P[:, 0:1] + radius*(cos_t * Nvec[:, 0:1] + sin_t * Bvec[:, 0:1])
    Y = P[:, 1:2] + radius*(cos_t * Nvec[:, 1:2] + sin_t * Bvec[:, 1:2])
    Z = P[:, 2:3] + radius*(cos_t * Nvec[:, 2:3] + sin_t * Bvec[:, 2:3])
    return X, Y, Z

def render_knot(P, out_png, title):
    """
    Render a 'fancy' 3D view:
      - tube surface (no explicit colors; default matplotlib shading)
      - equal aspect
      - minimalist axes
    """
    # Build tube
    X, Y, Z = make_tube(P, radius=0.04, n_theta=48)

    fig = plt.figure(figsize=(8, 8), dpi=160)
    ax = fig.add_subplot(111, projection='3d')

    # Plot tube surface (no explicit colormap/color to respect constraints)
    ax.plot_surface(X, Y, Z, linewidth=0, antialiased=True, shade=True)

    # Equal aspect
    max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
    mid_x = 0.5*(X.max()+X.min())
    mid_y = 0.5*(Y.max()+Y.min())
    mid_z = 0.5*(Z.max()+Z.min())
    ax.set_xlim(mid_x - 0.5*max_range, mid_x + 0.5*max_range)
    ax.set_ylim(mid_y - 0.5*max_range, mid_y + 0.5*max_range)
    ax.set_zlim(mid_z - 0.5*max_range, mid_z + 0.5*max_range)

    # Minimalist axes
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_xlabel(''); ax.set_ylabel(''); ax.set_zlabel('')
    ax.set_title(title)

    fig.tight_layout()
    fig.savefig(out_png, bbox_inches='tight')
    plt.close(fig)

# --- Discover files ---
base = Path("knots/6_2/")
candidates = [
    base / "knot.6_2.fseries",
    base / "knot.6_2d.fseries",
    base / "knot.6_2p.fseries",
    ]
existing = [p for p in candidates if p.exists()]

if not existing:
    raise FileNotFoundError("No .fseries files were found ")

# Evaluate and render each knot
s = np.linspace(0, 2*np.pi, 2000, endpoint=True)  # include closure
rows = []
outputs = []
for path in existing:
    j, A, B = load_fseries(path)
    P = eval_curve(j, A, B, s)
    P = center_and_scale(P)
    png_path = str(path.with_suffix(".png"))
    title = f"{path.name} (harmonics={len(j)})"
    render_knot(P, png_path, title)
    outputs.append(png_path)

    # Collect a small summary row
    radius_rms = np.sqrt((P**2).sum(axis=1)).mean()
    length = np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1))
    rows.append({
        "file": path.name,
        "harmonics": len(j),
        "mean_radius": radius_rms,
        "curve_length_units": length,
        "png": png_path
    })

# Show a quick summary table to the user
df = pd.DataFrame(rows)
display.display("Knot Fourier Series Summary", df)

# Return generated image paths for convenience
print(outputs)