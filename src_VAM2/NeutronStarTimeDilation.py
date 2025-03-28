# Constants
import numpy as np
import math
import os
import re
from datetime import datetime
import sympy as sp
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt

# Provided constants
C_e = 1.09384563e6        # m/s
rho_ae = 7e-7             # kg/m^3
r_c = 1.40897017e-15      # m
c = 2.99792458e8          # m/s
G = 6.67430e-11           # m^3/kg/s^2

# Derived constants
gamma = G * rho_ae**2     # m^5/s^2
kappa = C_e * r_c         # m^2/s
alpha = (r_c**2) / (C_e**2)  # s^2
Omega_k = C_e / r_c       # rad/s


# Physical constants
t_p = 5.391247e-44     # Planck time [s]
M_e = 9.10938356e-31   # Electron mass [kg]
A_0 = 5.29177210903e-11 # Bohr radius [m]
h = 6.62607015e-34     # Planck's constant [J s]
pi = np.pi
mu_0 = 4 * pi * 1e-7   # Vacuum permeability [H/m]

# Redefine key constants
gamma = (C_e * c**3 * t_p**2) / (rho_ae**2 * r_c * M_e)         # m^5/s^2
kappa_1 = C_e * r_c                                             # m^2/s
kappa_2 = h / (4 * pi * M_e * A_0)                              # m^2/s
alpha_1 = C_e**2 * t_p**2 / r_c**2                              # s^2
alpha_2 = (t_p / (r_c / C_e))**2                                # s^2
alpha_3 = (2 * A_0 * r_c) / c**2                                # s^2

keyConstants ={
    "gamma [m^5/s^2]": gamma,
    "kappa = C_e * r_c": kappa_1,
    "kappa = h / 4π M_e A_0": kappa_2,
    "alpha = (C_e t_p / r_c)^2": alpha_1,
    "alpha = (t_p / (r_c / C_e))^2": alpha_2,
    "alpha = 2 A_0 r_c / c^2": alpha_3
}

# Derived constants
gamma = G * rho_ae**2     # m^5/s^2
kappa = C_e * r_c         # m^2/s
alpha = (r_c**2) / (C_e**2)  # s^2
Omega_k = C_e / r_c       # rad/s

# Equation 1: Heuristic time dilation
t_ratio_heuristic = 1 / (1 + alpha * Omega_k**2)

# Equation 2: GR-like time dilation from vorticity
numerator = 2 * gamma * Omega_k**2
denominator = r_c * c**2
t_ratio_gr_like = np.sqrt(1 - numerator / denominator)

# Equation 3: Kerr-like time adjustment
term1 = gamma * Omega_k**2 / (r_c * c**2)
term2 = kappa**2 / (r_c**3 * c**2)
t_ratio_kerr_like = np.sqrt(1 - term1 - term2)

threeEquations = {
    "t_ratio_heuristic": t_ratio_heuristic,
    "t_ratio_gr_like": t_ratio_gr_like,
    "t_ratio_kerr_like": t_ratio_kerr_like
}
# Define a cutoff radius (to avoid unphysical core values)
# Set cutoff where time ratio remains real and > 0

# Define a range of radii from just above r_c to a few nanometers
r_values = np.linspace(1.1 * r_c, 1e-8, 500)

# Preallocate arrays
t_ratios_gr_like = []
t_ratios_kerr_like = []

for r in r_values:
    omega = C_e / r
    term_gr = 1 - (2 * gamma * omega**2) / (r * c**2)
    term_kerr = 1 - (gamma * omega**2) / (r * c**2) - (kappa**2) / (r**3 * c**2)

    # Avoid NaNs by setting invalid regions to np.nan
    t_ratios_gr_like.append(np.sqrt(term_gr) if term_gr > 0 else np.nan)
    t_ratios_kerr_like.append(np.sqrt(term_kerr) if term_kerr > 0 else np.nan)


# Plot both time ratio curves vs radius
plt.figure(figsize=(10, 6))
plt.plot(r_values * 1e9, t_ratios_gr_like, label="GR-like Time Dilation", color='blue')
plt.plot(r_values * 1e9, t_ratios_kerr_like, label="Kerr-like Time Adjustment", color='darkred')
plt.axhline(y=1, linestyle='--', color='gray')
plt.xlabel("Radius $r$ [nm]")
plt.ylabel("Normalized Time Rate $t_{\\text{local}} / t_{\\text{abs}}$")
plt.title("Time Dilation vs Radius (with Cutoff Applied)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Fix the LaTeX syntax issue by avoiding \text inside math expressions
plt.figure(figsize=(10, 6))
plt.plot(r_values * 1e9, t_ratios_gr_like, label="GR-like Time Dilation", color='blue')
plt.plot(r_values * 1e9, t_ratios_kerr_like, label="Kerr-like Time Adjustment", color='darkred')
plt.axhline(y=1, linestyle='--', color='gray')
plt.xlabel("Radius $r$ [nm]")
plt.ylabel("Normalized Time Rate $t_{\\mathrm{local}} / t_{\\mathrm{abs}}$")
plt.title("Time Dilation vs Radius (with Physical Cutoff)")
plt.legend()
plt.grid(True)
plt.tight_layout()


# Recalculate and validate the GR-3D derived time dilation equations using the updated constants

# Use updated gamma, kappa, and alpha from previous validation
gamma = 136.21023318101015        # m^5/s^2
kappa = 1.541195863254857e-09     # m^2/s
alpha = 1.7518097295713056e-45    # s^2
Omega_k = C_e / r_c               # rad/s

# Pick a radius where GR-3D equations should be physically valid (> core)
r_valid = 1e-10  # 0.1 nm

# Equation 1: Heuristic time dilation
t_ratio_heuristic = 1 / (1 + alpha * Omega_k**2)

# Equation 2: GR-like vortex time dilation
term_gr = 1 - (2 * gamma * Omega_k**2) / (r_valid * c**2)
t_ratio_gr_like = np.sqrt(term_gr) if term_gr > 0 else np.nan

# Equation 3: Kerr-like time dilation
term_kerr = 1 - (gamma * Omega_k**2) / (r_valid * c**2) - (kappa**2) / (r_valid**3 * c**2)
t_ratio_kerr_like = np.sqrt(term_kerr) if term_kerr > 0 else np.nan

threeEquations2 = {
    "Radius r [m]": r_valid,
    "t_ratio_heuristic": t_ratio_heuristic,
    "t_ratio_gr_like": t_ratio_gr_like,
    "t_ratio_kerr_like": t_ratio_kerr_like
}

# Let's compute time dilation around:
# 1. The Sun
# 2. A neutron star (mass ~1.4 solar masses, radius ~12 km)

# Constants
G = 6.67430e-11          # m^3 kg^-1 s^-2
c = 2.99792458e8         # m/s
M_sun = 1.98847e30       # kg
R_sun = 6.9634e8         # m

# Neutron star properties
M_ns = 1.4 * M_sun       # kg
R_ns = 1.2e4             # m

# GR time dilation near a mass (Schwarzschild)
def time_dilation_gr(M, r):
    return np.sqrt(1 - (2 * G * M) / (r * c**2))

# Dilation for the Sun and a neutron star
t_ratio_sun_surface = time_dilation_gr(M_sun, R_sun)
t_ratio_ns_surface = time_dilation_gr(M_ns, R_ns)

print(t_ratio_sun_surface, t_ratio_ns_surface)

# Compare Æther-based time dilation vs GR around neutron star

# Reuse validated constants
gamma = 136.21  # m^5/s^2
C_e = 1.09384563e6  # m/s
r_c = 1.40897017e-15  # m

# Create radius range from core to several multiples of neutron star radius
radii = np.linspace(1.2e4, 1e5, 500)  # from 12 km to 100 km

# GR time dilation curve
t_gr = np.sqrt(1 - (2 * G * M_ns) / (radii * c**2))

# Æther-vortex time dilation using: t/t_inf = sqrt(1 - 2γΩ² / rc²)
# Using Ω = C_e / r
omega = C_e / radii
t_ae = np.sqrt(1 - (2 * gamma * omega**2) / (radii * c**2))
t_ae = np.where(np.isreal(t_ae), t_ae, np.nan)  # avoid NaNs



# If Ω = C_e / r_c is treated as a constant, then time dilation becomes:
# t/t_inf = sqrt(1 - (2 * gamma * Ω^2) / (R * c^2))
# This now has a 1/R decay form, matching GR

# Recompute with constant Ω
Omega_const = C_e / r_c  # constant angular velocity from core

# Time dilation from vortex model with 1/R decay
t_ae_const = np.sqrt(1 - (2 * gamma * Omega_const**2) / (radii * c**2))
t_ae_const = np.where(np.isreal(t_ae_const), t_ae_const, np.nan)

plt.figure(figsize=(10, 6))
plt.plot(radii / 1e3, t_gr, label="GR Time Dilation", color='black')
plt.plot(radii / 1e3, t_ae_const, label="Æther Model (Const Ω)", color='blue', linestyle='--')
plt.xlabel("Radius from NS center [km]")
plt.ylabel("Normalized Time Rate")
plt.title("Time Dilation Near a Neutron Star: GR vs Æther (Ω constant)")
plt.grid(True)
plt.legend()


fig = plt.figure(figsize=(10, 6))
plt = fig.add_subplot(111, projection='3d')

# Add both lines in separate planes to visualize them distinctly
z_gr = np.zeros_like(radii)
z_ae = np.ones_like(radii)



plt.plot(radii / 1e3, t_gr, z_gr, label="GR Time Dilation", color='black')
plt.plot(radii / 1e3, t_ae_const, z_ae, label="Æther Model", color='blue', linestyle='--')
plt.set_xlabel("Radius from NS center [km]")
plt.set_ylabel("Normalized Time Rate")
plt.set_zlabel("Model Index (0 = GR, 1 = Æther)")
plt.set_title("Time Dilation Around a Neutron Star: GR vs Æther Model")
plt.grid(True)
plt.legend()





# Define symbols
r, r_c, gamma_sym, c, Omega_0 = sp.symbols("r r_c gamma c Omega_0", positive=True, real=True)

# Define angular velocity field (smoothed)
omega_r = Omega_0 / sp.sqrt(1 + (r / r_c)**2)

# Vorticity magnitude squared (assuming axisymmetric vortex ring)
omega_squared = omega_r**2

# Volume element in spherical coordinates: dV = 4πr^2 dr (integrate over shell)
dV = 4 * sp.pi * r**2

# Mass-equivalent integral from 0 to R: M(R) = ∫ ω²(r) * dV
R = sp.Symbol("R", positive=True)
M_R = sp.integrate(omega_squared * dV, (r, 0, R))

M_R.simplify()
