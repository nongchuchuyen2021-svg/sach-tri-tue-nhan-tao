import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        clean = re.sub(r"<[^>]+>", " ", html)
        for m in re.finditer(r"\bvl\b|\bvl\w+", clean, re.I):
            start = max(0, m.start() - 30)
            end = min(len(clean), m.end() + 30)
            print(f"[{b} - {les['id']}] Found '{m.group(0)}': ...{clean[start:end].strip()}...")
