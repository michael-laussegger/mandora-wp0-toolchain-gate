# Decision Record — WP-0 Modeling Toolchain Gate v0.2

**Status: PROPOSED / OPEN**

## Context
The canonical modeling source needs a reproducible semantic-validation and schema-generation toolchain. The local environment previously inspected did not include LinkML. Selecting a version without running it against the actual model would create unsupported confidence.

## Decision
Do not approve a LinkML version or generation command in this revision. Select the candidate in a network-enabled build environment, verify its actual CLI and output dialect, generate a hash-checked lock file, and attach the complete evidence bundle before approval.

## Consequences
- WP-0 remains blocked.
- No generated schema is published as though it were tool output.
- WP-1 remains a draft and must not be treated as production-ready.
- A future approval must identify the exact model revision, toolchain lock hash, CI run, and reviewer.

## Approval
No approval recorded.
