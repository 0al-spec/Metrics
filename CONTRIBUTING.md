# Contributing to SIB Metrics Extractor

Thank you for your interest in contributing to the SIB Metrics Extractor! This document provides guidelines for contributing to the tool.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [License](#license)

## 🤝 Code of Conduct

This project follows a simple code of conduct:

- **Be respectful** - Treat all contributors with respect
- **Be constructive** - Provide helpful feedback
- **Be collaborative** - Work together toward common goals
- **Be patient** - Remember that everyone is learning

## 🎯 How Can I Contribute?

### Reporting Bugs

If you find a bug, please open an issue with:

1. **Clear title** - Describe the issue concisely
2. **Steps to reproduce** - How to trigger the bug
3. **Expected behavior** - What should happen
4. **Actual behavior** - What actually happens
5. **Environment** - Python version, OS, LLM used
6. **Logs/Screenshots** - If applicable

**Example:**
```
Title: JSON parsing fails with Llama 3.2 model

Steps to reproduce:
1. Run: python extract_metrics.py specs/test.md --model llama3.2
2. Observe JSON parsing error

Expected: Extract metrics successfully
Actual: Warning: Failed to parse LLM response as JSON

Environment:
- Python 3.10.0
- Ollama 0.1.20
- macOS 14.0
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

1. **Use case** - Why is this enhancement needed?
2. **Proposed solution** - How would it work?
3. **Alternatives considered** - Other approaches you thought about
4. **Impact** - Who benefits from this change?

### Contributing Code

We welcome code contributions! See sections below for guidelines.

## 🛠 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/Metrics.git
cd Metrics
```

### 2. Install Dependencies

```bash
pip install -r requirements-extractor.txt
```

### 3. Install Development Tools (Optional)

```bash
# For code formatting
pip install black

# For linting
pip install pylint flake8

# For type checking
pip install mypy
```

### 4. Set Up LLM

```bash
# Option A: Ollama
ollama pull llama3

# Option B: LM Studio
# Download and run LM Studio, load a model
```

### 5. Run Tests

```bash
python test_output_modes.py
```

## 📝 Coding Standards

### Python Style

Follow [PEP 8](https://peps.python.org/pep-0008/) with these specifics:

- **Indentation**: 4 spaces (no tabs)
- **Line length**: 100 characters (soft limit)
- **Imports**: Grouped by standard lib, third-party, local
- **Docstrings**: Use for all public functions/classes

**Example:**
```python
def extract_intent_atoms(self, content: str) -> List[IntentAtom]:
    """Extract intent atoms from specification content

    Args:
        content: Markdown specification text

    Returns:
        List of IntentAtom objects extracted from content

    Raises:
        ValueError: If content is empty
    """
    if not content:
        raise ValueError("Content cannot be empty")

    # Implementation...
```

### Code Formatting

We recommend using `black` for consistent formatting:

```bash
# Format a file
black extract_metrics.py

# Check formatting
black --check extract_metrics.py
```

### Type Hints

Use type hints for function signatures:

```python
from typing import List, Dict, Optional
from pathlib import Path

def process_file(path: Path, output: Optional[str] = None) -> Dict[str, Any]:
    """Process a specification file"""
    pass
```

### Error Handling

- Use specific exception types
- Provide helpful error messages
- Log errors appropriately

```python
try:
    data = json.loads(response)
except json.JSONDecodeError as e:
    print(f"Warning: Failed to parse JSON: {e}")
    print(f"Response was: {response[:200]}...")
    return []
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python test_output_modes.py

# Run with verbose output
python test_output_modes.py -v
```

### Writing Tests

When adding new features, include tests:

```python
def test_new_feature():
    """Test description"""
    # Arrange
    input_data = Path("test_input.md")

    # Act
    result = extract_metrics(input_data)

    # Assert
    assert result.n_spec > 0
    assert result.n_func > 0
```

### Test Coverage

Aim for:
- **90%+ coverage** for core functionality
- **100% coverage** for utility functions
- **Edge cases** tested explicitly

## 📚 Documentation

### Code Documentation

- **Docstrings** for all public functions/classes
- **Inline comments** for complex logic
- **Type hints** for function signatures

### User Documentation

When adding features, update:
- `docs/extractor/EXTRACTOR_README.md` - Main documentation
- `docs/extractor/QUICK_REFERENCE.md` - Command examples
- `docs/extractor/README.md` - Documentation index if needed

### Examples

Provide examples for new features:

```markdown
## New Feature: Batch Processing

Process multiple directories in parallel:

\`\`\`bash
python extract_metrics.py specs1/ specs2/ --parallel
\`\`\`
```

## 🔄 Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Use prefixes:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions/changes

### 2. Make Changes

- Write clear, focused commits
- Follow coding standards
- Add tests for new features
- Update documentation

### 3. Commit Changes

Write clear commit messages:

```bash
git commit -m "Add parallel processing support

- Add --parallel flag for concurrent extraction
- Update documentation with examples
- Add tests for parallel execution
- Handle thread-safe JSON writing"
```

**Format:**
```
Title (50 chars or less)

- Bullet point 1
- Bullet point 2
- Bullet point 3
```

### 4. Run Tests

```bash
# Run tests
python test_output_modes.py

# Check formatting
black --check extract_metrics.py

# Verify no temp files
git status --ignored
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:

**Title:** Clear description (e.g., "Add parallel processing support")

**Description:**
```markdown
## Changes
- Brief description of what changed

## Motivation
- Why is this change needed?

## Testing
- How was this tested?
- What edge cases were considered?

## Documentation
- What documentation was updated?

## Breaking Changes
- Are there any breaking changes?
- How should users migrate?
```

### 6. Review Process

- Maintainers will review your PR
- Address feedback constructively
- Make requested changes
- Once approved, your PR will be merged

### 7. After Merge

```bash
# Update your fork
git checkout main
git pull upstream main
git push origin main

# Delete feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

## 🎨 Contribution Ideas

Looking for something to work on? Consider:

### Easy (Good First Issues)
- [ ] Add support for new LLM providers
- [ ] Improve error messages
- [ ] Add more examples to documentation
- [ ] Fix typos in documentation

### Medium
- [ ] Add progress bar for batch processing
- [ ] Implement caching for LLM responses
- [ ] Add retry logic with exponential backoff
- [ ] Support for more input formats (RST, AsciiDoc)

### Advanced
- [ ] Parallel processing with threading/multiprocessing
- [ ] JSON schema validation for structured outputs
- [ ] Plugin system for custom extractors
- [ ] Web UI for interactive extraction
- [ ] Integration with CI/CD systems

## 🐛 Known Issues

Check the [issues page](https://github.com/anthropics/Metrics/issues) for current known issues.

## 📧 Questions?

- **Documentation**: Check `docs/extractor/` first
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the **MIT License** (see LICENSE-EXTRACTOR file).

Note: The SIB paper (`SIB/`) is licensed under CC BY 4.0, while the extractor tool is under MIT License.

## 🙏 Acknowledgments

Thank you for contributing to the SIB Metrics Extractor! Your contributions help make AI-assisted software development more observable and measurable.

---

**Happy Contributing!** 🎉
