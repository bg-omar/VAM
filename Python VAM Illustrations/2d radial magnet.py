
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Torus parameters
R = 2  # major radius
r = 0.5  # minor radius
n = 20  # resolution

# Meshgrid in parametric space
u = np.linspace(0, 2*np.pi, n)
v = np.linspace(0, 2*np.pi, n)
u, v = np.meshgrid(u, v)

# Toroidal surface points
X = (R + r * np.cos(v)) * np.cos(u)
Y = (R + r * np.cos(v)) * np.sin(u)
Z = r * np.sin(v)

# Compute radial vectors (from origin to surface point)
BX = X
BY = Y
BZ = Z
# Normalize vectors
mag = np.sqrt(BX**2 + BY**2 + BZ**2)
BX /= mag
BY /= mag
BZ /= mag

# Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot torus surface
ax.plot_surface(X, Y, Z, alpha=0.2, color='gray', rstride=1, cstride=1, linewidth=0)

# Plot radial vectors
ax.quiver(X, Y, Z, BX, BY, BZ, length=0.3, normalize=True, color='crimson')

# Aesthetics
ax.set_box_aspect([1,1,1])
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([-1.5, 1.5])
ax.set_title("Radial Magnetic Field Vectors Along a Toroidal Surface")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.tight_layout()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Dipole field function
def dipole_field(r, m, r0):
    """Magnetic field from a dipole with moment m at position r0, evaluated at r"""
    mu0 = 4*np.pi*1e-7
    R = r - r0
    norm_R = np.linalg.norm(R, axis=-1)[..., np.newaxis]
    norm_R[norm_R == 0] = 1e-20  # Avoid division by zero
    term1 = 3 * R * np.sum(m * R, axis=-1)[..., np.newaxis] / (norm_R**5)
    term2 = m / (norm_R**3)
    B = (mu0 / (4*np.pi)) * (term1 - term2)
    return B

# Grid for field evaluation
x = np.linspace(-1, 1, 10)
y = np.linspace(-1, 1, 10)
z = np.linspace(-0.2, 0.2, 3)
X, Y, Z = np.meshgrid(x, y, z)
points = np.stack([X, Y, Z], axis=-1)

# Coil ring configuration
N_coils = 12
R_ring = 1.5
coil_positions = []
coil_moments = []

for i in range(N_coils):
    theta = 2 * np.pi * i / N_coils
    pos = np.array([R_ring * np.cos(theta), R_ring * np.sin(theta), 0.0])
    direction = -pos / np.linalg.norm(pos)  # Point toward center
    coil_positions.append(pos)
    coil_moments.append(1e-3 * direction)  # Dipole magnitude scaled

# Compute total magnetic field
B_total = np.zeros_like(points)
for pos, m in zip(coil_positions, coil_moments):
    B = dipole_field(points, m, pos)
    B_total += B

# Extract vectors
BX, BY, BZ = B_total[..., 0], B_total[..., 1], B_total[..., 2]
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}3.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

# Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, BX, BY, BZ, length=0.2, normalize=True, color='navy')

# Plot coil locations
for pos in coil_positions:
    ax.scatter(*pos, color='red', s=50)

ax.set_title("Radial Magnetic Field from Circular Coil Array (Dipoles Aimed at Center)")
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-0.5, 0.5])
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

# Re-run necessary imports after state reset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Magnetic field due to a dipole at position r0 with moment m
def dipole_field(r, m, r0):
    mu0 = 4 * np.pi * 1e-7
    R = r - r0
    norm_R = np.linalg.norm(R, axis=-1)[..., np.newaxis]
    norm_R[norm_R == 0] = 1e-20  # Avoid division by zero
    term1 = 3 * R * np.sum(m * R, axis=-1)[..., np.newaxis] / (norm_R**5)
    term2 = m / (norm_R**3)
    B = (mu0 / (4 * np.pi)) * (term1 - term2)
    return B

# Parameters
N_coils = 12
R_ring = 1.1
coil_positions = []
coil_moments = []

# Dipole configuration (radial inward)
for i in range(N_coils):
    theta = 2 * np.pi * i / N_coils
    pos = np.array([R_ring * np.cos(theta), R_ring * np.sin(theta), 0.0])
    direction = -pos / np.linalg.norm(pos)  # Point toward center
    coil_positions.append(pos)
    coil_moments.append(1e-3 * direction)  # Dipole magnitude scaled

# 3D grid for visualization
grid_size = 10
span = 1.0
lin = np.linspace(-span, span, grid_size)
X, Y, Z = np.meshgrid(lin, lin, lin)
points = np.stack([X, Y, Z], axis=-1)

# Calculate total magnetic field
B_total = np.zeros_like(points)
for pos, m in zip(coil_positions, coil_moments):
    B = dipole_field(points, m, pos)
    B_total += B

# Extract field components
BX, BY, BZ = B_total[..., 0], B_total[..., 1], B_total[..., 2]

# Downsample for quiver clarity
step = 2
Xq = X[::step, ::step, ::step]
Yq = Y[::step, ::step, ::step]
Zq = Z[::step, ::step, ::step]
BXq = BX[::step, ::step, ::step]
BYq = BY[::step, ::step, ::step]
BZq = BZ[::step, ::step, ::step]

# Plot vector field
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(Xq, Yq, Zq, BXq, BYq, BZq, length=0.1, normalize=True, color='navy')

ax.set_title("Net Magnetic Field from 12 Dipoles in Ring Configuration")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(-span, span)
ax.set_ylim(-span, span)
ax.set_zlim(-span, span)
ax.set_box_aspect([1, 1, 1])
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()

