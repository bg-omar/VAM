import matplotlib.pyplot as plt
import numpy as np

# Constants (VAM model)
rho_ae = 8.93e17  # kg/m^3 (æther density)
Gamma = 1.0       # circulation, arbitrary units
rc = 1.409e-15    # core radius in meters
c = 3e8           # speed of light in m/s

# Radial positions
r = np.logspace(-16, -10, 500)
pressure = np.where(r <= rc,
                    (rho_ae * Gamma**2 * r**2) / (8 * np.pi**2 * rc**4),
                    (rho_ae * Gamma**2) / (8 * np.pi**2 * r**2))

# Time dilation factor
time_dilation = 1 - pressure / (rho_ae * c**2)

# Plotting
# Zoom into the time dilation component by using a secondary axis to improve contrast

fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel("Radius $r$ [m]")
ax1.set_xscale('log')
ax1.set_ylabel("Pressure $P(r)$ [GPa]", color=color)
ax1.plot(r , pressure * 1e-9, color=color, lw=2, label="Pressure")
ax1.tick_params(axis='y', labelcolor=color)

# Create a second y-axis for time dilation
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel("Time dilation $d\\tau/dt$", color=color)
ax2.plot(r, time_dilation, color=color, lw=2, label="Time Dilation")
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title("Pressure and Time Dilation vs Radius in VAM")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()


