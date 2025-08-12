from turtle import pd
import ace_tools_open as tools;
from sympy import symbols, solve, Eq, N
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import pandas as pd
from constants import *


# Compute target factor from best match
gamma = 0.05
p_target, q_target = 309, 400
target_factor = np.sqrt(p_target**2 + q_target**2) + gamma * p_target * q_target

# Search for smaller (p', q') with approximately same factor
simpler_matches = []

# Parameters
R = 2  # Major radius
r = 0.5  # Minor radius
t = np.linspace(0, 2 * np.pi, 1000)

# Number of components
n = 6

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(n):
    phase = 2 * np.pi * i / n
    x = (R + r * np.cos(6 * t + phase)) * np.cos(6 * t + phase)
    y = (R + r * np.cos(6 * t + phase)) * np.sin(6 * t + phase)
    z = r * np.sin(6 * t + phase)
    ax.plot(x, y, z)

ax.set_box_aspect([1, 1, 1])
plt.title("Torus Link (6,6)")





R = 2     # Major radius of the torus
r = 0.5   # Minor radius
t = np.linspace(0, 2 * np.pi, 1000)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot 3 components
for k in range(3):
    phase = 2 * np.pi * k / 3
    x = (R + r * np.cos(9 * t)) * np.cos(6 * t + phase)
    y = (R + r * np.cos(9 * t)) * np.sin(6 * t + phase)
    z = r * np.sin(9 * t)
    ax.plot(x, y, z, label=f'Component {k+1}')

ax.set_box_aspect([1,1,1])
plt.title("Torus Link (6,9)")
plt.legend()


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Constants (as defined by the user)
rho_ae = 3.893e18  # kg/m^3
r_c = 1.40897e-15  # m
C_e = 1.09384563e6  # m/s
L_k = 0.0223  # Estimated circulation length to match proton mass

# Mass calculation from VAM formula
M_p_VAM = 3 * (8 * np.pi * rho_ae * r_c**3 / C_e) * L_k
M_p_real = 1.67262192369e-27  # kg, real proton mass

# Torus parameters for plotting
R = 2.0
r = 0.5
t = np.linspace(0, 2 * np.pi, 1000)
components = 3
phases = [2 * np.pi * k / components for k in range(components)]

# Prepare 3D plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Generate components of the (6,9) torus link
for phase in phases:
    x = (R + r * np.cos(9 * t)) * np.cos(6 * t + phase)
    y = (R + r * np.cos(9 * t)) * np.sin(6 * t + phase)
    z = r * np.sin(9 * t)
    ax.plot(x, y, z)

ax.set_title("Torus Link (6,9) – 3 Linked Trefoils as VAM Proton Model")
ax.set_box_aspect([1,1,1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Display calculated mass
mass_text = f"VAM Mass = {M_p_VAM:.3e} kg\nReal Proton Mass = {M_p_real:.3e} kg\nError = {abs(M_p_VAM - M_p_real)/M_p_real:.2%}"
plt.figtext(0.15, 0.8, mass_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

R = 2
r = 0.3
t = np.linspace(0, 2 * np.pi, 1000)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for k in range(12):
    phase = 2 * np.pi * k / 12
    x = (R + r * np.cos(36 * t)) * np.cos(24 * t + phase)
    y = (R + r * np.cos(36 * t)) * np.sin(24 * t + phase)
    z = r * np.sin(36 * t)
    ax.plot(x, y, z)

ax.set_box_aspect([1,1,1])
plt.title("Torus Link (24,36): 12 Trefoil Components")
plt.show()





import numpy as np
import pandas as pd

# Constants from user's model
rho_ae = 3.893e18        # kg/m^3
r_c = 1.40897e-15        # m
C_e = 1.09384563e6       # m/s

# Symbolic prefactor alpha = beta * lambda_0 * chi
# Choose representative values: beta = pi/2, lambda_0 = 1.0, chi = 10
beta = np.pi / 2
lambda_0 = 1.0
chi = 10
alpha = beta * lambda_0 * chi

# Predictive VAM mass formula
def vam_mass(p, q):
    return alpha * rhoMass * C_e * r_c**3 * np.sqrt(p ** 2 + q ** 2)

# Knot types
knot_list = [(2, 3), (4, 6), (6, 9), (12, 18), (18, 27), (20, 30), (24, 36), (40, 60)]
results = []

for p, q in knot_list:
    mass = vam_mass(p, q)
    results.append({
        'Knot': f'T({p},{q})',
        'sqrt(p^2 + q^2)': np.sqrt(p**2 + q**2),
        'Mass (kg)': mass
    })

df = pd.DataFrame(results)
tools.display_dataframe_to_user(name="VAM Knot Mass Predictions", dataframe=df)


# Knot types
knot_list = [(2, 3), (4, 6), (6, 9), (12, 18), (18, 27), (20, 30), (24, 36), (40, 60)]

# Define topological helicity correction
# Assume helicity increases with pq and adds a correction term to mass
def helicity_corrected_mass(p, q, gamma=0.05):
    # Base mass
    base_mass = vam_mass(p, q)
    # Topological correction factor (helicity-inspired)
    helicity_term = gamma * p * q
    return base_mass * (1 + helicity_term)

# Recompute masses with helicity correction
corrected_results = []

for p, q in knot_list:
    base = vam_mass(p, q)
    corrected = helicity_corrected_mass(p, q)
    helicity_term = corrected / base - 1
    corrected_results.append({
        'Knot': f'T({p},{q})',
        'sqrt(p^2 + q^2)': np.sqrt(p**2 + q**2),
        'Base Mass (kg)': base,
        'Helicity Term (×Base)': helicity_term,
        'Corrected Mass (kg)': corrected
    })

corrected_df = pd.DataFrame(corrected_results)
tools.display_dataframe_to_user(name="VAM Masses with Helicity Correction", dataframe=corrected_df)


# Updated formula with symbolic decomposition of the geometric/topological factors
# We'll define Swirl-Length = sqrt(p^2 + q^2), Topological Factor = helicity = gamma * p * q

def symbolic_mass(p, q, gamma=0.05):
    swirl_length = np.sqrt(p**2 + q**2)
    topological_factor = gamma * p * q
    # Full factor = swirl_length + topological_correction
    full_factor = swirl_length + topological_factor
    # VAM mass expression
    return (8 * np.pi * rhoMass * r_c ** 3 / C_e) * full_factor

# Compute new symbolic masses
symbolic_results = []

for p, q in knot_list:
    swirl = np.sqrt(p**2 + q**2)
    helicity = 0.05 * p * q
    total = swirl + helicity
    mass = symbolic_mass(p, q)
    symbolic_results.append({
        'Knot': f'T({p},{q})',
        'Swirl Length': swirl,
        'Topological Term (γpq)': helicity,
        'Full Factor': total,
        'Mass (kg)': mass
    })

symbolic_df = pd.DataFrame(symbolic_results)
tools.display_dataframe_to_user(name="Symbolic VAM Mass with Topological Correction", dataframe=symbolic_df)


import numpy as np
import pandas as pd

# Constants from user's model
rho_ae = 3.893e18        # kg/m^3
r_c = 1.40897e-15        # m
C_e = 1.09384563e6       # m/s

# Symbolic prefactor alpha = beta * lambda_0 * chi
# Choose representative values: beta = pi/2, lambda_0 = 1.0, chi = 10
beta = np.pi / 2
lambda_0 = 1.0
chi = 10
alpha = beta * lambda_0 * chi

# Predictive VAM mass formula
def vam_mass(p, q):
    return alpha * rhoMass * C_e * r_c**3 * np.sqrt(p ** 2 + q ** 2)

results = []

for p, q in knot_list:
    mass = vam_mass(p, q)
    results.append({
        'Knot': f'T({p},{q})',
        'sqrt(p^2 + q^2)': np.sqrt(p**2 + q**2),
        'Mass (kg)': mass
    })

df = pd.DataFrame(results)

tools.display_dataframe_to_user(name="VAM Knot Mass Predictions", dataframe=df)



# Updated formula with symbolic decomposition of the geometric/topological factors
# We'll define Swirl-Length = sqrt(p^2 + q^2), Topological Factor = helicity = gamma * p * q

def symbolic_mass(p, q, gamma=0.05):
    swirl_length = np.sqrt(p**2 + q**2)
    topological_factor = gamma * p * q
    # Full factor = swirl_length + topological_correction
    full_factor = swirl_length + topological_factor
    # VAM mass expression
    return (8 * np.pi * rhoMass * r_c ** 3 / C_e) * full_factor

# Compute new symbolic masses
symbolic_results = []

for p, q in knot_list:
    swirl = np.sqrt(p**2 + q**2)
    helicity = 0.05 * p * q
    total = swirl + helicity
    mass = symbolic_mass(p, q)
    symbolic_results.append({
        'Knot': f'T({p},{q})',
        'Swirl Length': swirl,
        'Topological Term (γpq)': helicity,
        'Full Factor': total,
        'Mass (kg)': mass
    })

symbolic_df = pd.DataFrame(symbolic_results)
tools.display_dataframe_to_user(name="Symbolic VAM Mass with Topological Correction", dataframe=symbolic_df)


# Define extended knot list as described by user, keeping only multiples of (2,3) and scaling
extended_knot_list = [
    (4, 6), (6, 9), (12, 18), (18, 27), (20, 30), (24, 36),
    (40, 60), (60, 90), (120, 180), (400, 600)
]

# Calculate symbolic mass using the earlier symbolic_mass function
proton_mass = 1.67262192369e-27  # kg

mass_comparison_results = []

for p, q in extended_knot_list:
    swirl = np.sqrt(p**2 + q**2)
    helicity = 0.05 * p * q
    total = swirl + helicity
    mass = symbolic_mass(p, q)
    error = abs(mass - proton_mass) / proton_mass
    mass_comparison_results.append({
        'Knot': f'T({p},{q})',
        'Swirl Length': swirl,
        'Topological Term (γpq)': helicity,
        'Total Factor': total,
        'Mass (kg)': mass,
        'Relative Error to Proton': f'{error:.2%}'
    })

mass_comparison_df = pd.DataFrame(mass_comparison_results)
tools.display_dataframe_to_user(name="VAM Mass Matching Proton (T(p,q) Series)", dataframe=mass_comparison_df)

# We want to find the integer pair (p, q), with p and q multiples of 2 or 3, such that:
# M(p,q) = M_proton, using the symbolic_mass function with the helicity correction.

# Create a search space: p, q in range [2, 1000] in steps of 2 or 3
p_range = list(range(2, 1001, 2)) + list(range(3, 1001, 3))
p_range = sorted(set(p_range))
q_range = p_range  # symmetric search space

best_match = {'p': None, 'q': None, 'mass': 0, 'error': float('inf')}

for p in p_range:
    for q in q_range:
        mass = symbolic_mass(p, q)
        error = abs(mass - proton_mass) / proton_mass
        if error < best_match['error']:
            best_match = {'p': p, 'q': q, 'mass': mass, 'error': error}

# Format results
best_match_result = pd.DataFrame([{
    'Best p': best_match['p'],
    'Best q': best_match['q'],
    'Mass (kg)': best_match['mass'],
    'Relative Error': f"{best_match['error']:.4%}"
}])

tools.display_dataframe_to_user(name="Best (p, q) Pair Matching Proton Mass", dataframe=best_match_result)


# Define symbolic variable
n = symbols('n', real=True, positive=True)

# Target factor
F_target = 6685.49

# Coefficients from symbolic model
eq = Eq(3 * n * (np.sqrt(13) + 6 * gamma * n), F_target)

# Solve for n
solutions = solve(eq, n)
numeric_solutions = [N(sol) for sol in solutions if sol.is_real and sol > 0]

numeric_solutions


# It seems the DataFrame is empty due to too strict of an error threshold.
# Let's relax the filter condition and rerun the search.

matching_results = []
# Updated formula with symbolic decomposition of the geometric/topological factors
# We'll define Swirl-Length = sqrt(p^2 + q^2), Topological Factor = helicity = gamma * p * q

def symbolic_mass(p, q, gamma=0.05):
    swirl_length = np.sqrt(p**2 + q**2)
    topological_factor = gamma * p * q
    # Full factor = swirl_length + topological_correction
    full_factor = swirl_length + topological_factor
    # VAM mass expression
    return (8 * np.pi * rhoMass * r_c ** 3 / C_e) * full_factor

# Compute new symbolic masses
symbolic_results = []

for p, q in knot_list:
    swirl = np.sqrt(p**2 + q**2)
    helicity = 0.05 * p * q
    total = swirl + helicity
    mass = symbolic_mass(p, q)
    symbolic_results.append({
        'Knot': f'T({p},{q})',
        'Swirl Length': swirl,
        'Topological Term (γpq)': helicity,
        'Full Factor': total,
        'Mass (kg)': mass
    })

symbolic_df = pd.DataFrame(symbolic_results)
tools.display_dataframe_to_user(name="Symbolic VAM Mass with Topological Correction", dataframe=symbolic_df)

from sympy import symbols, solve, Eq, N

# Define symbolic variable
n = symbols('n', real=True, positive=True)

# Target factor
F_target = 6685.49

# Coefficients from symbolic model
eq = Eq(3 * n * (np.sqrt(13) + 6 * gamma * n), F_target)

# Solve for n
solutions = solve(eq, n)
numeric_solutions = [N(sol) for sol in solutions if sol.is_real and sol > 0]

print(numeric_solutions)


# Use the derived n ≈ 80.39 to build the scaled trefoil triple configuration
n_opt = 80.3877
p_scaled = int(round(2 * n_opt))
q_scaled = int(round(3 * n_opt))

# Use symbolic_mass to compute single trefoil mass
def symbolic_mass(p, q, gamma=0.05):
    swirl_length = np.sqrt(p**2 + q**2)
    topological_factor = gamma * p * q
    full_factor = swirl_length + topological_factor
    prefactor = 8 * np.pi * rhoMass * r_c ** 3 / C_e
    return prefactor * full_factor

# Total mass from three scaled trefoils
mass_single = symbolic_mass(p_scaled, q_scaled)
mass_triplet = 3 * mass_single

# Relative error vs proton
error = abs(mass_triplet - proton_mass) / proton_mass

# Present as DataFrame
validation_df = pd.DataFrame([{
    'Knot (p,q)': f'T({p_scaled},{q_scaled})',
    'Single Trefoil Mass (kg)': mass_single,
    'Triplet Mass (kg)': mass_triplet,
    'Proton Mass (kg)': proton_mass,
    'Relative Error': f"{error:.6%}"
}])

tools.display_dataframe_to_user(name="Triple Trefoil Proton Model Validation", dataframe=validation_df)


# Proton mass
M_p = proton_mass

# Neutron mass (in kg)
mass_difference_meV = 1.29333236  # MeV/c^2
mass_difference_joules = mass_difference_meV * 1.60218e-13  # MeV to J
M_n = M_p + mass_difference_joules / C_e**2  # neutron mass in kg

# Compute required total symbolic factor for neutron
prefactor = 8 * np.pi * rho_ae * r_c**3 / C_e
F_required_neutron = M_n / prefactor

# Compare to proton value
F_proton = M_p / prefactor
delta_F = F_required_neutron - F_proton

# Output
neutron_analysis = pd.DataFrame([{
    'Proton Mass Factor': F_proton,
    'Neutron Mass Factor': F_required_neutron,
    'Delta Factor Needed': delta_F,
    'Relative Difference (%)': 100 * delta_F / F_proton
}])

tools.display_dataframe_to_user(name="Neutron Mass Adjustment Analysis", dataframe=neutron_analysis)

# Compute δ_Borromean required to explain the neutron mass excess

# Mass prefactor
prefactor = 8 * np.pi * rho_ae * r_c**3 / C_e

# Mass difference (neutron - proton)
mass_delta = (M_n - M_p)

# Convert delta mass to delta factor
delta_borromean = mass_delta / prefactor

# Display result
borromean_coupling_df = pd.DataFrame([{
    'Mass Difference (kg)': mass_delta,
    'Mass Prefactor': prefactor,
    'Required Δ_Borromean Factor': delta_borromean
}])

tools.display_dataframe_to_user(name="Required Borromean Coupling Term for Neutron", dataframe=borromean_coupling_df)


# Calculate total neutron mass as triple trefoil plus Borromean correction

# Trefoil component
p_scaled, q_scaled = 161, 241
mass_single_trefoil = symbolic_mass(p_scaled, q_scaled)

# Borromean correction term (to match observed neutron mass)
delta_borromean_factor = 692206.881121
borromean_mass = prefactor * delta_borromean_factor

# Total neutron mass
mass_neutron_model = 3 * mass_single_trefoil + borromean_mass
relative_error = abs(mass_neutron_model - M_n) / M_n

# Present results
neutron_validation_df = pd.DataFrame([{
    'Component Trefoil Knot': f'T({p_scaled},{q_scaled})',
    '3x Trefoil Mass (kg)': 3 * mass_single_trefoil,
    'Borromean Mass (kg)': borromean_mass,
    'Total Neutron Mass (kg)': mass_neutron_model,
    'Actual Neutron Mass (kg)': M_n,
    'Relative Error': f'{relative_error:.6%}'
}])

tools.display_dataframe_to_user(name="Borromean Neutron Model Validation", dataframe=neutron_validation_df)


# Updated symbolic mass formula:
# M(p, q) = (8π * ρ_ae * r_c^3 / C_e) * (p^2 + q^2 + γ * p * q)

def quadratic_symbolic_mass(p, q, gamma=0.05):
    term = p**2 + q**2 + gamma * p * q
    return prefactor * term

# Compute new single trefoil mass and neutron mass
mass_single_quad = quadratic_symbolic_mass(p_scaled, q_scaled)
mass_neutron_quad = 3 * mass_single_quad + borromean_mass  # Keep borromean term for parity

# Compare to actual neutron mass
error_quad = abs(mass_neutron_quad - M_n) / M_n

# Create output
quad_validation_df = pd.DataFrame([{
    'Component Trefoil Knot': f'T({p_scaled},{q_scaled})',
    '3x Quadratic Trefoil Mass (kg)': 3 * mass_single_quad,
    'Borromean Mass (kg)': borromean_mass,
    'Total Neutron Mass (kg)': mass_neutron_quad,
    'Actual Neutron Mass (kg)': M_n,
    'Relative Error': f'{error_quad:.6%}'
}])

tools.display_dataframe_to_user(name="Quadratic Mass Formula Neutron Validation", dataframe=quad_validation_df)


# Define both symbolic mass formulas for comparison
def mass_linear_sqrt(p, q, gamma=0.05):
    return prefactor * (np.sqrt(p**2 + q**2) + gamma * p * q)

def mass_quadratic(p, q, gamma=0.05):
    return prefactor * (p**2 + q**2 + gamma * p * q)

# Electron: assume T(2,3)
p_e, q_e = 2, 3
mass_e_linear = mass_linear_sqrt(p_e, q_e)
mass_e_quad = mass_quadratic(p_e, q_e)
mass_e_actual = 9.1093837015e-31  # kg

# Proton: 3 × T(161,241)
mass_p_linear = 3 * mass_linear_sqrt(161, 241)
mass_p_quad = 3 * mass_quadratic(161, 241)
mass_p_actual = M_p

# Neutron: 3 × T(161,241) + Borromean term
mass_n_linear = mass_p_linear + borromean_mass
mass_n_quad = mass_p_quad + borromean_mass
mass_n_actual = M_n

# Compare errors
df_model_comparison = pd.DataFrame([
    {
        'Particle': 'Electron',
        'Mass Actual (kg)': mass_e_actual,
        'Linear+Sqrt Mass': mass_e_linear,
        'Quadratic Mass': mass_e_quad,
        'Linear Rel. Error': abs(mass_e_linear - mass_e_actual) / mass_e_actual,
        'Quadratic Rel. Error': abs(mass_e_quad - mass_e_actual) / mass_e_actual
    },
    {
        'Particle': 'Proton',
        'Mass Actual (kg)': mass_p_actual,
        'Linear+Sqrt Mass': mass_p_linear,
        'Quadratic Mass': mass_p_quad,
        'Linear Rel. Error': abs(mass_p_linear - mass_p_actual) / mass_p_actual,
        'Quadratic Rel. Error': abs(mass_p_quad - mass_p_actual) / mass_p_actual
    },
    {
        'Particle': 'Neutron',
        'Mass Actual (kg)': mass_n_actual,
        'Linear+Sqrt Mass': mass_n_linear,
        'Quadratic Mass': mass_n_quad,
        'Linear Rel. Error': abs(mass_n_linear - mass_n_actual) / mass_n_actual,
        'Quadratic Rel. Error': abs(mass_n_quad - mass_n_actual) / mass_n_actual
    }
])

# Format percentages
df_model_comparison['Linear Rel. Error'] = df_model_comparison['Linear Rel. Error'].apply(lambda x: f"{x:.4%}")
df_model_comparison['Quadratic Rel. Error'] = df_model_comparison['Quadratic Rel. Error'].apply(lambda x: f"{x:.4%}")

tools.display_dataframe_to_user(name="Mass Formula Comparison: Electron, Proton, Neutron", dataframe=df_model_comparison)

# We want to find the integer pair (p, q), with p and q multiples of 2 or 3, such that:
# M(p,q) = M_proton, using the symbolic_mass function with the helicity correction.

# Create a search space: p, q in range [2, 1000] in steps of 2 or 3
p_range = list(range(2, 1001, 2)) + list(range(3, 1001, 3))
p_range = sorted(set(p_range))
q_range = p_range  # symmetric search space

best_match = {'p': None, 'q': None, 'mass': 0, 'error': float('inf')}

for p in p_range:
    for q in q_range:
        mass = symbolic_mass(p, q)
        error = abs(mass - proton_mass) / proton_mass
        if error < best_match['error']:
            best_match = {'p': p, 'q': q, 'mass': mass, 'error': error}

# Format results
best_match_result = pd.DataFrame([{
    'Best p': best_match['p'],
    'Best q': best_match['q'],
    'Mass (kg)': best_match['mass'],
    'Relative Error': f"{best_match['error']:.4%}"
}])

tools.display_dataframe_to_user(name="Best (p, q) Pair Matching Proton Mass", dataframe=best_match_result)

# Given constants
F_max = 29.053507               # N
r_c = 1.40897017e-15            # m
c = 2.99792458e8                # m/s
L_k_18_27 = 63                  # topological linking number

# Compute mass from first principles
M_18_27_from_first_principles = (8 * math.pi * F_max / (3 * c**2 * r_c)) * L_k_18_27
print(M_18_27_from_first_principles)

import pandas as pd
import math

# Redefine constants after state reset
C_e = 1.09384563e6            # m/s
c = 2.99792458e8              # m/s
t_p = 5.391247e-44            # s
M_e = 9.1093837015e-31        # kg
r_c = 1.40897017e-15          # m
F_max = 29.053507             # N
rho_ae = 3.893e18  # kg/m^3


# Placeholder values for dimensionless parameters
I = 1.0
N = 1.0
mu = 1.0
K = 1.0

# Knot list
extended_knot_list = [
    (4, 6), (6, 9), (12, 18), (18, 27), (20, 30), (24, 36),
    (40, 60), (60, 90), (120, 180), (160, 240), (161, 241), (400, 600)
]

def linking_number(p, q):
    d = math.gcd(p, q)
    n = d
    L_self = 3 * n
    L_cross = n * (n - 1) // 2
    return L_self + L_cross, n

def mass_fmax(L_k):
    return (8 * math.pi * F_max * t_p**2 / (3 * c**2 * r_c)) * (L_k / t_p**2)

def mass_kelvin(n):
    return (C_e * c**3 * t_p**2) / (M_e * r_c) * (I**1.5 / (N * mu * K**0.5 * math.sqrt(math.pi))) * n

def mass_empirical(L_k):
    return (8 * math.pi * rhoMass * r_c ** 3 / C_e) * L_k

# Benchmark results
results = []
for p, q in extended_knot_list:
    L_k, n = linking_number(p, q)
    m_fmax = mass_fmax(L_k)
    m_emperic = mass_empirical(L_k)
    m_kelvin = mass_kelvin(n)
    results.append({
        "Knot (p,q)": f"T({p},{q})",
        "Components": n,
        "L_k": L_k,
        "Mass_Fmax (kg)": m_fmax,
        "Mass_Kelvin (kg)": m_kelvin,
        "Mass_Empirical (kg)": m_emperic,
    })

df = pd.DataFrame(results)
tools.display_dataframe_to_user(name="VAM Mass Benchmark", dataframe=df)


import math

# Constants
r_c = 1.40897017e-15         # m
C_e = 1.09384563e6           # m/s
pi = math.pi

# Circulation Gamma = 2π * r_c * C_e
Gamma = 2 * pi * r_c * C_e

# Torus link T(18,27)
N = 9  # Number of components
SL_k = 3  # Self-linking for each trefoil
Lk_ij = 1  # Pairwise linking number

# Total helicity H = sum self + sum mutual
self_helicity = N * (Gamma**2) * SL_k
mutual_helicity = sum([2 * Gamma**2 * Lk_ij for _ in range(N * (N - 1) // 2)])
total_helicity = self_helicity + mutual_helicity

print(self_helicity, mutual_helicity, total_helicity)


# Re-import constants due to session reset
import numpy as np
import pandas as pd

# Physical constants (from user-provided values)
rho_ae = 3.893e18        # kg/m^3
r_c = 1.40897e-15        # m
C_e = 1.09384563e6       # m/s
gamma = 0.0059           # derived from electron mass and T(2,3)

# Proton and neutron reference masses
M_proton_real = 1.67262192369e-27  # kg
M_neutron_real = 1.67492749804e-27  # kg

# Define symbolic mass formula
def symbolic_mass(p, q, gamma=gamma):
    swirl = np.sqrt(p**2 + q**2)
    helicity = gamma * p * q
    factor = swirl + helicity
    prefactor = 8 * np.pi * rhoMass * r_c ** 3 / C_e
    return prefactor * factor

# Find best n for 3 × T(2n,3n) configuration to match proton and neutron
def solve_triplet_mass_target(target_mass):
    factor = target_mass * C_e / (8 * np.pi * rhoMass * r_c ** 3)
    # We solve: 3n(√13 + 6γn) = factor
    # → 6γn^2 + √13 n - factor/3 = 0
    a = 6 * gamma
    b = np.sqrt(13)
    c = -factor / 3
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None
    n = (-b + np.sqrt(discriminant)) / (2 * a)
    return int(round(n))

# Compute best n for both
n_proton = solve_triplet_mass_target(M_proton_real)
n_neutron = solve_triplet_mass_target(M_neutron_real)

# Convert to (p, q)
p_proton, q_proton = 2 * n_proton, 3 * n_proton
p_neutron, q_neutron = 2 * n_neutron, 3 * n_neutron

# Compute predicted masses
mass_proton = 3 * symbolic_mass(p_proton, q_proton)
mass_neutron = 3 * symbolic_mass(p_neutron, q_neutron)

# Relative errors
error_proton = abs(mass_proton - M_proton_real) / M_proton_real
error_neutron = abs(mass_neutron - M_neutron_real) / M_neutron_real

# Result summary
results = pd.DataFrame([
    {
        "Model": "Proton (3 × T(2n,3n))",
        "n": n_proton,
        "Knot": f"T({p_proton},{q_proton})",
        "Mass (kg)": mass_proton,
        "Relative Error": f"{error_proton:.6%}"
    },
    {
        "Model": "Neutron (3 × T(2n,3n))",
        "n": n_neutron,
        "Knot": f"T({p_neutron},{q_neutron})",
        "Mass (kg)": mass_neutron,
        "Relative Error": f"{error_neutron:.6%}"
    }
])

tools.display_dataframe_to_user(name="Proton and Neutron Mass Model (γ = 0.0059)", dataframe=results)

import numpy as np

# Redefine constants after kernel reset
rho_ae = 3.893e18        # kg/m^3
r_c = 1.40897e-15        # m
C_e = 1.09384563e6       # m/s
M_e_exp = 9.10938356e-31 # kg, experimental electron mass

# Constant term in the mass formula
const = (8 * np.pi * rho_ae * r_c**3) / C_e

# Trefoil knot parameters for the electron
p, q = 2, 3
length_term = np.sqrt(p**2 + q**2)
pq = p * q

# Solve for gamma
gamma = (M_e_exp / const - length_term) / pq
gamma
