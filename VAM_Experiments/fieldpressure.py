import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]

rho_fluid = 7e-7




# Constants
rho_ae = 3.89e18  # Æther fluid energy density in kg/m^3
grid_size = 21
space = np.linspace(-2, 2, grid_size)
X, Y, Z = np.meshgrid(space, space, space)

# Magnetic dipole field model (static ring - no pressure drop)
def magnetic_field_static_ring(X, Y, Z, num_dipoles=16, radius=1.5):
    Bx, By, Bz = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)
    for i in range(num_dipoles):
        phi = 2 * np.pi * i / num_dipoles
        pos = np.array([radius * np.cos(phi), radius * np.sin(phi), 0])
        m = np.array([np.cos(2 * phi), np.sin(2 * phi), 0])
        for ix in range(X.shape[0]):
            for iy in range(X.shape[1]):
                for iz in range(X.shape[2]):
                    r = np.array([X[ix, iy, iz], Y[ix, iy, iz], Z[ix, iy, iz]]) - pos
                    norm_r = np.linalg.norm(r)
                    if norm_r < 1e-6:
                        continue
                    r_hat = r / norm_r
                    B = (1 / (4 * np.pi * norm_r**3)) * (3 * np.dot(m, r_hat) * r_hat - m)
                    Bx[ix, iy, iz] += B[0]
                    By[ix, iy, iz] += B[1]
                    Bz[ix, iy, iz] += B[2]
    return Bx, By, Bz

# Compute vorticity using central differences
def compute_vorticity(Bx, By, Bz, dx):
    curl_x = (np.roll(Bz, -1, axis=1) - np.roll(Bz, 1, axis=1)) / (2 * dx) - \
             (np.roll(By, -1, axis=2) - np.roll(By, 1, axis=2)) / (2 * dx)
    curl_y = (np.roll(Bx, -1, axis=2) - np.roll(Bx, 1, axis=2)) / (2 * dx) - \
             (np.roll(Bz, -1, axis=0) - np.roll(Bz, 1, axis=0)) / (2 * dx)
    curl_z = (np.roll(By, -1, axis=0) - np.roll(By, 1, axis=0)) / (2 * dx) - \
             (np.roll(Bx, -1, axis=1) - np.roll(Bx, 1, axis=1)) / (2 * dx)
    return curl_x, curl_y, curl_z

# Compute pressure from vorticity magnitude
def compute_pressure(vorticity_x, vorticity_y, vorticity_z):
    omega_mag_sq = vorticity_x**2 + vorticity_y**2 + vorticity_z**2
    return -0.5 * rho_ae * omega_mag_sq

# Main pipeline
Bx, By, Bz = magnetic_field_static_ring(X, Y, Z)
vort_x, vort_y, vort_z = compute_vorticity(Bx, By, Bz, dx=space[1] - space[0])
pressure = compute_pressure(vort_x, vort_y, vort_z)
# f_x, f_y, f_z = -np.gradient(pressure, space[1] - space[0]) / rho_fluid
# Plot mid-Z pressure slice
mid = grid_size // 2
plt.figure(figsize=(10, 6))
plt.contourf(X[:, :, mid], Y[:, :, mid], pressure[:, :, mid], levels=50, cmap='inferno')
plt.colorbar(label="Æther Pressure (Pa)")
plt.title("Æther Pressure Field – Static Dipole Ring (Mid-Z Plane)")
plt.xlabel("X")
plt.ylabel("Y")
plt.tight_layout()
plt.show()
# 3D quiver plot of the static dipole ring magnetic field

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Subsample grid to reduce visual clutter
step = 3
Xq, Yq, Zq = X[::step, ::step, ::step], Y[::step, ::step, ::step], Z[::step, ::step, ::step]
Bxq, Byq, Bzq = Bx[::step, ::step, ::step], By[::step, ::step, ::step], Bz[::step, ::step, ::step]

# Normalize for arrow direction
magnitude = np.sqrt(Bxq**2 + Byq**2 + Bzq**2)
magnitude[magnitude == 0] = 1e-9
Bxq /= magnitude
Byq /= magnitude
Bzq /= magnitude

ax.quiver(Xq, Yq, Zq, Bxq, Byq, Bzq, length=0.2, normalize=False, color='blue', linewidth=0.5)
ax.set_title("3D Field Vectors – Static Dipole Ring")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)
ax.set_box_aspect([1, 1, 1])
plt.tight_layout()
plt.show()

# Add static dipoles and coil trace to the 3D field plot

def generate_static_dipole_ring(num_dipoles=16, radius=1.5):
    positions, orientations = [], []
    for i in range(num_dipoles):
        phi = 2 * np.pi * i / num_dipoles
        x, y, z = radius * np.cos(phi), radius * np.sin(phi), 0.0
        positions.append(np.array([x, y, z]))
        m = np.array([np.cos(2 * phi), np.sin(2 * phi), 0])
        m /= np.linalg.norm(m)
        orientations.append(m)
    return positions, orientations

# Rodin-style flat coil
def generate_flat_coil(turns=5, radius=1.0, pitch=0.1, points=1000):
    theta = np.linspace(0, 2 * np.pi * turns, points)
    r = radius * theta / (2 * np.pi * turns)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = pitch * theta / (2 * np.pi)
    return x, y, z - np.mean(z)

# Prepare data
dipole_positions, dipole_orientations = generate_static_dipole_ring()
coil_x, coil_y, coil_z = generate_flat_coil()

# Plot
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Quiver: magnetic field vectors
ax.quiver(Xq, Yq, Zq, Bxq, Byq, Bzq, length=0.2, normalize=False, color='blue', linewidth=0.5)

# Quiver: dipole arrows
for pos, ori in zip(dipole_positions, dipole_orientations):
    start = pos - 0.2 * ori
    ax.quiver(*start, *ori, length=0.4, color='red', linewidth=2, arrow_length_ratio=0.25)

# Coil trace
ax.plot(coil_x, coil_y, coil_z, color='black', linewidth=2, label='Flat Coil')

# Labels
ax.set_title("Static Dipole Ring with Flat Coil Overlay")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)
ax.set_box_aspect([1, 1, 1])
ax.legend()

plt.tight_layout()
plt.show()
