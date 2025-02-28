import math
import scipy.constants as const

# Define the physical constants again manually
h = 6.62607015e-34  # Planck constant in J·s
M_e = 9.1093837015e-31  # Electron mass in kg
R_c = 1.40897017e-15  # Coulomb barrier radius in m

R_pr = 1.32140985539e-15  # Proton Compton wavelength (m)
hbar = const.hbar  # Reduced Planck's constant (J·s)
c = const.c  # Speed of light (m/s)
R_infinity = const.Rydberg  # Rydberg constant (1/m)

# Given values
rho_ae = 7.0e-7  # Æther density in kg/m^3
r_c = 1.40897017e-15  # Vortex core radius in meters

# Compute v_v^2
v_v_squared = 4 / (rho_ae * r_c**2)

E_p = R_infinity * hbar * c

# Compute v_v
v_v = math.sqrt(v_v_squared)

# Solve for mu_v using the relationship: mu_v = (4 * E_p) / (9 * C_e^4 * R_c^5)
# We need to express C_e from the Rydberg formula
C_e = ((R_infinity * r_c * c**3 * const.pi) ** (1/3))  # Solve for C_e
print("C_e: ", C_e)
# Compute mu_v using derived formula
mu_v = (4 * E_p) / (9 * C_e**4 * R_c**5)


print("v_v^2:", v_v_squared)
print("v_v:", v_v)

# Print without scientific notation
print("v_v^2:", format(v_v_squared, ',.0f'))
print("v_v:", format(v_v, ',.0f'))

print("mu_v:", mu_v)

# Compute rho_AE using the given formula
rho_AE = (4 * mu_v) / (R_c**2)

# Display the computed density of the Æther
print(rho_AE)

k = (hbar * c) / (4 * const.pi**3  * r_c**2 * C_e * c**3)
print("k:", k)