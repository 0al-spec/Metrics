# Idea-to-Spec Maturity Metrics

`metric_pack_id`: `idea_to_spec_maturity`

Authority state: `draft_reference`

This pack defines diagnostic metrics for observing how a raw product idea
becomes a review-ready specification candidate through an agent-assisted
`product_idea_to_spec` workflow.

The pack is intentionally not a single score. It records raw counts, rates,
state transitions, and friction signals so downstream systems can inspect where
an idea matured, where it stalled, and which handoffs still require manual
operator action.

## Scope

The measurement subject is a product idea candidate, not a person or team.

The pack applies to workflows shaped like:

```text
raw product idea
  -> intake / event storming
  -> candidate graph
  -> clarification requests
  -> repair answers
  -> ontology gap decisions
  -> rerun preview / materialization
  -> repaired candidate handoff
  -> candidate approval
  -> promotion request
  -> Git review
  -> public read-model publication
```

The pack can be computed partially. Missing downstream stages should produce
`not_available` or `not_reached` states rather than forcing a failure.

## State Semantics

Dashboards and adapters must not collapse all non-ready states into one bucket.
The following states have distinct meanings:

| State | Meaning |
| --- | --- |
| `not_reached` | The upstream lifecycle has not reached this phase yet. |
| `not_available` | The required artifact family is absent or not integrated. |
| `unknown` | The artifact exists, but the value cannot be determined safely. |
| `blocked` | An explicit gate or validation finding prevented forward progress. |
| `ready` | The phase has enough validated evidence for its next handoff. |
| `failed` | Execution or validation attempted the phase and failed. |
| `dry_run` | A phase produced a non-mutating dry-run report instead of real execution. |

For example, `review_status: not_reached` means no review should exist yet,
while `review_status: unknown` means the review surface exists but the adapter
cannot determine its state. Those conditions require different operator action.

## Non-Goals

- Do not rank people, teams, or organizations.
- Do not collapse the workflow into one universal maturity score.
- Do not treat high graph growth as inherently good.
- Do not auto-approve candidates or trigger Git promotion.
- Do not accept ontology terms or write ontology packages.
- Do not mutate canonical specs.

## Authority Boundary

The metric pack is an observability layer. Metrics may report readiness,
friction, and publication state, but they do not grant authority to mutate
SpecGraph, Ontology, SpecSpace, Platform, Git, or public hosting state.

Every machine-readable report for this pack should carry an authority boundary
equivalent to:

```json
{
  "may_mutate_canonical_specs": false,
  "may_write_ontology_package": false,
  "may_accept_ontology_terms": false,
  "may_create_branch_or_commit": false,
  "may_open_pull_request": false,
  "may_merge_pull_request": false,
  "may_publish_read_model": false,
  "may_execute_prompt_agent": false
}
```

Consumers should reject or quarantine reports where any authority flag is
missing, truthy, non-boolean, or claims write capability. A metrics report can
say that a downstream handoff is ready; it must not perform that handoff.

## Required Input Families

### SpecGraph Inputs

- idea/event-storming intake artifact;
- candidate spec graph;
- clarification requests and accepted answers;
- product ontology gap review decisions;
- answer rerun input;
- rerun preview and rerun materialization;
- repaired candidate promotion handoff;
- repaired active candidate;
- repaired promotion gate;
- repaired repair session journal.

### SpecSpace Inputs

- repair draft state;
- repair rerun request state;
- candidate approval intent state;
- UI-visible workflow state, when available.

### Platform Inputs

- product repair rerun execution report;
- product repair rerun publication report;
- candidate approval execution report;
- product promotion request or handoff report;
- product promotion execution report;
- review status report;
- read-model publication report.

## Metric Groups

### 1. Clarification Load

These metrics describe how much context the system needed to ask for before the
candidate could mature.

| Metric id | Meaning |
| --- | --- |
| `clarification_question_count` | Total clarification requests emitted. |
| `blocking_question_count` | Clarification requests that block readiness. |
| `review_required_question_count` | Questions requiring human/operator review. |
| `answered_question_count` | Draft or accepted answers supplied by an operator. |
| `accepted_answer_count` | Answers accepted for rerun. |
| `deferred_answer_count` | Answers explicitly deferred. |
| `invalid_answer_count` | Drafts rejected by validation. |

Interpretation: a high question count is not automatically bad. It can mean the
raw idea was under-specified, the bounded context was broad, or the system is
asking overly granular questions. Trend and distribution matter more than
absolute value.

### 2. Answer Materialization

These metrics catch the gap between "the user answered" and "the candidate graph
actually improved."

| Metric id | Meaning |
| --- | --- |
| `materialized_answer_count` | Accepted answers that produced review-only candidate changes. |
| `unmaterialized_answer_count` | Accepted answers that did not change preview/materialization state. |
| `answer_materialization_rate` | `materialized_answer_count / accepted_answer_count`. |
| `candidate_review_hint_count` | Accepted non-ontology hints preserved for review. |
| `stale_answer_count` | Answers rejected because target refs or source refs no longer match. |

If `accepted_answer_count > 0` and `materialized_answer_count == 0`, the workflow
is likely collecting user work without converting it into specification progress.

### 3. Ontology Grounding

These metrics observe whether generated product terms are grounded in the active
ontology frame or intentionally kept project-local.

| Metric id | Meaning |
| --- | --- |
| `ontology_gap_count_initial` | Ontology gaps before repair answers/decisions. |
| `ontology_gap_resolved_count` | Ontology gaps preview-resolved by decisions or safe matching. |
| `ontology_gap_unresolved_count` | Ontology gaps remaining after rerun materialization. |
| `ontology_gap_resolution_rate` | `ontology_gap_resolved_count / ontology_gap_count_initial`. |
| `ontology_project_local_term_count` | Terms intentionally kept as project-local. |
| `ontology_rejected_term_count` | Terms rejected as non-domain or not useful. |
| `ontology_deferred_term_count` | Terms deferred for later owner review. |
| `ontology_match_kind_counts` | Resolution counts by match kind. |

Recommended `ontology_match_kind_counts` keys:

- `exact`;
- `normalized_exact`;
- `safe_inflection`;
- `safe_phrase_match`;
- `target_ref`;
- `aggregate_target`;
- `manual_bind`;
- `manual_alias`;
- `project_local_term`;
- `reject`;
- `defer`.

The metric pack should preserve match provenance and confidence. A high
resolution rate is useful only when match provenance remains conservative and
reviewable.

### 4. Candidate Repair and Blocker Closure

These metrics describe product/specification repair, separate from ontology
grounding.

| Metric id | Meaning |
| --- | --- |
| `candidate_gap_count_initial` | Product/spec gaps before repair materialization. |
| `candidate_gap_resolved_count` | Product/spec gaps removed in review-only materialization. |
| `candidate_gap_unresolved_count` | Product/spec gaps still present after repair. |
| `candidate_gap_closure_rate` | `candidate_gap_resolved_count / candidate_gap_count_initial`. |
| `risk_accepted_count` | Risks explicitly accepted for candidate review. |
| `enforcement_mechanism_added_count` | Enforcement-mechanism gaps closed by answers. |
| `context_supplied_count` | Gaps closed by additional bounded-context information. |
| `remaining_blocker_count` | Blocking issues still preventing approval readiness. |
| `rerun_count` | Number of repair rerun attempts. |

For reviewability, gap closure must preserve evidence such as `answer_id`,
`target_ref`, node scope, and resolution kind.

### 5. Workflow Friction

These metrics expose where the product lane still depends on manual operator
handoffs or repeated recovery.

| Metric id | Meaning |
| --- | --- |
| `manual_handoff_count` | Explicit operator commands or external handoffs needed. |
| `operator_command_count` | Commands run by an operator to advance the workflow. |
| `failed_gate_count` | Gates that returned blocked/error states. |
| `stale_ref_count` | Failures caused by stale source refs or mismatched artifacts. |
| `dry_run_count` | Dry-run executions instead of real controlled execution. |
| `rerun_request_count` | User or operator rerun requests. |
| `approval_attempt_count` | Candidate approval attempts. |

These are product-ergonomics signals. High friction may be acceptable in early
MVP/bootstrap mode but should trend down for product workspaces.

### 6. Promotion Readiness

These metrics describe lifecycle readiness without claiming that promotion has
actually happened.

| Metric id | Meaning |
| --- | --- |
| `ready_for_candidate_approval` | Candidate is ready for explicit approval intent. |
| `candidate_approval_intent_present` | SpecSpace-owned approval intent exists. |
| `candidate_approval_decision_present` | Platform materialized approval decision exists. |
| `ready_for_platform_promotion` | Candidate has approval decision and promotion prerequisites. |
| `promotion_path_count` | Materialized candidate paths approved for review. |
| `promotion_request_present` | Promotion request handoff artifact exists. |
| `promotion_execution_present` | Controlled promotion execution report exists. |
| `git_review_opened` | Review PR was opened or dry-run report says it would be opened. |

`ready_for_candidate_approval` and `ready_for_platform_promotion` must remain
separate. The former is product/spec readiness; the latter requires an explicit
approval decision and promotion handoff.

### 7. Review and Publication Completion

These metrics track the final review/read-model lifecycle.

| Metric id | Meaning |
| --- | --- |
| `review_status` | `not_reached`, `open`, `merged`, `blocked`, or `unknown`. |
| `review_pr_number` | Pull request number, when available. |
| `review_merge_commit_present` | Whether merge commit evidence is available. |
| `read_model_published` | Public-safe read model publication completed. |
| `published_file_count` | Number of public-safe files in the published bundle. |
| `published_manifest_digest_present` | Whether manifest/checksum evidence exists. |

Publishing is a public read-model event, not proof that ontology terms were
accepted or that canonical specs were mutated outside review.

## Metric Contract

The following table gives a minimal machine-readable contract for each metric
identifier. Implementations may add provenance fields, but should preserve the
metric ids, types, nullability rules, and source-of-truth boundaries.

| Metric id | Type | Unit | Nullability | Source of truth | Formula / derivation |
| --- | --- | --- | --- | --- | --- |
| `clarification_question_count` | integer | count | zero allowed | clarification requests | Count all emitted requests. |
| `blocking_question_count` | integer | count | zero allowed | clarification requests | Count requests that block readiness. |
| `review_required_question_count` | integer | count | zero allowed | clarification requests | Count requests marked review-required. |
| `answered_question_count` | integer | count | zero allowed | draft state and answers | Count submitted draft or accepted answers. |
| `accepted_answer_count` | integer | count | zero allowed | clarification answers | Count answers accepted for rerun. |
| `deferred_answer_count` | integer | count | zero allowed | draft import preview and answers | Count answers with defer semantics. |
| `invalid_answer_count` | integer | count | zero allowed | draft import preview | Count rejected or invalid drafts. |
| `materialized_answer_count` | integer | count | zero allowed | rerun materialization | Count accepted answers that produced candidate changes. |
| `unmaterialized_answer_count` | integer | count | zero allowed | rerun materialization | Accepted answers minus materialized answers, bounded at zero. |
| `answer_materialization_rate` | number | ratio 0..1 | null when denominator is zero | rerun materialization | `materialized_answer_count / accepted_answer_count`. |
| `candidate_review_hint_count` | integer | count | zero allowed | rerun input | Count non-ontology candidate review hints. |
| `stale_answer_count` | integer | count | zero allowed | draft import preview and rerun materialization | Count answers rejected for stale refs. |
| `ontology_gap_count_initial` | integer | count | zero allowed | candidate graph or repair session | Count ontology gaps before decisions. |
| `ontology_gap_resolved_count` | integer | count | zero allowed | rerun preview/materialization | Count preview-resolved ontology gaps. |
| `ontology_gap_unresolved_count` | integer | count | zero allowed | rerun preview/materialization | Count ontology gaps remaining after repair. |
| `ontology_gap_resolution_rate` | number | ratio 0..1 | null when denominator is zero | rerun preview/materialization | `ontology_gap_resolved_count / ontology_gap_count_initial`. |
| `ontology_project_local_term_count` | integer | count | zero allowed | ontology decisions | Count project-local term decisions. |
| `ontology_rejected_term_count` | integer | count | zero allowed | ontology decisions | Count rejected term decisions. |
| `ontology_deferred_term_count` | integer | count | zero allowed | ontology decisions | Count deferred term decisions. |
| `ontology_match_kind_counts` | object | count map | empty map allowed | ontology decisions and materialization evidence | Group ontology resolutions by match kind. |
| `candidate_gap_count_initial` | integer | count | zero allowed | candidate graph or repair session | Count product/spec gaps before materialization. |
| `candidate_gap_resolved_count` | integer | count | zero allowed | rerun materialization | Count candidate gaps removed in preview. |
| `candidate_gap_unresolved_count` | integer | count | zero allowed | rerun materialization | Count candidate gaps still present after repair. |
| `candidate_gap_closure_rate` | number | ratio 0..1 | null when denominator is zero | rerun materialization | `candidate_gap_resolved_count / candidate_gap_count_initial`. |
| `risk_accepted_count` | integer | count | zero allowed | candidate gap resolutions | Count risk-accepted resolutions. |
| `enforcement_mechanism_added_count` | integer | count | zero allowed | candidate gap resolutions | Count enforcement-mechanism resolutions. |
| `context_supplied_count` | integer | count | zero allowed | candidate gap resolutions | Count context-supplied resolutions. |
| `remaining_blocker_count` | integer | count | zero allowed | repair session and gates | Count unresolved blocking findings. |
| `rerun_count` | integer | count | zero allowed | rerun requests and execution reports | Count repair rerun attempts. |
| `manual_handoff_count` | integer | count | zero allowed | Platform and operator handoff reports | Count explicit operator handoffs. |
| `operator_command_count` | integer | count | zero allowed | Platform execution reports | Count operator-run commands needed to advance. |
| `failed_gate_count` | integer | count | zero allowed | Platform and SpecGraph gate reports | Count gate failures or blocked gate reports. |
| `stale_ref_count` | integer | count | zero allowed | gate reports and import previews | Count stale source-ref failures. |
| `dry_run_count` | integer | count | zero allowed | Platform execution reports | Count dry-run phases. |
| `rerun_request_count` | integer | count | zero allowed | SpecSpace rerun request state | Count rerun requests. |
| `approval_attempt_count` | integer | count | zero allowed | approval intent and gate reports | Count approval attempts. |
| `ready_for_candidate_approval` | boolean | flag | false when unavailable | repair session and repaired handoff | True only when candidate approval gate prerequisites are met. |
| `candidate_approval_intent_present` | boolean | flag | false when unavailable | SpecSpace approval intent state | True when approval intent exists for the active session. |
| `candidate_approval_decision_present` | boolean | flag | false when unavailable | Platform approval execution report | True when `candidate_approval_decision` exists. |
| `ready_for_platform_promotion` | boolean | flag | false when unavailable | Platform approval/promotion reports | True only after approval decision and promotion prerequisites exist. |
| `promotion_path_count` | integer | count | zero allowed | promotion gate and approval decision | Count approved materialized paths. |
| `promotion_request_present` | boolean | flag | false when unavailable | promotion request report | True when promotion request handoff exists. |
| `promotion_execution_present` | boolean | flag | false when unavailable | promotion execution report | True when controlled promotion execution report exists. |
| `git_review_opened` | boolean | flag | false when unavailable | promotion execution or review report | True when review PR opened, or dry-run says it would open. |
| `review_status` | enum | state | `not_reached` allowed | review status report | One of `not_reached`, `open`, `merged`, `blocked`, `unknown`. |
| `review_pr_number` | integer | identifier | null when absent | review status report | Pull request number. |
| `review_merge_commit_present` | boolean | flag | false when unavailable | review status report | True when merge commit evidence exists. |
| `read_model_published` | boolean | flag | false when unavailable | read-model publication report | True when public-safe publication completed. |
| `published_file_count` | integer | count | zero allowed | publication report and manifest | Count public-safe files. |
| `published_manifest_digest_present` | boolean | flag | false when unavailable | publication report and checksums | True when manifest/checksum digest evidence exists. |

## Derived Lifecycle States

Implementations may derive a coarse state for dashboards:

| State | Meaning |
| --- | --- |
| `intake_ready` | Idea intake has enough frame to build a candidate graph. |
| `repair_required` | Candidate exists but has unresolved questions/gaps. |
| `repair_rerun_requested` | User requested a rerun from saved drafts. |
| `repaired_candidate_ready` | Repaired candidate has zero blocking gaps. |
| `approval_ready` | Candidate can receive explicit approval intent. |
| `approval_materialized` | Platform produced `candidate_approval_decision`. |
| `promotion_requested` | Promotion request handoff exists. |
| `git_review_opened` | Controlled Git review opened or dry-run equivalent exists. |
| `read_model_published` | Public-safe read model publication completed. |
| `blocked` | A gate prevents forward progress. |

The derived state is a navigation aid. It must not hide raw blockers, counts, or
provenance.

## Formula Conventions

Rates should use `null` rather than `0` when the denominator is zero.

```text
answer_materialization_rate =
  materialized_answer_count / accepted_answer_count

ontology_gap_resolution_rate =
  ontology_gap_resolved_count / ontology_gap_count_initial

candidate_gap_closure_rate =
  candidate_gap_resolved_count / candidate_gap_count_initial

promotion_path_density =
  promotion_path_count / candidate_node_count
```

`promotion_path_density` is diagnostic only. A higher value does not imply a
better candidate; it may indicate over-materialization.

## Consistency Invariants

Implementations should validate these invariants before publishing or displaying
the report as a trustworthy metric artifact:

```text
0 <= blocking_question_count <= clarification_question_count
0 <= review_required_question_count <= clarification_question_count
0 <= accepted_answer_count <= answered_question_count
0 <= deferred_answer_count <= answered_question_count
0 <= invalid_answer_count <= answered_question_count

0 <= materialized_answer_count <= accepted_answer_count
0 <= unmaterialized_answer_count <= accepted_answer_count
materialized_answer_count + unmaterialized_answer_count <= accepted_answer_count

0 <= ontology_gap_resolved_count <= ontology_gap_count_initial
0 <= ontology_gap_unresolved_count <= ontology_gap_count_initial
ontology_gap_resolved_count + ontology_gap_unresolved_count
  <= ontology_gap_count_initial

0 <= candidate_gap_resolved_count <= candidate_gap_count_initial
0 <= candidate_gap_unresolved_count <= candidate_gap_count_initial
candidate_gap_resolved_count + candidate_gap_unresolved_count
  <= candidate_gap_count_initial

ready_for_platform_promotion == true
  requires candidate_approval_decision_present == true
  and promotion_request_present == true

read_model_published == true
  requires review_status == merged

git_review_opened == true
  requires promotion_execution_present == true
```

When an invariant fails, consumers should report `blocked` or `unknown` for the
affected derived state rather than silently normalizing the data.

## Run Artifact Sketch

```json
{
  "artifact_kind": "idea_maturity_metrics_report",
  "metric_pack_id": "idea_to_spec_maturity",
  "authority_state": "draft_reference",
  "candidate": {
    "candidate_id": "local-subscription-control",
    "workspace_route": "/local-subscription-control"
  },
  "summary": {
    "lifecycle_state": "approval_ready",
    "clarification_question_count": 25,
    "accepted_answer_count": 15,
    "materialized_answer_count": 15,
    "answer_materialization_rate": 1.0,
    "ontology_gap_count_initial": 11,
    "ontology_gap_resolved_count": 11,
    "ontology_gap_unresolved_count": 0,
    "ontology_gap_resolution_rate": 1.0,
    "candidate_gap_count_initial": 4,
    "candidate_gap_resolved_count": 4,
    "candidate_gap_unresolved_count": 0,
    "candidate_gap_closure_rate": 1.0,
    "manual_handoff_count": 0,
    "remaining_blocker_count": 0,
    "ready_for_candidate_approval": true,
    "ready_for_platform_promotion": false
  },
  "groups": {
    "ontology_grounding": {
      "match_kind_counts": {
        "normalized_exact": 1,
        "safe_inflection": 1,
        "project_local_term": 9
      }
    },
    "candidate_repair": {
      "resolution_kind_counts": {
        "risk_accepted": 1,
        "enforcement_mechanism_added": 3
      }
    },
    "workflow_friction": {
      "failed_gate_count": 0,
      "stale_ref_count": 0,
      "dry_run_count": 0
    }
  },
  "source_artifacts": [
    "runs/repaired_idea_to_spec_repair_session.json",
    "runs/repaired_candidate_promotion_handoff_report.json"
  ],
  "authority_boundary": {
    "may_mutate_canonical_specs": false,
    "may_write_ontology_package": false,
    "may_accept_ontology_terms": false,
    "may_create_branch_or_commit": false,
    "may_open_pull_request": false,
    "may_publish_read_model": false
  }
}
```

## Interpretation Guardrails

1. Maturity means "reviewable and bounded", not "large".
2. A low question count is not always good; it can indicate missing discovery.
3. A high materialization rate is useful only when answers are validated against
   current refs.
4. Ontology resolution must preserve conservative match provenance.
5. Project-local terms are legitimate outcomes, not failures.
6. Accepted risk must remain visible as risk evidence, not disappear as if the
   risk never existed.
7. Workflow friction should be interpreted as product ergonomics, not operator
   performance.
8. Publication metrics observe public-safe read-model state; they do not imply
   automatic canonical acceptance.

## Initial Adoption Path

1. Define a read-only metrics report over existing SpecGraph, SpecSpace, and
   Platform artifacts.
2. Display raw counts and rates in SpecSpace without a single composite score.
3. Compare runs for the same candidate before/after repair and after rerun.
4. Use high-friction and stale-ref counts to prioritize product workflow
   improvements.
5. Only after multiple pilots consider calibrated profiles for recurring
   workspace classes.
