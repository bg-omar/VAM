# Re-import required libraries after code execution state reset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Diagram 6: Swirlrichting (chiraliteit) en lading
theta = np.linspace(0, 2 * np.pi, 500)
R = 2
r = 0.5

# Linksdraaiend vortexknoop
x_left = (R + r * np.cos(3 * theta)) * np.cos(2 * theta)
y_left = (R + r * np.cos(3 * theta)) * np.sin(2 * theta)
z_left = r * np.sin(3 * theta)

# Rechtsdraaiend vortexknoop
x_right = (R + r * np.cos(-3 * theta)) * np.cos(2 * theta)
y_right = (R + r * np.cos(-3 * theta)) * np.sin(2 * theta)
z_right = r * np.sin(-3 * theta)

# Plot setup
fig, axes = plt.subplots(1, 2, figsize=(14, 6), subplot_kw={'projection': '3d'})

# Linksdraaiend
ax = axes[0]
ax.plot(x_left, y_left, z_left, color='crimson', linewidth=2)
ax.set_title("Linksdraaiend (positieve lading $+e$)")
ax.set_xlim([-4, 4])
ax.set_ylim([-4, 4])
ax.set_zlim([-2.5, 2.5])
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

# Rechtsdraaiend
ax = axes[1]
ax.plot(x_right, y_right, z_right, color='navy', linewidth=2)
ax.set_title("Rechtsdraaiend (negatieve lading $-e$)")
ax.set_xlim([-4, 4])
ax.set_ylim([-4, 4])
ax.set_zlim([-2.5, 2.5])
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")


# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()