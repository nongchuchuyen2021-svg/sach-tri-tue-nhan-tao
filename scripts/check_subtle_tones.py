import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

patterns = [
    r"\bkết quà\b",
    r"\btinh xác định\b",
    r"\bthiếu tinh\b",
    r"\bchinh xác\b",
    r"\bchính xac\b",
    r"\brỏ ràng\b",
    r"\bmổi\b",
    r"\blổi\b",
    r"\bchử\b",
    r"\bhảy\b",
    r"\bphài\b",
    r"\btừ khoá\b",
    r"\bngử cảnh\b",
    r"\bngữ cánh\b",
]

regex = re.compile("|".join(patterns), re.IGNORECASE)

for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        clean = re.sub(r"<[^>]+>", " ", html)
        matches = list(regex.finditer(clean))
        if matches:
            for m in matches:
                start = max(0, m.start() - 25)
                end = min(len(clean), m.end() + 25)
                print(f"[{b} - {les['id']}] '{m.group(0)}': ...{clean[start:end].strip()}...")
