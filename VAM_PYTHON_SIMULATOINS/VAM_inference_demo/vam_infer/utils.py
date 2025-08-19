import numpy as np, os, json

def make_noisy(observed, rel_noise=0.001, seed=123, floor=0.0):
    rng = np.random.default_rng(seed)
    scale = rel_noise * np.maximum(floor, np.abs(observed))
    return observed + rng.normal(0.0, scale, size=observed.shape)

def geomspace_exclude_zero(r_min, r_max, N):
    r_min = max(r_min, 1e-18)
    return np.geomspace(r_min, r_max, N)

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def save_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)