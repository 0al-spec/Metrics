# Metrics

Metrics for AI-Driven Development under CC BY 4.0 license.

## Papers

1. **[SIB - Specification-Implementation Balance](SIB/metrics.pdf)** - A non-normative diagnostic framework for observing the balance between specification (intent), implementation (code), and AI inference cost in modern AI-assisted software development. Rather than proposing optimization targets or productivity metrics, the framework is designed to expose structural and economic shifts in the process of intent-to-implementation conversion.

## Tools

### SIB Metrics Extractor

LLM-driven extraction tool for analyzing specification documents and computing SIB metrics.

**Quick Start:**
```bash
pip install -r requirements-extractor.txt
python extract_metrics.py specs/ --base-url http://localhost:11434
```

**Documentation:** [docs/extractor/](docs/extractor/)

**Features:**
- Extracts Intent Atoms (N_spec) and Functional Units (N_func) from markdown specifications
- Supports local LLMs (Ollama, LM Studio)
- Three output modes: default, alongside, custom
- Structured JSON outputs with automatic fallback
- Batch processing with error recovery

See the [full documentation](docs/extractor/EXTRACTOR_README.md) for setup and usage.

**Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

**License:** MIT License - see [LICENSE-EXTRACTOR](LICENSE-EXTRACTOR)

## Building Papers

Each paper is in its own directory with a Makefile:

```bash
cd SIB
make build   # Compile to PDF
make view    # Compile and open PDF
```

## License

This repository uses dual licensing:

- **Papers** (`SIB/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (Creative Commons Attribution 4.0 International)
- **Extractor Tool** (`extract_metrics.py`, `docs/extractor/`, etc.): [MIT License](LICENSE-EXTRACTOR)

See individual LICENSE files for details.