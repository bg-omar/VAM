import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend


# Time variables and points
labels = ["Aithēr-Time\n($\\mathcal{N}$)", "Now-Point\n($\\nu_0$)", "Chronos-Time\n($\\tau$)",
          "Swirl Clock\n($S(t)$)", "Kairos Moment\n($\\mathbb{K}$)", "Vortex Time\n($T_v$)"]

# Set circular positions on a swirl
theta = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
r = np.linspace(0.5, 2.5, len(labels))
x = r * np.cos(theta)
y = r * np.sin(theta)

# Plot
fig, ax = plt.subplots(figsize=(9, 9))
ax.plot(0, 0, 'ko', label="Æther Origin")
for i in range(len(labels)):
    ax.plot(x[i], y[i], 'o', markersize=8)
    ax.text(x[i]*1.1, y[i]*1.1, labels[i], ha='center', va='center', fontsize=10)

# Connecting lines to center
for i in range(len(labels)):
    ax.plot([0, x[i]], [0, y[i]], 'k--', alpha=0.4)

# Styling
ax.set_aspect('equal')
ax.set_title("Temporal Topology of the Vortex Æther Model", fontsize=14)
ax.axis('off')

plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()