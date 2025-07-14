
import numpy as np

import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# Define coil parameters
turns = 20   # Number of turns in the coil
height = .25   # Height of the coil
points_per_turn = 50  # Resolution of the coil
R, r = 0.5, 0.5  # Major and minor R of the torus
num_turns = 12   # Total turns per phase

# # Generate helical coil
t = np.linspace(0, 2 * np.pi * turns, turns * points_per_turn)
x_coil = R * np.cos(t)
y_coil = R * np.sin(t)
z_coil = np.linspace(-height / 2, height / 2, turns * points_per_turn)

# t = np.linspace(0, num_turns * 2 * np.pi, points_per_turn)
# phi = (2 + 2/5) * t  # Rodin winding ratio with phase shift
# x_coil = (R + r * np.cos(phi)) * np.cos(t)
# y_coil = (R + r * np.cos(phi)) * np.sin(t)
# z_coil = r * np.sin(phi)

# Define a larger 3D grid for better visualization
grid_size = 9
x_range = np.linspace(-1, 1, grid_size)  # Focus on the toroidal region
y_range = np.linspace(-1, 1, grid_size)
z_range = np.linspace(-1, 1, grid_size)

X, Y, Z = np.meshgrid(x_range, y_range, z_range)

# Compute an approximation of the magnetic field around the coil
def compute_magnetic_field(x, y, z, x_coil, y_coil, z_coil):
    """ Approximate the magnetic field at (x, y, z) due to a current loop """
    Bx, By, Bz = np.zeros_like(x), np.zeros_like(y), np.zeros_like(z)
    mu_0 = 4 * np.pi * 1e-7  # Vacuum permeability
    I = 1  # Assume unit current
    dl_x, dl_y, dl_z = np.gradient(x_coil), np.gradient(y_coil), np.gradient(z_coil)

    for i in range(len(x_coil)):
    #for i in range(0, len(x_coil), 5):  # Use every 5th segment
        rx, ry, rz = x - x_coil[i], y - y_coil[i], z - z_coil[i]
        r = np.sqrt(rx**2 + ry**2 + rz**2) + 1e-9  # Avoid division by zero

        # Create dL and r_vec correctly
        dL = np.array([dl_x[i], dl_y[i], dl_z[i]]).reshape(3, 1, 1, 1)  # Shape (3,1,1,1)
        r_vec = np.array([rx, ry, rz])  # Shape (3, grid_size, grid_size, grid_size)

        # Compute cross product element-wise
        dB = np.cross(dL, r_vec, axis=0) / (r**3)

        # Accumulate results
        Bx += dB[0]
        By += dB[1]
        Bz += dB[2]

    return Bx * mu_0 * I, By * mu_0 * I, Bz * mu_0 * I

# Compute the magnetic field at each point in the grid
Bx, By, Bz = compute_magnetic_field(X, Y, Z, x_coil, y_coil, z_coil)

# Normalize for streamline visualization
B_magnitude = np.sqrt(Bx**2 + By**2 + Bz**2) + 1e-9
Bx, By, Bz = Bx / B_magnitude, By / B_magnitude, Bz / B_magnitude

# Time-dependent AC current effect
omega = 2 * np.pi * 1  # Angular frequency (1 Hz for simplicity)
time_steps = 100  # Number of frames in animation

# Store B-fields over time to compute dB/dt
B_time_series = []
for t in np.linspace(0, 2 * np.pi, time_steps):
    I_t = np.cos(omega * t)  # AC current variation
    B_time_series.append((Bx * I_t, By * I_t, Bz * I_t))

# Convert to numpy array for differentiation
B_time_series = np.array(B_time_series)

# Compute dB/dt using finite differences
dBx_dt = np.gradient(B_time_series[:, 0], axis=0)
dBy_dt = np.gradient(B_time_series[:, 1], axis=0)
dBz_dt = np.gradient(B_time_series[:, 2], axis=0)

# Compute Electric Field (E = -dB/dt)
# Use a perpendicular rotation: E = ẑ × (-dB/dt)
Ex = -dBy_dt  # Rotated component from -∂Bz/∂t
Ey = dBx_dt   # Rotated component from ∂Bz/∂t
Ez = np.zeros_like(Ey)  # No electric field along z-axis (it forms loops)

# Create 3D figure
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# Plot the coil
ax.plot(x_coil, y_coil, z_coil, color='red', linewidth=2, label="Coil")

# Generate streamlines for magnetic field
streamline_points_B = np.array([X.flatten(), Y.flatten(), Z.flatten()]).T
streamline_vectors_B = np.array([Bx.flatten(), By.flatten(), Bz.flatten()]).T
streamline_vectors_B *= 10  # Scale up magnetic field visualization
streamline_segments_B = np.array([streamline_points_B, streamline_points_B + streamline_vectors_B * 0.3]).swapaxes(0, 1)

# Compute field magnitudes for coloring
B_magnitude_flat = np.sqrt(Bx.flatten()**2 + By.flatten()**2 + Bz.flatten()**2)
colors = cm.viridis(B_magnitude_flat / np.max(B_magnitude_flat))  # Normalize

# Add colored magnetic field streamlines
magnetic_field_lines = Line3DCollection(streamline_segments_B, colors=colors, linewidths=1, alpha=0.6)
ax.add_collection3d(magnetic_field_lines)


# Generate streamlines for electric field at initial frame
streamline_points_E = np.array([X.flatten(), Y.flatten(), Z.flatten()]).T
streamline_vectors_E = np.array([Ex[0].flatten(), Ey[0].flatten(), Ez[0].flatten()]).T
streamline_vectors_E *= 10  # Scale up electric field visualization
streamline_segments_E = np.array([streamline_points_E, streamline_points_E + streamline_vectors_E * 0.3]).swapaxes(0, 1)

# Add electric field streamlines
electric_field_lines = Line3DCollection(streamline_segments_E, colors='blue', linewidths=1, alpha=0.6)
ax.add_collection3d(electric_field_lines)

# Animation function
def update(frame):
    # Ensure frame index wraps around within available data
    idx = frame % time_steps  # Prevents out-of-bounds indexing

    # Oscillating current I(t) = cos(ωt)
    I_t = np.cos(omega * frame / time_steps * 2 * np.pi)

    # Update Magnetic Field (Oscillating)
    streamline_vectors_B = np.array([
        Bx.flatten() * I_t,
        By.flatten() * I_t,
        Bz.flatten() * I_t
    ]).T
    streamline_segments_B = np.array([
        streamline_points_B,
        streamline_points_B + streamline_vectors_B * 0.3
    ]).swapaxes(0, 1)
    magnetic_field_lines.set_segments(streamline_segments_B)

    # Compute dB/dt dynamically
    dBx_dt = -omega * np.sin(omega * frame / time_steps * 2 * np.pi) * Bx
    dBy_dt = -omega * np.sin(omega * frame / time_steps * 2 * np.pi) * By
    dBz_dt = -omega * np.sin(omega * frame / time_steps * 2 * np.pi) * Bz

    # Compute spatial derivatives of B (∇ × B)
    dBz_dy = np.gradient(Bz, axis=1)  # ∂Bz/∂y
    dBy_dz = np.gradient(By, axis=2)  # ∂By/∂z
    dBx_dz = np.gradient(Bx, axis=2)  # ∂Bx/∂z
    dBz_dx = np.gradient(Bz, axis=0)  # ∂Bz/∂x
    dBy_dx = np.gradient(By, axis=0)  # ∂By/∂x
    dBx_dy = np.gradient(Bx, axis=1)  # ∂Bx/∂y

    # Compute curl of dB/dt (∇ × dB/dt)
    dBz_dt_dy = np.gradient(dBz_dt, axis=1)
    dBy_dt_dz = np.gradient(dBy_dt, axis=2)
    dBx_dt_dz = np.gradient(dBx_dt, axis=2)
    dBz_dt_dx = np.gradient(dBz_dt, axis=0)
    dBy_dt_dx = np.gradient(dBy_dt, axis=0)
    dBx_dt_dy = np.gradient(dBx_dt, axis=1)

    # Compute Electric Field using Faraday’s Law: E = -∇ × B - ∇ × dB/dt
    Ex = -((dBz_dy - dBy_dz) + (dBz_dt_dy - dBy_dt_dz))
    Ey = -((dBx_dz - dBz_dx) + (dBx_dt_dz - dBz_dt_dx))
    Ez = -((dBy_dx - dBx_dy) + (dBy_dt_dx - dBx_dt_dy))


    # Scale Electric Field for better visualization
    scaling_factor = 0.2  # Adjust as needed
    streamline_vectors_E = np.array([
        Ex.flatten() * scaling_factor,
        Ey.flatten() * scaling_factor,
        Ez.flatten() * scaling_factor
    ]).T
    streamline_segments_E = np.array([
        streamline_points_E,
        streamline_points_E + streamline_vectors_E * 0.3
    ]).swapaxes(0, 1)
    electric_field_lines.set_segments(streamline_segments_E)

    return magnetic_field_lines, electric_field_lines

# Animate
ani = animation.FuncAnimation(fig, update, frames=time_steps, interval=100, blit=False)

# Labels and show
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio2
ax.set_title("Magnetic and Electric Field Streamlines Around a Coil")
ax.legend()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()