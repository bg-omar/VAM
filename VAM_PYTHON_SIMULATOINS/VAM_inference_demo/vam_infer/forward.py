# --------- package: forward.py ---------
from __future__ import annotations
import numpy as np
from typing import Dict, Literal
from .models import omega_swirl, time_dilation_ratio_from_omega, g_field

def predict_time_dilation(r: np.ndarray, constants: Dict, r_c_override: float | None = None) -> np.ndarray:
    omega = omega_swirl(r, constants, r_c_override=r_c_override)
    return time_dilation_ratio_from_omega(omega, constants)

def predict_g(r: np.ndarray, constants: Dict, rho_key: str = "rho_ae_fluid") -> np.ndarray:
    return g_field(r, constants, rho_key=rho_key)

