# Batch Processing Guide - Large Specification Archives

Guide for processing large specification archives like the TASK_ARCHIVE (702 files).

## 🎯 Quick Start - Process Entire Archive

### Command for TASK_ARCHIVE

Process all 702 files with JSON outputs next to each original file:

```bash
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE \
  --output-mode alongside \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"
```

**What this does:**
- **Recursively** processes all subdirectories
- **Places JSON** next to each .md file (alongside mode)
- **Individual files** - one JSON per markdown file
- **Automatic traversal** - finds all .md files in the tree

## 📁 Output Structure

### Before
```
SPECS/SIB/INTENT/TASK_ARCHIVE/
├── 01_A2_Configure_CI_Pipeline/
│   └── A2_Configure_CI_Pipeline.md
│
├── 01_B1_Chunked_File_Reader/
│   ├── B1_Chunked_File_Reader.md
│   └── B1_2025-10-04_Summary.md
│
└── 02_B2_Box_Header_Decoder/
    ├── B2_Box_Header_Decoder.md
    ├── next_tasks.md
    └── B2_Box_Header_Decoder_Summary.md
```

### After
```
SPECS/SIB/INTENT/TASK_ARCHIVE/
├── 01_A2_Configure_CI_Pipeline/
│   ├── A2_Configure_CI_Pipeline.md
│   └── A2_Configure_CI_Pipeline_metrics.json        ← NEW
│
├── 01_B1_Chunked_File_Reader/
│   ├── B1_Chunked_File_Reader.md
│   ├── B1_Chunked_File_Reader_metrics.json          ← NEW
│   ├── B1_2025-10-04_Summary.md
│   └── B1_2025-10-04_Summary_metrics.json           ← NEW
│
└── 02_B2_Box_Header_Decoder/
    ├── B2_Box_Header_Decoder.md
    ├── B2_Box_Header_Decoder_metrics.json           ← NEW
    ├── next_tasks.md
    ├── next_tasks_metrics.json                      ← NEW
    ├── B2_Box_Header_Decoder_Summary.md
    └── B2_Box_Header_Decoder_Summary_metrics.json   ← NEW
```

## ⏱️ Expected Runtime

### Full Archive (702 files)
- **Per file:** ~30-45 seconds (with openai/gpt-oss-20b)
- **Total time:** 7-8 hours
- **Recommendation:** Run overnight or in batches

### Resource Usage
- **CPU:** Moderate (LLM inference)
- **Memory:** 4-8 GB (for LM Studio)
- **Disk:** 5-10 MB (702 JSON files)
- **Network:** Local (no internet needed)

## 📊 Running with Progress Monitoring

### Background Execution with Logging

```bash
# Run in background with log file
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE \
  --output-mode alongside \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b" \
  2>&1 | tee extraction_full.log &

# Get the process ID
echo $! > extraction.pid

# Monitor progress in real-time
tail -f extraction_full.log

# Or watch summary
watch -n 10 'tail -20 extraction_full.log'
```

### Check Progress

```bash
# Count completed extractions
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_metrics.json" | wc -l

# Total markdown files
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*.md" | wc -l

# Completion percentage
completed=$(find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_metrics.json" | wc -l)
total=$(find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*.md" | wc -l)
echo "Progress: $completed / $total files ($(( completed * 100 / total ))%)"
```

### Stop/Resume

```bash
# Stop the background process
kill $(cat extraction.pid)

# Resume (will process remaining files)
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE \
  --output-mode alongside \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"
```

**Note:** Currently, the script will re-process files that already have JSON outputs. To skip completed files, you'd need to add skip logic (see enhancement ideas below).

## 🔄 Batch Processing Strategies

### Strategy 1: Process by Number Ranges

Process in chunks of ~100 directories:

```bash
# Batch 1: 01-99
python extract_metrics.py \
  SPECS/SIB/INTENT/TASK_ARCHIVE/0* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/1* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/2* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/3* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/4* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/5* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/6* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/7* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/8* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/9* \
  --output-mode alongside \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"

# Batch 2: 100-199
python extract_metrics.py \
  SPECS/SIB/INTENT/TASK_ARCHIVE/10* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/11* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/12* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/13* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/14* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/15* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/16* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/17* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/18* \
  SPECS/SIB/INTENT/TASK_ARCHIVE/19* \
  --output-mode alongside \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"

# Batch 3: 200-239
python extract_metrics.py \
  SPECS/SIB/INTENT/TASK_ARCHIVE/2* \
  --output-mode alongside \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"
```

### Strategy 2: Process First N Directories

```bash
# Get first 50 directories
dirs=$(ls -d SPECS/SIB/INTENT/TASK_ARCHIVE/*/ | head -50)

# Process them
for dir in $dirs; do
  echo "Processing: $dir"
  python extract_metrics.py "$dir" \
    --output-mode alongside \
    --individual-files \
    --base-url http://192.168.1.82:1234 \
    --model "openai/gpt-oss-20b"
done
```

### Strategy 3: Process by Task Type

```bash
# Just A-series tasks (architecture)
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE/*_A* \
  --output-mode alongside \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"

# Just B-series tasks (build)
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE/*_B* \
  --output-mode alongside \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"

# Just C-series tasks (code)
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE/*_C* \
  --output-mode alongside \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"
```

## 🔍 Verification and Quality Checks

### Check for Missing Extractions

Find markdown files without corresponding JSON:

```bash
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*.md" -type f | while read f; do
  json="${f%.md}_metrics.json"
  if [ ! -f "$json" ]; then
    echo "Missing: $f"
  fi
done
```

### Check for Failed Extractions

JSON files with zero or minimal content:

```bash
# Find very small JSON files (likely failures)
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_metrics.json" -size -100c

# Check for files with zero intent atoms or functional units
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_metrics.json" -exec grep -l '"n_spec": 0' {} \;
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_metrics.json" -exec grep -l '"n_func": 0' {} \;
```

### Aggregate Statistics

Count total metrics across all files:

```bash
# Total intent atoms
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_metrics.json" -exec grep -h '"n_spec"' {} \; | \
  awk -F': ' '{sum+=$2} END {print "Total Intent Atoms:", sum}'

# Total functional units
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_metrics.json" -exec grep -h '"n_func"' {} \; | \
  awk -F': ' '{sum+=$2} END {print "Total Functional Units:", sum}'
```

## ⚡ Performance Optimization

### 1. Faster Model

Use a faster model for initial extraction:

```bash
# Mistral is faster than Llama 3
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE \
  --output-mode alongside \
  --individual-files \
  --base-url http://localhost:11434 \
  --model mistral
```

### 2. Disable JSON Mode (if problematic)

```bash
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE \
  --output-mode alongside \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b" \
  --no-json-mode
```

### 3. Ensure LM Studio Resources

- **Close other applications**
- **Allocate 8GB+ RAM** to LM Studio
- **Use CPU or GPU** acceleration if available
- **Monitor temperature** - throttling slows inference

## 🐛 Troubleshooting

### Problem: Connection Timeouts

**Symptom:** `Error: Connection timeout`

**Solutions:**
```bash
# Increase timeout in extract_metrics.py (line ~107)
# Change: timeout=120
# To:     timeout=300

# Or restart LM Studio
# Or check network connectivity to http://192.168.1.82:1234
```

### Problem: JSON Parsing Errors

**Symptom:** `Warning: Failed to parse LLM response as JSON`

**Solutions:**
```bash
# Try with --no-json-mode flag
# Or switch to a model with better JSON adherence (Qwen 2.5, Llama 3.1)
# Or check individual failed files and re-process
```

### Problem: Out of Memory

**Symptom:** LM Studio crashes or system freezes

**Solutions:**
- Process in smaller batches
- Use a smaller model
- Close other applications
- Increase system swap space

### Problem: Very Slow Processing

**Symptom:** More than 60 seconds per file

**Solutions:**
- Check LM Studio is using GPU if available
- Try a smaller/faster model
- Check CPU isn't thermal throttling
- Ensure LM Studio has enough RAM allocated

## 📈 Post-Processing Analysis

### Create Aggregate Summary

Combine all metrics into a single analysis file:

```bash
# Count files by task type
echo "Task Distribution:"
ls SPECS/SIB/INTENT/TASK_ARCHIVE/ | grep -oE "_[A-Z][0-9]" | sort | uniq -c

# Average metrics by task type
for type in A B C D E F G H I J T; do
  echo "Task Type: $type"
  find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_${type}*_metrics.json" -exec grep '"n_spec"' {} \; | \
    awk -F': ' '{sum+=$2; count++} END {if(count>0) print "  Avg N_spec:", sum/count}'
  find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_${type}*_metrics.json" -exec grep '"n_func"' {} \; | \
    awk -F': ' '{sum+=$2; count++} END {if(count>0) print "  Avg N_func:", sum/count}'
done
```

### Export to CSV for Analysis

Create a CSV summary of all extractions (requires jq):

```bash
# Install jq if needed: brew install jq

# Create CSV header
echo "file_path,n_spec,n_func,intent_yield,file_size,line_count" > metrics_summary.csv

# Extract data from all JSON files
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_metrics.json" -exec jq -r \
  '[.file_path, .n_spec, .n_func, (.n_func/.n_spec), .metadata.file_size_bytes, .metadata.line_count] | @csv' \
  {} \; >> metrics_summary.csv

echo "Created metrics_summary.csv"
```

## 🎯 Best Practices

### Before Starting
1. ✅ Ensure LM Studio is running and responsive
2. ✅ Test with a small batch first (e.g., one directory)
3. ✅ Check available disk space (need ~10 MB for 702 files)
4. ✅ Note the start time for progress estimation

### During Extraction
1. ✅ Monitor progress periodically (tail -f logs)
2. ✅ Check for errors in log output
3. ✅ Don't interrupt mid-file (wait for "✓ Found..." message)
4. ✅ Keep LM Studio running continuously

### After Completion
1. ✅ Verify all files were processed
2. ✅ Check for extraction failures (0 intent atoms/functional units)
3. ✅ Create aggregate statistics
4. ✅ Backup JSON outputs (if needed)

## 🚀 Example: Full Extraction Session

Complete workflow from start to finish:

```bash
# 1. Verify setup
echo "Checking LM Studio connectivity..."
curl -s http://192.168.1.82:1234/v1/models | head

# 2. Count files to process
total=$(find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*.md" | wc -l)
echo "Will process $total markdown files"

# 3. Start extraction with logging
echo "Starting extraction at $(date)"
python extract_metrics.py SPECS/SIB/INTENT/TASK_ARCHIVE \
  --output-mode alongside \
  --individual-files \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b" \
  2>&1 | tee extraction_full.log &

echo $! > extraction.pid
echo "Process ID: $(cat extraction.pid)"

# 4. Monitor in another terminal
# tail -f extraction_full.log

# 5. When complete, verify
echo "Extraction completed at $(date)"
completed=$(find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_metrics.json" | wc -l)
echo "Extracted $completed / $total files"

# 6. Check for failures
echo "Checking for missing extractions..."
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*.md" -type f | while read f; do
  json="${f%.md}_metrics.json"
  [ ! -f "$json" ] && echo "Missing: $f"
done

# 7. Generate summary statistics
echo "Total metrics extracted:"
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_metrics.json" -exec grep -h '"n_spec"' {} \; | \
  awk -F': ' '{sum+=$2} END {print "  Intent Atoms:", sum}'
find SPECS/SIB/INTENT/TASK_ARCHIVE -name "*_metrics.json" -exec grep -h '"n_func"' {} \; | \
  awk -F': ' '{sum+=$2} END {print "  Functional Units:", sum}'

echo "Done!"
```

## 💡 Enhancement Ideas

### Skip Already Processed Files

Add this check to the script (future enhancement):

```python
# Before processing, check if output exists
output_path = get_output_path(input_file, mode, ...)
if output_path.exists():
    print(f"Skipping {input_file} (already processed)")
    continue
```

### Parallel Processing

Process multiple files simultaneously (future enhancement):

```python
# Use multiprocessing or threading
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(process_file, md_files)
```

### Progress Bar

Add visual progress indicator (future enhancement):

```bash
# Install tqdm: pip install tqdm
# Then add to script:
from tqdm import tqdm
for md_file in tqdm(md_files):
    extract_metrics(md_file)
```

## 📚 Related Documentation

- [EXTRACTOR_README.md](EXTRACTOR_README.md) - Main documentation
- [OUTPUT_MODES_GUIDE.md](OUTPUT_MODES_GUIDE.md) - Output mode details
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command reference

## ❓ Questions?

For issues or questions about batch processing:
1. Check the [troubleshooting section](#-troubleshooting) above
2. See [EXTRACTOR_README.md](EXTRACTOR_README.md) for general issues
3. Open an issue on GitHub with details about your batch size and errors

---

**Happy batch processing!** 🚀 Processing 702 files takes time, but the structured metrics data is worth it!
