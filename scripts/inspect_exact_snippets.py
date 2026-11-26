import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

checks = [
    ("lop-11", "bai-1-ki-thuat-viet-prompt-co-ban-va-nang-cao", ["vl dụ", "1ư"]),
    ("lop-12", "bai-1-gioi-thieu-ve-ai-agents", ["g8p", "t8t"]),
    ("lop-12", "bai-2-cau-truc-ai-agent-don-gian", ["4o", "phẩm7", "e0"]),
    ("lop-12", "bai-5-khai-thac-thu-vien-nguon-mo-llm", ["G1á", "cae thoc", "Quoryengine7ool", "10ggtmg"]),
    ("lop-12", "bai-7-ai-mo-ra-co-hoi-va-thach-thuc-cho-cac-nganh-nghe", ["Ah0d", "V2"]),
    ("lop-12", "bai-10-nguyen-li-co-ban-cua-hoc-may", ["з0l", "E3", "4P"]),
    ("lop-12", "bai-13-xay-dung-san-pham", ["placeho1der", "d6", "33R"]),
    ("lop-10", "bai-6-ai-tao-sinh-ho-tro-hoc-tap", ["4I"]),
    ("lop-10", "bai-9-cong-dan-so-trong-ki-nguyen-ai", ["A1"]),
    ("lop-10", "bai-10-ai-va-nghe-nghiep", ["A1"]),
    ("lop-10", "bai-12-bai-tap-du-an", ["j4", "k7", "T4n"]),
    ("lop-11", "bai-3-mo-hinh-ngon-ngu-lon-va-han-che-cua-no", ["F0"]),
    ("lop-11", "bai-4-gioi-thieu-ve-rag", ["O7"]),
    ("lop-11", "bai-6-phan-loai-va-phan-cum-du-lieu", ["T7"]),
    ("lop-11", "bai-8-gia-tri-con-nguoi-trong-ki-nguyen-ai", ["g1"]),
]

for grade, lid, words in checks:
    p = ROOT / "data" / f"lessons-{grade}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        if les["id"] == lid:
            html = les.get("html", "")
            clean = re.sub(r"<[^>]+>", " ", html)
            for w in words:
                for m in re.finditer(re.escape(w), clean):
                    start = max(0, m.start() - 35)
                    end = min(len(clean), m.end() + 35)
                    print(f"[{grade} - {lid}] '{w}' -> ...{clean[start:end].strip()}...")

