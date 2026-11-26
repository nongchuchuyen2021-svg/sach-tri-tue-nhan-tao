import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Collect text
all_text = ""
book_texts = {}

for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    bt = []
    for les in data:
        html = les.get("html", "")
        # strip html tags
        text = re.sub(r"<[^>]+>", " ", html)
        bt.append(text)
    book_texts[b] = " ".join(bt)

full_corpus = " ".join(book_texts.values())

# Common suspicious words / patterns
suspicious_patterns = [
    r"\b[a-zA-Zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]*[0-9]+[a-zA-Zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]+\b",
    r"\b[a-zA-Zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]+[0-9]+[a-zA-Zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]*\b",
]

# Check word tokens
words = re.findall(r'[a-zA-Zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]+', full_corpus)
word_counts = Counter(w.lower() for w in words)

print("Total words:", len(words))
print("Unique words:", len(word_counts))

# Known bad word checks
known_bad = [
    "quà", "tinh", "chinh", "càu", "hói", "trà", "cài", "hảy", "phài", "ngử", "cánh", "khoá",
    "dử", "xừ", "hê", "thuât", "nôi", "giao diên", "bài tạp", "thục", "vl", "v1", "g1", "lư",
    "thô", "lạo", "củ", "đồi", "gi", "tio", "khác", "nhớ", "hơi", "họp", "chử", "mổi", "lổi"
]

print("\n--- Testing known suspicious candidates in context ---")
for bad in ["quà", "tinh", "chinh", "càu", "hói", "trà", "cài", "hảy", "phài", "ngử", "cánh", "khoá", "gi", "tio", "đồi", "lạo"]:
    for b in ["lop-10", "lop-11", "lop-12"]:
        data = json.load(open(ROOT / "data" / f"lessons-{b}.json", encoding="utf-8"))
        for les in data:
            html = les.get("html", "")
            text = re.sub(r"<[^>]+>", " ", html)
            for m in re.finditer(rf"\b{bad}\b", text, re.IGNORECASE):
                s = max(0, m.start() - 30)
                e = min(len(text), m.end() + 30)
                snippet = text[s:e].replace('\n', ' ')
                print(f"[{b} - {les['id']}] '{m.group(0)}': ...{snippet}...")
