import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

num_turns=10
num_points=1000

# Reimporting necessary libraries after state reset
import os
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters
num_magnets = 16
radius = 1.5
turns = 2  # 720 degrees rotation over full circle

# Generate positions and orientations
positions = []
orientations = []

for i in range(num_magnets):
    phi = 2 * np.pi * i / num_magnets
    x, y, z = radius * np.cos(phi), radius * np.sin(phi), 0.0
    positions.append(np.array([x, y, z]))

    # Rotate vector in XY plane: full 720° over the 360° ring
    rot_angle = turns * phi
    ori_x, ori_y = np.cos(rot_angle), np.sin(rot_angle)
    orientations.append(np.array([ori_x, ori_y, 0.0]))

# Plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
for pos, ori in zip(positions, orientations):
    start = pos - ori * 0.2
    ax.quiver(*start, *ori, length=0.4, color='black', linewidth=2, arrow_length_ratio=0.25, normalize=False)

ax.set_title('Dipoles with 720° Rotation Over Ring (XY Plane)')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-1, 1.5)
ax.set_box_aspect([1, 1, 0.7])
plt.tight_layout()






from scipy.constants import mu_0

def compute_biot_savart_field(grid_x, grid_y, grid_z, dipole_positions, dipole_moments):
    Bx = np.zeros_like(grid_x)
    By = np.zeros_like(grid_y)
    Bz = np.zeros_like(grid_z)

    for r0, m in zip(dipole_positions, dipole_moments):
        rx = grid_x - r0[0]
        ry = grid_y - r0[1]
        rz = grid_z - r0[2]
        r_squared = rx**2 + ry**2 + rz**2 + 1e-9
        r_fifth = r_squared**2.5
        r_dot_m = rx * m[0] + ry * m[1] + rz * m[2]

        Bx += mu_0 / (4 * np.pi) * (3 * rx * r_dot_m - m[0] * r_squared) / r_fifth
        By += mu_0 / (4 * np.pi) * (3 * ry * r_dot_m - m[1] * r_squared) / r_fifth
        Bz += mu_0 / (4 * np.pi) * (3 * rz * r_dot_m - m[2] * r_squared) / r_fifth

    return Bx, By, Bz

# Generate a 2D grid above the ring
grid_size = 25
x = np.linspace(-2.5, 2.5, grid_size)
y = np.linspace(-2.5, 2.5, grid_size)
z = 0.75  # height above the magnet ring
X, Y = np.meshgrid(x, y)
Z = np.full_like(X, z)

# Compute the field from our 3D tilted dipoles
Bx, By, Bz = compute_biot_savart_field(X, Y, Z, positions, orientations)

# Normalize for quiver plotting
magnitude = np.sqrt(Bx**2 + By**2 + Bz**2)
mask = magnitude > 1e-13
Bx[~mask] = By[~mask] = 0
Bz[~mask] = 0
Bx /= magnitude + 1e-15
By /= magnitude + 1e-15

# Plot field slice
fig, ax = plt.subplots(figsize=(7, 7))
ax.quiver(X, Y, Bx, By, color='black', pivot='mid', scale=30, width=0.005)
ax.set_title('Magnetic Field Above Magnet Ring (Z = 0.75)')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_aspect('equal')
plt.tight_layout()




import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.constants import mu_0

# === Configuration ===
num_magnets = 16
radius = 1.5
grid_size = 25
arrow_length = 0.05
offset = 0.1
z_sample = 0.0

# === Dipole Ring Construction ===
positions = []
orientations = []

for i in range(num_magnets):
    phi = 2 * np.pi * i / num_magnets
    x, y, z = radius * np.cos(phi), radius * np.sin(phi), 0.0
    positions.append(np.array([x, y, z]))

    # 720° XY rotation + cosine Z tilt
    mx = np.cos(2 * phi)
    my = np.sin(2 * phi)
    mz = np.cos(phi)
    m = np.array([mx, my, mz])
    m /= np.linalg.norm(m)
    orientations.append(m)

# === Compute Biot-Savart Magnetic Field at z = 0.75 ===
x = np.linspace(-2.5, 2.5, grid_size)
y = np.linspace(-2.5, 2.5, grid_size)
X, Y = np.meshgrid(x, y)
Z = np.full_like(X, z_sample)

Bx = np.zeros_like(X)
By = np.zeros_like(Y)
Bz = np.zeros_like(Z)

for r0, m in zip(positions, orientations):
    rx = X - r0[0]
    ry = Y - r0[1]
    rz = Z - r0[2]
    r_squared = rx**2 + ry**2 + rz**2 + 1e-9
    r_fifth = r_squared**2.5
    r_dot_m = rx * m[0] + ry * m[1] + rz * m[2]

    Bx += mu_0 / (4 * np.pi) * (3 * rx * r_dot_m - m[0] * r_squared) / r_fifth
    By += mu_0 / (4 * np.pi) * (3 * ry * r_dot_m - m[1] * r_squared) / r_fifth
    Bz += mu_0 / (4 * np.pi) * (3 * rz * r_dot_m - m[2] * r_squared) / r_fifth

# Normalize for plotting
magnitude = np.sqrt(Bx**2 + By**2 + Bz**2)
mask = magnitude > 1e-13
Bx[~mask] = By[~mask] = Bz[~mask] = 0
Bx /= magnitude + 1e-15
By /= magnitude + 1e-15

# === Plot 3D Dipole Ring + Field Slice ===
winding_colors = np.linspace(0, 1, num_magnets, endpoint=False)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Dipole arrows
for pos, ori, c in zip(positions, orientations, winding_colors):
    start = pos - ori * offset
    ax.quiver(*start, *ori, length=arrow_length, color=plt.cm.hsv(c),
              linewidth=2, arrow_length_ratio=0.25, normalize=False)

# Magnetic field slice at z = 0.75
for i in range(0, grid_size, 2):
    for j in range(0, grid_size, 2):
        bx, by, bz = Bx[i, j], By[i, j], Bz[i, j]
        if np.linalg.norm([bx, by, bz]) > 0:
            ax.quiver(X[i, j], Y[i, j], z_sample, bx, by, bz,
                      length=0.5, color='black', linewidth=0.8,
                      arrow_length_ratio=0.2, normalize=True)

# Axis and layout
ax.set_title('3D Dipoles + Magnetic Field Above Ring (Z = 0.75)')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)
ax.set_zlim(-1.5, 2.0)
ax.set_box_aspect([1, 1, 0.8])
plt.tight_layout()


