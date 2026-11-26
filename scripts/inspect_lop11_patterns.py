import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / 'data/lessons-lop-11.json', encoding='utf-8') as f:
    lessons = json.load(f)

print(f"Loaded {len(lessons)} lessons for lop-11")

# List of regex patterns for common OCR errors in Vietnamese
patterns = [
    r'\bchúngta\b',
    r'\bđòng\b',
    r'\btừ1\b',
    r'\bvi dụ\b',
    r'\bVi dụ\b',
    r'\bVI dụ\b',
    r'\bvi dự\b',
    r'\bVi dự\b',
    r'\bco bản\b',
    r'\bco bán\b',
    r'\bcơ bán\b',
    r'\bco bàn\b',
    r'\bprompt co\b',
    r'\bnàng cao\b',
    r'\bgiài\b',
    r'\bbải\b',
    r'\bmỏ hình\b',
    r'\bmò hình\b',
    r'\bmỏ hinh\b',
    r'\bcầu sau\b',
    r'\bthém\b',
    r'\bcành\b',
    r'\btôm tắt\b',
    r'\btóm tát\b',
    r'\bHây\b',
    r'\bHấy\b',
    r'\bthịch\b',
    r'\bvăn bán\b',
    r'\bphù định\b',
    r'\btừ khoa\b',
    r'\bbối cành\b',
    r'\bmỗi làn\b',
    r'\bkịch bàn\b',
    r'\bchuyên động\b',
    r'\bchât lượng\b',
    r'\bban bàn tán\b',
    r'\bvê khói\b',
    r'\bbạn bé\b',
    r'\btim kiếm\b',
    r'\bkiêm chứng\b',
    r'\bbố sung\b',
    r'\bsô liệu\b',
    r'\bphai đọc\b',
    r'\bphần tích\b',
    r'\bmô tá\b',
    r'\bmảu\b',
    r'\bHoa sĩ\b',
    r'\bbàn phim\b',
    r'\bchỉ tiết\b',
    r'\bphần từ\b',
    r'\bgáp\b',
    r'\blăn só\b',
    r'\bđâu vào\b',
    r'\bphức lạp\b',
    r'\bcàn độ\b',
    r'\bChuối tư duy\b',
    r'\bTôc độ\b',
    r'\bthurc hiện\b',
    r'\bCẦU TRÚC\b',
    r'\bGiá sử\b',
    r'\bhằng quý\b',
    r'\bcà vốn\b',
    r'\bLời giài\b',
    r'\bsoạn thào\b',
    r'\btheo A:\b',
    r'x\?\s*\+\s*4x',
    r'\bXác đinh\b',
    r'\bTinh 4\b',
    r'\bđoan thơ\b',
    r'\bđoan văn\b',
    r'\bmục đich\b',
    r'\bgiái bài\b',
    r'\bHòi sau\b',
    r'\bLàm thể nào\b',
    r'\bchủ ý\b',
    r'\bvắn bản\b',
    r'\bdừ liệu\b',
    r'\bmục liêu\b',
    r'\bbản nghị luàn\b',
    r'\bý tường\b',
    r'\btừng tiêu chi\b',
    r'\bKét quả\b',
    r'\bbất ki\b',
    r'\bhọc bồng\b',
    r'\btrài qua\b',
    r'\btạo ành\b',
    r'\bSeli-Attention\b',
    r'\bsách vờ\b',
    r'\btuần theo\b',
    r'\bMáy tinh\b',
    r'\bchịp\b',
    r'\bhọc cùng cố\b',
    r'\bthi LLM\b',
    r'\bCâu hòi\b',
    r'\btinh, thành\b',
    r'\bnhầm tài liệu\b'
]

compiled = [re.compile(p, re.IGNORECASE) for p in patterns]

matches_found = []
for les_idx, les in enumerate(lessons):
    les_id = les['id']
    html = les['html']
    # split into lines or tags
    pieces = re.split(r'</?(?:p|li|h[1-6]|div|tr|td|th|blockquote)[^>]*>', html)
    for p_idx, piece in enumerate(pieces):
        clean_text = re.sub(r'<[^>]+>', ' ', piece).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        if not clean_text:
            continue
        for cp in compiled:
            m = cp.search(clean_text)
            if m:
                matches_found.append({
                    'lesson': les_id,
                    'piece_idx': p_idx,
                    'match': m.group(0),
                    'text': clean_text
                })

print(f"Total matching error occurrences found: {len(matches_found)}")
for it in matches_found[:40]:
    print(f"[{it['lesson']}] '{it['match']}': {it['text'][:100]}...")
