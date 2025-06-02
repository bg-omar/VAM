import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Trefoil knot parametric centerline
theta = np.linspace(0, 2 * np.pi, 100)
x = (2 + np.cos(3 * theta)) * np.cos(2 * theta)
y = (2 + np.cos(3 * theta)) * np.sin(2 * theta)
z = np.sin(3 * theta)

# Compute tangent at center point
i_center = len(x) // 2
dx = x[i_center + 1] - x[i_center - 1]
dy = y[i_center + 1] - y[i_center - 1]
dz = z[i_center + 1] - z[i_center - 1]
tangent = np.array([dx, dy, dz])
tangent /= np.linalg.norm(tangent)

# Desired alignment vector (align to z-axis)
target = np.array([0, 0, 1])

# Compute axis and angle for rotation
axis = np.cross(tangent, target)
axis_norm = np.linalg.norm(axis)
angle = np.arccos(np.clip(np.dot(tangent, target), -1.0, 1.0))

def rodrigues_rotation_matrix(axis, angle):
    axis = axis / np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]])
    I = np.eye(3)
    return I + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)

R = rodrigues_rotation_matrix(axis, angle) if axis_norm != 0 else np.eye(3)
x_rot, y_rot, z_rot = R @ np.vstack([x, y, z])

# Secondary rotation to align 3 key tangents to XYZ
target_axes = np.eye(3)
fractions = [11/36, 23/36, 35/36]
tangents = []

for frac in fractions:
    idx = int(len(x_rot) * frac)
    dx = x_rot[idx + 1] - x_rot[idx] if idx < len(x_rot) - 1 else x_rot[idx] - x_rot[idx - 1]
    dy = y_rot[idx + 1] - y_rot[idx] if idx < len(y_rot) - 1 else y_rot[idx] - y_rot[idx - 1]
    dz = z_rot[idx + 1] - z_rot[idx] if idx < len(z_rot) - 1 else z_rot[idx] - z_rot[idx - 1]
    t = np.array([dx, dy, dz])
    t /= np.linalg.norm(t)
    tangents.append(t)

current_frame = np.stack(tangents, axis=1)
U, _, Vt = np.linalg.svd(current_frame @ target_axes.T)
R2 = U @ Vt
x_final, y_final, z_final = R2 @ np.vstack([x_rot, y_rot, z_rot])

# Build tube
n_circle = 6
tube_radius = 0.3
phi = np.linspace(0, 2 * np.pi, n_circle)
circle_x = tube_radius * np.cos(phi)
circle_y = tube_radius * np.sin(phi)
tube_x, tube_y, tube_z = [], [], []

for i in range(len(x_final)):
    dx, dy, dz = (x_final[i + 1] - x_final[i], y_final[i + 1] - y_final[i], z_final[i + 1] - z_final[i]) \
        if i < len(x_final) - 1 else (x_final[i] - x_final[i - 1], y_final[i] - y_final[i - 1], z_final[i] - z_final[i - 1])
    tangent = np.array([dx, dy, dz])
    tangent /= np.linalg.norm(tangent)
    normal = np.cross(tangent, [0, 0, 1]) if np.linalg.norm(np.cross(tangent, [0, 0, 1])) != 0 \
        else np.cross(tangent, [0, 1, 0])
    normal /= np.linalg.norm(normal)
    binormal = np.cross(tangent, normal)
    binormal /= np.linalg.norm(binormal)
    ring_x = x_final[i] + circle_x * normal[0] + circle_y * binormal[0]
    ring_y = y_final[i] + circle_x * normal[1] + circle_y * binormal[1]
    ring_z = z_final[i] + circle_x * normal[2] + circle_y * binormal[2]
    tube_x.append(ring_x)
    tube_y.append(ring_y)
    tube_z.append(ring_z)

# Compute final quivers
quiver_arrows = []
for frac in fractions:
    idx = int(len(x_final) * frac)
    dx = x_final[idx + 1] - x_final[idx] if idx < len(x_final) - 1 else x_final[idx] - x_final[idx - 1]
    dy = y_final[idx + 1] - y_final[idx] if idx < len(y_final) - 1 else y_final[idx] - y_final[idx - 1]
    dz = z_final[idx + 1] - z_final[idx] if idx < len(z_final) - 1 else z_final[idx] - z_final[idx - 1]
    tangent = np.array([dx, dy, dz])
    tangent /= np.linalg.norm(tangent)
    point = (x_final[idx], y_final[idx], z_final[idx])

    quiver_arrows.append((point, tangent))

color = ['crimson', 'darkorange', 'gold']
# Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
i=0
for point, tangent in quiver_arrows:
    ax.quiver(*point, *tangent, color=color[i], length=5.0, normalize=True, linewidth=5, label=i)
    i += 1

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

ax.set_title("Trefoil Knot with Quivers Aligned to X/Y/Z Directions")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([-3, 3])
ax.set_box_aspect([1, 1, 1])
ax.legend()
ax.view_init(elev=10, azim=45)
plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()