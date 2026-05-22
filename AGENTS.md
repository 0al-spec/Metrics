# Metrics Agent Instructions

## Scope

This root-level guide applies to repository-wide agent behavior and local
coordination for Metrics. For work under `SIB/`, use `SIB/AGENTS.md` for
LaTeX, bibliography, and document-editing guidance; those narrower instructions
take precedence for SIB paper files.

## 0AL Local Ops Logging

`0AL` is the Zero-trust Agents Layer workspace. In this checkout, `../.0al` is
the local operator tracker used to coordinate sibling repositories when that
directory is present.

For cross-repo observations, coordination tasks, blockers, or handoffs, write a
local ops entry through the sibling `../.0al` logging CLI when it is available:

```bash
../.0al/scripts/0al-log.py --project metrics --kind note --owner unclassified \
  --title "<short title>" \
  --text "<what happened, what is needed, and any suggested next action>"
```

Use `.0al` only for coordination. Canonical Metrics changes belong in this
repository. Do not edit `../.0al/tasks.md` or `../.0al/decisions.md` directly unless
the user explicitly asks for tracker maintenance, and never write secrets,
credentials, private keys, or machine-local tokens to `.0al`.
