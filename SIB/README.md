# Specification-Implementation Balance: A Diagnostic Framework for AI-Mediated Software Construction

This repository contains a LaTeX academic paper introducing the Specification-Implementation Balance (SIB) metric framework for analyzing AI-assisted software development.

## Quick Start

To compile the PDF:

```bash
make build       # Compile to PDF
make view        # Compile and open the PDF
make clean       # Remove build artifacts
```

Or manually:

```bash
pdflatex metrics.tex
```

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Guidance for Claude Code instances working with this repository
- **[AGENTS.md](AGENTS.md)** - Guidelines for agents editing the document

## Project Files

- `metrics.tex` - Main LaTeX document
- `metrics.bib` - Bibliography and references
- `aastex701.cls` - AAS LaTeX document class
- `aasjournalv7.bst` - AAS bibliography style
- `Makefile` - Build automation
- `metrics.pdf` - Compiled document (generated)

## The SIB Framework

The paper defines five non-normative diagnostic metrics:

1. **SIB** (Specification-Implementation Balance): `N_spec / S_impl`
2. **IY** (Intent Yield): `N_func / N_spec`
3. **ICC** (Intent Conversion Cost): `C_inf / N_spec`
4. **FC** (Functional Cost): `C_inf / N_func`
5. **OY** (Operational Yield): `N_func / N_calls`

These metrics are designed for observability and analysis, not optimization or performance evaluation.

## License

CC BY 4.0 (Creative Commons Attribution 4.0 International)

## Citation

If you build on this work, please cite it with the following BibTeX template (replace the placeholders with the actual title, year, URL, etc.):

```bibtex
@misc{egorMetrics2024,
  author       = {Egor Author},
  title        = {Title of Your GitHub Project},
  howpublished = {\url{https://github.com/youruser/yourrepo}},
  year         = {2024},
  note         = {Version x.y, accessed Month Day, Year}
}
```
