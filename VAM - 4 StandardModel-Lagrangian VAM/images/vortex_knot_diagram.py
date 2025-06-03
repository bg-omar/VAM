import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


import math
import os
import re
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt
import numpy as np

# ✅ Get the script filename dynamically
import os
from datetime import datetime



# Parameters for the vortex knot (approximate trefoil)
theta = np.linspace(0, 2 * np.pi, 1000)
r = 1.0 + 0.3 * np.cos(3 * theta)
z = 0.3 * np.sin(3 * theta)
x = r * np.cos(theta)
y = r * np.sin(theta)


theta = np.linspace(0, 2 * np.pi, 1000)
# Parametric equations for a trefoil knot
x = (2 + np.cos(3 * theta)) * np.cos(2 * theta)
y = (2 + np.cos(3 * theta)) * np.sin(2 * theta)
z = np.sin(3 * theta)


# Compute gradient of swirl intensity (normalized)
swirl_intensity = np.sqrt(np.gradient(x)**2 + np.gradient(y)**2 + np.gradient(z)**2)
swirl_intensity_normalized = (swirl_intensity - np.min(swirl_intensity)) / (np.max(swirl_intensity) - np.min(swirl_intensity))

fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})
# Define view angles for each subplot
view_angles = [
    (30, 40),    # Angled view: Elevation, Azimuth
    (90, 180),    # Angled view
    (0, 20),    # Angled view
]
titles = ["Kid 1", "Kid 2", "ManBearPig"]

radii = [(1.5, 1), (1, 1), (0.5, 1)]
rgb = 1

for ax, (elev, azim), title in zip(axes.flatten(), view_angles, titles):
    # Create a colormap plot along the knot
    for i in range(len(x) - 1):
        ax.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=plt.cm.plasma(swirl_intensity_normalized[i]), linewidth=2)

    # Core indicators
    core_index = 500
    vx = -y[core_index] * 0.2
    vy = x[core_index] * 0.2
    vz = 0
    ax.quiver(x[core_index], y[core_index], z[core_index],
              vx, vy, vz, color='crimson', length=0.4,
              normalize=True, label='Tangential Velocity $C_e$')

    ax.plot([x[core_index], 0], [y[core_index], 0], [z[core_index], 0], 'k--', label='Core Radius $r_c$')
    ax.scatter([0], [0], [0], color='black', s=100, label='Knot Center')


    # Set view angle
    ax.view_init(elev=elev, azim=azim)

    # Set limits and labels
    # Plot settings
    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_zlim([-2.5, 2.5])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Trefoil Knot with Swirl Intensity Gradient')
    if rgb ==1:  ax.legend()
    rgb +=1
    ax.set_title(title)







# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()