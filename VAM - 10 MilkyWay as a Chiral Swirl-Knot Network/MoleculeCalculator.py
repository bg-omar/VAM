import math
import ace_tools_open as tools
import pandas as pd

from constants import a_0

# Set pandas display options for full output
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 0)
pd.set_option("display.max_colwidth", None)

# Re-import and define constants
rho_core = 3.8934358266918687e+18  # Core æther density [kg/m^3]
r_c = 1.40897017e-15               # Vortex core radius [m]
C_e = 1093845.63                   # Vortex tangential velocity [m/s]
alpha = 7.2973525643e-3            # Fine-structure constant
c = 299792458                     # Speed of light [m/s]
avogadro = 6.02214076e23          # Avogadro's number

# Derived constants
alpha_vam = 4 / alpha

# Volume of a toroidal knot: V = 2π² R r², with R = 2 * r_c
R = 2 * r_c
V_knot = 2 * math.pi**2 * R * r_c**2

# CO2: 66 total knots (12 C nucleons + 32 O nucleons + 22 electrons)
total_knots = 66
V_total = total_knots * V_knot

# Energy density: (1/2) * ρ * C_e^2
energy_density = 0.5 * rho_core * C_e**2
E_total = energy_density * V_total

# Mass from E = mc² and VAM scaling
M_CO2_estimate = alpha_vam * E_total / c**2  # [kg]

# Actual CO₂ molecular mass
M_CO2_actual = 44.01e-3 / avogadro  # [kg]

# Relative error
relative_error = M_CO2_estimate / M_CO2_actual

print("M_CO2_estimate: ",M_CO2_estimate, "M_CO2_actual: ", M_CO2_actual, "relative_error: ", relative_error)

# VAM scaling factor
alpha_vam = 4 / alpha

# Volume per torus knot: V = 2π² R r², with R = 2 * r_c
R = 2 * r_c
V_knot = 2 * math.pi**2 * R * r_c**2

# Oxygen atom: 8 protons + 8 neutrons + 8 electrons = 24 vortex structures
total_knots_O = 24
V_total_O = total_knots_O * V_knot

# Energy density: (1/2) * ρ * C_e^2
energy_density = 0.5 * rho_core * C_e**2
E_total_O = energy_density * V_total_O

# VAM-based mass for one oxygen atom
M_O_estimate = alpha_vam * E_total_O / c**2  # [kg]

# Actual atomic mass of oxygen-16: 15.999 g/mol → convert to kg
M_O_actual = 15.999e-3 / avogadro  # [kg]

# Relative error
relative_error_O = M_O_estimate / M_O_actual

print("M_O_estimate: ",M_O_estimate, "M_O_actual: ", M_O_actual, "relative_error: ", relative_error_O)


# List of elements/molecules with number of nucleons and electrons
# Format: name, num_protons, num_neutrons, num_electrons
# Define top 20 commonly used atoms with approximate (Z, N, electrons)
common_atoms = [
    ("H", 1, 0, 1), ("He", 2, 2, 2), ("C", 6, 6, 6), ("N", 7, 7, 7), ("O", 8, 8, 8),
    ("Na", 11, 12, 11), ("Mg", 12, 12, 12), ("Al", 13, 14, 13), ("Si", 14, 14, 14),
    ("P", 15, 16, 15), ("S", 16, 16, 16), ("Cl", 17, 18, 17), ("K", 19, 20, 19),
    ("Ca", 20, 20, 20), ("Fe", 26, 30, 26), ("Cu", 29, 35, 29), ("Zn", 30, 35, 30),
    ("Br", 35, 45, 35), ("I", 53, 74, 53), ("Pb", 82, 125, 82)
]

# Common molecules with approximate total nucleons and electrons
  # for CO2 = C: 6p6n, O2: 16p16n, + 2e for neutrality
common_molecules = [
    ("H2O", 10, 8, 10), ("CO2", 22, 22, 22), ("O2", 16, 16, 16), ("N2", 14, 14, 14),
    ("CH4", 10, 10, 10), ("C6H12O6", 72, 72, 72), ("NH3", 10, 10, 10), ("HCl", 18, 18, 18),
    ("C2H6", 18, 18, 18), ("C2H4", 16, 16, 16), ("C2H2", 14, 14, 14), ("NaCl", 28, 28, 28),
    ("C8H18", 98, 98, 98), ("C6H6", 48, 48, 48), ("CH3COOH", 32, 32, 32), ("H2SO4", 50, 50, 50),
    ("CaCO3", 50, 50, 50), ("C12H22O11", 176, 176, 176), ("Caffeine", 194, 194, 194),
    ("DNA Base (avg)", 10000, 10000, 10000)  # Approximation for a short base pair
]

# Actual atomic/molecular masses in g/mol from standard sources (converted to kg/molecule)
# Actual masses for reference in g/mol (for both atoms and molecules)
actual_masses_gmol = {

    "H2O": 18.015, "CO2": 44.01, "O2": 31.9988, "N2": 28.0134, "CH4": 16.04,
    "C6H12O6": 180.16, "NH3": 17.0305, "HCl": 36.46, "C2H6": 30.07, "C2H4": 28.05,
    "C2H2": 26.04, "NaCl": 58.44, "C8H18": 114.23, "C6H6": 78.11, "CH3COOH": 60.052,
    "H2SO4": 98.079, "CaCO3": 100.0869, "C12H22O11": 342.30, "Caffeine": 194.19,
    "DNA Base (avg)": 6500.0  # very rough average base pair molar mass
}
def vam_mass_og(name, protons, neutrons, electrons, beta=0.06):
    total_knots = protons + neutrons + electrons
    V_knot = 2 * math.pi**2 * (2 * r_c) * r_c**2
    V_total = total_knots * V_knot
    energy_density = 0.5 * rho_core * C_e**2
    E_total = energy_density * V_total  # in Joules

    # Apply suppression BEFORE dividing by c^2
    knot_cores = protons + neutrons  # only mass-contributing cores
    xi = 1 + beta * math.log(knot_cores)

    # Amplification
    amplification = (1 / ((1 + math.sqrt(5)) / 2)) * (4 / alpha) * xi
    M_vam = amplification * E_total / c**2  # final mass in kg

    return name, M_vam


# Process all atoms and molecules
atom_results = [vam_mass_og(name, Z, N, e) for name, Z, N, e in common_atoms]
molecule_results = [vam_mass_og(name, Z, N, e) for name, Z, N, e in common_molecules]

# Compute VAM vs actual
vam_results_og = []
for name, p, n, e in common_atoms:
    vam_kg = vam_mass_og(name, p, n, e)
    actual_kg = actual_masses_gmol[name] * 1e-3 / avogadro
    rel_error = 100 *(( vam_kg[1] - actual_kg)/ actual_kg)
    vam_results_og.append((name, vam_kg, actual_kg, rel_error))

# Convert to DataFrames
df = pd.DataFrame(vam_results_og, columns=["Element", "VAM Mass (kg)", "Actual Mass (kg)", "Ratio (VAM/Actual)"])
tools.display_dataframe_to_user(name="VAM vs Actual Mass Table", dataframe=df)
df_atoms = pd.DataFrame(atom_results, columns=["Atom", "VAM Mass (kg)"])
df_molecules = pd.DataFrame(molecule_results, columns=["Molecule", "VAM Mass (kg)"])

# Combine atoms and molecules
combined = df_atoms._append(df_molecules, ignore_index=True)
combined["Name"] = combined["Atom"].combine_first(combined["Molecule"])
combined.drop(columns=["Atom", "Molecule"], inplace=True)

# Add actual mass and compute difference
combined["Actual Mass (kg)"] = combined["Name"].map(lambda x: actual_masses_gmol.get(x, None))
combined["Actual Mass (kg)"] = combined["Actual Mass (kg)"] * 1e-3 / avogadro
combined["% Difference"] = 100 * (combined["VAM Mass (kg)"] - combined["Actual Mass (kg)"]) / combined["Actual Mass (kg)"]


tools.display_dataframe_to_user(name="Top 20 Atom and Molecule Masses (VAM)", dataframe=df_atoms._append(df_molecules, ignore_index=True))
tools.display_dataframe_to_user(name="VAM vs Actual Mass with Error", dataframe=combined)

# Extend common_atoms to all elements up to lead (Z=82)
full_common_atoms = [
    ("H", 1, 0, 1), ("He", 2, 2, 2), ("Li", 3, 4, 3), ("Be", 4, 5, 4), ("B", 5, 6, 5),
    ("C", 6, 6, 6), ("N", 7, 7, 7), ("O", 8, 8, 8), ("F", 9, 10, 9), ("Ne", 10, 10, 10),
    ("Na", 11, 12, 11), ("Mg", 12, 12, 12), ("Al", 13, 14, 13), ("Si", 14, 14, 14),
    ("P", 15, 16, 15), ("S", 16, 16, 16), ("Cl", 17, 18, 17), ("Ar", 18, 22, 18),
    ("K", 19, 20, 19), ("Ca", 20, 20, 20), ("Sc", 21, 24, 21), ("Ti", 22, 26, 22),
    ("V", 23, 28, 23), ("Cr", 24, 28, 24), ("Mn", 25, 30, 25), ("Fe", 26, 30, 26),
    ("Co", 27, 32, 27), ("Ni", 28, 31, 28), ("Cu", 29, 35, 29), ("Zn", 30, 35, 30),
    ("Ga", 31, 39, 31), ("Ge", 32, 41, 32), ("As", 33, 42, 33), ("Se", 34, 45, 34),
    ("Br", 35, 45, 35), ("Kr", 36, 48, 36), ("Rb", 37, 48, 37), ("Sr", 38, 50, 38),
    ("Y", 39, 50, 39), ("Zr", 40, 51, 40), ("Nb", 41, 52, 41), ("Mo", 42, 54, 42),
    ("Tc", 43, 55, 43), ("Ru", 44, 57, 44), ("Rh", 45, 58, 45), ("Pd", 46, 60, 46),
    ("Ag", 47, 61, 47), ("Cd", 48, 64, 48), ("In", 49, 66, 49), ("Sn", 50, 69, 50),
    ("Sb", 51, 71, 51), ("Te", 52, 76, 52), ("I", 53, 74, 53), ("Xe", 54, 77, 54),
    ("Cs", 55, 78, 55), ("Ba", 56, 81, 56), ("La", 57, 82, 57), ("Ce", 58, 82, 58),
    ("Pr", 59, 82, 59), ("Nd", 60, 84, 60), ("Pm", 61, 84, 61), ("Sm", 62, 88, 62),
    ("Eu", 63, 89, 63), ("Gd", 64, 93, 64), ("Tb", 65, 94, 65), ("Dy", 66, 97, 66),
    ("Ho", 67, 98, 67), ("Er", 68, 99, 68), ("Tm", 69, 100, 69), ("Yb", 70, 103, 70),
    ("Lu", 71, 104, 71), ("Hf", 72, 106, 72), ("Ta", 73, 108, 73), ("W", 74, 110, 74),
    ("Re", 75, 111, 75), ("Os", 76, 114, 76), ("Ir", 77, 115, 77), ("Pt", 78, 117, 78),
    ("Au", 79, 118, 79), ("Hg", 80, 121, 80), ("Tl", 81, 123, 81), ("Pb", 82, 125, 82),
    ("Bi", 83, 126, 83), ("Po", 84, 125, 84), ("At", 85, 125, 85), ("Rn", 86, 136, 86),
    ("Fr", 87, 136, 87), ("Ra", 88, 138, 88), ("Ac", 89, 138, 89), ("Th", 90, 142, 90),
    ("Pa", 91, 140, 91), ("U", 92, 146, 92),
    ("H2O", 10, 8, 10), ("CO2", 22, 22, 22), ("O2", 16, 16, 16), ("N2", 14, 14, 14),
    ("CH4", 10, 10, 10), ("C6H12O6", 72, 72, 72), ("NH3", 10, 10, 10), ("HCl", 18, 18, 18),
    ("C2H6", 18, 18, 18), ("C2H4", 16, 16, 16), ("C2H2", 14, 14, 14), ("NaCl", 28, 28, 28),
    ("C8H18", 98, 98, 98), ("C6H6", 48, 48, 48), ("CH3COOH", 32, 32, 32), ("H2SO4", 50, 50, 50),
    ("CaCO3", 50, 50, 50), ("C12H22O11", 176, 176, 176), ("Caffeine", 194, 194, 194),
    ("DNA Base (avg)", 10000, 10000, 10000)  # Approximation for a short base pair
]

# Extend actual_masses_gmol to include these if not already present
actual_masses_gmol.update({
    "Li": 6.94, "Be": 9.0122, "B": 10.81, "F": 18.998, "Ne": 20.180,
    "Ar": 39.948, "Sc": 44.955, "Ti": 47.867, "V": 50.942, "Cr": 51.996,
    "Mn": 54.938, "Co": 58.933, "Ni": 58.693, "Ga": 69.723, "Ge": 72.630,
    "As": 74.922, "Se": 78.971, "Kr": 83.798, "Rb": 85.468, "Sr": 87.62,
    "Y": 88.906, "Zr": 91.224, "Nb": 92.906, "Mo": 95.95, "Tc": 98.0,
    "Ru": 101.07, "Rh": 102.91, "Pd": 106.42, "Ag": 107.87, "Cd": 112.41,
    "In": 114.82, "Sn": 118.71, "Sb": 121.76, "Te": 127.60, "Xe": 131.29,
    "Cs": 132.91, "Ba": 137.33, "La": 138.91, "Ce": 140.12, "Pr": 140.91,
    "Nd": 144.24, "Pm": 145.0, "Sm": 150.36, "Eu": 151.96, "Gd": 157.25,
    "Tb": 158.93, "Dy": 162.50, "Ho": 164.93, "Er": 167.26, "Tm": 168.93,
    "Yb": 173.05, "Lu": 174.97, "Hf": 178.49, "Ta": 180.95, "W": 183.84,
    "Re": 186.21, "Os": 190.23, "Ir": 192.22, "Pt": 195.08, "Au": 196.97,
    "Hg": 200.59, "Tl": 204.38, "Bi": 208.98, "Po": 209.0, "At": 210.0,
    "Rn": 222.0, "Fr": 223.0, "Ra": 226.0, "Ac": 227.0, "Th": 232.04,
    "Pa": 231.04, "U": 238.03,
    "H2O": 18.015, "CO2": 44.01, "O2": 31.9988, "N2": 28.0134, "CH4": 16.04,
    "C6H12O6": 180.16, "NH3": 17.0305, "HCl": 36.46, "C2H6": 30.07, "C2H4": 28.05,
    "C2H2": 26.04, "NaCl": 58.44, "C8H18": 114.23, "C6H6": 78.11, "CH3COOH": 60.052,
    "H2SO4": 98.079, "CaCO3": 100.0869, "C12H22O11": 342.30, "Caffeine": 194.19,
    "DNA Base (avg)": 6500.0  # very rough average base pair molar mass
})




# Recompute results for full list
full_atom_results = [vam_mass_og(name, Z, N, e) for name, Z, N, e in full_common_atoms]
df_full_atoms = pd.DataFrame(full_atom_results, columns=["Name", "VAM Mass (kg)"])

# Reindex starting from 1 and format the full-length scientific notation
df_full_atoms.index = df_full_atoms.index + 1  # Start index at 1
# Add actual mass and % difference
df_full_atoms["Actual Mass (kg)"] = df_full_atoms["Name"].map(lambda x: actual_masses_gmol.get(x, None))
df_full_atoms["Actual Mass (kg)"] = df_full_atoms["Actual Mass (kg)"] * 1e-3 / avogadro
df_full_atoms["% Difference"] = 100 * (df_full_atoms["VAM Mass (kg)"] - df_full_atoms["Actual Mass (kg)"]) / df_full_atoms["Actual Mass (kg)"]

tools.display_dataframe_to_user(name="Extended Atom Mass Table (VAM vs Actual)", dataframe=df_full_atoms)

import numpy as np



import math
import numpy as np

# Constants
phi = (1 + math.sqrt(5)) / 2
alpha = 7.2973525643e-3
beta_default = 0.06
rho_core = 3.8934358266918687e+18  # kg/m^3
C_e = 1.09384563e6  # m/s
r_c = 1.40897017e-15  # m
c = 299792458  # m/s



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


# Volume per vortex
def compute_vortex_volume(r_c):
    return 2 * math.pi**2 * (2 * r_c) * r_c**2

# Main VAM mass function with coupling and separate electron treatment
def vam_mass(name, protons, neutrons, electrons, beta=beta_default, kappa=1.0):
    nucleons = protons + neutrons
    total_knots = nucleons + electrons
    V_knot = compute_vortex_volume(r_c)
    energy_density = 0.5 * rho_core * C_e**2

    # Per-knot volume contributions
    V_total_nucleon = nucleons * V_knot
    V_total_electron = electrons * V_knot  # assume same structure for now

    # Energy contributions
    E_nucleons = energy_density * V_total_nucleon
    E_electrons = energy_density * V_total_electron
    E_total_base = E_nucleons + E_electrons



    # tan_phi = sqrt( I**1.5 / (N * mu * K**0.5 * math.pi**0.5) )
    # where I = Z_rings * K * math.pi * a**2, etc.

    # tan_phi_fit ≈ (math.exp((x - 2) / 3) - 1) / 0.8


   #### Correction factor for electron suppression
    tan_phi_values = (a_0)/(nucleons * r_c *0.5)
    vam_errors = 3 * np.log(0.8 * tan_phi_values + 1) + 2
    ftan =vam_errors /100
    correction_factor = 1/ (1 + ftan)
    xi = correction_factor

    # Coherence term xi from nucleon count
    xi = 1 + beta * math.log(nucleons)


    # Coupling term (assume dot(ω_i, ω_j)=1, d_ij = 2*r_c)
    omega_k = np.ones(nucleons)
    d_matrix = np.full((nucleons, nucleons), 2 * r_c)
    coupling_sum = sum(
        omega_k[i] * omega_k[j] * math.exp(-d_matrix[i, j] / r_c)
        for i in range(nucleons) for j in range(i + 1, nucleons)
    )
    E_coupling = kappa * coupling_sum * energy_density * V_knot / nucleons

    # Total corrected energy
    E_total_corrected = E_total_base + E_coupling

    # Amplification factor
    amplification = (1 / phi) * (4 / alpha) * xi

    # Mass in kg
    M_vam = amplification * E_total_corrected / c**2
    return name, M_vam


# Compute VAM masses and compare
vam_results = []
for name, p, n, e in full_common_atoms:
    name, M_vam = vam_mass(name, p, n, e)
    M_actual = actual_masses_gmol.get(name, None)
    if M_actual:
        diff = 100 * (M_vam - M_actual) / M_actual
        vam_results.append((name, M_vam, M_actual, diff))

df_vam = pd.DataFrame(vam_results, columns=["Name", "VAM Mass (kg)", "Actual Mass (kg)", "% Difference"])
df_vam.index = df_vam.index + 1  # Start index at 1
tools.display_dataframe_to_user(name="VAM vs Actual Masses", dataframe=df_vam)