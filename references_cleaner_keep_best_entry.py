import re
from collections import defaultdict
from pathlib import Path

INPUT_BIB = "references.bib"
OUTPUT_BIB = "references.bib"

def normalize_key(key):
    return re.sub(r'[^a-z0-9]', '', key.lower())

def extract_key(entry):
    match = re.match(r"@\w+\{([^,]+),", entry.strip())
    return match.group(1).strip() if match else None

def score_entry(entry):
    """Score entry by presence of valuable metadata fields"""
    fields = ['doi', 'journal', 'publisher', 'volume', 'year', 'pages', 'booktitle', 'url', 'note']
    return sum(1 for f in fields if f"{f.lower()} =" in entry.lower())

# Load .bib file
with open(INPUT_BIB, encoding="utf-8") as f:
    lines = f.readlines()

# Parse entries
entries = []
current_entry = []
brace_count = 0

for line in lines:
    if line.strip().startswith("@") and brace_count == 0:
        current_entry = [line]
        brace_count = line.count("{") - line.count("}")
    else:
        current_entry.append(line)
        brace_count += line.count("{") - line.count("}")

    if brace_count == 0 and current_entry:
        entries.append("".join(current_entry).strip())
        current_entry = []

for i, entry in enumerate(entries):
    if entry.count("{") != entry.count("}"):
        print(f"⚠️ Unbalanced braces in entry #{i}:\n", entry)


# Collect keys and resolve duplicates
entry_groups = defaultdict(list)
normalized_keys = defaultdict(list)
duplicates = set()
case_mismatches = []

for entry in entries:
    key = extract_key(entry)
    if not key:
        continue
    norm = normalize_key(key)
    entry_groups[key].append(entry)
    normalized_keys[norm].append(key)

# Case mismatch detection
for norm, variants in normalized_keys.items():
    if len(set(variants)) > 1:
        case_mismatches.append(variants)

# Best-entry resolution
final_entries = {}
for key, group in entry_groups.items():
    if len(group) == 1:
        final_entries[key] = group[0]
    else:
        best = max(group, key=score_entry)
        final_entries[key] = best
        duplicates.add(key)

# Write to cleaned .bib
with open(OUTPUT_BIB, "w", encoding="utf-8") as f:
    for key in sorted(final_entries.keys(), key=lambda x: x.lower()):
        f.write(final_entries[key].strip() + "\n\n")

# Report
print("✅ Cleaned and sorted .bib written to:", OUTPUT_BIB)
print(f"\n🟡 Resolved {len(duplicates)} duplicate keys by keeping best entry:")
for key in sorted(duplicates):
    print("   ✔", key)
print("\n⚠️ Case-mismatched keys (check your \\cite commands):")
for group in sorted(case_mismatches, key=lambda g: g[0].lower()):
    print("  -", ", ".join(group))
