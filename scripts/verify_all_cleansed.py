import json
import re
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# List of patterns that must NOT appear anywhere in the codebase
forbidden_patterns = [
    (r"\bkhông vl dụ\b", "không vl dụ"),
    (r"\bvl dụ\b", "vl dụ"),
    (r"\bv1 dụ\b", "v1 dụ"),
    (r"\bcông củ AI\b", "công củ AI"),
    (r"\btạo ra.*công củ\b", "công củ"),
    (r"\bA/\s*lạo sinh\b", "A/ lạo sinh"),
    (r"\bAi thô hệ trước\b", "Ai thô hệ trước"),
    (r"\bkết quà\b", "kết quà"),
    (r"\bKết quà\b", "Kết quà"),
    (r"\bhiệu quà\b", "hiệu quà"),
    (r"\bchinh xác\b", "chinh xác"),
    (r"\bChinh xác\b", "Chinh xác"),
    (r"\bthiếu tinh\b", "thiếu tinh"),
    (r"\btinh huống\b", "tinh huống"),
    (r"\bTinh huống\b", "Tinh huống"),
    (r"\btinh huồng\b", "tinh huồng"),
    (r"\btinh huóng\b", "tinh huóng"),
    (r"\bngữ cánh\b", "ngữ cánh"),
    (r"\btừ khoá\b", "từ khoá"),
    (r"\bcuối khoá\b", "cuối khoá"),
    (r"\bphài\b", "phài"),
    (r"\bhảy trả lời\b", "hảy trả lời"),
    (r"\bcàu hỏi\b", "càu hỏi"),
    (r"\bcàu trả lời\b", "càu trả lời"),
    (r"\byêu càu\b", "yêu càu"),
    (r"\bcâu hói\b", "câu hói"),
    (r"\btrà lời\b", "trà lời"),
    (r"\bcài tiến\b", "cài tiến"),
    (r"\bhiều lầm\b", "hiều lầm"),
    (r"\bHiều dúng\b", "Hiều dúng"),
    (r"\bHIỀU ĐÙNG\b", "HIỀU ĐÙNG"),
    (r"\bxày ra\b", "xày ra"),
    (r"\bđàm bào\b", "đàm bào"),
    (r"\bchia sẽ\b", "chia sẽ"),
    (r"\bphản hỏi\b", "phản hỏi"),
    (r"\blàm gi\b", "làm gi"),
    (r"\blà gi\b", "là gi"),
    (r"\bhỏi của khác\b", "hỏi của khác"),
    (r"\bthong_tin_tio_kiem\b", "thong_tin_tio_kiem"),
    (r"\b5ố giờ hoc\b", "5ố giờ hoc"),
    (r"\bđưa ra\s*kết quà\b", "kết quà"),
    (r"\bkhông chi tồn\b", "không chi tồn"),
]

files_to_check = [
    ROOT / "data" / "books.json",
    ROOT / "data" / "lessons-lop-10.json",
    ROOT / "data" / "lessons-lop-11.json",
    ROOT / "data" / "lessons-lop-12.json",
    ROOT / "data" / "search-lop-10.json",
    ROOT / "data" / "search-lop-11.json",
    ROOT / "data" / "search-lop-12.json",
    ROOT / "index.html",
    ROOT / "reader.html",
] + [Path(p) for p in glob.glob(str(ROOT / "lessons" / "*" / "*.html"))]

found_issues = 0

for fp in files_to_check:
    text = fp.read_text(encoding="utf-8")
    for pat, label in forbidden_patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            found_issues += 1
            s = max(0, m.start() - 25)
            e = min(len(text), m.end() + 25)
            ctx = text[s:e].replace('\n', ' ')
            print(f"[FAIL] {fp.relative_to(ROOT)}: '{label}' -> ...{ctx}...")

if found_issues == 0:
    print(f"[SUCCESS] Checked {len(files_to_check)} files: ZERO forbidden errors found!")
else:
    print(f"[WARNING] Found {found_issues} errors that still need attention!")
