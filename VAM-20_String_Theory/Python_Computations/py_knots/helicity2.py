import os

import numpy as np

# === Load Cleaned Fourier Series ===
def load_fourier_series_clean(filename):
    data = []
    with open(filename) as f:
        for line in f:
            if line.strip().startswith('%') or not line.strip():
                continue
            parts = line.split()
            if len(parts) == 6:
                data.append([float(x) for x in parts])
            if len(parts) != 6:
                continue  # instead of print warn

    data = np.array(data)
    return data[:, 0], data[:, 1], data[:, 2], data[:, 3], data[:, 4], data[:, 5]


# === Knot Reconstruction ===
def reconstruct_knot(a_x, b_x, a_y, b_y, a_z, b_z, N=1000):
    s = np.linspace(0, 2*np.pi, N)
    x = np.sum([a_x[j] * np.cos((j+1)*s) + b_x[j] * np.sin((j+1)*s) for j in range(len(a_x))], axis=0)
    y = np.sum([a_y[j] * np.cos((j+1)*s) + b_y[j] * np.sin((j+1)*s) for j in range(len(a_y))], axis=0)
    z = np.sum([a_z[j] * np.cos((j+1)*s) + b_z[j] * np.sin((j+1)*s) for j in range(len(a_z))], axis=0)
    return x, y, z

# === Biot–Savart Velocity ===
def compute_biot_savart_velocity(x, y, z, grid_points):
    N = len(x)
    velocity = np.zeros_like(grid_points)
    for i in range(N):
        r0 = np.array([x[i], y[i], z[i]])
        r1 = np.array([x[(i+1)%N], y[(i+1)%N], z[(i+1)%N]])
        dl = r1 - r0
        r_mid = 0.5 * (r0 + r1)
        R = grid_points - r_mid
        norm = np.linalg.norm(R, axis=1)**3 + 1e-12
        cross = np.cross(dl, R)
        velocity += cross / norm[:, np.newaxis]
    return velocity * (1 / (4 * np.pi))

# === Vorticity ===
def compute_vorticity_full_grid(velocity, shape, spacing):
    vx = velocity[:, 0].reshape(shape)
    vy = velocity[:, 1].reshape(shape)
    vz = velocity[:, 2].reshape(shape)
    curl_x = (np.roll(vz, -1, axis=1) - np.roll(vz, 1, axis=1))/(2*spacing) - (np.roll(vy, -1, axis=2) - np.roll(vy, 1, axis=2))/(2*spacing)
    curl_y = (np.roll(vx, -1, axis=2) - np.roll(vx, 1, axis=2))/(2*spacing) - (np.roll(vz, -1, axis=0) - np.roll(vz, 1, axis=0))/(2*spacing)
    curl_z = (np.roll(vy, -1, axis=0) - np.roll(vy, 1, axis=0))/(2*spacing) - (np.roll(vx, -1, axis=1) - np.roll(vx, 1, axis=1))/(2*spacing)
    return np.stack([curl_x, curl_y, curl_z], axis=-1).reshape(-1, 3)

# === Extract Inner Volume ===
def extract_interior_field(field, shape, interior):
    field_reshaped = field.reshape(*shape, 3)
    return field_reshaped[interior, interior, interior, :].reshape(-1, 3)

# === Core Parameters ===
grid_size = 32
spacing = 0.1
interior = slice(8, -8)
grid_range = spacing * (np.arange(grid_size) - grid_size // 2)
interior_vals = grid_range[interior]
X, Y, Z = np.meshgrid(grid_range, grid_range, grid_range, indexing='ij')
grid_points = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=-1)
Xf, Yf, Zf = np.meshgrid(interior_vals, interior_vals, interior_vals, indexing='ij')
r_sq = (Xf**2 + Yf**2 + Zf**2).ravel()
grid_shape = (grid_size, grid_size, grid_size)

# === Automatically Find All .fseries Files ===
knot_files = {
    os.path.splitext(fname)[0]: fname
    for fname in os.listdir(".")
    if fname.endswith(".fseries")
}

results = {}

for i, (label, file) in enumerate(knot_files.items(), 1):
    print(f"\n[{i}/{len(knot_files)}] Processing: {file}")
    a_x, b_x, a_y, b_y, a_z, b_z = load_fourier_series_clean(file)
    x, y, z = reconstruct_knot(a_x, b_x, a_y, b_y, a_z, b_z)
    velocity = compute_biot_savart_velocity(x, y, z, grid_points)
    vorticity = compute_vorticity_full_grid(velocity, grid_shape, spacing)
    v_sub = extract_interior_field(velocity, grid_shape, interior)
    w_sub = extract_interior_field(vorticity, grid_shape, interior)

    Nvox = w_sub.shape[0]  # number of interior voxels
    H_charge = np.sum(np.einsum('ij,ij->i', v_sub, w_sub)) / Nvox
    H_mass   = np.sum(np.linalg.norm(w_sub, axis=1)**2 * r_sq) / Nvox

    a_mu = 0.5 * (H_charge / H_mass - 1)
    results[label] = {"H_charge": H_charge, "H_mass": H_mass, "a_mu": a_mu}
    print(f"{label}:\n  H_charge = {H_charge:.6f}\n  H_mass = {H_mass:.6f}\n  H_ratio = {H_charge/H_mass:.6f} → a_mu^VAM = {a_mu:.8f}")



# === Print Results ===
for k, v in results.items():
    print(f"\n{k}:\n  H_charge = {v['H_charge']:.6f}\n  H_mass = {v['H_mass']:.6f}\n  a_mu^VAM = {v['a_mu']:.8f}")

# === Export summary (CSV + LaTeX) ============================================
import pandas as pd

rows = []
for label, v in results.items():
    R = v["H_charge"] / v["H_mass"]
    rows.append({
        "knot": label.replace("knot.", "").replace(".fseries", ""),
        "H_charge": v["H_charge"],
        "H_mass": v["H_mass"],
        "R = Hc/Hm": R,
        "a_mu^VAM": v["a_mu"]
    })

df = pd.DataFrame(rows).sort_values("a_mu^VAM")
df.to_csv("VAM_helicity_summary.csv", index=False)

# emit a compact LaTeX longtable (booktabs)
def to_longtable(df, fname="VAM_helicity_summary.tex", max_rows=40):
    cols = ["knot", "R = Hc/Hm", "a_mu^VAM"]
    sub = df.loc[:, cols].head(max_rows)
    lines = []
    lines.append(r"\begin{center}")
    lines.append(r"\begin{longtable}{lrr}")
    lines.append(r"\caption{VAM helicity summary for selected knots.}\\")
    lines.append(r"\toprule")
    lines.append(r"Knot & $R_K$ & $a_\mu^{\mathrm{VAM}}$ \\")
    lines.append(r"\midrule")
    lines.append(r"\endfirsthead")
    lines.append(r"\toprule")
    lines.append(r"Knot & $R_K$ & $a_\mu^{\mathrm{VAM}}$ \\")
    lines.append(r"\midrule")
    lines.append(r"\endhead")
    lines.append(r"\bottomrule")
    lines.append(r"\endfoot")
    for _, r in sub.iterrows():
        lines.append(f"{r['knot']} & {r['R = Hc/Hm']:.6f} & {r['a_mu^VAM']:.8f} \\\\")
    lines.append(r"\end{longtable}")
    lines.append(r"\end{center}")
    with open(fname, "w") as f:
        f.write("\n".join(lines))

to_longtable(df)
print("Wrote VAM_helicity_summary.csv and VAM_helicity_summary.tex")
