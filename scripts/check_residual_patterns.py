import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Let's inspect all files: lessons-lop-10, 11, 12 and books.json
all_text = ""
for b in ["10", "11", "12"]:
    all_text += (ROOT / "data" / f"lessons-lop-{b}.json").read_text(encoding="utf-8") + " "
all_text += (ROOT / "data" / "books.json").read_text(encoding="utf-8")

# Let's search for all known OCR letter confusions in Vietnamese:
checks = [
    "ảnhh", "bạng", "llên", "hoặt", "đăn", "Khới", "ngọi", "lưyng", "hoậc", "trỏi", "bảl", "câ nhân",
    "đải", "oông", "nên/khỏng", "Sừ", "ănh", "rèng", "lrách", "hồm", "cề trế", "cárt", "niển", "roir",
    "tirin", "Niếu", "chiuyện", "dàu", "Bude", "strj", "rtuyện", "bbi", "TUÊ", "co bán", "chương trinh",
    "nàng cao", "soan", "căn chỉnh", "Tỉnh chỉnh", "nghin", "dựa trèn", "mộn", "loán", "gản nhãn",
    "tưong", "bx", "lươi", "biéu", "muo", "giup", "sirh", "diém", "2f", "cụ/Agent", "THL", "LOC",
    "Sưno", "PHẨ", "thasing", "muán", "Dsy", "mot", "búc", "zadn", "Gerini", "Drep", "Reaserch",
    "sạu", "chalbot", "huắn", "LÚYỆN", "Xóá", "AIsA", "chên", "Vĩ dụ", "nhồm", "lệu", "Lích",
    "bạnnam", "fình", "yẽu", "Colabl", "Coladl", "ChaGPT", "hồm", "chuyệr", "kháchhhh", "trom a",
    "Lamalndex", "lón", "đữ", "sừa", "thoat", "điêm", "triên", "LUAN", "Góm", "triến", "huán",
    "prompi", "prompl", "tuê", "càa", "kiem", "tưong", "Gisy", "Giay", "Generato", "AIl", "khổi",
    "lệp", "vól", "vớ1", "xêp", "xừa", "XữIi", "đượs", "đãt", "đù/sai", "Đđ", "Ií", "ghành", "taàn",
    "kiém", "nguờn", "tỉn", "trớc", "miội", "háp", "kốt", "THẬC", "nhự", "tương tht", "Mội thoai",
    "Buot", "tốm t8t", "nọữ", "nghiĩa", "huồng", "Gúi", "hặn", "từy", "truór", "trạn", "phẩm7",
    "nguốn", "niện ray", "cuông", "Giất lượng", "đàm báo", "loạ độ", "luả", "Süa tuot", "Virgma",
    "toại nủa", "đả lua chọn", "phù nộp vếi", "vào vộc", "đưa rả", "ý luơng", "Ál", "ánput",
    "Thaught", "He Of glas", "finh vire", "Quý khuch", "Workfiows", "Warkflow"
]

found = []
for c in checks:
    count = all_text.count(c)
    if count > 0:
        found.append((c, count))

print(f"Total checked patterns found: {len(found)}")
for c, cnt in found:
    print(f"  '{c}': {cnt}")
