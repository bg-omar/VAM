#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SST_INVARIANT_MASS.py
Author: Omar Iskandarani
Date: 2025-08-25

Purpose
-------
A canonical, topology-driven implementation of the Swirl-String Theory (SST)
Invariant Master Mass Formula with selectable modes:

- exact_closure (default): auto-fit (s_u, s_d) so that proton & neutron are exact.
- canonical: single electron calibration only; fixed (s_u, s_d) from hyperbolic volumes.
- sector_norm: one baryon-sector normalization λ_b; proton exact, neutron predicted.

Invariant Master Formula (Canon)
--------------------------------
The mass M for a particle represented by a topology T is given by:
    M(T) = (4/α) * b(T)^(-3/2) * φ^(-g(T)) * n(T)^(-1/φ)
           * [ (1/2)ρ_core * v_swirl^2 ] * [ π * r_c^3 * L_tot(T) ] / c^2

Symbols: α (fine-structure), φ (golden ratio), ρ_core, v_swirl, r_c, c,
         b(T) braid index, g(T) Seifert genus, n(T) components, L_tot ropelength.

Calibration Strategy
--------------------
- Electron-only geometric calibration fixes L_tot(e) exactly (all modes).
- Baryon ropelength mapping: L_tot = scaling_factor * Σ s_i, scaling_factor = 2 π^2 κ_R.
- Mode determines how (s_u, s_d) and/or a sector λ_b are chosen.

References (BibTeX)
-------------------
@misc{SST_Canon_v0.3.0,
  author       = {Omar Iskandarani},
  title        = {Swirl String Theory (SST) Canon v0.3.0},
  year         = {2025},
  doi          = {10.5281/zenodo.16934536}
}
@misc{VAM_Canon_v0.4,
  author     = {Omar Iskandarani},
  title      = {VAM Canon (v0.4)},
  year       = {2025}
}
@misc{VAM_Master_Formula_v8.5,
  author     = {Omar Iskandarani},
  title      = {The Vortex Æther Model (VAM): Master Mass Formula},
  year       = {2025},
  doi        = {10.5281/zenodo.15849355}
}
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

import pandas as pd
import re

# ──────────────────────────────────────────────────────────────────────────────
# Constants (Canon-aligned)
# ──────────────────────────────────────────────────────────────────────────────
phi: float = (1 + math.sqrt(5)) / 2  # φ
alpha_fs: float = 7.2973525643e-3  # fine-structure constant
c: float = 299_792_458.0  # m/s
v_swirl: float = 1.093_845_63e6  # m/s  (Canon v_s)
r_c: float = 1.408_970_17e-15  # m    (core radius r_c or r_s)

# Effective density options (Canon values)
rho_fluid: float = 7.0e-7  # kg/m^3 (background)
rho_core: float = 3.8934358266918687e18  # kg/m^3 (mass-equivalent)

# Physical reference masses (for calibration and error tables)
M_e_actual: float = 9.109_383_7015e-31  # kg
M_p_actual: float = 1.672_621_923_69e-27  # kg
M_n_actual: float = 1.674_927_498_04e-27  # kg

avogadro: float = 6.022_140_76e23  # 1/mol


# ──────────────────────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────────────────────
@dataclass
class Config:
    mode: str = "exact_closure"  # "exact_closure" | "canonical" | "sector_norm"
    kappa_R: float = 2.0
    fixed_su: float = 2.8281
    fixed_sd: float = 3.1639


# ──────────────────────────────────────────────────────────────────────────────
# Data Structures for Topology
# ──────────────────────────────────────────────────────────────────────────────
@dataclass
class KnotTopology:
    """Stores the topological and geometric invariants for a particle."""
    name: str
    b: int  # Braid Index
    g: int  # Seifert Genus
    n: int  # Number of Components
    L_tot: float  # Total Ropelength


# ──────────────────────────────────────────────────────────────────────────────
# Invariant Master Formula Implementation
# ──────────────────────────────────────────────────────────────────────────────
def master_mass_invariant(
        topo: KnotTopology,
        rho: float = rho_core,
        v: float = v_swirl,
        alpha: float = alpha_fs,
        golden_phi: float = phi
) -> float:
    """
    M(T) = (4/α) * b⁻³/² * φ⁻ᵍ * n⁻¹/φ * ( (1/2)ρ v² ) * (π r_c³ L_tot) / c²
    Returns mass in kg.
    """
    u = 0.5 * rho * v * v  # [J/m^3]

    amplification = 4.0 / alpha
    braid_suppression = topo.b ** -1.5
    genus_suppression = golden_phi ** -topo.g
    component_suppression = topo.n ** (-1.0 / golden_phi)

    volume = math.pi * (r_c ** 3) * topo.L_tot  # [m^3]

    total_mass = (
        amplification *
        braid_suppression *
        genus_suppression *
        component_suppression *
        (u * volume) / (c * c)
    )
    return total_mass


# ──────────────────────────────────────────────────────────────────────────────
# Calibration helpers
# ──────────────────────────────────────────────────────────────────────────────
def calibrate_L_tot_electron(electron_topo_base: KnotTopology) -> float:
    """Solve for L_tot(e) so that M_e(pred) = M_e_actual. Single geometric calibration."""
    u = 0.5 * rho_core * v_swirl ** 2
    prefactor = (
        (4.0 / alpha_fs) *
        (electron_topo_base.b ** -1.5) *
        (phi ** -electron_topo_base.g) *
        (electron_topo_base.n ** (-1.0 / phi))
    )
    volume_prefactor = math.pi * (r_c ** 3)
    numerator = M_e_actual * (c ** 2)
    denominator = prefactor * u * volume_prefactor
    return numerator / denominator


def baryon_prefactor(b: int, g: int, n: int,
                     rho: float = rho_core, v: float = v_swirl,
                     alpha: float = alpha_fs, golden_phi: float = phi) -> float:
    """
    Return A such that for baryons M = A * L_tot (with L_tot dimensionless ropelength).
    A = (4/α) * b^{-3/2} * φ^{-g} * n^{-1/φ} * [ (1/2)ρ v^2 * (π r_c^3) / c^2 ].
    """
    u = 0.5 * rho * v * v
    return (4.0/alpha) * (b ** -1.5) * (golden_phi ** -g) * (n ** (-1.0/golden_phi)) * (u * math.pi * (r_c**3)) / (c*c)


def fit_quark_geom_factors_for_baryons(b: int, g: int, n: int, scaling_factor: float) -> tuple[float, float]:
    """
    Fit (s_u, s_d) so that proton and neutron match CODATA masses exactly.
    With M = A_baryon * scaling_factor * (Σ s_i), and:
        M_p = K * (2 s_u +   s_d)
        M_n = K * (  s_u + 2 s_d)
      where K = A_baryon * scaling_factor.
    Solve analytically:
        s_u = (2 M_p - M_n) / (3 K)
        s_d = (M_p / K) - 2 s_u
    """
    A = baryon_prefactor(b, g, n)
    K = A * scaling_factor
    s_u = (2.0 * M_p_actual - M_n_actual) / (3.0 * K)
    s_d = (M_p_actual / K) - 2.0 * s_u
    return float(s_u), float(s_d)


# ──────────────────────────────────────────────────────────────────────────────
# Assembly helpers for composite objects
# ──────────────────────────────────────────────────────────────────────────────
def get_particle_topologies(cfg: Config) -> Dict:
    """
    Define canonical topologies and ropelengths per mode.
    """
    # Electron base topology (e.g., Solomon link sector)
    electron_base = KnotTopology(name="Electron_base", b=2, g=1, n=1, L_tot=0.0)
    l_tot_e = calibrate_L_tot_electron(electron_base)

    # Baryon invariants (uud/udd sector)
    b_bary, g_bary, n_bary = 3, 2, 3
    scaling_factor = 2.0 * (math.pi ** 2) * cfg.kappa_R  # dimensionless

    A_bary = baryon_prefactor(b_bary, g_bary, n_bary)
    K = A_bary * scaling_factor

    # Choose (s_u, s_d) and λ_b by mode
    lam_b = 1.0
    if cfg.mode == "canonical":
        s_u, s_d = cfg.fixed_su, cfg.fixed_sd
    elif cfg.mode == "sector_norm":
        s_u, s_d = cfg.fixed_su, cfg.fixed_sd
        lam_b = M_p_actual / (K * (2.0 * s_u + s_d))  # enforce proton exact
    else:  # "exact_closure" (default)
        s_u, s_d = fit_quark_geom_factors_for_baryons(b_bary, g_bary, n_bary, scaling_factor)

    l_tot_p = lam_b * (2.0 * s_u + 1.0 * s_d) * scaling_factor
    l_tot_n = lam_b * (1.0 * s_u + 2.0 * s_d) * scaling_factor

    topologies = {
        "electron": KnotTopology(name="Electron", b=2, g=1, n=1, L_tot=l_tot_e),
        "proton":   KnotTopology(name="Proton",  b=b_bary, g=g_bary, n=n_bary, L_tot=l_tot_p),
        "neutron":  KnotTopology(name="Neutron", b=b_bary, g=g_bary, n=n_bary, L_tot=l_tot_n),
    }

    # Diagnostics for printing
    topologies["_diag"] = {
        "mode": cfg.mode, "kappa_R": cfg.kappa_R, "scaling_factor": scaling_factor,
        "A_bary": A_bary, "K": K, "lambda_b": lam_b, "s_u": s_u, "s_d": s_d
    }
    return topologies


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


# Note: Extended periodic table entries as provided by user
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
    ("I", 53, 74, 53, 126.90447), ("Xe", 54, 77, 54, 131.29), ("Cs", 55, 78, 55, 132.91), ("Ba", 56, 81, 56, 137.33),
    ("La", 57, 82, 57, 138.91), ("Ce", 58, 82, 58, 140.12), ("Pr", 59, 82, 59, 140.91), ("Nd", 60, 84, 60, 144.24),
    ("Pm", 61, 84, 61, 145.0), ("Sm", 62, 88, 62, 150.36), ("Eu", 63, 89, 63, 151.96), ("Gd", 64, 93, 64, 157.25),
    ("Tb", 65, 94, 65, 158.93), ("Dy", 66, 97, 66, 162.5), ("Ho", 67, 98, 67, 164.93), ("Er", 68, 99, 68, 167.26),
    ("Tm", 69, 100, 69, 168.93), ("Yb", 70, 103, 70, 173.05), ("Lu", 71, 104, 71, 174.97), ("Hf", 72, 106, 72, 178.49),
    ("Ta", 73, 108, 73, 180.95), ("W", 74, 110, 74, 183.84), ("Re", 75, 111, 75, 186.21), ("Os", 76, 114, 76, 190.23),
    ("Ir", 77, 115, 77, 192.22), ("Pt", 78, 117, 78, 195.08), ("Au", 79, 118, 79, 196.97), ("Hg", 80, 121, 80, 200.59),
    ("Tl", 81, 123, 81, 204.38), ("Pb", 82, 125, 82, 207.2), ("Bi", 83, 126, 83, 208.98), ("Po", 84, 125, 84, 209.0),
    ("At", 85, 125, 85, 210.0), ("Rn", 86, 136, 86, 222.0), ("Fr", 87, 136, 87, 223.0), ("Ra", 88, 138, 88, 226.0),
    ("Ac", 89, 138, 89, 227.0), ("Th", 90, 142, 90, 232.04), ("Pa", 91, 140, 91, 231.04), ("U", 92, 146, 92, 238.03),
]

# Supported molecules with their molar masses (g/mol), computed via stoichiometry
MOLECULES: Dict[str, float] = {
    "H2O": 18.015, "CO2": 44.01, "O2": 31.9988, "N2": 28.0134,
    "CH4": 16.04, "C6H12O6": 180.16, "NH3": 17.0305, "HCl": 36.46,
    "C2H2": 26.04, "NaCl": 58.44, "CaCO3": 100.0869, "C2H6": 30.07,
    "C2H4": 28.05, "C8H18": 114.23, "C6H6": 78.11, "CH3COOH": 60.052,
    "H2SO4": 98.079, "C12H22O11": 342.30, "Caffeine": 194.19
    # "DNA (avg)" excluded (no fixed stoichiometry)
}


# ──────────────────────────────────────────────────────────────────────────────
# Stoichiometry helpers
# ──────────────────────────────────────────────────────────────────────────────
def _elements_from_table() -> Dict[str, tuple[int,int,int,float]]:
    """Map element symbol -> (protons, neutrons, electrons, molar_mass_gmol)."""
    elements = {}
    for name, p, n, e, gmol in ATOMS_MOLS:
        if name.isalpha() and len(name) <= 2:
            elements[name] = (p, n, e, gmol)
    return elements


def _parse_formula(formula: str) -> Dict[str, int]:
    """Simple formula parser without parentheses. e.g., C6H12O6, CH3COOH."""
    if formula.lower() == "caffeine":
        # C8H10N4O2
        return {"C":8,"H":10,"N":4,"O":2}
    tokens = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    counts: Dict[str, int] = {}
    for sym, num in tokens:
        k = int(num) if num else 1
        counts[sym] = counts.get(sym, 0) + k
    return counts


# ──────────────────────────────────────────────────────────────────────────────
# Main table
# ──────────────────────────────────────────────────────────────────────────────
def compute_tables(topologies: Dict, cfg: Config) -> pd.DataFrame:
    M_e_pred = master_mass_invariant(topologies["electron"])
    M_p_pred = master_mass_invariant(topologies["proton"])
    M_n_pred = master_mass_invariant(topologies["neutron"])

    rows: List[Tuple[str, float, float, str]] = []
    rows.append(("Electron", M_e_pred, M_e_actual, emoji_marker(100.0*(M_e_pred-M_e_actual)/M_e_actual)))
    rows.append(("Proton",   M_p_pred, M_p_actual, emoji_marker(100.0*(M_p_pred-M_p_actual)/M_p_actual)))
    rows.append(("Neutron",  M_n_pred, M_n_actual, emoji_marker(100.0*(M_n_pred-M_n_actual)/M_n_actual)))

    # Elements from table
    elements = _elements_from_table()
    for name, (pZ, nN, eE, gmol) in elements.items():
        actual_kg = gmol * 1e-3 / avogadro
        predicted = pZ * M_p_pred + nN * M_n_pred + eE * M_e_pred
        rel_error = 100.0 * (predicted - actual_kg) / actual_kg
        rows.append((name, predicted, actual_kg, emoji_marker(rel_error)))

    # Molecules via stoichiometry
    for mol, gmol in MOLECULES.items():
        counts = _parse_formula(mol)
        pred = 0.0
        missing = False
        for sym, k in counts.items():
            if sym not in elements:
                missing = True
                break
            pZ, nN, eE, _ = elements[sym]
            pred += k * (pZ * M_p_pred + nN * M_n_pred + eE * M_e_pred)
        if missing:
            continue
        actual_kg = gmol * 1e-3 / avogadro
        rel_error = 100.0 * (pred - actual_kg) / actual_kg
        rows.append((mol, pred, actual_kg, emoji_marker(rel_error)))

    df = pd.DataFrame(rows, columns=["Object","Predicted Mass (kg)","Actual Mass (kg)","% Error"])
    return df


def main(mode: str = "exact_closure") -> None:
    print("=== SST Invariant Master Mass (Canon) ===")
    cfg = Config(mode=mode)

    topologies = get_particle_topologies(cfg)
    diag = topologies["_diag"]

    print("\n--- Mode & Model Parameters ---")
    print(f"mode = {diag['mode']}  |  kappa_R = {diag['kappa_R']:.6g}")
    print(f"s_u = {diag['s_u']:.6f}, s_d = {diag['s_d']:.6f}, lambda_b = {diag['lambda_b']:.6f}")
    print(f"A_bary = {diag['A_bary']:.6e},  K = {diag['K']:.6e}")
    print(f"scaling_factor = {diag['scaling_factor']:.6f}")

    print("\n--- Particle Topological & Geometric Invariants ---")
    for key in ["electron","proton","neutron"]:
        p = topologies[key]
        print(f"{p.name:<10}: b={p.b}, g={p.g}, n={p.n}, L_tot={p.L_tot:.6f}")

    df = compute_tables(topologies, cfg)

    print("\n--- Mass Prediction Results ---")
    pd.set_option("display.float_format", lambda x: f"{x:.6e}" if isinstance(x, float) else str(x))
    print(df.head(20).to_string(index=False))

    out_csv = "SST_Invariant_Mass_Results.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nSaved results to {out_csv}")


if __name__ == "__main__":
    # Allow a quick CLI mode override: python SST_INVARIANT_MASS.py canonical
    import sys
    arg_mode = sys.argv[1] if len(sys.argv) > 1 else "exact_closure"
    main(arg_mode)