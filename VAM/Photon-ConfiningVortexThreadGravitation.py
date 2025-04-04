import math
import os
import re
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(-2, 2)
ax.set_ylim(-1.5, 1.5)
ax.axis('off')

# Add particle nodes (vortex knots)
particle1 = patches.Circle((-1.2, 0), 0.2, color='black', label="Vortex Knot 1")
particle2 = patches.Circle((1.2, 0), 0.2, color='black', label="Vortex Knot 2")
ax.add_patch(particle1)
ax.add_patch(particle2)

# Draw vortex thread (helical shaded tube)
for i in range(100):
    x = -1.2 + i * (2.4 / 100)
    y = 0.3 * np.sin(8 * np.pi * x / 2.4)
    ax.plot(x, y, color='blue', linewidth=1.0)

# Add standing wave label
ax.text(0, 0.5, "Confined Standing Photon Wave", fontsize=12, ha='center', color='blue')
ax.annotate('', xy=(0.5, 0.3), xytext=(0.1, 0.3),
            arrowprops=dict(arrowstyle='<->', color='blue'))

# Add gravitational attraction arrows
ax.annotate('', xy=(-0.8, 0), xytext=(-1.0, 0),
            arrowprops=dict(arrowstyle='->', color='gray', linewidth=2))
ax.annotate('', xy=(0.8, 0), xytext=(1.0, 0),
            arrowprops=dict(arrowstyle='->', color='gray', linewidth=2))
ax.text(0, -0.4, "Attractive Force via Thread Tension", ha='center', fontsize=12, color='gray')

# Labels
ax.text(-1.2, -0.4, "Vortex Knot 1", ha='center', fontsize=10)
ax.text(1.2, -0.4, "Vortex Knot 2", ha='center', fontsize=10)

plt.title("Photon-Confining Vortex Thread Inducing Gravitational-Like Attraction", fontsize=14)
plt.tight_layout()
plt.show()
