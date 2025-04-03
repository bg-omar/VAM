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

# Physical constants (from your validated model)
c = 2.99792458e8               # Speed of light [m/s]
gamma = 1.0e-43                # Vorticity-gravity coupling [m^5/s^2]
kappa = 1.539047e-9            # Circulation [m^2/s]
C_e = 1.09384563e6             # Tangential velocity [m/s]
r_c = 1.40897017e-15           # Vortex core radius [m]

# Radius values (logarithmic range from r_c to nuclear scale ~10^-12 m)
r_vals = np.logspace(np.log10(r_c), -12, 1000)

# Define angular velocity Ω_k as C_e / r (capped at r_c to prevent singularity)
Omega_k = np.where(r_vals < r_c, C_e / r_c, C_e / r_vals)

# Kerr-like Æther model time dilation
term1 = gamma * Omega_k**2 / (r_vals * c**2)
term2 = kappa**2 / (r_vals**3 * c**2)
t_kerrlike = np.sqrt(1 - term1 - term2)

# Mask unphysical (imaginary) values
t_kerrlike_real = np.where(np.isreal(t_kerrlike), t_kerrlike, np.nan)

# General Relativity (Schwarzschild) time dilation for comparison
G = 6.67430e-11                 # Gravitational constant [m^3/kg/s^2]
M_ns = 1.4 * 1.98847e30         # Neutron star mass [kg]
t_gr = np.sqrt(1 - (2 * G * M_ns) / (r_vals * c**2))

# Plot comparison
plt.figure(figsize=(10, 6))
plt.plot(r_vals * 1e15, t_gr, label="GR (Schwarzschild)", color='black')
plt.plot(r_vals * 1e15, t_kerrlike_real, label="Vortex Æther Kerr-like", color='blue', linestyle='--')

plt.xscale('log')
plt.xlabel("Radial Distance $r$ [fm]")
plt.ylabel("Normalized Time Rate $t_{\mathrm{local}} / t_{\infty}$")
plt.title("Time Dilation Comparison: GR vs Vortex Æther (Kerr-like Model)")
plt.grid(True, which='both', linestyle='--')
plt.legend()
plt.tight_layout()
plt.show()
