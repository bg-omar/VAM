# Æther Vortex Simulation Framework
# Simulates vorticity field, pressure gradients, and local time modulation
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
G_val = 6.67430e-11             # m^3 kg^-1 s^-2
m_p_val = 1.67262192369e-27     # kg (mass of proton)
M_ns_val = 1.4 * 1.98847e30     # kg (mass of neutron star)
c_val = 2.99792458e8            # m/s

# Radius range (neutron star to outer space)
radii = np.linspace(1.2e4, 2e5, 1000)  # from NS surface outward

# Time dilation from GR
t_gr = np.sqrt(1 - (2 * G_val * M_ns_val) / (radii * c_val**2))

# Number of vortices = number of nucleons in neutron star
N_vortices_val = M_ns_val / m_p_val

# Use full proton mass per vortex
m_vortex_effective = m_p_val
M_total_vortex_corrected = m_vortex_effective * N_vortices_val

# Æther-based time dilation using full vortex mass
t_vortex_corrected = np.sqrt(1 - (2 * G_val * M_total_vortex_corrected) / (radii * c_val**2))
t_vortex_corrected = np.where(np.isreal(t_vortex_corrected), t_vortex_corrected, np.nan)
# Fix mathtext error in the labels by avoiding LaTeX-style \text{} and using plain text instead

# Main 2D plot
fig = plt.figure(figsize=(10, 6))
main_ax = fig.add_axes([0.1, 0.1, 0.75, 0.8])
main_ax.plot(radii / 1e3, t_gr, label="GR Time Dilation", color='black')
main_ax.plot(radii / 1e3, t_vortex_corrected, label="Æther Model ($M_\\text{vortex} = M_\\text{proton}$)", color='red', linestyle='--')
main_ax.set_xlabel("Radius from NS center [km]")
main_ax.set_ylabel("Normalized Time Rate")
main_ax.set_title("Time Dilation: GR vs Æther Model with Full Nucleon Mass per Vortex")
main_ax.grid(True)
main_ax.legend()

# Inset 3D plot
inset_ax = fig.add_axes([0.65, 0.15, 0.3, 0.4], projection='3d')
z_gr = np.zeros_like(radii)
z_ae = np.ones_like(radii)
inset_ax.plot(radii / 1e3, t_gr, z_gr, label="GR", color='black', linewidth=1)
inset_ax.plot(radii / 1e3, t_vortex_corrected, z_ae, label="VAM", color='red', linestyle='--', linewidth=1)
inset_ax.set_xlabel("r [km]")
inset_ax.set_ylabel("$t_\\text{local}$/$t_\\text{abs}$")
inset_ax.set_zlabel("0 = GR, 1 = VAM")
inset_ax.set_title("3D View", fontsize=10)
inset_ax.tick_params(labelsize=8)


# ✅ Get the script filename dynamically
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution


# Main 2D plot
fig = plt.figure(figsize=(10, 6))
main_ax = fig.add_axes([0.1, 0.1, 0.75, 0.8])
main_ax.plot(radii / 1e3, t_gr, label="GR Tijdsdilatatie", color='black')
main_ax.plot(radii / 1e3, t_vortex_corrected, label="Æther Model ($M_\\text{wervel} = M_\\text{proton}$)", color='red', linestyle='--')
main_ax.set_xlabel("Straal vanaf NS-centrum [km]")
main_ax.set_ylabel("Genormaliseerde tijdsnelheid")
main_ax.set_title("Tijdsdilatatie: GR versus Æthermodel met volledige nucleonmassa per Vortex")
main_ax.grid(True)
main_ax.legend()

# Inset 3D plot
inset_ax = fig.add_axes([0.65, 0.15, 0.3, 0.4], projection='3d')
z_gr = np.zeros_like(radii)
z_ae = np.ones_like(radii)
inset_ax.plot(radii / 1e3, t_gr, z_gr, label="GR", color='black', linewidth=1)
inset_ax.plot(radii / 1e3, t_vortex_corrected, z_ae, label="VAM", color='red', linestyle='--', linewidth=1)
inset_ax.set_xlabel("r [km]")
inset_ax.set_ylabel("$t_\\text{lokaal}$/$t_\\text{abs}$")
inset_ax.set_zlabel("0 = GR, 1 = VAM")
inset_ax.set_title("3D-weergave", fontsize=10)
inset_ax.tick_params(labelsize=8)


# ✅ Get the script filename dynamically
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}_nl.png"

plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()





