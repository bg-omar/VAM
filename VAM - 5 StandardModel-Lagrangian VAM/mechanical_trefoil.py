# Re-run after environment reset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters
n_main = 300  # resolution along the knot
n_ridges = 30  # number of ridges along the knot (roughly matching photo)
ridge_depth = 0.1  # amplitude of ridge
tube_radius = 0.4

# Trefoil knot parametric centerline
theta = np.linspace(0, 2 * np.pi, n_main)
x = (2 + np.cos(3 * theta)) * np.cos(2 * theta)
y = (2 + np.cos(3 * theta)) * np.sin(2 * theta)
z = np.sin(3 * theta)

# Local tangent vector
dx = np.gradient(x)
dy = np.gradient(y)
dz = np.gradient(z)
tangent = np.vstack([dx, dy, dz])
tangent /= np.linalg.norm(tangent, axis=0)

# Create orthogonal frame (normal and binormal)
reference = np.array([0, 0, 1])
normal = np.cross(tangent.T, reference)
normal[np.linalg.norm(normal, axis=1) == 0] = [0, 1, 0]
normal /= np.linalg.norm(normal, axis=1)[:, None]
binormal = np.cross(tangent.T, normal)

# Ridge modulation along the knot
phi = np.linspace(0, 2 * np.pi * n_ridges, n_main)
ridge_mod = 1 + ridge_depth * np.sin(phi)

# Create surface points
n_circle = 20
angle = np.linspace(0, 2 * np.pi, n_circle)
circle_x = np.cos(angle)
circle_y = np.sin(angle)

X, Y, Z = [], [], []
for i in range(n_main):
    for j in range(n_circle):
        dx = ridge_mod[i] * tube_radius * (circle_x[j] * normal[i] + circle_y[j] * binormal[i])
        X.append(x[i] + dx[0])
        Y.append(y[i] + dx[1])
        Z.append(z[i] + dx[2])

X = np.array(X).reshape((n_main, n_circle))
Y = np.array(Y).reshape((n_main, n_circle))
Z = np.array(Z).reshape((n_main, n_circle))

# Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='darkslateblue', edgecolor='gray', linewidth=0.05, alpha=0.95)

ax.set_title("Mechanische Trefoilknoop met Schroefstructuur (VAM)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.view_init(elev=20, azim=45)
plt.tight_layout()
plt.show()