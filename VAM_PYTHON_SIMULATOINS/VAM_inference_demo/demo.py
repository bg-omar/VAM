
# --------- demo script ---------
from __future__ import annotations
import os, json, numpy as np
import matplotlib.pyplot as plt
from vam_infer.constants import load_constants, compute_G_swirl, get_value
from vam_infer.forward import predict_time_dilation, predict_g
from vam_infer.inverse import fit_r_c_from_time_dilation, fit_rho_from_g
from vam_infer.utils import make_noisy, geomspace_exclude_zero

# 1) Load constants (VAM_constants.json if present in CWD)
C = load_constants("VAM_constants.json")
G_swirl = compute_G_swirl(C)

print("Loaded constants:")
for k,v in C.items():
    print(f"  {k:>14s}: {v.value} [{v.unit}] ({v.latex})")
print(f"\nComputed G_swirl = {G_swirl:.6e} SI\n")

# 2) Synthetic experiment design
r = geomspace_exclude_zero(1e-14, 1e-9, 300)   # radii [m]

# Forward predictions (ground-truth with current constants)
tau_true = predict_time_dilation(r, C)    # time dilation ratio vs r
g_true   = predict_g(r, C, rho_key="rho_ae_fluid")

# 3) Add measurement noise
tau_obs = make_noisy(tau_true, rel_noise=1e-6, seed=1)
g_obs   = make_noisy(g_true, rel_noise=1e-3, seed=2)

# 4) Inverse inference
rc_est, rc_loss = fit_r_c_from_time_dilation(r, tau_obs, C,
                    r_c_bounds=(1e-18, 1e-12), n_grid=200)

rho_est, rho_loss = fit_rho_from_g(r, g_obs, C, rho_key="rho_ae_fluid",
                    rho_bounds=(1e-12, 1e3), n_grid=300)

print(f"Estimated r_c ≈ {rc_est:.6e} m  (MSE={rc_loss:.3e});  true r_c = {get_value(C,'r_c'):.6e} m")
print(f"Estimated rho_ae_fluid ≈ {rho_est:.6e} kg/m^3 (MSE={rho_loss:.3e});  true rho = {get_value(C,'rho_ae_fluid'):.6e} kg/m^3")

# 5) Plots
os.makedirs("out_plots", exist_ok=True)

plt.figure()
plt.loglog(r, tau_obs, '.', label="τ_obs")
plt.loglog(r, predict_time_dilation(r, C, r_c_override=rc_est), '-', label="τ_fit")
plt.loglog(r, tau_true, '--', label="τ_true")
plt.xlabel("r [m]")
plt.ylabel("τ = dt_local/dt_infty")
plt.title("Time-dilation fit for r_c")
plt.legend()
plt.grid(True, which="both")
plt.tight_layout()
plt.savefig("out_plots/time_dilation_fit.png")
plt.close()

plt.figure()
plt.loglog(r, g_obs, '.', label="g_obs")
# Construct prediction at rho_est (temporarily modify constant copy)
import copy
C2 = copy.deepcopy(C)
C2["rho_ae_fluid"].value = rho_est
plt.loglog(r, predict_g(r, C2, rho_key="rho_ae_fluid"), '-', label="g_fit")
plt.loglog(r, g_true, '--', label="g_true")
plt.xlabel("r [m]")
plt.ylabel("g(r) [m s^-2]")
plt.title("g-field fit for rho_ae_fluid")
plt.legend()
plt.grid(True, which="both")
plt.tight_layout()
plt.savefig("out_plots/g_field_fit.png")
plt.close()

# 6) Save summary
summary = {
    "G_swirl": G_swirl,
    "r_c_true": get_value(C, "r_c"),
    "r_c_est": rc_est,
    "r_c_mse": rc_loss,
    "rho_true": get_value(C, "rho_ae_fluid"),
    "rho_est": rho_est,
    "rho_mse": rho_loss,
}
with open("out_plots/summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print("\\nWrote: out_plots/time_dilation_fit.png, out_plots/g_field_fit.png, out_plots/summary.json")


import os, textwrap, runpy, json, pandas as pd
import IPython.display as display

base = "./vam_infer_demo"
pkg = os.path.join(base, "vam_infer")

with open(os.path.join(base, "out_plots", "summary.json"), "r", encoding="utf-8") as f:
    summary = json.load(f)
df = pd.DataFrame([summary])
display.display("VAM inference summary (re-run)", df)

print("Artifacts:")
print(f"- README: {os.path.join(base, 'README.md')}")
print(f"- Time-dilation plot: {os.path.join(base, 'out_plots', 'time_dilation_fit.png')}")
print(f"- g-field plot: {os.path.join(base, 'out_plots', 'g_field_fit.png')}")
print(f"- Summary JSON: {os.path.join(base, 'out_plots', 'summary.json')}")