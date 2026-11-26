import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for grade, lid, word in [
    ("lop-10", "bai-4-du-lieu-huan-luyen", "Hóá"),
    ("lop-10", "bai-6-ai-tao-sinh-ho-tro-hoc-tap", "AI thể"),
    ("lop-10", "bai-9-cong-dan-so-trong-ki-nguyen-ai", "hóá"),
    ("lop-10", "bai-11-moi-truong-phat-trien-san-pham-ai", "bàng"),
    ("lop-10", "bai-12-bai-tap-du-an", "hóá"),
    ("lop-11", "bai-1-ki-thuat-viet-prompt-co-ban-va-nang-cao", "bàng"),
    ("lop-11", "bai-5-mang-no-ron-nhan-tao", "hóá"),
    ("lop-11", "bai-6-phan-loai-va-phan-cum-du-lieu", "bàng"),
    ("lop-11", "bai-6-phan-loai-va-phan-cum-du-lieu", "hóá"),
    ("lop-11", "bai-7-dao-duc-phap-luat-va-van-hoa-trong-su-dung-mo-hinh-ngon-ngu-lon", "hóá"),
    ("lop-11", "bai-12-tao-video-bang-mo-hinh-ngon-ngu-lon", "lạo"),
    ("lop-12", "bai-4-thu-vien-nguon-mo-llm", "hóá"),
    ("lop-12", "bai-9-phat-trien-ai-co-trach-nhiem", "bàng"),
]:
    p = ROOT / "data" / f"lessons-{grade}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        if les["id"] == lid:
            html = les.get("html", "")
            for m in re.finditer(re.escape(word), html, re.I):
                start = max(0, m.start() - 35)
                end = min(len(html), m.end() + 35)
                print(f"[{grade} - {lid}] '{word}' -> ...{html[start:end]}...")
