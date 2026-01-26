# Contributing and License Information

This document explains the contribution process and licensing for the SIB Metrics repository.

## 📜 Dual Licensing

This repository uses **dual licensing** to accommodate different types of content:

### 1. Research Papers (CC BY 4.0)

**Applies to:**
- `SIB/` - SIB paper and related materials
- Academic publications
- Research documentation

**License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

**You are free to:**
- Share — copy and redistribute
- Adapt — remix, transform, and build upon

**Under these terms:**
- Attribution — You must give appropriate credit

### 2. Software Tools (MIT License)

**Applies to:**
- `extract_metrics.py` - Main extractor script
- `test_output_modes.py` - Unit tests
- `requirements-extractor.txt` - Dependencies
- `example_spec.md` - Test fixture
- `docs/extractor/` - Tool documentation

**License:** [MIT License](LICENSE-EXTRACTOR)

**You are free to:**
- Use commercially
- Modify
- Distribute
- Private use

**With minimal restrictions:**
- Must include copyright notice
- Must include license text
- No warranty

## 🤝 How to Contribute

### For the Extractor Tool

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

1. **Reporting Bugs** - How to file good bug reports
2. **Suggesting Features** - How to propose enhancements
3. **Code Contributions** - Development setup and standards
4. **Pull Requests** - Submission process
5. **Testing** - How to write and run tests
6. **Documentation** - How to update docs

### For Research Papers

If you want to contribute to the SIB paper or suggest improvements:

1. **Open an Issue** - Describe the proposed change
2. **Provide Context** - Why is this improvement needed?
3. **Academic Discussion** - Reference related work if applicable
4. **LaTeX Changes** - If submitting code, follow existing style

## 📋 Contribution Quick Start

### Report a Bug
```
1. Check existing issues
2. Open a new issue
3. Include: description, steps to reproduce, expected vs actual behavior
4. Add: environment details (OS, Python version, LLM)
```

### Suggest a Feature
```
1. Check existing issues and discussions
2. Open a new issue with "Enhancement" label
3. Describe: use case, proposed solution, alternatives
4. Discuss with maintainers before implementing
```

### Submit Code

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/Metrics.git

# 2. Create branch
git checkout -b feature/your-feature

# 3. Make changes
# ... edit code ...

# 4. Test
python test_output_modes.py

# 5. Commit
git commit -m "Add feature: description"

# 6. Push
git push origin feature/your-feature

# 7. Open Pull Request on GitHub
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🎯 What to Contribute

### Good First Issues
- Documentation improvements
- Bug fixes
- Example additions
- Test coverage improvements

### Feature Ideas
- Support for additional LLM providers
- New output formats
- Performance optimizations
- CI/CD integrations

### Research Contributions
- Case studies using SIB metrics
- Validation studies
- Extensions to the framework
- Integration with other metrics

## 📝 Code of Conduct

### Be Respectful
- Treat all contributors with respect
- Welcome diverse perspectives
- Be patient with newcomers

### Be Constructive
- Provide actionable feedback
- Explain reasoning clearly
- Suggest improvements

### Be Collaborative
- Work toward common goals
- Help others succeed
- Share knowledge

## 🔗 Quick Links

- **Contributing Guide**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **MIT License (Tool)**: [LICENSE-EXTRACTOR](LICENSE-EXTRACTOR)
- **CC BY 4.0 (Papers)**: [Creative Commons](https://creativecommons.org/licenses/by/4.0/)
- **Documentation**: [docs/extractor/](docs/extractor/)
- **Issues**: [GitHub Issues](https://github.com/anthropics/Metrics/issues) (when published)

## 🙏 Acknowledgments

### Contributors

Thank you to all contributors who help improve the SIB Metrics project!

### Citations

If you use the SIB framework in your research, please cite:

```bibtex
@article{merkushev2026sib,
  title={Specification-Implementation Balance: A Diagnostic Framework for AI-Mediated Software Construction},
  author={Merkushev, Egor},
  year={2026}
}
```

### Tools and Libraries

This project builds on:
- Python and its excellent ecosystem
- Ollama and LM Studio for local LLM inference
- The open source community

## ❓ Questions?

### For Tool Usage
- Check [docs/extractor/EXTRACTOR_README.md](docs/extractor/EXTRACTOR_README.md)
- See [docs/extractor/QUICK_REFERENCE.md](docs/extractor/QUICK_REFERENCE.md)

### For Contributing
- Read [CONTRIBUTING.md](CONTRIBUTING.md)
- Open an issue for questions

### For Research
- Read the [SIB paper](SIB/metrics.pdf)
- Open an issue for academic discussion

## 📧 Contact

For questions not covered in documentation:
- **Issues**: Open a GitHub issue
- **Email**: See repository maintainer information

---

Thank you for your interest in contributing to SIB Metrics! 🎉
