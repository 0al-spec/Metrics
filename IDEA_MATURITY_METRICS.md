# Idea-to-Spec Lifecycle Telemetry

`metric_pack_id`: `idea_to_spec_maturity`

Authority state: `draft_reference`

This pack defines diagnostic lifecycle telemetry for observing how a raw product
idea becomes a review-ready specification candidate through an agent-assisted
`product_idea_to_spec` workflow.

The pack is intentionally not a single score. It records raw counts, rates,
state transitions, and friction signals so downstream systems can inspect where
an idea matured, where it stalled, and which handoffs still require manual
operator action.

The pack is 0AL-specific at the artifact binding layer. The reusable ideas are
clarification load, answer materialization, blocker closure, dwell time, handoff
friction, and review/publication evidence. The concrete bindings to SpecGraph,
SpecSpace, Platform, and Ontology artifacts are not intended to be portable
outside this workflow without an adapter profile.

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

This boundary is a negative declaration, not a security enforcement mechanism.
Consumers must not infer write authority from a metrics report. Real enforcement
must come from runtime permissions, credentials, policy engines, signed producer
identity, or external attestation.

The closed required key set is:

```text
may_mutate_canonical_specs
may_write_ontology_package
may_accept_ontology_terms
may_create_branch_or_commit
may_open_pull_request
may_merge_pull_request
may_publish_read_model
may_execute_prompt_agent
```

Reports may also carry external attestation references:

```json
{
  "producer_attestation": {
    "producer_id": "did:example:metrics-adapter",
    "agent_passport_ref": "agent-passport://example/metrics-adapter",
    "signature_ref": "cosign://example",
    "runtime_enforcement_evidence_ref": "zeroald://run/example"
  }
}
```

Attestation references are evidence hooks. They do not turn the metrics report
itself into an authority-bearing artifact.

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

## Machine-Readable Artifacts

This draft includes a schema-first anchor and examples:

- `schemas/idea_maturity_metrics_report.schema.json`;
- `schemas/idea_maturity_metrics_validation_report.schema.json`;
- `examples/idea_maturity_metrics_report.happy.json`;
- `examples/idea_maturity_metrics_report.blocked_stale_refs.json`;
- `examples/idea_maturity_metrics_report.readiness_explainers.json`;
- `examples/idea_maturity_metrics_report.future_additive_fields.json`;
- `examples/idea_maturity_metrics_validation_report.ok.json`;
- `examples/idea_maturity_metrics_validation_report.failed.json`;
- `examples/invalid/idea_maturity_metrics_report.bad_authority_flag.json`;
- `examples/invalid/idea_maturity_metrics_validation_report.bad_summary_counts.json`.

The blocked/stale example is intentionally more important than the happy path:
it demonstrates stale refs, stalled repair dwell time, zero materialization, and
policy findings without collapsing those observations into an invalid report.

The stable validator invocation and compatibility rules are defined in
`VALIDATOR_CONTRACT.md`. Consumers should treat Metrics as the source of truth
for schema and invariant validation, rather than copying validator logic into
SpecGraph, SpecSpace, Platform, or other sibling repositories.

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
| `materialized_answer_count` | Accepted answers that produced per-gap review-only candidate changes. |
| `consumed_answer_count` | Accepted answers consumed by the rerun input overlay. |
| `aggregate_answer_count` | Accepted answers consumed as aggregate/control evidence instead of per-gap materialization. |
| `dismissed_answer_count` | Accepted reject/dismiss actions consumed by the rerun input overlay without counting as closure evidence. |
| `closure_evidence_answer_count` | Accepted answers that have either per-gap materialization or aggregate/control closure evidence. |
| `unmaterialized_answer_count` | Accepted ordinary answers that still lack materialization or closure evidence. |
| `answer_materialization_rate` | `closure_evidence_answer_count / accepted_answer_count`. |
| `candidate_review_hint_count` | Accepted non-ontology hints preserved for review. |
| `stale_answer_count` | Answers rejected because target refs or source refs no longer match. |

If `accepted_answer_count > 0` and `closure_evidence_answer_count == 0`, the
workflow is likely collecting user work without converting it into specification
progress. Aggregate/control answers should not look like ordinary unmaterialized
debt when they were consumed by the rerun overlay as closure evidence.

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
| `project_local_ontology_review_status` | Status of the project-local ontology decision effect report. |
| `project_local_ontology_accepted_decision_count` | Accepted project-local ontology review decisions counted as review evidence. |
| `project_local_ontology_keep_local_count` | Accepted decisions to keep a term project-local. |
| `project_local_ontology_bind_existing_count` | Accepted decisions binding a project-local term to an existing ontology term. |
| `project_local_ontology_alias_count` | Accepted alias decisions for project-local terms. |
| `project_local_ontology_request_promotion_count` | Accepted requests to promote a term later, without accepting it globally now. |
| `project_local_ontology_reject_count` | Accepted decisions rejecting a project-local term. |
| `project_local_ontology_deferred_decision_count` | Deferred project-local ontology decisions requiring follow-up. |
| `project_local_ontology_invalid_decision_count` | Invalid project-local ontology decisions. |
| `project_local_ontology_missing_decision_count` | Required project-local ontology decisions not yet provided. |
| `project_local_ontology_blocking_decision_count` | Project-local ontology decisions that currently block maturity evidence. |

Closed required `ontology_match_kind_counts` key set:

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
- `defer`;
- `other`.

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
| `candidate_resolution_kind_counts` | Resolution counts by closed candidate gap resolution kind. |
| `risk_accepted_count` | Risks explicitly accepted for candidate review. |
| `enforcement_mechanism_added_count` | Enforcement-mechanism gaps closed by answers. |
| `context_supplied_count` | Gaps closed by additional bounded-context information. |
| `remaining_blocker_count` | Blocking issues still preventing approval readiness. |
| `rerun_count` | Number of repair rerun attempts. |

Closed required `candidate_resolution_kind_counts` key set:

- `risk_accepted`;
- `enforcement_mechanism_added`;
- `context_supplied`;
- `gap_rejected`;
- `other`.

For reviewability, gap closure must preserve evidence such as `answer_id`,
`target_ref`, node scope, and resolution kind.

### 5. Candidate Structure and Event-Storming Depth

These observations describe whether the candidate has enough explicit
event-storming and graph structure to be inspectable. They do not introduce a
new maturity score and they do not replace existing lifecycle metrics such as
`candidate_node_count` or `promotion_path_count`.

| Metric id | Meaning |
| --- | --- |
| `actor_count` | Actors captured in the event-storming intake. |
| `command_count` | Commands captured in the event-storming intake. |
| `domain_event_count` | Domain events captured in the event-storming intake. |
| `policy_count` | Policies captured in the event-storming intake. |
| `constraint_count` | Constraints captured in the event-storming intake. |
| `topology_edge_count` | Candidate graph topology edges. |
| `workflow_edge_count` | Candidate graph workflow edges such as actor-command, command-event, event-policy, policy-command, or constraint-command relations. |
| `requirement_count` | Candidate requirements attached to material candidate nodes. |
| `acceptance_criteria_count` | Acceptance criteria attached to material candidate nodes. |

Interpretation boundary: these are raw structural observations. Zero values are
valid measurements, not validation failures. For example, `actor_count = 0` or
`domain_event_count = 0` records that the event-storming model currently lacks
that structure; `workflow_edge_count = 0` records that the candidate graph is
flat from the workflow-topology perspective; `requirement_count = 0` or
`acceptance_criteria_count = 0` records that material candidate nodes currently
lack those verification surfaces.

These observations should be reported in
`groups.candidate_structure_depth`. Metrics does not define product-specific
thresholds, next actions, readiness blockers, policy findings, scores, approval
state, promotion state, Git authority, or ontology authority for these counts.
Downstream producers and consumers may interpret the observations in their own
readiness surfaces, but that interpretation must remain separate from the metric
contract. In the current `v0` readiness-explainer contract, `blocks[]` is a
closed enum. Producers must not add structural-depth-specific block values
without a contract/version migration. If a producer emits a
`readiness_explainers[]` item for these observations, the structural
interpretation should remain visible through `kind`, `source`, `message`,
`next_action`, and `evidence_refs`, not by overloading approval, promotion, Git,
or publication authority blocks.

Producers may also derive product-specific clarification prompts from these
counts, for example asking for actors when `actor_count = 0` or asking for
command/event links when `workflow_edge_count = 0`. Such prompts are
producer/consumer behavior, not Metrics contract fields. The Metrics layer must
continue to publish only objective counts and validation status; it must not
define the prompt wording, answer schema, rerun policy, readiness gate, score,
or authority boundary for those clarification loops.

### 6. Workflow Friction

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

### 7. Temporal Progress and Stalling

These metrics make "stalled" observable rather than inferred from a static
snapshot.

| Metric id | Meaning |
| --- | --- |
| `time_to_first_candidate_seconds` | Seconds from intake start to first candidate graph. |
| `time_to_first_materialization_seconds` | Seconds from intake start to first materialized preview. |
| `time_to_approval_ready_seconds` | Seconds from intake start to approval-ready repaired candidate. |
| `phase_dwell_seconds` | Map of lifecycle phase to dwell time in seconds. |
| `no_progress_rerun_count` | Reruns that did not reduce blockers or gaps. |
| `last_progress_at` | Timestamp of the latest measurable progress event. |
| `stalled_phase` | Phase currently considered stalled, or `null`. |

Time values are diagnostic and depend on clock quality. Producers should include
timestamp provenance when available and must not invent durations from
incomplete timestamps. For `time_to_*_seconds`, `null` means the duration is not
computable from available evidence. The reason must remain observable through
adjacent lifecycle state, timeline evidence, or policy findings, such as
`not_reached`, `unknown`, or `stale_ref_count`.

### 8. Promotion Readiness

These observations describe lifecycle readiness without claiming that promotion
has actually happened. They are lifecycle states and evidence, not scalar
quality scores.

| Metric id | Meaning |
| --- | --- |
| `candidate_approval_state` | Candidate approval lifecycle state. |
| `candidate_approval_intent_state` | SpecSpace-owned approval intent state. |
| `candidate_approval_decision_state` | Platform approval decision state. |
| `platform_promotion_state` | Platform promotion readiness state. |
| `promotion_path_count` | Materialized candidate paths approved for review. |
| `promotion_request_state` | Promotion request handoff state. |
| `promotion_execution_state` | Controlled promotion execution state. |

`candidate_approval_state` and `platform_promotion_state` must remain separate.
The former is product/spec readiness; the latter requires an explicit approval
decision and promotion handoff.

Recommended state values:

- `not_reached`;
- `not_available`;
- `unknown`;
- `blocked`;
- `ready`;
- `requested`;
- `materialized`;
- `dry_run`;
- `executed`;
- `failed`.

### 9. Review and Publication Completion

These metrics track the final review/read-model lifecycle.

| Metric id | Meaning |
| --- | --- |
| `review_status` | `not_reached`, `not_available`, `open`, `merged`, `blocked`, or `unknown`. |
| `review_pr_number` | Pull request number, when available. |
| `review_merge_commit_sha` | Merge commit SHA, when available. |
| `read_model_publication_state` | Public-safe read-model publication state. |
| `published_file_count` | Number of public-safe files in the published bundle. |
| `published_manifest_digest` | Manifest/checksum digest, when available. |

Publishing is a public read-model event, not proof that ontology terms were
accepted or that canonical specs were mutated outside review.

`read_model_publication_state` should use `not_reached`, `not_available`,
`unknown`, `blocked`, `published`, `dry_run`, or `failed`.

### 10. Economic Observability Bridge

This pack does not define cost formulas. It may link to the
`sib_economic_observability` pack when token footprint, tool footprint, pricing
surface, or observed spend exists.

Recommended bridge fields:

```json
{
  "economic_observability_ref": {
    "metric_pack_id": "sib_economic_observability",
    "run_cost_report_ref": "runs/idea_to_spec_cost_report.json",
    "token_footprint_available": true,
    "tool_footprint_available": true
  }
}
```

When absent, cost signals should be reported as `not_available`, not guessed.

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
| `materialized_answer_count` | integer | count | zero allowed | rerun materialization | Count accepted answers that produced per-gap candidate changes. |
| `consumed_answer_count` | integer | count | zero allowed | rerun input | Count accepted answers consumed by the rerun input overlay. |
| `aggregate_answer_count` | integer | count | zero allowed | rerun input | Count accepted answers consumed as aggregate/control evidence rather than per-gap changes. |
| `dismissed_answer_count` | integer | count | zero allowed | rerun input | Count accepted reject/dismiss actions that are consumed but not closure evidence. |
| `closure_evidence_answer_count` | integer | count | zero allowed | rerun input/materialization | Count accepted answers with per-gap materialization or aggregate/control closure evidence. |
| `unmaterialized_answer_count` | integer | count | zero allowed | rerun input/materialization | Accepted ordinary answers that still lack materialization or closure evidence. |
| `answer_materialization_rate` | number | ratio 0..1 | null when denominator is zero | rerun input/materialization | `closure_evidence_answer_count / accepted_answer_count`. |
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
| `project_local_ontology_review_status` | string | status | optional | project-local ontology decision effect report | Status of the review evidence surface. |
| `project_local_ontology_accepted_decision_count` | integer | count | zero allowed | project-local ontology decision effect report | Accepted review decisions counted as maturity evidence. |
| `project_local_ontology_keep_local_count` | integer | count | zero allowed | project-local ontology decision effect report | Count keep-local decisions. |
| `project_local_ontology_bind_existing_count` | integer | count | zero allowed | project-local ontology decision effect report | Count existing-term binding decisions. |
| `project_local_ontology_alias_count` | integer | count | zero allowed | project-local ontology decision effect report | Count alias decisions. |
| `project_local_ontology_request_promotion_count` | integer | count | zero allowed | project-local ontology decision effect report | Count promotion-request follow-ups. |
| `project_local_ontology_reject_count` | integer | count | zero allowed | project-local ontology decision effect report | Count rejected project-local terms. |
| `project_local_ontology_deferred_decision_count` | integer | count | zero allowed | project-local ontology decision effect report | Count deferred non-resolving decisions. |
| `project_local_ontology_invalid_decision_count` | integer | count | zero allowed | project-local ontology decision effect report | Count invalid decisions. |
| `project_local_ontology_missing_decision_count` | integer | count | zero allowed | project-local ontology decision effect report | Count required decisions not yet supplied. |
| `project_local_ontology_blocking_decision_count` | integer | count | zero allowed | project-local ontology decision effect report | Count invalid or missing decisions blocking maturity evidence. |
| `candidate_gap_count_initial` | integer | count | zero allowed | candidate graph or repair session | Count product/spec gaps before materialization. |
| `candidate_gap_resolved_count` | integer | count | zero allowed | rerun materialization | Count candidate gaps removed in preview. |
| `candidate_gap_unresolved_count` | integer | count | zero allowed | rerun materialization | Count candidate gaps still present after repair. |
| `candidate_gap_closure_rate` | number | ratio 0..1 | null when denominator is zero | rerun materialization | `candidate_gap_resolved_count / candidate_gap_count_initial`. |
| `candidate_resolution_kind_counts` | object | closed count map | all known keys present | candidate gap resolutions | Group candidate gap resolutions by closed resolution kind. |
| `risk_accepted_count` | integer | count | zero allowed | candidate gap resolutions | Count risk-accepted resolutions. |
| `enforcement_mechanism_added_count` | integer | count | zero allowed | candidate gap resolutions | Count enforcement-mechanism resolutions. |
| `context_supplied_count` | integer | count | zero allowed | candidate gap resolutions | Count context-supplied resolutions. |
| `actor_count` | integer | count | zero allowed | event-storming intake | Count actor entries in `event_storming.actors`. |
| `command_count` | integer | count | zero allowed | event-storming intake | Count command entries in `event_storming.commands`. |
| `domain_event_count` | integer | count | zero allowed | event-storming intake | Count domain event entries in `event_storming.domain_events`. |
| `policy_count` | integer | count | zero allowed | event-storming intake | Count policy entries in `event_storming.policies`. |
| `constraint_count` | integer | count | zero allowed | event-storming intake | Count constraint entries in `event_storming.constraints`. |
| `topology_edge_count` | integer | count | zero allowed | candidate graph | Count all candidate graph topology edges. |
| `workflow_edge_count` | integer | count | zero allowed | candidate graph | Count workflow topology edges from the known workflow relation vocabulary. |
| `requirement_count` | integer | count | zero allowed | candidate graph | Count candidate node requirement records. |
| `acceptance_criteria_count` | integer | count | zero allowed | candidate graph | Count candidate node acceptance criteria records. |
| `remaining_blocker_count` | integer | count | zero allowed | repair session and gates | Count unresolved blocking findings. |
| `rerun_count` | integer | count | zero allowed | rerun requests and execution reports | Count repair rerun attempts. |
| `time_to_first_candidate_seconds` | number | seconds | null when not reached or unknown | timeline | Intake start to first candidate graph. |
| `time_to_first_materialization_seconds` | number | seconds | null when not reached or unknown | timeline | Intake start to first materialized preview. |
| `time_to_approval_ready_seconds` | number | seconds | null when not reached or unknown | timeline | Intake start to approval-ready repaired candidate. |
| `phase_dwell_seconds` | object | seconds map | empty map allowed | timeline | Dwell seconds by lifecycle phase. |
| `no_progress_rerun_count` | integer | count | zero allowed | rerun reports | Reruns that did not reduce blockers or gaps. |
| `last_progress_at` | string | RFC 3339 timestamp | null when unknown | timeline | Latest measurable progress event. |
| `stalled_phase` | string | lifecycle phase id | null when none/unknown | timeline | Current stalled phase. |
| `manual_handoff_count` | integer | count | zero allowed | Platform and operator handoff reports | Count explicit operator handoffs. |
| `operator_command_count` | integer | count | zero allowed | Platform execution reports | Count operator-run commands needed to advance. |
| `failed_gate_count` | integer | count | zero allowed | Platform and SpecGraph gate reports | Count gate failures or blocked gate reports. |
| `stale_ref_count` | integer | count | zero allowed | gate reports and import previews | Count stale source-ref failures. |
| `dry_run_count` | integer | count | zero allowed | Platform execution reports | Count dry-run phases. |
| `rerun_request_count` | integer | count | zero allowed | SpecSpace rerun request state | Count rerun requests. |
| `approval_attempt_count` | integer | count | zero allowed | approval intent and gate reports | Count approval attempts. |
| `candidate_approval_state` | enum | state | `not_reached` allowed | repair session and repaired handoff | Approval readiness lifecycle state. |
| `candidate_approval_intent_state` | enum | state | `not_reached` allowed | SpecSpace approval intent state | Approval intent lifecycle state. |
| `candidate_approval_decision_state` | enum | state | `not_reached` allowed | Platform approval execution report | Approval decision lifecycle state. |
| `platform_promotion_state` | enum | state | `not_reached` allowed | Platform approval/promotion reports | Platform promotion lifecycle state. |
| `promotion_path_count` | integer | count | zero allowed | promotion gate and approval decision | Count approved materialized paths. |
| `promotion_request_state` | enum | state | `not_reached` allowed | promotion request report | Promotion request handoff state. |
| `promotion_execution_state` | enum | state | `not_reached` allowed | promotion execution report | Controlled promotion execution state. |
| `review_status` | enum | state | `not_reached` allowed | review status report | One of `not_reached`, `open`, `merged`, `blocked`, `unknown`. |
| `review_pr_number` | integer | identifier | null when absent | review status report | Pull request number. |
| `review_merge_commit_sha` | string | SHA | null when absent | review status report | Merge commit SHA. |
| `read_model_publication_state` | enum | state | `not_reached` allowed | read-model publication report | Public read-model publication state. |
| `published_file_count` | integer | count | zero allowed | publication report and manifest | Count public-safe files. |
| `published_manifest_digest` | string | digest | null when absent | publication report and checksums | Public artifact manifest/checksum digest. |
| `candidate_node_count` | integer | count | zero allowed | candidate graph | Count material candidate graph nodes. |

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
| `git_review_active` | Controlled Git review opened or dry-run equivalent exists. |
| `read_model_publication_complete` | Public-safe read model publication completed. |
| `blocked` | A gate prevents forward progress. |

The derived state is a navigation aid. It must not hide raw blockers, counts, or
provenance.

## Formula Conventions

Rates should use `null` rather than `0` when the denominator is zero.

```text
answer_materialization_rate =
  closure_evidence_answer_count / accepted_answer_count

ontology_gap_resolution_rate =
  ontology_gap_resolved_count / ontology_gap_count_initial

candidate_gap_closure_rate =
  candidate_gap_resolved_count / candidate_gap_count_initial

promotion_path_density =
  promotion_path_count / candidate_node_count
```

`promotion_path_density` is diagnostic only. A higher value does not imply a
better candidate; it may indicate over-materialization.

`candidate_node_count` counts material candidate graph nodes in the active
candidate graph or repaired candidate preview. It excludes metadata-only wrapper
objects, summaries, and platform reports.

## Consistency Invariants

Implementations should validate these invariants before publishing or displaying
the report as a trustworthy metric artifact:

```text
0 <= blocking_question_count <= clarification_question_count
0 <= review_required_question_count <= clarification_question_count
0 <= accepted_answer_count <= answered_question_count
0 <= deferred_answer_count <= answered_question_count
0 <= invalid_answer_count <= answered_question_count
accepted_answer_count + invalid_answer_count + deferred_answer_count
  <= answered_question_count

0 <= materialized_answer_count <= accepted_answer_count
0 <= unmaterialized_answer_count <= accepted_answer_count
0 <= closure_evidence_answer_count <= accepted_answer_count
0 <= dismissed_answer_count <= accepted_answer_count
materialized_answer_count <= closure_evidence_answer_count
closure_evidence_answer_count + dismissed_answer_count + unmaterialized_answer_count
  <= accepted_answer_count

0 <= ontology_gap_resolved_count <= ontology_gap_count_initial
0 <= ontology_gap_unresolved_count <= ontology_gap_count_initial
ontology_gap_resolved_count + ontology_gap_unresolved_count
  <= ontology_gap_count_initial

0 <= candidate_gap_resolved_count <= candidate_gap_count_initial
0 <= candidate_gap_unresolved_count <= candidate_gap_count_initial
candidate_gap_resolved_count + candidate_gap_unresolved_count
  <= candidate_gap_count_initial
```

When an invariant fails, consumers should report `blocked` or `unknown` for the
affected derived state rather than silently normalizing the data.

The `<=` gap accounting invariants allow explicitly excluded or deferred items.
If an implementation uses closed partitions, it may strengthen those invariants
to equality and report excluded/deferred counts separately.

JSON Schema validation alone is not enough for conformance because JSON Schema
cannot express every cross-field numeric relationship. Conformance for this pack
is schema validation plus a separate invariant/policy validator. This repository
includes `scripts/validate_idea_maturity_examples.py` as a small executable
reference for bundled examples and produced report artifacts.

`scripts/metrics.py validate idea-maturity` is the stable CLI entrypoint for
sibling repositories. When called with `--output`, it emits an
`idea_maturity_metrics_validation_report` artifact whose schema is
`schemas/idea_maturity_metrics_validation_report.schema.json`.

## Policy Findings

Policy findings are not data invariants. The telemetry report should preserve
observed reality even when the workflow happened out of order. Consumers can
then flag policy violations without discarding the observation.

Examples:

```json
{
  "policy_findings": [
    {
      "kind": "out_of_order_publication",
      "severity": "high",
      "observed": {
        "read_model_publication_state": "published",
        "review_status": "not_reached"
      }
    },
    {
      "kind": "stale_answer_refs",
      "severity": "medium",
      "observed": {
        "stale_ref_count": 4,
        "accepted_answer_count": 6
      }
    }
  ]
}
```

Recommended policy checks:

- `read_model_publication_state: published` while `review_status` is not
  `merged`;
- `promotion_request_state: requested` while `candidate_approval_decision_state`
  is not `materialized`;
- `git_review_state` or `promotion_execution_state` indicates execution before
  promotion request evidence exists;
- `stale_ref_count > 0` after accepted answers were submitted.

## Diagnostic Playbook

The pack avoids universal thresholds, but recurring signals should still guide
operator action.

| Signal | Interpretation | Suggested action |
| --- | --- | --- |
| `accepted_answer_count > 0` and `closure_evidence_answer_count == 0` | Answers are collected but not changing candidate or closure state. | Inspect rerun materialization, rerun overlay, preview diff, and stale refs before approval. |
| `stale_ref_count > 0` | Drafts or answers target obsolete refs. | Ask the operator to rebase answers against the active candidate graph. |
| `manual_handoff_count` rises across runs | Product workflow still depends on operator glue. | Prioritize automation or make the ownership boundary explicit. |
| High `phase_dwell_seconds.repair_required` | Candidate may be stalled in repair. | Escalate to operator review or emit a blocked state with reason. |
| `ontology_gap_resolution_rate` is low | Terms are not grounded in the active ontology frame. | Review bind/alias/project-local term decisions. |
| `candidate_gap_closure_rate` is low | Product/spec answers are not closing blockers. | Inspect candidate gap targets and materialization evidence. |

## Privacy and Anti-Goodhart Constraints

Workflow friction metrics can become harmful if joined to human identities. The
report shape should minimize that risk.

```json
{
  "privacy_boundary": {
    "contains_human_operator_identity": false,
    "join_to_identity_allowed": false,
    "minimum_aggregation_subject": "candidate_run"
  }
}
```

Reports must not include human operator identifiers. Consumers should aggregate
friction by candidate, run, workspace class, or workflow class, not by person.

This boundary is also a negative declaration, not data-loss prevention. Producers
and consumers still need redaction, path review, secret scanning, and adapter
tests because identities can leak through free-form ids, workspace routes, source
artifact paths, or policy finding text.

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
    "candidate_node_count": 8,
    "promotion_path_count": 8,
    "manual_handoff_count": 0,
    "remaining_blocker_count": 0,
    "candidate_approval_state": "ready",
    "candidate_approval_intent_state": "not_reached",
    "candidate_approval_decision_state": "not_reached",
    "platform_promotion_state": "not_reached",
    "promotion_request_state": "not_reached",
    "promotion_execution_state": "not_reached",
    "review_status": "not_reached",
    "read_model_publication_state": "not_reached"
  },
  "groups": {
    "ontology_grounding": {
      "ontology_match_kind_counts": {
        "exact": 0,
        "normalized_exact": 1,
        "safe_inflection": 1,
        "safe_phrase_match": 0,
        "target_ref": 0,
        "aggregate_target": 0,
        "manual_bind": 0,
        "manual_alias": 0,
        "project_local_term": 9,
        "reject": 0,
        "defer": 0,
        "other": 0
      }
    },
    "candidate_repair": {
      "candidate_resolution_kind_counts": {
        "risk_accepted": 1,
        "enforcement_mechanism_added": 3,
        "context_supplied": 0,
        "gap_rejected": 0,
        "other": 0
      }
    },
    "candidate_structure_depth": {
      "actor_count": 2,
      "command_count": 3,
      "domain_event_count": 3,
      "policy_count": 1,
      "constraint_count": 2,
      "topology_edge_count": 11,
      "workflow_edge_count": 8,
      "requirement_count": 8,
      "acceptance_criteria_count": 8
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
    "may_merge_pull_request": false,
    "may_execute_prompt_agent": false,
    "may_publish_read_model": false
  },
  "privacy_boundary": {
    "contains_human_operator_identity": false,
    "join_to_identity_allowed": false,
    "minimum_aggregation_subject": "candidate_run"
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
