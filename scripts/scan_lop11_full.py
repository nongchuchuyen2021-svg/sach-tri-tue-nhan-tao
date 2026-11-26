import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

data = json.load(open(ROOT / 'data/lessons-lop-11.json', encoding='utf-8'))
for les in data:
    lines = re.split(r'</?(?:p|li|h[1-6]|div|tr|td|th)[^>]*>', les.get('html', ''))
    for i, l in enumerate(lines):
        c = re.sub(r'<[^>]+>', ' ', l).strip()
        # Find suspicious accents or words
        matches = re.findall(r'\b(vi dụ|vi du|vi dự|bải|giài|mỏ hình|mò hình|cầu sau|thém|cành|đòng|hò|chúngta|từ1|căn chỉnh|chằng|đinh|lập trung|xừa|đủ/sai|đù/sai|bàn|bán|co |trinh|gáo|giảo|đảu|càu|thể nào|lưa chọn|giơ|chuân|nghệ thuât|pháp luât|dừ liệu|nghỉa|học bồng|nọữ|nghiĩa|chíp|chịp|chép|chép|lựa chọn|tôm tắt|tóm tắt|vắn bản|mục liêu|bất ki|mổi|lổi|chử)\b', c, re.IGNORECASE)
        if matches:
            print(f"[{les['id']}:{i}] Found {matches}: ...{c[:90]}...")
