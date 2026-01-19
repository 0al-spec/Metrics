# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a LaTeX academic paper titled "Specification-Implementation Balance: A Diagnostic Framework for AI-Mediated Software Construction" by Egor Merkushev. The paper introduces non-normative diagnostic metrics for analyzing AI-assisted software development.

## Building and Compiling

Use the Makefile for common tasks:

```bash
make build       # Compile the PDF
make clean       # Remove build artifacts (keep PDF)
make distclean   # Remove all artifacts including PDF
make view        # Compile and open the PDF
make help        # Show available targets
```

Manual compilation:

```bash
cd SIB
pdflatex metrics.tex
```

Alternative build commands using `latexmk`:

```bash
# Compile the main document
latexmk -pdf metrics.tex

# Clean build artifacts
latexmk -c metrics.tex

# Clean all artifacts including PDF
latexmk -C metrics.tex
```

## Document Structure

- **Main document**: `metrics.tex` - Contains the complete paper
- **Bibliography**: `sample701.bib` - References and citations
- **LaTeX class**: `aastex701.cls` - AAS LaTeX document class (astronomy/astrophysics formatting)
- **Bibliography style**: `aasjournalv7.bst` - AAS bibliography style
- **Output**: `metrics.pdf` - Compiled PDF
- **Images**: `orcid-ID.png` - Author ORCID image

## Document Content

The paper defines several key metrics:

1. **Specification-Implementation Balance (SIB)**: `N_spec / S_impl` - Distribution of semantic intent between specification and code
2. **Intent Yield (IY)**: `N_func / N_spec` - Observable functionality per unit intent
3. **Intent Conversion Cost (ICC)**: `C_inf / N_spec` - Economic cost of AI-mediated intent realization
4. **Functional Cost (FC)**: `C_inf / N_func` - Cost per unit of observable functionality

The paper explicitly emphasizes that these metrics are **non-normative** and diagnostic in nature—not intended for optimization, ranking, or performance evaluation.

## License

The repository is licensed under CC BY 4.0 (Creative Commons Attribution 4.0 International).

## Key Sections in metrics.tex

- **Introduction** (lines 22-34): Motivation for shifting from code-centric to intent-centric metrics
- **Analytic Framework** (lines 35-96): Formal definitions of Intent Atoms, Functional Output, and AI Inference Footprint
- **Discussion** (lines 98-110): Non-normative interpretation of metrics
- **Relation to Existing Metrics** (lines 112-197): Comparison with Function Points, Requirements Traceability, and Test Coverage
- **Threats to Validity** (lines 199-266): Limitations including construct validity, measurement subjectivity, and risk of metric misuse

## Common Tasks

- **Edit the paper**: Modify `metrics.tex` directly
- **Update bibliography**: Edit `sample701.bib` and recompile
- **Recompile with clean state**: Run `latexmk -C && latexmk -pdf metrics.tex`
