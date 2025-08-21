# vam_masses_topology.py

# ─── Imports ─────────────────────────────────────────────────────
import math, numpy as np, pandas as pd
import ace_tools_open as tools

# ─── Constants ───────────────────────────────────────────────────
phi = (1 + math.sqrt(5)) / 2
alpha = 7.2973525643e-3
rho_core = 3.8934358266918687e18
C_e = 1.09384563e6
r_c = 1.40897017e-15
c = 299792458
avogadro = 6.02214076e23
F_max = 29.053507
M_e = 9.1093837015e-31
a_0 = 5.29177210903e-11
beta_default = 0.06

# ─── Atomic and Molecular Definitions ───────────────────────────
# Format: (Symbol, protons, neutrons, electrons, atomic mass in g/mol)
atoms_molecules = [
    ("H", 1, 0, 1, 1.00784), ("He", 2, 2, 2, 4.002602), ("Li", 3, 4, 3, 6.94), ("Be", 4, 5, 4, 9.0122),
    ("B", 5, 6, 5, 10.81), ("C", 6, 6, 6, 12.011), ("N", 7, 7, 7, 14.0067), ("O", 8, 8, 8, 15.999),
    ("F", 9, 10, 9, 18.998), ("Ne", 10, 10, 10, 20.18), ("Na", 11, 12, 11, 22.989769), ("Mg", 12, 12, 12, 24.305),
    ("Al", 13, 14, 13, 26.9815385), ("Si", 14, 14, 14, 28.085), ("P", 15, 16, 15, 30.973762), ("S", 16, 16, 16, 32.06),
    ("Cl", 17, 18, 17, 35.45), ("Ar", 18, 22, 18, 39.948), ("K", 19, 20, 19, 39.0983), ("Ca", 20, 20, 20, 40.078),
    ("Sc", 21, 24, 21, 44.955), ("Ti", 22, 26, 22, 47.867), ("V", 23, 28, 23, 50.942), ("Cr", 24, 28, 24, 51.996),
    ("Mn", 25, 30, 25, 54.938), ("Fe", 26, 30, 26, 55.845), ("Co", 27, 32, 27, 58.933), ("Ni", 28, 31, 28, 58.693),
    ("Cu", 29, 35, 29, 63.546), ("Zn", 30, 35, 30, 65.38), ("Ga", 31, 39, 31, 69.723), ("Ge", 32, 41, 32, 72.63),
    ("As", 33, 42, 33, 74.922), ("Se", 34, 45, 34, 78.971), ("Br", 35, 45, 35, 79.904), ("Kr", 36, 48, 36, 83.798),
    ("Rb", 37, 48, 37, 85.468), ("Sr", 38, 50, 38, 87.62), ("Y", 39, 50, 39, 88.906), ("Zr", 40, 51, 40, 91.224),
    ("Nb", 41, 52, 41, 92.906), ("Mo", 42, 54, 42, 95.95), ("Tc", 43, 55, 43, 98.0), ("Ru", 44, 57, 44, 101.07),
    ("Rh", 45, 58, 45, 102.91), ("Pd", 46, 60, 46, 106.42), ("Ag", 47, 61, 47, 107.87), ("Cd", 48, 64, 48, 112.41),
    ("In", 49, 66, 49, 114.82), ("Sn", 50, 69, 50, 118.71), ("Sb", 51, 71, 51, 121.76), ("Te", 52, 76, 52, 127.6),
    ("I", 53, 74, 53, 126.90447), ("Xe", 54, 77, 54, 131.29), ("Cs", 55, 78, 55, 132.91), ("Ba", 56, 81, 56, 137.33),
    ("La", 57, 82, 57, 138.91), ("Ce", 58, 82, 58, 140.12), ("Pr", 59, 82, 59, 140.91), ("Nd", 60, 84, 60, 144.24),
    ("Pm", 61, 84, 61, 145.0), ("Sm", 62, 88, 62, 150.36), ("Eu", 63, 89, 63, 151.96), ("Gd", 64, 93, 64, 157.25),
    ("Tb", 65, 94, 65, 158.93), ("Dy", 66, 97, 66, 162.5), ("Ho", 67, 98, 67, 164.93), ("Er", 68, 99, 68, 167.26),
    ("Tm", 69, 100, 69, 168.93), ("Yb", 70, 103, 70, 173.05), ("Lu", 71, 104, 71, 174.97), ("Hf", 72, 106, 72, 178.49),
    ("Ta", 73, 108, 73, 180.95), ("W", 74, 110, 74, 183.84), ("Re", 75, 111, 75, 186.21), ("Os", 76, 114, 76, 190.23),
    ("Ir", 77, 115, 77, 192.22), ("Pt", 78, 117, 78, 195.08), ("Au", 79, 118, 79, 196.97), ("Hg", 80, 121, 80, 200.59),
    ("Tl", 81, 123, 81, 204.38), ("Pb", 82, 125, 82, 207.2), ("Bi", 83, 126, 83, 208.98), ("Po", 84, 125, 84, 209.0),
    ("At", 85, 125, 85, 210.0), ("Rn", 86, 136, 86, 222.0), ("Fr", 87, 136, 87, 223.0), ("Ra", 88, 138, 88, 226.0),
    ("Ac", 89, 138, 89, 227.0), ("Th", 90, 142, 90, 232.04), ("Pa", 91, 140, 91, 231.04), ("U", 92, 146, 92, 238.03),
    ("H2O", 10, 8, 10, 18.015), ("CO2", 22, 22, 22, 44.01), ("O2", 16, 16, 16, 31.9988), ("N2", 14, 14, 14, 28.0134),
    ("CH4", 10, 10, 10, 16.04), ("C6H12O6", 72, 72, 72, 180.16), ("NH3", 10, 10, 10, 17.0305), ("HCl", 18, 18, 18, 36.46),
    ("C2H6", 18, 18, 18, 30.07), ("C2H4", 16, 16, 16, 28.05), ("C2H2", 14, 14, 14, 26.04), ("NaCl", 28, 28, 28, 58.44),
    ("C8H18", 98, 98, 98, 114.23), ("C6H6", 48, 48, 48, 78.11), ("CH3COOH", 32, 32, 32, 60.052), ("H2SO4", 50, 50, 50, 98.079),
    ("CaCO3", 50, 50, 50, 100.0869), ("C12H22O11", 176, 176, 176, 342.30),
    ("Caffeine", 194, 194, 194, 194.19), ("DNA (avg)", 10000, 10000, 10000, 6500.0)
]


# ─── Knot Topology Definitions ──────────────────────────────────
knot_data = [
    ("3_1", 0.0,       True, 3), ("4_1", 2.02988321, False, 4), ("5_2", 2.8281220, True, 5),
    ("6_1", 3.1639632, True, 6), ("6_2", 2.8281220, True, 6), ("6_3", 3.1639632, True, 6),
    ("7_2", 3.1639632, True, 7), ("7_3", 3.4657359, True, 7), ("7_4", 3.1639632, True, 7),
    ("7_5", 3.6638624, True, 7), ("7_6", 3.6638624, True, 7), ("7_7", 3.4657359, True, 7),
    ("8_2", 3.6638624, True, 8), ("8_3", 3.4657359, True, 8), ("8_5", 3.6638624, True, 8),
    ("8_6", 4.0597658, True, 8), ("8_7", 4.0597658, True, 8), ("8_8", 3.6638624, True, 8),
    ("8_9", 3.4657359, True, 8), ("8_10", 3.6638624, True, 8),
]
df_knots = pd.DataFrame(knot_data, columns=["Knot", "Volume", "Chiral", "Crossings"])

# Define column names and create DataFrame
df = pd.DataFrame(knot_data, columns=["Knot", "Volume", "Chiral", "Crossings"])

# Filter chiral hyperbolic knots (Volume > 0) and sort by volume
chiral_hyperbolic_knots = df[(df["Volume"] > 0)].sort_values(by="Volume")

# Display the filtered DataFrame
tools.display_dataframe_to_user(name="Chiral Hyperbolic Knots with Topological Volume", dataframe=chiral_hyperbolic_knots)

# ─── Utility Functions ──────────────────────────────────────────
# Orbital radius per electron in atom
def compute_orbital_radius(N, Z):
    return N * (F_max * r_c**2) / (M_e * Z * C_e**2)

def compute_vortex_volume(R_x, R_core):
    """  Volume of a toroidal vortex knot shell: """
    """ V = 2π² R r² with R = R_x = N * (F_max * r_c**2) / (M_e * Z * C_e**2) """
    return 2 * math.pi**2 * R_x * R_core**2

# ─── VAM Core Models ────────────────────────────────────────────
# Master VAM Mass Formula:
# Mass = (4 / alpha) * eta * xi * tension * volume_sum * energy_density / c ** 2
# 4/alpha: Electroweak amplification (dimensionless)
# eta: Thread suppression factor (dimensionless)
# xi: Coherence suppression (dimensionless)
# tension: Topological tension (dimensionless)
# volume_sum * energy_density: Total base energy (Joules)
# / c^2: Convert energy → mass (via E=mc^2)
def vam_master_mass(n_knots, m_threads, s, V_list):
    volume_sum = sum(V_list)
    eta = (1 / m_threads)**(3/1)
    xi = n_knots**(-1/phi)
    tension = 1 / phi**s
    energy_density = 0.5 * rho_core * C_e**2
    M = (4 / alpha) * eta * xi * tension * volume_sum * energy_density / c**2
    return M

# Master Helicity-Based Electron Mass
def vam_electron_mass_helicity(p=2, q=3):
    """ Calculate electron mass from helicity-based formula."""
    """ Mass from topological helicity vector (used for e⁻, ν, etc.) """
    sqrt_term = math.sqrt(p**2 + q**2)
    m, n, s = 1, 1, 1

    """ Derived suppression factor to replace γpq (γ=beta empirical) """
    eta = (1 / m) ** 1.5
    xi = n ** (-1 / phi)
    tension = 1 / phi ** s
    V_torus = 4 * math.pi ** 2 * r_c ** 3
    A = eta * xi * tension * V_torus
    factor = 8 * math.pi * rho_core * r_c**3 / C_e
    return factor * (sqrt_term + A)

# Additional vam_mass_core, vam_mass_fast, vam_mass_integral definitions follow...
# Proton/neutron examples, DataFrame generation, display logic...
# ─── Core VAM mass models ────────────────────────────────────────────────────
def vam_mass_core(nucleons, electrons, beta=beta_default, kappa=1.0, m_threads = 1, eq=2):
    """ Computes mass of atom based on nucleon count, vortex volume, suppression model """
    Z = max(1, nucleons)  # atomic number approximation
    N = max(1, electrons)  # electron count

    # Orbital shell radius
    R_x = compute_orbital_radius(N, Z)

    # Canonical vortex knot volume (scaling with core size)
    V_knot = 2 * math.pi**2 * (2 * r_c) * r_c**2
    total_knots = nucleons + electrons
    V_tot = total_knots * V_knot

    # Energy density in core swirl
    energy_density = 0.5 * rho_core * C_e**2

    eta = 1
    """"
    # eq modes:
    # 0 → empirical log(n) suppression (with beta)
    # 1 → enhanced swirl suppression (power-law fit)
    # 2 → tan(φ)-based swirl suppression
    # 3 → pure first-principles golden suppression (preferred)
    # 4 → dynamic R_x volume model (without suppression)
    """
    if eq == 0: # 0 → empirical log(n) suppression (with beta = 0.06)
        eta = (1 / m_threads) ** 1.5
        # Coherence Correction Factor ξ(n)
        xi = 1 + beta * math.log(max(1, nucleons))

    if eq == 1: # 1 → enhanced swirl suppression (power-law fit)
        tan_phi_values = a_0 / (total_knots * r_c * 0.5)
        vam_errors = 3 * np.log(0.8 * tan_phi_values + 1) + 2
        ftan = vam_errors / 100
        xi = 1 / (1 + ftan ** 2.5)  # Enhanced suppression

    if eq == 2: # 2 → tan(φ)-based swirl suppression
        # Coherence Correction Factor ξ(n)
        tan_phi_values = (a_0)/(total_knots * r_c *0.5)
        vam_errors = 3 * np.log(0.8 * tan_phi_values + 1) + 2
        ftan =vam_errors /100
        correction_factor = 1/ (1 + ftan)
        xi = correction_factor

    if eq == 3: # 3 → pure first-principles golden suppression (preferred)
        # Pure first-principles coherence suppression
        phi_local = (1 + math.sqrt(5)) / 2
        xi = total_knots ** (-1 / phi_local)

    if eq == 4: # 4 → dynamic R_x volume model (without suppression)
        V_knot_dynamic = compute_vortex_volume(R_x, r_c)
        V_tot = total_knots * V_knot_dynamic
        xi = 1


    E_base = energy_density * V_tot

    # Coupling using R_x as d_ij
    if nucleons > 1:
        coupling_sum = (nucleons * (nucleons - 1) / 2) * math.exp(-R_x / r_c)
        E_couple = kappa * coupling_sum * energy_density * V_knot / nucleons # V_knot_fixed or V_knot_dynamic
    else:
        E_couple = 0.0

    # Amplification
    amplification = (1 / phi) * (4 / alpha) * xi * eta
    M_vam = amplification * (E_base + E_couple) / c**2
    return M_vam

# ─── VAM Mass Function ───────────────────────────────────────────────────────

def vam_mass(name, p, n, e, **kwargs):
    M = vam_mass_core(nucleons=p + n, electrons=e, **kwargs)
    return name, M

def vam_mass_fast(name, p, n, e, beta=beta_default, kappa=1.0):
    nucleons = p + n
    total_knots = nucleons + e
    V_knot = 4 * math.pi**2 * r_c**3
    ed = 0.5 * rho_core * C_e**2
    E_base = ed * total_knots * V_knot
    xi = 1 + beta * math.log(max(1, nucleons))
    coupling = nucleons*(nucleons-1)/2 * math.exp(-2)
    E_coup = kappa * coupling * ed * V_knot / max(1, nucleons)
    amplification = (1/phi)*(4/alpha)*xi
    M = amplification * (E_base + E_coup) / c**2
    return M


# ─── Vortex-Averaged Mass Integral ──────────────────────────────────────────────

def vam_mass_integral(vortices, phi=phi, alpha=alpha, beta=beta_default, kappa_ij=1.0, r_c=r_c):
    """
    vortices: list of dicts, each with keys:
      - 'volume': V_k (m^3)
      - 'rho': density (kg/m^3)
      - 'omega_sq_mean': <|ω|^2> average over V_k (rad^2/s^2)
      - 'helicity': H(K_k)
      - 'torsion': T(K_k)
      - 'position': 3D numpy array for center
    """
    n = len(vortices)
    xi = 1 + beta * math.log(max(1, n))
    prefactor = (1/phi) * (4/alpha) * xi

    M_sum = 0.0
    for vk in vortices:
        V_k = vk['volume']
        rho = vk['rho']
        omega2 = vk['omega_sq_mean']
        E_kin = 0.5 * rho * omega2 * V_k

        E_coup = 0.0
        if vk.get('position') is not None:
            omega_k = math.sqrt(omega2)
            for vj in vortices:
                if vj is vk:
                    continue
                d = np.linalg.norm(vk['position'] - vj['position'])
                omega_j = math.sqrt(vj['omega_sq_mean'])
                E_coup += kappa_ij * omega_k * omega_j * math.exp(-d / r_c)

        # apply prefactor *before* division by c²
        M_sum += E_kin + vk.get('helicity', 0.0) + vk.get('torsion', 0.0) + E_coup

    M_kg = prefactor * M_sum / c**2
    return M_kg


actual_mass = {symbol: (gmol * 1e-3 / avogadro) for (symbol, _, _, _, gmol) in atoms_molecules}

def emoji_marker(diff):
    d = abs(diff)
    if d < 1: icon = "🩷🡅"
    elif d < 2.5: icon = "🟢🡅"
    elif d < 10: icon = "🟡🡅"
    elif d < 25: icon = "🟠🡅"
    else: icon = "🔴🡅"
    if diff < 0: icon = icon.replace("🡅","🡇")
    if diff == 0: icon = "●"
    return f"{diff:.2f}% {icon}"


# --- Prepare DataFrame rows ---
rows = []
for name, p, n, e, gmol in atoms_molecules:
    m_act = gmol * 1e-3 / avogadro

    # Create proton and neutron examples
    V_torus = 2 * math.pi ** 2 * (2 * r_c) * r_c ** 2
    V_u_topo = 2.8281  # knot 6_2
    V_d_topo = 3.1639  # knot 7_4

    # Proton: uud → 2x6_2 + 1x7_4
    V_proton = [V_u_topo * V_torus, V_u_topo * V_torus, V_d_topo * V_torus]
    M_proton = vam_master_mass(n_knots=3, m_threads=1, s=3, V_list=V_proton)

    # Neutron: udd → 1x6_2 + 2x7_4
    V_neutron = [V_u_topo * V_torus, V_d_topo * V_torus, V_d_topo * V_torus]
    M_neutron = vam_master_mass(n_knots=3, m_threads=1, s=3, V_list=V_neutron)

    # Actual masses
    M_proton_actual = 1.67262192369e-27
    M_neutron_actual = 1.67492749804e-27

    # Compare
    rel_proton = 100 * (M_proton - M_proton_actual) / M_proton_actual
    rel_neutron = 100 * (M_neutron - M_neutron_actual) / M_neutron_actual
    rel_electron = 100 * (vam_electron_mass_helicity() - M_e) / M_e
    # Master VAM (Knot-based) model
    nucleons = p + n
    quark_knots = nucleons * 3  # Approx 3 quark-knots per nucleon
    V_list = [V_u_topo * V_torus] * (2 * nucleons) + [V_d_topo * V_torus] * (1 * nucleons)  # 2U + 1D per nucleon

    m_master = (p * M_proton) + (n * M_neutron) + (e * vam_electron_mass_helicity())
    diff_master = 100 * (m_master - m_act) / m_act


    basic_masses = [vam_mass_core(p+n, e, eq=eq) for eq in (0,1,2,3,4)]
    # Coupled model
    _, m_vam = vam_mass(name, p, n, e)
    diff_vam = 100 * (m_vam - m_act) / m_act

    diff_basic = [100 * (m - m_act) / m_act for m in basic_masses]

    rows.append((name, *basic_masses, m_master, m_act, *diff_basic, diff_vam, diff_master))

# --- Create DataFrame ---
columns = (["Name"] +
           [f"VAM Mass {eq}" for eq in (0,1,2,3,4)] +
           ["VAM Master", "Actual Mass (kg)"] +
           [f"% Diff {eq}" for eq in (0,1,2,3,4)] +
           ["% Diff", "% Diff Master"])

df = pd.DataFrame(rows, columns=columns)

# --- Add orbital radius ---
df["R_x (m)"] = [compute_orbital_radius(n, p+n) for name, p, n, e, _ in atoms_molecules]

def mark_diff_with_dot(diff):
    abs_diff = abs(diff)

    if abs_diff < 1:
        dot, arrow  = "🩷"  , "🡅"
    elif abs_diff < 2.5:
        dot, arrow  = "🟢", "🡅"
    elif abs_diff < 10:
        dot, arrow  = "🟡", "🡅"
    elif abs_diff < 25:
        dot, arrow  = "🟠", "🡅"
    else:
        dot, arrow  = "🔴", "🡅"
    if diff < 0:
        arrow = "🡇"  # Flip direction for underestimation
    if diff == 0:
        arrow = "●"  # Neutral

    return f"{diff:.2f}% {dot}{arrow}"


# Format the % Diff columns with emojis
for eq in (0,1,2,3,4):
    df[f"% Diff {eq}"] = df[f"% Diff {eq}"].apply(mark_diff_with_dot)
df["% Diff"] = df["% Diff"].apply(mark_diff_with_dot)
df["% Diff Master"] = df["% Diff Master"].apply(mark_diff_with_dot)
# --- Reorder columns ---
df = df[[
    "Name",
    "Actual Mass (kg)", "VAM Master", "% Diff Master",
    "% Diff 0",  "% Diff", "% Diff 1", "% Diff 2", "% Diff 3", "% Diff 4",
    "VAM Mass 0", "VAM Mass 1", "VAM Mass 2", "VAM Mass 3", "VAM Mass 4",
    "R_x (m)"
]]

df.index = df.index + 1

# --- Display final DataFrame ---
# Set pandas display options for full output
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 0)
pd.set_option("display.max_colwidth", None)
tools.display_dataframe_to_user(
    name="VAM Mass % Differences (With Accuracy Dots)",
    dataframe=df
)


# Create proton and neutron examples
V_torus = 2 * math.pi**2 * (2 * r_c) * r_c**2
V_u_topo = 2.8281  # knot 6_2
V_d_topo = 3.1639  # knot 7_4

# Proton: uud → 2x6_2 + 1x7_4
V_proton = [V_u_topo * V_torus, V_u_topo * V_torus, V_d_topo * V_torus]
M_proton = vam_master_mass(n_knots=3, m_threads=1, s=3, V_list=V_proton)

# Neutron: udd → 1x6_2 + 2x7_4
V_neutron = [V_u_topo * V_torus, V_d_topo * V_torus, V_d_topo * V_torus]
M_neutron = vam_master_mass(n_knots=3, m_threads=1, s=3, V_list=V_neutron)

# Actual masses
M_proton_actual = 1.67262192369e-27
M_neutron_actual = 1.67492749804e-27

# Compare
rel_proton = 100 * (M_proton - M_proton_actual) / M_proton_actual
rel_neutron = 100 * (M_neutron - M_neutron_actual) / M_neutron_actual

# Use canonical formula for proton and neutron, helicity-based for electron
M_e_helicity = vam_electron_mass_helicity()
rel_error_helicity = 100 * (M_e_helicity - M_e) / M_e

# Replace electron row with corrected value
df_updated = pd.DataFrame({
    "Particle": ["Proton", "Neutron", "Electron (helicity)"],
    "VAM Mass (kg)": [M_proton, M_neutron, M_e_helicity],
    "Actual Mass (kg)": [M_proton_actual, M_neutron_actual, M_e],
    "% Error": [rel_proton, rel_neutron, rel_error_helicity]
})

tools.display_dataframe_to_user(name="VAM Masses with Electron Helicity Correction", dataframe=df_updated)


