import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Define grid
grid_size = 200
x = np.linspace(-5, 5, grid_size)
y = np.linspace(-5, 5, grid_size)
X, Y = np.meshgrid(x, y)

# Vortex parameters
gamma = 5.0  # circulation strength
r_squared = X**2 + Y**2
epsilon = 0.1  # to prevent division by zero

# Compute velocity field for a rotating vortex (incompressible 2D potential vortex)
U =  gamma * Y / (r_squared + epsilon)
V = -gamma * X / (r_squared + epsilon)

# Mask central region to simulate a rotating sphere (e.g., core radius ~ 0.5)
mask = r_squared < 0.25
U[mask] = 0
V[mask] = 0

# Plotting
fig, ax = plt.subplots(figsize=(8, 8))
strm = ax.streamplot(X, Y, U, V, color=np.sqrt(U**2 + V**2), linewidth=1.2, cmap='plasma')
circle = plt.Circle((0, 0), 0.5, color='black', zorder=10)
ax.add_artist(circle)

ax.set_title('Æther Frame-Dragging Around Rotating Vortex Core (VAM Analogy)')
ax.set_xlabel('x (arbitrary units)')
ax.set_ylabel('y (arbitrary units)')
ax.set_aspect('equal')
plt.colorbar(strm.lines, label='Flow speed')
plt.tight_layout()

import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()
