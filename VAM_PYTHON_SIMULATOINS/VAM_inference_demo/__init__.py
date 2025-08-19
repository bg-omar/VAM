# VAM Inference Framework (forward + inverse) — self-contained demo
# This cell creates a small, modular codebase plus a runnable demo that:
#  1) Loads VAM constants (from VAM_constants.json if present, else uses defaults)
#  2) Implements forward models (Ω_swirl(r), time dilation τ, g-field from M_eff(r))
#  3) Implements a simple inverse inference (least-squares via grid + local refine)
#  4) Runs a synthetic test and outputs figures + a summary table
#
# Files created under vam_infer_demo/
# - vam_infer/__init__.py
# - vam_infer/constants.py
# - vam_infer/models.py
# - vam_infer/forward.py
# - vam_infer/inverse.py
# - vam_infer/utils.py
# - demo_vam_inference.py
# - README.md
#
# --------- package: vam_infer_demo/__init__.py ---------

import json, os, textwrap, math, pathlib, numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple, Callable