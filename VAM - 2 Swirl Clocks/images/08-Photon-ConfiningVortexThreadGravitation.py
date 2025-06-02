import math
import os
import re
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Create a cleaner and more visually appealing version of the image
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(-2, 2)
ax.set_ylim(-1.2, 1.2)
ax.axis('off')

# Add vortex knots
knot_radius = 0.2
knot1 = patches.Circle((-1.2, 0), knot_radius, color='black', zorder=3)
knot2 = patches.Circle((1.2, 0), knot_radius, color='black', zorder=3)
ax.add_patch(knot1)
ax.add_patch(knot2)

# Draw smooth sinusoidal vortex thread
x_vals = np.linspace(-1.2, 1.2, 500)
y_vals = 0.3 * np.sin(8 * np.pi * x_vals / 2.4)
ax.plot(x_vals, y_vals, color='royalblue', linewidth=2, label="Confined Photon Wave", zorder=2)

# Add double arrow and label for wave confinement
ax.annotate('', xy=(0.5, 0.3), xytext=(-0.5, 0.3),
            arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
ax.text(0, 0.4, "Confined Standing Wave", fontsize=12, ha='center', color='blue')

# Add force arrows (gravitational-like attraction)
ax.annotate('', xy=(-0.95, 0), xytext=(-1.15, 0),
            arrowprops=dict(arrowstyle='->', color='gray', linewidth=2))
ax.annotate('', xy=(0.95, 0), xytext=(1.15, 0),
            arrowprops=dict(arrowstyle='->', color='gray', linewidth=2))
ax.text(0, -0.4, "Attractive Tension in Ætheric Thread", ha='center', fontsize=11, color='gray')

# Add labels
ax.text(-1.2, -0.35, "Vortex Knot 1", ha='center', fontsize=11)
ax.text(1.2, -0.35, "Vortex Knot 2", ha='center', fontsize=11)

# Title
plt.title("Photon-Confining Vortex Thread with Induced Attraction", fontsize=14, weight='bold')

plt.tight_layout()

import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Create a cleaner and more visually appealing version of the image
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(-2, 2)
ax.set_ylim(-1.2, 1.2)
ax.axis('off')

# Add vortex knots
knot_radius = 0.2
knot1 = patches.Circle((-1.2, 0), knot_radius, color='black', zorder=3)
knot2 = patches.Circle((1.2, 0), knot_radius, color='black', zorder=3)
ax.add_patch(knot1)
ax.add_patch(knot2)

# Draw smooth sinusoidal vortex thread
x_vals = np.linspace(-1.2, 1.2, 500)
y_vals = 0.3 * np.sin(8 * np.pi * x_vals / 2.4)
ax.plot(x_vals, y_vals, color='royalblue', linewidth=2, label="Beperkte fotonengolf", zorder=2)

# Add double arrow and label for wave confinement
ax.annotate('', xy=(0.5, 0.3), xytext=(-0.5, 0.3),
            arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
ax.text(0, 0.4, "Beperkte staande golf", fontsize=12, ha='center', color='blue')

# Add force arrows (gravitational-like attraction)
ax.annotate('', xy=(-0.95, 0), xytext=(-1.15, 0),
            arrowprops=dict(arrowstyle='->', color='gray', linewidth=2))
ax.annotate('', xy=(0.95, 0), xytext=(1.15, 0),
            arrowprops=dict(arrowstyle='->', color='gray', linewidth=2))
ax.text(0, -0.4, "Aantrekkings spanning in ætherische draad", ha='center', fontsize=11, color='gray')

# Add labels
ax.text(-1.2, -0.35, "Wervelknoop 1", ha='center', fontsize=11)
ax.text(1.2, -0.35, "Wervelknoop 2", ha='center', fontsize=11)

# Title
plt.title("Fotonenbeperkend werveldraad met geïnduceerde aantrekkingskracht", fontsize=14, weight='bold')

plt.tight_layout()


import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}_nl.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()