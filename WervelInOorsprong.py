import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# Define grid
x = np.linspace(-3, 3, 400)
y = np.linspace(-3, 3, 400)
X, Y = np.meshgrid(x, y)

# Avoid division by zero
epsilon = 1e-5
r2 = X**2 + Y**2 + epsilon
r = np.sqrt(r2)

# Velocity field for vortex at origin (circulation Γ = 1)
Gamma = 1
U = -Gamma * Y / (2 * np.pi * r2)
V =  Gamma * X / (2 * np.pi * r2)

# Streamfunction and potential
psi = Gamma * np.log(r)
phi = -Gamma * np.arctan2(Y, X)

# Mask the singularity
mask = r < 0.05
U[mask] = np.nan
V[mask] = np.nan

# Plot setup
fig, ax = plt.subplots(figsize=(5, 5))

# Plot a single streamfunction line (Psi = 0) with arrows
circle_theta = np.linspace(0, 2*np.pi, 300)
R = 1.5
x_circle = R * np.cos(circle_theta)
y_circle = R * np.sin(circle_theta)
ax.plot(x_circle, y_circle, color='black', linewidth=1)

# Add an arrow to the circular streamline
arrow_pos = 50
ax.annotate('', xy=(x_circle[arrow_pos+1], y_circle[arrow_pos+1]),
            xytext=(x_circle[arrow_pos], y_circle[arrow_pos]),
            arrowprops=dict(arrowstyle='->', color='black'))

# Φ = const. (equipotential lines = radial dashed lines)
phi_lines = np.linspace(-np.pi, np.pi, 9)
for angle in phi_lines:
    ax.plot([0, 3*np.cos(angle)], [0, 3*np.sin(angle)], 'k--', linewidth=1)

# Axes
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

# Labels
ax.text(1.6, 0.3, r'$\Phi = \mathrm{const.}$', fontsize=12)
ax.text(0.2, -2.0, r'$\Psi = \mathrm{const.}$', fontsize=12)
ax.text(-2.7, 0.05, r'$v_{\mathrm{tang}} = \frac{-\Gamma}{2 \pi r}$', fontsize=12)
ax.text(2.8, 0.05, r'$x$', fontsize=12)
ax.text(0.05, 2.8, r'$y$', fontsize=12)

# Title
ax.set_title(r'Figuur 2.5: Wervel in de oorsprong.', fontsize=10)

# Formatting
ax.set_aspect('equal')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.axis('off')

plt.tight_layout()
plt.show()