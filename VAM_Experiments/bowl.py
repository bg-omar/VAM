import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')

# Params
turns = 30
points_per_turn = 200
height = 1.5
r_start = 0.5
r_end = 1.0
offset = 1.5
power = 2.2

theta = np.linspace(0, 2 * np.pi * turns, turns * points_per_turn)
z = np.linspace(0, height, turns * points_per_turn)
scale = np.linspace(0, 1, turns * points_per_turn)

# Data for 3 bowls
r1 = np.linspace(r_start, r_end, turns * points_per_turn)
x1, y1, z1 = r1 * np.cos(theta) - offset, r1 * np.sin(theta), z

r2 = r_start + (r_end - r_start) * (scale ** power)
x2, y2, z2 = r2 * np.cos(theta), r2 * np.sin(theta), z

r3 = r_end - (r_end - r_start) * (scale ** power)
x3, y3, z3 = r3 * np.cos(theta) + offset, r3 * np.sin(theta), height - z

# Plot setup
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.05, right=0.8)  # space for buttons

# Plot bowls
line1, = ax.plot(x1, y1, z1, color='orange', lw=2, label='Linear')
line2, = ax.plot(x2, y2, z2, color='purple', lw=2, label='Exponential')
line3, = ax.plot(x3, y3, z3, color='green', lw=2, label='Flipped Inverse')

# Axis scaling
all_x = np.concatenate([x1, x2, x3])
all_y = np.concatenate([y1, y2, y3])
all_z = np.concatenate([z1, z2, z3])
max_range = np.array([all_x.ptp(), all_y.ptp(), all_z.ptp()]).max() / 2.0
mid_x, mid_y, mid_z = all_x.mean(), all_y.mean(), all_z.mean()

ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

# Styling
ax.set_title("Toggleable 3D Bowls")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.view_init(elev=25, azim=45)

# CheckButtons
rax = plt.axes([0.82, 0.4, 0.15, 0.15])  # [left, bottom, width, height]
labels = ['Linear', 'Exponential', 'Flipped']
visibility = [True, True, True]
check = CheckButtons(rax, labels, visibility)

# Toggle handler
lines = [line1, line2, line3]

def toggle(label):
    index = labels.index(label)
    lines[index].set_visible(not lines[index].get_visible())
    plt.draw()

def compute_biot_savart_field(x, y, z, wire_x, wire_y, wire_z, dl, I=1.0):
    μ0 = 1  # Simplified constant
    field = np.zeros(3)
    for i in range(len(wire_x)):
        r_vec = np.array([x - wire_x[i], y - wire_y[i], z - wire_z[i]])
        r_mag = np.linalg.norm(r_vec)
        if r_mag < 1e-3:
            continue
        dB = np.cross(dl[i], r_vec) / (r_mag**3 + 1e-12)
        field += dB
    return μ0 * I / (4 * np.pi) * field

# --- Prepare coil segment tangents for field computation ---
dx = np.gradient(x3)
dy = np.gradient(y3)
dz = np.gradient(z3)
dl_vecs = np.vstack((dx, dy, dz)).T

# --- Seed point near the coil ---
seed = np.array([x3[100] + 0.1, y3[100], z3[100]])  # Slight offset from wire

# --- Trace field line using Euler integration ---
trajectory = [seed]
dt = 0.05  # step size
for _ in range(300):  # steps
    pos = trajectory[-1]
    B = compute_biot_savart_field(pos[0], pos[1], pos[2], x3, y3, z3, dl_vecs)
    Bnorm = np.linalg.norm(B)
    if Bnorm < 1e-6:
        break
    B_dir = B / Bnorm
    next_pos = pos + dt * B_dir
    trajectory.append(next_pos)

trajectory = np.array(trajectory)
ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], 'k--', linewidth=1.5, label='Field Line')

check.on_clicked(toggle)
plt.show()
