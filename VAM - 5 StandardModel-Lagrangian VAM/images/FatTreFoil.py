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

# Plot the tube
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

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
            [tube_x[i+1][j], tube_y[i+1][j], tube_z[i+1][j]],
            [tube_x[i+1][j+1], tube_y[i+1][j+1], tube_z[i+1][j+1]],
            [tube_x[i][j+1], tube_y[i][j+1], tube_z[i][j+1]]
        ]
        poly = Poly3DCollection([verts], color=plt.cm.plasma(i / len(tube_x)), linewidths=0.05, edgecolor='gray')
        ax.add_collection3d(poly)

# Final plot adjustments
ax.set_xlim([-4, 4])
ax.set_ylim([-4, 4])
ax.set_zlim([-2.5, 2.5])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Trefoil Knot with Physical Vortex Core (radius $r_c$)')

ax.legend()
plt.tight_layout()
plt.show()