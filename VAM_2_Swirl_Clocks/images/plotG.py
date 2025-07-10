import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Constants
F_max = 29.053507  # N
r_c = 1.40897017e-15  # m
r = np.linspace(0, 10 * r_c, 500)

# Ce values to simulate
Ce_values = [1e5, 5e5, 1e6]  # m/s

# Prepare plots
plt.figure(figsize=(10, 5))
for Ce in Ce_values:
    Phi = (Ce**3 / (2 * F_max * r_c)) * r * np.exp(-r / r_c)
    plt.plot(r * 1e15, Phi, label=f"Cₑ = {Ce:.1e} m/s")

plt.title("Gravitational Potential Φ(r) for Various Cₑ")
plt.xlabel("r (fm)")
plt.ylabel("Φ(r)")
plt.legend()
plt.grid(True)
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution



# Acceleration Δg(r)
plt.figure(figsize=(10, 5))
for Ce in Ce_values:
    A = Ce**3 / (2 * F_max * r_c**2)
    delta_g = -A * np.exp(-r / r_c) * (1 - r / r_c)
    plt.plot(r * 1e15, delta_g, label=f"Cₑ = {Ce:.1e} m/s")

plt.title("Gravitational Acceleration Δg(r) for Various Cₑ")
plt.xlabel("r (fm)")
plt.ylabel("Δg(r) [m/s²]")
plt.legend()
plt.grid(True)
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()
