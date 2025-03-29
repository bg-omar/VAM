import math
import os
import re
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


# Constants
C_e = 1.09384563e6        # m/s
rho_ae = 7e-7             # kg/m^3
r_c = 1.40897017e-15      # m
c = 2.99792458e8          # m/s
G = 6.67430e-11           # m^3/kg/s^2

# Derived constants
gamma = G * rho_ae**2     # m^5/s^2
kappa = C_e * r_c         # m^2/s
alpha = (r_c**2) / (C_e**2)  # s^2

# Radius range for evaluation
r_vals = np.logspace(-16, -12, 500)  # m
Omega_k_vals = C_e / r_vals

# Expressions to track when terms become negative
term_heuristic = 1 / (1 + alpha * Omega_k_vals**2)
term_gr_like = 1 - (2 * gamma * Omega_k_vals**2) / (r_vals * c**2)
term_kerr_like = 1 - (gamma * Omega_k_vals**2) / (r_vals * c**2) - (kappa**2) / (r_vals**3 * c**2)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(r_vals, term_heuristic, label="Heuristic Time Ratio", color='green')
plt.plot(r_vals, term_gr_like, label="GR-like Inner Expression", color='blue')
plt.plot(r_vals, term_kerr_like, label="Kerr-like Inner Expression", color='red')
plt.axhline(0, linestyle='--', color='black', linewidth=1)

plt.xscale('log')
plt.xlabel("Radius $r$ [m] (log scale)")
plt.ylabel("Expression Value")
plt.title("Critical Radius for Time Dilation Expressions")
plt.legend()
plt.grid(True)
plt.tight_layout()


# ✅ Get the script filename dynamically
script_name = os.path.splitext(os.path.basename(__file__))[0]
# ✅ **Create a Folder for Saving Frames**
save_folder = "export"
if not os.path.exists(save_folder):
    os.makedirs(save_folder, exist_ok=True)  # Ensure folder exists


filename = f"{script_name}1.png"


save_path = os.path.join(save_folder, filename)
plt.savefig(save_path, dpi=150)  # Save image with high resolution


# Constants
C_e = 1.09384563e6        # m/s
r_c = 1.40897017e-15      # m
alpha = (r_c**2) / (C_e**2)  # s^2

# Zoomed radius range near r_c
r_zoom = np.logspace(np.log10(r_c / 10), np.log10(r_c * 10), 500)
Omega_k_zoom = C_e / r_zoom
term_heuristic_zoom = 1 / (1 + alpha * Omega_k_zoom**2)

# Focused plot on the heuristic only
plt.figure(figsize=(8, 5))
plt.plot(r_zoom, term_heuristic_zoom, color='green', label="Heuristic Time Ratio")
plt.axvline(r_c, linestyle='--', color='gray', label=r"$r = r_c$")

plt.xscale('log')
plt.ylim(0.45, 1.01)
plt.xlabel("Radius $r$ [m] (log scale, near $r_c$)")
plt.ylabel(r"Time Ratio $t_{\text{local}} / t_{\text{abs}}$")
plt.title("Zoomed View: Heuristic Time Dilation Near Vortex Core")
plt.legend()
plt.grid(True)
plt.tight_layout()



filename = f"{script_name}2.png"


save_path = os.path.join(save_folder, filename)
plt.savefig(save_path, dpi=150)  # Save image with high resolution


# Zoom in: focus radius range near r_c (±2 orders of magnitude)
r_zoom = np.logspace(np.log10(r_c / 10), np.log10(r_c * 10), 500)
Omega_k_zoom = C_e / r_zoom
term_heuristic_zoom = 1 / (1 + alpha * Omega_k_zoom**2)
term_gr_like_zoom = 1 - (2 * gamma * Omega_k_zoom**2) / (r_zoom * c**2)
term_kerr_like_zoom = 1 - (gamma * Omega_k_zoom**2) / (r_zoom * c**2) - (kappa**2) / (r_zoom**3 * c**2)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(r_zoom, term_heuristic_zoom, label="Heuristic Time Ratio", color='green')
plt.plot(r_zoom, term_gr_like_zoom, label="GR-like Inner Expression", color='blue')
plt.plot(r_zoom, term_kerr_like_zoom, label="Kerr-like Inner Expression", color='red')
plt.axhline(0, linestyle='--', color='black', linewidth=1)
plt.axvline(r_c, linestyle='--', color='gray', label=r"$r = r_c$")

plt.xscale('log')
plt.xlabel("Radius $r$ [m] (log scale, zoomed near $r_c$)")
plt.ylabel("Expression Value")
plt.title("Zoomed: Time Dilation Expressions Near Vortex Core")
plt.legend()
plt.grid(True)
plt.tight_layout()

filename = f"{script_name}3.png"


save_path = os.path.join(save_folder, filename)
plt.savefig(save_path, dpi=150)  # Save image with high resolution

import numpy as np
import matplotlib.pyplot as plt

# Constants
C_e = 1.09384563e6        # m/s
r_c = 1.40897017e-15      # m
alpha = (r_c**2) / (C_e**2)  # s^2

# Zoomed radius range near r_c
r_zoom = np.logspace(np.log10(r_c / 10), np.log10(r_c * 10), 500)
Omega_k_zoom = C_e / r_zoom
term_heuristic_zoom = 1 / (1 + alpha * Omega_k_zoom**2)

# Focused plot on the heuristic only
plt.figure(figsize=(8, 5))
plt.plot(r_zoom, term_heuristic_zoom, color='green', label="Heuristic Time Ratio")
plt.axvline(r_c, linestyle='--', color='gray', label=r"$r = r_c$")

plt.xscale('log')
plt.ylim(0.45, 1.01)
plt.xlim(1e-15, 1e-14)
plt.xlabel("Radius $r$ [m] (log scale, near $r_c$)")
plt.ylabel(r"Time Ratio $t_{\text{local}} / t_{\text{abs}}$")
plt.title("Zoomed View: Heuristic Time Dilation Near Vortex Core")
plt.legend()
plt.grid(True)
plt.tight_layout()
filename = f"{script_name}4.png"

plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()


