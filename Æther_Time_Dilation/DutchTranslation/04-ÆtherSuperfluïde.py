import matplotlib.pyplot as plt
import numpy as np

# Create grid
x = np.linspace(-5, 5, 20)
y = np.linspace(-5, 5, 20)
X, Y = np.meshgrid(x, y)

# Uniform æther flow (constant horizontal flow)
U = np.ones_like(X) * 0.8
V = np.zeros_like(Y)

# Define some vortices (topological structures)
def add_vortex(X, Y, x0, y0, strength=5):
    dx = X - x0
    dy = Y - y0
    r2 = dx**2 + dy**2 + 1e-3  # avoid division by zero
    return -strength * dy / r2, strength * dx / r2

# Superpose a few vortices
vortex_positions = [(-2, -2), (2, 2), (-3, 3)]
for x0, y0 in vortex_positions:
    u_vort, v_vort = add_vortex(X, Y, x0, y0, strength=3)
    U += u_vort
    V += v_vort

# Plot streamlines
fig, ax = plt.subplots(figsize=(7, 7))
strm = ax.streamplot(X, Y, U, V, color='cornflowerblue', linewidth=1, arrowsize=1)
ax.set_aspect('equal')
ax.set_title("Superfluïde æther in een Euclidische ruimte", fontsize=14)
ax.set_xlabel("x (ruimtecoördinaat)")
ax.set_ylabel("y (ruimtecoördinaat)")

# Add background grid to suggest Euclidean structure
ax.set_xticks(np.arange(-5, 6, 1))
ax.set_yticks(np.arange(-5, 6, 1))
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)

# Caption
plt.figtext(0.5, -0.05,
            "Een uniforme ætherstroom door een Euclidisch raster met enkele wervelstructuren.",
            wrap=True, horizontalalignment='center', fontsize=11)
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()