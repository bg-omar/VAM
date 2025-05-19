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


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# Parameters for the trefoil knot T(2,3)
theta = np.linspace(0, 2 * np.pi, 1000)
x = (2 + np.cos(3 * theta)) * np.cos(2 * theta)
y = (2 + np.cos(3 * theta)) * np.sin(2 * theta)
z = np.sin(3 * theta)

# Compute swirl intensity (velocity gradient magnitude)
swirl_intensity = np.sqrt(np.gradient(x)**2 + np.gradient(y)**2 + np.gradient(z)**2)
swirl_norm = (swirl_intensity - np.min(swirl_intensity)) / (np.max(swirl_intensity) - np.min(swirl_intensity))

# Set up three view angles
fig, axes = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={'projection': '3d'})
view_angles = [(30, 60), (90, 180), (0, 20)]
titles = ["Perspectief", "Bovenaanzicht", "Zijaanzicht"]

for ax, (elev, azim), title in zip(axes, view_angles, titles):
    for i in range(len(x) - 1):
        ax.plot(x[i:i+2], y[i:i+2], z[i:i+2],
                color=plt.cm.plasma(swirl_norm[i]), linewidth=2)

    # Tangentiële snelheid vector bij knoopkern
    i_core = 500
    vx = -y[i_core] * 0.2
    vy = x[i_core] * 0.2
    vz = 0
    ax.quiver(x[i_core], y[i_core], z[i_core],
              vx, vy, vz, color='crimson', length=0.5,
              normalize=True, label='Tangentiële snelheid $C_e$')

    # Lijn naar centrum en kernmarkering
    ax.plot([x[i_core], 0], [y[i_core], 0], [z[i_core], 0], 'k--', label='Kernstraal $r_c$')
    ax.scatter([0], [0], [0], color='black', s=50, label='Knoopcentrum')

    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_zlim([-2.5, 2.5])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(title)
    ax.legend(loc='upper right')



# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()