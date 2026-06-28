#!/usr/bin/env python3
"""Validate idea-to-spec lifecycle telemetry examples.

This script intentionally avoids third-party dependencies. It checks the
cross-field invariants and closed count-map contracts that JSON Schema either
cannot express directly or cannot validate in this repository without an
external validator package.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

EXAMPLES = (
    ROOT / "examples" / "idea_maturity_metrics_report.happy.json",
    ROOT / "examples" / "idea_maturity_metrics_report.blocked_stale_refs.json",
)

AUTHORITY_KEYS = {
    "may_mutate_canonical_specs",
    "may_write_ontology_package",
    "may_accept_ontology_terms",
    "may_create_branch_or_commit",
    "may_open_pull_request",
    "may_merge_pull_request",
    "may_publish_read_model",
    "may_execute_prompt_agent",
}

SUMMARY_KEYS = {
    "lifecycle_state",
    "clarification_question_count",
    "blocking_question_count",
    "review_required_question_count",
    "answered_question_count",
    "accepted_answer_count",
    "deferred_answer_count",
    "invalid_answer_count",
    "materialized_answer_count",
    "unmaterialized_answer_count",
    "answer_materialization_rate",
    "ontology_gap_count_initial",
    "ontology_gap_resolved_count",
    "ontology_gap_unresolved_count",
    "ontology_gap_resolution_rate",
    "candidate_gap_count_initial",
    "candidate_gap_resolved_count",
    "candidate_gap_unresolved_count",
    "candidate_gap_closure_rate",
    "candidate_node_count",
    "remaining_blocker_count",
    "manual_handoff_count",
    "operator_command_count",
    "failed_gate_count",
    "stale_ref_count",
    "dry_run_count",
    "rerun_count",
    "rerun_request_count",
    "approval_attempt_count",
    "time_to_first_candidate_seconds",
    "time_to_first_materialization_seconds",
    "time_to_approval_ready_seconds",
    "last_progress_at",
    "stalled_phase",
    "candidate_approval_state",
    "candidate_approval_intent_state",
    "candidate_approval_decision_state",
    "platform_promotion_state",
    "promotion_path_count",
    "promotion_request_state",
    "promotion_execution_state",
    "review_status",
    "review_pr_number",
    "review_merge_commit_sha",
    "read_model_publication_state",
    "published_file_count",
    "published_manifest_digest",
}

ONTOLOGY_MATCH_KEYS = {
    "exact",
    "normalized_exact",
    "safe_inflection",
    "safe_phrase_match",
    "target_ref",
    "aggregate_target",
    "manual_bind",
    "manual_alias",
    "project_local_term",
    "reject",
    "defer",
    "other",
}

CANDIDATE_RESOLUTION_KEYS = {
    "risk_accepted",
    "enforcement_mechanism_added",
    "context_supplied",
    "gap_rejected",
    "other",
}


def _fail(path: Path, message: str) -> None:
    raise SystemExit(f"{path}: {message}")


def _object(path: Path, value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(path, f"{name} must be an object")
    return value


def _count(path: Path, summary: dict[str, Any], key: str) -> int:
    value = summary.get(key)
    if not isinstance(value, int) or value < 0:
        _fail(path, f"summary.{key} must be a non-negative integer")
    return value


def _check_summary_keys(path: Path, summary: dict[str, Any]) -> None:
    for key in summary:
        if key not in SUMMARY_KEYS and not key.startswith("x-"):
            _fail(path, f"summary.{key} is not a known metric id or x-* extension")


def _check_authority_boundary(path: Path, data: dict[str, Any]) -> None:
    boundary = _object(path, data.get("authority_boundary"), "authority_boundary")
    if set(boundary) != AUTHORITY_KEYS:
        _fail(path, "authority_boundary must contain exactly the closed key set")
    for key, value in boundary.items():
        if value is not False:
            _fail(path, f"authority_boundary.{key} must be literal false")


def _check_privacy_boundary(path: Path, data: dict[str, Any]) -> None:
    boundary = _object(path, data.get("privacy_boundary"), "privacy_boundary")
    if boundary.get("contains_human_operator_identity") is not False:
        _fail(path, "privacy_boundary.contains_human_operator_identity must be false")
    if boundary.get("join_to_identity_allowed") is not False:
        _fail(path, "privacy_boundary.join_to_identity_allowed must be false")
    if boundary.get("minimum_aggregation_subject") not in {
        "candidate_run",
        "workspace_run",
        "workflow_class",
    }:
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
        if key not in required_keys and not key.startswith("x-"):
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


def validate(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("artifact_kind") != "idea_maturity_metrics_report":
        _fail(path, "artifact_kind mismatch")
    if data.get("metric_pack_id") != "idea_to_spec_maturity":
        _fail(path, "metric_pack_id mismatch")

    summary = _object(path, data.get("summary"), "summary")
    _check_summary_keys(path, summary)
    _check_count_invariants(path, summary)
    _check_authority_boundary(path, data)
    _check_privacy_boundary(path, data)

    groups = _object(path, data.get("groups"), "groups")
    ontology = _object(path, groups.get("ontology_grounding"), "groups.ontology_grounding")
    _check_closed_count_map(
        path,
        ontology.get("ontology_match_kind_counts"),
        "groups.ontology_grounding.ontology_match_kind_counts",
        ONTOLOGY_MATCH_KEYS,
    )
    candidate = _object(path, groups.get("candidate_repair"), "groups.candidate_repair")
    _check_closed_count_map(
        path,
        candidate.get("candidate_resolution_kind_counts"),
        "groups.candidate_repair.candidate_resolution_kind_counts",
        CANDIDATE_RESOLUTION_KEYS,
    )


def main() -> int:
    for path in EXAMPLES:
        validate(path)
        print(f"ok {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
