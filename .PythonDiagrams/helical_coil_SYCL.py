import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import dpctl
import dpnp as dnp  # SYCL-accelerated NumPy

import dpctl.tensor as dpt  # SYCL-optimized tensor math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import numpy as np

# ✅ Select Intel Arc A770 GPU
device = dpctl.select_default_device()

queue = dpctl.SyclQueue(device)
print(f"Using Device: {device}")

# Define coil parameters
turns = 12   # Number of turns in the coil
radius = .25   # Radius of the coil
height = .25   # Height of the coil
points_per_turn = 12  # Resolution of the coil

# Use dpnp (SYCL-accelerated NumPy) for calculations
t = dnp.linspace(0, 2 * dnp.pi * turns, turns * points_per_turn, dtype=dnp.float32)
x_coil = radius * dnp.cos(t)
y_coil = radius * dnp.sin(t)
z_coil = dnp.linspace(-height / 2, height / 2, turns * points_per_turn, dtype=dnp.float32)

# Define a larger 3D grid for better visualization
grid_size = 19
x_range = dnp.linspace(-4, 4, grid_size, dtype=dnp.float32)
y_range = dnp.linspace(-4, 4, grid_size, dtype=dnp.float32)
z_range = dnp.linspace(-4, 4, grid_size, dtype=dnp.float32)

X, Y, Z = dnp.meshgrid(x_range, y_range, z_range)

# Compute the magnetic field using SYCL-accelerated functions
def compute_magnetic_field(x, y, z, x_coil, y_coil, z_coil):
    """ Compute the magnetic field at (x, y, z) using SYCL acceleration. """
    Bx = dnp.zeros_like(x)
    By = dnp.zeros_like(y)
    Bz = dnp.zeros_like(z)
    mu_0 = 4 * dnp.pi * 1e-7
    I = 1  # Assume unit current

    # Compute the differential coil segments (dl)
    dl_x, dl_y, dl_z = dnp.gradient(x_coil), dnp.gradient(y_coil), dnp.gradient(z_coil)

    for i in range(len(x_coil)):
        rx, ry, rz = x - x_coil[i], y - y_coil[i], z - z_coil[i]
        r = dnp.sqrt(rx**2 + ry**2 + rz**2) + 1e-9  # Avoid division by zero

        dL = dnp.array([dl_x[i], dl_y[i], dl_z[i]]).reshape(3, 1, 1, 1)
        r_vec = dnp.array([rx, ry, rz])  # Shape (3, grid_size, grid_size, grid_size)

        dB = dnp.cross(dL, r_vec, axis=0) / (r**3)

        Bx += dB[0]
        By += dB[1]
        Bz += dB[2]

    return Bx * mu_0 * I, By * mu_0 * I, Bz * mu_0 * I

# Compute magnetic field (SYCL accelerated)
Bx, By, Bz = compute_magnetic_field(X, Y, Z, x_coil, y_coil, z_coil)

# Normalize for streamline visualization
B_magnitude = dnp.sqrt(Bx**2 + By**2 + Bz**2) + 1e-9
Bx, By, Bz = Bx / B_magnitude, By / B_magnitude, Bz / B_magnitude

# Time-dependent AC current effect
omega = 2 * dnp.pi * 1  # 1 Hz for simplicity
time_steps = 100  # Animation frames

# Compute electric field using SYCL acceleration
B_time_series = []
for t in dnp.linspace(0, 2 * dnp.pi, time_steps, dtype=dnp.float32):
    I_t = dnp.cos(omega * t)  # AC current variation
    B_time_series.append((Bx * I_t, By * I_t, Bz * I_t))

B_time_series = dnp.array(B_time_series)

# Compute dB/dt using finite differences
dB_dt = dnp.gradient(B_time_series, axis=0)  # Compute for all components at once
dBx_dt, dBy_dt, dBz_dt = dB_dt[:, 0], dB_dt[:, 1], dB_dt[:, 2]  # Extract components

# Compute Electric Field (E = ẑ × -dB/dt) to ensure correct orientation
Ex = -dBy_dt  # Rotate component
Ey = dBx_dt   # Rotate component
Ez = dnp.zeros_like(Ey)  # No electric field along z-axis

# Convert dpnp arrays to NumPy before Matplotlib
X, Y, Z = X.asnumpy(), Y.asnumpy(), Z.asnumpy()
Bx, By, Bz = Bx.asnumpy(), By.asnumpy(), Bz.asnumpy()
Ex, Ey, Ez = Ex.asnumpy(), Ey.asnumpy(), Ez.asnumpy()

# Create 3D figure
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Generate streamlines for magnetic field
streamline_points_B = np.array([X.flatten(), Y.flatten(), Z.flatten()]).T
streamline_vectors_B = np.array([Bx.flatten(), By.flatten(), Bz.flatten()]).T
streamline_segments_B = np.array([streamline_points_B, streamline_points_B + streamline_vectors_B * 0.3]).swapaxes(0, 1)

magnetic_field_lines = Line3DCollection(streamline_segments_B, colors='red', linewidths=0.5, alpha=0.6)
ax.add_collection3d(magnetic_field_lines)

# Generate streamlines for electric field
streamline_points_E = np.array([X.flatten(), Y.flatten(), Z.flatten()]).T
streamline_vectors_E = np.array([Ex[0].flatten(), Ey[0].flatten(), Ez[0].flatten()]).T
streamline_segments_E = np.array([streamline_points_E, streamline_points_E + streamline_vectors_E * 0.3]).swapaxes(0, 1)

electric_field_lines = Line3DCollection(streamline_segments_E, colors='blue', linewidths=0.5, alpha=0.6)
ax.add_collection3d(electric_field_lines)

def update(frame):
    idx = frame % time_steps
    I_t = np.cos(omega * frame / time_steps * 2 * np.pi)

    # Update magnetic field
    streamline_vectors_B = np.array([
        (dnp.multiply(Bx, I_t)).flatten(),
        (dnp.multiply(By, I_t)).flatten(),
        (dnp.multiply(Bz, I_t)).flatten()
    ]).T

    streamline_segments_B = np.array([
        streamline_points_B,
        streamline_points_B + streamline_vectors_B * 0.3
    ]).swapaxes(0, 1)

    magnetic_field_lines.set_segments(streamline_segments_B)

    # Update electric field
    streamline_vectors_E = np.array([
        Ex[idx].flatten(),
        Ey[idx].flatten(),
        Ez[idx].flatten()
    ]).T

    streamline_segments_E = np.array([
        streamline_points_E,
        streamline_points_E + streamline_vectors_E * 0.3
    ]).swapaxes(0, 1)

    electric_field_lines.set_segments(streamline_segments_E)

    return magnetic_field_lines, electric_field_lines

# Plot the coil
ax.plot(x_coil, y_coil, z_coil, color='red', linewidth=2, label="Coil")
ani = animation.FuncAnimation(fig, update, frames=time_steps, interval=100, blit=False)

# Labels and show
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-4, 4)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio2
ax.set_title("Magnetic & Electric Field Visualization (Intel Arc A770)")
plt.show()
