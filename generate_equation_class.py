import os
import re

def latex_to_python(expr: str) -> str:
    """Convert a LaTeX math string to a Python expression string.

    Attempts to use sympy's latex parser if available.  When sympy is not
    installed, a very small set of text replacements is applied as a
    fallback so the returned expression may not be entirely accurate.
    """
    try:
        from sympy.parsing.latex import parse_latex  # type: ignore

        return str(parse_latex(expr))
    except Exception:
        # naive fallback replacements
        out = expr
        out = out.replace("^", "**")
        out = re.sub(r"\\frac\{([^}]+)\}\{([^}]+)\}", r"(\1)/(\2)", out)
        out = out.replace("\\", "")
        out = out.replace("{", "(").replace("}", ")")
        out = out.replace("sqrt", "sqrt")
        return out

BASE_DIR = "VAM - 2 Swirl Clocks"


def collect_tex_files(base: str, exclude: list[str] | None = None) -> list[str]:
    """Return all ``.tex`` files under ``base`` excluding any paths containing
    one of the ``exclude`` strings.

    Parameters
    ----------
    base:
        Directory to search recursively for ``.tex`` files.
    exclude:
        Optional list of directory name fragments to ignore while scanning.
    """

    tex_files: list[str] = []
    exclude = [e.lower() for e in exclude or []]
    for root, dirs, files in os.walk(base):
        root_lower = root.lower()
        if any(e in root_lower for e in exclude):
            continue
        for f in files:
            if f.endswith(".tex"):
                tex_files.append(os.path.join(root, f))
    tex_files.sort()
    return tex_files

pattern = re.compile(r"\\begin{equation}(.+?)\\end{equation}", re.DOTALL)


def extract_equations(
    base: str = BASE_DIR, exclude: list[str] | None = None
) -> list[str]:
    """Return a list of all LaTeX equations found under ``base``.

    Parameters
    ----------
    base:
        Directory to search for TeX files.
    exclude:
        Optional list of directory fragments to skip while scanning.
    """

    tex_files = collect_tex_files(base, exclude or ["WervelKlokken"])

    equations = []
    for path in tex_files:
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        for m in pattern.finditer(content):
            eq = m.group(1).strip()
            eq = re.sub(r"\\label\{[^}]*\}", "", eq).strip()
            equations.append(eq)
    return equations


def generate_swirl_equations() -> None:
    """Generate the ``swirl_equations.py`` module."""
    equations = extract_equations(BASE_DIR, ["WervelKlokken"])

    with open('swirl_equations.py', 'w', encoding='utf-8') as out:
        out.write('from __future__ import annotations\n')
        out.write('from typing import Optional\n')
        # Use an absolute import so the generated module can be imported
        # directly without requiring a package context.
        out.write('from generate_equation_class import latex_to_python\n\n')

        out.write('class SwirlEquations:\n')
        out.write('    """Collection of LaTeX equations extracted from VAM tex files."""\n')
        out.write('    def __init__(self):\n        pass\n\n')
        for i, eq in enumerate(equations, 1):
            func_name = f"equation_{i}"
            out.write(f'    def {func_name}(self, as_latex: bool = True) -> str:\n')
            out.write(f'        """Return equation {i} as LaTeX or Python string."""\n')
            out.write(f'        eq = r"""{eq}"""\n')
            out.write('        if as_latex:\n')
            out.write('            return eq\n')
            out.write('        return latex_to_python(eq)\n\n')

    print(f"Extracted {len(equations)} equations to swirl_equations.py")


if __name__ == "__main__":
    generate_swirl_equations()
