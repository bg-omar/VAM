import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Grid definition
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)

# Define stream function for dipole (with M < 0)
epsilon = 1e-5
r2 = X**2 + Y**2 + epsilon
psi = -Y / r2  # Negative dipole (M < 0)

# Create figure and axis
fig, ax = plt.subplots(figsize=(5, 5))

# Streamlines (contours of psi)
contours = ax.contour(X, Y, psi, levels=np.linspace(-2, 2, 17), colors='black', linewidths=1)

# Highlight psi = 0 lines
ax.contour(X, Y, psi, levels=[0], colors='black', linewidths=2)

# Axes
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

# Labels
ax.text(1.1, 0.1, r'$\Psi = 0$', fontsize=12)
ax.text(-1.5, 0.1, r'$\Psi = 0$', fontsize=12)
ax.text(1.55, 0.05, r'$x$', fontsize=12)
ax.text(0.05, 1.55, r'$y$', fontsize=12)

# Title
ax.set_title(r'Figuur 2.6: Dipool in de oorsprong ($M < 0$)', fontsize=10)

# Formatting
ax.set_aspect('equal')
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.axis('off')

plt.tight_layout()
plt.savefig("dipoleOorsprong.png", dpi=300)


################################################################

import numpy as np
import matplotlib.pyplot as plt

# Define grid
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)

# Avoid division by zero at origin
epsilon = 1e-5
r2 = X**2 + Y**2 + epsilon

# Velocity field for dipole (M < 0)
U = -(X**2 - Y**2) / r2**2
V = -(2 * X * Y) / r2**2

# Mask the singularity at the center
mask = r2 < 0.05
U[mask] = np.nan
V[mask] = np.nan

# Stream function (psi) for overlaying a contour
psi = -Y / r2

# Plot streamlines
fig, ax = plt.subplots(figsize=(5, 5))
ax.streamplot(X, Y, U, V, color='black', density=1, linewidth=1)

# Overlay the psi = 0 contour
ax.contour(X, Y, psi, levels=[0], colors='black', linewidths=2, linestyles='dashed')

# Axes and labels
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)
ax.text(1.1, 0.1, r'$\Psi = 0$', fontsize=12)
ax.text(-1.5, 0.1, r'$\Psi = 0$', fontsize=12)
ax.text(1.55, 0.05, r'$x$', fontsize=12)
ax.text(0.05, 1.55, r'$y$', fontsize=12)

# Title and formatting
ax.set_title(r'Figuur 2.6 (streamplot): Dipool in de oorsprong ($M < 0$)', fontsize=10)
ax.set_aspect('equal')
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.axis('off')

plt.tight_layout()
plt.savefig("dipoleOorsprong2.png", dpi=300)
plt.show()