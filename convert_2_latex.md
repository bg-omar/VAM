### 📙 `convert_to_latex.md` (Action-Specific)

This separate file contains a short, clear, actionable prompt specifically instructing GPT on converting plain text mathematical derivations into LaTeX.

Example content:

```markdown
# Action: Convert Plain-Text Derivation to LaTeX

As a specialized VAM LaTeX assistant (see `assistant.md` for detailed formatting and editing guidelines), your specific task here is:

1. Take provided plain-text mathematical derivations.
2. Convert them into rigorously formatted LaTeX equations using AMS math standards.
3. Clearly label equations (`\label{eq:<descriptive-label>}`) for cross-referencing.
4. Include BibTeX citations for any external sources.
5. Verify equations numerically against provided constants from:
   - `./VAM Benchmarks/constants.py`
   - `./physical_constants_latex.pdf`

Provide your output as a **clearly delimited LaTeX code snippet**, ready to paste directly into the manuscript.

Include comments highlighting key edits made or suggesting additional improvements.
```