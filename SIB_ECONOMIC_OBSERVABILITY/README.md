# SIB Economic Observability

This directory contains the LaTeX paper on economic observability and a local
PDF build pipeline equivalent to the ones used in `SIB` and `SIB_FULL`.

## Quick Start

To compile the PDF:

```bash
make build
make view
make clean
```

Or manually:

```bash
pdflatex sib_economic_observability.tex
```

## Project Files

- `sib_economic_observability.tex` - Main LaTeX document
- `aastex701.cls` - AAS LaTeX document class required for compilation
- `Makefile` - Build automation
- `sib_economic_observability.pdf` - Compiled document (generated)
