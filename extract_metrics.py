#!/usr/bin/env python3
"""
SIB Metrics Extractor
Extract Specification-Implementation Balance metrics from markdown specification documents.
Uses local LLMs via Ollama/LM Studio API.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import sys

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


@dataclass
class IntentAtom:
    """Represents a single intent atom (user story, acceptance criterion, etc.)"""
    type: str  # "user_story", "acceptance_criteria", "invariant", "architectural_decision"
    description: str
    source_line: Optional[int] = None


@dataclass
class FunctionalUnit:
    """Represents an observable functional output"""
    name: str
    description: str
    source_line: Optional[int] = None


@dataclass
class SpecificationMetrics:
    """Extracted metrics from a specification document"""
    file_path: str
    intent_atoms: List[IntentAtom]
    functional_units: List[FunctionalUnit]
    n_spec: int  # Count of intent atoms
    n_func: int  # Count of functional units
    metadata: Dict[str, Any]


class LocalLLMClient:
    """Client for local LLM inference (Ollama/LM Studio)"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3", api_type: str = "auto", use_json_mode: bool = True):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.use_json_mode = use_json_mode
        self.schemas = self._load_schemas()

        # Auto-detect API type
        if api_type == "auto":
            self.api_type = self._detect_api_type()
        else:
            self.api_type = api_type

        json_status = " with JSON Schema" if use_json_mode and self.api_type == "openai" and self.schemas else " with JSON mode"
        print(f"Using {self.api_type} API format{json_status}")

    def _load_schemas(self) -> Dict[str, Any]:
        """Load JSON schemas for structured output"""
        schemas = {}
        script_dir = Path(__file__).parent

        # Load intent atoms schema
        intent_schema_path = script_dir / "schema_intent_atoms.json"
        if intent_schema_path.exists():
            with open(intent_schema_path) as f:
                schemas["intent_atoms"] = json.load(f)

        # Load functional units schema
        func_schema_path = script_dir / "schema_functional_units.json"
        if func_schema_path.exists():
            with open(func_schema_path) as f:
                schemas["functional_units"] = json.load(f)

        return schemas

    def _detect_api_type(self) -> str:
        """Detect whether this is Ollama or OpenAI-compatible API"""
        try:
            # Try OpenAI format first (LM Studio)
            response = requests.get(f"{self.base_url}/v1/models", timeout=5)
            if response.status_code == 200:
                return "openai"
        except:
            pass

        try:
            # Try Ollama format
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                return "ollama"
        except:
            pass

        # Default to ollama
        print("Warning: Could not detect API type, defaulting to Ollama format")
        return "ollama"

    def generate(self, prompt: str, temperature: float = 0.1, schema_name: Optional[str] = None) -> str:
        """Generate response from local LLM

        Args:
            prompt: The prompt to send to the LLM
            temperature: Sampling temperature
            schema_name: Optional schema name ("intent_atoms" or "functional_units") for structured output
        """

        if self.api_type == "openai":
            # OpenAI-compatible API (LM Studio)
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": 2000
            }

            # Enable JSON Schema mode for structured outputs (LM Studio format)
            if self.use_json_mode and schema_name and schema_name in self.schemas:
                payload["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": f"{schema_name}_response",
                        "strict": True,
                        "schema": self.schemas[schema_name]
                    }
                }
            elif self.use_json_mode:
                # Fallback to basic JSON mode if schema not available
                payload["response_format"] = {"type": "json_object"}

            endpoint = f"{self.base_url}/v1/chat/completions"

            try:
                response = requests.post(endpoint, json=payload, timeout=120)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except requests.exceptions.HTTPError as e:
                # If JSON mode fails with 400, retry without it
                if e.response.status_code == 400 and self.use_json_mode:
                    print(f"Warning: JSON Schema mode not supported, falling back to standard mode")
                    self.use_json_mode = False
                    payload.pop("response_format", None)
                    response = requests.post(endpoint, json=payload, timeout=120)
                    response.raise_for_status()
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    print(f"Error calling LLM API: {e}")
                    raise
            except requests.exceptions.RequestException as e:
                print(f"Error calling LLM API: {e}")
                raise

        else:
            # Ollama API
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            }
            endpoint = f"{self.base_url}/api/generate"

            try:
                response = requests.post(endpoint, json=payload, timeout=120)
                response.raise_for_status()
                return response.json()["response"]
            except requests.exceptions.RequestException as e:
                print(f"Error calling LLM API: {e}")
                raise


class SpecificationExtractor:
    """Extract SIB metrics from specification documents using LLM"""

    def __init__(self, llm_client: LocalLLMClient):
        self.llm = llm_client

    def extract_intent_atoms(self, content: str) -> List[IntentAtom]:
        """Extract intent atoms from specification content"""

        prompt = f"""You are analyzing a software specification document to extract Intent Atoms.

Intent Atoms are discrete units of semantic intent, categorized as:
1. user_story: A user-facing feature or capability
2. acceptance_criteria: Specific conditions that must be met
3. invariant: System constraints or rules that must always hold
4. architectural_decision: Structural or design choices

Analyze the following specification and extract all Intent Atoms.

SPECIFICATION:
{content}

OUTPUT FORMAT (JSON):
{{
  "intent_atoms": [
    {{"type": "user_story", "description": "..."}},
    {{"type": "acceptance_criteria", "description": "..."}},
    ...
  ]
}}

Respond ONLY with valid JSON, no additional text.
"""

        response = self.llm.generate(prompt, schema_name="intent_atoms")

        # Parse JSON response
        try:
            # Try parsing directly first (for JSON mode)
            data = json.loads(response)
        except json.JSONDecodeError:
            # Fallback: Extract JSON from response (in case there's extra text)
            try:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    response = response[json_start:json_end]
                    data = json.loads(response)
                else:
                    raise ValueError("No JSON object found in response")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Warning: Failed to parse LLM response as JSON: {e}")
                print(f"Response was: {response[:200]}...")
                return []

        # Extract intent atoms from parsed data
        atoms = []
        for atom in data.get("intent_atoms", []):
            try:
                atoms.append(IntentAtom(
                    type=atom["type"],
                    description=atom["description"]
                ))
            except KeyError as e:
                print(f"Warning: Skipping malformed intent atom (missing {e})")
                continue

        return atoms

    def extract_functional_units(self, content: str) -> List[FunctionalUnit]:
        """Extract functional units from specification content"""

        prompt = f"""You are analyzing a software specification document to extract Functional Units.

Functional Units are observable, externally-visible capabilities or features that the system provides.
Examples: API endpoints, UI components, data processing pipelines, user workflows.

Analyze the following specification and extract all Functional Units.

SPECIFICATION:
{content}

OUTPUT FORMAT (JSON):
{{
  "functional_units": [
    {{"name": "Brief name", "description": "What it does"}},
    ...
  ]
}}

Respond ONLY with valid JSON, no additional text.
"""

        response = self.llm.generate(prompt, schema_name="functional_units")

        # Parse JSON response
        try:
            # Try parsing directly first (for JSON mode)
            data = json.loads(response)
        except json.JSONDecodeError:
            # Fallback: Extract JSON from response (in case there's extra text)
            try:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    response = response[json_start:json_end]
                    data = json.loads(response)
                else:
                    raise ValueError("No JSON object found in response")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Warning: Failed to parse LLM response as JSON: {e}")
                print(f"Response was: {response[:200]}...")
                return []

        # Extract functional units from parsed data
        units = []
        for unit in data.get("functional_units", []):
            try:
                units.append(FunctionalUnit(
                    name=unit["name"],
                    description=unit["description"]
                ))
            except KeyError as e:
                print(f"Warning: Skipping malformed functional unit (missing {e})")
                continue

        return units

    def extract_from_file(self, file_path: Path) -> SpecificationMetrics:
        """Extract metrics from a single specification file"""

        print(f"Processing: {file_path}")

        # Read file
        content = file_path.read_text(encoding="utf-8")

        # Extract components
        print("  - Extracting intent atoms...")
        intent_atoms = self.extract_intent_atoms(content)

        print("  - Extracting functional units...")
        functional_units = self.extract_functional_units(content)

        # Calculate metrics
        metrics = SpecificationMetrics(
            file_path=str(file_path),
            intent_atoms=intent_atoms,
            functional_units=functional_units,
            n_spec=len(intent_atoms),
            n_func=len(functional_units),
            metadata={
                "file_size_bytes": file_path.stat().st_size,
                "line_count": len(content.splitlines())
            }
        )

        print(f"  ✓ Found {metrics.n_spec} intent atoms, {metrics.n_func} functional units")

        return metrics


def get_output_path(input_path: Path, output_mode: str, output_file: Path,
                    output_dir: Optional[Path] = None) -> Path:
    """Determine output path based on mode

    Args:
        input_path: Input file path
        output_mode: "default", "alongside", or "custom"
        output_file: Default output filename
        output_dir: Custom output directory (for "custom" mode)

    Returns:
        Path where output should be written
    """
    if output_mode == "alongside":
        # Place output next to input file with .json extension
        return input_path.parent / f"{input_path.stem}_metrics.json"
    elif output_mode == "custom":
        # Place output in custom directory, preserving filename
        if output_dir is None:
            raise ValueError("output_dir must be specified for custom mode")
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / f"{input_path.stem}_metrics.json"
    else:  # "default"
        # Use the specified output file
        return output_file


def process_directory(directory: Path, output_file: Path, llm_client: LocalLLMClient,
                      output_mode: str = "default", output_dir: Optional[Path] = None,
                      individual_files: bool = False):
    """Process all markdown files in a directory

    Args:
        directory: Input directory to process
        output_file: Output filename (used for default mode)
        llm_client: LLM client instance
        output_mode: Output location mode - "default", "alongside", or "custom"
        output_dir: Custom output directory (for "custom" mode)
        individual_files: Write separate JSON for each input file
    """

    extractor = SpecificationExtractor(llm_client)
    all_metrics = []
    output_paths = []

    # Find all markdown files
    md_files = list(directory.rglob("*.md"))

    if not md_files:
        print(f"No markdown files found in {directory}")
        return

    print(f"Found {len(md_files)} markdown file(s)\n")

    # Process each file
    for md_file in md_files:
        try:
            metrics = extractor.extract_from_file(md_file)
            all_metrics.append(metrics)

            # Write individual file output if requested
            if individual_files:
                individual_output = get_output_path(md_file, output_mode, output_file, output_dir)
                individual_data = {
                    "file_path": metrics.file_path,
                    "n_spec": metrics.n_spec,
                    "n_func": metrics.n_func,
                    "intent_atoms": [asdict(atom) for atom in metrics.intent_atoms],
                    "functional_units": [asdict(unit) for unit in metrics.functional_units],
                    "metadata": metrics.metadata
                }
                individual_output.write_text(json.dumps(individual_data, indent=2), encoding="utf-8")
                output_paths.append(individual_output)
                print(f"  → Saved to: {individual_output}")

        except Exception as e:
            print(f"Error processing {md_file}: {e}")
            continue

    # Calculate aggregate metrics
    total_n_spec = sum(m.n_spec for m in all_metrics)
    total_n_func = sum(m.n_func for m in all_metrics)

    # Always write aggregate output unless using individual files mode
    if not individual_files:
        # Prepare aggregate output
        output_data = {
            "summary": {
                "total_files": len(all_metrics),
                "total_intent_atoms": total_n_spec,
                "total_functional_units": total_n_func,
                "intent_yield": total_n_func / total_n_spec if total_n_spec > 0 else 0
            },
            "files": [
                {
                    "file_path": m.file_path,
                    "n_spec": m.n_spec,
                    "n_func": m.n_func,
                    "intent_atoms": [asdict(atom) for atom in m.intent_atoms],
                    "functional_units": [asdict(unit) for unit in m.functional_units],
                    "metadata": m.metadata
                }
                for m in all_metrics
            ]
        }

        # Determine output path for aggregate
        if output_mode == "default":
            final_output = output_file
        elif output_mode == "custom" and output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            final_output = output_dir / output_file.name
        else:
            # For alongside mode with directory input, use default
            final_output = output_file

        # Write output
        final_output.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
        output_paths.append(final_output)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Files processed: {len(all_metrics)}")
    print(f"Total Intent Atoms (N_spec): {total_n_spec}")
    print(f"Total Functional Units (N_func): {total_n_func}")
    print(f"Intent Yield (IY): {total_n_func / total_n_spec if total_n_spec > 0 else 0:.2f}")

    if individual_files:
        print(f"\nIndividual results written to {len(output_paths)} files")
        if output_mode == "custom" and output_dir:
            print(f"Output directory: {output_dir}")
    else:
        print(f"\nResults written to: {output_paths[0] if output_paths else output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract SIB metrics from markdown specification documents using local LLM"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input markdown file or directory containing markdown files"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("sib_metrics.json"),
        help="Output JSON file (default: sib_metrics.json)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="llama3",
        help="Local model name (default: llama3)"
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default="http://localhost:11434",
        help="LLM API base URL (default: http://localhost:11434 for Ollama)"
    )
    parser.add_argument(
        "--api-type",
        type=str,
        default="auto",
        choices=["auto", "ollama", "openai"],
        help="API type: auto (detect), ollama, or openai (for LM Studio) (default: auto)"
    )
    parser.add_argument(
        "--json-mode",
        action="store_true",
        default=True,
        help="Enable JSON mode for structured outputs (OpenAI API only, default: True)"
    )
    parser.add_argument(
        "--no-json-mode",
        action="store_false",
        dest="json_mode",
        help="Disable JSON mode"
    )
    parser.add_argument(
        "--output-mode",
        type=str,
        default="default",
        choices=["default", "alongside", "custom"],
        help="Output location mode: default (current dir), alongside (next to input), custom (specify dir)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Custom output directory (required for --output-mode=custom)"
    )
    parser.add_argument(
        "--individual-files",
        action="store_true",
        help="Write separate JSON file for each input file (useful with alongside/custom modes)"
    )

    args = parser.parse_args()

    # Validate output mode and output_dir
    if args.output_mode == "custom" and not args.output_dir:
        parser.error("--output-dir is required when using --output-mode=custom")

    # Validate input
    if not args.input.exists():
        print(f"Error: Input path does not exist: {args.input}")
        sys.exit(1)

    # Initialize LLM client
    print(f"Connecting to local LLM at {args.base_url}")
    print(f"Using model: {args.model}\n")

    llm_client = LocalLLMClient(
        base_url=args.base_url,
        model=args.model,
        api_type=args.api_type,
        use_json_mode=args.json_mode
    )

    # Process input
    if args.input.is_file():
        # Single file
        extractor = SpecificationExtractor(llm_client)
        metrics = extractor.extract_from_file(args.input)

        output_data = {
            "summary": {
                "total_files": 1,
                "total_intent_atoms": metrics.n_spec,
                "total_functional_units": metrics.n_func,
                "intent_yield": metrics.n_func / metrics.n_spec if metrics.n_spec > 0 else 0
            },
            "files": [{
                "file_path": metrics.file_path,
                "n_spec": metrics.n_spec,
                "n_func": metrics.n_func,
                "intent_atoms": [asdict(atom) for atom in metrics.intent_atoms],
                "functional_units": [asdict(unit) for unit in metrics.functional_units],
                "metadata": metrics.metadata
            }]
        }

        # Determine output path
        output_path = get_output_path(args.input, args.output_mode, args.output, args.output_dir)
        output_path.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
        print(f"\nResults written to: {output_path}")

    elif args.input.is_dir():
        # Directory
        process_directory(
            args.input,
            args.output,
            llm_client,
            output_mode=args.output_mode,
            output_dir=args.output_dir,
            individual_files=args.individual_files
        )

    else:
        print(f"Error: Input must be a file or directory: {args.input}")
        sys.exit(1)


if __name__ == "__main__":
    main()
