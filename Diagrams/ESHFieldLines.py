import numpy as np
import matplotlib.pyplot as plt

# Grid setup
x = np.linspace(-2, 2, 200)
y = np.linspace(-2, 2, 200)
X, Y = np.meshgrid(x, y)

# Position of electrodes
wire_pos = np.array([0.0, 1.0])
foil_y = -1.2

# Compute field from wire (point-like positive electrode)
r_wire = np.sqrt((X - wire_pos[0])**2 + (Y - wire_pos[1])**2)
theta_wire = np.arctan2(Y - wire_pos[1], X - wire_pos[0])
E_wire_mag = 1 / (r_wire + 0.1)**2
E_wire_x = E_wire_mag * np.cos(theta_wire)
E_wire_y = E_wire_mag * np.sin(theta_wire)

# Compute field toward foil (flat negative electrode modeled as uniform field)
E_foil_y = -1.5 / ((Y - foil_y)**2 + 0.5)
E_foil_x = np.zeros_like(E_foil_y)

# Combine field components
E_total_x = E_wire_x + E_foil_x
E_total_y = E_wire_y + E_foil_y

# Plotting
plt.figure(figsize=(8, 10))
plt.streamplot(X, Y, E_total_x, E_total_y, color='blue', density=1.4)
plt.plot(wire_pos[0], wire_pos[1], 'ro', label='Wire Electrode (+)')
plt.axhline(foil_y, color='gray', linestyle='--', linewidth=2, label='Foil Electrode (−)')
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("EHD Lifter Field Lines Including Both Electrodes")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()