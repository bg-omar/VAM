# Re-import necessary libraries after kernel reset
import numpy as np
import matplotlib.pyplot as plt

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

# Plot the result
plt.figure(figsize=(10, 6))
plt.plot(radii / 1e3, t_gr, label="GR Time Dilation", color='black')
plt.plot(radii / 1e3, t_vortex_corrected, label="Æther Model (m_vortex = m_p)", color='red', linestyle='--')
plt.xlabel("Radius from NS center [km]")
plt.ylabel("Normalized Time Rate")
plt.title("Time Dilation: GR vs Æther Model with Full Nucleon Mass per Vortex")
plt.grid(True)
plt.legend()
plt.tight_layout()
from mpl_toolkits.mplot3d import Axes3D

# Create 3D plot to show both curves clearly
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Add both lines in separate planes to visualize them distinctly
z_gr = np.zeros_like(radii)
z_ae = np.ones_like(radii)

# Plot GR curve
ax.plot(radii / 1e3, t_gr, z_gr, label="GR Time Dilation", color='black', linewidth=2)

# Plot Æther model curve in a parallel z-plane
ax.plot(radii / 1e3, t_vortex_corrected, z_ae, label="Æther Model (m_vortex = m_p)", color='red', linestyle='--', linewidth=2)

# Axes labels
ax.set_xlabel("Radius from NS center [km]")
ax.set_ylabel("Normalized Time Rate")
ax.set_zlabel("Model Index (0 = GR, 1 = Æther)")
ax.set_title("3D Comparison: GR vs Æther Model (Time Dilation)")
ax.legend()
plt.tight_layout()
plt.show()

