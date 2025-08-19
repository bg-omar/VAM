import json, os

def load_constants(path=None):
    # Default constants
    C = {
        "C_e": {"value": 1.09384563e6, "unit": "m/s"},
        "r_c": {"value": 1.40897017e-15, "unit": "m"},
        "rho_ae_fluid": {"value": 7.0e-7, "unit": "kg/m^3"},
        "F_max": {"value": 29.053507, "unit": "N"},
        "c": {"value": 299792458.0, "unit": "m/s"},
        "t_p": {"value": 5.391247e-44, "unit": "s"}
    }
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            user_C = json.load(f)
        for k in user_C:
            if k in C and "value" in user_C[k]:
                C[k]["value"] = float(user_C[k]["value"])
    # Derived: G_swirl = (C_e c^5 t_p^2)/(2 F_max r_c^2)
    Ce, c, tp, Fmax, rc = [C[k]["value"] for k in ["C_e","c","t_p","F_max","r_c"]]
    C["G_swirl"] = {"value": Ce*c**5*tp**2 / (2*Fmax*rc**2), "unit": "m^3 kg^-1 s^-2"}
    return C