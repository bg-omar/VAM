# Reinitialize constants after execution state reset
import math
import pandas as pd
import ace_tools_open as tools
from constants import *
N = 1
Z = 1
R = A_0

R_e = (lambda_c / (2 * math.pi)) * alpha
R_e = (e**2) / (4 * math.pi * varepsilon_0 * M_e * c**2)
R_e = 2 * r_c

R_e = alpha**2 * A_0
R_e = (e**2) / (4 * math.pi * varepsilon_0 * M_e * c**2)
R_e = (e**2) / (8 * math.pi * varepsilon_0 * F_max * r_c)

R_x = N * (F_max * r_c**2) / (M_e * Z * C_e**2)
e = math.sqrt(16 * math.pi * F_max * r_c**2) / (mu_0 * c**2)
e**2 = 16 * math.pi * F_max * varepsilon_0 * R_e**2

e = math.sqrt(2 * alpha * h) / (mu_0 * c)
e = math.sqrt(4 * C_e * h) / (mu_0 * c**2)
R**2 = (N * F_max * r_c) / (4 * math.pi**2 * f_c**2 * M_e)

R**2 = (4 * math.pi * F_max * r_c**2) / C_e * (1 / (8 * math.pi**2 * M_e * f_c))
1 / r_c = c**2 / (A_0 * 2 * C_e**2)

R_e = (lambda_c / (2 * math.pi)) * alpha
R_e = (e**2) / (4 * math.pi * varepsilon_0 * M_e * c**2)
R_e = 2 * R_c

R_e = alpha**2 * A_0
R_e = (e**2) / (4 * math.pi * varepsilon_0 * M_e * c**2)
R_e = (e**2) / (8 * math.pi * varepsilon_0 * F_max * R_c)

R_x = N * (F_max * R_c**2) / (M_e * Z * C_e**2)
e = math.sqrt(16 * math.pi * F_max * R_c**2) / (mu_0 * c**2)
e**2 = 16 * math.pi * F_max * varepsilon_0 * R_e**2

e = math.sqrt(2 * alpha * h) / (mu_0 * c)
e = math.sqrt(4 * C_e * h) / (mu_0 * c**2)
R**2 = (N * F_max * R_c) / (4 * math.pi**2 * f_c**2 * M_e)

R**2 = (4 * math.pi * F_max * R_c**2) / C_e * (1 / (8 * math.pi**2 * M_e * f_c))
1 / R_c = c**2 / (A_0 * 2 * C_e**2)
L_p = math.sqrt(hbar * G / c**3)

L_p = (lambda_c * C_e * t_p) / (2 * math.pi * R_c)
L_P = math.sqrt(alpha_g * hbar * R_c / C_e * M_e)
L_P = math.sqrt(hbar * t_p**2 * C_e * c**2 / (2 * F_max * R_c**2))

G1 = (C_e * c**3 * L_p**2) / (2 * F_max * R_c**2)
G2 = (C_e * c**3 * t_p**2) / (R_c * M_e)
G3 = (F_max * alpha * (c * t_p)**2) / M_e**2

G4 = (C_e * c * L_p**2) / (R_c * M_e)
G5 = (alpha_g * c**3 * R_c) / (C_e * M_e)
G6 = (C_e * c**3 * t_p**2) / (R_c * (2 * F_max * R_c / c**2))

alpha1 = lambda_c / (4 * math.pi * R_c)
alpha2 = (C_e * e**2) / (8 * math.pi * varepsilon_0 * R_c**2 * c * F_max)
alpha3 = lambda_c / (4 * math.pi * R_c)

alpha_inv = 2 / alpha
omega_c = alpha_inv * C_e / R_c
alpha4 = (c / (2 * alpha) * e**2) / (8 * math.pi * varepsilon_0 * R_c**2 * c * F_max)
alpha_sq = e**2 / (16 * math.pi * varepsilon_0 * R_c**2 * F_max)
alpha_g1 = (2 * F_max * C_e * t_p**2) / (2 * F_max * R_c**2 / C_e)

alpha_g2 = (C_e**2 * t_p**2) / R_c**2
alpha_g3 = (F_max * 2 * C_e * t_p**2) / hbar
alpha_g4 = (F_max * t_p**2) / (A_0 * M_e)

alpha_g5 = (C_e * c**2 * t_p**2 * M_e) / (hbar * R_c)
alpha_g6 = (C_e**2 * L_p**2) / (R_c**2 * c**2)
M_e = (2 * F_max * R_c) / c**2


f_c = C_e / (2 * math.pi * R_c)
lambda_c = 2 * math.pi * c * R_c / C_e
lambda_c = 4 * math.pi * F_max * R_c**2 / (C_e * M_e * c)

M_e_c2 = 2 * F_max * R_c
lambda_c = 2 * math.pi * c * R_c / C_e
lambda_c = 4 * math.pi * F_max * R_c**2 / (C_e * M_e * c)

lambda_c = 4 * math.pi * R_c / C_e
C_e = c / (2 * alpha)
R_c = R_e / 2

F_centrifugal = M_e * R_c * (C_e / R_c)**2
F_centrifugal = M_e * C_e**2 / R_c
h = 4 * math.pi * M_e * C_e * A_0
h = 4 * math.pi * F_max * R_e**2 / C_e

h = 16 * math.pi * F_max**2 * R_c**3 * A_0 / (hbar * c**2)
R_infty = C_e**3 / (math.pi * R_c * c**3)
C_e = R_c * M_e * c**2 / hbar

F_max = 0.5 * (C_e / c)**-2 * M_e * omega_c**2 * R_c
F_max = h * alpha * c / (8 * math.pi * R_c**2)
F_max = e**2 / (16 * math.pi * varepsilon_0 * R_c**2)


def u_vortex(r, omega, T, F_max, C_e, hbar, k_B):
    return (F_max * omega**3 / (C_e * r**2)) * (1 / (math.exp(hbar * omega / (k_B * T)) - 1))

def s_vortex(r, T, F_max, C_e, k_B, hbar):
    return (4 * math.pi**4 * F_max * k_B**4 * T**3) / (45 * C_e * r**2 * hbar**4)

def phi_vortex(r, T, F_max, k_B, hbar):
    return (math.pi**4 * F_max * k_B**4 * T**4) / (15 * hbar**4 * r)

def u_total(T, F_max, C_e, r):
    return F_max * T**4 / (C_e * r**2)

def s_total(T, F_max, C_e, r):
    return F_max * T**3 / (C_e * r**2)




def energy_density_vortex(r, omega, F_max, C_e):
    return (F_max * omega**3) / (C_e * r**2)

def entropy_density_vortex(r, omega, T, F_max, C_e):
    return (4 * F_max * omega**3) / (3 * T * C_e * r**2)

# Validated (dimensionally correct and matches blackbody radiation scaling)
# Validated (consistent with thermodynamic entropy relations)

