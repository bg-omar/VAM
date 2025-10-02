import math, pandas as pd
import ace_tools_open as tools

# Constants
phi = (1 + math.sqrt(5)) / 2
alpha = 7.2973525643e-3
rho_core = 3.8934358266918687e18  # kg/m³
C_e = 1.09384563e6               # m/s
r_c = 1.40897017e-15             # m
c = 299792458                   # m/s
avogadro = 6.02214076e23        # mol⁻¹
M_e = 9.10938356e-31          # kg (electron mass)

def energy_density_k(k: int) -> float:
    # 0.5 * rho_core * (C_e/phi^k)^2   [J/m^3]
    return 0.5 * rho_core * (C_e / (phi**k))**2


# Master VAM Mass Formula:
# Mass = (4 / alpha) * eta * xi * tension * volume_sum * energy_density / c ** 2
# 4/alpha: Electroweak amplification (dimensionless)
# eta: Thread suppression factor (dimensionless)
# xi: Coherence suppression (dimensionless)
# tension: Topological tension (dimensionless)
# volume_sum * energy_density: Total base energy (Joules)
# / c^2: Convert energy → mass (via E=mc^2)
def vam_master_mass(n_knots, m_threads, s, V_list, k=0):
    volume_sum = sum(V_list)
    eta = (1 / m_threads)**3.0             # thread suppression (dimensionless)
    xi  = n_knots**(-1/phi)                # coherence suppression (dimensionless)
    tension = phi**(-s)                    # topological tension (dimensionless)
    En = energy_density_k(k)               # J/m^3
    M = (4/alpha) * eta * xi * tension * volume_sum * En / c**2
    return M

def vam_electron_mass_helicity(p=2, q=3):
    """Calculate electron mass from helicity-based formula."""
    sqrt_term = math.sqrt(p**2 + q**2)
    # Suppression parameters
    m = 1  # threads
    n = 1  # single knot
    s = 1  # golden renormalization index

    # Derived suppression factor to replace γpq
    eta = (1 / m) ** 1.5
    xi = n ** (-1 / phi)
    tension = 1 / phi ** s
    V_torus = 4 * math.pi ** 2 * r_c ** 3  # canonical torus volume
    A = eta * xi * tension * V_torus
    factor = 8 * math.pi * rho_core * r_c**3 / C_e
    M_e_helicity = factor * (sqrt_term + A)
    return M_e_helicity

# Create proton and neutron examples
V_torus = 2 * math.pi**2 * (2 * r_c) * r_c**2
V_u_topo = 2.8281  # knot 5_2
V_d_topo = 3.1639  # knot 6_1

# Proton: uud → 2x5_2 + 1x6_1
V_proton = [V_u_topo * V_torus, V_u_topo * V_torus, V_d_topo * V_torus]
M_proton = vam_master_mass(n_knots=3, m_threads=1, s=3, V_list=V_proton)

# Neutron: udd → 1x5_2 + 2x6_1
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

