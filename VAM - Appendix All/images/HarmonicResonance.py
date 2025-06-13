# Re-import required libraries after environment reset
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, simplify, Eq, Product, Rational
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]

# Define binary-vortex strings and their layout
vortex_sequences = ["1", "11", "111", "212", "21212", "21212212"]
radius_base = 1.0
spacing = 2.5
# Define symbolic variables
r0, n = symbols('r_0 n', positive=True)
seq = symbols('s', cls=symbols)

# Conversion rules:
# 1 → ×1/2
# 2 → ×3/2
def sequence_product(sequence, base_radius=r0):
    """
    Given a sequence like '21212', return the symbolic radius expression.
    """
    radius = base_radius
    for ch in sequence:
        if ch == '1':
            radius *= Rational(1, 2)
        elif ch == '2':
            radius *= Rational(3, 2)
    return simplify(radius)

# Try evaluating a few known sequences
sequences = ["1", "11", "111", "212", "21212", "21212212"]
results = {s: sequence_product(s) for s in sequences}
print(results)

# Set up figure
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_aspect('equal')
ax.axis('off')

# Function to draw concentric circles from a binary string
def draw_sequence(seq, center_x):
    radii = []
    r = radius_base
    for ch in seq:
        if ch == '1':
            r *= 0.5
        elif ch == '2':
            r *= 1.5
        radii.append(r)
    # Draw circles
    for i, r_i in enumerate(radii):
        ax.add_patch(plt.Circle((center_x, 0), r_i, fill=False, lw=2, alpha=0.7))
    ax.text(center_x, -max(radii)*1.1, f"{seq} = {len(seq)}", ha='center', va='top', fontsize=10)

# Draw all sequences
for i, seq in enumerate(vortex_sequences):
    draw_sequence(seq, i * spacing)

ax.set_xlim(-spacing, len(vortex_sequences)*spacing)
ax.set_ylim(-4, 4)
plt.title("Binary Vortex Harmonic Encoding", fontsize=14)
plt.tight_layout()
filename = f"{script_name}4.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()
