from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import os

script_name = os.path.splitext(os.path.basename(__file__))[0]

# Spiral parameters (widened)
theta = np.linspace(0, 3.5 * np.pi, 500)
r = np.linspace(0.4, 1.5, 500)  # widened spiral
z = np.linspace(0, 1.5, 500)
x = r * np.cos(theta)
y = r * np.sin(theta)

# Time layer labels and fractions
time_labels = [
    (1.45 / 1.5, "Kairos Moment ($\\mathbb{K}$)"),  # end of spiral
    (1.2 / 1.5, "Vortex Proper Time ($T_v$)"),
    (0.95 / 1.5, "Swirl Clock ($S^\\circlearrowleft_\\text{(t)}$)"),
    (0.65 / 1.5, "Chronos-Time ($\\tau$)"),
    (0.45 / 1.5, "Now-Point ($\\nu_0$)"),
]

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, color="black", lw=2)

# Draw labels with bounding boxes
for zi_frac, label in time_labels:
    idx = min(int(zi_frac * len(x)), len(x) - 1)
    ax.text(
        x[idx] + 0.3, y[idx], z[idx] + 0.02, label, fontsize=9,
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
    )

# Aithēr-Time label at base
ax.text(
    0.5, 0, 0, "Aithēr-Time ($\\mathcal{N}$)", fontsize=10, color="darkblue",
    bbox=dict(facecolor='white', edgecolor='navy', boxstyle='round,pad=0.3')
)





ax.set_title("Vortex Phase Spiral of Ætheric Time \n $\\mathcal{N} \\rightarrow \\nu_0 \\rightarrow \\tau \\rightarrow S^\\circlearrowleft_\\text{(t)} \\rightarrow T_v \\rightarrow \\mathbb{K}$", fontsize=12)
ax.set_axis_off()
ax.view_init(elev=-155, azim=175)

filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
ax.view_init(elev=80, azim=75)

filename = f"{script_name}v2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Time axis
t = np.linspace(0, 10, 1000)
omega_base = 2 * np.pi / 5

# Base phase evolution
theta = np.sin(omega_base * t) + 0.3 * np.sin(3 * omega_base * t)

# Kairos window parameters
kairos_time = 7
kairos_width = 0.6
kairos_start = kairos_time - kairos_width / 2
kairos_end = kairos_time + kairos_width / 2

# Apply disruption: a bursty oscillation + persistent phase shift
disruption = np.exp(-((t - kairos_time)**2) / (2 * (kairos_width/4)**2))
theta += 0.7 * disruption * np.sin(10 * omega_base * t)
theta += 1.0 * (t > kairos_end)  # Permanent upward phase shift after Kairos

# Create figure
fig, ax = plt.subplots(figsize=(10, 4))

# Plot swirlclock phase
ax.plot(t, theta, label=r'Swirlclock Phase $\theta(t)$', color='black')

# Highlight Kairos window
kairos_patch = patches.Rectangle(
    (kairos_start, -2),
    kairos_width,
    4,
    linewidth=0,
    facecolor='orange',
    alpha=0.3,
    label='Kairos Window'
)
ax.add_patch(kairos_patch)

# Annotate Kairos event from right side to avoid legend
kairos_index = np.abs(t - kairos_time).argmin()
ax.annotate("Topological Transition\n(Kairos Event)",
            xy=(kairos_time, theta[kairos_index]),
            xytext=(kairos_time - 3.0, 1.4),
            arrowprops=dict(arrowstyle="->", color='red'),
            fontsize=11,
            color='red',
            ha='right')

# Axis labels and styling
ax.set_title("Swirlclock Phase Evolution with Kairos Disruption", fontsize=14)
ax.set_xlabel("Æther Time $t$", fontsize=12)
ax.set_ylabel(r"Swirlclock Phase $\theta(t)$", fontsize=12)
ax.grid(True)
ax.set_ylim(-2, 3)
ax.legend()

plt.tight_layout()
filename = f"{script_name}KairosMoment.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()

