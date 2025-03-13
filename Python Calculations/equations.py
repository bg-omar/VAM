# Reinitialize constants after execution state reset
import math
import pandas as pd
import ace_tools_open as tools
from constants import *


# Given the new equations:
# ω = (2 * C_e) / r_c
# B_v = μ_v * (2 * C_e) / r_c
# μ_v = (ρ_ae * r_c^2) / 4

mu_v = (rho_ae * r_c**2) / 4
omega = (2 * C_e) / r_c
B_v = mu_v * omega


print("M_e: ", M_e)
print((2 * F_max * R_c) / c**2)

# Formulas translated into Python
print("\nA_0: ",A_0)
print(((c**2 * R_c) / (2 * C_e**2)))
print(((F_max * R_c**2) / (M_e * C_e**2)))
print(((4 * pi * varepsilon_0 * hbar**2) / (M_e * e**2)))
print(((h) / (4 * pi * M_e * C_e)))

print("\nR_squared", A_0**2)
print((h) / (4 * pi**2 * f_c * M_e * alpha**2))
print((c**2 * R_c) / (2 * pi * f_c * C_e * alpha**2))
print(((4 * pi * F_max * R_c**2) / (C_e)) * (1 /(4 * pi**2 * M_e * f_c * alpha**2)))

print("\nR_e: ",R_e)
print((e**2) / (4 * pi * varepsilon_0 * M_e * c**2))
print(2 * R_c)
print(alpha**2 * A_0)
print((e**2) / (4 * pi * varepsilon_0 * M_e * c**2))
print((e**2) / (8 * pi * varepsilon_0 * F_max * R_c))

print("\ne: ",e) ################################################
print(math.sqrt(16 * pi * F_max * R_c**2) / (mu_0 * c**2)) ################################################
print(math.sqrt(2 * alpha * h) / (mu_0 * c)) ################################################
print(math.sqrt(4 * C_e * h) / (mu_0 * c**2)) ################################################

print("\nL_p: ",L_p) ###########################################
print(math.sqrt(h * G / c**3)) ###########################################
print(math.sqrt((alpha_g * h * R_c) / (C_e * M_e))) ###########################################
print(math.sqrt((h * t_p**2 * C_e * c**2) / (2 * F_max * R_c**2))) ###########################################

print("\nalpha_g: ",alpha_g)
print((2 * F_max * C_e * t_p**2) / ((2 * F_max * R_c**2) / C_e))
print((C_e**2 * t_p**2) / (R_c**2))
print((F_max * 2 * C_e * t_p**2) / h)  ###########################################
print((F_max * t_p**2) / (A_0 * M_e))
print((C_e * c**2 * t_p**2 * M_e) / (h * R_c)) ###########################################
print((C_e**2 * L_p**2) / (R_c**2 * c**2))

print("\nG: ",G)
print((C_e * c**3 * L_p**2) / (2 * F_max * R_c**2))
print((C_e * c**3 * t_p**2) / (R_c * M_e))
print((F_max * alpha * (c * t_p)**2) / (M_e**2))
print((C_e * c * L_p**2) / (R_c * M_e))
print((alpha_g * c**3 * R_c) / (C_e * M_e))
print((C_e * c**5 * t_p**2) / (2 * F_max * R_c**2))

print("\nalpha: ", alpha)
print((h / (4 * pi * R_c))) ###########################################
print((C_e * e**2) / (8 * pi * varepsilon_0 * R_c**2 * c * F_max))
print((h / (4 * pi * R_c))) ###########################################
print((lambda_c * R_c) / (2 * C_e)) ###########################################

print("\nlambda_c: ",lambda_c)
print((2 * pi * c * R_c) / C_e)
print((4 * pi * F_max * R_c**2) / (C_e * M_e * c))

print("\nC_e: ",C_e)
print(c * (alpha/2))
print(h / (2 * pi * M_e * R_c))

print("\nR_c: ",R_c)
print(R_e / 2)

print("\nF_Cmax: ",F_Cmax)
print((c**4 / (4 * G)) * alpha * (R_c / L_p)**-2)
print((M_e * C_e**2) / R_c) ###########################################
print((h * alpha * c) / (8 * pi * R_c**2))
print(e**2 / (16 * pi * varepsilon_0 * R_c**2))
print((mu_v / (4 * math.pi)) * ((mu_v * omega) ** 2 / r_c**2))
print((mu_v / (4 * math.pi)) * ((mu_v * (2 * C_e / r_c)) ** 2 / r_c**2))

print("\nh: ",h)
print(4 * pi * M_e * C_e * A_0)
print((pi * F_max * R_e**2) / C_e)
print((96 * pi * F_max**2 * R_c**3 * A_0) / (h * c**2))

print("\nR_infinity: ",R_)
print((C_e**3) / (pi * R_c * c**3))



# Vortex Energy and Entropy Density
def vortex_energy_density(r, omega, T):
    return (F_Cmax * omega**3) / (C_e * r**2) / (math.exp(h * omega / (k_B * T)) - 1)

def vortex_entropy_density(r, T):
    return (4 * pi**4 * F_Cmax * k_B**4 * T**3) / (45 * C_e * r**2 * h**4)

def vortex_flux_density(r, T):
    return (pi**4 * F_Cmax * k_B**4 * T**4) / (15 * h**4 * r)

def total_energy(T, r):
    return (F_Cmax * T**4) / (C_e * r**2)

def total_entropy(T, r):
    return (F_Cmax * T**3) / (C_e * r**2)



