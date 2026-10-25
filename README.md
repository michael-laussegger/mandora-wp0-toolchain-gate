# Mandora WP-0 — Modeling Toolchain Gate v0.2

**Status: BLOCKED / IN PROGRESS. This package does not claim that LinkML semantic validation or JSON Schema generation has passed.**

## Purpose
Provide a fail-closed, auditable gate for selecting and validating the canonical modeling toolchain. The canonical model source remains the LinkML YAML under `model/`; generated schemas must not be hand-authored or represented as generated before a real generator run.

## What changed from v0.1
- Added an execution runbook for a network-enabled CI/build environment.
- Added an evidence-report template and an environment capture script.
- Clarified that a successful source lint or D1–D4 reference check does not pass the gate.
- Kept the generator fail-closed until a specific LinkML version and exact CLI invocation are verified.
- Added CI evidence upload instructions so a failed run remains diagnosable.

## Current known baseline
The previously inspected local environment had Python 3.13, PyYAML, `jsonschema`, and `pytest`; LinkML and its CLI were absent. No LinkML semantic validation or JSON Schema generation has been demonstrated. Recheck the environment when running this package; do not assume the prior baseline remains current.

## Run locally
```bash
python scripts/capture_environment.py
python scripts/validate_source_lint.py model/mandora-core-prototype.yaml
python tests/test_d1_d4_reference.py
```

The following commands are expected to remain blocked until the candidate toolchain is installed, pinned, and reviewed:
```bash
linkml-validate -s model/mandora-core-prototype.yaml
scripts/generate_schemas.sh
```

## Gate exit criteria
1. A candidate LinkML release is selected and tested in CI; Python and all dependencies are pinned.
2. A hash-checked lockfile is committed and install is performed with `pip --require-hashes`.
3. LinkML semantic validation passes against the canonical source.
4. JSON Schema Draft 2020-12 output is generated using the exact CLI of the pinned release.
5. Generated schema outputs are independently checked for the expected dialect and validated against positive and negative fixtures.
6. Regeneration is deterministic: a second run produces no unexplained diff.
7. D1–D4 tests pass, with app/database enforcement explicitly separated from schema-level checks.
8. CI logs, environment versions, generated artifacts, test results, and reviewed warnings are retained as evidence.

## Status discipline
Do not create `TOOLCHAIN_APPROVED` or mark the status as passed until the decision record is approved and all exit criteria have evidence. A green lint-only run is not a green WP-0 gate.
