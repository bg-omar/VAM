import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.widgets import RadioButtons


# Params
turns = 30
points_per_turn = 200
height = 1.5
r_start = 0.38
r_end = 1.0
offset = 0
power = 2.618

theta = np.linspace(0, 2 * np.pi * turns, turns * points_per_turn)
z = np.linspace(0, height, turns * points_per_turn)
scale = np.linspace(0, 1, turns * points_per_turn)

# Data for 3 bowls
r1 = r_end - (r_end - r_start) * (scale ** power)
x1, y1, z1 = r1 * np.cos(theta) + offset, r1 * np.sin(theta), height - z

r2 = r_start + (r_end - r_start) * (scale ** power)
x2, y2, z2 = r2 * np.cos(theta), r2 * np.sin(theta), z

r3 = np.linspace(r_start, r_end, turns * points_per_turn)
x3, y3, z3 = r3 * np.cos(theta) - offset, r3 * np.sin(theta), z


# Plot setup
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.05, right=0.8)  # space for buttons

# Plot bowls
line1, = ax.plot(x1, y1, z1, color='green', lw=2, label='Exponential')
line2, = ax.plot(x2, y2, z2, color='purple', lw=2, label='Linear')
line3, = ax.plot(x3, y3, z3, color='red', lw=2, label='Inverse Exp')

# Axis scaling
all_x = np.concatenate([x1, x2, x3])
all_y = np.concatenate([y1, y2, y3])
all_z = np.concatenate([z1, z2, z3])
max_range = np.array([np.ptp(all_x), np.ptp(all_y), np.ptp(all_z)]).max() / 2.0

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

# Place RadioButtons centered below the plot (adjust [left, bottom, width, height] as needed)
rax = plt.axes([0.45, 0.02, 0.1, 0.15])  # Centered at the bottom

labels = ['Linear', 'Exponential', 'Flipped']
radio = RadioButtons(rax, labels, active=0)  # Show 'Linear' by default

lines = [line1, line2, line3]

# Only the selected bowl is visible
def select(label):
    for i, l in enumerate(labels):
        lines[i].set_visible(l == label)
    plt.draw()

radio.on_clicked(select)

# Initially, hide others
for i, l in enumerate(labels):
    lines[i].set_visible(i == 0)

def toggle(label):
    index = labels.index(label)
    lines[index].set_visible(not lines[index].get_visible())
    plt.draw()


plt.show()

