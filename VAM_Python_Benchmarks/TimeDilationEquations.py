import math
from typing import Iterable

import numpy as np

# Import physical constants when available
try:
    from constants import c, G
except Exception:  # fallback values
    c = 299_792_458  # speed of light in vacuum (m/s)
    G = 6.67430e-11  # gravitational constant (m^3 kg^-1 s^-2)


class TimeDilationEquations:
    """Collection of time dilation related equations."""

    @staticmethod
    def delta_tau_over_delta_t(omega_obs: float, omega_0: float) -> float:
        """Equation from 3_vortex_clocks.tex."""
        return omega_obs / omega_0

    @staticmethod
    def sr_time_dilation(v: float, light_speed: float = c) -> float:
        """Equation from 4_special_relativity.tex."""
        return math.sqrt(1 - (v ** 2) / (light_speed ** 2))

    @staticmethod
    def omega_obs_sr(v: float, omega_0: float, light_speed: float = c) -> float:
        """Equation from 4_special_relativity.tex."""
        return omega_0 * math.sqrt(1 - (v ** 2) / (light_speed ** 2))

    @staticmethod
    def gravitational_time_dilation(r: float, M: float, *,
                                    grav_const: float = G,
                                    light_speed: float = c) -> float:
        """Equation from 5_gravitational_time_dilation.tex."""
        return math.sqrt(1 - (2 * grav_const * M) / (r * light_speed ** 2))

    @staticmethod
    def combined_time_dilation(u_vec: Iterable[float], v_g_vec: Iterable[float],
                               light_speed: float = c) -> float:
        """Equation from 6_combined_effects.tex using relative velocity."""
        u = np.asarray(list(u_vec), dtype=float)
        v_g = np.asarray(list(v_g_vec), dtype=float)
        v_rel = u - v_g
        v_rel_sq = float(np.dot(v_rel, v_rel))
        return math.sqrt(1 - v_rel_sq / (light_speed ** 2))

    @staticmethod
    def circular_orbit_dilation(r: float, M: float, *,
                                grav_const: float = G,
                                light_speed: float = c) -> float:
        """Equation from 6_combined_effects.tex for circular orbits."""
        return math.sqrt(1 - (3 * grav_const * M) / (r * light_speed ** 2))

    @staticmethod
    def single_vortex_time_increment(dt: float, v_rel: float,
                                     light_speed: float = c) -> float:
        """Equation from appendix_A.tex."""
        return dt * math.sqrt(1 - (v_rel ** 2) / (light_speed ** 2))

    @staticmethod
    def ensemble_time_increment(dtheta_list: Iterable[float],
                                omega_list: Iterable[float]) -> float:
        """Equation from appendix_A.tex for compound vortex systems."""
        dtheta = list(dtheta_list)
        omega = list(omega_list)
        N = len(omega)
        return sum((d / w) for d, w in zip(dtheta, omega)) / N

    @staticmethod
    def ensemble_time_increment_coherent(dtheta: float, omega: float) -> float:
        """Equation from appendix_A.tex for coherent systems."""
        return dtheta / omega

    @staticmethod
    def decoherent_time_increment(v_rel_list: Iterable[float], dt: float,
                                  light_speed: float = c) -> float:
        """Equation from appendix_A.tex for decoherent systems."""
        factors = [math.sqrt(1 - (v ** 2) / (light_speed ** 2)) for v in v_rel_list]
        return float(np.mean(factors)) * dt

    @staticmethod
    def decoherent_time_increment_approx(mean_v_rel_sq: float, dt: float,
                                         light_speed: float = c) -> float:
        """Approximation from appendix_A.tex."""
        return dt * math.sqrt(1 - mean_v_rel_sq / (light_speed ** 2))

    @staticmethod
    def rotating_superfluid_dilation(dt: float, omega: float, R: float,
                                     light_speed: float = c) -> float:
        """Equation from appendix_B.tex for rotating superfluids."""
        return dt * math.sqrt(1 - (omega ** 2) * (R ** 2) / (light_speed ** 2))

    @staticmethod
    def swirl_potential_delay(omega: float, r: float, dt: float,
                              light_speed: float = c) -> float:
        """Equation from appendix_B.tex relating swirl potential to delay."""
        phi_swirl = 0.5 * omega ** 2 * r ** 2
        return phi_swirl / (light_speed ** 2) * dt

    @staticmethod
    def light_bending_deflection(dn_dr_values: Iterable[float],
                                 r_values: Iterable[float]) -> float:
        """Equation from appendix_B.tex for light bending."""
        return float(np.trapz(list(dn_dr_values), x=list(r_values)))
