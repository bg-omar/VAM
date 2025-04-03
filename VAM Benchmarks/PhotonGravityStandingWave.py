# Re-import necessary libraries after kernel reset
import numpy as np

# Constants
G_val = 6.67430e-11             # m^3 kg^-1 s^-2
m_U = 3.952e-25                 # kg (approx mass of uranium atom)
r_nm = 1e-9                     # m (distance between atoms)
h_val = 6.62607015e-34          # J·s
c_val = 2.99792458e8            # m/s

# Gravitational force between two uranium atoms
F_grav = G_val * m_U**2 / r_nm**2

# Energy per photon in standing wave between atoms (fundamental mode)
E_photon = h_val * c_val / (2 * r_nm)

# Effective mass per photon via E=mc^2
m_eff_photon = E_photon / c_val**2

# Required number of photons: F_grav = G * (N * m_eff)^2 / r^2
N_required = np.sqrt(F_grav * r_nm**2 / (G_val * m_eff_photon**2))

print(N_required)
