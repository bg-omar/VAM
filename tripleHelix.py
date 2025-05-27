import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
# Define helix parameters
radius = 0.25
length = 10
turns = 100
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
# Re-run after reset: Trefoil knot with tangential quiver placement
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

# Trefoil knot parametric centerline
theta = np.linspace(0, 2 * np.pi, 300)
x = (2 + np.cos(3 * theta)) * np.cos(2 * theta)
y = (2 + np.cos(3 * theta)) * np.sin(2 * theta)
z = np.sin(3 * theta)

# Parameters for tube surface (vortex core)
tube_radius = 0.3
n_circle = 12  # resolution of the circular cross-section
phi = np.linspace(0, 2 * np.pi, n_circle)
circle_x = tube_radius * np.cos(phi)
circle_y = tube_radius * np.sin(phi)

# Create 3D tube coordinates
tube_x, tube_y, tube_z = [], [], []
quiver_pos = 150  # mid point for quiver placement
quiver_point = None
quiver_tangent = None

for i in range(len(x)):
    # approximate local tangent
    if i < len(x) - 1:
        dx, dy, dz = x[i+1] - x[i], y[i+1] - y[i], z[i+1] - z[i]
    else:
        dx, dy, dz = x[i] - x[i-1], y[i] - y[i-1], z[i] - z[i-1]
    tangent = np.array([dx, dy, dz])
    tangent /= np.linalg.norm(tangent)
    # generate two orthogonal vectors
    normal = np.cross(tangent, [0, 0, 1])
    if np.linalg.norm(normal) == 0:
        normal = np.cross(tangent, [0, 1, 0])
    normal /= np.linalg.norm(normal)
    binormal = np.cross(tangent, normal)
    binormal /= np.linalg.norm(binormal)
    # build the ring
    ring_x = x[i] + circle_x * normal[0] + circle_y * binormal[0]
    ring_y = y[i] + circle_x * normal[1] + circle_y * binormal[1]
    ring_z = z[i] + circle_x * normal[2] + circle_y * binormal[2]
    tube_x.append(ring_x)
    tube_y.append(ring_y)
    tube_z.append(ring_z)

    if i == quiver_pos:
        quiver_point = (x[i], y[i], z[i])
        quiver_tangent = tangent



# Begin plotting
fig, axes = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={'projection': '3d'})
# Define view angles for each subplot
view_angles = [
(10, 45),
    (38, 45),    # Angled view: Elevation, Azimuth
    (90, 180),    # Angled view
       # Angled view
]

for i, (ax, (elev, azim)) in enumerate(zip(axes.flatten(), view_angles)):
    # Quiver: Tangential velocity Ce at mid-point
    if quiver_point and quiver_tangent is not None:
        ax.quiver(quiver_point[0], quiver_point[1], quiver_point[2],
                  quiver_tangent[0], quiver_tangent[1], quiver_tangent[2],
                  color='crimson', length=5.0, normalize=True, linewidth=5,
                  label='Tangential Velocity $C_e$')

    # Create surface segments
    for i in range(len(tube_x) - 1):
        for j in range(n_circle - 1):
            verts = [
                [tube_x[i][j], tube_y[i][j], tube_z[i][j]],
                [tube_x[i + 1][j], tube_y[i + 1][j], tube_z[i + 1][j]],
                [tube_x[i + 1][j + 1], tube_y[i + 1][j + 1], tube_z[i + 1][j + 1]],
                [tube_x[i][j + 1], tube_y[i][j + 1], tube_z[i][j + 1]]
            ]
            poly = Poly3DCollection([verts], color=plt.cm.plasma(i / len(tube_x)), linewidths=0.05, edgecolor='gray')
            ax.add_collection3d(poly)

    ax.plot(x1 + 1, y1, z1, label='Helix along Z-axis', color='blue')
    ax.plot(x2, y2 + 1, z2, label='Helix along X-axis', color='green')
    if i==1:
        ax.plot(helix[:, 0], helix[:, 1], helix[:, 2], label='Diagonal Helix', color='purple')
    ax.plot(x3, y3, z3 + 1, label='Helix along Y-axis', color='red')


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