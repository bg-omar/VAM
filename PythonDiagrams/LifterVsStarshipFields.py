import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

# Setup: 2D field line visualizations for (1) Lifter and (2) Starship coil analog

# Create 2D grid
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)
r = np.sqrt(X**2 + Y**2)
theta = np.arctan2(Y, X)

# --- 1. Lifter-like E-field ---
# Simulate radial field from a point source (wire) to a grounded plane (foil)
E_r_lifter = 1 / (r + 0.1)**2
Ex_lifter = E_r_lifter * np.cos(theta)
Ey_lifter = E_r_lifter * np.sin(theta)

# --- 2. Starship coil-like rotating vortex field ---
# Simulate azimuthal (tangential) field lines like a vortex ring
E_theta_starship = 1 / (r + 0.1)
Ex_starship = -E_theta_starship * np.sin(theta)
Ey_starship = E_theta_starship * np.cos(theta)

# Plotting
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Lifter plot
axs[0].streamplot(X, Y, Ex_lifter, Ey_lifter, color='blue', density=1.2)
axs[0].set_title("Lifter-Like Field: Wire to Foil")
axs[0].set_aspect('equal')
axs[0].set_xlim(-2, 2)
axs[0].set_ylim(-2, 2)
axs[0].plot(0, 0, 'ro', label='Wire (+)')
axs[0].axhline(-1.5, color='gray', linestyle='--', label='Foil (-)')
axs[0].legend()

# Starship coil plot
axs[1].streamplot(X, Y, Ex_starship, Ey_starship, color='purple', density=1.2)
axs[1].set_title("Starship Coil-Like Field: Rotating Vortex")
axs[1].set_aspect('equal')
axs[1].set_xlim(-2, 2)
axs[1].set_ylim(-2, 2)
axs[1].plot(0, 0, 'ko', label='Coil Center')
axs[1].legend()

plt.suptitle("Field Line Comparison: Lifter vs Starship Coil (VAM Interpretation)", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.95])


# Create 3D grid
x = np.linspace(-2, 2, 20)
y = np.linspace(-2, 2, 20)
z = np.linspace(-1, 1, 8)
X, Y, Z = np.meshgrid(x, y, z)
R = np.sqrt(X**2 + Y**2)
Theta = np.arctan2(Y, X)

# Define a toroidal vector field (vortex-like)
# Tangential vector around z-axis, confined in radial direction
strength = np.exp(-((R - 1)**2 + Z**2))  # ring-shaped confinement around radius=1
U = -strength * np.sin(Theta)  # X-component of vortex
V = strength * np.cos(Theta)   # Y-component
W = np.zeros_like(U)           # No vertical motion in this simplified shell

# 3D vector field plot (quiver)
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
skip = (slice(None, None, 2), slice(None, None, 2), slice(None, None, 1))
ax.quiver(X[skip], Y[skip], Z[skip], U[skip], V[skip], W[skip], length=0.15, normalize=True, color='purple')

# Aesthetics
ax.set_title("Starship Coil VAM Field: 3D Toroidal Vortex Flow")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-1, 1])
ax.set_box_aspect([1,1,0.5])
plt.tight_layout()
plt.show()