import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

lp = ROOT / "data" / "lessons-lop-11.json"
with open(lp, encoding="utf-8") as f:
    lessons = json.load(f)

# Regex patterns for subtle misspellings in Vietnamese
PATTERNS = [
    (r'\bngười\s+dung\b', 'người dùng'),
    (r'\bkhóng\s+càn\b', 'không cần'),
    (r'\bkhóng\b', 'không'),
    (r'\blưu\s+trừ\b', 'lưu trữ'),
    (r'\bcác\s+cập\b', 'các cặp'),
    (r'\bthống\s+tin\b', 'thông tin'),
    (r'\bbáo\s+chỉ\b', 'báo chí'),
    (r'\bhệ\s+thóng\s+hoa\b', 'hệ thống hóa'),
    (r'\bhệ\s+thóng\b', 'hệ thống'),
    (r'\bhệ\s+thông\b', 'hệ thống'),
    (r'\bcó\s+thé\b', 'có thể'),
    (r'\bphỏng\s+vẫn\b', 'phỏng vấn'),
    (r'\bvấn\s+để\b', 'vấn đề'),
    (r'\bvân\s+đề\b', 'vấn đề'),
    (r'\bvấn\s+đê\b', 'vấn đề'),
    (r'\bvân\s+đê\b', 'vấn đề'),
    (r'\bchí\s+phí\b', 'chi phí'),
    (r'"hiều"', '"hiểu"'),
    (r'\bhiều\b', 'hiểu'),
    (r'\bchùng\s+ta\b', 'chúng ta'),
    (r'\bthị\s+giác\s+máy\s+tinh\b', 'thị giác máy tính'),
    (r'\bmáy\s+tinh\b', 'máy tính'),
    (r'\bxử\s+lI\b', 'xử lí'),
    (r'\bxử\s+li\b', 'xử lí'),
    (r'\bhợp\s+li\b', 'hợp lí'),
    (r'\bnguyên\s+lí\b', 'nguyên lí'),
    (r'\bnguyên\s+li\b', 'nguyên lí'),
    (r'\bquản\s+lí\b', 'quản lí'),
    (r'\bquản\s+li\b', 'quản lí'),
    (r'\bchu\s+kì\b', 'chu kì'),
    (r'\bchu\s+ki\b', 'chu kì'),
    (r'\bđịnh\s+kì\b', 'định kì'),
    (r'\bđịnh\s+ki\b', 'định kì'),
    (r'\bđăng\s+kí\b', 'đăng kí'),
    (r'\bđăng\s+ki\b', 'đăng kí'),
    (r'\bbất\s+kì\b', 'bất kì'),
    (r'\bbất\s+ki\b', 'bất kì'),
    (r'\bphương\s+trinh\b', 'phương trình'),
    (r'\bchương\s+trinh\b', 'chương trình'),
    (r'\btheo\s+A:\b', 'theo Δ:'),
    (r'\bNhờ\s+đỏ\b', 'Nhờ đó'),
    (r'\bself-altention\b', 'self-attention'),
    (r'\bTranformer\b', 'Transformer'),
    (r'\bdứ\s+liệu\b', 'dữ liệu'),
    (r'\bDừ\s+liệu\b', 'Dữ liệu'),
    (r'\bmô\s+phòng\b', 'mô phỏng'),
    (r'\bbáng\s+cách\b', 'bằng cách'),
    (r'\bmính\s+họạ\b', 'minh họa'),
    (r'\bđày\s+mô\s+tả\b', 'đây mô tả'),
    (r'\bmang\s+nơ-ron\b', 'mạng nơ-ron'),
    (r'Các tế bào thầnCác nút nơ-ron', 'Các nút nơ-ron'),
    (r'\btiêp\s+nhận\b', 'tiếp nhận'),
    (r'\bTin\s+hiệu\s+đầu\b', 'Tín hiệu đầu'),
    (r'\btiên\s+tiền\b', 'tiên tiến'),
    (r'\bCàm\s+xúc\b', 'Cảm xúc'),
    (r'\bGiài\s+tri\b', 'Giải trí'),
    (r'\bchia\s+khoa\b', 'chìa khóa'),
    (r'\bmặt\s+phầng\b', 'mặt phẳng'),
    (r'\bhang\s+chục\b', 'hàng chục'),
    (r'\blắn\s+át\b', 'lấn át'),
    (r'\btât\s+cả\b', 'tất cả'),
    (r'\btiêu\s+chi\b', 'tiêu chí'),
    (r'\btương\s+đong\b', 'tương đồng'),
    (r'\btương\s+đông\b', 'tương đồng'),
    (r'\bvệ\s+chung\b', 'về chung'),
    (r'\bhinh\s+dạng\b', 'hình dạng'),
    (r'\bđiểm\s+nhiều\b', 'điểm nhiễu'),
    (r'\bthi\s+cho\s+rằng\b', 'thì cho rằng'),
    (r'\bcụm\s+lá\b', 'cụm là'),
    (r'\bKhởí\s+động\b', 'Khởi động'),
    (r'\bđạo\s+dúr\b', 'đạo đức'),
    (r'\bvẫn\s+hóa\b', 'văn hóa'),
    (r'\bbc\s+hai\b', 'bậc hai'),
    (r'\bcâu\s+hòi\b', 'câu hỏi'),
    (r'\bXoa\s+hai\s+dầu\b', 'Xóa hai dấu'),
    (r'\bxoa\s+hai\s+dầu\b', 'xóa hai dấu'),
    (r'\bImager\b', 'Imagen'),
    (r'\bHãy\s+xoa\s+bớt\b', 'Hãy xóa bớt'),
    (r'\bnhân\s+tổ\s+hợp\s+phím\b', 'nhấn tổ hợp phím'),
    (r'\btext-lo-image\b', 'text-to-image'),
    (r'\bimage-lo-image\b', 'image-to-image'),
    (r'\bchi\s+sử\s+dụng\b', 'chỉ sử dụng'),
    (r'\bành\s+gốc\b', 'ảnh gốc'),
    (r'\bkhông\s+khi\b', 'không khí'),
    (r'\bkhi\s+hậu\b', 'khí hậu'),
    (r'\btiếng\s+ổn\b', 'tiếng ồn'),
    (r'\bThanh\s+thây\b', 'Thanh thấy'),
    (r'\btim\s+hiêu\b', 'tìm hiểu'),
    (r'\bhiêu\s+biết\b', 'hiểu biết'),
    (r'\bbáo\s+cảo\b', 'báo cáo'),
    (r'\bbảng\s+hòi\b', 'bảng hỏi'),
    (r'\buy\s+tin\b', 'uy tín'),
    (r'\bCống\s+thông\s+tin\b', 'Cổng thông tin'),
    (r'\bđầy\s+đù\b', 'đầy đủ'),
    (r'\btim\s+ra\b', 'tìm ra'),
    (r'\btim\s+kiếm\b', 'tìm kiếm'),
    (r'\bchuối\s+tư\s+duy\b', 'chuỗi tư duy'),
    (r'\bphù\s+định\b', 'phủ định'),
    (r'\btừ\s+khoa\b', 'từ khóa'),
    (r'\bkịch\s+bàn\b', 'kịch bản'),
    (r'\bchuyên\s+động\b', 'chuyển động'),
    (r'\bchât\s+lượng\b', 'chất lượng'),
    (r'\bkíp\s+thời\b', 'kịp thời'),
    (r'\btiêu\s+chuân\b', 'tiêu chuẩn'),
    (r'\bchuân\b', 'chuẩn'),
    (r'\bchuần\b', 'chuẩn'),
    (r'\bchính\s+xac\b', 'chính xác'),
    (r'\bchinh\s+xác\b', 'chính xác'),
    (r'\bphát\s+triến\b', 'phát triển'),
    (r'\btổng\s+quát\b', 'tổng quát'),
    (r'\btống\s+quát\b', 'tổng quát'),
    (r'\btự\s+động\b', 'tự động'),
    (r'\btư\s+động\b', 'tự động'),
    (r'\blự\s+động\b', 'tự động'),
    (r'\btự\s+nhiên\b', 'tự nhiên'),
    (r'\btư\s+nhiên\b', 'tự nhiên'),
    (r'\bhọc\s+tâp\b', 'học tập'),
    (r'\bluyện\s+tâp\b', 'luyện tập'),
    (r'\bluyên\s+tập\b', 'luyện tập'),
    (r'\bvận\s+dung\b', 'vận dụng'),
    (r'\bvân\s+dụng\b', 'vận dụng')
]

total_found = 0
for les in lessons:
    html = les.get("html", "")
    for pat, repl in PATTERNS:
        matches = list(re.finditer(pat, html, re.IGNORECASE))
        if matches:
            total_found += len(matches)
            for m in matches:
                start = max(0, m.start() - 30)
                end = min(len(html), m.end() + 30)
                snip = html[start:end].replace('\n', ' ')
                print(f"[{les['id']}] '{m.group(0)}' -> '{repl}' in ...{snip}...")

print(f"\n===> TOTAL MATCHES FOUND: {total_found}")
