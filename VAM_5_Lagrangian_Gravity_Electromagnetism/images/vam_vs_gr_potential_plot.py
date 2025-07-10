import numpy as np
import matplotlib.pyplot as plt

# Constants from VAM
C_e = 1.09384563e6  # m/s
r_c = 1.40897017e-15  # m
F_max = 29.053507  # N
G = 6.67430e-11  # m^3/kg/s^2
M = 1.67262192369e-27  # kg (proton mass for comparison)

# Range for r (in meters)
r = np.logspace(-17, -13, 500)  # from near-zero to several r_c

# VAM potential
omega_vam = (C_e / r_c) * np.exp(-r / r_c)
phi_vam = (C_e**2 / (2 * F_max)) * omega_vam * r  # = C_e^3 / (2 F_max r_c) * r * e^{-r/r_c}

# GR potential
phi_gr = -G * M / r

# Normalize both potentials for comparison
phi_vam_norm = phi_vam / np.max(np.abs(phi_vam))
phi_gr_norm = phi_gr / np.max(np.abs(phi_gr))

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(r, phi_vam_norm, label='VAM Swirl Potential', color='blue')
plt.plot(r, phi_gr_norm, label='GR Schwarzschild Potential', color='red', linestyle='--')

plt.xscale('log')
plt.xlabel('Radius $r$ (m)')
plt.ylabel('Normalized Gravitational Potential')
plt.title('VAM vs GR Gravitational Potential')
plt.legend()
plt.grid(True, which='both', ls='--', lw=0.5)

# Save the figure
output_path = "vam_vs_gr_potential_plot.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()
