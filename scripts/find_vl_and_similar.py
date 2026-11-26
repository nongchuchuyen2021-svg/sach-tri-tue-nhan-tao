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
        
        # Check for 'vl' or 'v1' or 'vI' or 'vỉ' or 'vĩ'
        matches = list(re.finditer(r"\b(v[l1I|] dụ|vỉ du|vỉ dụ|vì dụ|vĩ dụ|ví du|v[l1I|]\s+\w+)\b", clean, re.IGNORECASE))
        if matches:
            print(f"[{b} - {les['id']}]:")
            for m in matches:
                start = max(0, m.start() - 25)
                end = min(len(clean), m.end() + 25)
                print(f"   >>> {clean[start:end].strip()}")
