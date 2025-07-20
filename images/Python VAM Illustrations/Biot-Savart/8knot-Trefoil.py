import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_figure8(N=400):
    s = np.linspace(0, 2*np.pi, N)
    x = (2 + np.cos(2*s)) * np.cos(3*s)
    y = (2 + np.cos(2*s)) * np.sin(3*s)
    z = np.sin(4*s)
    return np.stack((x,y,z), axis=1)

def generate_trefoil(N=400):
    t = np.linspace(0, 2*np.pi, N)
    x = np.sin(t) + 2*np.sin(2*t)
    y = np.cos(t) - 2*np.cos(2*t)
    z = -np.sin(3*t)
    return np.stack((x,y,z), axis=1)

def compute_tangents(X):
    dX = np.gradient(X, axis=0)
    return dX / np.linalg.norm(dX, axis=1, keepdims=True)

def biot_savart(r, X, T, Gamma=1.0):
    v = np.zeros(3)
    coeff = Gamma / (4*np.pi)
    for xi, ti in zip(X, T):
        dr = r - xi
        norm = np.linalg.norm(dr)
        if norm > 1e-6:
            v += coeff * np.cross(ti, dr) / norm**3
    return v

def compute_vorticity(grid, vfield, h):
    # Central differences to approximate curl component-wise
    curl = np.zeros_like(vfield)
    # indices: (ix,iy,iz,component)
    for comp,varpair in enumerate([(1,2),(2,0),(0,1)]):
        i,j = varpair
        diff_j = (np.roll(vfield[..., i], -1, axis=j) - np.roll(vfield[..., i], 1, axis=j)) / (2*h)
        diff_i = (np.roll(vfield[..., j], -1, axis=i) - np.roll(vfield[..., j], 1, axis=i)) / (2*h)
        curl[..., comp] = diff_j - diff_i
    return curl

# Generate both knots
pos8, tan8 = generate_figure8(), compute_tangents(generate_figure8())
pos3, tan3 = generate_trefoil(), compute_tangents(generate_trefoil())

# Define small grid around origin
grid_N = 15
L = 2.0
axis = np.linspace(-L, L, grid_N)
Xg,Yg,Zg = np.meshgrid(axis, axis, axis, indexing='ij')
h = axis[1] - axis[0]

# Compute velocity at each grid point for both knots
points = np.stack((Xg, Yg, Zg), axis=-1).reshape(-1,3)
V8 = np.array([biot_savart(p, pos8, tan8) for p in points]).reshape(grid_N,grid_N,grid_N,3)
V3 = np.array([biot_savart(p, pos3, tan3) for p in points]).reshape(grid_N,grid_N,grid_N,3)

# Compute vorticity
omega8 = compute_vorticity(axis, V8, h)
omega3 = compute_vorticity(axis, V3, h)

# Compute magnitude
mag8 = np.linalg.norm(omega8, axis=-1)
mag3 = np.linalg.norm(omega3, axis=-1)

# Plot slice at z=0
mid = grid_N//2
fig, axs = plt.subplots(1,2,figsize=(12,5))
c1 = axs[0].contourf(axis, axis, mag8[:,:,mid], cmap='viridis')
axs[0].set_title('|∇×v| for Figure‑8 (z=0)')
fig.colorbar(c1, ax=axs[0])
c2 = axs[1].contourf(axis, axis, mag3[:,:,mid], cmap='inferno')
axs[1].set_title('|∇×v| for Trefoil (z=0)')
fig.colorbar(c2, ax=axs[1])
for ax in axs:
    ax.set_xlabel('x'); ax.set_ylabel('y')
plt.tight_layout()
plt.show()
