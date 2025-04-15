import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
titles = ['(1) Deeltje in rust in æther', '(2) Deeltje in beweging met snelheid v']
omega_labels = [r'$\omega_0$', r'$\omega_{\mathrm{obs}} < \omega_0$']

for i, ax in enumerate(axes):
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(titles[i], fontsize=12)

    # Draw vortex circle
    circle = plt.Circle((0, 0), 1, edgecolor='black', facecolor='lightblue', linewidth=2)
    ax.add_patch(circle)

    # Rotating marker
    theta = np.deg2rad(45)
    x_marker = np.cos(theta)
    y_marker = np.sin(theta)
    ax.plot(x_marker, y_marker, 'ro', markersize=10)

    # Rotation arrow (adjust length in moving case)
    if i == 0:
        ax.annotate('', xy=(0.7, 0), xytext=(0, 0.9),
                    arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))
    else:
        ax.annotate('', xy=(0.5, 0), xytext=(0, 0.6),
                    arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))

    ax.text(0.75 if i == 0 else 0.55, 0.05, omega_labels[i], fontsize=14)

    # Æther flow in moving case
    if i == 1:
        for y in np.linspace(-1.5, 1.5, 5):
            ax.arrow(-2, y, 4, 0, head_width=0.1, head_length=0.2,
                     fc='deepskyblue', ec='deepskyblue', linewidth=1.5)
        ax.text(0, -1.8, r'Ætherstroom $\vec{v}$', fontsize=12, ha='center', color='deepskyblue')

# Caption
plt.figtext(0.5, 0.01,
            "Beweging door æther verlaagt de waargenomen hoeksnelheid $\\omega_{\\mathrm{obs}}$.",
            wrap=True, horizontalalignment='center', fontsize=11)

plt.suptitle("Effect van ætherbeweging op rotatie van wervelkern", fontsize=14)
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()