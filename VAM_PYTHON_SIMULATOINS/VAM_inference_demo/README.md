# --------- README ---------

# VAM Inference (Forward + Inverse) — Minimal Framework

This folder contains a small, self-contained Python package `vam_infer` and a demo script:

- Forward models:
    - `Ω_swirl(r) = (C_e / r_c) e^{-r/r_c}`
    - `τ = dt_local/dt_∞ = sqrt(1 - Ω^2/c^2)`
    - `M_eff(r) = ∫_0^r 4π r'^2 ρ_ae e^{-r'/r_c} dr'` (closed-form used)
    - `g(r) = G_swirl M_eff(r) / r^2`, with `G_swirl = (C_e c^5 t_p^2) / (2 F_max r_c^2)`

- Inverse models:
    - Fit `r_c` from observed `τ(r)` (grid + local refine, MSE)
    - Fit `ρ_ae` from observed `g(r)` (linear scaling + refine)

- Constants:
    - If `VAM_constants.json` is present in the working directory, it is used.
    - Otherwise, sane defaults are used (editable in `constants.py`).


# VAM Inference GUI Demo\nRun `python vam_infer_gui.py` to start the GUI.
```bash
python demo.py
