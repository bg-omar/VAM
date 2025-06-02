
import numpy as np
import matplotlib.pyplot as plt

# Define grid
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)

# Source field
epsilon = 1e-5
r2 = X**2 + Y**2 + epsilon
U = X / r2
V = Y / r2

# Potential Φ and Streamfunction Ψ for a source
phi = 0.5 * np.log(r2)
psi = np.arctan2(Y, X)

# Mask the singularity at the center
mask = r2 < 0.05
U[mask] = np.nan
V[mask] = np.nan

# Plot
fig, ax = plt.subplots(figsize=(5, 5))

# Streamlines (Ψ = const.)
ax.contour(X, Y, psi, levels=np.linspace(-np.pi, np.pi, 12), colors='black', linestyles='solid')

# Equipotential lines (Φ = const.)
ax.contour(X, Y, phi, levels=6, colors='black', linestyles='dashed')

# Axes
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

# Labels
ax.text(1.0, 0.3, r'$\Psi = \text{const.}$', fontsize=12)
ax.text(0.4, -1.0, r'$\Phi = \text{const.}$', fontsize=12)
ax.text(1.6, 0.05, r'$x$', fontsize=12)
ax.text(0.05, 1.6, r'$y$', fontsize=12)

# Title
ax.set_title(r'Figuur 2.4: Bron in de oorsprong.', fontsize=10)

# Formatting
ax.set_aspect('equal')
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.axis('off')

plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()