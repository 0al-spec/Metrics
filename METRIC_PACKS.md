# Metric Packs and Interpretation Contract

This repository should be treated as a source of metric methods and metric
packs, not as a single hard-coded scoring model.

SpecGraph can consume these methods as read-only interpretive plugins over its
core state:

```text
SpecGraph core state
  -> Metric Pack `sib` (SIB)
  -> Metric Pack `sib_full` (SIB Full Metrics)
  -> Metric Pack `sib_economic_observability` (Economic Observability)
  -> future `metric_pack_id` entries for trace/review/security packs
  -> metric artifacts, dashboard overlays, gaps, and proposal pressure
```

Metric packs may produce findings, gaps, overlays, and proposal pressure. They
must not directly mutate canonical graph state or enforce policy without a
separate reviewable proposal and operational adapter.

## Pack Registry

`metric_pack_id` is the canonical machine identifier. Display names and source
paths are descriptive metadata and should not be used as stable identifiers.

| `metric_pack_id` | Display name | Source path |
| --- | --- | --- |
| `sib` | SIB | `SIB/metrics.tex` |
| `sib_full` | SIB Full Metrics | `SIB_FULL/sib_full_metrics.tex` |
| `sib_economic_observability` | SIB Economic Observability | `SIB_ECONOMIC_OBSERVABILITY/sib_economic_observability.tex` |
| `idea_to_spec_maturity` | Idea-to-Spec Lifecycle Telemetry | `IDEA_MATURITY_METRICS.md` |

## Pack Layers

1. **Metric source**: human-readable origin and provenance, such as a paper
   directory, a package, a local checkout, or an external reference.
2. **Metric pack contract**: machine-readable declaration of available metrics,
   required inputs, authority state, and output shape.
3. **Metric adapter**: optional code or rules that map SpecGraph artifacts into
   the inputs expected by the pack.
4. **Metric run artifact**: concrete computation result for one input snapshot,
   including values, gaps, provenance, and non-computable states.
5. **Metric projection**: viewer/dashboard overlay that displays values and
   gaps without turning draft metrics into policy.

## Authority States

Metric packs should declare one of these states:

- `draft_reference`: useful method or paper draft, not operational scoring.
- `validated_reference`: stable reference with reviewed definitions.
- `operational`: has a reviewed adapter, provenance, and run artifacts.
- `deprecated`: retained for compatibility or historical comparison only.

## Contract Sketch

```json
{
  "metric_pack_id": "sib_full",
  "authority_state": "draft_reference",
  "source": {
    "repository": "0al-spec/Metrics",
    "path": "SIB_FULL/sib_full_metrics.tex"
  },
  "inputs": [
    "spec_graph",
    "trace_plane",
    "implementation_work",
    "review_feedback"
  ],
  "metrics": [
    {
      "metric_id": "sib_eff_star",
      "label": "Effective Pre-Implementation SIB",
      "kind": "diagnostic",
      "phase": "pre_implementation",
      "requires": [
        "intent_atoms",
        "spec_verifiability_coverage",
        "expected_implementation_potential"
      ]
    }
  ]
}
```

## Run Artifact Sketch

```json
{
  "metric_pack_id": "sib_full",
  "run_id": "2026-04-30T20:00:00Z",
  "computed_at": "2026-04-30T20:00:00Z",
  "input_snapshot": "specgraph-main@example",
  "values": [],
  "gaps": [
    {
      "metric_id": "sib_eff_star",
      "status": "not_computable",
      "missing_inputs": ["intent_atoms"]
    }
  ]
}
```

## Interpretation Contract

These rules apply to all metric packs in this repository.

Machine-readable validators should publish a small compatibility contract next
to their schemas and examples. For `idea_to_spec_maturity`, the current
contract is [VALIDATOR_CONTRACT.md](VALIDATOR_CONTRACT.md), and downstream
repositories should call `scripts/metrics.py` instead of copying validation
logic.

### 1. Intended Use

Metrics are diagnostic observability signals. They are intended for drift
analysis, anomaly detection, graph self-diagnosis, and economic transparency.
They are not intended for ranking people, teams, or projects.

Absolute values are secondary. Deltas, drift velocity, distribution shifts, and
trend reversals are the primary interpretation mode.

### 2. Agent-Centric Measurement

The primary measurement subject is the agentic workflow, not individual human
performance. Useful signals include attempts, rollbacks, failed runs, token and
tool footprint, stabilization time, graph impact radius, and review feedback
loops.

This reduces the Goodhart risk compared with people-oriented productivity
metrics, but it does not remove the need for explicit non-normative guardrails.

### 3. Versioned Cost Provenance

Economic metrics must preserve their pricing and execution context:

- pricing surface identifier
- model and provider versions
- tool versions
- currency or unit convention
- time window
- whether each quantity is observed spend or a derived proxy

This makes inference cost useful for transparent cost accounting without
confusing provider-price drift with structural project drift.

### 4. Calibration Profiles

Weights such as `alpha`, `beta`, `gamma`, `delta`, `lambda`, and `kappa` are
calibration parameters, not universal constants.

Metric packs should prefer named calibration profiles, for example `default`,
`conservative`, `cost_sensitive`, or `latency_sensitive`. Future empirical work
may define reference coefficients for recurring project classes.

### 5. Value-Weighted Intent Future Layer

Intent value is a future layer, not a prerequisite for the current diagnostic
packs. Once product telemetry connects intent atoms to shipped features and
user-visible outcomes, packs may introduce value-weighted variants such as
value-weighted SIB, value-weighted false progress mass, or value-weighted review
pressure.

Until then, value should not be guessed into core formulas.

### 6. Graph-Based Defect Roots

Linear defect trajectories are acceptable as an MVP projection, especially when
changes land through a main-branch sequence.

SpecGraph should eventually support graph-native retrospective analysis:
multiple root nodes, weighted influence paths, premise paths, and branch
contribution. Defect-root metrics should therefore remain compatible with both
linear and multi-root graph interpretations.

## Candidate Packs

- `sib`: compact Specification--Implementation Balance baseline.
- `sib_full`: broader research/draft diagnostic pack covering pre-implementation,
  process, structural, and retrospective defect metrics.
- `sib_economic_observability`: economic lens over pricing surfaces, inference
  footprint, verification cost, build cost, and structural cost proxies.
- `idea_to_spec_maturity`: 0AL-specific product idea-to-spec lifecycle telemetry
  over clarification load, answer materialization, ontology grounding, candidate
  repair, temporal progress, workflow friction, promotion readiness, and
  publication completion.
