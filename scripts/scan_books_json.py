import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "data" / "books.json", "r", encoding="utf-8") as f:
    c = f.read()

patterns = [
    r"\bvl\b", r"\bvl dụ\b", r"\bchinh xác\b", r"\bquà\b", r"\btinh\b", r"\bhiều\b", r"\bđùng\b",
    r"\bcàu\b", r"\bhói\b", r"\btrà\b", r"\bcài\b", r"\bhảy\b", r"\bphài\b", r"\bngữ cánh\b",
    r"\btừ khoá\b", r"\bcuối khoá\b", r"\bxày ra\b", r"\bchia sẽ\b", r"\bđàm bào\b", r"\bbào vệ\b",
    r"\bmội trường\b", r"\bkhời động\b", r"\bKhời động\b", r"\bthay đồi\b", r"\btinh huống\b",
    r"\btinh huồng\b", r"\btinh huóng\b", r"\btinh trạng\b", r"\bthiếu tinh\b", r"\bgi\b",
    r"\btao ra\b", r"\bcông củ\b", r"\blạo sinh\b", r"\bthô hệ\b"
]

for pat in patterns:
    for m in re.finditer(pat, c, re.IGNORECASE):
        s = max(0, m.start() - 30)
        e = min(len(c), m.end() + 30)
        snippet = c[s:e].replace("\n", " ")
        print(f"[books.json] '{m.group(0)}': ...{snippet}...")
