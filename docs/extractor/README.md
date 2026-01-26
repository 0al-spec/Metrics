# SIB Metrics Extractor - Documentation

Complete documentation for the LLM-driven SIB metrics extraction tool.

## 📚 Documentation Index

### Getting Started
1. **[EXTRACTOR_README.md](EXTRACTOR_README.md)** - **Start here!**
   - Setup and installation
   - Basic usage examples
   - Model recommendations
   - Troubleshooting

2. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command cheat sheet
   - Common commands
   - Flag reference
   - Quick patterns

### Features

3. **[OUTPUT_MODES_GUIDE.md](OUTPUT_MODES_GUIDE.md)** - Output location modes
   - Default, alongside, and custom modes
   - Detailed usage examples
   - Use cases and patterns

4. **[BATCH_PROCESSING_GUIDE.md](BATCH_PROCESSING_GUIDE.md)** - Large archive processing
   - Processing 700+ files
   - Progress monitoring
   - Batch strategies
   - Verification and quality checks

5. **[STRUCTURED_OUTPUT_IMPROVEMENTS.md](STRUCTURED_OUTPUT_IMPROVEMENTS.md)** - JSON mode
   - Structured output support
   - Automatic fallback
   - Before/after comparison

### Technical Details

5. **[OUTPUT_MODES_SUMMARY.md](OUTPUT_MODES_SUMMARY.md)** - Feature summary
   - Visual examples
   - Implementation details
   - Code changes

6. **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - Complete overview
   - All features delivered
   - Testing results
   - Production readiness

7. **[extraction_test_summary.md](extraction_test_summary.md)** - Test results
   - Sample extraction results
   - Success rates
   - Analysis

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements-extractor.txt

# 2. Start LM Studio or Ollama

# 3. Run extraction
python extract_metrics.py specs/ \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"
```

## 📊 What It Does

Extracts **Specification-Implementation Balance (SIB) metrics** from markdown specifications:

- **N_spec** - Intent Atoms (user stories, acceptance criteria, invariants, architectural decisions)
- **N_func** - Functional Units (APIs, components, workflows)
- **Intent Yield (IY)** - N_func / N_spec

## 🎯 Key Features

✅ Local LLM support (Ollama, LM Studio)
✅ Three output modes (default, alongside, custom)
✅ Structured JSON outputs with fallback
✅ Individual or aggregate results
✅ Batch processing with error recovery

## 📁 File Organization

```
Metrics/
├── extract_metrics.py              # Main script
├── test_output_modes.py            # Unit tests
├── requirements-extractor.txt      # Dependencies
├── example_spec.md                 # Test fixture
├── docs/
│   └── extractor/                  # ← You are here
│       ├── README.md               # This file
│       ├── EXTRACTOR_README.md     # Main documentation
│       ├── QUICK_REFERENCE.md      # Cheat sheet
│       ├── OUTPUT_MODES_GUIDE.md   # Output modes
│       └── ...                     # Other guides
└── GIT_GUIDE.md                    # Repository git guide
```

## 🔗 Related Documentation

- **[SIB Paper](../../SIB/README.md)** - The theoretical framework
- **[Git Guide](../../GIT_GUIDE.md)** - Repository workflow

## 💡 Need Help?

1. Check **[EXTRACTOR_README.md](EXTRACTOR_README.md)** for setup and usage
2. See **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** for command examples
3. Review **[OUTPUT_MODES_GUIDE.md](OUTPUT_MODES_GUIDE.md)** for output options

## 📈 Next Steps

After reading the documentation:

1. **Test with example**: `python extract_metrics.py example_spec.md`
2. **Process your specs**: Choose an output mode and run
3. **Analyze results**: Review extracted metrics JSON
4. **Scale up**: Process your full specification archive

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](../../CONTRIBUTING.md) for:

- How to report bugs
- How to suggest enhancements
- Development setup
- Coding standards
- Pull request process

## 📜 License

The SIB Metrics Extractor is licensed under the **MIT License**.

See [LICENSE-EXTRACTOR](../../LICENSE-EXTRACTOR) for full details.

**Note:** The SIB paper (`../../SIB/`) is licensed separately under CC BY 4.0.
