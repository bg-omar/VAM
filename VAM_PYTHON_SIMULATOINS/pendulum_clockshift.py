#!/usr/bin/env python3
"""VAM–Pendulum Clockshift Calculator
Inputs: latitude [deg], lab_size [m], height_diff [m], optional delta_Omega_p [rad/s]
Outputs: component-wise fractional clock-rate shifts and total:
- GR height redshift   : + g*h / c^2
- Earth rotation (kin) : - v^2 / (2 c^2) with v = Ω_E * R_E * cos(latitude)
- Local swirl (VAM)    : - (Ω_eff^2 * R_eff^2) / (2 c^2),  Ω_eff = Ω_E*sin(latitude) + delta_Omega_p
Notes:
- R_eff defaults to lab_size/2 (swirl sampled on lab scale).
- Foucault relation: precession Ω_p = Ω_E * sin(latitude). We use Ω_eff built on that.
- Set delta_Omega_p to model engineered swirl (e.g., superfluid ring), else keep 0.
"""

from math import sin, cos, radians, pi

# Physical constants (SI)
c   = 299_792_458.0           # speed of light [m/s]
g   = 9.80665                 # standard gravity [m/s^2]
R_E = 6_378_137.0            # Earth equatorial radius [m]
Ω_E = 7.2921150e-5           # Earth sidereal rotation [rad/s]

def vam_clockshift(latitude_deg: float,
                   lab_size_m: float,
                   height_diff_m: float,
                   delta_Omega_p: float = 0.0,
                   R_eff: float | None = None):
    """Return dict of fractional shifts (dimensionless) and helpful byproducts."""
    φ = radians(latitude_deg)
    if R_eff is None:
        R_eff = 0.5 * lab_size_m  # sample swirl on half the lab span

    # 1) GR gravitational redshift from height difference
    gr_height = (g * height_diff_m) / (c**2)  # + sign: higher runs faster

    # 2) Kinematic (special-relativistic) dilation from Earth's rotation at latitude
    v_surface = Ω_E * R_E * cos(φ)
    kin_rot   = - (v_surface**2) / (2 * c**2)

    # 3) VAM swirl term tied to Foucault precession scale on lab radius
    Ω_p    = Ω_E * sin(φ)                  # Foucault precession rate
    Ω_eff  = Ω_p + delta_Omega_p
    v_lab  = Ω_eff * R_eff                 # tangential swirl speed on lab scale
    vam_swirl = - (v_lab**2) / (2 * c**2)  # small-velocity expansion of sqrt(1 - v^2/c^2)

    total = gr_height + kin_rot + vam_swirl

    # Convenience: also report precession period
    T_p = (2*pi/Ω_p) if abs(Ω_p) > 0 else float('inf')

    return {
        "inputs": {
            "latitude_deg": latitude_deg,
            "lab_size_m": lab_size_m,
            "height_diff_m": height_diff_m,
            "delta_Omega_p_rad_s": delta_Omega_p,
            "R_eff_m": R_eff
        },
        "derived": {
            "earth_surface_speed_m_s": v_surface,
            "foucault_rate_rad_s": Ω_p,
            "foucault_period_hours": T_p/3600.0 if T_p != float('inf') else float('inf'),
            "effective_Omega_rad_s": Ω_eff,
            "lab_tangential_speed_m_s": v_lab
        },
        "fractional_shifts": {
            "gr_height": gr_height,       # + runs faster at height
            "rotational_kinematic": kin_rot,  # - runs slower on rotating Earth
            "vam_swirl_local": vam_swirl, # - local swirl slowdown (lab scale)
            "total": total
        }
    }

def pretty_report(res: dict) -> str:
    f = res["fractional_shifts"]
    d = res["derived"]
    i = res["inputs"]
    pp = lambda x: f"{x:.6e}"
    lines = []
    lines.append("=== VAM–Pendulum Clockshift ===")
    lines.append(f"Latitude: {i['latitude_deg']:.6f}°   Lab size: {i['lab_size_m']} m   Height Δ: {i['height_diff_m']} m")
    lines.append(f"R_eff: {i['R_eff_m']} m   δΩ_p: {i['delta_Omega_p_rad_s']} rad/s")
    lines.append("--- Derived ---")
    lines.append(f"Surface speed v(lat): {d['earth_surface_speed_m_s']:.3f} m/s")
    lines.append(f"Foucault Ω_p: {d['foucault_rate_rad_s']:.9e} rad/s   Period: {d['foucault_period_hours']:.3f} h")
    lines.append(f"Ω_eff: {d['effective_Omega_rad_s']:.9e} rad/s   v_lab: {d['lab_tangential_speed_m_s']:.6e} m/s")
    lines.append("--- Fractional clock-rate shifts (Δτ/τ) ---")
    lines.append(f"GR height     : {pp(f['gr_height'])}")
    lines.append(f"Rotation (kin): {pp(f['rotational_kinematic'])}")
    lines.append(f"VAM swirl     : {pp(f['vam_swirl_local'])}")
    lines.append(f"TOTAL         : {pp(f['total'])}")
    return "\\n".join(lines)


if __name__ == "__main__":
    # Example: Groningen, NL ~ 53.219°N
    res = vam_clockshift(latitude_deg=53.219, lab_size_m=10.0, height_diff_m=5.0, delta_Omega_p=0.0)
    print(pretty_report(res))


