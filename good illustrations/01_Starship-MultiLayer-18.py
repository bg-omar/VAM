# 3D Visualization of the Starship Coil - Multiple Layers

import numpy as np

import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

coil_corners = 18
# Define parameters for multi-layer 3D coil
num_layers = 4  # Number of layers in the coil
layer_spacing = 0.1  # Distance between layers in the z-axis

total_corners = coil_corners * 1

rotation_steps=0
rotation_angle = (2 * np.pi / coil_corners)
# Define provided base sequence
# 1 + 7 mod 18
base_sequence = [1, 8, 15, 4, 11, 18, 7, 14, 3, 10, 17, 6, 13, 2, 9, 16, 5, 12, 1]

# Create explicit sequences as per user request
sequence_A_forward = [((num - 0 - 1) % (coil_corners)) + 1 for num in base_sequence]
# Create explicit sequences as per user request
sequence_A_backwards = [((num - 0 - 1) % (coil_corners)) + 1 for num in base_sequence[::-1]]

# Points setup
angles = np.linspace(0, 2 * np.pi, (coil_corners) +1)[:-1]
positions = {i+1: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles)}
segment_shift = ((2 * np.pi / (coil_corners)) / 3)


# Recalculate positions with adjusted angles for rotation and reversed numbering
angles_rotated = np.linspace(0, 2 * np.pi, (coil_corners)+1)[:-1] - np.pi*1.5 +(2*np.pi*(1/(coil_corners))) # Rotate 90° counterclockwise
angles_rotated = angles_rotated[::-1]  # Reverse numbering for clockwise count
positions_rotated = {i+1: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles_rotated)}

angles_rotated += rotation_angle


# Function to generate multi-layer wire paths
def generate_3d_wire(sequence, segment, z_layer, base_color, style, alpha=1.0):
    """Generates a 3D multi-layer wire visualization with smooth height increase."""
    angles = np.linspace(0, 2 * np.pi, coil_corners + 1)[:-1] - np.pi * 1.5 + (2 * np.pi * (1 / coil_corners))
    angles = angles[::-1]  # Reverse numbering for clockwise count
    segment_shift = (2 * np.pi / coil_corners)

    total_points = len(sequence) - 1  # To normalize height increase

    for i in range(total_points):
        num = sequence[i]
        next_num = sequence[i + 1]

        # Angles adjusted by segment
        angle_start = angles[(num - 1) % coil_corners] + segment_shift * (segment - 1)
        angle_end = angles[(next_num - 1) % coil_corners] + segment_shift * (segment - 1)

        x_start, y_start = np.cos(angle_start), np.sin(angle_start)
        x_end, y_end = np.cos(angle_end), np.sin(angle_end)

        # Smooth height interpolation
        z_start = z_layer + (layer_spacing * (i / total_points))
        z_end = z_layer + (layer_spacing * ((i + 1) / total_points))

        ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end],
                color=base_color, linestyle=style, linewidth=2, alpha=alpha)


# Setup 3D plot
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# Plot multiple layers of the coil
for layer in range(num_layers):
    z_layer = layer * layer_spacing

    # Phase A (Blue)
    generate_3d_wire(sequence_A_forward, 1, z_layer, 'blue', '-', alpha=0.9)
    generate_3d_wire(sequence_A_backwards, 1, z_layer, 'red', '-', alpha=0.9)





# Set plot title and display
ax.set_title("3D Multi-Layer Starship Rodin Coil", fontsize=16)
# Set axis labels
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
# Show legend
# ax.legend()
ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio



# ✅ Get the script filename dynamically
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()