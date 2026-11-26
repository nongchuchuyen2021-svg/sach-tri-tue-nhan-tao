import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

books = ["lop-10", "lop-11", "lop-12"]

for b in books:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    print(f"\n==================== BOOK {b} ({len(data)} lessons/sections) ====================")
    
    for les in data:
        lid = les["id"]
        html = les.get("html", "")
        # Remove code blocks and script/style tags
        clean = re.sub(r"<code>.*?</code>", "", html, flags=re.DOTALL)
        clean = re.sub(r"<[^>]+>", " ", clean)
        clean = re.sub(r"https?://\S+", "", clean)
        
        # Find suspicious characters
        greek_semis = len(re.findall(r";", clean))
        soft_hyphens = len(re.findall(r"\xad", clean))
        exclamation_in_word = re.findall(r"\b\w*!\w*\b", clean)
        slash_in_word = [w for w in re.findall(r"\b\w+/\w+\b", clean) if not re.match(r"^(và/hoặc|đ/gói|VND/Lit|low/no|If/Else|A/B)$", w, re.I)]
        
        # Suspicious Vietnamese words
        # Words with tone mark on wrong vowel or missing tones
        odd_words = re.findall(r"\b(?:công củ|tao ra|lạo|thô hệ|trợ !í|xử Ií|hộ thông|lương ứng|bạn bẻ|người thần|củng một|kết quá|thuận liện|trọng đó|đổi tượng|họp phim|phim Shift|họp thoại|sổ ta|lưu trứ|thực hiên|mó tả|Bải \d+|khả náng|hình ành|Ai thể|Ai thô|A/ lạo|khia cạnh|thúc đầy|thừ nghiệm|hóá|vàng cug|Mf Workspace|Mr Workspare|vững chúc|mạnh khoe|nhiều lâm|nu cười|miaro|đam mề|chù để|cẩm sách|dúng ý|hoàn chính|khiểm tra|bắt kì|chúc mùng|bàng|Bàng|tuyệt đối|đặc biệt)\b", clean, re.I)
        
        if greek_semis > 0 or soft_hyphens > 0 or exclamation_in_word or odd_words:
            print(f"[{lid}] {les.get('title')}:")
            if greek_semis > 0:
                print(f"   Greek semicolons (;): {greek_semis}")
            if soft_hyphens > 0:
                print(f"   Soft hyphens: {soft_hyphens}")
            if exclamation_in_word:
                print(f"   Exclamation in word: {exclamation_in_word}")
            if odd_words:
                print(f"   Suspicious words: {list(set(odd_words))[:10]}")
