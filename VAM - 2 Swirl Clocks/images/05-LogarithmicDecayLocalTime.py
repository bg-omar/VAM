import os
import re
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
omega0 = 2e6
alpha = 1e-8
I = 1e-20
t_abs = 1

# Femtometer-scale grid
r_zoom_fm = np.linspace(1e-17, 1e-14, 500)
Omega_k_r_zoom_fm = 1e6 / r_zoom_fm**2
t_local_r_zoom_fm = t_abs / (1 + 0.5 * alpha * I * Omega_k_r_zoom_fm**2)
# Double-check that t_local has valid values up to 1
# and replot if needed using a larger range and ensuring smooth transition

# Expand the slice range further in case the threshold was too tight
extended_threshold_index = np.argmax(t_local_r_zoom_fm > 0.999)

# Fallback: if no values exceed threshold, take a portion that shows clear variation
if extended_threshold_index == 0:
    extended_threshold_index = 200  # manual cutoff

# Slice arrays for plotting
r_focus = r_zoom_fm[:extended_threshold_index + 1]
t_focus = t_local_r_zoom_fm[:extended_threshold_index + 1]

r_wide = np.logspace(-17, -11, 1000)  # From 10^-17 to 10^-11 meters
Omega_k_wide = 1e6 / r_wide**2
t_local_wide = 1 / (1 + 0.5 * alpha * I * Omega_k_wide**2)

# Plot with log scale and expanded radius
plt.figure(figsize=(10, 6))
plt.plot(r_wide * 1e15, t_local_wide, color='darkgreen')
plt.title("Radial Profile of Time Dilation with Ωₖ ∝ 1/r²")
plt.xlabel("Radial Distance $r$ [fm]")
plt.ylabel("Normalized Local Time $t_{local} / t_{abs}$")
plt.yscale('log')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()

# Plot with log scale and expanded radius
plt.figure(figsize=(10, 6))
plt.plot(r_wide * 1e15, t_local_wide, color='darkgreen')
plt.title("Radiaal profiel van tijdsdilatatie met Ωₖ ∝ 1/r²")
plt.xlabel("Radiale afstand $r$ [fm]")
plt.ylabel("Genormaliseerde lokale tijd $t_{lokaal} / t_{abs}$")
plt.yscale('log')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}_nl.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()