import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LogLocator, FuncFormatter
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Define radial domain (logarithmic to show wide scale behavior)
r = np.logspace(-15, -3, 1000)  # meters from 1 fm to 1 mm

# Define scale-dependent density profile
# High density near core, asymptotically low at large scale
rho_core = 3.89e18  # core density in kg/m^3
rho_far = 1e-7      # macroscopic æther density in kg/m^3

# Transition function: exponential decay (sigmoid-like)
transition_radius = 1e-12  # characteristic decay radius
rho = rho_far + (rho_core - rho_far) * np.exp(-r / transition_radius)

# Custom tick formatter
def scientific_fmt(x, _):
    return r"$10^{{{}}}$".format(int(np.log10(x))) if x != 0 else "0"

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(r, rho, color='indigo', lw=2)  # Convert x-axis to femtometers

# Labels and styling
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Radiale afstand r (m)', fontsize=12)
ax.set_ylabel('Ætherdichtheid ρₐ (kg/m³)', fontsize=12)
ax.set_title('Schaalafhankelijke Ætherdichtheid in VAM $ \\rho_\\text{\\ae} (r) = \\rho_\\text{far} + (\\rho_\\text{core} - \\rho_\\text{far}) e^{-r / r_*} $', fontsize=14)
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# Log-ticks met custom formatter
ax.xaxis.set_major_locator(LogLocator(base=10.0, subs=(1.0,), numticks=12))
ax.xaxis.set_major_formatter(FuncFormatter(scientific_fmt))

# Inset for dense core
inset_ax = fig.add_axes([0.55, 0.5, 0.35, 0.35])
inset_r = np.logspace(-15, -13, 300)
inset_rho = rho_far + (rho_core - rho_far) * np.exp(-inset_r / transition_radius)
inset_ax.plot(inset_r, inset_rho, color='crimson', lw=2)
inset_ax.set_xscale('log')
inset_ax.set_yscale('log')
inset_ax.set_title('Zoom: Dichte kern', fontsize=10)
inset_ax.set_xlabel('r (m)', fontsize=8)
inset_ax.set_ylabel('ρₐ (kg/m³)', fontsize=8)
inset_ax.tick_params(axis='both', which='major', labelsize=8)
inset_ax.grid(True, which='both', linestyle=':', linewidth=0.5)

plt.tight_layout()

import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}_nl.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()
