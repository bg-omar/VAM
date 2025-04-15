import matplotlib.pyplot as plt
import numpy as np

# Snelheden van 0 tot c
c = 1  # eenheidslichtsnelheid
v_rel = np.linspace(0, c, 500, endpoint=False)
dil = np.sqrt(1 - v_rel**2 / c**2)

# Plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(v_rel, dil, color='darkorange', linewidth=2)
ax.set_title(r"Unified tijdsdilatatie: $\frac{d\tau}{dt} = \sqrt{1 - \frac{|\vec{v}_{\mathrm{rel}}|^2}{c^2}}$", fontsize=14)
ax.set_xlabel(r"$|\vec{v}_{\mathrm{rel}}|$ (relatieve snelheid t.o.v. æther)", fontsize=12)
ax.set_ylabel(r"$\frac{d\tau}{dt}$ (kloksnelheid)", fontsize=12)
ax.grid(True)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.05)

# Annotaties
ax.annotate("Rust (v = 0)", xy=(0, 1), xytext=(0.1, 0.95),
            arrowprops=dict(arrowstyle="->", color='black'), fontsize=11)
ax.annotate("Cirkelbaan (v ≈ √3GM/r)", xy=(0.6, np.sqrt(1 - 0.6**2)),
            xytext=(0.7, 0.65),
            arrowprops=dict(arrowstyle="->", color='black'), fontsize=11)
ax.annotate("Horizon (v = c)", xy=(0.99, 0), xytext=(0.75, 0.2),
            arrowprops=dict(arrowstyle="->", color='black'), fontsize=11)

# Caption
plt.figtext(0.5, 0.01,
            "De kloksnelheid daalt naarmate de relatieve snelheid door æther toeneemt. Bij |v⃗rel| = c stopt de tijd.",
            wrap=True, horizontalalignment='center', fontsize=11)

plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()