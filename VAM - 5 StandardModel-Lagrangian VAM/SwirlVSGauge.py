import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Set up the grid
x, y = np.meshgrid(np.linspace(-2, 2, 30), np.linspace(-2, 2, 30))
r = np.sqrt(x**2 + y**2)
theta = np.arctan2(y, x)

# Vortex field: swirl velocity v = ∇θ
vx = -y / (r**2 + 0.1)  # Avoid division by zero
vy = x / (r**2 + 0.1)

# Gauge potential: similar to vortex field
ax = -y / (r**2 + 0.1)
ay = x / (r**2 + 0.1)

fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Left plot: Swirl field (fluid side)
axs[0].quiver(x, y, vx, vy, color='blue', alpha=0.6)
axs[0].set_title("Swirl Field (Fluid View)")
axs[0].set_xlabel(r"$x$")
axs[0].set_ylabel(r"$y$")
axs[0].text(-1.8, 1.7, r"$\vec{v} = \nabla \theta$", fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
axs[0].text(-1.8, -1.9, r"Circulation $\Gamma = \oint \vec{v} \cdot d\ell$", fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
axs[0].axis('equal')
axs[0].grid(True)

# Right plot: Gauge potential field (field theory side)
axs[1].quiver(x, y, ax, ay, color='green', alpha=0.6)
axs[1].set_title("Gauge Potential Field (QFT View)")
axs[1].set_xlabel(r"$x$")
axs[1].set_ylabel(r"$y$")
axs[1].text(-1.8, 1.7, r"$A_\mu = \partial_\mu \theta$", fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
axs[1].text(-1.8, -1.9, r"$F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$", fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
axs[1].axis('equal')
axs[1].grid(True)

plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()

