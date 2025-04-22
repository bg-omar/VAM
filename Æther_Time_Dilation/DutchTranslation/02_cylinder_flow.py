import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt

# Rooster
x = np.linspace(-2, 2, 500)
y = np.linspace(-2, 2, 500)
X, Y = np.meshgrid(x, y)
R2 = X**2 + Y**2

# Parameters
U = 1.0      # achtergrondstroom
a = 0.5      # straal van de cilinder
eps = 1e-6   # om singulariteit te vermijden

# Stroming rond een vaste cilinder
u = U * (1 - (a**2 * (X**2 - Y**2)) / (R2**2 + eps))
v = -2 * U * a**2 * X * Y / (R2**2 + eps)

# Masker binnen de cilinder (r < a)
u[R2 < a**2] = 0
v[R2 < a**2] = 0

# Plot
fig, ax = plt.subplots(figsize=(7,5))
strm = ax.streamplot(X, Y, u, v, color='navy', density=2, linewidth=1)

# Cilinder
circle = plt.Circle((0, 0), a, color='black', fill=False, linewidth=2)
ax.add_patch(circle)

# Assen en labels
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_title('Stroming rond een vaste cilinder')
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig("02_cylinder_flow.png", dpi=300)
plt.show()