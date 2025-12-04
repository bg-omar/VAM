import math
from pylatex import Document, Section, Tabular, NoEscape, Package


class SSTConstant:
    def __init__(self, latex, value, unit, quantity, uncertainty):
        self.latex = latex
        self.value = value
        self.unit = unit
        self.quantity = quantity
        self.uncertainty = uncertainty

    def __repr__(self):
        return f"{self.latex} = {self.value} {self.unit} ({self.quantity}, Uncertainty: {self.uncertainty})"
# Dictionary of physical constants
sst_constants = {
    "C_e": SSTConstant(r"C_e", 1093845.63, "m s^-1", "Vortex-Tangential-Velocity", "exact"),
    "rhoMass": SSTConstant(r"\rho_\text{\ae}^\text{(mass)}",  3.8934358266918687e+18, "kg m^-3", "Æther Mass-Equivalent Density", "exact"),
    "rhoFluid": SSTConstant(r"\rho_\text{\ae}^\text{(fluid)}",  7.0e-7, "kg m^-3", "Æther Fluid Vacuum Density", "exact"),
    "rhoEnergy": SSTConstant(r"\rho_\text{\ae}^\text{(energy)}",  3.49924562e+35, "J m^-3", "Æther Energy Density", "exact"),
    "F_max": SSTConstant(r"F_\text{\ae}^\text{max}", 29.053507, "N", "Maximum force", "exact"),
    "r_c": SSTConstant(r"r_c", 1.40897017e-15, "m", "Vortex-Core radius", "exact"),
    "F_Coulomb": SSTConstant(r"F_\text{Coulomb}", 29.053507, "N", "Maximum Coulomb Force", "exact"),
    "F_GRmax": SSTConstant(r"F_\text{gr}^\text{max}", 3.0256389108455157e+43, "N", "Maximum Universal Force", "exact"),
    "c": SSTConstant(r"c", 299792458, "m s^-1", "Speed of light in vacuum", "exact"),
    "G": SSTConstant(r"G", 6.67430e-11, "m^3 kg^-1 s^-2", "Newtonian constant of gravitation", "2.2e-5"),
    "h": SSTConstant(r"h", 6.62607015e-34, "J Hz^-1", "Planck constant", "exact"),
    "alpha": SSTConstant(r"\alpha", 7.2973525643e-3, "", "Fine-structure constant", "1.6e-10"),
    "R_c": SSTConstant(r"r_c", 1.40897017e-15, "m", "Coulomb barrier", "exact"),
    "R_e": SSTConstant(r"R_e", 2.8179403262e-15, "m", "Classical electron radius", "1.3e-24"),
    "alpha_g": SSTConstant(r"\alpha_g", 1.7518e-45, "", "Gravitational coupling constant", "exact"),
    "mu_0": SSTConstant(r"\mu_0", 4 * math.pi * 1e-7, "N A^-2", "Vacuum magnetic permeability", "exact"),
    "varepsilon_0": SSTConstant(r"\varepsilon_0", 1 / (4 * math.pi * 1e-7 * (299792458)**2), "F m^-1", "Vacuum electric permittivity", "exact"),
    "Z_0": SSTConstant(r"Z_0", 376.730313412, "Ω", "Characteristic impedance of vacuum", "1.6e-10"),
    "hbar": SSTConstant(r"\hbar", 1.054571817e-34, "J s", "Reduced Planck constant", "exact"),
    "L_p": SSTConstant(r"L_p", 1.616255e-35, "m", "Planck length", "1.1e-5"),
    "M_p": SSTConstant(r"M_p", 2.176434e-8, "kg", "Planck mass", "1.1e-5"),
    "t_p": SSTConstant(r"t_p", 5.391247e-44, "s", "Planck time", "1.1e-5"),
    "T_p": SSTConstant(r"T_p", 1.416784e32, "K", "Planck temperature", "1.1e-5"),
    "e": SSTConstant(r"e", 1.602176634e-19, "C", "Elementary charge", "exact"),
    "R_": SSTConstant(r"R_\infty", 10973731.568157, "m^-1", "Rydberg constant", "1.1e-12"),
    "a_0": SSTConstant(r"a_0", 5.29177210903e-11, "m", "Bohr radius", "1.6e-10"),
    "M_e": SSTConstant(r"M_e", 9.1093837015e-31, "kg", "Electron mass", "3.1e-10"),
    "M_pr": SSTConstant(r"M_{proton}", 1.67262192369e-27, "kg", "Proton mass", "3.1e-10"),
    "M_n": SSTConstant(r"M_{neutron}", 1.67492749804e-27, "kg", "Neutron mass", "5.1e-10"),
    "k_B": SSTConstant(r"k_B", 1.380649e-23, "J K^-1", "Boltzmann constant", "exact"),
    "R": SSTConstant(r"R", 8.314462618, "J mol^-1 K^-1", "Gas constant", "exact"),
    "alpha-1": SSTConstant(r"\frac{1}{\alpha}", 137.035999084, "", "Fine structure constant reciprocal", "1.6e-10"),
    "f_c": SSTConstant(r"f_c", 1.235589965e20, "m", "Compton frequency of the electron", "1.0e-10"),
    "omega_c": SSTConstant(r"\Omega_c", 7.763440711e20, "m", "Compton angular frequency of the electron", "1.0e-10"),
    "lambda_c": SSTConstant(r"\lambda_c", 2.42631023867e-12, "m", "Compton wavelength of the electron", "1.0e-10"),
    "Phi_0": SSTConstant(r"\Phi_0", 2.067833848e-15, "Wb", "Magnetic flux quantum", "exact"),
    "varphi": SSTConstant(r"\varphi", 1.618033988, "", "Golden ratio (Fibonacci constant)", "7.3e-22"),
    "eV": SSTConstant(r"eV", 1.602176634e-19, "J", "Electron volt", "exact"),
    "G_F": SSTConstant(r"G_F", 0.000011663787, "GeV^-2", "Fermi coupling constant", "6e-12"),
    "lambda_p": SSTConstant(r"\lambda_{proton}", 1.32140985539e-15, "m", "Proton Compton wavelength", "4e-25"),
    "q_p": SSTConstant(r"q_p", 1.87554595641e-18, "C", "Planck charge", "exact"),
    "E_p": SSTConstant(r"E_p", 1.956e9, "J", "Planck energy", "exact"),
    "ER_": SSTConstant(r"ER_\infty", 2.1798723611035e-18, "J", "Rydberg energy (in joules)", "1.1e-12"),
    "fR_": SSTConstant(r"fR_\infty", 3.2898419602508e15, "Hz", "Rydberg frequency", "1.1e-12"),
    "sigma": SSTConstant(r"\sigma", 5.670374419e-8, "W m^-2 K^-4", "Stefan-Boltzmann constant", "exact"),
    "b": SSTConstant(r"b", 2.897771955e-3, "m K", "Wien displacement constant", "exact"),
    "k_e": SSTConstant(r"k_e", 8.9875517862e9, "N m^2 C^-2", "Coulomb constant", "exact")
}
C_e = sst_constants["C_e"].value # Vortex-Core Tangential Velocity (m/s)
R_c = sst_constants["R_c"].value
r_c = sst_constants["r_c"].value  # Coulomb barrier (m)
rhoMass = sst_constants["rhoMass"].value
rhoEnergy = sst_constants["rhoEnergy"].value
rhoFluid = sst_constants["rhoFluid"].value
F_max = sst_constants["F_max"].value
varepsilon_0 = sst_constants["varepsilon_0"].value
F_GRmax = sst_constants["F_GRmax"].value
F_Cmax = sst_constants["F_Coulomb"].value  # Maximum force (N)
c = sst_constants["c"].value
G = sst_constants["G"].value
h = sst_constants["h"].value
alpha = sst_constants["alpha"].value   # Fine-structure constant
R_e = sst_constants["R_e"].value
f_c = sst_constants["f_c"].value
omega_c = sst_constants["omega_c"].value
lambda_c = sst_constants["lambda_c"].value
alpha_g = sst_constants["alpha_g"].value
mu_0 = sst_constants["mu_0"].value  # Vacuum permeability (N/A^2)
Z_0 = sst_constants["Z_0"].value
hbar = sst_constants["hbar"].value
L_p = sst_constants["L_p"].value
M_p = sst_constants["M_p"].value
t_p = sst_constants["t_p"].value # Planck time (s)
T_p = sst_constants["T_p"].value # Planck Temperature (s)
e = sst_constants["e"].value
R_ = sst_constants["R_"].value
a_0 = sst_constants["a_0"].value # Bohr radius (m)
M_e = sst_constants["M_e"].value # Electron mass (kg)
M_pr = sst_constants["M_pr"].value
M_n = sst_constants["M_n"].value
k_B = sst_constants["k_B"].value
R = sst_constants["R"].value
alpha_1 = sst_constants["alpha-1"].value
Phi_0 = sst_constants["Phi_0"].value
varphi = sst_constants["varphi"].value
eV = sst_constants["eV"].value
G_F = sst_constants["G_F"].value
lambda_p = sst_constants["lambda_p"].value
q_p = sst_constants["q_p"].value
E_p = sst_constants["E_p"].value
ER_ = sst_constants["ER_"].value
fR_ = sst_constants["fR_"].value
sigma = sst_constants["sigma"].value
b = sst_constants["b"].value
pi = math.pi


# # Create a LaTeX document
# doc = Document("physical_constants_latex")
#
# doc.append(NoEscape(r"""
# \begin{table}[H]
#     \centering
#     \footnotesize
#     \raggedright
#     \renewcommand{\arraystretch}{1.2}
#     \begin{tabular}{|p{1.5cm}|p{6cm}|p{2.5cm}|p{2cm}|p{2cm}|}
#         \hline
#         \textbf{Symbol} & \textbf{Quantity} & \textbf{Value} & \textbf{Unit} & \textbf{Uncertainty} \\
#         \hline
# """))
#
# for const in sst_constants.values():
#     latex_clean = const.latex.replace(r"\ae", r"\text{\ae}")
#     row = rf"${latex_clean}$ & {const.quantity} & {const.value:.8e} & {const.unit.replace('Ω', r'\Omega')} & {const.uncertainty} \\ \hline"
#     doc.append(NoEscape(row))
#
# doc.append(NoEscape(r"""
#     \end{tabular}
#     \caption{Table of physical constants used in the Vortex Æther Model (VAM).}
#     \label{tab:physical_constants}
# \end{table}
# """))
#
# latex_pdf_path = "physical_constants_latex.pdf"
# doc.packages.append(Package("float"))  # For [H]
# doc.packages.append(Package('fancyhdr'))
# doc.append(NoEscape(r"\small"))
# doc.preamble.append(NoEscape(r'\pagestyle{fancy}'))
# doc.preamble.append(NoEscape(r'\fancyhf{}'))
# doc.generate_pdf(latex_pdf_path.replace(".pdf", ""), clean_tex=False, compiler='pdflatex')
#