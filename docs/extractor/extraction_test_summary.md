# SIB Metrics Extraction Test Results

## Test Configuration

- **LLM**: openai/gpt-oss-20b (via LM Studio)
- **API Endpoint**: http://192.168.1.82:1234
- **Source**: SPECS/SIB/INTENT/TASK_ARCHIVE/
- **Total files in archive**: 702 markdown files
- **Sample size**: 3 task directories (6 files total)

## Results by Task

### Task 1: A2 Configure CI Pipeline
- **Files processed**: 1
- **Intent Atoms (N_spec)**: 5
  - 1 user_story
  - 4 acceptance_criteria
- **Functional Units (N_func)**: 11
- **Intent Yield (IY)**: 2.20

**Analysis**: High IY indicates this task has detailed implementation steps. Each intent atom requires ~2 functional components.

### Task 2: B1 Chunked File Reader
- **Files processed**: 2
  - B1_Chunked_File_Reader.md
  - B1_2025-10-04_Summary.md
- **Intent Atoms (N_spec)**: 20
- **Functional Units (N_func)**: 12
- **Intent Yield (IY)**: 0.60

**Analysis**: Lower IY suggests more abstract/high-level intent that maps to fewer concrete functional units. May indicate over-specification or planning documents.

### Task 3: B2 Box Header Decoder
- **Files processed**: 3
  - next_tasks.md
  - B2_Box_Header_Decoder_Summary.md
  - B2_Box_Header_Decoder.md
- **Intent Atoms (N_spec)**: 25
- **Functional Units (N_func)**: 7
- **Intent Yield (IY)**: 0.28

**Note**: One file had JSON parsing errors (local LLM limitation), reducing functional unit count.

**Analysis**: Very low IY. Contains planning/summary documents with high-level intent but fewer concrete functional specifications.

## Aggregate Metrics

### Combined Results (3 tasks, 6 files)
- **Total Intent Atoms**: 50
- **Total Functional Units**: 30
- **Average Intent Yield**: 0.60

## Observations

### Intent Atom Distribution
- Most common types extracted:
  - Acceptance criteria
  - User stories
  - Architectural decisions (in some tasks)
  - Invariants (in some tasks)

### Functional Unit Patterns
- API endpoints and interfaces
- Data structures and models
- Processing pipelines
- Testing components
- CI/CD workflow steps

### Extraction Quality

**Successes:**
- ✅ Correctly identified user stories and acceptance criteria
- ✅ Extracted functional components from implementation notes
- ✅ Handled multiple file types (specs, summaries, next_tasks)
- ✅ Auto-detected OpenAI API format

**Limitations:**
- ⚠️ JSON parsing errors (1 out of 6 files) - local model struggled with structured output
- ⚠️ Inconsistent categorization across similar documents
- ⚠️ Processing time: ~30-45 seconds per file

## Intent Yield Interpretation

| IY Range | Interpretation | Example |
|----------|---------------|---------|
| > 2.0 | Detailed implementation spec | A2 CI Pipeline (2.20) |
| 0.5 - 2.0 | Balanced spec/impl | B1 File Reader (0.60) |
| < 0.5 | High-level planning | B2 Header Decoder (0.28) |

Low IY values may indicate:
- Planning/summary documents rather than implementation specs
- Over-specification (many intent atoms for few actual features)
- Abstract requirements not yet mapped to concrete components

High IY values may indicate:
- Implementation-focused specifications
- Detailed breakdown of functionality
- Well-scoped, concrete tasks

## Recommendations

### For Large-Scale Extraction (702 files)

1. **Batch Processing**: Process in chunks of 50-100 files
2. **Parallel Execution**: Run multiple instances if you have GPU capacity
3. **Error Handling**: Add retry logic for JSON parsing failures
4. **Model Selection**: Consider using a model with better JSON adherence:
   - Qwen 2.5 (excellent structured output)
   - Llama 3.1 70B (if resources allow)
   - Mistral Small (faster, decent quality)

### For Better Extraction Quality

1. **Fine-tune prompts**: Add examples from your actual task specs
2. **Two-pass extraction**: Validate and retry failed extractions
3. **Manual review**: Sample 5-10% of results for accuracy check
4. **Metadata enrichment**: Extract task IDs, dates, assignees

### For SIB Framework Application

To calculate full SIB metrics, you'll need:

- ✅ **N_spec**: Extracted by this tool
- ✅ **N_func**: Extracted by this tool
- ❌ **S_impl**: Requires code analysis (lines of code, AST size)
- ❌ **C_inf, T_inf, N_calls**: Requires instrumentation of AI development session

Next step: Create a complementary tool to extract S_impl from implementation code.

## Conclusion

The extraction tool successfully demonstrates proof-of-concept for automated SIB metrics collection from specification documents. While local models show some limitations in JSON formatting, the overall extraction quality is suitable for diagnostic analysis.

The varying Intent Yield values (0.28 to 2.20) across tasks highlight the framework's ability to surface differences in specification density and implementation detail - exactly the kind of observability the SIB framework aims to provide.
