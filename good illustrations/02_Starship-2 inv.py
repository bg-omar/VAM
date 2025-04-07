import numpy as np

import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from matplotlib.colors import Normalize

N_frames = 30
I_peak = 1.0
frame_dt = 1 / N_frames

# Define number of turns in the coil and spacing in the Z-direction
num_turns = 10  # Number of full cycles up the coil
z_spacing = 0.1  # Distance between layers in the Z-direction

xlimit = 10
ylimit = 10
zlimit = 10
# Define a 3D grid
grid_size = 20

# Corrected and clear visualization with sequences explicitly plotted and labeled with different colors and tints
coil_corners = 12
coil_amount = 3


total_corners = coil_corners * coil_amount

rotation_steps=0
rotation_angle = (2 * np.pi / 12) / 3
# Define provided base sequence
base_sequence = [1, 6, 11, 4, 9, 2, 7, 12, 5, 10, 3, 8, 1]
base_sequence_inv = [1, 8, 3, 10, 5, 12, 7, 2, 9, 4, 11, 6, 1]

# Create explicit sequences as per user request
sequence_A_forward = [((num * 3 - 0 - 1) % total_corners) + 1 for num in base_sequence]


sequence_B_forward = [((num * 3 - 1 - 1) % total_corners) + 1 for num in base_sequence_inv]



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

def plot_rotated_wire(sequence, segment, base_color, style, label, alpha, z_spacing, z_base, x_offset):
    total_segments = len(sequence) - 1
    for i in range(total_segments):
        num = sequence[i]
        next_num = sequence[i + 1]

        angle_start = angles_rotated[(num - 1 + rotation_steps) % total_corners] + segment_shift * (segment - 1)
        angle_end = angles_rotated[(next_num - 1 + rotation_steps) % total_corners] + segment_shift * (segment - 1)

        x_start, y_start = np.cos(angle_start) + x_offset, np.sin(angle_start)
        x_end, y_end = np.cos(angle_end) + x_offset, np.sin(angle_end)

        z_start = z_base + z_spacing * (i / total_segments)
        z_end = z_base + z_spacing * ((i + 1) / total_segments)

        ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end],
                color=base_color, linestyle=style, linewidth=2, alpha=alpha, label=label if i == 0 else "")



# Plot multiple layers of the coil
for layer in range(num_turns):
    z_layer = -1 + layer * z_spacing

    # Move A coil left, B coil right
    plot_rotated_wire(sequence_A_forward, 1, 'blue', '-', 'Phase A Forward', alpha=0.9, z_spacing=z_spacing, z_base=z_layer, x_offset=-2)
    plot_rotated_wire(sequence_B_forward, 1, 'red', '-', 'Phase B Forward', alpha=0.9, z_spacing=z_spacing, z_base=z_layer, x_offset=+2)




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

def generate_segments(sequence, segment_offset=0, z_spacing=1.0, z_base=0.0, x_offset=0.0):
    segments = []
    total_segments = len(sequence) - 1
    for i in range(total_segments):
        num = sequence[i]
        next_num = sequence[i + 1]

        angle_start = angles_rotated[(num - 1 + rotation_steps) % total_corners] + segment_shift * segment_offset
        angle_end = angles_rotated[(next_num - 1 + rotation_steps) % total_corners] + segment_shift * segment_offset

        x_start, y_start = np.cos(angle_start) + x_offset, np.sin(angle_start)
        x_end, y_end = np.cos(angle_end) + x_offset, np.sin(angle_end)

        z_start = z_base + z_spacing * (i / total_segments)
        z_end = z_base + z_spacing * ((i + 1) / total_segments)

        segments.append(((x_start, y_start, z_start), (x_end, y_end, z_end)))
    return segments


# Gather segments from all layers and all phases
all_segments = []
for layer in range(num_turns):
    z_layer = -1 + layer * z_spacing
    all_segments += generate_segments(sequence_A_forward, segment_offset=0, z_base=z_layer, x_offset=-2)
    all_segments += generate_segments(sequence_B_forward, segment_offset=1, z_base=z_layer, x_offset=+2)


# Observation point — center of the coil
observation_point = (0.0, 0.0, 0.0)
B = biot_savart_field(all_segments, observation_point)
print("Total magnetic field at center (0,0,0):", B, "Tesla")


lin = np.linspace(-xlimit, xlimit, grid_size)
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


Bmag = np.sqrt(Bx**2 + By**2 + Bz**2)
Bx_norm = Bx / (Bmag + 1e-12)  # avoid divide by zero
By_norm = By / (Bmag + 1e-12)
Bz_norm = Bz / (Bmag + 1e-12)





# Draw clearly numbered main points with rotated positions
for num, (x, y) in positions_rotated.items():
    ax.plot([x], [y], [0], 'ko', markersize=6)  # 3D point at z=0
    ax.text(x * 1.05, y * 1.05, 0, str(num), fontsize=10, ha='center', va='center')





# Adjustments and display
ax.set_title("3D Multi-Layer Starship Rodin Coil", fontsize=16)
# Set axis labels
ax.set_xlim(-xlimit, xlimit)
ax.set_ylim(-ylimit, ylimit)
ax.set_zlim(-zlimit, zlimit)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
# Show legend
# ax.legend()
ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio
plt.grid(True)


# ✅ Get the script filename dynamically
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}1.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()


# Vector field visualization in a separate figure
fig_field = plt.figure(figsize=(12, 10))
ax_field = fig_field.add_subplot(111, projection='3d')

# Normalize Bmag for colormap scaling
Bmag_flat = Bmag.flatten()
colors = plt.cm.viridis((Bmag_flat - Bmag_flat.min()) / (Bmag_flat.ptp() + 1e-12))  # Colormap scaled to B magnitude

# Flatten all arrays for quiver input
Xf = X.flatten()
Yf = Y.flatten()
Zf = Z.flatten()
U = Bx_norm.flatten()
V = By_norm.flatten()
W = Bz_norm.flatten()
norm = Normalize(vmin=Bmag.min(), vmax=Bmag.max())
sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
sm.set_array([])  # Required for older Matplotlib versions
cbar = fig_field.colorbar(sm, ax=ax_field, shrink=0.7)
cbar.set_label('Magnetic Field Magnitude (T)', fontsize=12)
# Plot quiver with color mapped to field strength
ax_field.quiver(Xf, Yf, Zf, U, V, W, length=0.3, normalize=True, colors=colors, linewidth=0.5)


ax_field.set_title("Magnetic Field Vector Field (5x5x5) – 3 Phase Coil", fontsize=14)
ax_field.set_xlabel('X')
ax_field.set_ylabel('Y')
ax_field.set_zlabel('Z')
ax_field.set_xlim(-xlimit, xlimit)
ax_field.set_ylim(-ylimit, ylimit)
ax_field.set_zlim(-zlimit, zlimit)
ax_field.set_box_aspect([1, 1, 1])

# ✅ Get the script filename dynamically
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()


import matplotlib.animation as animation

fig_anim = plt.figure(figsize=(10, 8))
ax_anim = fig_anim.add_subplot(111, projection='3d')

# We'll sample just a horizontal slice in Z = 0
slice_z = 0.0
X2D, Y2D = np.meshgrid(np.linspace(-xlimit, xlimit, grid_size), np.linspace(-ylimit, ylimit, grid_size))

Z2D = np.full_like(X2D, slice_z)

quiver = None

def update(frame):
    global quiver
    ax_anim.clear()
    ax_anim.set_title(f"Signal Transmission – Frame {frame+1}", fontsize=14)
    ax_anim.set_xlim(-xlimit, xlimit)
    ax_anim.set_ylim(-ylimit, ylimit)
    ax_anim.set_zlim(-zlimit, zlimit)
    ax_anim.set_xlabel('X')
    ax_anim.set_ylabel('Y')
    ax_anim.set_zlabel('Z')
    ax_anim.set_box_aspect([1,1,0.4])
    slice_z = -1.0 + 2.0 * (frame / N_frames)  # from -1 to +1 smoothly

    # Square wave current for Coil A (on left)
    I_A = I_peak if frame % 10 < 5 else -I_peak

    # Coil B stays passive
    segments_A = []
    segments_B = []
    for layer in range(num_turns):
        z_layer = -1 + layer * z_spacing
        segments_A += generate_segments(sequence_A_forward, segment_offset=0, z_base=z_layer, x_offset=-2)
        segments_B += generate_segments(sequence_B_forward, segment_offset=1, z_base=z_layer, x_offset=+2)

    # Only include Coil A's current
    Bx, By, Bz = np.zeros_like(X2D), np.zeros_like(Y2D), np.zeros_like(Z2D)
    for i in range(X2D.shape[0]):
        for j in range(X2D.shape[1]):
            pt = (X2D[i,j], Y2D[i,j], Z2D[i,j])
            B = biot_savart_field(segments_A, pt, current=I_A)
            Bx[i,j], By[i,j], Bz[i,j] = B

    # Normalize for quiver
    Bmag = np.sqrt(Bx**2 + By**2 + Bz**2)
    Bx_norm = Bx / (Bmag + 1e-12)
    By_norm = By / (Bmag + 1e-12)
    Bz_norm = Bz / (Bmag + 1e-12)

    # Show the field
    scale = 2.0
    quiver = ax_anim.quiver(X2D, Y2D, Z2D, scale * Bx_norm, scale * By_norm, scale * Bz_norm, length=0.3, color='purple', normalize=True)

    # Outline Coil A (left)
    ax_anim.plot([-2]*2, [-3,3], [slice_z]*2, 'blue', linestyle='--', linewidth=1)

    # Outline Coil B (right)
    ax_anim.plot([+2]*2, [-3,3], [slice_z]*2, 'red', linestyle='--', linewidth=1)
    I_A = I_peak if frame % 10 < 5 else -I_peak
    signal_color = 'limegreen' if I_A > 0 else 'orangered'
    ax_anim.text(0, 4.5, 1.5, f"Signal: {'HIGH' if I_A > 0 else 'LOW'}", color=signal_color, fontsize=12)



ani = animation.FuncAnimation(fig_anim, update, frames=N_frames, interval=200)
plt.tight_layout()
plt.show()
