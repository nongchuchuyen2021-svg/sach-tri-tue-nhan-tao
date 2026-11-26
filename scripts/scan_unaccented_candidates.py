import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Common Vietnamese words that CamScanner often stripped tones from
# or swapped tones:
# co -> cơ / có
# ban / bán -> bản / bạn
# trinh -> trình
# hinh -> hình
# tinh -> tính / tình
# mo -> mô
# du -> dữ / du
# lieu -> liệu
# thong -> thông
# tin -> tin / tính
# hoc -> học
# tap -> tập
# he -> hệ
# thong -> thống
# ung -> ứng
# dung -> dụng
# thuc -> thực
# hanh -> hành
# bai -> bài
# gi -> gì
# tao -> tạo
# sinh -> sinh
# phat -> phát
# trien -> triển
# cong -> công
# cu -> cụ
# ngu -> ngữ
# lon -> lớn

target_unaccented = [
    "co", "trinh", "hinh", "mo", "lieu", "thong", "tap", "ung", "thuc",
    "trien", "cu", "ngu", "lon", "soan", "nghin", "góm", "triến", "huán", "xóá",
    "prompi", "prompl", "nhồm", "tuê", "đữ", "loán", "lón", "gìảm", "họạ"
]

print("=== SEARCHING SUSPICIOUS UNACCENTED / DROPPED ACCENT TOKENS ===")
for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        clean = re.sub(r"<[^>]+>", " ", html)
        for w in target_unaccented:
            # check word boundary
            for m in re.finditer(rf"\b{w}\b", clean, re.IGNORECASE):
                # check context
                s = max(0, m.start() - 30)
                e = min(len(clean), m.end() + 30)
                ctx = clean[s:e].replace('\n', ' ')
                # exclude if it's english code like 'def', 'import', etc.
                if not re.search(r"\b(def|class|import|return|from|plt|fig)\b", ctx):
                    print(f"[{b}/{les['id']}] '{m.group(0)}': ...{ctx}...")
