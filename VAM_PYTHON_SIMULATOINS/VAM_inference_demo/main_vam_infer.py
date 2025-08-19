import os, sys, json, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from vam_infer.constants import load_constants
from vam_infer.models import tau_ratio, g_field
from vam_infer.utils import geomspace_exclude_zero, make_noisy, ensure_dir, save_json
from vam_infer.io import load_tau_csv, load_g_csv
from vam_infer.inverse import fit_rc_from_tau, fit_rho_from_g
from vam_infer.mcmc_infer import mcmc_tau, mcmc_g, mcmc_joint

OUT = "out_plots"

def synthetic_lsq(C):
    outdir = os.path.join(OUT, "synthetic_lsq"); ensure_dir(outdir)
    r_tau = geomspace_exclude_zero(1e-14, 1e-9, 300)
    r_g   = geomspace_exclude_zero(1e-6,  1e-2, 200)
    tau_true = tau_ratio(r_tau, C); g_true = g_field(r_g, C)
    tau_obs = make_noisy(tau_true, rel_noise=1e-6, seed=1, floor=0.0)
    g_obs   = make_noisy(g_true,   rel_noise=1e-9, seed=2, floor=0.0)
    rc_est, rc_mse   = fit_rc_from_tau(r_tau, tau_obs, C)
    rho_est, rho_mse = fit_rho_from_g(r_g, g_obs, C)
    # plots
    plt.figure()
    plt.loglog(r_tau, tau_obs, ".", label="τ_obs"); plt.loglog(r_tau, tau_ratio(r_tau, C), "-", label=f"τ_fit (r_c={C['r_c']['value']:.3e} m)")
    plt.xlabel("r [m]"); plt.ylabel("τ"); plt.title("Synthetic τ LSQ"); plt.grid(True, which="both"); plt.legend(); plt.tight_layout()
    plt.savefig(os.path.join(outdir, "tau_fit.png")); plt.close()
    plt.figure()
    plt.loglog(r_g, g_obs, ".", label="g_obs"); plt.loglog(r_g, g_field(r_g, C), "-", label=f"g_fit (ρ={C['rho_ae_fluid']['value']:.3e} kg/m³)")
    plt.xlabel("r [m]"); plt.ylabel("g [m s$^{-2}$]"); plt.title("Synthetic g LSQ"); plt.grid(True, which="both"); plt.legend(); plt.tight_layout()
    plt.savefig(os.path.join(outdir, "g_fit.png")); plt.close()
    save_json(os.path.join(outdir, "summary.json"), {"r_c_est": rc_est, "r_c_mse": rc_mse, "rho_est": rho_est, "rho_mse": rho_mse})
    print("Synthetic LSQ done ->", outdir)

def csv_lsq(C):
    path_tau = input("Path to τ(r) CSV (or blank): ").strip()
    path_g   = input("Path to g(r) CSV (or blank): ").strip()
    r_units  = input("r units [m/mm/um/nm] (default m): ").strip().lower() or "m"
    scale = {"m":1.0,"mm":1e-3,"um":1e-6,"nm":1e-9}.get(r_units,1.0)
    outdir = os.path.join(OUT, "csv_lsq"); ensure_dir(outdir)
    summary = {}
    if path_tau:
        r, tau = load_tau_csv(path_tau, r_scale=scale); idx = np.argsort(r); r = np.asarray(r)[idx]; tau = np.asarray(tau)[idx]
        rc_est, rc_mse = fit_rc_from_tau(r, tau, C); summary["r_c_est"] = rc_est; summary["r_c_mse"] = rc_mse
        plt.figure(); plt.loglog(r, tau, ".", label="τ_obs"); plt.loglog(r, tau_ratio(r, C), "-", label=f"τ_fit (r_c={C['r_c']['value']:.3e} m)")
        plt.xlabel("r [m]"); plt.ylabel("τ"); plt.title("CSV τ LSQ"); plt.grid(True, which="both"); plt.legend(); plt.tight_layout()
        plt.savefig(os.path.join(outdir, "tau_fit_csv.png")); plt.close()
    if path_g:
        r, g = load_g_csv(path_g, r_scale=scale); idx = np.argsort(r); r = np.asarray(r)[idx]; g = np.asarray(g)[idx]
        rho_est, rho_mse = fit_rho_from_g(r, g, C); summary["rho_est"] = rho_est; summary["rho_mse"] = rho_mse
        plt.figure(); plt.loglog(r, g, ".", label="g_obs"); plt.loglog(r, g_field(r, C), "-", label=f"g_fit (ρ={C['rho_ae_fluid']['value']:.3e} kg/m³)")
        plt.xlabel("r [m]"); plt.ylabel("g [m s$^{-2}$]"); plt.title("CSV g LSQ"); plt.grid(True, which="both"); plt.legend(); plt.tight_layout()
        plt.savefig(os.path.join(outdir, "g_fit_csv.png")); plt.close()
    save_json(os.path.join(outdir, "summary.json"), summary)
    print("CSV LSQ done ->", outdir)

def synthetic_mcmc(C):
    outdir = os.path.join(OUT, "synthetic_mcmc"); ensure_dir(outdir)
    r_tau = geomspace_exclude_zero(1e-14, 1e-9, 300)
    r_g   = geomspace_exclude_zero(1e-6,  1e-2, 200)
    tau_obs = tau_ratio(r_tau, C)
    g_obs   = g_field(r_g, C)
    # run chains
    chain_rc  = mcmc_tau(r_tau, tau_obs, C, sigma_tau=1e-6, n_samples=4000, burn=2000, thin=4, step=0.03)
    chain_rho = mcmc_g(r_g, g_obs, C, sigma_g=1e-9, n_samples=4000, burn=2000, thin=4, step=0.08)
    # summarize
    rc_samples  = 10**chain_rc[:,0]
    rho_samples = 10**chain_rho[:,0]
    rc_med = float(np.median(rc_samples)); rc_lo, rc_hi = np.percentile(rc_samples,[16,84])
    rho_med = float(np.median(rho_samples)); rho_lo, rho_hi = np.percentile(rho_samples,[16,84])
    save_json(os.path.join(outdir, "summary.json"), {
        "r_c_median": rc_med, "r_c_16%": float(rc_lo), "r_c_84%": float(rc_hi),
        "rho_median": rho_med, "rho_16%": float(rho_lo), "rho_84%": float(rho_hi)
    })
    # quick hist plots
    plt.figure(); plt.hist(rc_samples, bins=60); plt.xlabel("r_c [m]"); plt.ylabel("count"); plt.title("Posterior r_c (synthetic τ)"); plt.tight_layout()
    plt.savefig(os.path.join(outdir, "posterior_rc.png")); plt.close()
    plt.figure(); plt.hist(rho_samples, bins=60); plt.xlabel("rho [kg/m^3]"); plt.ylabel("count"); plt.title("Posterior rho (synthetic g)"); plt.tight_layout()
    plt.savefig(os.path.join(outdir, "posterior_rho.png")); plt.close()
    print("Synthetic MCMC done ->", outdir)

def csv_mcmc(C):
    path_tau = input("Path to τ(r) CSV (or blank): ").strip()
    path_g   = input("Path to g(r) CSV (or blank): ").strip()
    r_units  = input("r units [m/mm/um/nm] (default m): ").strip().lower() or "m"
    scale = {"m":1.0,"mm":1e-3,"um":1e-6,"nm":1e-9}.get(r_units,1.0)
    outdir = os.path.join(OUT, "csv_mcmc"); ensure_dir(outdir)
    rt = gt = None
    if path_tau:
        rt, tau = load_tau_csv(path_tau, r_scale=scale); idx = np.argsort(rt); rt = np.asarray(rt)[idx]; tau = np.asarray(tau)[idx]
    if path_g:
        rg, g  = load_g_csv(path_g,   r_scale=scale); idx = np.argsort(rg); rg = np.asarray(rg)[idx]; g   = np.asarray(g)[idx]
    summary = {}
    if path_tau and not path_g:
        chain = mcmc_tau(rt, tau, C, sigma_tau=1e-6, n_samples=4000, burn=2000, thin=4, step=0.03)
        rc_samples = 10**chain[:,0]; med = float(np.median(rc_samples)); lo,hi = np.percentile(rc_samples,[16,84])
        summary.update({"r_c_median": med, "r_c_16%": float(lo), "r_c_84%": float(hi)})
        plt.figure(); plt.hist(rc_samples, bins=60); plt.xlabel("r_c [m]"); plt.title("Posterior r_c (CSV τ)"); plt.tight_layout()
        plt.savefig(os.path.join(outdir, "posterior_rc.png")); plt.close()
    elif path_g and not path_tau:
        chain = mcmc_g(rg, g, C, sigma_g=1e-9, n_samples=4000, burn=2000, thin=4, step=0.08)
        rho_samples = 10**chain[:,0]; med = float(np.median(rho_samples)); lo,hi = np.percentile(rho_samples,[16,84])
        summary.update({"rho_median": med, "rho_16%": float(lo), "rho_84%": float(hi)})
        plt.figure(); plt.hist(rho_samples, bins=60); plt.xlabel("rho [kg/m^3]"); plt.title("Posterior rho (CSV g)"); plt.tight_layout()
        plt.savefig(os.path.join(outdir, "posterior_rho.png")); plt.close()
    elif path_tau and path_g:
        chain = mcmc_joint(rt, tau, rg, g, C, sigma_tau=1e-6, sigma_g=1e-9, n_samples=6000, burn=3000, thin=5, step=(0.03,0.08))
        rc_samples  = 10**chain[:,0]; rho_samples = 10**chain[:,1]
        rc_med = float(np.median(rc_samples)); rc_lo, rc_hi = np.percentile(rc_samples,[16,84])
        rho_med = float(np.median(rho_samples)); rho_lo, rho_hi = np.percentile(rho_samples,[16,84])
        summary.update({"r_c_median": rc_med, "r_c_16%": float(rc_lo), "r_c_84%": float(rc_hi),
                        "rho_median": rho_med, "rho_16%": float(rho_lo), "rho_84%": float(rho_hi)})
        # quick hists
        plt.figure(); plt.hist(rc_samples, bins=60); plt.xlabel("r_c [m]"); plt.title("Posterior r_c (CSV joint)"); plt.tight_layout()
        plt.savefig(os.path.join(outdir, "posterior_rc.png")); plt.close()
        plt.figure(); plt.hist(rho_samples, bins=60); plt.xlabel("rho [kg/m^3]"); plt.title("Posterior rho (CSV joint)"); plt.tight_layout()
        plt.savefig(os.path.join(outdir, "posterior_rho.png")); plt.close()
    else:
        print("No CSVs provided; aborting.")
        return
    save_json(os.path.join(outdir, "summary.json"), summary)
    print("CSV MCMC done ->", outdir)

def main():
    C = load_constants()
    menu = """
    Select inference mode:
    [1] Synthetic LSQ (τ + g)
    [2] CSV LSQ (load experimental data)
    [3] Synthetic Bayesian MCMC
    [4] CSV Bayesian MCMC
    [q] Quit
    > """
    while True:
        choice = input(menu).strip().lower()
        if choice == "1":
            synthetic_lsq(C)
        elif choice == "2":
            csv_lsq(C)
        elif choice == "3":
            synthetic_mcmc(C)
        elif choice == "4":
            csv_mcmc(C)
        elif choice in ["q","quit","exit"]:
            print("Bye."); break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()