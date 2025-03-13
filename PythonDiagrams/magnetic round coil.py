
import numpy as np

import matplotlib
from sympy.abc import alpha

matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# Define coil parameters
turns = 12  # Number of turns in the helical coil
height = 1  # Height of the coil
points_per_turn = 288  # Resolution of the coil
R, r = 0.5, 0.5  # Major and minor radius of the torus
num_turns = 12  # Total Rodin turns per phase
time_steps = 100  # Number of frames in animation
omega = 2 * np.pi * 1  # Angular frequency (1 Hz)
scaling_factor = 0.1  # Scale factor for E-field visualization
# Define the toroidal grid
theta = np.linspace(0, 2 * np.pi, points_per_turn)  # Angle around the central ring
phi = np.linspace(0, 2 * np.pi, points_per_turn)  # Angle around the tube
Theta, Phi = np.meshgrid(theta, phi)
# Compute torus coordinates
X = (R + r * np.cos(Phi)) * np.cos(Theta)
Y = (R + r * np.cos(Phi)) * np.sin(Theta)
Z = r * np.sin(Phi)
# Define a 3D grid for visualization
x_range = np.linspace(-2, 2, 24)
y_range = np.linspace(-2, 2, 24)
z_range = np.linspace(-1, 1, 9)
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
    t = np.linspace(0, 2 * np.pi * turns, points_per_turn)

    # Define a helical spiral through the center hole
    num_helix_turns = 72  # Number of turns of the spiral
    helix_theta = np.linspace(0, 2 * np.pi, points_per_turn*4)  # More resolution
    helix_phi = num_helix_turns * helix_theta  # Wraps 3 times around r per full revolution of R

    # Compute torus coordinates
    X_torus = (R + r * np.cos(helix_phi)) * np.cos(helix_theta)
    Y_torus = (R + r * np.cos(helix_phi)) * np.sin(helix_theta)
    Z_torus = r * np.sin(helix_phi)
    x_helical_coil = 2 * R * np.cos(t)
    y_helical_coil = 2 * R * np.sin(t)
    z_helical_coil = np.linspace(-height / 2, height / 2, points_per_turn)
    x_rodin_coil = (R + r * np.cos(phi)) * np.cos(theta)
    y_rodin_coil = (R + r * np.cos(phi)) * np.sin(theta)
    z_rodin_coil = r * np.sin(phi)
    if type == "helical":
        x = x_helical_coil
        y = y_helical_coil
        z = z_helical_coil
    elif type == "rodin":
        x = x_rodin_coil
        y = y_rodin_coil
        z = z_rodin_coil
    else:
        x = X_torus
        y = Y_torus
        z = Z_torus
    return x, y, z

def tangential_vector(field_radius, phase_adjustment, Bx_list, By_list, Bz_list, X_field, Y_field, Z_field):
    global i
    for i in range(len(x_coil//2)):
        # Define a local plane normal to the coil's tangent
        if i == len(x_coil) - 1:  # Avoid index out of bounds
            i_prev = i - 1
        else:
            i_prev = i + 1

        # Compute local tangent vector (coil direction)
        Tx = x_coil[i] - x_coil[i_prev]
        Ty = y_coil[i] - y_coil[i_prev]
        Tz = z_coil[i] - z_coil[i_prev]

        T_mag = np.sqrt(Tx ** 2 + Ty ** 2 + Tz ** 2) + 1e-9
        Tx, Ty, Tz = Tx / T_mag, Ty / T_mag, Tz / T_mag  # Normalize tangent

        # Generate two perpendicular vectors to form the circular field
        if np.abs(Tz) < 0.9:  # Avoid near-zero cross-product issues
            Nx, Ny, Nz = -Ty, Tx, 0  # Arbitrary perpendicular vector
        else:
            Nx, Ny, Nz = 0, -Tz, Ty

        # Normalize perpendicular vector
        N_mag = np.sqrt(Nx ** 2 + Ny ** 2 + Nz ** 2) + 1e-9
        Nx, Ny, Nz = Nx / N_mag, Ny / N_mag, Nz / N_mag

        # Second perpendicular vector (cross product of T and N)
        Mx, My, Mz = Ty * Nz - Tz * Ny, Tz * Nx - Tx * Nz, Tx * Ny - Ty * Nx

        # Generate field points and correctly rotating circular field vectors
        for angle in angles:
            X_field.append(x_coil[i] + field_radius * (Nx * np.cos(angle + phase_adjustment) + Mx * np.sin(angle + phase_adjustment)))
            Y_field.append(y_coil[i] + field_radius * (Ny * np.cos(angle + phase_adjustment) + My * np.sin(angle + phase_adjustment)))
            Z_field.append(z_coil[i] + field_radius * (Nz * np.cos(angle + phase_adjustment) + Mz * np.sin(angle + phase_adjustment)))

            # Field vectors should **rotate** tangentially around the wire
            Bx_list.append(-Nx * np.sin(angle + phase_adjustment) + Mx * np.cos(angle + phase_adjustment))
            By_list.append(-Ny * np.sin(angle + phase_adjustment) + My * np.cos(angle + phase_adjustment))
            Bz_list.append(-Nz * np.sin(angle + phase_adjustment) + Mz * np.cos(angle + phase_adjustment))
    return Bx_list, By_list, Bz_list, X_field, Y_field, Z_field


def plot_radial_vectors(field_radius, phase_adjustment, num_field_points):
    global angles
    # Generate field points around each wire segment
    angles = np.linspace(0, 2 * np.pi, num_field_points, endpoint=False)
    Bx_list, By_list, Bz_list = [], [], []
    X_field, Y_field, Z_field = [], [], []
    Bx_list, By_list, Bz_list, X_field, Y_field, Z_field = tangential_vector(field_radius, phase_adjustment, Bx_list, By_list, Bz_list,
                                                                             X_field, Y_field, Z_field)
    # Convert to arrays
    X_field, Y_field, Z_field = np.array(X_field), np.array(Y_field), np.array(Z_field)
    Bx_list, By_list, Bz_list = np.array(Bx_list), np.array(By_list), np.array(Bz_list)
    # Compute field magnitudes for coloring
    B_magnitude_flat = np.sqrt(Bx_list.flatten() ** 2 + By_list.flatten() ** 2 + Bz_list.flatten() ** 2)
    # Get colormap correctly
    B_colormap = plt.colormaps["turbo"]  # ✅ Correct Matplotlib 3.7+ syntax
    B_colors = B_colormap(B_magnitude_flat / np.max(B_magnitude_flat))
    # Plot magnetic field vectors around the wire
    ax.quiver(X_field, Y_field, Z_field, Bx_list, By_list, Bz_list,
              linewidth=1, length=0.1, alpha=0.2, normalize=True, color=B_colors)

def set_numers(num_labels):
    global i
    t = np.linspace(0, 2 * np.pi, 300)
    for i in range(num_labels):
        index = i * len(t) // num_labels
        ax.text(2 * R * np.cos(t)[index], 2 * R * np.sin(t)[index], 0, str(i + 1), color='black', fontsize=14,
                ha='center', va='center')

def set_labels():
    # Set limits and labels
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()



# Create multiple subplots for different views
fig, axes = plt.subplots(1, 3, figsize=(20, 15), subplot_kw={'projection': '3d'})
view_angles = [
    (0, 90),   # Top view
    (0, 90),    # Side view
    (0, 90)    # Angled view
]
rgb = 1
titles = ["WrappedField Top View", "WrappedField Side View", "WrappedField Angled View"]
for ax, (elev, azim), title in zip(axes, view_angles, titles):
    set_numers(12)

    if rgb == 1:
        x_coil, y_coil, z_coil = get_coil("rodin")
        # Plot the Rodin coil
        ax.plot(x_coil, y_coil, z_coil,
                color="red", linewidth=1, label="Rodin Coil")

        # Define points around the wire for field visualization
        num_field_points = 5  # Number of points in the plane around each coil segment
        field_radius = 0.2  # Radius of the circular magnetic field lines

        plot_radial_vectors(field_radius, 0, 3)
        plot_radial_vectors(field_radius * 2, np.pi / 3, 6)
        plot_radial_vectors(field_radius * 3, np.pi / 6, 9)
    if rgb == 2:
        x_coil, y_coil, z_coil = get_coil("helical")
        # Compute the magnetic field at each point in the grid
        Bx, By, Bz = compute_magnetic_field(X_grid, Y_grid, Z_grid, x_coil, y_coil, z_coil)
        # Normalize the magnetic field vectors
        B_magnitude = np.sqrt(Bx ** 2 + By ** 2 + Bz ** 2) + 1e-9
        Bx, By, Bz = Bx / B_magnitude, By / B_magnitude, Bz / B_magnitude
        B_magnitude_flat = np.sqrt(Bx.flatten() ** 2 + By.flatten() ** 2 + Bz.flatten() ** 2)
        # Get colormap correctly
        B_colormap = plt.colormaps["turbo"]  # ✅ Correct Matplotlib 3.7+ syntax
        B_colors = B_colormap(B_magnitude_flat / np.max(B_magnitude_flat))
        # Plot the coil
        ax.plot(x_coil, y_coil, z_coil, color="red", linewidth=1, label="Helix Coil")
        # Use quiver to plot the magnetic field vectors
        ax.quiver(X_grid, Y_grid, Z_grid, Bx, By, Bz, linewidth=0.5,length=0.2, normalize=True, color=B_colors)
    if rgb == 3:
        # Generate the coil
        x_coil_rodin, y_coil_rodin, z_coil_rodin = get_coil("rodin")
        # Compute the magnetic field at each point in the grid
        Bx_rodin, By_rodin, Bz_rodin = compute_magnetic_field(X_grid, Y_grid, Z_grid, x_coil_rodin, y_coil_rodin,
                                                              z_coil_rodin)
        # Normalize the magnetic field vectors
        B_magnitude_rodin = np.sqrt(Bx_rodin ** 2 + By_rodin ** 2 + Bz_rodin ** 2) + 1e-9
        Bx_rodin, By_rodin, Bz_rodin = Bx_rodin / B_magnitude_rodin, By_rodin / B_magnitude_rodin, Bz_rodin / B_magnitude_rodin
        B_magnitude_flat = np.sqrt(Bx_rodin.flatten() ** 2 + By_rodin.flatten() ** 2 + Bz_rodin.flatten() ** 2)
        # Get colormap correctly
        B_colormap = plt.colormaps["turbo"]  # ✅ Correct Matplotlib 3.7+ syntax
        B_colors = B_colormap(B_magnitude_flat / np.max(B_magnitude_flat))
        # Plot the coil
        ax.plot(x_coil_rodin, y_coil_rodin, z_coil_rodin, color="red", linewidth=0.5, label="Rodin Coil")
        # Use quiver to plot the magnetic field vectors
        ax.quiver(X_grid, Y_grid, Z_grid, Bx_rodin, By_rodin, Bz_rodin, linewidth=0.5,length=0.2, normalize=True, color=B_colors)

    set_labels()
    rgb += 1
plt.tight_layout()
plt.show()
