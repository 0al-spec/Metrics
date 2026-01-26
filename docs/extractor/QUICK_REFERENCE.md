# SIB Metrics Extractor - Quick Reference

**New:** JSON Schema support for 100% structured output with LM Studio. See [JSON_SCHEMA_GUIDE.md](JSON_SCHEMA_GUIDE.md).

## Basic Usage

```bash
# Process single file (default: current directory)
python extract_metrics.py specs/auth.md

# Process directory (aggregate output)
python extract_metrics.py specs/ -o results.json

# Use LM Studio
python extract_metrics.py specs/ \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"
```

## Output Modes

### 1. Default (Current Directory)
```bash
python extract_metrics.py specs/
# Output: ./sib_metrics.json
```

### 2. Alongside (Next to Input)
```bash
python extract_metrics.py specs/ --output-mode alongside --individual-files
# Output: specs/*_metrics.json (one per file)
```

### 3. Custom Directory
```bash
python extract_metrics.py specs/ \
  --output-mode custom \
  --output-dir ./metrics \
  --individual-files
# Output: ./metrics/*_metrics.json
```

## Common Patterns

### Quick Analysis
```bash
python extract_metrics.py specs/auth.md
```

### Version Control Integration
```bash
python extract_metrics.py specs/ \
  --output-mode alongside \
  --individual-files

git add specs/*_metrics.json
```

### CI/CD Pipeline
```bash
python extract_metrics.py specs/ \
  --output-mode custom \
  --output-dir ./build/metrics
```

### Large Archive (Your 702 Files)
```bash
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE \
  --output-mode custom \
  --output-dir ./task_metrics \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"
```

## Flags

| Flag | Description |
|------|-------------|
| `-o FILE` | Output filename |
| `--output-mode MODE` | `default`, `alongside`, or `custom` |
| `--output-dir DIR` | Custom output directory |
| `--individual-files` | One JSON per input file |
| `--model NAME` | LLM model name |
| `--base-url URL` | LLM API endpoint |
| `--no-json-mode` | Disable JSON mode |

## File Naming

| Mode | Input | Output |
|------|-------|--------|
| default | `auth.md` | `./sib_metrics.json` |
| alongside | `auth.md` | `auth_metrics.json` |
| custom | `auth.md` | `<dir>/auth_metrics.json` |

## Help

```bash
python extract_metrics.py --help
```

## Documentation

- `JSON_SCHEMA_GUIDE.md` - JSON Schema enforcement (NEW)
- `OUTPUT_MODES_GUIDE.md` - Detailed guide with examples
- `EXTRACTOR_README.md` - Complete documentation
- `BATCH_PROCESSING_GUIDE.md` - Large archive processing
- `STRUCTURED_OUTPUT_IMPROVEMENTS.md` - JSON mode details
