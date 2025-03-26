import math
from sympy import symbols, simplify

# Physical constants from VAM constants list
rho_ae = 7.0e-7  # Æther density [kg/m^3]
Gamma_e = 2 * math.pi * 1.054571817e-34 / (9.1093837015e-31)  # Circulation ~ hbar/m_e [m^2/s]
R = 2.8179403262e-15  # classical electron radius [m]
a = 1.616255e-35  # core radius ~ Planck length [m]
Lk = 3  # linking number for trefoil
Wr = 1.5  # estimated writhe
p = 2
q = 3

# Energy of a thin-core vortex ring (Saffman's formula)
alpha = 1.25  # estimated for hollow-core
E = rho_ae * Gamma_e**2 * R * (math.log(8 * R / a) - alpha)  # in joules

# Helicity
H = Gamma_e**2 * (Lk + Wr)

# Local time dilation ratio
dt_local_over_dt = (q / p) * (H / E)

# Return symbolic expression as well
Γ, ρ, R_sym, a_sym, Lk_sym, Wr_sym, α_sym, p_sym, q_sym = symbols('Γ ρ R a Lk Wr α p q')
E_sym = ρ * Γ**2 * R_sym * (math.log(8 * R / a) - α_sym)
H_sym = Γ**2 * (Lk_sym + Wr_sym)
dt_local_over_dt_sym = (q_sym / p_sym) * (H_sym / E_sym)
dt_local_over_dt_sym = simplify(dt_local_over_dt_sym)

print(dt_local_over_dt)
print(dt_local_over_dt_sym)

# Physical constants
t_planck = 5.391247e-44  # Planck time [s]
m_e = 9.1093837015e-31  # electron mass [kg]
hbar = 1.054571817e-34  # reduced Planck constant [J·s]

# Compton time: τ = λ_c / c = hbar / (m_e c^2)
c = 299792458  # speed of light [m/s]
tau_compton = hbar / (m_e * c**2)

# Local time duration compared to Planck time and Compton time
local_time_planck = t_planck * dt_local_over_dt
local_time_compton = tau_compton * dt_local_over_dt

print(local_time_planck)
print(local_time_compton)
print(tau_compton)
from sympy import symbols, solve, Eq, log

# Symbols
R_sym = symbols('R', positive=True)

# Constants used in symbolic form
Gamma_val = Gamma_e
rho_val = rho_ae
a_val = a
alpha_val = 1.25
Lk_val = 3
Wr_val = 1.5
p_val = 2
q_val = 3

# Define energy and helicity symbolically
E_expr = rho_val * Gamma_val**2 * R_sym * (log(8 * R_sym / a_val) - alpha_val)
H_expr = Gamma_val**2 * (Lk_val + Wr_val)

# Time dilation: dt_local/dt = (q/p) * (H/E)
dt_ratio_expr = (q_val / p_val) * (H_expr / E_expr)

# Set dt_local/dt = 1 / tau_compton to match local time = Compton time
target_ratio = 1 / tau_compton
eq = Eq(dt_ratio_expr, target_ratio)

# Solve for R
solution_R = solve(eq, R_sym)
print(solution_R)

# Try numeric root finding instead of symbolic solve
from scipy.optimize import fsolve
import numpy as np

# Define the equation numerically: dt_local/dt - (1 / tau_compton) = 0
def time_ratio_eq(R_val):
    E_val = rho_ae * Gamma_e**2 * R_val * (np.log(8 * R_val / a) - alpha)
    H_val = Gamma_e**2 * (Lk + Wr)
    dt_local_dt = (q / p) * (H_val / E_val)
    return dt_local_dt - (1 / tau_compton)

# Initial guess for R (somewhere near the classical electron radius)
R_guess = 1e-15
R_solution = fsolve(time_ratio_eq, R_guess)[0]
print(R_solution)
