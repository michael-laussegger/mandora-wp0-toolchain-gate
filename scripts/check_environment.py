from __future__ import annotations
import importlib.util
import shutil
import sys

print(f"Python: {sys.version.split()[0]}")
for module in ("yaml", "jsonschema", "pytest", "linkml"):
    print(f"Python module {module}: {'available' if importlib.util.find_spec(module) else 'MISSING'}")
for command in ("linkml-validate", "gen-json-schema"):
    print(f"CLI {command}: {shutil.which(command) or 'MISSING'}")
if not importlib.util.find_spec("linkml") or not shutil.which("linkml-validate") or not shutil.which("gen-json-schema"):
    print("RESULT: BLOCKED — LinkML validation/generation cannot be claimed in this environment.")
    raise SystemExit(2)
print("RESULT: LinkML commands detected; this check alone does not prove model validity.")
