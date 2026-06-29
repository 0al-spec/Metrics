# Metrics Validator Contract

This document defines the stable local contract for machine-readable metric-pack
validation. Sibling repositories should call the CLI instead of copying Metrics
validation logic.

## Idea Maturity Validator

Stable entrypoint:

```bash
python3 scripts/metrics.py validate idea-maturity \
  path/to/idea_maturity_metrics_report.json \
  --output path/to/idea_maturity_metrics_validation_report.json
```

Default self-test:

```bash
python3 scripts/metrics.py validate idea-maturity
python3 scripts/validate_idea_maturity_examples.py
```

The validator accepts one or more `idea_maturity_metrics_report` artifacts and
can emit one structured validation report for downstream consumers.

## Contract Identifiers

| Field | Value |
| --- | --- |
| Metric pack | `idea_to_spec_maturity` |
| Report artifact kind | `idea_maturity_metrics_report` |
| Validation artifact kind | `idea_maturity_metrics_validation_report` |
| Validator id | `metrics.idea_maturity_metrics.validator.v0.1` |
| Validator version | `0.1.0` |
| Report schema | `schemas/idea_maturity_metrics_report.schema.json` |
| Validation report schema | `schemas/idea_maturity_metrics_validation_report.schema.json` |

## Compatibility Policy

Policy id: `additive_v1`.

Rules:

- Required top-level fields, authority flags, privacy flags, and closed enum
  values are stable within validator major version `v0`.
- New optional top-level fields may be added.
- `summary` only accepts known metric ids plus `x-*` extension keys.
- Closed count maps only accept declared keys plus `x-*` extension keys.
- Consumers must ignore unknown `x-*` fields unless they explicitly opt in.
- Deprecated fields stay readable for at least one validator minor release before
  removal from bundled examples.
- Any authority-expanding flag must be literal `false`; truthy values such as
  `true`, `1`, or `"true"` are invalid.
- A validation report with `summary.status: failed` is a valid validation
  artifact when its counts and diagnostics are internally consistent.

## Authority Boundary

Metrics validation is report-only. It must not:

- mutate canonical specs;
- write Ontology packages;
- accept Ontology terms;
- create branches or commits;
- open or merge pull requests;
- publish read models;
- execute prompt agents.

Those operations belong to explicit downstream workflows and gates.
