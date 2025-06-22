import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Set up the figure
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7.5)
ax.axis('off')

# Labels for the left (GR) and right (VAM) columns
gr_labels = [
    ("Spacetime Metric", r"$ds^2 = g_{\mu\nu} dx^\mu dx^\nu$"),
    ("Ricci Curvature", r"$R_{\mu\nu}$"),
    ("Energy–Stress Tensor", r"$T_{\mu\nu} \approx U_{\mathrm{mass}}$"),
    ("Geodesics", r"$\frac{d^2 x^\mu}{dt^2} = -\mathcal{C}'_\zeta \frac{n g_\beta}{dt^\nu}$")
]

vam_labels = [
    ("Swirl Metric", r"$ds^2 = C_e^2 dT_v^2 - dr^2$"),
    ("Swirl Curvature", r"$\nabla_{\omega\omega_\mu}$"),
    ("Effective Energy Tensor", r"$T^\alpha_{\nu\,:\mathrm{vortex}} \approx U_{\mathrm{vortex}}$"),
    ("Swirl-Advection Paths", r"$\frac{d^2 x^\mu}{d\tau} = \omega_\mu^{\ \alpha} \mu^\nu dx^\mu$")
]

# Draw and label each pair of boxes with arrows
for i, ((gr_title, gr_eq), (vam_title, vam_eq)) in enumerate(zip(gr_labels, vam_labels)):
    y = 6.8 - i * 1.5

    # GR box (left)
    ax.add_patch(patches.FancyBboxPatch((0.5, y - 0.4), 4, 0.8,
                                        boxstyle="round,pad=0.1", edgecolor='black',
                                        facecolor='#b5cef3', lw=1.5))
    ax.text(2.5, y + 0.2, gr_title, ha='center', va='center', fontsize=11, weight='bold')
    ax.text(2.5, y - 0.15, gr_eq, ha='center', va='center', fontsize=11)

    # VAM box (right)
    ax.add_patch(patches.FancyBboxPatch((5.5, y - 0.4), 4, 0.8,
                                        boxstyle="round,pad=0.1", edgecolor='black',
                                        facecolor='#ffd08a', lw=1.5))
    ax.text(7.5, y + 0.2, vam_title, ha='center', va='center', fontsize=11, weight='bold')
    ax.text(7.5, y - 0.15, vam_eq, ha='center', va='center', fontsize=11)

    # Connecting arrows
    ax.annotate('', xy=(5.5, y), xytext=(4.5, y),
                arrowprops=dict(arrowstyle='->', lw=1.5))

# Title at the top
ax.text(5, 7.3, "Correspondence Between General Relativity (GR) and the Vortex Æther Model (VAM)",
        ha='center', va='center', fontsize=14, weight='bold')

plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution



# Fix LaTeX expressions by escaping properly for matplotlib

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis('off')

# Corrected LaTeX-safe box labels
boxes = {
    "GR: Spacetime Curvature": (1, 6),
    r"Metric Tensor $g_{\mu\nu}$": (1, 5),
    "Einstein Field Equations": (1, 4),
    "Time Dilation from Gravity": (1, 3),
    "Light Bending via Geodesics": (1, 2),
    "GR Prediction Domain": (1, 1),

    "VAM: Swirl Field Curvature": (6, 6),
    r"Swirl Energy $U_{\mathrm{vortex}}$": (6, 5),
    "Effective Fluid Field Equations": (6, 4),
    "Time Dilation via Swirl Speed": (6, 3),
    "Light Refraction via Index Gradient": (6, 2),
    "VAM Prediction Domain": (6, 1),
}

for text, (x, y) in boxes.items():
    ax.add_patch(patches.Rectangle((x, y - 0.4), 3, 0.8, fill=True, edgecolor='black', facecolor='lightgray'))
    ax.text(x + 1.5, y, text, ha='center', va='center', fontsize=10)

# Draw arrows between GR and VAM boxes
for y in range(6, 0, -1):
    ax.annotate("", xy=(4, y), xytext=(4.9, y),
                arrowprops=dict(arrowstyle="->", lw=1.5))


filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()

plt.show()
# Remove all unsupported LaTeX commands like \text for matplotlib mathtext compatibility

