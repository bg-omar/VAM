import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11         # gravitational constant [m^3 kg^-1 s^-2]
c = 2.99792458e8        # speed of light [m/s]
M_sun = 1.98847e30      # solar mass [kg]

# Mass of compact object for benchmark
M = 10 * M_sun

# Schwarzschild ISCO (GR prediction)
r_isco_gr = 6 * G * M / c**2

# VAM critical radius where v_phi = c
r_crit_vam = G * M / c**2

# Extended VAM ISCO: propose instability appears at ~6x r_crit
r_isco_vam = 6 * r_crit_vam

# Radius array for plotting
r = np.linspace(0.5 * r_crit_vam, 10 * r_crit_vam, 1000)

# Specific angular momentum (assume test particle in orbit)
L = np.sqrt(G * M * r)

# Circulation quantum (approximation for benchmark)
kappa = 1.54e-9  # m^2/s from VAM

# Effective potential GR-like (purely for comparison, L^2 / 2r^2 - GM/r)
Veff_gr = L**2 / (2 * r**2) - G * M / r

# Effective potential VAM-like (L^2 / 2r^2 - swirl energy + shear term)
gamma = 1e-44  # heuristic tuning parameter
omega = kappa / r**2
domega_dr = -2 * kappa / r**3
shear_term = gamma * domega_dr**2

Veff_vam = L**2 / (2 * r**2) - 0.5 * (kappa**2 / r**2) - shear_term

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(r * 1e-3, Veff_gr, label="GR Effective Potential", linewidth=2)
plt.plot(r * 1e-3, Veff_vam, label="VAM Effective Potential", linestyle='--', linewidth=2)
plt.axvline(r_isco_gr * 1e-3, color='blue', linestyle=':', label="GR ISCO (%.1f km)" % (r_isco_gr * 1e-3))
plt.axvline(r_isco_vam * 1e-3, color='orange', linestyle=':', label="VAM ISCO (%.1f km)" % (r_isco_vam * 1e-3))

plt.xlabel("Radial Distance r [km]")
plt.ylabel("Effective Potential per unit mass [J/kg]")
plt.title("Effective Potential Comparison: GR vs VAM")
plt.legend()
plt.grid(True)
plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# # plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()
