import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
plain_dir = ROOT / "scripts" / "lop11_plain"

files = sorted(plain_dir.glob("*.txt"))

# Check for specific words that might appear with typos
words_to_check = [
    'khong', 'khổng', 'trong', 'trọng', 'nhiều', 'it', 'ít', 'được', 'người', 'dùng', 'hoc', 'học',
    'sinh', 'giáo', 'viên', 'thầy', 'cô', 'bài', 'toán', 'văn', 'bản', 'mô', 'hình', 'dữ', 'liệu',
    'thông', 'tin', 'yêu', 'cầu', 'trả', 'lời', 'kết', 'quả', 'thực', 'hiện', 'nâng', 'cao', 'cơ', 'bản',
    'chỉ', 'thị', 'ngữ', 'cảnh', 'ví', 'dụ', 'định', 'dạng', 'độ', 'dài', 'bước', 'giải', 'thích',
    'tóm', 'tắt', 'hỏi', 'đáp', 'lỗi', 'đúng', 'sai', 'tự', 'nhiên', 'nhân', 'tạo', 'mạng', 'nơ-ron',
    'phân', 'loại', 'cụm', 'thuật', 'đạo', 'đức', 'pháp', 'luật', 'văn', 'hóa', 'sáng', 'tạo', 'nội', 'dung',
    'lập', 'trình', 'mã', 'lệnh', 'ảnh', 'video', 'dự', 'án', 'báo', 'cáo'
]

# Let's search for unaccented or mal-accented forms of these words in Vietnamese sentences
bad_variants = [
    (r'\bnguòn\b', 'nguồn'),
    (r'\bbàn\s+đồ\b', 'bản đồ'),
    (r'\bbàn\s+phím\b', 'bàn phím'), # this is correct!
    (r'\bban\s+phím\b', 'bàn phím'),
    (r'\bbàn\s+quyền\b', 'bản quyền'),
    (r'\bbàng\s+cách\b', 'bằng cách'),
    (r'\bkhá\s+năng\b', 'khả năng'),
    (r'\bphán\s+ánh\b', 'phản ánh'),
    (r'\bquản\s+trọng\b', 'quan trọng'),
    (r'\bliên\s+quản\b', 'liên quan'),
    (r'\btổng\s+quản\b', 'tổng quan'),
    (r'\btổng\s+hợp\b', 'tổng hợp'),
    (r'\btống\s+hợp\b', 'tổng hợp'),
    (r'\bhiệu\s+quà\b', 'hiệu quả'),
    (r'\bhậu\s+quà\b', 'hậu quả'),
    (r'\bkết\s+quà\b', 'kết quả'),
    (r'\bchinh\s+xác\b', 'chính xác'),
    (r'\bđòn\s+giản\b', 'đơn giản'),
    (r'\bmáy\s+tinh\b', 'máy tính'),
    (r'\btinh\s+toán\b', 'tính toán'),
    (r'\bnguyên\s+tác\b', 'nguyên tắc'),
    (r'\bđao\s+đức\b', 'đạo đức'),
    (r'\bkĩ\s+thuât\b', 'kĩ thuật'),
    (r'\btư\s+động\b', 'tự động'),
    (r'\bxử\s+li\b', 'xử lí'),
    (r'\bhợp\s+li\b', 'hợp lí'),
    (r'\bnghỉa\b', 'nghĩa'),
    (r'\bý\s+nghỉa\b', 'ý nghĩa'),
    (r'\bý\s+nghia\b', 'ý nghĩa'),
    (r'\bý\s+nghiã\b', 'ý nghĩa'),
    (r'\bkết\s+nôi\b', 'kết nối'),
    (r'\bnối\s+tiếp\b', 'nối tiếp'),
    (r'\bcung\s+cáp\b', 'cung cấp'),
    (r'\btrách\s+nhiêm\b', 'trách nhiệm'),
    (r'\bphát\s+triến\b', 'phát triển'),
    (r'\bcà\s+lớp\b', 'cả lớp'),
    (r'\bchuối\b', 'chuỗi'),
    (r'\bkhóa\b', 'khóa'),
    (r'\bkhoa\s*:\b', 'khóa:'),
    (r'\bphù\s+định\b', 'phủ định'),
    (r'\blàn\b', 'lần'),
    (r'\bvăn\s+bàn\b', 'văn bản'),
    (r'\bkịch\s+bàn\b', 'kịch bản'),
    (r'\bcơ\s+bàn\b', 'cơ bản'),
    (r'\bkhống\s+lồ\b', 'khổng lồ'),
    (r'\bkhổng\s+lồ\b', 'khổng lồ'),
    (r'\bchí\s+phí\b', 'chi phí'),
    (r'\bchi\s+phí\b', 'chi phí'),
    (r'\bphương\s+trinh\b', 'phương trình'),
    (r'\bchương\s+trinh\b', 'chương trình'),
    (r'\btiêu\s+chi\b', 'tiêu chí'),
    (r'\bgiá\s+sử\b', 'giả sử'),
    (r'\bđoan\b', 'đoạn'),
    (r'\btôm\b', 'tóm'),
    (r'\bhòi\b', 'hỏi'),
    (r'\bthém\b', 'thêm'),
    (r'\bcành\b', 'cảnh'),
    (r'\bbải\b', 'bài'),
    (r'\bgiài\b', 'giải'),
    (r'\bmỏ\b', 'mô'),
    (r'\bmò\b', 'mô'),
    (r'\bsô\b', 'số'),
    (r'\blăn\b', 'lần'),
    (r'\bgáp\b', 'gấp'),
    (r'\blạp\b', 'tạp'),
    (r'\bcàn\b', 'cần'),
    (r'\bthào\b', 'thảo'),
    (r'\bgiái\b', 'giải'),
    (r'\bđòng\b', 'đồng'),
    (r'\bhò\b', 'hồ')
]

for f in files:
    if f.name == "all_lop11.txt":
        continue
    content = f.read_text(encoding="utf-8")
    lines = content.split('\n')
    for l_idx, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("==="):
            continue
        for pat, repl in bad_variants:
            m = re.findall(pat, line_clean, re.IGNORECASE)
            if m:
                print(f"[{f.stem}:{l_idx+1}] Matched {pat} -> {repl}: {line_clean[:90]}")
