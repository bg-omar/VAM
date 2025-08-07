import numpy as np

import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import matplotlib.animation as animation
import matplotlib.pyplot as plt



from mpl_toolkits.mplot3d import Axes3D
from skimage import measure

from scipy.integrate import solve_ivp


# Configuration from the first preset: (32, 11, -9)
coil_corners = 32
skip_forward = 11
skip_backward = -9
num_layers = 1
layer_spacing = 1
radius = 1.0

# Generate alternating skip sequence for preset
def generate_alternating_skip_sequence(corners, step_even, step_odd, radius=1.0, z_layer=0.0, angle_offset=0.0):
    sequence = []
    current = 1
    toggle = True
    for _ in range(corners + 1):
        sequence.append(current)
        step = step_even if toggle else step_odd
        current = (current + step - 1) % corners + 1
        toggle = not toggle
    angles = np.linspace(0, 2*np.pi, corners, endpoint=False) - np.pi/2
    positions = [
        (radius*np.cos(angles[i % corners] + angle_offset),
         radius*np.sin(angles[i % corners] + angle_offset),
         z_layer)
        for i in sequence
    ]
    return sequence, positions


angles = np.linspace(0, 2*np.pi, coil_corners, endpoint=False) - np.pi/2
seq, positions = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward)


fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Generate sequence and positions
seq, positions = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward)

# Draw full connected coil path
xs, ys, zs = [], [], []
for i in range(len(seq)):
    idx = (seq[i] - 1) % coil_corners
    angle = angles[idx]
    x = np.cos(angle)
    y = np.sin(angle)
    z = i * (layer_spacing / (len(seq)-1))  # Gradual Z offset for spiral visualization
    xs.append(x)
    ys.append(y)
    zs.append(z)

ax.plot(xs, ys, zs, color='purple', lw=2, label="Connected Coil Path")

ax.set_title(f"Unified Rodin Coil Path\nN={coil_corners}, Skip=({skip_forward}, {skip_backward})")
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(0, 1)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()

coil_field_filename = f"Unified Rodin Coil Path N={coil_corners} Skip=({skip_forward} {skip_backward}).png"
plt.tight_layout()
plt.savefig(coil_field_filename, dpi=150)
# plt.show()


# Generate 3-phase coils with 120° offset
colors = ['purple', 'blue', 'green']
phase_offsets = [0, 2*np.pi/3, 4*np.pi/3]

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for idx, offset in enumerate(phase_offsets):
    seq, _ = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward, angle_offset=offset)

    xs, ys, zs = [], [], []
    for i in range(len(seq)):
        angle_idx = (seq[i] - 1) % coil_corners
        angle = angles[angle_idx] + offset
        x = np.cos(angle)
        y = np.sin(angle)
        z = i * (layer_spacing / (len(seq)-1))
        xs.append(x)
        ys.append(y)
        zs.append(z)

    ax.plot(xs, ys, zs, color=colors[idx], lw=2, label=f"Phase {idx + 1}")

ax.set_title(f"3-Phase Rodin Coil\nN={coil_corners}, Skip=({skip_forward}, {skip_backward})")
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(0, 1)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()
coil_field_filename = f"3-Phase Rodin Coil N={coil_corners} Skip=({skip_forward} {skip_backward}).png"
plt.tight_layout()
plt.savefig(coil_field_filename, dpi=150)
# plt.show()

layer_spacing = 0.15

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Biot-Savart law function
def biot_savart_field(arrows, grid_dims, x_range, y_range, z_range, current_amplitudes):
    μ0 = 4 * np.pi * 1e-7  # vacuum permeability
    dl = 0.05

    x = np.linspace(*x_range, grid_dims[0])
    y = np.linspace(*y_range, grid_dims[1])
    z = np.linspace(*z_range, grid_dims[2])
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    Bx, By, Bz = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)

    for phase_arrows, I in zip(arrows, current_amplitudes):
        for origin, vector in phase_arrows:
            x0, y0, z0 = origin
            dx, dy, dz = np.array(vector) * dl
            r0 = np.array([x0, y0, z0])

            RX = X - r0[0]
            RY = Y - r0[1]
            RZ = Z - r0[2]
            norm_R = np.sqrt(RX**2 + RY**2 + RZ**2) + 1e-8

            cross_x = dy*RZ - dz*RY
            cross_y = dz*RX - dx*RZ
            cross_z = dx*RY - dy*RX
            factor = μ0 * I / (4 * np.pi * norm_R**3)

            Bx += cross_x * factor
            By += cross_y * factor
            Bz += cross_z * factor

    B_mag = np.sqrt(Bx**2 + By**2 + Bz**2) + 1e-9
    return X, Y, Z, Bx / B_mag, By / B_mag, Bz / B_mag, B_mag

# Function to generate 3-phase arrows
def get_3phase_arrows():
    arrows_per_phase = []
    for offset in phase_offsets:
        seq, positions = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward, angle_offset=offset)
        arrow_list = []
        for i in range(len(seq)-1):
            idx1 = (seq[i] - 1) % coil_corners
            idx2 = (seq[i+1] - 1) % coil_corners
            angle1 = angles[idx1] + offset
            angle2 = angles[idx2] + offset
            x1, y1 = np.cos(angle1), np.sin(angle1)
            x2, y2 = np.cos(angle2), np.sin(angle2)
            z1 = i * (layer_spacing / (len(seq)-1))
            z2 = (i+1) * (layer_spacing / (len(seq)-1))
            p0 = (x1, y1, z1)
            p1 = (x2, y2, z2)
            v = np.subtract(p1, p0)
            arrow_list.append((p0, v))
        arrows_per_phase.append(arrow_list)
    return arrows_per_phase

# Prepare field visualization
grid_dims = (11, 11, 11)
x_range, y_range, z_range = (-1.0, 1.0), (-1.0, 1.0), (0.0, 1.0)
current_amplitudes = [1.0, -0.5, -0.5]  # balanced 3-phase for AC-like field pattern

arrows_3phase = get_3phase_arrows()
X, Y, Z, Bx, By, Bz, B_mag = biot_savart_field(arrows_3phase, grid_dims, x_range, y_range, z_range, current_amplitudes)

# Plot a slice of the field in the XY plane at mid Z
mid_z = grid_dims[2] // 2
plt.figure(figsize=(8, 6))
plt.quiver(X[:, :, mid_z], Y[:, :, mid_z], Bx[:, :, mid_z], By[:, :, mid_z], B_mag[:, :, mid_z], cmap='viridis')
plt.title("Biot–Savart Field (XY midplane slice) for 3-Phase Coil")
plt.xlabel("X")
plt.ylabel("Y")
plt.axis('equal')
plt.colorbar(label="|B|")
coil_field_filename = f"Biot–Savart Field (XY midplane slice) for 3-Phase Coil.png"
plt.tight_layout()
plt.savefig(coil_field_filename, dpi=150)
# plt.show()



# 3D Quiver plot of the Biot–Savart field
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

density = 2  # reduce density for clarity
Xf, Yf, Zf = X[::density,::density,::density], Y[::density,::density,::density], Z[::density,::density,::density]
Bxf, Byf, Bzf = Bx[::density,::density,::density], By[::density,::density,::density], Bz[::density,::density,::density]
Bmagf = B_mag[::density,::density,::density]

# Flatten for plotting
Xf, Yf, Zf = Xf.flatten(), Yf.flatten(), Zf.flatten()
Bxf, Byf, Bzf = Bxf.flatten(), Byf.flatten(), Bzf.flatten()
Bmagf = Bmagf.flatten()

# Normalize color
colors = plt.cm.plasma((Bmagf - Bmagf.min()) / (Bmagf.max() - Bmagf.min()))

# Plot arrows
for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors):
    ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.08, color=ci, normalize=True, linewidth=0.5, arrow_length_ratio=0.3)

ax.set_title("3D Biot–Savart Field of 3-Phase Double Star Coil")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
coil_field_filename = f"3D Biot–Savart Field of 3-Phase Double Star Coil.png"
plt.tight_layout()
plt.savefig(coil_field_filename, dpi=150)
plt.show()


import matplotlib.animation as animation

# Prepare figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Time-Varying Biot–Savart Field (3-Phase Rodin Coil)")

# Subsample grid
density = 2
Xf, Yf, Zf = X[::density,::density,::density], Y[::density,::density,::density], Z[::density,::density,::density]
Xf, Yf, Zf = Xf.flatten(), Yf.flatten(), Zf.flatten()

# Store Biot–Savart arrows for each phase
arrows_3phase = get_3phase_arrows()

# Initialize quiver object
quivers = []

def update_quiver(t):
    global quivers
    for q in quivers:
        q.remove()
    quivers.clear()

    # Oscillating current amplitudes (3-phase sinusoidal AC)
    I1 = np.sin(t)
    I2 = np.sin(t - 2*np.pi/3)
    I3 = np.sin(t - 4*np.pi/3)
    currents = [I1, I2, I3]

    _, _, _, Bx, By, Bz, Bmag = biot_savart_field(arrows_3phase, grid_dims, x_range, y_range, z_range, currents)
    Bxf, Byf, Bzf = Bx[::density,::density,::density], By[::density,::density,::density], Bz[::density,::density,::density]
    Bxf, Byf, Bzf = Bxf.flatten(), Byf.flatten(), Bzf.flatten()

    Bmagf = np.sqrt(Bxf**2 + Byf**2 + Bzf**2)
    colors = plt.cm.plasma((Bmagf - Bmagf.min()) / (Bmagf.max() - Bmagf.min()))

    for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors):
        q = ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.08, color=ci, normalize=True,
                      linewidth=0.5, arrow_length_ratio=0.3)
        quivers.append(q)

    ax.set_title(f"3-Phase Field at Time t = {t:.2f} (AC Cycle)")

ani = animation.FuncAnimation(fig, update_quiver, frames=np.linspace(0, 2*np.pi, 40), interval=150, blit=False)
# plt.show()


# Export the animation as a GIF
gif_filename = "3phase_field_AC_cycle.gif"
ani.save(gif_filename, writer='pillow', fps=10)



from scipy.integrate import solve_ivp

# Compute streamlines (field lines) by integrating the normalized B-field
def compute_streamline(seed_point, Bx, By, Bz, X, Y, Z, step=0.01, length=1.5):
    def field_line(t, r):
        xi = np.argmin(np.abs(X[:,0,0] - r[0]))
        yi = np.argmin(np.abs(Y[0,:,0] - r[1]))
        zi = np.argmin(np.abs(Z[0,0,:] - r[2]))
        if 0 <= xi < Bx.shape[0] and 0 <= yi < By.shape[1] and 0 <= zi < Bz.shape[2]:
            return [Bx[xi, yi, zi], By[xi, yi, zi], Bz[xi, yi, zi]]
        else:
            return [0, 0, 0]

    sol = solve_ivp(field_line, [0, length], seed_point, max_step=step, rtol=1e-5)
    return sol.y

# Use peak current values for static snapshot
currents = [1.0, -0.5, -0.5]
_, _, _, Bx, By, Bz, Bmag = biot_savart_field(arrows_3phase, grid_dims, x_range, y_range, z_range, currents)

# Seed points for field lines
seed_points = [
    [-0.6, 0.0, 0.5],
    [0.0, 0.6, 0.5],
    [0.6, 0.0, 0.5],
    [0.0, -0.6, 0.5],
    [-0.6, -0.6, 0.5],
    [0.6, 0.6, 0.5],
]

# Plot 3D field lines
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for pt in seed_points:
    line = compute_streamline(pt, Bx, By, Bz, X, Y, Z)
    ax.plot(line[0], line[1], line[2], lw=2)

ax.set_title("Magnetic Field Lines from 3-Phase Rodin Coil")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
plt.tight_layout()

# Save as PNG
fieldline_filename = "3phase_field_lines.png"
plt.savefig(fieldline_filename, dpi=150)
# plt.show()

# Compute æther pressure from magnetic field (Bernoulli-like analogy in VAM)
# Use: P = P0 - (1/2) * rho_fluid * |B|^2 / mu0
rho_ae_fluid = 7.0e-7  # kg/m³ (VAM-defined fluid vacuum density)
μ0 = 4 * np.pi * 1e-7  # vacuum permeability

# Bernoulli-like pressure field
pressure = -0.5 * rho_ae_fluid * (B_mag**2) / μ0
pressure -= pressure.min()  # normalize: zero = min pressure
pressure /= pressure.max()  # now in range [0, 1]

# Midplane slice for visualization
mid_z = grid_dims[2] // 2
pressure_slice = pressure[:, :, mid_z]

plt.figure(figsize=(8, 6))
plt.contourf(X[:, :, mid_z], Y[:, :, mid_z], pressure_slice, levels=30, cmap='inferno')
plt.colorbar(label="Normalized Æther Pressure Drop (Bernoulli-like)")
plt.title("Midplane Æther Pressure Drop\nInduced by 3-Phase VAM Swirl")
plt.xlabel("X")
plt.ylabel("Y")
plt.axis('equal')
plt.tight_layout()

# Save pressure plot
pressure_filename = "3phase_pressure_drop.png"
plt.savefig(pressure_filename, dpi=150)
# plt.show()

# Apply log scaling to pressure field (add small epsilon to avoid log(0))
pressure_log = np.log10(pressure + 1e-10)

# Plot log-scaled midplane slice
plt.figure(figsize=(8, 6))
plt.contourf(X[:, :, mid_z], Y[:, :, mid_z], pressure_log[:, :, mid_z], levels=30, cmap='magma')
plt.colorbar(label="Log₁₀ Æther Pressure Drop (Normalized)")
plt.title("Midplane Æther Pressure Drop (Log Scale)\nInduced by 3-Phase Swirl Coil")
plt.xlabel("X")
plt.ylabel("Y")
plt.axis('equal')
plt.tight_layout()

log_pressure_filename = "3phase_Æther LogScale Pressure Drop Induced by 3-Phase VAM Swirl.png"
plt.savefig(log_pressure_filename, dpi=150)
# plt.show()



# Redefine parameters explicitly since previous context was lost
coil_corners = 32
skip_forward = 11
skip_backward = -9
layer_spacing = 0.15
num_layers = 10

params = {
    "coil_corners": coil_corners,
    "skip_forward": skip_forward,
    "skip_backward": skip_backward,
    "num_layers": num_layers,
    "layer_spacing": layer_spacing,
}

grid_dims = (11, 11, 11)
x_range, y_range, z_range = (-1.0, 1.0), (-1.0, 1.0), (0.0, 1.0)
rho_ae_fluid = 7.0e-7
μ0 = 4 * np.pi * 1e-7
current_amplitudes = [1.0, -0.5, -0.5]
angles = np.linspace(0, 2 * np.pi, coil_corners, endpoint=False) - np.pi / 2
phase_offsets = [0, 2*np.pi/3, 4*np.pi/3]

# Rebuild 3-phase arrows with 10 layers
def get_3phase_arrows_with_layers():
    arrows_per_phase = []
    for offset in phase_offsets:
        seq, positions = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward, angle_offset=offset)
        arrow_list = []
        for L in range(num_layers):
            z_offset = L * layer_spacing
            for i in range(len(seq)-1):
                idx1 = (seq[i] - 1) % coil_corners
                idx2 = (seq[i+1] - 1) % coil_corners
                angle1 = angles[idx1] + offset
                angle2 = angles[idx2] + offset
                x1, y1 = np.cos(angle1), np.sin(angle1)
                x2, y2 = np.cos(angle2), np.sin(angle2)
                z1 = z_offset + i * (layer_spacing / len(seq))
                z2 = z_offset + (i+1) * (layer_spacing / len(seq))
                p0 = (x1, y1, z1)
                p1 = (x2, y2, z2)
                v = np.subtract(p1, p0)
                arrow_list.append((p0, v))
        arrows_per_phase.append(arrow_list)
    return arrows_per_phase

# Compute everything
arrows_3phase = get_3phase_arrows_with_layers()
X, Y, Z, Bx, By, Bz, B_mag = biot_savart_field(arrows_3phase, grid_dims, x_range, y_range, z_range, current_amplitudes)
pressure = -0.5 * rho_ae_fluid * (B_mag**2) / μ0
pressure -= pressure.min()
pressure /= pressure.max()

from skimage import measure
# Isosurface
iso_threshold_raw = np.percentile(pressure, 70)
verts, faces, _, _ = measure.marching_cubes(pressure, iso_threshold_raw)

scale_x = (x_range[1] - x_range[0]) / (grid_dims[0] - 1)
scale_y = (y_range[1] - y_range[0]) / (grid_dims[1] - 1)
scale_z = (z_range[1] - z_range[0]) / (grid_dims[2] - 1)
verts[:, 0] = verts[:, 0] * scale_x + x_range[0]
verts[:, 1] = verts[:, 1] * scale_y + y_range[0]
verts[:, 2] = verts[:, 2] * scale_z + z_range[0]

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
mesh = ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2],
                       cmap='inferno', lw=0.3, alpha=0.85)

ax.set_title("3D Æther Pressure Drop Isosurface\n10-Layer 3-Phase Coil (70th percentile)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
fig.colorbar(mesh, ax=ax, shrink=0.6, label="Z (Pressure Drop Depth)")

iso_layers10_filename = "3phase_pressure_isosurface_layers10.png"
plt.tight_layout()
plt.savefig(iso_layers10_filename, dpi=150)
plt.show()

# Parameters for 1-phase coil
coil_corners = 32
skip_forward = 11
skip_backward = -9
layer_spacing = 0.15
num_layers = 10
angle_offset = 0  # Phase A
coil_height = num_layers * layer_spacing
x_range, y_range, z_range = (-1.0, 1.0), (-1.0, 1.0), (-1.0, 1.0)
# Generate 1-phase coil segment
angles = np.linspace(0, 2 * np.pi, coil_corners, endpoint=False) - np.pi / 2
seq, _ = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward, angle_offset=angle_offset)

positions = []
for L in range(num_layers):
    z_offset = L * layer_spacing
    for i in range(len(seq)):
        angle = angles[(seq[i]-1) % coil_corners] + angle_offset
        x = np.cos(angle)
        y = np.sin(angle)
        z = z_offset + i * (layer_spacing / len(seq)) - coil_height * 0.5  # Center around z=0
        positions.append((x, y, z))


# Redefine missing helper: get_wire_arrows
def get_wire_arrows(positions):
    arrows = []
    for i in range(len(positions) - 1):
        p0 = np.array(positions[i])
        p1 = np.array(positions[i + 1])
        v = p1 - p0
        arrows.append((tuple(p0), tuple(v)))
    return arrows

# Now retry generating arrows and plotting
arrows_1phase = get_wire_arrows(positions)

# Compute Biot–Savart field for this 1-phase coil
X, Y, Z, Bx, By, Bz, Bmag = biot_savart_field([arrows_1phase], grid_dims, x_range, y_range, z_range, [1.0])
density = 2

# Downsample for plotting
Xf = X[::density, ::density, ::density].flatten()
Yf = Y[::density, ::density, ::density].flatten()
Zf = Z[::density, ::density, ::density].flatten()
Bxf = Bx[::density, ::density, ::density].flatten()
Byf = By[::density, ::density, ::density].flatten()
Bzf = Bz[::density, ::density, ::density].flatten()
Bmagf = Bmag[::density, ::density, ::density].flatten()
colors = plt.cm.viridis((Bmagf - Bmagf.min()) / (Bmagf.max() - Bmagf.min()))

# Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot magnetic field vectors
for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors):
    ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.08, color=ci, normalize=True,
              linewidth=0.5, arrow_length_ratio=0.3)

# Plot coil geometry
coil_xs, coil_ys, coil_zs = zip(*positions)
ax.plot(coil_xs, coil_ys, coil_zs, color='red', linewidth=2, label="Phase A Coil")

ax.set_title("1-Phase Coil + Biot–Savart Field (3D View)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
ax.legend()

coil_field_filename = "1phase_coil_biot_savart.png"
plt.tight_layout()
plt.savefig(coil_field_filename, dpi=150)
# plt.show()


# Update spacing and recompute everything
layer_spacing = 0.05
params["layer_spacing"] = layer_spacing

# Regenerate coil positions for tighter spacing
positions = []
for L in range(num_layers):
    z_offset = L * layer_spacing
    for i in range(len(seq)):
        angle = angles[(seq[i]-1) % coil_corners] + angle_offset
        x = np.cos(angle)
        y = np.sin(angle)
        z = z_offset + i * (layer_spacing / len(seq))  - (num_layers * layer_spacing * 0.5)  # Center around z=0
        positions.append((x, y, z))

# Get new arrows and compute updated field
arrows_1phase = get_wire_arrows(positions)
X, Y, Z, Bx, By, Bz, Bmag = biot_savart_field([arrows_1phase], grid_dims, x_range, y_range, z_range, [1.0])

# Increase quiver density
density = 1  # denser field
Xf = X[::density, ::density, ::density].flatten()
Yf = Y[::density, ::density, ::density].flatten()
Zf = Z[::density, ::density, ::density].flatten()
Bxf = Bx[::density, ::density, ::density].flatten()
Byf = By[::density, ::density, ::density].flatten()
Bzf = Bz[::density, ::density, ::density].flatten()
Bmagf = Bmag[::density, ::density, ::density].flatten()
colors = plt.cm.viridis((Bmagf - Bmagf.min()) / (Bmagf.max() - Bmagf.min()))

# Plot updated field with coil
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors):
    ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.06, color=ci, normalize=True,
              linewidth=0.4, arrow_length_ratio=0.3)

coil_xs, coil_ys, coil_zs = zip(*positions)
ax.plot(coil_xs, coil_ys, coil_zs, color='red', linewidth=2, label="Phase A Coil")

ax.set_title("1-Phase Coil + Biot–Savart Field (Tighter Spacing, Denser Field)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
ax.legend()

coil_dense_filename = "1phase_coil_biot_savart_dense.png"
plt.tight_layout()
plt.savefig(coil_dense_filename, dpi=150)
# plt.show()


from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Normalize direction using Z component of the field
norm_z = Normalize(vmin=Bzf.min(), vmax=Bzf.max())
colormap = plt.cm.seismic
colors_dir = colormap(norm_z(Bzf))

# Normalize magnitude for alpha blending (opacity)
alpha_norm = (Bmagf - Bmagf.min()) / (Bmagf.max() - Bmagf.min())
colors_rgba = np.zeros((len(Bxf), 4))
colors_rgba[:, :3] = colors_dir[:, :3]  # RGB from direction
colors_rgba[:, 3] = alpha_norm          # Alpha from strength

# Plot with direction-based color and magnitude-based opacity
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors_rgba):
    ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.06, color=ci, normalize=True,
              linewidth=0.4, arrow_length_ratio=0.3)

# Plot coil path again
ax.plot(coil_xs, coil_ys, coil_zs, color='red', linewidth=2, label="Phase A Coil")

ax.set_title("1-Phase Coil + Direction-Colored, Strength-Faded Field")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
ax.legend()

colored_field_filename = "1phase_coil_biot_savart_colordir_alpha.png"
plt.tight_layout()
plt.savefig(colored_field_filename, dpi=150)
# plt.show()




# Apply gamma correction and floor to alpha values
gamma = 0.6
alpha_corrected = np.clip((alpha_norm ** gamma), 0.2, 1.0)

# Rebuild RGBA array
colors_rgba_corrected = np.zeros((len(Bxf), 4))
colors_rgba_corrected[:, :3] = colors_dir[:, :3]  # RGB from direction
colors_rgba_corrected[:, 3] = alpha_corrected     # Corrected alpha

# Plot with improved visibility
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors_rgba_corrected):
    ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.06, color=ci, normalize=True,
              linewidth=0.4, arrow_length_ratio=0.3)

# Plot coil again
ax.plot(coil_xs, coil_ys, coil_zs, color='red', linewidth=2, label="Phase A Coil")

ax.set_title("1-Phase Coil + Direction-Colored, Strength-Faded Field (Corrected Alpha)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
ax.legend()

corrected_alpha_filename = "1phase_coil_biot_savart_colordir_alpha_corrected.png"
plt.tight_layout()
plt.savefig(corrected_alpha_filename, dpi=150)
# plt.show()



# Apply updated opacity mapping:
# - Minimum alpha = 0.15 (weaker vectors)
# - Maximum alpha = 0.85 (strongest)
# - Gamma correction to shape the contrast curve

alpha_min = 0.15
alpha_max = 0.85
gamma = 0.6

# Recompute alpha with gamma and range scaling
alpha_scaled = alpha_min + (alpha_max - alpha_min) * (alpha_norm ** gamma)

# Rebuild RGBA array
colors_rgba_scaled = np.zeros((len(Bxf), 4))
colors_rgba_scaled[:, :3] = colors_dir[:, :3]  # RGB from direction
colors_rgba_scaled[:, 3] = alpha_scaled        # New alpha range

# Plot again
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors_rgba_scaled):
    ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.06, color=ci, normalize=True,
              linewidth=0.4, arrow_length_ratio=0.3)

# Replot coil
ax.plot(coil_xs, coil_ys, coil_zs, color='red', linewidth=2, label="Phase A Coil")

ax.set_title("1-Phase Coil + Field Colored by Direction, Opacity by Strength (Improved Contrast)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
ax.legend()

final_quiver_filename = "1phase_coil_biot_savart_colordir_alpha_final.png"
plt.tight_layout()
plt.savefig(final_quiver_filename, dpi=150)
plt.show()

# Apply linear alpha scaling without gamma, with min = 0.5 and max = 1.0
alpha_min = 0.5
alpha_max = 1.0

alpha_linear = alpha_min + (alpha_max - alpha_min) * alpha_norm

# Rebuild RGBA array
colors_rgba_linear = np.zeros((len(Bxf), 4))
colors_rgba_linear[:, :3] = colors_dir[:, :3]  # RGB from direction
colors_rgba_linear[:, 3] = alpha_linear        # Linear alpha

# Plot quiver with updated alpha range
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors_rgba_linear):
    ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.06, color=ci, normalize=True,
              linewidth=0.4, arrow_length_ratio=0.3)

# Coil overlay
ax.plot(coil_xs, coil_ys, coil_zs, color='red', linewidth=2, label="Phase A Coil")

ax.set_title("1-Phase Coil + Field Colored by Direction, Opacity 50–100% (Linear)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
ax.legend()

linear_quiver_filename = "1phase_coil_biot_savart_colordir_alpha_linear.png"
plt.tight_layout()
plt.savefig(linear_quiver_filename, dpi=150)
# plt.show()



# Plot only the quiver field, no coil path
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors_rgba_linear):
    ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.06, color=ci, normalize=True,
              linewidth=0.4, arrow_length_ratio=0.3)

ax.set_title("1-Phase Biot–Savart Field Only (No Coil)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)

field_only_filename = "1phase_biot_savart_quiver_only.png"
plt.tight_layout()
plt.savefig(field_only_filename, dpi=150)
# plt.show()



# Compute CW/CCW rotation in the XY plane via azimuthal vorticity component
# Use cross product of position vector and field to infer handedness
position_vectors = np.stack([Xf, Yf, np.zeros_like(Zf)], axis=1)
field_vectors_xy = np.stack([Bxf, Byf, np.zeros_like(Bzf)], axis=1)
cross_product_z = np.cross(position_vectors, field_vectors_xy)[:, 2]  # z-component of cross product

# Normalize to -1 (CW) ... 0 ... +1 (CCW)
cw_ccw_scalar = cross_product_z / (np.linalg.norm(position_vectors[:, :2], axis=1) *
                                   np.linalg.norm(field_vectors_xy[:, :2], axis=1) + 1e-8)
cw_ccw_scalar = np.clip(cw_ccw_scalar, -1.0, 1.0)  # safety clip

# Map CW/CCW to red-blue (horizontal rotation)
rb_color = plt.cm.seismic((cw_ccw_scalar + 1) / 2)[:, :3]

# For Z component: use gray scale opacity
vz_strength = np.abs(Bzf)
vz_norm = (vz_strength - vz_strength.min()) / (vz_strength.max() - vz_strength.min())
alpha_z = 0.1 + 0.9 * vz_norm  # Pure vertical = full opacity, weak = transparent

# Compose final RGBA: red/blue hue, alpha from verticality
colors_custom = np.zeros((len(Bxf), 4))
colors_custom[:, :3] = rb_color
colors_custom[:, 3] = alpha_z

# Plot field only with new color/opacity mapping
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors_custom):
    ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.06, color=ci, normalize=True,
              linewidth=0.4, arrow_length_ratio=0.3)

ax.set_title("Field Colored by CW/CCW (XY), Opacity by Z-Axis Strength")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)

cwccw_filename = "1phase_biot_savart_quiver_cwccw_xy_opacity_z.png"
plt.tight_layout()
plt.savefig(cwccw_filename, dpi=150)
# plt.show()

# Redefine views with corrected orientations:
# - Top View: Z looking down → elev=90, azim=-90
# - Bottom View: Z looking up → elev=-90, azim=-90
# - Side View: Y-Z plane → elev=0, azim=0
# - Isometric: typical 3D
corrected_views = [
    ("Top View", dict(elev=90, azim=-90)),        # Looking down +Z
    ("Bottom View", dict(elev=-90, azim=-90)),    # Looking up -Z
    ("Side View (Y-Z)", dict(elev=0, azim=0)),    # Looking along +X
    ("Isometric View", dict(elev=45, azim=45))    # Standard 3D
]

fig = plt.figure(figsize=(14, 12))

for i, (title, view) in enumerate(corrected_views, 1):
    ax = fig.add_subplot(2, 2, i, projection='3d')
    for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors_custom):
        ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.06, color=ci, normalize=True,
                  linewidth=0.4, arrow_length_ratio=0.3)
    ax.view_init(**view)
    ax.set_title(title)
    ax.set_xlim(*x_range)
    ax.set_ylim(*y_range)
    ax.set_zlim(*z_range)
    ax.set_axis_off()

fig.suptitle("1-Phase Biot–Savart Field\nCW/CCW Hue (XY) + Z Opacity\nTop | Bottom | Side | Isometric", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])

corrected_multiview_filename = "1phase_biot_savart_multiview_corrected.png"
plt.savefig(corrected_multiview_filename, dpi=150)
# plt.show()

print(corrected_multiview_filename)



# Center the Z-position of the coil in the vertical domain for side view alignment
# First compute current Z extent of the coil
z_positions = np.array([pos[2] for pos in positions])
z_min_coil = z_positions.min()
z_max_coil = z_positions.max()
z_mid_coil = 0.5 * (z_min_coil + z_max_coil)
z_center_target = 0.5 * (z_range[0] + z_range[1])  # desired center in full view
z_shift = z_center_target - z_mid_coil

# Apply Z shift to coil positions and field positions
positions_centered = [(x, y, z + z_shift) for (x, y, z) in positions]
Xf_c = Xf
Yf_c = Yf
Zf_c = Zf + z_shift  # shift field Z coordinates

# Also shift arrows
coil_xs_c, coil_ys_c, coil_zs_c = zip(*positions_centered)

# Plot centered multiview
fig = plt.figure(figsize=(14, 12))
for i, (title, view) in enumerate(corrected_views, 1):
    ax = fig.add_subplot(2, 2, i, projection='3d')
    for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf_c, Yf_c, Zf_c, Bxf, Byf, Bzf, colors_custom):
        ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.06, color=ci, normalize=True,
                  linewidth=0.4, arrow_length_ratio=0.3)
    ax.view_init(**view)
    ax.set_title(title)
    ax.set_xlim(*x_range)
    ax.set_ylim(*y_range)
    ax.set_zlim(*z_range)
    ax.set_axis_off()

fig.suptitle("Centered Coil | Biot–Savart Field\nCW/CCW Hue (XY) + Z Opacity\nTop | Bottom | Side | Isometric", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])

centered_multiview_filename = "1phase_biot_savart_multiview_centered.png"
plt.savefig(centered_multiview_filename, dpi=150)
plt.show()

# Apply a fixed vertical shift of +0.25 to all Z coordinates to place coil from z = 0.25 to 0.75
z_shift_fixed = 0.25

# Shift coil positions
positions_shifted = [(x, y, z + z_shift_fixed) for (x, y, z) in positions]
coil_xs_s, coil_ys_s, coil_zs_s = zip(*positions_shifted)

# Shift field positions
Zf_s = Zf + z_shift_fixed

# Plot shifted multiview layout
fig = plt.figure(figsize=(14, 12))
for i, (title, view) in enumerate(corrected_views, 1):
    ax = fig.add_subplot(2, 2, i, projection='3d')
    for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf, Yf, Zf_s, Bxf, Byf, Bzf, colors_custom):
        ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.06, color=ci, normalize=True,
                  linewidth=0.4, arrow_length_ratio=0.3)
    ax.view_init(**view)
    ax.set_title(title)
    ax.set_xlim(*x_range)
    ax.set_ylim(*y_range)
    ax.set_zlim(*z_range)
    ax.set_axis_off()

fig.suptitle("Biot–Savart Field\nCW/CCW Hue (XY) + Z Opacity\nTop | Bottom | Side | Isometric", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])

raised_multiview_filename = "1phase_biot_savart_multiview_centered_fixedshift.png"
plt.savefig(raised_multiview_filename, dpi=150)
# plt.show()

# Re-declare missing parameters using last known configuration
coil_corners = 32
skip_fwd = 11
skip_bwd = -9
num_layers = 10
layer_spacing = 0.05

# Redefine the function with confirmed dictionary output
def generate_alternating_skip_sequence(corners, step_even, step_odd, radius=1.0, z_layer=0.0, angle_offset=0.0):
    sequence = []
    current = 1
    toggle = True
    for _ in range(corners + 1):
        sequence.append(current)
        step = step_even if toggle else step_odd
        current = (current + step - 1) % corners + 1
        toggle = not toggle
    angles = np.linspace(0, 2*np.pi, corners, endpoint=False) - np.pi/2
    positions = [
        (radius*np.cos(angles[i % corners] + angle_offset),
         radius*np.sin(angles[i % corners] + angle_offset),
         z_layer)
        for i in sequence
    ]
    return {"sequence": sequence, "positions": positions}

# Define the two additional phase angle offsets (120° and 240°)
phase_angles = [0, 2*np.pi/3, 4*np.pi/3]
phase_colors = ['red', 'green', 'blue']

# Retry the 3-phase plot now that the function is corrected
phase_arrows = []
for angle in phase_angles:
    seq_data = generate_alternating_skip_sequence(coil_corners, skip_fwd, skip_bwd,
                                                  radius=1.0, z_layer=0.0, angle_offset=angle)
    pos = seq_data["positions"]
    phase_positions = []
    for L in range(num_layers):
        z_offset = L * layer_spacing
        phase_positions += [(x, y, z + z_offset + z_shift_fixed) for (x, y, z) in pos]
    arrows = get_wire_arrows(phase_positions)
    phase_arrows.append(arrows)

# Flatten all 3 phase arrows into one list for combined field
all_phase_arrows = sum(phase_arrows, [])

# Redefine compute_field_vectors function
def compute_field_vectors(arrows, grid_dims, x_range, y_range, z_range):
    dl = 0.05
    x = np.linspace(*x_range, grid_dims[0])
    y = np.linspace(*y_range, grid_dims[1])
    z = np.linspace(*z_range, grid_dims[2])
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    Bx = np.zeros_like(X)
    By = np.zeros_like(Y)
    Bz = np.zeros_like(Z)

    for origin, vector in arrows:
        x0, y0, z0 = origin
        dx, dy, dz = vector
        dl_vec = np.array([dx, dy, dz]) * dl
        r0 = np.array([x0, y0, z0])

        RX = X - r0[0]
        RY = Y - r0[1]
        RZ = Z - r0[2]
        norm_R = np.sqrt(RX**2 + RY**2 + RZ**2) + 1e-8

        cross_x = dl_vec[1]*RZ - dl_vec[2]*RY
        cross_y = dl_vec[2]*RX - dl_vec[0]*RZ
        cross_z = dl_vec[0]*RY - dl_vec[1]*RX
        factor = 1 / (norm_R**3)

        Bx += cross_x * factor
        By += cross_y * factor
        Bz += cross_z * factor

    return X, Y, Z, Bx, By, Bz

# Now retry the full 3-phase field visualization
X3, Y3, Z3, Bx3, By3, Bz3 = compute_field_vectors(
    arrows=all_phase_arrows,
    grid_dims=grid_dims,
    x_range=x_range,
    y_range=y_range,
    z_range=z_range
)

# Compute B magnitude
Bmag3 = np.sqrt(Bx3**2 + By3**2 + Bz3**2)

# Flatten fields
Xf3 = X3.flatten()
Yf3 = Y3.flatten()
Zf3 = Z3.flatten()
Bxf3 = Bx3.flatten()
Byf3 = By3.flatten()
Bzf3 = Bz3.flatten()
Bmagf3 = Bmag3.flatten()

# CW/CCW and vertical direction coloring
position_vectors_3 = np.stack([Xf3, Yf3, np.zeros_like(Zf3)], axis=1)
field_vectors_xy_3 = np.stack([Bxf3, Byf3, np.zeros_like(Bzf3)], axis=1)
cross_z_3 = np.cross(position_vectors_3, field_vectors_xy_3)[:, 2]
cw_ccw_scalar_3 = cross_z_3 / (np.linalg.norm(position_vectors_3[:, :2], axis=1) *
                               np.linalg.norm(field_vectors_xy_3[:, :2], axis=1) + 1e-8)
cw_ccw_scalar_3 = np.clip(cw_ccw_scalar_3, -1.0, 1.0)
rb_color_3 = plt.cm.seismic((cw_ccw_scalar_3 + 1) / 2)[:, :3]

vz_strength_3 = np.abs(Bzf3)
vz_norm_3 = (vz_strength_3 - vz_strength_3.min()) / (vz_strength_3.max() - vz_strength_3.min())
alpha_3 = 0.5 + 0.5 * vz_norm_3

colors_3phase = np.zeros((len(Bxf3), 4))
colors_3phase[:, :3] = rb_color_3
colors_3phase[:, 3] = alpha_3

# Final plot
fig = plt.figure(figsize=(14, 12))
for i, (title, view) in enumerate(corrected_views, 1):
    ax = fig.add_subplot(2, 2, i, projection='3d')
    for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xf3, Yf3, Zf3, Bxf3, Byf3, Bzf3, colors_3phase):
        ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.06, color=ci, normalize=True,
                  linewidth=0.4, arrow_length_ratio=0.3)
    ax.view_init(**view)
    ax.set_title(title)
    ax.set_xlim(*x_range)
    ax.set_ylim(*y_range)
    ax.set_zlim(*z_range)
    ax.set_axis_off()

fig.suptitle("3-Phase Coil | Biot–Savart Field\nCW/CCW Hue (XY) + Z Opacity\nTop | Bottom | Side | Isometric", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])

three_phase_multiview_filename = "3phase_biot_savart_multiview_centered_fixedshift.png"
plt.savefig(three_phase_multiview_filename, dpi=150)
# plt.show()


from numpy import gradient, stack


# Compute the vorticity field: ω = ∇ × v from (Bx, By, Bz)
dvz_dy, dvz_dx, dvz_dz = np.gradient(Bz3, axis=(1, 0, 2))
dvy_dz, dvy_dx, dvy_dy = np.gradient(By3, axis=(2, 0, 1))
dvx_dz, dvx_dx, dvx_dy = np.gradient(Bx3, axis=(2, 0, 1))

# Vorticity components
# Assume v = (vx, vy, vz) defined on a 3D grid
omega_x = dvy_dz - dvz_dy
omega_y = dvz_dx - dvx_dz
omega_z = dvx_dy - dvy_dx

# Swirl curvature tensor: R_ij = 0.5 * (∂i ω_j + ∂j ω_i)
R_swirl = np.empty((3, 3, *omega_x.shape))

# Derivatives of vorticity components
grad_omega_x = np.gradient(omega_x)
grad_omega_y = np.gradient(omega_y)
grad_omega_z = np.gradient(omega_z)

omega_fields = [omega_x, omega_y, omega_z]
grad_omega = [grad_omega_x, grad_omega_y, grad_omega_z]

# Build symmetric swirl curvature tensor
for i in range(3):
    for j in range(3):
        R_swirl[i, j] = 0.5 * (grad_omega[j][i] + grad_omega[i][j])

print(R_swirl.shape)  # (3, 3, Nx, Ny, Nz)


# Compute gravitational field: g_i = - ω_j R_ij
# First prepare the vorticity vector field
omega_vec = np.stack([omega_x, omega_y, omega_z], axis=0)  # shape: (3, Nx, Ny, Nz)

# Initialize gravity vector field g_i
g = np.zeros_like(omega_vec)  # shape: (3, Nx, Ny, Nz)

for i in range(3):  # i = x, y, z
    for j in range(3):  # j = x, y, z
        g[i] -= omega_vec[j] * R_swirl[i, j]

# Flatten for quiver plotting
Xg = X3.flatten()
Yg = Y3.flatten()
Zg = Z3.flatten()
gx = g[0].flatten()
gy = g[1].flatten()
gz = g[2].flatten()

# Normalize direction for coloring
gmag = np.sqrt(gx**2 + gy**2 + gz**2) + 1e-10
gx_n, gy_n, gz_n = gx / gmag, gy / gmag, gz / gmag

# Use direction to color by hue (similar to a compass)
colors_g = plt.cm.plasma((gz_n + 1) / 2)

# Plot the gravitational swirl field as quivers
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xg, Yg, Zg, gx, gy, gz, colors_g):
    ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.07, normalize=True,
              color=ci, linewidth=0.5, arrow_length_ratio=0.3)

ax.set_title("Swirl-Induced Gravitational Field\nfrom Vorticity Curvature Tensor", fontsize=14)
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
ax.set_axis_off()

gravity_field_filename = "vam_swirl_gravitational_field_3d.png"
plt.savefig(gravity_field_filename, dpi=150)
# plt.show()




# Define the 3-step polarity rotation for the coils
# (+1, -1, 0), (-1, 0, +1), (0, +1, -1)
polarities = [
    [1, -1, 0],
    [-1, 0, 1],
    [0, 1, -1]
]

# Scale factors for each phase
colors_for_phases = [0.0, 2 * np.pi / 3, 4 * np.pi / 3]
base_arrows_by_phase = []

# Reuse parameters from the previous 3-phase coil
for angle in colors_for_phases:
    seq_pos = generate_alternating_skip_sequence(
        corners=coil_corners,
        step_even=skip_forward,
        step_odd=skip_backward,
        radius=1.0,
        z_layer=0.0,
        angle_offset=angle
    )["positions"]
    # Stack vertically with num_layers
    full_positions = []
    for L in range(num_layers):
        z_off = L * layer_spacing + 0.25  # vertically centered
        full_positions += [(x, y, z + z_off) for x, y, z in seq_pos]
    base_arrows_by_phase.append(get_wire_arrows(full_positions))

# Store gravity fields at each timestep
gravity_fields = []

# Compute g_i = - ω_j R_ij for each polarity rotation
for step_idx, (p1, p2, p3) in enumerate(polarities):
    combined_arrows = []
    for p, arrows in zip([p1, p2, p3], base_arrows_by_phase):
        for origin, vector in arrows:
            combined_arrows.append((origin, np.array(vector) * p))

    # Compute Biot–Savart field
    Xs, Ys, Zs, Bxs, Bys, Bzs = compute_field_vectors(
        arrows=combined_arrows,
        grid_dims=grid_dims,
        x_range=x_range,
        y_range=y_range,
        z_range=z_range
    )

    # Vorticity
    dBz_dy, dBz_dx, dBz_dz = np.gradient(Bzs, axis=(1, 0, 2))
    dBy_dz, dBy_dx, dBy_dy = np.gradient(Bys, axis=(2, 0, 1))
    dBx_dz, dBx_dx, dBx_dy = np.gradient(Bxs, axis=(2, 0, 1))

    omega_x = dBy_dz - dBz_dy
    omega_y = dBz_dx - dBx_dz
    omega_z = dBx_dy - dBy_dx
    omega_vec = np.stack([omega_x, omega_y, omega_z], axis=0)

    # Gradients of ω
    grad_omega = [np.gradient(omega_x), np.gradient(omega_y), np.gradient(omega_z)]

    # Swirl curvature tensor R_ij
    R_swirl_step = np.empty((3, 3, *omega_x.shape))
    for i in range(3):
        for j in range(3):
            R_swirl_step[i, j] = 0.5 * (grad_omega[j][i] + grad_omega[i][j])

    # Compute g_i = -ω_j R_ij
    g_step = np.zeros_like(omega_vec)
    for i in range(3):
        for j in range(3):
            g_step[i] -= omega_vec[j] * R_swirl_step[i, j]

    gravity_fields.append(g_step)

# Sum the swirl gravitational field over the 3 steps
g_total = sum(gravity_fields)

# Flatten for visualization
Xg = Xs.flatten()
Yg = Ys.flatten()
Zg = Zs.flatten()
gx = g_total[0].flatten()
gy = g_total[1].flatten()
gz = g_total[2].flatten()
gmag = np.sqrt(gx**2 + gy**2 + gz**2)

# Normalize direction and color
gx_n, gy_n, gz_n = gx / (gmag + 1e-10), gy / (gmag + 1e-10), gz / (gmag + 1e-10)
colors_g = plt.cm.coolwarm((gz_n + 1) / 2)

# Plot the net gravitational field
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
for xi, yi, zi, dxi, dyi, dzi, ci in zip(Xg, Yg, Zg, gx, gy, gz, colors_g):
    ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=0.07, normalize=True,
              color=ci, linewidth=0.5, arrow_length_ratio=0.3)

ax.set_title("Net Swirl Gravity Field\nfrom Rotating (+−0,−0+,0+−) 3-Phase Sequence", fontsize=13)
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_zlim(*z_range)
ax.set_axis_off()

net_rotating_swirl_filename = "net_rotating_swirl_gravity_field.png"
plt.savefig(net_rotating_swirl_filename, dpi=150)
plt.show()