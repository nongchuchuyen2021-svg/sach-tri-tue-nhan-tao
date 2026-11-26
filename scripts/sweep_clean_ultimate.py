import json
import re
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Sweep replacements
replacements = [
    # Universal string replacements
    ("Trí tuê nhân tạo", "Trí tuệ nhân tạo"),
    ("Trí tuê", "Trí tuệ"),
    ("Thực bạng,", "Thực trạng,"),
    ("Thực bạng", "Thực trạng"),
    ("Mô hình tỉnh chinh", "Mô hình tinh chỉnh"),
    ("tỉnh chinh", "tinh chỉnh"),
    ("Đảm bào tỉnh khách quan", "Đảm bảo tính khách quan"),
    ("View AIl Blocks", "View All Blocks"),
    ("Generato HTML", "Generator HTML"),
    ("Ganerate Asset", "Generate Asset"),
    ("tạo ănh", "tạo ảnh"),
    ("cửa niển. có thể kết hợp thêm lòi thoai roir. tiểu cảm nhân vật để tâng tirin tre yet phuc",
     "Diễn biến: Có thể kết hợp thêm lời thoại, biểu cảm nhân vật để tăng tính thuyết phục."),
    ("met cárt,", "một cách rõ ràng,"),
    ("Mang 4 trong dàu chuyện của bạn Linh", "Trang 4 trong câu chuyện của bạn Linh"),
    ("ảnhh", "ảnh"),
    ("tình bạng", "tình trạng"),
    ("thực bạng", "thực trạng"),
    ("bạng thái", "trạng thái"),
    ("chủ đề llên", "chủ đề liên"),
    ("llên quan", "liên quan"),
    ("sinh hoặt", "sinh hoạt"),
    ("Khới động", "Khởi động"),
    ("khen ngọi", "khen ngợi"),
    ("ngọi.", "ngợi."),
    ("hiện lưyng", "hiện tượng"),
    ("lưyng.", "lượng."),
    ("hoậc mù rông kì ráng", "hoặc mở rộng kĩ năng"),
    ("hoậc", "hoặc"),
    ("mù rông", "mở rộng"),
    ("kì ráng", "kĩ năng"),
    ("trỏi chảy", "trôi chảy"),
    ("Sau bảl học này, em sẻ:", "Sau bài học này, em sẽ:"),
    ("Sau bảl học này", "Sau bài học này"),
    ("em sẻ:", "em sẽ:"),
    ("bảl học", "bài học"),
    ("bất kì câ nhân", "bất kì cá nhân"),
    ("câ nhân", "cá nhân"),
    ("Trong kà nguyên AI, oông dân số", "Trong kỉ nguyên AI, công dân số"),
    ("kà nguyên AI", "kỉ nguyên AI"),
    ("oông dân số", "công dân số"),
    ("nên/khỏng", "nên/không"),
    ("đăng kị quyền", "đăng kí quyền"),
    ("đăng kị", "đăng kí"),
    ("Hệ thưng tường tht Mội thoai Buot thệt", "Hệ thống tương tác Hội thoại Chatbot"),
    ("Hệ thưng", "Hệ thống"),
    ("Mội thoai", "Hội thoại"),
    ("Buot thệt", "Chatbot"),
    ("phát triên", "phát triển"),
    ("lệu đã chuẩn bì", "liệu đã chuẩn bị"),
    ("chuẩn bì", "chuẩn bị"),
    ("của nhồm của họ", "của nhóm của họ"),
    ("nhồm của họ", "nhóm của họ"),
    ("thông tín về", "thông tin về"),
    ("thông tín", "thông tin"),
    ("thành mộn chi mus (oner)", "thành một chỉ mục (index)"),
    ("thành mộn chi mus", "thành một chỉ mục"),
    ("mộn chi mus", "một chỉ mục"),
    ("Generative AIl", "Generative AI"),
    ("Generato Agent", "Generator Agent"),
    ("KHÁM PHẨ", "KHÁM PHÁ"),
    ("Tin kiêm thông tin sên quan tự trớc miội caa đính xác và nhanh chống",
     "Tìm kiếm thông tin liên quan từ trước một cách chính xác và nhanh chóng"),
    ("sên quan", "liên quan"),
    ("miội caa đính xác", "một cách chính xác"),
    ("nhanh chống", "nhanh chóng"),
    ("phong cách rèng", "phong cách riêng"),
    ("có lrách nhiệm", "có trách nhiệm"),
    ("lrách nhiệm", "trách nhiệm"),
    ("ngày hồm qua", "ngày hôm qua"),
    ("hồm qua", "hôm qua"),
    ("phú hợp cề trế hiện được mach truyện", "phù hợp để thể hiện được mạch truyện"),
    ("cề trế hiện", "để thể hiện"),
    ("mach truyện", "mạch truyện"),
    ("cárt truyện", "các trang truyện"),
    ("niển biến", "diễn biến"),
    ("roir dung", "nội dung"),
    ("tirin cảm", "tình cảm"),
    ("của câu chiuyện", "của câu chuyện"),
    ("bắt dàu", "bắt đầu"),
    ("Bude 6", "Bước 6"),
    ("rtuyện tranh", "truyện tranh"),
    ("bbi cánh", "bối cảnh"),
    ("Giu đinh cuông", "Gia đình chuộng"),
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
    ("kháchhhh hàng", "khách hàng"),
    ("kháchhhh", "khách"),
    ("UX/UI co bán", "UX/UI cơ bản"),
    ("tính loán", "tính toán"),
    ("bài loán", "bài toán"),
]

def clean_text_thoroughly(text):
    if not isinstance(text, str):
        return text
    for old, new in replacements:
        text = text.replace(old, new)
    # Regex fallback
    text = re.sub(r"\bảnhh\b", "ảnh", text, flags=re.IGNORECASE)
    text = re.sub(r"\bPrompt\s+co\s+bán\b", "Prompt cơ bản", text, flags=re.IGNORECASE)
    text = re.sub(r"\bprompt\s+co\s+bản\b", "prompt cơ bản", text, flags=re.IGNORECASE)
    text = re.sub(r"\bco\s+bản\b", "cơ bản", text, flags=re.IGNORECASE)
    text = re.sub(r"\bchương\s+trinh\b", "chương trình", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(Hinh|hinh)\s+(\d+\.\d+)", r"Hình \2", text)
    return text

def walk(obj):
    if isinstance(obj, dict):
        return {k: walk(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [walk(item) for item in obj]
    elif isinstance(obj, str):
        return clean_text_thoroughly(obj)
    return obj

# 1. Update books.json
bp = ROOT / "data" / "books.json"
b_data = json.loads(bp.read_text(encoding="utf-8"))
bp.write_text(json.dumps(walk(b_data), ensure_ascii=False, indent=2), encoding="utf-8")

# 2. Update lessons JSON
for b in ["lop-10", "lop-11", "lop-12"]:
    lp = ROOT / "data" / f"lessons-{b}.json"
    l_data = json.loads(lp.read_text(encoding="utf-8"))
    lp.write_text(json.dumps(walk(l_data), ensure_ascii=False, indent=2), encoding="utf-8")

# 3. Update all HTML files
for hf in glob.glob(str(ROOT / "lessons" / "*" / "*.html")):
    p = Path(hf)
    p.write_text(clean_text_thoroughly(p.read_text(encoding="utf-8")), encoding="utf-8")

for rf in ["index.html", "reader.html"]:
    rp = ROOT / rf
    if rp.exists():
        rp.write_text(clean_text_thoroughly(rp.read_text(encoding="utf-8")), encoding="utf-8")

# 4. Rebuild search indexes
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

print("Sweep clean completed!")
