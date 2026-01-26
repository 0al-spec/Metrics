# JSON Schema Guide for LM Studio

This guide explains how to use JSON Schemas with LM Studio to enforce structured output from the SIB metrics extractor.

## 📋 What are JSON Schemas?

JSON Schemas define the exact structure that JSON output must follow. When you provide a schema to LM Studio, it will enforce that the model's output matches this structure, eliminating parsing errors.

## 📁 Schema Files

This repository includes two JSON Schema files:

1. **`schema_intent_atoms.json`** - For extracting Intent Atoms
2. **`schema_functional_units.json`** - For extracting Functional Units

## 🔧 How to Use in LM Studio

### Option 1: Manual Configuration (For Testing)

Unfortunately, LM Studio's JSON Schema feature is currently only available through the API, not through the GUI. However, you can test it manually:

1. Open LM Studio
2. Go to the "Developer" or "API" section
3. Look for "JSON Schema" or "Structured Output" settings
4. Copy and paste the contents of either schema file

### Option 2: Automatic via Script (Recommended)

The extractor script can be updated to automatically send the JSON Schema with each request. This is the recommended approach for production use.

## 📊 Schema Details

### Intent Atoms Schema

**File:** `schema_intent_atoms.json`

Enforces this structure:
```json
{
  "intent_atoms": [
    {
      "type": "user_story",
      "description": "A user-facing feature or capability"
    },
    {
      "type": "acceptance_criteria",
      "description": "Specific conditions that must be met"
    }
  ]
}
```

**Constraints:**
- `type` must be one of: `user_story`, `acceptance_criteria`, `invariant`, `architectural_decision`
- Both `type` and `description` are required
- No additional properties allowed

### Functional Units Schema

**File:** `schema_functional_units.json`

Enforces this structure:
```json
{
  "functional_units": [
    {
      "name": "API Endpoint Name",
      "description": "What this functional unit does"
    }
  ]
}
```

**Constraints:**
- Both `name` and `description` are required
- No additional properties allowed

## 🚀 Benefits of Using JSON Schema

1. **100% Parse Success Rate**: Eliminates JSON parsing errors
2. **Type Safety**: Ensures correct field types (string, array, etc.)
3. **Validation**: Catches missing required fields
4. **Enum Enforcement**: For intent atom types, only valid values are allowed
5. **No Extra Text**: Model cannot add explanatory text outside the JSON

## ⚠️ Current Limitation

The current `extract_metrics.py` script uses OpenAI's `response_format: {"type": "json_object"}` parameter, which requests JSON mode but doesn't send the schema.

To use JSON Schema with LM Studio, the script needs to be updated to include the `response_format` with a `schema` property (if supported by your LM Studio version).

## 🔄 Script Update Required

To fully leverage JSON Schemas, the `LocalLLMClient` class in `extract_metrics.py` would need to:

1. Load the appropriate schema file
2. Include it in the API request as:
   ```json
   {
     "response_format": {
       "type": "json_schema",
       "schema": <schema_content>
     }
   }
   ```

This update would ensure that LM Studio enforces the exact output format on every request.

## 📖 References

- [JSON Schema Documentation](https://json-schema.org/)
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [LM Studio API Documentation](https://lmstudio.ai/docs)

## 💡 Next Steps

1. Test the schemas manually in LM Studio
2. If JSON Schema enforcement works, update the script to automatically include schemas
3. Run test extractions to verify 100% structured output compliance
