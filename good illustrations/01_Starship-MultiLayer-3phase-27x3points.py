# 3D Visualization of the Starship Coil - Multiple Layers

import numpy as np

import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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


# Plot multiple layers of the coil
for layer in range(num_layers):
    z_layer = layer * layer_spacing-0.5

    # Phase A (Blue)
    generate_3d_wire(sequence_A_forward, 1, z_layer, 'blue', '-', alpha=0.9)
    generate_3d_wire(sequence_A_neutral, 2, z_layer, 'blue', '--', alpha=0.3)
    generate_3d_wire(sequence_A_backward, 3, z_layer, 'cyan', '-', alpha=0.9)

    # Phase B (Red)
    generate_3d_wire(sequence_B_forward, 1, z_layer, 'red', '-', alpha=0.9)
    generate_3d_wire(sequence_B_neutral, 2, z_layer, 'red', '--', alpha=0.3)
    generate_3d_wire(sequence_B_backward, 3, z_layer, 'orange', '-', alpha=0.9)

    # Phase C (Green)
    generate_3d_wire(sequence_C_forward, 1, z_layer, 'green', '-', alpha=0.9)
    generate_3d_wire(sequence_C_neutral, 2, z_layer, 'green', '--', alpha=0.3)
    generate_3d_wire(sequence_C_backward, 3, z_layer, 'purple', '-', alpha=0.9)

# Set plot title and display
ax.set_title("3D Multi-Layer Starship Rodin Coil", fontsize=16)
# Set axis labels
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
# Show legend
# ax.legend()
ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio



# ✅ Get the script filename dynamically
import os
from datetime import datetime
script_name = os.path.splitext(os.path.basename(__file__))[0]
timestamp = datetime.now().strftime("%H%M%S")
filename = f"{script_name}_{timestamp}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()