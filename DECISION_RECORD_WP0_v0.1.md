# Decision Record — WP-0 Toolchain and Reproducible Generation v0.1

**Status:** Proposed; no toolchain approval implied.

## Decision to be made
Whether LinkML is accepted as the canonical source of model definitions and which exact runtime/tool versions and generation commands become the supported build contract.

## Required evidence
1. LinkML source validation succeeds on the Mandora prototype.
2. Generated JSON Schemas meet Draft 2020-12 expectations and preserve required/conditional constraints where expressible.
3. Cross-record rules are explicitly assigned to domain validation and tested separately.
4. A clean build reproduces committed artifacts.
5. Tool versions are locked with hashes and documented upgrade procedure.

## Current result
Not decided. The current execution environment lacks LinkML; local lint and reference tests are insufficient to approve the toolchain.

## Consequence
No generated schema is represented as an actual LinkML-generated artifact in this package. WP-0 remains blocked until evidence is attached and reviewed.
