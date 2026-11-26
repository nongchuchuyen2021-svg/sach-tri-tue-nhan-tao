import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Let's inspect all words across the 3 books that might have OCR tone errors or typos
books = ["lop-10", "lop-11", "lop-12"]

for b in books:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        clean = re.sub(r"<[^>]+>", " ", html)
        
        # Look for suspicious substrings or patterns
        suspicious = []
        
        # 1. OCR garbled patterns
        for m in re.finditer(r"\b\w*[\d]+\w*\b", clean):
            token = m.group(0)
            # exclude valid terms like 2D, 3D, GPT-4, 4o, 10, 11, 12, etc.
            if not re.match(r"^(GPT-?\d.*|Claude-?\d.*|\d+D|\d+(st|nd|rd|th)?|\d+(px|rem|em|%|k|M|B|G|fps|s|ms|h|min)?|\d+([.,]\d+)?)$", token, re.IGNORECASE):
                # check if contains vietnamese letters with numbers inside
                if re.search(r"[a-zA-Zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", token) and re.search(r"\d", token):
                    suspicious.append(("number_in_word", token, m.start()))

        # 2. Known tone inversions and OCR typos
        # We can search for known wrong n-grams
        bad_words = [
            r"\bhiều\b", r"\bđùng\b", r"\bxày ra\b", r"\bchia sẽ\b", r"\bđàm bào\b",
            r"\bbào vệ\b", r"\bbáo vệ\b", r"\bcá nhãn\b", r"\bmội trường\b", r"\bKhời động\b",
            r"\bkhời động\b", r"\bthay đồi\b", r"\bkết quà\b", r"\bKết quà\b", r"\bhiệu quà\b",
            r"\bchinh xác\b", r"\bChinh xác\b", r"\bthiếu tinh\b", r"\btinh huống\b", r"\bTinh huống\b",
            r"\btinh huồng\b", r"\btinh trạng\b", r"\bđồng tinh\b", r"\btinh lãi\b", r"\bTinh giá trị\b",
            r"\bngữ cánh\b", r"\bngử cảnh\b", r"\btừ khoá\b", r"\bTừ khoá\b", r"\bcuối khoá\b",
            r"\bcàu hỏi\b", r"\bcàu trả lời\b", r"\byêu càu\b", r"\bcâu hói\b", r"\bhói gì\b",
            r"\bhói của\b", r"\btrà lời\b", r"\bTrà lời\b", r"\bcài tiến\b", r"\bCài tiến\b",
            r"\bphài\b", r"\bhảy\b", r"\bHảy\b", r"\blàm gi\b", r"\blà gi\b", r"\bcó gi\b",
            r"\bmục đích gi\b", r"\bhậu quả gi\b", r"\bkĩ năng gi\b", r"\bkhó khăn gi\b",
            r"\bthay đồi\b", r"\bKẻ tên\b", r"\bbái viết\b", r"\bhãng quý\b", r"\bGia sử\b",
            r"\bvé sán phẩm\b", r"\bsán phẩm\b", r"\bkhác hàng\b", r"\bKhuyến mãt\b",
            r"\bvl dụ\b", r"\bv1 dụ\b", r"\bvi dụ\b", r"\bphản hỏi\b", r"\bnhớ vậy\b",
            r"\bkhông chi\b", r"\btio_kiem\b", r"\blạo sinh\b", r"\bthô hệ\b"
        ]
        
        for bw in bad_words:
            for m in re.finditer(bw, clean, re.IGNORECASE):
                suspicious.append(("bad_ngram", m.group(0), m.start()))

        if suspicious:
            print(f"=== [{b} - {les['id']}] ===")
            for stype, word, pos in suspicious[:10]: # show up to 10
                ctx = clean[max(0, pos-25):min(len(clean), pos+len(word)+25)].replace('\n', ' ')
                print(f"  [{stype}] '{word}' -> ...{ctx}...")
