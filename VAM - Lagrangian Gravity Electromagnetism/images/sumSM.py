import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
# ✅ Get the script filename dynamically and save as pdf
import os

script_name = os.path.splitext(os.path.basename(__file__))[0]
# Save with incrementing filename if file exists, restart count on rerun
base_filename = f"{script_name}.png"
filename = base_filename
count = 1

# Visualize a qualitative breakdown of SM fields as vortex structures in a conceptual diagram
# We'll create a chart showing mapping from SM particles to topological vortex classes

import matplotlib.pyplot as plt

# Define particle types and corresponding VAM structures
particles = [
    "Photon", "Electron", "Proton", "Neutron",
    "Neutrino", "Gluon", "W/Z Bosons", "Higgs Boson"
]

vam_models = [
    "Dipole Vortex Ring (massless, chiral translation)",
    "Trefoil Knot (T(2,3), chiral, spin-1/2)",
    "3-Linked Unknots (Chiral Link, Spin-1/2)",
    "Borromean Rings (Neutral, Meta-stable)",
    "Null Knot (Zero Helicity Twist Ring)",
    "Interlinked Knots (Color Vortices)",
    "Heavy Knots (Massive Chiral Braids)",
    "Swirl Density Peak (Scalar Amplitude Mode)"
]

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("off")
for i, (p, m) in enumerate(zip(particles, vam_models)):
    ax.text(0.01, 1 - i*0.11, f"{p}", fontsize=12, fontweight="bold", verticalalignment='top')
    ax.text(0.25, 1 - i*0.11, f"{m}", fontsize=11, verticalalignment='top')

ax.set_title("Benchmark 10: Standard Model Particles as VAM Topological Structures", fontsize=14)
plt.tight_layout()
while os.path.exists(filename):
    filename = f"{script_name}_{count}.png"
    count += 1
plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()

