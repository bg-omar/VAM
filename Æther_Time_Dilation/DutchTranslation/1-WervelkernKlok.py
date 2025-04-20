import os

import matplotlib.pyplot as plt
import numpy as np

# Plot parameters
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.axis('off')

# Draw the vortex circle
circle = plt.Circle((0, 0), 1, edgecolor='black', facecolor='lightblue', linewidth=2)
ax.add_patch(circle)

# Add a rotating marker (dot)
theta = np.deg2rad(45)  # example angle
x_marker = np.cos(theta)
y_marker = np.sin(theta)
ax.plot(x_marker, y_marker, 'ro', markersize=10, label='Markering (ronddraaiend)')

# Draw rotation arrow
arrow_length = 0.4
ax.annotate('', xy=(0, 1.2), xytext=(0.6, 0),
            arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))
ax.text(0.65, 0.45, r'$\omega$', fontsize=16)

# Add label in center
ax.text(0, 0, 'Wervelkern', ha='center', va='center', fontsize=12, weight='bold')

# Add caption
plt.figtext(0.5, 0.05,
            "Elke $2\pi$ rotatie van de wervelkern komt overeen \nmet één tick van de interne klok.",
            wrap=True, horizontalalignment='center', fontsize=11)

plt.title("Visualisatie van wervelrotatie als interne klok", fontsize=14)
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()