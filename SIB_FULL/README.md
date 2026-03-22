# SIB Full Metrics

This directory contains the extended LaTeX paper and a local PDF build
pipeline equivalent to the one used in `SIB`.

## Quick Start

To compile the PDF:

```bash
make build
make view
make clean
```

Or manually:

```bash
pdflatex sib_full_metrics.tex
```

## Project Files

- `sib_full_metrics.tex` - Main LaTeX document
- `aastex701.cls` - AAS LaTeX document class required for compilation
- `Makefile` - Build automation
- `sib_full_metrics.pdf` - Compiled document (generated)
