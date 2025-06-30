import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# === Starship Coil Configurations ===
# Format: (number of corners, forward skip, backward skip)
config_index = 0  # 0-6 to pick different patterns
coil_configs = [
    (32, 11, -9),
    (34, 11,  7),
    (30, 11,  3),
    (32, 13,  9),
    (28, 11,  7),
    (28, 11, -9),
    (34, 15, -13),
    (80, 33, -27),
]

# === Pick a Configuration by Index ===
coil_corners, skip_forward, skip_backward = coil_configs[config_index]
skip_backward %= coil_corners  # Ensure positive modulo

num_layers = 5          # Number of layers in Z
layer_spacing = 0.15     # Vertical spacing between layers


# === Function to generate alternating skip sequence ===
def generate_alternating_skip_sequence(corners, step_even, step_odd, radius=1.0, z_layer=0.0):
    """
    Generate a closed-loop alternating skip sequence with:
    - Alternating step_even and step_odd
    - Segment pairs split into even/odd indexed connections
    - Positions corresponding to each node
    """
    sequence = []
    current = 1
    toggle = True  # start with even step
    for _ in range(corners + 1):  # +1 to close loop
        sequence.append(current)
        step = step_even if toggle else step_odd
        current = (current + step - 1) % corners + 1
        toggle = not toggle  # alternate step type

    # Precompute angles and positions
    angles = np.linspace(0, 2 * np.pi, corners, endpoint=False) - np.pi / 2
    positions = [(radius * np.cos(angles[(i - 1) % corners]),
                  radius * np.sin(angles[(i - 1) % corners]),
                  z_layer) for i in sequence]

    # Segment pairs
    even_steps = [(sequence[i], sequence[i+1]) for i in range(0, len(sequence)-1, 2)]
    odd_steps = [(sequence[i], sequence[i+1]) for i in range(1, len(sequence)-1, 2)]

    return {
        "sequence": sequence,
        "even_pairs": even_steps,
        "odd_pairs": odd_steps,
        "positions": positions
    }


# Function to generate wire from selected indexed segments
def generate_3d_wire_filtered(sequence, segment, z_layer, base_color, style, alpha=1.0, filter_type='even'):
    angles = np.linspace(0, 2 * np.pi, coil_corners, endpoint=False) - np.pi / 2
    total_points = len(sequence) - 1

    for i in range(total_points):
        if (filter_type == 'even' and i % 2 != 0) or (filter_type == 'odd' and i % 2 == 0):
            continue  # Skip depending on type

        angle_start = angles[(sequence[i] - 1) % coil_corners]
        angle_end = angles[(sequence[i + 1] - 1) % coil_corners]

        x_start, y_start = np.cos(angle_start), np.sin(angle_start)
        x_end, y_end = np.cos(angle_end), np.sin(angle_end)

        z_start = z_layer + layer_spacing * (i / total_points)
        z_end = z_layer + layer_spacing * ((i + 1) / total_points)

        ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end],
                color=base_color, linestyle=style, linewidth=2, alpha=alpha)



# Use original unified sequence (32-point starship with skip +11)
unified_sequence = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward)
unified_sequence = unified_sequence["sequence"]
unified_sequence = [((num - 1) % coil_corners) + 1 for num in unified_sequence]


# === Generate positions for all layers ===
layers = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward)
sequence = layers["sequence"]
base_positions = layers["positions"]
positions = []
for layer in range(num_layers):
    z_offset = layer * layer_spacing
    for (x, y, z) in base_positions:
        positions.append((x, y, z + z_offset))

# === Generate vector arrows from consecutive points ===
arrows = []
for i in range(len(positions) - 1):
    x0, y0, z0 = positions[i]
    x1, y1, z1 = positions[i + 1]
    dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
    arrows.append(((x0, y0, z0), (dx, dy, dz)))

I = 1     # Current (unit)
dl = 0.05 # Approximate wire segment length
# Create a coarse 3D grid for field vectors
grid_size = 15
x = np.linspace(-1, 1, grid_size)
y = np.linspace(-1, 1, grid_size)
z = np.linspace(0, num_layers * layer_spacing, 15)
X, Y, Z = np.meshgrid(x, y, z)

# Reinitialize magnetic field components
Bx = np.zeros_like(X)
By = np.zeros_like(Y)
Bz = np.zeros_like(Z)

# Recompute magnetic field vectors using Biot–Savart law on coarse grid
for origin, vector in arrows:
    x0, y0, z0 = origin
    dx, dy, dz = vector
    segment = np.array([dx, dy, dz]) * dl
    r0 = np.array([x0, y0, z0])

    for i in range(grid_size):
        for j in range(grid_size):
            for k in range(grid_size):
                r = np.array([X[i, j, k], Y[i, j, k], Z[i, j, k]])
                R = r - r0
                norm_R = np.linalg.norm(R)
                if norm_R < 1e-3:
                    continue  # Avoid singularity

                dB = np.cross(segment, R) / (norm_R**3)
                Bx[i, j, k] += dB[0]
                By[i, j, k] += dB[1]
                Bz[i, j, k] += dB[2]

# Normalize vectors for consistent arrow length
B_magnitude = np.sqrt(Bx**2 + By**2 + Bz**2)
Bx /= B_magnitude + 1e-9
By /= B_magnitude + 1e-9
Bz /= B_magnitude + 1e-9





# Plot even vs odd segments on same path
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

ax.set_facecolor('black')
fig.patch.set_facecolor('black')
ax.quiver(X, Y, Z, Bx, By, Bz, length=0.1, normalize=True, color='cyan')


sequence_data = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward)
sequence = sequence_data["sequence"]
total_segments = len(sequence) - 1
print("total_segments: ", total_segments)
steps_to_plot = int(total_segments * num_layers)
print("steps_to_plot: ", steps_to_plot)

unified_sequence = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward)
unified_sequence = [((num - 1) % coil_corners) + 1 for num in unified_sequence["sequence"]]


for layer in range(num_layers):
    z_layer = layer * layer_spacing
    # Alternate coloring on same path
    generate_3d_wire_filtered(unified_sequence, 1, z_layer, '#ff9900', '-', alpha=1.0, filter_type='even')
    generate_3d_wire_filtered(unified_sequence, 2, z_layer, '#cc0000', '-', alpha=1.0, filter_type='odd')

# Final layout
ax.set_title("Starship Coil (32): Shared Path, Alternating Color (Even/ Odd)", color='white')
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-0.2, num_layers * (layer_spacing + 0.1) + 0.2)
ax.set_axis_off()
ax.view_init(elev=88, azim=45)

plt.tight_layout()
plt.show()




