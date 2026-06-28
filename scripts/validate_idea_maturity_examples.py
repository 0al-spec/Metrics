#!/usr/bin/env python3
"""Validate idea-to-spec lifecycle telemetry reports.

This script intentionally avoids third-party dependencies. It checks the
schema-derived enum/key/range contracts plus cross-field invariants that JSON
Schema cannot express directly. Without positional arguments it validates the
bundled examples; with paths it validates those reports instead.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "idea_maturity_metrics_report.schema.json"

EXAMPLES = (
    ROOT / "examples" / "idea_maturity_metrics_report.happy.json",
    ROOT / "examples" / "idea_maturity_metrics_report.blocked_stale_refs.json",
)

X_EXTENSION_PREFIX = "x-"


class ValidationError(Exception):
    """Raised when an idea maturity report violates the contract."""


def _fail(path: Path, message: str) -> None:
    raise ValidationError(f"{path}: {message}")


def _object(path: Path, value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(path, f"{name} must be an object")
    return value


def _list(path: Path, value: Any, name: str) -> list[Any]:
    if not isinstance(value, list):
        _fail(path, f"{name} must be an array")
    return value


class Contract:
    def __init__(self, schema: dict[str, Any]) -> None:
        self.defs = _object(SCHEMA_PATH, schema.get("$defs"), "$defs")
        properties = _object(SCHEMA_PATH, schema.get("properties"), "properties")
        summary = _object(SCHEMA_PATH, properties.get("summary"), "properties.summary")
        summary_properties = _object(
            SCHEMA_PATH,
            summary.get("properties"),
            "properties.summary.properties",
        )
        self.summary_keys = set(summary_properties)
        self.count_fields = self._summary_fields_with_ref(summary_properties, "count")
        self.ratio_fields = self._summary_fields_with_ref(summary_properties, "nullable_ratio")
        self.seconds_fields = self._summary_fields_with_ref(summary_properties, "nullable_seconds")
        self.timestamp_fields = self._summary_fields_with_ref(
            summary_properties,
            "nullable_timestamp",
        )
        self.summary_enums = self._summary_enums(summary_properties)
        self.authority_keys = self._required_def_keys("authority_boundary")
        self.ontology_match_keys = self._required_def_keys("ontology_match_kind_counts")
        self.candidate_resolution_keys = self._required_def_keys(
            "candidate_resolution_kind_counts"
        )
        privacy = _object(SCHEMA_PATH, self.defs.get("privacy_boundary"), "privacy_boundary")
        privacy_props = _object(SCHEMA_PATH, privacy.get("properties"), "privacy.properties")
        minimum_subject = _object(
            SCHEMA_PATH,
            privacy_props.get("minimum_aggregation_subject"),
            "privacy.minimum_aggregation_subject",
        )
        self.privacy_subjects = set(_list(SCHEMA_PATH, minimum_subject.get("enum"), "enum"))

    def _required_def_keys(self, def_name: str) -> set[str]:
        definition = _object(SCHEMA_PATH, self.defs.get(def_name), f"$defs.{def_name}")
        return set(_list(SCHEMA_PATH, definition.get("required"), f"$defs.{def_name}.required"))

    def _summary_fields_with_ref(
        self,
        summary_properties: dict[str, Any],
        def_name: str,
    ) -> set[str]:
        return {
            key
            for key, value in summary_properties.items()
            if isinstance(value, dict) and value.get("$ref") == f"#/$defs/{def_name}"
        }

    def _summary_enums(
        self,
        summary_properties: dict[str, Any],
    ) -> dict[str, set[str]]:
        enums: dict[str, set[str]] = {}
        for key, value in summary_properties.items():
            if not isinstance(value, dict):
                continue
            if "enum" in value:
                enums[key] = set(_list(SCHEMA_PATH, value["enum"], f"summary.{key}.enum"))
                continue
            ref = value.get("$ref")
            if not isinstance(ref, str) or not ref.startswith("#/$defs/"):
                continue
            def_name = ref.removeprefix("#/$defs/")
            definition = self.defs.get(def_name)
            if isinstance(definition, dict) and "enum" in definition:
                enums[key] = set(
                    _list(SCHEMA_PATH, definition["enum"], f"$defs.{def_name}.enum")
                )
        return enums


def _count(path: Path, summary: dict[str, Any], key: str) -> int:
    value = summary.get(key)
    if not isinstance(value, int) or value < 0:
        _fail(path, f"summary.{key} must be a non-negative integer")
    return value


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _parse_rfc3339(path: Path, value: Any, name: str) -> None:
    if value is None:
        return
    if not isinstance(value, str):
        _fail(path, f"{name} must be an RFC 3339 timestamp string or null")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        dt.datetime.fromisoformat(normalized)
    except ValueError as exc:
        _fail(path, f"{name} must be an RFC 3339 timestamp: {exc}")


def _check_summary_keys(path: Path, summary: dict[str, Any], contract: Contract) -> None:
    for key in summary:
        if key not in contract.summary_keys and not key.startswith(X_EXTENSION_PREFIX):
            _fail(path, f"summary.{key} is not a known metric id or x-* extension")


def _check_summary_schema_shape(
    path: Path,
    summary: dict[str, Any],
    contract: Contract,
) -> None:
    for key in contract.count_fields:
        if key in summary:
            _count(path, summary, key)
    for key in contract.ratio_fields:
        if key not in summary:
            continue
        value = summary[key]
        if value is not None and (not _is_number(value) or value < 0 or value > 1):
            _fail(path, f"summary.{key} must be a ratio in 0..1 or null")
    for key in contract.seconds_fields:
        if key not in summary:
            continue
        value = summary[key]
        if value is not None and (not _is_number(value) or value < 0):
            _fail(path, f"summary.{key} must be non-negative seconds or null")
    for key in contract.timestamp_fields:
        if key in summary:
            _parse_rfc3339(path, summary[key], f"summary.{key}")
    for key, allowed_values in contract.summary_enums.items():
        if key in summary and summary[key] not in allowed_values:
            _fail(path, f"summary.{key} has unsupported value {summary[key]!r}")


def _check_timeline_timestamps(path: Path, data: dict[str, Any]) -> None:
    timeline = data.get("timeline")
    if timeline is None:
        return
    timeline_object = _object(path, timeline, "timeline")
    for key, value in timeline_object.items():
        if key.endswith("_at"):
            _parse_rfc3339(path, value, f"timeline.{key}")


def _check_phase_dwell_seconds(path: Path, data: dict[str, Any]) -> None:
    groups = data.get("groups")
    if not isinstance(groups, dict):
        return
    temporal = groups.get("temporal_progress")
    if not isinstance(temporal, dict):
        return
    phase_dwell = temporal.get("phase_dwell_seconds")
    if phase_dwell is None:
        return
    phase_dwell_object = _object(
        path,
        phase_dwell,
        "groups.temporal_progress.phase_dwell_seconds",
    )
    for key, value in phase_dwell_object.items():
        if value is not None and (not _is_number(value) or value < 0):
            _fail(path, f"groups.temporal_progress.phase_dwell_seconds.{key} invalid")


def _check_authority_boundary(
    path: Path,
    data: dict[str, Any],
    contract: Contract,
) -> None:
    boundary = _object(path, data.get("authority_boundary"), "authority_boundary")
    if set(boundary) != contract.authority_keys:
        _fail(path, "authority_boundary must contain exactly the closed key set")
    for key, value in boundary.items():
        if value is not False:
            _fail(path, f"authority_boundary.{key} must be literal false")


def _check_privacy_boundary(path: Path, data: dict[str, Any], contract: Contract) -> None:
    boundary = _object(path, data.get("privacy_boundary"), "privacy_boundary")
    if boundary.get("contains_human_operator_identity") is not False:
        _fail(path, "privacy_boundary.contains_human_operator_identity must be false")
    if boundary.get("join_to_identity_allowed") is not False:
        _fail(path, "privacy_boundary.join_to_identity_allowed must be false")
    if boundary.get("minimum_aggregation_subject") not in contract.privacy_subjects:
        _fail(path, "privacy_boundary.minimum_aggregation_subject is unsupported")


def _check_closed_count_map(
    path: Path,
    value: Any,
    name: str,
    required_keys: set[str],
) -> None:
    count_map = _object(path, value, name)
    missing = required_keys - set(count_map)
    if missing:
        _fail(path, f"{name} missing keys: {', '.join(sorted(missing))}")
    for key, count in count_map.items():
        if key not in required_keys and not key.startswith(X_EXTENSION_PREFIX):
            _fail(path, f"{name}.{key} is not in the closed key set or x-*")
        if not isinstance(count, int) or count < 0:
            _fail(path, f"{name}.{key} must be a non-negative integer")


def _check_count_invariants(path: Path, summary: dict[str, Any]) -> None:
    clarification = _count(path, summary, "clarification_question_count")
    blocking = _count(path, summary, "blocking_question_count")
    review_required = _count(path, summary, "review_required_question_count")
    answered = _count(path, summary, "answered_question_count")
    accepted = _count(path, summary, "accepted_answer_count")
    deferred = _count(path, summary, "deferred_answer_count")
    invalid = _count(path, summary, "invalid_answer_count")
    materialized = _count(path, summary, "materialized_answer_count")
    unmaterialized = _count(path, summary, "unmaterialized_answer_count")

    if blocking > clarification:
        _fail(path, "blocking_question_count exceeds clarification_question_count")
    if review_required > clarification:
        _fail(path, "review_required_question_count exceeds clarification_question_count")
    if accepted > answered:
        _fail(path, "accepted_answer_count exceeds answered_question_count")
    if deferred > answered:
        _fail(path, "deferred_answer_count exceeds answered_question_count")
    if invalid > answered:
        _fail(path, "invalid_answer_count exceeds answered_question_count")
    if accepted + invalid + deferred > answered:
        _fail(path, "accepted + invalid + deferred answers exceed answered answers")
    if materialized > accepted:
        _fail(path, "materialized_answer_count exceeds accepted_answer_count")
    if unmaterialized > accepted:
        _fail(path, "unmaterialized_answer_count exceeds accepted_answer_count")
    if materialized + unmaterialized > accepted:
        _fail(path, "materialized + unmaterialized answers exceed accepted answers")

    ontology_initial = _count(path, summary, "ontology_gap_count_initial")
    ontology_resolved = _count(path, summary, "ontology_gap_resolved_count")
    ontology_unresolved = _count(path, summary, "ontology_gap_unresolved_count")
    if ontology_resolved > ontology_initial:
        _fail(path, "ontology_gap_resolved_count exceeds ontology_gap_count_initial")
    if ontology_unresolved > ontology_initial:
        _fail(path, "ontology_gap_unresolved_count exceeds ontology_gap_count_initial")
    if ontology_resolved + ontology_unresolved > ontology_initial:
        _fail(path, "ontology resolved + unresolved gaps exceed initial gaps")

    candidate_initial = _count(path, summary, "candidate_gap_count_initial")
    candidate_resolved = _count(path, summary, "candidate_gap_resolved_count")
    candidate_unresolved = _count(path, summary, "candidate_gap_unresolved_count")
    if candidate_resolved > candidate_initial:
        _fail(path, "candidate_gap_resolved_count exceeds candidate_gap_count_initial")
    if candidate_unresolved > candidate_initial:
        _fail(path, "candidate_gap_unresolved_count exceeds candidate_gap_count_initial")
    if candidate_resolved + candidate_unresolved > candidate_initial:
        _fail(path, "candidate resolved + unresolved gaps exceed initial gaps")


def validate(path: Path, contract: Contract) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("artifact_kind") != "idea_maturity_metrics_report":
        _fail(path, "artifact_kind mismatch")
    if data.get("metric_pack_id") != "idea_to_spec_maturity":
        _fail(path, "metric_pack_id mismatch")
    if data.get("authority_state") != "draft_reference":
        _fail(path, "authority_state mismatch")

    summary = _object(path, data.get("summary"), "summary")
    _check_summary_keys(path, summary, contract)
    _check_summary_schema_shape(path, summary, contract)
    _check_count_invariants(path, summary)
    _check_authority_boundary(path, data, contract)
    _check_privacy_boundary(path, data, contract)
    _check_timeline_timestamps(path, data)
    _check_phase_dwell_seconds(path, data)

    groups = _object(path, data.get("groups"), "groups")
    ontology = _object(path, groups.get("ontology_grounding"), "groups.ontology_grounding")
    _check_closed_count_map(
        path,
        ontology.get("ontology_match_kind_counts"),
        "groups.ontology_grounding.ontology_match_kind_counts",
        contract.ontology_match_keys,
    )
    candidate = _object(path, groups.get("candidate_repair"), "groups.candidate_repair")
    _check_closed_count_map(
        path,
        candidate.get("candidate_resolution_kind_counts"),
        "groups.candidate_repair.candidate_resolution_kind_counts",
        contract.candidate_resolution_keys,
    )


def _paths_from_args(argv: list[str] | None = None) -> list[Path]:
    parser = argparse.ArgumentParser(
        description="Validate idea-to-spec lifecycle telemetry reports.",
    )
    parser.add_argument(
        "reports",
        nargs="*",
        type=Path,
        help="Report JSON files to validate. Defaults to bundled examples.",
    )
    args = parser.parse_args(argv)
    return args.reports or list(EXAMPLES)


def main() -> int:
    contract = Contract(json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    for path in _paths_from_args():
        resolved = path if path.is_absolute() else Path.cwd() / path
        try:
            validate(resolved, contract)
        except ValidationError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        try:
            label = resolved.relative_to(ROOT)
        except ValueError:
            label = resolved
        print(f"ok {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
