import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# === Starship Coil Configurations ===
# Format: (number of corners, forward skip, backward skip)
config_index = 1  # 0-6 to pick different patterns
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
    sequence = []
    current = 1
    toggle = True
    for _ in range(corners + 1):
        sequence.append(current)
        step = step_even if toggle else step_odd
        current = (current + step - 1) % corners + 1
        toggle = not toggle

    angles = np.linspace(0, 2 * np.pi, corners, endpoint=False) - np.pi / 2
    positions = [(radius * np.cos(angles[(i - 1) % corners]),
                  radius * np.sin(angles[(i - 1) % corners]),
                  z_layer) for i in sequence]

    return sequence, positions

# === Generate positions for all layers ===
sequence, base_positions = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward)

positions = []
for layer in range(num_layers):
    offset = layer * layer_spacing
    layer_positions = [
        (x, y, z + offset) for (x, y, z) in base_positions
    ]
    if layer > 0:
        # Avoid duplicating first point of each new layer
        positions.extend(layer_positions[1:])
    else:
        positions.extend(layer_positions)

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
grid_size = 5
x = np.linspace(-1.5, 1.5, grid_size)
y = np.linspace(-1.5, 1.5, grid_size)
z = np.linspace(0, num_layers * layer_spacing, grid_size)
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



# === Plotting ===
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

# Draw arrows (Biot–Savart segments)
for origin, vector in arrows:
    ax.quiver(*origin, *vector, length=1.0, normalize=False,
              color='cyan', arrow_length_ratio=0.2, linewidth=0.7)

ax.set_facecolor('black')
fig.patch.set_facecolor('black')
ax.quiver(X, Y, Z, Bx, By, Bz, length=0.1, normalize=True, color='cyan')
ax.set_title("Biot–Savart Source Arrows for Starship Coil (32)", color='white')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-0.2, num_layers * (layer_spacing + 0.1) + 0.2)
ax.set_axis_off()
ax.view_init(elev=85, azim=45)
plt.tight_layout()



plt.show()