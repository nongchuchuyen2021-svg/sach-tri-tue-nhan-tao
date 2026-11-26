import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Load all 3 lessons files
files = {
    "lop-10": ROOT / "data" / "lessons-lop-10.json",
    "lop-11": ROOT / "data" / "lessons-lop-11.json",
    "lop-12": ROOT / "data" / "lessons-lop-12.json",
}

ocr_artifacts = Counter()
suspicious_words = Counter()

# Common words to look for patterns
patterns = [
    r"\b[a-zA-ZÀ-ỹ]*[!@#$%^&*\/][a-zA-ZÀ-ỹ]*\b", # words with symbols inside like A/, !í
    r"\b[A-Za-zÀ-ỹ]*[0-9]+[A-Za-zÀ-ỹ]+\b", # words with digits mixed like l0, b1
    r"\b(?:công củ|tao ra|lạo sinh|thô hệ|trợ !í|xử Ií|hộ thông|lương ứng|bạn bẻ|người thần|củng một|kết quá|thuận liện|trọng đó|đổi tượng|họp phim|phim Shift|họp thoại|sổ ta|lưu trứ|thực hiên|mó tả|Bải \d+|khả náng|hình ành|Ai thể|Ai thô|A/ lạo)\b",
]

for grade, p in files.items():
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        text = les.get("html", "")
        # Remove tags for word scanning
        text_clean = re.sub(r"<[^>]+>", " ", text)
        
        # Check specific known OCR errors
        for m in re.finditer(r"(A/\s*\w+|\w+\s*!í|\b[a-zA-ZÀ-ỹ]+[;\xad][a-zA-ZÀ-ỹ]+|\b\w+\s+(?:củ|tao|lạo|thô|Ií|hộ|bẻ|thần)\b)", text_clean):
            ocr_artifacts[m.group(0)] += 1
            
        for pat in patterns:
            for m in re.finditer(pat, text_clean, re.IGNORECASE):
                suspicious_words[m.group(0)] += 1

print("Top OCR artifacts found:")
for word, count in ocr_artifacts.most_common(40):
    print(f"  {word}: {count}")

print("\nTop suspicious words:")
for word, count in suspicious_words.most_common(40):
    print(f"  {word}: {count}")
