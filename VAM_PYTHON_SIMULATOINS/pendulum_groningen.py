# Compute a Groningen benchmark and a small sweep table for the VAM–Pendulum–Clock mapping.
import math
import pandas as pd
from itertools import product
import os, textwrap, runpy, json, pandas as pd
import IPython.display as display

# Physical constants
c   = 299_792_458.0           # [m/s]
g   = 9.80665                 # [m/s^2]
R_E = 6_378_137.0             # [m] WGS84 equatorial radius
Omega_E = 7.2921150e-5        # [rad/s] Earth sidereal rotation
sec_per_day = 86400.0

# Site: Groningen
lat_deg = 53.219
phi = math.radians(lat_deg)
sin_phi = math.sin(phi)
cos_phi = math.cos(phi)

# Derived Foucault and rotation kinematics
Omega_p = Omega_E * sin_phi     # [rad/s]
T_p_hours = (2*math.pi/Omega_p)/3600.0

v_surface = Omega_E * R_E * cos_phi

# Baseline (per-day drifts) at height h=0, lab_size=10 m, delta_Omega_p=0
lab_size_default = 10.0
R_eff_default = lab_size_default/2.0
delta_Omega_p_default = 0.0
Omega_eff_default = Omega_p + delta_Omega_p_default
v_lab_default = Omega_eff_default * R_eff_default

rot_kin_frac = - (v_surface**2) / (2*c**2)
vam_swirl_frac = - (v_lab_default**2) / (2*c**2)
baseline_total_frac = rot_kin_frac + vam_swirl_frac  # at h=0

# Convert to ns/day
to_ns_day = lambda frac: frac * sec_per_day * 1e9
baseline_rot_ns_day = to_ns_day(rot_kin_frac)
baseline_vam_ns_day = to_ns_day(vam_swirl_frac)
baseline_total_ns_day = to_ns_day(baseline_total_frac)

# Build a sweep over a few parameters
heights_m = [0, 50, 100, 200]          # height above geoid
lab_sizes_m = [5.0, 10.0, 20.0]        # lab span (R_eff=lab/2)
delta_Omegas = [0.0, 1e-7, 5e-7, 1e-6] # engineered swirl add-on [rad/s]

rows = []
for h, L, dOm in product(heights_m, lab_sizes_m, delta_Omegas):
    R_eff = L/2.0
    # Terms
    gr_height_frac = (g*h)/c**2                          # + faster with height
    rot_frac = rot_kin_frac                              # constant for a given latitude
    Omega_eff = Omega_p + dOm
    v_lab = Omega_eff * R_eff
    vam_swirl_frac_case = - (v_lab**2) / (2*c**2)
    total_frac = gr_height_frac + rot_frac + vam_swirl_frac_case

    rows.append({
        "latitude_deg": lat_deg,
        "height_m": h,
        "lab_size_m": L,
        "R_eff_m": R_eff,
        "delta_Omega_p_rad_s": dOm,
        "Foucault_Omega_p_rad_s": Omega_p,
        "Foucault_period_hours": T_p_hours,
        "v_surface_m_s": v_surface,
        "v_lab_m_s": v_lab,
        "frac_GR_height": gr_height_frac,
        "frac_rot_kin": rot_frac,
        "frac_VAM_swirl": vam_swirl_frac_case,
        "frac_TOTAL": total_frac,
        "ns_day_GR_height": to_ns_day(gr_height_frac),
        "ns_day_rot_kin": to_ns_day(rot_frac),
        "ns_day_VAM_swirl": to_ns_day(vam_swirl_frac_case),
        "ns_day_TOTAL": to_ns_day(total_frac),
    })

df = pd.DataFrame(rows)

# Show a compact view sorted by height and engineered swirl
df_sorted = df.sort_values(["height_m", "lab_size_m", "delta_Omega_p_rad_s"]).reset_index(drop=True)

# Save CSV for download
csv_path = "./groningen_vam_pendulum_clockshift_sweep.csv"
df_sorted.to_csv(csv_path, index=False)

# Display a trimmed selection to the user
cols_to_show = [
    "height_m","lab_size_m","delta_Omega_p_rad_s",
    "Foucault_Omega_p_rad_s","Foucault_period_hours",
    "v_surface_m_s","v_lab_m_s",
    "ns_day_GR_height","ns_day_rot_kin","ns_day_VAM_swirl","ns_day_TOTAL"
]
display.display("VAM–Pendulum–Clock: Groningen Sweep (ns/day)", df_sorted[cols_to_show].round(6))

# Also print a short textual summary of the baseline and a couple of examples
baseline_summary = f"""
Groningen baseline (lat={lat_deg:.3f}°)
- Foucault Ω_p = {Omega_p:.9e} rad/s  (period ≈ {T_p_hours:.3f} h)
- Surface speed v(lat) = {v_surface:.3f} m/s
- Baseline per day (h=0, lab=10 m, δΩ_p=0):
    Rotation (SR)   : {baseline_rot_ns_day:.3f} ns/day (slower)
    VAM swirl (lab) : {baseline_vam_ns_day:.6f} ns/day (slower, tiny at lab scale)
    TOTAL           : {baseline_total_ns_day:.3f} ns/day
CSV saved: {csv_path}
"""
print(baseline_summary)


