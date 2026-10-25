#!/usr/bin/env bash
set -euo pipefail
# Intentionally fail closed until the selected LinkML version's generator syntax is verified.
if ! command -v gen-json-schema >/dev/null 2>&1; then
  echo "gen-json-schema CLI not found; WP-0 blocked" >&2
  exit 2
fi
if [[ ! -f TOOLCHAIN_APPROVED ]]; then
  echo "TOOLCHAIN_APPROVED marker absent; do not generate with an unapproved/unpinned toolchain" >&2
  exit 2
fi
# Replace this guard with the reviewed, version-specific generator invocation and per-class outputs.
echo "Generator invocation has not yet been approved for this LinkML version" >&2
exit 2
