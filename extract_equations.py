import os
import re
import json
from pathlib import Path


def build_constant_mapping(constants_path: str) -> dict:
    text = Path(constants_path).read_text(encoding='utf-8')
    entry_re = re.compile(r'"(?P<key>[^"]+)": PhysicalConstant\(r"(?P<latex>.*?)"')
    entries = dict(entry_re.findall(text))

    assign_re = re.compile(r'(?P<var>[A-Za-z_][A-Za-z0-9_]*) = constants_dict\["(?P<key>[^"]+)"\]\.value')
    mapping = {}
    for var, key in assign_re.findall(text):
        latex = entries.get(key)
        if latex:
            mapping[latex] = var
            mapping[key] = var  # allow simple key replacement
    return mapping


def latex_to_python(expr: str, mapping: dict) -> str:
    out = expr.replace('\n', ' ')
    # replace fractions iteratively
    frac_re = re.compile(r'\\frac\{([^{}]+)\}\{([^{}]+)\}')
    while True:
        new = frac_re.sub(r'(\1)/(\2)', out)
        if new == out:
            break
        out = new
    out = re.sub(r'\\left|\\right', '', out)
    out = out.replace('\\cdot', '*')
    out = re.sub(r'\^{\s*([^{}]+)\s*}', r'**(\1)', out)
    out = re.sub(r'\^([A-Za-z0-9]+)', r'**(\1)', out)
    out = out.replace('\\', ' ')
    out = out.replace('{', '').replace('}', '')
    for latex, var in mapping.items():
        token = latex.replace('{', '').replace('}', '')
        out = out.replace(token, var)
    out = ' '.join(out.split())
    return out


def extract_equations(tex_path: Path, mapping: dict) -> dict:
    pattern = re.compile(r'\\begin\{(equation|align|gather)(\*?)\}(.*?)\\end{\1\2}', re.DOTALL)
    label_re = re.compile(r'\\label\{([^}]+)\}')
    equations = {}
    content = tex_path.read_text(encoding='utf-8')
    for idx, match in enumerate(pattern.findall(content)):
        _, _, body = match
        label_match = label_re.search(body)
        label = label_match.group(1) if label_match else f'{tex_path.stem}_{idx}'
        body = label_re.sub('', body)
        python_expr = latex_to_python(body, mapping)
        equations[label] = python_expr
    return equations


def main():
    constants_path = Path('Python VAM Benchmarks/constants.py')
    mapping = build_constant_mapping(constants_path)

    translation_dirs = {
        'VAM - 1 TimeDilation': 'TimeDilation',
        'VAM - 2 Swirl Clocks': 'Swirl_Clocks',
    }

    out_root = Path('out/equations')
    out_root.mkdir(parents=True, exist_ok=True)

    vam_bases = [p for p in Path('../tools').iterdir() if p.is_dir() and p.name.startswith('VAM -')]
    total = 0
    for base in vam_bases:
        if base.name.startswith('VAM - 2'):
            # Swirl Clocks already extracted
            continue

        sub = translation_dirs.get(base.name)
        search_dir = base / sub if sub else base

        all_eqs: dict[str, str] = {}
        for tex in search_dir.rglob('*.tex'):
            eqs = extract_equations(tex, mapping)
            all_eqs.update(eqs)

        if not all_eqs:
            continue

        safe_name = re.sub(r'[\s/]', '_', base.name)
        out_path = out_root / f'{safe_name}.json'
        with out_path.open('w', encoding='utf-8') as f:
            json.dump(all_eqs, f, indent=2)
        print(f'Extracted {len(all_eqs)} equations from {search_dir} to {out_path}')
        total += len(all_eqs)

    print(f'Total equations extracted: {total}')


if __name__ == '__main__':
    main()
