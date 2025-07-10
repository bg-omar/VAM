import numpy as np
import matplotlib.pyplot as plt
from ace_tools_open import display_dataframe_to_user
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

import numpy as np
import matplotlib.pyplot as plt

# --- Constants ---
G = 6.67430e-11                      # Gravitational constant (unused here)
M = 1.0e11 * 1.989e30                # Mass of galaxy in kg (for MOND comparison)
kpc_to_m = 3.086e19
r = np.linspace(0.1, 50, 500) * kpc_to_m  # Radius from 0.1 to 50 kpc in meters
r_c = 5 * kpc_to_m                  # Coherence radius
C_core = 100e3                      # Core swirl contribution in m/s
C_tail = 100e3                      # Tail swirl saturation in m/s

# --- VAM Final Model ---
v_core = C_core / np.sqrt(1 + (r_c / r)**2)
v_tail = C_tail * (1 - np.exp(-r / r_c))
v_vam_final = v_core + v_tail

# --- MOND Model (for comparison only) ---
R_d = 15 * kpc_to_m
M_r = np.where(r < R_d, M * r / R_d, M)
a0 = 1.2e-10  # MOND critical acceleration
a_newton = G * M_r / r**2
a_mond = np.sqrt(a_newton * a0)
v_mond = np.sqrt(a_mond * r)

# --- Observational Data ---
r_data = np.array([2, 4, 6, 8, 10, 15, 20, 25, 30, 35, 40])  # kpc
v_data = np.array([100, 130, 150, 170, 180, 190, 195, 200, 200, 200, 200])  # km/s

# --- Plot ---
plt.figure(figsize=(8, 6))
plt.plot(r / kpc_to_m, v_vam_final / 1e3, label="VAM (core + swirl blend)", linewidth=2, color='darkgreen')
plt.plot(r / kpc_to_m, v_mond / 1e3, label="MOND", linestyle='-.', color='black')
plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
plt.xlabel("Radius (kpc)")
plt.ylabel("Orbital Velocity (km/s)")
plt.title("Refined VAM Model: Swirl Core + Saturated Tail")
plt.legend()
plt.grid(True)
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()


# # Constants and setup
# G = 6.67430e-11  # gravitational constant
# M = 1.0e11 * 1.989e30  # mass of galaxy (solar mass to kg)
# omega_bg = 0.12  # background swirl frequency in s^-1
# r = np.linspace(0.1, 50, 500) * 3.086e19  # radius in meters (0.1 to 50 kpc)
#
# # Newtonian velocity profile
# v_newton = np.sqrt(G * M / r)
#
# # VAM velocity profile
# v_vam = np.sqrt(G * M / r + (r**2) * omega_bg**2)

# # MOND velocity profile (simplified)
# a0 = 1.2e-10  # MOND acceleration in m/s^2
# a_newton = G * M / r**2
# a_mond = np.sqrt(a_newton * a0)
# v_mond = np.sqrt(a_mond * r)
#
# # Plotting
# plt.figure(figsize=(8, 6))
# plt.plot(r / 3.086e19, v_newton / 1e3, label="Newtonian", linestyle='--')
# plt.plot(r / 3.086e19, v_vam / 1e3, label="VAM", linewidth=2)
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.')
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("Galaxy Rotation Curves: VAM vs MOND vs Newton")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
#
# # Re-import necessary libraries after code state reset
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Constants and setup
# G = 6.67430e-11  # gravitational constant
# M = 1.0e11 * 1.989e30  # mass of galaxy (solar mass to kg)
# omega_bg = 0.12  # background swirl frequency in s^-1
# r = np.linspace(0.1, 50, 500) * 3.086e19  # radius in meters (0.1 to 50 kpc)
#
# # Newtonian velocity profile
# v_newton = np.sqrt(G * M / r)
#
# # VAM velocity profile
# v_vam = np.sqrt(G * M / r + (r**2) * omega_bg**2)
#
# # MOND velocity profile (simplified)
# a0 = 1.2e-10  # MOND acceleration in m/s^2
# a_newton = G * M / r**2
# a_mond = np.sqrt(a_newton * a0)
# v_mond = np.sqrt(a_mond * r)
#
# # Sample real data for overlay (e.g. from NGC 3198 or generic)
# r_data = np.array([2, 4, 6, 8, 10, 15, 20, 25, 30, 35, 40])  # in kpc
# v_data = np.array([100, 130, 150, 170, 180, 190, 195, 200, 200, 200, 200])  # in km/s
#
# # Plotting
# plt.figure(figsize=(8, 6))
# plt.plot(r / 3.086e19, v_newton / 1e3, label="Newtonian", linestyle='--')
# plt.plot(r / 3.086e19, v_vam / 1e3, label="VAM", linewidth=2)
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.')
# plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("Galaxy Rotation Curves with Observational Data")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
#
#
# # Define a decaying swirl term: ω(r) = ω0 * exp(-r / rc)
# omega_0 = 0.12  # swirl strength at center
# rc_kpc = 10     # coherence radius in kiloparsecs
# rc_m = rc_kpc * 3.086e19  # convert to meters
#
# # Updated VAM velocity profile with decaying swirl
# omega_r = omega_0 * np.exp(-r / rc_m)
# v_vam_decay = np.sqrt(G * M / r + (r**2) * omega_r**2)
#
# # Plot with decay
# plt.figure(figsize=(8, 6))
# plt.plot(r / 3.086e19, v_newton / 1e3, label="Newtonian", linestyle='--')
# plt.plot(r / 3.086e19, v_vam_decay / 1e3, label="VAM (decaying swirl)", linewidth=2, color='purple')
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.')
# plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("Corrected VAM Rotation Curve with Decaying Swirl")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
#
#
# # Recalculate Newtonian curve with realistic disk-limited mass profile
#
# # Disk scale radius
# R_d_kpc = 15  # disk radius in kiloparsecs
# R_d = R_d_kpc * 3.086e19  # convert to meters
#
# # Create M(r): linear increase up to R_d, constant afterward
# M_r = np.where(r < R_d, M * r / R_d, M)
#
# # Updated Newtonian velocity profile
# v_newton_realistic = np.sqrt(G * M_r / r)
#
# # Plot updated with corrected Newtonian curve
# plt.figure(figsize=(8, 6))
# plt.plot(r / 3.086e19, v_newton_realistic / 1e3, label="Newtonian (realistic)", linestyle='--', color='blue')
# plt.plot(r / 3.086e19, v_vam_decay / 1e3, label="VAM (decaying swirl)", linewidth=2, color='purple')
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.', color='black')
# plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("Galaxy Rotation Curves with Realistic Newtonian Dropoff")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
#
#
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Recalculate constants and radius array
# G = 6.67430e-11
# M = 1.0e11 * 1.989e30  # solar mass to kg
# C_e = 1.094e6  # vortex core tangential velocity, in m/s
# r = np.linspace(0.1, 50, 500) * 3.086e19  # radius from 0.1 to 50 kpc
# r_c = 5 * 3.086e19  # coherence radius in meters
#
# # Define realistic mass profile (same as before)
# R_d = 15 * 3.086e19
# M_r = np.where(r < R_d, M * r / R_d, M)
# v_newton_realistic = np.sqrt(G * M_r / r)
#
# # VAM model using saturating swirl term
# v_swirl_squared = C_e**2 / (1 + (r / r_c)**2)
# v_vam_corrected = np.sqrt(v_newton_realistic**2 + v_swirl_squared)
#
# # MOND profile (unchanged)
# a0 = 1.2e-10
# a_newton = G * M_r / r**2
# a_mond = np.sqrt(a_newton * a0)
# v_mond = np.sqrt(a_mond * r)
#
# # Observed data
# r_data = np.array([2, 4, 6, 8, 10, 15, 20, 25, 30, 35, 40])
# v_data = np.array([100, 130, 150, 170, 180, 190, 195, 200, 200, 200, 200])
#
# # Plot updated rotation curves
# plt.figure(figsize=(8, 6))
# plt.plot(r / 3.086e19, v_newton_realistic / 1e3, label="Newtonian (realistic)", linestyle='--', color='blue')
# plt.plot(r / 3.086e19, v_vam_corrected / 1e3, label="VAM (bounded swirl)", linewidth=2, color='green')
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.', color='black')
# plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("VAM Rotation Curve with Bounded Swirl Energy")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
# # Recompute VAM with a realistic effective swirl velocity C_eff = 200 km/s
# C_eff = 200e3  # 200 km/s in m/s
#
# # Updated VAM profile with corrected swirl magnitude
# v_swirl_corrected = C_eff**2 / (1 + (r / r_c)**2)
# v_vam_realistic = np.sqrt(v_newton_realistic**2 + v_swirl_corrected)
#
# # Plot the corrected VAM against observations
# plt.figure(figsize=(8, 6))
# plt.plot(r / 3.086e19, v_newton_realistic / 1e3, label="Newtonian (realistic)", linestyle='--', color='blue')
# plt.plot(r / 3.086e19, v_vam_realistic / 1e3, label="VAM (realistic swirl)", linewidth=2, color='green')
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.', color='black')
# plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("Final VAM Fit Using Realistic Swirl Velocity")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
# # Re-import required libraries after code execution state reset
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Re-define constants
# G = 6.67430e-11          # gravitational constant (m^3 kg^-1 s^-2)
# M = 1e11 * 1.9885e30     # galaxy mass in kg (1e11 solar masses)
# C_e = 1.094e6            # vortex core tangential velocity (m/s)
# r_c = 1.409e-15          # vortex core radius (m)
# omega_bg = 0.12          # background swirl frequency (s^-1)
#
# # Define radial distance array in meters (from 1 kpc to 50 kpc)
# r = np.linspace(1e3, 50e3, 500) * 3.086e16  # convert from kpc to meters
#
# # Newtonian rotation velocity
# v_newton_realistic = np.sqrt(G * M / r)
#
# # MOND characteristic acceleration and velocity
# a0 = 1.2e-10
# a_N = G * M / r**2
# a_MOND = np.sqrt(a_N * a0)
# v_mond = np.sqrt(a_MOND * r)
#
# # VAM swirl contribution with realistic terminal swirl velocity
# C_eff = 200e3
# v_swirl_corrected = C_eff**2 / (1 + (r / r_c)**2)
# v_vam_realistic = np.sqrt(v_newton_realistic**2 + v_swirl_corrected)
#
# # VAM derived: v = r * omega_bg
# v_flat_derived = r * omega_bg
#
# # Observed data points (radius in kpc, velocity in km/s)
# r_data = np.array([5, 10, 15, 20, 25, 30, 35, 40])  # kpc
# v_data = np.array([180, 195, 200, 210, 205, 200, 198, 195])  # km/s
#
# # Plot all
# plt.figure(figsize=(8, 6))
# plt.plot(r / 3.086e19, v_newton_realistic / 1e3, label="Newtonian", linestyle='--', color='blue')
# plt.plot(r / 3.086e19, v_vam_realistic / 1e3, label="VAM (realistic swirl)", linewidth=2, color='green')
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.', color='black')
# plt.plot(r / 3.086e19, v_flat_derived / 1e3, label="VAM (derived: $r\\omega_{bg}$)", linestyle=':', linewidth=2, color='orange')
# plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
#
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("Comparison of Galaxy Rotation Models")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
# # Re-import packages and constants after reset (if needed)
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Constants
# G = 6.67430e-11         # gravitational constant (m^3 kg^-1 s^-2)
# M = 1e11 * 1.9885e30    # galaxy mass in kg
# C_e = 1.094e6           # vortex core tangential velocity (m/s)
# omega_bg = 0.12         # background swirl frequency (s^-1)
#
# # Radius from 1 to 50 kpc in meters
# r = np.linspace(0.1, 50, 500) * 3.086e19  # radius from 0.1 to 50 kpc
# # Newtonian profile
# v_newton_realistic = np.sqrt(G * M / r)
#
# # MOND profile
# a0 = 1.2e-10
# a_N = G * M / r**2
# a_MOND = np.sqrt(a_N * a0)
# v_mond = np.sqrt(a_MOND * r)
#
# # VAM (realistic swirl) profile using a bounded term (C_eff = 200 km/s)
# C_eff = 200e3
# r_c = 1.409e-15  # vortex core radius (for consistency, though not used directly here)
# v_swirl_corrected = C_eff**2 / (1 + (r / r_c)**2)
# v_vam_realistic = np.sqrt(v_newton_realistic**2 + v_swirl_corrected)
#
# # Now compute the three derived VAM swirl-based velocities:
#
# # 1. From v_flat = (G M C_e^2 ω_bg^4 / r^4)^{1/4}
# v_vam_1 = (G * M * C_e**2 * omega_bg**4 / r**4)**(1/4)
#
# # 2. From v_flat = sqrt(G M / r + r^2 * omega_bg^2)
# v_vam_2 = np.sqrt(G * M / r + r**2 * omega_bg**2)
#
# # 3. From v_flat = r * omega_bg (direct proportional)
# v_vam_3 = r * omega_bg
#
# # Observed data points
# r_data = np.array([5, 10, 15, 20, 25, 30, 35, 40])  # kpc
# v_data = np.array([180, 195, 200, 210, 205, 200, 198, 195])  # km/s
#
# # Plot
# plt.figure(figsize=(9, 6))
# plt.plot(r / 3.086e19, v_newton_realistic / 1e3, label="Newtonian", linestyle='--', color='blue')
# plt.plot(r / 3.086e19, v_vam_realistic / 1e3, label="VAM (bounded swirl)", linewidth=2, color='green')
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.', color='black')
# plt.plot(r / 3.086e19, v_vam_1 / 1e3, label=r"VAM $(GM C_e^2 \omega^4 / r^4)^{1/4}$", linestyle=':', color='orange')
# plt.plot(r / 3.086e19, v_vam_2 / 1e3, label=r"VAM $\sqrt{GM/r + r^2 \omega^2}$", linestyle='--', color='purple')
# plt.plot(r / 3.086e19, v_vam_3 / 1e3, label=r"VAM $r \omega$", linestyle='dashdot', color='brown')
# plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
#
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("Galaxy Rotation Models from First-Principles VAM")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
# # Re-plot without the sqrt(GM/r + r^2 ω^2) curve (v_vam_2)
#
# plt.figure(figsize=(9, 6))
# plt.plot(r / 3.086e19, v_newton_realistic / 1e3, label="Newtonian", linestyle='--', color='blue')
# plt.plot(r / 3.086e19, v_vam_realistic / 1e3, label="VAM (bounded swirl)", linewidth=2, color='green')
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.', color='black')
# plt.plot(r / 3.086e19, v_vam_1 / 1e3, label=r"VAM $(GM C_e^2 \omega^4 / r^4)^{1/4}$", linestyle=':', color='orange')
# plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
#
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("Galaxy Rotation Models from First-Principles VAM")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
#
# # Re-plot with only Newtonian, MOND, derived VAM formula, and observed data (no bounded swirl)
#
# plt.figure(figsize=(9, 6))
# plt.plot(r / 3.086e19, v_newton_realistic / 1e3, label="Newtonian", linestyle='--', color='blue')
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.', color='black')
# plt.plot(r / 3.086e19, v_vam_1 / 1e3, label=r"VAM $(GM C_e^2 \omega^4 / r^4)^{1/4}$", linestyle=':', color='orange')
# plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
#
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("Rotation Curves from Derived VAM vs MOND")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
# v_boxed = np.full_like(r, 200e3)  # in m/s
#
#
# velocity_profiles = [
#     (v_newton / 1e3, "Newtonian", 0),
#     (v_mond / 1e3, "MOND", 1),
#     (v_vam_1 / 1e3, "VAM (derived)", 2),
#     (v_boxed / 1e3, "Boxed Flat", 3)
# ]
#
#
#
# # Recompute VAM with a realistic effective swirl velocity C_eff = 200 km/s
# C_eff = 200e3  # 200 km/s in m/s
#
# # Updated VAM profile with corrected swirl magnitude
# v_swirl_corrected = C_eff**2 / (1 + (r / r_c)**2)
# v_vam_realistic = np.sqrt(v_newton_realistic**2 + v_swirl_corrected)
#
# # Plot the corrected VAM against observations
# plt.figure(figsize=(8, 6))
# plt.plot(r / 3.086e19, v_newton_realistic / 1e3, label="Newtonian (realistic)", linestyle='--', color='blue')
# plt.plot(r / 3.086e19, v_vam_realistic / 1e3, label="VAM (realistic swirl)", linewidth=2, color='green')
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.', color='black')
# plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("Final VAM Fit Using Realistic Swirl Velocity")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
#
# # Observed data (in kpc and km/s)
# r_data_kpc = np.array([5, 10, 15, 20, 25, 30, 35, 40])  # kpc
# v_data_kms = np.array([180, 195, 200, 210, 205, 200, 198, 195])  # km/s
#
# # Convert radius to meters and velocity to km/s
# r_data_m = r_data_kpc * 3.086e19
# v_data = v_data_kms  # already in km/s
#
# fig = plt.figure(figsize=(10, 6))
# ax = fig.add_subplot(111, projection='3d')
#
# # Plot theoretical profiles
# for profile, label, z_offset in velocity_profiles:
#     ax.plot(r / 3.086e19, profile, zs=z_offset, zdir='z', label=label)
#
# # Add observed data at the bottom z=−1
# ax.scatter(r_data_kpc, v_data, zs=-1, zdir='z', label="Observed", color='black', s=50)
#
# # Labels and visual limits
# ax.set_xlabel("Radius (kpc)")
# ax.set_ylabel("Velocity (km/s)")
# ax.set_zlabel("Model Index")
# ax.set_zticks([-1] + list(range(len(velocity_profiles))))
# ax.set_zticklabels(["Observed"] + [label for _, label, _ in velocity_profiles])
# ax.set_xlim(0, 50)
# ax.set_ylim(150, 250)
# ax.set_zlim(-1.5, len(velocity_profiles) - 0.5)
# ax.set_title("3D Comparison of Galaxy Rotation Models with Observations")
#
# plt.tight_layout()
# plt.legend()
#
#
# # Constants
# G = 6.67430e-11         # m^3 kg^-1 s^-2
# M = 1e11 * 1.9885e30    # kg
# C_e = 1.094e6           # m/s
# a0 = 1.2e-10            # MOND critical acceleration
# omega_bg = 0.12         # rad/s
# r = np.linspace(1e3, 50e3, 500) * 3.086e16  # radius in meters
#
# # Newtonian acceleration and velocity
# a_N = G * M / r**2
# v_newton = np.sqrt(G * M / r)
#
# # MOND velocity — full interpolating function μ(x) = a / (a + a0)
# mu = a_N / (a_N + a0)
# a_mond_interp = a_N / mu
# v_mond_interp = np.sqrt(a_mond_interp * r)
#
# # MOND asymptotic (deep-MOND) flat velocity
# v_mond_flat = np.full_like(r, (G * M * a0)**0.25)
#
# # VAM derived from (GM C_e^2 ω^4 / r^4)^{1/4}
# v_vam_1 = (G * M * C_e**2 * omega_bg**4 / r**4)**0.25
#
# # Observed data
# r_data_kpc = np.array([5, 10, 15, 20, 25, 30, 35, 40])  # kpc
# v_data_kms = np.array([180, 195, 200, 210, 205, 200, 198, 195])  # km/s
#
# # 3D Plot
# fig = plt.figure(figsize=(10, 6))
# ax = fig.add_subplot(111, projection='3d')
#
# # Theoretical models
# ax.plot(r / 3.086e19, v_newton / 1e3, zs=0, zdir='z', label="Newtonian", color='blue')
# ax.plot(r / 3.086e19, v_mond_interp / 1e3, zs=1, zdir='z', label="MOND (interpolated)", color='black')
# ax.plot(r / 3.086e19, v_mond_flat / 1e3, zs=2, zdir='z', label="MOND (flat limit)", color='gray')
# ax.plot(r / 3.086e19, v_vam_1 / 1e3, zs=3, zdir='z', label="VAM (derived)", color='orange')
#
# # Observational data
# ax.scatter(r_data_kpc, v_data_kms, zs=-1, zdir='z', label="Observed", color='red', s=50)
#
# # Axis settings
# ax.set_xlabel("Radius (kpc)")
# ax.set_ylabel("Velocity (km/s)")
# ax.set_zlabel("Model Index")
# ax.set_zticks([-1, 0, 1, 2, 3])
# ax.set_zticklabels(["Observed", "Newtonian", "MOND\ninterp", "MOND\nflat", "VAM"])
# ax.set_xlim(0, 50)
# ax.set_ylim(150, 250)
# ax.set_zlim(-1.5, 3.5)
# ax.set_title("3D Comparison of Galaxy Rotation Models with Interpolated and Flat MOND")
#
# plt.tight_layout()
# plt.legend()
#
#
#
#
# # Final unified VAM formula: v(r) = sqrt(GM/r + r^2 * omega_bg^2)
# v_vam_unified = np.sqrt(G * M / r + (r**2) * omega_bg**2)
#
# # 3D plot against MOND (both) and observations only
# fig = plt.figure(figsize=(10, 6))
# ax = fig.add_subplot(111, projection='3d')
#
# # Plot models
# ax.plot(r / 3.086e19, v_mond_interp / 1e3, zs=0, zdir='z', label="MOND (interpolated)", color='black')
# ax.plot(r / 3.086e19, v_mond_flat / 1e3, zs=1, zdir='z', label="MOND (flat limit)", color='gray')
# ax.plot(r / 3.086e19, v_vam_unified / 1e3, zs=2, zdir='z', label="VAM Unified", color='orange')
#
# # Observed data
# ax.scatter(r_data_kpc, v_data_kms, zs=-1, zdir='z', label="Observed", color='red', s=50)
#
# # Axes settings
# ax.set_xlabel("Radius (kpc)")
# ax.set_ylabel("Velocity (km/s)")
# ax.set_zlabel("Model Index")
# ax.set_zticks([-1, 0, 1, 2])
# ax.set_zticklabels(["Observed", "MOND\ninterp", "MOND\nflat", "VAM"])
# ax.set_xlim(0, 50)
# ax.set_ylim(150, 250)
# ax.set_zlim(-1.5, 2.5)
# ax.set_title("Unified VAM vs MOND and Observed Galaxy Rotation")
#
# plt.tight_layout()
# plt.legend()
#
#
# # Updated omega_bg to match realistic flat rotation curve (~200 km/s at 30 kpc)
# omega_bg_fixed = 2.2e-16  # rad/s
#
# # Recalculate unified VAM velocity with corrected swirl angular velocity
# v_vam_unified_fixed = np.sqrt(G * M / r + (r**2) * omega_bg_fixed**2)
#
# # 3D plot: corrected VAM vs. MOND and observations
# fig = plt.figure(figsize=(10, 6))
# ax = fig.add_subplot(111, projection='3d')
#
# # Plot models
# ax.plot(r / 3.086e19, v_mond_interp / 1e3, zs=0, zdir='z', label="MOND (interpolated)", color='black')
# ax.plot(r / 3.086e19, v_mond_flat / 1e3, zs=1, zdir='z', label="MOND (flat limit)", color='gray')
# ax.plot(r / 3.086e19, v_vam_unified_fixed / 1e3, zs=2, zdir='z', label="VAM Unified (fixed)", color='orange')
#
# # Observational data
# ax.scatter(r_data_kpc, v_data_kms, zs=-1, zdir='z', label="Observed", color='red', s=50)
#
# # Axis settings
# ax.set_xlabel("Radius (kpc)")
# ax.set_ylabel("Velocity (km/s)")
# ax.set_zlabel("Model Index")
# ax.set_zticks([-1, 0, 1, 2])
# ax.set_zticklabels(["Observed", "MOND\ninterp", "MOND\nflat", "VAM"])
# ax.set_xlim(0, 50)
# ax.set_ylim(150, 250)
# ax.set_zlim(-1.5, 2.5)
# ax.set_title("VAM Unified (Fixed) vs. MOND and Observed Rotation Curves")
#
# plt.tight_layout()
# plt.legend()
#
#
#
# # Define swirl-modified unified VAM model
# r_kpc = r / 3.086e19  # radius in kpc for readability
# r_c = 5  # kpc
# r_s = 10 * 3.086e19  # swirl saturation radius in meters
# C_s = 200e3  # saturation swirl velocity in m/s
#
# # Option A: softened swirl term
# v_vam_soft = np.sqrt(G * M / r + (r**2 * omega_bg_fixed**2) / (1 + (r_kpc / r_c)**2))
#
# # Option B: saturating swirl term
# v_vam_saturate = np.sqrt(G * M / r + C_s**2 * (1 - np.exp(-r / r_s))**2)
#
# # 3D plot: both improved VAM forms vs MOND and observations
# fig = plt.figure(figsize=(10, 6))
# ax = fig.add_subplot(111, projection='3d')
#
# # Plot models
# ax.plot(r_kpc, v_mond_interp / 1e3, zs=0, zdir='z', label="MOND (interpolated)", color='black')
# ax.plot(r_kpc, v_mond_flat / 1e3, zs=1, zdir='z', label="MOND (flat limit)", color='gray')
# ax.plot(r_kpc, v_vam_soft / 1e3, zs=2, zdir='z', label="VAM (softened)", color='orange')
# ax.plot(r_kpc, v_vam_saturate / 1e3, zs=3, zdir='z', label="VAM (saturating)", color='green')
#
# # Observed data
# ax.scatter(r_data_kpc, v_data_kms, zs=-1, zdir='z', label="Observed", color='red', s=50)
#
# # Axis settings
# ax.set_xlabel("Radius (kpc)")
# ax.set_ylabel("Velocity (km/s)")
# ax.set_zlabel("Model Index")
# ax.set_zticks([-1, 0, 1, 2, 3])
# ax.set_zticklabels(["Observed", "MOND\ninterp", "MOND\nflat", "VAM\nsoft", "VAM\nsat"])
# ax.set_xlim(0, 50)
# ax.set_ylim(150, 250)
# ax.set_zlim(-1.5, 3.5)
# ax.set_title("Improved VAM vs. MOND and Observed Rotation Curves")
#
# plt.tight_layout()
# plt.legend()
#
#
#
# # New VAM formula: v = C_eff / sqrt(1 + (r_c/r)^2)
# C_eff = 200e3  # effective saturation velocity in m/s
# r_c_phys = 5 * 3.086e19  # 5 kpc in meters
#
# v_vam_new_formula = C_eff / np.sqrt(1 + (r_c_phys / r)**2)
#
# # 3D Plot against MOND and observed
# fig = plt.figure(figsize=(10, 6))
# ax = fig.add_subplot(111, projection='3d')
#
# # Plot models
# ax.plot(r_kpc, v_mond_interp / 1e3, zs=0, zdir='z', label="MOND (interpolated)", color='black')
# ax.plot(r_kpc, v_mond_flat / 1e3, zs=1, zdir='z', label="MOND (flat limit)", color='gray')
# ax.plot(r_kpc, v_vam_new_formula / 1e3, zs=2, zdir='z', label=r"VAM $C_{\mathrm{eff}} / \sqrt{1 + (r_c/r)^2}$", color='blue')
#
# # Observations
# ax.scatter(r_data_kpc, v_data_kms, zs=-1, zdir='z', label="Observed", color='red', s=50)
#
# # Axis settings
# ax.set_xlabel("Radius (kpc)")
# ax.set_ylabel("Velocity (km/s)")
# ax.set_zlabel("Model Index")
# ax.set_zticks([-1, 0, 1, 2])
# ax.set_zticklabels(["Observed", "MOND\ninterp", "MOND\nflat", "VAM"])
# ax.set_xlim(0, 50)
# ax.set_ylim(150, 250)
# ax.set_zlim(-1.5, 2.5)
# ax.set_title("VAM Smooth Transition vs MOND and Observations")
#
# plt.tight_layout()
# plt.legend()
#
#
# # Improved model with logistic/plateau blend instead of additive square root
# C_eff_core = 100e3    # swirl-like Newtonian component (inner)
# C_eff_tail = 100e3    # swirl tail saturation (outer)
#
# # Hybrid VAM model using additive linear terms
# v_vam_blend = (C_eff_core / np.sqrt(1 + (r_c / r)**2)) + C_eff_tail * (1 - np.exp(-r / r_c))
#
# # Plot this final VAM model
# plt.figure(figsize=(8, 6))
# plt.plot(r / 3.086e19, v_vam_blend / 1e3, label="VAM (core + swirl blend)", linewidth=2, color='darkgreen')
# plt.plot(r / 3.086e19, v_mond / 1e3, label="MOND", linestyle='-.', color='black')
# plt.scatter(r_data, v_data, color='black', label="Observed", zorder=5)
# plt.xlabel("Radius (kpc)")
# plt.ylabel("Orbital Velocity (km/s)")
# plt.title("Refined VAM Model: Swirl Core + Saturated Tail")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.savefig("GalexyRotation.pdf")  # Save to downloadable PDF
# plt.show()
#
#



