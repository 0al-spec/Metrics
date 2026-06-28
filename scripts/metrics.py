#!/usr/bin/env python3
"""Metrics repository CLI.

The CLI is intentionally dependency-free for early contract adoption. It owns
reference validation for metric-pack reports and can emit structured validation
reports for sibling repositories such as SpecGraph.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

from validate_idea_maturity_examples import (
    EXAMPLES,
    ROOT,
    SCHEMA_PATH,
    Contract,
    ValidationError,
    validate,
)

SCHEMA_VERSION = 1
IDEA_MATURITY_VALIDATION_ARTIFACT_KIND = "idea_maturity_metrics_validation_report"
IDEA_MATURITY_VALIDATOR_ID = "metrics.idea_maturity_metrics.validator.v0.1"
IDEA_MATURITY_METRIC_PACK_ID = "idea_to_spec_maturity"

AUTHORITY_BOUNDARY = {
    "may_mutate_canonical_specs": False,
    "may_write_ontology_package": False,
    "may_accept_ontology_terms": False,
    "may_create_branch_or_commit": False,
    "may_open_pull_request": False,
    "may_merge_pull_request": False,
    "may_publish_read_model": False,
    "may_execute_prompt_agent": False,
}


def _now_iso() -> str:
    return dt.datetime.now(tz=dt.timezone.utc).isoformat()


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _validate_idea_maturity_reports(paths: list[Path]) -> dict[str, Any]:
    contract = Contract(json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    entries: list[dict[str, Any]] = []
    valid_count = 0

    for path in paths:
        resolved = path if path.is_absolute() else Path.cwd() / path
        diagnostics: list[dict[str, str]] = []
        status = "ok"
        try:
            validate(resolved, contract)
            valid_count += 1
        except (OSError, json.JSONDecodeError, ValidationError) as exc:
            status = "invalid"
            diagnostics.append({
                "severity": "error",
                "message": str(exc),
            })

        entries.append({
            "path": _display_path(resolved),
            "status": status,
            "diagnostics": diagnostics,
        })

    invalid_count = len(entries) - valid_count
    return {
        "artifact_kind": IDEA_MATURITY_VALIDATION_ARTIFACT_KIND,
        "schema_version": SCHEMA_VERSION,
        "generated_at": _now_iso(),
        "metric_pack_id": IDEA_MATURITY_METRIC_PACK_ID,
        "validator": {
            "id": IDEA_MATURITY_VALIDATOR_ID,
            "rfc_ref": "IDEA_MATURITY_METRICS.md",
            "schema_ref": "schemas/idea_maturity_metrics_report.schema.json",
            "script_ref": "scripts/metrics.py",
        },
        "summary": {
            "status": "ok" if invalid_count == 0 else "failed",
            "report_count": len(entries),
            "valid_count": valid_count,
            "invalid_count": invalid_count,
        },
        "authority_boundary": AUTHORITY_BOUNDARY,
        "reports": entries,
    }


def _cmd_validate_idea_maturity(args: argparse.Namespace) -> int:
    paths = args.reports or list(EXAMPLES)
    report = _validate_idea_maturity_reports(paths)
    if args.output is not None:
        _write_json(args.output, report)

    for entry in report["reports"]:
        if entry["status"] == "ok":
            print(f"ok {entry['path']}")
        else:
            for diagnostic in entry["diagnostics"]:
                print(diagnostic["message"], file=sys.stderr)

    return 0 if report["summary"]["status"] == "ok" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Metrics repository CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate metric-pack artifacts.")
    validate_subparsers = validate_parser.add_subparsers(dest="metric_pack", required=True)

    idea_parser = validate_subparsers.add_parser(
        "idea-maturity",
        help="Validate idea-to-spec maturity metric reports.",
    )
    idea_parser.add_argument(
        "reports",
        nargs="*",
        type=Path,
        help="Report JSON files to validate. Defaults to bundled examples.",
    )
    idea_parser.add_argument(
        "--output",
        type=Path,
        help="Optional structured validation report output path.",
    )
    idea_parser.set_defaults(func=_cmd_validate_idea_maturity)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
