import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
# Re-import necessary modules after code reset


from mpl_toolkits.mplot3d import Axes3D



# Define colored sub-knots (p, q, label, z-offset, color)
composite_knots = [
    (4, 5, "Hoofdkern T(4,5)", 0.0, 'blue'),
    (2, 7, "Satelliet 1 T(2,7)", 1.5, 'green'),
    (2, 9, "Satelliet 2 T(2,9)", -1.5, 'orange')
]

# Generate torus knot with z offset
def generate_torus_knot(p, q, z_offset=0.0, n_points=1000):
    theta = np.linspace(0, 2 * np.pi, n_points)
    r = 2 + np.cos(q * theta)
    x = r * np.cos(p * theta)
    y = r * np.sin(p * theta)
    z = np.sin(q * theta) + z_offset
    return x, y, z

# Create figure: 2x3 layout
fig = plt.figure(figsize=(18, 12))

# Top row: individual knots (top-down view)
for idx, (p, q, label, z_offset, color) in enumerate(composite_knots):
    x, y, z = generate_torus_knot(p, q, z_offset=0.0)
    ax = fig.add_subplot(2, 3, idx + 1, projection='3d')
    ax.plot(x, y, z, lw=2, color=color)
    ax.set_title(f"{label} (bovenaanzicht)", fontsize=10)
    ax.view_init(elev=90, azim=0)
    ax.axis('off')

# Bottom row: composite views
view_angles = [(90, 0), (30, 45), (0, 0)]
for j, (elev, azim) in enumerate(view_angles):
    ax = fig.add_subplot(2, 3, 3 + j + 1, projection='3d')
    for p, q, label, z_offset, color in composite_knots:
        x, y, z = generate_torus_knot(p, q, z_offset=z_offset)
        ax.plot(x, y, z, lw=2, color=color, label=label)
    ax.set_title(f"Composiet (elev={elev}°, azim={azim}°)", fontsize=10)
    ax.view_init(elev=elev, azim=azim)
    ax.axis('off')
    if j == 2:
        ax.legend(fontsize=8, loc='upper left')

# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()
