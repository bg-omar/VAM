import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


plotGridsize = 4
# Define trefoil knot centerline
def trefoil_knot(s):
    x = (2 + np.cos(3 * s)) * np.cos(2 * s)
    y = (2 + np.cos(3 * s)) * np.sin(2 * s)
    z = np.sin(3 * s)
    return np.stack((x, y, z), axis=-1)

# Derivative for tangent vectors
def compute_tangent(X):
    dX = np.gradient(X, axis=0)
    norms = np.linalg.norm(dX, axis=1, keepdims=True)
    return dX / norms

# Smoothed vorticity field using Gaussian cores
def vorticity_field(r, X, T, Gamma=1.0, epsilon=0.1):
    omega = np.zeros_like(r)
    for xi, ti in zip(X, T):
        dr = r - xi
        weight = np.exp(-np.sum(dr**2, axis=-1) / (2 * epsilon**2))
        omega += (Gamma / ((2 * np.pi * epsilon**2) ** 1.5)) * weight[..., None] * ti
    return omega



# Biot-Savart velocity field at a point r
def biot_savart_velocity(r, X, T, Gamma=1.0):
    v = np.zeros(3)
    for xi, ti in zip(X, T):
        dr = r - xi
        norm_dr = np.linalg.norm(dr)
        if norm_dr > 1e-3:
            v += np.cross(ti, dr) / norm_dr**3
    return Gamma / (4 * np.pi) * v

# Generate trefoil knot data
s_vals = np.linspace(0, 2 * np.pi, 400)
X = trefoil_knot(s_vals)
T = compute_tangent(X)

# Create a grid of points in a slice (z = 0) to evaluate velocity and pressure
grid_size = 50
x_vals = np.linspace(-4, 4, grid_size)
y_vals = np.linspace(-4, 4, grid_size)
z_val = 0.0
velocity_magnitude = np.zeros((grid_size, grid_size))
pressure_field = np.zeros((grid_size, grid_size))

# Constants
rho_ae = 7e-7  # kg/m^3
P_infinity = 0.0  # reference pressure

# Evaluate fields
for i, x in enumerate(x_vals):
    for j, y in enumerate(y_vals):
        r = np.array([x, y, z_val])
        v = biot_savart_velocity(r, X, T)
        v_mag = np.linalg.norm(v)
        velocity_magnitude[j, i] = v_mag
        pressure_field[j, i] = P_infinity - 0.5 * rho_ae * v_mag**2

# Display velocity magnitude and pressure
import ace_tools_open as tools; tools.display_dataframe_to_user(name="Trefoil Vortex Field Slice (z = 0)", dataframe=
pd.DataFrame({
    "x (1e-15m)": np.tile(x_vals, grid_size),
    "y (1e-15m)": np.repeat(y_vals, grid_size),
    "|v| (m/s)": velocity_magnitude.flatten(),
    "P (Pa)": pressure_field.flatten()
}))

# 2D Visualization: Velocity magnitude and Pressure contours

fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Velocity magnitude plot
c1 = axs[0].contourf(x_vals, y_vals, velocity_magnitude, levels=50, cmap='viridis')
axs[0].set_xlim(-plotGridsize, plotGridsize)
axs[0].set_ylim(-plotGridsize, plotGridsize)

axs[0].set_title('Velocity Magnitude |v| (m/s) at z=0')
axs[0].set_xlabel('x (m)')
axs[0].set_ylabel('y (m)')
fig.colorbar(c1, ax=axs[0], label='|v| (m/s)')

# Pressure field plot
c2 = axs[1].contourf(x_vals, y_vals, pressure_field, levels=50, cmap='coolwarm')
axs[1].set_xlim(-plotGridsize, plotGridsize)
axs[1].set_ylim(-plotGridsize, plotGridsize)

axs[1].set_title('Pressure Field P (Pa) at z=0')
axs[1].set_xlabel('x (m)')
axs[1].set_ylabel('y (m)')
fig.colorbar(c2, ax=axs[1], label='Pressure (Pa)')

plt.tight_layout()
# plt.show()

# Reduce grid size for faster processing
grid_size_light = 25
x_vals_light = np.linspace(-4, 4, grid_size_light)
y_vals_light = np.linspace(-4, 4, grid_size_light)

# Reuse same z-slices
slice_data_light = []

# Use only 3 slices to avoid timeouts
z_slices_focus = [-1.0, 0.0, 1.0]
slice_data_focus = []

# Evaluate velocity magnitude and pressure for focused slices
for z_val in z_slices_focus:
    velocity_slice = np.zeros((grid_size_light, grid_size_light))
    pressure_slice = np.zeros((grid_size_light, grid_size_light))
    for i, x in enumerate(x_vals_light):
        for j, y in enumerate(y_vals_light):
            r = np.array([x, y, z_val])
            v = biot_savart_velocity(r, X, T)
            v_mag = np.linalg.norm(v)
            velocity_slice[j, i] = v_mag
            pressure_slice[j, i] = P_infinity - 0.5 * rho_ae * v_mag**2
    slice_data_focus.append({
        "z": z_val,
        "velocity": velocity_slice,
        "pressure": pressure_slice
    })

# Visualize selected z-slices
fig, axs = plt.subplots(len(z_slices_focus), 2, figsize=(12, 4 * len(z_slices_focus)))

for idx, slice_info in enumerate(slice_data_focus):
    z = slice_info["z"]
    vel = slice_info["velocity"]
    pres = slice_info["pressure"]

    # Velocity magnitude
    ax_v = axs[idx, 0]
    c1 = ax_v.contourf(x_vals_light, y_vals_light, vel, levels=40, cmap='viridis')
    ax_v.set_xlim(-plotGridsize, plotGridsize)
    ax_v.set_ylim(-plotGridsize, plotGridsize)

    ax_v.set_title(f'|v| at z = {z:.2f}')
    ax_v.set_xlabel('x (m)')
    ax_v.set_ylabel('y (m)')

    # Pressure field
    ax_p = axs[idx, 1]
    c2 = ax_p.contourf(x_vals_light, y_vals_light, pres, levels=40, cmap='coolwarm')
    ax_p.set_xlim(-plotGridsize, plotGridsize)
    ax_p.set_ylim(-plotGridsize, plotGridsize)

    ax_p.set_title(f'P at z = {z:.2f}')
    ax_p.set_xlabel('x (m)')
    ax_p.set_ylabel('y (m)')

plt.tight_layout()
# plt.show()

from mpl_toolkits.mplot3d import Axes3D

# 3D plot of trefoil vortex centerline with velocity vectors in a surrounding grid

# Define 3D grid slice around the knot (smaller for clarity)
n_vectors = 15
xv = np.linspace(-3, 3, n_vectors)
yv = np.linspace(-3, 3, n_vectors)
zv = np.linspace(-3, 3, n_vectors)
Xg, Yg, Zg = np.meshgrid(xv, yv, zv)
points = np.stack((Xg, Yg, Zg), axis=-1).reshape(-1, 3)

# Compute velocity vectors
V = np.array([biot_savart_velocity(p, X, T) for p in points])
Vmag = np.linalg.norm(V, axis=1)
Vnorm = V / Vmag[:, np.newaxis]  # normalize for visualization

# Sample the trefoil knot
knot_sample = trefoil_knot(np.linspace(0, 2*np.pi, 400))
B_magnitude = np.sqrt(T[:, 0] ** 2 + T[:, 1] ** 2 + T[:, 2] ** 2)
Bx, By, Bz = T[:, 0] / B_magnitude, T[:, 1] / B_magnitude, T[:, 2] / B_magnitude

rotation_axis = "x"  # Change to "x" or "y" as needed
pole_axis = "y"  # Change to "x" or "y" as needed

if rotation_axis == "z":
    dBy_dx = np.gradient(By, axis=0)  # ∂By/∂x
    dBx_dy = np.gradient(Bx, axis=0)  # ∂Bx/∂y
    rotation_direction = dBy_dx - dBx_dy  # Rotation in XY-plane (Z-axis rotation)

elif rotation_axis == "y":
    dBx_dz = np.gradient(Bx, axis=0)  # ∂Bx/∂z
    dBz_dx = np.gradient(Bz, axis=0)  # ∂Bz/∂x
    rotation_direction = dBx_dz - dBz_dx  # Rotation in XZ-plane (Y-axis rotation)

elif rotation_axis == "x":
    dBz_dy = np.gradient(Bz, axis=0)  # ∂Bz/∂y
    dBy_dz = np.gradient(By, axis=0)  # ∂By/∂z
    rotation_direction = dBz_dy - dBy_dz  # Rotation in YZ-plane (X-axis rotation)

if pole_axis == "z":
    dBy_dx = np.gradient(By, axis=0)  # ∂By/∂x
    dBx_dy = np.gradient(Bx, axis=0)  # ∂Bx/∂y
    pole_direction = dBy_dx - dBx_dy  # Rotation in XY-plane (Z-axis rotation)

elif pole_axis == "y":
    dBx_dz = np.gradient(Bx, axis=0)  # ∂Bx/∂z
    dBz_dx = np.gradient(Bz, axis=0)  # ∂Bz/∂x
    pole_direction = dBx_dz - dBz_dx  # Rotation in XZ-plane (Y-axis rotation)

elif pole_axis == "x":
    dBz_dy = np.gradient(Bz, axis=0)  # ∂Bz/∂y
    dBy_dz = np.gradient(By, axis=0)  # ∂By/∂z
    pole_direction = dBz_dy - dBy_dz  # Rotation in YZ-plane (X-axis rotation)


# Normalize rotation for color mapping
rotation_normalized = (rotation_direction - np.min(rotation_direction)) / (np.max(rotation_direction) - np.min(rotation_direction))

# Normalize pole for color mapping
pole_normalized = (pole_direction - np.min(pole_direction)) / (np.max(pole_direction) - np.min(pole_direction))


rot_cmap = plt.get_cmap("seismic")  # Get Turbo colormap safely
rotate_colors = rot_cmap(rotation_normalized.flatten())  # Get Turbo colors (RGBA)

pole_cmap = plt.get_cmap("Greys")  # White → Black transition
pole_colors = pole_cmap(pole_normalized.flatten())  # Get Blue-Red colormap for Z-axis

# --- 3. Blend the colors ---
blend_factor = 0.25   # Adjust for color dominance
final_colors = (blend_factor * rotate_colors + (1 - blend_factor) * pole_colors)  # Weighted blend



angles = np.arctan2(T[:, 1].flatten(), T[:, 0].flatten() )  # Angle in the XY plane
colormap = plt.colormaps["turbo"]  # ✅
colors = colormap((angles + np.pi) / (2 * np.pi))  # Normalize angles between 0 and 1


# 3D plot
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(points[:, 0], points[:, 1], points[:, 2],
          Vnorm[:, 0], Vnorm[:, 1], Vnorm[:, 2],
          length=0.4, normalize=True, color=final_colors, alpha=0.5)

# Plot the trefoil knot
ax.plot(knot_sample[:, 0], knot_sample[:, 1], knot_sample[:, 2],
        color='red', linewidth=2, label='Trefoil Vortex Filament')

ax.set_title('3D Trefoil Vortex and Induced Velocity Field')
ax.set_xlim(-plotGridsize, plotGridsize)
ax.set_ylim(-plotGridsize, plotGridsize)
ax.set_zlim(-plotGridsize, plotGridsize)

ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
ax.legend()
plt.tight_layout()


# Compute a simple time evolution of the trefoil vortex using the vorticity transport equation
# Here, we perform a basic discretized evolution of the filament using the Biot–Savart-induced velocity field

def evolve_vortex(X_init, T_init, dt=0.01, steps=10, Gamma=1.0):
    X_evolved = np.copy(X_init)
    for step in range(steps):
        V_induced = np.array([biot_savart_velocity(xi, X_evolved, T_init, Gamma=Gamma) for xi in X_evolved])
        X_evolved += dt * V_induced
    return X_evolved

# Evolve for 10 small time steps
X_evolved = evolve_vortex(X, T, dt=0.01, steps=10)
T_evolved = compute_tangent(X_evolved)

# # Plot initial and evolved trefoil vortex
# fig = plt.figure(figsize=(12, 10))
# ax = fig.add_subplot(111, projection='3d')
#
# # Initial vortex (gray)
# ax.plot(X[:, 0], X[:, 1], X[:, 2], color='gray', linewidth=1.5, label='Initial Trefoil')
#
# # Evolved vortex (red)
# ax.plot(X_evolved[:, 0], X_evolved[:, 1], X_evolved[:, 2], color='red', linewidth=2.5, label='Evolved Trefoil')
#
# ax.set_title('Trefoil Vortex Evolution Under VAM Dynamics')
# ax.set_xlim(-plotGridsize, plotGridsize)
# ax.set_ylim(-plotGridsize, plotGridsize)
# ax.set_zlim(-plotGridsize, plotGridsize)
#
# ax.set_xlabel('x (m)')
# ax.set_ylabel('y (m)')
# ax.set_zlabel('z (m)')
# ax.legend()
# plt.tight_layout()
# # plt.show()
#
# # Optimize by reducing number of points and steps
# # Sample fewer points along the knot
# s_vals_light = np.linspace(0, 2 * np.pi, 150)
# X_light = trefoil_knot(s_vals_light)
# T_light = compute_tangent(X_light)
#
# # Evolve with fewer steps
# X_evolved_light = evolve_vortex(X_light, T_light, dt=0.01, steps=5)
# T_evolved_light = compute_tangent(X_evolved_light)
#
# # Plot initial and evolved vortex
# fig = plt.figure(figsize=(12, 10))
# ax = fig.add_subplot(111, projection='3d')
#
# # Initial vortex (gray)
# ax.plot(X_light[:, 0], X_light[:, 1], X_light[:, 2], color='gray', linewidth=1.5, label='Initial Trefoil')
#
# # Evolved vortex (red)
# ax.plot(X_evolved_light[:, 0], X_evolved_light[:, 1], X_evolved_light[:, 2], color='red', linewidth=2.5, label='Evolved Trefoil')
#
# ax.set_title('Optimized 3D Trefoil Vortex Evolution (VAM Dynamics)')
# ax.set_xlim(-plotGridsize, plotGridsize)
# ax.set_ylim(-plotGridsize, plotGridsize)
# ax.set_zlim(-plotGridsize, plotGridsize)
#
# ax.set_xlabel('x (m)')
# ax.set_ylabel('y (m)')
# ax.set_zlabel('z (m)')
# ax.legend()
# plt.show()