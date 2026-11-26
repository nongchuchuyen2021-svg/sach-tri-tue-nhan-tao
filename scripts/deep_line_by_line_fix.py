import json
import re
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Line-by-line & word-by-word comprehensive correction dictionary
corrections = [
    # --- Grade 11 Bai 1 Specific user screenshot ---
    ("1. Prompt co bán Trong chương trinh lớp 10, em đã học cách viết prompt co bản, gồm chỉ thị và dữ liệu đầu vào.",
     "1. Prompt cơ bản\n\nTrong chương trình lớp 10, em đã học cách viết prompt cơ bản, gồm chỉ thị và dữ liệu đầu vào."),
    ("1. Prompt co bán", "1. Prompt cơ bản"),
    ("Prompt co bán", "Prompt cơ bản"),
    ("prompt co bán", "prompt cơ bản"),
    ("prompt co bản", "prompt cơ bản"),
    ("Prompt co bản", "Prompt cơ bản"),
    ("Bảng 1.1. So sánh prompt co bản và prompt nàng cao", "Bảng 1.1. So sánh prompt cơ bản và prompt nâng cao"),
    ("prompt nàng cao", "prompt nâng cao"),
    ("nàng cao", "nâng cao"),
    ("chương trinh", "chương trình"),
    ("Chương trinh", "Chương trình"),

    # --- Grade 10 Cover & Front matter ---
    ("VŨ VĂN LUAN", "VŨ VĂN LUÂN"),
    ("HOÀNG THL MAI", "HOÀNG THỊ MAI"),
    ("LÊ ANI VINH", "LÊ ANH VINH"),
    ("ĐÔNG CHU BIEN", "ĐỒNG CHỦ BIÊN"),
    ("CAD LOC.", ""),
    ("TRÍ TUÊ NHÂN TAO   LóP 1]", "TRÍ TUỆ NHÂN TẠO LỚP 11"),
    ("TRÍ TUÊ NHÂN TẠO LỚP 11", "TRÍ TUỆ NHÂN TẠO LỚP 11"),
    ("TRÍ TUÊ NHÂN TAO", "TRÍ TUỆ NHÂN TẠO"),
    ("TRÍ TUÊ", "TRÍ TUỆ"),
    ("Tri tuê", "Trí tuệ"),
    ("Góm những", "Gồm những"),
    ("Góm các", "Gồm các"),
    ("phát triến", "phát triển"),
    ("ngôn ngữ lón", "ngôn ngữ lớn"),
    ("mô hình ngôn ngữ lón", "mô hình ngôn ngữ lớn"),

    # --- Grade 10 Lessons ---
    ("Sưno A/", "Suno AI"),
    ("Sưno AI", "Suno AI"),
    ("KHÁM PHẨ", "KHÁM PHÁ"),
    ("hình ănh", "hình ảnh"),
    ("sinh hình ănh", "sinh hình ảnh"),
    ("Ban. du muán tôi tạo thêm hình ảnh náo nữa không?", "Bạn có muốn tôi tạo thêm hình ảnh nào nữa không?"),
    ("Dsy ls mot búc tranh né mùa zadn", "Đây là một bức tranh về mùa xuân"),
    ("Shoe thasing v", ""),
    ("Ash Gerini", "Ask Gemini"),
    ("Drep Reaserch", "Deep Research"),
    ("minh họạ", "minh họa"),
    ("hình ảnh minh họạ", "hình ảnh minh họa"),
    ("đọc câu sạu", "đọc câu sau"),
    ("câu sạu", "câu sau"),
    ("chalbot AI", "chatbot AI"),
    ("chalbot", "chatbot"),
    ("huắn luyện", "huấn luyện"),
    ("LÚYỆN TẬP", "LUYỆN TẬP"),
    ("huán luyện", "huấn luyện"),
    ("Xóá bỏ", "Xóa bỏ"),
    ("xóá bỏ", "xóa bỏ"),
    ("xóá ô", "xóa ô"),
    ("xóá", "xóa"),
    ("Xóá", "Xóa"),
    ("AIsA", ""),
    ("llên quan", "liên quan"),
    ("hoặt động", "hoạt động"),
    ("Xàc định", "Xác định"),
    ("đăn ra", "đặt ra"),
    ("dễ chên tiêu để", "dễ chèn tiêu đề"),
    ("chên tiêu để", "chèn tiêu đề"),
    ("chên tiêu đề", "chèn tiêu đề"),
    ("tiêu để", "tiêu đề"),
    ("1.  Giới thiệu prompi", "1. Giới thiệu prompt"),
    ("prompi", "prompt"),
    ("prompl", "prompt"),
    ("Vĩ dụ prompl:", "Ví dụ prompt:"),
    ("Vĩ dụ", "Ví dụ"),
    ("nhồm bạn Mai", "nhóm bạn Mai"),
    ("nhồm bạn", "nhóm bạn"),
    ("nhôm bạn", "nhóm bạn"),
    ("bải thuyết trinh", "bài thuyết trình"),
    ("thuyết trinh", "thuyết trình"),
    ("môn Lích sử", "môn Lịch sử"),
    ("Lích sử", "Lịch sử"),
    ("Khẩu hinh", "Khẩu hình"),
    ("khẩu hinh", "khẩu hình"),
    ("làm gìảm", "làm giảm"),
    ("làm gìảm tính", "làm giảm tính"),
    ("làm gìảm độ", "làm giảm độ"),
    ("làm gìảm hiệu quả", "làm giảm hiệu quả"),
    ("gìảm", "giảm"),
    ("tư lệu", "tư liệu"),
    ("tìm them tư", "tìm thêm tư"),
    ("từng khung hinh", "từng khung hình"),
    ("khung hinh", "khung hình"),
    ("Tri tuê nhân tạo", "Trí tuệ nhân tạo"),
    ("càa cầu chuyệr", "của câu chuyện"),
    ("cầu chuyệr", "câu chuyện"),
    ("càa", "của"),
    ("Bude 6 Tuong tär. 'i. ?.. -,1'strj rs. AI và kiem tra, hiệu chính kết quả tạo ảnh",
     "Bước 6. Tương tác với AI và kiểm tra, hiệu chỉnh kết quả tạo ảnh"),
    ("Tuong tär", "Tương tác"),
    ("kiem tra", "kiểm tra"),
    ("hiệu chính", "hiệu chỉnh"),
    ("tạo ản", "tạo ảnh"),
    ("bạnnam", "bạn nam"),
    ("fình", "hình"),
    ("yẽu", "yêu"),
    ("Colabl", "Colab"),
    ("Coladl", "Colab"),
    ("ChaGPT", "ChatGPT"),
    ("câu chiuyện", "câu chuyện"),
    ("chiuyện", "chuyện"),
    ("rtuyện", "truyện"),
    ("bài thuyết trinh", "bài thuyết trình"),

    # --- Grade 11 Lessons ---
    ("soan thảo", "soạn thảo"),
    ("căn chỉnh sửa", "cần chỉnh sửa"),
    ("Tỉnh chỉnh (Fine-tuning)", "Tinh chỉnh (Fine-tuning)"),
    ("Tỉnh chỉnh", "Tinh chỉnh"),
    ("hàng trăm nghin", "hàng trăm nghìn"),
    ("nghin", "nghìn"),
    ("dựa trèn", "dựa trên"),
    ("trèn", "trên"),
    ("mộn học", "môn học"),
    ("bài loán", "bài toán"),
    ("loán", "toán"),
    ("gản nhãn", "gắn nhãn"),
    ("tưong tác", "tương tác"),
    ("tưong", "tương"),
    ("chưong trinh", "chương trình"),
    ("chưong", "chương"),
    ("thoat", "thoát"),
    ("triên khai", "triển khai"),
    ("sừa", "sửa"),
    ("điêm", "điểm"),
    ("Gisy", "Giấy"),
    ("Giay", "Giấy"),

    # --- Grade 12 Lessons ---
    ("UX/UI co bán", "UX/UI cơ bản"),
    ("AI Flow co bản", "AI Flow cơ bản"),
    ("kháchhhh hàng", "khách hàng"),
    ("kháchhhh", "khách"),
    ("trom a Data Source", "from a Data Source"),
    ("trom a", "from a"),
    ("Syslec Prampr", "System Prompt"),
    ("Evatuations Profiter", "Evaluations Profiler"),
    ("Lamalndex", "LlamaIndex"),
    ("lamalndex", "llamaindex"),
    ("Sữa lươi Vinamilk có dường: 29 000 VND/lít", "Sữa tươi Vinamilk có đường: 29 000 VND/lít"),
    ("Sữa lươi", "Sữa tươi"),
    ("có dường", "có đường"),
    ("CÔNG CU (tools)", "CÔNG CỤ (tools)"),
    ("CÔNG CU", "CÔNG CỤ"),
    ("Coca-Colo Ion", "Coca-Cola lon"),
    ("Coca-Colo", "Coca-Cola"),
    ("đữ liệu", "dữ liệu"),
    ("đữ", "dữ"),
    ("Học mây cợ bản", "Học máy cơ bản"),
    ("Học mây", "Học máy"),
    ("hăng nghin", "hàng nghìn"),
    ("đữ liệu mói", "dữ liệu mới"),
    ("Vi biéu do phán lin (sealler plot)", "Vẽ biểu đồ phân tán (scatter plot)"),
    ("sealler plot", "scatter plot"),
    ("phán lin", "phân tán"),
    ("biéu do", "biểu đồ"),
    ("biéu", "biểu"),
    ("giản mát mát", "giảm mất mát"),
    ("càng lón thi sai lệch", "càng lớn thì sai lệch"),
    ("càng lón", "càng lớn"),
    ("tính loán", "tính toán"),
    ("lảm việc nhóm. lập trinh, kiếm thừ", "làm việc nhóm, lập trình, kiểm thử"),
    ("lập trinh", "lập trình"),
    ("kiếm thừ", "kiểm thử"),
    ("tử kháu ý tưởng đến trinh bày", "từ khâu ý tưởng đến trình bày"),
    ("tử kháu", "từ khâu"),
    ("trinh bày", "trình bày"),
    ("giúp ich gì", "giúp ích gì"),
    ("giúp ich", "giúp ích"),
    ("XữIi quy trình phúc tạp", "Xử lí quy trình phức tạp"),
    ("XữIi", "Xử lí"),
    ("phúc tạp", "phức tạp"),
    ("đượs giải quyết", "được giải quyết"),
    ("đượs", "được"),
    ("không đây đù/sai", "không đầy đủ/sai"),
    ("không đây đù", "không đầy đủ"),
    ("print (\"Đđ tạo chỉ sực dữ liệu thành côn", "print(\"Đã tạo chỉ mục dữ liệu thành công\")"),
    ("ưu đãt", "ưu đãi"),
    ("Vinamilh", "Vinamilk"),
    ("Vinanilk", "Vinamilk"),
    ("Vinarilk", "Vinamilk"),
    ("Vlnamilk", "Vinamilk"),
    ("són phẩn", "sản phẩm"),
    ("Gid süa", "Giá sữa"),
    ("Süa tuot Virgma 100% Organic", "Sữa tươi Vinamilk 100% Organic"),
    ("toại nủa này đả lua chọn phù nộp vếi nhu câu", "loại sữa này để lựa chọn phù hợp với nhu cầu"),
    ("vào vộc đưa rả các ý luơng", "vào việc đưa ra các ý tưởng"),
    ("vào vộc", "vào việc"),
    ("đưa rả", "đưa ra"),
    ("ý luơng", "ý tưởng"),
    ("Ál tạo sinh", "AI tạo sinh"),
    ("Ál", "AI"),
    ("khổi", "khối"),
    ("lệp", "tệp"),
    ("giup", "giúp"),
    ("sirh", "sinh"),
    ("diém", "điểm"),
    ("àp cáu rói à dày", "áp câu hỏi ở đây"),
    ("Step ánput", "Step input"),
    ("Thaught: I car ansver vithout", "Thought: I can answer without"),
    ("He Of glas tiep trie thp vill nguth, diung", "Hệ thống giao tiếp trực tiếp với người dùng"),
    ("finh vire Tin hox iher Khoa rù nay tinh", "lĩnh vực Tin học như Khoa học máy tính"),
    ("Quý khuch có trể cản nhớc", "Quý khách có thể cân nhắc"),
    ("Workfiows", "Workflows"),
    ("Warkflow", "Workflow"),
]

def apply_clean(text):
    if not isinstance(text, str):
        return text
    for old, new in corrections:
        text = text.replace(old, new)
    
    # Common OCR regex fixes
    text = re.sub(r"\bPrompt\s+co\s+bán\b", "Prompt cơ bản", text, flags=re.IGNORECASE)
    text = re.sub(r"\bprompt\s+co\s+bản\b", "prompt cơ bản", text, flags=re.IGNORECASE)
    text = re.sub(r"\bco\s+bản\b", "cơ bản", text, flags=re.IGNORECASE)
    text = re.sub(r"\bchương\s+trinh\b", "chương trình", text, flags=re.IGNORECASE)
    text = re.sub(r"\bquá\s+trinh\b", "quá trình", text, flags=re.IGNORECASE)
    text = re.sub(r"\blập\s+trinh\b", "lập trình", text, flags=re.IGNORECASE)
    text = re.sub(r"\bthuyết\s+trinh\b", "thuyết trình", text, flags=re.IGNORECASE)
    text = re.sub(r"\btrinh\s+bày\b", "trình bày", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmô\s+hinh\b", "mô hình", text, flags=re.IGNORECASE)
    text = re.sub(r"\bkhung\s+hinh\b", "khung hình", text, flags=re.IGNORECASE)
    text = re.sub(r"\bkhẩu\s+hinh\b", "khẩu hình", text, flags=re.IGNORECASE)
    text = re.sub(r"\bhình\s+ảnh\s+minh\s+họạ\b", "hình ảnh minh họa", text, flags=re.IGNORECASE)
    text = re.sub(r"\bminh\s+họạ\b", "minh họa", text, flags=re.IGNORECASE)
    text = re.sub(r"\blàm\s+gìảm\b", "làm giảm", text, flags=re.IGNORECASE)
    text = re.sub(r"\bhàng\s+trăm\s+nghin\b", "hàng trăm nghìn", text, flags=re.IGNORECASE)
    text = re.sub(r"\bhàng\s+nghin\b", "hàng nghìn", text, flags=re.IGNORECASE)
    text = re.sub(r"\bgiúp\s+ich\b", "giúp ích", text, flags=re.IGNORECASE)
    text = re.sub(r"\bkháchhhh\b", "khách", text, flags=re.IGNORECASE)
    text = re.sub(r"\bkháchhhh\s+hàng\b", "khách hàng", text, flags=re.IGNORECASE)
    text = re.sub(r"\bUX/UI\s+co\s+bán\b", "UX/UI cơ bản", text, flags=re.IGNORECASE)
    text = re.sub(r"\btính\s+loán\b", "tính toán", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbài\s+loán\b", "bài toán", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(Hinh|hinh)\s+(\d+\.\d+)", r"Hình \2", text)
    return text

def walk_and_fix(obj):
    if isinstance(obj, dict):
        return {k: walk_and_fix(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [walk_and_fix(item) for item in obj]
    elif isinstance(obj, str):
        return apply_clean(obj)
    return obj

# 1. Clean data/books.json
print("Cleaning data/books.json...")
books_p = ROOT / "data" / "books.json"
books_data = json.loads(books_p.read_text(encoding="utf-8"))
cleaned_books = walk_and_fix(books_data)
books_p.write_text(json.dumps(cleaned_books, ensure_ascii=False, indent=2), encoding="utf-8")

# 2. Clean data/lessons-lop-{10,11,12}.json
for b in ["lop-10", "lop-11", "lop-12"]:
    lp = ROOT / "data" / f"lessons-{b}.json"
    print(f"Cleaning {lp}...")
    data = json.loads(lp.read_text(encoding="utf-8"))
    cleaned_data = walk_and_fix(data)
    lp.write_text(json.dumps(cleaned_data, ensure_ascii=False, indent=2), encoding="utf-8")

# 3. Clean all lessons/lop-*/*.html
html_files = glob.glob(str(ROOT / "lessons" / "*" / "*.html"))
print(f"Cleaning {len(html_files)} HTML files...")
for hf in html_files:
    p = Path(hf)
    content = p.read_text(encoding="utf-8")
    cleaned = apply_clean(content)
    p.write_text(cleaned, encoding="utf-8")

# 4. Clean index.html and reader.html
for rf in ["index.html", "reader.html"]:
    rp = ROOT / rf
    if rp.exists():
        content = rp.read_text(encoding="utf-8")
        cleaned = apply_clean(content)
        rp.write_text(cleaned, encoding="utf-8")

# 5. Rebuild search indexes
print("Rebuilding search indexes...")
for b in ["lop-10", "lop-11", "lop-12"]:
    lp = ROOT / "data" / f"lessons-{b}.json"
    sp = ROOT / "data" / f"search-{b}.json"
    
    lessons = json.loads(lp.read_text(encoding="utf-8"))
    search_data = []
    
    for item in lessons:
        html = item.get("html", "")
        clean_text = re.sub(r"<[^>]+>", " ", html)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        
        full_content = f"{item.get('group', '')} {item.get('title', '')} {clean_text}".strip()
        full_content = re.sub(r"\s+", " ", full_content)
        
        search_data.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "group": item.get("group"),
            "startPage": item.get("startPage", 1),
            "content": full_content
        })
    
    sp.write_text(json.dumps(search_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rebuilt {sp} with {len(search_data)} entries.")

print("All line-by-line corrections applied!")
