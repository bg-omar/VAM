import numpy as np

import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Corrected and clear visualization with sequences explicitly plotted and labeled with different colors and tints
coil_corners = 12
coil_amount = 3
# Define parameters for multi-layer 3D coil
num_layers = 10  # Number of layers in the coil
layer_spacing = 0.1  # Distance between layers in the z-axis

total_corners = coil_corners * coil_amount

rotation_steps=0
rotation_angle = (2 * np.pi / 12) / 3
# Define provided base sequence
base_sequence = [1, 6, 11, 4, 9, 2, 7, 12, 5, 10, 3, 8, 1]

# Create explicit sequences as per user request
sequence_A_forward = [((num * 3 - 0 - 1) % total_corners) + 1 for num in base_sequence]


sequence_B_forward = [((coil_corners + num * 3 - 1 - 1) % total_corners) + 1 for num in base_sequence]


sequence_C_forward = [(((coil_corners * 2) + num * 3 - 2 - 1) % total_corners) + 1 for num in base_sequence]

# Define number of turns in the coil and spacing in the Z-direction
num_turns = 10  # Number of full cycles up the coil
z_spacing = 0.1  # Distance between layers in the Z-direction

# Points setup
angles = np.linspace(0, 2 * np.pi, total_corners, endpoint=False)

positions = {i+1: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles)}
segment_shift = ((2 * np.pi / total_corners) / 3)


# Recalculate positions with adjusted angles for rotation and reversed numbering
angles_rotated = np.linspace(0, 2 * np.pi, total_corners, endpoint=False) - np.pi*1.5 +(2*np.pi*(1/total_corners)) # Rotate 90° counterclockwise
angles_rotated = angles_rotated[::-1]  # Reverse numbering for clockwise count
positions_rotated = {i+1: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles_rotated)}
angles_rotated += rotation_angle

# Generate 3D coil wire path using only the 9 points
x_vals, y_vals, z_vals = [], [], []
for turn in range(num_turns):
    z_layer = turn * z_spacing  # Increase height per turn
    for num in base_sequence:
        x, y = positions[num]  # Get (x, y) position from the sequence
        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(z_layer)  # Move up in height with each full loop


# Plot setup
fig = plt.figure(figsize=(14, 14))
ax = fig.add_subplot(111, projection='3d')
plt.axis('equal')

def plot_rotated_wire(sequence, segment, base_color, style, label, alpha=1.0, z_spacing=0.2, z_base=0.0):
    total_segments = len(sequence) - 1
    for i in range(total_segments):
        num = sequence[i]
        next_num = sequence[i + 1]

        angle_start = angles_rotated[(num - 1 + rotation_steps) % total_corners] + segment_shift * (segment - 1)
        angle_end = angles_rotated[(next_num - 1 + rotation_steps) % total_corners] + segment_shift * (segment - 1)

        x_start, y_start = np.cos(angle_start), np.sin(angle_start)
        x_end, y_end = np.cos(angle_end), np.sin(angle_end)

        # Smooth vertical increase relative to base layer
        z_start = z_base + z_spacing * (i / total_segments)
        z_end = z_base + z_spacing * ((i + 1) / total_segments)

        ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end],
                color=base_color, linestyle=style, linewidth=2, alpha=alpha, label=label if i == 0 else "")



# Plot multiple layers of the coil
for layer in range(num_turns):
    z_layer = -1 + layer * z_spacing  # Stretch layers apart more if needed

    plot_rotated_wire(sequence_A_forward, 1, 'blue', '-', 'Phase A Forward', alpha=0.9, z_spacing=1.0, z_base=z_layer)
    plot_rotated_wire(sequence_B_forward, 1, 'red', '-', 'Phase B Forward', alpha=0.9, z_spacing=1.0, z_base=z_layer)
    plot_rotated_wire(sequence_C_forward, 1, 'green', '-', 'Phase C Forward', alpha=0.9, z_spacing=1.0, z_base=z_layer)


# Biot–Savart Magnetic Field Calculator
mu_0 = 4 * np.pi * 1e-7  # Vacuum permeability

def biot_savart_field(segments, observation_point, current=1.0):
    B_total = np.zeros(3)
    for p1, p2 in segments:
        dl = np.array(p2) - np.array(p1)
        r_prime = (np.array(p1) + np.array(p2)) / 2
        r = np.array(observation_point)
        R = r - r_prime
        norm_R = np.linalg.norm(R)
        if norm_R == 0:
            continue
        dB = (mu_0 * current / (4 * np.pi)) * np.cross(dl, R) / (norm_R**3)
        B_total += dB
    return B_total

def generate_segments(sequence, segment_offset=0, z_spacing=1.0, z_base=0.0):
    segments = []
    total_segments = len(sequence) - 1
    for i in range(total_segments):
        num = sequence[i]
        next_num = sequence[i + 1]

        angle_start = angles_rotated[(num - 1 + rotation_steps) % total_corners] + segment_shift * segment_offset
        angle_end = angles_rotated[(next_num - 1 + rotation_steps) % total_corners] + segment_shift * segment_offset

        x_start, y_start = np.cos(angle_start), np.sin(angle_start)
        x_end, y_end = np.cos(angle_end), np.sin(angle_end)

        z_start = z_base + z_spacing * (i / total_segments)
        z_end = z_base + z_spacing * ((i + 1) / total_segments)

        segments.append(((x_start, y_start, z_start), (x_end, y_end, z_end)))
    return segments

# Gather segments from all layers and all phases
all_segments = []
for layer in range(num_turns):
    z_layer = -1 + layer * z_spacing
    all_segments += generate_segments(sequence_A_forward, segment_offset=0, z_base=z_layer)
    all_segments += generate_segments(sequence_B_forward, segment_offset=1, z_base=z_layer)
    all_segments += generate_segments(sequence_C_forward, segment_offset=2, z_base=z_layer)

# Observation point — center of the coil
observation_point = (0.0, 0.0, 0.0)
B = biot_savart_field(all_segments, observation_point)
print("Total magnetic field at center (0,0,0):", B, "Tesla")

# Define a 3D grid
grid_size = 5
span = 1.5  # Field region limits
lin = np.linspace(-span, span, grid_size)
X, Y, Z = np.meshgrid(lin, lin, lin)

# Allocate space for field components
Bx = np.zeros_like(X)
By = np.zeros_like(Y)
Bz = np.zeros_like(Z)

# Compute the B field at each point in the grid
for ix in range(grid_size):
    for iy in range(grid_size):
        for iz in range(grid_size):
            point = (X[ix, iy, iz], Y[ix, iy, iz], Z[ix, iy, iz])
            B = biot_savart_field(all_segments, point, current=1.0)
            Bx[ix, iy, iz], By[ix, iy, iz], Bz[ix, iy, iz] = B


ax.quiver(X, Y, Z, Bx, By, Bz, length=0.1, normalize=True, color='purple')


plt.tight_layout()


# Draw clearly numbered main points with rotated positions
for num, (x, y) in positions_rotated.items():
    ax.plot([x], [y], [0], 'ko', markersize=6)  # 3D point at z=0
    ax.text(x * 1.05, y * 1.05, 0, str(num), fontsize=10, ha='center', va='center')





# Adjustments and display
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
plt.grid(True)


# ✅ Get the script filename dynamically
import os
from datetime import datetime
script_name = os.path.splitext(os.path.basename(__file__))[0]
timestamp = datetime.now().strftime("%H%M%S")
filename = f"{script_name}_{timestamp}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()
