import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CORRECTIONS_PASS2 = [
    (r"\bHóá\b", "Hóa"),
    (r"\bhóá\b", "hóa"),
    (r"\bHÓÁ\b", "HÓA"),
    (r"\bphủ hợp\b", "phù hợp"),
    (r"\btội thiểu\b", "tối thiểu"),
    (r"\blạo video\b", "tạo video"),
    (r"\blạo ảnh\b", "tạo ảnh"),
    (r"\blạo hinh\b", "tạo hình"),
    (r"\bCông bàng\b", "Công bằng"),
    (r"\bcông bàng\b", "công bằng"),
    (r"\bbàng tin\b", "bảng tin"),
    (r"\bdạng bàng\b", "dạng bảng"),
    (r"\bmột bàng\b", "một bảng"),
    (r"\bkhung cánh\b", "khung cảnh"),
    (r"\bảnh góc\b", "ảnh gốc"),
    (r"\bso với lạo\b", "so với tạo"),
    (r"\bthời gian lạo\b", "thời gian tạo"),
]

for grade in ["lop-10", "lop-11", "lop-12"]:
    json_path = ROOT / "data" / f"lessons-{grade}.json"
    html_dir = ROOT / "lessons" / grade
    data = json.load(open(json_path, encoding="utf-8"))
    
    for les in data:
        html = les.get("html", "")
        for pat, rep in CORRECTIONS_PASS2:
            html = re.sub(pat, rep, html)
        les["html"] = html
        
        # HTML file
        lid = les["id"]
        html_file = html_dir / f"{lid}.html"
        if html_file.exists():
            f_content = html_file.read_text(encoding="utf-8")
            for pat, rep in CORRECTIONS_PASS2:
                f_content = re.sub(pat, rep, f_content)
            html_file.write_text(f_content, encoding="utf-8")
            
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Re-index search
    search_idx = []
    for les in data:
        clean_text = re.sub(r"<[^>]+>", " ", les.get("html", ""))
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        search_idx.append({
            "id": les["id"],
            "title": les.get("title", ""),
            "group": les.get("group", ""),
            "startPage": les.get("startPage", 1),
            "content": clean_text[:4000]
        })
    search_path = ROOT / "data" / f"search-{grade}.json"
    with open(search_path, "w", encoding="utf-8") as f:
        json.dump(search_idx, f, ensure_ascii=False, indent=2)

print("Pass 2 corrections applied successfully!")
