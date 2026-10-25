# Mandora WP-0 Toolchain Gate — Status Report v0.2

**Status: BLOCKED / IN PROGRESS — not passed.**

## Evidence currently available
- Prior local inspection found Python 3.13, PyYAML, `jsonschema`, and `pytest` importable.
- The LinkML package and CLI were absent in that inspected environment.
- Source lint and D1–D4 reference assertions were previously reported to pass.
- This package adds a runbook, evidence template, and environment-capture script.

## Evidence not yet available
- A selected and tested LinkML release.
- Hash-checked lock file for the approved toolchain.
- Successful LinkML semantic validation.
- Actual generated JSON Schema Draft 2020-12 files.
- Independent generated-schema fixture tests.
- Reproducible second generation.
- CI run logs and reviewer approval.

## Required next action
Run the v0.2 package in a network-enabled CI/build environment following `docs/WP0_EXECUTION_RUNBOOK_v0.1.md`. Populate `reports/WP0_EVIDENCE_REPORT_TEMPLATE.md` with real output. Do not infer success from this package's existence or from basic YAML parsing.
