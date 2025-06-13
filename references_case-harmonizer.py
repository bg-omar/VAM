import re
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict

DRY_RUN = False   # Toggle this to True for testing
BACKUP_BIB = True
BACKUP_TEX = True
DELETE_REDUNDANT_KEYS = False  # Only if you're confident they're identical


bib_path = "references.bib"
tex_root = Path(".")

def backup_file(path: Path):
    if path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        path.replace(backup_path)
        print(f"📦 Backup created: {backup_path}")


def extract_entries(text):
    entries = []
    brace_count = 0
    current = []
    for line in text.splitlines(keepends=True):
        if line.strip().startswith("@") and brace_count == 0:
            current = [line]
            brace_count += line.count("{") - line.count("}")
        else:
            current.append(line)
            brace_count += line.count("{") - line.count("}")
        if brace_count == 0:
            entries.append("".join(current))
    return entries

# Load entries
with open(bib_path, encoding="utf-8") as f:
    content = f.read()
entries = extract_entries(content)

# Group by lowercase key
def get_key(e):
    return re.search(r"@\w+\{([^,]+),", e).group(1)
groups = defaultdict(list)
for e in entries:
    key = get_key(e)
    groups[key.lower()].append((key, e))

# Filter case-mismatch groups with similar content
replacements = {}
for normkey, versions in groups.items():
    if len(versions) < 2:
        continue
    keys = [k for k, _ in versions]
    bodies = [re.sub(r"@\w+\{[^,]+,", "@TYPE{", e).strip() for _, e in versions]
    for i in range(len(bodies)):
        for j in range(i+1, len(bodies)):
            sim = SequenceMatcher(None, bodies[i], bodies[j]).ratio()
            if sim > 0.98:  # 98% similar — assume duplicate
                old_key = keys[j]
                new_key = keys[i]
                if new_key != old_key:
                    replacements[old_key] = new_key

# Replace in all .tex files
cite_re = re.compile(r"\\cite\{([^}]+)\}")
for texfile in tex_root.rglob("*.tex"):
    changed = False
    lines = []
    with open(texfile, encoding="utf-8") as f:
        for line in f:
            def repl(match):
                keys = match.group(1).split(",")
                new_keys = [replacements.get(k.strip(), k.strip()) for k in keys]
                return f"\\cite{{{','.join(new_keys)}}}"
            newline = cite_re.sub(repl, line)
            if newline != line:
                changed = True
            lines.append(newline)

    if changed:
        if BACKUP_TEX and not DRY_RUN:
            backup_file(texfile)
        if not DRY_RUN:
            with open(texfile, "w", encoding="utf-8") as f:
                f.writelines(lines)
        print(f"{'✅' if not DRY_RUN else '🟡'} {'Would update' if DRY_RUN else 'Updated'}: {texfile}")

if DELETE_REDUNDANT_KEYS:
    new_entries = []
    for normkey, versions in groups.items():
        keep_key = replacements.get(versions[1][0], versions[0][0])
        for key, entry in versions:
            if key == keep_key or key not in replacements:
                new_entries.append(entry)
    if not DRY_RUN:
        if BACKUP_BIB:
            backup_file(Path(bib_path))
        with open(bib_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(new_entries))
        print("🧹 Cleaned .bib file with redundant keys removed.")

print("\n🔁 Harmonized citation keys:")
for old, new in sorted(replacements.items()):
    print(f"  {old} → {new}")
if DRY_RUN:
    print("\n🟡 DRY RUN: No files were modified.")
