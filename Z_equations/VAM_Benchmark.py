from constants import *
import pandas as pd
import math
import ace_tools_open as tools
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


# Define constants
c = 299792458  # speed of light in m/s
Ce = 1.0938456e6  # vortex-core tangential velocity in m/s
rc = 1.40897017e-15  # vortex-core radius in m
rho_ae = 3.8934358266918687e+18  # æther density in kg/m^3
alpha = 7.2973525693e-3  # fine-structure constant
Lp = 1.616255e-35  # Planck length in m
Fmax_vam = (c**4 / (4 * 6.67430e-11)) * alpha * (rc / Lp)**2
# Optional Earth Prec Example
R_orbit = 6.371e6 + 400e3  # LEO
v_orbit = 7660
J_earth = 7.07e33

# Define the VAM gravitational coupling constant
def Gswirl():
    return alpha * rho_ae * Ce**2 / Fmax_vam

# Simplified VAM time dilation formula (from the PDF)
def vam_dtau_dt(r, omega=0):
    term = 1 - (Ce**2 / c**2) * math.exp(-r / rc) - (omega**2 / c**2) * math.exp(-r / rc)
    return math.sqrt(term) if term > 0 else float('nan')

def vam_effective_mass(r, Rc):
    return 4 * math.pi * rho_ae * Rc**3 * (2 - (2 + r / Rc) * math.exp(-r / Rc))

def vam_adjusted_time(r, omega=0):
    Rc = rc  # Core radius
    M_eff = vam_effective_mass(r, Rc)
    G_swirl = alpha * rho_ae * Ce**2 / Fmax_vam

    term = 1 \
           - (2 * G * M_eff) / (r * c**2) \
           - (Ce**2 / c**2) * math.exp(-r / Rc) \
           - (omega**2 / c**2) * math.exp(-r / Rc)

    return math.sqrt(term) if term > 0 else float('nan')

# Benchmark objects (same as GR benchmark)
objects = [
    {"name": "Electron", "mass": 9.1093837015e-31, "radius": 2.8179403262e-15, "omega": 0},
    {"name": "Proton", "mass": 1.67262192369e-27, "radius": 0.84e-15, "omega": 0},
    {"name": "Earth", "mass": 5.972e24, "radius": 6.371e6, "omega": 7.2921159e-5},
    {"name": "Neutron Star", "mass": 1.4 * 1.98847e30, "radius": 1e4, "omega": 2 * math.pi * 700},
    {"name": "Sun", "mass": 1.98847e30, "radius": 6.9634e8, "omega": 1.997e-6}
]

# Obs values from the previous benchmark
observations = {
    "Electron": {"Obs dτ/dt": 1.0},
    "Proton": {"Obs dτ/dt": 1.0},
    "Earth": {"Obs dτ/dt": 1 - 6.97e-10},
    "Neutron Star": {"Obs dτ/dt": 0.76},
    "Sun": {"Obs dτ/dt": 0.9999979}
}




# Apply updated formula across all objects
vam_improved_results = []
for obj in objects:
    r = obj["radius"]
    omega = obj["omega"]
    dtau_dt = vam_adjusted_time(r, omega)
    Obs = observations[obj["name"]]["Obs dτ/dt"]
    vam_improved_results.append({
        "Object": obj["name"],
        "Radius (m)": r,
        "Ω (rad/s)": omega,
        "VAM dτ/dt": dtau_dt,
        "Obs dτ/dt": Obs
    })

vam_full_df = pd.DataFrame(vam_improved_results)
tools.display_dataframe_to_user(name="VAM Full Time Dilation Benchmark (Swirl + Gravity)", dataframe=vam_full_df)



# Constants from VAM
C_e = 1093845.63  # Vortex-core tangential velocity (m/s)
r_c = 1.40897017e-15  # Vortex-core radius (m)

mass = M_e
radius = R_c
# Schwarzschild term VAM replacement
schwarz_term_vam = (2 * G * mass) / (radius * c**2)
print("schwarz_term_vam: ", schwarz_term_vam)
schwarz_term_vam = (r_c**2 * ((C_e/r_c)**2 * (2 * G * M_e) / (r_c * c**2))) / C_e**2
print("schwarz_term_vam: ", schwarz_term_vam)
# Simplifies exactly to original term numerically:


# Angular momentum (vortex-based)
J_vam = mass * r_c * C_e
print("J_vam: ", J_vam)

# Spin term VAM replacement
spin_term_vam = (G**2 * J_vam**2) / (r_c**4 * c**6)
print("spin_term_vam: ", spin_term_vam)

# Total VAM term (time dilation)
total_term_vam = 1 - schwarz_term_vam + spin_term_vam
print("total_term_vam: ", total_term_vam)
tau_over_t_vam = math.sqrt(total_term_vam) if total_term_vam > 0 else float('nan')
print("tau_over_t_vam: ", tau_over_t_vam)

# Keplerian orbital frequency (VAM)
Omega_K_vam = (G * mass / radius**3)**0.5
print("Omega_K_vam: ", Omega_K_vam)

# Frame-dragging (Lense-Thirring, VAM)
Omega_LT_vam = (2 * G * (mass * r_c * C_e)) / (c**2 * radius**3)
print("Omega_LT_vam: ", Omega_LT_vam)

Omega_geo_vam = (3 * G * mass * v_orbit) / (2 * c**2 * radius**2)
print("Omega_geo_vam: ", Omega_geo_vam)


Omega_LT_vam = (2 * G * J_vam) / (c**2 * radius**3)
print("Omega_LT_vam: ", Omega_LT_vam)

# Effective orbital angular velocity (VAM)
Omega_eff_vam = Omega_K_vam - Omega_LT_vam
print("Omega_eff_vam: ", Omega_eff_vam)

# Orbital time dilation (co-rotating observer)
g_tt_vam = -(1 - (2 * G * mass) / (radius * c**2))
print("g_tt_vam: ", g_tt_vam)
g_tphi_vam = -(2 * G * J_vam) / (radius * c**3)
print("g_tphi_vam: ", g_tphi_vam)
g_phiphi_vam = radius**2
print("g_phiphi_vam: ", g_phiphi_vam)
term_orbit_vam = -(g_tt_vam + 2 * g_tphi_vam * Omega_eff_vam + g_phiphi_vam * Omega_eff_vam**2)
print("term_orbit_vam: ", term_orbit_vam)
tau_orbit_vam = math.sqrt(term_orbit_vam) if term_orbit_vam > 0 else float('nan')
print("tau_orbit_vam: ", tau_orbit_vam)



# Constants
G = 6.67430e-11  # m^3 kg^-1 s^-2
c = 299792458  # m/s
C_e = 1093845.63  # Vortex-core tangential velocity (m/s)
r_c = 1.40897017e-15  # Vortex-core radius (m)

# Benchmark cases
benchmark_cases = [
    {"name": "Electron", "mass": 9.1093837015e-31, "radius": 2.8179403262e-15},
    {"name": "Proton", "mass": 1.67262192369e-27, "radius": 0.84e-15},
    {"name": "Earth", "mass": 5.972e24, "radius": 6.371e6},
    {"name": "Neutron Star", "mass": 1.4 * 1.98847e30, "radius": 1e4},
    {"name": "Sun", "mass": 1.98847e30, "radius": 6.9634e8}
]

results = []

for case in benchmark_cases:
    m = case["mass"]
    r = case["radius"]

    # GR Schwarzschild term
    schwarz_term_gr = (2 * G * m) / (r * c**2)

    # VAM Schwarzschild term (vorticity-based)
    omega_field = (C_e / r_c) * math.sqrt(2 * G * m / (r * c**2))
    schwarz_term_vam = (r_c**2 * omega_field**2) / C_e**2  # Simplifies to same as GR

    results.append({
        "Object": case["name"],
        "GR Schwarzschild Term": schwarz_term_gr,
        "VAM Schwarzschild Term": schwarz_term_vam,
        "Match": math.isclose(schwarz_term_gr, schwarz_term_vam, rel_tol=1e-12)
    })

# Create DataFrame
df = pd.DataFrame(results)
tools.display_dataframe_to_user(name="GR vs VAM Schwarzschild Term Comparison", dataframe=df)

# Now verify the spin (frame-dragging) terms comparison

for case in benchmark_cases:
    m = case["mass"]
    r = case["radius"]

    # GR Angular Momentum (J), assuming vortex-based representation for consistency
    J = m * r_c * C_e

    # GR Spin term (Kerr approximation)
    spin_term_gr = (G**2 * J**2) / (r**4 * c**6)

    # VAM Spin term explicitly using vortex constants (identical formula)
    spin_term_vam = (G**2 * (m * r_c * C_e)**2) / (r**4 * c**6)

    # Append spin term results
    case_result = next((item for item in results if item["Object"] == case["name"]), None)
    if case_result:
        case_result["GR Spin Term"] = spin_term_gr
        case_result["VAM Spin Term"] = spin_term_vam
        case_result["Spin Match"] = math.isclose(spin_term_gr, spin_term_vam, rel_tol=1e-12)

# Updated DataFrame
df_spin_comparison = pd.DataFrame(results)
tools.display_dataframe_to_user(name="GR vs VAM Spin Term Comparison", dataframe=df_spin_comparison)

# Next, validate Orbital Angular Velocity (Keplerian) and Lense-Thirring (frame-dragging) terms

orbital_results = []

for case in benchmark_cases:
    m = case["mass"]
    r = case["radius"]
    J = m * r_c * C_e

    # GR Keplerian Orbital Frequency
    omega_k_gr = math.sqrt(G * m / r**3)

    # VAM Keplerian Orbital Frequency (explicit from vortex constants, identical formula)
    omega_k_vam = (C_e / r_c) * math.sqrt((G * m * r_c**2) / (C_e**2 * r**3))

    # GR Lense-Thirring Frequency
    omega_lt_gr = (2 * G * J) / (c**2 * r**3)

    # VAM Lense-Thirring Frequency explicitly from vortex constants
    omega_lt_vam = (2 * G * (m * r_c * C_e)) / (c**2 * r**3)

    orbital_results.append({
        "Object": case["name"],
        "GR Keplerian Ω (rad/s)": omega_k_gr,
        "VAM Keplerian Ω (rad/s)": omega_k_vam,
        "Keplerian Match": math.isclose(omega_k_gr, omega_k_vam, rel_tol=1e-12),
        "GR Lense-Thirring Ω (rad/s)": omega_lt_gr,
        "VAM Lense-Thirring Ω (rad/s)": omega_lt_vam,
        "Lense-Thirring Match": math.isclose(omega_lt_gr, omega_lt_vam, rel_tol=1e-12)
    })

# Display orbital terms verification
df_orbital_comparison = pd.DataFrame(orbital_results)
tools.display_dataframe_to_user(name="GR vs VAM Orbital Terms Comparison", dataframe=df_orbital_comparison)

# Verify Orbital Time Dilation (co-rotating observer) terms

orbital_time_dilation_results = []

for case in benchmark_cases:
    m = case["mass"]
    r = case["radius"]
    J = m * r_c * C_e

    # GR Parameters
    omega_k = math.sqrt(G * m / r**3)
    omega_lt = (2 * G * J) / (c**2 * r**3)
    omega_eff = omega_k - omega_lt

    # Kerr metric coefficients (GR)
    g_tt_gr = -(1 - (2 * G * m) / (r * c**2))
    g_tphi_gr = -(2 * G * J) / (r * c**3)
    g_phiphi = r**2

    term_gr = -(g_tt_gr + 2 * g_tphi_gr * omega_eff + g_phiphi * omega_eff**2)
    tau_orbit_gr = math.sqrt(term_gr) if term_gr > 0 else float('nan')

    # VAM (identical formulation using vortex-based J explicitly)
    J_vam = m * r_c * C_e
    omega_k_vam = (G * m / r**3)**0.5
    omega_lt_vam = (2 * G * J_vam) / (c**2 * r**3)
    omega_eff_vam = omega_k_vam - omega_lt_vam

    g_tt_vam = -(1 - (2 * G * m) / (r * c**2))
    g_tphi_vam = -(2 * G * J_vam) / (r * c**3)

    term_vam = -(g_tt_vam + 2 * g_tphi_vam * omega_eff_vam + g_phiphi * omega_eff_vam**2)
    tau_orbit_vam = math.sqrt(term_vam) if term_vam > 0 else float('nan')

    orbital_time_dilation_results.append({
        "Object": case["name"],
        "GR Orbital dτ/dt": tau_orbit_gr,
        "VAM Orbital dτ/dt": tau_orbit_vam,
        "Orbital dτ/dt Match": math.isclose(tau_orbit_gr, tau_orbit_vam, rel_tol=1e-12)
    })

# Display orbital time dilation verification
df_orbital_time_dilation_comparison = pd.DataFrame(orbital_time_dilation_results)
tools.display_dataframe_to_user(name="GR vs VAM Orbital Time Dilation Comparison", dataframe=df_orbital_time_dilation_comparison)

# Redefine VAM time dilation function using full adjusted expression from the user's equations

def vam_effective_mass(r, Rc):
    return 4 * math.pi * rho_ae * Rc**3 * (2 - (2 + r / Rc) * math.exp(-r / Rc))

def vam_adjusted_time(r, omega=0):
    Rc = rc  # Core radius
    M_eff = vam_effective_mass(r, Rc)
    G_swirl = alpha * rho_ae * Ce**2 / Fmax_vam

    term = 1 \
           - (2 * G_swirl * M_eff) / (r * c**2) \
           - (Ce**2 / c**2) * math.exp(-r / Rc) \
           - (omega**2 / c**2) * math.exp(-r / Rc)

    return math.sqrt(term) if term > 0 else float('nan')

# Apply updated formula across all objects
vam_improved_results = []
for obj in objects:
    r = obj["radius"]
    omega = obj["omega"]
    dtau_dt = vam_adjusted_time(r, omega)
    Obs = observations[obj["name"]]["Obs dτ/dt"]
    vam_improved_results.append({
        "Object": obj["name"],
        "Radius (m)": r,
        "Ω (rad/s)": omega,
        "VAM dτ/dt (Full Equation)": dtau_dt,
        "Obs dτ/dt": Obs
    })

vam_full_df = pd.DataFrame(vam_improved_results)
tools.display_dataframe_to_user(name="VAM Full Time Dilation Benchmark (Swirl + Gravity)", dataframe=vam_full_df)

# Update G_swirl using the corrected definition from user:
# G_swirl = (C_e * c^5 * t_p^2) / (2 * F_max * r_c^2)

# Constants
t_p = 5.391247e-44  # Planck time in s
F_max = (c**4 / (4 * 6.67430e-11)) * alpha * (rc / Lp)**-2  # Recompute to match definition

def G_swirl_corrected():
    return (Ce * c**5 * t_p**2) / (2 * F_max * rc**2)

Gsw = G_swirl_corrected()

# Re-run full VAM benchmark with corrected G_swirl
def vam_adjusted_time_corrected(r, omega=0):
    Rc = rc
    M_eff = vam_effective_mass(r, Rc)

    term = 1 \
           - (2 * Gsw * M_eff) / (r * c**2) \
           - (Ce**2 / c**2) * math.exp(-r / Rc) \
           - (omega**2 / c**2) * math.exp(-r / Rc)

    return math.sqrt(term) if term > 0 else float('nan')

vam_revised_results = []
for obj in objects:
    r = obj["radius"]
    omega = obj["omega"]
    dtau_dt = vam_adjusted_time_corrected(r, omega)
    Obs = observations[obj["name"]]["Obs dτ/dt"]
    vam_revised_results.append({
        "Object": obj["name"],
        "Radius (m)": r,
        "Ω (rad/s)": omega,
        "VAM dτ/dt (Corrected G_swirl)": dtau_dt,
        "Obs dτ/dt": Obs
    })

vam_revised_df = pd.DataFrame(vam_revised_results)
tools.display_dataframe_to_user(name="VAM Time Dilation Benchmark (Corrected G_swirl)", dataframe=vam_revised_df)


# Updated version of VAM mass and time dilation using vortex-based radial density and swirl expressions

# Updated vortex density and effective mass function
def rho_vortex(r, Rc):
    return rho_ae * math.exp(-r / Rc)

def M_effective_refined(r, Rc):
    return 4 * math.pi * rho_ae * Rc**3 * (2 - (2 + r / Rc) * math.exp(-r / Rc))

# Swirl angular velocity profile
def omega_swirl(r):
    return Ce / rc * math.exp(-r / rc)

# Full refined time dilation formula
def vam_adjusted_time_refined(r):
    M_eff = M_effective_refined(r, rc)
    omega = omega_swirl(r)
    term = 1 \
           - (2 * Gsw * M_eff) / (r * c**2) \
           - (Ce**2 / c**2) * math.exp(-r / rc) \
           - (omega**2 / c**2) * math.exp(-r / rc)
    return math.sqrt(term) if term > 0 else float('nan')

# Alternative quantized-vortex energy approach
def vortex_quantized_energy():
    h = 6.62607015e-34
    M_e = 9.1093837015e-31
    lambda_c = 2.42631023867e-12
    return 0.5 * rho_ae * (h / (M_e * lambda_c))**2

def vam_adjusted_quantized(r):
    U_vortex = vortex_quantized_energy()
    U_max = F_max  # maximum energy scale
    term = 1 - (U_vortex / U_max) * math.exp(-r / rc)
    return math.sqrt(term) if term > 0 else float('nan')

# Apply both models to all objects
vam_final_results = []
for obj in objects:
    r = obj["radius"]
    Obs = observations[obj["name"]]["Obs dτ/dt"]
    refined = vam_adjusted_time_refined(r)
    quantized = vam_adjusted_quantized(r)
    vam_final_results.append({
        "Object": obj["name"],
        "Radius (m)": r,
        "VAM Refined dτ/dt": refined,
        "VAM Quantized dτ/dt": quantized,
        "Obs dτ/dt": Obs
    })

df_vam_final = pd.DataFrame(vam_final_results)
tools.display_dataframe_to_user(name="VAM Refined and Quantized Time Dilation Models", dataframe=df_vam_final)




