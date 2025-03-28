
import pandas as pd
import math
import ace_tools_open as tools
from constants import *

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


# Constants
M_sun = 1.98847e30  # kg

def schwarzschild_precession(M, a, e):
    return (6 * math.pi * G * M) / (a * (1 - e**2) * c**2)

def shapiro_delay(M, r1, r2, b):
    return (2 * G * M / c**3) * math.log((4 * r1 * r2) / b**2)

def light_deflection(M, R):
    return (4 * G * M) / (R * c**2)

def isco_radius(M, a=0):
    return 6 * G * M / c**2  # Schwarzschild case

def gw_inspiral_period_derivative(m1, m2, a):
    μ = m1 * m2 / (m1 + m2)
    M = m1 + m2
    return -(192 * math.pi * G**(5/3) * μ * M**(2/3)) / (5 * c**5 * a**(5/2))

def geodetic_precession(M, R, v_orbit):
    return (3 * G * M * v_orbit) / (2 * c**2 * R**2)

def lense_thirring_precession(J, R):
    return (2 * G * J) / (c**2 * R**3)

def flrw_cosmological_redshift(a_emit, a_obs=1.0):
    return (a_obs / a_emit) - 1

def flrw_scale_factor_from_z(z):
    return 1 / (1 + z)

def orbital_time_dilation(mass, radius, J):
    Omega_K = math.sqrt(G * mass / radius**3)
    Omega_LT = (2 * G * J) / (c**2 * radius**3)
    Omega = Omega_K - Omega_LT

    g_tt = -(1 - (2 * G * mass) / (radius * c**2))
    g_tphi = - (2 * G * J) / (radius * c**3)
    g_phiphi = radius**2

    term = g_tt + 2 * g_tphi * Omega + g_phiphi * Omega**2
    return math.sqrt(term) if term > 0 else float('nan'), Omega, Omega_LT

def compute_gr_properties(name, mass, radius, J=None, rotation_freq=None):
    if J is None and rotation_freq is not None:
        omega = 2 * math.pi * rotation_freq
        I = (2 / 5) * mass * radius**2
        J = I * omega


def build_gr_table():
    # Constants (assumes already defined)
    global G, c, M_sun

    # Reuse your existing computation functions:
    vam_table = {
        "Perihelion Precession (Mercury)": {
            "C (Computed)": schwarzschild_precession(M_sun, 5.79e10, 0.2056),  # rad/orbit
            "A (Analytical)": 5.018e-7,
            "M (Measured)": 5.035e-7,
            "Units": "rad/orbit",
            "Source (M)": "https://doi.org/10.1007/BF01327326"
        },
        "Shapiro Delay (Sun)": {
            "C (Computed)": shapiro_delay(M_sun, 1.5e11, 1.5e11, 6.9634e8),
            "A (Analytical)": 2.47e-4,
            "M (Measured)": 2.38e-4,
            "Units": "s",
            "Source (M)": "https://doi.org/10.1103/PhysRevLett.92.121101"
        },
        "Light Deflection (Solar Limb)": {
            "C (Computed)": math.degrees(light_deflection(M_sun, 6.9634e8)) * 3600,
            "A (Analytical)": 1.75,
            "M (Measured)": 1.751,
            "Units": "arcsec",
            "Source (M)": "https://ui.adsabs.harvard.edu/abs/2009IAUS..261..311F/abstract"
        },
        "ISCO Radius (Schwarzschild)": {
            "C (Computed)": isco_radius(M_sun),
            "A (Analytical)": 6 * G * M_sun / c**2,
            "M (Measured)": None,
            "Units": "m",
            "Source (M)": "Theoretical prediction"
        },
        "GW Period Derivative (Binary NS)": {
            "C (Computed)": gw_inspiral_period_derivative(1.4 * M_sun, 1.4 * M_sun, 7.5e8),
            "A (Analytical)": -2.4e-12,
            "M (Measured)": -2.4e-12,
            "Units": "s/s",
            "Source (M)": "https://doi.org/10.1086/309335"
        },
        "Geodetic Precession (LEO)": {
            "C (Computed)": geodetic_precession(5.972e24, 6.371e6 + 400e3, 7660),
            "A (Analytical)": 1.9e-12,
            "M (Measured)": 1.8e-12,
            "Units": "rad/s",
            "Source (M)": "https://doi.org/10.1103/PhysRevLett.106.221101"
        },
        "Lense–Thirring (Earth LEO)": {
            "C (Computed)": lense_thirring_precession(7.07e33, 6.371e6 + 400e3),
            "A (Analytical)": 2.0e-14,
            "M (Measured)": 3.03e-14,
            "Units": "rad/s",
            "Source (M)": "https://doi.org/10.1038/nature01997"
        },
        "FLRW z (a=0.5)": {
            "C (Computed)": flrw_cosmological_redshift(0.5),
            "A (Analytical)": 1.0,
            "M (Measured)": 1.0,
            "Units": "-",
            "Source (M)": "Cosmological models"
        },
        "FLRW a (z=3)": {
            "C (Computed)": flrw_scale_factor_from_z(3),
            "A (Analytical)": 0.25,
            "M (Measured)": 0.25,
            "Units": "-",
            "Source (M)": "Standard FLRW relation"
        }
    }

    df_vam = pd.DataFrame(vam_table).transpose()

    # Optional error metric:
    df_vam["% Error (V vs M)"] = df_vam.apply(
        lambda row: (
            abs(row["C (Computed)"] - row["M (Measured)"]) / abs(row["M (Measured)"]) * 100
            if pd.notnull(row["M (Measured)"]) and row["M (Measured)"] != 0 else None
        ),
        axis=1
    )
    # Reorder columns to put % Error before Source
    ordered_cols = [
        "C (Computed)", "A (Analytical)", "M (Measured)", "Units",
        "% Error (V vs M)", "Source (M)"
    ]
    df_vam = df_vam[ordered_cols]
    return df_vam


pd.set_option('display.float_format', '\t{:.8e}'.format)
df_tests = build_gr_table()
tools.display_dataframe_to_user(name="Canonical GR Predictions", dataframe=df_tests)