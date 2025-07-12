from pathlib import Path
import re
import bibtexparser

bib_path = Path("VAM_15_Quantum_Gravity.bib")
tex_path = Path("VAM_15_Quantum_Gravity.tex")

# Parse the bib file robustly
with open(bib_path, encoding='utf-8') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

bib_entries = {}
for entry in bib_database.entries:
    if entry.get('ID', '').startswith('reference_') and 'note' in entry:
        ref_key = entry['ID']
        # Match "VAM-xx. ..." at the beginning of note, robust to line breaks
        m = re.match(r'(VAM-\d+)\.\s*(.*)', entry['note'], re.DOTALL)
        if m:
            vam_code = m.group(1).replace("-", "")
            note = m.group(2).strip()
            bib_entries[ref_key] = (vam_code, note)
        else:
            print(f"Could not parse note for {ref_key}: {entry['note']}")

# Replace citations
def replace_cite(match):
    ref_key = match.group(1)
    if ref_key in bib_entries:
        vam_code, footnote = bib_entries[ref_key]
        return f"\\cite{{{vam_code}}}\\footnote{{{footnote}}}"
    else:
        return match.group(0)

tex_content = tex_path.read_text(encoding="utf-8")
tex_updated = re.sub(r'\\cite\{(reference_\d+)\}', replace_cite, tex_content)

output_path = Path("VAM_15_Quantum_Gravity_updated.tex")
output_path.write_text(tex_updated, encoding="utf-8")

print("Done! Output written to VAM_15_Quantum_Gravity_updated.tex")
