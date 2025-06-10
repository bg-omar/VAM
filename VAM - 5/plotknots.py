import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import os
import ace_tools_open as tools
from constants import *

phi= 1.6180339887 # Golden ratio
n_vals = np.arange(0, 11) # Topological levels from 0 to 10
A = (8 * np.pi * rho_ae * r_c**3 * C_e) / c

vam_masses = A * phi**n_vals


# Generate extended torus knot spectrum using (p*n, q*n)
p, q = 2, 3
n_range = np.arange(1, 11)
gamma = 0.005901

torus_masses_pn_qn = [
    (p * n, q * n, (8 * np.pi * 3.8934358267e18 * r_c**3 / C_e) *
     (np.sqrt((p * n)**2 + (q * n)**2) + gamma * (p * n) * (q * n)))
    for n in n_range
]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(n_vals, vam_masses, 'o-', label=r'$M_n = A \cdot \phi^n$')

for n, (pn, qn, mass) in zip(n_range, torus_masses_pn_qn):
    plt.scatter(n, mass, label=fr'$M({pn},{qn})$', s=100, marker='x')

plt.yscale('log')
plt.xlabel('Topological Level $n$')
plt.ylabel('Mass [kg]')
plt.title('Extended Knot Spectrum: $M(pn, qn)$ vs $M_n$')
plt.legend()
plt.grid(True)
plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

# Generate extended torus knot spectrum using (p*n, q*n)
p, q = 2, 3
n_range = np.arange(1, 11)
gamma = 0.005901

torus_masses_pn_qn = [
    (p * n, q * n, (8 * np.pi * 3.8934358267e18 * r_c**3 / C_e) *
     (np.sqrt((p * n)**2 + (q * n)**2) + gamma * (p * n) * (q * n)))
    for n in n_range
]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(n_vals, vam_masses, 'o-', label=r'$M_n = A \cdot \phi^n$')

for n, (pn, qn, mass) in zip(n_range, torus_masses_pn_qn):
    plt.scatter(n, mass, label=fr'$M({pn},{qn})$', s=100, marker='x')

plt.yscale('log')
plt.xlabel('Topological Level $n$')
plt.ylabel('Mass [kg]')
plt.title('Extended Knot Spectrum: $M(pn, qn)$ vs $M_n$')
plt.legend()
plt.grid(True)
plt.tight_layout()
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

# Explore (p * n^2, q * n^2) scaling
torus_masses_pn2_qn2 = [
    (p * n**2, q * n**2, (8 * np.pi * 3.8934358267e18 * r_c**3 / C_e) *
     (np.sqrt((p * n**2)**2 + (q * n**2)**2) + gamma * (p * n**2) * (q * n**2)))
    for n in n_range
]

# Known particle masses for annotation (mass in kg)
known_particles = {
    "electron": 9.10938356e-31,
    "muon": 1.883531627e-28,
    "proton": 1.67262192369e-27,
    "helium-4": 6.6464764e-27,
    "carbon-12": 1.9926468e-26,
}

# Plotting
plt.figure(figsize=(12, 7))

# Global spectrum
plt.plot(n_vals, vam_masses, 'o-', label=r'$M_n = A \cdot \phi^n$')

# Torus knot spectrum (p*n^2, q*n^2)
for n, (pn, qn, mass) in zip(n_range, torus_masses_pn2_qn2):
    plt.scatter(n, mass, label=fr'$M({pn},{qn})$', s=100, marker='x')

# Known particle masses
for name, mass in known_particles.items():
    plt.axhline(mass, linestyle='--', label=f'{name} mass', linewidth=1)

plt.yscale('log')
plt.xlabel('Topological Index $n$')
plt.ylabel('Mass [kg]')
plt.title('Topological Mass Spectra: $M_n$ vs $M(pn^2, qn^2)$ with Known Particles')
plt.legend(loc='upper left', fontsize=9)
plt.grid(True)
plt.tight_layout()
filename = f"{script_name}3.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution


from math import sqrt, e

# Define a list of exponents to try
irrational_exponents = [("golden", phi), ("sqrt2", sqrt(2)), ("e", e)]
match_errors = []

# Evaluate match errors to known particles for each irrational exponent
for label, exponent in irrational_exponents:
    for n in n_range:
        pn = int(round(p * n**exponent))
        qn = int(round(q * n**exponent))
        mass = (8 * np.pi * 3.8934358267e18 * r_c**3 / C_e) * (np.sqrt(pn**2 + qn**2) + gamma * pn * qn)

        for name, true_mass in known_particles.items():
            percent_error = 100 * (mass - true_mass) / true_mass
            match_errors.append([label, exponent, n, pn, qn, name, true_mass, mass, percent_error])

# Create DataFrame
df_matches = pd.DataFrame(match_errors, columns=[
    "Exponent Label", "Exponent Value", "n", "pn", "qn", "Particle", "Known Mass (kg)", "Predicted Mass (kg)", "Percent Error (%)"
])

# Filter to matches within ±10%
filtered_matches = df_matches[np.abs(df_matches["Percent Error (%)"]) <= 10].sort_values(by="Percent Error (%)", key=np.abs)

tools.display_dataframe_to_user(name="Best Matches Using Irrational Hybrid Scaling", dataframe=filtered_matches)

# Plotting
plt.figure(figsize=(12, 7))

# Global spectrum
plt.plot(n_vals, vam_masses, 'o-', label=r'$M_n = A \cdot \phi^n$')

# Torus knot spectrum (p*n^2, q*n^2)
for n, (pn, qn, mass) in zip(n_range, torus_masses_pn2_qn2):
    plt.scatter(n, mass, label=fr'$M({pn},{qn})$', s=100, marker='x')

# Known particle masses
for name, mass in known_particles.items():
    plt.axhline(mass, linestyle='--', label=f'{name} mass', linewidth=1)

plt.yscale('log')
plt.xlabel('Topological Index $n$')
plt.ylabel('Mass [kg]')
plt.title('Topological Mass Spectra: $M_n$ vs $M(pn^2, qn^2)$ with Known Particles')
plt.legend(loc='upper left', fontsize=9)
plt.grid(True)
plt.tight_layout()
filename = f"{script_name}4.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()