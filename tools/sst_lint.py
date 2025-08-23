#!/usr/bin/env python3
import re, sys, pathlib

FORBIDDEN = [
    (r'(?i)(?<!Einstein[-\s])æther', "Use 'foliation' (no 'æther' in prose)"),
    (r'(?i)\bÆther[-\s]?Time\b', "Say 'absolute time parametrization'"),
    (r'(?i)\bvortex(?!i[tc])\b', "Use 'swirl string' (no 'vortex' in prose)"),
    (r'(?i)\bvortices\b', "Use 'swirl strings'"),
]
MACROS = [
    (r'\\rho_0\b', r"Use \rhof"),
    (r'\\rho_f\b', r"Use \rhof macro"),
    (r'\\rho_E\b', r"Use \rhoE macro"),
    (r'\\rho_m(?![A-Za-z])', r"Use \rhom macro"),
    (r'\\rho_\{\\mathrm\{fluid\}\}', r"Use \rhof"),
    (r'(?<!\\)v_s\b', r"Use \vswirl"),
]
COARSE_GRAIN_OK = (re.compile(r"K\s*=\s*\\frac\{\\rhocore\\, r_c\}\{\\vswirl\}"),
                   re.compile(r"\\rhof\s*=\s*K\s*\\,?\s*\\Omega"))

def scan_file(p: pathlib.Path):
    text = p.read_text(encoding='utf-8', errors='ignore')
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        for pat, msg in FORBIDDEN + MACROS:
            for m in re.finditer(pat, line):
                col = m.start() + 1
                # JetBrains-friendly: filename:line:column: message
                out.append(f"{p}:{i}:{col}: {msg}")
    # Coarse-graining canonical check (file-level)
    cgK, cgR = COARSE_GRAIN_OK
    if ("\\rhof" in text or "\\rhocore" in text) and "K" in text:
        if not (cgK.search(text) and cgR.search(text)):
            out.append(f"{p}:1:1: EXPECTED canonical coarse-graining: K=(\\rhocore r_c)/\\vswirl and \\rhof=K\\,\\Omega")
    return out

def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    files = list(root.rglob("*.tex"))
    msgs = []
    for f in files:
        if f.name == "_notation_macros.tex":  # allow definitions here
            continue
        msgs += scan_file(f)
    if msgs:
        print("\n".join(msgs))
        sys.exit(1)
    print("sst_lint: OK")
    sys.exit(0)

if __name__ == "__main__":
    main()
