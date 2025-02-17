import numpy as np
import matplotlib.pyplot as plt

# Define parameters
Rc = 1  # Coulomb barrier radius (normalized)
a0 = 3  # Bohr radius (normalized, larger scale for visualization)
r = np.linspace(0, 5 * a0, 400)  # Radial distance

# Define vortex swirl function (exponential decay beyond Rc)
def vortex_swirl(r, Rc, a0):
    return np.where(r < Rc, 0.2, np.exp(-(r - Rc) / a0))

# Compute swirl intensity
swirl = vortex_swirl(r, Rc, a0)

# Plot the diagram
fig, ax = plt.subplots(figsize=(8, 6))

# Background swirl regions
ax.fill_between(r, 0, swirl, where=(r < Rc), color="lightgray", alpha=0.6, label="Core (low swirl)")
ax.fill_between(r, 0, swirl, where=(r >= Rc), color="orange", alpha=0.5, label="Activated Vortex")

# Draw important lines
ax.axvline(Rc, color="black", linestyle="--", label="Coulomb Barrier ($R_c$)")
ax.annotate("Core Region (Low Swirl)", xy=(0.2, 0.1), fontsize=10, color="black")
ax.annotate("Vortex Turns On", xy=(Rc + 0.2, 0.4), fontsize=10, color="black")
ax.annotate("Exponential Decay Region", xy=(a0 * 2, 0.2), fontsize=10, color="black")

# Labels and appearance
ax.set_xlabel("Radial Distance $r$", fontsize=12)
ax.set_ylabel("Vortex Swirl Intensity", fontsize=12)
ax.set_title("1s Orbital as a Spherically Symmetric Vortex in VAM", fontsize=14)
ax.legend()
ax.grid()

# Show the plot
plt.show()