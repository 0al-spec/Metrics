# AGENTS.md

Guidance for agents working with this LaTeX paper repository.

## Building the document

Use the Makefile to compile:

```bash
make build       # Compile the PDF
make view        # Compile and open the PDF
make clean       # Remove build artifacts (keep PDF)
make distclean   # Remove all artifacts including PDF
```

Or compile manually:

```bash
cd SIB
pdflatex metrics.tex
```

After making changes to `metrics.tex` or `metrics.bib`, always recompile to verify no errors were introduced.

## Validation

- After editing `metrics.tex`, check the compilation output for warnings or errors. Common issues include unmatched braces, missing packages, or broken citations.
- If you modify citations, ensure they exist in `metrics.bib` with correct formatting.
- The document uses the `aastex701` class (astronomy/astrophysics format). Respect existing formatting conventions.

## Document structure

- The paper emphasizes that all defined metrics (SIB, IY, ICC, FC) are **non-normative** and diagnostic. Never rewrite sections in a way that suggests these metrics should be used for optimization or performance evaluation.
- Maintain the distinction between sections: Introduction → Analytic Framework → Discussion → Relation to Existing Metrics → Threats to Validity.
- Mathematical notation uses standard LaTeX: `\mathrm{}` for text in equations, subscripts with underscores.

## Editing guidelines

- When adding or removing sections, update the line number references in CLAUDE.md if they change.
- Preserve the two-column layout defined by `\documentclass[twocolumn]{aastex701}` unless explicitly requested otherwise.
- The bibliography style is `aasjournalv7.bst`—do not switch bibliography styles without coordination.
- Author information (name, email, affiliation) is defined in the preamble. Update carefully.

## File conventions

- Main content: `metrics.tex`
- Citations: `metrics.bib` (BibTeX format)
- Do not commit generated files: `metrics.pdf`, `metrics.aux`, `metrics.log`, `metrics.out`, `metrics.fdb_latexmk`, `metrics.fls`
- The `.gitignore` should already exclude these; verify before committing.

## Commit guidelines

- Write clear commit messages that describe the change: "Expand Threats to Validity section" or "Fix citation formatting in References"
- Small edits (typos, rephrasing) can be grouped into a single commit.
- Structural changes (new sections, reorganization) warrant separate commits.
- Always compile successfully before committing.
