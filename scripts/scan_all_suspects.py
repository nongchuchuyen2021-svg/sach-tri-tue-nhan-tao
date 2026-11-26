import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Let's inspect all tokens across all lessons
all_tokens = Counter()
token_contexts = {}

for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        clean = re.sub(r"<[^>]+>", " ", html)
        # extract words
        words = re.findall(r"[a-zA-Zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]+", clean)
        for w in words:
            wl = w.lower()
            all_tokens[wl] += 1
            if wl not in token_contexts:
                # find context
                idx = clean.lower().find(wl)
                if idx != -1:
                    token_contexts[wl] = (b, les['id'], clean[max(0, idx-20):min(len(clean), idx+len(wl)+20)].replace('\n', ' '))

# Check words with tones on rare or likely mistyped syllables
# List of syllables that are almost never real Vietnamese words in this textbook context:
suspect_syllables = [
    "quà", "hiều", "đùng", "càu", "hói", "trà", "cài", "hảy", "phài", "ngử", "cánh", "khoá",
    "dử", "xừ", "hê", "thuât", "nôi", "thục", "vl", "v1", "g1", "lư", "thô", "lạo", "củ", "đồi",
    "xày", "đàm", "bào", "báo", "nhãn", "mội", "khời", "hãng", "sán", "mãt", "nhớ", "hơi", "chử",
    "mổi", "lổi", "tinh", "chinh", "kẻ", "bái", "vé", "mên", "thiêu", "thiểu", "d0", "bậi", "lậm"
]

print("=== FOUND SUSPICIOUS SYLLABLES ===")
for s in suspect_syllables:
    if s in all_tokens:
        print(f"Word: '{s}' (count: {all_tokens[s]})")
        # print contexts across all occurrences
        for b in ["lop-10", "lop-11", "lop-12"]:
            data = json.load(open(ROOT / "data" / f"lessons-{b}.json", encoding="utf-8"))
            for les in data:
                html = les.get("html", "")
                clean = re.sub(r"<[^>]+>", " ", html)
                for m in re.finditer(rf"\b{s}\b", clean, re.IGNORECASE):
                    ctx = clean[max(0, m.start()-25):min(len(clean), m.end()+25)].replace('\n', ' ')
                    print(f"   [{b}/{les['id']}] '{m.group(0)}': ...{ctx}...")
