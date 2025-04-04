import math
import os
import re
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt
import numpy as np


# Define grid
x = np.linspace(-1, 1, 400)
y = np.linspace(-1, 1, 400)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

# Vortex-induced time potential well (inverted Gaussian-like shape)
# The closer to the vortex core (r=0), the deeper the time well
omega0 = 2e6  # representative angular velocity
alpha = 1e-8
I = 1e-20
t_abs = 1
t_local = t_abs / (1 + 0.5 * alpha * I * omega0**2 * np.exp(-R**2 / 0.1))
# Varying Omega_k with radius: assume Ω_k ∝ 1/r^2 (core rotation decays with radius)
r = np.linspace(0.01, 1.0, 500)  # avoid r = 0
Omega_k_r = 1e6 / r**2           # example vortex profile
alpha = 1e-8
I = 1e-20

# Time dilation as function of r
t_local_r = 1 / (1 + 0.5 * alpha * I * Omega_k_r**2)

# Zooming in on the radial plot for r in [0.01, 0.2]
r_zoom = np.linspace(0.00001, 0.0002, 500)
Omega_k_r_zoom = 1e6 / r_zoom**2
t_local_r_zoom = 1 / (1 + 0.5 * alpha * I * Omega_k_r_zoom**2)

plt.figure(figsize=(10, 6))
plt.plot(r_zoom, t_local_r_zoom, color='darkgreen')
plt.title("Radial Profile of Local Time Dilation with Ωₖ ∝ 1/r²")
plt.xlabel("Radial Distance $r$ [m]")
plt.ylabel("Normalized Local Time $t_{local} / t_{abs}$")
plt.grid(True)
plt.tight_layout()
# ✅ Get the script filename dynamically
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}_Radial_LocalTime_Dilation.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

# Constants
C_e = 1.09384563e6        # m/s
rho_ae = 7e-7             # kg/m^3
r_c = 1.40897017e-15      # m
c = 2.99792458e8          # m/s
G = 6.67430e-11           # m^3/kg/s^2

# Derived constants
alpha = (r_c**2) / (C_e**2)  # s^2
I = 1e-20  # rotational inertia scaling for consistency if needed

# Define a femtometer-scale 2D grid
x = np.linspace(-5e-15, 5e-15, 400)  # ~10 fm across
y = np.linspace(-5e-15, 5e-15, 400)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

# Apply a softening factor to avoid division by zero
epsilon = 1e-20
Omega_k_2D = C_e / (R + epsilon)

# Heuristic model (no rotational inertia used here)
t_local_2D = 1 / (1 + alpha * Omega_k_2D**2)

# Plotting the 2D time well at femtometer scale
plt.figure(figsize=(8, 6))
contour = plt.contourf(X * 1e15, Y * 1e15, t_local_2D, levels=50, cmap='viridis')
cbar = plt.colorbar(contour)
cbar.set_label("Local Time $t_{local} / t_{abs}$")
plt.title("Vortex-Induced Time Well (Femtometer Scale)")
plt.xlabel("x [fm]")
plt.ylabel("y [fm]")
plt.axis('equal')
plt.grid(True)
plt.tight_layout()

filename = f"{script_name}_Vortex-Induced_Time_Well.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()