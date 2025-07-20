import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Coil geometry generators (reduced resolution)
def horn_torus_coil(R, r, turns, pts):
    theta = np.linspace(0, 2*np.pi*turns, pts)
    phi = theta
    x = (R + (r + 0.5*r*np.cos(theta)) * np.cos(phi)) * np.cos(theta)
    y = (R + (r + 0.5*r*np.cos(theta)) * np.cos(phi)) * np.sin(theta)
    z = (r + 0.5*r*np.cos(theta)) * np.sin(phi)
    return np.vstack([x, y, z]).T

def ring_torus_coil(R, r, turns, pts):
    theta = np.linspace(0, 2*np.pi*turns, pts)
    phi = theta
    x = (R + r*np.cos(phi)) * np.cos(theta)
    y = (R + r*np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)
    return np.vstack([x, y, z]).T

def starship_coil(R, r, turns, pts):
    theta = np.linspace(0, 2*np.pi*turns, pts)
    phi = (2 + 2/5) * theta
    x = (R + r*np.cos(phi)) * np.cos(theta)
    y = (R + r*np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)
    return np.vstack([x, y, z]).T

def ordinary_helix(R, pitch, turns, pts):
    theta = np.linspace(0, 2*np.pi*turns, pts)
    x = R * np.cos(theta)
    y = R * np.sin(theta)
    z = np.linspace(-pitch*turns/2, pitch*turns/2, pts)
    return np.vstack([x, y, z]).T

# Biot-Savart on slice (vectorized in chunks)
def biot_savart_slice(coil, X, Y):
    mu0, I = 4*np.pi*1e-7, 1.0
    dl = np.diff(coil, axis=0)
    L = coil[:-1]
    # flatten grid
    M = X.size
    points = np.stack([X.ravel(), Y.ravel(), np.zeros(M)], axis=1)
    B = np.zeros((M,3))
    # loop over segments
    for seg, dL in zip(L, dl):
        R_vec = points - seg
        dist3 = np.linalg.norm(R_vec,axis=1)**3 + 1e-9
        dB = np.cross(dL, R_vec) / dist3[:,None]
        B += dB
    B *= (mu0*I/(4*np.pi))
    Bx = B[:,0].reshape(X.shape)
    By = B[:,1].reshape(X.shape)
    return Bx, By

# Prepare slice grid
grid_n = 50
grid = np.linspace(-2, 2, grid_n)
X, Y = np.meshgrid(grid, grid)

# Coil setups (reduced pts)
coils = [
    horn_torus_coil(1.0, 0.3, 8, 800),
    ring_torus_coil(1.0, 0.3, 6, 600),
    starship_coil(1.0, 0.3, 5, 500),
    ordinary_helix(1.0, 0.2, 10, 800)
]
titles = ["Vorticial Horn Torus", "Vorticial Ring Torus", "Starship Coil", "Ordinary Helix"]

# Plot
fig, axes = plt.subplots(2,2, figsize=(10,10))
for ax, coil, title in zip(axes.flat, coils, titles):
    Bx, By = biot_savart_slice(coil, X, Y)
    Bmag = np.sqrt(Bx**2 + By**2)
    cf = ax.contourf(X, Y, Bmag, levels=30)
    ax.plot(coil[:,0], coil[:,1], color='black', linewidth=1)
    ax.set_title(title)
    ax.set_aspect('equal')
    fig.colorbar(cf, ax=ax, shrink=0.8)
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()
