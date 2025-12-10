import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# ==========================
# Geometry parameters
# ==========================
# (5,12) torus knot on a torus with golden-ratio aspect
p, q = 5, 12                      # torus knot type
phi = (1 + np.sqrt(5)) / 2       # golden ratio

R = 0.75                          # major radius of torus (arbitrary units)
r = R / phi                       # minor radius (golden aspect)

# Parameter range for the knot
num_steps = 4000
t = np.linspace(0, 2 * np.pi, num_steps)


def torus_knot_5_12(t, cell_phase=0.0, mirror=False):
    """
    (5,12) torus knot with per-cell phase offset.

    cell_phase in [0,1) means: fraction of ONE toroidal sector (2π/q).
    So:
      cell_phase=0     => starts at n
      cell_phase=1/3   => starts at n + 1/3 of the sector
      cell_phase=2/3   => starts at n + 2/3 of the sector
    """
    # convert per-cell phase into a t-shift
    dt = cell_phase * (2 * np.pi / q)
    tp = t + dt

    theta = p * tp        # toroidal angle
    phi_t = q * tp        # poloidal angle

    x = (R + r * np.cos(phi_t)) * np.cos(theta)
    y = (R + r * np.cos(phi_t)) * np.sin(theta)
    z = r * np.sin(phi_t)

    if mirror:
        z = -z  # CCW / mirrored coil

    return x, y, z


# ==========================
# Build 3-phase CW + 3-phase CCW
# ==========================

# three phases inside each of the q=12 toroidal slots
cell_phases = [0.0, 1.0 / 3.0, 2.0 / 3.0]

# colors for visualization
colors_cw = ['crimson', 'darkorange', 'gold']
colors_ccw = ['royalblue', 'navy', 'teal']

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# --- 3-phase CW (normal) ---
for cp, col in zip(cell_phases, colors_cw):
    x, y, z = torus_knot_5_12(t, cell_phase=cp, mirror=False)
    ax.plot(x, y, z, color=col, linewidth=2, label=f'CW phase {cp:.2f}')

# --- 3-phase CCW (mirrored) ---
for cp, col in zip(cell_phases, colors_ccw):
    x, y, z = torus_knot_5_12(t, cell_phase=cp, mirror=True)
    ax.plot(x, y, z, color=col, linestyle='--', linewidth=2,
            label=f'CCW phase {cp:.2f}')

# ==========================
# Optional: torus wireframe for context
# ==========================
theta_grid = np.linspace(0, 2 * np.pi, 80)
phi_grid = np.linspace(0, 2 * np.pi, 40)
Theta, Phi = np.meshgrid(theta_grid, phi_grid)

X_torus = (R + r * np.cos(Phi)) * np.cos(Theta)
Y_torus = (R + r * np.cos(Phi)) * np.sin(Theta)
Z_torus = r * np.sin(Phi)

ax.plot_wireframe(X_torus, Y_torus, Z_torus,
                  color='gray', alpha=0.15, linewidth=0.5)

# ==========================
# Plot cosmetics
# ==========================
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('(5,12) Starship Coil\n3-phase CW + 3-phase CCW (per-cell phases 0, 1/3, 2/3)')

# Equal aspect ratio
max_range = np.array([X_torus.max()-X_torus.min(),
                      Y_torus.max()-Y_torus.min(),
                      Z_torus.max()-Z_torus.min()]).max() / 2.0

mid_x = (X_torus.max()+X_torus.min()) * 0.5
mid_y = (Y_torus.max()+Y_torus.min()) * 0.5
mid_z = (Z_torus.max()+Z_torus.min()) * 0.5

ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)
ax.set_box_aspect([1, 1, 1])

ax.legend(loc='upper left', fontsize=8)
plt.tight_layout()
plt.show()

num_turns=10
num_points=1000

# Reimporting necessary libraries after state reset
import os
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt

# Define parameters for the ring torus (R = 4r)
R_ring = 0.75  # Major radius of the ring torus
r_ring = 0.125  # Minor radius of the ring torus

# Define parameters for the horn torus (R = 4r)
R_horn = 0.5  # Major radius of the horn torus
r_horn = 1  # Minor radius of the horn torus

# Define the grid for the tori
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, 2 * np.pi, 100)
theta, phi = np.meshgrid(theta, phi)

# Parametric equations for the ring torus
X_ring = (R_ring + r_ring * np.cos(phi)) * np.cos(theta)
Y_ring = (R_ring + r_ring * np.cos(phi)) * np.sin(theta)
Z_ring = r_ring * np.sin(phi)

# Parametric equations for the horn torus
X_horn = (R_horn + r_horn * np.cos(phi)) * np.cos(theta)
Y_horn = (R_horn + r_horn * np.cos(phi)) * np.sin(theta)
Z_horn = r_horn * np.sin(phi)


# Function to generate Rodin coil windings
def generate_rodin_coil(R, r, num_turns=12, num_points=1000):
    """
    Generate Rodin coil windings in a toroidal coordinate system.

    Parameters:
    R -- Major radius of the torus
    r -- Minor radius of the torus
    num_turns -- Number of full turns around the torus
    num_points -- Resolution of the coil path

    Returns:
    x, y, z -- Coordinates of the Rodin coil winding
    """
    theta = np.linspace(0, num_turns * 2 * np.pi, num_points)
    phi =  12 *np.linspace(0, num_turns * 2 * np.pi, num_points)

    # Compute Rodin coil path
    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)
    return x, y, z

# Function to generate 3-phase shifted windings
def generate_rodin_3phase(R, r, num_turns=12, num_points=1000):
    """
    Generate 3-phase interwoven Rodin coil windings.

    Returns:
    Three sets of x, y, z coordinates corresponding to phase shifts of 120° each.
    """
    x1, y1, z1 = generate_rodin_coil(R, r, num_turns, num_points)
    x2, y2, z2 = generate_rodin_coil(R, r, num_turns, num_points)
    x3, y3, z3 = generate_rodin_coil(R, r, num_turns, num_points)

    # Apply 120-degree phase shifts
    theta_shift = 2 * np.pi / 3
    theta = np.linspace(0, num_turns * 2 * np.pi, num_points)
    phi = (2 + 2 / 5) * theta  # Adjusted winding ratio for Rodin pattern
    x2 = (R + r * np.cos(phi + theta_shift)) * np.cos(theta + theta_shift)
    y2 = (R + r * np.cos(phi + theta_shift)) * np.sin(theta + theta_shift)
    z2 = r * np.sin(phi + theta_shift)

    x3 = (R + r * np.cos(phi - theta_shift)) * np.cos(theta - theta_shift)
    y3 = (R + r * np.cos(phi - theta_shift)) * np.sin(theta - theta_shift)
    z3 = r * np.sin(phi - theta_shift)

    return (x1, y1, z1), (x2, y2, z2), (x3, y3, z3)




rotation_steps=0
rotation_angle = (2 * np.pi / 27) / 3
# Define provided base sequence
base_sequence = [1, 5, 9, 4, 8, 3, 7, 2, 6, 1]

# Create explicit sequences as per user request
sequence_A_forward = [((num * 3 - 0 - 1) % 27) + 1 for num in base_sequence]
sequence_A_neutral = [((num * 3 - 0 - 1) % 27) + 1 for num in base_sequence]
sequence_A_backward = [((num * 3 - 0 - 1) % 27) + 1 for num in base_sequence]

sequence_B_forward = [((num * 3 - 1 - 1) % 27) + 1 for num in base_sequence]
sequence_B_neutral = [((num * 3 - 1 - 1) % 27) + 1 for num in base_sequence]
sequence_B_backward = [((num * 3 - 1 - 1) % 27) + 1 for num in base_sequence]

sequence_C_forward = [((num * 3 - 2 - 1) % 27) + 1 for num in base_sequence]
sequence_C_neutral = [((num * 3 - 2 - 1) % 27) + 1 for num in base_sequence]
sequence_C_backward = [((num * 3 - 2 - 1) % 27) + 1 for num in base_sequence]

# Points setup
angles = np.linspace(0, 2 * np.pi, 28)[:-1]
positions = {i+1: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles)}
segment_shift = ((2 * np.pi / 27) / 3)


# Recalculate positions with adjusted angles for rotation and reversed numbering
angles_rotated = np.linspace(0, 2 * np.pi, 28)[:-1] - np.pi*1.5 +(2*np.pi*(1/27)) # Rotate 90° counterclockwise
angles_rotated = angles_rotated[::-1]  # Reverse numbering for clockwise count
positions_rotated = {i+1: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles_rotated)}

angles_rotated += rotation_angle

# Define parameters for multi-layer 3D coil
num_layers = 10  # Number of layers in the coil
layer_spacing = 0.1  # Distance between layers in the z-axis



# Function to generate multi-layer wire paths
def generate_3d_wire(sequence, segment, z_layer, base_color, style, alpha=1.0):
    # Recalculate 3D positions for multiple layers
    angles = np.linspace(0, 2 * np.pi, 28)[:-1] - np.pi * 1.5 + (2 * np.pi * (1 / 27))
    angles = angles[::-1]  # Reverse numbering for clockwise count
    segment_shift = ((2 * np.pi / 27) / 3)
    """Generates a 3D multi-layer wire visualization."""
    for i in range(len(sequence) - 1):
        num = sequence[i]
        next_num = sequence[i + 1]

        # Apply rotation and segment shift
        angle_start = angles[(num - 1) % 27] + segment_shift * (segment - 1)
        angle_end = angles[(next_num - 1) % 27] + segment_shift * (segment - 1)

        x_start, y_start = np.cos(angle_start), np.sin(angle_start)
        x_end, y_end = np.cos(angle_end), np.sin(angle_end)

        # Move up one layer in z when sequence restarts
        z_start = z_layer
        z_end = z_layer

        if i == len(sequence) - 2:  # If reaching the end, move to next layer
            z_end = z_layer + layer_spacing

        ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end],
                color=base_color, linestyle=style, linewidth=2, alpha=alpha)

# Setup 3D plot
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')




# Function to plot the Rodin coil and its variations
def plot_rodin_coil():
    phi = (1 + np.sqrt(5)) / 2       # golden ratio

    R = 0.75                          # major radius of torus (arbitrary units)
    r = R / phi                       # minor radius (golden aspect)
    colors1 = ['crimson', 'darkred', 'gold']
    colors2 = ['dodgerblue', 'navy', 'darkorange']

    # Plot 3-phase Rodin coil windings
    (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = generate_rodin_3phase(R, r)
    ax.plot(x1, y1, z1, color=colors1[0], linewidth=2, label="Phase 1")
    ax.plot(x2, y2, z2, color=colors1[1], linewidth=2, label="Phase 2")
    ax.plot(x3, y3, z3, color=colors1[2], linewidth=2, label="Phase 3")

    # Plot 3-phase Rodin coil windings
    (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = generate_rodin_3phase(-R, r)
    ax.plot(x1, y1, z1, color=colors2[0], linewidth=2, label="Phase 1")
    ax.plot(x2, y2, z2, color=colors2[1], linewidth=2, label="Phase 2")
    ax.plot(x3, y3, z3, color=colors2[2], linewidth=2, label="Phase 3")

    # Plot the ring torus in blue with 85% transparency
    # ax.plot_surface(X_ring, Y_ring, Z_ring, rstride=5, cstride=5, color='blue', alpha=0.15, edgecolor='k')

    # Plot the horn torus in red with 90% transparency
    # ax.plot_surface(X_horn, Y_horn, Z_horn, rstride=5, cstride=5, color='red', alpha=0.10, edgecolor='k')

    # Plot toroidal frame
    theta = 5* np.linspace(0, 2 * np.pi, 100)
    phi = 12* np.linspace(0, 2 * np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)

    X = (R + r * np.cos(phi)) * np.cos(theta)
    Y = (R + r * np.cos(phi)) * np.sin(theta)
    Z = r * np.sin(phi)

    ax.plot_wireframe(X, Y, Z, color='gray', alpha=0.2, linewidth=0.5)


    # Set plot labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title("Optimized 3-Phase Rodin Coil")

    # Set equal aspect ratio
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_box_aspect([1,1,1])
    ax.legend()
    # ✅ Get the script filename dynamically
    import os
    from datetime import datetime
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"{script_name}_{timestamp}.png"
    plt.savefig(filename, dpi=150)  # Save image with high resolution
    plt.show()

# Generate and plot the optimized Rodin coil
plot_rodin_coil()