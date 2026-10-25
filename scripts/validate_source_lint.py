#!/usr/bin/env python3
"""Basic source lint for the Mandora prototype; not a LinkML validator."""
import sys, yaml
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1] / "model" / "mandora-core-prototype.yaml")
d=yaml.safe_load(p.read_text())
known=set(d.get("types",{}))|set(d.get("enums",{}))|{"string","integer","float","boolean","uri","uriorcurie","date","datetime","time","decimal","ncname","object","json"}
errors=[]
for sn, spec in d.get("slots",{}).items():
 r=spec.get("range")
 if r and r not in known: errors.append(f"unknown range: {sn} -> {r}")
for cn, cls in d.get("classes",{}).items():
 for sn in cls.get("slots",[]):
  if sn not in d.get("slots",{}): errors.append(f"undeclared slot: {cn}.{sn}")
 for sn, usage in cls.get("slot_usage",{}).items():
  if "range" in usage and usage["range"] not in known: errors.append(f"unknown range: {cn}.{sn} -> {usage['range']}")
if errors:
 print("FAIL"); print("\n".join(errors)); sys.exit(1)
print("PASS: basic YAML/internal-reference lint only; run LinkML validator and generator separately.")
