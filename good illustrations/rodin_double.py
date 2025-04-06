import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
R_horn = 1  # Major radius of the horn torus
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
    phi = (2 + 2/5) * theta  # Adjusted winding ratio for Rodin pattern

    # Compute Rodin coil path
    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)
    return x, y, z

# Function to generate 3-phase shifted windings
def generate_rodin_3phase(R, r, num_turns=10, num_points=1000):
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
    R, r = 1, 1  # Set torus major and minor radii
    colors1 = ['crimson', 'darkred', 'gold']
    colors2 = ['dodgerblue', 'navy', 'darkorange']

    # Plot 3-phase Rodin coil windings
    (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = generate_rodin_3phase(R, r)
    ax.plot(x1, y1, z1, color=colors1[0], linewidth=2, label="Phase 1")
    ax.plot(x2, y2, z2, color=colors1[1], linewidth=2, label="Phase 2")
    # ax.plot(x3, y3, z3, color=colors1[2], linewidth=2, label="Phase 3")

    # Plot 3-phase Rodin coil windings
    (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = generate_rodin_3phase(-R, r)
    ax.plot(x1, y1, z1, color=colors2[0], linewidth=2, label="Phase 1")
    ax.plot(x2, y2, z2, color=colors2[1], linewidth=2, label="Phase 2")
    # ax.plot(x3, y3, z3, color=colors2[2], linewidth=2, label="Phase 3")

    # Plot the ring torus in blue with 85% transparency
    # ax.plot_surface(X_ring, Y_ring, Z_ring, rstride=5, cstride=5, color='blue', alpha=0.15, edgecolor='k')

    # Plot the horn torus in red with 90% transparency
    # ax.plot_surface(X_horn, Y_horn, Z_horn, rstride=5, cstride=5, color='red', alpha=0.10, edgecolor='k')

    # Plot toroidal frame
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, 2 * np.pi, 100)
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