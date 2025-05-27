import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
# Define helix parameters
radius = 0.25
length = 10
turns = 50
points = 1000
theta = np.linspace(0, 2 * np.pi * turns, points)
z = np.linspace(-length / 2, length / 2, points)

# Helix along Z-axis
x1 = radius * np.cos(theta)
y1 = radius * np.sin(theta)
z1 = z

# Helix along X-axis
x2 = z
y2 = radius * np.cos(theta)
z2 = radius * np.sin(theta)

# Helix along Y-axis
x3 = radius * np.cos(theta)
y3 = z
z3 = radius * np.sin(theta)

# Diagonal helix from (5,5,5) to (-5,-5,-5)
s = np.linspace(0, 1, 1000)
center_line = np.array([5 - 10 * s, 5 - 10 * s, 5 - 10 * s])
radius = 0.3
helix_t = np.linspace(0, 100 * np.pi, 1000)
# Orthogonal vectors for helical rotation
# Compute orthogonal vectors for rotation
v1 = np.array([1, -1, 0])
v2 = np.cross([1, 1, 1], v1)
v1 = v1 / np.linalg.norm(v1)
v2 = v2 / np.linalg.norm(v2)

# Reshape for broadcasting
v1 = v1.reshape(1, 3)
v2 = v2.reshape(1, 3)
cos_t = np.cos(helix_t).reshape(-1, 1)
sin_t = np.sin(helix_t).reshape(-1, 1)

# Compute the helical displacement and add to the center line
helix = center_line.T + radius * cos_t * v1 + radius * sin_t * v2


# Begin plotting
fig, axes = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={'projection': '3d'})
# Define view angles for each subplot
view_angles = [
    (38, 45),    # Angled view: Elevation, Azimuth
    (90, 180),    # Angled view
    (0, 0),    # Angled view
]

for i, (ax, (elev, azim)) in enumerate(zip(axes.flatten(), view_angles)):
    ax.plot(x1 + 1, y1, z1, label='Helix along Z-axis', color='blue')
    ax.plot(x2, y2 + 1, z2, label='Helix along X-axis', color='green')
    ax.plot(x3, y3, z3 + 1, label='Helix along Y-axis', color='red')
    ax.plot(helix[:, 0], helix[:, 1], helix[:, 2], label='Diagonal Helix', color='purple')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Triple Orthogonal Helices')
    ax.set_box_aspect([1, 1, 1])
    ax.legend()

    ax.view_init(elev=elev, azim=azim)


plt.tight_layout()
plt.subplots_adjust(left=0.03, right=0.97, wspace=0.2)



plt.tight_layout()

# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()