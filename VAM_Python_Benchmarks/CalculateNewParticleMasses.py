import math
import pandas as pd

# Constants from NIST and VAM (blended source)
constants = {
    "rho_ae": 3.893e18,  # kg/m^3, VAM æther density
    "r_c": 1.40897017e-15,  # m, vortex core radius (from VAM)
    "C_e": 1.09384563e6,  # m/s, VAM swirl velocity

    # Particle masses (from CODATA 2018)
    "m_e": 9.1093837015e-31,  # kg, electron
    "m_p": 1.67262192369e-27,  # kg, proton
    "m_n": 1.67492749804e-27,  # kg, neutron
    "m_mu": 1.883531627e-28,  # kg, muon
    "m_tau": 3.16754e-27,  # kg, tau
    "m_u": 2.2e-30,  # kg, up quark (estimate)
    "m_d": 4.7e-30,  # kg, down quark (estimate)
    "m_c": 1.27e-27,  # kg, charm quark
    "m_s": 9.6e-29,  # kg, strange quark
    "m_t": 2.89e-25,  # kg, top quark
    "m_b": 4.18e-27,  # kg, bottom quark
}

# Core prefactor for mass formula
def mass_prefactor(rho_ae, r_c, C_e):
    return (8 * math.pi * rho_ae * r_c**3) / C_e

prefactor = mass_prefactor(constants["rho_ae"], constants["r_c"], constants["C_e"])

# Model: M(p,q) = A * (sqrt(p^2 + q^2) + gamma(p,q) * pq)
def helicity_mass(p, q, gamma_func):
    gamma = gamma_func(p, q)
    return prefactor * (math.sqrt(p**2 + q**2) + gamma * p * q)

# Logarithmic gamma model (tunable)
def gamma_logarithmic(p, q, eta=0.0055, zeta=0.0012, xi=0.15):
    return eta + zeta * math.log1p(xi * p * q)

# Compute masses for a few candidates
candidates = {
    "m_e": (2, 3),
    "m_p": (410, 615),
    "m_mu": (4, 12),
    "m_tau": (6, 30),
    "m_u": (1, 2),
    "m_d": (1, 3),
}

results = []
for name, (p, q) in candidates.items():
    model_mass = helicity_mass(p, q, gamma_logarithmic)
    exp_mass = constants.get(f"{name.lower()}", None)
    error = ((model_mass - exp_mass) / exp_mass) * 100 if exp_mass else None
    results.append({
        "Particle": name,
        "T(p,q)": f"T({p},{q})",
        "Model Mass (kg)": model_mass,
        "Exp Mass (kg)": exp_mass,
        "Error (%)": error
    })

df = pd.DataFrame(results)
import ace_tools_open as tools; tools.display_dataframe_to_user(name="VAM Helicity Mass Predictions", dataframe=df)
