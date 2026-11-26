import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Search for words with mixed or suspicious characters across all 3 books
patterns = [
    r"\bvl\s+dụ\b",
    r"\b[vV][l1I|iìỉĩí]\s+d[ụuự]\b",
    r"\b[vV][l1I|iìỉĩí]\s+sao\b",
    r"\bvắn\s+đ[ểẻề]\b",
    r"\b[dđ][ãỡữũ]\s+liệu\b",
    r"\blóm\s+tắt\b",
    r"\btim\s+ki[ếe]m\b",
    r"\bch[ìi]nh\s+sửa\b",
    r"\btinh\s+ch[ìi]nh\b",
    r"\bbi[ếể]u\s+đ[òồ]\b",
    r"\bgi[àa]\s+sử\b",
    r"\btu\s+duy\b",
    r"\bthiên\s+nhi[ềe]n\b",
    r"\bkhi\s+thải\b",
    r"\bto[àa]\s+nhiệt\b",
    r"\btiêu\s+t[ồo]n\b",
    r"\bnưóc\b",
    r"\bkhung\s+cánh\b",
    r"\bảnh\s+góc\b",
    r"\bgiải\s+thich\b",
    r"\bđặc\s+bi[êe]t\b",
    r"\bh[ọo]p\s+thoại\b",
    r"\bd[ủu]\s+có\b",
    r"\bd[ủu]\s+là\b",
    r"\bd[ủu]\s+cho\b",
    r"\bthông\s+tín\b",
    r"\bk[ĩiI]\s+n[ăaâ][nngg]\b",
    r"\bh[oọ]c\s+m[áa]y\b",
]

regex = re.compile("|".join(patterns), re.IGNORECASE)

found_total = 0
for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    b_matches = 0
    for les in data:
        html = les.get("html", "")
        clean = re.sub(r"<[^>]+>", " ", html)
        for m in regex.finditer(clean):
            b_matches += 1
            start = max(0, m.start() - 25)
            end = min(len(clean), m.end() + 25)
            # print snippet
            if b_matches <= 15 or 'vl' in m.group(0).lower():
                print(f"[{b} - {les['id']}]: '{m.group(0)}' in: ...{clean[start:end].strip()}...")
    print(f"Total in {b}: {b_matches}")
    found_total += b_matches

print(f"\nGRAND TOTAL MATCHES: {found_total}")
