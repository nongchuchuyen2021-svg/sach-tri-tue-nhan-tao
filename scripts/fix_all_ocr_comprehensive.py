import json
import re
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Complete mapping of OCR errors to correct Vietnamese text
exhaustive_fixes = [
    # Specific OCR sentences & blocks
    ("1. Prompt co bán Trong chương trinh lớp 10, em đã học cách viết prompt co bản, gồm chỉ thị và dữ liệu đầu vào.",
     "1. Prompt cơ bản\n\nTrong chương trình lớp 10, em đã học cách viết prompt cơ bản, gồm chỉ thị và dữ liệu đầu vào."),
    ("1. Prompt co bán", "1. Prompt cơ bản"),
    ("Prompt co bán", "Prompt cơ bản"),
    ("prompt co bán", "prompt cơ bản"),
    ("prompt co bản", "prompt cơ bản"),
    ("Prompt co bản", "Prompt cơ bản"),
    ("Bảng 1.1. So sánh prompt co bản và prompt nàng cao", "Bảng 1.1. So sánh prompt cơ bản và prompt nâng cao"),
    ("BÁI C: 4I TẠO SINH HỒ TRỢ", "BÀI 6: AI TẠO SINH HỖ TRỢ HỌC TẬP"),
    ("BÀI C: 4I TẠO SINH", "BÀI 6: AI TẠO SINH"),
    ("4I TẠO SINH", "AI TẠO SINH"),
    ("CHỦ ĐỀ 2. NGUYÊN LĨ HOẠT ĐỘNG", "CHỦ ĐỀ 2. NGUYÊN LÍ HOẠT ĐỘNG"),
    ("CHỦ ĐỂ 2. NGUYÊN ÚÍ HOẠT ĐỘNG CỦA MÔ HÌNH NGÔN NG", "CHỦ ĐỀ 2. NGUYÊN LÍ HOẠT ĐỘNG CỦA MÔ HÌNH NGÔN NGỮ LỚN"),
    ("NGUYÊN LĨ", "NGUYÊN LÍ"),
    ("NGUYÊN ÚÍ", "NGUYÊN LÍ"),
    ("BẠI 5. KHAI THẬC, THỪ VIỆN", "BÀI 5. KHAI THÁC THƯ VIỆN"),
    ("KHAI THẬC, THỪ VIỆN", "KHAI THÁC THƯ VIỆN"),
    ("BAO VỀ MÔI TRUƠNG", "BẢO VỆ MÔI TRƯỜNG"),
    ("HƯỚNG DẪN SỪ DỤNG SÁCH", "HƯỚNG DẪN SỬ DỤNG SÁCH"),
    ("TRÍ TUÊ NHÂN TAO   LóP 1]", "TRÍ TUỆ NHÂN TẠO LỚP 11"),
    ("TRÍ TUÊ NHÂN TẠO LỚP 11", "TRÍ TUỆ NHÂN TẠO LỚP 11"),
    ("TRÍ TUÊ NHÂN TAO", "TRÍ TUỆ NHÂN TẠO"),
    ("TRÍ TUÊ", "TRÍ TUỆ"),
    ("Tri tuê", "Trí tuệ"),
    ("tri tuê", "trí tuệ"),
    ("Giú: 40.000đ", "Giá: 40.000đ"),
    ("1/khoăng cách", "1/khoảng cách"),
    ("chuỗi 1ư duy", "chuỗi tư duy"),
    ("Thương Niệu vy tin • Giất lượng đàm báo", "Thương hiệu uy tín • Chất lượng đảm bảo"),
    ("Thương Niệu vy tin", "Thương hiệu uy tín"),
    ("Giất lượng đàm báo", "Chất lượng đảm bảo"),
    ("(Glá trị nội dung chính)", "(Giá trị nội dung chính)"),
    ("Glá trị", "Giá trị"),
    ("Gúi thư điện sử", "Gửi thư điện tử"),
    ("thư điện sử", "thư điện tử"),
    ("Mi lôm Háo Hôo", "Mì tôm Hảo Hảo"),
    ("Háo Hôo", "Hảo Hảo"),
    ("Mi lôm", "Mì tôm"),
    ("Trợ Ií ảo", "Trợ lí ảo"),
    ("Trợ Ií", "Trợ lí"),
    ("Khôa học trực tuyên", "Khóa học trực tuyến"),
    ("Khôa học", "Khóa học"),
    ("Liệc phát triển và vận hành", "Việc phát triển và vận hành"),
    ("Liệc phát triển", "Việc phát triển"),
    ("Ngường đò = 60", "Ngưỡng đo = 60"),
    ("Niếu xuất hiện", "Nếu xuất hiện"),
    ("Sừ dụng Google Colab", "Sử dụng Google Colab"),
    ("Sừ dụng", "Sử dụng"),
    ("SỪ DỤNG", "SỬ DỤNG"),
    ("Tổng Giảm đóc", "Tổng Giám đốc"),
    ("NGUYỄN TIÊN THẠNH", "NGUYỄN TIẾN THANH"),
    ("NGUYỄN THANH GIẠNG", "NGUYỄN THANH GIẢNG"),
    ("môn Tuán, LI, Hóa", "môn Toán, Lí, Hóa"),
    ("môn Tuán", "môn Toán"),
    ("tháng Tảm (1945-1975)", "tháng Tám (1945-1975)"),
    ("tháng Tảm", "tháng Tám"),
    ("Sữa tươc Vinamilk", "Sữa tươi Vinamilk"),
    ("Sữa tươc", "Sữa tươi"),
    ("Sữa lươi", "Sữa tươi"),
    ("có dường", "có đường"),
    ("CÔNG CU (tools)", "CÔNG CỤ (tools)"),
    ("CÔNG CU", "CÔNG CỤ"),
    ("Coca-Colo Ion", "Coca-Cola lon"),
    ("Coca-Colo", "Coca-Cola"),
    ("Học mây cợ bản", "Học máy cơ bản"),
    ("Học mây", "Học máy"),
    ("hăng nghin", "hàng nghìn"),
    ("đữ liệu mói", "dữ liệu mới"),
    ("đữ liệu", "dữ liệu"),
    ("đữ", "dữ"),
    ("Tin kiêm thông tỉn sên quan tự trớc miội caa đính xác và nhanh chóng",
     "Tìm kiếm thông tin liên quan từ trước một cách chính xác và nhanh chóng"),
    ("Dịch thuật và tốm t8t", "Dịch thuật và tóm tắt"),
    ("tốm t8t", "tóm tắt"),
    ("tốm tắt", "tóm tắt"),
    ("Tưong tớe vel ne thông khác", "Tương tác với hệ thống khác"),
    ("Tưong tớe", "Tương tác"),
    ("tụp động hoa", "tự động hóa"),
    ("từy chọn", "tùy chọn"),
    ("Ai tựr động", "AI tự động"),
    ("tựr động", "tự động"),
    ("khung vuông/dọc giúp lập trung vào chủ thế", "khung vuông/dọc giúp tập trung vào chủ thể"),
    ("lập trung vào", "tập trung vào"),
    ("chủ thế", "chủ thể"),
    ("Tín hiệu đầu vàoGiá trị đầu vào", "Tín hiệu đầu vào - Giá trị đầu vào"),
    ("sù dung Ollena vól mo hinh \"1lama2\" chay c7s bộ", "sử dụng Ollama với mô hình \"llama2\" chạy cục bộ"),
    ("sù dung", "sử dụng"),
    ("vól mo hinh", "với mô hình"),
    ("chay c7s bộ", "chạy cục bộ"),
    ("IlamaIndex v1 nó tích họp tốt vớ1 các công cụ của blameIndex",
     "LlamaIndex vì nó tích hợp tốt với các công cụ của LlamaIndex"),
    ("tích họp", "tích hợp"),
    ("vớ1 các công cụ", "với các công cụ"),
    ("sắp xêp hàng hoa", "sắp xếp hàng hóa"),
    ("sắp xêp", "sắp xếp"),
    ("hàng hoa", "hàng hóa"),
    ("Ngày xừa ngày xưa", "Ngày xửa ngày xưa"),
    ("xừa ngày xưa", "xửa ngày xưa"),
    ("hợp Íí chưa", "hợp lí chưa"),
    ("hợp Íí", "hợp lí"),
    ("đat đến mức độ", "đạt đến mức độ"),
    ("đat đến", "đạt đến"),
    ("câu hỏi đùng/sai", "câu hỏi đúng/sai"),
    ("đùng/sai", "đúng/sai"),
    ("đăn guitar", "đàn guitar"),
    ("chơi đăn", "chơi đàn"),
    ("đải truyền hình", "đài truyền hình"),
    ("[Dữ liệu đảu vào]", "[Dữ liệu đầu vào]"),
    ("đảu vào", "đầu vào"),
    ("yêu ố mới", "yếu tố mới"),
    ("yêu ố", "yếu tố"),
    ("nọữ nghiĩa", "ngữ nghĩa"),
    ("tình huồng", "tình huống"),
    ("lệnh/it; lệnh", "lệnh/ít lệnh"),
    ("lệnh/it", "lệnh/ít"),
    ("hặn", "bản"),
    ("từy", "tùy"),
    ("truór", "trước"),
    ("trạn", "bạn"),
    ("sản phẩm7", "sản phẩm?"),
    ("nguốn thông tin", "nguồn thông tin"),
    ("nguốn", "nguồn"),
    ("niện ray", "hiện nay"),
    ("loạ độ", "tọa độ"),
    ("luả đề", "lựa để"),
    ("ghành một nhiệm vụ", "thành một nhiệm vụ"),
    ("ghành", "thành"),
    ("bài taàn", "bài toán"),
    ("Tìm kiém", "Tìm kiếm"),
    ("kiém kiến thức", "kiếm kiến thức"),
    ("kiém", "kiếm"),
    ("gòm có", "gồm có"),
    ("nguờn khác nhau", "nguồn khác nhau"),
    ("nguờn", "nguồn"),
    ("thông tỉn", "thông tin"),
    ("kốt hợp", "kết hợp"),
    ("nhự LangChain", "như LangChain"),
    ("càa cầu chuyệr", "của câu chuyện"),
    ("càa", "của"),
    ("chuyệr", "chuyện"),
    ("Bude 6", "Bước 6"),
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
    ("chiuyện", "chuyện"),
    ("rtuyện", "truyện"),
    ("bbi", "bài"),
    ("soan thảo", "soạn thảo"),
    ("căn chỉnh sửa", "cần chỉnh sửa"),
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
    ("XữIi quy trình phúc tạp", "Xử lí quy trình phức tạp"),
    ("XữIi", "Xử lí"),
    ("phúc tạp", "phức tạp"),
    ("đượs giải quyết", "được giải quyết"),
    ("đượs", "được"),
    ("không đây đù/sai", "không đầy đủ/sai"),
    ("không đây đù", "không đầy đủ"),
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
    ("nàng cao", "nâng cao"),
    ("chương trinh", "chương trình"),
    ("Chương trinh", "Chương trình"),
    ("quá trinh", "quá trình"),
    ("Quá trinh", "Quá trình"),
    ("lập trinh", "lập trình"),
    ("thuyết trinh", "thuyết trình"),
    ("trinh bày", "trình bày"),
    ("Trinh bày", "Trình bày"),
    ("mô hinh", "mô hình"),
    ("Mô hinh", "Mô hình"),
    ("mò hinh", "mô hình"),
    ("khung hinh", "khung hình"),
    ("khẩu hinh", "khẩu hình"),
    ("minh họạ", "minh họa"),
    ("làm gìảm", "làm giảm"),
    ("hàng trăm nghin", "hàng trăm nghìn"),
    ("hàng nghin", "hàng nghìn"),
    ("giúp ich", "giúp ích"),
    ("tính loán", "tính toán"),
    ("bài loán", "bài toán"),
]

def clean_entire_text(text):
    if not isinstance(text, str):
        return text
    
    # 1. First, replace 'ảnhh' -> 'ảnh' (critical OCR issue)
    text = re.sub(r"\bảnhh\b", "ảnh", text, flags=re.IGNORECASE)
    
    # 2. Apply all exact pairs
    for old, new in exhaustive_fixes:
        text = text.replace(old, new)
        
    # 3. Regex passes for boundary issues
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
    text = re.sub(r"\bminh\s+họạ\b", "minh họa", text, flags=re.IGNORECASE)
    text = re.sub(r"\blàm\s+gìảm\b", "làm giảm", text, flags=re.IGNORECASE)
    text = re.sub(r"\bhàng\s+trăm\s+nghin\b", "hàng trăm nghìn", text, flags=re.IGNORECASE)
    text = re.sub(r"\bhàng\s+nghin\b", "hàng nghìn", text, flags=re.IGNORECASE)
    text = re.sub(r"\bgiúp\s+ich\b", "giúp ích", text, flags=re.IGNORECASE)
    text = re.sub(r"\bkháchhhh\b", "khách", text, flags=re.IGNORECASE)
    text = re.sub(r"\bUX/UI\s+co\s+bán\b", "UX/UI cơ bản", text, flags=re.IGNORECASE)
    text = re.sub(r"\btính\s+loán\b", "tính toán", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbài\s+loán\b", "bài toán", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(Hinh|hinh)\s+(\d+\.\d+)", r"Hình \2", text)
    return text

def walk_tree(obj):
    if isinstance(obj, dict):
        return {k: walk_tree(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [walk_tree(item) for item in obj]
    elif isinstance(obj, str):
        return clean_entire_text(obj)
    return obj

# Update books.json
books_p = ROOT / "data" / "books.json"
print("Updating books.json...")
b_data = json.loads(books_p.read_text(encoding="utf-8"))
books_p.write_text(json.dumps(walk_tree(b_data), ensure_ascii=False, indent=2), encoding="utf-8")

# Update lessons JSON
for b in ["lop-10", "lop-11", "lop-12"]:
    lp = ROOT / "data" / f"lessons-{b}.json"
    print(f"Updating {lp}...")
    l_data = json.loads(lp.read_text(encoding="utf-8"))
    lp.write_text(json.dumps(walk_tree(l_data), ensure_ascii=False, indent=2), encoding="utf-8")

# Update all HTML files
for hf in glob.glob(str(ROOT / "lessons" / "*" / "*.html")):
    p = Path(hf)
    content = p.read_text(encoding="utf-8")
    p.write_text(clean_entire_text(content), encoding="utf-8")

for rf in ["index.html", "reader.html"]:
    rp = ROOT / rf
    if rp.exists():
        rp.write_text(clean_entire_text(rp.read_text(encoding="utf-8")), encoding="utf-8")

# Rebuild search indexes
for b in ["lop-10", "lop-11", "lop-12"]:
    lp = ROOT / "data" / f"lessons-{b}.json"
    sp = ROOT / "data" / f"search-{b}.json"
    lessons = json.loads(lp.read_text(encoding="utf-8"))
    search_data = []
    for item in lessons:
        clean_text = re.sub(r"<[^>]+>", " ", item.get("html", ""))
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        full_content = re.sub(r"\s+", " ", f"{item.get('group', '')} {item.get('title', '')} {clean_text}".strip())
        search_data.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "group": item.get("group"),
            "startPage": item.get("startPage", 1),
            "content": full_content
        })
    sp.write_text(json.dumps(search_data, ensure_ascii=False, indent=2), encoding="utf-8")

print("All OCR fixes successfully applied across books and search indexes!")
