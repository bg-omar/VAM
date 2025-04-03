# Re-import modules after code execution reset
import matplotlib.pyplot as plt
import numpy as np

# Constants
rho_ae = 7.0e-7  # kg/m^3, Æther density
C_e = 1.09384563e6  # m/s, vortex core tangential velocity
r = 1e-3  # m, radius of vortex shell (1 mm)
area = np.pi * r**2  # m^2
T_max = rho_ae * area * C_e**2  # maximum thrust in Newtons

# Convert to grams (1 N ≈ 101.97 g)
T_max_g = T_max * 101.97

# Experimental voltage data (glass shielded)
voltage_glass_kV = np.array([
    9, 11, 12.5, 13.5, 14.5, 15, 16, 16.5, 17, 18,
    18.8, 19, 20, 20.1, 20.3, 21, 21.2, 22, 22.2, 27.2, 29
])
voltage_glass = voltage_glass_kV * 1000  # V
thrust_glass_g = np.array([
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    11, 13, 14, 15, 16, 17, 18, 19, 20, 30, 33
])

# VAM sigmoid thrust model
def vam_thrust(V, T_max_g, lam):
    return T_max_g * (1 - np.exp(-lam * V**2))

# Choose λ to fit shape (empirically tuned)
lambda_vam = 2e-10

# Generate VAM curve
V_sim = np.linspace(8000, 30000, 500)
T_sim = vam_thrust(V_sim, T_max_g, lambda_vam)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(voltage_glass, thrust_glass_g, color='blue', label='Experimental Data (Glass Shield)')
plt.plot(V_sim, T_sim, color='purple', linestyle='--', label='VAM Prediction')
plt.xlabel('Voltage (V)')
plt.ylabel('Thrust (g)')
plt.title('Thrust vs Voltage – VAM Model with Æther Constants')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print(T_max_g)  # Report the max theoretical thrust limit in grams