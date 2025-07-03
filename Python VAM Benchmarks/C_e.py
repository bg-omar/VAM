import math
import scipy.constants as const
import scipy.constants as sc
import numpy as np
import math
import random
from constants import *

G_calc = (alpha * F_max * (c * T_p)**2)/ (M_e**2)
G_calc2 = (L_p**2 * c**4 )/ (lambda_c *2 * np.pi * R_c)
G_calc3 = (C_e * c**3 * t_p )/ (R_e * M_e)
print(G_calc)
print(G_calc2)
print(G_calc3)

# Define the physical constants again manually
R_pr = 1.32140985539e-15  # Proton Compton wavelength (m)
R_infinity = const.Rydberg  # Rydberg constant (1/m)

# Compute v_v^2
v_v_squared = 4 / (rhoMass * r_c ** 2)
E_p = R_infinity * hbar * c

# Compute v_v
v_v = math.sqrt(v_v_squared)


# Constants from quantum mechanics
Me = sc.electron_mass  # Electron mass (kg
pi = np.pi            # Pi constant
r_t = 2.8179403227e-15   # Classical electron radius (m) or use Compton wavelength

# Vorticity Magnitude Estimate
omega = 1e23  # Typical vorticity (1/s), refine if needed

# Calculate Æther Density
rho_æther = (M_e * c**2) / (pi**2 * a_0 * R_e**2 * omega**2)

# Print result
print(f"Æther Density (ρ_æ): {rho_æther:.3e} kg/m³")
# Compute Proton Compton Wavelength
lambda_C_p = h / (M_pr * c)  # Proton Compton wavelength (m)
# Compute Proton Compton Angular Frequency
omega_C_p = c / lambda_C_p  # Proton Compton angular frequency (1/s)
# Calculate Æther Density using toroidal formula
rho_æther = (M_e * c**2) / (pi**2 * a_0 * R_e**2 * omega_C_p**2)

rho_æther2 = (M_e * c**2) / (pi**2 * R_c * R_c**2 * (c/lambda_c)**2)
# Print results
print(f"Proton Compton Wavelength: {lambda_C_p:.3e} m")
print(f"Proton Compton Angular Frequency (ω_C_p): {omega_C_p:.3e} s⁻¹")
print(f"Æther Density (ρ_æ): {rho_æther:.3e} kg/m³")
print(f"Æther Density2 (ρ_æ): {rho_æther2:.3e} kg/m³")

# Vortex Æther Model constants (approximate values, to be refined)
rho_ae_value = (hbar**2) / (2 * F_max * r_c * lambda_c**2)
print("rho_ae_value: ", rho_ae_value)

# Compute LHS of first equation: Quantum kinetic energy scale
lhs_qm = hbar**2 / (2 * Me)
rhs_vam = (F_max * R_c**3) / (5 * lambda_c * C_e)
ratio = lhs_qm / rhs_vam

print(" hbar**2 / (2 * Me): ",lhs_qm)
print(" (F_max * R_c**3) / (5 * lambda_c * C_e): ",rhs_vam)
print("ratio: ", ratio)

# Solve for mu_v using the relationship: mu_v = (4 * E_p) / (9 * C_e^4 * R_c^5)
# We need to express C_e from the Rydberg formula
C_e = ((R_infinity * r_c * c**3 * const.pi) ** (1/3))  # Solve for C_e
print("C_e: ", C_e)
# Compute mu_v using derived formula
mu_v = (4 * E_p) / (9 * C_e**4 * R_c**5)

print("v_v^2:", v_v_squared)
print("v_v^2:", format(v_v_squared, ',.0f'))
print("v_v:", v_v)
print("v_v:", format(v_v, ',.0f'))
print("mu_v:", mu_v)

# Compute rho_AE using the given formula
rho_AE = (4 * mu_v) / (R_c**2)
# Display the computed density of the Æther
print("rho_AE = (4 * mu_v) / (R_c**2)",rho_AE)

k = (hbar * c) / (4 * const.pi**3  * r_c**2 * C_e * c**3)
print("k:", k)
print("F_grmax:", F_GRmax)
f_e = C_e/ (2 * pi * R_c)
print("f_e = C_e/ (2 * pi * R_c): ", f_e)
f_e2 = M_e * c**2 / h
print("f_e = M_e * c**2 / h: ", f_e2)

def calculate_charge_circulation(m_æther, alpha, c, hbar, h, epsilon_0):
    """Calculate charge from vortex circulation quantization."""
    Gamma_1 = h / m_æther
    k = m_æther * np.sqrt((4 * np.pi * epsilon_0 * alpha * c) / hbar)
    e_derived = k * Gamma_1
    return e_derived

def calculate_coulomb_force(e_known, epsilon_0, a_0):
    """Calculate Coulomb force at the Bohr radius."""
    return (1 / (4 * np.pi * epsilon_0)) * (e_known**2 / a_0**2)

def calculate_vortex_force(m_æther, alpha, c, hbar, Gamma_1, a_0):
    """Calculate vortex-induced force."""
    return (m_æther**2 * alpha * c / hbar) * (Gamma_1**2 / a_0**2)

def calculate_max_force_scaling(c, G, alpha, L_p, R_c_values):
    """Calculate max force scaling as a function of vortex core radius."""
    return (c**4 / (4 * G)) * alpha * (R_c_values / L_p) ** -2

# Constants
m_æther = 7.0e-7  # Estimated Æther mass density in kg/m³

# Compute values
e_derived = calculate_charge_circulation(m_æther, alpha, c, hbar, h, varepsilon_0)
F_Coulomb_derived = calculate_coulomb_force(e, varepsilon_0, a_0)
Gamma_1 = h / m_æther
F_Vortex = calculate_vortex_force(m_æther, alpha, c, hbar, Gamma_1, a_0)
F_max_scaling = calculate_max_force_scaling(c, G, alpha, L_p, R_c)

# Display results
print(f"Derived Charge (C): {e_derived:.3e}")
print(f"Known Elementary Charge (C): {e:.3e}")
print(f"Coulomb Force at Bohr Radius (N): {F_Coulomb_derived:.3e}")
print(f"Vortex-Induced Force (N): {F_Vortex:.3e}")
print("Max Force Scaling for Different Core Radii:")
print(F_max_scaling)

print ( (3 * h) / (2 * np.pi * M_e * R_c**3))