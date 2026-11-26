import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

checks = [
    ("lop-12", "bai-6-tac-dong-cua-ai-den-doi-song-con-nguoi", ["hộp đen", "Ahiển", "Arư điêm"]),
    ("lop-12", "bai-7-ai-mo-ra-co-hoi-va-thach-thuc-cho-cac-nganh-nghe", ["Ddes tir", "Hạc hỏi"]),
    ("lop-12", "bai-8-quyen-con-nguoi-trong-ki-nguyen-ai", ["g lài só cng h ch gi", "bảo hiếm"]),
    ("lop-12", "bai-10-nguyen-li-co-ban-cua-hoc-may", ["Hat ượng", "bàt luàn", "Lam sach", "Biss cao"]),
    ("lop-12", "bai-14-hoan-chinh-san-pham", ["sử Aì co mể", "xuy tưân"]),
]

for b, les_id, keywords in checks:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        if les['id'] == les_id:
            html = les.get("html", "")
            clean = re.sub(r"<[^>]+>", "\n", html)
            print(f"=====================================")
            print(f"=== {b} / {les_id} ===")
            print(f"=====================================")
            for kw in keywords:
                for m in re.finditer(re.escape(kw), clean, re.IGNORECASE):
                    start = max(0, m.start() - 250)
                    end = min(len(clean), m.end() + 250)
                    print(f"--- Keyword: '{kw}' ---")
                    print(clean[start:end].strip())
                    print("----------------------")
