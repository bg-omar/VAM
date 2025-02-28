import math
import scipy.constants as const
import math
import random

class PhysicalConstant:
    """
    A class to store physical constants with LaTeX representation, value, units, and uncertainty.
    """
    def __init__(self, latex, value, unit, quantity, uncertainty):
        self.latex = latex
        self.value = value
        self.unit = unit
        self.quantity = quantity
        self.uncertainty = uncertainty

    def __repr__(self):
        return f"{self.latex} = {self.value} {self.unit} ({self.quantity}, Uncertainty: {self.uncertainty})"

# Æther Density with Dynamic Selection
def get_dynamic_rho_ae(method="midpoint"):
    """
    Returns a dynamically chosen value for the Æther density constant.

    Parameters:
        method (str): "min", "max", "midpoint", or "random".
                      - "min": Returns the lower bound.
                      - "max": Returns the upper bound.
                      - "midpoint": Returns the geometric mean of the range.
                      - "random": Returns a random value within the range.

    Returns:
        PhysicalConstant: A PhysicalConstant object for \rho_{\text{\ae}}.
    """
    rho_min = 5.0e-8   # Lower bound
    rho_max = 5.0e-5   # Upper bound

    if method == "min":
        rho_value = rho_min
    elif method == "max":
        rho_value = rho_max
    elif method == "midpoint":
        rho_value = (rho_min * rho_max) ** 0.5  # Geometric mean
    elif method == "random":
        rho_value = random.uniform(rho_min, rho_max)
    else:
        raise ValueError("Invalid method. Choose 'min', 'max', 'midpoint', or 'random'.")

    return PhysicalConstant(r"\rho_\text{\ae}", rho_value, "kg m^-3", "Æther density", f"Range: {rho_min} to {rho_max} kg m^-3")

# Dictionary of physical constants
constants_dict = {
    "C_e": PhysicalConstant(r"C_e", 1093845.63, "m s^-1", "Vortex-Tangential-Velocity", "exact"),
    "rho_ae": get_dynamic_rho_ae("midpoint"),
    "F_max": PhysicalConstant(r"F_{\text{max}}", 29.053507, "N", "Maximum force", "exact"),
    "F_Coulomb": PhysicalConstant(r"F_{\text{Coulomb}}", 29.053507, "N", "Maximum Coulomb Force", "exact"),
    "c": PhysicalConstant(r"c", 299792458, "m s^-1", "Speed of light in vacuum", "exact"),
    "G": PhysicalConstant(r"G", 6.67430e-11, "m^3 kg^-1 s^-2", "Newtonian constant of gravitation", "2.2e-5"),
    "h": PhysicalConstant(r"h", 6.62607015e-34, "J Hz^-1", "Planck constant", "exact"),
    "alpha": PhysicalConstant(r"\alpha", 7.2973525643e-3, "", "Fine-structure constant", "1.6e-10"),
    "R_c": PhysicalConstant(r"R_c", 1.40897017e-15, "m", "Coulomb barrier", "exact"),
    "r_c": PhysicalConstant(r"r_c", 1.40897017e-15, "m", "Vortex-Core radius", "exact"),
    "R_e": PhysicalConstant(r"R_e", 2.8179403262e-15, "m", "Classical electron radius", "1.3e-24"),
    "alpha_g": PhysicalConstant(r"\alpha_g", 1.7518e-45, "", "Gravitational coupling constant", "exact"),
    "mu_0": PhysicalConstant(r"\mu_0", 4 * math.pi * 1e-7, "N A^-2", "Vacuum magnetic permeability", "exact"),
    "varepsilon_0": PhysicalConstant(r"\varepsilon_0", 1 / (4 * math.pi * 1e-7 * (299792458)**2), "F m^-1", "Vacuum electric permittivity", "exact"),
    "Z_0": PhysicalConstant(r"Z_0", 376.730313412, "Ω", "Characteristic impedance of vacuum", "1.6e-10"),
    "hbar": PhysicalConstant(r"\hbar", 1.054571817e-34, "J s", "Reduced Planck constant", "exact"),
    "L_p": PhysicalConstant(r"L_p", 1.616255e-35, "m", "Planck length", "1.1e-5"),
    "M_p": PhysicalConstant(r"M_p", 2.176434e-8, "kg", "Planck mass", "1.1e-5"),
    "t_p": PhysicalConstant(r"t_p", 5.391247e-44, "s", "Planck time", "1.1e-5"),
    "T_p": PhysicalConstant(r"T_p", 1.416784e32, "K", "Planck temperature", "1.1e-5"),
    "e": PhysicalConstant(r"e", 1.602176634e-19, "C", "Elementary charge", "exact"),
    "R_": PhysicalConstant(r"R_\infty", 10973731.568157, "m^-1", "Rydberg constant", "1.1e-12"),
    "A_0": PhysicalConstant(r"A_0", 5.29177210903e-11, "m", "Bohr radius", "1.6e-10"),
    "M_e": PhysicalConstant(r"M_e", 9.1093837015e-31, "kg", "Electron mass", "3.1e-10"),
    "M_pr": PhysicalConstant(r"M_{proton}", 1.67262192369e-27, "kg", "Proton mass", "3.1e-10"),
    "M_n": PhysicalConstant(r"M_{neutron}", 1.67492749804e-27, "kg", "Neutron mass", "5.1e-10"),
    "k_B": PhysicalConstant(r"k_B", 1.380649e-23, "J K^-1", "Boltzmann constant", "exact"),
    "R": PhysicalConstant(r"R", 8.314462618, "J mol^-1 K^-1", "Gas constant", "exact"),
    "alpha-1": PhysicalConstant(r"\frac{1}{\alpha}", 137.035999084, "", "Fine structure constant reciprocal", "1.6e-10"),
    "lambda_c": PhysicalConstant(r"\lambda_c", 2.42631023867e-12, "m", "Compton wavelength of the electron", "1.0e-10"),
    "Phi_0": PhysicalConstant(r"\Phi_0", 2.067833848e-15, "Wb", "Magnetic flux quantum", "exact"),
    "varphi": PhysicalConstant(r"\varphi", 1.618033988, "", "Golden ratio (Fibonacci constant)", "7.3e-22"),
    "eV": PhysicalConstant(r"eV", 1.602176634e-19, "J", "Electron volt", "exact"),
    "G_F": PhysicalConstant(r"G_F", 0.000011663787, "GeV^-2", "Fermi coupling constant", "6e-12"),
    "lambda_p": PhysicalConstant(r"\lambda_{proton}", 1.32140985539e-15, "m", "Proton Compton wavelength", "4e-25"),
    "q_p": PhysicalConstant(r"q_p", 1.87554595641e-18, "C", "Planck charge", "exact"),
    "E_p": PhysicalConstant(r"E_p", 1.956e9, "J", "Planck energy", "exact"),
    "ER_": PhysicalConstant(r"ER_\infty", 2.1798723611035e-18, "J", "Rydberg energy (in joules)", "1.1e-12"),
    "fR_": PhysicalConstant(r"fR_\infty", 3.2898419602508e15, "Hz", "Rydberg frequency", "1.1e-12"),
    "sigma": PhysicalConstant(r"\sigma", 5.670374419e-8, "W m^-2 K^-4", "Stefan-Boltzmann constant", "exact"),
    "b": PhysicalConstant(r"b", 2.897771955e-3, "m K", "Wien displacement constant", "exact")
}


C_e = constants_dict["C_e"].value
rho_ae = constants_dict["rho_ae"].value
F_max = constants_dict["F_max"].value
F_Coulomb = constants_dict["F_Coulomb"].value
c = constants_dict["c"].value
G = constants_dict["G"].value
h = constants_dict["h"].value
alpha = constants_dict["alpha"].value
R_c = constants_dict["R_c"].value
r_c = constants_dict["r_c"].value
R_e = constants_dict["R_e"].value
alpha_g = constants_dict["alpha_g"].value
mu_0 = constants_dict["mu_0"].value
varepsilon_0 = constants_dict["varepsilon_0"].value
Z_0 = constants_dict["Z_0"].value
hbar = constants_dict["hbar"].value
L_p = constants_dict["L_p"].value
M_p = constants_dict["M_p"].value
t_p = constants_dict["t_p"].value
T_p = constants_dict["T_p"].value
e = constants_dict["e"].value
R_ = constants_dict["R_"].value
A_0 = constants_dict["A_0"].value
M_e = constants_dict["M_e"].value
M_pr = constants_dict["M_pr"].value
M_n = constants_dict["M_n"].value
k_B = constants_dict["k_B"].value
R = constants_dict["R"].value
alpha_1 = constants_dict["alpha-1"].value
lambda_c = constants_dict["lambda_c"].value
Phi_0 = constants_dict["Phi_0"].value
varphi = constants_dict["varphi"].value
eV = constants_dict["eV"].value
G_F = constants_dict["G_F"].value
lambda_p = constants_dict["lambda_p"].value
q_p = constants_dict["q_p"].value
E_p = constants_dict["E_p"].value
ER_ = constants_dict["ER_"].value
fR_ = constants_dict["fR_"].value
sigma = constants_dict["sigma"].value
b = constants_dict["b"].value

# Define the physical constants again manually


R_pr = 1.32140985539e-15  # Proton Compton wavelength (m)

c = const.c  # Speed of light (m/s)
R_infinity = const.Rydberg  # Rydberg constant (1/m)

# Given values

# Compute v_v^2
v_v_squared = 4 / (rho_ae * r_c**2)

E_p = R_infinity * hbar * c

# Compute v_v
v_v = math.sqrt(v_v_squared)

import scipy.constants as sc

# Constants from quantum mechanics

Me = sc.electron_mass  # Electron mass (kg)
c = sc.c  # Speed of light (m/s)

import numpy as np

# Physical Constants
m_e = 9.10938356e-31  # Electron mass (kg)
pi = np.pi            # Pi constant

r_t = 2.8179403227e-15   # Classical electron radius (m) or use Compton wavelength

# Vorticity Magnitude Estimate
omega = 1e23  # Typical vorticity (1/s), refine if needed

# Calculate Æther Density
rho_aether = (m_e * c**2) / (pi**2 * A_0 * R_e**2 * omega**2)

# Print result
print(f"Aether Density (ρ_æ): {rho_aether:.3e} kg/m³")


# Compute Proton Compton Wavelength
lambda_C_p = h / (M_pr * c)  # Proton Compton wavelength (m)

# Compute Proton Compton Angular Frequency
omega_C_p = c / lambda_C_p  # Proton Compton angular frequency (1/s)



# Calculate Æther Density using toroidal formula
rho_aether = (m_e * c**2) / (pi**2 * A_0 * R_e**2 * omega_C_p**2)
rho_aether = (m_e * c**2) / (pi**2 * R_c * R_c**2 * (c/lambda_c)**2)
# Print results
print(f"Proton Compton Wavelength: {lambda_C_p:.3e} m")
print(f"Proton Compton Angular Frequency (ω_C_p): {omega_C_p:.3e} s⁻¹")
print(f"Aether Density (ρ_æ): {rho_aether:.3e} kg/m³")


# Vortex Æther Model constants (approximate values, to be refined)

rho_ae_value = (hbar**2) / (2 * F_max * r_c * lambda_c**2)
print("rho_ae_value: ", rho_ae_value)

# Compute LHS of first equation: Quantum kinetic energy scale
lhs_qm = hbar**2 / (2 * Me)

# Compute RHS of first equation: Vortex model energy scale
rhs_vam = (F_max * R_c**3) / (5 * lambda_c * C_e)

# Compute ratio to check agreement
ratio = lhs_qm / rhs_vam

print("lhs_qm: ",lhs_qm,  "rhs_vam: ", rhs_vam, "ratio: ", ratio)

# Solve for mu_v using the relationship: mu_v = (4 * E_p) / (9 * C_e^4 * R_c^5)
# We need to express C_e from the Rydberg formula
C_e = ((R_infinity * r_c * c**3 * const.pi) ** (1/3))  # Solve for C_e
print("C_e: ", C_e)
# Compute mu_v using derived formula
mu_v = (4 * E_p) / (9 * C_e**4 * R_c**5)


print("v_v^2:", v_v_squared)
print("v_v:", v_v)

# Print without scientific notation
print("v_v^2:", format(v_v_squared, ',.0f'))
print("v_v:", format(v_v, ',.0f'))

print("mu_v:", mu_v)

# Compute rho_AE using the given formula
rho_AE = (4 * mu_v) / (R_c**2)

# Display the computed density of the Æther
print(rho_AE)

k = (hbar * c) / (4 * const.pi**3  * r_c**2 * C_e * c**3)
print("k:", k)