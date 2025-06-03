import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Constants
G = 6.67430e-11          # Gravitational constant (m^3 kg^-1 s^-2)
c = 3.0e8                # Speed of light (m/s)
M = 1.4 * 1.9885e30      # Mass of neutron star (kg)
r_min = 1.1 * 12e3       # Avoid singularity at exact radius
r_max = 100e3            # Max radial distance (m)

# Radial distances
r = np.linspace(r_min, r_max, 500)

# GR time dilation
tau_gr = np.sqrt(1 - (2 * G * M) / (r * c**2))

# VAM time dilation based on escape velocity
v = np.sqrt((2 * G * M) / r)
tau_vam = 1 / (1 / np.sqrt(1 - (v**2 / c**2)))  # inverse gamma

# Plotting
plt.figure(figsize=(8, 5))
plt.plot(r / 1000, tau_gr, label="General Relativity", linewidth=2)
plt.plot(r / 1000, tau_vam, '--', label="Vortex Æther Model", linewidth=2)

plt.xlabel("Radial Distance from Center (km)")
plt.ylabel("Normalized Proper Time (dτ/dt)")
plt.title("Gravitational Time Dilation: GR vs VAM")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()