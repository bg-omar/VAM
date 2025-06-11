# Visualize a compact high-energy vortex ring at the Planck scale
# We'll use the user's constants for r_c and C_e to illustrate a maximal configuration

from math import pi

# User constants
r_c = 1.40897017e-15  # vortex core radius [m]
C_e = 1093845.63       # vortex tangential velocity [m/s]
rho_core = 3.8934358266918687e18  # core density [kg/m^3]
F_max = 29.053507      # maximum force [N]

# Calculate the angular velocity and energy density in the core
omega_core = C_e / r_c  # [rad/s]
energy_density = 0.5 * rho_core * omega_core**2 * r_c**2  # [J/m^3]

# Estimate max pressure gradient force from core energy
volume = (4/3) * pi * r_c**3  # [m^3]
max_energy = energy_density * volume  # [J]
force_estimate = max_energy / r_c  # [N] by pressure over distance

# Output summary
{
    "Core Radius r_c [m]": r_c,
    "Core Tangential Velocity C_e [m/s]": C_e,
    "Core Angular Velocity ω_core [rad/s]": omega_core,
    "Core Energy Density [J/m^3]": energy_density,
    "Core Volume [m^3]": volume,
    "Core Energy [J]": max_energy,
    "Estimated Force from Core Energy [N]": force_estimate,
    "Maximum Force Defined F_max [N]": F_max,
    "Ratio Force Estimate / F_max": force_estimate / F_max
}
