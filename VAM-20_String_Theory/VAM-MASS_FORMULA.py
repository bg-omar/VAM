import math
import pandas as pd

# ─── Constants ───────────────────────────────────────────────────────────────
phi = (1 + math.sqrt(5)) / 2
alpha = 7.2973525643e-3
rho_core = 3.8934358266918687e18
C_e = 1.09384563e6
r_c = 1.40897017e-15
c = 299_792_458
M_e = 9.1093837015e-31
avogadro = 6.02214076e23

# ─── Knot Volumes ────────────────────────────────────────────────────────────
V_torus = 2 * math.pi**2 * (2 * r_c) * r_c**2
V_u_topo = 2.8281
V_d_topo = 3.1639

# ─── Higgs/Topo Correction ───────────────────────────────────────────────────
def higgs_topo_factor(knot_complexity, twist=0, link=0, alpha_corr=0.02):
    return 1.0 + alpha_corr * (knot_complexity + twist + link)

# ─── VAM Mass Formula ────────────────────────────────────────────────────────
def vam_master_mass(n_knots, m_threads, s, V_list):
    """
    Mass = (4 / alpha) * eta * xi * tension * volume_sum * energy_density / c ** 2
    4/alpha: Electroweak amplification (dimensionless)
    eta: Thread suppression factor (dimensionless)
    xi: Coherence suppression (dimensionless)
    tension: Topological tension (dimensionless)
    volume_sum * energy_density: Total base energy (Joules)
    / c^2: Convert energy -> mass (via E=mc^2)
    """
    volume_sum = sum(V_list)
    eta = (1 / m_threads)**(3)
    xi = n_knots**(-1/phi)
    tension = 1 / phi**s
    energy_density = 0.5 * rho_core * C_e**2
    M = (4 / alpha) * eta * xi * tension * volume_sum * energy_density / c**2
    return M

# ─── Helicity Electron Mass ──────────────────────────────────────────────────
def vam_electron_mass_helicity(p=2, q=3):
    """ Calculate electron mass from helicity-based formula."""
    sqrt_term = math.sqrt(p**2 + q**2)
    m = 1
    n = 1
    s = 1
    eta = (1 / m) ** 1.5
    xi = n ** (-1 / phi)
    tension = 1 / phi ** s
    V_helical = 4 * math.pi ** 2 * r_c ** 3
    A = eta * xi * tension * V_helical
    factor = 8 * math.pi * rho_core * r_c**3 / C_e
    M_e_helicity = factor * (sqrt_term + A)
    return M_e_helicity

# ─── Atomic and Molecular Definitions ───────────────────────────
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

# ─── Emoji Marker ────────────────────────────────────────────────────────────
def emoji_marker(diff):
    d = abs(diff)
    if d < 1: icon = "🩷🡅"
    elif d < 2.5: icon = "🟢🡅"
    elif d < 10: icon = "🟡🡅"
    elif d < 25: icon = "🟠🡅"
    else: icon = "🔴🡅"
    if diff < 0: icon = icon.replace("🡅", "🡇")
    if diff == 0: icon = "●"
    return f"{diff:.2f}% {icon}"

# ─── Run All Calculations ────────────────────────────────────────────────────
if __name__ == "__main__":
    # 1. Calculate Elementary Particles' Masses
    M_e_pred_base = vam_electron_mass_helicity()
    e_corr = higgs_topo_factor(knot_complexity=3, twist=1)
    M_e_pred = M_e_pred_base * e_corr
    M_e_actual = M_e

    V_u_list = [V_u_topo * V_torus] * 2
    V_d_list = [V_d_topo * V_torus] * 1
    M_up = vam_master_mass(n_knots=2, m_threads=1, s=3, V_list=V_u_list)
    M_down = vam_master_mass(n_knots=1, m_threads=1, s=3, V_list=V_d_list)

    V_proton = [V_u_topo * V_torus] * 2 + [V_d_topo * V_torus] * 1
    M_proton_pred = vam_master_mass(n_knots=3, m_threads=1, s=3, V_list=V_proton)
    M_proton_actual = 1.67262192369e-27

    V_neutron = [V_u_topo * V_torus] * 1 + [V_d_topo * V_torus] * 2
    M_neutron_pred = vam_master_mass(n_knots=3, m_threads=1, s=3, V_list=V_neutron)
    M_neutron_actual = 1.67492749804e-27

    # 2. Add elementary particles to a DataFrame
    elem_rows = [
        ("Electron", M_e_pred, M_e_actual, emoji_marker(100 * (M_e_pred - M_e_actual) / M_e_actual)),
        ("Up quark", M_up, "—", "—"),
        ("Down quark", M_down, "—", "—"),
        ("Proton", M_proton_pred, M_proton_actual, emoji_marker(100 * (M_proton_pred - M_proton_actual) / M_proton_actual)),
        ("Neutron", M_neutron_pred, M_neutron_actual, emoji_marker(100 * (M_neutron_pred - M_neutron_actual) / M_neutron_actual)),
    ]
    df_elem = pd.DataFrame(elem_rows, columns=["Particle", "Predicted Mass (kg)", "Actual Mass (kg)", "% Error"])

    # 3. Predict Atomic and Molecular Masses based on elementary particle masses
    atom_rows = []
    for name, p, n, e, gmol in atoms_molecules:
        actual_kg = gmol * 1e-3 / avogadro
        predicted = p * M_proton_pred + n * M_neutron_pred + e * M_e_pred
        rel_error = 100 * (predicted - actual_kg) / actual_kg
        atom_rows.append((name, predicted, actual_kg, emoji_marker(rel_error)))

    df_atoms = pd.DataFrame(atom_rows, columns=["Particle", "Predicted Mass (kg)", "Actual Mass (kg)", "% Error"])

    # 4. Combine and Display
    df_final = pd.concat([df_elem, df_atoms], ignore_index=True)
    pd.set_option("display.float_format", lambda x: f"{x:.4e}" if isinstance(x, float) else str(x))

    print(df_final.to_string(index=False))

    # 5. Save to CSV
    df_final.to_csv("VAM_Mass_Results.csv", index=False)