# Documentation Structure

Documentation has been organized into a clean folder structure.

## 📁 Repository Structure

```
Metrics/
├── README.md                       # Main repository README
├── GIT_GUIDE.md                    # Git workflow guide
├── CONTRIBUTING.md                 # Contribution guidelines
├── CONTRIBUTING_AND_LICENSE.md     # Licensing overview
├── LICENSE-EXTRACTOR               # MIT License for extractor
│
├── extract_metrics.py              # Main extractor script
├── test_output_modes.py            # Unit tests
├── requirements-extractor.txt      # Python dependencies
├── example_spec.md                 # Test fixture
│
├── docs/                           # Documentation folder
│   └── extractor/                  # Extractor tool docs
│       ├── README.md               # Documentation index (START HERE)
│       ├── EXTRACTOR_README.md     # Main documentation
│       ├── QUICK_REFERENCE.md      # Command cheat sheet
│       ├── OUTPUT_MODES_GUIDE.md   # Output location modes
│       ├── OUTPUT_MODES_SUMMARY.md # Feature summary
│       ├── STRUCTURED_OUTPUT_IMPROVEMENTS.md  # JSON mode
│       ├── IMPLEMENTATION_COMPLETE.md         # Complete overview
│       └── extraction_test_summary.md         # Test results
│
├── SIB/                            # SIB Paper
│   ├── metrics.tex                 # LaTeX source
│   ├── metrics.pdf                 # Compiled PDF
│   ├── metrics.bib                 # Bibliography
│   ├── README.md                   # Paper documentation
│   └── CLAUDE.md                   # AI assistant guide
│
└── SPECS/                          # Specification archive (702 files)
    └── SIB/INTENT/TASK_ARCHIVE/    # Task specifications
```

## 📚 Where to Start

### For Users
1. **Quick Start**: [README.md](README.md)
2. **Extractor Docs**: [docs/extractor/README.md](docs/extractor/README.md)
3. **Setup Guide**: [docs/extractor/EXTRACTOR_README.md](docs/extractor/EXTRACTOR_README.md)

### For Developers
1. **Git Workflow**: [GIT_GUIDE.md](GIT_GUIDE.md)
2. **Implementation**: [docs/extractor/IMPLEMENTATION_COMPLETE.md](docs/extractor/IMPLEMENTATION_COMPLETE.md)
3. **Tests**: `test_output_modes.py`

### For Researchers
1. **SIB Paper**: [SIB/metrics.pdf](SIB/metrics.pdf)
2. **Paper Source**: [SIB/metrics.tex](SIB/metrics.tex)
3. **Test Results**: [docs/extractor/extraction_test_summary.md](docs/extractor/extraction_test_summary.md)

## 🎯 Documentation by Purpose

### Getting Started
| File | Purpose | Audience |
|------|---------|----------|
| [README.md](README.md) | Repository overview | Everyone |
| [docs/extractor/README.md](docs/extractor/README.md) | Documentation index | Users |
| [docs/extractor/EXTRACTOR_README.md](docs/extractor/EXTRACTOR_README.md) | Setup & usage | Users |
| [docs/extractor/QUICK_REFERENCE.md](docs/extractor/QUICK_REFERENCE.md) | Command cheatsheet | Users |

### Features & Guides
| File | Purpose | Audience |
|------|---------|----------|
| [docs/extractor/OUTPUT_MODES_GUIDE.md](docs/extractor/OUTPUT_MODES_GUIDE.md) | Output location modes | Users |
| [docs/extractor/STRUCTURED_OUTPUT_IMPROVEMENTS.md](docs/extractor/STRUCTURED_OUTPUT_IMPROVEMENTS.md) | JSON mode details | Developers |

### Technical Details
| File | Purpose | Audience |
|------|---------|----------|
| [docs/extractor/IMPLEMENTATION_COMPLETE.md](docs/extractor/IMPLEMENTATION_COMPLETE.md) | Complete overview | Developers |
| [docs/extractor/OUTPUT_MODES_SUMMARY.md](docs/extractor/OUTPUT_MODES_SUMMARY.md) | Feature summary | Developers |
| [docs/extractor/extraction_test_summary.md](docs/extractor/extraction_test_summary.md) | Test results | Researchers |

### Repository Management
| File | Purpose | Audience |
|------|---------|----------|
| [GIT_GUIDE.md](GIT_GUIDE.md) | Git workflow | Contributors |
| [.gitignore](.gitignore) | Ignored patterns | Contributors |

## 🔄 Changes Made

### Reorganization (2026-01-26)
✅ **Created** `docs/extractor/` folder
✅ **Moved** 7 documentation files to `docs/extractor/`
✅ **Created** `docs/extractor/README.md` as documentation index
✅ **Updated** main `README.md` to include tool overview
✅ **Updated** `GIT_GUIDE.md` to reflect new structure

### Files Moved
```
EXTRACTOR_README.md              → docs/extractor/EXTRACTOR_README.md
OUTPUT_MODES_GUIDE.md            → docs/extractor/OUTPUT_MODES_GUIDE.md
OUTPUT_MODES_SUMMARY.md          → docs/extractor/OUTPUT_MODES_SUMMARY.md
STRUCTURED_OUTPUT_IMPROVEMENTS.md → docs/extractor/STRUCTURED_OUTPUT_IMPROVEMENTS.md
QUICK_REFERENCE.md               → docs/extractor/QUICK_REFERENCE.md
extraction_test_summary.md       → docs/extractor/extraction_test_summary.md
IMPLEMENTATION_COMPLETE.md       → docs/extractor/IMPLEMENTATION_COMPLETE.md
```

### Files Kept in Root
```
README.md                   # Repository overview
GIT_GUIDE.md               # Git workflow (repository-level)
extract_metrics.py         # Main script (not documentation)
test_output_modes.py       # Tests (not documentation)
requirements-extractor.txt # Dependencies (not documentation)
example_spec.md           # Test fixture (not documentation)
```

## ✨ Benefits

### 1. Clean Root Directory
- Only essential files in root
- Clear separation between code and docs
- Easy to find what you need

### 2. Organized Documentation
- All extractor docs in one place
- Logical grouping by purpose
- Documentation index for easy navigation

### 3. Scalable Structure
- Easy to add more tools/papers
- Each tool can have its own docs folder
- Clear hierarchy: `docs/<tool-name>/`

### 4. Git-Friendly
- Clean git status
- Easy to track documentation changes
- Logical commit organization

## 🚀 Future Structure

As the repository grows:

```
Metrics/
├── docs/
│   ├── extractor/          # SIB metrics extractor
│   ├── analyzer/           # Future: Code analyzer
│   ├── visualizer/         # Future: Metrics dashboard
│   └── api/                # Future: API documentation
│
├── tools/
│   ├── extractor/          # Extractor source code
│   ├── analyzer/           # Analyzer source code
│   └── ...
│
└── papers/
    ├── SIB/                # SIB paper
    ├── CodeMetrics/        # Future papers
    └── ...
```

## 📖 Quick Links

**For Users:**
- [Start Here](docs/extractor/README.md) - Documentation index
- [Setup Guide](docs/extractor/EXTRACTOR_README.md) - Installation and usage
- [Quick Reference](docs/extractor/QUICK_REFERENCE.md) - Command cheatsheet

**For Developers:**
- [Git Guide](GIT_GUIDE.md) - Repository workflow
- [Implementation](docs/extractor/IMPLEMENTATION_COMPLETE.md) - Technical details
- [Tests](test_output_modes.py) - Unit tests

**For Researchers:**
- [SIB Paper](SIB/metrics.pdf) - Theoretical framework
- [Test Results](docs/extractor/extraction_test_summary.md) - Extraction analysis
