import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML

# Generate Phase A full coil (center-tapped combined halves)
coil_corners = 12
coil_amount = 3
total_corners = coil_corners * coil_amount
num_layers = 10
z_spacing = 0.1
base_sequence = [1, 6, 11, 4, 9, 2, 7, 12, 5, 10, 3, 8, 1]

# Compute rotated positions
angles_rot = np.linspace(0, 2*np.pi, total_corners, endpoint=False) - np.pi*1.5
angles_rot = angles_rot[::-1]
positions_rot = {i+1: (np.cos(angles_rot[i]), np.sin(angles_rot[i])) for i in range(total_corners)}

# Generate full Phase A coil (all layers)
seqA = [((num*3 - 1) % total_corners) + 1 for num in base_sequence]
coilA = []
for layer in range(num_layers):
    z0 = -num_layers*z_spacing/2 + layer*z_spacing
    for num in seqA:
        x, y = positions_rot[num]
        coilA.append((x, y, z0))
coilA = np.array(coilA)

# Biot–Savart at z0 slice
def biot_savart_at_z(coil, X, Y, z0):
    mu0, I = 4*np.pi*1e-7, 1.0
    dl = np.diff(coil, axis=0)
    L = coil[:-1]
    Bx = np.zeros_like(X)
    By = np.zeros_like(Y)
    for (x0,y0,zc), dL in zip(L, dl):
        rx = X - x0
        ry = Y - y0
        rz = z0 - zc
        r3 = (rx**2 + ry**2 + rz**2)**1.5 + 1e-9
        Bx += (dL[1]*rz - dL[2]*ry)/r3
        By += (dL[2]*rx - dL[0]*rz)/r3
    factor = mu0*I/(4*np.pi)
    return Bx*factor, By*factor

# Prepare grid
grid_n = 100
grid = np.linspace(-1.5,1.5,grid_n)
X, Y = np.meshgrid(grid, grid)

# Z-slices for animation
z_levels = np.linspace(-num_layers*z_spacing/2, num_layers*z_spacing/2, 30)

# Setup figure
fig, ax = plt.subplots(figsize=(6,6))
cf = ax.contourf(X, Y, np.zeros_like(X), levels=30, cmap='viridis')
line, = ax.plot([], [], 'k-', lw=1)
title = ax.text(0.5,1.05, '', transform=ax.transAxes, ha='center')

def init():
    ax.set_xlim(-1.5,1.5)
    ax.set_ylim(-1.5,1.5)
    ax.set_aspect('equal')
    line.set_data([], [])
    title.set_text('')
    return cf.collections + [line, title]

def animate(i):
    z0 = z_levels[i]
    Bx, By = biot_savart_at_z(coilA, X, Y, z0)
    Bmag = np.sqrt(Bx**2 + By**2)
    ax.clear()
    cf = ax.contourf(X, Y, Bmag, levels=30, cmap='viridis')
    ax.plot(coilA[:,0], coilA[:,1], 'k-', lw=1, alpha=0.3)
    ax.set_title(f'z = {z0:.2f}')
    ax.set_aspect('equal')
    return cf.collections

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=len(z_levels), init_func=init, blit=False, interval=200)
plt.close()

# Display animation
HTML(ani.to_jshtml())
