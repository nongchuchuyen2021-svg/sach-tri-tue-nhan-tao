import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LESSONS_DIR = ROOT / "lessons"

TONE_PAIRS = [
    (r'\btrợ\s+thù\b', 'trợ thủ'),
    (r'\bbảng\s+cách\b', 'bằng cách'),
    (r'\bcần\s+thận\b', 'cẩn thận'),
    (r'\bthực\s+tiền\b', 'thực tiễn'),
    (r'\bbô\s+sung\b', 'bổ sung'),
    (r'\bbảo\s+cáo\b', 'báo cáo'),
    (r'\bbàn\s+đồ\b', 'bản đồ'),
    (r'\bsàn\s+phẩm\b', 'sản phẩm'),
    (r'\bbạn\s+bé\b', 'bạn bè'),
    (r'\bvè\s+nhà\b', 'về nhà'),
    (r'\bvè\s+sau\b', 'về sau'),
    (r'\bthực\s+hiên\b', 'thực hiện'),
    (r'\bphát\s+triên\b', 'phát triển'),
    (r'\btuân\s+thù\b', 'tuân thủ'),
    (r'\bvân\s+đề\b', 'vấn đề'),
    (r'\bvấn\s+để\b', 'vấn đề'),
    (r'\bhiêu\s+biết\b', 'hiểu biết'),
    (r'\bhiếu\s+rõ\b', 'hiểu rõ'),
    (r'\bhiều\s+biết\b', 'hiểu biết'),
    (r'\bhiều\b', 'hiểu'),
    (r'\btim\s+hiêu\b', 'tìm hiểu'),
    (r'\btim\s+kiếm\b', 'tìm kiếm'),
    (r'\btim\s+ra\b', 'tìm ra'),
    (r'\bđầy\s+đù\b', 'đầy đủ'),
    (r'\bbáo\s+cảo\b', 'báo cáo'),
    (r'\bbảng\s+hòi\b', 'bảng hỏi'),
    (r'\buy\s+tin\b', 'uy tín'),
    (r'\bCống\s+thông\s+tin\b', 'Cổng thông tin'),
    (r'\bngười\s+dung\b', 'người dùng'),
    (r'\bkhóng\s+càn\b', 'không cần'),
    (r'\bkhóng\b', 'không'),
    (r'\bcàn\s+cung\s+cấp\b', 'cần cung cấp'),
    (r'\blưu\s+trừ\b', 'lưu trữ'),
    (r'\bcác\s+cập\b', 'các cặp'),
    (r'\bcâu\s+hòi\b', 'câu hỏi'),
    (r'\bthống\s+tin\b', 'thông tin'),
    (r'\bNhờ\s+đỏ\b', 'Nhờ đó'),
    (r'\bxừ\s+lí\b', 'xử lí'),
    (r'\bMang\s+nơ-ron\b', 'Mạng nơ-ron'),
    (r'\bmang\s+nơ-ron\b', 'mạng nơ-ron'),
    (r'\bchuối\s+tư\s+duy\b', 'chuỗi tư duy'),
    (r'\bphương\s+trinh\b', 'phương trình'),
    (r'\bchương\s+trinh\b', 'chương trình'),
    (r'theo A:', 'theo Δ:'),
    (r'\bself-altention\b', 'self-attention'),
    (r'\bTranformer\b', 'Transformer'),
    (r'\bdứ\s+liệu\b', 'dữ liệu'),
    (r'\bDừ\s+liệu\b', 'Dữ liệu'),
    (r'\bmô\s+phòng\b', 'mô phỏng'),
    (r'\bbáng\s+cách\b', 'bằng cách'),
    (r'\bmính\s+họạ\b', 'minh họa'),
    (r'\bđày\s+mô\s+tả\b', 'đây mô tả'),
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
    (r'\bXoa\s+hai\s+dầu\b', 'Xóa hai dấu'),
    (r'\bxoa\s+hai\s+dầu\b', 'xóa hai dấu'),
    (r'\bImager\b', 'Imagen'),
    (r'\bHãy\s+xoa\s+bớt\b', 'Hãy xóa bớt'),
    (r'\bnhân\s+tổ\s+hợp\s+phím\b', 'nhấn tổ hợp phím'),
    (r'\btext-lo-image\b', 'text-to-image'),
    (r'\bimage-lo-image\b', 'image-to-image'),
    (r'\bchi\s+sử\s+dụng\b', 'chỉ sử dụng'),
    (r'\bành\s+gốc\b', 'ảnh gốc'),
    (r'\btiếng\s+ổn\b', 'tiếng ồn'),
    (r'\bphù\s+định\b', 'phủ định'),
    (r'\btừ\s+khoa\b', 'từ khóa'),
    (r'\bkịch\s+bàn\b', 'kịch bản'),
    (r'\bchuyên\s+động\b', 'chuyển động'),
    (r'\bchât\s+lượng\b', 'chất lượng'),
    (r'\bkíp\s+thời\b', 'kịp thời'),
    (r'\bchí\s+phí\b', 'chi phí'),
    (r'\bchùng\s+ta\b', 'chúng ta'),
    (r'\bmáy\s+tinh\b', 'máy tính'),
    (r'\bthị\s+giác\s+máy\s+tinh\b', 'thị giác máy tính'),
    (r'\bxử\s+lI\b', 'xử lí'),
    (r'\bxử\s+li\b', 'xử lí'),
    (r'\bhợp\s+li\b', 'hợp lí'),
    (r'\bnguyên\s+li\b', 'nguyên lí'),
    (r'\bquản\s+li\b', 'quản lí'),
    (r'\bchu\s+ki\b', 'chu kì'),
    (r'\bđịnh\s+ki\b', 'định kì'),
    (r'\bđăng\s+ki\b', 'đăng kí'),
    (r'\bbất\s+ki\b', 'bất kì'),
    (r'\btiêu\s+chuân\b', 'tiêu chuẩn'),
    (r'\bchính\s+xac\b', 'chính xác'),
    (r'\bphát\s+triến\b', 'phát triển'),
    (r'\btống\s+quát\b', 'tổng quát'),
    (r'\btư\s+động\b', 'tự động'),
    (r'\blự\s+động\b', 'tự động'),
    (r'\btư\s+nhiên\b', 'tự nhiên'),
    (r'\bhọc\s+tâp\b', 'học tập'),
    (r'\bluyện\s+tâp\b', 'luyện tập'),
    (r'\bluyên\s+tập\b', 'luyện tập'),
    (r'\bvận\s+dung\b', 'vận dụng'),
    (r'\bvân\s+dụng\b', 'vận dụng')
]

for b in ["lop-11", "lop-10", "lop-12"]:
    lp = DATA_DIR / f"lessons-{b}.json"
    content = lp.read_text(encoding="utf-8")
    for pat, repl in TONE_PAIRS:
        content = re.sub(pat, repl, content)
    lp.write_text(content, encoding="utf-8")
    
    html_dir = LESSONS_DIR / b
    if html_dir.exists():
        for f in html_dir.glob("*.html"):
            c = f.read_text(encoding="utf-8")
            for pat, repl in TONE_PAIRS:
                c = re.sub(pat, repl, c)
            f.write_text(c, encoding="utf-8")

bp = DATA_DIR / "books.json"
bc = bp.read_text(encoding="utf-8")
for pat, repl in TONE_PAIRS:
    bc = re.sub(pat, repl, bc)
bp.write_text(bc, encoding="utf-8")

from master_deep_fix import rebuild_search_indexes
rebuild_search_indexes()
print("Fixed all tone pairs across all files!")
