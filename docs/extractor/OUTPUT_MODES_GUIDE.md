# Output Location Modes Guide

The SIB metrics extractor now supports three flexible output modes to organize your results.

## Output Modes

### 1. Default Mode (default)
**Output files are placed in the current directory where you run the script.**

```bash
# Single file - outputs to current directory
python extract_metrics.py specs/auth.md
# Creates: ./sib_metrics.json

# Specify custom filename in current directory
python extract_metrics.py specs/auth.md -o my_results.json
# Creates: ./my_results.json

# Directory - aggregate output in current directory
python extract_metrics.py specs/ -o all_specs.json
# Creates: ./all_specs.json
```

**Use when:**
- Running ad-hoc analyses
- You want all results in one central location
- Processing multiple directories and want outputs in one place

---

### 2. Alongside Mode (--output-mode alongside)
**Output files are placed next to each input file.**

```bash
# Single file - output next to input
python extract_metrics.py specs/auth.md --output-mode alongside
# Creates: specs/auth_metrics.json

# Directory with individual files
python extract_metrics.py specs/ --output-mode alongside --individual-files
# Creates:
#   specs/auth_metrics.json
#   specs/user_management_metrics.json
#   specs/api_gateway_metrics.json
#   ... (one per input file)

# Directory with aggregate (uses default location)
python extract_metrics.py specs/ --output-mode alongside
# Creates: ./sib_metrics.json (aggregate of all files)
```

**Use when:**
- You want results stored with source specifications
- Working with version-controlled specs (commit metrics alongside specs)
- Each spec should have its own metrics file
- Building a distributed metrics collection

**Tip:** Use `--individual-files` with alongside mode to create one output per input.

---

### 3. Custom Directory Mode (--output-mode custom)
**Output files are placed in a specified directory.**

```bash
# Single file to custom directory
python extract_metrics.py specs/auth.md \
  --output-mode custom \
  --output-dir ./metrics_output
# Creates: ./metrics_output/auth_metrics.json

# Directory with individual files to custom location
python extract_metrics.py specs/ \
  --output-mode custom \
  --output-dir ./metrics_output \
  --individual-files
# Creates:
#   ./metrics_output/auth_metrics.json
#   ./metrics_output/user_management_metrics.json
#   ./metrics_output/api_gateway_metrics.json
#   ... (one per input file)

# Directory with aggregate to custom location
python extract_metrics.py specs/ \
  --output-mode custom \
  --output-dir ./metrics_output \
  -o aggregate.json
# Creates: ./metrics_output/aggregate.json
```

**Use when:**
- Organizing outputs separately from source files
- Building a metrics database/archive
- CI/CD pipelines with dedicated output directories
- Multi-project analysis with organized structure

**Note:** The output directory is created automatically if it doesn't exist.

---

## Individual Files Flag

The `--individual-files` flag controls whether to write separate JSON files for each input or one aggregate file.

### With Individual Files
```bash
python extract_metrics.py specs/ \
  --output-mode custom \
  --output-dir ./metrics \
  --individual-files
```

**Output structure:**
```
./metrics/
  ├── auth_metrics.json           # Metrics for auth.md
  ├── user_management_metrics.json # Metrics for user_management.md
  └── api_gateway_metrics.json    # Metrics for api_gateway.md
```

Each file contains:
```json
{
  "file_path": "specs/auth.md",
  "n_spec": 15,
  "n_func": 6,
  "intent_atoms": [...],
  "functional_units": [...],
  "metadata": {...}
}
```

### Without Individual Files (default)
```bash
python extract_metrics.py specs/ \
  --output-mode custom \
  --output-dir ./metrics \
  -o aggregate.json
```

**Output structure:**
```
./metrics/
  └── aggregate.json  # All metrics combined
```

Aggregate file contains:
```json
{
  "summary": {
    "total_files": 3,
    "total_intent_atoms": 50,
    "total_functional_units": 30,
    "intent_yield": 0.60
  },
  "files": [
    { "file_path": "specs/auth.md", "n_spec": 15, ... },
    { "file_path": "specs/user_management.md", "n_spec": 20, ... },
    { "file_path": "specs/api_gateway.md", "n_spec": 15, ... }
  ]
}
```

---

## Common Use Cases

### Use Case 1: Quick Analysis
**Goal:** Analyze a few specs and see results immediately.

```bash
python extract_metrics.py specs/auth.md specs/users.md
# Results: ./sib_metrics.json (current directory)
```

### Use Case 2: Version Control Integration
**Goal:** Commit metrics alongside specifications for tracking over time.

```bash
python extract_metrics.py specs/ \
  --output-mode alongside \
  --individual-files

git add specs/*_metrics.json
git commit -m "Update SIB metrics"
```

### Use Case 3: CI/CD Pipeline
**Goal:** Extract metrics in CI and archive as build artifacts.

```bash
# In your CI script
python extract_metrics.py ./specs \
  --output-mode custom \
  --output-dir ./build/metrics \
  -o sib_metrics_$(date +%Y%m%d).json

# Upload ./build/metrics/ as artifact
```

### Use Case 4: Multi-Project Analysis
**Goal:** Process multiple projects and organize outputs by project.

```bash
# Project A
python extract_metrics.py ~/projects/projectA/specs \
  --output-mode custom \
  --output-dir ~/metrics_archive/projectA \
  -o projectA_metrics.json

# Project B
python extract_metrics.py ~/projects/projectB/specs \
  --output-mode custom \
  --output-dir ~/metrics_archive/projectB \
  -o projectB_metrics.json

# Results organized:
# ~/metrics_archive/
#   ├── projectA/projectA_metrics.json
#   └── projectB/projectB_metrics.json
```

### Use Case 5: Large Archive Processing
**Goal:** Process your 702-file task archive with organized outputs.

```bash
# Extract to dedicated directory with individual files
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE \
  --output-mode custom \
  --output-dir ./task_metrics \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"

# Creates ./task_metrics/ with 702 JSON files
# Easy to process incrementally, resume on failure, or parallelize
```

---

## Command-Line Reference

```
--output-mode {default,alongside,custom}
    Where to place output files
    - default: Current directory (where script is run)
    - alongside: Next to each input file
    - custom: Specified custom directory

--output-dir PATH
    Custom output directory (required for --output-mode=custom)
    Created automatically if it doesn't exist

--individual-files
    Write separate JSON for each input file
    Without this flag, writes one aggregate JSON

-o, --output FILENAME
    Output filename (default: sib_metrics.json)
    Used differently depending on mode:
    - default/custom: Name of aggregate file
    - alongside: Ignored (generates names automatically)
```

---

## File Naming Convention

| Mode | Input | Output Filename |
|------|-------|----------------|
| default | `auth.md` | `sib_metrics.json` (or `-o` value) |
| alongside | `auth.md` | `auth_metrics.json` |
| custom | `auth.md` | `<output-dir>/auth_metrics.json` |
| custom + aggregate | directory | `<output-dir>/<-o value>` |

All output files use the `_metrics.json` suffix when generated from input filenames.

---

## Tips and Best Practices

1. **Use alongside mode for specs under version control** - Track metric evolution over time.

2. **Use custom mode for CI/CD** - Keep outputs separate from source code.

3. **Use individual files for large batches** - Easier to process incrementally, resume on failures.

4. **Combine with batch processing** - Process subsets and aggregate later:
   ```bash
   # Process in batches
   find specs/ -name "*.md" | head -100 | \
     xargs -I {} python extract_metrics.py {} \
       --output-mode custom --output-dir ./batch1
   ```

5. **Use descriptive output names** - Makes analysis easier:
   ```bash
   python extract_metrics.py specs/ -o specs_2026-01-26.json
   ```

---

## Error Handling

- **custom mode without --output-dir:** Error: `--output-dir is required`
- **output-dir doesn't exist:** Created automatically
- **File write permission issues:** Check directory permissions
- **Individual file name conflicts:** Overwrites existing files (backup first!)
