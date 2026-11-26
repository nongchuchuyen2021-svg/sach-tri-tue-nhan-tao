import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LESSONS_DIR = ROOT / "lessons"

EXACT_REPLACEMENTS = [
    # bai-1
    ("biện luận số nghiệm của phương trình theo A:", "biện luận số nghiệm của phương trình theo Δ:"),
    ("theo A:", "theo Δ:"),
    
    # bai-2
    ("(khoa : giá trị)", "(khóa : giá trị)"),
    ("khoa : giá trị", "khóa : giá trị"),
    
    # bai-3
    ("một nhành của NLP", "một nhánh của NLP"),
    ("nhành của NLP", "nhánh của NLP"),
    
    # bai-6
    ("nhỏmTự", "nhóm. Tự"),
    ("nhỏmTự động", "nhóm đã biết trước. Tự động"),
    ("vào các nhỏmTự", "vào các nhóm. Tự"),
    ("vào càc nhóm", "vào các nhóm"),
    ("càc nhóm", "các nhóm"),
    ("là quả trình sắp xếp", "là quá trình sắp xếp"),
    ("quả trình sắp xếp", "quá trình sắp xếp"),
    ("DỨ LIỆU", "DỮ LIỆU"),
    
    # bai-7
    ("Vấn để: Quá trình", "Vấn đề: Quá trình"),
    ("Vấn để:", "Vấn đề:"),
    
    # bai-8
    ("Rõ rảng, câu trả lời", "Rõ ràng, câu trả lời"),
    ("Rõ rảng,", "Rõ ràng,"),
    ("Rõ rảng", "Rõ ràng"),
    ("bệnh nhán", "bệnh nhân"),
    ("tuân thù các quy tắc", "tuân thủ các quy tắc"),
    ("tuân thù", "tuân thủ"),
    ("<p class=\"lesson-p\">ENGUSH</p>", "<p class=\"lesson-p\">ENGLISH</p>"),
    ("ENGUSH", "ENGLISH"),
    
    # bai-9
    ("hoặc quả trình.", "hoặc quá trình."),
    ("hoặc quả trình", "hoặc quá trình"),
    
    # bai-10
    ("<p class=\"lesson-p\">Vân đề</p>", "<p class=\"lesson-p\">Vấn đề</p>"),
    ("Vân đề", "Vấn đề"),
    
    # bai-12
    ("cung cấp thêm promct mô tả", "cung cấp thêm prompt mô tả"),
    ("promct mô tả", "prompt mô tả"),
    ("promct", "prompt"),
    ("chỉ thêm chuyến động", "chỉ thêm chuyển động"),
    ("chuyến động vào ảnh", "chuyển động vào ảnh"),
    ("tính toán it hơn", "tính toán ít hơn"),
    ("it hơn so với chi dùng", "ít hơn so với chỉ dùng"),
    ("so với chi dùng", "so với chỉ dùng"),
    ("chi dùng prompt", "chỉ dùng prompt"),
    ("em cùng có thể cung cấp", "em cũng có thể cung cấp"),
    ("em cùng có thể", "em cũng có thể"),
    
    # bai-13
    ("sản phẩm minh•  họạ", "sản phẩm minh họa"),
    ("minh•  họạ", "minh họa"),
    ("minh• họạ", "minh họa"),
    
    # bang giai thich thuat ngu
    ("học tàp", "học tập"),
    ("lớp 10°", "lớp 10\""),
    
    # thong tin xuat ban bia sau
    ("tưr liệu được sử dụng", "tư liệu được sử dụng"),
    ("tưr liệu", "tư liệu"),
    ("<p class=\"lesson-p\">HANNo</p>", "")
]

def apply_fixes(text):
    if not text:
        return text
    current = text
    for target, repl in EXACT_REPLACEMENTS:
        current = current.replace(target, repl)
    return current

def clean_data_structure(data):
    if isinstance(data, str):
        return apply_fixes(data)
    elif isinstance(data, list):
        return [clean_data_structure(it) for it in data]
    elif isinstance(data, dict):
        return {k: clean_data_structure(v) for k, v in data.items()}
    return data

for b in ["lop-11", "lop-10", "lop-12"]:
    lp = DATA_DIR / f"lessons-{b}.json"
    with open(lp, encoding="utf-8") as f:
        data = json.load(f)
    cleaned = clean_data_structure(data)
    with open(lp, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"Applied fixes to {lp}")
    
    html_dir = LESSONS_DIR / b
    if html_dir.exists():
        for html_file in html_dir.glob("*.html"):
            c = html_file.read_text(encoding="utf-8")
            cc = apply_fixes(c)
            html_file.write_text(cc, encoding="utf-8")
    print(f"Applied fixes to HTMLs in {html_dir}")

bp = DATA_DIR / "books.json"
with open(bp, encoding="utf-8") as f:
    bdata = json.load(f)
cleaned_b = clean_data_structure(bdata)
with open(bp, "w", encoding="utf-8") as f:
    json.dump(cleaned_b, f, ensure_ascii=False, indent=2)
print("Applied fixes to books.json")

# Rebuild search indexes
from master_deep_fix import rebuild_search_indexes
rebuild_search_indexes()
print("Search indexes rebuilt successfully!")
