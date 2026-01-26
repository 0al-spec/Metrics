# Output Modes Feature Summary

## New Capabilities Added

✅ **Three flexible output location modes**
✅ **Individual file outputs for batch processing**
✅ **Automatic directory creation**
✅ **Smart file naming conventions**

---

## Quick Comparison

| Mode | Where Files Go | Best For |
|------|---------------|----------|
| **default** | Current directory | Quick analysis, centralized results |
| **alongside** | Next to input files | Version control, distributed metrics |
| **custom** | Specified directory | CI/CD, organized archives |

---

## Visual Examples

### Mode 1: Default (Current Directory)
```
Project Structure:
  specs/
    ├── auth.md
    ├── users.md
    └── api.md
  extract_metrics.py

Command:
  $ python extract_metrics.py specs/

Output:
  specs/
    ├── auth.md
    ├── users.md
    └── api.md
  extract_metrics.py
  sib_metrics.json          ← All results here
```

### Mode 2: Alongside (Next to Input)
```
Project Structure:
  specs/
    ├── auth.md
    ├── users.md
    └── api.md

Command:
  $ python extract_metrics.py specs/ \
      --output-mode alongside \
      --individual-files

Output:
  specs/
    ├── auth.md
    ├── auth_metrics.json        ← Results for auth.md
    ├── users.md
    ├── users_metrics.json       ← Results for users.md
    ├── api.md
    └── api_metrics.json         ← Results for api.md
```

### Mode 3: Custom Directory
```
Project Structure:
  specs/
    ├── auth.md
    ├── users.md
    └── api.md

Command:
  $ python extract_metrics.py specs/ \
      --output-mode custom \
      --output-dir ./metrics_output \
      --individual-files

Output:
  specs/
    ├── auth.md
    ├── users.md
    └── api.md
  metrics_output/
    ├── auth_metrics.json        ← Results organized here
    ├── users_metrics.json
    └── api_metrics.json
```

---

## Code Changes Summary

### New Functions
- `get_output_path()` - Determines output location based on mode
- Enhanced `process_directory()` - Supports new output modes
- Updated `main()` - New CLI arguments

### New CLI Arguments
```python
--output-mode {default,alongside,custom}  # Where to place outputs
--output-dir PATH                          # Custom directory path
--individual-files                         # One JSON per input
```

### File Naming Logic
```python
# Alongside mode
"auth.md" → "auth_metrics.json"

# Custom mode
"auth.md" → "<output-dir>/auth_metrics.json"

# Default mode
"auth.md" → "sib_metrics.json" (or -o value)
```

---

## Use Case Examples

### 1. Quick Analysis (Default Mode)
```bash
python extract_metrics.py specs/
# Result: ./sib_metrics.json
```
**Use when:** Running ad-hoc analysis, want centralized output

### 2. Version Control (Alongside Mode)
```bash
python extract_metrics.py specs/ \
  --output-mode alongside \
  --individual-files

git add specs/*_metrics.json
git commit -m "Update metrics"
```
**Use when:** Tracking metrics evolution with specs over time

### 3. CI/CD Pipeline (Custom Mode)
```bash
python extract_metrics.py specs/ \
  --output-mode custom \
  --output-dir ./build/metrics \
  -o metrics_$(date +%Y%m%d).json
```
**Use when:** Build artifacts, organized archives

### 4. Large Batch Processing (Custom + Individual)
```bash
# Process your 702-file archive
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE \
  --output-mode custom \
  --output-dir ./task_metrics \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"
```
**Use when:** Large archives, want individual tracking

---

## Benefits

### 1. Flexibility
- Choose where outputs go based on your workflow
- No more moving files around manually

### 2. Organization
- Keep source and metrics separate (custom mode)
- Or keep them together (alongside mode)

### 3. Batch Processing
- Individual files enable incremental processing
- Easy to resume on failures
- Parallel processing possible

### 4. CI/CD Friendly
- Dedicated output directories
- Timestamped filenames
- Artifact-ready structure

### 5. Version Control
- Track metrics with specs
- Commit history shows metric evolution

---

## Implementation Details

### Error Handling
```python
# Validates required arguments
if args.output_mode == "custom" and not args.output_dir:
    parser.error("--output-dir is required when using --output-mode=custom")

# Creates directories automatically
output_dir.mkdir(parents=True, exist_ok=True)
```

### Smart Output Path Resolution
```python
def get_output_path(input_path, mode, output_file, output_dir):
    if mode == "alongside":
        return input_path.parent / f"{input_path.stem}_metrics.json"
    elif mode == "custom":
        return output_dir / f"{input_path.stem}_metrics.json"
    else:  # default
        return output_file
```

### Individual vs Aggregate
```python
# Individual files: One JSON per input
for md_file in md_files:
    metrics = extract(md_file)
    output = get_output_path(md_file, mode, ...)
    write_json(output, metrics)

# Aggregate: One JSON for all inputs
all_metrics = [extract(f) for f in md_files]
write_json(output, {"summary": ..., "files": all_metrics})
```

---

## Testing Checklist

- [x] Default mode with single file
- [x] Default mode with directory
- [x] Alongside mode with single file
- [ ] Alongside mode with directory + individual files (needs LM Studio)
- [ ] Custom mode with single file (needs LM Studio)
- [ ] Custom mode with directory (needs LM Studio)
- [ ] Custom mode with directory + individual files (needs LM Studio)
- [x] Error handling for missing --output-dir
- [x] Automatic directory creation
- [x] File naming conventions

---

## Next Steps

Once LM Studio is back online, test:
1. Alongside mode with multiple files
2. Custom directory mode
3. Individual files flag with large batch
4. Process sample of 702-file archive

## Documentation Files

- `OUTPUT_MODES_GUIDE.md` - Comprehensive guide with examples
- `EXTRACTOR_README.md` - Updated with new options
- `extract_metrics.py` - Implementation complete
