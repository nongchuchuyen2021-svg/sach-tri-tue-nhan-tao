import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Advanced dictionary of corrections
DEEP_CORRECTIONS = [
    # 1. The "Ví dụ" & "Vì sao" Normalization
    (r"\bkhông\s+vl\s+dụ\b", "không ví dụ"),
    (r"\bkhông\s+vi\s+dụ\b", "không ví dụ"),
    (r"\bkhông\s+v1\s+dụ\b", "không ví dụ"),
    (r"\bvl\s+dụ\b", "ví dụ"),
    (r"\bv1\s+d[ụự]\b", "ví dụ"),
    (r"\bvi\s+dự\b", "ví dụ"),
    (r"\bvỉ\s+du\b", "ví dụ"),
    (r"\bvi\s+dụ\b", "ví dụ"),
    (r"\bVì\s+dụ\b", "Ví dụ"),
    (r"\bvì\s+dụ\b", "ví dụ"),
    (r"\bVĩ\s+dụ\b", "Ví dụ"),
    (r"\bvĩ\s+dụ\b", "ví dụ"),
    (r"\bVi\s+dụ\b", "Ví dụ"),
    (r"\bVI\s+dụ\b", "Ví dụ"),
    (r"\bVÍ\s+DỤ\b", "VÍ DỤ"),
    
    # "Vì sao" & Multiple-choice options
    (r"\bVi\s+sao\b", "Vì sao"),
    (r"\bVI\s+sao\b", "Vì sao"),
    (r"\bvi\s+sao\b", "vì sao"),
    (r"\b([A-D]\.\s*)VI\b", r"\1Vì"),
    (r"\b([A-D]\.\s*)Vi\b", r"\1Vì"),
    
    # 2. Digit-in-word OCR errors
    (r"\bchuỗi\s+1ư\s+duy\b", "chuỗi tư duy"),
    (r"\b1ư\s+duy\b", "tư duy"),
    (r"\bđể\s+làm\s+g1\?", "để làm gì?"),
    (r"\blàm\s+g1\?", "làm gì?"),
    (r"\bBÁI\s+C:\s*4I\s+TẠO\s+SINH\s+HỒ\s+TRỢ\b", "BÀI 6: AI TẠO SINH HỖ TRỢ"),
    (r"\b4I\s+TẠO\s+SINH\b", "AI TẠO SINH"),
    (r"\bkỉ\s+nguyên\s+A1\b", "kỉ nguyên AI"),
    (r"\bnguyên\s+A1\b", "nguyên AI"),
    (r"\bhỗ\s+tr[ơợ]\s+của\s+A1\b", "hỗ trợ của AI"),
    (r"\bsức\s+mạnh\s+của\s+A1\b", "sức mạnh của AI"),
    (r"\bphẩm7\b", "phẩm?"),
    (r"\btốm\s+t8t\b", "tóm tắt"),
    (r"\bt[óo]m\s+t8t\b", "tóm tắt"),
    (r"\bthrstng\s+g8p\b", "thường gặp"),
    (r"\bthường\s+g8p\b", "thường gặp"),
    (r"\(placeho1der\)", "(placeholder)"),
    (r"\bd6\s+truy\s+[a-zÀ-ỹ]+\b", "để truy xuất"),
    (r"\bd6\s+chu[a-zÀ-ỹ]+\b", "để chuẩn bị"),
    (r"\bQuoryengine7ool\b", "QueryEngineTool"),
    (r"\bQuoryengine[A-Za-z0-9]*\b", "QueryEngineTool"),
    (r"\broolketadasa\b", "ToolMetadata"),
    (r"\b100lo\b", "100%"),
    (r"\bST2S\b", "ST25"),
    
    # 3. Lop 12 Bai 5 Prompt/Store Block Fixes
    (r"<p class=\"lesson-p\">\s*cae\s+thoc\s+ei\s+m\s+at\s+a\s+a\s+prh[^\<]*</p>", ""),
    (r"G1á\s+cà\s+của\s+són\s+phẩn", "Giá cả của sản phẩm"),
    (r"G1á\s+cả\s+của\s+sản\s+phẩm", "Giá cả của sản phẩm"),
    (r"Gid\s+süa\s+Vlnamilk\s+la\s+bao\s+nhléu\?", "Giá sữa Vinamilk là bao nhiêu?"),
    (r"Thông\s+tin\s+chi\s+trết\s+về\s+sản\s+phẩm\s*\(vi\s+dự:\s*\"Bánh\s+quy\s+Rinh\s+Đô\s+Marie\s+có\s+gì\s+đăc\s+biệt\?\"\)", 
     "Thông tin chi tiết về sản phẩm (ví dụ: \"Bánh quy Kinh Đô Marie có gì đặc biệt?\")"),
    (r"Các\s+chưong\s+trinh\s+khuyến\s+mãi,\s+ưu\s+đãt\s*\(v1\s+dụ:\s*\"M1\s+tôm\s+Hảo\s+lào\s+có\s+khuyến\s+mái\s+gì\s+không\?\",\s*\"Khuyến\s+mãt\s+tháng\s+6\s+la\s+gi\?\"\)",
     "Các chương trình khuyến mãi, ưu đãi (ví dụ: \"Mì tôm Hảo Hảo có khuyến mãi gì không?\", \"Khuyến mãi tháng 6 là gì?\")"),
    (r"Bạn\s+PHAI\s+sủ\s+dụng\s+công\s+cụ\s+này\s+để\s+trụy", "Bạn PHẢI sử dụng công cụ này để truy xuất"),
    (r"Sử\s+dung\s+công\s+cự\s+này\s+khi\s+người\s+dùng\s+hỏi\s+vê:", "Sử dụng công cụ này khi người dùng hỏi về:"),
    
    # 4. General Word Typo Fixes
    (r"\bvắn\s+đ[ểẻề]\b", "vấn đề"),
    (r"\bvấn\s+dề\b", "vấn đề"),
    (r"\b[dđ][ãỡũ]\s+liệu\b", "dữ liệu"),
    (r"\bđỡ\s+liệu\b", "dữ liệu"),
    (r"\bđữ\s+liệu\b", "dữ liệu"),
    (r"\bdữ\s+liệu\s+mói\b", "dữ liệu mới"),
    (r"\blóm\s+tắt\b", "tóm tắt"),
    (r"\btim\s+ki[ếe]m\b", "tìm kiếm"),
    (r"\btim\s+hiểu\b", "tìm hiểu"),
    (r"\bch[ìi]nh\s+sửa\b", "chỉnh sửa"),
    (r"\btinh\s+ch[ìi]nh\b", "tinh chỉnh"),
    (r"\bbi[ếể]u\s+đ[òồ]\b", "biểu đồ"),
    (r"\bgi[àa]\s+sử\b", "giả sử"),
    (r"\btu\s+duy\b", "tư duy"),
    (r"\bthiên\s+nhi[ềe]n\b", "thiên nhiên"),
    (r"\bkhi\s+thải\b", "khí thải"),
    (r"\bto[àa]\s+nhiệt\b", "tỏa nhiệt"),
    (r"\btiêu\s+t[ồo]n\b", "tiêu tốn"),
    (r"\bnưóc\b", "nước"),
    (r"\bgiải\s+thich\b", "giải thích"),
    (r"\bđặc\s+biêt\b", "đặc biệt"),
    (r"\bh[ọo]p\s+thoại\b", "hộp thoại"),
    (r"\bd[ủu]\s+có\b", "dù có"),
    (r"\bd[ủu]\s+là\b", "dù là"),
    (r"\bd[ủu]\s+cho\b", "dù cho"),
    (r"\bthông\s+tín\b", "thông tin"),
    (r"\bkI\s+năng\b", "kĩ năng"),
    (r"\bkĩ\s+náng\b", "kĩ năng"),
    (r"\brèn\s+kĩ\s+náng\b", "rèn kĩ năng"),
    (r"\bhọc\s+máy\b", "Học máy"),
    (r"\bHọc\s+mảy\b", "Học máy"),
    (r"\bphân\s+lin\b", "phân tán"),
    (r"\bđiểm\s+th\s+thật\b", "điểm thi thật"),
    (r"\bsố\s+sụ\s+thể\b", "số cụ thể"),
    (r"\bhợp\s+nhật\b", "hợp nhất"),
    (r"\bcổ\s+máy\b", "cỗ máy"),
    (r"\bnhấm\s+đúng\b", "nhắm đúng"),
    (r"\bkiểm\s+từ\s+sóm\b", "kiểm thử sớm"),
    (r"\bTạo\s+luông\b", "Tạo luồng"),
    (r"\bthông\s+báo\s+lỏi\b", "thông báo lỗi"),
    (r"\bbò\s+sót\b", "bỏ sót"),
    (r"\bban\s+muốn\s+AI\b", "bạn muốn AI"),
    (r"\bthích\s+nghỉ\b", "thích nghi"),
    (r"\bthay\s+dổi\s+the\s+giới\b", "thay đổi thế giới"),
    (r"\bthe\s+giới\b", "thế giới"),
    (r"\bquy\s+trinh\b", "quy trình"),
]

def apply_deep_clean(text):
    if not text:
        return text
    for pat, rep in DEEP_CORRECTIONS:
        text = re.sub(pat, rep, text)
    return text

total_updates = 0

for grade in ["lop-10", "lop-11", "lop-12"]:
    json_path = ROOT / "data" / f"lessons-{grade}.json"
    html_dir = ROOT / "lessons" / grade
    data = json.load(open(json_path, encoding="utf-8"))
    grade_updates = 0
    
    for les in data:
        # Title
        t = apply_deep_clean(les.get("title", ""))
        if t != les.get("title", ""):
            les["title"] = t
            grade_updates += 1
            
        # Summary
        s = apply_deep_clean(les.get("summary", ""))
        if s != les.get("summary", ""):
            les["summary"] = s
            grade_updates += 1
            
        # Group
        g = apply_deep_clean(les.get("group", ""))
        if g != les.get("group", ""):
            les["group"] = g
            grade_updates += 1
            
        # HTML
        h = apply_deep_clean(les.get("html", ""))
        if h != les.get("html", ""):
            les["html"] = h
            grade_updates += 1
            
        # HTML file on disk
        lid = les["id"]
        html_file = html_dir / f"{lid}.html"
        if html_file.exists():
            f_content = html_file.read_text(encoding="utf-8")
            clean_f = apply_deep_clean(f_content)
            if clean_f != f_content:
                html_file.write_text(clean_f, encoding="utf-8")
                
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
        
    print(f"✓ Deep cleaned {grade_updates} items in {grade}")
    total_updates += grade_updates

# Also update books.json
books_path = ROOT / "data" / "books.json"
books_data = json.load(open(books_path, encoding="utf-8"))
for b in books_data.get("books", []):
    b["title"] = apply_deep_clean(b.get("title", ""))
    b["description"] = apply_deep_clean(b.get("description", ""))
    for ch in b.get("chapters", []):
        ch["title"] = apply_deep_clean(ch.get("title", ""))
        ch["desc"] = apply_deep_clean(ch.get("desc", ""))

with open(books_path, "w", encoding="utf-8") as f:
    json.dump(books_data, f, ensure_ascii=False, indent=2)

print(f"\nALL DEEP CORRECTIONS FINISHED! Total updates: {total_updates}")
