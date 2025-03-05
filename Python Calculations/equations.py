import math
from scipy.constants import pi, c, h, epsilon_0, G, k, m_e, e

# Given constants
C_e = 1093845.63  # Vortex-Core Tangential Velocity (m/s)
R_c = 1.40897017e-15  # Coulomb barrier (m)
M_e = 9.1093837015e-31  # Electron mass (kg)
alpha = 7.2973525643e-3  # Fine-structure constant
t_p = 5.391247e-44  # Planck time (s)
F_max = 29.053507  # Maximum force (N)
A_0 = 5.29177210903e-11  # Bohr radius (m)
mu_0 = 4 * pi * 1e-7  # Vacuum permeability (N/A^2)


M_e = (2 * F_max * R_c) / c**2
f_e = C_e / (2 * pi * R_c)

# Formulas translated into Python
R_e = (e**2) / (4 * pi * epsilon_0 * M_e * c**2)
R_e = 2 * R_c
R_e = alpha**2 * A_0
R_e = (e**2) / (4 * pi * epsilon_0 * M_e * c**2)
R_e = (e**2) / (8 * pi * epsilon_0 * F_max * R_c)

R_x = (F_max * R_c**2) / (M_e * C_e**2)

e = math.sqrt(16 * pi * F_max * R_c**2) / (mu_0 * c**2)
e = math.sqrt(2 * alpha * h) / (mu_0 * c)
e = math.sqrt(4 * C_e * h) / (mu_0 * c**2)

L_p = math.sqrt(h * G / c**3)
L_p = math.sqrt((alpha_g * h * R_c) / (C_e * M_e))
L_p = math.sqrt((h * t_p**2 * C_e * c**2) / (2 * F_max * R_c**2))

R_squared = (F_max * R_c) / (4 * pi**2 * f_e * m_e)
R_squared = (4 * pi * F_max * R_c**2) / (C_e * 8 * pi**2 * M_e * f_e)

alpha_g = (2 * F_max * C_e * t_p**2) / ((2 * F_max * R_c**2) / C_e)
alpha_g = (C_e**2 * t_p**2) / (R_c**2)
alpha_g = (F_max * 2 * C_e * t_p**2) / h
alpha_g = (F_max * t_p**2) / (A_0 * M_e)
alpha_g = (C_e * c**2 * t_p**2 * m_e) / (h * R_c)
alpha_g = (C_e**2 * L_p**2) / (R_c**2 * c**2)

G = (C_e * c**3 * L_p**2) / (2 * F_max * R_c**2)
G = (C_e * c**3 * t_p**2) / (R_c * m_e)
G = (F_max * alpha * (c * t_p)**2) / (m_e**2)
G = (C_e * c * L_p**2) / (R_c * M_e)
G = (alpha_g * c**3 * R_c) / (C_e * M_e)
G = (C_e * c**5 * t_p**2) / (2 * F_max * R_c**2)

alpha = (h / (4 * pi * R_c))
alpha = (C_e * e**2) / (8 * pi * epsilon_0 * R_c**2 * c * F_max)
alpha = (h / (4 * pi * R_c))
alpha = (omega_c * R_c) / (2 * C_e)

lambda_c = (2 * pi * c * R_c) / C_e
lambda_c = (4 * pi * F_max * R_c**2) / (C_e * m_e * c)

C_e = c / (2 * alpha)
R_c = R_e / 2

F_Cmax = (M_e * C_e**2) / R_c

h = 4 * pi * m_e * C_e * A_0
h = (4 * pi * F_max * R_e**2) / C_e
h = (16 * pi * F_max**2 * R_c**3 * A_0) / (h * c**2)

R_infinity = (C_e**3) / (pi * R_c * c**3)

F_Cmax = (h * alpha * c) / (8 * pi * R_c**2)
F_Cmax = e**2 / (16 * pi * epsilon_0 * R_c**2)

# Vortex Energy and Entropy Density
def vortex_energy_density(r, omega, T):
    return (F_Cmax * omega**3) / (C_e * r**2) / (math.exp(h * omega / (k * T)) - 1)

def vortex_entropy_density(r, T):
    return (4 * pi**4 * F_Cmax * k**4 * T**3) / (45 * C_e * r**2 * h**4)

def vortex_flux_density(r, T):
    return (pi**4 * F_Cmax * k**4 * T**4) / (15 * h**4 * r)

def total_energy(T, r):
    return (F_Cmax * T**4) / (C_e * r**2)

def total_entropy(T, r):
    return (F_Cmax * T**3) / (C_e * r**2)


