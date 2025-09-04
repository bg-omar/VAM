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

# ========== Magnetic Field Utilities ==========
def magnetic_field_dipole(r, m):
    mu0 = 1.0  # normalized
    norm_r = np.linalg.norm(r)
    if norm_r < 1e-8:
        return np.zeros(3)
    r_hat = r / norm_r
    return (mu0 / (4 * np.pi * norm_r**3)) * (3 * np.dot(m, r_hat) * r_hat - m)

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

def generate_dipole_ring(radius, num_magnets, z_offset=0.0, invert=False):
    positions = []
    orientations = []
    for i in range(num_magnets):
        phi = 2 * np.pi * i / num_magnets
        x, y, z = radius * np.cos(phi), radius * np.sin(phi), z_offset
        mx = np.cos(2 * phi)
        my = np.sin(2 * phi)
        mz = np.cos(phi)
        m = np.array([mx, my, (-1 if invert else 1) * mz])
        m /= np.linalg.norm(m)
        orientations.append(m)
        positions.append(np.array([x, y, z]))
    return positions, orientations

# --- Rodin Starship Coil Geometry ---
def generate_rodin_starship(R=1.0, r=1.0, num_turns=10, num_points=1000):
    theta = np.linspace(0, num_turns * 2 * np.pi, num_points)
    phi = (2 + 2/5) * theta
    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi) * 0.3  # Flatten Z to fit between dipole rings
    return x, y, z


# ========== Parameters ==========
num_magnets = 16
radius = 1.2
dipole_ring_radius = 1.5
arrow_length = 0.3
offset = 0.1
winding_colors = np.linspace(0, 1, num_magnets, endpoint=False)
x_range = (-2, 2)
y_range = (-2, 2)
z_range = (-2, 2)
X, Y, Z = np.meshgrid(np.linspace(*x_range, 11), np.linspace(*y_range, 11), np.linspace(*z_range, 11))


rodin_x, rodin_y, rodin_z = generate_rodin_starship(
    R=1.2,    # Major radius, matches your rings
    r=0.6,    # Minor radius (tube)
    num_turns=10,
    num_points=2000
)


# --- Dipole rings ---
bottom_pos, bottom_ori = generate_dipole_ring(dipole_ring_radius, num_magnets, 0.75, invert=False)
top_pos, top_ori = generate_dipole_ring(dipole_ring_radius, num_magnets, 0.75,  invert=True)
middle_pos, middle_ori = generate_dipole_ring(dipole_ring_radius, num_magnets, z_offset=0.0)

biot_savart_mode = 'middle'   # or 'all' for everything

if biot_savart_mode == 'bottom':
    positions = bottom_pos
    orientations = bottom_ori
elif biot_savart_mode == 'top':
    positions = top_pos
    orientations = top_ori
elif biot_savart_mode == 'middle':
    positions = middle_pos
    orientations = middle_ori
elif biot_savart_mode == 'all':
    positions = bottom_pos + middle_pos + top_pos
    orientations = bottom_ori + middle_ori + top_ori
else:
    raise ValueError("Invalid biot_savart_mode!")


# ======= Compute the magnetic field =======
Bx, By, Bz = compute_dipole_field_from_orientations(X, Y, Z, positions, orientations)
magnitude = np.sqrt(Bx**2 + By**2 + Bz**2)
magnitude[magnitude == 0] = 1e-9
Bx_norm, By_norm, Bz_norm = Bx / magnitude, By / magnitude, Bz / magnitude

# ========== Plotting ==========
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, Bx_norm, By_norm, Bz_norm, length=0.15, normalize=True, color='blue', linewidth=0.25)
ax.plot3D(rodin_x, rodin_y, rodin_z, color='magenta', linewidth=2, label='Rodin Starship Coil')
# Draw dipole arrows for both rings, always shown for context
for pos, ori, c in zip(bottom_pos, bottom_ori, winding_colors):
    start = pos - ori * 0.3
    ax.quiver(*start, *ori, length=0.6, color=plt.cm.hsv(c), linewidth=2, arrow_length_ratio=0.25)
for pos, ori, c in zip(top_pos, top_ori, winding_colors):
    start = pos - ori * 0.3
    ax.quiver(*start, *ori, length=0.6, color=plt.cm.hsv(c), linewidth=2, arrow_length_ratio=0.25)

for pos, ori, c in zip(middle_pos, middle_ori, winding_colors):
    start = pos - ori * 0.3
    ax.quiver(*start, *ori, length=0.6, color=plt.cm.hsv(c), linewidth=2, arrow_length_ratio=0.25)


ax.set_title(f'Biot-Savart Field: {biot_savart_mode.title()} Dipole Ring(s)')
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
