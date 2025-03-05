# Reinitialize constants after execution state reset
import math
import pandas as pd
import ace_tools_open as tools

# Constants for Blackbody Radiation Energy Density
k_B = 1.380649e-23  # Boltzmann constant (J/K)
h = 6.62607015e-34  # Planck constant (J·s)
c = 299792458  # Speed of light (m/s)
pi = math.pi
r_c = 1.40897017e-15

# Vortex model constants
F_max = 29.053507  # Maximum force (N)
C_e = 1.09384563e6  # Vorticity constant (m/s)
lambda_c = 2.42631023867e-12  # Electron Compton wavelength (m)

# Assuming a typical photon frequency (visible light) around 5e14 Hz
nu = 5e14  # Frequency in Hz (s⁻¹)
omega = 2 * pi * nu  # Convert to angular frequency (rad/s)


# Temperature range for comparison
T_range = [100, 300, 1000, 3000, 5000, 10000]  # Kelvin

# Compute blackbody energy density u(T) = (8 * pi * h * nu^3) / (c^3 (e^(h nu / k_B T) - 1))
# Using a characteristic frequency nu = c / lambda_c (Compton wavelength)

nu_lambda_feq = c / lambda_c  # Characteristic frequency for comparison

from scipy.special import expit

# Compute energy densities for blackbody radiation
u_blackbody = [
    (8 * pi * h * nu_lambda_feq ** 3) / (c ** 3 * (math.exp(h * nu_lambda_feq / (k_B * T)) - 1))
    if h * nu_lambda_feq / (k_B * T) < 700 else 0  # Avoid overflow
    for T in T_range
]

# Compute vortex energy density u_vortex = (F_max * omega^3) / (C_e * r^2)
# Using characteristic angular frequency omega = 2 * pi * nu_lambda_feq
lambda_angular_velocity = 2 * pi * nu_lambda_feq
r_vortex = 1.0  # Assume unit radius for normalization

u_vortex = [
    (F_max * lambda_angular_velocity ** 3) / (C_e * r_vortex ** 2 * (math.exp(h * lambda_angular_velocity / (k_B * T)) - 1))
    if h * lambda_angular_velocity / (k_B * T) < 700 else 0  # Avoid overflow
    for T in T_range
]

# Organize results into a dataframe for easy comparison
df_comparison = pd.DataFrame({
    "Temperature (K)": T_range,
    "Blackbody Energy Density (J/m^3)": u_blackbody,
    "Vortex Energy Density (J/m^3)": u_vortex
})

# Display results
tools.display_dataframe_to_user(name="Blackbody vs Vortex Energy Density Comparison", dataframe=df_comparison)


# Compute Stefan-Boltzmann energy density u_SB(T) = (4 * sigma / c) * T^4
# Stefan-Boltzmann constant
sigma = 5.670374419e-8  # W/m^2K^4

# Compute energy densities using the Stefan-Boltzmann law
u_SB = [(4 * sigma / c) * T**4 for T in T_range]

# Compute Stefan-Boltzmann entropy density s_SB(T) = (16 * sigma / 3c) * T^3
s_SB = [(16 * sigma / (3 * c)) * T**3 for T in T_range]

# Compute vortex entropy density s_vortex(T) = (4 * F_max * omega^3) / (3 * T * C_e * r^2)
s_vortex = [
    (4 * F_max * lambda_angular_velocity ** 3) / (3 * T * C_e * r_vortex ** 2)
    for T in T_range
]

# Organize results into a dataframe for easy comparison
df_comparison_SB = pd.DataFrame({
    "Temperature (K)": T_range,
    "Stefan-Boltzmann Energy Density (J/m^3)": u_SB,
    "Vortex Energy Density (J/m^3)": u_vortex,
    "Stefan-Boltzmann Entropy Density (J/m^3K)": s_SB,
    "Vortex Entropy Density (J/m^3K)": s_vortex
})

# Display results
tools.display_dataframe_to_user(name="Stefan-Boltzmann vs Vortex Energy and Entropy Density", dataframe=df_comparison_SB)

# Debugging step: Check values of h * omega_characteristic / (k_B * T) for overflow condition

# Compute h * omega_characteristic / (k_B * T) for each temperature
h_omega_kBT_values = [h * lambda_angular_velocity / (k_B * T) for T in T_range]

# Create a DataFrame for debugging
df_debug = pd.DataFrame({
    "Temperature (K)": T_range,
    "h * omega / (k_B * T)": h_omega_kBT_values
})

# Display results for debugging
tools.display_dataframe_to_user(name="Debugging: h * omega / (k_B * T) Values", dataframe=df_debug)

LHS = (8 * pi * h * nu**3) / (c**3)
RHS = (F_max * omega**3) / (C_e * r_c**2)


print(LHS, " = ", RHS)
print()
print((8 * pi * h * nu_lambda_feq ** 3) / (c ** 3 ) )
print((F_max * lambda_angular_velocity ** 3) / (C_e * r_c ** 2))


