#!/usr/bin/env python3
"""Capture basic toolchain facts without implying that the WP-0 gate passed."""
from __future__ import annotations
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def command_version(command: str) -> dict[str, object]:
    path = shutil.which(command)
    if not path:
        return {"available": False, "path": None, "version_output": None}
    try:
        result = subprocess.run([command, "--version"], text=True, capture_output=True, timeout=15)
        return {
            "available": True,
            "path": path,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except Exception as exc:  # environment evidence must capture failures, not hide them
        return {"available": True, "path": path, "error": repr(exc)}


packages = {}
for package in ("linkml", "jsonschema", "PyYAML", "pytest"):
    try:
        packages[package] = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        packages[package] = None

report = {
    "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    "python_version": sys.version,
    "python_executable": sys.executable,
    "platform": platform.platform(),
    "packages": packages,
    "commands": {
        name: command_version(name)
        for name in ("linkml", "linkml-validate", "gen-json-schema")
    },
    "interpretation": "Environment capture only; not a WP-0 pass result.",
}
output = Path("reports/environment-capture.json")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
print(f"Wrote {output}")
