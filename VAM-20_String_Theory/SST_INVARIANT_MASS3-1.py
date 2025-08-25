#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SST_INVARIANT_MASS.py
Author: Omar Iskandarani
Date: 2025-08-25

Purpose
-------
A canonical, topology-driven implementation of the Swirl-String Theory (SST)
Invariant Master Mass Formula, structured similarly to VAM-MASS_FORMULA.py but
grounded strictly in the Canon “master equation”. The script provides three
calculation modes (see below) that change only topological-to-geometry inputs;
the invariant kernel is identical in all modes.

Modes (Computation Paths)
-------------------------
- exact_closure (default): fits the dimensionless quark geometry factors (s_u, s_d)
  analytically so that the **proton and neutron** masses are matched exactly, while
  preserving the electron-only geometric calibration. No extra scaling beyond
  the Canon kernel is introduced.
- canonical: strict Canon evaluation with a **single** electron calibration (fixes L_tot(e)).
  Uses fixed (s_u, s_d) from hyperbolic-volume assignments; **no** baryon-sector
  rescaling. Nucleon residuals reflect the direct Canon mapping.
- sector_norm: keeps fixed (s_u, s_d) as in canonical, but introduces a **single**
  baryon-sector normalization λ_b to make the **proton** exact; the neutron is predicted.

What changes across modes?
--------------------------
Only the **geometric inputs** to L_tot(T) for baryons:
1) The invariant kernel
       M(T) = (4/α)·b(T)^{-3/2}·φ^{-g(T)}·n(T)^{-1/φ} · [ (1/2)ρ_core v_swirl^2 ] · [ π r_c^3 L_tot(T) ] / c^2      (Eq. K)
   is fixed and identical in all modes.
2) The baryon ropelength mapping uses
       L_tot = scaling_factor · Σ s_i,   with   scaling_factor = 2 π^2 κ_R,   κ_R ≈ 2.                          (Eq. L)
   - **exact_closure**: (s_u, s_d) are solved from M_p, M_n using (Eq. K–L).
   - **canonical**: (s_u, s_d) are fixed constants (from hyperbolic volumes).
   - **sector_norm**: (s_u, s_d) fixed as canonical, and a single λ_b multiplies L_tot
     in the baryon sector so that M_p is exact.

Master Equation (Canon)
-----------------------
Define the swirl energy density
    u = (1/2) ρ v_swirl^2.                                                                               (Eq. 0)

The SST mass mapping can be written compactly as
    M = (4/α) · φ^{-1} · (u · V) / c^2,                                                                  (Eq. 1)
i.e.
    M = (4/α) · (1/φ) · [ (1/2) ρ v_swirl^2 · V ] / c^2.                                                 (Eq. 1′)

Here V is the effective geometric/topological volume associated with the object.
In the invariant kernel actually used in code (Eq. K), V = π r_c^3 L_tot(T) with
L_tot a **dimensionless ropelength** set by topology and the mode-specific mapping (Eq. L).

Symbols:
- α          : fine-structure constant
- φ          : golden ratio
- ρ, ρ_core  : effective density scale (default: ρ = ρ_core)
- v_swirl    : characteristic swirl speed (Canon: v_swirl ≈ 1.09384563×10^6 m/s)
- r_c        : core radius of the swirl string
- c          : speed of light
- b(T)       : braid index
- g(T)       : Seifert genus
- n(T)       : number of components
- L_tot(T)   : total ropelength (dimensionless)

Geometry
--------
A convenient reference geometry is the torus volume
    V_torus(R, r) = 2 π^2 R r^2,                                                                         (Eq. 2)
with r set to r_c and R = κ_R r_c (κ_R ≈ 2). The ropelength proxy used by the
Canon kernel (Eq. K) is V = π r_c^3 L_tot, consistent with dimensionless L_tot.

Calibration Strategy
--------------------
- Electron-only geometric calibration: determine L_tot(e) so that the model exactly
  reproduces M_e(actual). This fixes the absolute geometry scale for all modes.
- Baryons: assemble L_tot via (Eq. L). Depending on mode, (s_u, s_d) are either
  solved (exact_closure) or taken as fixed (canonical/sector_norm). In sector_norm
  a single λ_b multiplies baryon L_tot to make the proton exact.

Outputs
-------
- Console table with columns:
      Object, Actual Mass (kg), Predicted Mass (kg), % Error
- CSV: SST_Invariant_Mass_Results.csv
- Optional cross-mode comparison (interactive prompt) appends:
      Predicted Mass (kg) [CANON], % Error [CANON],
      Predicted Mass (kg) [Sector Norm], % Error [Sector Norm]
  to SST_Invariant_Mass_Results_all_modes.csv.

Units & Dimensional Check
-------------------------
- u = (1/2) ρ v_swirl^2 has units [J/m^3]; u·V has [J]; division by c^2 gives [kg].
- The factors (4/α), φ^{-g(T)}, n(T)^{-1/φ}, b(T)^{-3/2} are dimensionless.

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
phi: float = (1 + math.sqrt(5)) / 2
alpha_fs: float = 7.2973525643e-3
c: float = 299_792_458.0
v_swirl: float = 1.093_845_63e6
r_c: float = 1.408_970_17e-15
rho_core: float = 3.8934358266918687e18
avogadro: float = 6.022_140_76e23

# Physical reference masses (CODATA 2018)
M_e_actual: float = 9.109_383_7015e-31   # Electron
M_mu_actual: float = 1.883_531_627e-28   # Muon
M_tau_actual: float = 3.167_54e-27       # Tau
M_p_actual: float = 1.672_621_923_69e-27   # Proton
M_n_actual: float = 1.674_927_498_04e-27   # Neutron


# ──────────────────────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────────────────────
@dataclass
class Config:
    mode: str = "exact_closure"
    kappa_R: float = 2.0
    fixed_su: float = 2.8281
    fixed_sd: float = 3.1639


# ──────────────────────────────────────────────────────────────────────────────
# Data Structures for Topology
# ──────────────────────────────────────────────────────────────────────────────
@dataclass
class KnotTopology:
    name: str
    b: int  # Braid Index
    g: int  # Seifert Genus
    n: int  # Number of Components
    L_tot: float  # Total Ropelength


# ──────────────────────────────────────────────────────────────────────────────
# Invariant Master Formula
# ──────────────────────────────────────────────────────────────────────────────
def master_mass_invariant(topo: KnotTopology) -> float:
    u = 0.5 * rho_core * v_swirl * v_swirl
    amplification = 4.0 / alpha_fs
    braid_suppression = topo.b ** -1.5
    genus_suppression = phi ** -topo.g
    component_suppression = topo.n ** (-1.0 / phi)
    volume = math.pi * (r_c ** 3) * topo.L_tot
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
def solve_for_L_tot(mass_actual: float, topo_base: KnotTopology) -> float:
    """Generic function to solve for L_tot given a known mass and base topology."""
    u = 0.5 * rho_core * v_swirl ** 2
    prefactor = (
            (4.0 / alpha_fs) *
            (topo_base.b ** -1.5) *
            (phi ** -topo_base.g) *
            (topo_base.n ** (-1.0 / phi))
    )
    volume_prefactor = math.pi * (r_c ** 3)
    numerator = mass_actual * (c ** 2)
    denominator = prefactor * u * volume_prefactor
    return numerator / denominator


def baryon_prefactor(b: int, g: int, n: int) -> float:
    u = 0.5 * rho_core * v_swirl * v_swirl
    return (4.0/alpha_fs) * (b ** -1.5) * (phi ** -g) * (n ** (-1.0/phi)) * (u * math.pi * (r_c**3)) / (c*c)


def fit_quark_geom_factors_for_baryons(b: int, g: int, n: int, scaling_factor: float) -> tuple[float, float]:
    A = baryon_prefactor(b, g, n)
    K = A * scaling_factor
    s_u = (2.0 * M_p_actual - M_n_actual) / (3.0 * K)
    s_d = (M_p_actual / K) - 2.0 * s_u
    return float(s_u), float(s_d)


# ──────────────────────────────────────────────────────────────────────────────
# Assembly helpers
# ──────────────────────────────────────────────────────────────────────────────
def get_particle_topologies(cfg: Config) -> Dict:
    # Lepton Generation Calibration
    electron_base = KnotTopology(name="Electron_base", b=2, g=1, n=1, L_tot=0.0)
    muon_base = KnotTopology(name="Muon_base (5_1)", b=5, g=2, n=1, L_tot=0.0)
    tau_base = KnotTopology(name="Tau_base (7_1)", b=7, g=3, n=1, L_tot=0.0)

    l_tot_e = solve_for_L_tot(M_e_actual, electron_base)
    l_tot_mu = solve_for_L_tot(M_mu_actual, muon_base)
    l_tot_tau = solve_for_L_tot(M_tau_actual, tau_base)

    # Baryon Sector Calibration
    b_bary, g_bary, n_bary = 3, 2, 3
    scaling_factor = 2.0 * (math.pi ** 2) * cfg.kappa_R
    A_bary = baryon_prefactor(b_bary, g_bary, n_bary)
    K = A_bary * scaling_factor
    lam_b = 1.0

    if cfg.mode == "canonical":
        s_u, s_d = cfg.fixed_su, cfg.fixed_sd
    elif cfg.mode == "sector_norm":
        s_u, s_d = cfg.fixed_su, cfg.fixed_sd
        lam_b = M_p_actual / (K * (2.0 * s_u + s_d))
    else: # exact_closure
        s_u, s_d = fit_quark_geom_factors_for_baryons(b_bary, g_bary, n_bary, scaling_factor)

    l_tot_p = lam_b * (2.0 * s_u + 1.0 * s_d) * scaling_factor
    l_tot_n = lam_b * (1.0 * s_u + 2.0 * s_d) * scaling_factor

    topologies = {
        "electron": KnotTopology(name="Electron", b=2, g=1, n=1, L_tot=l_tot_e),
        "muon":     KnotTopology(name="Muon (5_1)", b=5, g=2, n=1, L_tot=l_tot_mu),
        "tau":      KnotTopology(name="Tau (7_1)", b=7, g=3, n=1, L_tot=l_tot_tau),
        "proton":   KnotTopology(name="Proton",  b=b_bary, g=g_bary, n=n_bary, L_tot=l_tot_p),
        "neutron":  KnotTopology(name="Neutron", b=b_bary, g=g_bary, n=n_bary, L_tot=l_tot_n),
        "_diag": {
            "mode": cfg.mode, "kappa_R": cfg.kappa_R, "scaling_factor": scaling_factor,
            "A_bary": A_bary, "K": K, "lambda_b": lam_b, "s_u": s_u, "s_d": s_d
        }
    }
    return topologies



# ──────────────────────────────────────────────────────────────────────────────
# Tabulation
# ──────────────────────────────────────────────────────────────────────────────
def emoji_marker(diff_pct: float) -> str:
    d = abs(diff_pct)
    if d < 0.01: return f"{diff_pct:.3f}% 🩷️"
    if d < 1: icon = "❤️🡅"
    elif d < 2.5: icon = "🟢🡅"
    elif d < 10: icon = "🟡🡅"
    elif d < 25: icon = "🟠🡅"
    else: icon = "🔴🡅"
    if diff_pct < 0: icon = icon.replace("🡅", "🡇")
    if diff_pct == 0: icon = "🩷"
    return f"{diff_pct:.2f}% {icon}"


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

MOLECULES: Dict[str, float] = {
    "H2O": 18.015, "CO2": 44.01, "O2": 31.9988, "N2": 28.0134,
    "CH4": 16.04, "C6H12O6": 180.16, "NH3": 17.0305, "HCl": 36.46,
    "C2H2": 26.04, "NaCl": 58.44, "CaCO3": 100.0869, "C2H6": 30.07,
    "C2H4": 28.05, "C8H18": 114.23, "C6H6": 78.11, "CH3COOH": 60.052,
    "H2SO4": 98.079, "C12H22O11": 342.30, "Caffeine": 194.19
}


def _elements_from_table() -> Dict[str, tuple[int,int,int,float]]:
    elements = {}
    for name, p, n, e, gmol in ATOMS_MOLS:
        if name.isalpha() and len(name) <= 2:
            elements[name] = (p, n, e, gmol)
    return elements

def _parse_formula(formula: str) -> Dict[str, int]:
    tokens = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    counts: Dict[str, int] = {}
    for sym, num in tokens:
        k = int(num) if num else 1
        counts[sym] = counts.get(sym, 0) + k
    return counts

def compute_tables(topologies: Dict, cfg: Config) -> pd.DataFrame:
    M_e_pred = master_mass_invariant(topologies["electron"])
    M_p_pred = master_mass_invariant(topologies["proton"])
    M_n_pred = master_mass_invariant(topologies["neutron"])

    rows: List[Tuple[str, float, float, str]] = []
    # Elementary rows
    rows.append(("Electron", M_e_actual, M_e_pred, emoji_marker(100.0*(M_e_pred-M_e_actual)/M_e_actual)))
    rows.append(("Proton",   M_p_actual, M_p_pred, emoji_marker(100.0*(M_p_pred-M_p_actual)/M_p_actual)))
    rows.append(("Neutron",  M_n_actual, M_n_pred, emoji_marker(100.0*(M_n_pred-M_n_actual)/M_n_actual)))

    # Elements
    elements = _elements_from_table()
    for name, (pZ, nN, eE, gmol) in elements.items():
        actual_kg = gmol * 1e-3 / avogadro
        predicted = pZ * M_p_pred + nN * M_n_pred + eE * M_e_pred
        rel_error = 100.0 * (predicted - actual_kg) / actual_kg
        rows.append((name, actual_kg, predicted, emoji_marker(rel_error)))

    # Molecules
    for mol, gmol in MOLECULES.items():
        counts = _parse_formula(mol)
        pred = 0.0
        for sym, k in counts.items():
            pZ, nN, eE, _ = elements[sym]
            pred += k * (pZ * M_p_pred + nN * M_n_pred + eE * M_e_pred)
        actual_kg = gmol * 1e-3 / avogadro
        rel_error = 100.0 * (pred - actual_kg) / actual_kg
        rows.append((mol, actual_kg, pred, emoji_marker(rel_error)))

    return pd.DataFrame(rows, columns=["Object","Actual Mass (kg)","Predicted Mass (kg)","% Error"])


# ──────────────────────────────────────────────────────────────────────────────
# Main Execution
# ──────────────────────────────────────────────────────────────────────────────
def main(mode: str = "exact_closure") -> None:
    print("=== SST Invariant Master Mass (Canon) ===")
    cfg = Config(mode=mode)
    topologies = get_particle_topologies(cfg)
    diag = topologies.pop("_diag")

    print("\n--- Mode & Model Parameters ---")
    print(f"mode = {diag['mode']}  |  kappa_R = {diag['kappa_R']:.6g}")
    print(f"s_u = {diag['s_u']:.6f}, s_d = {diag['s_d']:.6f}, lambda_b = {diag['lambda_b']:.6f}")
    print(f"A_bary = {diag['A_bary']:.6e},  K = {diag['K']:.6e}")
    print(f"scaling_factor = {diag['scaling_factor']:.6f}")

    print("\n--- Particle Topological & Geometric Invariants ---")
    # Pop leptons for separate display
    lepton_topos = {k: topologies.pop(k) for k in ["electron", "muon", "tau"]}
    for p in lepton_topos.values():
        print(f"{p.name:<12}: b={p.b}, g={p.g}, n={p.n}, L_tot={p.L_tot:.6f}")
    for p in topologies.values(): # Baryons
        print(f"{p.name:<12}: b={p.b}, g={p.g}, n={p.n}, L_tot={p.L_tot:.6f}")

    # Re-add leptons for table generation
    topologies.update(lepton_topos)
    df = compute_tables(topologies, cfg)

    print("\n--- Mass Prediction Results ---")
    pd.set_option("display.float_format", lambda x: f"{x:.6e}" if isinstance(x, float) else str(x))
    print(df.to_string(index=False))

    # Ropelength Analysis
    ltot_e = topologies["electron"].L_tot
    ltot_mu = topologies["muon"].L_tot
    ltot_tau = topologies["tau"].L_tot
    print("\n--- Ropelength Analysis ---")
    print(f"Calibrated L_tot for Electron: {ltot_e:.6f}")
    print(f"Required L_tot for Muon (5_1):  {ltot_mu:.6f}")
    print(f"Required L_tot for Tau (7_1):   {ltot_tau:.6f}")
    print(f"Ratio (L_mu / L_e):   {ltot_mu / ltot_e:.4f}")
    print(f"Ratio (L_tau / L_mu): {ltot_tau / ltot_mu:.4f}")

    out_csv = f"SST_Invariant_Mass_Results_{mode}.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nSaved results to {out_csv}")


if __name__ == "__main__":
    import sys
    arg_mode = sys.argv[1] if len(sys.argv) > 1 else "exact_closure"
    main(arg_mode)

    try:
        ans = input("\nCompare with other modes and add predicted columns? [y/N]: ").strip().lower()
    except EOFError:
        ans = "n"

    if ans in ("y", "yes"):
        all_modes = ["exact_closure", "canonical", "sector_norm"]
        label_map = {"canonical":"CANON", "sector_norm":"Sector Norm", "exact_closure":"Exact Closure"}

        # Get the base dataframe from the mode just run
        cfg_base = Config(mode=arg_mode)
        tops_base = get_particle_topologies(cfg_base)
        # We need to remove the diagnostic dict before passing to compute_tables
        tops_base.pop("_diag", None)
        df_cmp = compute_tables(tops_base, cfg_base)

        # Compute results for other modes and merge
        other_modes = [m for m in all_modes if m != arg_mode]
        for m in other_modes:
            cfg_m = Config(mode=m)
            tops_m = get_particle_topologies(cfg_m)
            tops_m.pop("_diag", None)
            df_m = compute_tables(tops_m, cfg_m)[["Object","Actual Mass (kg)","Predicted Mass (kg)"]].rename(
                columns={"Predicted Mass (kg)": f"Predicted Mass (kg) [{label_map[m]}]"}
            )
            # Error column for that mode
            df_m[f"% Error [{label_map[m]}]"] = 100.0 * (df_m[f"Predicted Mass (kg) [{label_map[m]}]"] - df_m["Actual Mass (kg)"]) / df_m["Actual Mass (kg)"]
            df_m[f"% Error [{label_map[m]}]"] = df_m[f"% Error [{label_map[m]}]"].apply(emoji_marker)
            df_m = df_m.drop(columns=["Actual Mass (kg)"])
            df_cmp = df_cmp.merge(df_m, on="Object", how="left")

        # Reorder columns for clarity
        desired_cols = ["Object","Actual Mass (kg)","Predicted Mass (kg)","% Error",
                        "Predicted Mass (kg) [CANON]","% Error [CANON]",
                        "Predicted Mass (kg) [Sector Norm]","% Error [Sector Norm]"]
        cols = [c for c in desired_cols if c in df_cmp.columns] + [c for c in df_cmp.columns if c not in desired_cols]
        df_cmp = df_cmp[cols]

        out_csv_all = "SST_Invariant_Mass_Results_all_modes.csv"
        df_cmp.to_csv(out_csv_all, index=False)
        print(f"\nSaved comparison to {out_csv_all}")
