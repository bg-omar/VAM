#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SST_MASTER_MASS.py
Author: Omar Iskandarani
Date: 2025-08-25

Purpose
-------
A clean, canonical implementation of the Swirl-String Theory (SST) master
mass equation, structured similarly to VAM-MASS_FORMULA.py but grounded
strictly in the Canon "master equation".

Master Equation (Canon)
-----------------------
Let the swirl energy density be
    u = (1/2) * ρ * v_swirl^2                                        (Eq. 0)

The SST master mass mapping is
    M = (4/α) * φ^{-1} * ( u * V ) / c^2                            (Eq. 1)

i.e.,
    M = (4 / α) * (1/φ) * ( (1/2) * ρ * v_swirl^2 * V ) / c^2       (Eq. 1')

Symbols:
- ρ        : effective density scale (choose 'fluid' or 'core'; default 'core')
- v_swirl  : characteristic swirl speed (Canon: v_swirl ≈ 1.09384563e6 m/s)
- V        : geometric/topological volume associated to the object
- α        : fine-structure constant
- φ        : golden ratio
- c        : speed of light

Geometry
--------
For convenience we use a torus volume for elementary building blocks:
    V_torus(R, r) = 2 π^2 R r^2                                     (Eq. 2)
with major radius R and minor radius r. By Canon convention we set
r = r_c (core radius), and allow R = κ_R * r_c with κ_R ≈ 2 by default.

Calibration Strategy
--------------------
The absolute product (ρ, v_swirl, V) in Eq. (1') depends on the
effective density choice and geometric modeling. To keep the model
strictly Canon-compatible yet useful, we:
1) keep Eq. (1') fixed,
2) use Canon constants for ρ and v_swirl,
3) define a *dimensionless* topological factor s_e for the electron volume:
       V_e = s_e * V_torus(R=κ_R r_c, r=r_c).
   We determine s_e by requiring M_e(pred) = M_e(actual). This fixes the
   overall geometric normalization for the chosen (ρ, v_swirl, κ_R).

Once s_e is fixed, we predict baryons by assembling volumes from
dimensionless factors (s_u, s_d, ...) multiplied by the same base torus.
Defaults for (s_u, s_d) are provided but can be edited.

Output
------
- Pretty-printed table (p, n, e, selected atoms/molecules)
- CSV file: SST_Mass_Results.csv

Units & Dimensional Check
-------------------------
- u = (1/2) ρ v^2 has units [J/m^3]. u*V has [J]. Division by c^2 gives [kg].
- The prefactor (4/α)*(1/φ) is dimensionless.

References (BibTeX)
-------------------
@article{Einstein1905,
  author    = {Albert Einstein},
  title     = {Ist die Trägheit eines Körpers von seinem Energieinhalt abhängig?},
  journal   = {Annalen der Physik},
  volume    = {323},
  number    = {13},
  pages     = {639--641},
  year      = {1905},
  doi       = {10.1002/andp.19053231314}
}

@book{Batchelor1967,
  author    = {G. K. Batchelor},
  title     = {An Introduction to Fluid Dynamics},
  publisher = {Cambridge University Press},
  year      = {1967}
}

@book{Saffman1992,
  author    = {P. G. Saffman},
  title     = {Vortex Dynamics},
  publisher = {Cambridge University Press},
  year      = {1992}
}

@article{CODATA2018,
  author    = {P. J. Mohr and D. B. Newell and B. N. Taylor},
  title     = {CODATA Recommended Values of the Fundamental Physical Constants: 2018},
  journal   = {Reviews of Modern Physics},
  volume    = {88},
  pages     = {035009},
  year      = {2016},
  doi       = {10.1103/RevModPhys.88.035009}
}

Notes: Eq. (1) is Canon; Eq. (2) is standard geometry. For the usages of .fseries in the Canon papers, see https://david.fremlin.de/knots/index.htm.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

import pandas as pd


# ──────────────────────────────────────────────────────────────────────────────
# Constants (Canon-aligned)
# ──────────────────────────────────────────────────────────────────────────────
phi: float = (1 + math.sqrt(5)) / 2                         # φ
alpha_fs: float = 7.2973525643e-3                           # fine-structure constant
c: float = 299_792_458.0                                    # m/s
v_swirl: float = 1.093_845_63e6                             # m/s  (Canon v_{⟲})
r_c: float = 1.408_970_17e-15                               # m    (core radius)

# Effective density options (Canon values)
rho_fluid: float = 7.0e-7                                   # kg/m^3
rho_core: float  = 3.8934358266918687e18                    # kg/m^3

# Physical reference masses (for calibration and error tables)
M_e_actual: float = 9.109_383_7015e-31                      # kg
M_p_actual: float = 1.672_621_923_69e-27                    # kg
M_n_actual: float = 1.674_927_498_04e-27                    # kg

avogadro: float = 6.022_140_76e23                           # 1/mol


# ──────────────────────────────────────────────────────────────────────────────
# Geometry utilities
# ──────────────────────────────────────────────────────────────────────────────
def torus_volume(R: float, r: float) -> float:
    """V_torus = 2 π^2 R r^2  (Eq. 2)"""
    return 2.0 * math.pi**2 * R * (r**2)


# ──────────────────────────────────────────────────────────────────────────────
# Master equation implementation (Eq. 1')
# ──────────────────────────────────────────────────────────────────────────────
def swirl_energy_density(rho: float, v: float = v_swirl) -> float:
    """u = (1/2) ρ v^2  [J/m^3]  (Eq. 0)"""
    return 0.5 * rho * v * v


def master_mass(volume: float,
                rho: float = rho_core,
                v: float = v_swirl,
                alpha: float = alpha_fs,
                golden_phi: float = phi) -> float:
    """
    M = (4/α) * (1/φ) * ( (1/2) ρ v^2 * V ) / c^2   (Eq. 1')
    Returns mass in kg.
    """
    u = swirl_energy_density(rho, v)
    return (4.0 / alpha) * (1.0 / golden_phi) * (u * volume) / (c * c)


# ──────────────────────────────────────────────────────────────────────────────
# Model configuration
# ──────────────────────────────────────────────────────────────────────────────
@dataclass
class SSTConfig:
    kappa_R: float = 2.0              # R = kappa_R * r_c
    rho_choice: str = "core"          # "core" or "fluid"
    s_u: float = 2.8281               # dimensionless up-factor  (editable)
    s_d: float = 3.1639               # dimensionless down-factor (editable)

    @property
    def rho(self) -> float:
        if self.rho_choice == "core":
            return rho_core
        elif self.rho_choice == "fluid":
            return rho_fluid
        else:
            raise ValueError("rho_choice must be 'core' or 'fluid'")

    @property
    def V_base(self) -> float:
        """Base torus at (R=κ_R r_c, r=r_c)."""
        return torus_volume(self.kappa_R * r_c, r_c)


# ──────────────────────────────────────────────────────────────────────────────
# Calibration (fix s_e so that electron matches exactly)
# ──────────────────────────────────────────────────────────────────────────────
def calibrate_s_e(cfg: SSTConfig) -> float:
    """
    Solve for s_e from M_e(actual) = master_mass( s_e * V_base, rho ).
    s_e = M_e * c^2 * φ * α / ( 4 * (1/2) ρ v^2 * V_base ).
    """
    u = swirl_energy_density(cfg.rho, v_swirl)
    numerator = M_e_actual * c * c * phi * alpha_fs
    denom = 4.0 * u * cfg.V_base
    return numerator / denom


# ──────────────────────────────────────────────────────────────────────────────
# Assembly helpers for composite objects
# ──────────────────────────────────────────────────────────────────────────────
def electron_mass(cfg: SSTConfig, s_e: float) -> float:
    return master_mass(s_e * cfg.V_base, rho=cfg.rho)


def proton_mass(cfg: SSTConfig, s_e: float) -> float:
    # Proton: uud  → 2*u + 1*d building volumes (scaled from same base)
    V_p = (2.0 * cfg.s_u + 1.0 * cfg.s_d) * cfg.V_base
    return master_mass(V_p, rho=cfg.rho)


def neutron_mass(cfg: SSTConfig, s_e: float) -> float:
    # Neutron: udd → 1*u + 2*d
    V_n = (1.0 * cfg.s_u + 2.0 * cfg.s_d) * cfg.V_base
    return master_mass(V_n, rho=cfg.rho)


# ──────────────────────────────────────────────────────────────────────────────
# Tabulation
# ──────────────────────────────────────────────────────────────────────────────
def emoji_marker(diff_pct: float) -> str:
    d = abs(diff_pct)
    if d < 1: icon = "🩷🡅"
    elif d < 2.5: icon = "🟢🡅"
    elif d < 10: icon = "🟡🡅"
    elif d < 25: icon = "🟠🡅"
    else: icon = "🔴🡅"
    if diff_pct < 0: icon = icon.replace("🡅", "🡇")
    if diff_pct == 0: icon = "●"
    return f"{diff_pct:.2f}% {icon}"


# basic set (symbol, protons, neutrons, electrons, molar mass [g/mol])
ATOMS_MOLS: List[Tuple[str, int, int, int, float]] = [
    ("H", 1, 0, 1, 1.00784), ("He", 2, 2, 2, 4.002602), ("Li", 3, 4, 3, 6.94), ("Be", 4, 5, 4, 9.0122),
    ("B", 5, 6, 5, 10.81), ("C", 6, 6, 6, 12.011), ("N", 7, 7, 7, 14.0067), ("O", 8, 8, 8, 15.999),
    ("F", 9, 10, 9, 18.998), ("Ne", 10, 10, 10, 20.18), ("Na", 11, 12, 11, 22.989769), ("Mg", 12, 12, 12, 24.305),
    ("Al", 13, 14, 13, 26.9815385), ("Si", 14, 14, 14, 28.085), ("P", 15, 16, 15, 30.973762), ("S", 16, 16, 16, 32.06),
    ("Cl", 17, 18, 17, 35.45), ("Ar", 18, 22, 18, 39.948), ("K", 19, 20, 19, 39.0983), ("Ca", 20, 20, 20, 40.078),
    ("Sc", 21, 24, 21, 44.955), ("Ti", 22, 26, 22, 47.867), ("V", 23, 28, 23, 50.942), ("Cr", 24, 28, 24, 51.996),
    ("Mn", 25, 30, 25, 54.938), ("Fe", 26, 30, 26, 55.845), ("Co", 27, 32, 27, 58.933), ("Ni", 28, 31, 28, 58.693),
    ("Cu", 29, 35, 29, 63.546), ("Zn", 30, 35, 30, 65.38), ("Ga", 31, 39, 31, 69.723), ("Ge", 32, 41, 32, 72.63),
    ("As", 33, 42, 33, 74.922), ("Se", 34, 45, 34, 78.971), ("Br", 35, 45, 35, 79.904), ("Kr", 36, 48, 36, 83.798),
    ("Rb", 37, 48, 37, 85.468), ("Sr", 38, 50, 38, 87.62), ("Y", 39, 50, 39, 88.906), ("Zr", 40, 51, 40, 91.224),
    ("Nb", 41, 52, 41, 92.906), ("Mo", 42, 54, 42, 95.95), ("Tc", 43, 55, 43, 98.0), ("Ru", 44, 57, 44, 101.07),
    ("Rh", 45, 58, 45, 102.91), ("Pd", 46, 60, 46, 106.42), ("Ag", 47, 61, 47, 107.87), ("Cd", 48, 64, 48, 112.41),
    ("In", 49, 66, 49, 114.82), ("Sn", 50, 69, 50, 118.71), ("Sb", 51, 71, 51, 121.76), ("Te", 52, 76, 52, 127.6),
    ("I", 53, 74, 53, 126.90447), ("Xe", 54, 77, 54, 131.29),
    # some molecules
    ("H2O", 10, 8, 10, 18.015), ("CO2", 22, 22, 22, 44.01), ("O2", 16, 16, 16, 31.9988), ("N2", 14, 14, 14, 28.0134),
    ("CH4", 10, 10, 10, 16.04), ("C6H12O6", 72, 72, 72, 180.16), ("NH3", 10, 10, 10, 17.0305), ("HCl", 18, 18, 18, 36.46),
]


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
def compute_tables(cfg: SSTConfig) -> pd.DataFrame:
    s_e = calibrate_s_e(cfg)

    M_e_pred = electron_mass(cfg, s_e)
    M_p_pred = proton_mass(cfg, s_e)
    M_n_pred = neutron_mass(cfg, s_e)

    # Elementary rows
    rows: List[Tuple[str, float, float, str]] = []
    rows.append(("Electron", M_e_pred, M_e_actual,
                 emoji_marker(100.0 * (M_e_pred - M_e_actual) / M_e_actual)))
    rows.append(("Proton", M_p_pred, M_p_actual,
                 emoji_marker(100.0 * (M_p_pred - M_p_actual) / M_p_actual)))
    rows.append(("Neutron", M_n_pred, M_n_actual,
                 emoji_marker(100.0 * (M_n_pred - M_n_actual) / M_n_actual)))

    # Atoms & molecules
    for name, p, n, e, gmol in ATOMS_MOLS:
        actual_kg = gmol * 1e-3 / avogadro
        predicted = p * M_p_pred + n * M_n_pred + e * M_e_pred
        rel_error = 100.0 * (predicted - actual_kg) / actual_kg
        rows.append((name, predicted, actual_kg, emoji_marker(rel_error)))

    df = pd.DataFrame(rows, columns=["Object", "Predicted Mass (kg)", "Actual Mass (kg)", "% Error"])
    return df


def main() -> None:
    cfg = SSTConfig(
        kappa_R=2.0,        # R = 2 r_c
        rho_choice="core",  # use 'core' density to match Canon usage in prior work
        s_u=2.8281,
        s_d=3.1639,
    )

    print("=== SST Master Mass (Canon) ===")
    print(f"phi = {phi:.12f}")
    print(f"alpha_fs = {alpha_fs:.12e}")
    print(f"c = {c:.3f} m/s")
    print(f"v_swirl = {v_swirl:.5e} m/s")
    print(f"r_c = {r_c:.5e} m")
    print(f"rho(core) = {rho_core:.6e} kg/m^3, rho(fluid) = {rho_fluid:.6e} kg/m^3")
    print(f"kappa_R = {cfg.kappa_R}, V_base = {cfg.V_base:.5e} m^3")

    s_e = calibrate_s_e(cfg)
    print(f"Calibrated s_e (dimensionless electron volume factor) = {s_e:.6e}")

    df = compute_tables(cfg)
    pd.set_option("display.float_format", lambda x: f"{x:.6e}\" if isinstance(x, float) else str(x))")
    print(df.to_string(index=False))

    out_csv = "SST_Mass_Results.csv"
    df.to_csv(out_csv, index=False)
    print(f"\\nSaved results to {out_csv}")


if __name__ == "__main__":
    main()
