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


# Recalculate vortex schematic with Ω_k(R) ∝ 1/R²
epsilon = 0.01  # to prevent division by zero
Omega_k_2D = 1e6 / (R**2 + epsilon)
t_local_2D = 1 / (1 + 0.5 * alpha * I * Omega_k_2D**2)
# Varying Omega_k with radius: assume Ω_k ∝ 1/r^2 (core rotation decays with radius)
r = np.linspace(0.01, 1.0, 500)  # avoid r = 0
Omega_k_r = 1e6 / r**2           # example vortex profile
alpha = 1e-8
I = 1e-20

# Time dilation as function of r
t_local_r = 1 / (1 + 0.5 * alpha * I * Omega_k_r**2)

# Zoom in the 2D vortex well around center: crop to region [-0.2, 0.2]
zoom_idx = np.logical_and(np.abs(x) <= 0.2, True)
X_zoom, Y_zoom = np.meshgrid(x[zoom_idx], y[zoom_idx])
R_zoom = np.sqrt(X_zoom**2 + Y_zoom**2)
Omega_k_zoom = 1e6 / (R_zoom**2 + epsilon)
t_local_zoom = 1 / (1 + 0.5 * alpha * I * Omega_k_zoom**2)

plt.figure(figsize=(8, 6))
contour_zoom = plt.contourf(X_zoom, Y_zoom, t_local_zoom, levels=50, cmap='viridis')
cbar = plt.colorbar(contour_zoom)
cbar.set_label("Local Time $t_{local} / t_{abs}$")
plt.title("Schematic of Vortex-Induced Time Well (Ωₖ ∝ 1/R²)")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.axis('equal')
plt.grid(True)
plt.tight_layout()


# ✅ Get the script filename dynamically
script_name = os.path.splitext(os.path.basename(__file__))[0]
# ✅ **Create a Folder for Saving Frames**
save_folder = "export"
if not os.path.exists(save_folder):
    os.makedirs(save_folder, exist_ok=True)  # Ensure folder exists

# Generate a unique filename using timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{script_name}_Vortex-Induced_Time_Well.png"



save_path = os.path.join(save_folder, filename)
plt.savefig(save_path, dpi=150)  # Save image with high resolution

plt.show()