import numpy as np
import matplotlib.pyplot as plt

# Reimporting necessary libraries after state reset
import os
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
script_name = os.path.splitext(os.path.basename(__file__))[0]

# === Step 1: Generate the figure-eight knot ===
def generate_figure8_knot(N=400):
    s = np.linspace(0, 2 * np.pi, N)
    x = (2 + np.cos(2 * s)) * np.cos(3 * s)
    y = (2 + np.cos(2 * s)) * np.sin(3 * s)
    z = np.sin(4 * s)
    return np.stack((x, y, z), axis=1)

# === Step 2: Compute tangents ===
def compute_tangents(X):
    dX = np.gradient(X, axis=0)
    norms = np.linalg.norm(dX, axis=1, keepdims=True)
    return dX / norms

# === Step 3: Biot–Savart velocity ===
def biot_savart_velocity(r, X, T, Gamma=1.0):
    v = np.zeros(3)
    coeff = Gamma / (4 * np.pi)
    for xi, ti in zip(X, T):
        dr = r - xi
        norm = np.linalg.norm(dr)
        if norm > 1e-6:
            cross = np.cross(ti, dr)
            v += coeff * cross / norm**3
    return v

# === Step 4: Setup ===
positions1 = generate_figure8_knot()
positions2 = positions1 * np.array([-1, 1, 1])  # Mirror across x-y plane
positions = np.vstack((positions1, positions2))
tangents = compute_tangents(positions)
rho_ae = 7e-7
P_inf = 0.0

# Evaluate on z = 0 slice
grid_N = 50
x_vals = np.linspace(-5, 5, grid_N)
y_vals = np.linspace(-5, 5, grid_N)
z_val = 0.0

velocity_mag = np.zeros((grid_N, grid_N))
pressure_field = np.zeros((grid_N, grid_N))

# === Step 5: Evaluate ===
for i, x in enumerate(x_vals):
    for j, y in enumerate(y_vals):
        r = np.array([x, y, z_val])
        v = biot_savart_velocity(r, positions, tangents)
        vmag = np.linalg.norm(v)
        velocity_mag[j, i] = vmag
        pressure_field[j, i] = P_inf - 0.5 * rho_ae * vmag**2

# === Step 6: Plot ===
fig, axs = plt.subplots(1, 2, figsize=(14, 6))
c1 = axs[0].contourf(x_vals, y_vals, velocity_mag, levels=50, cmap='viridis')
axs[0].set_title('|v| (m/s) at z = 0')
axs[0].set_xlabel('x')
axs[0].set_ylabel('y')
fig.colorbar(c1, ax=axs[0])

c2 = axs[1].contourf(x_vals, y_vals, pressure_field, levels=50, cmap='coolwarm')
axs[1].set_title('Pressure (Pa) at z = 0')
axs[1].set_xlabel('x')
axs[1].set_ylabel('y')
fig.colorbar(c2, ax=axs[1])

plt.tight_layout()
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# === Knot and field setup ===
def generate_figure8_knot(N=400):
    s = np.linspace(0, 2 * np.pi, N)
    x = (2 + np.cos(2 * s)) * np.cos(3 * s)
    y = (2 + np.cos(2 * s)) * np.sin(3 * s)
    z = np.sin(4 * s)
    return np.stack((x, y, z), axis=1)

def compute_tangents(X):
    dX = np.gradient(X, axis=0)
    norms = np.linalg.norm(dX, axis=1, keepdims=True)
    return dX / norms

def biot_savart_velocity(r, X, T, Gamma=1.0):
    v = np.zeros(3)
    coeff = Gamma / (4 * np.pi)
    for xi, ti in zip(X, T):
        dr = r - xi
        norm = np.linalg.norm(dr)
        if norm > 1e-6:
            cross = np.cross(ti, dr)
            v += coeff * cross / norm**3
    return v

# === Generate knot ===
positions = generate_figure8_knot()
tangents = compute_tangents(positions)

# === Setup 3D grid ===
grid_N = 7  # smaller for speed
xv = np.linspace(-4, 4, grid_N)
yv = np.linspace(-4, 4, grid_N)
zv = np.linspace(-4, 4, grid_N)
Xg, Yg, Zg = np.meshgrid(xv, yv, zv)
points = np.stack((Xg, Yg, Zg), axis=-1).reshape(-1, 3)

# === Evaluate field ===
V = np.array([biot_savart_velocity(p, positions, tangents) for p in points])
Vmag = np.linalg.norm(V, axis=1)
Vnorm = V / (Vmag[:, np.newaxis] + 1e-12)  # avoid division by zero

# === Plotting ===
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Velocity vectors
ax.quiver(points[:, 0], points[:, 1], points[:, 2],
          Vnorm[:, 0], Vnorm[:, 1], Vnorm[:, 2],
          length=0.5, normalize=True, color='gray', alpha=0.75)

# Knot filament
ax.plot(positions[:, 0], positions[:, 1], positions[:, 2],
        color='blue', linewidth=2, label='Figure-8 Knot')

ax.set_title("3D Biot–Savart Velocity Field (Figure-8 Knot)")
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-4, 4)
ax.set_box_aspect([1, 1, 1])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.legend()
plt.tight_layout()
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

xv = np.linspace(-4, 4, grid_N)
yv = np.linspace(-4, 4, grid_N)
zv = np.linspace(-4, 4, grid_N)
Xg, Yg, Zg = np.meshgrid(xv, yv, zv)
points = np.stack((Xg, Yg, Zg), axis=-1).reshape(-1, 3)

V = np.array([biot_savart_velocity(p, positions, tangents) for p in points])
Vmag = np.linalg.norm(V, axis=1)
Vnorm = V / (Vmag[:, np.newaxis] + 1e-12)

# Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.quiver(points[:, 0], points[:, 1], points[:, 2],
          Vnorm[:, 0], Vnorm[:, 1], Vnorm[:, 2],
          length=0.5, normalize=True, color='gray', alpha=0.75)

# Plot both knots
ax.plot(positions1[:, 0], positions1[:, 1], positions1[:, 2],
        color='blue', linewidth=2, label='Knot 1')
ax.plot(positions2[:, 0], positions2[:, 1], positions2[:, 2],
        color='red', linewidth=2, linestyle='--', label='Mirrored Knot')

ax.set_title("3D Biot–Savart Field with Mirrored Figure-8 Knots")
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-4, 4)
ax.set_box_aspect([1, 1, 1])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.legend()
plt.tight_layout()
plt.show()

