
import numpy as np
import matplotlib
from setuptools.command.rotate import rotate
from sympy.abc import alpha
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection


gridsize = 1

# Define points around the wire for field visualization
num_field_points = 5  # Number of points in the plane around each coil segment
field_radius = 0.2  # Radius of the circular magnetic field lines
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
x_range = np.linspace(-gridsize, gridsize, 9)
y_range = np.linspace(-gridsize, gridsize, 9)
z_range = np.linspace(-0.5, 0.5, 9)
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
    helix_theta = np.linspace(0, num_turns*2 * np.pi, points_per_turn*4)  # More resolution
    helix_phi = num_helix_turns * helix_theta  # Wraps 3 times around r per full revolution of R

    # Compute torus coordinates
    X_torus = (R + r * np.cos(helix_phi)) * np.cos(helix_theta)
    Y_torus = (R + r * np.cos(helix_phi)) * np.sin(helix_theta)
    Z_torus = r * np.sin(helix_phi)
    x_helical_coil = 2 * R * np.cos(t)
    y_helical_coil = 2 * R * np.sin(t)
    z_helical_coil = np.linspace(-height / 2, height / 2, points_per_turn)
    x_rodin_coil2 = (R + .5*r * np.cos(phi)) * np.cos(theta)
    y_rodin_coil2 = (R + .5*r * np.cos(phi)) * np.sin(theta)
    z_rodin_coil2 = .5*r * np.sin(phi)
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
    elif type == "rodin2":
        x = x_rodin_coil2
        y = y_rodin_coil2
        z = z_rodin_coil2
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
    # Use the angle of direction to define the color
    angles = np.arctan2(By_list.flatten() , Bx_list.flatten() )  # Angle in the XY plane
    colormap = plt.colormaps["turbo"]  # ✅ Correct Matplotlib 3.7+ syntax
    colors = colormap((angles + np.pi) / (2 * np.pi))  # Normalize angles between 0 and 1

    # Plot magnetic field vectors around the wire
    ax.quiver(X_field, Y_field, Z_field, Bx_list, By_list, Bz_list,
              linewidth=1, length=0.1, alpha=0.2, normalize=True, color=colors)

def set_numers(ax, num_labels):
    global i
    t = np.linspace(0, 2 * np.pi, 300)
    for i in range(num_labels):
        index = i * len(t) // num_labels
        ax.text(2 * R * np.cos(t)[index], 2 * R * np.sin(t)[index], 0, str(i + 1), color='black', fontsize=14,
                ha='center', va='center')

def set_labels(ax, elev, azim):
    # Set limits and labels
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(-gridsize, gridsize)
    ax.set_ylim(-gridsize, gridsize)
    ax.set_zlim(-gridsize, gridsize)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()



# Create multiple subplots for different views
fig, axes = plt.subplots(2, 2, figsize=(12, 12), subplot_kw={'projection': '3d'})
view_angles = [
    (50, 150),   # Top view
    (50, 150),    # Side view
    (50, 150),    # Angled view
    (50, 150)    # Angled view
]
rgb = 1
titles = ["Rodin", "Helical", "Rodin", "Star-shaped"]
for ax, (elev, azim), title in zip(axes.flatten(), view_angles, titles):

    if rgb == 1:
        x_coil, y_coil, z_coil = get_coil("rodin")
        # Plot the Rodin coil
        ax.plot(x_coil, y_coil, z_coil,
                color="red", linewidth=1, label="Rodin Coil")

        # plot_radial_vectors(field_radius, 0, 3)
        # plot_radial_vectors(field_radius * 2, np.pi / 3, 6)
        # plot_radial_vectors(field_radius * 3, np.pi / 6, 9)
    if rgb == 2:
        x_coil, y_coil, z_coil = get_coil("helical")

    if rgb == 3:
        # Generate the coil
        x_coil, y_coil, z_coil = get_coil("rodin2")
    if rgb == 4:
        set_numers(ax, 9)
        # Define the base sequence for the star-shaped coil using only 9 points
        base_sequence = [1, 5, 9, 4, 8, 3, 7, 2, 6]  # This sequence should only use 9 unique points

        # Define number of turns in the coil and spacing in the Z-direction
        num_layers = 10  # Number of full cycles up the coil
        z_spacing = 0.1  # Distance between layers in the Z-direction

        # Define the 9 points evenly spaced around a circle
        angles = np.linspace(0, 2 * np.pi, 10)[:-1]  # 9 points in a circular arrangement
        positions = {i+1: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles)}

        # Generate 3D coil wire path using only the 9 points
        x_coil, y_coil, z_coil = [], [], []
        for turn in range(num_layers):
            z_layer = turn * z_spacing  # Increase height per turn
            for num in base_sequence:
                x, y = positions[num]  # Get (x, y) position from the sequence
                x_coil.append(x)
                y_coil.append(y)
                z_coil.append(z_layer - (num_layers * z_spacing) * 0.5)

        # Mark each coil point
        ax.scatter(x_coil, y_coil, z_coil, color='red', s=10, label="Points")



    # Compute the magnetic field at each point in the grid
    Bx, By, Bz = compute_magnetic_field(X_grid, Y_grid, Z_grid, x_coil, y_coil, z_coil)
    B_magnitude = np.sqrt(Bx ** 2 + By ** 2 + Bz ** 2) + 1e-9
    Bx, By, Bz = Bx / B_magnitude, By / B_magnitude, Bz / B_magnitude
    B_magnitude_flat = np.sqrt(Bx.flatten() ** 2 + By.flatten() ** 2 + Bz.flatten() ** 2)

    ax.plot(x_coil, y_coil, z_coil, color="red", linewidth=1, label="Coil")

    rotation_axis = "x"  # Change to "x" or "y" as needed
    pole_axis = "y"  # Change to "x" or "y" as needed

    if rotation_axis == "z":
        dBy_dx = np.gradient(By, axis=0)  # ∂By/∂x
        dBx_dy = np.gradient(Bx, axis=1)  # ∂Bx/∂y
        rotation_direction = dBy_dx - dBx_dy  # Rotation in XY-plane (Z-axis rotation)

    elif rotation_axis == "y":
        dBx_dz = np.gradient(Bx, axis=2)  # ∂Bx/∂z
        dBz_dx = np.gradient(Bz, axis=0)  # ∂Bz/∂x
        rotation_direction = dBx_dz - dBz_dx  # Rotation in XZ-plane (Y-axis rotation)

    elif rotation_axis == "x":
        dBz_dy = np.gradient(Bz, axis=1)  # ∂Bz/∂y
        dBy_dz = np.gradient(By, axis=2)  # ∂By/∂z
        rotation_direction = dBz_dy - dBy_dz  # Rotation in YZ-plane (X-axis rotation)

    if pole_axis == "z":
        dBy_dx = np.gradient(By, axis=0)  # ∂By/∂x
        dBx_dy = np.gradient(Bx, axis=1)  # ∂Bx/∂y
        pole_direction = dBy_dx - dBx_dy  # Rotation in XY-plane (Z-axis rotation)

    elif pole_axis == "y":
        dBx_dz = np.gradient(Bx, axis=2)  # ∂Bx/∂z
        dBz_dx = np.gradient(Bz, axis=0)  # ∂Bz/∂x
        pole_direction = dBx_dz - dBz_dx  # Rotation in XZ-plane (Y-axis rotation)

    elif pole_axis == "x":
        dBz_dy = np.gradient(Bz, axis=1)  # ∂Bz/∂y
        dBy_dz = np.gradient(By, axis=2)  # ∂By/∂z
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
    blend_factor = 1   # Adjust for color dominance
    final_colors = (blend_factor * rotate_colors + (1 - blend_factor) * pole_colors)  # Weighted blend

    # --- 4. Plot with combined colors ---
    ax.quiver(
        X_grid, Y_grid, Z_grid,
        Bx, By, Bz,
        linewidth=0.5, length=0.2, normalize=True, color=final_colors, label="Vectors"
    )
    set_labels(ax, elev, azim)
    rgb += 1
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()
