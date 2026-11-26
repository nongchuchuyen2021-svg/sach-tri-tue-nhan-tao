import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LESSONS_DIR = ROOT / "lessons"

EXHAUSTIVE_REPLACEMENTS = [
    # Specific OCR misspellings found in Grade 11
    (r'\bbáo chỉ\b', 'báo chí'),
    (r'\bhệ thóng hoa\b', 'hệ thống hóa'),
    (r'\bhệ thóng\b', 'hệ thống'),
    (r'\bhệ thông\b', 'hệ thống'),
    (r'\bcó thé\b', 'có thể'),
    (r'\bcó thế\b', 'có thể'),
    (r'\bphỏng vẫn\b', 'phỏng vấn'),
    (r'\bvấn để\b', 'vấn đề'),
    (r'\bvân đề\b', 'vấn đề'),
    (r'\bvấn đê\b', 'vấn đề'),
    (r'\bvân đê\b', 'vấn đề'),
    (r'\bvẫn đề\b', 'vấn đề'),
    (r'\btử thực tiền\b', 'từ thực tiễn'),
    (r'\bthực tiền\b', 'thực tiễn'),
    (r'\bbô sung\b', 'bổ sung'),
    (r'\bkhông khi\b', 'không khí'),
    (r'\bkhi hậu\b', 'khí hậu'),
    (r'\bThanh thây\b', 'Thanh thấy'),
    (r'\btim hiêu\b', 'tìm hiểu'),
    (r'\bhiêu biết\b', 'hiểu biết'),
    (r'\bhiếu rõ\b', 'hiểu rõ'),
    (r'\bhiều biết\b', 'hiểu biết'),
    (r'\bhiều\b', 'hiểu'),
    (r'\bbáo cảo\b', 'báo cáo'),
    (r'\bbảng hòi\b', 'bảng hỏi'),
    (r'\buy tin\b', 'uy tín'),
    (r'\bCống thông tin\b', 'Cổng thông tin'),
    (r'\bđầy đù\b', 'đầy đủ'),
    (r'\btim ra\b', 'tìm ra'),
    (r'\btim kiếm\b', 'tìm kiếm'),
    (r'\bngười dung\b', 'người dùng'),
    (r'\bkhóng càn\b', 'không cần'),
    (r'\bkhóng\b', 'không'),
    (r'\bcàn cung cấp\b', 'cần cung cấp'),
    (r'\blưu trừ\b', 'lưu trữ'),
    (r'\bcác cập\b', 'các cặp'),
    (r'\bcâu hòi\b', 'câu hỏi'),
    (r'\bthống tin\b', 'thông tin'),
    (r'\bNhờ đỏ\b', 'Nhờ đó'),
    (r'\bxừ lí\b', 'xử lí'),
    (r'\bMang nơ-ron\b', 'Mạng nơ-ron'),
    (r'\bmang nơ-ron\b', 'mạng nơ-ron'),
    (r'\bchuối tư duy\b', 'chuỗi tư duy'),
    (r'\bphương trinh\b', 'phương trình'),
    (r'\bchương trinh\b', 'chương trình'),
    (r'\btheo A:\b', 'theo Δ:'),
    (r'\bself-altention\b', 'self-attention'),
    (r'\bTranformer\b', 'Transformer'),
    (r'\bdứ liệu\b', 'dữ liệu'),
    (r'\bDừ liệu\b', 'Dữ liệu'),
    (r'\bmô phòng\b', 'mô phỏng'),
    (r'\bbáng cách\b', 'bằng cách'),
    (r'\bmính họạ\b', 'minh họa'),
    (r'\bđày mô tả\b', 'đây mô tả'),
    (r'Các tế bào thầnCác nút nơ-ron', 'Các nút nơ-ron'),
    (r'\btiêp nhận\b', 'tiếp nhận'),
    (r'\bTin hiệu đầu\b', 'Tín hiệu đầu'),
    (r'\btiên tiền\b', 'tiên tiến'),
    (r'\bCàm xúc\b', 'Cảm xúc'),
    (r'\bGiài tri\b', 'Giải trí'),
    (r'\bchia khoa\b', 'chìa khóa'),
    (r'\bmặt phầng\b', 'mặt phẳng'),
    (r'\bhang chục\b', 'hàng chục'),
    (r'\blắn át\b', 'lấn át'),
    (r'\btât cả\b', 'tất cả'),
    (r'\btiêu chi\b', 'tiêu chí'),
    (r'\btương đong\b', 'tương đồng'),
    (r'\btương đông\b', 'tương đồng'),
    (r'\bvệ chung\b', 'về chung'),
    (r'\bhinh dạng\b', 'hình dạng'),
    (r'\bđiểm nhiều\b', 'điểm nhiễu'),
    (r'\bthi cho rằng\b', 'thì cho rằng'),
    (r'\bcụm lá\b', 'cụm là'),
    (r'\bKhởí động\b', 'Khởi động'),
    (r'\bđạo dúr\b', 'đạo đức'),
    (r'\bvẫn hóa\b', 'văn hóa'),
    (r'\bbc hai\b', 'bậc hai'),
    (r'\bXoa hai dầu\b', 'Xóa hai dấu'),
    (r'\bxoa hai dầu\b', 'xóa hai dấu'),
    (r'\bImager\b', 'Imagen'),
    (r'\bHãy xoa bớt\b', 'Hãy xóa bớt'),
    (r'\bnhân tổ hợp\b', 'nhấn tổ hợp'),
    (r'\btext-lo-image\b', 'text-to-image'),
    (r'\bimage-lo-image\b', 'image-to-image'),
    (r'\bchi sử dụng\b', 'chỉ sử dụng'),
    (r'\bành gốc\b', 'ảnh gốc'),
    (r'\btiếng ổn\b', 'tiếng ồn'),
    (r'\bphù định\b', 'phủ định'),
    (r'\btừ khoa\b', 'từ khóa'),
    (r'\bkịch bàn\b', 'kịch bản'),
    (r'\bchuyên động\b', 'chuyển động'),
    (r'\bchât lượng\b', 'chất lượng'),
    (r'\bkíp thời\b', 'kịp thời'),
    (r'\bchí phí\b', 'chi phí'),
    (r'\bchùng ta\b', 'chúng ta'),
    (r'\bmáy tinh\b', 'máy tính'),
    (r'\bthị giác máy tinh\b', 'thị giác máy tính'),
    (r'\bxử lI\b', 'xử lí'),
    (r'\bxử li\b', 'xử lí'),
    (r'\bhợp li\b', 'hợp lí'),
    (r'\bnguyên li\b', 'nguyên lí'),
    (r'\bquản li\b', 'quản lí'),
    (r'\bchu ki\b', 'chu kì'),
    (r'\bđịnh ki\b', 'định kì'),
    (r'\bđăng ki\b', 'đăng kí'),
    (r'\bbất ki\b', 'bất kì'),
    (r'\btiêu chuân\b', 'tiêu chuẩn'),
    (r'\bchính xac\b', 'chính xác'),
    (r'\bphát triến\b', 'phát triển'),
    (r'\btống quát\b', 'tổng quát'),
    (r'\btư động\b', 'tự động'),
    (r'\blự động\b', 'tự động'),
    (r'\btư nhiên\b', 'tự nhiên'),
    (r'\bhọc tâp\b', 'học tập'),
    (r'\bluyện tâp\b', 'luyện tập'),
    (r'\bluyên tập\b', 'luyện tập'),
    (r'\bvận dung\b', 'vận dụng'),
    (r'\bvân dụng\b', 'vận dụng'),
    (r'DANT O', ''),
    (r'n cu thê, vi dac "Hày - \(025,-0\.0 \. 057, 26 - F0\.03, 0\. \.\., 0\.2\.\.', ''),
    (r'O7', ''),
    (r'Mre di tur col', ''),
    (r'T7 lĐ tưoơng lác nộ', ''),
    (r'ti cong ue st ding cs ir', ''),
    (r'Vieicure to ài Studio', ''),
    (r'Hình 12\.1, Video con lác dom Gry, las bäng LUV', 'Hình 12.1. Video con lắc đơn tạo bằng LLM'),
    (r'LLM có thể tạo video theo yêu cầu cia rgyh sung bằng prompt mô tả\. Tạo video bằng LLM giúp sảt kiêm', 'LLM có thể tạo video theo yêu cầu của người dùng bằng prompt mô tả. Tạo video bằng LLM giúp tiết kiệm'),
    (r'Ngoài việc tạo video bắng prompt mô tả, nguei dung con có the iso video từ möt hoặc nhiều ảnh tĩnh', 'Ngoài việc tạo video bằng prompt mô tả, người dùng còn có thể tạo video từ một hoặc nhiều ảnh tĩnh'),
    (r'Khi đó\. LUM sẽ trêm sự chuyển đặng vào', 'Khi đó, LLM sẽ thêm sự chuyển động vào'),
    (r'Việc sử dụng ảnh tinin khi tạo video', 'Việc sử dụng ảnh tĩnh khi tạo video'),
    (r'Welcame b RiSudo', '')
]

def apply_replacements(text):
    if not text:
        return text
    current = text
    for pat, repl in EXHAUSTIVE_REPLACEMENTS:
        current = re.sub(pat, repl, current)
    return current

def clean_data_structure(data):
    if isinstance(data, str):
        return apply_replacements(data)
    elif isinstance(data, list):
        return [clean_data_structure(it) for it in data]
    elif isinstance(data, dict):
        return {k: clean_data_structure(v) for k, v in data.items()}
    return data

# Process Lop 11, Lop 10, Lop 12
for b in ["lop-11", "lop-10", "lop-12"]:
    lp = DATA_DIR / f"lessons-{b}.json"
    with open(lp, encoding="utf-8") as f:
        data = json.load(f)
    cleaned = clean_data_structure(data)
    with open(lp, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"Exhaustive cleaned {lp}")
    
    html_dir = LESSONS_DIR / b
    if html_dir.exists():
        for html_file in html_dir.glob("*.html"):
            c = html_file.read_text(encoding="utf-8")
            cc = apply_replacements(c)
            html_file.write_text(cc, encoding="utf-8")
    print(f"Exhaustive cleaned HTMLs in {html_dir}")

bp = DATA_DIR / "books.json"
with open(bp, encoding="utf-8") as f:
    bdata = json.load(f)
cleaned_b = clean_data_structure(bdata)
with open(bp, "w", encoding="utf-8") as f:
    json.dump(cleaned_b, f, ensure_ascii=False, indent=2)
print("Exhaustive cleaned books.json")

# Rebuild search indexes
from master_deep_fix import rebuild_search_indexes
rebuild_search_indexes()
print("All files cleaned and indexes rebuilt successfully!")
