# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains LaTeX academic papers on metrics for AI-driven development. Currently includes one paper:

- **SIB (Specification-Implementation Balance)**: A non-normative diagnostic framework for observing the balance between specification, implementation, and AI inference cost in AI-assisted software development.

## Building

All documents are in the `SIB/` directory. From that directory:

```bash
cd SIB
```

```bash
make build       # Compile to PDF
make view        # Compile and open PDF
make clean       # Remove build artifacts (keep PDF)
make distclean   # Remove all artifacts including PDF
```

Manual compilation:
```bash
pdflatex metrics.tex
```

## Project Structure

```
SIB/
  metrics.tex     # Main LaTeX document
  metrics.bib     # Bibliography
  aastex701.cls   # AAS LaTeX document class
  aasjournalv7.bst # AAS bibliography style
  CLAUDE.md       # Detailed guidance for the SIB paper
  AGENTS.md       # Guidelines for agents editing the document
```

## Key Constraints

- The SIB metrics are **non-normative and diagnostic**. Never suggest they should be used for optimization or performance evaluation.
- After editing `.tex` or `.bib` files, always recompile to verify no errors.
- The document uses `aastex701` class (astronomy/astrophysics formatting). Preserve existing formatting conventions.

## License

CC BY 4.0 (Creative Commons Attribution 4.0 International)
