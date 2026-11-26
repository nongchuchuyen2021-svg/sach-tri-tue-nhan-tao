import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Let's inspect the exact lines where severe OCR corruptions occurred
files_to_check = [
    ("lop-10", "bai-4-du-lieu-huan-luyen"),
    ("lop-10", "bai-8-hieu-dung-ve-ai-tao-sinh-thien-vi-hieu-lam-va-tac-hai-voi-con-nguoi"),
    ("lop-10", "bai-10-ai-va-nghe-nghiep"),
    ("lop-10", "bai-12-bai-tap-du-an"),
    ("lop-10", "muc-luc"),
    ("lop-11", "muc-luc"),
    ("lop-11", "bai-1-ki-thuat-viet-prompt-co-ban-va-nang-cao"),
    ("lop-11", "bai-4-gioi-thieu-ve-rag"),
    ("lop-11", "bai-6-phan-loai-va-phan-cum-du-lieu"),
    ("lop-11", "bai-7-dao-duc-phap-luat-va-van-hoa-trong-su-dung-mo-hinh-ngon-ngu-lon"),
    ("lop-11", "bai-9-mo-hinh-ngon-ngu-lon-ho-tro-hoc-tap"),
    ("lop-11", "bai-11-tao-va-sua-hinh-anh-bang-mo-hinh-ngon-ngu-lon"),
    ("lop-11", "bang-giai-thich-thuat-ngu"),
    ("lop-12", "bai-1-gioi-thieu-ve-ai-agents"),
    ("lop-12", "bai-2-cau-truc-ai-agent-don-gian"),
    ("lop-12", "bai-5-khai-thac-thu-vien-nguon-mo-llm"),
    ("lop-12", "bai-6-tac-dong-cua-ai-den-doi-song-con-nguoi"),
    ("lop-12", "bai-7-ai-mo-ra-co-hoi-va-thach-thuc-cho-cac-nganh-nghe"),
    ("lop-12", "bai-8-quyen-con-nguoi-trong-ki-nguyen-ai"),
    ("lop-12", "bai-10-nguyen-li-co-ban-cua-hoc-may"),
    ("lop-12", "bai-11-toi-uu-hoa-mo-hinh"),
    ("lop-12", "bai-13-xay-dung-san-pham"),
    ("lop-12", "bai-14-hoan-chinh-san-pham"),
    ("lop-12", "bai-15-trinh-bay-ket-qua-du-an"),
]

for b, les_id in files_to_check:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        if les['id'] == les_id:
            html = les.get("html", "")
            print(f"=== {b} / {les_id} ===")
            # find snippets with weird patterns:
            # find words like bón, ổm, biêu, bèn, bèo, aì, ahiển, arư, etc.
            matches = re.finditer(r"[^\n.!?]{0,40}(bị ổm|Buốn|đểgian|đượcdùng|đựa trên|đừa ra|Đừng dưa|Đậy là|cung đỉnh|nhóm nào đổ|đắt nước|đại Aần|Bàl|Bòl|Bâi|BÁNG GIẢI|tiêu biếu|biêu điẻn|buợc hành|tiều vận bân|bât kì|bèn cung cấp|đảm bèo|lài liệu bén|bó cục|bón người|xoa bót|bô sung|cục bú|Tẹo một búc|cúc tác giả|củng đổng|chuyển đốt|Hat ượng|Ạl tạo|CHỦ ĐẺ|Ahiển chùng|Arư điêm|sử Aì|vià Aí|tìm kiêm thông tin aản|bàt luàn|vito erito|kho 122|mên Ngữ văn|sán phẩm|Khuyến mãt)[^\n.!?]{0,40}", html, re.IGNORECASE)
            for m in matches:
                print("   Snippet:", m.group(0).strip())
