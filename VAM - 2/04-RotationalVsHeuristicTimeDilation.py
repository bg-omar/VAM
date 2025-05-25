import os
import re
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


# Define zoomed-in radial range
r_zoom = np.linspace(0.00001, 0.0002, 500)
Omega_k_r_zoom = 1e6 / r_zoom**2

# Constants for both models
alpha_rot = 1e-8
I_rot = 1e-20

# Rotational model: includes moment of inertia
t_rot = 1 / (1 + 0.5 * alpha_rot * I_rot * Omega_k_r_zoom**2)

# Heuristic model: no inertia term
alpha_heuristic = alpha_rot * I_rot
t_heuristic = 1 / (1 + alpha_heuristic * Omega_k_r_zoom**2)

# Plot comparison
plt.figure(figsize=(10, 6))
plt.plot(r_zoom * 1e6, t_rot, label="Rotational Energy Model", color='darkgreen')
plt.plot(r_zoom * 1e6, t_heuristic, label="Heuristic Model", color='orange', linestyle='--')
plt.xlabel("Radial Distance $r$ [$\mu$m]")
plt.ylabel("Normalized Local Time $t_{local} / t_{abs}$")
plt.title("Comparison: Heuristic vs Rotational Time Dilation (Ωₖ ∝ 1/r²)")
plt.grid(True)
plt.legend()
plt.tight_layout()
# ✅ Get the script filename dynamically
script_name = os.path.splitext(os.path.basename(__file__))[0]
# ✅ **Create a Folder for Saving Frames**
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution


# Plot comparison
plt.figure(figsize=(10, 6))
plt.plot(r_zoom * 1e6, t_rot, label="Rotatie-energiemodel", color='darkgreen')
plt.plot(r_zoom * 1e6, t_heuristic, label="Heuristisch model", color='orange', linestyle='--')
plt.xlabel("Radiale afstand $r$ [$\mu$m]")
plt.ylabel("Genormaliseerde lokale tijd $t_{lokaal} / t_{abs}$")
plt.title("Vergelijking: Heuristische vs. Rotatie Tijddilatatie (Ωₖ ∝ 1/r²)")
plt.grid(True)
plt.legend()
plt.tight_layout()
# ✅ Get the script filename dynamically
script_name = os.path.splitext(os.path.basename(__file__))[0]
# ✅ **Create a Folder for Saving Frames**
filename = f"{script_name}_nl.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()