
import numpy as np

import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# Define coil parameters
turns = 20  # Number of turns in the helical coil
height = 0.1  # Height of the coil
points_per_turn = 600  # Resolution of the coil
R, r = 1.5, 1  # Major and minor radius of the torus
num_turns = 12  # Total Rodin turns per phase
time_steps = 100  # Number of frames in animation
omega = 2 * np.pi * 1  # Angular frequency (1 Hz)
scaling_factor = 0.1  # Scale factor for E-field visualization

# Define a 3D grid for visualization
x_range = np.linspace(-3, 3, 18)
y_range = np.linspace(-3, 3, 18)
z_range = np.linspace(-3, 3, 7)
X_grid, Y_grid, Z_grid = np.meshgrid(x_range, y_range, z_range)


# Define a function to compute the magnetic field
def compute_magnetic_field(x, y, z, x_coil, y_coil, z_coil):
    """Compute the magnetic field using the Biot-Savart law."""
    Bx, By, Bz = np.zeros_like(x), np.zeros_like(y), np.zeros_like(z)
    mu_0 = 4 * np.pi * 1e-7  # Vacuum permeability
    I = 1  # Assume unit current

    dl_x, dl_y, dl_z = np.gradient(x_coil), np.gradient(y_coil), np.gradient(z_coil)

    for i in range(len(x_coil)):
        rx, ry, rz = x - x_coil[i], y - y_coil[i], z - z_coil[i]
        r = np.sqrt(rx**2 + ry**2 + rz**2) + 1e-9  # Avoid division by zero

        # dL vector
        dL = np.array([dl_x[i], dl_y[i], dl_z[i]])  # Shape (3,)

        # r vector
        r_vec = np.array([rx, ry, rz])  # Shape (3, grid_size, grid_size, grid_size)

        # Compute cross product using np.cross along axis 0
        dB = np.cross(dL[:, np.newaxis, np.newaxis, np.newaxis], r_vec, axis=0) / (r**3)

        # Accumulate the contributions
        Bx += dB[0]
        By += dB[1]
        Bz += dB[2]

    return Bx * mu_0 * I, By * mu_0 * I, Bz * mu_0 * I


# Define a function to generate a helical coil
def get_coil(type = "helical"):
    theta = np.linspace(0, num_turns * 2 * np.pi, points_per_turn)
    phi = (2 + 2 / 5) * theta  # Rodin winding ratio with phase shift

    # # Generate helical coil
    t = np.linspace(0, 2 * np.pi * turns, turns * points_per_turn)
    x_helical_coil = R * np.cos(t)
    y_helical_coil = R * np.sin(t)
    z_helical_coil = np.linspace(-height / 2, height / 2, turns * points_per_turn)
    x_rodin_coil = (R + r * np.cos(phi)) * np.cos(theta)
    y_rodin_coil = (R + r * np.cos(phi)) * np.sin(theta)
    z_rodin_coil = r * np.sin(phi)
    if type == "helical":
        x = x_helical_coil
        y = y_helical_coil
        z = z_helical_coil
    else:
        x = x_rodin_coil
        y = y_rodin_coil
        z = z_rodin_coil

    return x, y, z


# Generate the coil
x_coil, y_coil, z_coil = get_coil("helical")
# Compute the magnetic field at each point in the grid
Bx, By, Bz = compute_magnetic_field(X_grid, Y_grid, Z_grid, x_coil, y_coil, z_coil)
# Normalize the magnetic field vectors
B_magnitude = np.sqrt(Bx**2 + By**2 + Bz**2) + 1e-9
Bx, By, Bz = Bx / B_magnitude, By / B_magnitude, Bz / B_magnitude
# Visualization using quiver (arrows) instead of Line3DCollection
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")
# Plot the coil
ax.plot(x_coil, y_coil, z_coil, color="red", linewidth=1, label="Coil")
# Use quiver to plot the magnetic field vectors
ax.quiver(X_grid, Y_grid, Z_grid, Bx, By, Bz, length=0.3, normalize=True, color="blue")
# Set limits and labels
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Magnetic Field Around a Helical Coil (Arrows)")
ax.legend()

# Generate the coil
x_coil_rodin, y_coil_rodin, z_coil_rodin = get_coil("rodin")
# Compute the magnetic field at each point in the grid
Bx_rodin, By_rodin, Bz_rodin = compute_magnetic_field(X_grid, Y_grid, Z_grid, x_coil_rodin, y_coil_rodin, z_coil_rodin)
# Normalize the magnetic field vectors
B_magnitude_rodin = np.sqrt(Bx_rodin**2 + By_rodin**2 + Bz_rodin**2) + 1e-9
Bx_rodin, By_rodin, Bz_rodin = Bx_rodin / B_magnitude_rodin, By_rodin / B_magnitude_rodin, Bz_rodin / B_magnitude_rodin
# Visualization using quiver (arrows) instead of Line3DCollection
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")
# Plot the coil
ax.plot(x_coil_rodin, y_coil_rodin, z_coil_rodin, color="red", linewidth=0.5, label="Coil")
# Use quiver to plot the magnetic field vectors
ax.quiver(X_grid, Y_grid, Z_grid, Bx_rodin, By_rodin, Bz_rodin, length=0.3, normalize=True, color="blue")
# Set limits and labels
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Magnetic Field Around a Rodin Coil (Arrows)")
ax.legend()

plt.show()


