


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import os
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
script_name = os.path.splitext(os.path.basename(__file__))[0]

def saving(plot):
    filename = f"{script_name}.png"
    plot.savefig(filename, dpi=150)  # Save image with high resolution

num_turns=10
num_points=1000

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



import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ========== Magnetic Field Utilities ==========
def magnetic_field_dipole(r, m):
    mu0 = 1.0  # normalized
    norm_r = np.linalg.norm(r)
    if norm_r < 1e-8:
        return np.zeros(3)
    r_hat = r / norm_r
    return (mu0 / (4 * np.pi * norm_r**3)) * (3 * np.dot(m, r_hat) * r_hat - m)

# ========== Dipole Configuration ==========
def compute_focused_dipole_orientations(num_magnets, f, radius):
    positions, orientations = [], []
    for i in range(num_magnets):
        phi = 2 * np.pi * i / num_magnets
        x, y, z = radius * np.cos(phi), radius * np.sin(phi), 0.0
        positions.append(np.array([x, y, z]))

        # Dipole vector: 720° in XY, cosine tilt in Z
        mx = np.cos(2 * phi)
        my = np.sin(2 * phi)
        mz = np.cos(phi)
        m = np.array([mx, my, mz])
        m /= np.linalg.norm(m)
        orientations.append(m)
    return positions, orientations

# ========== Compute Magnetic Field from Dipoles ==========

def compute_dipole_field_from_orientations(X, Y, Z, positions, orientations):
    Bx, By, Bz = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)
    for pos, m in zip(positions, orientations):
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                for k in range(X.shape[2]):
                    r = np.array([X[i, j, k], Y[i, j, k], Z[i, j, k]]) - pos
                    B = magnetic_field_dipole(r, m)
                    Bx[i, j, k] += B[0]
                    By[i, j, k] += B[1]
                    Bz[i, j, k] += B[2]
    return Bx, By, Bz


winding_colors = np.linspace(0, 1, num_magnets, endpoint=False)
# ========== Parameters ==========
num_magnets = 16
radius = 1.2
f_focus = 1.0

# Grid
x_range = (-2, 2)
y_range = (-2, 2)
z_range = (-2, 2)
X, Y, Z = np.meshgrid(np.linspace(*x_range, 11), np.linspace(*y_range, 11), np.linspace(*z_range, 11))

# Orientation
positions_focused, orientations_focused = compute_focused_dipole_orientations(num_magnets, f_focus, radius)
Bx, By, Bz = compute_dipole_field_from_orientations(X, Y, Z, positions_focused, orientations_focused)
magnitude = np.sqrt(Bx**2 + By**2 + Bz**2)
magnitude[magnitude == 0] = 1e-9
Bx_norm, By_norm, Bz_norm = Bx / magnitude, By / magnitude, Bz / magnitude

# ========== Plotting ==========
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, Bx_norm, By_norm, Bz_norm, length=0.15, normalize=True, color='blue', linewidth=0.25)

for pos, ori, c in zip(positions_focused, orientations_focused, winding_colors):
    # draw_correctly_aligned_cube(ax, pos, ori, size=0.3)
    arrow_start = pos - ori * 0.3
    ax.quiver(*arrow_start, *ori, length=0.6, color=plt.cm.hsv(c), linewidth=2, arrow_length_ratio=0.25, normalize=False)

ax.set_title('Verified Dipole-Aligned Cubes with Correct North/South Faces')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
ax.set_box_aspect([1, 1, 1])
plt.tight_layout()
saving(plt)
plt.show()
