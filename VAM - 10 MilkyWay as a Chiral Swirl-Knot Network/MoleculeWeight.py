import math
import numpy as np
import pandas as pd
import ace_tools_open as tools
from constants import a_0

# ─── Constants ────────────────────────────────────────────────────────────────
phi = (1 + math.sqrt(5)) / 2
alpha = 7.2973525643e-3
beta_default = 0.06
rho_core = 3.8934358266918687e18  # kg/m³
C_e = 1.09384563e6               # m/s
r_c = 1.40897017e-15            # m
c = 299792458                   # m/s
avogadro = 6.02214076e23        # mol⁻¹
F_max = 29.053507  # N
M_e = 9.1093837015e-31  # kg


# ─── Lord Kelvin ────────────────────────────────────────────────────────────────
# Mathematical expressions translated to Python functions
# 𝐾 = knot number (e.g. torus winding count or twist number),
# 𝑁 = number of vortex threads (vortex cores),
# 𝑎 = ring major radius (loop center offset),
# 𝑟 = ring tube radius (core radius),
# 𝜇 = rotational angular momentum,
# 𝐼 = impulse (linear or swirl momentum density × volume),
# 𝑍 rings = ring layers or stackings per unit length.
def tan_kelvin(I, N, mu, K, pi=math.pi):
    # tan(phi) = sqrt( I**1.5 / (N * mu * K**0.5 * pi**0.5) )
    return math.sqrt(I**(3/2) / (N * mu * K**0.5 * pi**0.5))

def tan_phi_kelvin(a, N, r):
    # tan(phi) = (2 * pi * a / N) * (1 / (2 * pi * r))
    return (2 * math.pi * a / N) * (1 / (2 * math.pi * r))

def I_impuls_ring(Z_rings, K, a):
    # I_impuls = Z_rings * K * pi * a**2
    return Z_rings * K * math.pi * a**2

def mu_rot_momentum(K, N, r, a):
    # mu_RotMomentum = K * N * pi * r**2 * a
    return K * N * math.pi * r**2 * a

def a_squared(I, K, pi=math.pi):
    # a^2 = I / (K * pi)
    return I / (K * pi)

def r_squared(mu, N, K, I, pi=math.pi):
    # r^2 = mu / (N * K * (1/2) * pi**(1/2) * I**(1/2))
    return mu / (N * K * 0.5 * pi**0.5 * I**0.5)

def tan_phi_formula_3(I, N, mu, K, Z_rings, pi=math.pi):
    # tan(phi) = sqrt( (1/Z_rings) * I**1.5 / (N * mu * K**0.5 * pi**0.5) )
    return math.sqrt((1/Z_rings) * I**(3/2) / (N * mu * K**0.5 * pi**0.5))
# ─── Lord Kelvin ────────────────────────────────────────────────────────────────


# Define function
def compute_orbital_radius(N, Z):
    return N * (F_max * r_c**2) / (M_e * Z * C_e**2)


# Volume per vortex-knot: V = 2π² R r² with R = R_x = N * (F_max * r_c**2) / (M_e * Z * C_e**2)
def compute_vortex_volume(R_x, r_c):
    return 2 * math.pi**2 * R_x * r_c**2



# ─── Core VAM mass models ────────────────────────────────────────────────────
def vam_mass_core(nucleons, electrons, beta=beta_default, kappa=1.0, m_threads = 1):
    Z = max(1, nucleons)  # atomic number approximation
    N = max(1, electrons)  # electron count

    # Orbital radius R_x
    R_x = N * (F_max * r_c**2) / (M_e * Z * C_e**2)

    # V_knot_dynamic = compute_vortex_volume(R_x, r_c)
    # total_knots = nucleons + electrons
    # V_tot = total_knots * V_knot_dynamic
    # energy_density = 0.5 * rho_core * C_e**2
    # E_base = energy_density * V_tot

    # Fixed core-based knot volume (restored)
    V_knot_fixed = 2 * math.pi**2 * (2 * r_c) * r_c**2
    total_knots = nucleons + electrons
    V_tot = total_knots * V_knot_fixed
    energy_density = 0.5 * rho_core * C_e**2
    E_base = energy_density * V_tot


    #### Correction factor for electron suppression
    # I = Z_rings * h * math.pi * a**2
    # tan_phi = sqrt( I**1.5 / (N * mu * K**0.5 * math.pi**0.5) )

    # tan_phi_fit ≈ (math.exp((x - 2) / 3) - 1) / 0.8
    # tan_phi_values = (a_0)/(total_knots * r_c *0.5)
    # vam_errors = 3 * np.log(0.8 * tan_phi_values + 1) + 2
    # ftan =vam_errors /100
    # correction_factor = 1/ (1 + ftan)
    # xi = correction_factor


    # Coherence Correction Factor ξ(n)
    xi = 1 + beta * math.log(max(1, nucleons))

    # Thread Suppression Factor η(m)
    eta = (1 / m_threads) ** 1.5

    # Coupling using R_x as d_ij
    if nucleons > 1:
        coupling_sum = (nucleons * (nucleons - 1) / 2) * math.exp(-R_x / r_c)
        E_couple = kappa * coupling_sum * energy_density * V_knot_fixed / nucleons # V_knot_fixed or V_knot_dynamic
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

fused_atoms_molecules = [
    ("H", 1, 0, 1, 1.00784), ("He", 2, 2, 2, 4.002602), ("Li", 3, 4, 3, 6.94), ("Be", 4, 5, 4, 9.0122), ("B", 5, 6, 5, 10.81), ("C", 6, 6, 6, 12.011), ("N", 7, 7, 7, 14.0067), ("O", 8, 8, 8, 15.999), ("F", 9, 10, 9, 18.998), ("Ne", 10, 10, 10, 20.18), ("Na", 11, 12, 11, 22.989769), ("Mg", 12, 12, 12, 24.305), ("Al", 13, 14, 13, 26.9815385), ("Si", 14, 14, 14, 28.085), ("P", 15, 16, 15, 30.973762), ("S", 16, 16, 16, 32.06), ("Cl", 17, 18, 17, 35.45), ("Ar", 18, 22, 18, 39.948), ("K", 19, 20, 19, 39.0983), ("Ca", 20, 20, 20, 40.078), ("Sc", 21, 24, 21, 44.955), ("Ti", 22, 26, 22, 47.867), ("V", 23, 28, 23, 50.942), ("Cr", 24, 28, 24, 51.996), ("Mn", 25, 30, 25, 54.938), ("Fe", 26, 30, 26, 55.845), ("Co", 27, 32, 27, 58.933), ("Ni", 28, 31, 28, 58.693), ("Cu", 29, 35, 29, 63.546), ("Zn", 30, 35, 30, 65.38), ("Ga", 31, 39, 31, 69.723), ("Ge", 32, 41, 32, 72.63), ("As", 33, 42, 33, 74.922), ("Se", 34, 45, 34, 78.971), ("Br", 35, 45, 35, 79.904), ("Kr", 36, 48, 36, 83.798), ("Rb", 37, 48, 37, 85.468), ("Sr", 38, 50, 38, 87.62), ("Y", 39, 50, 39, 88.906), ("Zr", 40, 51, 40, 91.224), ("Nb", 41, 52, 41, 92.906), ("Mo", 42, 54, 42, 95.95), ("Tc", 43, 55, 43, 98.0), ("Ru", 44, 57, 44, 101.07), ("Rh", 45, 58, 45, 102.91), ("Pd", 46, 60, 46, 106.42), ("Ag", 47, 61, 47, 107.87), ("Cd", 48, 64, 48, 112.41), ("In", 49, 66, 49, 114.82), ("Sn", 50, 69, 50, 118.71), ("Sb", 51, 71, 51, 121.76), ("Te", 52, 76, 52, 127.6), ("I", 53, 74, 53, 126.90447), ("Xe", 54, 77, 54, 131.29), ("Cs", 55, 78, 55, 132.91), ("Ba", 56, 81, 56, 137.33), ("La", 57, 82, 57, 138.91), ("Ce", 58, 82, 58, 140.12), ("Pr", 59, 82, 59, 140.91), ("Nd", 60, 84, 60, 144.24), ("Pm", 61, 84, 61, 145.0), ("Sm", 62, 88, 62, 150.36), ("Eu", 63, 89, 63, 151.96), ("Gd", 64, 93, 64, 157.25), ("Tb", 65, 94, 65, 158.93), ("Dy", 66, 97, 66, 162.5), ("Ho", 67, 98, 67, 164.93), ("Er", 68, 99, 68, 167.26), ("Tm", 69, 100, 69, 168.93), ("Yb", 70, 103, 70, 173.05), ("Lu", 71, 104, 71, 174.97), ("Hf", 72, 106, 72, 178.49), ("Ta", 73, 108, 73, 180.95), ("W", 74, 110, 74, 183.84), ("Re", 75, 111, 75, 186.21), ("Os", 76, 114, 76, 190.23), ("Ir", 77, 115, 77, 192.22), ("Pt", 78, 117, 78, 195.08), ("Au", 79, 118, 79, 196.97), ("Hg", 80, 121, 80, 200.59), ("Tl", 81, 123, 81, 204.38), ("Pb", 82, 125, 82, 207.2), ("H2O", 10, 8, 10, 18.015), ("CO2", 22, 22, 22, 44.01), ("O2", 16, 16, 16, 31.9988), ("N2", 14, 14, 14, 28.0134), ("CH4", 10, 10, 10, 16.04), ("C6H12O6", 72, 72, 72, 180.16), ("NH3", 10, 10, 10, 17.0305), ("HCl", 18, 18, 18, 36.46), ("C2H6", 18, 18, 18, 30.07), ("C2H4", 16, 16, 16, 28.05), ("C2H2", 14, 14, 14, 26.04), ("NaCl", 28, 28, 28, 58.44), ("C8H18", 98, 98, 98, 114.23), ("C6H6", 48, 48, 48, 78.11), ("CH3COOH", 32, 32, 32, 60.052), ("H2SO4", 50, 50, 50, 98.079), ("CaCO3", 50, 50, 50, 100.0869), ("C12H22O11", 176, 176, 176, 342.30), ("Caffeine", 194, 194, 194, 194.19), ("DNA Base (avg)", 10000, 10000, 10000, 6500.0)
]





actual_mass = {symbol: (gmol * 1e-3 / avogadro) for (symbol, _, _, _, gmol) in fused_atoms_molecules}

# ─── Compute and Display Results ──────────────────────────────────────────────
# 1. Common atoms + molecules
results = [vam_mass(symbol, p, n, e) for (symbol, p, n, e, _) in fused_atoms_molecules]

# 2. Compare to actual
rows = []
for name, m_vam in results:
    m_act = actual_mass.get(name)
    if m_act is None:
        continue
    diff = 100 * (m_vam - m_act) / m_act
    rows.append((name, m_vam, m_act, diff))


# Set pandas display options for full output
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 0)
pd.set_option("display.max_colwidth", None)


radii = [(name, compute_orbital_radius(N, Z)) for name, Z, _, N, _ in fused_atoms_molecules]
df_radii = pd.DataFrame(radii, columns=["Element", "R_x (m)"])
tools.display_dataframe_to_user(name="VAM Orbital Radius Estimates", dataframe=df_radii)

df = pd.DataFrame(rows, columns=["Name", "VAM Mass (kg)", "Actual Mass (kg)", "% Difference"])
tools.display_dataframe_to_user(name="VAM vs Actual Mass Table", dataframe=df)


