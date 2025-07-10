import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
# ✅ Get the script filename dynamically and save as pdf
import os

script_name = os.path.splitext(os.path.basename(__file__))[0]
# Save with incrementing filename if file exists, restart count on rerun
base_filename = f"{script_name}.png"
filename = base_filename
count = 1

# Constants (user-defined)
C_e = 1093845.63            # vortex tangential velocity [m/s]
F_max = 29.053507           # maximum æther force [N]
r_c = 1.40897017e-15        # vortex core radius [m]
rho_ae = 7.0e-7             # æther vacuum density [kg/m^3]

# Define radial range
r_vals = np.logspace(-14, -6, 500)  # from ~core radius to larger scale

# VAM swirl potential:
# Phi(r) = (C_e^2 / (2 F_max)) * (omega * r), using exponential vortex profile
# omega(r) = C_e / r_c * exp(-r/r_c)
omega_r = (C_e / r_c) * np.exp(-r_vals / r_c)
Phi_r = (C_e**2 / (2 * F_max)) * omega_r * r_vals

# GR Schwarzschild potential: Phi(r) = -G M / r (for reference)
G = 6.67430e-11  # m^3 kg^-1 s^-2
M = 1.67262192369e-27 * 1e57  # ~10^57 protons, rough galactic core
Phi_GR = -G * M / r_vals

# Plot comparison
plt.figure(figsize=(8, 6))
plt.loglog(r_vals, np.abs(Phi_r), label="VAM Swirl Potential", linewidth=2)
plt.loglog(r_vals, np.abs(Phi_GR), '--', label="GR Schwarzschild Potential", linewidth=2)
plt.xlabel("Radial distance $r$ [m]")
plt.ylabel("Potential $|\\Phi(r)|$ [J/kg]")
plt.title("Benchmark 9: VAM vs GR Gravitational Potential")
plt.legend()
plt.grid(True, which="both", ls=":")
plt.tight_layout()
while os.path.exists(filename):
    filename = f"{script_name}_{count}.png"
    count += 1
plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()

