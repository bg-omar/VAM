import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
import argparse
import shutil

# Priority keywords
priority_words = ["iskandarani", "vam", "æther"]


def normalize_key(key):
    return re.sub(r'[^a-z0-9]', '', key.lower())

def extract_key(entry):
    match = re.match(r"@\w+\{([^,]+),", entry.strip())
    return match.group(1).strip() if match else None

def score_entry(entry):
    fields = ['doi', 'journal', 'publisher', 'volume', 'year', 'pages', 'booktitle', 'url', 'note']
    return sum(1 for f in fields if f"{f.lower()} =" in entry.lower())

def backup_file(path: Path):
    if path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        shutil.copy(path, backup_path)
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

def clean_bib(bib_path, dry_run, backup, delete_redundant, priority_keywords=None):

    with open(bib_path, encoding="utf-8") as f:
        content = f.read()
    entries = extract_entries(content)

    entry_groups = defaultdict(list)
    normalized_keys = defaultdict(list)
    duplicates = set()
    case_mismatches = []

    for i, entry in enumerate(entries):
        if entry.count("{") != entry.count("}"):
            print(f"⚠️ Unbalanced braces in entry #{i}:\n", entry)

    for entry in entries:
        key = extract_key(entry)
        if not key:
            continue
        norm = normalize_key(key)
        entry_groups[key].append(entry)
        normalized_keys[norm].append(key)

    for norm, variants in normalized_keys.items():
        if len(set(variants)) > 1:
            case_mismatches.append(variants)

    final_entries = {}
    for key, group in entry_groups.items():
        if len(group) == 1:
            final_entries[key] = group[0]
        else:
            best = max(group, key=score_entry)
            final_entries[key] = best
            duplicates.add(key)

    # Lowercase all priority words once
    priority_keywords = [w.lower() for w in (priority_keywords or [])]

    def priority_score(entry):
        content = entry.lower()
        return any(word in content for word in priority_keywords)

    sorted_keys = sorted(
        final_entries.keys(),
        key=lambda k: (not priority_score(final_entries[k]), k.lower())
    )

    if not dry_run:
        if backup:
            backup_file(Path(bib_path))
        with open(bib_path, "w", encoding="utf-8") as f:
            for key in sorted_keys:
                f.write(final_entries[key].strip() + "\n\n")

    print("\n✅ Cleaned .bib written to:", bib_path)
    print(f"\n🟡 Resolved {len(duplicates)} duplicate keys by keeping best entry:")
    for key in sorted(duplicates):
        print("   ✔", key)
    print("\n⚠️ Case-mismatched keys (check your \\cite commands):")
    for group in sorted(case_mismatches, key=lambda g: g[0].lower()):
        print("  -", ", ".join(group))

    return entries, entry_groups

def harmonize_tex(tex_dir, groups, dry_run, backup, delete_redundant, bib_path):
    replacements = {}
    for normkey, versions in groups.items():
        if len(versions) < 2:
            continue
        keys = [k for k, _ in versions]
        bodies = [re.sub(r"@\w+\{[^,]+,", "@TYPE{", e).strip() for _, e in versions]
        for i in range(len(bodies)):
            for j in range(i+1, len(bodies)):
                sim = SequenceMatcher(None, bodies[i], bodies[j]).ratio()
                if sim > 0.98:
                    old_key = keys[j]
                    new_key = keys[i]
                    if new_key != old_key:
                        replacements[old_key] = new_key

    cite_re = re.compile(r"\\cite\w*\{([^}]+)\}")
    print("🔁 Replacement map:", replacements)
    for texfile in Path(tex_dir).rglob("*.tex"):
        changed = False
        lines = []
        with open(texfile, encoding="utf-8") as f:
            for line in f:
                def repl(match):
                    keys = match.group(1).split(",")
                    new_keys = [replacements.get(k.strip(), k.strip()) for k in keys]
                    prefix = match.group(0)[: match.group(0).find("{") + 1]
                    return prefix + ", ".join(new_keys) + "}"

                newline = cite_re.sub(repl, line)
                if newline != line:
                    changed = True
                lines.append(newline)

        if changed:
            if backup and not dry_run:
                backup_file(texfile)
            if not dry_run:
                with open(texfile, "w", encoding="utf-8") as f:
                    f.writelines(lines)
            print(f"{'✅' if not dry_run else '🟡'} {'Would update' if dry_run else 'Updated'}: {texfile}")

    if delete_redundant:
        new_entries = []
        for normkey, versions in groups.items():
            keep_key = replacements.get(versions[1][0], versions[0][0])
            for key, entry in versions:
                if key == keep_key or key not in replacements:
                    new_entries.append(entry)
        if not dry_run:
            if backup:
                backup_file(Path(bib_path))
            with open(bib_path, "w", encoding="utf-8") as f:
                f.write("\n\n".join(new_entries))
            print("🧹 Cleaned .bib file with redundant keys removed.")

    print("\n🔁 Harmonized citation keys:")
    for old, new in sorted(replacements.items()):
        print(f"  {old} → {new}")
    if dry_run:
        print("\n🟡 DRY RUN: No files were modified.")

def main():
    parser = argparse.ArgumentParser(description="Clean and harmonize .bib and .tex files")
    parser.add_argument("--bib", type=str, default="references.bib", help="Path to .bib file")
    parser.add_argument("--tex-dir", type=str, default=".", help="Root directory of .tex files")
    parser.add_argument("--real-run", action="store_true", help="Actually modify files")
    parser.add_argument("--no-backup", action="store_true", help="Disable file backups")
    parser.add_argument("--delete-redundant", action="store_true", help="Delete redundant .bib entries")
    parser.add_argument("--priority-keywords", type=str, nargs="+", default=["iskandarani", "VAM", "Æther"], help="List of words to prioritize when sorting .bib entries")

    args = parser.parse_args()

    dry_run = not args.real_run

    print("🛠️ DRY RUN MODE: No files will be modified unless you confirm later.\n")

    entries, entry_groups = clean_bib(
        bib_path=args.bib,
        dry_run=True,
        backup=not args.no_backup,
        delete_redundant=args.delete_redundant,
        priority_keywords=args.priority_keywords,
    )

    grouped = defaultdict(list)
    for e in entries:
        key = extract_key(e)
        if key:
            grouped[key.lower()].append((key, e))

    harmonize_tex(
        tex_dir=args.tex_dir,
        groups=grouped,
        dry_run=True,
        backup=not args.no_backup,
        delete_redundant=args.delete_redundant,
        bib_path=args.bib
    )

    # Ask to confirm real run
    if not args.real_run:
        response = input("\n💡 Do you want to apply these changes? [y/N]: ").strip().lower()
        if response == "y":
            print("\n🔁 Applying changes now...\n")
            entries, entry_groups = clean_bib(
                bib_path=args.bib,
                dry_run=False,
                backup=not args.no_backup,
                delete_redundant=args.delete_redundant,
                priority_keywords=args.priority_keywords
            )
            grouped = defaultdict(list)
            for e in entries:
                key = extract_key(e)
                if key:
                    grouped[key.lower()].append((key, e))
            harmonize_tex(
                tex_dir=args.tex_dir,
                groups=grouped,
                dry_run=False,
                backup=not args.no_backup,
                delete_redundant=args.delete_redundant,
                bib_path=args.bib
            )
        else:
            print("❌ No changes made. Exiting.")


if __name__ == "__main__":
    main()
