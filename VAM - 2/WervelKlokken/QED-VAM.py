import numpy as np
import matplotlib.pyplot as plt

# Parameters
Lk = np.linspace(0, 10, 100)  # Linking number
rc = 1e-15  # core radius in meters
rho = 1e-6  # æther density
Ce = 1e6    # core velocity

# Emergent VAM quantities
mass_vortex = (8 * np.pi * rho * rc**3 * Lk) / Ce  # simplified from Lagrangian
charge_vortex = (Ce**2 * rc / (2e-12)) * np.ones_like(Lk)  # lambda_c ~ 2 pm

# Plot
fig, ax1 = plt.subplots()

ax1.plot(Lk, mass_vortex * 1e27, label='M_vortex (in zg)', color='blue')  # zg = zeptogram
ax1.set_xlabel('Topologische koppeling $L_k$')
ax1.set_ylabel('Emergente massa $M_{\\text{vortex}}$ (zeptogram)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True)

# Add second axis for emergent charge
ax2 = ax1.twinx()
ax2.plot(Lk, charge_vortex / 1.6e-19, '--', label='q_vortex (in e)', color='red')
ax2.set_ylabel('Emergente lading $q_{\\text{vortex}}$ (in $e$)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.title('Vergelijking klassieke $m, q$ versus VAM $M_{\\text{vortex}}, q_{\\text{vortex}}$')
fig.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()


import numpy as np
import matplotlib.pyplot as plt

r = np.linspace(0.1, 2, 500)
omega = 1 / r**2
vortex_mass = 8 * np.pi * (1e-3) * r**3 * omega  # simplified form

plt.plot(r, vortex_mass)
plt.title("Vortex-geïnduceerde massa versus straal")
plt.xlabel("r (straal)")
plt.ylabel("M_vortex (arbitraire eenheden)")
plt.grid(True)
plt.show()
