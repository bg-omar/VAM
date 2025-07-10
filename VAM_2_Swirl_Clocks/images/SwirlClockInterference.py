import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]

# Swirl Clock Phase Interference Plot
t = np.linspace(0, 10, 1000)
omega1 = 4 * np.pi
omega2 = 5 * np.pi
S1 = np.sin(omega1 * t)
S2 = np.sin(omega2 * t)
interference = S1 + S2

plt.figure(figsize=(10, 6))
plt.plot(t, interference, label=r"$S_1(t) + S_2(t)$ (Interference)", linewidth=2)
plt.plot(t, S1, '--', label=r"$S_1(t)$", alpha=0.5)
plt.plot(t, S2, '--', label=r"$S_2(t)$", alpha=0.5)
plt.title("Swirl Clock Interference Pattern")
plt.xlabel("Time $t$ (s)")
plt.ylabel("Swirl Phase")
plt.legend()
plt.grid(True)
plt.tight_layout()
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution



# Kairos Energy Dynamics Sketch
N = np.linspace(0, 1e-20, 500)
J_div = 1.2e-13
K_event = 3.3e-12
dE_dN = K_event - J_div

energy_change = dE_dN * N

plt.figure(figsize=(10, 6))
plt.plot(N * 1e21, energy_change, label=r"$\frac{dE}{d\mathcal{N}} = \mathbb{K} - \nabla \cdot \vec{J}$", color='darkred', linewidth=2)
plt.axvline(x=0.5, color='gray', linestyle='--', label="Kairos Trigger Point")
plt.title("Energy Growth Triggered by Kairos Moment")
plt.xlabel(r"Universal Time $\mathcal{N}$ ($10^{-21}$ s)")
plt.ylabel("Energy Density Change (W/m³)")
plt.legend()
plt.grid(True)
plt.tight_layout()
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution



# Swirl-modulated gauge field visualization
x = np.linspace(-3, 3, 500)
theta = np.pi * x  # simulate a swirl phase
lambda_ = 1.0
phi = lambda_ * np.sin(theta)
A_x = np.exp(-x**2)
t = 0.5  # fixed time slice
omega = 2 * np.pi
A_xt = A_x * np.cos(omega * t)
F_10 = omega * A_x * np.sin(omega * t) + phi

plt.figure(figsize=(10, 6))
plt.plot(x, F_10, label=r"$F^{1 0}(x)$", color='purple', linewidth=2)
plt.plot(x, phi, '--', label=r"$\phi(\circlearrowleft)$", color='blue')
plt.plot(x, A_xt, '--', label=r"$A_x(t)$", color='green')
plt.title("Swirl-Modulated Gauge Field Tensor Component $F^{1 0}$")
plt.xlabel("Spatial Axis $x$")
plt.ylabel("Field Strength")
plt.legend()
plt.grid(True)
plt.tight_layout()
filename = f"{script_name}3.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()
