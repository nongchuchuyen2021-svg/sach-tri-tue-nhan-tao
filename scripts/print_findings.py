import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "scripts" / "lop11_scan_findings.json", encoding="utf-8") as f:
    findings = json.load(f)

print(f"Total findings: {len(findings)}\n")

for i, it in enumerate(findings):
    print(f"[{i+1}] {it['file']}:{it['line_no']} | {it['desc']}")
    print(f"    Line: {it['text']}\n")
