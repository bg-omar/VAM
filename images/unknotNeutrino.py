# Re-import required libraries after kernel reset
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



# Visualize a null-knot or vortex ring with zero net helicity – candidate for neutrino model
# We'll make a twisted but non-chiral closed loop to represent a "null" knot configuration

def null_knot(t, R=1.0, r=0.25, n_twists=2):
    """
    Null knot: A toroidal structure with symmetric twisting (e.g. figure-8-like loop)
    that has zero net chirality (helicity balanced).
    """
    x = (R + r * np.cos(n_twists * t)) * np.cos(t)
    y = (R + r * np.cos(n_twists * t)) * np.sin(t)
    z = r * np.sin(n_twists * t)
    return x, y, z

# Parameter domain
t_vals = np.linspace(0, 2 * np.pi, 1000)
x_nu, y_nu, z_nu = null_knot(t_vals)

# Plot the neutrino null-knot
fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_nu, y_nu, z_nu, color='purple', linewidth=2)
ax.set_title("Null Knot (Neutrino Candidate)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.grid(True)
plt.tight_layout()
while os.path.exists(filename):
    filename = f"{script_name}_{count}.png"
    count += 1
plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()

