import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Time variables and points
labels = ["Æthēr-Time\n($\\mathcal{N}$)", "Ætheric Now-Point\n($\\nu_0$)", "Chronos-Time\n($\\tau$)",
          "Swirl Clock\n($\\circlearrowleft(t)$)", "Vortex Time\n($T_v$)", "Kairos Moment\n($\\mathbb{K}$)"]
colors = ['#4B8BBE', '#306998', '#88CCCA', '#FFD43B', '#646464', '#E06C75']  # blue to warm gradient

# Set circular positions on a swirl
theta = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
r = np.linspace(0.25, 2.5, len(labels))
x = r * np.cos(theta)
y = r * np.sin(theta)

# Adjust text offsets for fine-tuned positioning
offsets = [(0.2, 0.05), (0, 0.1), (0, 0), (0, 0.05), (0, 0.1), (0, 0.1)]  # (x_offset, y_offset) for each label

# Plot with adjusted text positions
fig, ax = plt.subplots(figsize=(10, 10))
ax.plot(0, 0, 'ko', label="Æther Origin")

for i in range(len(labels)):
    x_text = x[i]*1.1 + offsets[i][0]
    y_text = y[i]*1.1 + offsets[i][1]
    ax.text(x_text, y_text, labels[i], ha='center', va='center', fontsize=13)
    ax.arrow(0, 0, 0.9 * x[i], 0.9 * y[i], head_width=0.05, head_length=0.1, fc=colors[i], ec=colors[i], alpha=0.6)

# Styling
ax.set_aspect('equal')
ax.set_title("Temporal Topology Spiral in the Vortex Æther Model", fontsize=16, pad=20)
ax.axis('off')


plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()
