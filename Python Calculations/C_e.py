import math

# Define the physical constants again manually
h = 6.62607015e-34  # Planck constant in J·s
M_e = 9.1093837015e-31  # Electron mass in kg
R_c = 1.40897017e-15  # Coulomb barrier radius in m

# Compute the right-hand side of the equation
C_e_computed = (3 * h) / (2 * math.pi * M_e * R_c**3)

# Display the result
print(C_e_computed)