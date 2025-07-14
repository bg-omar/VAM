# Re-import required modules after reset
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Experimental data (from glass shield section)
voltage_kV = np.array([
    9, 11, 12.5, 13.5, 14.5, 15, 16, 16.5, 17, 18,
    18.8, 19, 20, 20.1, 20.3, 21, 21.2, 22, 22.2, 27.2, 29
])
voltage = voltage_kV * 1000  # convert to volts

thrust_g = np.array([
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    11, 13, 14, 15, 16, 17, 18, 19, 20, 30, 33
])

# Define a nonlinear function for fitting
def thrust_model(V, a, b, c, V0):
    return a * V**2 / (1 + np.exp(-b * (V - V0))) + c

# Initial guess for parameters
initial_guess = [1e-9, 0.001, 0, 18000]

# Curve fitting
params, covariance = curve_fit(thrust_model, voltage, thrust_g, p0=initial_guess)
a, b, c, V0 = params

# Generate fit line
V_fit = np.linspace(8000, 30000, 300)
T_fit = thrust_model(V_fit, *params)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(voltage, thrust_g, color='blue', label='Measured Thrust Data')
plt.plot(V_fit, T_fit, color='red', label='Fitted VAM Thrust Model')
plt.xlabel('Voltage (V)')
plt.ylabel('Thrust (g)')
plt.title('Thrust vs Voltage – Glass Shielded Lifter')
plt.legend()
plt.grid(True)
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

# Re-import modules after code execution reset


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
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()

print(T_max_g)  # Report the max theoretical thrust limit in grams
