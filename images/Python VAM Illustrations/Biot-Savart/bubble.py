import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
# Vectorized Biot–Savart for a (p,q) torus knot on a 2D slice

# 1. Generate torus-knot wire
def torus_knot(p, q, R, r, N=2000):
    phi = np.linspace(0, 2*np.pi, N, endpoint=False)
    x = (R + r * np.cos(q * phi)) * np.cos(p * phi)
    y = (R + r * np.cos(q * phi)) * np.sin(p * phi)
    z = r * np.sin(q * phi)
    return np.stack((x, y, z), axis=1)

p, q = 2, 3
R, r = 1.0, 0.4
wire_pts = torus_knot(p, q, R, r)
wire_next = np.vstack((wire_pts[1:], wire_pts[0]))
dL = wire_next - wire_pts

# 2. Create a 2D slice grid (y=0 plane)
grid_size = 100
x = np.linspace(-2, 2, grid_size)
z = np.linspace(-2, 2, grid_size)
X, Z = np.meshgrid(x, z)
points = np.stack((X.ravel(), np.zeros(X.size), Z.ravel()), axis=1)  # (M,3)

# 3. Compute Biot–Savart by broadcasting
# R_vec: shape (M, N, 3)
R_vec = points[:, None, :] - wire_pts[None, :, :]
dist3 = np.linalg.norm(R_vec, axis=2)**3
dist3[dist3 == 0] = np.inf  # avoid singularity

# cross product dL x R_vec, shape (M, N, 3)
cross_prod = np.cross(dL[None, :, :], R_vec, axis=2)

# sum over wire segments
B = np.sum(cross_prod / dist3[..., None], axis=1)  # shape (M,3)

# extract in-plane components and magnitude
Bx = B[:, 0].reshape(X.shape)
Bz = B[:, 2].reshape(X.shape)
Vmag = np.sqrt(Bx**2 + Bz**2)

# 4. Plot velocity magnitude contour
plt.figure(figsize=(6, 6))
contours = plt.contourf(X, Z, Vmag, levels=50)
plt.xlabel('x')
plt.ylabel('z')
plt.title('|v| from Vectorized Biot–Savart on y=0 slice')
plt.colorbar(contours, label='|v| (arb. units)')
plt.tight_layout()
plt.show()
