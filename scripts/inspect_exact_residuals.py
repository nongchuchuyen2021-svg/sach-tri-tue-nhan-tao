import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

patterns = [
    "ảnhh", "bạng", "llên", "hoặt", "đăn", "Khới", "ngọi", "lưyng", "hoậc", "trỏi", "bảl", "câ nhân",
    "oông", "nên/khỏng", "ănh", "rèng", "lrách", "hồm", "cề trế", "cárt", "niển", "roir",
    "tirin", "dàu", "mộn", "PHẨ", "chên", "nhồm", "lệu", "triên", "tuê", "kiem",
    "Generato", "AIl", "trớc", "miội", "Mội thoai", "Buot", "cuông"
]

for b in ["10", "11", "12"]:
    p = ROOT / "data" / f"lessons-lop-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        summary = les.get("summary", "")
        for pat in patterns:
            if pat in html or pat in summary:
                # find context in html or summary
                for source_name, text in [("html", html), ("summary", summary)]:
                    if pat in text:
                        idx = text.find(pat)
                        s = max(0, idx - 40)
                        e = min(len(text), idx + len(pat) + 60)
                        print(f"[{b}/{les['id']} ({source_name})] '{pat}': ...{text[s:e].replace(chr(10), ' ')}...")
