# SIB Metrics Extractor

Automatically extract Specification-Implementation Balance (SIB) metrics from markdown specification documents using local LLMs.

## Features

- **Local LLM support**: Uses Ollama or LM Studio (no API costs)
- **Intent Atom extraction**: Identifies user stories, acceptance criteria, invariants, and architectural decisions
- **Functional Unit extraction**: Identifies observable functional outputs
- **Batch processing**: Process entire directories of specifications
- **JSON output**: Structured data ready for analysis

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements-extractor.txt
```

### 2. Install and Run a Local LLM

**Option A: Ollama (Recommended)**

```bash
# Install Ollama from https://ollama.ai

# Pull a model (llama3 recommended for structured output)
ollama pull llama3

# Ollama runs automatically on http://localhost:11434
```

**Option B: LM Studio**

1. Download from https://lmstudio.ai
2. Load a model (recommend: Llama 3 or Mistral)
3. Start the local server (default: http://localhost:1234)

## Usage

### Process a Single File

```bash
# Output to current directory (default)
python extract_metrics.py path/to/spec.md

# Output next to the input file
python extract_metrics.py path/to/spec.md --output-mode alongside

# Output to custom directory
python extract_metrics.py path/to/spec.md --output-mode custom --output-dir ./metrics
```

### Process a Directory

```bash
# Aggregate output in current directory
python extract_metrics.py specs/ -o results.json

# Individual files next to each input
python extract_metrics.py specs/ --output-mode alongside --individual-files

# Individual files in custom directory
python extract_metrics.py specs/ --output-mode custom --output-dir ./metrics --individual-files
```

### Use a Different Model

```bash
# With Ollama
python extract_metrics.py specs/ --model mistral

# With LM Studio (different port)
python extract_metrics.py specs/ --base-url http://localhost:1234 --model your-model-name
```

### Output Location Modes

The script supports three output modes:

1. **default** - Output to current directory
2. **alongside** - Output next to each input file
3. **custom** - Output to specified directory

See [OUTPUT_MODES_GUIDE.md](OUTPUT_MODES_GUIDE.md) for detailed examples and use cases.

## Command-Line Options

```
usage: extract_metrics.py [-h] [-o OUTPUT] [--model MODEL] [--base-url BASE_URL]
                          [--api-type {auto,ollama,openai}] [--json-mode] [--no-json-mode]
                          [--output-mode {default,alongside,custom}] [--output-dir DIR]
                          [--individual-files]
                          input

positional arguments:
  input                 Input markdown file or directory

options:
  -h, --help            Show help message
  -o, --output OUTPUT   Output JSON file (default: sib_metrics.json)
  --model MODEL         Local model name (default: llama3)
  --base-url BASE_URL   LLM API base URL (default: http://localhost:11434)
  --api-type TYPE       API type: auto (detect), ollama, or openai (default: auto)
  --json-mode           Enable JSON mode for structured outputs (default: True)
  --no-json-mode        Disable JSON mode (use if your LLM doesn't support it)
  --output-mode MODE    Where to place outputs: default (current dir),
                        alongside (next to input), custom (specify dir)
  --output-dir DIR      Custom output directory (required for --output-mode=custom)
  --individual-files    Write separate JSON for each input file
```

## Output Format

The script generates a JSON file with the following structure:

```json
{
  "summary": {
    "total_files": 3,
    "total_intent_atoms": 42,
    "total_functional_units": 18,
    "intent_yield": 0.43
  },
  "files": [
    {
      "file_path": "specs/auth.md",
      "n_spec": 15,
      "n_func": 6,
      "intent_atoms": [
        {
          "type": "user_story",
          "description": "As a user, I can log in with email and password",
          "source_line": null
        },
        {
          "type": "acceptance_criteria",
          "description": "Password must be at least 8 characters",
          "source_line": null
        }
      ],
      "functional_units": [
        {
          "name": "Login endpoint",
          "description": "POST /api/auth/login - authenticate user",
          "source_line": null
        }
      ],
      "metadata": {
        "file_size_bytes": 2048,
        "line_count": 85
      }
    }
  ]
}
```

## Extracted Metrics

### Intent Atoms (N_spec)

Four types of intent atoms are extracted:

1. **user_story**: User-facing features or capabilities
2. **acceptance_criteria**: Specific conditions that must be met
3. **invariant**: System constraints or rules that must always hold
4. **architectural_decision**: Structural or design choices

### Functional Units (N_func)

Observable, externally-visible capabilities:
- API endpoints
- UI components
- Data processing pipelines
- User workflows

### Derived Metrics

The output includes **Intent Yield (IY)**:

```
IY = N_func / N_spec
```

This measures how much observable functionality is produced per unit of intent.

## Structured Outputs (JSON Mode)

The script supports structured JSON outputs for improved extraction reliability:

**OpenAI-compatible APIs (LM Studio):**
- Automatically uses `response_format: {"type": "json_object"}`
- Significantly reduces JSON parsing errors
- Automatically falls back to standard mode if not supported

**Ollama:**
- JSON mode not currently supported by Ollama API
- Uses robust JSON extraction from text responses

**Benefits:**
- ✅ Higher extraction success rate (fewer parsing errors)
- ✅ Cleaner JSON output from models
- ✅ Automatic fallback if unsupported

**Disable if needed:**
```bash
python extract_metrics.py specs/ --no-json-mode
```

## Model Recommendations

For best extraction quality:

- **Llama 3 (8B or 70B)**: Best balance of speed and accuracy
- **Mistral (7B)**: Faster, good for large document sets
- **Qwen 2.5**: Excellent structured output capabilities (highly recommended)
- **Phi-3**: Lightweight option for resource-constrained systems

**Note:** Models with better instruction-following produce cleaner JSON output.

## Limitations

- **Accuracy depends on model quality**: Smaller models may miss nuanced intent atoms
- **Markdown-only**: Currently only processes `.md` files
- **No implementation analysis**: This tool only processes specifications, not code
- **Subjective extraction**: Different models may categorize atoms differently

## Integration with SIB Framework

This tool extracts **N_spec** and **N_func** from specification documents. To calculate full SIB metrics, you also need:

- **S_impl**: Implementation size (lines of code, tokens, AST units)
- **C_inf, T_inf, N_calls**: AI inference footprint (if using AI-assisted development)

See the main SIB paper (`SIB/metrics.pdf`) for the complete framework.

## Troubleshooting

**"Error calling LLM API: Connection refused"**
- Ensure Ollama/LM Studio is running
- Check the base URL matches your LLM server

**"Warning: Failed to parse LLM response as JSON"**
- Try a different model (some models are better at structured output)
- Reduce document size (split large specifications)
- Lower temperature for more deterministic output (edit script)

**"No markdown files found"**
- Verify the input directory path
- Ensure files have `.md` extension

## Contributing

We welcome contributions! See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines on:

- Reporting bugs
- Suggesting enhancements
- Submitting pull requests
- Coding standards

## License

The SIB Metrics Extractor is licensed under the **MIT License**.

See [LICENSE-EXTRACTOR](../../LICENSE-EXTRACTOR) for full details.

**Note:** The SIB paper is licensed separately under CC BY 4.0.
