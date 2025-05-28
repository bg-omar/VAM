# Re-import necessary modules after code execution state reset
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Torus knot parameters (p, q) with labels
torus_knots = [
    (2, 3, "Waterstof (T(2,3))"),
    (2, 5, "Helium (T(2,5))"),
    (2, 7, "Lithium (T(2,7))"),
    (2, 9, "Beryllium (T(2,9))"),
    (2, 11, "Boor (T(2,11))"),
    (2, 13, "Koolstof (T(2,13))"),
    (4, 3, "IJzer (T(4,3))"),
]

# Function to generate torus knot
def generate_torus_knot(p, q, n_points=1000):
    theta = np.linspace(0, 2 * np.pi, n_points)
    r = 2 + np.cos(q * theta)
    x = r * np.cos(p * theta)
    y = r * np.sin(p * theta)
    z = np.sin(q * theta)
    return x, y, z

# Create a large figure with subplots showing all torus knots from top-down view
fig = plt.figure(figsize=(18, 10))
cols = 4
rows = int(np.ceil(len(torus_knots) / cols))

for idx, (p, q, label) in enumerate(torus_knots):
    x, y, z = generate_torus_knot(p, q)
    ax = fig.add_subplot(rows, cols, idx + 1, projection='3d')
    ax.plot(x, y, z, lw=1.5)
    ax.set_title(label, fontsize=10)
    ax.axis('off')
    ax.view_init(elev=90, azim=0)  # Top-down view

# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()