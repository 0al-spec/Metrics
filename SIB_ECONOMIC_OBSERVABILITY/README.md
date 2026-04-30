# SIB Economic Observability

This directory contains the LaTeX paper on economic observability and a local
PDF build pipeline equivalent to the ones used in `SIB` and `SIB_FULL`.

## Interpretation

The paper treats economic metrics as non-normative observability signals, not
performance targets. Direct costs such as inference, verification, and build
cost are observed under an explicit pricing surface. Change and ownership costs
are structural proxies and must be labeled as such when shown in dashboards.

Economic artifacts should preserve provenance: pricing surface identifier,
model/tool versions, time window, currency or unit convention, and whether each
quantity is observed spend or a derived proxy.

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
