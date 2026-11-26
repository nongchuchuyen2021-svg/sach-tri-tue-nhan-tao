import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Comprehensive list of regex replacement rules (ordered logically)
CORRECTIONS = [
    # --- 1. Character & Punctuation Cleanup ---
    (r";", ";"),
    (r"\xad", ""),  # strip soft hyphens
    
    # --- 2. Stray OCR Artifacts & Page Noise ---
    (r"<p class=\"lesson-p\">\s*10\s+11\s*</p>", ""),
    (r"<p class=\"lesson-p\">\s*0\"\s*o\s*c-?\s*</p>", ""),
    (r"<p class=\"lesson-p\">\s*:\s*Mf\s*Workspace\s*</p>", ""),
    (r"<p class=\"lesson-p\">\s*Mr\s*Workspare\s*</p>", ""),
    (r"<p class=\"lesson-p\">\s*\.35\s*</p>", ""),
    (r"n\s+t\s+vàng\s+cug\s+tưnn\s+tang\s+lử\s+nửn\s*\.\s*", ""),
    (r"<p class=\"lesson-p\">\s*CS\s*CamScanner\s*</p>", ""),

    # --- 3. User Reported & Core Tech Terms ---
    (r"\bcông củ AI\b", "công cụ AI"),
    (r"\bcông củ\b", "công cụ"),
    (r"\bA/\s*lạo\s*sinh\b", "AI tạo sinh"),
    (r"\bAl\s*lạo\s*sinh\b", "AI tạo sinh"),
    (r"\bAI\s*lạo\s*sinh\b", "AI tạo sinh"),
    (r"\bAi\s*lạo\s*sinh\b", "AI tạo sinh"),
    (r"\bAi\s*thô\s*hệ\s*trước\b", "AI thế hệ trước"),
    (r"\bAI\s*thô\s*hệ\s*trước\b", "AI thế hệ trước"),
    (r"\bAi\s*thể\s*hệ\s*trước\b", "AI thế hệ trước"),
    (r"\bAI\s*thể\s*hệ\s*trước\b", "AI thế hệ trước"),
    (r"\bAi\s*thế\s*hệ\s*trước\b", "AI thế hệ trước"),
    (r"\bAi\s*thế\s*hệ\b", "AI thế hệ"),
    (r"\bAi\s*thể\s*hệ\b", "AI thế hệ"),
    (r"\bAi\s*thô\s*hệ\b", "AI thế hệ"),
    (r"\bAI\s*thô\s*hệ\b", "AI thế hệ"),
    (r"\bAI\s*thể\s*hệ\b", "AI thế hệ"),
    (r"\bA/\s*lạo\b", "AI tạo"),
    (r"\bA/\s*cho\b", "AI cho"),
    (r"\bA/\s*với\b", "AI với"),
    (r"\bChatQPT\b", "ChatGPT"),
    (r"\bCopilol\b", "Copilot"),
    (r"\bSưno AI\b", "Suno AI"),
    (r"\bSưno A/\b", "Suno AI"),
    (r"\bSuno A/\b", "Suno AI"),
    (r"\bSuno Al\b", "Suno AI"),
    (r"\bopenal\.com\b", "openai.com"),
    (r"\bCraiyon\.\.\.\.", "Craiyon,..."),
    (r"\bColaboralory\b", "Colaboratory"),
    (r"\bIkagglelinput\b", "/kaggle/input"),
    (r"\bLlamalndex\b", "LlamaIndex"),
    (r"\bIlama-index\b", "llama-index"),
    (r"\bIlama\b", "llama"),
    (r"\bLocalhost:11434\b", "localhost:11434"),
    (r"\bLocaLhost:11434\b", "localhost:11434"),
    (r"\bA/\b", "AI"),
    
    # --- 4. "Tạo" and "Tạo sinh" OCR Variations ---
    (r"\btao ra\b", "tạo ra"),
    (r"\blạo ra\b", "tạo ra"),
    (r"\blạo sinh\b", "tạo sinh"),
    (r"\blạo hình ảnh\b", "tạo hình ảnh"),
    (r"\blạo hinh ánh\b", "tạo hình ảnh"),
    (r"\blạo hình\b", "tạo hình"),
    (r"\blạo nên\b", "tạo nên"),
    (r"\blạo thành\b", "tạo thành"),
    (r"\blạo vector\b", "tạo vector"),
    (r"\bTao một\b", "Tạo một"),
    (r"\btao một\b", "tạo một"),
    (r"\btao vector\b", "tạo vector"),
    (r"\btao embedding\b", "tạo embedding"),
    (r"\btao embeuding\b", "tạo embedding"),
    (r"\bsáng lạo\b", "sáng tạo"),
    (r"\bsáng tao\b", "sáng tạo"),
    (r"\bnhân lạo\b", "nhân tạo"),
    (r"\bnhân tao\b", "nhân tạo"),
    (r"\bkhởi tao\b", "khởi tạo"),
    (r"\bkhởi lạo\b", "khởi tạo"),
    (r"\btự tao\b", "tự tạo"),
    (r"\btự lạo\b", "tự tạo"),
    (r"\bthể lạo\b", "thể tạo"),
    (r"\bthể tao\b", "thể tạo"),
    (r"\bđược lạo\b", "được tạo"),
    (r"\bđược tao\b", "được tạo"),
    (r"\bvề tao\b", "về tạo"),
    (r"\bvề lạo\b", "về tạo"),
    (r"\bcần tao\b", "cần tạo"),
    (r"\bcần lạo\b", "cần tạo"),
    (r"\bvà tao\b", "và tạo"),
    (r"\bvà lạo\b", "và tạo"),
    (r"\bđể lạo\b", "để tạo"),
    (r"\bđể tao\b", "để tạo"),
    (r"\bBước lạo\b", "Bước tạo"),
    (r"\bbước lạo\b", "bước tạo"),
    (r"\bHãy lạo\b", "Hãy tạo"),
    (r"\bHãy tao\b", "Hãy tạo"),
    (r"\bStudio lạo\b", "Studio tạo"),
    (r"\bthống lạo\b", "thống tạo"),
    (r"\bquả lạo\b", "quả tạo"),
    (r"\bAI tao\b", "AI tạo"),
    (r"\bAl tao\b", "AI tạo"),
    (r"\bAI lạo\b", "AI tạo"),
    (r"\bAl lạo\b", "AI tạo"),

    # --- 5. "lí" / "lý" and "trợ lí" Words ---
    (r"\bxử Ií\b", "xử lí"),
    (r"\bxử lĩ\b", "xử lí"),
    (r"\btrợ !í\b", "trợ lí"),
    (r"\btrợ Ií\b", "trợ lí"),
    (r"\btrợ lí áo\b", "trợ lí ảo"),
    (r"\bkiện Ií\b", "kiện lí"),
    (r"\bhợp Ií\b", "hợp lí"),
    (r"\bquản Ií\b", "quản lí"),
    (r"\bvật Ií\b", "vật lí"),
    (r"\btâm Ií\b", "tâm lí"),
    (r"\bđịa Ií\b", "địa lí"),
    (r"\bpháp Ií\b", "pháp lí"),
    (r"\blí thuyết\b", "lí thuyết"),

    # --- 6. "-hóa" Typos (hóá -> hóa) ---
    (r"\btối ưu hóá\b", "tối ưu hóa"),
    (r"\bTối ưu hóá\b", "Tối ưu hóa"),
    (r"\bhiện thực hóá\b", "hiện thực hóa"),
    (r"\bmã hóá\b", "mã hóa"),
    (r"\bchuẩn hóá\b", "chuẩn hóa"),
    (r"\btự động hóá\b", "tự động hóa"),
    (r"\bhàng hóá\b", "hàng hóa"),
    (r"\btạp hóá\b", "tạp hóa"),
    (r"\bhóá đơn\b", "hóa đơn"),
    (r"\bhóá ý tưởng\b", "hóa ý tưởng"),
    (r"\bkhóá học\b", "khóa học"),
    (r"\bcuối khóá\b", "cuối khóa"),
    (r"\bmở khóá\b", "mở khóa"),

    # --- 7. "Bảng" and "Bài" Typos ---
    (r"\bBải (\d+)\b", r"Bài \1"),
    (r"\bBẢI (\d+)\b", r"BÀI \1"),
    (r"\bBòi (\d+)\b", r"Bài \1"),
    (r"\bBal (\d+)\b", r"Bài \1"),
    (r"\bBàng (\d+)\b", r"Bảng \1"),
    (r"\bBÀNG (\d+)\b", r"BẢNG \1"),
    (r"\bvẽ một bằng\b", "vẽ một bảng"),
    (r"\bvẽ bằng\b", "vẽ bảng"),
    (r"\bbằng gồm hai cột\b", "bảng gồm hai cột"),
    (r"\bbằng gồm (\d+) cột\b", r"bảng gồm \1 cột"),
    (r"\bđiền vào bằng\b", "điền vào bảng"),
    (r"\blập bằng\b", "lập bảng"),
    (r"\bbằng so sánh\b", "bảng so sánh"),
    (r"\bhai bằng\b", "hai bảng"),

    # --- 8. Specific Vietnamese Diacritic OCR Fixes ---
    (r"\bmó tả\b", "mô tả"),
    (r"\bmô lả\b", "mô tả"),
    (r"\bhộ thông\b", "hệ thống"),
    (r"\bhệ thông\b", "hệ thống"),
    (r"\blương ứng\b", "tương ứng"),
    (r"\bkhả náng\b", "khả năng"),
    (r"\bhinh ành\b", "hình ảnh"),
    (r"\bhình ành\b", "hình ảnh"),
    (r"\bhinh ảnh\b", "hình ảnh"),
    (r"\bHình ành\b", "Hình ảnh"),
    (r"\bbức ành\b", "bức ảnh"),
    (r"\bkết quá\b", "kết quả"),
    (r"\bkết qua\b", "kết quả"),
    (r"\bcủng một\b", "cùng một"),
    (r"\bcủng lúc\b", "cùng lúc"),
    (r"\bcủng với\b", "cùng với"),
    (r"\bcủng như\b", "cùng như"),
    (r"\bthuận liện\b", "thuận tiện"),
    (r"\btrọng đó\b", "trong đó"),
    (r"\btrọng các\b", "trong các"),
    (r"\btrọng việc\b", "trong việc"),
    (r"\btrọng một\b", "trong một"),
    (r"\btrọng khi\b", "trong khi"),
    (r"\bngười thần\b", "người thân"),
    (r"\bbạn bẻ\b", "bạn bè"),
    (r"\bđổi tượng\b", "đối tượng"),
    (r"\bthực hiên\b", "thực hiện"),
    (r"\bThực hiên\b", "Thực hiện"),
    (r"\bphát triền\b", "phát triển"),
    (r"\bPhát triền\b", "Phát triển"),
    (r"\btiến triền\b", "tiến triển"),
    (r"\btriền khai\b", "triển khai"),
    (r"\blâm việc\b", "làm việc"),
    (r"\bnhiều lâm!\b", "nhiều lắm!"),
    (r"\bnhiều lâm\b", "nhiều lắm"),
    (r"\bquan lâm\b", "quan tâm"),
    (r"\bmạnh khoe\b", "mạnh khỏe"),
    (r"\bsức khoe\b", "sức khỏe"),
    (r"\bnu cười\b", "nụ cười"),
    (r"\bvừng chúc\b", "vững chắc"),
    (r"\brô ráng\b", "rõ ràng"),
    (r"\bhiền thị\b", "hiển thị"),
    (r"\bHiền thị\b", "Hiển thị"),
    (r"\báp phích tuyến truyền\b", "áp phích tuyên truyền"),
    (r"\bbiều tượng\b", "biểu tượng"),
    (r"\bmiaro\b", "micro"),
    (r"\bđổi diện\b", "đối diện"),
    (r"\bđam mề\b", "đam mê"),
    (r"\bchù để\b", "chủ đề"),
    (r"\bChù để\b", "Chủ đề"),
    (r"\bcẩm sách\b", "cầm sách"),
    (r"\bdúng ý\b", "đúng ý"),
    (r"\bhoàn chính\b", "hoàn chỉnh"),
    (r"\bkhiểm tra\b", "kiểm tra"),
    (r"\bxoa,\.\.\.\b", "xoá,..."),
    (r"\bcắt, dẫn\b", "cắt, dán"),
    (r"\bHiến thị/ần\b", "Hiển thị/ẩn"),
    (r"\bbắt kì\b", "bất kì"),
    (r"\bbài thuyêt trình\b", "bài thuyết trình"),
    (r"\bchúc mùng\b", "chúc mừng"),
    (r"\bhọp phim\b", "hợp phím"),
    (r"\btổ họp\b", "tổ hợp"),
    (r"\bphim Shift\b", "phím Shift"),
    (r"\bphim Enter\b", "phím Enter"),
    (r"\bsổ ta\b", "sổ tay"),
    (r"\blưu trứ\b", "lưu trữ"),
    (r"\bkhia cạnh\b", "khía cạnh"),
    (r"\bthúc đầy\b", "thúc đẩy"),
    (r"\bthừ nghiệm\b", "thử nghiệm"),
    (r"\bThừ nghiệm\b", "Thử nghiệm"),
    (r"\bTrách nhiệmgiải\b", "Trách nhiệm giải"),
    (r"\bđọc kT lại\b", "đọc kĩ lại"),
    (r"\bđọc kT\b", "đọc kĩ"),
    (r"\bthông tín trên mạng\b", "thông tin trên mạng"),
    (r"\bphiều của\b", "phiếu của"),
    (r"\bkhi thải\b", "khí thải"),
    (r"\bthiên nhiền\b", "thiên nhiên"),
    (r"\btoà nhiệt\b", "tỏa nhiệt"),
    (r"\btiêu tồn\b", "tiêu tốn"),
    (r"\bnưóc\b", "nước"),
    (r"\bđặc biêt\b", "đặc biệt"),
    (r"\bvăn hoá\b", "văn hóa"),
    (r"\bcổ máy\b", "cỗ máy"),
    (r"\bnhấm đúng\b", "nhắm đúng"),
    (r"\bnhỏ var bin\b", "nhỏ văn bản"),
    (r"\bkiểm từ sóm\b", "kiểm thử sớm"),
    (r"\bTạo luông\b", "Tạo luồng"),
    (r"\bTạo luong\b", "Tạo luồng"),
    (r"\bdũ liệu\b", "dữ liệu"),
    (r"\bthông bảo lỏi\b", "thông báo lỗi"),
    (r"\bbò sót\b", "bỏ sót"),
    (r"\bban muốn AI\b", "bạn muốn AI"),
    (r"\bbiếu đò\b", "biểu đồ"),
    (r"\bthích nghỉ\b", "thích nghi"),
    (r"\brèn kĩ náng\b", "rèn kĩ năng"),
    (r"\bmở rông kì ráng\b", "mở rộng kĩ năng"),
    (r"\bthay dổi the giới\b", "thay đổi thế giới"),
    (r"\btinh chình\b", "tinh chỉnh"),
    (r"\bthách thức Cohei\b", "thách thức Cơ hội"),
    (r"\bquy trinh\b", "quy trình"),
    (r"\bnhập củng\b", "nhập cùng"),
    (r"\bmô tà\b", "mô tả"),
    (r"\bhinh ánh\b", "hình ảnh"),
    (r"\bnhiêm vu\b", "nhiệm vụ"),
    (r"\bvăn bàn\b", "văn bản"),
    (r"\bThực hành lạo\b", "Thực hành tạo"),
    (r"\bhướng dẫn lạo\b", "hướng dẫn tạo"),

    # --- 9. Covers & Publishing Info ---
    (r"\bTRÍ TUỂ NHÂN TAO\b", "TRÍ TUỆ NHÂN TẠO"),
    (r"\bTRÍ TUẾ NHÂN TAO\b", "TRÍ TUỆ NHÂN TẠO"),
    (r"\bTẢI TUE NHÂN TAO\b", "TRÍ TUỆ NHÂN TẠO"),
    (r"\bLÓP 10\b", "LỚP 10"),
    (r"\bTÓP 10\b", "LỚP 10"),
    (r"\bLÓP 11\b", "LỚP 11"),
    (r"\bTÓP 11\b", "LỚP 11"),
    (r"\bLÓP 12\b", "LỚP 12"),
    (r"\bTÓP 12\b", "LỚP 12"),
]

def apply_clean(text):
    if not text:
        return text
    for pat, rep in CORRECTIONS:
        text = re.sub(pat, rep, text)
    return text

total_edits = 0

# 1. Process lessons JSON files and HTML files for all 3 books
for grade in ["lop-10", "lop-11", "lop-12"]:
    json_path = ROOT / "data" / f"lessons-{grade}.json"
    html_dir = ROOT / "lessons" / grade
    
    data = json.load(open(json_path, encoding="utf-8"))
    grade_edits = 0
    
    for les in data:
        # Title
        old_title = les.get("title", "")
        new_title = apply_clean(old_title)
        if new_title != old_title:
            les["title"] = new_title
            grade_edits += 1
            
        # Summary
        old_sum = les.get("summary", "")
        new_sum = apply_clean(old_sum)
        if new_sum != old_sum:
            les["summary"] = new_sum
            grade_edits += 1
            
        # Group
        old_grp = les.get("group", "")
        new_grp = apply_clean(old_grp)
        if new_grp != old_grp:
            les["group"] = new_grp
            grade_edits += 1

        # HTML
        old_html = les.get("html", "")
        new_html = apply_clean(old_html)
        if new_html != old_html:
            les["html"] = new_html
            grade_edits += 1
            
        # Also write individual HTML file
        lid = les["id"]
        html_file = html_dir / f"{lid}.html"
        if html_file.exists():
            f_content = html_file.read_text(encoding="utf-8")
            f_clean = apply_clean(f_content)
            if f_clean != f_content:
                html_file.write_text(f_clean, encoding="utf-8")
                
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"✓ Fixed {grade_edits} sections/fields in {grade} ({json_path.name})")
    total_edits += grade_edits

# 2. Process data/books.json
books_path = ROOT / "data" / "books.json"
books_data = json.load(open(books_path, encoding="utf-8"))
b_edits = 0
for b in books_data.get("books", []):
    b["title"] = apply_clean(b.get("title", ""))
    b["description"] = apply_clean(b.get("description", ""))
    for ch in b.get("chapters", []):
        ch["title"] = apply_clean(ch.get("title", ""))
        ch["desc"] = apply_clean(ch.get("desc", ""))

with open(books_path, "w", encoding="utf-8") as f:
    json.dump(books_data, f, ensure_ascii=False, indent=2)
print("✓ Synchronized data/books.json")

# 3. Re-build search indexes data/search-lop-*.json
for grade in ["lop-10", "lop-11", "lop-12"]:
    lessons_data = json.load(open(ROOT / "data" / f"lessons-{grade}.json", encoding="utf-8"))
    search_idx = []
    for les in lessons_data:
        # strip tags for index
        clean_text = re.sub(r"<[^>]+>", " ", les.get("html", ""))
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        search_idx.append({
            "id": les["id"],
            "title": les.get("title", ""),
            "group": les.get("group", ""),
            "startPage": les.get("startPage", 1),
            "content": clean_text[:4000] # indexed snippet
        })
    search_path = ROOT / "data" / f"search-{grade}.json"
    with open(search_path, "w", encoding="utf-8") as f:
        json.dump(search_idx, f, ensure_ascii=False, indent=2)
    print(f"✓ Re-indexed {search_path.name}")

print(f"\nCOMPLETED! Total of {total_edits} updates across all 3 books!")
