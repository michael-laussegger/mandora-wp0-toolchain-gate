# WP-0 Execution Runbook v0.1

## Objective
Determine whether the candidate LinkML toolchain can validate the canonical model and reproducibly generate the target JSON Schema contracts.

## Preconditions
- Use an isolated build environment with internet access or an approved internal package mirror.
- Begin from a clean checkout of this package.
- Do not edit the canonical model to silence a toolchain error without a reviewed change.
- Do not add generated files until they have been produced by the pinned generator.

## Procedure
1. Capture the Python and platform versions using `python scripts/capture_environment.py`.
2. Select a candidate LinkML version. Record the version, Python compatibility, source URL, and rationale in the WP-0 decision record.
3. Install the candidate in a disposable environment and record `python --version`, `python -m pip --version`, `linkml --version` (if supported), `linkml-validate --help`, and `gen-json-schema --help`.
4. Confirm the exact validation and generation commands from that installed version's help output. Do not infer command syntax from a different release.
5. Create a fully pinned, hash-checked lock file from the tested environment. Verify a clean install using `python -m pip install --require-hashes -r requirements-lock.txt`.
6. Run LinkML semantic validation against `model/mandora-core-prototype.yaml`; save complete stdout/stderr and exit status.
7. Generate schemas for every class approved for publication. Record the exact command and output paths. Confirm each generated schema declares JSON Schema Draft 2020-12.
8. Validate generated schemas independently with a JSON Schema Draft 2020-12 validator. Run positive and negative fixtures; distinguish schema tests from cross-record/domain/database tests.
9. Run generation twice from clean output directories. Compare artifacts byte-for-byte or with a documented canonicalization procedure. Explain any nondeterministic metadata.
10. Run the D1–D4 reference tests and source linter.
11. Complete `reports/WP0_EVIDENCE_REPORT_TEMPLATE.md`, including failed checks and unresolved warnings.
12. Review the evidence and update the decision record. Only then may the gate be marked passed.

## Failure handling
- If LinkML rejects the model, retain the full error and propose the smallest model correction in a separate reviewed change.
- If the generator cannot produce the target dialect, record the mismatch and evaluate supported options; do not relabel another dialect as Draft 2020-12.
- If output changes between runs, gate release until the difference is explained and controlled.
- If cross-record rules cannot be represented in generated schemas, document their enforcement layer and add domain-level tests rather than claiming schema coverage.

## Required evidence bundle
- Environment capture
- Lock file and install log
- LinkML validation log
- Generator help output and exact generation command
- Generated schemas
- Independent schema-validation report
- Positive/negative fixture results
- Reproducibility diff
- D1–D4/source-lint test results
- Completed evidence report and reviewed decision record
