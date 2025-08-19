# -*- coding: utf-8 -*-
from __future__ import annotations
import csv, math
from typing import List, Tuple, Optional

def _read_delimited(path: str) -> List[dict]:
    """
    Reads CSV/TSV with a header row. Auto-detects delimiter (comma or tab).
    Returns a list of dict rows with string keys from the header.
    Lines starting with '#' are ignored.
    """
    # Peek first non-comment line to guess delimiter
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln for ln in f.readlines() if not ln.lstrip().startswith("#")]
    if not lines:
        raise ValueError(f"No data in {path}")
    sniff = csv.Sniffer().sniff(lines[0])
    delim = sniff.delimiter if sniff.delimiter in [",", "\t", ";"] else ","
    reader = csv.DictReader(lines, delimiter=delim)
    return [dict(row) for row in reader]

def _pick_colname(names: List[str], want: str) -> Optional[str]:
    """
    Heuristics to select a column by semantic intent:
    - want="r"  -> pick first name containing 'r' and not 'rho' (case-insensitive)
    - want="tau"-> name containing 'tau' or 't_ratio'
    - want="g"  -> name equal/contains 'g'
    """
    low = [n.strip() for n in names]
    if want == "r":
        for n in low:
            ln = n.lower()
            if "rho" in ln:  # avoid mis-pick of density column
                continue
            if ln in ["r", "radius", "r_m"]: return n
        for n in low:
            if "r" in n.lower(): return n
    elif want == "tau":
        for n in low:
            ln = n.lower()
            if ln in ["tau", "t_ratio", "dt_local/dt_inf", "dt_local/dt_infty", "t_local_over_t_inf"]:
                return n
        for n in low:
            if "tau" in n.lower(): return n
    elif want == "g":
        for n in low:
            ln = n.lower()
            if ln in ["g", "g_m_s2", "g_ms2", "g_r"]:
                return n
        for n in low:
            if "g" in n.lower(): return n
    return None

def _parse_floats(rows: List[dict], col: str) -> List[float]:
    out = []
    for r in rows:
        v = r.get(col, "").strip()
        if v == "" or v.lower() == "nan":
            continue
        out.append(float(v))
    return out

def load_tau_csv(path: str,
                 r_col: str | None = None,
                 tau_col: str | None = None,
                 r_scale: float = 1.0) -> Tuple[List[float], List[float]]:
    """
    Load tau(r) CSV. Expects a header row. Units:
      - r values are multiplied by r_scale (default 1.0 means 'meters' already)
    """
    rows = _read_delimited(path)
    if not rows:
        raise ValueError(f"No rows in {path}")
    names = list(rows[0].keys())
    r_col = r_col or _pick_colname(names, "r")
    tau_col = tau_col or _pick_colname(names, "tau")
    if r_col is None or tau_col is None:
        raise ValueError(f"Could not infer columns (r={r_col}, tau={tau_col}). "
                         f"Columns present: {names}")
    r = [r_scale * float(v) for v in _parse_floats(rows, r_col)]
    tau = _parse_floats(rows, tau_col)
    if len(r) != len(tau):
        n = min(len(r), len(tau))
        r, tau = r[:n], tau[:n]
    return r, tau

def load_g_csv(path: str,
               r_col: str | None = None,
               g_col: str | None = None,
               r_scale: float = 1.0) -> Tuple[List[float], List[float]]:
    """
    Load g(r) CSV. Expects a header row. Units:
      - r values are multiplied by r_scale (default 1.0 means 'meters' already)
      - g values should be in m s^-2
    """
    rows = _read_delimited(path)
    if not rows:
        raise ValueError(f"No rows in {path}")
    names = list(rows[0].keys())
    r_col = r_col or _pick_colname(names, "r")
    g_col = g_col or _pick_colname(names, "g")
    if r_col is None or g_col is None:
        raise ValueError(f"Could not infer columns (r={r_col}, g={g_col}). "
                         f"Columns present: {names}")
    r = [r_scale * float(v) for v in _parse_floats(rows, r_col)]
    g = _parse_floats(rows, g_col)
    if len(r) != len(g):
        n = min(len(r), len(g))
        r, g = r[:n], g[:n]
    return r, g


import csv

def _read_rows(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.lstrip().startswith("#")]
    dialect = csv.Sniffer().sniff(lines[0])
    delim = dialect.delimiter if dialect.delimiter in [",",";","\\t"] else ","
    reader = csv.DictReader(lines, delimiter=delim)
    return [dict(r) for r in reader]

def _col(rows, name):
    return [float(r[name]) for r in rows if r.get(name,"").strip() not in ["","nan","NaN","None"]]

