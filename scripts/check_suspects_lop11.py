import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
plain_dir = ROOT / "scripts" / "lop11_plain"

# Scan for words with unusual vowel accents or common OCR failures
suspicious_patterns = [
    r'\b[a-zA-Zà-ỹÀ-Ỹ]*[áàảãạâấầẩẫậăắằẳẵặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ][a-zA-Zà-ỹÀ-Ỹ]*',
]

# Let's inspect every file and print words that have known misspellings
ALL_SUSPECTS = [
    'chuối tư duy', 'phương trinh', 'theo A:', 'Nhờ đỏ', 'khoa :', 'self-altention',
    'Tranformer', 'dứ liệu', 'Dừ liệu', 'mô phòng', 'báng cách', 'mính họạ', 'đày mô tả',
    'mang nơ-ron', 'thầnCác', 'tiêp nhận', 'xử li', 'Tin hiệu đầu', 'tiên tiền',
    'Càm xúc', 'Giài tri', 'chia khoa', 'mặt phầng', 'hang chục', 'lắn át', 'tât cả',
    'tiêu chi', 'tương đông', 'vệ chung', 'hinh dạng', 'điểm nhiều', 'thi cho rằng',
    'cụm lá', 'T7 lĐ', 'tưoơng lác', 'ti cong', 'Khởí động', 'đạo dúr', 'vẫn hóa',
    'bc hai', 'câu hòi', 'Xoa hai dầu', 'Vieicure', 'Imager', 'Hãy xoa bớt', 'nhân tổ hợp',
    'text-lo-image', 'image-lo-image', 'chi sử dụng', 'ành gốc', 'tiếng ổn', 'con lác dom',
    'las bäng', 'cia rgyh', 'sảt kiêm', 'nguei dung', 'möt hoặc', 'LUM sẽ trêm',
    'chuyển đặng', 'ảnh tinin', 'Welcame', 'Thanh thây', 'không khi', 'khi hậu',
    'tim hiêu', 'vân đề', 'hiêu biết', 'báo cảo', 'bảng hòi', 'uy tin', 'Cống thông tin',
    'đầy đù', 'tim ra', 'tưy chọn', 'lưng bước', 'chuông đòng'
]

files = sorted(plain_dir.glob("*.txt"))
found_count = 0
for f in files:
    if f.name == "all_lop11.txt":
        continue
    content = f.read_text(encoding="utf-8")
    for s in ALL_SUSPECTS:
        if s.lower() in content.lower():
            found_count += 1
            print(f"[{f.stem}] Found suspect: '{s}'")

print(f"Total suspects found across Lop 11: {found_count}")
