####################################################################################################
# 💡 VAM HELICITY EXPLANATION BLOCK
#
# This script evaluates helicity-based topological signatures of knots using their Fourier-mode
# representation in 3D space. These properties emerge from the Vortex Atom Model (VAM), which maps
# closed-loop knotted field lines to particle identities in the Standard Model.
#
# === 🔬 Physical Quantities Measured ===
#
# 1️⃣ H_charge: (Kinetic Helicity / Topological Twist)
# ----------------------------------------------------
#   H_charge = ∫ (v · ω) dV
#   - v     : Biot–Savart velocity field induced by the knot
#   - ω     : Vorticity field (curl of velocity)
#   - Measures the alignment and linking of vortex filaments
#   - Analogy: Electric current linked with magnetic field
#
# 2️⃣ H_mass: (Helical Mass / Twist Inertia)
# ------------------------------------------
#   H_mass = ∫ |ω|² · r² dV
#   - |ω|²  : Local intensity of vorticity
#   - r²    : Radial weighting (distance from origin)
#   - Measures spatial inertia of vorticity
#   - Analogy: Mass-like behavior of swirling fields
#
# 3️⃣ a_mu: (Anomalous Magnetic Moment under VAM)
# -----------------------------------------------
#   a_mu = 0.5 · (H_charge / H_mass - 1)
#   - Captures deviation from ideal coupling of v and ω
#   - Negative: distributed mass exceeds twist coupling
#   - Positive: compact twist dominates mass footprint
#   - Used as classifier for elementary particle identity
#
# === 🧬 Particle Classification Bands (a_mu ranges) ===
#   - Electron   : −0.520 ≤ a_mu ≤ −0.480     💠
#   - Muon       : −0.580 ≤ a_mu <  −0.520     🟡
#   - Tau        : −0.660 ≤ a_mu <  −0.580     🟣
#   - Neutrino   : −0.180 ≤ a_mu <  −0.100     🟢
#   - Up Quark   : −0.460 ≤ a_mu <  −0.420     🔵
#   - Down Quark : −0.419 ≤ a_mu <  −0.300     🔴
#   - Unknown/Exotic: Everything else          ❓
#
# === 📈 Visualization-Ready Outputs ===
#   - Biot–Savart velocity field on 3D grid
#   - Vorticity and radial-weighted distributions
#   - H_charge, H_mass, a_mu scalars per file
#   - Optional histogram and clustering for pattern mining
#
# === Example Workflow ===
#   1. Load .fseries coefficients (a_j, b_j) for each knot
#   2. Reconstruct the knot curve in 3D
#   3. Compute velocity field from Biot–Savart integration
#   4. Derive vorticity and compute helicities
#   5. Classify particle type using a_mu fingerprint
#
#   💡 A step toward mapping quantum matter to topological vortex geometry.
####################################################################################################

import os
import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored
import os
import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored
from bs4 import BeautifulSoup
import pandas as pd
import os

from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA

def cluster_amu_values(results, n_clusters=5):
    a_mu_vals = np.array([[r[1]] for r in results])
    model = GaussianMixture(n_components=n_clusters, random_state=42)
    labels = model.fit_predict(a_mu_vals)

    for i, (_, a_mu, label) in enumerate(results):
        results[i] += (labels[i],)  # append cluster ID

    return results, model

def plot_clustered_amu(results):
    import seaborn as sns
    sns.set(style="whitegrid")
    cluster_ids = [r[3] for r in results]
    a_mu_vals = [r[1] for r in results]

    plt.figure(figsize=(10, 5))
    sns.histplot(x=a_mu_vals, hue=cluster_ids, palette='tab10', bins=30, multiple='stack')
    plt.title("Clustering of $a_\\mu$ Values (GMM)")
    plt.xlabel("$a_\\mu$")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()
# --- Load and Parse Symmetry Table ---
def parse_symmetry_table(html_path):
    with open(html_path, 'r', encoding='iso-8859-1') as f:
        soup = BeautifulSoup(f, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')

    headers = ['Knot', 'D2(r)', 'D2k', 'Z2k', 'I', 'Reversible', 'Amphichiral', 'Periods', 'FSG']
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 9:
            knot = cols[0].get_text(strip=True).replace('\n', ' ')
            values = [col.get_text(strip=True) for col in cols[1:9]]
            data.append([knot] + values)
    return pd.DataFrame(data, columns=headers)

# --- Match Knot Symmetry Metadata ---
def extract_knot_code(filename):
    # assumes filename format like "knot.3_1.short.fseries" or "3_1.fseries"
    base = os.path.basename(filename)
    match = next((part for part in base.split('.') if '_' in part), '')
    return match.replace('_', '/')

def attach_symmetries(results, df_symmetries):
    for i, (fname, a_mu, label) in enumerate(results):
        knot_code = extract_knot_code(fname)
        match = df_symmetries[df_symmetries['Knot'].str.contains(knot_code)]
        if not match.empty:
            symm = match.iloc[0].to_dict()
            results[i] += (symm,)
        else:
            results[i] += ({'Knot': 'Unknown'},)
    return results



# --- Classification ---
PARTICLE_CLASSES = [
    ("Electron",         -0.520, -0.480, "cyan"),
    ("Muon",             -0.580, -0.521, "yellow"),
    ("Tau",              -0.660, -0.581, "magenta"),
    ("Neutrino",         -0.180, -0.100, "green"),
    ("Up Quark",         -0.460, -0.420, "blue"),
    ("Down Quark",       -0.419, -0.300, "red"),
    ("Unknown/Exotic",   float("-inf"), float("inf"), "grey"),
]

def classify_by_amu(a_mu):
    for label, lo, hi, color in PARTICLE_CLASSES:
        if lo <= a_mu <= hi:
            return label, color
    return "Unknown/Exotic", "white"

def load_fourier_series_clean(path):
    data = np.loadtxt(path)
    a_x, b_x, a_y, b_y, a_z, b_z = np.hsplit(data, 6)
    return a_x.flatten(), b_x.flatten(), a_y.flatten(), b_y.flatten(), a_z.flatten(), b_z.flatten()
# --- Fourier Series Loader ---
def load_fourier_series_clean(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip().startswith('%') or not line.strip():
                continue
            parts = line.split()
            if len(parts) == 6:
                data.append([float(p) for p in parts])
    return np.array(data).T

# --- Knot Reconstructor ---
def reconstruct_knot(a_x, b_x, a_y, b_y, a_z, b_z, N=1000):
    s = np.linspace(0, 2*np.pi, N)
    x = np.sum([a_x[j]*np.cos((j+1)*s) + b_x[j]*np.sin((j+1)*s) for j in range(len(a_x))], axis=0)
    y = np.sum([a_y[j]*np.cos((j+1)*s) + b_y[j]*np.sin((j+1)*s) for j in range(len(a_y))], axis=0)
    z = np.sum([a_z[j]*np.cos((j+1)*s) + b_z[j]*np.sin((j+1)*s) for j in range(len(a_z))], axis=0)
    return x, y, z

# --- Biot–Savart Velocity ---
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
        velocity += np.cross(dl, R) / norm[:, None]
    return velocity * (1 / (4 * np.pi))

# --- Vorticity Grid ---
def compute_vorticity_full_grid(velocity, shape, spacing):
    vx, vy, vz = velocity[:, 0].reshape(shape), velocity[:, 1].reshape(shape), velocity[:, 2].reshape(shape)
    curl_x = (np.roll(vz, -1, axis=1) - np.roll(vz, 1, axis=1))/(2*spacing) - (np.roll(vy, -1, axis=2) - np.roll(vy, 1, axis=2))/(2*spacing)
    curl_y = (np.roll(vx, -1, axis=2) - np.roll(vx, 1, axis=2))/(2*spacing) - (np.roll(vz, -1, axis=0) - np.roll(vz, 1, axis=0))/(2*spacing)
    curl_z = (np.roll(vy, -1, axis=0) - np.roll(vy, 1, axis=0))/(2*spacing) - (np.roll(vx, -1, axis=1) - np.roll(vx, 1, axis=1))/(2*spacing)
    return np.stack([curl_x, curl_y, curl_z], axis=-1).reshape(-1, 3)

def extract_interior_field(field, shape, interior):
    return field.reshape(*shape, 3)[interior, interior, interior, :].reshape(-1, 3)

# --- Analyzer Core ---
def analyze_all_fseries(path='.'):
    results = []

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

    for fname in sorted(f for f in os.listdir(path) if f.endswith('.fseries')):
        print(f"Processing {fname}...")
        try:
            a_x, b_x, a_y, b_y, a_z, b_z = load_fourier_series_clean(os.path.join(path, fname))
            x, y, z = reconstruct_knot(a_x, b_x, a_y, b_y, a_z, b_z)
            velocity = compute_biot_savart_velocity(x, y, z, grid_points)
            vorticity = compute_vorticity_full_grid(velocity, grid_shape, spacing)
            v_sub = extract_interior_field(velocity, grid_shape, interior)
            w_sub = extract_interior_field(vorticity, grid_shape, interior)

            H_charge = np.sum(np.einsum('ij,ij->i', v_sub, w_sub))
            H_mass = np.sum(np.linalg.norm(w_sub, axis=1)**2 * r_sq)
            a_mu = 0.5 * (H_charge / H_mass - 1)

            label, color = classify_by_amu(a_mu)

            print(colored(f"→ H_charge = {H_charge:.6f}, H_mass = {H_mass:.6f}, a_mu = {a_mu:.8f}", color))
            print(colored(f"→ Classified as: {label}", color))
            print()

            results.append((fname, a_mu, label))
        except Exception as e:
            print(colored(f"❌ Error processing {fname}: {e}", "red"))

    return results

# --- Histogram Plot ---
def plot_amu_histogram(results):
    a_mu_values = [r[1] for r in results]
    plt.figure(figsize=(10, 5))
    plt.hist(a_mu_values, bins=30, color='skyblue', edgecolor='k')
    plt.title("Distribution of $a_\\mu$ values across all .fseries knots")
    plt.xlabel("$a_\\mu$")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.show()





def compute_invariants(a_x, b_x, a_y, b_y, a_z, b_z):
    j = np.arange(1, len(a_x)+1)
    H_charge = np.sum(j * (a_x * b_x + a_y * b_y + a_z * b_z))
    H_mass = np.sum(j**2 * (a_x**2 + b_x**2 + a_y**2 + b_y**2 + a_z**2 + b_z**2))
    a_mu = 0.5 * (H_charge / H_mass - 1)
    return H_charge, H_mass, a_mu

def classify_vam_by_amu(a_mu):
    if abs(a_mu - (-0.5)) < 0.05:
        return "Lepton (Chiral, Invertible)", 'cyan'
    elif abs(a_mu) < 0.05:
        return "Dark Sector (Achiral)", 'yellow'
    elif a_mu < -0.55:
        return "Fully Chiral (Non-invertible)", 'magenta'
    elif a_mu > 0.15:
        return "Exotic Amphichiral (possibly neutral)", 'green'
    else:
        return "Ambiguous/Composite State", 'red'

def analyze_vam_knots(path='.'):
    results = []
    for fname in os.listdir(path):
        if fname.endswith('.fseries'):
            full_path = os.path.join(path, fname)
            a_x, b_x, a_y, b_y, a_z, b_z = load_fourier_series_clean(full_path)
            H_charge, H_mass, a_mu = compute_invariants(a_x, b_x, a_y, b_y, a_z, b_z)
            label, color = classify_vam_by_amu(a_mu)

            print(colored(f"{fname}", attrs=['bold']))
            print(colored(f"→ H_charge = {H_charge:.6f}, H_mass = {H_mass:.6f}, a_mu = {a_mu:.8f}", color))
            print(colored(f"→ VAM Classification: {label}", color))
            print()
            results.append((fname, a_mu, label))
    return results

def plot_amu_histogram(results):
    a_mu_values = [r[1] for r in results]
    plt.figure(figsize=(10, 5))
    plt.hist(a_mu_values, bins=30, color='skyblue', edgecolor='k')
    plt.title("Distribution of $a_\\mu$ values across all .fseries knots (VAM Model)")
    plt.xlabel("$a_\\mu$")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def classify_vam_by_amu(a_mu, fname):
    if '3_1' in fname:
        return "Electron (Lepton)", 'cyan'
    elif '4_1' in fname:
        return "Dark Sector / Photon", 'yellow'
    elif '6_2' in fname:
        return "Up Quark", 'blue'
    elif '7_4' in fname:
        return "Down Quark", 'red'
    elif abs(a_mu) < 0.05:
        return "Dark Sector (Achiral)", 'green'
    elif a_mu < -0.55:
        return "Chiral Lepton (Tau?)", 'magenta'
    else:
        return "Ambiguous/Exotic", 'grey'

def analyze_vam_knots(path='.', symmetry_html=None):
    results = []
    for fname in sorted(f for f in os.listdir(path) if f.endswith('.fseries')):
        full_path = os.path.join(path, fname)
        a_x, b_x, a_y, b_y, a_z, b_z = load_fourier_series_clean(full_path)
        H_charge, H_mass, a_mu = compute_invariants(a_x, b_x, a_y, b_y, a_z, b_z)
        label, color = classify_vam_by_amu(a_mu, fname)

        print(colored(f"{fname}", attrs=['bold']))
        print(colored(f"→ H_charge = {H_charge:.6f}, H_mass = {H_mass:.6f}, a_mu = {a_mu:.8f}", color))
        print(colored(f"→ VAM Classification: {label}", color))
        print()

        results.append((fname, a_mu, label))

    if symmetry_html:
        df_sym = parse_symmetry_table(symmetry_html)
        results = attach_symmetries(results, df_sym)
        for fname, a_mu, label, symm in results:
            print(f"{fname} → {label} ({a_mu:.6f})\nSymmetries: {symm}\n")

    return results

def plot_amu_histogram(results):
    a_mu_values = [r[1] for r in results]
    plt.figure(figsize=(10, 5))
    plt.hist(a_mu_values, bins=30, color='skyblue', edgecolor='k')
    plt.title("Distribution of $a_\\mu$ values across all .fseries knots (VAM Model)")
    plt.xlabel("$a_\\mu$")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# --- Runner ---
if __name__ == "__main__":
    all_results = analyze_all_fseries(".")
    plot_amu_histogram(all_results)
    # --- After computing all_results ---
    # Parse symmetry metadata table
    df_sym = parse_symmetry_table("list.html")  # replace with actual path

    all_results, model = cluster_amu_values(all_results, n_clusters=6)
    plot_amu_histogram(all_results)
    plot_clustered_amu(all_results)

    # Show one example from each cluster
    for cluster_id in sorted(set(r[3] for r in all_results)):
        example = next(r for r in all_results if r[3] == cluster_id)
        print(f"📎 Cluster {cluster_id} Example: {example[0]}, a_mu={example[1]:.5f}, label={example[2]}")

    # Attach symmetry info to each knot result
    all_results = attach_symmetries(all_results, df_sym)

    # You can now access symmetry info:
    for fname, a_mu, label, symm in all_results:
        print(f"{fname} → {label} ({a_mu:.6f})")
        print(f"Symmetries: {symm}")
        print()

    all_results = analyze_vam_knots('.', symmetry_html='list.html')
    plot_amu_histogram(all_results)
