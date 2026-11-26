import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

patterns = [
    "bạng", "đăn", "ănh", "cárt", "niển", "roir", "tirin", "dàu", "PHẨ", "chên", "tuê", "kiem",
    "Generato", "AIl", "tỉn", "trạn"
]

for b in ["10", "11", "12"]:
    p = ROOT / "data" / f"lessons-lop-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        summary = les.get("summary", "")
        for pat in patterns:
            for src_name, text in [("html", html), ("summary", summary)]:
                if pat in text:
                    for line in text.splitlines():
                        if pat in line:
                            print(f"[{b}/{les['id']} ({src_name})] '{pat}': {line.strip()[:110]}")
