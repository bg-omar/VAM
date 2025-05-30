import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Set up figure
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# ---- Left Side: Swirl Fields ----
ax.text(1, 5.5, "Swirl Flow Field (VAM)", fontsize=12, weight='bold', ha='center')
for y in np.linspace(1, 5, 9):
    x = 1.5
    ax.quiver(x, y, 0, 0.4*np.cos(y), angles='xy', scale_units='xy', scale=1, width=0.005, color='blue')

ax.text(1.5, 0.4, r"$\vec{v}(x) \rightarrow \vec{v}(x) + \nabla\theta(x)$", fontsize=11, color='blue', ha='center')
ax.text(1.5, 0.1, r"Gauge = swirl redundancy", fontsize=10, color='gray', ha='center')

# ---- Middle Divider ----
ax.plot([5, 5], [0.5, 5.5], 'k--')
ax.text(5, 0, "Topological Equivalence", ha='center', fontsize=10, color='gray')

# ---- Right Side: Gauge Fields ----
ax.text(8.5, 5.5, "Gauge Field (SM)", fontsize=12, weight='bold', ha='center')
for y in np.linspace(1, 5, 9):
    x = 8.5
    ax.quiver(x, y, 0.4*np.sin(y), 0, angles='xy', scale_units='xy', scale=1, width=0.005, color='green')

ax.text(8.5, 0.4, r"$A_\mu(x) \rightarrow A_\mu(x) + \partial_\mu \theta(x)$", fontsize=11, color='green', ha='center')
ax.text(8.5, 0.1, r"Gauge = phase freedom", fontsize=10, color='gray', ha='center')

plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()
