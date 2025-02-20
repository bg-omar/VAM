import math

# Define the physical constants again manually
h = 6.62607015e-34  # Planck constant in J·s
M_e = 9.1093837015e-31  # Electron mass in kg
R_c = 1.40897017e-15  # Coulomb barrier radius in m


# Given values
rho_ae = 7.0e-7  # Æther density in kg/m^3
r_c = 1.40897017e-15  # Vortex core radius in meters

# Compute v_v^2
v_v_squared = 4 / (rho_ae * r_c**2)

# Compute v_v
v_v = math.sqrt(v_v_squared)

print("v_v^2:", v_v_squared)
print("v_v:", v_v)

# Print without scientific notation
print("v_v^2:", format(v_v_squared, ',.0f'))

print("v_v:", format(v_v, ',.0f'))