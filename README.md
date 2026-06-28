# Metrics

Metrics for AI-Driven Development under CC BY 4.0 license.

## Papers

1. **[SIB - Specification-Implementation Balance](SIB/metrics.pdf)** - A non-normative diagnostic framework for observing the balance between specification (intent), implementation (code), and AI inference cost in modern AI-assisted software development. Rather than proposing optimization targets or productivity metrics, the framework is designed to expose structural and economic shifts in the process of intent-to-implementation conversion.
2. **[SIB Full Metrics](SIB_FULL/sib_full_metrics.pdf)** - An extended draft framework covering pre-implementation, process, structural, and retrospective defect metrics.
3. **[SIB Economic Observability](SIB_ECONOMIC_OBSERVABILITY/sib_economic_observability.pdf)** - A non-normative economic observability lens for inference, verification, build cost, and structural cost proxies.

## Metric Packs

See [METRIC_PACKS.md](METRIC_PACKS.md) for the plugin-style metric pack model,
authority states, run artifact sketches, and interpretation guardrails used when
SpecGraph consumes these metrics as read-only diagnostic overlays.

The draft [Idea-to-Spec Lifecycle Telemetry](IDEA_MATURITY_METRICS.md) pack
defines objective observability signals for product idea-to-spec workflows,
including clarification load, answer materialization, ontology grounding,
candidate repair, temporal progress, workflow friction, approval readiness, and
read-model publication state. Its initial machine-readable report contract lives
in [schemas/idea_maturity_metrics_report.schema.json](schemas/idea_maturity_metrics_report.schema.json).
Example report invariants can be checked without third-party dependencies:

```bash
python3 scripts/validate_idea_maturity_examples.py
```

## Building

Each paper is in its own directory with a Makefile:

```bash
cd SIB
make build   # Compile to PDF
make view    # Compile and open PDF
```

## License

CC BY 4.0 (Creative Commons Attribution 4.0 International)
