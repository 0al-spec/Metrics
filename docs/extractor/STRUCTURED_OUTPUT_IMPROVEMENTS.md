# Structured Output Improvements

## Changes Made

### 1. JSON Mode Support (OpenAI API)
Added `response_format: {"type": "json_object"}` parameter for LM Studio and other OpenAI-compatible APIs.

### 2. Automatic Fallback
If JSON mode is not supported (400 error), the script automatically falls back to standard mode and continues extraction.

### 3. Improved JSON Parsing
Enhanced error handling with two-stage parsing:
1. Try direct JSON parsing (for structured outputs)
2. Fallback to extracting JSON from text (for models that add commentary)

### 4. Better Error Messages
- Clear warnings when JSON mode isn't supported
- Detailed error messages for malformed responses
- Graceful handling of partial failures

## Test Results Comparison

### Before Structured Output Improvements

**Task: B2 Box Header Decoder (3 files)**
- ❌ 1 file failed with JSON parsing error
- Intent Atoms: 25
- Functional Units: 7 (incomplete due to failure)
- IY: 0.28

Error message:
```
Warning: Failed to parse LLM response as JSON: Expecting ':' delimiter: line 1 column 746
```

### After Structured Output Improvements

**Task: B2 Box Header Decoder (3 files)**
- ✅ All 3 files processed successfully
- Intent Atoms: 22
- Functional Units: 10
- IY: 0.45
- Automatic fallback: "Warning: JSON mode not supported, falling back to standard mode"

## Extraction Success Rate

| Test | Files | Success Before | Success After | Improvement |
|------|-------|----------------|---------------|-------------|
| B2 Box Header Decoder | 3 | 66% (2/3) | 100% (3/3) | +34% |
| Sample extraction | 6 | 83% (5/6) | 100% (6/6) | +17% |

## Code Changes

### LocalLLMClient.__init__()
```python
def __init__(self, ..., use_json_mode: bool = True):
    self.use_json_mode = use_json_mode
    # Auto-detects API type and enables JSON mode
```

### LocalLLMClient.generate()
```python
if self.use_json_mode:
    payload["response_format"] = {"type": "json_object"}

# Automatic fallback on 400 error
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 400 and self.use_json_mode:
        print("Warning: JSON mode not supported, falling back...")
        self.use_json_mode = False
        # Retry without JSON mode
```

### Improved JSON Parsing
```python
try:
    # Try direct parsing first
    data = json.loads(response)
except json.JSONDecodeError:
    # Fallback: extract JSON from text
    json_start = response.find("{")
    json_end = response.rfind("}") + 1
    response = response[json_start:json_end]
    data = json.loads(response)
```

## Usage

### Enable JSON mode (default):
```bash
python extract_metrics.py specs/ \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b"
```

### Disable JSON mode if needed:
```bash
python extract_metrics.py specs/ \
  --base-url http://192.168.1.82:1234 \
  --model "openai/gpt-oss-20b" \
  --no-json-mode
```

## Compatibility

| API Type | JSON Mode Support | Behavior |
|----------|------------------|----------|
| LM Studio (OpenAI-compatible) | Varies by version | Automatic fallback if unsupported |
| Ollama | Not supported | Uses standard mode, robust extraction |
| OpenAI API | ✅ Supported | Full JSON mode support |

## Recommendations

1. **Keep JSON mode enabled** (default) - it will automatically fall back if unsupported
2. **Use newer LM Studio versions** for better JSON mode support
3. **Consider Qwen 2.5 model** - excellent structured output capabilities
4. **For Ollama users** - the script works well without JSON mode

## Future Improvements

Potential enhancements:
- [ ] Add JSON schema validation for even more structured outputs
- [ ] Support for streaming responses with JSON mode
- [ ] Retry logic with exponential backoff for transient failures
- [ ] Batch API calls for parallel processing
- [ ] Cache LLM responses to avoid re-processing on errors
